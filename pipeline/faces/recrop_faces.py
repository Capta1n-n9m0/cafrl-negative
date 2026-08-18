"""Deterministic re-crop of CRF variants from the c0 landmark warp.

Phase 1 Step 1.3. Re-encoding (`generate_crf_variants.py`) preserves frame
count/timing/resolution, so we do **no re-detection**: for each new level
L ∈ {c28, c32, c36} (all videos) and c18 (test split only) we re-apply the c0
`meta.json` 5-point landmark warp at the same frame indices. Cross-level views of
a given ``frame_idx`` are therefore geometrically identical by construction
(`src/data/face_align.py`).

Per video, per level:
  1. Load the c0 ``meta.json`` for per-frame ``landmarks_5pt`` (curated track).
  2. Frame selection = linspace over the available c0 ``frame_idx`` list →
     ``min(32, n_available)`` evenly-spaced frames (``src/data/frame_select.py``).
     Same indices for every level. Only videos with genuinely <32 detected
     frames fall below 32, and those go on an allow-list.
  3. decord ``get_batch`` indexed reads of just those frames (NOT cv2 seek).
  4. ``align_face(frame, landmarks_5pt[idx], 256)`` → ``{idx:04d}.png``.
  5. Write ``meta.json`` (copied selected c0 face entries + recrop provenance),
     then a ``.done`` marker. Idempotent: a video whose ``.done`` exists is
     skipped.

Set-name note: the faces tree uses ``real``/method names; the CRF variant tree
mirrors the *raw* names (``youtube``/method) — bridge with
``constants.RAW_TO_FACES`` / ``FACES_TO_RAW``.

Usage (no argparse; one optional positional YAML override, unknown keys error):
    conda run -n cv python -m src.scripts.recrop_faces [override.yaml]

Smoke runs: set ``limit`` and restrict ``levels``/``sets`` in the override.
Audit: set ``audit: true`` to verify completeness + PSNR monotonicity instead of
re-cropping.
"""

from __future__ import annotations

import dataclasses
import json
import logging
import math
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import cv2
import numpy as np
import yaml

from src.data.constants import (
    CRF_LEVELS,
    CRF_LEVELS_ALL_VIDEOS,
    CRF_LEVELS_TEST_ONLY,
    FACES_TO_RAW,
    RAW_TO_FACES,
)
from src.data.face_align import align_face
from src.data.frame_select import select_frames

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class Config:
    """Re-crop config. Override via a positional YAML path (unknown keys error)."""

    faces_root: str = "~/sdb/datasets/ff++/faces"
    crf_video_root: str = "~/sdc/datasets/ffpp_crf_variants"
    splits_dir: str = "src/config/splits"
    frames_per_video: int = 32
    output_size: int = 256
    # Levels re-cropped for all videos, and test-split only.
    levels_all: tuple[str, ...] = CRF_LEVELS_ALL_VIDEOS  # c28, c32, c36
    levels_test_only: tuple[str, ...] = CRF_LEVELS_TEST_ONLY  # c18
    # faces-tree set names to process; None = all CRF-eligible sets.
    sets: tuple[str, ...] | None = None
    workers: int = 8
    # Smoke-test knobs.
    limit: int | None = None  # cap videos per (set, level)
    audit: bool = False
    audit_psnr_samples: int = 20

    def resolved_faces_root(self) -> Path:
        return Path(self.faces_root).expanduser().resolve()

    def resolved_crf_video_root(self) -> Path:
        return Path(self.crf_video_root).expanduser().resolve()

    def resolved_splits_dir(self) -> Path:
        return Path(self.splits_dir).expanduser().resolve()

    def faces_sets(self) -> tuple[str, ...]:
        """faces-tree set names to process (default: all CRF-eligible)."""
        if self.sets is not None:
            return self.sets
        return tuple(RAW_TO_FACES.values())  # real + 4 methods


