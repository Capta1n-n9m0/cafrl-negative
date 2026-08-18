"""Read this repository's prediction files into the evaluation harness.

`src/evaluation/` is the campaign's own code, copied here unmodified: it consumes
the run-report structure the training/evaluation stack wrote. This module is the
one piece of glue that is specific to the release — it turns the published
`predictions/*.json` files back into that structure, so every statistic in the
paper is recomputed by the same functions that computed it originally rather than
by a re-implementation.

Nothing here does statistics. It loads, checks shape, and hands over.

    from release_io import Predictions
    p = Predictions()                            # defaults to ../predictions
    cell = p.cell("b7_effnet_b0_mq_fliponly", "c40")
    pooled = p.pool(["f1_none_fair_s42", "f1_none_fair_s1", "f1_none_fair_s2"], "c40")

Score semantics: raw fake-class logits, mean-pooled over each video's 32 sampled
frames. AUC is rank-based, so the scale does not matter.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np

# The pooling key that identifies a video within an evaluation set: one source
# video appearing under several manipulations stays distinct. The separator is
# the ASCII unit separator, as in the original evaluation.
KEY_SEP = "\x1f"

HERE = Path(__file__).resolve().parent
DEFAULT_PREDICTIONS = HERE.parent / "predictions"

FFPP_LEVELS = ("c0", "c18", "c23", "c28", "c32", "c36", "c40")
COMP_LEVELS = ("c28", "c32", "c36", "c40")


class ReleaseDataError(RuntimeError):
    """A released artifact is missing or does not have the expected shape."""


def _key(video_id: str, method: str) -> str:
    return f"{video_id}{KEY_SEP}{method}"


class Predictions:
    """Loader over ``predictions/`` with the harness's report shape as its output."""

    def __init__(self, root: str | Path | None = None) -> None:
        self.root = Path(root) if root is not None else DEFAULT_PREDICTIONS
        if not self.root.is_dir():
            raise ReleaseDataError(f"predictions directory not found: {self.root}")
        self._cache: dict[tuple[str, str], dict[str, Any]] = {}

    # -- raw files ---------------------------------------------------------

    def file(self, run: str, eval_set: str = "ffpp") -> dict[str, Any]:
        hit = self._cache.get((run, eval_set))
        if hit is None:
            path = self.root / eval_set / f"{run}.json"
            if not path.is_file():
                raise ReleaseDataError(
                    f"no {eval_set} predictions for run {run!r} (looked for {path}). "
                    f"See predictions/GAPS.md for the cells that have no per-video scores."
                )
            hit = json.loads(path.read_text())
            self._cache[(run, eval_set)] = hit
        return hit

    def runs(self, eval_set: str = "ffpp") -> list[str]:
        return sorted(p.stem for p in (self.root / eval_set).glob("*.json"))

    # -- one cell ----------------------------------------------------------

    def cell(self, run: str, level: str, eval_set: str = "ffpp") -> dict[str, Any]:
        """One (run, level) cell: ``keys``, ``scores``, ``labels``, ``video_auc``.

        Arrays come back in the file's original evaluation order — the order that
        pairs position-by-position across runs.
        """
        payload = self.file(run, eval_set)
        cells = payload.get("cells", {})
        if level not in cells:
            raise ReleaseDataError(
                f"{run}/{eval_set}: no cell {level!r} (have: {', '.join(sorted(cells))})"
            )
        c = cells[level]
        for field in ("video_id", "method", "label", "score"):
            if field not in c:
                raise ReleaseDataError(
                    f"{run}/{eval_set}/{level}: no per-video scores in this cell "
                    f"(missing {field!r}); see predictions/GAPS.md"
                )
        n = len(c["video_id"])
        if not all(len(c[f]) == n for f in ("method", "label", "score")):
            raise ReleaseDataError(f"{run}/{eval_set}/{level}: parallel arrays disagree in length")
        return {
            "run": run,
            "level": level,
            "keys": [_key(v, m) for v, m in zip(c["video_id"], c["method"])],
            "scores": np.asarray(c["score"], dtype=np.float64),
            "labels": np.asarray(c["label"], dtype=np.int64),
            "video_auc": float(c["video_auc"]),
            "n_videos": int(c.get("n_videos", n)),
            "keys_sha256": c.get("keys_sha256"),
        }

    def metric(self, run: str, cell: str, key: str = "video_auc",
               eval_set: str = "cross_dataset") -> float:
        """A stored scalar from a cell that has no per-video scores (Table 7, P2).

        Cross-dataset cells are dictionaries of statistics; the P2 probe's report
        predates that convention and stores its AUC as a bare number, so both
        shapes are accepted.
        """
        payload = self.file(run, eval_set)
        cells = payload.get("cells", {})
        if cell not in cells:
            raise ReleaseDataError(f"{run}/{eval_set}: no cell {cell!r}")
        body = cells[cell]
        if not isinstance(body, dict):
            return float(body)
        if key not in body:
            raise ReleaseDataError(f"{run}/{eval_set}/{cell}: no {key!r}")
        return float(body[key])

    # -- harness-shaped views ----------------------------------------------

    def as_report(self, run: str, levels: Sequence[str] = FFPP_LEVELS,
                  eval_set: str = "ffpp") -> dict[str, Any]:
        """The run-report shape ``src/evaluation/aggregate_runs.py`` expects.

        Only the fields that module reads are populated; the point is to feed the
        released scores to the frozen pooling and adjudication code unchanged.
        """
        payload = self.file(run, eval_set)
        sweep: dict[str, Any] = {}
        for level in levels:
            if level not in payload.get("cells", {}):
                continue
            c = self.cell(run, level, eval_set)
            sweep[level] = {
                "status": "ok",
                "level": level,
                "video_auc": c["video_auc"],
                "video_keys": c["keys"],
                "video_scores": c["scores"].tolist(),
                "video_labels": c["labels"].tolist(),
                "n_videos": c["n_videos"],
            }
        report: dict[str, Any] = {"run": run, "seed": payload.get("seed"), "sweep": sweep}
        if "c23" in sweep:
            report["AUC_c23"] = sweep["c23"]["video_auc"]
        comp = [lv for lv in COMP_LEVELS if lv in sweep]
        if comp:
            report["AUC_comp"] = float(np.mean([sweep[lv]["video_auc"] for lv in comp]))
            if "AUC_c23" in report:
                report["drop"] = report["AUC_c23"] - sweep["c40"]["video_auc"] if "c40" in sweep else None
        return report

    def pool(self, runs: Iterable[str], level: str, eval_set: str = "ffpp") -> dict[str, Any]:
        """Seed-pool an arm's runs at one level, with the campaign's own function.

        Delegates to ``src.evaluation.aggregate_runs.seed_pool_level``: align the
        seeds on their common video keys, average each video's score across seeds,
        and return the arrays in **sorted-key order** — the order the campaign's
        paired bootstrap consumed, and therefore the order that reproduces its
        intervals replicate for replicate.
        """
        from src.evaluation.aggregate_runs import seed_pool_level

        runs = list(runs)
        reports = [self.as_report(r, (level,), eval_set) for r in runs]
        pooled = seed_pool_level(reports, level)
        return {
            "runs": runs,
            "level": level,
            "keys": pooled["keys"],
            "scores": np.asarray(pooled["scores"], dtype=np.float64),
            "labels": np.asarray(pooled["labels"], dtype=np.int64),
        }


def align(a: dict[str, Any], b: dict[str, Any]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Two pooled/loaded cells → (scores_a, scores_b, labels) on their common keys.

    Raises if the two sides disagree about a video's label, which would mean the
    pairing is not what it claims to be.
    """
    idx_b = {k: i for i, k in enumerate(b["keys"])}
    common = [k for k in a["keys"] if k in idx_b]
    if not common:
        raise ReleaseDataError("no common videos between the two cells")
    ia = [i for i, k in enumerate(a["keys"]) if k in idx_b]
    ib = [idx_b[k] for k in common]
    ya, yb = a["labels"][ia], b["labels"][ib]
    if not np.array_equal(ya, yb):
        raise ReleaseDataError("labels differ between the two arms on their common videos")
    return a["scores"][ia], b["scores"][ib], ya
