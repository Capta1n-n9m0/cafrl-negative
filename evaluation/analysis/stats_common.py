"""Shared machinery for the revision's statistical analyses.

Everything in this directory reads only released artifacts: the per-video scores
in ``predictions/`` and the frozen harness in ``evaluation/src/``. The bootstrap
recipe is the campaign's own, and it is pinned: per-video scores in **sorted
pooling-key order**, seeds pooled by per-video mean, **10,000** replicates,
**RNG seed 0**, percentile intervals. Under the plain video-resampling scheme
the engine here reproduces the frozen harness replicate for replicate — the
``--self-check`` flag of ``cluster_bootstrap.py`` asserts it — so the new
analyses extend the published ones rather than re-implementing them.

The one deliberate difference from ``src/evaluation/metrics.py`` is speed: the
AUC is computed from ranks rather than through scikit-learn, because a clustered
bootstrap over a dozen contrasts calls it a million times. The two agree to
floating-point noise (asserted).
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence

import numpy as np
from scipy.stats import rankdata

HERE = Path(__file__).resolve().parent
# `release_io` and the harness package live one level up, in `evaluation/`.
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))

# -- the pinned recipe -------------------------------------------------------
B_REPLICATES = 10_000
RNG_SEED = 0
CI_LEVEL = 0.95
TOST_CI_LEVEL = 0.90       # the TOST-equivalent interval for alpha = 0.05 per side
DELTA_MARGIN = 0.01        # the equivalence margin: 1 AUC point. POST HOC — see README.md
LEVEL = "c40"              # the compression level every headline contrast is read at

KEY_SEP = "\x1f"

# -- the arms, by released run id -------------------------------------------
SPATIALBASE = ["b7_effnet_b0_mq_fliponly",
               "b7_effnet_b0_mq_fliponly_s1",
               "b7_effnet_b0_mq_fliponly_s2"]
FAIR_N = ["f1_none_fair_s42", "f1_none_fair_s1", "f1_none_fair_s2"]
FAIR_W = ["f2_spatres_full_s42", "f2_spatres_full_s1", "f2_spatres_full_s2"]
TRUNKCTRL = ["trunk_recipe_s42", "trunk_recipe_s1", "trunk_recipe_s2"]


@dataclass(frozen=True)
class Contrast:
    """One adjudicated contrast of the paper."""

    row: str                     # stable identifier, used as the key in the outputs
    name: str                    # the row label the manuscript prints
    a: list[str]                 # released run ids on the left of the difference
    b: list[str]                 # released run ids on the right
    level: str = LEVEL
    eval_set: str = "ffpp"       # "ffpp" | "faceshifter"
    published: dict[str, float] = field(default_factory=dict)
    family: str = "confirmatory"  # "confirmatory" | "descriptive"
    headline: bool = False        # the two pooled 3v3 equivalence rows
    table: str = "contrasts"


# The eight rows of the adjudicated-contrasts table, in printed order, and the
# four held-out-manipulation contrasts of the appendix. `published` is what the
# manuscript prints, so every run re-checks the printed column as a side effect.
CONTRASTS: list[Contrast] = [
    Contrast("C1", "SpatialBase - CAFRL as specified (s42)",
             ["b7_effnet_b0_mq_fliponly"], ["a0"],
             published={"delta": +0.0366, "ci_lo": +0.0205, "ci_hi": +0.0540}),
    Contrast("C2", "Fair-N - CAFRL-adv (s42)",
             ["f1_none_fair_s42"], ["a1_none_s42"],
             published={"delta": +0.0396, "ci_lo": +0.0231, "ci_hi": +0.0570}),
    Contrast("C3", "Fair-N - SpatialBase (s42)",
             ["f1_none_fair_s42"], ["b7_effnet_b0_mq_fliponly"],
             published={"delta": -0.0004, "ci_lo": -0.0092, "ci_hi": +0.0080}),
    Contrast("C4", "Fair-W - SpatialBase (s42)",
             ["f2_spatres_full_s42"], ["b7_effnet_b0_mq_fliponly"],
             published={"delta": +0.0056, "ci_lo": -0.0022, "ci_hi": +0.0134}),
    Contrast("C5", "Fair-N pool - SpatialBase pool (3v3)", FAIR_N, SPATIALBASE,
             published={"delta": -0.0010, "ci_lo": -0.0066, "ci_hi": +0.0045},
             headline=True),
    Contrast("C6", "Fair-W pool - SpatialBase pool (3v3)", FAIR_W, SPATIALBASE,
             published={"delta": +0.0022, "ci_lo": -0.0035, "ci_hi": +0.0080},
             headline=True),
    Contrast("C7", "SpatialBase (s42) - TrunkCtrl pool",
             ["b7_effnet_b0_mq_fliponly"], TRUNKCTRL,
             published={"delta": -0.0038, "ci_lo": -0.0116, "ci_hi": +0.0039}),
    Contrast("C8", "TrunkCtrl pool - spatial-residual (s42)",
             TRUNKCTRL, ["cafrl_spatres_s42"],
             published={"delta": +0.0490, "ci_lo": +0.0294, "ci_hi": +0.0705}),
    Contrast("F1", "Fair-N pool - SpatialBase pool (FaceShifter)", FAIR_N, SPATIALBASE,
             eval_set="faceshifter", table="faceshifter",
             published={"delta": -0.0325, "ci_lo": -0.0545, "ci_hi": -0.0114}),
    Contrast("F2", "Fair-W pool - SpatialBase pool (FaceShifter)", FAIR_W, SPATIALBASE,
             eval_set="faceshifter", table="faceshifter",
             published={"delta": -0.0318, "ci_lo": -0.0575, "ci_hi": -0.0065}),
    Contrast("F3", "Fair-N s42 - SpatialBase pool (FaceShifter)",
             ["f1_none_fair_s42"], SPATIALBASE,
             eval_set="faceshifter", table="faceshifter",
             published={"delta": +0.0220, "ci_lo": -0.0062, "ci_hi": +0.0508}),
    Contrast("F4", "Fair-W s42 - SpatialBase pool (FaceShifter)",
             ["f2_spatres_full_s42"], SPATIALBASE,
             eval_set="faceshifter", table="faceshifter",
             published={"delta": -0.0227, "ci_lo": -0.0537, "ci_hi": +0.0081}),
]

CONTRAST_BY_ROW = {c.row: c for c in CONTRASTS}
HEADLINE_ROWS = [c.row for c in CONTRASTS if c.headline]


# ---------------------------------------------------------------------------
# AUC
# ---------------------------------------------------------------------------

def auc(labels: np.ndarray, scores: np.ndarray) -> float:
    """Rank-based ROC AUC, ties averaged.

    Equal to ``sklearn.metrics.roc_auc_score`` to floating-point noise; the rank
    form is used because the bootstrap calls it hundreds of thousands of times.
    """
    n1 = int(labels.sum())
    n0 = labels.shape[0] - n1
    if n1 == 0 or n0 == 0:
        raise ValueError("auc needs both classes present")
    r = rankdata(scores)
    return float((r[labels == 1].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0))


# ---------------------------------------------------------------------------
# Clusters: the exchangeability unit
# ---------------------------------------------------------------------------
#
# An evaluation key is `video_id \x1f method`. A real video's key is its own
# identity with an empty method; a manipulated video is named `{target}_{source}`
# — the footage and the head pose come from the *target* video, the swapped-in
# face from the *source* identity. The official FaceForensics++ test split is 70
# identity pairs, and each of its 140 identities appears once as a target and
# once as a source, so the evaluated videos decompose four different ways. The
# cluster labels below are derived from the released keys alone; no external
# metadata file is needed (the naming convention is stated in
# `evaluation/src/data/splits.py` and holds for every row of the split).

CLUSTER_SCHEMES = ("source", "target", "basevideo", "pair")
PRIMARY_CLUSTER = "source"

CLUSTER_DOC = {
    "source": "the swapped-in face identity; a real video is its own identity "
              "(FF++ test: 140 clusters of 5 — one real and the four manipulations "
              "that take their face from it)",
    "target": "the footage identity: a real video and the manipulations built on "
              "that same footage (FF++ test: 140 clusters of 5)",
    "basevideo": "one cluster per manipulated base video (its manipulation methods) "
                 "and one per real video (FF++ test: 280 clusters)",
    "pair": "the unordered identity pair of the official split — the coarsest unit, "
            "which absorbs the target and the source dependence at once "
            "(FF++ test: 70 clusters of 10)",
}


def parse_key(key: str) -> tuple[str, str]:
    video_id, _, method = key.partition(KEY_SEP)
    return video_id, method


def cluster_labels(keys: Sequence[str], scheme: str) -> np.ndarray:
    """Cluster id per video, under one exchangeability scheme."""
    if scheme not in CLUSTER_SCHEMES:
        raise ValueError(f"unknown cluster scheme {scheme!r}")

    partner: dict[str, str] = {}
    for key in keys:
        video_id, method = parse_key(key)
        if method:
            target, source = video_id.split("_")
            for x, y in ((target, source), (source, target)):
                if partner.setdefault(x, y) != y:
                    raise ValueError(
                        f"identity {x} is paired with both {partner[x]} and {y}; the "
                        "`pair` scheme assumes the official split's pairing"
                    )

    out: list[str] = []
    for key in keys:
        video_id, method = parse_key(key)
        if method:
            target, source = video_id.split("_")
        else:
            target = source = video_id
        if scheme == "source":
            out.append(source)
        elif scheme == "target":
            out.append(target)
        elif scheme == "basevideo":
            out.append(video_id if method else f"real:{video_id}")
        else:
            mate = partner.get(video_id, video_id) if not method else source
            out.append("|".join(sorted({target, source, mate})) if method
                       else "|".join(sorted({video_id, mate})))
    return np.asarray(out, dtype=object)


def cluster_index(labels: np.ndarray) -> list[np.ndarray]:
    """Member positions of each cluster, clusters in sorted-label order."""
    return [np.flatnonzero(labels == lab) for lab in sorted(set(labels.tolist()))]


# ---------------------------------------------------------------------------
# Bootstrap engines
# ---------------------------------------------------------------------------

def _summarize(deltas: np.ndarray, *, delta_point: float, n_units: int,
               n_videos: int, n_redraws: int, scheme: str,
               margin: float = DELTA_MARGIN) -> dict[str, Any]:
    """The standard summary of one bootstrap distribution of Δ."""
    q = {f"q{p}": float(np.quantile(deltas, p / 100.0))
         for p in (2.5, 5.0, 50.0, 95.0, 97.5)}
    se = float(deltas.std(ddof=1))
    out: dict[str, Any] = {
        "scheme": scheme,
        "delta": delta_point,
        "delta_boot_mean": float(deltas.mean()),
        "se": se,
        "ci_lo": q["q2.5"], "ci_hi": q["q97.5"], "ci_level": CI_LEVEL,
        "ci90_lo": q["q5.0"], "ci90_hi": q["q95.0"], "ci90_level": TOST_CI_LEVEL,
        "quantiles": q,
        "p_delta_gt_0": float(np.mean(deltas > 0.0)),
        "excludes_zero": bool(q["q2.5"] > 0.0 or q["q97.5"] < 0.0),
        # bootstrap achieved significance levels: tail mass beyond a threshold
        "asl_two_sided_vs_0": float(2.0 * min(np.mean(deltas <= 0.0),
                                              np.mean(deltas >= 0.0))),
        "asl_le_minus_margin": float(np.mean(deltas <= -margin)),
        "asl_ge_plus_margin": float(np.mean(deltas >= +margin)),
        "margin": margin,
        "b": int(deltas.shape[0]),
        "rng_seed": RNG_SEED,
        "n_resampling_units": int(n_units),
        "n_videos": int(n_videos),
        "n_redraws": int(n_redraws),
    }
    if se > 0:
        z = delta_point / se
        out["z"] = float(z)
        out["p_two_sided_z"] = float(math.erfc(abs(z) / math.sqrt(2.0)))
    return out


def _draw(rng: np.random.Generator, n: int, members: list[np.ndarray] | None,
          n_units: int) -> np.ndarray:
    if members is None:
        return rng.integers(0, n, size=n)
    pick = rng.integers(0, n_units, size=n_units)
    return np.concatenate([members[j] for j in pick])


def paired_bootstrap(scores_a: np.ndarray, scores_b: np.ndarray,
                     labels: np.ndarray, *, scheme: str = "video",
                     clusters: np.ndarray | None = None,
                     b: int = B_REPLICATES, seed: int = RNG_SEED) -> dict[str, Any]:
    """Paired Δ = AUC(A) − AUC(B) bootstrap, resampling videos or clusters.

    One resample vector per replicate scores **both** arms, so the arms' shared
    error differences away; a replicate that lands on a single class is redrawn,
    and the redraw is shared. With ``scheme="video"`` the draw is the frozen
    harness's own, so the intervals reproduce the published ones exactly.
    """
    n = labels.shape[0]
    if scheme == "video":
        members = None
    elif clusters is None:
        raise ValueError("a clustered scheme needs cluster labels")
    else:
        members = cluster_index(clusters)
    n_units = n if members is None else len(members)

    rng = np.random.default_rng(seed)
    deltas = np.empty(b, dtype=np.float64)
    n_redraws = 0
    for i in range(b):
        while True:
            idx = _draw(rng, n, members, n_units)
            yi = labels[idx]
            if np.unique(yi).size >= 2:
                break
            n_redraws += 1
        deltas[i] = auc(yi, scores_a[idx]) - auc(yi, scores_b[idx])

    point = auc(labels, scores_a) - auc(labels, scores_b)
    return _summarize(deltas, delta_point=point, n_units=n_units, n_videos=n,
                      n_redraws=n_redraws, scheme=scheme)


def two_level_bootstrap(per_seed_a: np.ndarray, per_seed_b: np.ndarray,
                        labels: np.ndarray, *, scheme: str = "seed+video",
                        clusters: np.ndarray | None = None,
                        b: int = B_REPLICATES, seed: int = RNG_SEED) -> dict[str, Any]:
    """Δ bootstrap that resamples **seeds and videos**, not videos alone.

    ``per_seed_a`` / ``per_seed_b`` are ``(k, n)`` per-video score matrices, one
    row per seed, aligned to the same video order. Each replicate draws k seeds
    with replacement independently for each arm (the runs are independent),
    pools them by per-video mean exactly as the campaign pools seeds, then draws
    one shared video (or cluster) resample. The resulting interval is not
    conditional on which seeds were realized — the published pooled intervals are.
    """
    ka, n = per_seed_a.shape
    kb, nb = per_seed_b.shape
    if n != nb or labels.shape[0] != n:
        raise ValueError("per-seed matrices and labels disagree in length")
    members = None if clusters is None else cluster_index(clusters)
    n_units = n if members is None else len(members)

    rng = np.random.default_rng(seed)
    deltas = np.empty(b, dtype=np.float64)
    n_redraws = 0
    for i in range(b):
        sa = per_seed_a[rng.integers(0, ka, size=ka)].mean(axis=0)
        sb = per_seed_b[rng.integers(0, kb, size=kb)].mean(axis=0)
        while True:
            idx = _draw(rng, n, members, n_units)
            yi = labels[idx]
            if np.unique(yi).size >= 2:
                break
            n_redraws += 1
        deltas[i] = auc(yi, sa[idx]) - auc(yi, sb[idx])

    point = auc(labels, per_seed_a.mean(axis=0)) - auc(labels, per_seed_b.mean(axis=0))
    return _summarize(deltas, delta_point=point, n_units=n_units, n_videos=n,
                      n_redraws=n_redraws, scheme=scheme)


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def predictions(root: str | Path | None = None):
    from release_io import Predictions
    return Predictions(root)


def load_contrast(pred, c: Contrast) -> dict[str, Any]:
    """Aligned pooled scores for one contrast, in the pinned sorted-key order."""
    from release_io import align

    a = pred.pool(c.a, c.level, c.eval_set)
    b = pred.pool(c.b, c.level, c.eval_set)
    sa, sb, y = align(a, b)
    common = set(b["keys"])
    return {"scores_a": sa, "scores_b": sb, "labels": y,
            "keys": [k for k in a["keys"] if k in common]}


def per_seed_matrix(pred, runs: Sequence[str], keys: Sequence[str],
                    level: str = LEVEL, eval_set: str = "ffpp") -> np.ndarray:
    """``(k, n)`` per-video scores for one arm, reindexed onto ``keys``."""
    rows = []
    for run in runs:
        cell = pred.cell(run, level, eval_set)
        pos = {k: i for i, k in enumerate(cell["keys"])}
        rows.append(cell["scores"][[pos[k] for k in keys]])
    return np.vstack(rows)


# ---------------------------------------------------------------------------
# Small shared CLI / IO helpers
# ---------------------------------------------------------------------------

def add_common_args(ap: argparse.ArgumentParser) -> argparse.ArgumentParser:
    ap.add_argument("--predictions", default=None,
                    help="path to predictions/ (default: ../../predictions)")
    ap.add_argument("--out", default=None, help="output JSON path")
    ap.add_argument("--b", type=int, default=B_REPLICATES,
                    help=f"bootstrap replicates (default: the pinned {B_REPLICATES})")
    return ap


def read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise SystemExit(f"missing input {path} — run the scripts in the order "
                         "given in README.md (or run_all.py)")
    return json.loads(path.read_text())


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"wrote {path.name}")
