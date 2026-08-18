# cafrl-negative — reproducibility artifacts

Artifacts for **Data Diversity, Not Frequency Invariance: A Controlled and Self-Audited Study of Compression-Robust Deepfake Detection** — IEEE Access, under submission.

The paper reports a negative result: a compression-aware frequency-learning
architecture (CAFRL) does not beat a plain spatial backbone of matched capacity
trained on the same multi-compression data, and the compression robustness both of
them show comes from the training data rather than from the frequency machinery.
A negative result is only worth anything if a stranger can check it, so this
repository exists to let you check it: every number the paper prints can be
recomputed from the per-video model scores released here, under decision rules
that were frozen before the runs they adjudicate.

> **Status.** This repository is being assembled for submission. Directories with
> a `STATUS.md` are not yet populated — see *What is not here yet* below.
> Last built 2026-08-18.

## What is here

| directory | contents |
|---|---|
| `predictions/` | Per-video scores, labels and evaluation statistics for every reported cell: 49 files covering 27 runs, 200 cells with full per-video detail. Gaps are listed in `predictions/GAPS.md`. |
| `preregistration/` | The frozen STOP-gate and win-rule texts, the tagged commit's content, the decision rules of every audit re-test, and the commit/artifact timeline that places each rule before the runs it governed. |
| `configs/` | The effective as-run configuration of all 27 released runs, 34 launch overrides (including arms that were specified and deliberately never run), the base configuration, and `RUNS.md` — the index mapping each run to its model, protocol, augmentation policy, seed, launch command and role in the manuscript. |
| `splits/` | 12 evaluation-set video-ID lists: FF++ test at each of seven compression levels, the held-out FaceShifter cell, Celeb-DF v2, and DFD — plus the official FF++ split files. |
| `LICENSE`, `LICENSE-DATA` | MIT for code; CC BY 4.0 for predictions, splits, rule texts and metadata. Read `LICENSE-DATA` before regenerating crops: derived imagery inherits the source datasets' agreement terms. |

## What is not here yet

`evaluation/`, `pipeline/`, `figures/` and `audit/` are placeholders; each carries a
`STATUS.md` saying what will land in it. The environment lockfile and the
end-to-end `verify` script are part of the same wave. Until they land, the
predictions and rule texts stand on their own: they are the raw material, not the
derivations.

## What is deliberately not here

**No dataset media, ever.** FaceForensics++, DeepFakeDetection (distributed
through the FaceForensics++ infrastructure) and Celeb-DF v2 are obtained under
signed end-user agreements, and none of them permits redistributing videos or
derived imagery. What this repository gives you instead is everything needed to
rebuild the evaluation inputs from data you obtain yourself: the video-ID lists,
the per-video crop coordinates (in the archival deposit), and the re-encode and
cropping pipeline. Crops are a deterministic function of source video plus stored
coordinates — regenerating them reproduces the original crops exactly.

**No model weights in git.** The trained checkpoints (~6.5 GB) ship in the
archival deposit alongside the crop coordinates.

Archival deposit: **to be assigned before publication**

## Reproduction contract

Reproduction means different things at different layers, and the paper's claim of
bit-exactness applies to one of them. Precisely:

1. **Re-deriving the reported numbers from released predictions.** Every table
   cell, contrast, confidence interval and bootstrap in the paper is a function of
   the per-video scores in `predictions/` and nothing else. This is exact and
   costs no GPU: the released scores reproduce each cell's stored video-AUC, and
   the build fails if they do not — 69 manuscript-printed values are
   checked against the released artifacts on every build. The bootstrap is seeded,
   so its intervals reproduce identically.

2. **Regenerating predictions by re-running a released checkpoint.** This requires
   the crops, and is subject to the numerics of your GPU, driver and framework
   build. Training and evaluation used bfloat16 mixed precision with float32
   islands in the frequency and loss paths, so expect small run-to-run differences
   in scores rather than bit-identity. Do not read a difference in the fifth
   decimal of an AUC as a discrepancy.

3. **Re-training a run from its configuration.** Bit-exact re-training is only
   attainable under the deterministic mode (`--deterministic`), which forces
   float32 and single-threaded data loading; under the production recipe
   (bfloat16, multi-worker loading) an interrupted-and-resumed run diverges by up
   to 4e-3 in loss, which is fine for crash recovery and not a reproduction
   guarantee. Across independent seeds the honest expectation is the
   between-seed variation the paper reports: at the heaviest compression level,
   the across-seed standard deviation of video-AUC is about 0.6 points for the
   spatial backbone and about 0.25 points for the fair CAFRL variants. Any
   single-seed difference smaller than that is noise, which is why the paper's
   headline contrasts are three seeds against three seeds.

Layer 1 is the one the paper's claims rest on and the one this repository makes
independently checkable today.

## How the predictions are organised

One JSON per run per evaluation set. Each cell carries the reported statistics and
four parallel arrays — `video_id`, `method`, `label`, `score` — in the original
evaluation order.

That order is the pairing contract. The paper's inter-arm test is a paired
video-resampling bootstrap: each of 10,000 replicates draws **one** shared
video-index vector and scores both arms with it, so position *i* of one run's
`score` array and position *i* of another's refer to the same video. Every
released run was evaluated on the same ordered video list, which the build
verifies run by run; `keys_sha256` pins it in both the prediction file and the
matching file in `splits/`.

Pooling: a video's score is the mean over its 32 uniformly spaced sampled frames,
and the pooling key is the pair `(video_id, method)` so one source video appearing
under several manipulations stays distinct. Labels are `1` for fake throughout.

## On the word "pre-registered"

The paper says the decision rules were frozen before the runs they governed. That
claim is made precise here rather than left to trust.

`preregistration/` contains the rule texts verbatim — the STOP-gate that halted
the campaign, the win-rule that would have adjudicated the ablation bake-off, and
the decision rule of every audit re-test — together with the content of the git
tag that froze the win-rule and a timeline (`history-excerpts.md`) pairing each
rule document's first commit with the timestamps of the run artifacts it governs.

What this is not: registration with a third party. The research repository was
private during the campaign, so the ordering evidence is author-controlled version
history, not a registry's timestamp. We publish the rules and the history in full
and say plainly which part rests on our records. Note also what the rules
themselves make verifiable: the win-rule is computed post-hoc on saved
checkpoints, and it is written symmetrically, so it was capable of declaring the
authors' own preferred mechanism the loser. It did.

## Citing this release

Cite the paper. If you use the predictions or the split lists directly, please
also cite the archival deposit (to be assigned before publication).

```
Abbas Aliyev and Samir Rustamov. Data Diversity, Not Frequency Invariance: A Controlled and Self-Audited Study of Compression-Robust Deepfake Detection. IEEE Access, 2026.
Artifacts: https://github.com/Capta1n-n9m0/cafrl-negative
```

## Contact

Issues and questions: https://github.com/Capta1n-n9m0/cafrl-negative/issues
