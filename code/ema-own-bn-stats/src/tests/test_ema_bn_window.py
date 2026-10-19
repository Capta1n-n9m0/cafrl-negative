"""W5b V3 guard (W5b-S0 fixer, verifier A MINOR 1 + 2): the trainer's EMA
BN-observation window and the fallback WARNING.

Stubs only (lesson W5-2): a ``Trainer`` built with ``__new__`` and just the
attributes ``_train_one_epoch`` reads, a list "loader" of dummy batches, a stub
``_train_step``. No model forward, no data, no CLI, no run dir.

The real ``_train_step`` calls ``_ema_observe_bn`` (→ ``ModelEMA.observe_bn``)
exactly when ``self._ema_bn_observe_now`` is True (trainer.py, after
``ema.update``; the wiring test in ``test_ema_own_bn_stats.py`` covers that
call). So the number of steps a stub sees with the flag True is the number of
``observe_bn`` calls in one epoch. Here the stub also routes the call through the
real ``_ema_observe_bn`` → a counting ``observe_bn``, so the count is literal.
"""
from __future__ import annotations

import logging
from types import SimpleNamespace

import pytest
import torch
from torch import nn

from src.training import trainer as trainer_mod
from src.training.scheduler import ModelEMA
from src.training.trainer import Trainer, _EMA_BN_WINDOW_STEPS, _LOSS_LOG_KEYS


class _CountingEMA:
    """Stand-in for ModelEMA: counts observe_bn calls (no forward)."""

    def __init__(self, own_bn_stats: bool) -> None:
        self.own_bn_stats = own_bn_stats
        self.n_observe = 0

    def observe_bn(self, model, images, **kw) -> None:  # noqa: ARG002
        if not self.own_bn_stats:
            raise RuntimeError("observe_bn requires own_bn_stats=True")
        self.n_observe += 1


def _stub_trainer(n_batches: int, own_bn_stats: bool, start_step: int = 0) -> Trainer:
    tr = Trainer.__new__(Trainer)
    tr.curriculum = SimpleNamespace(phase_bounds=(10, 25))
    tr.arm = "none"
    tr.hsic_scale = None
    tr.train_loader = [object()] * n_batches
    tr.start_step_in_epoch = start_step
    tr.ema = _CountingEMA(own_bn_stats)
    tr._ema_bn_observe_now = False
    tr.rank = 0
    tr.tb = None
    tr.step_log_detail = False
    tr.step_log_every = 50
    tr.global_step = 0
    tr.device = torch.device("cpu")
    tr.core = nn.Identity()
    tr.flags_seen = []

    def _stub_train_step(batch, loss_w, disc_w, want_raw_hsic_y=False):  # noqa: ARG001
        tr.flags_seen.append(tr._ema_bn_observe_now)
        if tr._ema_bn_observe_now:  # the real _train_step's condition, verbatim
            tr._ema_observe_bn(torch.zeros(1), {}, "cpu", False)
        tr.global_step += 1
        return {k: torch.tensor(0.0) for k in _LOSS_LOG_KEYS}, None, None

    tr._train_step = _stub_train_step
    return tr