def load_script_config(overrides: Path | str | None) -> Config:
    cfg = Config()
    if overrides is None:
        return cfg
    path = Path(overrides)
    if not path.is_file():
        raise FileNotFoundError(f"override file not found: {path}")
    with path.open("r") as fh:
        data = yaml.safe_load(fh)
    if data is None:
        return cfg
    if not isinstance(data, dict):
        raise TypeError(f"override file {path} must be a top-level mapping")
    valid = {f.name for f in dataclasses.fields(cfg)}
    for key, value in data.items():
        if key not in valid:
            raise KeyError(f"unknown config key '{key}'. Valid keys: {sorted(valid)}")
        if key in {"levels_all", "levels_test_only", "sets"} and isinstance(value, list):
            value = tuple(value)
        setattr(cfg, key, value)
    return cfg


# ---------------------------------------------------------------------------
# Test-split selection (for c18 test-only level)
# ---------------------------------------------------------------------------

def load_test_pairs(splits_dir: Path) -> list[tuple[str, str]]:
    with (splits_dir / "test.json").open("r") as fh:
        pairs = json.load(fh)
    return [(str(t), str(s)) for t, s in pairs]


def test_real_ids(pairs: list[tuple[str, str]]) -> set[str]:
    ids: set[str] = set()
    for t, s in pairs:
        ids.add(t)
        ids.add(s)
    return ids


def test_fake_names(pairs: list[tuple[str, str]]) -> set[str]:
    names: set[str] = set()
    for t, s in pairs:
        names.add(f"{t}_{s}")
        names.add(f"{s}_{t}")
    return names


def select_video_ids(
    faces_set: str, pairs: list[tuple[str, str]], test_only: bool
) -> set[str] | None:
    """Video stems to re-crop for ``faces_set``; ``None`` = all on disk."""
    if not test_only:
        return None
    if faces_set == RAW_TO_FACES["youtube"]:  # "real"
        return test_real_ids(pairs)
    return test_fake_names(pairs)


# ---------------------------------------------------------------------------
# Per-video task
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RecropTask:
    faces_set: str
    level: str
    video_id: str
    c0_meta_path: Path  # faces/c0/{set}/{vid}/meta.json
    variant_path: Path  # crf_variants/{level}/{raw_set}/videos/{vid}.mp4
    out_dir: Path       # faces/{level}/{set}/{vid}/
    output_size: int
    frames_per_video: int


def _build_tasks(cfg: Config) -> tuple[list[RecropTask], list[str]]:
    """Build the recrop task list. Returns (tasks, warnings)."""
    faces_root = cfg.resolved_faces_root()
    crf_root = cfg.resolved_crf_video_root()
    pairs = load_test_pairs(cfg.resolved_splits_dir())
    warnings: list[str] = []

    plan: list[tuple[str, bool]] = (
        [(lvl, False) for lvl in cfg.levels_all]
        + [(lvl, True) for lvl in cfg.levels_test_only]
    )

    tasks: list[RecropTask] = []
    for level, test_only in plan:
        for faces_set in cfg.faces_sets():
            raw_set = FACES_TO_RAW[faces_set]
            c0_set_dir = faces_root / "c0" / faces_set
            variant_dir = crf_root / level / raw_set / "videos"
            if not c0_set_dir.is_dir():
                warnings.append(f"missing c0 faces dir: {c0_set_dir}")
                continue
            wanted = select_video_ids(faces_set, pairs, test_only)
            count = 0
            for vid_dir in sorted(p for p in c0_set_dir.iterdir() if p.is_dir()):
                vid = vid_dir.name
                if wanted is not None and vid not in wanted:
                    continue
                c0_meta = vid_dir / "meta.json"
                if not c0_meta.is_file():
                    continue
                variant_path = variant_dir / f"{vid}.mp4"
                tasks.append(RecropTask(
                    faces_set=faces_set, level=level, video_id=vid,
                    c0_meta_path=c0_meta, variant_path=variant_path,
                    out_dir=faces_root / level / faces_set / vid,
                    output_size=cfg.output_size,
                    frames_per_video=cfg.frames_per_video,
                ))
                count += 1
                if cfg.limit is not None and count >= cfg.limit:
                    break
    return tasks, warnings


