"""``aggregate_runs.py`` — Phase 5 Step 5.2: multi-seed aggregator + A1 win-rule.

Consumes per-run ``report.json`` files (from ``eval_battery.py``), groups them by
arm, **seed-pools** the per-video predictions BY KEY, and applies the
**panel-hardened, pre-registered A1 win-rule** (phase5.md Step 5.2, CRUX-3). The
output table is emitted IDENTICALLY whether the verdict is WIN or NULL — the rule
is **SYMMETRIC** and can declare GRL (A0) the loser; there is no parsimony tiebreak
favouring GRL.

This module is the frozen adjudication machinery. The exact, verbatim rule (incl.
every threshold pinned below) lives in ``runs/phase5_build/PREREGISTRATION-A1.md``,
committed + git-tagged BEFORE the A1 runs complete. Do NOT re-interpret a pinned
threshold after data is observed — that PARKS to the human (the integrity floor).

The PRIMARY endpoint is ``AUC_comp`` = mean video-AUC over {c28,c32,c36,c40}. The
PRIMARY decisive test is the **paired video-resampling bootstrap** of
Δ = AUC_comp(best) − AUC_comp(runner-up) on the **seed-pooled** per-video
predictions (``metrics.paired_auc_comp_delta``). Marginal per-arm CI overlap is a
descriptive sidecar only — never the inter-arm test.

WIN requires ALL of (verbatim, pinned):
  (1) best arm has the strictly highest 3-seed-mean ``AUC_comp``;
  (2) the paired-Δ bootstrap CI vs the runner-up excludes 0 (positive side);
  (3) the seed-mean gap > the across-seed band ``4.30·s/√3`` — PINNED as
      ``gap > max(half_width_best, half_width_runnerup)`` (the larger single-arm
      band; conservative, symmetric);
  (4) c23 video-AUC shows no regression beyond the ~0.5-pt noise band — PINNED as
      ``best.c23_mean ≥ runnerup.c23_mean − 0.005`` AND the winner's drop
      ``Δ = AUC@c23 − AUC_comp`` ≤ the runner-up's drop (can't win by being a
      uniformly-better detector that is LESS invariant).
Else: NULL — "no compression-invariance mechanism dominates within seed+test
noise" (an acceptable, registered outcome; do NOT p-hack toward a winner).

Pre-registered escalation (CRUX-1 tripwire): any arm whose per-seed ``AUC_comp``
std (ddof=1) > 0.005 (0.5 pt) is FLAGGED ``escalate`` — escalate that arm to 5
seeds BEFORE adjudicating.

Run::

    python -m src.evaluation.aggregate_runs --manifest manifest.json --out verdict
    # manifest.json = {"none": ["runs/a1_none_s42/report.json", ...], "grl": [...], ...}
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any

import numpy as np

from src.evaluation.metrics import auc_comp, paired_auc_comp_delta, seed_band

_LOG = logging.getLogger("src.evaluation.aggregate_runs")

DEFAULT_COMP_LEVELS: tuple[str, ...] = ("c28", "c32", "c36", "c40")

# PINNED thresholds (frozen; mirror PREREGISTRATION-A1.md exactly).
C23_NOISE_BAND: float = 0.005      # criterion (4): clean-AUC regression tolerance
ESCALATE_SEED_STD: float = 0.005   # tripwire: per-seed AUC_comp std > 0.5 pt → 5 seeds
BOOTSTRAP_B: int = 10_000


# ---------------------------------------------------------------------------
# Seed-pooling (align per-video preds BY KEY across an arm's seeds)
# ---------------------------------------------------------------------------

def _cell_preds(report: dict[str, Any], level: str) -> dict[str, tuple[float, int]]:
    """Extract ``{key: (score, label)}`` for one level from one run's report."""
    cell = report.get("sweep", {}).get(level, {})
    if cell.get("status") != "ok" or "video_scores" not in cell:
        raise ValueError(
            f"report {report.get('run')!r} level {level}: no per-video preds "
            f"(status={cell.get('status')}). Re-run eval_battery with return_preds."
        )
    keys = cell["video_keys"]
    scores = cell["video_scores"]
    labels = cell["video_labels"]
    return {str(k): (float(s), int(y)) for k, s, y in zip(keys, scores, labels)}


