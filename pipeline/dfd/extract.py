"""Extract DFD face crops using the selected target track + DTW alignment.

For each (target, scene) group:
  * REAL take: crop the selected track's face per frame (landmarks from
    all_detections.json) at c23 and c40 (frame-identical re-encodes).
  * Each FAKE built on it: DTW-align the fake to the target (t(i)), then crop
    fake frame i using the target's selected-track landmark at frame t(i). The
    fake reuses the target's frames/pose outside the swapped face, so the reused
    landmark localises the manipulated face (same guarantee the FF++ core fix
    relied on, generalised from i<->i to i<->t(i)).

Output mirrors extract_faces.py / propagate_tracks.py:
  faces/{c23,c40}/actors/{real_stem}/            (label 0)
  faces/{c23,c40}/DeepFakeDetection/{fake_stem}/ (label 1, replaces old crops)
Each dir gets per-frame 256x256 PNGs, meta.json, and a .done marker.

The old largest-face fake extraction is moved to a backup tree (default on sdc
to fit disk) before replacement. Reversible and idempotent: already-track_fixed
units are skipped unless --force.

Run:
  conda run -n cv python extract.py --units real            # all reals
  conda run -n cv python extract.py --units fake --targets multi --workers 8
  conda run -n cv python extract.py --units both --workers 8
"""
from __future__ import annotations

import json
import logging
import shutil
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from align import align, fingerprints  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from index import build_index  # noqa: E402
from reextract_tracks import align_face  # noqa: E402

logger = logging.getLogger("dfd.extract")

ACTORS_DIR = Path("${HOME}/sdc/datasets/ffpp_original/original_sequences/actors")
FAKE_VID_DIR = Path("${HOME}/sdc/datasets/ffpp_original/manipulated_sequences/DeepFakeDetection")
TRACKS_ROOT = Path.home() / "sdb" / "datasets" / "ff++" / "faces_v2" / "c23" / "actors"
FACES_ROOT = Path.home() / "sdb" / "datasets" / "ff++" / "faces"
# Backup on sdc (cold) because sdb cannot hold old + new DFD fakes at once.
BACKUP_ROOT = Path("${HOME}/sdc/datasets/dfd_singleface_backup")


@dataclass
class Config:
    units: str = "both"          # real | fake | both
    targets: str = "all"         # all | multi (which target groups to process)
    compressions: list[str] = field(default_factory=lambda: ["c23", "c40"])
    output_size: int = 256
    decode_batch: int = 64
    workers: int = 1
    force: bool = False
    dry_run: bool = False
    limit: int = 0
    good_align: float = 0.05     # warn if a fake's mean align cost exceeds this


# --------------------------------------------------------------------------
# Selected-track landmark resolution (shared with propagation semantics)
# --------------------------------------------------------------------------

def gather_selected_frames(all_detections: dict[str, Any],
                           selected: list[int]) -> dict[int, dict[str, Any]]:
    """target frame_idx -> chosen detection (highest score among selected tracks)."""
    sel = set(selected)
    out: dict[int, dict[str, Any]] = {}
    for fstr, dets in all_detections["frames"].items():
        cands = [d for d in dets if d["track_id"] in sel]
        if cands:
            out[int(fstr)] = max(cands, key=lambda d: d["det_score"])
    return dict(sorted(out.items()))


# --------------------------------------------------------------------------
# Crop writing
# --------------------------------------------------------------------------

def write_crops(video_path: Path, frame_to_det: dict[int, dict[str, Any]],
                staging: Path, cfg: Config, meta_base: dict[str, Any]) -> int:
    """Decode video, align each listed frame with its detection's landmarks, write."""
    import decord
    decord.bridge.set_bridge("native")

    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True, exist_ok=True)

    vr = decord.VideoReader(str(video_path), num_threads=1)
    n = len(vr)
    indices = sorted(f for f in frame_to_det if f < n)

    faces: list[dict[str, Any]] = []
    for start in range(0, len(indices), cfg.decode_batch):
        chunk = indices[start:start + cfg.decode_batch]
        frames = vr.get_batch(chunk).asnumpy()           # RGB
        for j, fidx in enumerate(chunk):
            det = frame_to_det[fidx]
            kps = np.array(det["kps"], dtype=np.float32)
            aligned = align_face(frames[j], kps, cfg.output_size)
            fn = f"{fidx:04d}.png"
            cv2.imwrite(str(staging / fn), cv2.cvtColor(aligned, cv2.COLOR_RGB2BGR))
            bbox = det["bbox"]
            faces.append({
                "frame_idx": fidx, "filename": fn, "bbox": bbox,
                "landmarks_5pt": det["kps"], "confidence": det["det_score"],
                "original_face_size": [bbox[2] - bbox[0], bbox[3] - bbox[1]],
            })

    meta = {**meta_base, "compression": video_path.parent.parent.name,
            "num_frames_total": n, "num_frames_extracted": len(faces), "faces": faces,
            "processing": {**meta_base["processing"],
                           "timestamp": datetime.now(timezone.utc).isoformat()}}
    (staging / "meta.json").write_text(json.dumps(meta))
    (staging / ".done").touch()
    return len(faces)


