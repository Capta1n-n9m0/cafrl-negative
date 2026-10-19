"""Training schedules & optimizer construction — Phase 4 Step 4.1 (G1).

Four pure-logic, unit-testable pieces the Phase-4 trainer wires together:

* :class:`GRLLambdaScheduler` — the load-bearing Ganin λ ramp (the *only* place
  the adversarial strength is scheduled; the discriminator CE weight is constant
  1.0 forever — Ganin asymmetry, phase3 R12/R22).
* :func:`build_optimizer` — AdamW with **role × weight-decay** param groups
  (backbone-1e-5 / freq+heads+disc-1e-4 roles, each split into wd=1e-4 weights
  and wd=0 norm-affine+bias) per `runs/phase4_build/PREREGISTRATION.md` **R-CJ1**.
* :func:`build_lr_scheduler` — cosine annealing over the full run (per-epoch step).
* :class:`ModelEMA` — the averaged-iterate model used for *every reported number*
  (G1: the averaged iterate is the convergent object).

Design ground truth: ``docs/phases/phase4.md`` Step 4.1 ·
``runs/phase4_build/PREREGISTRATION.md`` (R-CJ1 the wd=0 rule) ·
``docs/phases/phase3-asbuilt.md`` §B4 (per-arm disc), §B5 (``param_groups()`` /
self-enforcing freeze), R12/R15/R22 · ``docs/phases/phase1-asbuilt.md`` §B3.

The GRL λ closed form (Ganin 2016, γ=10), with the ramp anchored at the
**curriculum Phase-B onset** rather than step 0 so all of Phase A holds λ≡0::

    p = clamp((global_step − phase_b_start_step) / (total_steps − phase_b_start_step), 0, 1)
    λ_p = λ_max · (2 / (1 + exp(−10·p)) − 1)

Because ``p`` clamps to 0 for every Phase-A step, ``2/(1+exp(0))−1 = 0`` ⇒ λ_p is
**exactly 0 throughout Phase A** with no special-casing (verified by test). The
HSIC arms ramp their own weights on the **same** ``p`` (cross-arm comparability)
via :meth:`GRLLambdaScheduler.progress`.
"""

from __future__ import annotations

import math
from copy import deepcopy

import torch
from torch import nn

from src.config.defaults import TrainConfig


# ---------------------------------------------------------------------------
# (1) GRL λ schedule
# ---------------------------------------------------------------------------


