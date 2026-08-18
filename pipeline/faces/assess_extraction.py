"""Assess completeness of FF++ face extraction.

Checks:
  1. Video-level coverage   — every CSV video has a .done extraction
  2. Frame-level yield      — face count vs source frame count
  3. Marker consistency     — .done ↔ actual content agreement
  4. Image integrity        — PNG dimensions, non-zero size (sampled)
  5. Cross-compression      — video IDs present across c0/c23/c40
  6. Spatial consistency    — face bbox drift within a video
  7. Aggregate summary      — per-method, per-compression stats
"""

from __future__ import annotations

import csv
import json
import struct
import sys
import zlib
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

FACES_ROOT = Path.home() / "sdb" / "datasets" / "ff++" / "faces"
METADATA_CSV = (
    Path(__file__).resolve().parents[4] / "datasets" / "ffpp_metadata.csv"
)

# Methods in the CSV → output directory name
METHOD_TO_DIR = {
    "youtube": "real",
    "actors": "real",
    "Deepfakes": "Deepfakes",
    "Face2Face": "Face2Face",
    "FaceSwap": "FaceSwap",
    "NeuralTextures": "NeuralTextures",
    "FaceShifter": "FaceShifter",
    "DeepFakeDetection": "DeepFakeDetection",
}

COMPRESSIONS = ["c0", "c23", "c40"]

YIELD_WARN_THRESHOLD = 0.5
YIELD_CRITICAL_THRESHOLD = 0.2

INTEGRITY_SAMPLE_PER_VIDEO = 3

# For spatial consistency: if the bbox center moves more than this fraction
# of the frame diagonal between consecutive detected frames, flag it.
SPATIAL_JUMP_THRESHOLD = 0.25
# If the median absolute deviation of bbox centers (as fraction of diagonal)
# exceeds this, flag the video as spatially inconsistent.
SPATIAL_MAD_THRESHOLD = 0.15


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class VideoIssue:
    video_id: str
    compression: str
    method: str
    issue_type: str
    detail: str


@dataclass
class MethodStats:
    expected: int = 0
    extracted: int = 0
    total_frames: int = 0
    total_faces: int = 0
    total_size_bytes: int = 0


@dataclass
class Report:
    issues: list[VideoIssue] = field(default_factory=list)
    stats: dict[tuple[str, str], MethodStats] = field(default_factory=dict)
    extra_dirs: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# PNG header check (no PIL dependency)
# ---------------------------------------------------------------------------

def read_png_dimensions(path: Path) -> tuple[int, int] | None:
    """Read width, height from PNG IHDR chunk. Returns None on invalid PNG."""
    try:
        with open(path, "rb") as f:
            sig = f.read(8)
            if sig != b"\x89PNG\r\n\x1a\n":
                return None
            length = struct.unpack(">I", f.read(4))[0]
            chunk_type = f.read(4)
            if chunk_type != b"IHDR" or length < 13:
                return None
            data = f.read(13)
            w, h = struct.unpack(">II", data[:8])
            return (w, h)
    except (OSError, struct.error):
        return None


# ---------------------------------------------------------------------------
# Load expected videos from metadata CSV
# ---------------------------------------------------------------------------

def load_expected_videos(
    csv_path: Path,
) -> dict[tuple[str, str], set[str]]:
    """Returns {(compression, output_dir_method): {video_id, ...}}."""
    expected: dict[tuple[str, str], set[str]] = defaultdict(set)
    with open(csv_path) as f:
        for row in csv.DictReader(f):
            method = row["method"]
            compression = row["compression"]
            video_id = row["filename"].rsplit(".", 1)[0]
            out_method = METHOD_TO_DIR.get(method)
            if out_method is None:
                continue
            expected[(compression, out_method)].add(video_id)
    return dict(expected)


# ---------------------------------------------------------------------------
# Scan extracted directories
# ---------------------------------------------------------------------------

