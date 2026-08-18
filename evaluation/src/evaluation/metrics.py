"""Evaluation metrics (phase1.md Step 1.8 `metrics.py`).

The primary protocol metric is **video-level AUC** (implementation-plan.md §6):
mean-pool the per-frame fake scores over the 32 sampled frames of a video, then
take the ROC AUC over videos. Every reported cell additionally carries a **95%
bootstrap CI whose resampling unit is the video** (B = 10,000), and a
frame-level AUC column is reported for literature comparability.

Functions
---------
* ``frame_auc(scores, labels)``      — frame-level ROC AUC (sklearn).
* ``video_scores(frame_scores, video_ids, frame_labels)`` — mean-pool per video,
  returning aligned ``(video_score, video_label)`` arrays.
* ``video_auc(frame_scores, video_ids, frame_labels)`` — video-level AUC.
* ``bootstrap_ci(scores, labels, ...)`` — percentile CI, resample = video,
  degenerate single-class resamples redrawn (count returned + logged).
* ``crf_slope(aucs)`` / ``crf_std(aucs)`` — the compression-robustness statistics
  (linear fit of AUC vs numeric CRF, and the std-of-AUC across levels).

CRF x-axis convention
---------------------
``crf_slope`` fits AUC against a *numeric* CRF. libx264 CRF is defined on [0, 51];
``c0`` is FFV1/near-lossless rather than a true CRF, so we map it to the numeric
value **0** (the natural floor of the CRF axis — implementation-plan.md §6 reports
the sweep over CRF {0, 18, 23, 28, 32, 36, 40} with c0 sitting at 0). Level names
are parsed as ``c{N}`` → ``N``; this choice is documented here and in the slope's
docstring so the centerpiece "AUC vs CRF" figure has a stated x-axis.
"""

from __future__ import annotations

import logging
import math
from collections.abc import Sequence
from typing import Any

import numpy as np
from sklearn.metrics import roc_auc_score

_LOG = logging.getLogger(__name__)

# Array-likes accepted throughout.
ArrayLike = Sequence[float] | np.ndarray
LabelLike = Sequence[int] | np.ndarray
IdLike = Sequence[str] | np.ndarray


# ---------------------------------------------------------------------------
# Frame-level AUC
# ---------------------------------------------------------------------------

def frame_auc(scores: ArrayLike, labels: LabelLike) -> float:
    """Frame-level ROC AUC over per-frame fake-probabilities/logits.

    ``scores`` may be probabilities or monotone logits — AUC is rank-based so the
    scale is irrelevant. Raises ``ValueError`` if a single class is present (AUC
    is undefined).
    """
    s = np.asarray(scores, dtype=np.float64).reshape(-1)
    y = np.asarray(labels).reshape(-1).astype(np.int64)
    if s.shape != y.shape:
        raise ValueError(f"scores {s.shape} and labels {y.shape} length mismatch")
    if np.unique(y).size < 2:
        raise ValueError("frame_auc needs both classes present")
    return float(roc_auc_score(y, s))


# ---------------------------------------------------------------------------
# Video-level pooling + AUC
# ---------------------------------------------------------------------------

