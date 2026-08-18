"""Propagate reviewed face-track selections across compression levels.

For the FF++ youtube originals that were re-extracted with ArcFace tracking
(see ``reextract_tracks.py``), this script applies the human-reviewed track
selections (``selections.json``) to produce corrected face crops for c0, c23
AND c40, then replaces the old single-face extractions in the main ``faces/``
tree.

Only the 23 *multi-track* videos are processed. The 8 videos whose
re-extraction yielded a single track had one consistent identity throughout,
so the original 'largest-face' extraction already picked the right face —
re-propagating them would change nothing meaningful while making them
inconsistent with the ~969 untouched originals. They are skipped by default
(override with ``--include-single-track``).

Why this works (verified in docs/11):
  * FF++ compression levels are frame-for-frame identical re-encodes — same
    resolution, frame count, fps, only CRF differs. So a landmark set detected
    on the lossless c0 frame localises the same face in the c23/c40 frame.
  * The c0 landmarks for the selected track(s) are stored per frame in
    ``faces_v2/c0/real/{vid}/all_detections.json``.
  * No GPU / face detection is needed here: we just decode each compression's
    frames and apply the same similarity-transform alignment used everywhere
    else (``align_face``), guaranteeing spatial consistency across c0/c23/c40.

Replacement is safe and reversible: the old single-face extraction for each
(video, compression) is moved to a backup tree before the new crops take its
place. Re-runs are idempotent (the backup is created at most once, and already
fixed videos are skipped unless ``--force``).

Output crops + meta.json match the schema produced by ``extract_faces.py`` so
the downstream dataloader sees a uniform interface, with extra provenance
fields under ``processing`` (``track_fix``, ``selected_tracks``,
``landmarks_source``).
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

# Reuse the exact alignment used by both extraction scripts.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from reextract_tracks import align_face  # noqa: E402

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Manipulation methods whose fakes are built on a target video's frames.
# For a multi-track target T, the fake `T_*.mp4` reuses T's selected-track
# landmarks at the same frame index (validated: pose-preserving manipulation,
# head-aligned frames, IoU >= 0.87 across methods).
FAKE_METHODS: list[str] = [
    "Deepfakes", "FaceShifter", "Face2Face", "FaceSwap", "NeuralTextures",
]


@dataclass
class PropagateConfig:
    faces_v2_root: str = str(Path.home() / "sdb" / "datasets" / "ff++" / "faces_v2")
    faces_root: str = str(Path.home() / "sdb" / "datasets" / "ff++" / "faces")
    backup_root: str = str(Path.home() / "sdb" / "datasets" / "ff++" / "faces_singleface_backup")
    source_video_root: str = "${HOME}/sdc/datasets/ffpp_original/original_sequences/youtube"
    mani_video_root: str = "${HOME}/sdc/datasets/ffpp_original/manipulated_sequences"
    compressions: list[str] = field(default_factory=lambda: ["c0", "c23", "c40"])
    out_method: str = "real"  # subdir holding the re-extracted track data (faces_v2)
    mode: str = "both"        # "real" | "fake" | "both" — which units to (re)process
    output_size: int = 256
    scale_factor: float = 1.3  # carried for schema parity (unused by alignment)
    decode_batch: int = 64
    workers: int = 1        # process-parallel decode workers (units are independent)
    dry_run: bool = False   # build + verify into staging, do not replace
    no_replace: bool = False  # build into staging and keep it, do not touch old tree
    force: bool = False     # reprocess even if already fixed
    include_single_track: bool = False  # also reprocess videos with a single track


# ---------------------------------------------------------------------------
# Selection -> per-frame landmark resolution
# ---------------------------------------------------------------------------

def load_selections(faces_v2_root: str, out_method: str) -> dict[str, list[int]]:
    """Load selections.json, normalising every value to a list of track ids."""
    path = Path(faces_v2_root) / "c0" / out_method / "selections.json"
    raw = json.loads(path.read_text())
    norm: dict[str, list[int]] = {}
    for vid, sel in raw.items():
        norm[vid] = [int(sel)] if isinstance(sel, int) else [int(t) for t in sel]
    return norm


def gather_selected_frames(
    all_detections: dict[str, Any],
    selected_tracks: list[int],
) -> dict[int, dict[str, Any]]:
    """Resolve the chosen detection (kps/bbox/score) for each frame.

    Frames covered by more than one selected track (overlap region of a
    multi-track merge, e.g. video 509 frames 62-64) keep the higher-confidence
    detection — deterministic and, for same-person merges, visually identical.

    Returns frame_idx -> detection dict, ordered by frame index.
    """
    sel = set(selected_tracks)
    by_frame: dict[int, dict[str, Any]] = {}
    for fstr, dets in all_detections["frames"].items():
        fidx = int(fstr)
        cands = [d for d in dets if d["track_id"] in sel]
        if not cands:
            continue
        by_frame[fidx] = max(cands, key=lambda d: d["det_score"])
    return dict(sorted(by_frame.items()))


def faces_in_frame(all_detections: dict[str, Any], fidx: int) -> int:
    """Total faces detected in a frame (for the num_faces_detected field)."""
    return len(all_detections["frames"].get(str(fidx), []))


def num_tracks(vid: str, cfg: PropagateConfig) -> int:
    """Number of identity tracks found for a video during re-extraction.

    A single track means there was only one consistent identity across the
    whole video, so the original 'largest-face' extraction already picked the
    correct face — there is nothing to fix. These videos are skipped by default
    (the spatial flag that surfaced them was head motion, not face switching).
    """
    tj = Path(cfg.faces_v2_root) / "c0" / cfg.out_method / vid / "tracks.json"
    return int(json.loads(tj.read_text())["num_tracks"])


# ---------------------------------------------------------------------------
# Processing units — one real video OR one manipulated video to (re)extract
# ---------------------------------------------------------------------------

@dataclass
class Unit:
    """A single output to produce by reusing a target's selected landmarks.

    ``target_vid`` is the real multi-track original whose reviewed track
    selection supplies the per-frame landmarks. For a real unit the output IS
    that video; for a fake unit the output is a manipulation built on it
    (``out_id`` like ``420_257``), cropped with the same landmarks at the same
    frame index.
    """
    target_vid: str          # real target whose landmarks we reuse
    out_method: str          # "real" or a manipulation method (e.g. "Deepfakes")
    out_id: str              # output dir name (target id, or fake stem)
    label: int               # 0 real, 1 fake
    manipulation: str | None
    kind: str                # "real" | "fake"


def unit_video_path(unit: Unit, comp: str, cfg: PropagateConfig) -> Path:
    if unit.kind == "real":
        return Path(cfg.source_video_root) / comp / "videos" / f"{unit.out_id}.mp4"
    return Path(cfg.mani_video_root) / unit.out_method / comp / "videos" / f"{unit.out_id}.mp4"


def unit_target_dir(unit: Unit, comp: str, cfg: PropagateConfig) -> Path:
    return Path(cfg.faces_root) / comp / unit.out_method / unit.out_id


def unit_backup_dir(unit: Unit, comp: str, cfg: PropagateConfig) -> Path:
    return Path(cfg.backup_root) / comp / unit.out_method / unit.out_id


def extract_to_staging(
    unit: Unit,
    comp: str,
    selected_tracks: list[int],
    selected_frames: dict[int, dict[str, Any]],
    all_detections: dict[str, Any],
    staging_dir: Path,
    cfg: PropagateConfig,
) -> dict[str, Any]:
    """Decode the unit's video, align the target landmarks per frame, write crops + meta."""
    import decord
    decord.bridge.set_bridge("native")

    video_path = unit_video_path(unit, comp, cfg)
    if not video_path.exists():
        raise FileNotFoundError(f"source video missing: {video_path}")

    if staging_dir.exists():
        shutil.rmtree(staging_dir)
    staging_dir.mkdir(parents=True, exist_ok=True)

    vr = decord.VideoReader(str(video_path), num_threads=1)
    n = len(vr)

    # Reuse target landmarks at the same frame index; skip frames the video
    # doesn't have (manipulated clips can be shorter/longer than the original).
    indices = [f for f in selected_frames if f < n]
    skipped_oob = len(selected_frames) - len(indices)
    if skipped_oob:
        logger.warning("  [%s/%s/%s] %d landmark frames beyond video length %d, skipped",
                       comp, unit.out_method, unit.out_id, skipped_oob, n)

    face_entries: list[dict[str, Any]] = []
    for start in range(0, len(indices), cfg.decode_batch):
        chunk = indices[start:start + cfg.decode_batch]
        frames = vr.get_batch(chunk).asnumpy()  # RGB
        for j, fidx in enumerate(chunk):
            det = selected_frames[fidx]
            kps = np.array(det["kps"], dtype=np.float32)
            aligned = align_face(frames[j], kps, cfg.output_size)  # RGB
            filename = f"{fidx:04d}.png"
            cv2.imwrite(
                str(staging_dir / filename),
                cv2.cvtColor(aligned, cv2.COLOR_RGB2BGR),
            )
            bbox = det["bbox"]
            face_entries.append({
                "frame_idx": fidx,
                "filename": filename,
                "bbox": bbox,
                "landmarks_5pt": det["kps"],
                "confidence": det["det_score"],
                "original_face_size": [bbox[2] - bbox[0], bbox[3] - bbox[1]],
                "num_faces_detected": faces_in_frame(all_detections, fidx),
            })

    meta = {
        "video_id": unit.out_id,
        "source_path": str(video_path),
        "dataset": "ff++",
        "label": unit.label,
        "manipulation": unit.manipulation,
        "compression": comp,
        "num_frames_total": n,
        "num_frames_extracted": len(face_entries),
        "faces": face_entries,
        "processing": {
            "detector": "scrfd_10g",
            "tracking": "arcface_buffalo_l",
            "track_fix": True,
            "selected_tracks": selected_tracks,
            "landmarks_source": "c0" if unit.kind == "real" else f"c0_real_target:{unit.target_vid}",
            "target_id": unit.target_vid,
            "scale_factor": cfg.scale_factor,
            "output_size": cfg.output_size,
            "alignment": "similarity_transform",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }
    (staging_dir / "meta.json").write_text(json.dumps(meta))
    (staging_dir / ".done").touch()

    return {
        "compression": comp,
        "num_extracted": len(face_entries),
        "png_count": len(list(staging_dir.glob("*.png"))),
        "video_frames": n,
    }


def commit_replacement(unit: Unit, comp: str, staging_dir: Path, cfg: PropagateConfig) -> None:
    """Atomically swap staging crops into the main tree, backing up the old once."""
    target = unit_target_dir(unit, comp, cfg)
    backup = unit_backup_dir(unit, comp, cfg)

    if backup.exists():
        # Already backed up on a prior run; the current target is our own output.
        if target.exists():
            shutil.rmtree(target)
    elif target.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(target), str(backup))
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(staging_dir), str(target))


