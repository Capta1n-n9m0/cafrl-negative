"""CAFRL configuration tree (defaults).

Nested dataclasses holding every default from `docs/implementation-plan.md` §9
(reconciled with `docs/phases/phase1.md` Step 1.1 — phase1.md wins on conflict).

Conventions: type hints everywhere; dataclass configs (no argparse). Path fields
are stored as ``~/...`` strings and resolved on demand via ``resolve_path`` /
``PathsConfig.resolved`` so the defaults stay human-readable and portable.
The YAML deep-merge loader and ``dump`` live in ``load.py``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

def resolve_path(p: str | Path) -> Path:
    """Expand ``~`` and environment variables, returning an absolute ``Path``."""
    return Path(p).expanduser().resolve()


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

@dataclass
class PathsConfig:
    """Filesystem roots. Stored as ``~/...`` strings; resolve via ``resolved``."""

    faces_root: str = "~/sdb/datasets/ff++/faces"
    celebdf_root: str = "~/sdb/datasets/celeb-df-v2/faces"
    crf_video_root: str = "~/sdc/datasets/ffpp_crf_variants"
    dataset_root: str = "~/sdc/datasets/ffpp_original"
    splits_dir: str = "src/config/splits"
    metadata_csv: str = "${METADATA_CSV}"
    runs_root: str = "${RUNS_ROOT}"

    def resolved(self, name: str) -> Path:
        """Return the resolved ``Path`` for a named path field."""
        return resolve_path(getattr(self, name))


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

@dataclass
class DataConfig:
    levels: tuple[str, ...] = ("c0", "c23", "c28", "c32", "c36", "c40")
    frames_per_video: int = 32
    methods: tuple[str, ...] = ("Deepfakes", "Face2Face", "FaceSwap", "NeuralTextures")
    quality_mix: tuple[float, float, float] = (0.3, 0.4, 0.3)
    paired_fraction: float = 0.25
    real_oversample: int = 4
    batch_size: int = 32
    num_workers: int = 8
    # 6 ordinal bins (index 0-5); c0 exists in training data, so 6 not G2's 5
    # (reconciliation: implementation-plan.md §11.1).
    bin_levels: tuple[str, ...] = ("c0", "c23", "c28", "c32", "c36", "c40")
    soft_label_eps: float = 0.1


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

@dataclass
class DCTConfig:
    block: int = 8
    band_sizes: tuple[int, ...] = (6, 10, 20, 28)
    band_channels: int = 64
    # Per-coefficient normalization of the DCT coefficients fed to the band
    # convs (phase2.md Step 2.1). "log1p" = sign(c)·log1p(|c|) (default, bounded-
    # ish, sign-preserving). "raw" = passthrough. "standardize" (per-coefficient
    # train-set stats) is the T2 ablation hook — raises NotImplementedError until
    # built.
    coeff_norm: str = "log1p"
    # DCT conv input layout. "channelized" = coefficients as channels at block-
    # grid resolution (default; 1×1 intra ∥ 3×3 inter convs). "pixel" = literal
    # pixel-tiled DCT map with true dilation-8 inter-block convs — ablation hook
    # A4, raises NotImplementedError until built.
    layout: str = "channelized"


@dataclass
class PhaseConfig:
    window: int = 32
    channels: tuple[int, ...] = (64, 128, 256)
    head_pairs: int = 32


@dataclass
class EstimatorConfig:
    emb_dim: int = 64
    num_bins: int = 6
    joint_training: bool = True


@dataclass
class FusionConfig:
    # Fusion merge arm (A3 ablation + the spatial-residual salvage variant).
    #   "cmam" (default)     — Zhao CMAM 3-modal channel attention + He cleanup.
    #   "sum" / "concat"     — demoted-fusion ablation baselines (G5 §1.1).
    #   "spatial_residual"   — SALVAGE variant: the pooled spatial vector drives the
    #                          PRIMARY logit; frequency (z_freq) is a ZERO-INIT
    #                          residual correction (residual_gamma=0 at init), so the
    #                          model starts as an exact spatial classifier and can
    #                          only add frequency if it learns γ≠0 (do-no-harm).
    #   "spatial_residual_full" — F2 (audit D4): the same residual head, but the
    #                          spatial logit taps the FULL backbone rep (GAP(1280),
    #                          b7's representation) via `backbone_full_head=True`
    #                          instead of GAP(F_spat); exposes `freq_logit` for the
    #                          aux-BCE deadlock-breaker (D2).
    kind: str = "cmam"
    stream_dim: int = 256


@dataclass
class DiscriminatorConfig:
    hidden: int = 1024
    dropout: float = 0.5
    spectral_norm: bool = True


class InvarianceArm(str, Enum):
    """Compression-invariance mechanism (A1 bake-off — G1)."""

    NONE = "none"
    GRL = "grl"
    HSIC = "hsic"
    BOTH = "both"
    CONTRASTIVE = "contrastive"


@dataclass
class ModelConfig:
    dct: DCTConfig = field(default_factory=DCTConfig)
    phase: PhaseConfig = field(default_factory=PhaseConfig)
    estimator: EstimatorConfig = field(default_factory=EstimatorConfig)
    fusion: FusionConfig = field(default_factory=FusionConfig)
    discriminator: DiscriminatorConfig = field(default_factory=DiscriminatorConfig)
    invariance_arm: InvarianceArm = InvarianceArm.GRL
    backbone: str = "efficientnet_b0"
    # Phase 5.4 (F2, audit D4). When True, the spatial backbone keeps EfficientNet-
    # B0's `conv_head` (320→1280, pretrained) and exposes the pooled 1280-d
    # representation b7 uses; `SpatialBackbone(full_head=True)`. The F_spat
    # (B,256,8,8) contract for the freq/alignment path is preserved (proj rebuilt
    # 1280→256). REQUIRED by `fusion.kind == "spatial_residual_full"` (CAFRL raises
    # if that kind is set without this). Default False ⇒ every pre-5.4 arm builds
    # the 320-tap `features_only` trunk byte-identically.
    backbone_full_head: bool = False
    # A2 ablation arm for the compression-conditioned band gate (phase2.md Step
    # 2.4). Crosses two modules: the gate arm (``attention.ConditionedBandGate``)
    # AND the DCT concat-emb plumbing (``dct.BlockDCTStream(concat_emb=...)``).
    #   "estimated" (default, A2b) — FiLM from the estimator's q_emb;
    #   "oracle"    (A2c)          — FiLM from an embedded true CRF bin;
    #   "none"                     — unconditioned gate g = softplus(b);
    #   "concat"    (negative ctrl)— gate degrades to "none" and q_emb is
    #                                channel-concatenated in dct.encode instead.
    conditioning: str = "estimated"
    # The fusion merge arm (A3 ablation) lives at ``fusion.kind`` — the nested
    # FusionConfig is the single source of truth (phase3.md writes `fusion.kind`;
    # orchestrator ruling R20, 2026-06-13 — a flat duplicate here was removed).
    # A2 ablation arm for the compression-conditioned *fusion* gate (phase3.md
    # Step 3.2, R11) — mirrors ``conditioning`` but for the FiLM fusion gate
    # (independent axis: A2 crosses band/fusion arms). "estimated" (default) FiLM
    # from q_emb; "oracle" module-local nn.Embedding(6,64) of the true bin (rejects
    # bin_idx<0, c18-incompatible); "none" no FiLM/embedding params; "concat" no
    # FiLM, q_emb concatenated onto both CMAM squeeze vectors.
    fusion_conditioning: str = "estimated"


# ---------------------------------------------------------------------------
# Loss
# ---------------------------------------------------------------------------

@dataclass
class LossConfig:
    cls_smoothing: float = 0.05
    w_crf: float = 0.2
    w_div: float = 1.0
    # Phase 5.4 (F2, audit D2). Weight on the auxiliary BCE on the residual arm's
    # `freq_logit` — gives the frequency path label supervision REGARDLESS of the
    # residual γ, breaking the γ=0 deadlock (at γ=0 the main logit sends the freq
    # path zero label gradient, so γ→0 is otherwise self-sealing). Applied only when
    # `outputs` carries `freq_logit` (the spatial_residual_full arm) AND w_freq_aux>0.
    # Default 0.0 ⇒ every existing arm's loss is byte-identical. F2 uses 0.2.
    w_freq_aux: float = 0.0
    # Diversity-loss cosine margin s_max (phase3.md Step 3.2, R18; Zhao publishes
    # no margin — CAFRL default, sweep if R_div is inert or dominant).
    div_s_max: float = 0.3
    w_cons: float = 0.5  # -> 0.3 in Phase C
    w_phase: float = 0.3
    w_circ_rel: float = 0.2
    grl_lambda_max: float = 0.5
    hsic_ratio: tuple[float, float] = (1.0, 5.0)
    # HSIC RBF bandwidth policy (Batch-3 / R18): "median" heuristic (default),
    # "5sqrt_d" (HBaR App. E), or a numeric string parsed as a fixed σ upstream.
    hsic_sigma: str = "median"
    # Optional CKA normalization of the HSIC terms (R18) — [0,1] range, magnitude-
    # stable in the phase-varying loss mix.
    hsic_cka: bool = False


# ---------------------------------------------------------------------------
# Train
# ---------------------------------------------------------------------------

# Valid ``TrainConfig.grl_ramp`` values (see the field's comment).
GRL_RAMPS: tuple[str, ...] = ("phase_anchored", "from_step0")


@dataclass
class TrainConfig:
    lr_freq: float = 1e-4
    lr_backbone: float = 1e-5
    lr_disc: float = 1e-4
    weight_decay: float = 1e-4
    epochs: int = 50
    phase_bounds: tuple[int, int] = (10, 25)
    # Curriculum mode (phase5.3 F1 — the fair-frequency test).
    #   "baby_step" (default) — the 3-phase progressive curriculum (Phase A/B/C:
    #                           accumulating CRF levels, backbone frozen in A, and
    #                           the per-phase w_cons/w_phase STEP overrides). Every
    #                           pre-5.3 run/test is byte-identical under this default.
    #   "flat"                — all 6 CRF levels every epoch, backbone NEVER frozen,
    #                           and the YAML loss weights GOVERN VERBATIM (no per-phase
    #                           w_cons/w_phase override). This is the audit-D1 fix:
    #                           baby_step HARDCODES w_cons/w_phase so YAML zeros are
    #                           ignored; flat lets a zero-invariance F1 arm train
    #                           frequency free of compression-invariance pressure at
    #                           the baseline's optimization recipe.
    curriculum: str = "baby_step"
    ema_decay: float = 0.999
    grad_clip: float = 1.0
    amp: str = "bf16"
    seed: int = 42
    # --- Phase 6 (Revision 1, W0) options. Every default reproduces the f2e3558
    # trainer bit for bit (decision "Phase 6 build: default options must reproduce
    # the old code bit for bit"); new runs opt in through their YAML. -------------
    # GRL λ ramp origin (lesson L1).
    #   "phase_anchored" (default) — the ramp starts at curriculum Phase B
    #       (`phase_bounds[0]`), even in flat mode, so λ ≡ 0 for epochs 1..10.
    #   "from_step0" — the DANN ramp λ = λmax·(2/(1+e^(−10p)) − 1) with
    #       p = global_step / total_steps, total_steps summed over ALL epochs. This
    #       is E1's ramp (decision "Revision 1 W0: adversary tested as designed,
    #       ramp from step 0"). Ignored by arms without a GRL.
    grl_ramp: str = "phase_anchored"
    # Step-scalar cadence in global steps (was the module constant
    # `_STEP_LOG_EVERY = 50`). The smoke sets 1 to log λ at every step.
    step_log_every: int = 50
    # When True, every `step_log_every` steps also emit a greppable `STEP` line
    # (step, λ used, losses, train-batch est_pm1 and disc_bal_acc) to the log and
    # add est_pm1/disc_bal_acc to the step TB scalars. Read-only on the forward
    # outputs, so training numerics are unchanged.
    step_log_detail: bool = False
    # When True, each validation also scores the RAW (live) model on the same val
    # levels and logs its AUCs next to the EMA ones. Selection is unchanged (EMA).
    # The extra pass runs under a forked RNG, so the training stream is unchanged.
    val_raw: bool = False
    # W5b V3 (the post hoc EMA-fix arm; diagnosis runs/phase6_build/steps/
    # W5b-S0.diagnosis.md). When True, the EMA
    # shadow keeps BatchNorm running stats computed from its OWN weights (an extra
    # no-grad forward of the shadow on each of the last steps of every epoch, see
    # trainer `_EMA_BN_WINDOW_STEPS`) instead of the live model's copied stats.
    # False (default) is the original EMA, unchanged.
    ema_own_bn_stats: bool = False

    def __setattr__(self, name: str, value: object) -> None:
        """Reject an unknown ``grl_ramp`` when the config is built or loaded.

        Runs on dataclass ``__init__`` and on every ``load_config`` merge (it sets
        fields with ``setattr``), so a typo in a YAML fails at load time, not at
        ``Trainer.__init__`` (S2 2b verifier, NIT 6).
        """
        if name == "grl_ramp" and value not in GRL_RAMPS:
            raise ValueError(
                f"train.grl_ramp must be one of {list(GRL_RAMPS)}; got {value!r}"
            )
        super().__setattr__(name, value)


# ---------------------------------------------------------------------------
# Eval
# ---------------------------------------------------------------------------

@dataclass
class EvalConfig:
    bootstrap_b: int = 10_000
    frames_per_video: int = 32
    ci: float = 0.95


# ---------------------------------------------------------------------------
# Top-level config
# ---------------------------------------------------------------------------

@dataclass
class Config:
    paths: PathsConfig = field(default_factory=PathsConfig)
    data: DataConfig = field(default_factory=DataConfig)
    model: ModelConfig = field(default_factory=ModelConfig)
    loss: LossConfig = field(default_factory=LossConfig)
    train: TrainConfig = field(default_factory=TrainConfig)
    eval: EvalConfig = field(default_factory=EvalConfig)

    def dump(
        self, run_dir: Path | str, filename: str = "config.yaml",
        *, provenance: dict | None = None,
    ) -> Path:
        """Write the fully-resolved config as YAML into ``run_dir``.

        Thin wrapper over ``load.dump_config`` (lazy import avoids a cycle);
        ``provenance`` adds the optional top-level run-provenance record.
        """
        from .load import dump_config

        return dump_config(self, run_dir, filename=filename, provenance=provenance)