class GRLLambdaScheduler:
    """Ganin gradient-reversal coefficient schedule (the load-bearing schedule).

    The trainer calls :meth:`lambda_p` each step and pushes the result into the
    GRL via ``grl.set_lambda(λ_p)`` — **nowhere else** does the adversarial
    strength change (the discriminator CE weight is a constant 1.0; phase3 R12/
    R22, the Ganin asymmetry). HSIC arms instead read :meth:`progress` (the raw
    clamped ``p``) so they ramp their weight on the same progress variable for
    cross-arm comparability (phase4.md §4.1).

    Args:
        lambda_max: the ceiling of the ramp (``LossConfig.grl_lambda_max`` = 0.5).
        total_steps: total optimizer steps over the whole run — the ramp reaches
            ``p = 1`` (hence λ ≈ ``lambda_max``) at ``total_steps``.
        phase_b_start_step: the global step at which curriculum Phase B begins
            (the ramp's origin; for every ``global_step < phase_b_start_step``,
            ``p`` clamps to 0 ⇒ λ_p = 0 throughout Phase A).
        unimodal: optional T2-1 flag (default ``False`` = a strict no-op). When
            ``True``, λ is step-decayed by 0.5× once ``global_step`` reaches
            ``unimodal_decay_step`` (set it via the constructor). Off-by-default
            and a no-op so the A0 default path is untouched.
        unimodal_decay_step: the global step at/after which the 0.5× decay applies
            when ``unimodal`` is set. Ignored when ``unimodal`` is ``False``.

    Note:
        Pure function of ``global_step`` — holds no mutable schedule state, so it
        needs no ``state_dict`` (it is reconstructed from config on resume and the
        step counter lives in the trainer/checkpoint).
    """

    def __init__(
        self,
        lambda_max: float,
        total_steps: int,
        phase_b_start_step: int,
        unimodal: bool = False,
        *,
        unimodal_decay_step: int | None = None,
    ) -> None:
        if total_steps <= phase_b_start_step:
            raise ValueError(
                f"total_steps ({total_steps}) must exceed phase_b_start_step "
                f"({phase_b_start_step}) so the ramp denominator is positive."
            )
        if phase_b_start_step < 0:
            raise ValueError(f"phase_b_start_step must be >= 0; got {phase_b_start_step}")
        self.lambda_max = float(lambda_max)
        self.total_steps = int(total_steps)
        self.phase_b_start_step = int(phase_b_start_step)
        self.unimodal = bool(unimodal)
        self.unimodal_decay_step = (
            None if unimodal_decay_step is None else int(unimodal_decay_step)
        )

    def progress(self, global_step: int) -> float:
        """The raw clamped ramp progress ``p`` ∈ [0, 1].

        ``p = clamp((global_step − phase_b_start_step) /
        (total_steps − phase_b_start_step), 0, 1)`` — 0 for all of Phase A,
        rising to 1 at ``total_steps``. The HSIC arm ramps its weight on this
        exact value so GRL and HSIC arms share a single progress variable
        (phase4.md §4.1). Clamped at both ends.
        """
        denom = self.total_steps - self.phase_b_start_step
        p = (global_step - self.phase_b_start_step) / denom
        if p < 0.0:
            return 0.0
        if p > 1.0:
            return 1.0
        return p

    def lambda_p(self, global_step: int) -> float:
        """The Ganin λ at ``global_step``: ``λ_max·(2/(1+exp(−10·p)) − 1)``.

        With ``p`` clamped to 0 throughout Phase A (``global_step <
        phase_b_start_step``), the sigmoid term is ``2·0.5 − 1 = 0`` so **λ_p is
        exactly 0 for all of Phase A** — no special-casing, it falls out of the
        closed form. From Phase B onward λ rises monotonically toward
        ``λ_max·(2/(1+exp(−10)) − 1) ≈ λ_max·0.99991`` at ``total_steps``.

        The optional ``unimodal`` T2-1 flag step-decays λ by 0.5× once
        ``global_step >= unimodal_decay_step`` (a strict no-op when off).
        """
        p = self.progress(global_step)
        lam = self.lambda_max * (2.0 / (1.0 + math.exp(-10.0 * p)) - 1.0)
        if (
            self.unimodal
            and self.unimodal_decay_step is not None
            and global_step >= self.unimodal_decay_step
        ):
            lam *= 0.5
        return lam


def lambda_p(
    step: int, total_steps: int, lam_max: float, gamma: float = 10.0,
) -> float:
    """The DANN λ ramp from step 0: ``λmax·(2/(1+e^(−γp)) − 1)``, ``p = step/T``.

    Phase 6 (lesson L1): the phase-anchored ramp gives λ = 0 for epochs 1..10 even
    in flat mode, so E1 ramps from global step 0 over the whole run instead
    (decision "Revision 1 W0: adversary tested as designed, ramp from step 0").
    ``p`` is clamped to [0, 1], so λ(0) = 0 and λ(T) = λmax·(2/(1+e^(−γ)) − 1).
    A pure function so the pass rule can be tested without a trainer.

    Args:
        step: the 0-based global optimizer step whose forward uses λ.
        total_steps: T = Σ steps per epoch over ALL epochs (must be > 0).
        lam_max: λmax (``LossConfig.grl_lambda_max``; 0.5 for E1).
        gamma: the ramp steepness (Ganin's 10).
    """
    if total_steps <= 0:
        raise ValueError(f"total_steps must be > 0; got {total_steps}")
    p = step / total_steps
    if p < 0.0:
        p = 0.0
    elif p > 1.0:
        p = 1.0
    return lam_max * (2.0 / (1.0 + math.exp(-gamma * p)) - 1.0)