# ---------------------------------------------------------------------------
# Drivers
# ---------------------------------------------------------------------------

def is_already_fixed(unit: Unit, cfg: PropagateConfig) -> bool:
    """True if every compression target already carries the track-fix marker."""
    for comp in cfg.compressions:
        meta_path = unit_target_dir(unit, comp, cfg) / "meta.json"
        if not meta_path.exists():
            return False
        try:
            meta = json.loads(meta_path.read_text())
        except Exception:
            return False
        if not meta.get("processing", {}).get("track_fix"):
            return False
    return True


def build_units(selections: dict[str, list[int]], cfg: PropagateConfig) -> list[Unit]:
    """Build the list of real/fake units for the multi-track targets."""
    import glob
    units: list[Unit] = []
    for vid in sorted(selections):
        if not cfg.include_single_track and num_tracks(vid, cfg) == 1:
            continue
        if cfg.mode in ("real", "both"):
            units.append(Unit(vid, cfg.out_method, vid, 0, None, "real"))
        if cfg.mode in ("fake", "both"):
            for method in FAKE_METHODS:
                pattern = str(Path(cfg.mani_video_root) / method / "c0" / "videos" / f"{vid}_*.mp4")
                cands = sorted(glob.glob(pattern))
                if not cands:
                    logger.warning("[%s/%s] no fake file %s_*.mp4 found, skipping", vid, method, vid)
                    continue
                if len(cands) > 1:
                    logger.warning("[%s/%s] %d files match %s_*; using %s",
                                   vid, method, len(cands), vid, Path(cands[0]).name)
                stem = Path(cands[0]).stem
                units.append(Unit(vid, method, stem, 1, method, "fake"))
    return units