def is_done(out_dir: Path) -> bool:
    mp = out_dir / "meta.json"
    if not (out_dir / ".done").exists() or not mp.exists():
        return False
    try:
        return bool(json.loads(mp.read_text()).get("processing", {}).get("track_fix"))
    except Exception:  # noqa: BLE001
        return False


def commit(out_dir: Path, backup_dir: Path, staging: Path) -> None:
    """Move old crops to backup (once), then move staging into place."""
    if backup_dir.exists():
        if out_dir.exists():
            shutil.rmtree(out_dir)
    elif out_dir.exists():
        backup_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(out_dir), str(backup_dir))
    out_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(staging), str(out_dir))


# --------------------------------------------------------------------------
# Per-group worker
# --------------------------------------------------------------------------

def process_group(packed: tuple[dict, Config]) -> dict[str, Any]:
    g, cfg = packed
    real_stem = g["real_stem"]
    selected = g["selected"]
    res: dict[str, Any] = {"real_stem": real_stem, "selected": selected,
                           "reals": 0, "fakes": 0, "fake_ok": 0, "warnings": []}
    try:
        ad = json.loads((TRACKS_ROOT / real_stem / "all_detections.json").read_text())
        selected_frames = gather_selected_frames(ad, selected)
        if not selected_frames:
            res["warnings"].append("no selected frames"); res["_status"] = "error"
            res["_error"] = "no selected frames"; return res

        # ---- REAL ----
        if cfg.units in ("real", "both"):
            for comp in cfg.compressions:
                out_dir = FACES_ROOT / comp / "actors" / real_stem
                if not cfg.force and is_done(out_dir):
                    continue
                vpath = ACTORS_DIR / comp / "videos" / f"{real_stem}.mp4"
                staging = out_dir.parent / f".{real_stem}.new"
                meta_base = {"video_id": real_stem, "source_path": str(vpath),
                             "dataset": "ff++_dfd", "label": 0, "manipulation": None,
                             "processing": {"detector": "scrfd_10g_det1024",
                                            "tracking": "arcface_buffalo_l",
                                            "track_fix": True, "selected_tracks": selected,
                                            "landmarks_source": "c23_detection",
                                            "alignment": "similarity_transform",
                                            "output_size": cfg.output_size}}
                k = write_crops(vpath, selected_frames, staging, cfg, meta_base)
                if cfg.dry_run:
                    shutil.rmtree(staging, ignore_errors=True)
                else:
                    out_dir.parent.mkdir(parents=True, exist_ok=True)
                    if out_dir.exists():
                        shutil.rmtree(out_dir)
                    shutil.move(str(staging), str(out_dir))
                res["reals"] += k

        # ---- FAKES ----
        if cfg.units in ("fake", "both") and g["fakes"]:
            tgt_path23 = ACTORS_DIR / "c23" / "videos" / f"{real_stem}.mp4"
            tgt_fp = fingerprints(tgt_path23)
            for fake in g["fakes"]:
                stem = fake["stem"]
                # skip if all comps already track-fixed
                if not cfg.force and all(
                        is_done(FACES_ROOT / c / "DeepFakeDetection" / stem)
                        for c in cfg.compressions):
                    res["fakes"] += 1; res["fake_ok"] += 1; continue

                fpath23 = FAKE_VID_DIR / "c23" / "videos" / f"{stem}.mp4"
                al = align(fpath23, tgt_path23, fk=fingerprints(fpath23), tgt=tgt_fp)
                if al.mean_cost > cfg.good_align:
                    res["warnings"].append(f"{stem} align_cost={al.mean_cost:.3f}")
                # fake frame i -> target landmark at t(i)
                frame_to_det = {int(i): selected_frames[int(al.t[i])]
                                for i in range(al.n_fake)
                                if int(al.t[i]) in selected_frames}
                res["fakes"] += 1
                if not frame_to_det:
                    res["warnings"].append(f"{stem} no mapped frames"); continue

                counts = []
                for comp in cfg.compressions:
                    out_dir = FACES_ROOT / comp / "DeepFakeDetection" / stem
                    vpath = FAKE_VID_DIR / comp / "videos" / f"{stem}.mp4"
                    staging = out_dir.parent / f".{stem}.new"
                    meta_base = {"video_id": stem, "source_path": str(vpath),
                                 "dataset": "ff++_dfd", "label": 1,
                                 "manipulation": "DeepFakeDetection",
                                 "processing": {"detector": "scrfd_10g_det1024",
                                                "tracking": "arcface_buffalo_l",
                                                "track_fix": True,
                                                "selected_tracks": selected,
                                                "landmarks_source": f"c23_real_target:{real_stem}",
                                                "alignment": "dtw_similarity_transform",
                                                "align_mean_cost": round(al.mean_cost, 5),
                                                "align_max_gap": al.max_gap,
                                                "target_id": real_stem,
                                                "output_size": cfg.output_size}}
                    k = write_crops(vpath, frame_to_det, staging, cfg, meta_base)
                    counts.append(k)
                    if cfg.dry_run:
                        shutil.rmtree(staging, ignore_errors=True)
                    else:
                        backup = BACKUP_ROOT / comp / "DeepFakeDetection" / stem
                        commit(out_dir, backup, staging)
                if len(set(counts)) == 1:
                    res["fake_ok"] += 1
                else:
                    res["warnings"].append(f"{stem} comp count mismatch {counts}")
        res["_status"] = "ok"
    except Exception as e:  # noqa: BLE001
        res["_status"] = "error"; res["_error"] = str(e)
    return res


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

