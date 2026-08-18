"""Face extraction pipeline for deepfake detection datasets.

Extracts aligned face crops from video datasets using SCRFD face detection.
Architecture: decode workers feed frame batches via queue to GPU detection workers,
main thread collects results and does crop/align/save.
"""

from __future__ import annotations

import json
import logging
import multiprocessing as mp
import shutil
import sys
import time
import traceback
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from tqdm import tqdm

from src.data.face_align import (  # noqa: F401 (re-exported for compatibility)
    REFERENCE_LANDMARKS_256,
    align_face,
    estimate_similarity_transform,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class ExtractionConfig:
    dataset: str = "ff++"
    dataset_root: str = "${HOME}/sdc/datasets/ffpp_original"
    output_root: str = str(Path.home() / "sdb" / "datasets")
    compression: str = "c0"
    methods: list[str] = field(default_factory=lambda: ["youtube"])
    output_size: int = 256
    scale_factor: float = 1.3
    det_size: int = 640
    det_thresh: float = 0.5
    batch_size: int = 32
    num_decode_workers: int = 4
    gpus: list[int] = field(default_factory=lambda: [0, 1])
    failed_log: str = "failed_videos.jsonl"


# ---------------------------------------------------------------------------
# FF++ dataset adapter
# ---------------------------------------------------------------------------

FFPP_REAL_METHODS = {"youtube", "actors"}
FFPP_FAKE_METHODS = {
    "Deepfakes", "Face2Face", "FaceSwap", "NeuralTextures",
    "FaceShifter", "DeepFakeDetection",
}

CELEBDF_SUBDIRS = {
    "Celeb-real": 0,
    "Celeb-synthesis": 1,
    "YouTube-real": 0,
}


@dataclass
class VideoTask:
    video_path: Path
    video_id: str
    output_dir: Path
    label: int
    method: str
    compression: str


def discover_ffpp_videos(cfg: ExtractionConfig) -> list[VideoTask]:
    root = Path(cfg.dataset_root)
    tasks: list[VideoTask] = []
    for method in cfg.methods:
        if method in FFPP_REAL_METHODS:
            video_dir = root / "original_sequences" / method / cfg.compression / "videos"
            label = 0
            out_method = "real"
        elif method in FFPP_FAKE_METHODS:
            video_dir = root / "manipulated_sequences" / method / cfg.compression / "videos"
            label = 1
            out_method = method
        else:
            raise ValueError(f"Unknown FF++ method: {method}")

        if not video_dir.is_dir():
            logger.warning("Video directory not found: %s", video_dir)
            continue

        for vpath in sorted(video_dir.glob("*.mp4")):
            video_id = vpath.stem
            out_dir = (
                Path(cfg.output_root) / "ff++" / "faces"
                / cfg.compression / out_method / video_id
            )
            tasks.append(VideoTask(
                video_path=vpath,
                video_id=video_id,
                output_dir=out_dir,
                label=label,
                method=method,
                compression=cfg.compression,
            ))
    return tasks


def discover_celebdf_videos(cfg: ExtractionConfig) -> list[VideoTask]:
    root = Path(cfg.dataset_root)
    tasks: list[VideoTask] = []
    version = "v2" if "v2" in str(root) else "v1"

    for subdir, label in CELEBDF_SUBDIRS.items():
        video_dir = root / subdir
        if not video_dir.is_dir():
            logger.warning("Directory not found: %s", video_dir)
            continue

        out_category = "real" if label == 0 else "fake"
        for vpath in sorted(video_dir.glob("*.mp4")):
            video_id = vpath.stem
            out_dir = (
                Path(cfg.output_root) / f"celeb-df-{version}" / "faces"
                / out_category / video_id
            )
            tasks.append(VideoTask(
                video_path=vpath,
                video_id=video_id,
                output_dir=out_dir,
                label=label,
                method=subdir,
                compression="raw",
            ))
    return tasks


def discover_videos(cfg: ExtractionConfig) -> list[VideoTask]:
    if cfg.dataset == "ff++":
        return discover_ffpp_videos(cfg)
    if cfg.dataset == "celeb-df":
        return discover_celebdf_videos(cfg)
    raise ValueError(f"Unsupported dataset: {cfg.dataset}")


# ---------------------------------------------------------------------------
# Face alignment — moved to src/data/face_align.py (imported above, re-exported
# for any code that still imports it from this module).
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# GPU face detection worker (runs in subprocess, one per GPU)
# ---------------------------------------------------------------------------

def gpu_worker_fn(
    gpu_id: int,
    input_queue: mp.Queue,
    output_queue: mp.Queue,
    det_size: int,
    log_file: str | None = None,
) -> None:
    """Persistent GPU process: takes (batch_id, frames) from queue, returns detections."""
    import os
    import warnings
    warnings.filterwarnings("ignore")

    os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)

    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stderr)]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    logging.basicConfig(
        level=logging.INFO,
        format=f"%(asctime)s %(levelname)s GPU-{gpu_id}: %(message)s",
        handlers=handlers,
        force=True,
    )
    gpu_logger = logging.getLogger(f"gpu_{gpu_id}")

    from insightface.app import FaceAnalysis
    gpu_logger.info("Loading SCRFD model on GPU %d...", gpu_id)
    app = FaceAnalysis(
        name="buffalo_l",
        providers=["CUDAExecutionProvider"],
        allowed_modules=["detection"],
    )
    # ctx_id=0 because CUDA_VISIBLE_DEVICES remaps to device 0
    app.prepare(ctx_id=0, det_size=(det_size, det_size))
    gpu_logger.info("SCRFD model loaded on GPU %d", gpu_id)

    batches_processed = 0
    while True:
        item = input_queue.get()
        if item is None:
            gpu_logger.info("GPU %d shutting down after %d batches", gpu_id, batches_processed)
            break

        batch_id, frames = item
        try:
            results: list[dict[str, Any] | None] = []
            for frame in frames:
                faces = app.get(frame)
                if not faces:
                    results.append(None)
                    continue
                largest = max(
                    faces,
                    key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]),
                )
                results.append({
                    "bbox": largest.bbox.tolist(),
                    "kps": largest.kps.tolist(),
                    "det_score": float(largest.det_score),
                    "num_faces": len(faces),
                })
            output_queue.put((batch_id, results))
            batches_processed += 1
        except Exception as e:
            gpu_logger.error("GPU %d error on batch %d: %s\n%s", gpu_id, batch_id, e, traceback.format_exc())
            output_queue.put((batch_id, [None] * len(frames)))


