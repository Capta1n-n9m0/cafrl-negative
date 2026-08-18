"""Select which target-real face track is the manipulated identity (diff-vote).

For a multi-person target take we must pick the track corresponding to the actor
whose face the fakes swap. The manipulation only changes that actor's inner face,
so where a fake differs from its target *is* that face. We aggregate this signal:

  for each fake in the (target, scene) group:
    align fake -> target (DTW, gives t(i))
    for sampled fake frames i:
      diff = | fake[i] - target[t(i)] |            (low-res grayscale)
      for each target track present at frame t(i):
        accumulate mean diff energy inside that track's bbox

The manipulated track has high energy; the bystander's track stays near zero
(only compression noise). We select every track within 40% of the max energy
(captures one identity split into several temporal segments), and record the
margin so low-confidence cases can be reviewed.

Cases:
  0 tracks            -> flagged (no usable face)
  1 track             -> that track (no diff needed)
  multi + is target   -> diff-vote
  multi + orphan real -> longest track (no fakes to diff against)

Writes faces_v2/c23/actors/selections.json (real_stem -> [track_ids]) and a
detailed selection_report.json.
"""
from __future__ import annotations

import json
import logging
import sys
import time
from pathlib import Path

import numpy as np
from decord import VideoReader, cpu

sys.path.insert(0, str(Path(__file__).resolve().parent))
from align import align, fingerprints  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from index import build_index, TargetGroup  # noqa: E402

logger = logging.getLogger("dfd.select")

ACTORS_DIR = Path("${HOME}/sdc/datasets/ffpp_original/original_sequences/actors/c23/videos")
FAKE_DIR = Path("${HOME}/sdc/datasets/ffpp_original/manipulated_sequences/DeepFakeDetection/c23/videos")
TRACKS_ROOT = Path.home() / "sdb" / "datasets" / "ff++" / "faces_v2" / "c23" / "actors"

DW, DH = 480, 270            # diff decode resolution
SCALE = DW / 1920.0          # bbox scale (videos are 1920x1080)
N_SAMPLE = 40                # fake frames sampled per fake for voting
MAX_FAKES = 8                # fakes used per group for voting
ENERGY_FRAC = 0.60           # select tracks with energy >= frac * max
# 0.60 chosen after visual audit: genuine same-identity track splits sit at
# >=0.69*max (energy ~2.7-5.6), while bystander/short-fragment over-inclusions in
# high-motion scenes sit at ~0.4-0.5*max (energy ~1.3-1.8). 0.60 cleanly separates.
GOOD_ALIGN = 0.05            # skip fakes whose mean align cost exceeds this


def load_track_bboxes(real_stem: str) -> tuple[dict[int, dict[int, list[float]]], int]:
    """Return {frame_idx: {track_id: bbox}} and num_tracks from all_detections.json."""
    ad = json.loads((TRACKS_ROOT / real_stem / "all_detections.json").read_text())
    tj = json.loads((TRACKS_ROOT / real_stem / "tracks.json").read_text())
    by_frame: dict[int, dict[int, list[float]]] = {}
    for fstr, dets in ad["frames"].items():
        fidx = int(fstr)
        for d in dets:
            tid = d["track_id"]
            if tid < 0:
                continue
            by_frame.setdefault(fidx, {})[tid] = d["bbox"]
    return by_frame, int(tj["num_tracks"])


def _gray_lowres(path: Path, indices: list[int]) -> np.ndarray:
    vr = VideoReader(str(path), ctx=cpu(0), width=DW, height=DH)
    n = len(vr)
    indices = [min(i, n - 1) for i in indices]
    frames = vr.get_batch(indices).asnumpy()
    return frames.mean(axis=3).astype(np.float32)        # [N, DH, DW]


