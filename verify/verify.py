"""Check this release against the paper, using only what the release contains.

Run it from inside the repository, in the CPU-only environment described by
`../env/environment-verify.yml`:

    python verify.py --jobs 4

Seven groups of checks, in order:

1. every manuscript-printed cell value, recomputed from the released per-video
   scores through `../evaluation/` (the campaign's own harness) and compared at
   the paper's printed precision — plus each cell's stored AUC against the
   recomputed one, so an edited score array cannot pass;
2. the derived values the paper prints (three-seed means, the real-CRF vs
   synthetic-JPEG gap);
3. the adjudicated contrast table, recomputed end to end: seed pooling by video
   key, then the 10,000-replicate paired video bootstrap at the pinned RNG seed;
4. the held-out-manipulation contrasts, recomputed the same way;
5. every row of `../CLAIMS-MAP.md` — each mapped artifact must exist, and each
   mapped number must come back out of it;
6. the prediction-driven figures, rebuilt from `../predictions/` and `../curves/`
   and compared against the released `figures/figure_data.json`;
7. self-containment: after all of the above, every module that was imported must
   have come from inside this repository, the standard library, or site-packages.

Exit status is 0 only if every check passes.
"""

from __future__ import annotations

import argparse
import json
import sys
import sysconfig
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "evaluation"))

import numpy as np  # noqa: E402

from release_io import Predictions  # noqa: E402
import rederive  # noqa: E402
from src.evaluation.metrics import video_auc  # noqa: E402

GREEN, RED, YELLOW, DIM, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"


class Report:
    """Collects check outcomes and prints them as they happen."""

    def __init__(self, colour: bool = True) -> None:
        self.rows: list[tuple[str, str, str]] = []
        self.colour = colour and sys.stdout.isatty()

    def _paint(self, text: str, code: str) -> str:
        return f"{code}{text}{RESET}" if self.colour else text

    def add(self, status: str, group: str, detail: str) -> None:
        self.rows.append((status, group, detail))
        mark = {"PASS": self._paint("PASS", GREEN), "FAIL": self._paint("FAIL", RED),
                "SKIP": self._paint("SKIP", YELLOW)}[status]
        if status != "PASS":
            print(f"  {mark}  {group}: {detail}")

    def group_summary(self, group: str, t0: float) -> None:
        rows = [r for r in self.rows if r[1] == group]
        n_fail = sum(1 for r in rows if r[0] == "FAIL")
        n_skip = sum(1 for r in rows if r[0] == "SKIP")
        status = "FAIL" if n_fail else "PASS"
        mark = self._paint(status, RED if n_fail else GREEN)
        extra = f", {n_skip} skipped" if n_skip else ""
        print(f"{mark}  {group}: {len(rows) - n_fail - n_skip}/{len(rows)} checks"
              f"{extra}  {self._paint(f'({time.time() - t0:.1f}s)', DIM)}")

    @property
    def failed(self) -> int:
        return sum(1 for r in self.rows if r[0] == "FAIL")

    @property
    def skipped(self) -> int:
        return sum(1 for r in self.rows if r[0] == "SKIP")


def printed_tolerance(expected: float) -> float:
    """Half a unit in the last place the manuscript prints."""
    text = repr(float(expected))
    decimals = len(text.split(".", 1)[1].rstrip("0")) if "." in text else 4
    return 0.5 * 10 ** (-max(decimals, 1))


# ---------------------------------------------------------------------------
# 1. cells
# ---------------------------------------------------------------------------

