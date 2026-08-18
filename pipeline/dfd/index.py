"""DFD index: map every fake to its target real, group fakes by target take.

DFD naming (verified against ffpp_metadata.csv, 0 unmatched / 3068 fakes):
  fake : ``{target}_{source}__{scene}__{rnd}.mp4``   (target = manipulated/"to")
  real : ``{actor}__{scene}.mp4``

The target real for a fake is exactly ``{target}__{scene}.mp4``. One real take
is usually the target of many fakes (median ~8.5), so face-of-interest selection
happens once per (target, scene) group and is inherited by every fake.

This module is the single source of truth for the fake<->target relationship;
detection, selection and extraction all consume :func:`build_index`.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

META = Path("${METADATA_CSV}")

FAKE_RE = re.compile(r"^(\d+)_(\d+)__(.+)__([A-Z0-9]+)$")


@dataclass
class Fake:
    stem: str          # filename without .mp4
    target: str        # actor id whose video/motion is preserved (manipulated)
    source: str        # actor id whose identity is painted in
    scene: str
    rnd: str
    n_frames: int      # c23 frame count (== c40)


@dataclass
class TargetGroup:
    """One real take used as a manipulation target, with all fakes built on it."""
    real_stem: str         # "{target}__{scene}"
    target: str
    scene: str
    n_frames: int          # real take c23 frame count
    fakes: list[Fake] = field(default_factory=list)


@dataclass
class DFDIndex:
    groups: dict[str, TargetGroup]   # real_stem -> group (reals that ARE targets)
    orphan_reals: list[str]          # real_stems never used as a target
    all_reals: list[str]             # every real take stem
    n_fakes: int

    def all_fakes(self) -> list[Fake]:
        return [f for g in self.groups.values() for f in g.fakes]


def _load_rows() -> list[dict[str, str]]:
    with open(META) as fh:
        return list(csv.DictReader(fh))


def build_index() -> DFDIndex:
    rows = _load_rows()

    real_frames: dict[str, int] = {}      # real_stem -> c23 frames
    for r in rows:
        if r["method"] == "actors" and r["compression"] == "c23":
            real_frames[r["filename"][:-4]] = int(r["num_frames"])

    groups: dict[str, TargetGroup] = {}
    n_fakes = 0
    unmatched: list[str] = []
    for r in rows:
        if r["method"] != "DeepFakeDetection" or r["compression"] != "c23":
            continue
        stem = r["filename"][:-4]
        m = FAKE_RE.match(stem)
        if not m:
            unmatched.append(stem)
            continue
        target, source, scene, rnd = m.groups()
        real_stem = f"{target}__{scene}"
        if real_stem not in real_frames:
            unmatched.append(stem)
            continue
        n_fakes += 1
        grp = groups.get(real_stem)
        if grp is None:
            grp = groups[real_stem] = TargetGroup(
                real_stem=real_stem, target=target, scene=scene,
                n_frames=real_frames[real_stem],
            )
        grp.fakes.append(Fake(stem, target, source, scene, rnd, int(r["num_frames"])))

    if unmatched:
        raise RuntimeError(f"{len(unmatched)} fakes did not map to a target real: "
                           f"{unmatched[:5]}")

    all_reals = sorted(real_frames)
    orphan_reals = sorted(set(all_reals) - set(groups))
    return DFDIndex(groups=groups, orphan_reals=orphan_reals,
                    all_reals=all_reals, n_fakes=n_fakes)


def main() -> None:
    idx = build_index()
    fpg = [len(g.fakes) for g in idx.groups.values()]
    import statistics as st
    print(f"target groups (reals used as targets): {len(idx.groups)}")
    print(f"total fakes mapped:                     {idx.n_fakes}")
    print(f"all real takes:                         {len(idx.all_reals)}")
    print(f"orphan reals (never a target):          {len(idx.orphan_reals)} {idx.orphan_reals}")
    print(f"fakes per group: min={min(fpg)} median={st.median(fpg)} max={max(fpg)}")

    if len(sys.argv) > 1 and sys.argv[1] == "--dump":
        out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("dfd_index.json")
        payload = {
            "groups": {
                rs: {
                    "real_stem": g.real_stem, "target": g.target, "scene": g.scene,
                    "n_frames": g.n_frames,
                    "fakes": [vars(f) for f in g.fakes],
                }
                for rs, g in idx.groups.items()
            },
            "orphan_reals": idx.orphan_reals,
            "all_reals": idx.all_reals,
            "n_fakes": idx.n_fakes,
        }
        out.write_text(json.dumps(payload, indent=2))
        print(f"dumped -> {out}")


if __name__ == "__main__":
    main()
