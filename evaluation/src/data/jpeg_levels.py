"""JPEG level map for the Phase-6 E3 arms (codec swap, H.264 -> JPEG).

Why this exists
---------------
E3 asks whether the gain of multi-quality training comes from *H.264* data or from
*any* compression of matched strength. The JPEG arms therefore keep everything of
the H.264 arm except the codec (decision "Phase 6 build: JPEG arms reuse the H.264
plan and apply JPEG in the data worker"):

* the sampler keeps the H.264 level names and video table, so the plan (videos,
  frames, flips, pairs) is the b7 plan for the same seed; each level's frame
  availability is restricted to ``avail_L ∩ avail_c0`` because every JPEG view is
  made from the **c0** crop at the planned frame (S0 m6);
* for a level ``L != c0`` the dataset worker loads the c0 crop and re-encodes it as
  JPEG at the calibrated ``level_to_qf[L]`` (one fixed QF per level, no RNG), on the
  uint8 RGB 256² crop, *before* flip and ``to_tensor`` (S0 M6); c0 is untouched.

The QFs come from ``runs/phase6_build/jpeg_calibration.json`` (schema S0 §6), written
by stage S1. This module reads only ``schema_version``, ``status``, ``level_to_qf``,
``jpeg_encoder.params`` and ``arm_levels``, refuses anything that is not
``status: "final"`` unless the caller explicitly allows a fixture (tests), and
records the file's sha256 so a run's ``config.yaml`` names the exact calibration.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import pandas as pd

SCHEMA_VERSION = 1
# Levels the calibration may name (the six training bins). c0 is the source crop
# and must map to null.
_KNOWN_LEVELS: tuple[str, ...] = ("c0", "c23", "c28", "c32", "c36", "c40")
# The only encoder parameter the contract allows (nothing else is set: default
# 4:2:0 chroma, baseline, no optimize).
_ALLOWED_ENCODER_PARAMS: frozenset[str] = frozenset({"IMWRITE_JPEG_QUALITY"})


class CalibrationError(ValueError):
    """The calibration file is missing, malformed, or not allowed for this use."""


@dataclass(frozen=True)
class JpegCalibration:
    """The validated subset of ``jpeg_calibration.json`` that training needs."""

    path: str
    sha256: str
    status: str
    schema_version: int
    level_to_qf: dict[str, int | None]
    encoder_params: dict[str, Any]
    arm_levels: dict[str, tuple[str, ...]] = field(default_factory=dict)

    def qf_map_for(self, levels: Sequence[str]) -> dict[str, int | None]:
        """``level -> QF`` for the given training levels (c0 -> None).

        Raises if a non-c0 level has no integer QF, so a JPEG arm can never train
        a level silently as plain c0.
        """
        out: dict[str, int | None] = {}
        for lvl in levels:
            if lvl == "c0":
                out[lvl] = None
                continue
            qf = self.level_to_qf.get(lvl)
            if qf is None:
                raise CalibrationError(
                    f"{self.path}: level_to_qf has no QF for training level {lvl!r}")
            out[lvl] = int(qf)
        return out

    def provenance(self) -> dict[str, Any]:
        """What a run's config.yaml records about the calibration."""
        return {
            "path": self.path,
            "sha256": self.sha256,
            "status": self.status,
            "schema_version": self.schema_version,
            "level_to_qf": dict(self.level_to_qf),
            "encoder_params": dict(self.encoder_params),
            "cv2_version": cv2.__version__,
        }


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jpeg_calibration(
    path: str | Path, *, allow_fixture: bool = False
) -> JpegCalibration:
    """Load and validate a calibration file (S0 §6 schema).

    Args:
        path: the JSON file named in config/CLI (never a hard-coded copy).
        allow_fixture: accept ``status: "fixture"`` (unit tests and pipeline
            smokes only). Without it anything but ``"final"`` is refused, so a
            real run can never train on the synthetic fixture.
    """
    p = Path(path).expanduser()
    if not p.is_file():
        raise CalibrationError(f"calibration file not found: {p}")
    try:
        data = json.loads(p.read_text())
    except json.JSONDecodeError as exc:
        raise CalibrationError(f"{p}: not valid JSON ({exc})") from exc
    if not isinstance(data, dict):
        raise CalibrationError(f"{p}: top level must be an object")

    sv = data.get("schema_version")
    if sv != SCHEMA_VERSION:
        raise CalibrationError(f"{p}: schema_version {sv!r} != {SCHEMA_VERSION}")

    status = data.get("status")
    if status not in ("final", "fixture"):
        raise CalibrationError(f"{p}: status {status!r} not in ('final', 'fixture')")
    if status != "final" and not allow_fixture:
        raise CalibrationError(
            f"{p}: status is {status!r}; only a 'final' calibration may be used "
            "for training (pass --allow-fixture-calibration in tests/smokes only)")

    raw_map = data.get("level_to_qf")
    if not isinstance(raw_map, dict) or not raw_map:
        raise CalibrationError(f"{p}: level_to_qf must be a non-empty object")
    level_to_qf: dict[str, int | None] = {}
    for lvl, qf in raw_map.items():
        if lvl not in _KNOWN_LEVELS:
            raise CalibrationError(f"{p}: level_to_qf has unknown level {lvl!r}")
        if lvl == "c0":
            if qf is not None:
                raise CalibrationError(f"{p}: level_to_qf['c0'] must be null")
            level_to_qf[lvl] = None
            continue
        # bool is an int subclass; refuse it explicitly.
        if isinstance(qf, bool) or not isinstance(qf, int) or not (1 <= qf <= 100):
            raise CalibrationError(
                f"{p}: level_to_qf[{lvl!r}] = {qf!r} is not an integer QF in [1, 100]")
        level_to_qf[lvl] = int(qf)

    enc = data.get("jpeg_encoder")
    if not isinstance(enc, dict) or not isinstance(enc.get("params"), dict):
        raise CalibrationError(f"{p}: jpeg_encoder.params missing")
    params = dict(enc["params"])
    if set(params) != _ALLOWED_ENCODER_PARAMS:
        raise CalibrationError(
            f"{p}: jpeg_encoder.params must set exactly {sorted(_ALLOWED_ENCODER_PARAMS)} "
            f"(got {sorted(params)}); this code sets nothing else")

    arms_raw = data.get("arm_levels")
    if not isinstance(arms_raw, dict) or not arms_raw:
        raise CalibrationError(f"{p}: arm_levels must be a non-empty object")
    arm_levels: dict[str, tuple[str, ...]] = {}
    for arm, lv in arms_raw.items():
        if not isinstance(lv, list) or not lv or any(x not in _KNOWN_LEVELS for x in lv):
            raise CalibrationError(f"{p}: arm_levels[{arm!r}] = {lv!r} is invalid")
        missing = [x for x in lv if x != "c0" and level_to_qf.get(x) is None]
        if missing:
            raise CalibrationError(
                f"{p}: arm_levels[{arm!r}] uses levels without a QF: {missing}")
        arm_levels[str(arm)] = tuple(lv)

    return JpegCalibration(
        path=str(p.resolve()),
        sha256=_sha256(p),
        status=str(status),
        schema_version=int(sv),
        level_to_qf=level_to_qf,
        encoder_params=params,
        arm_levels=arm_levels,
    )