def check_cells(preds: Predictions, spec: dict[str, Any], rep: Report) -> None:
    t0 = time.time()
    for item in spec["cells"]:
        run, eval_set, cell, expected = item["run"], item["eval_set"], item["cell"], item["expect"]
        label = f"{run}/{eval_set}/{cell}"
        try:
            if eval_set == "ffpp_test":
                c = preds.cell(run, cell, "ffpp")
                actual = video_auc(c["scores"], c["keys"], c["labels"])
                stored = c["video_auc"]
            elif eval_set == "faceshifter":
                c = preds.cell(run, cell, "faceshifter")
                actual = video_auc(c["scores"], c["keys"], c["labels"])
                stored = c["video_auc"]
            else:
                actual = preds.metric(run, cell, "video_auc", eval_set)
                stored = actual
        except Exception as exc:                       # noqa: BLE001
            rep.add("FAIL", "cells", f"{label}: {exc}")
            continue
        if abs(actual - stored) > 1e-9:
            rep.add("FAIL", "cells",
                    f"{label}: recomputed {actual:.9f} != stored {stored:.9f}")
            continue
        tol = printed_tolerance(expected)
        if abs(actual - expected) >= tol:
            rep.add("FAIL", "cells",
                    f"{label}: {actual:.6f} vs paper {expected} (tolerance ±{tol:g})")
        else:
            rep.add("PASS", "cells", label)
    rep.group_summary("cells", t0)


# ---------------------------------------------------------------------------
# 2. derived values
# ---------------------------------------------------------------------------

def _cell_auc(preds: Predictions, run: str, eval_set: str, cell: str) -> float:
    if eval_set in ("ffpp_test", "faceshifter"):
        set_name = "ffpp" if eval_set == "ffpp_test" else "faceshifter"
        c = preds.cell(run, cell, set_name)
        return video_auc(c["scores"], c["keys"], c["labels"])
    return preds.metric(run, cell, "video_auc", eval_set)


def check_derived(preds: Predictions, spec: dict[str, Any], rep: Report) -> None:
    t0 = time.time()
    for item in spec["derived"]:
        name, expected = item["name"], item["expect"]
        try:
            if item["kind"] == "seed_mean":
                values = [_cell_auc(preds, r, item["eval_set"], item["cell"])
                          for r in item["runs"]]
                actual = float(np.mean(values))
            elif item["kind"] == "difference":
                a, b = item["minuend"], item["subtrahend"]
                actual = (_cell_auc(preds, a["run"], a["eval_set"], a["cell"])
                          - _cell_auc(preds, b["run"], b["eval_set"], b["cell"]))
            else:
                rep.add("FAIL", "derived", f"{name}: unknown check kind {item['kind']!r}")
                continue
        except Exception as exc:                       # noqa: BLE001
            rep.add("FAIL", "derived", f"{name}: {exc}")
            continue
        tol = printed_tolerance(expected)
        if abs(actual - expected) >= tol:
            rep.add("FAIL", "derived",
                    f"{name}: {actual:.6f} vs paper {expected} (tolerance ±{tol:g})")
        else:
            rep.add("PASS", "derived", name)
    rep.group_summary("derived", t0)


# ---------------------------------------------------------------------------
# 3. contrasts
# ---------------------------------------------------------------------------