class StepZeroLambdaScheduler:
    """GRL λ schedule that ramps from step 0 (``TrainConfig.grl_ramp = from_step0``).

    Drop-in for :class:`GRLLambdaScheduler` where the trainer reads it
    (``lambda_p`` / ``progress`` / ``total_steps`` / ``phase_b_start_step``); it
    delegates to the pure :func:`lambda_p`. ``phase_b_start_step`` is 0 by
    definition. Stateless, so resume needs nothing beyond the global step.
    """

    def __init__(self, lambda_max: float, total_steps: int, gamma: float = 10.0) -> None:
        if total_steps <= 0:
            raise ValueError(f"total_steps must be > 0; got {total_steps}")
        self.lambda_max = float(lambda_max)
        self.total_steps = int(total_steps)
        self.phase_b_start_step = 0
        self.gamma = float(gamma)

    def progress(self, global_step: int) -> float:
        """``p = clamp(global_step / total_steps, 0, 1)``."""
        return min(max(global_step / self.total_steps, 0.0), 1.0)

    def lambda_p(self, global_step: int) -> float:
        """λ at ``global_step`` (the pure :func:`lambda_p`)."""
        return lambda_p(global_step, self.total_steps, self.lambda_max, self.gamma)


# ---------------------------------------------------------------------------
# (2) Optimizer builder — role × weight-decay param groups (R-CJ1)
# ---------------------------------------------------------------------------


def _is_no_decay(p: nn.Parameter) -> bool:
    """R-CJ1 ``ndim`` rule: a param with ``ndim <= 1`` is no-decay.

    1-D (or 0-D) params are exactly the BatchNorm/LayerNorm affine weights *and*
    every bias — they are never weight-decayed (independent best practice, and
    mandatory here: option-(c)'s zero-grad touch gives the compressed sub-BN a
    *zero* gradient, on which AdamW's decoupled weight decay would still fire
    unless wd=0). ``ndim >= 2`` params (conv/linear weights) are decayed.
    """
    return p.ndim <= 1


def build_optimizer(model, train_cfg: TrainConfig) -> torch.optim.AdamW:
    """Build the AdamW optimizer with **role × weight-decay** param groups.

    Roles & learning rates (phase4.md §4.1, phase3-asbuilt §B4/§B5):

    * **backbone** — the EfficientNet-B0 params (``model.backbone.param_groups()
      ["backbone"]``) → ``lr_backbone`` (1e-5).
    * **freq** — the backbone 1×1 projection ``head`` PLUS *all* frequency-side
      params (dct, phase, estimator, band_gate, fusion) → ``lr_freq`` (1e-4).
      Computed as "every param that is neither backbone-EffNet nor discriminator".
    * **disc** — the discriminator params → ``lr_disc`` (1e-4), **only if
      ``model.discriminator is not None``** (arm-scoped: present under grl/both,
      absent under none/hsic — §B4).

    Within each role the params split (R-CJ1) by the ``ndim`` rule into a
    ``weight_decay = train_cfg.weight_decay`` (1e-4) group for ``ndim >= 2``
    weights and a ``weight_decay = 0.0`` group for ``ndim <= 1`` norm-affine +
    bias params. Up to 6 groups (3 roles × {decay, no-decay}); **empty groups are
    skipped**. Each group is tagged with a ``name`` (e.g. ``"backbone_decay"``,
    ``"freq_no_decay"``, ``"disc_decay"``) for diagnostics.

    **CJ-2 (keep-frozen-backbone-in-optimizer):** the backbone EffNet params are
    included **even while frozen** — the curriculum unfreezes them at epoch 11, so
    excluding them would orphan-trap them (a param in no group is never stepped).
    A frozen param has ``grad is None`` ⇒ AdamW skips it ⇒ bit-identical
    (audit-confirmed). We therefore do NOT filter on ``requires_grad`` here.

    The constructed groups are asserted to partition ``model.parameters()``
    exactly once (every param covered, none double-counted) by object identity.

    Args:
        model: a constructed :class:`~src.models.cafrl.CAFRL`.
        train_cfg: the :class:`TrainConfig` (reads ``lr_backbone``, ``lr_freq``,
            ``lr_disc``, ``weight_decay``).

    Returns:
        a :class:`torch.optim.AdamW` with the role × weight-decay groups (AdamW
        default betas/eps; per-group ``lr`` and ``weight_decay``).
    """
    # Role membership by object identity (no string name-matching — §B5).
    backbone_groups = model.backbone.param_groups()
    backbone_params = list(backbone_groups["backbone"])
    backbone_ids = {id(p) for p in backbone_params}

    disc_params: list[nn.Parameter] = []
    disc_ids: set[int] = set()
    if getattr(model, "discriminator", None) is not None:
        disc_params = list(model.discriminator.parameters())
        disc_ids = {id(p) for p in disc_params}

    # freq role = everything that is neither backbone-EffNet nor discriminator
    # (this is the backbone "head"/proj + all frequency-side params). Iterate the
    # full model so nothing is dropped.
    freq_params = [
        p
        for p in model.parameters()
        if id(p) not in backbone_ids and id(p) not in disc_ids
    ]

    roles: list[tuple[str, list[nn.Parameter], float]] = [
        ("backbone", backbone_params, float(train_cfg.lr_backbone)),
        ("freq", freq_params, float(train_cfg.lr_freq)),
    ]
    if disc_params:
        roles.append(("disc", disc_params, float(train_cfg.lr_disc)))

    wd = float(train_cfg.weight_decay)
    groups: list[dict] = []
    for role_name, params, lr in roles:
        decay = [p for p in params if not _is_no_decay(p)]
        no_decay = [p for p in params if _is_no_decay(p)]
        if decay:
            groups.append(
                {"name": f"{role_name}_decay", "params": decay, "lr": lr, "weight_decay": wd}
            )
        if no_decay:
            groups.append(
                {
                    "name": f"{role_name}_no_decay",
                    "params": no_decay,
                    "lr": lr,
                    "weight_decay": 0.0,
                }
            )

    # Assert the groups partition model.parameters() exactly once.
    grouped_ids: list[int] = [id(p) for g in groups for p in g["params"]]
    model_ids = {id(p) for p in model.parameters()}
    if len(grouped_ids) != len(set(grouped_ids)):
        raise AssertionError("optimizer param groups double-count a parameter")
    if set(grouped_ids) != model_ids:
        missing = len(model_ids - set(grouped_ids))
        extra = len(set(grouped_ids) - model_ids)
        raise AssertionError(
            f"optimizer param groups do not partition model.parameters(): "
            f"{missing} param(s) dropped, {extra} foreign."
        )

    return torch.optim.AdamW(groups)


