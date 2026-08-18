"""Generate H.264 CRF variants of FF++ from the lossless c0 sources.

Re-encodes the youtube reals + the four protocol fakes (Deepfakes, Face2Face,
FaceSwap, NeuralTextures) from c0 to CRF {28, 32, 36} for all 1000 videos per
set, plus CRF 18 for the test split only. FaceShifter and DFD are excluded (see
``src/data/constants.py``).

The compression *level* (not the on-disk crop) is the learning signal CAFRL
needs, so faithful real H.264 re-encoding — not a JPEG approximation — is the
point of this step (implementation-plan.md §4.2 / G4). Re-crops to faces come in
Step 1.3 and reuse the c0 landmark warp at the same frame indices.

Design notes
------------
* ``-preset medium``: FF++ never published their preset; we fix ``medium`` (the
  x264 default) for a reproducible speed/quality operating point.
* ``-fps_mode passthrough``: copy each source frame 1:1, never insert/drop frames
  to hit a constant frame rate. Some FF++ sources have odd/VFR timebases; without
  this, libx264's default CFR muxing can duplicate frames and break the
  c0-frame-count invariant the re-crop pairing relies on.
* ``-pix_fmt yuv420p``: 8-bit 4:2:0, the standard delivery format and what the
  faces pipeline expects.

Idempotency & verification
--------------------------
Per output: skipped if the file exists AND its ``-count_frames`` frame count
equals the c0 source's. A ``.done`` marker is written per (set, level) once every
video in that set+level passes. Frame-count mismatches are logged to
``failed.log`` under the output root, re-encoded once, then flagged for manual
review if still failing.

Usage (no argparse — a dataclass + one optional positional YAML override):
    conda run -n cv python -m src.scripts.generate_crf_variants [override.yaml]

The override YAML follows the same unknown-key-is-an-error rule as the main
config loader. A ``limit`` field caps videos per (set, level) for smoke tests.
"""

from __future__ import annotations

import csv
import dataclasses
import json
import logging
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from src.data.constants import (
    CRF_LEVELS,
    CRF_LEVELS_ALL_VIDEOS,
    CRF_LEVELS_TEST_ONLY,
    CRF_RAW_SETS,
    PROTOCOL_METHODS,
    RAW_REAL_SET,
    raw_set_dir,
)

logger = logging.getLogger(__name__)

# Cached frame-passthrough flag (resolved once per process; see _passthrough_args).
_PASSTHROUGH_ARGS: list[str] | None = None


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class Config:
    """Script config. Override via a positional YAML path (unknown keys error)."""

    dataset_root: str = "~/sdc/datasets/ffpp_original"
    output_root: str = "~/sdc/datasets/ffpp_crf_variants"
    splits_dir: str = "src/config/splits"
    # Levels generated for all 1000 videos of each set, and (test-split only).
    crf_levels_all: tuple[str, ...] = CRF_LEVELS_ALL_VIDEOS  # c28, c32, c36
    crf_levels_test_only: tuple[str, ...] = CRF_LEVELS_TEST_ONLY  # c18
    sets: tuple[str, ...] = CRF_RAW_SETS  # youtube + 4 protocol methods
    workers: int = 20
    preset: str = "medium"
    # Threads per ffmpeg/ffprobe process. Uncapped, each x264 spawns ~1.5x
    # nproc threads (104 cores -> ~150) and concurrent workers thrash; 8 is
    # efficient for 1080p and lets workers*threads ~ saturate the box.
    threads: int = 8
    # Source (c0) frame counts from ffpp_metadata.csv instead of a full
    # ffprobe decode per task. Validated decode-accurate (2026-06-12, 25/25
    # sampled outputs); missing entries fall back to ffprobe.
    metadata_csv: str = "../../datasets/ffpp_metadata.csv"
    # Cap videos per (set, level); None = no cap. For smoke tests only.
    limit: int | None = None

    def resolved_dataset_root(self) -> Path:
        return Path(self.dataset_root).expanduser().resolve()

    def resolved_output_root(self) -> Path:
        return Path(self.output_root).expanduser().resolve()

    def resolved_splits_dir(self) -> Path:
        return Path(self.splits_dir).expanduser().resolve()

    def resolved_metadata_csv(self) -> Path:
        return Path(self.metadata_csv).expanduser().resolve()


