"""``CelebDFFacesDataset`` — Celeb-DF v2, eval-only (phase1.md Step 1.4).

Restricted to the official ``List_of_testing_videos.txt`` (518 videos; the file
has no trailing newline so ``wc -l`` shows 517).

**Label-inversion trap:** the official list uses ``1`` = real / ``0`` = fake —
the opposite of our ``fake=1`` convention. The dataset emits ``label=1`` for
``faces/fake`` videos and ``label=0`` for ``faces/real`` videos. Each test-list
line ``{official}\t{Category}/{stem}.mp4`` is mapped to our faces tree by stem:
``Celeb-synthesis`` → ``fake/`` (our label 1), ``Celeb-real`` / ``YouTube-real``
→ ``real/`` (our label 0). Real and fake stems do not collide.

Images are returned raw [0,1] RGB CHW (no normalization), as for FF++.
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from torch.utils.data import Dataset

from src.config.defaults import Config, resolve_path
from src.data.frame_select import select_frames

# Official test list lives next to the raw videos.
_DEFAULT_TEST_LIST = Path(
    "~/sdc/datasets/celeb-df-v2/List_of_testing_videos.txt"
)

# Category prefix (in the official list) -> our faces subdir.
_FAKE_CATEGORIES = frozenset({"Celeb-synthesis"})
_REAL_CATEGORIES = frozenset({"Celeb-real", "YouTube-real"})


def parse_test_list(path: Path) -> list[tuple[str, int]]:
    """Parse the official list into ``(stem, our_label)`` pairs.

    ``our_label`` is 1 for fakes (``Celeb-synthesis``), 0 for reals — i.e. the
    inverse of the file's ``1=real/0=fake`` column.
    """
    out: list[tuple[str, int]] = []
    with path.open("r") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            official, relpath = line.split()
            category = relpath.split("/", 1)[0]
            stem = Path(relpath).stem
            if category in _FAKE_CATEGORIES:
                out.append((stem, 1))
            elif category in _REAL_CATEGORIES:
                out.append((stem, 0))
            else:
                raise ValueError(f"unknown Celeb-DF category: {category!r}")
    return out


class CelebDFFacesDataset(Dataset):
    """Eval-only Celeb-DF v2 dataset over the official 518-video test list."""

    def __init__(
        self,
        cfg: Config,
        frames_per_video: int | None = None,
        test_list: Path | str | None = None,
    ) -> None:
        self.cfg = cfg
        self.faces_root = cfg.paths.resolved("celebdf_root")
        self.frames_per_video = frames_per_video or cfg.data.frames_per_video
        list_path = resolve_path(test_list) if test_list is not None \
            else resolve_path(_DEFAULT_TEST_LIST)
        self.entries = parse_test_list(list_path)

        # Flatten to (stem, label, subdir, frame_idx).
        self._samples: list[tuple[str, int, str, int]] = []
        for stem, label in self.entries:
            subdir = "fake" if label == 1 else "real"
            vid_dir = self.faces_root / subdir / stem
            meta_path = vid_dir / "meta.json"
            if not meta_path.is_file():
                continue  # crops missing for this test video (logged by caller)
            with meta_path.open("r") as fh:
                meta = json.load(fh)
            avail = sorted(int(f["frame_idx"]) for f in meta.get("faces", []))
            num_total = int(meta.get("num_frames_total", 0)) or (
                (avail[-1] + 1) if avail else 0
            )
            frames = select_frames(num_total, avail, self.frames_per_video)
            for fidx in frames:
                self._samples.append((stem, label, subdir, fidx))

    def __len__(self) -> int:
        return len(self._samples)

    def __getitem__(self, i: int) -> dict[str, Any]:
        stem, label, subdir, frame_idx = self._samples[i]
        png = self.faces_root / subdir / stem / f"{frame_idx:04d}.png"
        bgr = cv2.imread(str(png))
        if bgr is None:
            raise FileNotFoundError(f"crop not found: {png}")
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        img = np.transpose(rgb, (2, 0, 1)).astype(np.float32) / 255.0
        return {
            "image": img,
            "label": label,
            "video_id": stem,
            "frame_idx": frame_idx,
            "method": "Celeb-DF" if label == 1 else "",
        }