# ---------------------------------------------------------------------------
# (3) Cosine LR scheduler
# ---------------------------------------------------------------------------


def build_lr_scheduler(
    optimizer: torch.optim.Optimizer, train_cfg: TrainConfig
) -> torch.optim.lr_scheduler.LRScheduler:
    """Cosine-annealing LR scheduler over the full run.

    Cosine annealing over ``train_cfg.epochs`` (50). No warmup by default; a
    ``warmup_epochs`` knob may exist on ``train_cfg`` (default 0 = off) — when
    ``> 0`` a linear warmup is prepended via ``SequentialLR``. Each group's own
    per-group ``lr`` (backbone 1e-5 vs freq/disc 1e-4) is annealed proportionally,
    so the role LR ratio is preserved across the schedule.

    **Stepping cadence (the trainer must call it correctly):** this is a
    **per-epoch** scheduler — call ``scheduler.step()`` once at the **end of each
    epoch** (after all optimizer steps in that epoch), NOT per optimizer step.
    ``CosineAnnealingLR(T_max=epochs)`` reaches its minimum after ``epochs``
    ``.step()`` calls. The returned scheduler exposes ``state_dict()`` /
    ``load_state_dict()`` for checkpoint round-trip.

    Args:
        optimizer: the optimizer from :func:`build_optimizer`.
        train_cfg: the :class:`TrainConfig` (reads ``epochs`` and the optional
            ``warmup_epochs``).

    Returns:
        a :class:`torch.optim.lr_scheduler.LRScheduler` (cosine, optionally with a
        linear warmup head).
    """
    epochs = int(train_cfg.epochs)
    warmup = int(getattr(train_cfg, "warmup_epochs", 0))

    cosine = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=max(epochs - warmup, 1)
    )
    if warmup <= 0:
        return cosine

    warmup_sched = torch.optim.lr_scheduler.LinearLR(
        optimizer, start_factor=1e-3, end_factor=1.0, total_iters=warmup
    )
    return torch.optim.lr_scheduler.SequentialLR(
        optimizer, schedulers=[warmup_sched, cosine], milestones=[warmup]
    )


