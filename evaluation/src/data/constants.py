"""Shared dataset constants: the set-name map between the raw and faces trees.

The raw FF++ tree and the extracted-faces tree name the real set differently
(raw ``original_sequences/youtube`` vs faces ``real``); the four protocol fake
methods are named identically in both. Any script that touches both trees must
use the single source of truth here so the two layouts never drift.

Layout reference:
  raw:    {dataset_root}/original_sequences/youtube/c{N}/videos/{id}.mp4
          {dataset_root}/manipulated_sequences/{Method}/c{N}/videos/{t_s}.mp4
  faces:  {faces_root}/c{N}/{real|Method}/{video_id}/{frame:04d}.png
  crf:    {crf_video_root}/c{N}/{youtube|Method}/videos/{name}.mp4
          (the CRF tree mirrors the *raw* set names — `youtube`, not `real`)
"""

from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
# Set-name map: raw-tree set name -> faces-tree set name.
# ---------------------------------------------------------------------------
# `youtube` is the raw real set; in the faces tree it is stored under `real`.
# The four protocol methods map identically. FaceShifter and DFD
# (`actors` / `DeepFakeDetection`) are intentionally ABSENT here: they are
# excluded from CRF variant generation (FaceShifter is held out as an
# unseen-method eval; DFD is eval-only at c23/c40). Use `RAW_TO_FACES` as the
# canonical iterable of CRF-eligible sets.

PROTOCOL_METHODS: tuple[str, ...] = (
    "Deepfakes",
    "Face2Face",
    "FaceSwap",
    "NeuralTextures",
)

# Sets re-encoded for CRF variants (reals + the 4 protocol methods).
RAW_TO_FACES: dict[str, str] = {
    "youtube": "real",
    **{m: m for m in PROTOCOL_METHODS},
}
FACES_TO_RAW: dict[str, str] = {v: k for k, v in RAW_TO_FACES.items()}

# Real set name in each tree.
RAW_REAL_SET: str = "youtube"
FACES_REAL_SET: str = "real"

# Excluded from CRF generation (documented for clarity; not iterated over).
CRF_EXCLUDED_RAW_SETS: tuple[str, ...] = ("FaceShifter", "DeepFakeDetection")
CRF_EXCLUDED_FACES_SETS: tuple[str, ...] = ("FaceShifter", "actors", "DeepFakeDetection")

# CRF-eligible raw set names, in a stable order (real first).
CRF_RAW_SETS: tuple[str, ...] = (RAW_REAL_SET, *PROTOCOL_METHODS)


# ---------------------------------------------------------------------------
# Compression levels.
# ---------------------------------------------------------------------------
# Canonical level list (ordinal bin index 0-5). c0/c23/c40 are the
# already-extracted source levels; c28/c32/c36 (+ c18 test-only) are generated.
ALL_LEVELS: tuple[str, ...] = ("c0", "c23", "c28", "c32", "c36", "c40")

# Generated CRF variants: level name -> the numeric CRF passed to libx264.
# (Level name is just "c{crf}" — kept as an explicit map so callers never parse.)
CRF_LEVELS: dict[str, int] = {
    "c18": 18,
    "c28": 28,
    "c32": 32,
    "c36": 36,
}

# Levels generated for every video vs. test-split only (c18 is the eval sweep
# point, generated only for the test split — see generate_crf_variants.py).
CRF_LEVELS_ALL_VIDEOS: tuple[str, ...] = ("c28", "c32", "c36")
CRF_LEVELS_TEST_ONLY: tuple[str, ...] = ("c18",)


def raw_set_dir(dataset_root: Path, raw_set: str, level: str) -> Path:
    """Return the raw-tree ``.../videos`` directory for a set+level.

    Reals live under ``original_sequences``, fakes under
    ``manipulated_sequences``.
    """
    root = Path(dataset_root)
    if raw_set == RAW_REAL_SET:
        return root / "original_sequences" / raw_set / level / "videos"
    return root / "manipulated_sequences" / raw_set / level / "videos"