def process_unit(unit: Unit, selected_tracks: list[int],
                 selected_frames: dict[int, dict[str, Any]],
                 all_detections: dict[str, Any], cfg: PropagateConfig) -> dict[str, Any]:
    per_comp: list[dict[str, Any]] = []
    staging_dirs: dict[str, Path] = {}
    for comp in cfg.compressions:
        staging = unit_target_dir(unit, comp, cfg).parent / f".{unit.out_id}.new"
        per_comp.append(extract_to_staging(
            unit, comp, selected_tracks, selected_frames, all_detections, staging, cfg))
        staging_dirs[comp] = staging

    # Compressions of one video are frame-identical re-encodes -> equal counts.
    counts = {s["num_extracted"] for s in per_comp}
    consistent = len(counts) == 1

    if cfg.dry_run:
        for staging in staging_dirs.values():
            shutil.rmtree(staging, ignore_errors=True)
    elif not cfg.no_replace:
        if not consistent:
            for staging in staging_dirs.values():
                shutil.rmtree(staging, ignore_errors=True)
            raise RuntimeError(f"refusing to replace {unit.out_method}/{unit.out_id}: counts {counts}")
        for comp in cfg.compressions:
            commit_replacement(unit, comp, staging_dirs[comp], cfg)

    return {
        "out_method": unit.out_method,
        "out_id": unit.out_id,
        "target_vid": unit.target_vid,
        "kind": unit.kind,
        "num_selected_frames": len(selected_frames),
        "per_compression": per_comp,
        "consistent": consistent,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: list[str]) -> PropagateConfig:
    cfg = PropagateConfig()
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--dry-run":
            cfg.dry_run = True; i += 1
        elif arg == "--no-replace":
            cfg.no_replace = True; i += 1
        elif arg == "--force":
            cfg.force = True; i += 1
        elif arg == "--include-single-track":
            cfg.include_single_track = True; i += 1
        elif arg == "--mode":
            cfg.mode = argv[i + 1]; i += 2
            if cfg.mode not in ("real", "fake", "both"):
                raise ValueError(f"--mode must be real|fake|both, got {cfg.mode}")
        elif arg == "--compressions":
            cfg.compressions = argv[i + 1].split(","); i += 2
        elif arg == "--faces-root":
            cfg.faces_root = argv[i + 1]; i += 2
        elif arg == "--faces-v2-root":
            cfg.faces_v2_root = argv[i + 1]; i += 2
        elif arg == "--backup-root":
            cfg.backup_root = argv[i + 1]; i += 2
        elif arg == "--workers":
            cfg.workers = int(argv[i + 1]); i += 2
        else:
            raise ValueError(f"Unknown argument: {arg}")
    return cfg


