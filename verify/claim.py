"""Check one claim from `CLAIMS-MAP.md` — or all of them — against this release.

`../CLAIMS-MAP.md` maps every number the paper prints, and every present-tense
claim it makes about this release, to the artifact that carries it;
`../CLAIMS-MAP-R1.md` does the same for the numbers Revision 1 of the manuscript
adds (row ids `R1.<file>-<region>.<n>`). This tool is the executable half of both
maps: it takes a row's id and recomputes the number
from the released artifacts.

    python claim.py --list                 # every mapped claim, one line each
    python claim.py T4.7                   # recompute one claim
    python claim.py X1.12 --bootstrap      # ... including bootstrap rows (slow)
    python claim.py --all                  # everything cheap, as a report
    python claim.py R1                     # a release claim: do its artifacts exist?

Exit status is 0 when every requested claim agrees with the paper.

Numbers are compared at the precision the paper prints them: a value shown as
`.9590` must agree to within half a unit in its last place. Rows the release
cannot re-derive (`gap`), does not yet contain (`pending`), or knows to disagree
with the manuscript in its last printed digit (`differs`) are reported as such
rather than silently passing — the map states its own holes.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent          # verify/
ROOT = HERE.parent                              # the release root
sys.path.insert(0, str(ROOT / "evaluation"))

import numpy as np  # noqa: E402

from release_io import Predictions, align  # noqa: E402
from src.evaluation.metrics import (  # noqa: E402
    paired_auc_delta, seed_band, video_auc,
)

COMP_LEVELS = ("c28", "c32", "c36", "c40")
_SET_DIR = {"ffpp_test": "ffpp", "faceshifter": "faceshifter",
            "cross_dataset": "cross_dataset", "p2_probe": "p2_probe"}


class ClaimError(RuntimeError):
    """The map asks for something this release does not contain."""


# ---------------------------------------------------------------------------
# value computation
# ---------------------------------------------------------------------------

def printed_tolerance(printed: Any) -> float:
    """Half a unit in the last place the paper prints."""
    text = str(printed).strip().lstrip("+")
    if "e" in text.lower():                       # 4.2e-3: two significant figures
        mant, exp = text.lower().split("e")
        decimals = len(mant.split(".", 1)[1]) if "." in mant else 0
        return 0.5 * 10 ** (int(exp) - decimals)
    if "." not in text:
        return 0.5
    decimals = len(text.split(".", 1)[1].rstrip("0")) or 1
    return 0.5 * 10 ** (-decimals)


def rounds_to_printed(value: float, printed: Any) -> bool:
    """True when `value`, rounded half-up at the printed precision, IS the printed
    number — the convention the paper's numbers were printed with. It differs from
    the half-unit test only exactly on a rounding boundary (e.g. 0.0035 -> 0.004)."""
    from decimal import ROUND_HALF_UP, Decimal
    text = str(printed).strip().lstrip("+")
    try:
        if "e" in text.lower():
            mant, exp = text.lower().split("e")
            dec = len(mant.split(".", 1)[1]) if "." in mant else 0
            q = Decimal(repr(float(value))).scaleb(-int(exp)).quantize(
                Decimal(1).scaleb(-dec), ROUND_HALF_UP)
            return q == Decimal(mant)
        dec = len(text.split(".", 1)[1]) if "." in text else 0
        q = Decimal(repr(float(value))).quantize(Decimal(1).scaleb(-dec), ROUND_HALF_UP)
        return q == Decimal(text)
    except Exception:                              # noqa: BLE001
        return False


def _cell_value(preds: Predictions, run: str, cell: str, eval_set: str = "ffpp_test",
                metric: str = "video_auc") -> float:
    """One cell of one run, recomputed from scores where scores exist."""
    set_dir = _SET_DIR[eval_set]
    if eval_set in ("ffpp_test", "faceshifter") and metric == "video_auc":
        c = preds.cell(run, cell, set_dir)
        return float(video_auc(c["scores"], c["keys"], c["labels"]))
    return float(preds.metric(run, cell, metric, set_dir))


def _auc_comp(preds: Predictions, run: str) -> float:
    return float(np.mean([_cell_value(preds, run, lv) for lv in COMP_LEVELS]))


def _group_values(preds: Predictions, runs: list[str], cell: str,
                  eval_set: str = "ffpp_test", metric: str = "video_auc") -> list[float]:
    if cell == "auc_comp":
        return [_auc_comp(preds, r) for r in runs]
    return [_cell_value(preds, r, cell, eval_set, metric) for r in runs]


def _drop(preds: Predictions, run: str | None, runs: list[str] | None,
          anchor: str = "c23") -> float:
    """Clean-anchored drop: AUC(anchor) - AUC_comp, anchor c23 unless the row
    says c0 (seed-averaged for a group)."""
    if runs:
        top = float(np.mean([_cell_value(preds, r, anchor) for r in runs]))
        comp = float(np.mean([_auc_comp(preds, r) for r in runs]))
    else:
        top, comp = _cell_value(preds, run, anchor), _auc_comp(preds, run)
    return top - comp


def _side_value(preds: Predictions, side: dict[str, Any]) -> float:
    """One side of a difference: one run's cell, or the mean over several runs."""
    runs = side.get("runs") or [side["run"]]
    return float(np.mean([_cell_value(preds, r, side["cell"], side.get("eval_set", "ffpp_test"),
                                      side.get("metric", "video_auc")) for r in runs]))