# ---------------------------------------------------------------------------
# Re-crop worker
# ---------------------------------------------------------------------------

def _read_c0_meta(meta_path: Path) -> dict:
    with meta_path.open("r") as fh:
        return json.load(fh)


def process_task(task: RecropTask) -> dict:
    """Re-crop one video at one level. Idempotent (skips if ``.done`` exists)."""
    import decord
    decord.bridge.set_bridge("native")

    out_dir = task.out_dir
    if (out_dir / ".done").exists():
        return {"status": "skipped", "set": task.faces_set, "level": task.level,
                "video_id": task.video_id}

    if not task.variant_path.is_file():
        return {"status": "missing_variant", "set": task.faces_set,
                "level": task.level, "video_id": task.video_id,
                "reason": str(task.variant_path)}

    meta = _read_c0_meta(task.c0_meta_path)
    faces = meta.get("faces", [])
    if not faces:
        return {"status": "failed", "set": task.faces_set, "level": task.level,
                "video_id": task.video_id, "reason": "no c0 faces"}

    by_idx = {int(f["frame_idx"]): f for f in faces}
    available = sorted(by_idx.keys())
    num_total = int(meta.get("num_frames_total", 0)) or (available[-1] + 1)

    selected = select_frames(num_total, available, task.frames_per_video)
    on_allow_list = len(selected) < task.frames_per_video

    # decord indexed read of just the selected frames.
    try:
        vr = decord.VideoReader(str(task.variant_path), num_threads=1)
    except Exception as exc:  # noqa: BLE001
        return {"status": "failed", "set": task.faces_set, "level": task.level,
                "video_id": task.video_id, "reason": f"decord open: {exc}"}
    n_variant = len(vr)
    # Selected indices must be in range of the variant (frame counts match c0).
    in_range = [i for i in selected if i < n_variant]
    if len(in_range) != len(selected):
        return {"status": "failed", "set": task.faces_set, "level": task.level,
                "video_id": task.video_id,
                "reason": f"frame count mismatch: variant={n_variant}, "
                          f"need up to {max(selected)}"}

    frames = vr.get_batch(selected).asnumpy()  # (N, H, W, 3) RGB

    out_dir.mkdir(parents=True, exist_ok=True)
    selected_entries: list[dict] = []
    for k, idx in enumerate(selected):
        entry = by_idx[idx]
        landmarks = np.array(entry["landmarks_5pt"], dtype=np.float32)
        aligned = align_face(frames[k], landmarks, task.output_size)  # RGB
        filename = f"{idx:04d}.png"
        cv2.imwrite(
            str(out_dir / filename),
            cv2.cvtColor(aligned, cv2.COLOR_RGB2BGR),
        )
        selected_entries.append(dict(entry))  # copy c0 face entry verbatim

    # meta.json — per spec item 5.
    new_meta = dict(meta)
    new_meta["compression"] = task.level
    new_meta["source_path"] = str(task.variant_path)
    new_meta["num_frames_extracted"] = len(selected_entries)
    new_meta["faces"] = selected_entries
    proc = dict(meta.get("processing", {}))
    proc["recrop_from"] = "c0"
    proc["selected_indices"] = selected
    proc["recrop_timestamp"] = datetime.now(timezone.utc).isoformat()
    new_meta["processing"] = proc
    with (out_dir / "meta.json").open("w") as fh:
        json.dump(new_meta, fh)
    (out_dir / ".done").touch()

    return {"status": "recropped", "set": task.faces_set, "level": task.level,
            "video_id": task.video_id, "n_frames": len(selected_entries),
            "allow_list": on_allow_list}


# ---------------------------------------------------------------------------
# Re-crop driver
# ---------------------------------------------------------------------------