def scan_extracted(
    faces_root: Path,
) -> dict[tuple[str, str], dict[str, Path]]:
    """Returns {(compression, method): {video_id: dir_path}}."""
    extracted: dict[tuple[str, str], dict[str, Path]] = defaultdict(dict)
    for comp_dir in sorted(faces_root.iterdir()):
        if not comp_dir.is_dir():
            continue
        comp = comp_dir.name
        for method_dir in sorted(comp_dir.iterdir()):
            if not method_dir.is_dir():
                continue
            method = method_dir.name
            for video_dir in sorted(method_dir.iterdir()):
                if not video_dir.is_dir():
                    continue
                extracted[(comp, method)][video_dir.name] = video_dir
    return dict(extracted)


# ---------------------------------------------------------------------------
# Check 1: Video-level coverage
# ---------------------------------------------------------------------------

def check_coverage(
    expected: dict[tuple[str, str], set[str]],
    extracted: dict[tuple[str, str], dict[str, Path]],
    report: Report,
) -> None:
    for key, expected_ids in sorted(expected.items()):
        comp, method = key
        ext_ids = set(extracted.get(key, {}).keys())

        # Videos expected but not extracted
        missing = expected_ids - ext_ids
        for vid in sorted(missing):
            report.issues.append(VideoIssue(
                vid, comp, method, "missing_video",
                "Expected from metadata CSV but not found in extraction output",
            ))

        # Videos extracted but not in CSV (unexpected)
        extra = ext_ids - expected_ids
        for vid in sorted(extra):
            report.issues.append(VideoIssue(
                vid, comp, method, "extra_video",
                "Found in extraction output but not in metadata CSV",
            ))


# ---------------------------------------------------------------------------
# Check 2 & 3 & 4 & 6: Per-video checks (yield, markers, integrity, spatial)
# ---------------------------------------------------------------------------

