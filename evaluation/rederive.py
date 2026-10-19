"""Re-derive the paper's tables from this repository's prediction files.

Everything the manuscript prints about FaceForensics++ evaluation is a function
of the per-video scores in ``predictions/`` and of the code in
``evaluation/src/``, which is the campaign's own harness copied unmodified. This
script is that function, written out: it recomputes the compression sweeps, the
per-seed table and 3-seed bands, the adjudicated contrasts (10,000-replicate
paired video bootstrap), the cross-dataset and held-out-manipulation cells, and
the real-CRF-versus-JPEG probe — and writes them as JSON plus readable Markdown.

It does not check anything against the paper; that is ``verify/verify.py``, which
calls into this module and compares. Run it on its own to simply see the numbers:

    python rederive.py --out ../verify/out

CPU only, no GPU, no dataset. The bootstrap is the expensive part (10,000
resamples per contrast, ~25 s each); ``--jobs`` runs contrasts in parallel and
``--fast`` cuts the replicate count for a quick look — never for a check that is
meant to reproduce a published interval.
"""

from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))          # release_io
sys.path.insert(0, str(HERE / "src"))  # the harness package root: `src.evaluation.…`
sys.path.insert(0, str(HERE.parent))   # so `evaluation/src` resolves as `src.…`

from release_io import COMP_LEVELS, FFPP_LEVELS, Predictions, align  # noqa: E402
from src.evaluation.metrics import (  # noqa: E402
    bootstrap_ci, crf_slope, paired_auc_comp_delta, paired_auc_delta, seed_band, video_auc,
)

DEFAULT_SPEC = HERE.parent / "verify" / "expected.json"


def load_spec(path: str | Path | None = None) -> dict[str, Any]:
    p = Path(path) if path else DEFAULT_SPEC
    if not p.is_file():
        raise SystemExit(f"specification not found: {p}")
    return json.loads(p.read_text())


# ---------------------------------------------------------------------------
# Sweeps: every FF++ cell, recomputed from the released per-video scores
# ---------------------------------------------------------------------------

def sweeps(preds: Predictions) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for run in preds.runs("ffpp"):
        row: dict[str, Any] = {}
        for level in FFPP_LEVELS:
            try:
                c = preds.cell(run, level)
            except Exception:
                continue
            row[level] = {
                "video_auc": video_auc(c["scores"], c["keys"], c["labels"]),
                "stored": c["video_auc"],
                "n_videos": c["n_videos"],
            }
        comp = [row[lv]["video_auc"] for lv in COMP_LEVELS if lv in row]
        out[run] = {
            "levels": row,
            "auc_comp": float(np.mean(comp)) if comp else None,
            "crf_slope": (crf_slope({lv: row[lv]["video_auc"] for lv in row})
                          if len(row) >= 2 else None),
        }
    return out


# ---------------------------------------------------------------------------
# Per-seed values and 3-seed bands
# ---------------------------------------------------------------------------

