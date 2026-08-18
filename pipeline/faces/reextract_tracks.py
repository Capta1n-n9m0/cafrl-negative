"""Re-extract faces from problematic multi-person FF++ videos with face tracking.

Detects ALL faces per frame (not just the largest), computes ArcFace embeddings,
clusters them into face tracks using online greedy cosine-similarity assignment,
and saves aligned face crops per track.

Target: 31 FF++ c0/youtube original videos where single-face extraction failed
due to face switching between people.
"""

from __future__ import annotations

import json
import logging
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from tqdm import tqdm

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class TrackExtractionConfig:
    gpu_id: int = 0
    output_root: str = str(Path.home() / "sdb" / "datasets" / "ff++" / "faces_v2")
    det_size: int = 640
    cos_threshold: float = 0.5
    min_track_length: int = 30
    output_size: int = 256
    det_thresh: float = 0.5
    max_gap: int = 60  # max frames a track can be dormant before considered ended
    emb_momentum: float = 0.9  # weight for existing track embedding in EMA update


# The 31 problematic video IDs
PROBLEM_VIDEO_IDS: list[str] = [
    "456", "257", "233", "420", "156", "869", "824", "953", "332", "474",
    "258", "356", "252", "345", "414", "016", "014", "281", "436", "216",
    "738", "823", "212", "217", "509", "253", "105", "908", "324", "038",
    "175",
]

SOURCE_VIDEO_DIR = Path("${HOME}/sdc/datasets/ffpp_original/original_sequences/youtube/c0/videos")


# ---------------------------------------------------------------------------
# Face alignment — similarity transform from 5-point landmarks
# ---------------------------------------------------------------------------

REFERENCE_LANDMARKS_256 = np.array([
    [89.0, 105.0],   # left eye
    [167.0, 105.0],  # right eye
    [128.0, 150.0],  # nose
    [96.0, 195.0],   # left mouth
    [160.0, 195.0],  # right mouth
], dtype=np.float32)


def estimate_similarity_transform(
    src: np.ndarray, dst: np.ndarray,
) -> np.ndarray:
    """Estimate 2x3 similarity transform matrix from point correspondences."""
    src_mean = src.mean(axis=0)
    dst_mean = dst.mean(axis=0)
    src_c = src - src_mean
    dst_c = dst - dst_mean

    denom = (src_c ** 2).sum()
    if denom < 1e-10:
        return np.eye(2, 3, dtype=np.float32)

    a = (dst_c[:, 0] * src_c[:, 0] + dst_c[:, 1] * src_c[:, 1]).sum() / denom
    b = (dst_c[:, 1] * src_c[:, 0] - dst_c[:, 0] * src_c[:, 1]).sum() / denom

    return np.array([
        [a, -b, dst_mean[0] - a * src_mean[0] + b * src_mean[1]],
        [b,  a, dst_mean[1] - b * src_mean[0] - a * src_mean[1]],
    ], dtype=np.float32)


def align_face(
    img: np.ndarray,
    landmarks: np.ndarray,
    output_size: int = 256,
) -> np.ndarray:
    """Align a face crop using similarity transform to reference landmarks."""
    ref = REFERENCE_LANDMARKS_256 * (output_size / 256.0)
    M = estimate_similarity_transform(landmarks, ref)
    return cv2.warpAffine(
        img, M, (output_size, output_size),
        borderMode=cv2.BORDER_REPLICATE,
    )


# ---------------------------------------------------------------------------
# Face detection with embeddings
# ---------------------------------------------------------------------------

@dataclass
class Detection:
    """Single face detection in one frame."""
    bbox: list[float]
    kps: list[list[float]]
    det_score: float
    embedding: np.ndarray  # 512-d ArcFace


@dataclass
class FrameDetections:
    """All face detections in a single frame."""
    frame_idx: int
    detections: list[Detection]


def load_face_analysis(gpu_id: int, det_size: int) -> Any:
    """Load insightface FaceAnalysis with detection + recognition."""
    import os
    os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)

    import warnings
    warnings.filterwarnings("ignore")

    from insightface.app import FaceAnalysis

    logger.info("Loading insightface model (SCRFD + ArcFace) on GPU %d...", gpu_id)
    app = FaceAnalysis(
        name="buffalo_l",
        providers=["CUDAExecutionProvider"],
        allowed_modules=["detection", "recognition"],
    )
    app.prepare(ctx_id=0, det_size=(det_size, det_size))
    logger.info("Model loaded successfully.")
    return app