def pool_by_key(
    frame_scores: ArrayLike,
    keys: IdLike,
    frame_labels: LabelLike,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Mean-pool frames per key → ``(keys, scores, labels)`` in appearance order.

    The keyed primitive behind :func:`video_scores` (which drops the keys). The
    Phase-5 paired-Δ aggregator needs the per-video **keys** so it can align arms /
    seeds / CRF levels **by key** rather than assume positional alignment across
    separately-loaded passes. ``keys`` is the per-frame pooling key (the
    ``(video_id, method)`` composite for FF++). Returns the distinct keys (object
    array), the per-key mean score, and the per-key label, all ordered by first
    appearance of the key. A key whose frames carry inconsistent labels raises.
    """
    s = np.asarray(frame_scores, dtype=np.float64).reshape(-1)
    k = np.asarray(keys).reshape(-1)
    y = np.asarray(frame_labels).reshape(-1).astype(np.int64)
    if not (s.shape == k.shape == y.shape):
        raise ValueError(
            f"length mismatch: scores {s.shape}, keys {k.shape}, labels {y.shape}"
        )

    order: list[str] = []
    sums: dict[str, float] = {}
    counts: dict[str, int] = {}
    label_of: dict[str, int] = {}
    for score, key, lab in zip(s, k, y):
        key = str(key)
        if key not in sums:
            order.append(key)
            sums[key] = 0.0
            counts[key] = 0
            label_of[key] = int(lab)
        elif label_of[key] != int(lab):
            raise ValueError(
                f"inconsistent labels for key {key!r}: "
                f"{label_of[key]} vs {int(lab)}"
            )
        sums[key] += float(score)
        counts[key] += 1

    out_keys = np.array(order, dtype=object)
    out_scores = np.array([sums[v] / counts[v] for v in order], dtype=np.float64)
    out_labels = np.array([label_of[v] for v in order], dtype=np.int64)
    return out_keys, out_scores, out_labels


def video_scores(
    frame_scores: ArrayLike,
    video_ids: IdLike,
    frame_labels: LabelLike,
) -> tuple[np.ndarray, np.ndarray]:
    """Mean-pool frame scores per video.

    Args:
        frame_scores: per-frame fake scores, length N.
        video_ids: per-frame video id (the grouping key), length N.
        frame_labels: per-frame label (0/1), length N. A video's label is the
            label shared by its frames (asserted consistent).

    Returns:
        ``(scores, labels)`` aligned arrays, one entry per distinct video, ordered
        by first appearance of the video id. ``scores`` is the per-video mean of
        frame scores; ``labels`` the per-video label. Thin wrapper over
        :func:`pool_by_key` (which additionally returns the keys).
    """
    _keys, out_scores, out_labels = pool_by_key(frame_scores, video_ids, frame_labels)
    return out_scores, out_labels


def video_auc(
    frame_scores: ArrayLike,
    video_ids: IdLike,
    frame_labels: LabelLike,
) -> float:
    """Video-level ROC AUC: mean-pool per video, then AUC over videos."""
    vs, vy = video_scores(frame_scores, video_ids, frame_labels)
    if np.unique(vy).size < 2:
        raise ValueError("video_auc needs both classes present")
    return float(roc_auc_score(vy, vs))


# ---------------------------------------------------------------------------
# Bootstrap CI (resampling unit = video)
# ---------------------------------------------------------------------------

def bootstrap_ci(
    video_scores_arr: ArrayLike,
    labels: LabelLike,
    b: int = 10_000,
    ci: float = 0.95,
    seed: int = 0,
    return_redraws: bool = False,
) -> tuple[float, float] | tuple[float, float, int]:
    """Percentile bootstrap CI of the AUC, **resampling videos** (not frames).

    Each bootstrap replicate draws ``n`` videos with replacement (``n`` = number
    of videos) and recomputes the AUC over those video-level scores/labels. A
    replicate that lands on a single class is **degenerate** (AUC undefined) and
    is **redrawn** until both classes appear; the total redraw count is logged
    and optionally returned.

    Args:
        video_scores_arr: per-video pooled scores (length n) — already pooled by
            :func:`video_scores`.
        labels: per-video labels (length n).
        b: number of bootstrap replicates.
        ci: central interval mass (0.95 → 2.5/97.5 percentiles).
        seed: RNG seed (reproducible).
        return_redraws: if True, return ``(lo, hi, n_redraws)``.

    Returns:
        ``(lo, hi)`` (or ``(lo, hi, n_redraws)``). Both endpoints are AUCs.
    """
    s = np.asarray(video_scores_arr, dtype=np.float64).reshape(-1)
    y = np.asarray(labels).reshape(-1).astype(np.int64)
    if s.shape != y.shape:
        raise ValueError(f"scores {s.shape} and labels {y.shape} length mismatch")
    n = s.shape[0]
    if n == 0:
        raise ValueError("bootstrap_ci needs at least one video")
    if np.unique(y).size < 2:
        raise ValueError("bootstrap_ci needs both classes present in the videos")

    rng = np.random.default_rng(seed)
    aucs = np.empty(b, dtype=np.float64)
    n_redraws = 0
    for i in range(b):
        while True:
            idx = rng.integers(0, n, size=n)
            yi = y[idx]
            if np.unique(yi).size >= 2:
                break
            n_redraws += 1  # degenerate single-class resample — redraw
        aucs[i] = roc_auc_score(yi, s[idx])

    alpha = (1.0 - ci) / 2.0
    lo = float(np.quantile(aucs, alpha))
    hi = float(np.quantile(aucs, 1.0 - alpha))
    if n_redraws:
        _LOG.info(
            "bootstrap_ci: redrew %d degenerate single-class resamples (b=%d)",
            n_redraws, b,
        )
    if return_redraws:
        return lo, hi, n_redraws
    return lo, hi


# ---------------------------------------------------------------------------
# Compression-robustness statistics
# ---------------------------------------------------------------------------

def _level_to_crf(level: str) -> float:
    """Map a level name ``c{N}`` to a numeric CRF; ``c0`` → 0.0 (axis floor).

    libx264 CRF is on [0, 51]. ``c0`` is our near-lossless source level, mapped
    to the numeric floor 0 so it sits at the left of the AUC-vs-CRF sweep
    (implementation-plan.md §6).
    """
    if not level.startswith("c"):
        raise ValueError(f"unrecognized level name {level!r} (expected 'c<N>')")
    return float(int(level[1:]))


def crf_slope(aucs: dict[str, float]) -> float:
    """Slope of a linear fit of video-AUC vs numeric CRF (degradation slope).

    ``aucs`` maps level names (``c0``, ``c23``, ...) to their video-level AUC. The
    x-axis is the numeric CRF (``c0`` → 0; see ``_level_to_crf``). A more negative
    slope means faster degradation under compression. Needs ≥ 2 distinct CRF
    points; raises ``ValueError`` otherwise.
    """
    if len(aucs) < 2:
        raise ValueError("crf_slope needs at least 2 levels")
    xs = np.array([_level_to_crf(k) for k in aucs], dtype=np.float64)
    ys = np.array([float(v) for v in aucs.values()], dtype=np.float64)
    if np.unique(xs).size < 2:
        raise ValueError("crf_slope needs at least 2 distinct CRF values")
    slope, _intercept = np.polyfit(xs, ys, deg=1)
    return float(slope)


def crf_std(aucs: dict[str, float]) -> float:
    """Population std of AUC across the swept levels (robustness spread).

    A smaller std = more compression-robust. Uses ``ddof=0`` (population std) so
    the statistic is well-defined for a single point (→ 0.0).
    """
    if not aucs:
        raise ValueError("crf_std needs at least 1 level")
    ys = np.array([float(v) for v in aucs.values()], dtype=np.float64)
    return float(np.std(ys, ddof=0))


# ---------------------------------------------------------------------------
# Paired AUC-difference bootstrap (the Phase-5 A1 / STOP-gate PRIMARY test)
# ---------------------------------------------------------------------------
#
# The decisive inter-arm test of phase5.md Step 5.2 (CRUX-3): a PAIRED
# video-resampling bootstrap. For arm-A vs arm-B scored on the SAME ordered set of
# videos, each replicate draws ONE shared video-index vector (identical across both
# arms ⇒ pairing) and records Δ_r = AUC_A − AUC_B on it. The 95% percentile CI of
# {Δ_r} is the decision statistic; an arm WINS this axis iff the CI excludes 0.
#
# Why paired (not marginal per-arm CI overlap): the two arms' errors are strongly
# correlated (same test videos), so the paired Δ has far smaller variance than the
# marginal CIs suggest. Marginal CI-overlap is statistically wrong for paired data
# (≈ a p<0.006-strict criterion) and MANUFACTURES FALSE NULLS — it is DEMOTED to a
# descriptive sidecar in the aggregator, never the inter-arm test.
#
# Self-paired guarantee (the free hard-correctness assertion): paired_auc_delta of
# an arm against ITSELF (a==b, shared indices) is Δ ≡ 0 every replicate ⇒ CI=[0,0],
# delta_mean=0, excludes_zero=False. The aggregator asserts this on runs/a0/best.pt.


def _percentile_ci(deltas: np.ndarray, ci: float) -> tuple[float, float]:
    """Two-sided percentile CI of a bootstrap Δ distribution."""
    alpha = (1.0 - ci) / 2.0
    return float(np.quantile(deltas, alpha)), float(np.quantile(deltas, 1.0 - alpha))


def _pack_delta(deltas: np.ndarray, ci: float, n: int, b: int, n_redraws: int,
                return_dist: bool) -> dict[str, Any]:
    """Package a paired-Δ bootstrap distribution into the standard result dict."""
    lo, hi = _percentile_ci(deltas, ci)
    out: dict[str, Any] = {
        "delta_mean": float(deltas.mean()),
        "ci_lo": lo,
        "ci_hi": hi,
        "ci_level": float(ci),
        "p_delta_gt_0": float(np.mean(deltas > 0.0)),
        "b": int(b),
        "n_videos": int(n),
        "n_redraws": int(n_redraws),
        # WIN-axis test: the CI excludes 0 (either side). For the STOP-gate /
        # "A beats B" direction we additionally require lo > 0 (positive side).
        "excludes_zero": bool(lo > 0.0 or hi < 0.0),
        "excludes_zero_positive": bool(lo > 0.0),
    }
    if return_dist:
        out["dist"] = deltas
    return out


def paired_auc_delta(
    scores_a: ArrayLike,
    scores_b: ArrayLike,
    labels: LabelLike,
    *,
    b: int = 10_000,
    ci: float = 0.95,
    seed: int = 0,
    return_dist: bool = False,
) -> dict[str, Any]:
    """Paired video-resampling bootstrap of Δ = AUC_A − AUC_B (single endpoint).

    The Phase-5 PRIMARY inter-arm test (a single CRF level, e.g. the STOP-gate's
    c40 video-AUC). ``scores_a`` and ``scores_b`` are per-video pooled fake-scores
    for the **same ordered set of videos** (so a shared resample index pairs the two
    arms); ``labels`` are the shared per-video labels.

    Each of ``b`` replicates draws ONE shared video-index vector with replacement
    (the SAME indices score both arms ⇒ pairing) and records
    ``Δ_r = AUC(y[idx], a[idx]) − AUC(y[idx], b[idx])``. A replicate whose
    resampled labels are single-class (AUC undefined) is **redrawn** (the redraw is
    shared, so both arms still see identical indices). Returns the 95% percentile CI
    of ``{Δ_r}`` + ``P(Δ>0)`` + the mean Δ + the ``excludes_zero`` flags.

    Self-paired: ``paired_auc_delta(s, s, y)`` ⇒ every Δ_r is identically 0 ⇒
    ``ci_lo == ci_hi == delta_mean == 0`` (a hard correctness assertion, not a
    statistical hope — the shared index feeds the same scores to both arms).

    Args:
        scores_a/scores_b: per-video pooled scores (length n), same video order.
        labels: per-video labels (length n), shared by both arms.
        b: bootstrap replicates (10,000 per the protocol).
        ci: central interval mass (0.95).
        seed: RNG seed (reproducible).
        return_dist: include the raw ``{Δ_r}`` array under key ``"dist"``.

    Returns:
        dict with ``delta_mean``, ``ci_lo``, ``ci_hi``, ``p_delta_gt_0``,
        ``excludes_zero`` (CI excludes 0 either side), ``excludes_zero_positive``
        (lo > 0 — "A beats B"), plus ``b``/``n_videos``/``n_redraws``/``ci_level``.
    """
    a = np.asarray(scores_a, dtype=np.float64).reshape(-1)
    bb = np.asarray(scores_b, dtype=np.float64).reshape(-1)
    y = np.asarray(labels).reshape(-1).astype(np.int64)
    if not (a.shape == bb.shape == y.shape):
        raise ValueError(
            f"paired length mismatch: a {a.shape}, b {bb.shape}, labels {y.shape}"
        )
    n = a.shape[0]
    if n == 0:
        raise ValueError("paired_auc_delta needs at least one video")
    if np.unique(y).size < 2:
        raise ValueError("paired_auc_delta needs both classes present")

    rng = np.random.default_rng(seed)
    deltas = np.empty(b, dtype=np.float64)
    n_redraws = 0
    for i in range(b):
        while True:
            idx = rng.integers(0, n, size=n)
            yi = y[idx]
            if np.unique(yi).size >= 2:
                break
            n_redraws += 1
        deltas[i] = roc_auc_score(yi, a[idx]) - roc_auc_score(yi, bb[idx])

    if n_redraws:
        _LOG.info("paired_auc_delta: redrew %d single-class resamples (b=%d)",
                  n_redraws, b)
    return _pack_delta(deltas, ci, n, b, n_redraws, return_dist)


def auc_comp(per_level_scores: dict[str, ArrayLike], labels: LabelLike,
             levels: Sequence[str]) -> float:
    """Point estimate of ``AUC_comp`` = mean over ``levels`` of video-level AUC.

    The A1 primary endpoint (`phase5.md` Step 5.2): the per-arm mean of the
    video-AUCs at the compressed CRF levels {c28,c32,c36,c40}. ``per_level_scores``
    maps each level to its per-video pooled scores (all over the **same** ordered
    video set as ``labels``).
    """
    y = np.asarray(labels).reshape(-1).astype(np.int64)
    if np.unique(y).size < 2:
        raise ValueError("auc_comp needs both classes present")
    vals = []
    for lv in levels:
        s = np.asarray(per_level_scores[lv], dtype=np.float64).reshape(-1)
        if s.shape != y.shape:
            raise ValueError(f"auc_comp level {lv}: scores {s.shape} vs labels {y.shape}")
        vals.append(roc_auc_score(y, s))
    return float(np.mean(vals))


def paired_auc_comp_delta(
    per_level_a: dict[str, ArrayLike],
    per_level_b: dict[str, ArrayLike],
    labels: LabelLike,
    levels: Sequence[str],
    *,
    b: int = 10_000,
    ci: float = 0.95,
    seed: int = 0,
    return_dist: bool = False,
) -> dict[str, Any]:
    """Paired bootstrap of Δ = AUC_comp_A − AUC_comp_B (the A1 PRIMARY endpoint).

    ``AUC_comp`` = mean over ``levels`` (= {c28,c32,c36,c40}) of video-level AUC.
    Per replicate a single shared video-index vector is drawn; for each arm the
    per-level AUCs are recomputed on the resampled videos and averaged → AUC_comp;
    ``Δ_r = AUC_comp_A − AUC_comp_B``. The shared index pairs the two arms exactly
    as in :func:`paired_auc_delta`. All level score arrays for both arms must be
    aligned to the SAME ordered video set as ``labels`` (the aggregator aligns by
    video key before calling this).

    Self-paired: identical inputs ⇒ Δ ≡ 0 every replicate ⇒ CI = [0, 0].
    """
    y = np.asarray(labels).reshape(-1).astype(np.int64)
    n = y.shape[0]
    if n == 0:
        raise ValueError("paired_auc_comp_delta needs at least one video")
    if np.unique(y).size < 2:
        raise ValueError("paired_auc_comp_delta needs both classes present")
    if not levels:
        raise ValueError("paired_auc_comp_delta needs at least one level")

    A = {lv: np.asarray(per_level_a[lv], dtype=np.float64).reshape(-1) for lv in levels}
    B = {lv: np.asarray(per_level_b[lv], dtype=np.float64).reshape(-1) for lv in levels}
    for lv in levels:
        if A[lv].shape != y.shape or B[lv].shape != y.shape:
            raise ValueError(
                f"paired_auc_comp_delta level {lv}: shape mismatch vs labels {y.shape}"
            )

    rng = np.random.default_rng(seed)
    deltas = np.empty(b, dtype=np.float64)
    n_redraws = 0
    for i in range(b):
        while True:
            idx = rng.integers(0, n, size=n)
            yi = y[idx]
            if np.unique(yi).size >= 2:
                break
            n_redraws += 1
        ca = np.mean([roc_auc_score(yi, A[lv][idx]) for lv in levels])
        cb = np.mean([roc_auc_score(yi, B[lv][idx]) for lv in levels])
        deltas[i] = ca - cb

    if n_redraws:
        _LOG.info("paired_auc_comp_delta: redrew %d single-class resamples (b=%d)",
                  n_redraws, b)
    return _pack_delta(deltas, ci, n, b, n_redraws, return_dist)


# ---------------------------------------------------------------------------
# Across-seed honest band (source-B variance; seed = experimental unit)
# ---------------------------------------------------------------------------

# t_{.975, 2 dof} — the multiplier for a 95% CI of a mean of 3 seeds (2 dof). The
# half-width is t·s/√3 = 4.30·s/√3 ≈ 2.48·s. NOTE (phase5.md): 4.30 is the
# t-multiplier, THEN divided by √3 — do not misread 4.30 as already absorbing /√3.
# FROZEN: this exact 4.30 (a rounded t_{.975,2}=4.3027) is pinned in the Phase-5
# pre-registration (runs/phase5_build/PREREGISTRATION-A1.md, tag phase5-prereg-a1).
# The 3-seed (k=3) band MUST stay bit-identical to ``4.30·s/√3``, so ``seed_band``
# uses this constant verbatim for k=3 and never a recomputed quantile.
T_975_2DOF: float = 4.30

# Two-sided 95% Student-t multiplier by seed count k (df = k-1), for k=2..10. The
# df=2 (k=3) entry is pinned to the FROZEN ``T_975_2DOF`` above (4.30, NOT the
# exact 4.3027) so the pre-registered 3-seed band is bit-identical; the rest are
# standard t_{.975, k-1} quantiles. k>10 falls back to ``scipy.stats.t`` (see
# ``_t_975``). Fixing k≠3 corrects the prior bug that used 4.30 for every k.
_T_975_BY_K: dict[int, float] = {
    2: 12.706,      # df=1
    3: T_975_2DOF,  # df=2 — FROZEN at 4.30 (pre-registration), not 4.3027
    4: 3.182,       # df=3
    5: 2.776,       # df=4
    6: 2.571,       # df=5
    7: 2.447,       # df=6
    8: 2.365,       # df=7
    9: 2.306,       # df=8
    10: 2.262,      # df=9
}


def _t_975(k: int) -> float:
    """Two-sided 95% t-multiplier for a ``k``-seed mean (df = k-1).

    k=2..10 come from the pinned ``_T_975_BY_K`` table; k=3 is FROZEN at
    ``T_975_2DOF`` (4.30) to keep the pre-registered 3-seed band bit-identical.
    For k>10 the quantile is computed from ``scipy.stats.t`` if importable, else
    a ``ValueError`` is raised (rather than silently mis-scaling the band with a
    3-seed constant). Requires ``k >= 2`` (df >= 1).
    """
    if k in _T_975_BY_K:
        return _T_975_BY_K[k]
    try:
        from scipy.stats import t as _student_t
    except ImportError as exc:  # pragma: no cover - scipy ships in the `cv` env
        raise ValueError(
            f"seed_band: t_{{.975, {k - 1}}} needs scipy for k>10 (k={k}); "
            "scipy unavailable"
        ) from exc
    return float(_student_t.ppf(0.975, k - 1))


def seed_band(seed_values: Sequence[float]) -> dict[str, float]:
    """Across-seed mean ± the honest 95% band ``t_{.975,k-1}·s/√k`` (seed = unit).

    Treats the seed as the experimental unit (phase5.md Step 5.2, source B): per
    arm, ``mean ± t·s/√k`` where ``s`` is the across-seed sample std (ddof=1),
    ``k`` the seed count and ``t = t_{.975, k-1}`` the two-sided 95% Student-t
    multiplier (via :func:`_t_975`). For the canonical **3-seed** case this is
    ``4.30·s/√3 ≈ 2.48·s`` — the FROZEN pre-registered band (k=3 stays
    bit-identical to the old formula). k=2 uses 12.706, k=5 uses 2.776, etc.;
    k>10 uses ``scipy.stats.t``. Returns the mean, std, the half-width, and the
    band endpoints. For a single seed (k=1) the std / band is ``nan`` (undefined
    — flagged, not silently 0); k=0 raises.
    """
    v = np.asarray(list(seed_values), dtype=np.float64).reshape(-1)
    k = v.shape[0]
    if k == 0:
        raise ValueError("seed_band needs at least one seed value")
    mean = float(v.mean())
    if k < 2:
        return {"mean": mean, "std": float("nan"), "half_width": float("nan"),
                "lo": float("nan"), "hi": float("nan"), "n_seeds": k}
    s = float(np.std(v, ddof=1))
    half = _t_975(k) * s / math.sqrt(k)
    return {"mean": mean, "std": s, "half_width": half,
            "lo": mean - half, "hi": mean + half, "n_seeds": k}
