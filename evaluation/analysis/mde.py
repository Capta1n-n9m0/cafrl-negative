"""Minimum detectable effect and power for the neutral verdicts.

A confidence interval that includes zero says what the design could not detect,
not that the effect is zero. This script quantifies the "could not detect" at
both levels of the design:

* **seed level** — a k = 3 vs k = 3 comparison of per-seed AUCs, with the
  observed across-seed SDs;
* **video level, conditional on the realized seeds** — from the realized
  standard error of the paired bootstrap (both the published video unit and the
  clustered units, read from ``cluster_bootstrap.json``).

    python mde.py                          # -> mde.json  (needs cluster_bootstrap.json)
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
from scipy.stats import norm, t as student_t

import stats_common as S

ARMS = {
    "SpatialBase": S.SPATIALBASE,
    "Fair-N": S.FAIR_N,
    "Fair-W": S.FAIR_W,
    "TrunkCtrl": S.TRUNKCTRL,
}
PAIRS = [("Fair-N", "SpatialBase"), ("Fair-W", "SpatialBase")]
POWERS = (0.80, 0.90)
ALPHA = 0.05


def seed_level_mde(s_pooled: float, k: int, power: float, alpha: float = ALPHA) -> float:
    """Two-sample MDE for k vs k seeds: (t_{1-a/2,df} + t_{power,df}) s_p sqrt(2/k)."""
    df = 2 * k - 2
    return float((student_t.ppf(1 - alpha / 2, df) + student_t.ppf(power, df))
                 * s_pooled * math.sqrt(2.0 / k))


def conditional_mde(se: float, power: float, alpha: float = ALPHA) -> float:
    """MDE from a realized standard error: (z_{1-a/2} + z_power) * SE."""
    return float((norm.ppf(1 - alpha / 2) + norm.ppf(power)) * se)


def main() -> None:
    ap = S.add_common_args(argparse.ArgumentParser(description=__doc__))
    ap.add_argument("--bootstrap", default=None,
                    help="cluster_bootstrap.json (default: beside this script)")
    ap.add_argument("--seed-bootstrap", default=None,
                    help="seed_uncertainty.json (default: beside this script)")
    args = ap.parse_args()

    pred = S.predictions(args.predictions)
    out_path = Path(args.out) if args.out else S.HERE / "mde.json"
    boot_path = Path(args.bootstrap) if args.bootstrap else S.HERE / "cluster_bootstrap.json"

    # -- seed level ---------------------------------------------------------
    per_seed: dict[str, dict] = {}
    for arm, runs in ARMS.items():
        vals = [pred.cell(r, S.LEVEL)["video_auc"] for r in runs]
        v = np.asarray(vals, dtype=np.float64)
        sd = float(v.std(ddof=1))
        per_seed[arm] = {
            "runs": runs, "auc": vals, "k": len(vals),
            "mean": float(v.mean()), "sd": sd,
            "band_half_width_t430": 4.30 * sd / math.sqrt(len(vals)),
        }
        print(f"{arm:12s} mean={v.mean():.4f} sd={sd:.4f} "
              f"(+/-{4.30 * sd / math.sqrt(len(vals)):.4f})")

    seed_mde: dict[str, dict] = {}
    for a, b in PAIRS:
        ka, kb = per_seed[a]["k"], per_seed[b]["k"]
        if ka != kb:
            raise ValueError("the seed-level MDE assumes equal k per arm")
        sp = math.sqrt((per_seed[a]["sd"] ** 2 + per_seed[b]["sd"] ** 2) / 2.0)
        seed_mde[f"{a} vs {b}"] = {
            "k": ka, "sd_a": per_seed[a]["sd"], "sd_b": per_seed[b]["sd"],
            "sd_pooled": sp, "df": 2 * ka - 2,
            "observed_seed_mean_difference": per_seed[a]["mean"] - per_seed[b]["mean"],
            **{f"mde_power{int(p*100)}": seed_level_mde(sp, ka, p) for p in POWERS},
        }
        print(f"seed-level MDE {a} vs {b}: "
              f"{seed_mde[f'{a} vs {b}']['mde_power80']*100:.2f} pt @80% power")

    # -- video level, conditional on the realized seeds ----------------------
    boot = S.read_json(boot_path)
    cond: dict[str, dict] = {}
    for row, entry in boot["contrasts"].items():
        cond[row] = {"name": entry["name"], "schemes": {}}
        for scheme, res in entry["schemes"].items():
            cond[row]["schemes"][scheme] = {
                "se": res["se"],
                "ci_half_width": (res["ci_hi"] - res["ci_lo"]) / 2.0,
                **{f"mde_power{int(p*100)}": conditional_mde(res["se"], p) for p in POWERS},
            }

    # -- video level, seeds resampled too (unconditional) --------------------
    seed_path = (Path(args.seed_bootstrap) if args.seed_bootstrap
                 else S.HERE / "seed_uncertainty.json")
    two_level: dict[str, dict] = {}
    for row, entry in S.read_json(seed_path)["contrasts"].items():
        two_level[row] = {"name": entry["name"], "schemes": {
            scheme: {"se": res["se"],
                     **{f"mde_power{int(p*100)}": conditional_mde(res["se"], p)
                        for p in POWERS}}
            for scheme, res in entry["schemes"].items()}}

    primary = boot.get("primary_cluster_scheme", S.PRIMARY_CLUSTER)
    headline = {}
    for scheme in ("video", primary):
        vals = [cond[r]["schemes"][scheme]["mde_power80"] for r in S.HEADLINE_ROWS]
        headline[scheme] = {
            "rows": S.HEADLINE_ROWS,
            "mde_power80_max": max(vals),
            "mde_power80_max_pt": round(max(vals) * 100, 2),
        }
        print(f"conditional MDE @80% ({scheme}): "
              f"{max(vals)*100:.2f} pt over the headline rows")

    payload = {
        "what": "what the design could and could not have detected",
        "headline_sentence": (
            "the design cannot distinguish a zero effect from a true effect of up to "
            f"{headline[primary]['mde_power80_max_pt']:.1f} AUC points at the video "
            "level (conditional on the three realized seeds), or "
            f"{max(v['mde_power80'] for v in seed_mde.values()) * 100:.1f} points "
            "treating the seed as the experimental unit, at 80% power"),
        "headline_two_level_mde_power80_pt": round(max(
            v["schemes"]["seed+video"]["mde_power80"] for v in two_level.values()
        ) * 100, 2),
        "alpha": ALPHA, "powers": list(POWERS), "level": S.LEVEL,
        "seed_level": {
            "definition": "two-sample t comparison of per-seed video-AUCs, k vs k, "
                          "MDE = (t_{1-a/2,df} + t_{power,df}) * s_pooled * sqrt(2/k)",
            "per_arm": per_seed, "pairs": seed_mde,
        },
        "video_level_unconditional_on_seeds": {
            "definition": "the same MDE formula applied to the two-level "
                          "(seed x video) bootstrap's standard error",
            "source": "seed_uncertainty.json", "per_contrast": two_level,
        },
        "video_level_conditional": {
            "definition": "MDE = (z_{1-a/2} + z_power) * SE, with SE the standard "
                          "deviation of the paired bootstrap distribution; "
                          "conditional on the three realized seeds",
            "source": boot_path.name, "per_contrast": cond, "headline": headline,
        },
    }
    S.write_json(out_path, payload)


if __name__ == "__main__":
    main()