def detect_all_faces_in_video(
    video_path: Path,
    app: Any,
    det_thresh: float = 0.5,
) -> tuple[list[FrameDetections], int]:
    """Decode video and detect all faces in every frame.

    Returns:
        Tuple of (list of FrameDetections, total_frame_count)
    """
    import decord
    decord.bridge.set_bridge("native")

    vr = decord.VideoReader(str(video_path), num_threads=1)
    n_frames = len(vr)
    all_frame_detections: list[FrameDetections] = []

    for frame_idx in range(n_frames):
        frame = vr[frame_idx].asnumpy()  # H x W x 3, RGB
        # insightface expects BGR
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        faces = app.get(frame_bgr)

        detections: list[Detection] = []
        for face in faces:
            if face.det_score < det_thresh:
                continue
            detections.append(Detection(
                bbox=face.bbox.tolist(),
                kps=face.kps.tolist(),
                det_score=float(face.det_score),
                embedding=face.embedding.copy(),
            ))

        all_frame_detections.append(FrameDetections(
            frame_idx=frame_idx,
            detections=detections,
        ))

    return all_frame_detections, n_frames


# ---------------------------------------------------------------------------
# Online greedy face tracking
# ---------------------------------------------------------------------------

@dataclass
class Track:
    """A face track across multiple frames."""
    track_id: int
    mean_embedding: np.ndarray  # normalized 512-d
    frame_indices: list[int]
    detections: list[Detection]  # corresponding detection per frame
    last_seen: int  # last frame index where this track was matched


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a < 1e-10 or norm_b < 1e-10:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def run_tracking(
    frame_detections: list[FrameDetections],
    cos_threshold: float,
    max_gap: int,
    emb_momentum: float,
    min_track_length: int,
) -> list[Track]:
    """Online greedy tracking using cosine similarity of ArcFace embeddings.

    Args:
        frame_detections: Per-frame detection results
        cos_threshold: Minimum cosine similarity to match a detection to a track
        max_gap: Maximum frames a track can go unmatched before being finalized
        emb_momentum: Weight for existing embedding in EMA update
        min_track_length: Minimum frames for a track to be kept

    Returns:
        List of Track objects (filtered by min_track_length)
    """
    active_tracks: list[Track] = []
    finished_tracks: list[Track] = []
    next_track_id: int = 0

    for frame_det in frame_detections:
        frame_idx = frame_det.frame_idx
        detections = frame_det.detections

        # Move dormant tracks to finished
        still_active: list[Track] = []
        for track in active_tracks:
            if frame_idx - track.last_seen > max_gap:
                finished_tracks.append(track)
            else:
                still_active.append(track)
        active_tracks = still_active

        if not detections:
            continue

        if not active_tracks:
            # All detections start new tracks
            for det in detections:
                emb = det.embedding.copy()
                norm = np.linalg.norm(emb)
                if norm > 1e-10:
                    emb = emb / norm
                active_tracks.append(Track(
                    track_id=next_track_id,
                    mean_embedding=emb,
                    frame_indices=[frame_idx],
                    detections=[det],
                    last_seen=frame_idx,
                ))
                next_track_id += 1
            continue

        # Compute similarity matrix: [num_detections x num_tracks]
        num_det = len(detections)
        num_tracks = len(active_tracks)
        sim_matrix = np.zeros((num_det, num_tracks), dtype=np.float32)

        for di, det in enumerate(detections):
            for ti, track in enumerate(active_tracks):
                sim_matrix[di, ti] = cosine_similarity(det.embedding, track.mean_embedding)

        # Greedy assignment: best match first
        matched_dets: set[int] = set()
        matched_tracks: set[int] = set()

        # Flatten and sort by similarity (descending)
        flat_indices = np.argsort(sim_matrix.ravel())[::-1]

        for flat_idx in flat_indices:
            di = int(flat_idx // num_tracks)
            ti = int(flat_idx % num_tracks)

            if di in matched_dets or ti in matched_tracks:
                continue

            sim = sim_matrix[di, ti]
            if sim < cos_threshold:
                break  # all remaining are below threshold

            # Match detection di to track ti
            det = detections[di]
            track = active_tracks[ti]

            # Update track embedding with EMA
            new_emb = emb_momentum * track.mean_embedding + (1.0 - emb_momentum) * det.embedding
            norm = np.linalg.norm(new_emb)
            if norm > 1e-10:
                new_emb = new_emb / norm
            track.mean_embedding = new_emb

            track.frame_indices.append(frame_idx)
            track.detections.append(det)
            track.last_seen = frame_idx

            matched_dets.add(di)
            matched_tracks.add(ti)

        # Unmatched detections with sufficient confidence start new tracks
        for di in range(num_det):
            if di in matched_dets:
                continue
            det = detections[di]
            if det.det_score < 0.5:
                continue
            emb = det.embedding.copy()
            norm = np.linalg.norm(emb)
            if norm > 1e-10:
                emb = emb / norm
            active_tracks.append(Track(
                track_id=next_track_id,
                mean_embedding=emb,
                frame_indices=[frame_idx],
                detections=[det],
                last_seen=frame_idx,
            ))
            next_track_id += 1

    # Move all remaining active tracks to finished
    finished_tracks.extend(active_tracks)

    # Filter by minimum track length
    valid_tracks = [t for t in finished_tracks if len(t.frame_indices) >= min_track_length]

    # Sort by track length (longest first) and re-assign IDs
    valid_tracks.sort(key=lambda t: len(t.frame_indices), reverse=True)
    for new_id, track in enumerate(valid_tracks):
        track.track_id = new_id

    return valid_tracks


# ---------------------------------------------------------------------------
# Saving results
# ---------------------------------------------------------------------------

def save_aligned_crops(
    video_path: Path,
    tracks: list[Track],
    output_dir: Path,
    output_size: int,
) -> None:
    """Re-decode video and save aligned face crops for each track."""
    import decord
    decord.bridge.set_bridge("native")

    vr = decord.VideoReader(str(video_path), num_threads=1)

    for track in tracks:
        track_dir = output_dir / f"track_{track.track_id:02d}"
        track_dir.mkdir(parents=True, exist_ok=True)

        for frame_idx, det in zip(track.frame_indices, track.detections):
            frame = vr[frame_idx].asnumpy()  # RGB
            landmarks = np.array(det.kps, dtype=np.float32)
            aligned = align_face(frame, landmarks, output_size)
            # Convert RGB to BGR for cv2.imwrite
            aligned_bgr = cv2.cvtColor(aligned, cv2.COLOR_RGB2BGR)
            out_path = track_dir / f"{frame_idx:04d}.png"
            cv2.imwrite(str(out_path), aligned_bgr)


def write_tracks_json(
    video_id: str,
    video_path: Path,
    num_frames_total: int,
    tracks: list[Track],
    output_dir: Path,
) -> None:
    """Write tracks.json summary."""
    tracks_data: list[dict[str, Any]] = []
    for track in tracks:
        # Compute mean confidence
        scores = [d.det_score for d in track.detections]
        mean_conf = float(np.mean(scores))

        # Compute mean face size (width, height from bbox)
        sizes = []
        for d in track.detections:
            w = d.bbox[2] - d.bbox[0]
            h = d.bbox[3] - d.bbox[1]
            sizes.append([w, h])
        mean_size = [float(np.mean([s[0] for s in sizes])), float(np.mean([s[1] for s in sizes]))]

        # Frame range
        frame_range = [track.frame_indices[0], track.frame_indices[-1]]

        # Sample frames (up to 6 evenly spaced)
        n = len(track.frame_indices)
        if n <= 6:
            sample_frames = track.frame_indices[:]
        else:
            step = n // 6
            sample_frames = [track.frame_indices[i * step] for i in range(6)]

        tracks_data.append({
            "track_id": track.track_id,
            "num_frames": len(track.frame_indices),
            "mean_confidence": round(mean_conf, 4),
            "mean_face_size": [round(mean_size[0], 1), round(mean_size[1], 1)],
            "frame_range": frame_range,
            "sample_frames": sample_frames,
        })

    summary = {
        "video_id": video_id,
        "source_path": str(video_path),
        "num_frames_total": num_frames_total,
        "num_tracks": len(tracks),
        "tracks": tracks_data,
    }

    out_path = output_dir / "tracks.json"
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)


