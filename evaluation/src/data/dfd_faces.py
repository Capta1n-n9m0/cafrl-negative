"""``DFDFacesDataset`` — DeepFakeDetection (DFD), eval-only (phase1.md Step 1.4).

DFD is eval-only (training is FF++ c23 per protocol). The whole curated DFD set
is test. It lives inside the FF++ faces tree at
``faces/{c23,c40}/{actors, DeepFakeDetection}`` — ``actors`` are the reals
(label 0), ``DeepFakeDetection`` the fakes (label 1).

Identity metadata: fakes carry ``processing.target_id`` (the manipulated target
actor). Per-identity aggregation note (simplifies G6's per-identity rule): DFD
crops are already a single curated track of the manipulated target (diff-vote
selection at extraction), so a mean-pool over our crops *is* per-identity
aggregation — see ``src/evaluation/aggregation.py``. The ``target_id`` is exposed
here so a thin per-identity wrapper can group videos by target if ever wanted.

Images are returned raw [0,1] RGB CHW (no normalization), as for FF++.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from torch.utils.data import Dataset

from src.config.defaults import Config
from src.data.frame_select import select_frames

_REAL_SET = "actors"
_FAKE_SET = "DeepFakeDetection"


class DFDFacesDataset(Dataset):
    """Eval-only DFD dataset at a single compression level (``c23`` or ``c40``)."""

    def __init__(
        self,
        cfg: Config,
        level: str,
        frames_per_video: int | None = None,
    ) -> None:
        if level not in ("c23", "c40"):
            raise ValueError(f"DFD is eval-only at c23/c40; got {level!r}")
        self.cfg = cfg
        self.level = level
        self.faces_root = cfg.paths.resolved("faces_root")
        self.frames_per_video = frames_per_video or cfg.data.frames_per_video

        # (video_id, label, set, target_id, frame_idx)
        self._samples: list[tuple[str, int, str, str, int]] = []
        for set_name, label in ((_REAL_SET, 0), (_FAKE_SET, 1)):
            set_dir = self.faces_root / level / set_name
            if not set_dir.is_dir():
                continue
            for vid_dir in sorted(p for p in set_dir.iterdir() if p.is_dir()):
                meta_path = vid_dir / "meta.json"
                if not meta_path.is_file():
                    continue
                with meta_path.open("r") as fh:
                    meta = json.load(fh)
                target_id = str(
                    meta.get("processing", {}).get("target_id", vid_dir.name)
                )
                avail = sorted(int(f["frame_idx"]) for f in meta.get("faces", []))
                num_total = int(meta.get("num_frames_total", 0)) or (
                    (avail[-1] + 1) if avail else 0
                )
                frames = select_frames(num_total, avail, self.frames_per_video)
                for fidx in frames:
                    self._samples.append(
                        (vid_dir.name, label, set_name, target_id, fidx)
                    )

    def __len__(self) -> int:
        return len(self._samples)

    def __getitem__(self, i: int) -> dict[str, Any]:
        video_id, label, set_name, target_id, frame_idx = self._samples[i]
        png = self.faces_root / self.level / set_name / video_id / f"{frame_idx:04d}.png"
        bgr = cv2.imread(str(png))
        if bgr is None:
            raise FileNotFoundError(f"crop not found: {png}")
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        img = np.transpose(rgb, (2, 0, 1)).astype(np.float32) / 255.0
        return {
            "image": img,
            "label": label,
            "video_id": video_id,
            "frame_idx": frame_idx,
            "method": "DFD" if label == 1 else "",
            "target_id": target_id,
        }