def diff_vote(group: TargetGroup,
              track_bboxes: dict[int, dict[int, list[float]]],
              n_tracks: int) -> dict:
    """Accumulate per-track diff energy across the group's fakes."""
    tgt_path = ACTORS_DIR / f"{group.real_stem}.mp4"
    tgt_fp = fingerprints(tgt_path)                       # cache target fingerprints

    energy = np.zeros(n_tracks, dtype=np.float64)
    count = np.zeros(n_tracks, dtype=np.int64)
    used_fakes = 0
    skipped_align = 0

    fakes = sorted(group.fakes, key=lambda f: -f.n_frames)[:MAX_FAKES]
    for fake in fakes:
        fpath = FAKE_DIR / f"{fake.stem}.mp4"
        fk_fp = fingerprints(fpath)
        al = align(fpath, tgt_path, fk=fk_fp, tgt=tgt_fp)
        if al.mean_cost > GOOD_ALIGN:
            skipped_align += 1
            continue
        used_fakes += 1

        # sample fake frames spread over its length
        idx = np.linspace(0, al.n_fake - 1, min(N_SAMPLE, al.n_fake)).astype(int)
        ti = al.t[idx]                                    # target frames
        fake_g = _gray_lowres(fpath, idx.tolist())
        tgt_g = _gray_lowres(tgt_path, ti.tolist())
        d = np.abs(fake_g - tgt_g)                        # [S, DH, DW]

        for s, tf in enumerate(ti.tolist()):
            tracks_here = track_bboxes.get(int(tf), {})
            for tid, bbox in tracks_here.items():
                if tid >= n_tracks:
                    continue
                x0 = max(0, int(bbox[0] * SCALE)); y0 = max(0, int(bbox[1] * SCALE))
                x1 = min(DW, int(bbox[2] * SCALE)); y1 = min(DH, int(bbox[3] * SCALE))
                if x1 <= x0 or y1 <= y0:
                    continue
                energy[tid] += float(d[s, y0:y1, x0:x1].mean())
                count[tid] += 1

    mean_e = np.where(count > 0, energy / np.maximum(count, 1), 0.0)
    max_e = float(mean_e.max()) if n_tracks else 0.0
    selected = [int(t) for t in range(n_tracks)
                if count[t] > 0 and mean_e[t] >= ENERGY_FRAC * max_e]
    # margin: top selected vs best non-selected
    others = [mean_e[t] for t in range(n_tracks) if t not in selected]
    margin = max_e - (max(others) if others else 0.0)
    return {
        "method": "diff_vote",
        "selected": selected or [int(np.argmax(mean_e))],
        "n_tracks": n_tracks,
        "energies": [round(float(e), 4) for e in mean_e],
        "counts": [int(c) for c in count],
        "max_energy": round(max_e, 4),
        "margin": round(float(margin), 4),
        "used_fakes": used_fakes,
        "skipped_align": skipped_align,
    }


def select_one(real_stem: str, groups: dict[str, TargetGroup]) -> dict:
    track_bboxes, n_tracks = load_track_bboxes(real_stem)
    if n_tracks == 0:
        return {"method": "no_face", "selected": [], "n_tracks": 0}
    if n_tracks == 1:
        return {"method": "single", "selected": [0], "n_tracks": 1}
    if real_stem in groups:
        return diff_vote(groups[real_stem], track_bboxes, n_tracks)
    return {"method": "longest", "selected": [0], "n_tracks": n_tracks}  # orphan multi


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                        datefmt="%H:%M:%S")
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 0
    only_multi = "--only-multi" in sys.argv

    idx = build_index()
    ready = [r for r in idx.all_reals if (TRACKS_ROOT / r / "tracks.json").exists()]
    logger.info("%d/%d reals have detection done", len(ready), len(idx.all_reals))

    report: dict[str, dict] = {}
    t0 = time.monotonic()
    todo = ready[:limit] if limit else ready
    for n, stem in enumerate(todo, 1):
        res = select_one(stem, idx.groups)
        if only_multi and res["n_tracks"] < 2:
            continue
        report[stem] = res
        if res["method"] in ("diff_vote",) or res["n_tracks"] >= 2:
            logger.info("[%d/%d] %s: %s sel=%s nt=%d margin=%s E=%s used=%s",
                        n, len(todo), stem, res["method"], res["selected"],
                        res["n_tracks"], res.get("margin"), res.get("energies"),
                        res.get("used_fakes"))

    # selections.json: real_stem -> [track_ids] (compatible with propagation)
    selections = {k: v["selected"] for k, v in report.items()}
    (TRACKS_ROOT / "selections.json").write_text(json.dumps(selections, indent=2))
    (TRACKS_ROOT / "selection_report.json").write_text(json.dumps(report, indent=2))

    from collections import Counter
    methods = Counter(v["method"] for v in report.values())
    multi = [v for v in report.values() if v["n_tracks"] >= 2]
    lowmargin = [k for k, v in report.items()
                 if v["method"] == "diff_vote" and v.get("margin", 1) < 0.5]
    logger.info("=" * 60)
    logger.info("selected %d reals in %.1fs | methods=%s", len(report),
                time.monotonic() - t0, dict(methods))
    logger.info("multi-track: %d | multi selecting >1 track: %d | low-margin(<0.5): %d %s",
                len(multi), sum(len(v["selected"]) > 1 for v in multi),
                len(lowmargin), lowmargin[:10])


if __name__ == "__main__":
    main()
