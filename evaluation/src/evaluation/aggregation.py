"""Frame→video / track aggregation (phase1.md Step 1.8 `aggregation.py`).

Two aggregators:

* ``mean_pool`` — the default: average per-frame fake scores into one per-video
  score. This is the protocol pooling for FF++ and Celeb-DF (implementation-plan
  §6).
* ``per_identity_max`` — DFD's "per-identity-track aggregation then max across
  tracks" (implementation-plan §6 / §2.18). **Thin by design** (phase1.md Step 1.4
  note): our DFD crops are already a *single curated track* of the manipulated
  target (diff-vote selection at extraction), so each video maps to exactly one
  identity track and **mean-pool over our crops IS per-identity aggregation**.
  With one track per identity, the "max across tracks" reduces to the per-video
  mean-pooled score. The wrapper is kept so that, if multiple tracks per identity
  are ever extracted, the max-across-tracks step is already wired.

Both operate on the flat ``(scores, ids, labels)`` triple the evaluator collects
from a DataLoader pass and return aligned per-key ``(scores, labels)`` arrays —
the same shape :func:`metrics.video_scores` produces, so they drop straight into
``video_auc`` / ``bootstrap_ci``.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from src.evaluation.metrics import video_scores

ArrayLike = Sequence[float] | np.ndarray
LabelLike = Sequence[int] | np.ndarray
IdLike = Sequence[str] | np.ndarray


def mean_pool(
    frame_scores: ArrayLike,
    video_ids: IdLike,
    frame_labels: LabelLike,
) -> tuple[np.ndarray, np.ndarray]:
    """Mean-pool frame scores per video → ``(scores, labels)``.

    Thin alias of :func:`metrics.video_scores` so callers can name the pooling
    explicitly alongside :func:`per_identity_max`.
    """
    return video_scores(frame_scores, video_ids, frame_labels)


def per_identity_max(
    frame_scores: ArrayLike,
    identity_ids: IdLike,
    frame_labels: LabelLike,
    track_ids: IdLike | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Per-identity-track aggregation then max across tracks (DFD; G6 §6).

    The general rule: mean-pool frames within each ``(identity, track)`` track,
    then take the **max** track score per identity (the one fake face must not be
    diluted). With our DFD extraction there is exactly **one track per identity**
    (the curated diff-vote track), so this reduces to a per-identity mean-pool —
    the documented equivalence (phase1.md Step 1.4 note).

    Args:
        frame_scores: per-frame fake scores, length N.
        identity_ids: per-frame identity key (e.g. ``target_id``), length N.
        frame_labels: per-frame labels, length N.
        track_ids: optional per-frame track key. ``None`` (default) ⇒ one track
            per identity (our DFD case), and the result equals the per-identity
            mean-pool. When provided, frames are pooled per ``(identity, track)``
            then maxed per identity.

    Returns:
        ``(scores, labels)`` aligned arrays, one entry per identity, ordered by
        first appearance of the identity.
    """
    s = np.asarray(frame_scores, dtype=np.float64).reshape(-1)
    ids = np.asarray(identity_ids).reshape(-1)
    y = np.asarray(frame_labels).reshape(-1).astype(np.int64)
    if not (s.shape == ids.shape == y.shape):
        raise ValueError(
            f"length mismatch: scores {s.shape}, ids {ids.shape}, labels {y.shape}"
        )

    if track_ids is None:
        # One track per identity → mean-pool per identity is the whole story.
        return video_scores(s, ids, y)

    tids = np.asarray(track_ids).reshape(-1)
    if tids.shape != s.shape:
        raise ValueError(f"track_ids {tids.shape} length mismatch with scores {s.shape}")

    # Mean-pool per (identity, track), keyed by a composite key, then max per id.
    composite = np.array(
        [f"{i}\x1f{t}" for i, t in zip(ids, tids)], dtype=object
    )
    track_scores, track_labels = video_scores(s, composite, y)
    # Recover the identity for each composite key in first-appearance order.
    seen: list[str] = []
    comp_to_id: dict[str, str] = {}
    for i, t in zip(ids, tids):
        key = f"{i}\x1f{t}"
        if key not in comp_to_id:
            comp_to_id[key] = str(i)
            seen.append(key)

    id_order: list[str] = []
    id_best: dict[str, float] = {}
    id_label: dict[str, int] = {}
    for key, sc, lab in zip(seen, track_scores, track_labels):
        ident = comp_to_id[key]
        if ident not in id_best:
            id_order.append(ident)
            id_best[ident] = float(sc)
            id_label[ident] = int(lab)
        else:
            if id_label[ident] != int(lab):
                # An identity whose tracks carry both labels has no single ground
                # truth — the caller must key on a label-consistent unit (e.g. the
                # video) rather than a shared actor id. (DFD: reals and the fakes
                # targeting them share a target_id; key on video_id instead.)
                raise ValueError(
                    f"identity {ident!r} has tracks of both labels — cannot "
                    f"max-pool to one scored unit; key on a label-consistent id"
                )
            id_best[ident] = max(id_best[ident], float(sc))
    out_scores = np.array([id_best[i] for i in id_order], dtype=np.float64)
    out_labels = np.array([id_label[i] for i in id_order], dtype=np.int64)
    return out_scores, out_labels
