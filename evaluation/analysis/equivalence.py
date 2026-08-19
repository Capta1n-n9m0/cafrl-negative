"""Equivalence tests (TOST) for the paper's two neutral headline contrasts.

A confidence interval that includes zero licenses "we could not detect a
difference", never "there is no difference". The neutral verdicts in this paper
are equivalence claims, so they are tested as equivalence claims here: two
one-sided tests against an equivalence margin of **delta = 1 AUC point**, which
is concluded when the whole 90% interval of the paired bootstrap lies inside
(-delta, +delta).

**The margin is post hoc.** It was chosen after the results existed, and the
paper says so wherever the test is reported. Its justification is on the paper's
own scale: re-running the plain spatial baseline at a different random seed moves
its c40 video-AUC by more than a point (its 95% three-seed band is +/-1.60 pt,
across-seed SD 0.65 pt), and doubling the width of the spatial trunk — a real
architectural change — buys about 1 pt. A difference smaller than either is
below the resolution at which this study can act.

The test is run against every resampling unit available: the published video
unit, the four cluster units of `cluster_bootstrap.py`, and the two-level
seed x video bootstrap of `seed_uncertainty.py`. Reporting all of them is the
point — the conclusion is not the same in all of them, and the difference is
exactly the seed-conditionality the reviewers asked about.

    python equivalence.py        # needs cluster_bootstrap.json + seed_uncertainty.json
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import stats_common as S


def _phi_sf(z: float) -> float:
    """Upper-tail normal probability."""
    return 0.5 * math.erfc(z / math.sqrt(2.0))


def tost(res: dict, margin: float) -> dict:
    """Two one-sided tests from a bootstrap Δ distribution summary."""
    lo90, hi90 = res["ci90_lo"], res["ci90_hi"]
    within = bool(lo90 > -margin and hi90 < +margin)
    # bootstrap achieved significance levels (tail mass beyond each margin)
    p_lower = res["asl_le_minus_margin"]   # H01: Δ <= -margin
    p_upper = res["asl_ge_plus_margin"]    # H02: Δ >= +margin
    out = {
        "scheme": res["scheme"],
        "delta": res["delta"],
        "se": res["se"],
        "ci90": [lo90, hi90],
        "ci90_lo": lo90, "ci90_hi": hi90,
        "ci95": [res["ci_lo"], res["ci_hi"]],
        "ci95_lo": res["ci_lo"], "ci95_hi": res["ci_hi"],
        "margin": margin,
        "ci90_within_margin": within,
        "equivalence_concluded": within,
        "p_tost_bootstrap": max(p_lower, p_upper),
        "p_tost_bootstrap_lower": p_lower,
        "p_tost_bootstrap_upper": p_upper,
        # the smallest margin this interval would have concluded equivalence at
        "smallest_margin_concluded": max(abs(lo90), abs(hi90)),
    }
    if res["se"] > 0:
        z_lo = (res["delta"] + margin) / res["se"]
        z_hi = (margin - res["delta"]) / res["se"]
        out["p_tost_normal"] = max(_phi_sf(z_lo), _phi_sf(z_hi))
    return out


def main() -> None:
    ap = S.add_common_args(argparse.ArgumentParser(description=__doc__))
    ap.add_argument("--margin", type=float, default=S.DELTA_MARGIN)
    ap.add_argument("--bootstrap", default=None)
    ap.add_argument("--seed-bootstrap", default=None)
    args = ap.parse_args()

    out_path = Path(args.out) if args.out else S.HERE / "equivalence.json"
    boot = S.read_json(Path(args.bootstrap) if args.bootstrap
                       else S.HERE / "cluster_bootstrap.json")
    seed = S.read_json(Path(args.seed_bootstrap) if args.seed_bootstrap
                       else S.HERE / "seed_uncertainty.json")

    payload: dict = {
        "what": "two one-sided tests (TOST) of the neutral headline contrasts",
        "margin": args.margin,
        "margin_is_post_hoc": True,
        "margin_justification": (
            "on the paper's own scale: the plain spatial baseline's own 95% three-seed "
            "band at c40 is +/-1.60 pt (across-seed SD 0.65 pt), and widening the "
            "spatial trunk is worth about 1 pt"),
        "rule": "equivalence is concluded when the whole 90% percentile interval of "
                "the paired bootstrap lies inside (-margin, +margin)",
        "contrasts": {},
    }

    for row in S.HEADLINE_ROWS:
        entry: dict = {"name": S.CONTRAST_BY_ROW[row].name, "schemes": {}}
        for scheme, res in boot["contrasts"][row]["schemes"].items():
            entry["schemes"][scheme] = tost(res, args.margin)
        for scheme, res in seed["contrasts"][row]["schemes"].items():
            entry["schemes"][scheme] = tost(res, args.margin)
        conditional = [v for k, v in entry["schemes"].items() if not k.startswith("seed+")]
        unconditional = [v for k, v in entry["schemes"].items() if k.startswith("seed+")]
        entry["equivalence_all_video_and_cluster_units"] = all(
            v["equivalence_concluded"] for v in conditional)
        entry["equivalence_two_level"] = all(
            v["equivalence_concluded"] for v in unconditional)
        entry["worst_p_tost_conditional"] = max(v["p_tost_bootstrap"] for v in conditional)
        entry["smallest_margin_conditional"] = max(
            v["smallest_margin_concluded"] for v in conditional)
        entry["smallest_margin_two_level"] = max(
            v["smallest_margin_concluded"] for v in unconditional)
        payload["contrasts"][row] = entry
        print(f"{row} {entry['name']}")
        for scheme, v in entry["schemes"].items():
            print(f"   {scheme:12s} 90% CI [{v['ci90'][0]:+.5f}, {v['ci90'][1]:+.5f}] "
                  f"within +/-{args.margin:.3f}: {str(v['equivalence_concluded']):5s} "
                  f"p_TOST={v['p_tost_bootstrap']:.4f}")

    payload["equivalence_concluded_conditional_all_rows"] = all(
        e["equivalence_all_video_and_cluster_units"] for e in payload["contrasts"].values())
    payload["equivalence_concluded_two_level_all_rows"] = all(
        e["equivalence_two_level"] for e in payload["contrasts"].values())
    S.write_json(out_path, payload)


if __name__ == "__main__":
    main()