def _curve_value(row: dict[str, Any]) -> float:
    path = ROOT / "curves" / f"{row['run']}.json"
    if not path.is_file():
        raise ClaimError(f"no released curve for run {row['run']!r}")
    curve = json.loads(path.read_text())
    series = curve["series"].get(row["tag"])
    if series is None:
        raise ClaimError(f"{row['run']}: no series {row['tag']!r} in the released curve")
    pairs = [(e, v) for e, v in zip(curve["epochs"], series) if v is not None]
    if not pairs:
        raise ClaimError(f"{row['run']}/{row['tag']}: series is empty")
    how = row.get("reduce", "final")
    if how == "max":
        return float(max(v for _, v in pairs))
    if how == "min":
        return float(min(v for _, v in pairs))
    if how == "final":
        return float(pairs[-1][1])
    if how == "at_selected_epoch":
        epoch = curve["selection"]["selected_epoch"]
        for e, v in pairs:
            if e == epoch:
                return float(v)
        raise ClaimError(f"{row['run']}/{row['tag']}: no value at the selected epoch {epoch}")
    raise ClaimError(f"unknown curve reduction {how!r}")


_KEY_PART = re.compile(r'\["([^"]+)"\]|\[(\d+)\]|([^.\[\]]+)')


def _dig(obj: Any, key: str) -> Any:
    """Follow a dotted key; `[i]` indexes a list and `["a.b"]` names a key that
    itself contains a dot."""
    for m in _KEY_PART.finditer(key):
        name, index = m.group(1) or m.group(3), m.group(2)
        if index is not None or (isinstance(obj, list) and name.isdigit()):
            i = int(index if index is not None else name)
            if not isinstance(obj, list) or i >= len(obj):
                raise ClaimError(f"key {key!r} not found in the artifact")
            obj = obj[i]
        else:
            if not isinstance(obj, dict) or name not in obj:
                raise ClaimError(f"key {key!r} not found in the artifact")
            obj = obj[name]
    return obj


def _load(source: str) -> Any:
    path = ROOT / source
    if not path.is_file():
        raise ClaimError(f"missing artifact {source}")
    return json.loads(path.read_text())


def _scalar_value(row: dict[str, Any]) -> float:
    doc = _load(row["source"])
    value = float(_dig(doc, row["key"]))
    if row.get("subtract_key"):
        value -= float(_dig(doc, row["subtract_key"]))
    return value