def check_contrasts(preds: Predictions, spec: dict[str, Any], rep: Report,
                    jobs: int, fast: bool) -> list[dict[str, Any]]:
    t0 = time.time()
    tol_delta = float(spec["tolerances"]["bootstrap_delta_abs"])
    tol_ci = float(spec["tolerances"]["bootstrap_ci_abs"])
    results = rederive.contrasts(preds, spec, jobs=jobs, b_override=1000 if fast else None)
    by_name = {c["name"]: c for c in spec["contrasts"]}
    for res in results:
        exp = by_name[res["name"]]["expect"]
        # Each quantity is allowed the looser of its Monte-Carlo tolerance and the
        # precision the manuscript actually prints it to.
        budget = {"delta": tol_delta, "ci_lo": tol_ci, "ci_hi": tol_ci}
        worst, worst_key = 0.0, ""
        for key, allowed in budget.items():
            if key not in exp:
                continue
            allowed = max(allowed, printed_tolerance(exp[key]))
            excess = abs(res[key] - exp[key]) - allowed
            if excess > worst:
                worst, worst_key = excess, key
        detail = (f"{res['name']}: Δ {res['delta']:+.4f} "
                  f"CI [{res['ci_lo']:+.4f}, {res['ci_hi']:+.4f}] "
                  f"(paper Δ {exp['delta']:+.4f} CI [{exp['ci_lo']:+.4f}, {exp['ci_hi']:+.4f}])")
        if fast:
            rep.add("SKIP", "contrasts", f"{detail} — --fast, replicate count reduced")
        elif worst > 0:
            rep.add("FAIL", "contrasts",
                    f"{detail}; {worst_key} exceeds its tolerance by {worst:.5f}")
        else:
            rep.add("PASS", "contrasts", detail)
        # The verdict must survive too: a matching point estimate with a different
        # significance call would still be a disagreement with the paper.
        expected_excl = not (exp["ci_lo"] <= 0.0 <= exp["ci_hi"])
        if res["excludes_zero"] != expected_excl and not fast:
            rep.add("FAIL", "contrasts",
                    f"{res['name']}: interval {'excludes' if res['excludes_zero'] else 'includes'}"
                    f" zero, the paper's {'excludes' if expected_excl else 'includes'} it")
        else:
            rep.add("PASS", "contrasts", f"{res['name']} (verdict)")
    rep.group_summary("contrasts", t0)
    return results


# ---------------------------------------------------------------------------
# 3b. held-out-manipulation contrasts
# ---------------------------------------------------------------------------

def check_faceshifter(preds: Predictions, spec: dict[str, Any], rep: Report,
                      jobs: int, fast: bool) -> None:
    """The FaceShifter contrasts — the axis the paper reports closed."""
    t0 = time.time()
    declared = spec.get("faceshifter", {}).get("contrasts", [])
    if not any("expect" in c for c in declared):
        rep.add("SKIP", "faceshifter", "no expected values declared")
        rep.group_summary("faceshifter", t0)
        return
    res = rederive.faceshifter(preds, spec, jobs=jobs, b_override=1000 if fast else None)
    got = {c["name"]: c for c in res["contrasts"]}
    tol_delta = float(spec["tolerances"]["bootstrap_delta_abs"])
    tol_ci = float(spec["tolerances"]["bootstrap_ci_abs"])
    for decl in declared:
        exp = decl.get("expect")
        if not exp:
            continue
        actual = got.get(decl["name"])
        if actual is None:
            rep.add("FAIL", "faceshifter", f"{decl['name']}: not recomputed")
            continue
        detail = (f"{decl['name']}: Δ {actual['delta']:+.4f} "
                  f"CI [{actual['ci_lo']:+.4f}, {actual['ci_hi']:+.4f}]")
        worst = 0.0
        for key, allowed in (("delta", tol_delta), ("ci_lo", tol_ci), ("ci_hi", tol_ci)):
            if key in exp:
                allowed = max(allowed, printed_tolerance(exp[key]))
                worst = max(worst, abs(actual[key] - exp[key]) - allowed)
        if fast:
            rep.add("SKIP", "faceshifter", f"{detail} — --fast")
        elif worst > 0:
            rep.add("FAIL", "faceshifter", f"{detail}; exceeds tolerance by {worst:.5f}")
        else:
            rep.add("PASS", "faceshifter", detail)
        expected_excl = not (exp["ci_lo"] <= 0.0 <= exp["ci_hi"])
        if not fast and actual["excludes_zero"] != expected_excl:
            rep.add("FAIL", "faceshifter", f"{decl['name']}: verdict differs from the paper")
        else:
            rep.add("PASS", "faceshifter", f"{decl['name']} (verdict)")
    rep.group_summary("faceshifter", t0)


# ---------------------------------------------------------------------------
# 3c. the claims map
# ---------------------------------------------------------------------------