def jpeg_roundtrip(rgb: np.ndarray, qf: int) -> np.ndarray:
    """RGB -> BGR -> ``cv2.imencode('.jpg', [IMWRITE_JPEG_QUALITY, qf])`` ->
    ``cv2.imdecode`` -> RGB, on a ``H×W×3`` uint8 array. Nothing else is set.

    This is the exact roundtrip the calibration measured (S0 §6
    ``jpeg_encoder.roundtrip``); any other parameter would break the PSNR match.
    """
    if rgb.dtype != np.uint8 or rgb.ndim != 3 or rgb.shape[2] != 3:
        raise ValueError(f"expected HxWx3 uint8 RGB, got {rgb.dtype} {rgb.shape}")
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    ok, enc = cv2.imencode(".jpg", bgr, [int(cv2.IMWRITE_JPEG_QUALITY), int(qf)])
    if not ok:
        raise RuntimeError(f"cv2.imencode failed at QF {qf}")
    dec = cv2.imdecode(enc, cv2.IMREAD_COLOR)
    if dec is None:
        raise RuntimeError(f"cv2.imdecode failed at QF {qf}")
    return cv2.cvtColor(dec, cv2.COLOR_BGR2RGB)


def restrict_to_c0_availability(
    video_table: pd.DataFrame,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Restrict every level's ``frame_indices`` to the frames that also have a c0 crop.

    ``video_table`` is the sampler input (union of per-level index rows with a
    ``level`` column; it must contain the c0 rows). A JPEG view at level L is made
    from the c0 crop at the planned frame, so the frame must exist at c0 as well
    as at L (keeping L's own list preserves the H.264 plan wherever the lists
    already agree). Raises if a video has no c0 row or an intersection is empty:
    silently dropping either would change the plan without a trace.

    Returns ``(table, stats)``; ``stats`` counts the rows whose list changed.
    """
    if "c0" not in set(video_table["level"]):
        raise ValueError("JPEG arms need the c0 rows in the video table")
    c0 = {
        (str(r.video_id), str(r.set)): set(int(x) for x in r.frame_indices)
        for r in video_table[video_table["level"] == "c0"].itertuples(index=False)
    }
    new_lists: list[list[int]] = []
    changed: dict[str, int] = {}
    dropped_frames: dict[str, int] = {}
    for r in video_table.itertuples(index=False):
        lvl = str(r.level)
        cur = [int(x) for x in r.frame_indices]
        if lvl == "c0":
            new_lists.append(cur)
            continue
        key = (str(r.video_id), str(r.set))
        if key not in c0:
            raise ValueError(f"video {key} has level {lvl} rows but no c0 row")
        inter = [f for f in cur if f in c0[key]]
        if not inter:
            raise ValueError(f"video {key}: no frame of level {lvl} has a c0 crop")
        if len(inter) != len(cur):
            changed[lvl] = changed.get(lvl, 0) + 1
            dropped_frames[lvl] = dropped_frames.get(lvl, 0) + len(cur) - len(inter)
        new_lists.append(inter)
    out = video_table.copy()
    out["frame_indices"] = new_lists
    return out, {"rows_changed": changed, "frames_dropped": dropped_frames}


def qf_for(level_to_qf: Mapping[str, int | None] | None, level: str) -> int | None:
    """The QF applied to a crop at ``level`` (None = no JPEG: H.264 arms and c0)."""
    if level_to_qf is None or level == "c0":
        return None
    qf = level_to_qf.get(level)
    if qf is None:
        raise KeyError(f"JPEG map has no QF for level {level!r}")
    return int(qf)
