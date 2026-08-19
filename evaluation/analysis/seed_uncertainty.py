"""Two-level (seed x video) bootstrap for the two headline contrasts.

The published pooled intervals are **conditional on the three seeds that were
run**: they average each video's score over those seeds and then resample videos
only. This script adds the level they leave out. It resamples the seeds too —
independently for each arm, since the runs are independent — before resampling
the videos or the identity clusters, so the interval is not conditional on which
seeds were realized.

The result is the honest wide interval. With k = 3 the seed resample is coarse,
which is a property of the design (three seeds is a pilot, not a sample) rather
than of the estimator; `mde.py` quantifies the same limitation as a minimum
detectable effect.

    python seed_uncertainty.py --jobs 6
"""

from __future__ import annotations

import argparse
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import stats_common as S

SCHEMES = ("seed+video", "seed+source", "seed+pair")


def _task(args: tuple[str, str, str | None, int]) -> tuple[str, str, dict]:
    row, scheme, pred_root, b = args
    c = S.CONTRAST_BY_ROW[row]
    pred = S.predictions(pred_root)
    d = S.load_contrast(pred, c)
    unit = scheme.split("+")[1]
    clusters = None if unit == "video" else S.cluster_labels(d["keys"], unit)
    A = S.per_seed_matrix(pred, c.a, d["keys"], c.level, c.eval_set)
    B = S.per_seed_matrix(pred, c.b, d["keys"], c.level, c.eval_set)
    t0 = time.time()
    res = S.two_level_bootstrap(A, B, d["labels"], scheme=scheme,
                               clusters=clusters, b=b)
    res["seconds"] = round(time.time() - t0, 1)
    return row, scheme, res


def main() -> None:
    ap = S.add_common_args(argparse.ArgumentParser(description=__doc__))
    ap.add_argument("--rows", default=",".join(S.HEADLINE_ROWS))
    ap.add_argument("--jobs", type=int, default=1)
    args = ap.parse_args()

    pred = S.predictions(args.predictions)
    out_path = Path(args.out) if args.out else S.HERE / "seed_uncertainty.json"
    rows = [r.strip() for r in args.rows.split(",") if r.strip()]

    payload: dict = {
        "what": "seed x video bootstrap: the pooled contrast with the seed draw "
                "included, so the interval is not conditional on the realized seeds",
        "recipe": {"b": args.b, "rng_seed": S.RNG_SEED, "key_order": "sorted",
                   "seed_pooling": "per-video mean", "interval": "percentile",
                   "seed_draw": "k seeds with replacement, independently per arm"},
        "contrasts": {},
    }

    for row in rows:
        c = S.CONTRAST_BY_ROW[row]
        d = S.load_contrast(pred, c)
        A = S.per_seed_matrix(pred, c.a, d["keys"], c.level, c.eval_set)
        B = S.per_seed_matrix(pred, c.b, d["keys"], c.level, c.eval_set)
        payload["contrasts"][row] = {
            "name": c.name, "runs_a": c.a, "runs_b": c.b,
            "k_a": int(A.shape[0]), "k_b": int(B.shape[0]),
            "published": c.published,
            "per_seed_auc_a": [S.auc(d["labels"], A[i]) for i in range(A.shape[0])],
            "per_seed_auc_b": [S.auc(d["labels"], B[i]) for i in range(B.shape[0])],
            "schemes": {},
        }

    tasks = [(row, scheme, args.predictions, args.b)
             for row in rows for scheme in SCHEMES]
    if args.jobs > 1:
        with ProcessPoolExecutor(max_workers=args.jobs) as pool:
            results = list(pool.map(_task, tasks))
    else:
        results = [_task(t) for t in tasks]

    for row, scheme, res in results:
        payload["contrasts"][row]["schemes"][scheme] = res
        print(f"{row} {scheme:12s} d={res['delta']:+.4f} "
              f"CI[{res['ci_lo']:+.4f},{res['ci_hi']:+.4f}] se={res['se']:.5f}")

    S.write_json(out_path, payload)


if __name__ == "__main__":
    main()
