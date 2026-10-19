"""CAFRL training integration core — Phase 4 Step 4.3 (`Trainer`).

Wires the Phase-1 data pipeline + Phase-2/3 model + losses + the Batch-1
schedules/curriculum/EMA into the §4.3 per-step training loop, with the 3-phase
progressive curriculum, the GRL λ ramp, EMA validation, the §4.5 diagnostic
collection materials, and mid-epoch-resumable checkpointing. It BUILDS everything
from a :class:`~src.config.defaults.Config`, so it is fully testable without DDP;
``train.py`` (Batch 3) wraps `core` in DDP and passes it via ``ddp_wrap``.

The binding design ground truth:

* ``docs/phases/phase4.md`` §4.3 (per-step flow, disc lifecycle, estimator
  staged-mode, HSIC magnitude-matching, Q_d=0, validation, checkpoint/resume).
* ``runs/phase4_build/PREREGISTRATION.md`` — **R-CJ1b (CORRECTED)** (DDP uses
  ``find_unused_parameters=True`` and the R-CJ1 all-trainable-params zero touch is
  REMOVED — FUP=True natively tolerates the unused compressed sub-BN affine and the
  registered-but-frozen backbone; the touch's extra autograd edge per param
  double-counted under FUP's reducer), the surviving **wd=0** norm/bias group, and
  **R-HSIC-GUARD** (the ``mean(HSIC_y) < 1e-6 ⇒ s=1.0`` divide-by-zero guard, NOT a
  ``max(denom,ε)`` clamp).
* the as-built registers ``phase{1,2,3}-asbuilt.md`` (the forward/loss/sampler/
  freeze/eval contracts the per-step order honors).

**The EXACT per-step order** (the verifier checks this), in
:meth:`Trainer._train_step`:

1. move batch tensors to device; ``clean_mask = clean_mask_from_bin_idx(bin_idx)``
   (asserts ``>= 0`` — let it raise on the −1 c18 sentinel).
2. if ``core.grl is not None``: ``core.grl.set_lambda(grl_sched.lambda_p(step))``
   BEFORE this step's forward (λ captured at forward; Phase A ⇒ exactly 0).
3. ``optimizer.zero_grad(set_to_none=True)``.
4. autocast(bf16): ``outputs = fwd(images, clean_mask=...[, bin_idx=... oracle])``;
   ``losses = compute_losses(outputs, batch, loss_w, arm, disc_weight=disc_w)``;
   ``total = losses["total"]``.
5. ``total.backward()`` → ``clip_grad_norm_(core.parameters(), grad_clip)`` →
   ``optimizer.step()`` → ``ema.update(core)`` → ``global_step += 1``. No all-params
   touch (R-CJ1b CORRECTED): under ``find_unused_parameters=True`` the unused
   trainable params (the all-clean Phase-A compressed sub-BN affine + any
   disconnected head) get grad-None ⇒ AdamW skips them ⇒ bit-identical, and
   frozen-backbone params (``requires_grad=False``) likewise stay grad-None ⇒
   bit-identical. FUP=True natively all-reduces the backbone after the epoch-11
   unfreeze.
6. accumulate loss scalars; HSIC magnitude-match accumulation during epoch 11
   (hsic/both); log step scalars every 50 steps on rank 0.
"""

from __future__ import annotations

import logging
import math
from pathlib import Path
from collections.abc import Sequence
from typing import Any, Callable

import pandas as pd
import torch
import torch.distributed as dist
from torch import Tensor, nn
from torch.utils.data import DataLoader

from src.config.defaults import Config
from src.data.ffpp_faces import FFppFacesDataset
from src.data.sampler import (
    MultiQualityBatchSampler,
    SpecDatasetWrapper,
    collate,
)
from src.evaluation.evaluator import Evaluator
from src.losses import compute_losses
from src.losses.hsic import hsic_invariance_terms
from src.models.cafrl import CAFRL, CAFRLEvalAdapter
from src.models.norms import clean_mask_from_bin_idx
from src.training.curriculum import CurriculumScheduler
from src.training.difficulty import DifficultyModule
from src.training.scheduler import (
    GRLLambdaScheduler,
    ModelEMA,
    StepZeroLambdaScheduler,
    build_lr_scheduler,
    build_optimizer,
)
from src.utils import checkpoint as ckpt
from src.utils.logging import TBLogger

_LOG = logging.getLogger(__name__)

# Loss-term scalar keys logged/accumulated per step (all present in compute_losses).
_LOSS_LOG_KEYS: tuple[str, ...] = (
    "total", "cls", "crf", "cons", "phase_geo", "circ", "div",
    "adv", "hsic_crf", "hsic_y", "freq_aux",
)
# R-HSIC-GUARD floor: below this the keep-label HSIC term is treated as collapsed.
_EPS_HSIC: float = 1e-6
# Default step-scalar cadence; the live value is `cfg.train.step_log_every`
# (Phase 6), whose default equals this.
_STEP_LOG_EVERY: int = 50
# W5b V3 (`train.ema_own_bn_stats`): the EMA shadow refreshes its own BN running
# stats on the last this-many steps of every epoch (BN momentum 0.1 forgets the
# previous values within ~50 steps). Unused when the flag is off.
_EMA_BN_WINDOW_STEPS: int = 200
_GRL_RAMPS = frozenset({"phase_anchored", "from_step0"})

_GRL_ARMS = frozenset({"grl", "both"})
_HSIC_ARMS = frozenset({"hsic", "both"})
_ORACLE_BAND = frozenset({"oracle"})


