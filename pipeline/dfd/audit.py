"""Audit DFD extraction: coverage, markers, c23/c40 consistency, integrity, backups."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from index import build_index  # noqa: E402

FACES = Path.home() / "sdb/datasets/ff++/faces"
BACKUP = Path("${HOME}/sdc/datasets/dfd_singleface_backup")
COMPS = ["c23", "c40"]


def dir_ok(d: Path) -> tuple[bool, int, bool]:
    """returns (has_done_and_trackfix, png_count, meta_count_matches)."""
    if not (d / ".done").exists() or not (d / "meta.json").exists():
        return False, 0, False
    try:
        meta = json.loads((d / "meta.json").read_text())
    except Exception:
        return False, 0, False
    tf = bool(meta.get("processing", {}).get("track_fix"))
    npng = len(list(d.glob("*.png")))
    matches = npng == meta.get("num_frames_extracted", -1)
    return tf, npng, matches


def main() -> None:
    idx = build_index()
    reals = idx.all_reals
    fakes = [f.stem for f in idx.all_fakes()]
    print(f"expected: {len(reals)} reals, {len(fakes)} fakes\n")

    issues: list[str] = []
    for kind, method, names in (("real", "actors", reals),
                                ("fake", "DeepFakeDetection", fakes)):
        present = {c: 0 for c in COMPS}
        trackfix = {c: 0 for c in COMPS}
        mismatch_meta = 0
        cross_mismatch = 0
        total_png = {c: 0 for c in COMPS}
        for name in names:
            counts = {}
            for c in COMPS:
                d = FACES / c / method / name
                if not d.exists():
                    issues.append(f"MISSING {c}/{method}/{name}")
                    continue
                present[c] += 1
                tf, npng, mm = dir_ok(d)
                if tf:
                    trackfix[c] += 1
                if not mm:
                    mismatch_meta += 1
                    issues.append(f"META-MISMATCH {c}/{method}/{name}")
                counts[c] = npng
                total_png[c] += npng
            if len(set(counts.values())) > 1:
                cross_mismatch += 1
                issues.append(f"C23!=C40 {method}/{name}: {counts}")
        print(f"[{kind}] {method}")
        for c in COMPS:
            print(f"   {c}: present={present[c]}/{len(names)} "
                  f"track_fix={trackfix[c]} png_total={total_png[c]}")
        print(f"   meta-count mismatches: {mismatch_meta} | c23!=c40: {cross_mismatch}")

    # backups: old fakes should have moved to sdc
    nb = {c: len(list((BACKUP / c / "DeepFakeDetection").glob("*/"))) for c in COMPS}
    print(f"\nbackup fake dirs on sdc: {nb}")

    print(f"\nTOTAL ISSUES: {len(issues)}")
    for i in issues[:20]:
        print("  ", i)
    if len(issues) > 20:
        print(f"   ... and {len(issues) - 20} more")


if __name__ == "__main__":
    main()