def bbox_center(bbox: list[float]) -> np.ndarray:
    return np.array([(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2])


def check_video(
    video_dir: Path,
    compression: str,
    method: str,
    report: Report,
    stats: MethodStats,
) -> None:
    has_done = (video_dir / ".done").exists()
    meta_path = video_dir / "meta.json"
    pngs = sorted(video_dir.glob("*.png"))
    video_id = video_dir.name

    stats.total_size_bytes += sum(p.stat().st_size for p in pngs)

    # --- Marker consistency ---
    if has_done and not pngs and not meta_path.exists():
        report.issues.append(VideoIssue(
            video_id, compression, method, "marker_no_content",
            ".done marker exists but no PNGs or meta.json found",
        ))
        return

    if pngs and not has_done:
        report.issues.append(VideoIssue(
            video_id, compression, method, "content_no_marker",
            f"{len(pngs)} PNGs exist but no .done marker (interrupted extraction?)",
        ))

    if not meta_path.exists():
        if pngs:
            report.issues.append(VideoIssue(
                video_id, compression, method, "missing_meta",
                f"{len(pngs)} PNGs exist but no meta.json",
            ))
        return

    # --- Load and validate meta.json ---
    try:
        with open(meta_path) as f:
            meta = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        report.issues.append(VideoIssue(
            video_id, compression, method, "corrupt_meta",
            f"Cannot parse meta.json: {e}",
        ))
        return

    num_total = meta.get("num_frames_total", 0)
    num_extracted = meta.get("num_frames_extracted", 0)
    faces = meta.get("faces", [])

    stats.total_frames += num_total
    stats.total_faces += num_extracted
    stats.extracted += 1

    # Check meta/PNG count agreement
    if len(pngs) != len(faces):
        report.issues.append(VideoIssue(
            video_id, compression, method, "png_meta_mismatch",
            f"PNG count ({len(pngs)}) != meta.json faces count ({len(faces)})",
        ))

    # --- Frame-level yield ---
    if num_total > 0:
        yield_ratio = num_extracted / num_total
        if yield_ratio < YIELD_CRITICAL_THRESHOLD:
            report.issues.append(VideoIssue(
                video_id, compression, method, "yield_critical",
                f"Only {num_extracted}/{num_total} frames extracted "
                f"({yield_ratio:.1%}) — possible detection failure",
            ))
        elif yield_ratio < YIELD_WARN_THRESHOLD:
            report.issues.append(VideoIssue(
                video_id, compression, method, "yield_warning",
                f"{num_extracted}/{num_total} frames extracted ({yield_ratio:.1%})",
            ))

    # --- Image integrity (sampled) ---
    if pngs:
        sample_indices = np.linspace(
            0, len(pngs) - 1, min(INTEGRITY_SAMPLE_PER_VIDEO, len(pngs)),
        ).astype(int)
        for idx in sample_indices:
            p = pngs[idx]
            if p.stat().st_size == 0:
                report.issues.append(VideoIssue(
                    video_id, compression, method, "zero_size_png",
                    f"{p.name} is 0 bytes",
                ))
                continue
            dims = read_png_dimensions(p)
            if dims is None:
                report.issues.append(VideoIssue(
                    video_id, compression, method, "invalid_png",
                    f"{p.name} is not a valid PNG",
                ))
            elif dims != (256, 256):
                report.issues.append(VideoIssue(
                    video_id, compression, method, "wrong_dimensions",
                    f"{p.name} is {dims[0]}x{dims[1]}, expected 256x256",
                ))

    # --- Spatial consistency ---
    if len(faces) < 2:
        return

    centers = []
    for face in faces:
        bbox = face.get("bbox")
        if bbox and len(bbox) == 4:
            centers.append(bbox_center(bbox))

    if len(centers) < 2:
        return

    centers_arr = np.array(centers)

    # Use first frame's bbox to estimate frame diagonal for normalization
    first_bbox = faces[0]["bbox"]
    face_w = first_bbox[2] - first_bbox[0]
    face_h = first_bbox[3] - first_bbox[1]
    # The original_face_size gives us face size; estimate frame size from
    # typical video. Use face diagonal * 5 as rough frame diagonal
    # (face is ~20% of frame height). But better: use the actual bbox
    # coordinates as reference scale. We normalize by face diagonal itself
    # since we don't have frame dimensions in meta.json reliably.
    face_diag = np.sqrt(face_w**2 + face_h**2)
    if face_diag < 1:
        return

    # Frame-to-frame jumps
    diffs = np.diff(centers_arr, axis=0)
    jump_distances = np.linalg.norm(diffs, axis=1) / face_diag

    max_jump_idx = np.argmax(jump_distances)
    max_jump = jump_distances[max_jump_idx]

    if max_jump > SPATIAL_JUMP_THRESHOLD:
        frame_from = faces[max_jump_idx]["frame_idx"]
        frame_to = faces[max_jump_idx + 1]["frame_idx"]
        report.issues.append(VideoIssue(
            video_id, compression, method, "spatial_jump",
            f"Face bbox jumped {max_jump:.2f}x face diagonal "
            f"between frames {frame_from}→{frame_to} "
            f"(threshold: {SPATIAL_JUMP_THRESHOLD}x)",
        ))

    # Overall spread: median absolute deviation of centers
    median_center = np.median(centers_arr, axis=0)
    deviations = np.linalg.norm(centers_arr - median_center, axis=1) / face_diag
    mad = np.median(deviations)

    if mad > SPATIAL_MAD_THRESHOLD:
        report.issues.append(VideoIssue(
            video_id, compression, method, "spatial_spread",
            f"Face position MAD = {mad:.2f}x face diagonal "
            f"(threshold: {SPATIAL_MAD_THRESHOLD}x) — "
            f"face region varies significantly across video",
        ))


# ---------------------------------------------------------------------------
# Check 5: Cross-compression consistency
# ---------------------------------------------------------------------------

def check_cross_compression(
    extracted: dict[tuple[str, str], dict[str, Path]],
    report: Report,
) -> None:
    methods_across_comps: dict[str, dict[str, set[str]]] = defaultdict(
        lambda: defaultdict(set)
    )
    for (comp, method), vids in extracted.items():
        methods_across_comps[method][comp] = set(vids.keys())

    for method, comp_dict in sorted(methods_across_comps.items()):
        comps_present = sorted(comp_dict.keys())
        if len(comps_present) < 2:
            continue
        all_ids = set()
        for ids in comp_dict.values():
            all_ids |= ids

        for vid in sorted(all_ids):
            present_in = [c for c in comps_present if vid in comp_dict[c]]
            missing_from = [c for c in comps_present if vid not in comp_dict[c]]
            if missing_from:
                report.issues.append(VideoIssue(
                    vid, ",".join(missing_from), method,
                    "cross_compression_gap",
                    f"Present in {','.join(present_in)} but missing from "
                    f"{','.join(missing_from)}",
                ))


# ---------------------------------------------------------------------------
# Printing
# ---------------------------------------------------------------------------

ISSUE_SEVERITY = {
    "missing_video": "WARN",
    "extra_video": "INFO",
    "marker_no_content": "ERROR",
    "content_no_marker": "WARN",
    "missing_meta": "WARN",
    "corrupt_meta": "ERROR",
    "png_meta_mismatch": "WARN",
    "yield_critical": "ERROR",
    "yield_warning": "WARN",
    "zero_size_png": "ERROR",
    "invalid_png": "ERROR",
    "wrong_dimensions": "ERROR",
    "spatial_jump": "WARN",
    "spatial_spread": "WARN",
    "cross_compression_gap": "INFO",
}


def print_report(report: Report) -> None:
    # --- Aggregate summary ---
    print("=" * 80)
    print("EXTRACTION COMPLETENESS REPORT")
    print("=" * 80)

    print("\n── Aggregate Summary ──\n")
    print(f"{'Compression':<8} {'Method':<20} {'Expected':>8} {'Extracted':>9} "
          f"{'%Done':>6} {'Frames':>10} {'Faces':>10} {'Yield':>6} {'Size':>10}")
    print("─" * 95)

    totals = MethodStats()

    for (comp, method), st in sorted(report.stats.items()):
        pct = (st.extracted / st.expected * 100) if st.expected > 0 else 0
        yld = (st.total_faces / st.total_frames * 100) if st.total_frames > 0 else 0
        size_gb = st.total_size_bytes / (1024**3)
        print(f"{comp:<8} {method:<20} {st.expected:>8} {st.extracted:>9} "
              f"{pct:>5.1f}% {st.total_frames:>10} {st.total_faces:>10} "
              f"{yld:>5.1f}% {size_gb:>8.1f}GB")
        totals.expected += st.expected
        totals.extracted += st.extracted
        totals.total_frames += st.total_frames
        totals.total_faces += st.total_faces
        totals.total_size_bytes += st.total_size_bytes

    print("─" * 95)
    pct = (totals.extracted / totals.expected * 100) if totals.expected > 0 else 0
    yld = (totals.total_faces / totals.total_frames * 100) if totals.total_frames > 0 else 0
    size_gb = totals.total_size_bytes / (1024**3)
    print(f"{'TOTAL':<29} {totals.expected:>8} {totals.extracted:>9} "
          f"{pct:>5.1f}% {totals.total_frames:>10} {totals.total_faces:>10} "
          f"{yld:>5.1f}% {size_gb:>8.1f}GB")

    # --- Issues by type ---
    issues_by_type: dict[str, list[VideoIssue]] = defaultdict(list)
    for issue in report.issues:
        issues_by_type[issue.issue_type].append(issue)

    if not report.issues:
        print("\n✓ No issues found — extraction looks complete and consistent.")
        return

    print(f"\n── Issues Summary ({len(report.issues)} total) ──\n")

    for issue_type in sorted(issues_by_type.keys()):
        issues = issues_by_type[issue_type]
        severity = ISSUE_SEVERITY.get(issue_type, "INFO")
        print(f"  [{severity}] {issue_type}: {len(issues)}")

    # --- Issue details (grouped) ---
    print("\n── Issue Details ──\n")

    for issue_type in sorted(issues_by_type.keys()):
        issues = issues_by_type[issue_type]
        severity = ISSUE_SEVERITY.get(issue_type, "INFO")
        print(f"\n[{severity}] {issue_type} ({len(issues)}):")

        # For large groups, show first 20 + summary
        show = issues[:20]
        for iss in show:
            print(f"  {iss.compression}/{iss.method}/{iss.video_id}: {iss.detail}")
        if len(issues) > 20:
            print(f"  ... and {len(issues) - 20} more")


def save_issues_csv(report: Report, path: Path) -> None:
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["video_id", "compression", "method", "issue_type",
                     "severity", "detail"])
        for iss in sorted(report.issues, key=lambda i: (i.issue_type, i.compression, i.method, i.video_id)):
            severity = ISSUE_SEVERITY.get(iss.issue_type, "INFO")
            w.writerow([iss.video_id, iss.compression, iss.method,
                        iss.issue_type, severity, iss.detail])


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    faces_root = FACES_ROOT
    csv_path = METADATA_CSV

    if not csv_path.exists():
        print(f"ERROR: Metadata CSV not found at {csv_path}")
        sys.exit(1)
    if not faces_root.exists():
        print(f"ERROR: Faces root not found at {faces_root}")
        sys.exit(1)

    print(f"Metadata CSV:  {csv_path}")
    print(f"Faces root:    {faces_root}")
    print()

    report = Report()

    # Load expected videos
    print("Loading expected videos from metadata CSV...")
    expected = load_expected_videos(csv_path)
    total_expected = sum(len(v) for v in expected.values())
    print(f"  {total_expected} expected video extractions across "
          f"{len(expected)} (compression, method) groups")

    # Scan extracted directories
    print("Scanning extracted face directories...")
    extracted = scan_extracted(faces_root)
    total_extracted = sum(len(v) for v in extracted.values())
    print(f"  {total_extracted} extracted video directories found")

    # Initialize stats for all expected groups
    for key, ids in expected.items():
        report.stats[key] = MethodStats(expected=len(ids))

    # Also track groups that exist on disk but aren't in CSV
    for key in extracted:
        if key not in report.stats:
            report.stats[key] = MethodStats()

    # Check 1: Coverage
    print("\nCheck 1/6: Video-level coverage...")
    check_coverage(expected, extracted, report)

    # Checks 2-4, 6: Per-video
    print("Check 2-4,6: Per-video checks (yield, markers, integrity, spatial)...")
    n_videos = sum(len(v) for v in extracted.values())
    checked = 0
    for (comp, method), videos in sorted(extracted.items()):
        st = report.stats.get((comp, method))
        if st is None:
            st = MethodStats()
            report.stats[(comp, method)] = st

        for vid, vdir in sorted(videos.items()):
            check_video(vdir, comp, method, report, st)
            checked += 1
            if checked % 2000 == 0:
                print(f"  ... checked {checked}/{n_videos} videos")

    print(f"  ... checked {checked}/{n_videos} videos")

    # Check 5: Cross-compression consistency
    print("Check 5/6: Cross-compression consistency...")
    check_cross_compression(extracted, report)

    # Print report
    print()
    print_report(report)

    # Save detailed issues CSV
    if report.issues:
        issues_csv = faces_root / "extraction_issues.csv"
        save_issues_csv(report, issues_csv)
        print(f"\nDetailed issues saved to: {issues_csv}")


if __name__ == "__main__":
    main()
