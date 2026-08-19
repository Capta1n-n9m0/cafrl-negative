"""Run every analysis in this directory, in dependency order.

    python run_all.py --jobs 8

`cluster_bootstrap.py` and `seed_uncertainty.py` do the resampling and write
their distributions' summaries; `equivalence.py`, `mde.py` and
`multiplicity.py` are post-processing over those files and take seconds.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

STEPS = [
    ("cluster_bootstrap.py", ["--self-check"]),
    ("seed_uncertainty.py", []),
    ("equivalence.py", []),
    ("mde.py", []),
    ("multiplicity.py", []),
]
PARALLEL = {"cluster_bootstrap.py", "seed_uncertainty.py"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--predictions", default=None)
    args = ap.parse_args()

    for script, extra in STEPS:
        cmd = [sys.executable, str(HERE / script), *extra]
        if args.predictions:
            cmd += ["--predictions", args.predictions]
        if script in PARALLEL and args.jobs > 1:
            cmd += ["--jobs", str(args.jobs)]
        print(f"\n=== {script} " + "=" * (60 - len(script)))
        rc = subprocess.call(cmd, cwd=HERE)
        if rc != 0:
            return rc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