# ---------------------------------------------------------------------------
# (4) EMA
# ---------------------------------------------------------------------------


class ModelEMA:
    """Exponential-moving-average shadow of a live :class:`CAFRL` model.

    Holds a **deep-copied** model in :attr:`module`, initialized from the live
    weights at construction over the **full param list**. The trainer:

    * calls :meth:`update` after **every optimizer step** —
      ``ema_p = decay·ema_p + (1−decay)·live_p`` over *parameters only*;
    * calls :meth:`copy_buffers_from` **before every evaluation** — ALL buffers
      (incl. BatchNorm running stats, which the split-BN clean-branch inference
      reads) are copied **verbatim** from the live model; buffers are NEVER EMA'd.

    Two consequences that prevent silent corruption (phase4.md §4.1):

    * **Frozen backbone params are constant in Phase A**, so their EMA update is a
      no-op — no re-sync is needed at the epoch-11 unfreeze (the full-param init
      already mirrors them).
    * **BN buffers are never stale**: the verbatim copy exports the (frozen,
      bit-identical) backbone/estimator running stats into the EMA module so every
      validation/model-selection number uses clean stats (G1: the averaged iterate
      is the convergent object; **all reported numbers use the EMA module**, wrapped
      in :class:`~src.models.cafrl.CAFRLEvalAdapter` for the evaluator).

    ``self.module.state_dict()`` round-trips through ``utils/checkpoint.py`` (its
    keys match the live model exactly — it is a structural deep copy).

    W5b V3 (``own_bn_stats=True``, config ``train.ema_own_bn_stats``; default
    off): the W5b-S0 diagnosis showed the verbatim copy above fails when the live
    model moves fast — EMA weights scored with the live weights' BN stats
    collapsed (r1_abl_curriculum_s42, epoch 14). With the flag on,
    :meth:`observe_bn` refreshes the shadow's BN stats from its own forward and
    :meth:`copy_buffers_from` skips those BN layers. Flag off ⇒ the original
    code path, unchanged.

    Args:
        model: the live :class:`CAFRL` to shadow.
        decay: EMA decay (``TrainConfig.ema_decay`` = 0.999).
    """

    def __init__(
        self, model: nn.Module, decay: float = 0.999, *, own_bn_stats: bool = False,
    ) -> None:
        self.decay = float(decay)
        # Deep copy so the shadow is a fully independent module (own params +
        # buffers), initialized from the live weights. Held in eval mode (it is
        # only ever read for validation) and detached from autograd.
        self.module = deepcopy(model)
        self.module.eval()
        for p in self.module.parameters():
            p.requires_grad_(False)
        # W5b V3 (``TrainConfig.ema_own_bn_stats``, default False). When False
        # nothing below is used and copy_buffers_from is the original verbatim
        # copy. When True, :meth:`observe_bn` gives the shadow BN running stats
        # computed from its OWN forward (the EMA weights), and copy_buffers_from
        # leaves those BN layers alone.
        self.own_bn_stats = bool(own_bn_stats)
        self._bn_observed: frozenset[str] = frozenset()
        # W5b-S0 fixer (verifier A MINOR 1): with the flag on, a copy_buffers_from
        # that finds no observation (no window reached since the last eval, e.g. a
        # resume after the window) falls back to the verbatim live copy. It is
        # recorded here so the trainer logs a WARNING and the W5b watcher can act.
        # Never set with the flag off.
        self.last_copy_was_fallback: bool = False
        self.bn_fallback_count: int = 0

    @torch.no_grad()
    def update(self, model: nn.Module) -> None:
        """EMA-update the shadow **parameters** from ``model`` (call after each step).

        ``ema_p ← decay·ema_p + (1−decay)·live_p`` over the full, order-matched
        parameter lists. Buffers are untouched here (they are copied verbatim by
        :meth:`copy_buffers_from`). Frozen (constant) live params leave their EMA
        unchanged, so the Phase-A frozen backbone needs no special handling.
        """
        d = self.decay
        for ema_p, live_p in zip(self.module.parameters(), model.parameters()):
            ema_p.mul_(d).add_(live_p.detach(), alpha=1.0 - d)

    @torch.no_grad()
    def copy_buffers_from(self, model: nn.Module) -> None:
        """Copy ALL buffers verbatim from ``model`` into the shadow (call before eval).

        Buffers — BatchNorm ``running_mean`` / ``running_var`` /
        ``num_batches_tracked`` (incl. the split-BN clean branch inference reads)
        and any other registered buffers — are **never EMA'd**; they are copied
        as-is from the live model so the EMA module evaluates with the live (and,
        for the frozen modules, bit-identical clean) statistics.
        """
        if not self.own_bn_stats or not self._bn_observed:
            # Original behaviour (always taken when ema_own_bn_stats is off).
            for ema_b, live_b in zip(self.module.buffers(), model.buffers()):
                ema_b.copy_(live_b)
            if self.own_bn_stats:
                # Flag on but nothing observed: a fallback, recorded (never silent).
                self.last_copy_was_fallback = True
                self.bn_fallback_count += 1
            return
        self.last_copy_was_fallback = False
        # ema_own_bn_stats: keep the BN running stats the shadow computed from its
        # own weights (observe_bn); copy every other buffer (BN layers the live
        # model holds in eval — e.g. the frozen backbone — and constants).
        live_bufs = dict(model.named_buffers())
        for name, ema_b in self.module.named_buffers():
            if name.rpartition(".")[0] in self._bn_observed:
                continue
            ema_b.copy_(live_bufs[name])
        self._bn_observed = frozenset()  # the window is consumed by this eval

    @torch.no_grad()
    def observe_bn(self, model: nn.Module, images: torch.Tensor, **fwd_kwargs) -> None:
        """Update the shadow's BN running stats from its OWN forward (V3, W5b).

        Only with ``own_bn_stats=True``. Every BatchNorm layer (and every
        :class:`~src.models.norms.SplitBatchNorm2d` router) whose live counterpart
        in ``model`` is in train mode is put in train mode in the shadow, the
        batch is forwarded through the shadow (EMA weights) with the same
        ``fwd_kwargs`` (e.g. the split-BN ``clean_mask``), and the shadow is put
        back in eval. The running stats therefore follow the live rule (same
        layers, same momentum, same batches) but describe the EMA weights' own
        activations — the W5b-S0 diagnosis found that EMA weights scored with the
        live model's BN stats collapse when the live model moves fast. Parameters
        are untouched; layers the live model holds in eval (the frozen Phase-A
        backbone) keep the live, copied stats. The caller decides when to call it
        (the trainer: the last steps of each epoch) and should keep it RNG-neutral.

        Note: the observation forward runs with every non-BN module of the shadow
        in eval, so dropout / stochastic depth are OFF, while the live BN stats
        are gathered with them on. For the curriculum arm (``invariance_arm:
        none``, no discriminator, drop_path 0) this changes nothing; on the grl
        arms the shadow's stats would be slightly more eval-consistent than the
        live ones.
        """
        if not self.own_bn_stats:
            raise RuntimeError("observe_bn requires ModelEMA(own_bn_stats=True)")
        from src.models.norms import SplitBatchNorm2d

        live_mods = dict(model.named_modules())
        observed: set[str] = set()
        for name, m in self.module.named_modules():
            live = live_mods.get(name)
            if live is None or not live.training:
                continue
            if isinstance(m, nn.modules.batchnorm._BatchNorm):
                m.train()
                observed.add(name)
            elif isinstance(m, SplitBatchNorm2d):
                m.train()  # route by clean_mask as the live model does
        try:
            self.module(images, **fwd_kwargs)
        finally:
            self.module.eval()
        self._bn_observed = self._bn_observed | frozenset(observed)

    def state_dict(self) -> dict:
        """The shadow module's ``state_dict`` (round-trips through checkpoint.py)."""
        return self.module.state_dict()

    def load_state_dict(self, state: dict, strict: bool = True) -> None:
        """Load a saved shadow ``state_dict`` (checkpoint resume)."""
        self.module.load_state_dict(state, strict=strict)