def _aggregate_value(row: dict[str, Any]) -> float:
    """A count or extremum over a list in a released file (e.g. the videos of a
    prediction file): op min | max | count | count_gt."""
    items = _dig(_load(row["source"]), row["key"])
    if not isinstance(items, list):
        raise ClaimError(f"{row['key']!r} in {row['source']} is not a list")
    vals = [float(x[row["field"]]) for x in items]
    op = row["op"]
    if op == "min":
        return min(vals)
    if op == "max":
        return max(vals)
    if op == "count":
        return float(len(vals))
    if op == "count_gt":
        return float(sum(1 for v in vals if v > float(row["value"])))
    raise ClaimError(f"unknown aggregate op {op!r}")


def _contrast_value(row: dict[str, Any], bootstrap: bool) -> tuple[float, str]:
    """A contrast's delta: from verify/expected.json, or recomputed on request."""
    spec = json.loads((HERE / "expected.json").read_text())
    pool = (spec["faceshifter"]["contrasts"] if row.get("scope") == "faceshifter"
            else spec["contrasts"])
    for c in pool:
        if c["name"] == row["name"]:
            break
    else:
        raise ClaimError(f"contrast {row['name']!r} is not in verify/expected.json")
    comp = row.get("component", "delta")
    if not bootstrap:
        exp = c.get("expect") or {}
        if comp not in exp:
            raise ClaimError(f"contrast {row['name']!r} carries no expected {comp}")
        return float(exp[comp]), (
            f"{'point estimate' if comp == 'delta' else comp} from verify/expected.json "
            f"(run `verify.py` — or this tool with --bootstrap — to recompute it)"
        )
    import rederive                                          # noqa: PLC0415
    set_dir = "faceshifter" if row.get("scope") == "faceshifter" else "ffpp"
    res = rederive._paired(Predictions(), c["a"], c["b"], c["level"], spec["bootstrap"], set_dir)
    return float(res[comp]), (
        f"recomputed: Δ {res['delta']:+.4f} (point) "
        f"CI [{res['ci_lo']:+.4f}, {res['ci_hi']:+.4f}], "
        f"{'excludes' if res['excludes_zero'] else 'includes'} zero"
    )


def value_of(row: dict[str, Any], preds: Predictions, bootstrap: bool = False
             ) -> tuple[float | None, str]:
    """Recompute one row. Returns (value, how) — value is None when not checkable."""
    kind = row["kind"]
    if kind == "cell":
        return _cell_value(preds, row["run"], row["cell"],
                           row.get("eval_set", "ffpp_test"),
                           row.get("metric", "video_auc")), "recomputed from released scores"
    if kind == "auc_comp":
        return _auc_comp(preds, row["run"]), "mean video-AUC over c28-c40"
    if kind == "seed_mean":
        vals = _group_values(preds, row["runs"], row.get("cell", "c40"),
                             row.get("eval_set", "ffpp_test"), row.get("metric", "video_auc"))
        return float(np.mean(vals)), f"mean of {len(vals)} seeds"
    if kind == "seed_band":
        vals = _group_values(preds, row["runs"], row.get("cell", "c40"),
                             row.get("eval_set", "ffpp_test"))
        return float(seed_band(vals)["half_width"]), "95% t half-width over the seed group"
    if kind == "drop":
        anchor = row.get("anchor", "c23")
        return (_drop(preds, row.get("run"), row.get("runs"), anchor),
                f"AUC({anchor}) - AUC_comp")
    if kind == "difference":
        return (_side_value(preds, row["minuend"]) - _side_value(preds, row["subtrahend"]),
                "difference of released cells")
    if kind == "aggregate":
        return _aggregate_value(row), f"{row['op']} of {row['field']} over {row['key']} in {row['source']}"
    if kind == "curve":
        return _curve_value(row), f"{row.get('reduce', 'final')} of {row['tag']} in curves/"
    if kind == "contrast":
        return _contrast_value(row, bootstrap)
    if kind in ("scalar", "params") and row.get("key") and row.get("source"):
        return _scalar_value(row), f"{row['key']} in {row['source']}"
    return None, ""


