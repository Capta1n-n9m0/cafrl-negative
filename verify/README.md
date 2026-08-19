# `verify/` — checking this release against the paper

The point of the repository is that a stranger can check the paper's numbers
without asking us for anything. This directory is that check, automated.

```bash
conda env create -f ../env/environment-verify.yml
conda activate cafrl-verify
python verify.py --jobs 4          # a few minutes; CPU only
```

It runs entirely inside this repository — no GPU, no dataset, no network — and
prints a CI-style pass/fail line per check.

## What it checks

1. **64 manuscript-printed cell values.** Each is recomputed from the
   released per-video scores through `../evaluation/` and compared with the paper
   at its printed precision. The stored per-cell AUC is checked against the
   recomputed one too, so a tampered score array cannot pass.
2. **5 derived values** — three-seed means and the real-CRF-versus-JPEG gap.
3. **8 adjudicated contrasts** — the paper's headline table, recomputed
   end to end: seeds pooled by video key, then a 10,000-replicate paired video
   bootstrap (RNG seed 0).
4. **Figure regeneration** — the prediction-driven figures are rebuilt from
   `../predictions/` and `../curves/` and their inputs compared against the
   released `figures/figure_data.json`.
5. **Self-containment** — after everything has run, the check inspects which files
   its own modules were imported from and fails if any of them came from outside
   this repository.

## Tolerances, and why they differ

Deterministic quantities — AUCs, means, differences — must match the manuscript
at **printed precision**: half a unit in the last digit the paper prints. There is
no slack; they are exact functions of the released scores.

Bootstrap quantities — the deltas and their intervals — are Monte-Carlo estimates.
They are reproducible to the digit *given the same input order and RNG seed*,
which is why both are pinned here, and the checks are run at the same settings the
paper used. Each quantity is still allowed the looser of the manuscript's own printed
precision and a Monte-Carlo budget: 0.0005 for the point estimate, which is
stable at ten thousand replicates and does reproduce the published values, and
0.001 for the interval endpoints, which wobble at roughly half that. One
endpoint in the published contrast table — the lower bound of the STOP-gate row —
recomputes 0.0005 away from its printed value for exactly this reason; nothing
else in the table differs at all. A check that fails these tolerances is a real
disagreement, not rounding. The verdict (does the interval exclude zero) is
checked separately and admits no tolerance.

One contrast is deliberately asymmetric, and `expected.json` says so where it is
defined: the architecture-share row compares the single frozen backbone run with
the three-seed pool of the trunk control, which is what the rule that adjudicated
it specified. Averaging scores across seeds is an ensemble and lifts whichever
side receives it, so the asymmetry is recorded rather than quietly evened out.

`expected.json` is the machine-readable form of everything the paper prints that
this repository can check, generated from the release manifest. Reading it
alongside the claims map (`../CLAIMS-MAP.md`) tells you
which artifact stands behind which cell.
