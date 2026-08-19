# `evaluation/` — the harness that produced and re-derives the numbers

Every figure in the paper that is not a diagram, and every table cell drawn from
FaceForensics++, is a function of the per-video scores in `predictions/` and of
the code in this directory. That code is not a re-implementation written for the
release: `src/` is the campaign's own evaluation package, copied file for file,
with its complete import closure so it runs on its own.

```
evaluation/
├── src/               the harness, verbatim (19 files, full import closure)
├── release_io.py      release-only: reads predictions/*.json into the shape src/ expects
├── rederive.py        recomputes the paper's tables and writes them out
├── CALIBRATION.md     published-anchor calibration of the three literature-protocol
│                      baselines + the F3-Net/FreqNet adaptation choices (the
│                      material the paper's Appendix C points here for)
└── analysis/          the statistics added in revision (equivalence, MDE,
                    cluster and two-level bootstraps, multiplicity) + their outputs
```

## Re-derive the tables

```bash
conda env create -f ../env/environment-verify.yml   # CPU only, ~5 packages
conda activate cafrl-verify
python rederive.py --out ../verify/out --jobs 4
```

This reads only `../predictions/`, takes a few minutes (the bootstrap dominates),
and needs no GPU, no dataset and no network. To check the output against what the
manuscript prints, run `../verify/verify.py` instead — same computation, plus the
comparison and a pass/fail summary.

## What each module does

| file | role |
|---|---|
| `src/__init__.py` | package marker |
| `src/config/__init__.py` | package exports |
| `src/config/defaults.py` | the dataclass configuration definitions |
| `src/config/load.py` | YAML override loading and config serialisation |
| `src/data/__init__.py` | package marker |
| `src/data/celebdf_faces.py` | the Celeb-DF v2 evaluation dataset |
| `src/data/constants.py` | level/method/label constants |
| `src/data/dfd_faces.py` | the DFD evaluation dataset |
| `src/data/ffpp_faces.py` | the FF++ evaluation dataset |
| `src/data/frame_select.py` | the 32-frame uniform selection rule |
| `src/data/index.py` | the per-level crop indexes |
| `src/data/sample_spec.py` | the sampling specification |
| `src/data/splits.py` | official FF++ split loading |
| `src/data/transforms.py` | evaluation-time preprocessing |
| `src/evaluation/__init__.py` | package exports |
| `src/evaluation/aggregate_runs.py` | seed pooling by video key, per-arm summaries, and the frozen four-criterion win rule |
| `src/evaluation/aggregation.py` | frame→video pooling strategies (mean pool, per-identity max) |
| `src/evaluation/evaluator.py` | the GPU evaluation pass that produced the released scores (needs crops and a checkpoint; not used to re-derive tables) |
| `src/evaluation/metrics.py` | video-AUC, the 10k paired video bootstrap with shared index vectors, marginal bootstrap CIs, AUC_comp, the CRF slope, and the seed band (with the k≠3 t-quantile fix) |

`evaluator.py` is the only module that needs a GPU and the face crops: it is the
pass that turned checkpoints into the scores in `predictions/`. It is included so
that the path from a released checkpoint back to a released score is auditable,
not because re-deriving the tables requires it.

## The statistics, in one place

* **Video-level AUC.** Frame scores are mean-pooled per video (32 uniformly
  spaced frames), then ranked. The pooling key is `(video_id, method)`, so one
  source identity appearing under several manipulations contributes several
  distinct videos. `predictions/` ships scores that are already pooled; pooling
  them again is a no-op, which is why the released arrays reproduce each cell's
  stored AUC exactly.
* **Paired video bootstrap** (`metrics.paired_auc_delta`). The inter-arm test:
  10,000 replicates, each drawing *one* video-index vector that scores **both**
  arms, so the arms' shared error is differenced away. The reported interval is
  the 95% percentile interval of the 10,000 deltas. Replicates that resample a
  single class are redrawn, and the redraw is shared. Against itself an arm gives
  a delta of exactly 0 in every replicate — a correctness invariant the harness's
  tests assert.
* **Marginal CIs** (`metrics.bootstrap_ci`). Per-arm intervals, resampling
  videos. They are reported for cells that have no paired comparator; they are
  *not* the inter-arm test, because CI overlap between correlated arms manufactures
  false nulls.
* **Seed pooling** (`aggregate_runs.seed_pool_level`). An arm's seeds are aligned
  by video key and averaged per video; the pooled arrays are returned in sorted-key
  order. Pooled contrasts in the paper are that pooled vector against the
  comparator's, through the same paired bootstrap.
* **Seed bands** (`metrics.seed_band`). Mean ± *t*<sub>.975,k−1</sub>·s/√k with the
  seed as the experimental unit. For k=3 the multiplier is the pre-registered
  4.30 (kept bit-identical to the frozen rule); other k use the correct quantile
  for their degrees of freedom, which is the D8 fix — the earlier code used 4.30
  for every k.
* **CRF slope** (`metrics.crf_slope`). Least-squares slope of video-AUC against
  CRF across the sweep.

## Reproducibility of the intervals

The bootstrap is seeded (RNG seed 0) and its input order is fixed (sorted pooling
key), so its intervals are reproducible to the digit rather than only in
distribution. Change the order or the seed and the interval moves in its last
decimal — that is Monte-Carlo noise, not disagreement. `verify/` states the
tolerance it applies and why.