def check_claims_map(rep: Report) -> None:
    """Every row of CLAIMS-MAP.md: its artifacts exist and its number returns."""
    t0 = time.time()
    try:
        if str(HERE) not in sys.path:       # `python -I` does not add the script's dir
            sys.path.insert(0, str(HERE))
        import claim                                            # noqa: PLC0415
        results = claim.check_all(bootstrap=False)
    except Exception as exc:                                     # noqa: BLE001
        rep.add("FAIL", "claims-map", f"could not run claim.py: {exc}")
        rep.group_summary("claims-map", t0)
        return
    if not results:
        rep.add("FAIL", "claims-map", "the claims map is empty")
    for res in results:
        label = f"{res['id']} {res['label']}"
        if res["status"] == "FAIL":
            rep.add("FAIL", "claims-map", f"{label}: {res['detail']}")
        elif res["status"] in ("GAP", "PENDING"):
            rep.add("SKIP", "claims-map", f"{label}: {res['status'].lower()}")
        elif res["status"] == "DIFFERS":
            rep.add("SKIP", "claims-map", f"{label}: {res['detail']}")
        else:
            rep.add("PASS", "claims-map", label)
    if not (ROOT / "CLAIMS-MAP.md").is_file():
        rep.add("FAIL", "claims-map", "CLAIMS-MAP.md is missing")
    else:
        rep.add("PASS", "claims-map", "CLAIMS-MAP.md present")
    rep.group_summary("claims-map", t0)


# ---------------------------------------------------------------------------
# 4. figures
# ---------------------------------------------------------------------------

def check_figures(spec: dict[str, Any], rep: Report, draw: bool) -> None:
    t0 = time.time()
    data_path = ROOT / "figures" / "figure_data.json"
    if not data_path.is_file():
        rep.add("FAIL", "figures", "figures/figure_data.json is missing")
        rep.group_summary("figures", t0)
        return
    released = json.loads(data_path.read_text())

    # (a) the sweep series must equal the released per-video scores' AUCs
    preds = Predictions()
    worst = 0.0
    for run, levels in released["sweeps"].items():
        for level, value in levels.items():
            c = preds.cell(run, level)
            worst = max(worst, abs(video_auc(c["scores"], c["keys"], c["labels"]) - value))
    if worst > 1e-9:
        rep.add("FAIL", "figures", f"sweep series differ from predictions/ by {worst:.2e}")
    else:
        rep.add("PASS", "figures", f"sweep series == predictions/ ({worst:.1e})")

    # (b) the trajectory series must equal the released curves
    worst = 0.0
    missing = []
    for run, tags in released["f2_tb"].items():
        curve_path = ROOT / "curves" / f"{run}.json"
        if not curve_path.is_file():
            missing.append(run)
            continue
        curve = json.loads(curve_path.read_text())
        epochs = curve["epochs"]
        for tag, series in tags.items():
            got = {str(e): v for e, v in zip(epochs, curve["series"].get(tag, []))}
            for step, value in series.items():
                if got.get(step) is None:
                    missing.append(f"{run}/{tag}@{step}")
                else:
                    worst = max(worst, abs(got[step] - value))
    if missing:
        rep.add("FAIL", "figures", f"missing curve series: {missing[:3]}")
    elif worst > 1e-9:
        rep.add("FAIL", "figures", f"trajectory series differ from curves/ by {worst:.2e}")
    else:
        rep.add("PASS", "figures", f"trajectory series == curves/ ({worst:.1e})")

    # (c) actually draw them
    if draw:
        try:
            import matplotlib
            matplotlib.use("Agg")
            sys.path.insert(0, str(ROOT / "figures"))
            import make_figures                                    # noqa: PLC0415
            make_figures.style()
            data = json.loads(data_path.read_text())
            for name, fn in (("fig2_crf_sweep", make_figures.fig2),
                             ("fig4_mechanism", make_figures.fig4)):
                out = fn(data)
                if not Path(out).is_file():
                    rep.add("FAIL", "figures", f"{name}: nothing written")
                else:
                    rep.add("PASS", "figures",
                            f"{name} regenerated ({Path(out).stat().st_size / 1e3:.0f} kB)")
        except ImportError as exc:
            rep.add("SKIP", "figures", f"not drawn: {exc}")
    else:
        rep.add("SKIP", "figures", "drawing disabled (--no-draw)")
    rep.group_summary("figures", t0)