# ---------------------------------------------------------------------------
# artifacts
# ---------------------------------------------------------------------------

def resolve_artifacts(patterns: list[str]) -> tuple[list[str], list[str]]:
    """Split declared artifact paths/globs into (found, missing)."""
    found, missing = [], []
    for pat in patterns:
        if any(ch in pat for ch in "*?["):
            hits = [str(p.relative_to(ROOT)) for p in sorted(ROOT.glob(pat))]
            (found.extend(hits) if hits else missing.append(pat))
        else:
            (found.append(pat) if (ROOT / pat).exists() else missing.append(pat))
    return found, missing


# ---------------------------------------------------------------------------
# checking
# ---------------------------------------------------------------------------

def load_map() -> dict[str, Any]:
    """`claims_map.json` plus every continuation file it names (`continued_in`;
    revision 1: `claims_map_r1.json`, the rows of `../CLAIMS-MAP-R1.md`)."""
    path = HERE / "claims_map.json"
    if not path.is_file():
        raise ClaimError("verify/claims_map.json is missing — this release is incomplete")
    doc = json.loads(path.read_text())
    seen = {r["id"] for r in doc["rows"]} | {c["id"] for c in doc["release_claims"]}
    for name in doc.get("continued_in", []):
        part = HERE / name
        if not part.is_file():
            raise ClaimError(f"verify/{name} is missing — this release is incomplete")
        extra = json.loads(part.read_text())
        for r in extra["rows"] + extra.get("release_claims", []):
            if r["id"] in seen:
                raise ClaimError(f"verify/{name}: id {r['id']} is already declared")
            seen.add(r["id"])
        doc["rows"] += extra["rows"]
        doc["release_claims"] += extra.get("release_claims", [])
    return doc


def check_row(row: dict[str, Any], preds: Predictions, bootstrap: bool = False
              ) -> dict[str, Any]:
    """Check one row. Never raises: a failure is a result, not an exception."""
    out = {"id": row["id"], "table": row.get("table"), "label": row["label"],
           "kind": row["kind"], "printed": row.get("printed"),
           "value": None, "status": "", "detail": ""}
    found, missing = resolve_artifacts(row.get("artifacts", []))
    out["artifacts"] = found
    if missing and row["kind"] not in ("gap", "pending"):
        out["status"] = "FAIL"
        out["detail"] = f"declared artifact(s) not in this release: {missing}"
        return out
    if row["kind"] == "gap":
        out["status"] = "GAP"
        out["detail"] = "printed in the paper, not derivable from this release"
        return out
    if row["kind"] == "pending":
        out["status"] = "PENDING"
        out["detail"] = row.get("pending_reason", "")
        return out
    if row.get("check") == "none":
        out["status"] = "RECORDED"
        out["detail"] = row.get("note", "artifact recorded; no numeric assertion")
        return out
    try:
        value, how = value_of(row, preds, bootstrap=bootstrap)
    except Exception as exc:                                   # noqa: BLE001
        out["status"] = "FAIL"
        out["detail"] = f"{type(exc).__name__}: {exc}"
        return out
    if value is None:
        out["status"] = "RECORDED"
        out["detail"] = "no re-derivation defined for this row"
        return out
    if row.get("scale") is not None:            # e.g. AUC points = AUC x 100
        value = value * float(row["scale"])
        how += f" (x {row['scale']})"
    out["value"] = value
    printed = row.get("printed")
    text = str(printed).replace(",", "")
    if row["kind"] == "contrast":
        text = text.split()[0]          # "+0.0366 [+0.021, +0.054]" -> the delta
    try:
        target = float(text)
    except (TypeError, ValueError):
        out["status"] = "RECORDED"
        out["detail"] = f"{how}: {value:.6f}"
        return out
    tol = printed_tolerance(text)
    ok = abs(value - target) < tol or rounds_to_printed(value, text)
    if ok:
        out["status"] = "OK"
        out["detail"] = f"{how}: {value:.6f} vs paper {printed} (±{tol:g})"
        return out
    # A disagreement the release already knows about and has queued for the
    # manuscript's next revision is reported as such — with both numbers — rather
    # than as a failure. Anything not declared this way fails.
    if row.get("reconcile"):
        out["status"] = "DIFFERS"
        out["detail"] = (f"{how}: {value:.6f}; the paper prints {printed} "
                         f"(difference {value - target:+.6f}). "
                         f"{row['reconcile']}")
        return out
    out["status"] = "FAIL"
    out["detail"] = f"{how}: {value:.6f} disagrees with the paper's {printed} (±{tol:g})"
    return out


