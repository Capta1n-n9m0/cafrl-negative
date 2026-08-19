"""Cluster bootstrap for every adjudicated contrast.

The published intervals resample **videos** as if they were independent draws.
They are not: the FaceForensics++ test split is 70 identity pairs, and each of
its 140 identities contributes one real video and four manipulated ones that
share either its footage or its face. This script re-runs every contrast with
the resampling unit moved up to the cluster — under four different definitions
of what a cluster is — and reports both interval sets side by side, so a reader
can see whether any verdict depends on the exchangeability assumption. (None
does; the summary at the end prints the flips, and there are none.)

    python cluster_bootstrap.py --self-check --jobs 8

Everything else is the pinned recipe: sorted pooling-key order, seeds pooled by
per-video mean, 10,000 replicates, RNG seed 0, percentile intervals. Each
(contrast, scheme) task seeds its own generator, so the results do not depend on
how the work is scheduled.
"""

from __future__ import annotations

import argparse
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import stats_common as S

SCHEMES = ("video",) + S.CLUSTER_SCHEMES


def _task(args: tuple[str, str, str | None, int]) -> tuple[str, str, dict]:
    row, scheme, pred_root, b = args
    c = S.CONTRAST_BY_ROW[row]
    pred = S.predictions(pred_root)
    d = S.load_contrast(pred, c)
    clusters = None if scheme == "video" else S.cluster_labels(d["keys"], scheme)
    t0 = time.time()
    res = S.paired_bootstrap(d["scores_a"], d["scores_b"], d["labels"],
                             scheme=scheme, clusters=clusters, b=b)
    res["seconds"] = round(time.time() - t0, 1)
    return row, scheme, res


def self_check(pred) -> dict[str, float]:
    """Assert this module's engine reproduces the frozen harness (video scheme)."""
    from src.evaluation.metrics import paired_auc_delta

    c = S.CONTRAST_BY_ROW["C5"]
    d = S.load_contrast(pred, c)
    ref = paired_auc_delta(d["scores_a"], d["scores_b"], d["labels"])
    mine = S.paired_bootstrap(d["scores_a"], d["scores_b"], d["labels"], scheme="video")
    gaps = {"ci_lo": abs(mine["ci_lo"] - ref["ci_lo"]),
            "ci_hi": abs(mine["ci_hi"] - ref["ci_hi"]),
            "delta": abs(mine["delta_boot_mean"] - ref["delta_mean"])}
    if max(gaps.values()) > 1e-9:
        raise AssertionError(f"engine disagrees with the frozen harness: {gaps}")
    print(f"self-check: engine == frozen harness to {max(gaps.values()):.1e}")
    return gaps


def main() -> None:
    ap = S.add_common_args(argparse.ArgumentParser(description=__doc__))
    ap.add_argument("--schemes", default=",".join(SCHEMES))
    ap.add_argument("--rows", default=",".join(c.row for c in S.CONTRASTS))
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--self-check", action="store_true",
                    help="verify the engine against the frozen harness first")
    args = ap.parse_args()

    pred = S.predictions(args.predictions)
    out_path = Path(args.out) if args.out else S.HERE / "cluster_bootstrap.json"
    schemes = [s.strip() for s in args.schemes.split(",") if s.strip()]
    rows = [r.strip() for r in args.rows.split(",") if r.strip()]

    payload: dict = {
        "what": "paired AUC-difference bootstrap for every adjudicated contrast, at "
                "four exchangeability units alongside the published video unit",
        "recipe": {"b": args.b, "rng_seed": S.RNG_SEED, "key_order": "sorted",
                   "seed_pooling": "per-video mean", "interval": "percentile"},
        "primary_cluster_scheme": S.PRIMARY_CLUSTER,
        "cluster_schemes": S.CLUSTER_DOC,
        "contrasts": {},
    }
    if args.self_check:
        payload["self_check_vs_frozen_harness"] = self_check(pred)

    for row in rows:
        c = S.CONTRAST_BY_ROW[row]
        payload["contrasts"][row] = {
            "name": c.name, "table": c.table, "eval_set": c.eval_set,
            "level": c.level, "headline": c.headline, "family": c.family,
            "runs_a": c.a, "runs_b": c.b, "published": c.published, "schemes": {},
        }

    tasks = [(row, scheme, args.predictions, args.b)
             for row in rows for scheme in schemes]
    if args.jobs > 1:
        with ProcessPoolExecutor(max_workers=args.jobs) as pool:
            results = list(pool.map(_task, tasks))
    else:
        results = [_task(t) for t in tasks]

    for row, scheme, res in results:
        payload["contrasts"][row]["schemes"][scheme] = res
        print(f"{row} {scheme:10s} d={res['delta']:+.4f} "
              f"CI[{res['ci_lo']:+.4f},{res['ci_hi']:+.4f}] "
              f"se={res['se']:.5f} excludes0={res['excludes_zero']}")

    flips = []
    for row, entry in payload["contrasts"].items():
        got = entry["schemes"]
        if "video" in got and S.PRIMARY_CLUSTER in got:
            entry["verdict_flips_vs_video"] = bool(
                got["video"]["excludes_zero"] != got[S.PRIMARY_CLUSTER]["excludes_zero"])
            entry["verdict_flips_any_scheme"] = bool(
                len({r["excludes_zero"] for r in got.values()}) > 1)
            if entry["verdict_flips_any_scheme"]:
                flips.append(row)
    payload["verdict_flips"] = flips
    print("\nverdicts that change with the resampling unit:", flips or "none")
    S.write_json(out_path, payload)


if __name__ == "__main__":
    main()
