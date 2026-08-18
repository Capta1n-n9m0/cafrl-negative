"""Cached flat per-level face index (phase1.md Step 1.4 `index.py`).

Scanning 24k+ ``meta.json`` per run is too slow, so build a flat parquet index
once per compression level. Rows:

  * ``video_id``        — FF++ stem (``{t}_{s}`` fake / ``{id}`` real).
  * ``set``             — faces-tree set name (``real``, ``Deepfakes``, ...).
  * ``label``           — 0 real / 1 fake.
  * ``method``          — manipulation method for fakes, ``""`` for reals.
  * ``num_frames_total``— total frames of the source video (from meta.json).
  * ``frame_indices``   — list of frame indices that actually have a crop on
                          disk (differs from total for partial-detection videos;
                          the sampler/re-crop need the *available* list).

The parquet is cached under ``{faces_root}/_index/faces_index_{level}.parquet``
and rebuilt only when missing or ``force=True``.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.data.constants import FACES_REAL_SET

# Sets that are real (label 0); everything else is a manipulation (label 1).
_REAL_SETS: frozenset[str] = frozenset({FACES_REAL_SET, "actors"})

_INDEX_SUBDIR = "_index"


def index_path(faces_root: Path | str, level: str) -> Path:
    """Cache path for the level's parquet index."""
    return Path(faces_root) / _INDEX_SUBDIR / f"faces_index_{level}.parquet"


def _level_dir(faces_root: Path, level: str) -> Path:
    return Path(faces_root) / level


def _scan_video(meta_path: Path, set_name: str) -> dict | None:
    """Read one video's ``meta.json`` into an index row; ``None`` if unreadable."""
    try:
        with meta_path.open("r") as fh:
            meta = json.load(fh)
    except (OSError, json.JSONDecodeError):
        return None

    faces = meta.get("faces", [])
    frame_indices = [int(f["frame_idx"]) for f in faces]
    label = 0 if set_name in _REAL_SETS else 1
    method = "" if label == 0 else set_name
    num_total = int(meta.get("num_frames_total", 0)) or (
        max(frame_indices) + 1 if frame_indices else 0
    )
    return {
        "video_id": meta_path.parent.name,
        "set": set_name,
        "label": label,
        "method": method,
        "num_frames_total": num_total,
        "frame_indices": frame_indices,
    }


def build_index(
    faces_root: Path | str, level: str, force: bool = False
) -> pd.DataFrame:
    """Build (or load-from-cache) the flat index for ``level``.

    Scans ``{faces_root}/{level}/{set}/{video_id}/meta.json``. Writes the parquet
    cache and returns the DataFrame.
    """
    faces_root = Path(faces_root)
    out = index_path(faces_root, level)
    if out.is_file() and not force:
        return pd.read_parquet(out)

    level_dir = _level_dir(faces_root, level)
    if not level_dir.is_dir():
        raise FileNotFoundError(f"level dir not found: {level_dir}")

    rows: list[dict] = []
    for set_dir in sorted(p for p in level_dir.iterdir() if p.is_dir()):
        set_name = set_dir.name
        for video_dir in sorted(p for p in set_dir.iterdir() if p.is_dir()):
            meta_path = video_dir / "meta.json"
            if not meta_path.is_file():
                continue
            row = _scan_video(meta_path, set_name)
            if row is not None:
                rows.append(row)

    df = pd.DataFrame(rows)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out, index=False)
    return df


def load_index(
    faces_root: Path | str, level: str, force: bool = False
) -> pd.DataFrame:
    """Return the level index, building (and caching) it if missing or forced."""
    out = index_path(faces_root, level)
    if out.is_file() and not force:
        return pd.read_parquet(out)
    return build_index(faces_root, level, force=force)
