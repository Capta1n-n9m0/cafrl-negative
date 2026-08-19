"""Multiplicity: do the significant results survive an adjustment?

The paper reports a family of adjudicated contrasts and calls three of them
significant. This script states the family, computes a p-value for each member
from the same bootstrap the intervals come from, and applies Bonferroni and
Holm-Bonferroni over it. It also carries the one significant comparison that is
not a paired contrast — the real-CRF vs synthetic-JPEG training gap, whose
JPEG-side run has no released per-video scores — as a deliberately conservative
unpaired z from the two marginal intervals.

p-values are the normal-approximation two-sided p from the bootstrap standard
error, ``p = 2 * (1 - Phi(|delta| / se))``, because the bootstrap's own
achieved significance level saturates at 1/B for the significant rows (no
replicate of 10,000 crosses zero). Both are reported.

    python multiplicity.py       # needs cluster_bootstrap.json
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import stats_common as S

ALPHA = 0.05

# The +7.3 pt training-data comparison. Neither side has released per-video
# scores for the JPEG arm, so this is an unpaired comparison of two marginal
# bootstrap intervals: conservative by construction, since pairing on the shared
# test videos would shrink the standard error.
JPEG_GAP = {
    "name": "real-CRF - synthetic-JPEG training (Xception, c40)",
    "a": {"run": "b4b_xception_mq_fliponly", "eval_set": "ffpp", "cell": "c40"},
    "b": {"run": "p2a_xcep_jpeg", "eval_set": "p2_probe", "cell": "real_c40"},
    "note": "unpaired: the JPEG arm's report stored no per-video scores",
}


def _se_from_ci(lo: float, hi: float, level: float = 0.95) -> float:
    z = 1.959963984540054 if abs(level - 0.95) < 1e-9 else float("nan")
    return (hi - lo) / (2.0 * z)


def _p_from_z(z: float) -> float:
    return float(math.erfc(abs(z) / math.sqrt(2.0)))


def holm(pvalues: dict[str, float], alpha: float = ALPHA) -> dict[str, dict]:
    """Holm-Bonferroni step-down over a family of p-values."""
    ordered = sorted(pvalues.items(), key=lambda kv: kv[1])
    m = len(ordered)
    out: dict[str, dict] = {}
    still_rejecting = True
    for i, (key, p) in enumerate(ordered):
        threshold = alpha / (m - i)
        if still_rejecting and p <= threshold:
            reject = True
        else:
            reject = False
            still_rejecting = False
        out[key] = {"p": p, "rank": i + 1, "holm_threshold": threshold,
                    "holm_reject": reject}
    return out


def jpeg_gap(pred) -> dict:
    """The unpaired +7.3 pt comparison, from the two released marginal intervals."""
    a_file = pred.file(JPEG_GAP["a"]["run"], JPEG_GAP["a"]["eval_set"])
    a_cell = a_file["cells"][JPEG_GAP["a"]["cell"]]
    a_auc, a_lo, a_hi = a_cell["video_auc"], a_cell["ci_lo"], a_cell["ci_hi"]
    b_file = pred.file(JPEG_GAP["b"]["run"], JPEG_GAP["b"]["eval_set"])
    b_cell = b_file["cells"][JPEG_GAP["b"]["cell"]]
    b_auc = float(b_cell if not isinstance(b_cell, dict) else b_cell["video_auc"])
    b_lo, b_hi = b_file["cells"]["ci"]
    se_a, se_b = _se_from_ci(a_lo, a_hi), _se_from_ci(b_lo, b_hi)
    delta = a_auc - b_auc
    se = math.hypot(se_a, se_b)
    z = delta / se
    return {
        "name": JPEG_GAP["name"], "note": JPEG_GAP["note"],
        "a": {"run": JPEG_GAP["a"]["run"], "auc": a_auc, "ci": [a_lo, a_hi], "se": se_a},
        "b": {"run": JPEG_GAP["b"]["run"], "auc": b_auc, "ci": [b_lo, b_hi], "se": se_b},
        "delta": delta, "se_unpaired": se, "z": z, "p_two_sided_z": _p_from_z(z),
        "intervals_overlap": bool(not (a_lo > b_hi or b_lo > a_hi)),
    }


def main() -> None:
    ap = S.add_common_args(argparse.ArgumentParser(description=__doc__))
    ap.add_argument("--bootstrap", default=None)
    ap.add_argument("--alpha", type=float, default=ALPHA)
    args = ap.parse_args()

    out_path = Path(args.out) if args.out else S.HERE / "multiplicity.json"
    boot = S.read_json(Path(args.bootstrap) if args.bootstrap
                       else S.HERE / "cluster_bootstrap.json")
    pred = S.predictions(args.predictions)
    primary = boot.get("primary_cluster_scheme", S.PRIMARY_CLUSTER)

    members: dict[str, dict] = {}
    for row, entry in boot["contrasts"].items():
        res = entry["schemes"][primary]
        pub = entry["schemes"]["video"]
        members[row] = {
            "name": entry["name"], "table": entry["table"],
            "delta": res["delta"], "se": res["se"], "z": res["z"],
            "p_video_unit": pub["p_two_sided_z"],
            "p": res["p_two_sided_z"],
            "asl_bootstrap": res["asl_two_sided_vs_0"],
            "significant_unadjusted": bool(res["excludes_zero"]),
        }

    gap = jpeg_gap(pred)
    members["G1"] = {
        "name": gap["name"], "table": "appendix", "delta": gap["delta"],
        "se": gap["se_unpaired"], "z": gap["z"], "p": gap["p_two_sided_z"],
        "p_video_unit": gap["p_two_sided_z"],
        "asl_bootstrap": None,
        "significant_unadjusted": bool(not gap["intervals_overlap"]),
        "note": gap["note"],
    }

    families = {
        "contrasts_table": [c.row for c in S.CONTRASTS if c.table == "contrasts"],
        "contrasts_table_plus_faceshifter": [c.row for c in S.CONTRASTS],
        "all_adjudicated_including_training_data_gap":
            [c.row for c in S.CONTRASTS] + ["G1"],
    }

    payload: dict = {
        "what": "multiplicity adjustment over the adjudicated contrast family",
        "alpha": args.alpha,
        "p_value_definition": (
            "two-sided normal-approximation p from the bootstrap standard error, "
            "p = erfc(|delta| / (se * sqrt(2))); the bootstrap's own achieved "
            "significance level is reported alongside and saturates at 1/B"),
        "resampling_unit": primary,
        "unpaired_gap": gap,
        "members": members,
        "families": {},
    }

    for fam, rows in families.items():
        m = len(rows)
        bonf = args.alpha / m
        pv = {r: members[r]["p"] for r in rows}
        h = holm(pv, args.alpha)
        payload["families"][fam] = {
            "m": m, "bonferroni_threshold": bonf,
            "members": {
                r: {"p": pv[r], "bonferroni_survives": bool(pv[r] <= bonf),
                    **h[r]}
                for r in rows},
            "significant_after_bonferroni": [r for r in rows if pv[r] <= bonf],
            "significant_after_holm": [r for r in rows if h[r]["holm_reject"]],
        }
        print(f"family {fam}: m={m}, Bonferroni alpha={bonf:.5f} -> "
              f"survives: {payload['families'][fam]['significant_after_bonferroni']}")

    print(f"\nunpaired training-data gap: delta={gap['delta']:+.4f} "
          f"z={gap['z']:.2f} p={gap['p_two_sided_z']:.2e} "
          f"(intervals overlap: {gap['intervals_overlap']})")
    S.write_json(out_path, payload)


if __name__ == "__main__":
    main()