def parse_args(argv: list[str]) -> Config:
    cfg = Config()
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--units": cfg.units = argv[i + 1]; i += 2
        elif a == "--targets": cfg.targets = argv[i + 1]; i += 2
        elif a == "--compressions": cfg.compressions = argv[i + 1].split(","); i += 2
        elif a == "--workers": cfg.workers = int(argv[i + 1]); i += 2
        elif a == "--limit": cfg.limit = int(argv[i + 1]); i += 2
        elif a == "--force": cfg.force = True; i += 1
        elif a == "--dry-run": cfg.dry_run = True; i += 1
        else: raise ValueError(f"unknown arg {a}")
    return cfg


def build_group_tasks(cfg: Config) -> list[dict]:
    idx = build_index()
    selections = json.loads((TRACKS_ROOT / "selections.json").read_text())
    report = json.loads((TRACKS_ROOT / "selection_report.json").read_text())
    tasks: list[dict] = []
    # target groups
    for rs, g in idx.groups.items():
        if rs not in selections:
            continue
        if cfg.targets == "multi" and report.get(rs, {}).get("n_tracks", 1) < 2:
            continue
        tasks.append({"real_stem": rs, "selected": selections[rs],
                      "fakes": [vars(f) for f in g.fakes]})
    # orphan reals (real-only)
    if cfg.units in ("real", "both") and cfg.targets == "all":
        for rs in idx.orphan_reals:
            if rs in selections:
                tasks.append({"real_stem": rs, "selected": selections[rs], "fakes": []})
    return tasks


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                        datefmt="%H:%M:%S")
    cfg = parse_args(sys.argv[1:])
    tasks = build_group_tasks(cfg)
    if cfg.limit:
        tasks = tasks[:cfg.limit]
    mode = "DRY-RUN" if cfg.dry_run else "WRITE"
    logger.info("=" * 70)
    logger.info("DFD extract | units=%s targets=%s comps=%s workers=%d %s | %d groups",
                cfg.units, cfg.targets, cfg.compressions, cfg.workers, mode, len(tasks))
    logger.info("=" * 70)

    results: list[dict] = []
    failed: list[tuple[str, str]] = []
    t0 = time.monotonic()

    def record(r: dict) -> None:
        if r["_status"] == "error":
            failed.append((r["real_stem"], r.get("_error", "?")))
            logger.error("[%s] FAILED: %s", r["real_stem"], r.get("_error"))
        else:
            results.append(r)
            if r["warnings"]:
                logger.warning("[%s] sel=%s reals=%d fakes=%d/%d warn=%s",
                               r["real_stem"], r["selected"], r["reals"],
                               r["fake_ok"], r["fakes"], r["warnings"][:3])

    packed = [(t, cfg) for t in tasks]
    if cfg.workers > 1 and packed:
        import multiprocessing as mp
        with mp.get_context("spawn").Pool(cfg.workers) as pool:
            for n, r in enumerate(pool.imap_unordered(process_group, packed), 1):
                record(r)
                if n % 20 == 0:
                    logger.info("progress %d/%d groups (%.1f min)", n, len(packed),
                                (time.monotonic() - t0) / 60)
    else:
        for n, p in enumerate(packed, 1):
            r = process_group(p); record(r)
            logger.info("[%d/%d] %s reals=%d fakes=%d/%d", n, len(packed),
                        r["real_stem"], r["reals"], r["fake_ok"], r["fakes"])

    el = time.monotonic() - t0
    tot_real = sum(r["reals"] for r in results)
    tot_fake = sum(r["fakes"] for r in results)
    tot_fake_ok = sum(r["fake_ok"] for r in results)
    logger.info("=" * 70)
    logger.info("DONE %.1f min | groups=%d failed=%d | real_crops=%d fake_vids=%d (ok=%d)",
                el / 60, len(results), len(failed), tot_real, tot_fake, tot_fake_ok)
    if failed:
        logger.error("FAILURES: %s", failed[:10])
    if not cfg.dry_run:
        summ = {"config": vars(cfg), "elapsed_min": round(el / 60, 1),
                "groups": len(results), "failed": failed,
                "real_crops": tot_real, "fake_videos": tot_fake, "fake_ok": tot_fake_ok,
                "results": results, "timestamp": datetime.now(timezone.utc).isoformat()}
        sp = TRACKS_ROOT / f"extract_summary_{cfg.units}_{cfg.targets}.json"
        sp.write_text(json.dumps(summ, indent=2))
        logger.info("summary -> %s", sp)


if __name__ == "__main__":
    main()
