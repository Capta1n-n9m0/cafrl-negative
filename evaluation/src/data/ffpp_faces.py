"""``FFppFacesDataset`` — FF++ face crops, train + eval (phase1.md Step 1.4).

Train mode is driven by the Step-1.5 sampler through ``fetch(spec)``; eval mode
iterates (video × 32 fixed frames × one level). Images are returned **raw [0,1]
RGB CHW** — no normalization. All stream-specific prep (BT.601 Y for DCT/phase,
ImageNet norm for the spatial branch) lives inside the model so the three streams
always see one consistent input.

Frame availability is asymmetric by design: c0/c23/c40 carry all frames (eval
re-derives the 32 via the linspace-over-available rule); the generated levels
(c18/c28/c32/c36) store only 32 frames whose indices the index records.

JPEG arms (Phase 6 E3): with ``jpeg_level_to_qf`` set, a train-mode fetch at level
``L != c0`` loads the **c0** crop at the planned frame and re-encodes it as JPEG at
``jpeg_level_to_qf[L]`` before any augmentation, flip and ``to_tensor``
(``src/data/jpeg_levels.py``). Without it (the default, and always in eval mode)
the path is unchanged.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import pandas as pd
from torch.utils.data import Dataset

from src.config.defaults import Config
from src.data.frame_select import select_frames
from src.data.index import load_index
from src.data.jpeg_levels import jpeg_roundtrip
from src.data.sample_spec import SampleSpec
from src.data.splits import video_split
from src.data.transforms import maybe_flip, to_tensor

# Levels with all frames on disk (eval re-derives the 32 via linspace-over-
# available); everything else stores only the 32 selected frames.
_ALL_FRAME_LEVELS: frozenset[str] = frozenset({"c0", "c23", "c40"})


class FFppFacesDataset(Dataset):
    """FF++ face-crop dataset over one or more compression levels.

    Args:
        cfg: the resolved ``Config`` (uses ``paths.faces_root`` and
            ``data.bin_levels``).
        split: ``"train"`` / ``"val"`` / ``"test"``.
        levels: compression levels to include.
        training: train mode (sampler-driven ``fetch``) vs eval mode (fixed
            iteration over video × 32 frames × level).
        frame_augmentor: optional callable applied to the loaded crop as a
            ``H×W×3`` numpy ``uint8`` RGB frame **before** ``to_tensor`` (and
            before any flip), and **only** when ``training=True``. Used by the
            Phase-5 baselines (``src/baselines/augment.py``); CAFRL always leaves
            this ``None`` so its data path is bit-identical to before this param
            existed. The eval/val path (``training=False``) NEVER augments.
        jpeg_level_to_qf: optional ``level -> QF`` map (c0 -> None) for the
            Phase-6 JPEG arms; train mode only (refused with ``training=False``
            so a val/test set can never be JPEG-coded by accident). ``None``
            (default) leaves the load path bit-identical to before.
    """

    def __init__(
        self,
        cfg: Config,
        split: str,
        levels: Sequence[str],
        training: bool,
        frame_augmentor: Callable[[np.ndarray], np.ndarray] | None = None,
        jpeg_level_to_qf: Mapping[str, int | None] | None = None,
    ) -> None:
        self.cfg = cfg
        self.split = split
        self.levels = tuple(levels)
        self.training = training
        self.frame_augmentor = frame_augmentor
        if jpeg_level_to_qf is not None and not training:
            raise ValueError("jpeg_level_to_qf is a train-mode option only")
        self.jpeg_level_to_qf: dict[str, int | None] | None = (
            dict(jpeg_level_to_qf) if jpeg_level_to_qf is not None else None
        )
        if self.jpeg_level_to_qf is not None:
            missing = [lvl for lvl in levels
                       if lvl != "c0" and self.jpeg_level_to_qf.get(lvl) is None]
            if missing:
                raise ValueError(f"JPEG map has no QF for levels {missing}")
        self.faces_root = cfg.paths.resolved("faces_root")
        self.bin_levels = tuple(cfg.data.bin_levels)
        self.frames_per_video = cfg.data.frames_per_video
        self.methods = tuple(cfg.data.methods)

        # Per-level flat index (built/cached on first use).
        self._index: dict[str, pd.DataFrame] = {
            lvl: load_index(self.faces_root, lvl) for lvl in self.levels
        }
        # Restrict to this split + (for fakes) the protocol methods + reals.
        self._index = {lvl: self._filter(df) for lvl, df in self._index.items()}

        # Eval-mode flat sample list: (video_id, set, label, method, level, frame).
        self._eval_samples: list[tuple[str, str, int, str, str, int]] = []
        if not self.training:
            self._build_eval_samples()

    # -- index filtering ---------------------------------------------------

    def _keep_row(self, row: pd.Series) -> bool:
        if int(row["label"]) == 0:  # reals: keep if the id is in this split
            try:
                return video_split(row["video_id"]) == self.split
            except KeyError:
                return False
        # fakes: keep only protocol methods whose pair is in this split
        if row["method"] not in self.methods:
            return False
        try:
            return video_split(row["video_id"]) == self.split
        except KeyError:
            return False

    def _filter(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        mask = df.apply(self._keep_row, axis=1)
        return df[mask].reset_index(drop=True)

    # -- eval-mode sample enumeration --------------------------------------

    def _frames_for(self, row: pd.Series, level: str) -> list[int]:
        avail = [int(x) for x in row["frame_indices"]]
        if level in _ALL_FRAME_LEVELS:
            return select_frames(int(row["num_frames_total"]), avail,
                                 self.frames_per_video)
        # generated level: indices already exactly the stored 32 (or allow-list)
        return sorted(avail)

    def _build_eval_samples(self) -> None:
        for level in self.levels:
            df = self._index[level]
            for _, row in df.iterrows():
                frames = self._frames_for(row, level)
                for fidx in frames:
                    self._eval_samples.append((
                        row["video_id"], row["set"], int(row["label"]),
                        row["method"], level, fidx,
                    ))

    # -- crop loading ------------------------------------------------------

    def _bin_idx(self, level: str) -> int:
        # c18 (the eval-only sweep point) is not one of the 6 training bins;
        # bin_idx is a training-conditioning concept the eval path never reads,
        # so out-of-bin levels get a -1 sentinel instead of an error.
        try:
            return self.bin_levels.index(level)
        except ValueError:
            return -1

    def jpeg_qf(self, level: str) -> int | None:
        """QF applied to a train crop at ``level`` (None: no JPEG, load as is)."""
        if (not self.training or self.jpeg_level_to_qf is None
                or level == "c0"):
            return None
        return self.jpeg_level_to_qf[level]

    def source_level(self, level: str) -> str:
        """Level dir the crop for ``level`` is read from (c0 for JPEG views)."""
        return "c0" if self.jpeg_qf(level) is not None else level

    def _load_image(self, set_name: str, video_id: str, level: str,
                    frame_idx: int) -> np.ndarray:
        qf = self.jpeg_qf(level)
        src_level = "c0" if qf is not None else level
        png = self.faces_root / src_level / set_name / video_id / f"{frame_idx:04d}.png"
        bgr = cv2.imread(str(png))
        if bgr is None:
            raise FileNotFoundError(f"crop not found: {png}")
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)  # HWC uint8
        # JPEG arms: the c0 crop is re-encoded at the level's calibrated QF on the
        # stored uint8 RGB crop, before augmentation, flip and to_tensor (S0 M6).
        if qf is not None:
            rgb = jpeg_roundtrip(rgb, qf)
        # Baseline-only augmentation: applied on the uint8 numpy RGB crop, BEFORE
        # to_tensor (and before maybe_flip). Train-mode only. When the augmentor
        # is None (CAFRL's default, and the eval/val path), this branch is skipped
        # and the path below is bit-identical to before this hook existed.
        if self.training and self.frame_augmentor is not None:
            rgb = self.frame_augmentor(rgb)  # HWC uint8 RGB → HWC uint8 RGB
        return to_tensor(rgb)  # CHW float32 [0,1] (Step 1.6 transform)

    def _make_record(self, *, video_id: str, set_name: str, label: int,
                     method: str, level: str, frame_idx: int,
                     flip: bool) -> dict[str, Any]:
        img = self._load_image(set_name, video_id, level, frame_idx)
        img = maybe_flip(img, flip)  # CHW; sampler decided the flag (Step 1.6)
        return {
            "image": img,
            "label": label,
            "bin_idx": self._bin_idx(level),
            "video_id": video_id,
            "frame_idx": frame_idx,
            "method": method,
        }

    # -- train-mode fetch --------------------------------------------------

    def fetch(self, spec: SampleSpec) -> dict[str, Any]:
        """Load one crop named by a ``SampleSpec`` (train mode)."""
        label = 0 if spec.set in ("real", "actors") else 1
        method = "" if label == 0 else spec.set
        rec = self._make_record(
            video_id=spec.video_id, set_name=spec.set, label=label,
            method=method, level=spec.level, frame_idx=spec.frame_idx,
            flip=spec.flip,
        )
        # Provenance for the per-epoch fetched-level / (level, QF) counters. The
        # shared ``collate`` ignores these keys, so the CAFRL batch is unchanged.
        rec["level"] = spec.level
        rec["src_level"] = self.source_level(spec.level)
        rec["jpeg_qf"] = self.jpeg_qf(spec.level)
        return rec

    # -- Dataset protocol (eval mode) --------------------------------------

    def __len__(self) -> int:
        if self.training:
            raise RuntimeError("len() is for eval mode; train mode is sampler-driven")
        return len(self._eval_samples)

    def __getitem__(self, i: int) -> dict[str, Any]:
        if self.training:
            raise RuntimeError("__getitem__ is for eval mode; use fetch(spec)")
        video_id, set_name, label, method, level, frame_idx = self._eval_samples[i]
        return self._make_record(
            video_id=video_id, set_name=set_name, label=label, method=method,
            level=level, frame_idx=frame_idx, flip=False,
        )

    # -- helpers for the sampler (train mode) ------------------------------

    def video_table(self, level: str) -> pd.DataFrame:
        """The filtered per-video index for ``level`` (sampler input)."""
        return self._index[level]