def seeds(preds: Predictions, spec: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for arm, runs in spec["seed_groups"].items():
        per_seed = []
        for run in runs:
            c = preds.cell(run, spec["seed_level"])
            per_seed.append({
                "run": run,
                "seed": preds.file(run)["seed"],
                "video_auc": video_auc(c["scores"], c["keys"], c["labels"]),
            })
        band = seed_band([r["video_auc"] for r in per_seed])
        out[arm] = {"level": spec["seed_level"], "per_seed": per_seed, "band": band}
    return out


# ---------------------------------------------------------------------------
# Contrasts: the paired video bootstrap, pooled over seeds where an arm has them
# ---------------------------------------------------------------------------

def _paired(preds: Predictions, a_runs: list[str], b_runs: list[str], level: str,
            boot: dict[str, Any], eval_set: str = "ffpp") -> dict[str, Any]:
    """One paired contrast A - B: the point estimate (the un-resampled difference,
    which is what the paper prints) and the paired video bootstrap around it.

    ``level`` is one CRF level, or ``auc_comp`` — the mean over c28-c40, re-sampled
    jointly through the harness's ``paired_auc_comp_delta``."""
    if level == "auc_comp":
        per_a, per_b, labels, keys = {}, {}, None, None
        auc_a, auc_b = [], []
        for lv in COMP_LEVELS:
            a = preds.pool(a_runs, lv, eval_set)
            b = preds.pool(b_runs, lv, eval_set)
            sa, sb, y = align(a, b)
            k = [kk for kk in a["keys"] if kk in set(b["keys"])]
            if keys is None:
                keys, labels = k, y
            elif k != keys or not np.array_equal(y, labels):
                raise ValueError(f"{lv}: video set differs across the compressed levels")
            per_a[lv], per_b[lv] = sa, sb
            auc_a.append(video_auc(sa, k, y))
            auc_b.append(video_auc(sb, k, y))
        res = paired_auc_comp_delta(per_a, per_b, labels, list(COMP_LEVELS),
                                    b=boot["b"], seed=boot["seed"])
        n, aa, ab = len(labels), float(np.mean(auc_a)), float(np.mean(auc_b))
    else:
        a = preds.pool(a_runs, level, eval_set)
        b = preds.pool(b_runs, level, eval_set)
        sa, sb, y = align(a, b)
        k = [kk for kk in a["keys"] if kk in set(b["keys"])]
        res = paired_auc_delta(sa, sb, y, b=boot["b"], seed=boot["seed"])
        n, aa, ab = len(y), float(video_auc(sa, k, y)), float(video_auc(sb, k, y))
    return {
        "n_videos": int(n),
        "auc_a": aa,
        "auc_b": ab,
        # The paper prints the point estimate (decision 2026-10-17, "every delta is
        # printed as a point estimate"); v1.0.0 printed the bootstrap mean, which
        # is kept beside it.
        "delta": aa - ab,
        "delta_boot_mean": res["delta_mean"],
        "ci_lo": res["ci_lo"],
        "ci_hi": res["ci_hi"],
        "p_delta_gt_0": res["p_delta_gt_0"],
        "excludes_zero": res["excludes_zero"],
        "b": res["b"],
        "seed": boot["seed"],
    }


def _one_contrast(job: dict[str, Any]) -> dict[str, Any]:
    preds = Predictions(job["root"])
    out = _paired(preds, job["a"], job["b"], job["level"], job["bootstrap"],
                  job.get("eval_set", "ffpp"))
    return {"name": job["name"], "a": job["a"], "b": job["b"], "level": job["level"], **out}


def contrasts(preds: Predictions, spec: dict[str, Any], jobs: int = 1,
              b_override: int | None = None) -> list[dict[str, Any]]:
    boot = dict(spec["bootstrap"])
    if b_override:
        boot["b"] = b_override
    work = [
        {"name": c["name"], "a": c["a"], "b": c["b"], "level": c["level"],
         "root": str(preds.root), "bootstrap": boot}
        for c in spec["contrasts"]
    ]
    if jobs > 1 and len(work) > 1:
        with ProcessPoolExecutor(max_workers=jobs) as pool:
            return list(pool.map(_one_contrast, work))
    return [_one_contrast(w) for w in work]


# ---------------------------------------------------------------------------
# The cells with no per-video scores: cross-dataset, and the JPEG-augmentation probe
# ---------------------------------------------------------------------------

def cross_dataset(preds: Predictions, spec: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for run in preds.runs("cross_dataset"):
        payload = preds.file(run, "cross_dataset")
        out[run] = {
            cell: {k: v for k, v in body.items() if not isinstance(v, list)}
            for cell, body in payload.get("cells", {}).items()
        }
    return out


def faceshifter(preds: Predictions, spec: dict[str, Any], jobs: int = 1,
                b_override: int | None = None) -> dict[str, Any]:
    """Held-out FaceShifter: per-run AUCs, plus the seed-pooled contrasts."""
    per_run: dict[str, Any] = {}
    for run in preds.runs("faceshifter"):
        row = {}
        for level in spec["faceshifter"]["levels"]:
            c = preds.cell(run, level, "faceshifter")
            row[level] = video_auc(c["scores"], c["keys"], c["labels"])
        per_run[run] = row

    boot = dict(spec["bootstrap"])
    if b_override:
        boot["b"] = b_override
    work = [
        {"name": c["name"], "a": c["a"], "b": c["b"], "level": c["level"],
         "root": str(preds.root), "bootstrap": boot, "eval_set": "faceshifter"}
        for c in spec["faceshifter"].get("contrasts", [])
    ]
    results = []
    for w in work:
        out = _paired(Predictions(w["root"]), w["a"], w["b"], w["level"], w["bootstrap"],
                      "faceshifter")
        results.append({"name": w["name"], "level": w["level"], **out})
    return {"per_run": per_run, "contrasts": results}


def probe(preds: Predictions, spec: dict[str, Any]) -> dict[str, Any]:
    """The real-CRF versus synthetic-JPEG comparison (two marginal AUCs)."""
    p = spec["probe"]
    cells = preds.file(p["jpeg_run"], "p2_probe")["cells"]
    jpeg_auc = preds.metric(p["jpeg_run"], p["jpeg_cell"], eval_set="p2_probe")
    jpeg_ci = list(cells.get("ci") or [float("nan"), float("nan")])
    c = preds.cell(p["crf_run"], p["level"])
    crf_auc = video_auc(c["scores"], c["keys"], c["labels"])
    crf_lo, crf_hi = bootstrap_ci(c["scores"], c["labels"], b=spec["bootstrap"]["b"],
                                  seed=spec["bootstrap"]["seed"])
    return {
        "jpeg": {"run": p["jpeg_run"], "video_auc": jpeg_auc,
                 "ci_lo": jpeg_ci[0], "ci_hi": jpeg_ci[1],
                 "per_video_scores": False},
        "crf": {"run": p["crf_run"], "video_auc": crf_auc,
                "ci_lo": crf_lo, "ci_hi": crf_hi, "per_video_scores": True},
        "gap": crf_auc - jpeg_auc,
        "note": p["note"],
    }


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

def _md_sweeps(res: dict[str, Any]) -> str:
    lines = ["## Compression sweeps (video-AUC, FF++ test)", "",
             "| run | " + " | ".join(FFPP_LEVELS) + " | AUC_comp |", "|---" * 9 + "|"]
    for run in sorted(res):
        row = res[run]["levels"]
        cells = [f"{row[lv]['video_auc']:.4f}" if lv in row else "—" for lv in FFPP_LEVELS]
        comp = f"{res[run]['auc_comp']:.4f}" if res[run]["auc_comp"] is not None else "—"
        lines.append(f"| `{run}` | " + " | ".join(cells) + f" | {comp} |")
    return "\n".join(lines)


def _md_seeds(res: dict[str, Any]) -> str:
    lines = ["## Per-seed values and 3-seed bands", "",
             "| arm | per-seed video-AUC | mean | std | 95% band |", "|---|---|---|---|---|"]
    for arm, body in res.items():
        vals = ", ".join(f"{r['video_auc']:.4f}" for r in body["per_seed"])
        bd = body["band"]
        lines.append(
            f"| {arm} | {vals} | {bd['mean']:.4f} | {bd['std']:.4f} | "
            f"±{bd['half_width']:.4f} |")
    return "\n".join(lines)


def _md_contrasts(res: list[dict[str, Any]]) -> str:
    lines = ["## The adjudicated contrasts (10k paired video bootstrap)", "",
             "Δ is the point estimate (the un-resampled difference, what the paper "
             "prints); the bootstrap mean is shown beside it.", "",
             "| contrast | level | Δ | bootstrap mean | 95% CI | P(Δ>0) | CI excludes 0 |",
             "|---|---|---|---|---|---|---|"]
    for r in res:
        lines.append(
            f"| {r['name']} | {r['level']} | {r['delta']:+.4f} | {r['delta_boot_mean']:+.4f} | "
            f"[{r['ci_lo']:+.4f}, {r['ci_hi']:+.4f}] | "
            f"{r['p_delta_gt_0']:.2f} | {'yes' if r['excludes_zero'] else 'no'} |")
    return "\n".join(lines)


def _md_faceshifter(res: dict[str, Any]) -> str:
    lines = ["## Held-out manipulation (FaceShifter, n=280)", "",
             "| run | c23 | c40 |", "|---|---|---|"]
    for run in sorted(res["per_run"]):
        row = res["per_run"][run]
        lines.append(f"| `{run}` | " + " | ".join(f"{row[lv]:.4f}" for lv in sorted(row)) + " |")
    if res["contrasts"]:
        lines += ["", "| pooled contrast | level | Δ | 95% CI |", "|---|---|---|---|"]
        for r in res["contrasts"]:
            lines.append(f"| {r['name']} | {r['level']} | {r['delta']:+.4f} | "
                         f"[{r['ci_lo']:+.4f}, {r['ci_hi']:+.4f}] |")
    return "\n".join(lines)


def _md_cross(res: dict[str, Any]) -> str:
    cells = sorted({c for body in res.values() for c in body})
    lines = ["## Cross-dataset cells (marginal statistics; no per-video scores released)", "",
             "| run | " + " | ".join(cells) + " |", "|---" * (len(cells) + 1) + "|"]
    for run in sorted(res):
        vals = []
        for c in cells:
            body = res[run].get(c)
            vals.append(f"{body['video_auc']:.4f}" if body and "video_auc" in body else "—")
        lines.append(f"| `{run}` | " + " | ".join(vals) + " |")
    return "\n".join(lines)


def _md_probe(res: dict[str, Any]) -> str:
    j, c = res["jpeg"], res["crf"]
    return "\n".join([
        "## Compression diversification: real CRF re-encodes vs synthetic JPEG", "",
        "| arm | video-AUC @ c40 | 95% CI |", "|---|---|---|",
        f"| `{j['run']}` (synthetic JPEG) | {j['video_auc']:.4f} | "
        f"[{j['ci_lo']:.4f}, {j['ci_hi']:.4f}] |",
        f"| `{c['run']}` (real CRF) | {c['video_auc']:.4f} | "
        f"[{c['ci_lo']:.4f}, {c['ci_hi']:.4f}] |",
        "", f"Gap: **{res['gap'] * 100:.1f} pt**. {res['note']}",
    ])


# ---------------------------------------------------------------------------

def rederive_all(root: Path | None, spec: dict[str, Any], jobs: int = 1,
                 b_override: int | None = None) -> dict[str, Any]:
    preds = Predictions(root)
    return {
        "sweeps": sweeps(preds),
        "seeds": seeds(preds, spec),
        "contrasts": contrasts(preds, spec, jobs=jobs, b_override=b_override),
        "faceshifter": faceshifter(preds, spec, jobs=jobs, b_override=b_override),
        "cross_dataset": cross_dataset(preds, spec),
        "probe": probe(preds, spec),
    }


def render(res: dict[str, Any]) -> str:
    return "\n\n".join([
        "# Tables re-derived from `predictions/`",
        "",
        "Produced by `evaluation/rederive.py` using `evaluation/src/` — the "
        "campaign's own harness — over the released per-video scores. No GPU, no "
        "dataset, no network.",
        _md_sweeps(res["sweeps"]),
        _md_seeds(res["seeds"]),
        _md_contrasts(res["contrasts"]),
        _md_faceshifter(res["faceshifter"]),
        _md_cross(res["cross_dataset"]),
        _md_probe(res["probe"]),
        "",
    ])


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--predictions", default=None, help="predictions/ directory")
    ap.add_argument("--spec", default=None, help="what to compute (verify/expected.json)")
    ap.add_argument("--out", default=None, help="write tables.json + TABLES.md here")
    ap.add_argument("--jobs", type=int, default=1, help="parallel bootstrap workers")
    ap.add_argument("--fast", action="store_true",
                    help="1,000 replicates instead of 10,000 (exploration only)")
    args = ap.parse_args(argv)

    spec = load_spec(args.spec)
    res = rederive_all(Path(args.predictions) if args.predictions else None, spec,
                       jobs=args.jobs, b_override=1000 if args.fast else None)
    text = render(res)
    if args.out:
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        (out / "tables.json").write_text(json.dumps(res, indent=1, default=float) + "\n")
        (out / "TABLES.md").write_text(text)
        print(f"wrote {out / 'tables.json'} and {out / 'TABLES.md'}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
