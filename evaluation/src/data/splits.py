"""Official FF++ train/val/test splits + membership rules.

The splits are JSON lists of ``[target, source]`` ID pairs (360/70/70). A FF++
fake video is named ``{target}_{source}.mp4`` (the corrected as-built fact — see
exp3 ``CLAUDE.md``); a real video is named ``{id}.mp4``.

Membership rules:
* fake ``{t}_{s}`` belongs to the split that contains the **unordered** pair
  ``{t, s}`` (both orderings ``t_s`` and ``s_t`` therefore land in the same
  split — they always exist together);
* real ``{id}`` belongs to the split that contains ``id``.

Splits are read from ``src/config/splits/{name}.json`` (copied in-repo for
self-containment). Lookups are cached per process.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

SPLIT_NAMES: tuple[str, ...] = ("train", "val", "test")

# Default location of the in-repo split JSONs (relative to the exp3 dir).
_DEFAULT_SPLITS_DIR = Path(__file__).resolve().parents[1] / "config" / "splits"


def _splits_dir(splits_dir: Path | str | None) -> Path:
    return Path(splits_dir) if splits_dir is not None else _DEFAULT_SPLITS_DIR


def load_split(
    name: str, splits_dir: Path | str | None = None
) -> list[tuple[str, str]]:
    """Load ``{name}.json`` as a list of ``(target, source)`` ID-pair tuples.

    IDs are kept as strings exactly as stored (zero-padded, e.g. ``"071"``).
    """
    if name not in SPLIT_NAMES:
        raise ValueError(f"unknown split {name!r}; valid: {SPLIT_NAMES}")
    path = _splits_dir(splits_dir) / f"{name}.json"
    with path.open("r") as fh:
        pairs = json.load(fh)
    return [(str(t), str(s)) for t, s in pairs]


@lru_cache(maxsize=8)
def _pair_index(splits_dir_key: str | None) -> dict[frozenset[str], str]:
    """Map each unordered pair ``frozenset{t, s}`` -> split name."""
    splits_dir = Path(splits_dir_key) if splits_dir_key else None
    index: dict[frozenset[str], str] = {}
    for name in SPLIT_NAMES:
        for t, s in load_split(name, splits_dir):
            index[frozenset((t, s))] = name
    return index


@lru_cache(maxsize=8)
def _real_index(splits_dir_key: str | None) -> dict[str, str]:
    """Map each real ID -> split name (an ID may appear in many pairs of one
    split; FF++ official splits keep each identity in a single split)."""
    splits_dir = Path(splits_dir_key) if splits_dir_key else None
    index: dict[str, str] = {}
    for name in SPLIT_NAMES:
        for t, s in load_split(name, splits_dir):
            index.setdefault(t, name)
            index.setdefault(s, name)
    return index


def video_split(video_id: str, splits_dir: Path | str | None = None) -> str:
    """Return the split (``train``/``val``/``test``) a video belongs to.

    Accepts a fake name ``{t}_{s}`` or a real id ``{id}``. Raises ``KeyError``
    if the id/pair is not in any split.
    """
    key = str(splits_dir) if splits_dir is not None else None
    if "_" in video_id:
        t, s = video_id.split("_", 1)
        pair = frozenset((t, s))
        split = _pair_index(key).get(pair)
        if split is None:
            raise KeyError(f"fake pair {{{t}, {s}}} not in any split")
        return split
    split = _real_index(key).get(video_id)
    if split is None:
        raise KeyError(f"real id {video_id!r} not in any split")
    return split