# ---------------------------------------------------------------------------
# Minimal YAML override loader (same unknown-key-error rule as config/load.py)
# ---------------------------------------------------------------------------

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
            raise KeyError(
                f"unknown config key '{key}'. Valid keys: {sorted(valid)}"
            )
        # Coerce YAML lists into tuples for the tuple-typed fields.
        if key in {"crf_levels_all", "crf_levels_test_only", "sets"} and isinstance(
            value, list
        ):
            value = tuple(value)
        setattr(cfg, key, value)
    return cfg


# ---------------------------------------------------------------------------
# Test-split selection (local to this step; full splits.py is Step 1.4)
# ---------------------------------------------------------------------------

def load_test_split_pairs(splits_dir: Path) -> list[tuple[str, str]]:
    """Load test.json as a list of (target, source) ID-pair tuples."""
    with (splits_dir / "test.json").open("r") as fh:
        pairs = json.load(fh)
    return [(t, s) for t, s in pairs]


def test_split_real_ids(pairs: list[tuple[str, str]]) -> set[str]:
    """Union of all IDs appearing in the test pairs (the test-split reals)."""
    ids: set[str] = set()
    for t, s in pairs:
        ids.add(t)
        ids.add(s)
    return ids


def test_split_fake_names(pairs: list[tuple[str, str]]) -> set[str]:
    """Both orderings ``{t}_{s}`` and ``{s}_{t}`` of each test pair (per method)."""
    names: set[str] = set()
    for t, s in pairs:
        names.add(f"{t}_{s}")
        names.add(f"{s}_{t}")
    return names


def select_video_ids(
    raw_set: str, pairs: list[tuple[str, str]], test_only: bool
) -> set[str] | None:
    """Return the set of video stems to encode for ``raw_set``.

    ``None`` means "all videos in the set directory". For the c18 test-only loop,
    returns the test-split reals (for youtube) or the both-ordering fake names
    (for the protocol methods).
    """
    if not test_only:
        return None
    if raw_set == RAW_REAL_SET:
        return test_split_real_ids(pairs)
    return test_split_fake_names(pairs)


# ---------------------------------------------------------------------------
# ffmpeg / ffprobe helpers (run in worker processes)
# ---------------------------------------------------------------------------

def count_frames(video: Path, threads: int = 8) -> int | None:
    """Decode-accurate frame count via ``ffprobe -count_frames``; None on error."""
    try:
        out = subprocess.run(
            [
                "ffprobe", "-v", "error", "-threads", str(threads),
                "-count_frames", "-select_streams", "v:0",
                "-show_entries", "stream=nb_read_frames",
                "-of", "csv=p=0", str(video),
            ],
            capture_output=True, text=True, check=True,
        )
    except subprocess.CalledProcessError:
        return None
    txt = out.stdout.strip()
    if not txt or not txt.isdigit():
        return None
    return int(txt)


def _passthrough_args() -> list[str]:
    """Frame-passthrough flag — ``-fps_mode passthrough`` on FFmpeg >=5,
    its identical predecessor ``-vsync passthrough`` on FFmpeg 4.x.

    The option was renamed (``-vsync`` -> ``-fps_mode``) in FFmpeg 5.0 with the
    same semantics: copy each source frame 1:1, never insert/drop to hit a
    constant frame rate. We probe the installed ffmpeg once and cache the result
    so the c0-frame-count invariant holds on whichever version is on PATH.
    """
    global _PASSTHROUGH_ARGS
    if _PASSTHROUGH_ARGS is not None:
        return _PASSTHROUGH_ARGS
    try:
        ver = subprocess.run(
            ["ffmpeg", "-version"], capture_output=True, text=True, check=True
        ).stdout
        # e.g. "ffmpeg version 4.2.2 ..." or "ffmpeg version n6.0 ..."
        token = ver.split()[2].lstrip("n")
        major = int(token.split(".")[0])
    except (subprocess.CalledProcessError, IndexError, ValueError):
        major = 5  # assume modern on probe failure
    _PASSTHROUGH_ARGS = (
        ["-fps_mode", "passthrough"] if major >= 5 else ["-vsync", "passthrough"]
    )
    return _PASSTHROUGH_ARGS


