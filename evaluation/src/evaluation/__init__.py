"""Evaluation harness (phase1.md Step 1.8): metrics, aggregation, evaluator."""

from __future__ import annotations

from src.evaluation.aggregation import mean_pool, per_identity_max


def __getattr__(name):  # release build: import the GPU pass on demand
    """Load `Evaluator` / `eval_collate` (and torch) only when asked for."""
    if name in ("Evaluator", "eval_collate"):
        from src.evaluation import evaluator as _ev
        return getattr(_ev, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
from src.evaluation.metrics import (
    bootstrap_ci,
    crf_slope,
    crf_std,
    frame_auc,
    video_auc,
    video_scores,
)

__all__ = [
    "bootstrap_ci",
    "crf_slope",
    "crf_std",
    "frame_auc",
    "video_auc",
    "video_scores",
    "mean_pool",
    "per_identity_max",
    "Evaluator",
    "eval_collate",
]