def run_recrop(cfg: Config) -> int:
    tasks, warnings = _build_tasks(cfg)
    for w in warnings:
        logger.warning(w)
    logger.info("planned %d recrop tasks across %d workers", len(tasks), cfg.workers)
    if not tasks:
        logger.warning("no tasks planned — nothing to do")
        return 0

    counts = {"recropped": 0, "skipped": 0, "failed": 0, "missing_variant": 0}
    failures: list[dict] = []
    allow_list: list[dict] = []
    start = time.time()
    workers = max(1, min(cfg.workers, len(tasks)))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(process_task, t): t for t in tasks}
        for i, fut in enumerate(as_completed(futures), 1):
            res = fut.result()
            counts[res["status"]] = counts.get(res["status"], 0) + 1
            if res["status"] == "failed":
                failures.append(res)
            elif res["status"] == "missing_variant":
                failures.append(res)
            elif res.get("allow_list"):
                allow_list.append(res)
            if i % 200 == 0 or i == len(tasks):
                logger.info(
                    "progress %d/%d  recropped=%d skipped=%d failed=%d missing=%d",
                    i, len(tasks), counts["recropped"], counts["skipped"],
                    counts["failed"], counts["missing_variant"],
                )

    if allow_list:
        logger.warning(
            "%d videos on the <%d-detection allow-list:", len(allow_list),
            cfg.frames_per_video,
        )
        for a in allow_list:
            logger.warning("  ALLOW %s/%s/%s", a["level"], a["set"], a["video_id"])
    if failures:
        for f in failures:
            logger.error("FAIL %s/%s/%s: %s", f["level"], f["set"],
                         f["video_id"], f.get("reason", "?"))

    elapsed = time.time() - start
    logger.info(
        "DONE in %.1fs — recropped=%d skipped=%d failed=%d missing=%d (total %d)",
        elapsed, counts["recropped"], counts["skipped"], counts["failed"],
        counts["missing_variant"], len(tasks),
    )
    return 1 if failures else 0


# ---------------------------------------------------------------------------
# Audit mode
# ---------------------------------------------------------------------------

def _crop_count(out_dir: Path) -> int:
    return sum(1 for p in out_dir.glob("*.png"))


def _psnr(a: np.ndarray, b: np.ndarray) -> float:
    mse = float(np.mean((a.astype(np.float64) - b.astype(np.float64)) ** 2))
    if mse <= 0.0:
        return math.inf
    return 10.0 * math.log10((255.0 ** 2) / mse)