class Trainer:
    """The CAFRL training integration core (DDP-agnostic; §4.3).

    Builds the model, optimizer (role × wd=0 norm/bias groups), LR scheduler, EMA,
    curriculum, GRL λ schedule, and the train/val data pipeline from ``cfg``. The
    forward path runs through :attr:`fwd` (optionally DDP-wrapped); freezing, the
    GRL/discriminator handles, and grad-clip use :attr:`core` (under DDP they share
    the same submodule objects).

    Args:
        cfg: the resolved :class:`Config` (the arm/conditioning/fusion come from
            ``cfg.model``; LR/curriculum/EMA from ``cfg.train``; data from
            ``cfg.data``).
        rank: this process's DDP rank (logging/checkpointing/validation are rank-0).
        world_size: number of DDP ranks.
        device: torch device (defaults to cuda if available, else cpu).
        run_dir: the run output directory (checkpoints + TB under it).
        subset_fraction: train+val video subset fraction in (0, 1] for the smoke /
            tests (deterministic, class-balanced over videos when < 1.0).
        ddp_wrap: optional callable wrapping ``core_model`` into a DDP module; the
            returned module is used for forward only.
        max_epochs: optional override of ``cfg.train.epochs`` (the smoke runs fewer).
        pretrained_backbone: load ImageNet weights into the backbone (default True;
            pass False in tests/CI).
    """

    def __init__(
        self,
        cfg: Config,
        *,
        rank: int = 0,
        world_size: int = 1,
        device: torch.device | str | None = None,
        run_dir: Path | str,
        subset_fraction: float = 1.0,
        ddp_wrap: Callable[[nn.Module], nn.Module] | None = None,
        max_epochs: int | None = None,
        pretrained_backbone: bool = True,
        frame_augmentor: Any | None = None,
    ) -> None:
        self.cfg = cfg
        self.rank = int(rank)
        self.world_size = int(world_size)
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = torch.device(device)
        self.run_dir = Path(run_dir)
        self.run_dir.mkdir(parents=True, exist_ok=True)
        if not (0.0 < float(subset_fraction) <= 1.0):
            raise ValueError(f"subset_fraction must be in (0, 1]; got {subset_fraction}")
        self.subset_fraction = float(subset_fraction)
        self.max_epochs = int(max_epochs if max_epochs is not None else cfg.train.epochs)
        # Optional TRAIN-only frame augmentor (default None ⇒ CAFRL is bit-identical;
        # A0 + every default/A1/A2/A3 run leaves this None). Set ONLY for the
        # aug-matched STOP-gate control (CAFRL-mq-aug vs Xception-mq-aug). Threaded
        # to the train FFppFacesDataset; never the val datasets (eval stays clean).
        self.frame_augmentor = frame_augmentor

        # -- model: build core, wrap for forward only (DDP shares submodules) ----
        core_model = CAFRL(cfg.model, pretrained_backbone=pretrained_backbone)
        core_model.to(self.device)
        self.core: CAFRL = core_model
        self.fwd: nn.Module = ddp_wrap(core_model) if ddp_wrap is not None else core_model

        self.arm: str = self.core.invariance_arm  # normalized str value
        # The model forward only needs bin_idx for the oracle band/fusion arms.
        self._needs_bin_idx: bool = (
            self.core.conditioning in _ORACLE_BAND
            or self.core.fusion_conditioning in _ORACLE_BAND
        )

        # -- optimizer / lr / ema / curriculum / difficulty ----------------------
        self.optimizer = build_optimizer(core_model, cfg.train)
        self.lr_scheduler = build_lr_scheduler(self.optimizer, cfg.train)
        self.ema = ModelEMA(
            core_model, cfg.train.ema_decay,
            own_bn_stats=bool(getattr(cfg.train, "ema_own_bn_stats", False)),
        )
        # W5b V3: set per step by _train_one_epoch (only ever True when the flag is on).
        self._ema_bn_observe_now: bool = False
        self.curriculum = CurriculumScheduler(cfg.data, cfg.loss, cfg.train)
        self.difficulty = DifficultyModule(enabled=False)
        # num_bins is the model's CRF-bin count (estimator/discriminator);
        # equal to len(bin_levels) = 6 by construction.
        self.num_bins = int(cfg.model.estimator.num_bins)

        # -- the train data pipeline (phase1-asbuilt §B8 union form) -------------
        self._build_train_loader()

        # -- Phase 6 logging / ramp options (defaults = the f2e3558 behaviour) ----
        self.grl_ramp: str = str(getattr(cfg.train, "grl_ramp", "phase_anchored"))
        if self.grl_ramp not in _GRL_RAMPS:
            raise ValueError(
                f"train.grl_ramp must be one of {sorted(_GRL_RAMPS)}; "
                f"got {self.grl_ramp!r}"
            )
        self.step_log_every: int = int(getattr(cfg.train, "step_log_every", _STEP_LOG_EVERY))
        if self.step_log_every < 1:
            raise ValueError(f"train.step_log_every must be >= 1; got {self.step_log_every}")
        self.step_log_detail: bool = bool(getattr(cfg.train, "step_log_detail", False))
        self.val_raw: bool = bool(getattr(cfg.train, "val_raw", False))
        # Detail-mode per-step readouts (filled by _train_step on log steps only).
        self._last_lambda: float = float("nan")
        self._last_step_est_pm1: float = float("nan")

        # -- GRL λ schedule: derive total_steps + phase_b_start_step -------------
        if self.grl_ramp == "from_step0":
            # Lesson L1: ramp from global step 0 over ALL epochs, never anchored
            # at phase_bounds (works in flat and baby_step alike).
            total_steps = self._total_steps_all_epochs()
            self.total_steps = total_steps
            self.phase_b_start_step = 0
            self.grl_sched = StepZeroLambdaScheduler(
                cfg.loss.grl_lambda_max, total_steps,
            )
        else:
            total_steps, phase_b_start = self._derive_lambda_anchors()
            self.total_steps = total_steps
            self.phase_b_start_step = phase_b_start
            self.grl_sched = GRLLambdaScheduler(
                cfg.loss.grl_lambda_max, total_steps, phase_b_start,
            )

        # -- validation datasets (rank-0 only consumes them) ---------------------
        self.val_ds_c23 = self._build_val_dataset(("c23",))
        self.val_ds_c40 = self._build_val_dataset(("c40",))

        # -- TB logger (rank 0 only) ---------------------------------------------
        self.tb: TBLogger | None = TBLogger(self.run_dir) if self.rank == 0 else None

        # -- training state ------------------------------------------------------
        self.global_step: int = 0
        self.best_metric: float = float("-inf")
        self.best_valloss: float = float("inf")  # additional best-by-val-loss
        self.start_epoch: int = 1
        self.start_step_in_epoch: int = 0  # mid-epoch resume offset
        self.hsic_scale: float | None = None
        # R-DISC-ACC train-stream disc monitor (filled per epoch in
        # _train_one_epoch; diagnostic-only, never checkpointed). Empty until the
        # first epoch runs so a standalone validate() (tests) falls back to the
        # single-bin c23 disc materials.
        self._disc_preds_epoch: list[int] = []
        self._disc_bins_epoch: list[int] = []

    # =====================================================================
    # construction helpers
    # =====================================================================

    def _subset_video_table(self, video_table: pd.DataFrame) -> pd.DataFrame:
        """Deterministic, class-balanced video subset of the (level-union) table.

        Keeps ``subset_fraction`` of the DISTINCT videos per class (label), then
        keeps every row of those videos (so each kept video keeps all its level
        rows). Deterministic: videos are sorted by ``(video_id, set)`` and the
        first ``ceil(frac·n)`` per class are kept — no RNG, so the subset is stable
        across processes/ranks/resumes. ``subset_fraction == 1.0`` returns the
        table unchanged.
        """
        if self.subset_fraction >= 1.0:
            return video_table
        keep_keys: set[tuple[str, str]] = set()
        # distinct video = (video_id, set) — a fake stem appears once per method.
        for label in (0, 1):
            sub = video_table[video_table["label"] == label]
            keys = sorted({(str(r.video_id), str(r.set)) for r in sub.itertuples(index=False)})
            n_keep = max(1, math.ceil(self.subset_fraction * len(keys)))
            keep_keys.update(keys[:n_keep])
        mask = video_table.apply(
            lambda r: (str(r["video_id"]), str(r["set"])) in keep_keys, axis=1
        )
        return video_table[mask].reset_index(drop=True)

    def _build_train_loader(self) -> None:
        """Build the level-union train dataset + sampler + loader (§B8 form)."""
        cfg = self.cfg
        levels = tuple(cfg.data.levels)
        self.ds_train = FFppFacesDataset(
            cfg, "train", levels=levels, training=True,
            frame_augmentor=self.frame_augmentor,
        )
        video_table = pd.concat(
            [self.ds_train.video_table(lvl).assign(level=lvl) for lvl in levels],
            ignore_index=True,
        )
        video_table = self._subset_video_table(video_table)
        self.sampler = MultiQualityBatchSampler(
            video_table, cfg, rank=self.rank, world_size=self.world_size,
            seed=cfg.train.seed,
        )
        # An explicit DataLoader generator makes iterator creation RNG-NEUTRAL: a
        # bare DataLoader seeds its per-iterator base seed from the GLOBAL torch
        # RNG (even at num_workers=0), which would shift the global RNG at every
        # epoch boundary AND break mid-epoch resume bit-equality (the iterator is
        # re-created at a different global-RNG point on resume). With a fixed
        # generator the global RNG is untouched by loader iteration, so the
        # forward/dropout RNG stream the model consumes is reproducible and the
        # §4.6 / Gate-4 resume test is bit-exact.
        self._loader_gen = torch.Generator()
        self._loader_gen.manual_seed(int(cfg.train.seed))
        self.train_loader = DataLoader(
            SpecDatasetWrapper(self.ds_train),
            batch_sampler=self.sampler,
            collate_fn=collate,
            num_workers=cfg.data.num_workers,
            generator=self._loader_gen,
        )

    def _build_val_dataset(self, levels: tuple[str, ...]) -> FFppFacesDataset:
        """Eval-mode FFpp val dataset at ``levels``, subset by video when < 1.0.

        Eval datasets are not sampler-driven, so the subset is applied by trimming
        the enumerated ``(video × frame)`` sample list to the kept videos (same
        deterministic per-class video keep as training, computed off the val index).
        """
        ds = FFppFacesDataset(self.cfg, "val", levels=levels, training=False)
        if self.subset_fraction >= 1.0:
            return ds
        # Deterministic class-balanced video keep, computed off the eval samples.
        per_class: dict[int, list[tuple[str, str]]] = {0: [], 1: []}
        seen: set[tuple[str, str, int]] = set()
        for (vid, set_name, label, _method, _level, _fidx) in ds._eval_samples:
            key = (str(vid), str(set_name), int(label))
            if key in seen:
                continue
            seen.add(key)
            per_class[int(label)].append((str(vid), str(set_name)))
        keep: set[tuple[str, str]] = set()
        for label in (0, 1):
            keys = sorted(set(per_class[label]))
            n_keep = max(1, math.ceil(self.subset_fraction * len(keys)))
            keep.update(keys[:n_keep])
        ds._eval_samples = [
            s for s in ds._eval_samples if (str(s[0]), str(s[1])) in keep
        ]
        return ds

    def _steps_for_levels(self, levels: tuple[str, ...]) -> int:
        """Realized per-epoch step count (== len(sampler)) for an active level set.

        Builds the sampler's plan for ``levels`` at epoch 0 and reads its length
        (the rank-sharded batch count). Restores the sampler's prior active levels
        and invalidates its cache so this probe never leaks into training.
        """
        prior_levels = self.sampler.active_levels
        prior_epoch = self.sampler._epoch
        self.sampler.set_active_levels(levels)
        self.sampler.set_epoch(0)
        n = len(self.sampler)
        # Restore + invalidate so the first real epoch rebuilds cleanly.
        self.sampler.set_active_levels(prior_levels)
        self.sampler.set_epoch(prior_epoch)
        return int(n)

    def _derive_lambda_anchors(self) -> tuple[int, int]:
        """Derive ``(total_steps, phase_b_start_step)`` from realized step counts.

        The GRL λ closed form needs two GLOBAL-STEP anchors:
        ``phase_b_start_step`` (the global step at which curriculum Phase B begins)
        and ``total_steps`` (the global step at which the ramp reaches ``p = 1``).

        Active levels — hence ``len(sampler)`` steps/epoch — DIFFER per phase
        (Phase A: c0/c23; B: +c28/c32; C: all 6), so we sum the *realized* per-epoch
        step counts across the epochs the curriculum will actually run:

            phase_b_start_step = Σ steps/epoch over Phase-A epochs (1..a_end)
            total_steps        = Σ steps/epoch over ALL epochs (1..max_epochs)

        with each epoch's step count taken from the sampler plan for that epoch's
        active level set (Phase A/B/C). This is exact for the realized run (the
        sampler plan is deterministic from seed+epoch and the per-phase active sets
        are fixed) — the §4.6 smoke re-derives it the same way. ``max_epochs`` may
        be scaled down for the smoke, so the anchors track the scaled run.
        """
        a_end, _b_end = self.curriculum.phase_bounds
        # Cache step counts per phase active-level set (one sampler build each).
        steps_by_phase: dict[str, int] = {}

        def steps_for(epoch: int) -> int:
            phase = self.curriculum.phase_of(epoch)
            if phase not in steps_by_phase:
                active, _w, _f = self.curriculum.on_epoch_start(epoch)
                steps_by_phase[phase] = self._steps_for_levels(active)
            return steps_by_phase[phase]

        total = 0
        phase_b_start = 0
        for epoch in range(1, self.max_epochs + 1):
            s = steps_for(epoch)
            if epoch <= a_end:
                phase_b_start += s
            total += s
        # Guard: if Phase A spans the whole (scaled) run there is no ramp window;
        # GRLLambdaScheduler needs total > phase_b_start. Give one nominal step of
        # ramp window so the scheduler constructs (λ stays ~0 anyway — A0 path).
        if total <= phase_b_start:
            total = phase_b_start + 1
        return int(total), int(phase_b_start)

    def _total_steps_all_epochs(self) -> int:
        """T = Σ realized steps per epoch over epochs 1..max_epochs (no guard).

        Used by the ``from_step0`` ramp. Each epoch's count comes from the sampler
        plan for that epoch's curriculum active set (one probe per phase), exactly
        as :meth:`_derive_lambda_anchors` sums ``total`` — but without its
        ``total > phase_b_start`` guard, which would add one phantom step when
        the whole (smoke) run sits inside Phase A.
        """
        steps_by_phase: dict[str, int] = {}
        total = 0
        for epoch in range(1, self.max_epochs + 1):
            phase = (
                "flat" if self.curriculum.mode == "flat"
                else self.curriculum.phase_of(epoch)
            )
            if phase not in steps_by_phase:
                active, _w, _f = self.curriculum.on_epoch_start(epoch)
                steps_by_phase[phase] = self._steps_for_levels(active)
            total += steps_by_phase[phase]
        if total <= 0:
            raise ValueError("from_step0 GRL ramp: the run has zero training steps")
        return int(total)

    # =====================================================================
    # the epoch loop
    # =====================================================================

    def train(self) -> None:
        """Run the full curriculum training loop (start_epoch .. max_epochs)."""
        for epoch in range(self.start_epoch, self.max_epochs + 1):
            active_levels, loss_w, frozen = self.curriculum.on_epoch_start(epoch)
            self.core.set_frozen(frozen)  # self-enforcing; no extra .eval()
            self.sampler.set_active_levels(active_levels)
            self.sampler.set_epoch(epoch)

            disc_w = None
            if self.arm in _GRL_ARMS:
                disc_w = self.curriculum.disc_class_weights(
                    self.sampler, self.num_bins, self.device,
                )

            self.fwd.train()  # frozen backbone/estimator stay eval (train() override)

            # Apply the frozen HSIC magnitude-match scale (post epoch-11) to the
            # per-phase loss weights for the hsic/both arms (no-op for grl/none).
            loss_w = self._apply_hsic_scale(loss_w, epoch)

            self._train_one_epoch(epoch, loss_w, disc_w, active_levels)

            self.lr_scheduler.step()  # PER-EPOCH

            is_best = False
            is_best_valloss = False
            if self.rank == 0:
                # R-DISC-ACC: thread the epoch's train-stream disc monitor into the
                # diagnostics (grl/both arms fill it; empty ⇒ falls back to c23).
                metrics = self.validate(
                    epoch, active_levels,
                    disc_preds=self._disc_preds_epoch,
                    disc_bins=self._disc_bins_epoch,
                )
                is_best = metrics["sel_metric"] > self.best_metric
                if is_best:
                    self.best_metric = metrics["sel_metric"]
                # Best-epoch-by-val-loss (additional to the AUC-selected best.pt —
                # the primary protocol metric stays mean val AUC, plan §6).
                vloss = float(metrics.get("val_loss", float("nan")))
                is_best_valloss = vloss == vloss and vloss < self.best_valloss
                if is_best_valloss:
                    self.best_valloss = vloss
                # Per-epoch one-line stdout summary — the A0-HEALTHY monitor greps
                # this (cls↓ (i); val AUC@c23 floor+climbing (ii); disc bal-acc vs
                # chance (iii)). EPOCH-tagged for easy filtering.
                # F2 (Phase 5.4): a conditional suffix appends the γ trajectory +
                # freq-head val-AUC (empty for every other arm ⇒ their log lines are
                # byte-identical — the smoke greps "γ=" to confirm γ moved off 0).
                f2_suffix = ""
                if "residual_gamma" in metrics:
                    f2_suffix = (
                        " | γ=%.4f(live %.4f) freqAUC c23=%.4f c40=%.4f" % (
                            metrics["residual_gamma"], metrics["residual_gamma_live"],
                            metrics.get("freq_auc_c23", float("nan")),
                            metrics.get("freq_auc_c40", float("nan")),
                        )
                    )
                # Phase 6 (val_raw): the raw (live) model's val AUCs next to the
                # EMA ones; empty when off ⇒ the EPOCH line is byte-identical.
                if "raw_val_auc_c23" in metrics:
                    f2_suffix += (
                        " | raw_val_auc_c23=%.5f raw_val_auc_c40=%.5f raw_sel=%.5f" % (
                            metrics["raw_val_auc_c23"], metrics["raw_val_auc_c40"],
                            metrics["raw_sel_metric"],
                        )
                    )
                _LOG.info(
                    "EPOCH %d done | n_active_bins=%d λ=%.5f | train_cls=%.5f | "
                    "val_auc_c23=%.5f val_auc_c40=%.5f sel=%.5f | "
                    "val_loss=%.5f (c23=%.5f c40=%.5f) | "
                    "disc_bal_acc=%.5f disc_chance=%.5f est_pm1=%.4f%s%s%s",
                    epoch, len(active_levels),
                    self.grl_sched.lambda_p(self.global_step),
                    getattr(self, "_last_epoch_cls", float("nan")),
                    metrics["val_auc_c23"], metrics["val_auc_c40"],
                    metrics["sel_metric"],
                    vloss, metrics.get("val_loss_c23", float("nan")),
                    metrics.get("val_loss_c40", float("nan")),
                    metrics.get("disc_balanced_acc", float("nan")),
                    metrics.get("disc_chance", float("nan")),
                    metrics.get("est_pm1_acc", float("nan")),
                    " *BEST-AUC*" if is_best else "",
                    " *BEST-LOSS*" if is_best_valloss else "",
                    f2_suffix,
                )
                # -- Phase 5.5 WARN-only diagnostics guardrails (D1 + D6) ----------
                # No training-behaviour change: these only emit extra WARN lines
                # (the EPOCH line above is unchanged). D1 caught at ep ~12 instead
                # of a post-hoc audit; D6 the same.
                from src.training import diagnostics as _diag

                for alarm in _diag.aux_dominance_alarms(
                    getattr(self, "_last_epoch_loss_means", {}), loss_w, self.arm,
                ):
                    _LOG.warning(
                        "AUX-DOMINANCE epoch %d: weighted %s=%.4g ran %.1f× "
                        "cls=%.4g (>10×) — D1 guardrail; the aux term is dwarfing "
                        "classification, check its loss weight",
                        epoch, alarm.component, alarm.weighted,
                        alarm.ratio, alarm.cls,
                    )
                if _diag.estimator_health_alarm(
                    metrics.get("est_pm1_acc", float("nan")),
                    band_conditioning=self.core.conditioning,
                    fusion_conditioning=self.core.fusion_conditioning,
                ):
                    _LOG.warning(
                        "ESTIMATOR-HEALTH epoch %d: est_pm1_acc=%.4f < 0.70 while "
                        "conditioning is 'estimated' (band=%s fusion=%s) — the "
                        "compression-conditioning premise (P1 ±1-bin 0.876) is "
                        "invalidated — D6 guardrail",
                        epoch, metrics.get("est_pm1_acc", float("nan")),
                        self.core.conditioning, self.core.fusion_conditioning,
                    )
            # save_checkpoint runs a per-rank RNG all-gather collective (F1), so it
            # MUST be called on EVERY rank; only rank 0 writes the file. `is_best`
            # is False on non-rank-0 (validate is rank-0-only) — harmless, the
            # best.pt write is rank-0-gated inside save_checkpoint.
            self.save_checkpoint(epoch, is_best=is_best, is_best_valloss=is_best_valloss)
            # Reset the mid-epoch resume offset after the first (possibly resumed)
            # epoch completes — subsequent epochs always start at step 0.
            self.start_step_in_epoch = 0

    def _apply_hsic_scale(self, loss_w, epoch: int):
        """Fold the frozen HSIC magnitude-match scale ``s`` into ``hsic_ratio``.

        Once ``self.hsic_scale`` is frozen (end of epoch 11, hsic/both only) every
        subsequent epoch scales the 1:5 ratio by ``s``: ``hsic_ratio = (s/5, s)``.
        Before epoch 11 (or for grl/none) this is a no-op. The accumulation that
        produces ``s`` happens DURING epoch 11 inside the step loop; epoch 11 itself
        runs at the unscaled default ratio (the term's contribution is ≈0 early in
        the ramp by design).
        """
        from dataclasses import replace

        if self.arm not in _HSIC_ARMS or self.hsic_scale is None:
            return loss_w
        s = float(self.hsic_scale)
        return replace(loss_w, hsic_ratio=(s / 5.0, s))

    def _train_one_epoch(
        self, epoch: int, loss_w, disc_w: Tensor | None,
        active_levels: tuple[str, ...],
    ) -> None:
        """One epoch of the per-step loop, with §4.5 step logging + HSIC accum."""
        a_end, _b_end = self.curriculum.phase_bounds
        in_hsic_match_epoch = (
            self.arm in _HSIC_ARMS
            and epoch == a_end + 1  # epoch 11 = first Phase-B epoch
            and self.hsic_scale is None
        )
        # Running accumulators for the epoch (logged at epoch end on rank 0).
        epoch_sums: dict[str, float] = {k: 0.0 for k in _LOSS_LOG_KEYS}
        n_steps = 0
        # HSIC magnitude-match accumulators (epoch 11 only).
        ce_sum = 0.0
        hsic_y_sum = 0.0
        # R-DISC-ACC: epoch-scoped train-stream disc monitor (grl/both only). The
        # multi-quality sampler's batches span the phase's active bins by
        # construction, so these accumulate balanced-acc material over ≥2 active
        # bins (the c23-only val pass collapses to a single bin — A0-HEALTHY (iii)
        # needs the active-bin balanced acc). Diagnostic-only: never checkpointed
        # (a mid-epoch resume just under-counts that one epoch's monitor).
        collect_disc = self.arm in _GRL_ARMS
        disc_preds_epoch: list[int] = []
        disc_bins_epoch: list[int] = []

        # W5b V3 (ema_own_bn_stats only): first step of the EMA BN-stats window.
        ema_bn_from = (
            len(self.train_loader) - _EMA_BN_WINDOW_STEPS
            if self.ema.own_bn_stats else None
        )
        for step_in_epoch, batch in enumerate(self.train_loader):
            # Mid-epoch resume: skip already-completed steps of this epoch.
            if step_in_epoch < self.start_step_in_epoch:
                continue
            if ema_bn_from is not None:
                self._ema_bn_observe_now = step_in_epoch >= ema_bn_from
            losses, raw_hsic_y, disc_pred_bin = self._train_step(
                batch, loss_w, disc_w, want_raw_hsic_y=in_hsic_match_epoch,
            )
            n_steps += 1
            for k in _LOSS_LOG_KEYS:
                epoch_sums[k] += float(losses[k].detach())
            if in_hsic_match_epoch and raw_hsic_y is not None:
                ce_sum += float(losses["cls"].detach())
                hsic_y_sum += float(raw_hsic_y)
            if collect_disc and disc_pred_bin is not None:
                disc_preds_epoch.extend(disc_pred_bin[0])
                disc_bins_epoch.extend(disc_pred_bin[1])

            # Step-level scalars every `step_log_every` (default 50) steps, rank 0.
            log_now = self.global_step % self.step_log_every == 0
            step_detail: dict[str, float] = {}
            if self.rank == 0 and self.step_log_detail and log_now:
                step_detail = self._log_step_detail(
                    losses, disc_pred_bin, active_levels,
                )
            if self.rank == 0 and self.tb is not None and log_now:
                step_scalars = {
                    f"loss_step/{k}": float(losses[k].detach())
                    for k in _LOSS_LOG_KEYS
                }
                step_scalars["lambda_p"] = self.grl_sched.lambda_p(self.global_step)
                if step_detail:
                    step_scalars["lambda_used"] = step_detail["lambda_used"]
                    step_scalars["diag_step/est_pm1"] = step_detail["est_pm1"]
                    step_scalars["diag_step/disc_bal_acc"] = step_detail["disc_bal_acc"]
                self.tb.log_scalars(step_scalars, self.global_step)

        # Freeze the HSIC magnitude-match scale at the END of epoch 11.
        if in_hsic_match_epoch:
            self._freeze_hsic_scale(ce_sum, hsic_y_sum, n_steps)

        # Stash the epoch's train-stream disc monitor for validate()'s diagnostics
        # (R-DISC-ACC). Empty for none/hsic arms; diagnostic-only, not checkpointed.
        self._disc_preds_epoch = disc_preds_epoch
        self._disc_bins_epoch = disc_bins_epoch

        # Train cls-loss epoch mean — stashed for the per-epoch stdout summary
        # (the A0-HEALTHY (i) "cls strictly ↓" monitor reads this from the log).
        self._last_epoch_cls = (
            epoch_sums["cls"] / n_steps if n_steps > 0 else float("nan")
        )
        # Raw per-epoch loss means (all _LOSS_LOG_KEYS) — stashed so the rank-0
        # epoch-end block can run the Phase-5.5 aux-dominance guardrail (D1) off the
        # SAME means the trainer already tracks. Computed on every rank (only rank 0
        # reads it); diagnostic-only, never checkpointed, no behaviour change.
        self._last_epoch_loss_means = (
            {k: epoch_sums[k] / n_steps for k in _LOSS_LOG_KEYS}
            if n_steps > 0 else {}
        )

        # Epoch-mean loss terms + LRs + λ + hsic_scale on rank 0.
        if self.rank == 0 and self.tb is not None and n_steps > 0:
            epoch_means = {
                f"loss/{k}": epoch_sums[k] / n_steps for k in _LOSS_LOG_KEYS
            }
            for gi, group in enumerate(self.optimizer.param_groups):
                epoch_means[f"lr/{group.get('name', gi)}"] = float(group["lr"])
            epoch_means["lambda_p"] = self.grl_sched.lambda_p(self.global_step)
            if self.hsic_scale is not None:
                epoch_means["hsic_scale"] = float(self.hsic_scale)
            self.tb.log_scalars(epoch_means, epoch)

    def _log_step_detail(
        self, losses: dict[str, Tensor],
        disc_pred_bin: tuple[list[int], list[int]] | None,
        active_levels: tuple[str, ...],
    ) -> dict[str, float]:
        """Emit the greppable per-step ``STEP`` line (``train.step_log_detail``).

        ``s`` is the 0-based global step whose forward used ``λ`` (so ``s=0`` has
        λ = 0 under the step-0 ramp and ``s=1`` has λ > 0). ``est_pm1`` is the
        train-batch estimator ±1-bin accuracy; ``disc_bal_acc`` the train-batch
        discriminator balanced accuracy over the bins present (nan without a
        discriminator, i.e. the none/hsic arms). Both are read from the
        already-computed forward outputs, so the step is numerically unchanged.
        """
        from src.training.diagnostics import disc_balanced_accuracy

        disc_bal = float("nan")
        if disc_pred_bin is not None and len(disc_pred_bin[0]) > 0:
            disc_bal, _ = disc_balanced_accuracy(
                disc_pred_bin[0], disc_pred_bin[1],
                num_active_bins=max(len(active_levels), 1),
            )
        detail = {
            "lambda_used": float(self._last_lambda),
            "est_pm1": float(self._last_step_est_pm1),
            "disc_bal_acc": float(disc_bal),
        }
        loss_txt = " ".join(
            f"{k}={float(losses[k].detach()):.6g}" for k in _LOSS_LOG_KEYS
        )
        _LOG.info(
            "STEP s=%d λ=%.10f | %s | est_pm1=%.4f disc_bal_acc=%.4f",
            self.global_step - 1, detail["lambda_used"], loss_txt,
            detail["est_pm1"], detail["disc_bal_acc"],
        )
        return detail

    def _freeze_hsic_scale(
        self, ce_sum: float, hsic_y_sum: float, n_steps: int
    ) -> None:
        """R-HSIC-GUARD: freeze ``s = mean(CE)/mean(HSIC_y)`` at epoch-11 end.

        If ``mean(HSIC_y) < 1e-6`` the keep-label term has collapsed (expected
        early in the ramp) → default ``s = 1.0`` (no rescale) and log a warning.
        We do NOT use ``max(denom, ε)`` — that injects a huge ``s`` and over-amplifies
        the HSIC term (the wrong direction). ``s`` then scales the 1:5 ratio to
        ``(s/5, s)`` for the rest of training (applied in :meth:`_apply_hsic_scale`).
        """
        if n_steps == 0:
            self.hsic_scale = 1.0
            return
        denom = hsic_y_sum / n_steps
        if denom < _EPS_HSIC:
            self.hsic_scale = 1.0
            _LOG.warning(
                "HSIC magnitude-match: mean(HSIC_y)=%.3g < %g at epoch-11 end; "
                "defaulting s=1.0 (no rescale)", denom, _EPS_HSIC,
            )
        else:
            self.hsic_scale = (ce_sum / n_steps) / denom
        _LOG.info("HSIC magnitude-match scale frozen: s=%.4g", self.hsic_scale)

    # =====================================================================
    # the per-step flow (EXACT order — the verifier checks this)
    # =====================================================================

    def _train_step(
        self, batch: dict[str, Any], loss_w, disc_w: Tensor | None,
        *, want_raw_hsic_y: bool = False,
    ) -> tuple[dict[str, Tensor], float | None, tuple[list[int], list[int]] | None]:
        """One optimizer step in the §4.3 order.

        Returns ``(losses, raw_hsic_y?, disc_pred_bin?)``. The third element is the
        train-stream discriminator monitor material (R-DISC-ACC / Option A): for the
        grl/both arms it is ``(argmax(disc_logits), bin_idx)`` as plain int lists,
        read from the **already-computed** forward outputs with ``.detach()`` — so it
        is RNG-neutral (no extra forward, no RNG draw) and does NOT touch the §4.3
        per-step order, the loss assembly, the optimizer, or EMA. It is ``None`` for
        the none/hsic arms (no discriminator).
        """
        # (1) move tensors to device; derive the split-BN clean mask (asserts >=0).
        images = batch["image"].to(self.device, non_blocking=True)
        labels = batch["label"].to(self.device, non_blocking=True)
        bin_idx = batch["bin_idx"].to(self.device, non_blocking=True)
        pair_index = batch["pair_index"].to(self.device, non_blocking=True)
        clean_mask = clean_mask_from_bin_idx(bin_idx)  # raises on −1 (let it)

        loss_batch = {"label": labels, "bin_idx": bin_idx, "pair_index": pair_index}

        # (2) set λ BEFORE this step's forward (captured at forward; Phase A ⇒ 0).
        if self.core.grl is not None:
            self.core.grl.set_lambda(self.grl_sched.lambda_p(self.global_step))
        # Phase 6 detail log: the λ this step's forward uses (pure read).
        detail_now = self.step_log_detail and (
            (self.global_step + 1) % self.step_log_every == 0
        )
        if detail_now:
            self._last_lambda = float(self.grl_sched.lambda_p(self.global_step))

        # (3) zero grads.
        self.optimizer.zero_grad(set_to_none=True)

        # (4) forward + losses under bf16 autocast (cpu in tests). `cfg.train.amp`
        #     gates it: "bf16" ⇒ autocast on (production); anything else (fp32/off)
        #     ⇒ autocast disabled ⇒ full fp32 — the `--deterministic` resume
        #     bit-equality path (A-SMOKE1R3: bf16 has an inherent ~1e-3 run-to-run
        #     floor, so bit-exactness requires fp32; `enabled=False` is a no-op ctx).
        use_amp = str(self.cfg.train.amp).lower() in ("bf16", "bfloat16")
        autocast_device = "cuda" if self.device.type == "cuda" else "cpu"
        with torch.autocast(autocast_device, dtype=torch.bfloat16, enabled=use_amp):
            fwd_kwargs: dict[str, Any] = {"clean_mask": clean_mask}
            if self._needs_bin_idx:
                fwd_kwargs["bin_idx"] = bin_idx
            outputs = self.fwd(images, **fwd_kwargs)
            losses = compute_losses(
                outputs, loss_batch, loss_w, self.arm, disc_weight=disc_w,
            )
        total = losses["total"]

        # (5) backward → grad-clip → step → EMA update → advance step.
        #     No all-params touch (R-CJ1b CORRECTED): under DDP with
        #     find_unused_parameters=True the unused trainable params (the
        #     all-clean Phase-A compressed sub-BN affine + any disconnected head)
        #     get grad-None → AdamW skips them → bit-identical, and FUP=True's
        #     reducer tolerates them. The old `0.0·Σ p.sum()` touch added a second
        #     autograd edge per param that FUP=True double-counts ("marked ready
        #     twice"), so it is retired.
        total.backward()
        torch.nn.utils.clip_grad_norm_(self.core.parameters(), self.cfg.train.grad_clip)
        self.optimizer.step()
        self.ema.update(self.core)
        if self._ema_bn_observe_now:  # W5b V3; never True with the flag off
            self._ema_observe_bn(images, fwd_kwargs, autocast_device, use_amp)
        self.global_step += 1

        # (6) HSIC magnitude-match raw keep-label term (epoch 11 accumulation).
        raw_hsic_y: float | None = None
        if want_raw_hsic_y:
            with torch.no_grad():
                _hx, hy = hsic_invariance_terms(
                    outputs["z_freq"].detach().float(), bin_idx, labels,
                    num_bins=self.num_bins,
                    sigma=getattr(loss_w, "hsic_sigma", "median"),
                    use_cka=getattr(loss_w, "hsic_cka", False),
                )
            raw_hsic_y = float(hy)

        # (6b) Phase 6 detail log: train-batch estimator ±1-bin accuracy, read
        #      from the already-computed outputs (.detach() ⇒ RNG-neutral).
        if detail_now and "crf_logits" in outputs:
            with torch.no_grad():
                est = outputs["crf_logits"].detach().argmax(dim=1)
                self._last_step_est_pm1 = float(
                    ((est - bin_idx).abs() <= 1).float().mean()
                )

        # (7) R-DISC-ACC train-stream disc monitor material (grl/both only). Read
        #     from the already-computed forward outputs (.detach() ⇒ RNG-neutral).
        disc_pred_bin: tuple[list[int], list[int]] | None = None
        if self.arm in _GRL_ARMS and "disc_logits" in outputs:
            disc_pred_bin = (
                outputs["disc_logits"].argmax(dim=1).detach().cpu().tolist(),
                bin_idx.detach().cpu().tolist(),
            )

        return losses, raw_hsic_y, disc_pred_bin

    @torch.no_grad()
    def _ema_observe_bn(
        self, images: Tensor, fwd_kwargs: dict[str, Any],
        autocast_device: str, use_amp: bool,
    ) -> None:
        """W5b V3: refresh the EMA shadow's BN stats from its own forward.

        Same batch, same forward kwargs (split-BN ``clean_mask``) and the same
        autocast as the training forward; run under a forked RNG so the training
        stream is the one the flag-off run would draw. No gradient, no parameter
        change; only the shadow's BN running stats move (``ModelEMA.observe_bn``).
        """
        devices: list[int] = []
        if self.device.type == "cuda":
            devices = [
                self.device.index if self.device.index is not None
                else torch.cuda.current_device()
            ]
        with torch.random.fork_rng(devices=devices):
            with torch.autocast(autocast_device, dtype=torch.bfloat16, enabled=use_amp):
                self.ema.observe_bn(self.core, images, **fwd_kwargs)

    def _warn_ema_bn_fallback(self, epoch: int) -> None:
        """W5b V3 (flag on only): log a fixed WARNING line when the EMA had no
        BN observation before this validation and the live BN stats were copied.

        The W5b watcher greps ``EMA-OWN-BN fallback``; any such line in V3 is a
        recorded deviation and an ESCALATION (W5b plan §5). The EPOCH line is
        unchanged.
        """
        if self.ema.last_copy_was_fallback:
            _LOG.warning(
                "EMA-OWN-BN fallback epoch %d: no observation window reached; "
                "live BN stats copied (fallbacks so far: %d)",
                epoch, self.ema.bn_fallback_count,
            )

    # =====================================================================
    # validation (rank 0, EMA model)
    # =====================================================================

    @torch.no_grad()
    def validate(
        self, epoch: int, active_levels: tuple[str, ...] | None = None,
        *,
        disc_preds: Sequence[int] | None = None,
        disc_bins: Sequence[int] | None = None,
    ) -> dict[str, Any]:
        """Validate on FFpp val c23/c40 with the EMA model; log §4.5 diagnostics.

        Returns a dict with the model-selection metric ``sel_metric =
        mean(val_auc_c23, val_auc_c40)`` (best checkpoint by this; val-based, never
        test), the two AUCs, the raw diagnostic materials, AND the Batch-4 rich
        diagnostic scalars merged from ``diagnostics.log_epoch_diagnostics`` —
        notably ``disc_balanced_acc`` / ``disc_chance`` / ``est_pm1_acc``, which
        Batch-6's A0-HEALTHY gate + the checkpoint metrics read.

        ``active_levels`` (the epoch's active CRF levels) sets the per-phase chance
        ``1/len(active_levels)`` (1/2 Phase A, 1/4 B, 1/6 C). When ``None`` (e.g. a
        bare ``validate(epoch)`` call in tests) it falls back to all configured
        levels, so the chance is the full-bin value.

        ``disc_preds`` / ``disc_bins`` (R-DISC-ACC / Option A): the epoch's
        TRAIN-STREAM discriminator monitor (argmax(disc_logits) vs true bin),
        accumulated over the multi-quality batches that span the phase's active
        bins. When provided (non-empty) they REPLACE the single-bin c23 val-pass
        disc materials, so ``disc_balanced_acc`` is a genuine balanced accuracy over
        the active bins and ``a_distance_mean`` is finite (the c23-only pass
        collapses both — A0-HEALTHY (iii) is unmeasurable from it). ``train()``
        threads in the stash filled by :meth:`_train_one_epoch`; the
        estimator-confusion / t-SNE / band-gates stay on the c23 pass.
        """
        # EMA buffers verbatim from live (incl. split-BN clean stats) before eval.
        self.ema.copy_buffers_from(self.core)
        if self.ema.own_bn_stats:  # W5b V3 only; never entered with the flag off
            self._warn_ema_bn_fallback(epoch)
        adapter = CAFRLEvalAdapter(self.ema.module)
        ev = Evaluator(self.cfg, self.device)

        cell_c23 = ev.evaluate(adapter, self.val_ds_c23, "c23")
        cell_c40 = ev.evaluate(adapter, self.val_ds_c40, "c40")
        auc_c23 = float(cell_c23.get("video_auc", float("nan")))
        auc_c40 = float(cell_c40.get("video_auc", float("nan")))
        sel = 0.5 * (auc_c23 + auc_c40)
        # Validation LOSS (frame-level BCE, EMA model) — tracked alongside AUC so a
        # best-epoch-by-val-loss can be compared to the protocol AUC selection. The
        # primary model-selection metric stays `sel` (mean val AUC, plan §6); this is
        # an additional curve + the `best_valloss.pt` checkpoint.
        loss_c23 = float(cell_c23.get("frame_bce", float("nan")))
        loss_c40 = float(cell_c40.get("frame_bce", float("nan")))
        val_loss = 0.5 * (loss_c23 + loss_c40)

        # -- F2 (Phase 5.4) mechanism readouts, spatial_residual arms only --------
        # residual_gamma trajectory (γ→0 ⇒ frequency discarded) + the standalone
        # val-AUC of the frequency-only `freq_logit` head (pre-registered readouts;
        # no gate). γ is logged EMA (the eval-relevant checkpoint value) AND live
        # (the training trajectory / smoke movement signal); both are also
        # recoverable from every epoch_*.pt. The freq-head AUC runs only for the
        # spatial_residual_full arm (the only kind that exposes freq_logit).
        f2_metrics: dict[str, Any] = {}
        core_fusion = self.core.fusion
        if hasattr(core_fusion, "residual_gamma"):
            f2_metrics["residual_gamma"] = float(
                self.ema.module.fusion.residual_gamma.detach()
            )
            f2_metrics["residual_gamma_live"] = float(
                core_fusion.residual_gamma.detach()
            )
        if getattr(self.core, "fusion_kind", None) == "spatial_residual_full":
            from src.models.cafrl import CAFRLFreqHeadEvalAdapter

            freq_adapter = CAFRLFreqHeadEvalAdapter(self.ema.module)
            fcell_c23 = ev.evaluate(freq_adapter, self.val_ds_c23, "c23")
            fcell_c40 = ev.evaluate(freq_adapter, self.val_ds_c40, "c40")
            fa_c23 = float(fcell_c23.get("video_auc", float("nan")))
            fa_c40 = float(fcell_c40.get("video_auc", float("nan")))
            f2_metrics["freq_auc_c23"] = fa_c23
            f2_metrics["freq_auc_c40"] = fa_c40
            f2_metrics["freq_auc_mean"] = 0.5 * (fa_c23 + fa_c40)

        # -- Phase 6 (val_raw): the RAW (live) model on the same val levels -------
        # Selection stays on the EMA `sel`. The pass runs under a forked RNG
        # (DataLoader iterators draw a base seed from the global RNG), so the
        # training stream is identical with the option on or off.
        raw_metrics: dict[str, Any] = {}
        if self.val_raw:
            raw_metrics = self._validate_raw(ev)

        diag = self._collect_diagnostics()

        # R-DISC-ACC: replace the single-bin c23 disc materials with the multi-bin
        # train-stream monitor (when supplied + non-empty) so disc_balanced_acc is a
        # real balanced accuracy over the phase's active bins and a_distance_mean is
        # finite. The estimator/t-SNE/band-gate materials stay on the c23 pass.
        if disc_preds is not None and disc_bins is not None and len(disc_preds) > 0:
            diag["disc_preds"] = list(disc_preds)
            diag["disc_bins"] = list(disc_bins)

        metrics: dict[str, Any] = {
            "val_auc_c23": auc_c23,
            "val_auc_c40": auc_c40,
            "sel_metric": sel,
            "val_loss_c23": loss_c23,
            "val_loss_c40": loss_c40,
            "val_loss": val_loss,
            **f2_metrics,
            **raw_metrics,
            **diag,
        }
        # §4.5 diagnostics: compute the rich metrics + log to TB (rank 0). t-SNE
        # is gated to its every-5-epochs cadence. The returned scalars (esp.
        # disc_balanced_acc / disc_chance / est_pm1_acc) merge into `metrics` so
        # Batch-6 + the checkpoint can read the disc-balanced-acc-vs-AUC monitor.
        if self.rank == 0:
            from src.training import diagnostics

            levels = active_levels if active_levels is not None else tuple(self.cfg.data.levels)
            extra_scalars = {
                "auc/c23": auc_c23, "auc/c40": auc_c40, "sel_metric": sel,
                "val_loss/c23": loss_c23, "val_loss/c40": loss_c40,
                "val_loss/mean": val_loss,
            }
            # F2 (Phase 5.4) mechanism scalars (γ trajectory + freq-head val-AUC).
            _f2_tb = {
                "residual_gamma": "diag/residual_gamma",
                "residual_gamma_live": "diag/residual_gamma_live",
                "freq_auc_c23": "auc/freq_c23",
                "freq_auc_c40": "auc/freq_c40",
                "freq_auc_mean": "auc/freq_mean",
            }
            extra_scalars.update(
                {tag: f2_metrics[k] for k, tag in _f2_tb.items() if k in f2_metrics}
            )
            if raw_metrics:
                extra_scalars.update({
                    "auc_raw/c23": raw_metrics["raw_val_auc_c23"],
                    "auc_raw/c40": raw_metrics["raw_val_auc_c40"],
                    "auc_raw/sel_metric": raw_metrics["raw_sel_metric"],
                })
            rich = diagnostics.log_epoch_diagnostics(
                self.tb, diag,
                epoch=epoch,
                active_levels=levels,
                num_bins=self.num_bins,
                extra_scalars=extra_scalars,
                log_tsne=(epoch % 5 == 0),
            )
            metrics.update(rich)
        return metrics

    @torch.no_grad()
    def _validate_raw(self, ev: Evaluator) -> dict[str, Any]:
        """Score the raw (live, non-EMA) model on val c23/c40 (``train.val_raw``).

        Kickoff §3: CAFRL-family runs log validation AUC for both raw and EMA
        weights. RNG-neutral (``fork_rng``) and mode-restoring, so training is
        unchanged; the selection metric is untouched.
        """
        devices: list[int] = []
        if self.device.type == "cuda":
            devices = [
                self.device.index if self.device.index is not None
                else torch.cuda.current_device()
            ]
        was_training = self.core.training
        with torch.random.fork_rng(devices=devices):
            adapter = CAFRLEvalAdapter(self.core)
            cell_c23 = ev.evaluate(adapter, self.val_ds_c23, "c23")
            cell_c40 = ev.evaluate(adapter, self.val_ds_c40, "c40")
        self.core.train(was_training)
        r23 = float(cell_c23.get("video_auc", float("nan")))
        r40 = float(cell_c40.get("video_auc", float("nan")))
        return {
            "raw_val_auc_c23": r23,
            "raw_val_auc_c40": r40,
            "raw_sel_metric": 0.5 * (r23 + r40),
        }

    @torch.no_grad()
    def _collect_diagnostics(self) -> dict[str, Any]:
        """Gather Batch-4 diagnostic materials from a val subset (no rich metrics).

        Runs the EMA model (with ``discriminator.eval()`` if present) over a small
        val-c23 subset to collect the §4.5 materials
        (``src.training.diagnostics.log_epoch_diagnostics`` consumes this dict):

        * ``disc_preds`` / ``disc_bins`` — disc balanced-acc + A-distance;
        * ``band_gates`` ``(N, num_bands)`` + ``gate_bins`` ``(N,)`` — gate-per-bin;
        * ``est_preds`` / ``est_bins`` — estimator confusion + ±1-bin;
        * ``stream_feats`` ``list[(N, D)]`` — per-stream cosines;
        * ``z_freq`` ``(N, D)`` + ``labels`` ``(N,)`` + ``z_bins`` ``(N,)`` — t-SNE.

        This is a **c23-only** pass, so every true CRF bin is ``1`` (c23 = bin 1);
        the per-bin diagnostics still render (one present bin). Returns empty
        containers if there are no val samples (e.g. an empty subset).
        """
        model = self.ema.module
        model.eval()
        disc = getattr(model, "discriminator", None)
        if disc is not None:
            disc.eval()

        empty: dict[str, Any] = {
            "disc_preds": [], "disc_bins": [], "band_gates": None,
            "gate_bins": [], "est_preds": [], "est_bins": [],
            "stream_feats": None, "z_freq": None, "labels": [], "z_bins": [],
        }
        disc_preds: list[int] = []
        disc_bins: list[int] = []
        gate_chunks: list[Tensor] = []
        gate_bins: list[int] = []
        est_preds: list[int] = []
        est_bins: list[int] = []
        labels: list[int] = []
        z_bins: list[int] = []
        zfreq_chunks: list[Tensor] = []
        stream_chunks: list[list[Tensor]] | None = None

        # A small fixed val subset for the diagnostic pass (cheap; the rich metrics
        # are computed from these in `diagnostics`). Reuse the eval-collate loader.
        from src.evaluation.evaluator import eval_collate

        n_collect = min(len(self.val_ds_c23), 256)
        if n_collect == 0:
            return empty
        loader = DataLoader(
            torch.utils.data.Subset(self.val_ds_c23, list(range(n_collect))),
            batch_size=self.cfg.data.batch_size, shuffle=False,
            collate_fn=eval_collate, num_workers=0,
        )
        for batch in loader:
            images = batch["image"].to(self.device, non_blocking=True)
            bsz = int(images.shape[0])
            out = model(images)  # all-clean eval path (no bin_idx/clean_mask)
            crf_logits = out["crf_logits"]
            est_preds.extend(crf_logits.argmax(dim=1).cpu().tolist())
            est_bins.extend([1] * bsz)  # c23 → true bin 1
            labels.extend([int(x) for x in batch["label"]])
            z_bins.extend([1] * bsz)
            zfreq_chunks.append(out["z_freq"].detach().float().cpu())
            if out.get("band_gates") is not None:
                gate_chunks.append(out["band_gates"].detach().float().cpu())
                gate_bins.extend([1] * bsz)
            sf = out.get("stream_feats")
            if sf is not None:
                if stream_chunks is None:
                    stream_chunks = [[] for _ in sf]
                for k, s in enumerate(sf):
                    stream_chunks[k].append(s.detach().float().cpu())
            if disc is not None and "disc_logits" in out:
                disc_preds.extend(out["disc_logits"].argmax(dim=1).cpu().tolist())
                disc_bins.extend([1] * bsz)  # c23 → true bin 1

        band_gates = (
            torch.cat(gate_chunks, dim=0).numpy() if gate_chunks else None
        )
        z_freq = (
            torch.cat(zfreq_chunks, dim=0).numpy() if zfreq_chunks else None
        )
        stream_feats = (
            [torch.cat(chunks, dim=0).numpy() for chunks in stream_chunks]
            if stream_chunks is not None else None
        )
        return {
            "disc_preds": disc_preds, "disc_bins": disc_bins,
            "band_gates": band_gates, "gate_bins": gate_bins,
            "est_preds": est_preds, "est_bins": est_bins,
            "stream_feats": stream_feats, "z_freq": z_freq,
            "labels": labels, "z_bins": z_bins,
        }

    # =====================================================================
    # checkpoint / resume (mid-epoch capable)
    # =====================================================================

    def _gather_per_rank_rng(self) -> list[dict[str, Any]] | None:
        """Collect each rank's OWN RNG state (CPU/active-CUDA/numpy/python).

        **Collective — must be called on EVERY rank** when a process group is live
        (``dist.all_gather_object`` synchronizes all ranks). Returns an ordered list
        (index == rank) of per-rank ``own_rng_state`` payloads under DDP, or
        ``None`` for the single-process path (so the legacy single-process RNG form
        is stored, preserving single-GPU/CPU bit-exactness — F1).
        """
        if not (self.world_size > 1 and dist.is_available() and dist.is_initialized()):
            return None
        local = ckpt.own_rng_state()
        gathered: list[dict[str, Any]] = [None] * self.world_size  # type: ignore[list-item]
        dist.all_gather_object(gathered, local)
        return gathered

    def save_checkpoint(
        self, epoch: int, *, is_best: bool, is_best_valloss: bool = False,
        step_in_epoch: int | None = None,
    ) -> Path | None:
        """Save a full resumable checkpoint via ``utils/checkpoint.save_checkpoint``.

        ``extra`` carries ``global_step`` / ``hsic_scale`` / ``step_in_epoch`` so a
        resume rebuilds the exact training position. ``save_rng=True`` captures the
        torch/numpy/python RNG (data-order + augmentation continue identically).
        ``step_in_epoch`` (default ``None`` = an epoch boundary, i.e. 0) records a
        mid-epoch save point for the §4.6 / Gate-4 mid-epoch resume.

        **Under DDP (F1):** this method runs a per-rank RNG gather (an
        ``all_gather_object`` collective), so it **must be invoked on every rank**
        — only rank 0 writes the file, but it now carries ALL ranks' own RNG states
        so each rank restores its OWN active-device CUDA RNG on resume. Returns the
        snapshot path on rank 0 and ``None`` on non-zero ranks (or single-process).
        """
        # Collective FIRST (all ranks), before the rank-0-only file write.
        per_rank_rng = self._gather_per_rank_rng()
        if self.world_size > 1 and self.rank != 0:
            return None
        extra = {
            "global_step": int(self.global_step),
            "hsic_scale": self.hsic_scale,
            "step_in_epoch": int(step_in_epoch or 0),
        }
        return ckpt.save_checkpoint(
            self.run_dir,
            model=self.core,
            ema_model=self.ema.module,
            optimizer=self.optimizer,
            scheduler=self.lr_scheduler,
            epoch=int(epoch),
            best_metric=float(self.best_metric),
            config=self.cfg,
            is_best=is_best,
            is_best_valloss=is_best_valloss,
            extra=extra,
            save_rng=True,
            per_rank_rng=per_rank_rng,
        )

    def load_checkpoint(self, path: Path | str) -> None:
        """Restore full training state for ``--resume`` (mid-epoch capable).

        Restores core/ema/optimizer/scheduler + RNG via ``checkpoint.load_checkpoint``,
        then ``global_step`` / ``best_metric`` / ``hsic_scale`` and the resume
        position: if the checkpoint was taken **mid-epoch** (``step_in_epoch > 0``)
        we resume INTO the same epoch and fast-forward the loader by that many
        batches (the sampler plan is deterministic from seed+epoch, so the post-skip
        batch sequence is identical); otherwise we start at ``epoch + 1``.
        """
        payload = ckpt.load_checkpoint(
            path,
            model=self.core,
            ema_model=self.ema.module,
            optimizer=self.optimizer,
            scheduler=self.lr_scheduler,
            map_location=str(self.device),
            restore_rng=True,
            rank=self.rank,  # F1: restore THIS rank's own per-rank RNG entry
        )
        extra = payload.get("extra") or {}
        self.global_step = int(extra.get("global_step", 0))
        self.best_metric = float(payload.get("best_metric", float("-inf")))
        self.hsic_scale = extra.get("hsic_scale", None)
        saved_epoch = int(payload.get("epoch", 0))
        step_in_epoch = int(extra.get("step_in_epoch", 0))
        if step_in_epoch > 0:
            # Mid-epoch resume: continue the same epoch, skip done steps.
            self.start_epoch = saved_epoch
            self.start_step_in_epoch = step_in_epoch
        else:
            self.start_epoch = saved_epoch + 1
            self.start_step_in_epoch = 0