def write_all_detections_json(
    video_id: str,
    num_frames_total: int,
    frame_detections: list[FrameDetections],
    tracks: list[Track],
    output_dir: Path,
) -> None:
    """Write all_detections.json with per-frame detection data and track assignments."""
    # Build mapping: (frame_idx, detection_index_in_frame) -> track_id
    # We need to figure out which detection in the original frame_detections
    # corresponds to which track. We do this by matching bbox coordinates.
    #
    # Actually, we can build a mapping from (frame_idx, bbox_tuple) -> track_id
    track_assignment: dict[tuple[int, tuple[float, ...]], int] = {}
    for track in tracks:
        for frame_idx, det in zip(track.frame_indices, track.detections):
            bbox_key = tuple(round(x, 2) for x in det.bbox)
            track_assignment[(frame_idx, bbox_key)] = track.track_id

    frames_data: dict[str, list[dict[str, Any]]] = {}
    for frame_det in frame_detections:
        frame_idx = frame_det.frame_idx
        if not frame_det.detections:
            continue  # skip empty frames to keep file size reasonable

        dets_json: list[dict[str, Any]] = []
        for det in frame_det.detections:
            bbox_key = tuple(round(x, 2) for x in det.bbox)
            tid = track_assignment.get((frame_idx, bbox_key), -1)
            dets_json.append({
                "bbox": [round(x, 2) for x in det.bbox],
                "kps": [[round(x, 2) for x in pt] for pt in det.kps],
                "det_score": round(det.det_score, 4),
                "track_id": tid,
            })
        frames_data[str(frame_idx)] = dets_json

    result = {
        "video_id": video_id,
        "num_frames": num_frames_total,
        "frames": frames_data,
    }

    out_path = output_dir / "all_detections.json"
    with open(out_path, "w") as f:
        json.dump(result, f)


