"""W5b V3 guard: EMA weights scored with the LIVE model's BN stats collapse.

Toy reproduction of the mechanism the W5b-S0 diagnosis found in
``r1_abl_curriculum_s42`` epoch 14 (``runs/phase6_build/steps/W5b-S0.diagnosis.md``):
a conv layer feeding a BatchNorm drifts quickly along a direction the BN cancels
(here: its weight scale grows each step, as the DCT-stream weights grew while
the band gates shrank). The live model is unaffected (BN renormalises; its
running stats track the live scale). The EMA lags in scale, so EMA weights
evaluated with the copied live running stats see a shifted, rescaled input to
the BN → near-constant outputs. With ``own_bn_stats=True`` the shadow's BN stats
come from its own forward and the EMA model stays healthy.

Stubs only: a 1-conv toy net, synthetic tensors, CPU, no trainer/CLI/run dir.
The step loop mirrors the trainer's order: live train forward → (stub) optimizer
step → ``ema.update`` → ``ema.observe_bn`` on the last ``window`` steps →
``ema.copy_buffers_from`` before eval.
"""
from __future__ import annotations

import torch
from torch import nn

from src.training.scheduler import ModelEMA


class _Toy(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv = nn.Conv2d(1, 4, 1, bias=False)
        self.bn = nn.BatchNorm2d(4)
        self.head = nn.Linear(4, 1)
        with torch.no_grad():
            self.conv.weight.copy_(torch.tensor([1.0, 0.5, 2.0, 1.5]).view(4, 1, 1, 1))
            self.head.weight.copy_(torch.tensor([[1.0, 1.0, 1.0, 1.0]]))
            self.head.bias.zero_()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = torch.relu(self.bn(self.conv(x)))
        return self.head(h.mean(dim=(2, 3))).squeeze(1)


def _batch(g: torch.Generator, n: int = 64) -> torch.Tensor:
    # Inputs with a large mean (μ/σ = 4) so a scale mismatch shifts the BN output.
    return 4.0 + torch.randn(n, 1, 6, 6, generator=g)


def _run(own_bn_stats: bool, steps: int = 120, window: int = 40) -> tuple[torch.Tensor, torch.Tensor]:
    """Return (ema_eval_logits, live_eval_logits) on a fixed probe batch."""
    torch.manual_seed(0)
    g = torch.Generator().manual_seed(0)
    live = _Toy()
    ema = ModelEMA(live, decay=0.95, own_bn_stats=own_bn_stats)
    for step in range(steps):
        x = _batch(g)
        live.train()
        live(x)  # updates the live BN running stats (the trainer's forward)
        with torch.no_grad():  # stub optimizer step: fast BN-cancelled scale drift
            live.conv.weight.mul_(1.04)
        ema.update(live)
        if own_bn_stats and step >= steps - window:
            ema.observe_bn(live, x)
    live.eval()
    ema.copy_buffers_from(live)
    probe = _batch(torch.Generator().manual_seed(123), 512)
    with torch.no_grad():
        return ema.module(probe), live(probe)


def _corr(a: torch.Tensor, b: torch.Tensor) -> float:
    a = a - a.mean()
    b = b - b.mean()
    return float((a * b).sum() / (a.norm() * b.norm() + 1e-12))


def _healthy(ema_out: torch.Tensor, live_out: torch.Tensor) -> bool:
    """EMA outputs track the live function: same spread and high correlation."""
    ratio = float(ema_out.std() / live_out.std())
    return 0.8 < ratio < 1.25 and _corr(ema_out, live_out) > 0.95


def test_flag_off_reproduces_the_collapse() -> None:
    ema_out, live_out = _run(own_bn_stats=False)
    # near-constant EMA outputs (the epoch-14 signature) vs a healthy live model
    assert float(ema_out.std()) < 0.5 * float(live_out.std())
    assert not _healthy(ema_out, live_out)


def test_flag_on_removes_the_collapse() -> None:
    ema_out, live_out = _run(own_bn_stats=True)
    assert _healthy(ema_out, live_out)


def test_flag_off_copy_is_the_original_verbatim_copy() -> None:
    """own_bn_stats=False: copy_buffers_from copies ALL buffers (original path)."""
    live = _Toy()
    ema = ModelEMA(live, decay=0.9)
    live.train()
    live(_batch(torch.Generator().manual_seed(1)))
    ema.copy_buffers_from(live)
    for (n, b_ema), (_, b_live) in zip(ema.module.named_buffers(), live.named_buffers()):
        assert torch.equal(b_ema, b_live), n
    try:
        ema.observe_bn(live, _batch(torch.Generator().manual_seed(2)))
    except RuntimeError:
        pass
    else:  # pragma: no cover
        raise AssertionError("observe_bn must refuse when own_bn_stats is off")


def test_flag_on_keeps_eval_layers_on_live_stats_and_params_untouched() -> None:
    """Layers the live model holds in eval (e.g. a frozen backbone) keep the live
    copied stats; observe_bn never changes parameters; the shadow ends in eval."""
    live = _Toy()
    ema = ModelEMA(live, decay=0.9, own_bn_stats=True)
    params_before = [p.clone() for p in ema.module.parameters()]
    live.train()
    live.bn.eval()  # the live model does not update this BN (frozen)
    x = _batch(torch.Generator().manual_seed(3))
    live.conv.weight.data.mul_(3.0)
    ema.observe_bn(live, x)
    assert not ema.module.training and not ema.module.bn.training
    for a, b in zip(params_before, ema.module.parameters()):
        assert torch.equal(a, b)
    live.bn.running_mean.add_(1.0)
    ema.copy_buffers_from(live)
    assert torch.equal(ema.module.bn.running_mean, live.bn.running_mean)


def test_flag_on_window_is_consumed_by_one_eval() -> None:
    """After one copy_buffers_from the next copy without observation is verbatim."""
    live = _Toy()
    ema = ModelEMA(live, decay=0.9, own_bn_stats=True)
    live.train()
    x = _batch(torch.Generator().manual_seed(4))
    live(x)
    ema.observe_bn(live, x)
    ema.copy_buffers_from(live)
    live(x)
    ema.copy_buffers_from(live)
    for (n, b_ema), (_, b_live) in zip(ema.module.named_buffers(), live.named_buffers()):
        assert torch.equal(b_ema, b_live), n


def test_old_state_dict_round_trips() -> None:
    """The shadow's state_dict keys are unchanged, so old checkpoints still load."""
    live = _Toy()
    old = ModelEMA(live, decay=0.9)
    new = ModelEMA(live, decay=0.9, own_bn_stats=True)
    assert list(old.state_dict()) == list(new.state_dict())
    new.load_state_dict(old.state_dict())


# ---------------------------------------------------------------------------
# Trainer wiring (real on-disk FF++ faces subset, CPU; same fixture style as
# test_trainer.py — no CLI, no run dir): the flag changes ONLY the EMA's BN stats.
# ---------------------------------------------------------------------------

import tempfile  # noqa: E402
from pathlib import Path  # noqa: E402

import pytest  # noqa: E402

_FACES_ROOT = Path("~/sdb/datasets/ff++/faces").expanduser()
_HAS_FACES = (_FACES_ROOT / "c23").is_dir() and (_FACES_ROOT / "c40").is_dir()


def _cafrl_trainer(own_bn_stats: bool):
    from src.config.load import load_config
    from src.training.trainer import Trainer
    from src.utils.seed import seed_everything

    seed_everything(42)
    cfg = load_config(None)
    object.__setattr__(cfg.data, "num_workers", 0)
    object.__setattr__(cfg.train, "phase_bounds", (1, 2))
    object.__setattr__(cfg.train, "ema_own_bn_stats", own_bn_stats)
    cfg.model.invariance_arm = "none"
    return Trainer(cfg, device="cpu", run_dir=tempfile.mkdtemp(), subset_fraction=0.006,
                   pretrained_backbone=False, max_epochs=3)


@pytest.mark.skipif(not _HAS_FACES, reason="FF++ faces (c23+c40) not on disk")
def test_trainer_flag_changes_only_ema_bn_stats() -> None:
    runs = {}
    for flag in (False, True):
        tr = _cafrl_trainer(flag)
        assert tr.ema.own_bn_stats is flag
        active, loss_w, frozen = tr.curriculum.on_epoch_start(2)  # Phase B: unfrozen
        tr.core.set_frozen(frozen)
        tr.sampler.set_active_levels(active)
        tr.sampler.set_epoch(2)
        tr.fwd.train()
        losses = []
        it = iter(tr.train_loader)
        for _ in range(3):
            tr._ema_bn_observe_now = flag  # what _train_one_epoch sets in the window
            losses.append(float(tr._train_step(next(it), loss_w, None)[0]["total"]))
        live_state = {k: v.clone() for k, v in tr.core.state_dict().items()}
        tr.ema.copy_buffers_from(tr.core)
        runs[flag] = (losses, live_state, {k: v.clone() for k, v in tr.ema.state_dict().items()})
    (l0, live0, ema0), (l1, live1, ema1) = runs[False], runs[True]
    assert l0 == l1  # CPU is deterministic; the training stream is untouched
    for k in live0:
        assert torch.equal(live0[k], live1[k]), k  # live params AND live buffers
    bn_keys = [k for k in ema0 if k.endswith(("running_mean", "running_var",
                                              "num_batches_tracked"))]
    for k in ema0:
        if k not in bn_keys:
            assert torch.equal(ema0[k], ema1[k]), k  # EMA params unchanged by the flag
    # flag off: EMA BN stats == live; flag on: the observed BN stats are the EMA's own
    assert all(torch.equal(ema0[k], live0[k]) for k in bn_keys)
    assert any(not torch.equal(ema1[k], live1[k]) for k in bn_keys if "running_var" in k)