def seed_pool_level(reports: list[dict[str, Any]], level: str) -> dict[str, Any]:
    """Seed-pool one level's per-video preds across an arm's seed runs, by key.

    Aligns on the **intersection** of video keys present in every seed (warns on a
    mismatch), then averages each video's score across seeds. Asserts label
    consistency across seeds. Returns ``{"keys", "scores", "labels"}`` in sorted-key
    order (deterministic + comparable across arms).
    """
    per_seed = [_cell_preds(r, level) for r in reports]
    keysets = [set(d) for d in per_seed]
    common = set.intersection(*keysets) if keysets else set()
    union = set.union(*keysets) if keysets else set()
    if len(common) != len(union):
        _LOG.warning("level %s: %d/%d keys common across %d seeds (dropping non-common)",
                     level, len(common), len(union), len(reports))
    keys = sorted(common)
    scores = np.empty(len(keys), dtype=np.float64)
    labels = np.empty(len(keys), dtype=np.int64)
    for i, k in enumerate(keys):
        ss = [d[k][0] for d in per_seed]
        ys = {d[k][1] for d in per_seed}
        if len(ys) != 1:
            raise ValueError(f"level {level} key {k!r}: inconsistent labels across seeds {ys}")
        scores[i] = float(np.mean(ss))
        labels[i] = int(ys.pop())
    return {"keys": keys, "scores": scores, "labels": labels}


# ---------------------------------------------------------------------------
# Per-arm summary
# ---------------------------------------------------------------------------

def summarize_arm(
    arm: str, reports: list[dict[str, Any]], comp_levels: tuple[str, ...],
) -> dict[str, Any]:
    """Per-arm: per-seed AUC_comp/c23/drop, seed-mean + band, escalate flag, pooled preds."""
    if not reports:
        raise ValueError(f"arm {arm!r} has no reports")
    per_seed_comp = [float(r["AUC_comp"]) for r in reports if r.get("AUC_comp") is not None]
    per_seed_c23 = [float(r["AUC_c23"]) for r in reports if r.get("AUC_c23") is not None]
    per_seed_drop = [float(r["drop"]) for r in reports if r.get("drop") is not None]
    per_seed_slope = [r.get("crf_slope") for r in reports]
    seeds = [r.get("seed") for r in reports]
    if len(per_seed_comp) != len(reports):
        _LOG.warning("arm %s: %d/%d reports have AUC_comp", arm,
                     len(per_seed_comp), len(reports))

    comp_band = seed_band(per_seed_comp)
    comp_std = float(np.std(per_seed_comp, ddof=1)) if len(per_seed_comp) >= 2 else float("nan")
    escalate = bool(comp_std > ESCALATE_SEED_STD) if comp_std == comp_std else False

    # Seed-pooled per-video preds for the comp levels (paired-bootstrap input).
    pooled = {lv: seed_pool_level(reports, lv) for lv in comp_levels}
    # Pooled-prediction AUC_comp point estimate (reported alongside the seed-mean).
    lv0 = comp_levels[0]
    labels = pooled[lv0]["labels"]
    keys0 = pooled[lv0]["keys"]
    # All comp levels share the same FF++ test videos ⇒ same key order; assert.
    for lv in comp_levels:
        if pooled[lv]["keys"] != keys0:
            raise ValueError(f"arm {arm}: comp level {lv} key order differs from {lv0}")
    pooled_scores = {lv: pooled[lv]["scores"] for lv in comp_levels}
    auc_comp_pooled = auc_comp(pooled_scores, labels, comp_levels)

    return {
        "arm": arm,
        "n_seeds": len(reports),
        "seeds": seeds,
        "per_seed_auc_comp": per_seed_comp,
        "per_seed_auc_c23": per_seed_c23,
        "per_seed_drop": per_seed_drop,
        "per_seed_crf_slope": per_seed_slope,
        "auc_comp_mean": comp_band["mean"],          # criterion (1) ranking statistic
        "auc_comp_std": comp_std,
        "auc_comp_band_half": comp_band["half_width"],
        "auc_comp_pooled": auc_comp_pooled,          # pooled-pred point estimate
        "auc_c23_mean": float(np.mean(per_seed_c23)) if per_seed_c23 else float("nan"),
        "drop_mean": float(np.mean(per_seed_drop)) if per_seed_drop else float("nan"),
        "crf_slope_mean": (float(np.nanmean([s for s in per_seed_slope if s is not None]))
                           if any(s is not None for s in per_seed_slope) else float("nan")),
        "escalate": escalate,
        "_pooled_scores": pooled_scores,             # private: for the paired test
        "_labels": labels,
        "_keys": keys0,
    }