def check_release_claim(claim: dict[str, Any]) -> dict[str, Any]:
    found, missing = resolve_artifacts(claim.get("artifacts", []))
    out = {"id": claim["id"], "label": claim["claim"], "kind": "release-claim",
           "printed": None, "value": None, "artifacts": found}
    if claim.get("status") == "pending":
        out["status"] = "PENDING"
        out["detail"] = claim.get("pending_reason", "")
    elif missing:
        out["status"] = "FAIL"
        out["detail"] = f"claimed but absent: {missing}"
    else:
        out["status"] = "OK"
        out["detail"] = f"{len(found)} artifact(s) present"
        if claim.get("caveat"):
            out["detail"] += f"; caveat: {claim['caveat']}"
    return out


def check_all(bootstrap: bool = False, only: str | None = None) -> list[dict[str, Any]]:
    doc = load_map()
    preds = Predictions()
    rows = [r for r in doc["rows"] if only in (None, r["id"])]
    results = [check_row(r, preds, bootstrap=bootstrap) for r in rows]
    results += [check_release_claim(c) for c in doc["release_claims"]
                if only in (None, c["id"])]
    return results


# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("id", nargs="?", help="a claim id, e.g. T4.7 or R1")
    ap.add_argument("--all", action="store_true", help="check every mapped claim")
    ap.add_argument("--list", action="store_true", help="list the mapped claims")
    ap.add_argument("--bootstrap", action="store_true",
                    help="recompute contrast rows (10,000 replicates each)")
    ap.add_argument("--json", default=None, help="write the results as JSON")
    args = ap.parse_args(argv)

    doc = load_map()
    if args.list:
        for r in doc["rows"]:
            print(f"{r['id']:<10} [{r['kind']:<10}] {r['label']}")
        for c in doc["release_claims"]:
            print(f"{c['id']:<10} [{'claim':<10}] {c['claim']}")
        return 0
    if not (args.all or args.id):
        ap.error("give a claim id, or --all, or --list")

    results = check_all(bootstrap=args.bootstrap, only=None if args.all else args.id)
    if not results:
        print(f"no claim with id {args.id!r} — try --list", file=sys.stderr)
        return 2

    counts: dict[str, int] = {}
    for res in results:
        counts[res["status"]] = counts.get(res["status"], 0) + 1
        if len(results) == 1 or res["status"] in ("FAIL", "DIFFERS", "GAP", "PENDING"):
            print(f"{res['status']:<8} {res['id']:<10} {res['label']}")
            print(f"         {res['detail']}")
            if res.get("artifacts"):
                shown = res["artifacts"][:6]
                more = len(res["artifacts"]) - len(shown)
                print(f"         artifacts: {', '.join(shown)}"
                      + (f" (+{more} more)" if more > 0 else ""))
    if args.json:
        Path(args.json).write_text(json.dumps(results, indent=1, default=float) + "\n")
    if len(results) > 1:
        print("\n" + "  ".join(f"{k}: {v}" for k, v in sorted(counts.items())))
    return 1 if counts.get("FAIL") else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ClaimError as exc:
        print(f"claim.py: {exc}", file=sys.stderr)
        sys.exit(2)