def _process_one(packed: tuple["Unit", list[int], PropagateConfig]) -> dict[str, Any]:
    """Pool worker: load the target's landmarks and process one unit.

    Independent per unit — each unit owns a distinct output dir and a uniquely
    named staging dir, so workers never collide. Returns a result dict tagged
    with status (the pool must not raise).
    """
    unit, tracks, cfg = packed
    label = f"{unit.out_method}/{unit.out_id}"
    try:
        ad = json.loads((Path(cfg.faces_v2_root) / "c0" / cfg.out_method
                         / unit.target_vid / "all_detections.json").read_text())
        selected_frames = gather_selected_frames(ad, tracks)
        if not selected_frames:
            raise ValueError(f"no frames for selected tracks {tracks}")
        res = process_unit(unit, tracks, selected_frames, ad, cfg)
        res["_status"] = "ok"
        res["_label"] = label
        return res
    except Exception as e:
        return {"_status": "error", "_label": label, "_error": str(e)}


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
    )
    cfg = parse_args(sys.argv[1:])

    run_mode = "DRY-RUN" if cfg.dry_run else ("NO-REPLACE" if cfg.no_replace else "REPLACE")
    logger.info("=" * 70)
    logger.info("Propagate track selections | units=%s | comps=%s | %s",
                cfg.mode, cfg.compressions, run_mode)
    logger.info("=" * 70)

    selections = load_selections(cfg.faces_v2_root, cfg.out_method)
    units = build_units(selections, cfg)
    logger.info("Built %d units (%d real, %d fake) from %d selections",
                len(units), sum(u.kind == "real" for u in units),
                sum(u.kind == "fake" for u in units), len(selections))

    # Partition into already-fixed (skip) and to-process.
    skip_enabled = not (cfg.force or cfg.dry_run or cfg.no_replace)
    todo: list[Unit] = []
    skipped: list[str] = []
    for unit in units:
        if skip_enabled and is_already_fixed(unit, cfg):
            skipped.append(f"{unit.out_method}/{unit.out_id}")
        else:
            todo.append(unit)
    logger.info("%d to process, %d already fixed (skipped) | workers=%d",
                len(todo), len(skipped), cfg.workers)

    results: list[dict[str, Any]] = []
    failed: list[tuple[str, str]] = []
    t0 = time.monotonic()

    def record(res: dict[str, Any]) -> None:
        label = res["_label"]
        if res["_status"] == "error":
            logger.error("[%s] FAILED: %s", label, res["_error"])
            failed.append((label, res["_error"]))
        else:
            results.append(res)
            logger.info("[%s] %d frames/comp x %d | consistent=%s | counts=%s",
                        label, res["per_compression"][0]["num_extracted"],
                        len(cfg.compressions), res["consistent"],
                        [s["num_extracted"] for s in res["per_compression"]])

    packed = [(u, selections[u.target_vid], cfg) for u in todo]
    if cfg.workers > 1 and packed:
        import multiprocessing as mp
        ctx = mp.get_context("spawn")
        with ctx.Pool(cfg.workers) as pool:
            for res in pool.imap_unordered(_process_one, packed):
                record(res)
    else:
        for p in packed:
            record(_process_one(p))

    elapsed = time.monotonic() - t0
    logger.info("=" * 70)
    logger.info("DONE in %.1fs | processed=%d skipped_already_fixed=%d failed=%d",
                elapsed, len(results), len(skipped), len(failed))
    if failed:
        logger.error("FAILURES: %s", failed)

    total_crops = sum(s["num_extracted"] for r in results for s in r["per_compression"])
    logger.info("Total crops written/verified: %d across %d compressions",
                total_crops, len(cfg.compressions))

    if not cfg.dry_run:
        suffix = "" if cfg.mode == "both" else f"_{cfg.mode}"
        summary_path = Path(cfg.faces_v2_root) / "c0" / cfg.out_method / f"propagation_summary{suffix}.json"
        summary = {
            "units_mode": cfg.mode,
            "run_mode": run_mode,
            "compressions": cfg.compressions,
            "elapsed_seconds": round(elapsed, 1),
            "num_processed": len(results),
            "num_skipped_already_fixed": len(skipped),
            "num_failed": len(failed),
            "results": results,
            "failures": failed,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        summary_path.write_text(json.dumps(summary, indent=2))
        logger.info("Summary written to %s", summary_path)


if __name__ == "__main__":
    main()