def _align_for_paired(a: dict[str, Any], b: dict[str, Any], comp_levels):
    """Align two arms' seed-pooled preds to common video keys per level."""
    keys_a = {k: i for i, k in enumerate(a["_keys"])}
    keys_b = {k: i for i, k in enumerate(b["_keys"])}
    common = [k for k in a["_keys"] if k in keys_b]
    ia = [keys_a[k] for k in common]
    ib = [keys_b[k] for k in common]
    labels_a = a["_labels"][ia]
    labels_b = b["_labels"][ib]
    if not np.array_equal(labels_a, labels_b):
        raise ValueError("paired align: labels differ between arms on common keys")
    pla = {lv: a["_pooled_scores"][lv][ia] for lv in comp_levels}
    plb = {lv: b["_pooled_scores"][lv][ib] for lv in comp_levels}
    return pla, plb, labels_a


# ---------------------------------------------------------------------------
# The 4-criterion WIN decision (frozen)
# ---------------------------------------------------------------------------

def adjudicate(
    summaries: list[dict[str, Any]], comp_levels: tuple[str, ...],
    *, b: int = BOOTSTRAP_B, seed: int = 0,
) -> dict[str, Any]:
    """Apply the pre-registered 4-criterion WIN rule (SYMMETRIC; NULL fallback)."""
    ranked = sorted(summaries, key=lambda s: s["auc_comp_mean"], reverse=True)
    out: dict[str, Any] = {
        "ranking": [s["arm"] for s in ranked],
        "comp_levels": list(comp_levels),
        "escalations": [s["arm"] for s in summaries if s["escalate"]],
    }
    if len(ranked) < 2:
        out["verdict"] = "INSUFFICIENT_ARMS"
        out["note"] = "need ≥2 arms to adjudicate; per-arm seed-mean + band emitted"
        return out

    best, runner = ranked[0], ranked[1]
    pla, plb, labels = _align_for_paired(best, runner, comp_levels)
    paired = paired_auc_comp_delta(pla, plb, labels, comp_levels, b=b, ci=0.95, seed=seed)

    gap = best["auc_comp_mean"] - runner["auc_comp_mean"]
    band = max(
        best["auc_comp_band_half"] if best["auc_comp_band_half"] == best["auc_comp_band_half"] else 0.0,
        runner["auc_comp_band_half"] if runner["auc_comp_band_half"] == runner["auc_comp_band_half"] else 0.0,
    )

    c1 = gap > 0.0                                              # strictly highest mean
    c2 = bool(paired["excludes_zero_positive"])                # paired CI excludes 0 (+)
    c3 = gap > band                                            # > across-seed band
    c4 = (best["auc_c23_mean"] >= runner["auc_c23_mean"] - C23_NOISE_BAND
          and best["drop_mean"] <= runner["drop_mean"])        # no clean regression + more invariant

    win = c1 and c2 and c3 and c4
    out.update({
        "best_arm": best["arm"],
        "runner_up": runner["arm"],
        "seed_mean_gap": gap,
        "across_seed_band": band,
        "paired_delta": {k: paired[k] for k in
                         ("delta_mean", "ci_lo", "ci_hi", "p_delta_gt_0",
                          "excludes_zero_positive", "n_videos", "n_redraws")},
        "criteria": {
            "c1_strictly_highest_mean": c1,
            "c2_paired_ci_excludes_zero_pos": c2,
            "c3_gap_exceeds_seed_band": c3,
            "c4_no_c23_regression_and_more_invariant": c4,
        },
        "verdict": ("WIN:" + best["arm"]) if win else "NULL",
        "null_statement": None if win else
            "no compression-invariance mechanism dominates within seed+test noise; "
            "headline rests on compression-LEVEL conditioning + curriculum.",
    })
    return out


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def _md_table(summaries: list[dict[str, Any]], decision: dict[str, Any]) -> str:
    lines = [
        "| arm | n | AUC_comp (seed-mean ± 4.30·s/√3) | per-seed AUC_comp | AUC@c23 | drop Δ | crf_slope | escalate |",
        "|---|---|---|---|---|---|---|---|",
    ]
    order = {a: i for i, a in enumerate(decision.get("ranking", []))}
    for s in sorted(summaries, key=lambda x: order.get(x["arm"], 99)):
        hw = s["auc_comp_band_half"]
        band = f"±{hw:.4f}" if hw == hw else "±nan"
        ps = ", ".join(f"{v:.4f}" for v in s["per_seed_auc_comp"])
        lines.append(
            f"| {s['arm']} | {s['n_seeds']} | {s['auc_comp_mean']:.4f} {band} | {ps} | "
            f"{s['auc_c23_mean']:.4f} | {s['drop_mean']:.4f} | "
            f"{s['crf_slope_mean']:.5f} | {'⚠️' if s['escalate'] else '—'} |"
        )
    out = ["## Per-arm summary (SYMMETRIC — emitted identically regardless of verdict)", "",
           *lines, ""]
    if "paired_delta" in decision:
        pd = decision["paired_delta"]
        out += [
            f"## Decisive test — paired Δ(AUC_comp): **{decision['best_arm']}** vs "
            f"**{decision['runner_up']}** (runner-up)", "",
            f"- Δ mean = {pd['delta_mean']:+.4f}, 95% paired CI "
            f"[{pd['ci_lo']:+.4f}, {pd['ci_hi']:+.4f}], P(Δ>0) = {pd['p_delta_gt_0']:.3f}",
            f"- seed-mean gap = {decision['seed_mean_gap']:+.4f}; across-seed band = "
            f"{decision['across_seed_band']:.4f}",
            "",
            "### 4 criteria (ALL required for WIN)",
            f"- (1) strictly highest 3-seed-mean AUC_comp: {decision['criteria']['c1_strictly_highest_mean']}",
            f"- (2) paired-Δ CI excludes 0 (positive): {decision['criteria']['c2_paired_ci_excludes_zero_pos']}",
            f"- (3) gap > across-seed band: {decision['criteria']['c3_gap_exceeds_seed_band']}",
            f"- (4) no c23 regression + winner more invariant: {decision['criteria']['c4_no_c23_regression_and_more_invariant']}",
            "",
            f"## VERDICT: **{decision['verdict']}**",
        ]
        if decision.get("null_statement"):
            out += ["", f"> {decision['null_statement']}"]
    else:
        out += [f"## VERDICT: **{decision.get('verdict')}** — {decision.get('note','')}"]
    if decision.get("escalations"):
        out += ["", f"**Escalation tripwire fired** (seed-std AUC_comp > {ESCALATE_SEED_STD}): "
                f"{decision['escalations']} → 5 seeds BEFORE adjudicating."]
    return "\n".join(out)