@pytest.mark.parametrize("n_batches", [1, 50, _EMA_BN_WINDOW_STEPS,
                                       _EMA_BN_WINDOW_STEPS + 1, 6583 // 10, 1000])
def test_window_counts_min_200_len(n_batches: int) -> None:
    tr = _stub_trainer(n_batches, own_bn_stats=True)
    tr._train_one_epoch(11, None, None, ("c0", "c23"))
    expect = min(_EMA_BN_WINDOW_STEPS, n_batches)
    assert tr.ema.n_observe == expect
    assert sum(tr.flags_seen) == expect
    # the window is the LAST `expect` steps, contiguous
    assert tr.flags_seen == [False] * (n_batches - expect) + [True] * expect


@pytest.mark.parametrize("n_batches", [1, 50, 1000])
def test_flag_off_never_observes(n_batches: int) -> None:
    tr = _stub_trainer(n_batches, own_bn_stats=False)
    tr._train_one_epoch(11, None, None, ("c0", "c23"))
    assert tr.ema.n_observe == 0
    assert not any(tr.flags_seen)
    assert tr._ema_bn_observe_now is False


def test_window_repeats_every_epoch() -> None:
    tr = _stub_trainer(500, own_bn_stats=True)
    for ep in (1, 2, 3):
        tr._train_one_epoch(ep, None, None, ("c0", "c23"))
    assert tr.ema.n_observe == 3 * _EMA_BN_WINDOW_STEPS


def test_resume_inside_window_observes_remaining_steps_only() -> None:
    tr = _stub_trainer(500, own_bn_stats=True, start_step=450)
    tr._train_one_epoch(11, None, None, ("c0", "c23"))
    assert tr.ema.n_observe == 50


# --- fallback (MINOR 1) ---------------------------------------------------

class _Toy(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv = nn.Conv2d(1, 2, 1, bias=False)
        self.bn = nn.BatchNorm2d(2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.bn(self.conv(x))


def _x() -> torch.Tensor:
    return torch.randn(8, 1, 4, 4, generator=torch.Generator().manual_seed(0))


def test_fallback_is_recorded_flag_on() -> None:
    live = _Toy()
    ema = ModelEMA(live, decay=0.9, own_bn_stats=True)
    live.train()
    live(_x())
    ema.copy_buffers_from(live)  # no observation → fallback
    assert ema.last_copy_was_fallback is True and ema.bn_fallback_count == 1
    ema.observe_bn(live, _x())
    ema.copy_buffers_from(live)  # observed → no fallback
    assert ema.last_copy_was_fallback is False and ema.bn_fallback_count == 1
    ema.copy_buffers_from(live)  # window consumed → fallback again
    assert ema.last_copy_was_fallback is True and ema.bn_fallback_count == 2


def test_fallback_never_recorded_flag_off() -> None:
    live = _Toy()
    ema = ModelEMA(live, decay=0.9)
    live.train()
    for _ in range(3):
        live(_x())
        ema.copy_buffers_from(live)
    assert ema.last_copy_was_fallback is False and ema.bn_fallback_count == 0


def _warn_trainer(ema: ModelEMA) -> Trainer:
    tr = Trainer.__new__(Trainer)
    tr.ema = ema
    return tr


def test_fallback_warning_line(caplog: pytest.LogCaptureFixture) -> None:
    live = _Toy()
    ema = ModelEMA(live, decay=0.9, own_bn_stats=True)
    tr = _warn_trainer(ema)
    with caplog.at_level(logging.WARNING, logger=trainer_mod.__name__):
        ema.copy_buffers_from(live)
        tr._warn_ema_bn_fallback(7)
        ema.observe_bn(live, _x())
        ema.copy_buffers_from(live)
        tr._warn_ema_bn_fallback(8)
    msgs = [r.getMessage() for r in caplog.records if r.levelno == logging.WARNING]
    assert msgs == [
        "EMA-OWN-BN fallback epoch 7: no observation window reached; "
        "live BN stats copied (fallbacks so far: 1)"
    ]


def test_no_warning_flag_off(caplog: pytest.LogCaptureFixture) -> None:
    live = _Toy()
    ema = ModelEMA(live, decay=0.9)
    tr = _warn_trainer(ema)
    with caplog.at_level(logging.WARNING, logger=trainer_mod.__name__):
        ema.copy_buffers_from(live)
        tr._warn_ema_bn_fallback(1)
    assert not [r for r in caplog.records if "EMA-OWN-BN" in r.getMessage()]


def test_window_constant_is_the_planned_200() -> None:
    """The W5b plan fixes the V3 observation window at 200 steps (re-check MINOR, 2026-10-16)."""
    assert _EMA_BN_WINDOW_STEPS == 200
