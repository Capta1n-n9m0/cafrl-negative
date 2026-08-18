"""Detect + track all faces on DFD target real videos (actors/, c23).

Reuses the SCRFD+ArcFace detection and online ArcFace tracking from
``reextract_tracks.py``. For every actor real take we write per-video:
  faces_v2/c23/actors/{real_stem}/tracks.json          (track summaries)
  faces_v2/c23/actors/{real_stem}/all_detections.json  (per-frame kps/bbox/track_id)

These feed diff-vote track selection (which identity was manipulated) and the
final landmark-reuse extraction. No crops are written here — only track metadata.

c23 is the highest-quality DFD compression (there is no c0); c40 is a
frame-identical re-encode, so c23 landmarks localise the same face in c40.

Sharding for 2-GPU parallelism: ``--num-shards 2 --shard {0,1}`` partitions the
real list by index. Resumable: a video with tracks.json is skipped.

Run (per GPU):
  conda run -n cv python detect_targets.py --gpu 0 --num-shards 2 --shard 0
  conda run -n cv python detect_targets.py --gpu 1 --num-shards 2 --shard 1
"""
from __future__ import annotations

import json
import logging
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # src/scripts on path
from index import build_index  # noqa: E402
from reextract_tracks import (  # noqa: E402
    TrackExtractionConfig, detect_all_faces_in_video, load_face_analysis,
    run_tracking, write_all_detections_json, write_tracks_json,
)

logger = logging.getLogger("dfd.detect")

REAL_DIR = Path("${HOME}/sdc/datasets/ffpp_original/original_sequences/actors/c23/videos")
OUT_ROOT = Path.home() / "sdb" / "datasets" / "ff++" / "faces_v2" / "c23" / "actors"


def parse_args(argv: list[str]) -> dict:
    opts = {"gpu": 0, "num_shards": 1, "shard": 0, "det_size": 1024, "limit": 0}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--gpu", "--num-shards", "--shard", "--det-size", "--limit"):
            opts[a.lstrip("-").replace("-", "_")] = int(argv[i + 1]); i += 2
        else:
            raise ValueError(f"unknown arg {a}")
    return opts


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                        datefmt="%H:%M:%S")
    opts = parse_args(sys.argv[1:])

    idx = build_index()
    reals = idx.all_reals
    reals = [r for n, r in enumerate(reals) if n % opts["num_shards"] == opts["shard"]]
    if opts["limit"]:
        reals = reals[:opts["limit"]]

    todo = [r for r in reals if not (OUT_ROOT / r / "tracks.json").exists()]
    logger.info("shard %d/%d: %d reals, %d to process, det_size=%d, gpu=%d",
                opts["shard"], opts["num_shards"], len(reals), len(todo),
                opts["det_size"], opts["gpu"])
    if not todo:
        logger.info("nothing to do"); return

    cfg = TrackExtractionConfig(gpu_id=opts["gpu"], det_size=opts["det_size"])
    app = load_face_analysis(cfg.gpu_id, cfg.det_size)

    t_start = time.monotonic()
    for n, stem in enumerate(todo, 1):
        vpath = REAL_DIR / f"{stem}.mp4"
        out_dir = OUT_ROOT / stem
        out_dir.mkdir(parents=True, exist_ok=True)
        try:
            t0 = time.monotonic()
            frame_dets, n_frames = detect_all_faces_in_video(vpath, app, cfg.det_thresh)
            tracks = run_tracking(frame_dets, cfg.cos_threshold, cfg.max_gap,
                                  cfg.emb_momentum, cfg.min_track_length)
            write_tracks_json(stem, vpath, n_frames, tracks, out_dir)
            write_all_detections_json(stem, n_frames, frame_dets, tracks, out_dir)
            dt = time.monotonic() - t0
            mean_faces = (sum(len(fd.detections) for fd in frame_dets)
                          / max(1, n_frames))
            logger.info("[%d/%d] %s: %d frames, %d tracks, %.2f faces/frame (%.1fs)",
                        n, len(todo), stem, n_frames, len(tracks), mean_faces, dt)
        except Exception as e:  # noqa: BLE001
            logger.error("[%d/%d] %s FAILED: %s", n, len(todo), stem, e, exc_info=True)
            (out_dir / "FAILED.txt").write_text(str(e))

    logger.info("shard %d done in %.1f min", opts["shard"],
                (time.monotonic() - t_start) / 60)


if __name__ == "__main__":
    main()