def aggregate(manifest: dict[str, list[str]], comp_levels: tuple[str, ...],
              *, b: int = BOOTSTRAP_B, seed: int = 0) -> dict[str, Any]:
    """Load a manifest ``{arm: [report.json, ...]}`` → summaries + the win-rule decision."""
    summaries = []
    for arm, paths in manifest.items():
        reports = [json.loads(Path(p).read_text()) for p in paths]
        summaries.append(summarize_arm(arm, reports, comp_levels))
    decision = adjudicate(summaries, comp_levels, b=b, seed=seed)
    public = [{k: v for k, v in s.items() if not k.startswith("_")} for s in summaries]
    return {"summaries": public, "decision": decision,
            "markdown": _md_table(summaries, decision)}


def main(argv: list[str] | None = None) -> None:
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(name)s %(levelname)s %(message)s")
    p = argparse.ArgumentParser(prog="src.evaluation.aggregate_runs",
                                description="Multi-seed aggregator + A1 win-rule (Phase 5).")
    p.add_argument("--manifest", required=True,
                   help='JSON {"arm": ["report.json", ...], ...}')
    p.add_argument("--comp-levels", default=None, help="comma-sep (default c28,c32,c36,c40)")
    p.add_argument("--out", default=None, help="output stem (writes .json + .md)")
    p.add_argument("--b", type=int, default=BOOTSTRAP_B)
    args = p.parse_args(argv)

    manifest = json.loads(Path(args.manifest).read_text())
    comp_levels = (tuple(args.comp_levels.split(",")) if args.comp_levels
                   else DEFAULT_COMP_LEVELS)
    result = aggregate(manifest, comp_levels, b=args.b)
    print(result["markdown"])
    if args.out:
        Path(args.out + ".json").write_text(json.dumps(
            {"summaries": result["summaries"], "decision": result["decision"]}, indent=2))
        Path(args.out + ".md").write_text(result["markdown"])
        _LOG.info("wrote %s.json + %s.md", args.out, args.out)


if __name__ == "__main__":
    main()
