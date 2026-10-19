"""``Evaluator`` — the Phase-1 evaluation harness (phase1.md Step 1.8 `evaluator.py`).

Runs the implementation-plan §6 protocol end-to-end. In Phase 1 it is exercised
with a **dummy model** (random logits) so the entire eval path is validated
before any real model exists (Gate 1).

Model interface contract
-------------------------
The evaluator treats ``model`` as a callable:

    scores_or_logits = model(images)          # images: (B, 3, 256, 256) float32 [0,1]

returning a per-frame **fake score** as a 1-D tensor of length B — either a
probability or a monotone logit (AUC is rank-based, so either is fine; the
evaluator does not apply a sigmoid). A 2-D ``(B, 1)`` output is squeezed; a
``(B, 2)`` two-logit output is reduced to the fake-class logit (column 1). The
model is moved to the evaluator's device, put in ``eval()`` mode, and called under
``torch.no_grad()``. This is the minimal contract Phase 1 needs; the full CAFRL
model (Phase 3) returns a dict — a thin adapter will expose ``logit`` here.

What it produces
----------------
* ``evaluate(model, dataset, level)`` → one cell dict: video AUC + bootstrap CI
  (+ redraw count) + frame AUC + counts.
* ``sweep(model, levels)`` → FF++ test AUC vs CRF across levels, **skipping
  missing levels with a logged warning** (the generated levels are produced
  overnight; the sweep must run on whatever exists now), plus the slope/std
  robustness statistics over the levels that ran.
* ``cross_dataset(model)`` → Celeb-DF v2 + DFD (c23) cells per the standard
  protocol (DFD via per-identity aggregation; see ``aggregation.py``).
"""

from __future__ import annotations

import logging
import time
from collections.abc import Sequence
from typing import Any, Callable

import numpy as np
import torch
from sklearn.metrics import roc_auc_score
from torch.utils.data import DataLoader, Dataset

from src.config.defaults import Config
from src.data.celebdf_faces import CelebDFFacesDataset
from src.data.dfd_faces import DFDFacesDataset
from src.data.ffpp_faces import FFppFacesDataset
from src.data.index import index_path
from src.evaluation import aggregation
from src.evaluation.metrics import (
    bootstrap_ci,
    crf_slope,
    crf_std,
    frame_auc,
    pool_by_key,
)

_LOG = logging.getLogger(__name__)

ModelLike = Callable[[torch.Tensor], torch.Tensor]