# ---------------------------------------------------------------------------
# Video decoding
# ---------------------------------------------------------------------------

def decode_video(video_path: Path, batch_size: int) -> list[tuple[list[int], np.ndarray]]:
    """Decode all frames from a video, returning batches of (indices, frames_array)."""
    import decord
    decord.bridge.set_bridge("native")

    vr = decord.VideoReader(str(video_path), num_threads=1)
    n_frames = len(vr)
    batches = []

    for start in range(0, n_frames, batch_size):
        end = min(start + batch_size, n_frames)
        indices = list(range(start, end))
        frames = vr.get_batch(indices).asnumpy()
        batches.append((indices, frames))

    return batches


# ---------------------------------------------------------------------------
# Metadata & logging
# ---------------------------------------------------------------------------

def write_meta_json(
    task: VideoTask,
    face_entries: list[dict[str, Any]],
    num_frames_total: int,
    scale_factor: float,
    output_size: int,
    dataset: str = "ff++",
) -> None:
    meta = {
        "video_id": task.video_id,
        "source_path": str(task.video_path),
        "dataset": dataset,
        "label": task.label,
        "manipulation": task.method if task.label == 1 else None,
        "compression": task.compression,
        "num_frames_total": num_frames_total,
        "num_frames_extracted": len(face_entries),
        "faces": face_entries,
        "processing": {
            "detector": "scrfd_10g",
            "scale_factor": scale_factor,
            "output_size": output_size,
            "alignment": "similarity_transform",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }
    with open(task.output_dir / "meta.json", "w") as f:
        json.dump(meta, f)


def log_failure(log_path: Path, video_id: str, source: str, error: str) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(json.dumps({
            "video_id": video_id,
            "source": source,
            "error": error,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }) + "\n")


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run_pipeline(cfg: ExtractionConfig) -> None:
    all_tasks = discover_videos(cfg)
    logger.info("Discovered %d videos total", len(all_tasks))

    tasks: list[VideoTask] = []
    skipped = 0
    for t in all_tasks:
        if (t.output_dir / ".done").exists():
            skipped += 1
        else:
            tasks.append(t)

    logger.info("Skipping %d already-completed, %d to process", skipped, len(tasks))
    if not tasks:
        logger.info("Nothing to do.")
        return

    dataset_dir = cfg.dataset if cfg.dataset == "ff++" else cfg.dataset
    if cfg.dataset == "celeb-df":
        version = "v2" if "v2" in cfg.dataset_root else "v1"
        dataset_dir = f"celeb-df-{version}"

    failed_log_path = Path(cfg.output_root) / dataset_dir / cfg.failed_log

    log_dir = Path(cfg.output_root) / dataset_dir
    log_dir.mkdir(parents=True, exist_ok=True)
    tag = cfg.compression if cfg.dataset == "ff++" else "raw"
    log_file_path = str(log_dir / f"extraction_{tag}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    # Start GPU detection workers (persistent for the whole run)
    det_input: mp.Queue = mp.Queue(maxsize=len(cfg.gpus) * 8)
    det_output: mp.Queue = mp.Queue()

    gpu_procs = []
    for gpu_id in cfg.gpus:
        p = mp.Process(
            target=gpu_worker_fn,
            args=(gpu_id, det_input, det_output, cfg.det_size, log_file_path),
            daemon=True,
        )
        p.start()
        logger.info("Started GPU worker on GPU %d (PID %d)", gpu_id, p.pid)
        gpu_procs.append(p)

    succeeded = 0
    failed = 0
    total_frames_processed = 0
    pipeline_start = time.monotonic()
    pbar = tqdm(total=len(tasks), desc="Extracting faces", unit="video")

    for task in tasks:
        video_start = time.monotonic()

        # Decode in main thread (decord is not thread-safe)
        try:
            batches = decode_video(task.video_path, cfg.batch_size)
        except Exception as e:
            logger.warning("FAIL [%s] decode error: %s", task.video_id, e)
            log_failure(failed_log_path, task.video_id, str(task.video_path), f"decode: {e}")
            failed += 1
            pbar.update(1)
            continue

        if not batches:
            logger.warning("FAIL [%s] no frames decoded", task.video_id)
            log_failure(failed_log_path, task.video_id, str(task.video_path), "no frames")
            failed += 1
            pbar.update(1)
            continue

        n_batches = len(batches)
        num_frames_total = sum(len(idx) for idx, _ in batches)

        # Submit batches to GPU
        t_det_start = time.monotonic()
        for batch_idx, (indices, frames) in enumerate(batches):
            det_input.put((batch_idx, frames))

        # Collect detection results
        det_results: dict[int, list[dict | None]] = {}
        for _ in range(n_batches):
            batch_id, dets = det_output.get()
            det_results[batch_id] = dets
        t_det_elapsed = time.monotonic() - t_det_start

        # Align, crop, save
        task.output_dir.mkdir(parents=True, exist_ok=True)
        face_entries: list[dict[str, Any]] = []

        try:
            t_save_start = time.monotonic()
            for batch_idx in range(n_batches):
                indices, frames = batches[batch_idx]
                dets = det_results[batch_idx]

                for i, (frame_idx, det) in enumerate(zip(indices, dets)):
                    if det is None:
                        continue

                    kps = np.array(det["kps"], dtype=np.float32)
                    aligned = align_face(frames[i], kps, cfg.output_size)

                    filename = f"{frame_idx:04d}.png"
                    cv2.imwrite(
                        str(task.output_dir / filename),
                        cv2.cvtColor(aligned, cv2.COLOR_RGB2BGR),
                    )

                    face_entries.append({
                        "frame_idx": frame_idx,
                        "filename": filename,
                        "bbox": det["bbox"],
                        "landmarks_5pt": det["kps"],
                        "confidence": det["det_score"],
                        "original_face_size": [
                            det["bbox"][2] - det["bbox"][0],
                            det["bbox"][3] - det["bbox"][1],
                        ],
                        "num_faces_detected": det["num_faces"],
                    })
            t_save_elapsed = time.monotonic() - t_save_start
        except Exception as e:
            logger.error("FAIL [%s] crop/save: %s\n%s", task.video_id, e, traceback.format_exc())
            log_failure(failed_log_path, task.video_id, str(task.video_path), f"crop/save: {e}")
            if task.output_dir.exists():
                shutil.rmtree(task.output_dir)
            failed += 1
            pbar.update(1)
            continue

        write_meta_json(task, face_entries, num_frames_total, cfg.scale_factor, cfg.output_size, dataset=cfg.dataset)
        (task.output_dir / ".done").touch()
        succeeded += 1
        total_frames_processed += num_frames_total
        video_elapsed = time.monotonic() - video_start

        # Per-video log (every video)
        logger.info(
            "OK [%s] %d/%d frames | det=%.1fs save=%.1fs total=%.1fs",
            task.video_id, len(face_entries), num_frames_total,
            t_det_elapsed, t_save_elapsed, video_elapsed,
        )

        # Summary every 50 videos
        done_count = succeeded + failed
        if done_count % 50 == 0:
            elapsed = time.monotonic() - pipeline_start
            rate = succeeded / elapsed * 60 if elapsed > 0 else 0
            remaining = (len(tasks) - done_count) / rate if rate > 0 else 0
            logger.info(
                "PROGRESS %d/%d done (%d ok, %d fail) | %.1f vid/min | ~%.0f min remaining | %d frames total",
                done_count, len(tasks), succeeded, failed, rate, remaining, total_frames_processed,
            )

        pbar.update(1)

    pbar.close()

    for _ in gpu_procs:
        det_input.put(None)
    for p in gpu_procs:
        p.join(timeout=30)

    elapsed = time.monotonic() - pipeline_start
    logger.info(
        "DONE: %d succeeded, %d failed out of %d | %.1f min | %d frames | %.1f vid/min",
        succeeded, failed, len(tasks), elapsed / 60, total_frames_processed,
        succeeded / elapsed * 60 if elapsed > 0 else 0,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: list[str]) -> ExtractionConfig:
    cfg = ExtractionConfig()
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--dataset":
            cfg.dataset = argv[i + 1]; i += 2
        elif arg == "--dataset-root":
            cfg.dataset_root = argv[i + 1]; i += 2
        elif arg == "--output-root":
            cfg.output_root = argv[i + 1]; i += 2
        elif arg == "--compression":
            cfg.compression = argv[i + 1]; i += 2
        elif arg == "--methods":
            cfg.methods = argv[i + 1:]; break
        elif arg == "--output-size":
            cfg.output_size = int(argv[i + 1]); i += 2
        elif arg == "--scale-factor":
            cfg.scale_factor = float(argv[i + 1]); i += 2
        elif arg == "--det-size":
            cfg.det_size = int(argv[i + 1]); i += 2
        elif arg == "--det-thresh":
            cfg.det_thresh = float(argv[i + 1]); i += 2
        elif arg == "--batch-size":
            cfg.batch_size = int(argv[i + 1]); i += 2
        elif arg == "--num-workers":
            cfg.num_decode_workers = int(argv[i + 1]); i += 2
        elif arg == "--gpus":
            cfg.gpus = [int(g) for g in argv[i + 1].split(",")]; i += 2
        elif arg == "--failed-log":
            cfg.failed_log = argv[i + 1]; i += 2
        else:
            raise ValueError(f"Unknown argument: {arg}")
    return cfg


def main() -> None:
    mp.set_start_method("spawn", force=True)
    cfg = parse_args(sys.argv[1:])

    if cfg.dataset == "celeb-df":
        version = "v2" if "v2" in cfg.dataset_root else "v1"
        main_log_dir = Path(cfg.output_root) / f"celeb-df-{version}"
        tag = "raw"
    else:
        main_log_dir = Path(cfg.output_root) / "ff++"
        tag = cfg.compression
    main_log_dir.mkdir(parents=True, exist_ok=True)
    log_file = main_log_dir / f"extraction_{tag}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.StreamHandler(sys.stderr),
            logging.FileHandler(log_file),
        ],
    )
    logger.info("Config: %s", cfg)
    logger.info("Log file: %s", log_file)

    try:
        run_pipeline(cfg)
    except Exception as e:
        logger.error("Pipeline crashed: %s\n%s", e, traceback.format_exc())
        raise


if __name__ == "__main__":
    main()