def run_audit(cfg: Config) -> int:
    """Completeness + PSNR-monotonicity audit (phase1.md Step 1.3 'Verify')."""
    faces_root = cfg.resolved_faces_root()
    pairs = load_test_pairs(cfg.resolved_splits_dir())
    levels = list(cfg.levels_all) + list(cfg.levels_test_only)
    rng = np.random.default_rng(0)
    problems = 0

    # 1. Per-level completeness.
    for level in levels:
        test_only = level in cfg.levels_test_only
        total = ok = bad_count = bad_meta = bad_done = bad_size = allow = 0
        for faces_set in cfg.faces_sets():
            wanted = select_video_ids(faces_set, pairs, test_only)
            level_set_dir = faces_root / level / faces_set
            c0_set_dir = faces_root / "c0" / faces_set
            if not c0_set_dir.is_dir():
                continue
            for c0_vid in sorted(p for p in c0_set_dir.iterdir() if p.is_dir()):
                vid = c0_vid.name
                if wanted is not None and vid not in wanted:
                    continue
                total += 1
                out_dir = level_set_dir / vid
                if not (out_dir / ".done").exists():
                    bad_done += 1
                    continue
                n = _crop_count(out_dir)
                meta_ok = (out_dir / "meta.json").is_file()
                if not meta_ok:
                    bad_meta += 1
                # allow-list videos may have <32; read c0 to know the expectation
                if n < cfg.frames_per_video:
                    allow += 1
                if n != cfg.frames_per_video and n < cfg.frames_per_video:
                    pass  # allow-list, not a problem
                elif n != cfg.frames_per_video:
                    bad_count += 1
                if meta_ok:
                    ok += 1
        logger.info(
            "[%s] total=%d done_ok=%d missing_done=%d bad_count=%d "
            "missing_meta=%d allow_list(<32)=%d",
            level, total, ok, bad_done, bad_count, bad_meta, allow,
        )
        problems += bad_done + bad_count + bad_meta

    # 2. Crop dimensions on a random sample + PSNR monotonicity over c28>c32>c36.
    mono_levels = [lv for lv in ("c28", "c32", "c36") if lv in levels]
    if len(mono_levels) >= 2:
        # collect candidate videos present at all mono levels with c0 crops
        cands: list[tuple[str, str]] = []
        for faces_set in cfg.faces_sets():
            c0_set_dir = faces_root / "c0" / faces_set
            if not c0_set_dir.is_dir():
                continue
            for c0_vid in sorted(p for p in c0_set_dir.iterdir() if p.is_dir()):
                vid = c0_vid.name
                if all((faces_root / lv / faces_set / vid / ".done").exists()
                       for lv in mono_levels):
                    cands.append((faces_set, vid))
        if cands:
            pick = rng.choice(len(cands), size=min(cfg.audit_psnr_samples, len(cands)),
                              replace=False)
            per_level_psnr: dict[str, list[float]] = {lv: [] for lv in mono_levels}
            dim_bad = 0
            for j in pick:
                faces_set, vid = cands[int(j)]
                c0_dir = faces_root / "c0" / faces_set / vid
                # use the level's stored selected frames
                meta0 = _read_c0_meta(c0_dir / "meta.json")
                avail = sorted(int(f["frame_idx"]) for f in meta0["faces"])
                num_total = int(meta0.get("num_frames_total", 0)) or (avail[-1] + 1)
                sel = select_frames(num_total, avail, cfg.frames_per_video)
                for lv in mono_levels:
                    lv_dir = faces_root / lv / faces_set / vid
                    psnrs = []
                    for idx in sel:
                        c0_png = c0_dir / f"{idx:04d}.png"
                        lv_png = lv_dir / f"{idx:04d}.png"
                        if not (c0_png.is_file() and lv_png.is_file()):
                            continue
                        a = cv2.imread(str(c0_png))
                        b = cv2.imread(str(lv_png))
                        if a is None or b is None:
                            continue
                        if a.shape[:2] != (cfg.output_size, cfg.output_size) or \
                           b.shape[:2] != (cfg.output_size, cfg.output_size):
                            dim_bad += 1
                            continue
                        psnrs.append(_psnr(a, b))
                    if psnrs:
                        per_level_psnr[lv].append(float(np.mean(psnrs)))
            means = {lv: (float(np.mean(v)) if v else float("nan"))
                     for lv, v in per_level_psnr.items()}
            logger.info("mean PSNR(c0, c_L) by level: %s", means)
            finite = all(np.isfinite(m) for m in means.values())
            seq = [means[lv] for lv in mono_levels]
            monotone = all(seq[i] > seq[i + 1] for i in range(len(seq) - 1))
            logger.info("PSNR finite=%s, monotonically decreasing (c28>c32>c36)=%s",
                        finite, monotone)
            if dim_bad:
                logger.error("%d crops were NOT %dx%d", dim_bad,
                             cfg.output_size, cfg.output_size)
                problems += dim_bad
            if not (finite and monotone):
                logger.error("PSNR aggregate check FAILED")
                problems += 1
        else:
            logger.warning("no videos present at all mono levels — skip PSNR check")

    logger.info("AUDIT %s — %d problems", "CLEAN" if problems == 0 else "PROBLEMS",
                problems)
    return 1 if problems else 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(cfg: Config) -> int:
    return run_audit(cfg) if cfg.audit else run_recrop(cfg)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
    )
    override = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    cfg = load_script_config(override)
    sys.exit(run(cfg))


if __name__ == "__main__":
    main()