def eval_collate(records: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """Stack eval-dataset records (numpy ``image``) into a batch.

    Mirrors the train-mode ``collate`` but without pairing — eval samples are
    independent frames. Carries ``video_id`` / ``label`` / ``method`` /
    ``target_id`` (DFD) through as Python lists so the evaluator can group + pool
    afterwards. ``method`` is needed because FF++ fake stems are **shared across
    the 4 manipulation methods** (``000_003`` exists as Deepfakes / Face2Face /
    FaceSwap / NeuralTextures) — pooling on the bare stem would merge 4 distinct
    videos into 1, collapsing the 700-video test set to 280. The pooling unit is
    ``(video_id, method)`` (see ``_video_keys``).
    """
    images = torch.from_numpy(
        np.ascontiguousarray(np.stack([r["image"] for r in records]))
    ).float()
    labels = np.array([int(r["label"]) for r in records], dtype=np.int64)
    video_ids = [str(r["video_id"]) for r in records]
    methods = [str(r.get("method", "")) for r in records]
    target_ids = [str(r.get("target_id", r["video_id"])) for r in records]
    return {
        "image": images,
        "label": labels,
        "video_id": video_ids,
        "method": methods,
        "target_id": target_ids,
    }


def _video_keys(video_ids: Sequence[str], methods: Sequence[str]) -> list[str]:
    """Compose the per-video pooling key ``"{video_id}\x1f{method}"``.

    For FF++ this separates the 4 methods that share a fake stem; for reals
    (method ``""``) and for Celeb-DF / DFD (one method tag, already-unique stems)
    it is equivalent to keying on ``video_id`` alone.
    """
    return [f"{v}\x1f{m}" for v, m in zip(video_ids, methods)]


class Evaluator:
    """Batched, device-aware evaluation over the standard protocol."""

    def __init__(
        self,
        cfg: Config,
        device: torch.device | str | None = None,
        num_workers: int | None = None,
        batch_size: int | None = None,
    ) -> None:
        self.cfg = cfg
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = torch.device(device)
        # Keep DataLoader load polite (a concurrent encode job runs); cap at 8.
        nw = num_workers if num_workers is not None else cfg.data.num_workers
        self.num_workers = min(int(nw), 8)
        self.batch_size = int(batch_size or cfg.data.batch_size)
        self.bootstrap_b = cfg.eval.bootstrap_b
        self.ci = cfg.eval.ci

    # -- inference ---------------------------------------------------------

    @staticmethod
    def _to_scores(out: torch.Tensor) -> np.ndarray:
        """Normalize a model output to a 1-D per-frame fake-score numpy array."""
        if out.ndim == 1:
            scores = out
        elif out.ndim == 2 and out.shape[1] == 1:
            scores = out[:, 0]
        elif out.ndim == 2 and out.shape[1] == 2:
            scores = out[:, 1]  # fake-class logit
        else:
            raise ValueError(
                f"model output must be (B,), (B,1) or (B,2); got {tuple(out.shape)}"
            )
        return scores.detach().to(torch.float32).cpu().numpy()

    def _infer(
        self, model: ModelLike, loader: DataLoader
    ) -> tuple[np.ndarray, np.ndarray, list[str], list[str], list[str]]:
        """Run the model, collecting (scores, labels, video_keys, vids, targets).

        ``video_keys`` is the per-frame ``(video_id, method)`` pooling key; raw
        ``vids`` and ``targets`` are also returned for analysis/aggregation.
        """
        if isinstance(model, torch.nn.Module):
            model.to(self.device)
            model.eval()
        all_scores: list[np.ndarray] = []
        all_labels: list[np.ndarray] = []
        all_keys: list[str] = []
        all_vids: list[str] = []
        all_targets: list[str] = []
        with torch.no_grad():
            for batch in loader:
                images = batch["image"].to(self.device, non_blocking=True)
                out = model(images)
                all_scores.append(self._to_scores(out))
                all_labels.append(batch["label"])
                all_keys.extend(_video_keys(batch["video_id"], batch["method"]))
                all_vids.extend(batch["video_id"])
                all_targets.extend(batch["target_id"])
        scores = np.concatenate(all_scores) if all_scores else np.empty(0)
        labels = np.concatenate(all_labels) if all_labels else np.empty(0, dtype=np.int64)
        return scores, labels, all_keys, all_vids, all_targets

    def _loader(self, dataset: Dataset) -> DataLoader:
        return DataLoader(
            dataset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
            collate_fn=eval_collate,
            pin_memory=(self.device.type == "cuda"),
            persistent_workers=False,
        )

    # -- one cell ----------------------------------------------------------

    def _cell(
        self,
        scores: np.ndarray,
        labels: np.ndarray,
        video_keys: Sequence[str],
        *,
        target_ids: Sequence[str] | None = None,
        aggregate: str = "mean_pool",
        name: str = "",
        return_preds: bool = False,
    ) -> dict[str, Any]:
        """Compute frame AUC + video AUC + bootstrap CI for one collected pass.

        ``video_keys`` is the per-frame ``(video_id, method)`` pooling unit (one
        scored video each) — never the bare stem (FF++ fake stems repeat across
        the 4 methods).
        """
        n_frames = int(scores.shape[0])
        if n_frames == 0:
            return {"name": name, "status": "empty", "n_frames": 0}

        if aggregate == "per_identity_max":
            # DFD: each curated video IS one identity track (diff-vote selection),
            # so the scored unit is the *video* (the composite key). A real actor
            # video and the fakes that target it legitimately share a
            # ``target_id`` but carry opposite labels — so the bare ``target_id``
            # is NOT a valid pooling key (it would merge a real and its fakes into
            # one ambiguous unit). With one track per video, "per-identity-track
            # aggregation then max across tracks" reduces to a per-video mean-pool
            # — the documented equivalence (phase1.md Step 1.4 / plan §2.18).
            vid_scores, vid_labels = aggregation.per_identity_max(
                scores, video_keys, labels
            )
        else:
            vid_scores, vid_labels = aggregation.mean_pool(scores, video_keys, labels)

        n_videos = int(vid_scores.shape[0])
        both_classes = np.unique(vid_labels).size >= 2
        result: dict[str, Any] = {
            "name": name,
            "status": "ok" if both_classes else "single_class",
            "n_frames": n_frames,
            "n_videos": n_videos,
            "n_pos": int(np.sum(vid_labels == 1)),
            "n_neg": int(np.sum(vid_labels == 0)),
            "aggregate": aggregate,
        }
        if not both_classes:
            _LOG.warning("cell %s has a single class (n_videos=%d) — AUC skipped",
                         name, n_videos)
            return result

        # Video AUC is over the (already aggregated) per-video/-identity scores.
        result["video_auc"] = float(roc_auc_score(vid_labels, vid_scores))
        # frame AUC is well-defined whenever both classes appear among frames
        if np.unique(labels).size >= 2:
            result["frame_auc"] = float(frame_auc(scores, labels))
        # Frame-level BCE-with-logits — the validation LOSS for best-epoch-by-loss
        # selection (`scores` are raw logits, no sigmoid). Stable form:
        # max(s,0) − s·y + log1p(exp(−|s|)). Independent of pooling/aggregation.
        _s = scores.astype(np.float64)
        _y = labels.astype(np.float64)
        result["frame_bce"] = float(
            np.mean(np.maximum(_s, 0.0) - _s * _y + np.log1p(np.exp(-np.abs(_s))))
        )
        lo, hi, redraws = bootstrap_ci(
            vid_scores, vid_labels, b=self.bootstrap_b, ci=self.ci,
            seed=0, return_redraws=True,
        )
        result["ci_lo"] = lo
        result["ci_hi"] = hi
        result["ci_redraws"] = redraws

        # Per-video KEYED predictions (Phase-5 paired-Δ aggregator input). Same
        # inference pass — no extra forward. The aggregator aligns arms/seeds/levels
        # by these keys (NOT positional), so a run's report.json carries the exact
        # per-video pooled scores the win-rule resamples. pool_by_key reproduces the
        # mean-pool / one-track per_identity_max scored unit used above (keyed).
        if return_preds:
            pkeys, pscores, plabels = pool_by_key(scores, video_keys, labels)
            result["video_keys"] = [str(k) for k in pkeys]
            result["video_scores"] = [float(x) for x in pscores]
            result["video_labels"] = [int(x) for x in plabels]
        return result

    # -- public API --------------------------------------------------------

    def evaluate(
        self, model: ModelLike, dataset: Dataset, level: str,
        aggregate: str = "mean_pool", name: str | None = None,
        *, return_preds: bool = False,
    ) -> dict[str, Any]:
        """Evaluate ``model`` on ``dataset`` (one level) → a cell dict with timing.

        ``return_preds=True`` additionally attaches the per-video keyed predictions
        (``video_keys`` / ``video_scores`` / ``video_labels``) to the cell — the
        Phase-5 paired-Δ bootstrap input, dumped by ``eval_battery.py`` into a run's
        ``report.json`` (no extra inference pass).
        """
        cell_name = name or f"{type(dataset).__name__}@{level}"
        t0 = time.time()
        loader = self._loader(dataset)
        scores, labels, keys, _vids, targets = self._infer(model, loader)
        cell = self._cell(
            scores, labels, keys, target_ids=targets,
            aggregate=aggregate, name=cell_name, return_preds=return_preds,
        )
        cell["level"] = level
        cell["wall_s"] = round(time.time() - t0, 2)
        return cell

    def _ffpp_level_available(self, level: str) -> bool:
        """Whether FF++ crops/index exist for ``level`` right now."""
        faces_root = self.cfg.paths.resolved("faces_root")
        if (faces_root / level).is_dir():
            return True
        return index_path(faces_root, level).is_file()

    def sweep(
        self, model: ModelLike, levels: Sequence[str], split: str = "test",
        *, return_preds: bool = False,
    ) -> dict[str, Any]:
        """FF++ ``split`` video-AUC vs CRF across ``levels`` (skip missing).

        Missing levels (crops not generated yet) are logged and skipped. The
        robustness statistics (``crf_slope``/``crf_std``) are computed over the
        levels that actually produced an AUC. ``return_preds=True`` threads through
        to attach per-video keyed predictions to each cell (eval_battery / paired-Δ).
        """
        cells: dict[str, dict[str, Any]] = {}
        aucs: dict[str, float] = {}
        for level in levels:
            if not self._ffpp_level_available(level):
                _LOG.warning("sweep: FF++ level %s not on disk — skipping", level)
                cells[level] = {"name": f"FFpp@{level}", "status": "missing",
                                "level": level}
                continue
            ds = FFppFacesDataset(self.cfg, split=split, levels=(level,),
                                  training=False)
            cell = self.evaluate(model, ds, level, name=f"FFpp-{split}@{level}",
                                 return_preds=return_preds)
            cells[level] = cell
            if cell.get("status") == "ok" and "video_auc" in cell:
                aucs[level] = cell["video_auc"]

        out: dict[str, Any] = {"cells": cells, "aucs": aucs, "split": split}
        if len(aucs) >= 2:
            out["crf_slope"] = crf_slope(aucs)
            out["crf_std"] = crf_std(aucs)
        else:
            _LOG.warning("sweep: <2 levels produced an AUC — slope/std skipped")
        return out

    def cross_dataset(
        self, model: ModelLike, *, return_preds: bool = False,
    ) -> dict[str, Any]:
        """Celeb-DF v2 + DFD (c23 **and** c40) cells per the standard protocol.

        ``return_preds=True`` (Phase 6, lesson L6) attaches the per-video keyed
        predictions to each cell exactly as in ``sweep``. It is default-off and only
        adds the ``video_keys``/``video_scores``/``video_labels`` fields; every scalar
        comes from the same single inference pass, so it is identical either way.

        Phase-5 Step 5.3 added the **DFD-c40** cell (crops on disk,
        `phase1-asbuilt §C3`) — both DFD levels are part of the pre-registered
        CRUX-3 consistency check (the winning A1 mechanism must not reverse the sign
        of its drop advantage on DFD-c40). WildDeepfake / DFDC-partial land as their
        acquisition completes (the slower parallel workstream); they are descriptive
        cross-dataset context and never block the A1 decision (CRUX-2).
        """
        out: dict[str, dict[str, Any]] = {}

        # Celeb-DF v2 (mean-pool).
        try:
            cdf = CelebDFFacesDataset(self.cfg)
            if len(cdf) > 0:
                out["celebdf_v2"] = self.evaluate(model, cdf, "test",
                                                  name="CelebDF-v2",
                                                  return_preds=return_preds)
            else:
                _LOG.warning("cross_dataset: Celeb-DF has 0 samples — skipping")
                out["celebdf_v2"] = {"name": "CelebDF-v2", "status": "empty"}
        except (FileNotFoundError, OSError) as exc:
            _LOG.warning("cross_dataset: Celeb-DF unavailable (%s)", exc)
            out["celebdf_v2"] = {"name": "CelebDF-v2", "status": "unavailable"}

        # DFD c23 + c40 (per-identity aggregation; thin → mean-pool over curated
        # track). The c40-cell pattern mirrors eval_dummy.py:84.
        for lvl in ("c23", "c40"):
            key = f"dfd_{lvl}"
            try:
                dfd = DFDFacesDataset(self.cfg, level=lvl)
                if len(dfd) > 0:
                    out[key] = self.evaluate(
                        model, dfd, lvl, aggregate="per_identity_max",
                        name=f"DFD@{lvl}", return_preds=return_preds,
                    )
                else:
                    _LOG.warning("cross_dataset: DFD %s has 0 samples — skipping", lvl)
                    out[key] = {"name": f"DFD@{lvl}", "status": "empty"}
            except (FileNotFoundError, OSError) as exc:
                _LOG.warning("cross_dataset: DFD %s unavailable (%s)", lvl, exc)
                out[key] = {"name": f"DFD@{lvl}", "status": "unavailable"}

        return out