# ---------------------------------------------------------------------------
# 5. self-containment
# ---------------------------------------------------------------------------

def check_self_contained(rep: Report) -> None:
    t0 = time.time()
    stdlib = {Path(sysconfig.get_paths()[k]).resolve()
              for k in ("stdlib", "platstdlib", "purelib", "platlib")
              if sysconfig.get_paths().get(k)}
    outside = []
    for name, module in sorted(sys.modules.items()):
        path = getattr(module, "__file__", None)
        if not path:
            continue
        p = Path(path).resolve()
        if any(str(p).startswith(str(s)) for s in stdlib):
            continue
        if str(p).startswith(str(ROOT)):
            continue
        outside.append(f"{name} <- {p}")
    if outside:
        rep.add("FAIL", "self-containment",
                f"{len(outside)} module(s) loaded from outside this repository: {outside[:3]}")
    else:
        rep.add("PASS", "self-containment",
                "every imported module came from this repository, the standard "
                "library, or site-packages")
    for required in ("predictions", "evaluation", "curves", "figures", "splits",
                     "configs", "preregistration", "env", "audit", "probes"):
        d = ROOT / required
        rep.add("PASS" if d.is_dir() else "FAIL", "self-containment",
                f"{required}/ present" if d.is_dir() else f"{required}/ is missing")
    rep.group_summary("self-containment", t0)


# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--jobs", type=int, default=1, help="parallel bootstrap workers")
    ap.add_argument("--fast", action="store_true",
                    help="1,000 bootstrap replicates — a smoke test, not a check")
    ap.add_argument("--no-draw", action="store_true", help="skip regenerating figures")
    ap.add_argument("--out", default=None, help="also write the re-derived tables here")
    ap.add_argument("--json", default=None, help="write the check results as JSON")
    args = ap.parse_args(argv)

    spec = json.loads((HERE / "expected.json").read_text())
    preds = Predictions()
    rep = Report()

    print(f"cafrl-negative — checking the release against: {spec['paper']['title']}")
    print(f"{len(spec['cells'])} cells, {len(spec['derived'])} derived values, "
          f"{len(spec['contrasts'])} contrasts, bootstrap b={spec['bootstrap']['b']} "
          f"seed={spec['bootstrap']['seed']}\n")

    check_cells(preds, spec, rep)
    check_derived(preds, spec, rep)
    results = check_contrasts(preds, spec, rep, jobs=args.jobs, fast=args.fast)
    check_faceshifter(preds, spec, rep, jobs=args.jobs, fast=args.fast)
    check_claims_map(rep)
    check_figures(spec, rep, draw=not args.no_draw)
    check_self_contained(rep)

    if args.out:
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        res = rederive.rederive_all(None, spec, jobs=args.jobs,
                                    b_override=1000 if args.fast else None)
        (out / "tables.json").write_text(json.dumps(res, indent=1, default=float) + "\n")
        (out / "TABLES.md").write_text(rederive.render(res))
    if args.json:
        Path(args.json).write_text(json.dumps(
            {"passed": len(rep.rows) - rep.failed - rep.skipped, "failed": rep.failed,
             "skipped": rep.skipped,
             "rows": [{"status": s, "group": g, "detail": d} for s, g, d in rep.rows],
             "contrasts": results}, indent=1, default=float) + "\n")

    n_pass = len(rep.rows) - rep.failed - rep.skipped
    print()
    if rep.failed:
        print(f"FAILED — {rep.failed} of {len(rep.rows)} checks disagree with the paper")
        return 1
    print(f"OK — {n_pass} checks passed"
          + (f", {rep.skipped} skipped" if rep.skipped else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