def encode_one(src: Path, dst: Path, crf: int, preset: str, threads: int = 8) -> bool:
    """Re-encode ``src`` -> ``dst`` at the given CRF. True on ffmpeg success."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_suffix(dst.suffix + ".tmp.mp4")
    cmd = [
        "ffmpeg", "-y", "-i", str(src),
        "-c:v", "libx264", "-crf", str(crf),
        "-preset", preset, "-pix_fmt", "yuv420p",
        "-threads", str(threads),
        *_passthrough_args(), "-an", str(tmp),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        if tmp.exists():
            tmp.unlink()
        logger.error("ffmpeg failed for %s: %s", dst.name, proc.stderr[-400:])
        return False
    tmp.replace(dst)
    return True


# ---------------------------------------------------------------------------
# Per-video task
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class EncodeTask:
    raw_set: str
    level: str
    crf: int
    src: Path
    dst: Path
    preset: str
    threads: int = 8
    # Decode-accurate c0 frame count from ffpp_metadata.csv (None -> probe).
    src_frames: int | None = None


def process_task(task: EncodeTask) -> dict:
    """Worker entry point: idempotent encode + frame-count verification.

    Returns a status dict: ``{status, set, level, name, src_frames, dst_frames}``
    where status is one of: skipped, encoded, failed.
    """
    src_frames = task.src_frames
    if src_frames is None:
        src_frames = count_frames(task.src, task.threads)
    if src_frames is None:
        return {
            "status": "failed", "set": task.raw_set, "level": task.level,
            "name": task.dst.name, "reason": "source unreadable",
        }

    # Idempotency: existing output that already matches the source -> skip.
    if task.dst.exists():
        existing = count_frames(task.dst, task.threads)
        if existing == src_frames:
            return {
                "status": "skipped", "set": task.raw_set, "level": task.level,
                "name": task.dst.name, "src_frames": src_frames,
                "dst_frames": existing,
            }

    # Encode, verify; one retry on a frame-count mismatch.
    for attempt in (1, 2):
        ok = encode_one(task.src, task.dst, task.crf, task.preset, task.threads)
        if not ok:
            continue
        dst_frames = count_frames(task.dst, task.threads)
        if dst_frames == src_frames:
            return {
                "status": "encoded", "set": task.raw_set, "level": task.level,
                "name": task.dst.name, "src_frames": src_frames,
                "dst_frames": dst_frames, "attempt": attempt,
            }
        logger.warning(
            "frame mismatch %s: src=%s dst=%s (attempt %d)",
            task.dst.name, src_frames, dst_frames, attempt,
        )

    return {
        "status": "failed", "set": task.raw_set, "level": task.level,
        "name": task.dst.name, "src_frames": src_frames,
        "dst_frames": count_frames(task.dst, task.threads),
        "reason": "frame mismatch after retry",
    }


# ---------------------------------------------------------------------------
# Task building
# ---------------------------------------------------------------------------

def load_source_frame_counts(csv_path: Path, dataset_root: Path) -> dict[Path, int]:
    """Map absolute c0 source path -> decode-accurate frame count from the CSV.

    Returns an empty dict (-> per-task ffprobe fallback) if the CSV is missing.
    """
    if not csv_path.is_file():
        logger.warning("metadata CSV not found (%s); falling back to ffprobe", csv_path)
        return {}
    counts: dict[Path, int] = {}
    with csv_path.open(newline="") as fh:
        for row in csv.DictReader(fh):
            if row["compression"] == "c0":
                counts[dataset_root / row["rel_path"]] = int(row["num_frames"])
    logger.info("loaded %d c0 frame counts from %s", len(counts), csv_path)
    return counts


def build_tasks(cfg: Config) -> list[EncodeTask]:
    dataset_root = cfg.resolved_dataset_root()
    output_root = cfg.resolved_output_root()
    pairs = load_test_split_pairs(cfg.resolved_splits_dir())
    src_counts = load_source_frame_counts(cfg.resolved_metadata_csv(), dataset_root)

    plan: list[tuple[str, bool]] = (
        [(lvl, False) for lvl in cfg.crf_levels_all]
        + [(lvl, True) for lvl in cfg.crf_levels_test_only]
    )

    tasks: list[EncodeTask] = []
    for level, test_only in plan:
        crf = CRF_LEVELS[level]
        wanted = None  # filled per set below
        for raw_set in cfg.sets:
            src_dir = raw_set_dir(dataset_root, raw_set, "c0")
            if not src_dir.is_dir():
                logger.warning("missing source dir, skipping: %s", src_dir)
                continue
            wanted = select_video_ids(raw_set, pairs, test_only)
            out_dir = output_root / level / raw_set / "videos"
            srcs = sorted(src_dir.glob("*.mp4"))
            if wanted is not None:
                srcs = [p for p in srcs if p.stem in wanted]
            if cfg.limit is not None:
                srcs = srcs[: cfg.limit]
            for src in srcs:
                tasks.append(EncodeTask(
                    raw_set=raw_set, level=level, crf=crf,
                    src=src, dst=out_dir / src.name, preset=cfg.preset,
                    threads=cfg.threads, src_frames=src_counts.get(src),
                ))
    return tasks


# ---------------------------------------------------------------------------
# Done markers
# ---------------------------------------------------------------------------

def done_marker(output_root: Path, level: str, raw_set: str) -> Path:
    return output_root / level / raw_set / ".done"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(cfg: Config) -> int:
    output_root = cfg.resolved_output_root()
    output_root.mkdir(parents=True, exist_ok=True)
    failed_log = output_root / "failed.log"

    tasks = build_tasks(cfg)
    logger.info("planned %d encode tasks across %d workers", len(tasks), cfg.workers)
    if not tasks:
        logger.warning("no tasks planned — nothing to do")
        return 0

    # failed.log reflects only the latest run: stale entries from a previous
    # run would over-count against the Gate 1 "0 unresolved entries" check.
    failed_log.unlink(missing_ok=True)

    counts = {"encoded": 0, "skipped": 0, "failed": 0}
    failures: list[dict] = []
    # Track per (level, set) whether every task succeeded -> write .done.
    set_level_keys = {(t.level, t.raw_set) for t in tasks}
    set_level_ok: dict[tuple[str, str], bool] = {k: True for k in set_level_keys}

    start = time.time()
    workers = max(1, min(cfg.workers, len(tasks)))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(process_task, t): t for t in tasks}
        for i, fut in enumerate(as_completed(futures), 1):
            res = fut.result()
            status = res["status"]
            counts[status] += 1
            key = (res["level"], res["set"])
            if status == "failed":
                set_level_ok[key] = False
                failures.append(res)
            if i % 200 == 0 or i == len(tasks):
                logger.info(
                    "progress %d/%d  encoded=%d skipped=%d failed=%d",
                    i, len(tasks), counts["encoded"], counts["skipped"],
                    counts["failed"],
                )

    # Write failures.
    if failures:
        with failed_log.open("a") as fh:
            for res in failures:
                fh.write(json.dumps(res) + "\n")
        logger.error("%d failures logged to %s", len(failures), failed_log)

    # Write .done markers for fully-successful (level, set) groups.
    # Only when no limit (a capped run is a partial subset, not a complete set).
    if cfg.limit is None:
        for (level, raw_set), ok in set_level_ok.items():
            if ok:
                marker = done_marker(output_root, level, raw_set)
                marker.parent.mkdir(parents=True, exist_ok=True)
                marker.write_text(
                    json.dumps({"level": level, "set": raw_set,
                                "completed": time.strftime("%Y-%m-%dT%H:%M:%S")})
                )

    elapsed = time.time() - start
    logger.info(
        "DONE in %.1fs — encoded=%d skipped=%d failed=%d (total %d)",
        elapsed, counts["encoded"], counts["skipped"], counts["failed"], len(tasks),
    )
    return 1 if failures else 0


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