# ---------------------------------------------------------------------------
# Main processing loop
# ---------------------------------------------------------------------------

def process_video(
    video_id: str,
    video_path: Path,
    output_dir: Path,
    app: Any,
    cfg: TrackExtractionConfig,
) -> dict[str, Any]:
    """Process a single video: detect, track, align, save.

    Returns:
        Dictionary with processing stats.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Phase 1: Detection
    logger.info("  Detecting faces in %s (%s)...", video_id, video_path.name)
    t0 = time.time()
    frame_detections, num_frames = detect_all_faces_in_video(
        video_path, app, det_thresh=cfg.det_thresh,
    )
    t_detect = time.time() - t0

    # Count total detections
    total_dets = sum(len(fd.detections) for fd in frame_detections)
    frames_with_faces = sum(1 for fd in frame_detections if fd.detections)
    logger.info(
        "  Detection complete: %d frames, %d total detections, %d frames with faces (%.1fs)",
        num_frames, total_dets, frames_with_faces, t_detect,
    )

    # Handle edge case: no faces detected at all
    if total_dets == 0:
        logger.warning("  No faces detected in video %s, writing empty results.", video_id)
        write_tracks_json(video_id, video_path, num_frames, [], output_dir)
        write_all_detections_json(video_id, num_frames, frame_detections, [], output_dir)
        return {
            "video_id": video_id,
            "num_frames": num_frames,
            "total_detections": 0,
            "num_tracks": 0,
            "time_detect": t_detect,
            "time_track": 0.0,
            "time_save": 0.0,
        }

    # Phase 2: Tracking
    logger.info("  Running face tracking...")
    t0 = time.time()
    tracks = run_tracking(
        frame_detections,
        cos_threshold=cfg.cos_threshold,
        max_gap=cfg.max_gap,
        emb_momentum=cfg.emb_momentum,
        min_track_length=cfg.min_track_length,
    )
    t_track = time.time() - t0
    logger.info("  Tracking complete: %d valid tracks (%.1fs)", len(tracks), t_track)

    for track in tracks:
        logger.info(
            "    Track %d: %d frames, range [%d, %d]",
            track.track_id, len(track.frame_indices),
            track.frame_indices[0], track.frame_indices[-1],
        )

    # Phase 3: Save aligned crops
    logger.info("  Saving aligned face crops...")
    t0 = time.time()
    save_aligned_crops(video_path, tracks, output_dir, cfg.output_size)
    t_save = time.time() - t0
    logger.info("  Crops saved (%.1fs)", t_save)

    # Phase 4: Write metadata
    write_tracks_json(video_id, video_path, num_frames, tracks, output_dir)
    write_all_detections_json(video_id, num_frames, frame_detections, tracks, output_dir)

    return {
        "video_id": video_id,
        "num_frames": num_frames,
        "total_detections": total_dets,
        "num_tracks": len(tracks),
        "time_detect": t_detect,
        "time_track": t_track,
        "time_save": t_save,
    }


def parse_args() -> TrackExtractionConfig:
    """Parse CLI arguments from sys.argv."""
    cfg = TrackExtractionConfig()

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--gpu" and i + 1 < len(sys.argv):
            cfg.gpu_id = int(sys.argv[i + 1])
            i += 2
        elif arg == "--output-root" and i + 1 < len(sys.argv):
            cfg.output_root = sys.argv[i + 1]
            i += 2
        elif arg == "--det-size" and i + 1 < len(sys.argv):
            cfg.det_size = int(sys.argv[i + 1])
            i += 2
        elif arg == "--cos-threshold" and i + 1 < len(sys.argv):
            cfg.cos_threshold = float(sys.argv[i + 1])
            i += 2
        elif arg == "--min-track-length" and i + 1 < len(sys.argv):
            cfg.min_track_length = int(sys.argv[i + 1])
            i += 2
        else:
            logger.warning("Unknown argument: %s", arg)
            i += 1

    return cfg


def main() -> None:
    """Main entry point."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    cfg = parse_args()

    logger.info("=" * 70)
    logger.info("Face Re-extraction with Tracking")
    logger.info("=" * 70)
    logger.info("GPU: %d", cfg.gpu_id)
    logger.info("Output root: %s", cfg.output_root)
    logger.info("Detection size: %d", cfg.det_size)
    logger.info("Cosine threshold: %.2f", cfg.cos_threshold)
    logger.info("Min track length: %d", cfg.min_track_length)
    logger.info("Videos to process: %d", len(PROBLEM_VIDEO_IDS))
    logger.info("=" * 70)

    # Validate source videos exist
    missing_videos: list[str] = []
    video_paths: dict[str, Path] = {}
    for vid in PROBLEM_VIDEO_IDS:
        vpath = SOURCE_VIDEO_DIR / f"{vid}.mp4"
        if not vpath.exists():
            missing_videos.append(vid)
        else:
            video_paths[vid] = vpath

    if missing_videos:
        logger.error("Missing source videos: %s", missing_videos)
        logger.error("Cannot proceed with missing videos. Check paths.")
        sys.exit(1)

    # Check which videos already have tracks.json (resume support)
    output_base = Path(cfg.output_root) / "c0" / "real"
    videos_to_process: list[str] = []
    for vid in PROBLEM_VIDEO_IDS:
        out_dir = output_base / vid
        tracks_file = out_dir / "tracks.json"
        if tracks_file.exists():
            logger.info("Skipping %s (tracks.json already exists)", vid)
        else:
            videos_to_process.append(vid)

    if not videos_to_process:
        logger.info("All videos already processed. Nothing to do.")
        return

    logger.info("%d videos to process (skipped %d already done)",
                len(videos_to_process), len(PROBLEM_VIDEO_IDS) - len(videos_to_process))

    # Load model
    app = load_face_analysis(cfg.gpu_id, cfg.det_size)

    # Process videos
    results: list[dict[str, Any]] = []
    total_start = time.time()

    for vid in tqdm(videos_to_process, desc="Processing videos", unit="video"):
        vpath = video_paths[vid]
        out_dir = output_base / vid

        try:
            stats = process_video(vid, vpath, out_dir, app, cfg)
            results.append(stats)
        except Exception as e:
            logger.error("FAILED processing video %s: %s", vid, e, exc_info=True)
            results.append({
                "video_id": vid,
                "error": str(e),
            })

    total_time = time.time() - total_start

    # Summary
    logger.info("=" * 70)
    logger.info("COMPLETE")
    logger.info("=" * 70)
    successful = [r for r in results if "error" not in r]
    failed = [r for r in results if "error" in r]

    logger.info("Processed: %d/%d videos in %.1f minutes",
                len(successful), len(videos_to_process), total_time / 60)
    if failed:
        logger.error("Failed: %d videos: %s", len(failed), [r["video_id"] for r in failed])

    total_tracks = sum(r.get("num_tracks", 0) for r in successful)
    logger.info("Total tracks created: %d", total_tracks)

    avg_tracks = total_tracks / max(len(successful), 1)
    logger.info("Average tracks per video: %.1f", avg_tracks)

    # Write summary to output
    summary_path = output_base / "reextract_summary.json"
    summary = {
        "config": {
            "gpu_id": cfg.gpu_id,
            "det_size": cfg.det_size,
            "cos_threshold": cfg.cos_threshold,
            "min_track_length": cfg.min_track_length,
            "output_size": cfg.output_size,
        },
        "total_time_seconds": round(total_time, 1),
        "num_processed": len(successful),
        "num_failed": len(failed),
        "total_tracks": total_tracks,
        "results": results,
    }
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    logger.info("Summary written to %s", summary_path)


if __name__ == "__main__":
    main()
