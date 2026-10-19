# cafrl-negative — reproducibility artifacts

Artifacts for **A Controlled Audit of a Negative Result: Training Recipe, H.264 Compression Levels and a Frequency-Stream Deepfake Detector** — under review at IEEE Access (revision 1).

This controlled, self-audited study tests one frequency-based design for
compression-robust deepfake detection: CAFRL, which adds block-DCT and
FFT-phase streams with compression-conditioned band attention, and an
adversarial compression-invariance loss, to an EfficientNet-B0 face backbone.

Five separate findings follow. (1) Under the registered rule, CAFRL as specified scored
3.66 AUC points below a backbone-matched EfficientNet-B0 at CRF 40 (paired,
one seed). (2) After the audit found eight defects, the control's training
recipe recovered 3.96 points for CAFRL's own components (post-audit
pre-specified); in a one-seed ablation reverting changes singly, only the
backbone learning rate gave an interval excluding zero. (3) At that recipe,
these untuned frequency-stream implementations showed no detectable
difference from the spatial controls at two feature widths (post-audit
pre-specified), yet a standalone frequency head scored 85.27 test-split AUC points at
CRF 40 at the selected checkpoints (exploratory). (4) Restoring the
adversarial loss at that recipe made no detectable difference in a
registered test (0.87 points, Holm-adjusted p = 0.084); the estimator stayed
accurate at the selected checkpoints. (5) In registered three-seed tests,
real H.264 training levels beat PSNR-matched JPEG versions of the same
frames by 7.48 points at CRF 40 (averaged over CRF-40 exposure), and
CRF-40-level data added 1.88 points averaged over codec; flat robustness was
measured within the trained levels. CAFRL numbers use EMA weights.
Evidence: FaceForensics++-family, GAN-era, single-pass H.264 compression.

A negative result is only worth anything if a stranger can check it, so this
repository exists to let you check it: the numbers the paper prints are
recomputed from the per-video model scores released here or read back from
shipped analysis outputs, under decision rules that were frozen before the runs
they adjudicate; four cannot be re-derived (see *Reproducibility tiers* below).

> **Status.** Version 2.0.1, released with the revised manuscript (revision 1).
> `RELEASE-NOTES.md` lists every change from v1.0.0 and the reviewer comment
> behind it, and the corrections of v2.0.1. Every directory of the layout carries content; the handful of numbers
> this release cannot re-derive are named individually in `CLAIMS-MAP.md` and
> summarized under *What is not here yet* below. Last built 2026-10-19.

## Check it yourself

```bash
conda env create -f env/environment-verify.yml   # CPU only, six packages
conda activate cafrl-verify
python verify/verify.py --jobs 4
```

A few minutes later you have a pass/fail line for every number the paper prints
that this repository can check: 64 table cells, recomputed from the
released per-video scores where those were written and read back from the
stored statistic where they were not, the derived means and gaps, and the 20
adjudicated contrasts re-run through the same 10,000-replicate paired bootstrap
the paper used. The same run also checks the numbers the revision added, listed
in `CLAIMS-MAP-R1.md`, by recomputing or reading back each one; *Reproducibility
tiers* below says which. No GPU, no dataset, no network. `verify/README.md` explains
the tolerances and why they differ between the deterministic and the resampled
quantities.

## What is here

| directory | contents |
|---|---|
| `predictions/` | Per-video scores, labels and evaluation statistics for every reported cell: 776 files covering 53 runs, 1316 cells with full per-video detail. Gaps are listed in `predictions/GAPS.md`. |
| `preregistration/` | The frozen STOP-gate and win-rule texts, the tagged commit's content, the decision rules of every audit re-test, and the commit/artifact timeline that places each rule before the runs it governed; for the revision campaign, its registration (`PREREGISTRATION-R1.md`), the content of the tag `phase6-prereg` and its timeline (`history-excerpts-r1.md`). |
| `configs/` | The effective as-run configuration of all 53 released runs, 60 launch overrides (including arms that were specified and deliberately never run), the base configuration, and `RUNS.md` — the index mapping each run to its model, protocol, augmentation policy, seed, launch command and role in the manuscript. |
| `splits/` | 12 evaluation-set video-ID lists: FF++ test at each of seven compression levels, the held-out FaceShifter cell, Celeb-DF v2, and DFD — plus the official FF++ split files. |
| `evaluation/` | The evaluation harness that produced the scores and re-derives every statistic from them — 20 files copied from the research code with their full import closure, plus a loader for the released prediction files and a script that rebuilds the paper's tables. |
| `evaluation/analysis/` | The statistics added in revision, as runnable scripts and as their outputs: equivalence tests against a stated margin, minimum detectable effect, a cluster bootstrap at four exchangeability units, a two-level seed×video bootstrap, and multiplicity adjustment over the contrast family. |
| `curves/` | Per-epoch validation curves for all 53 runs and their selection outcomes: which epoch each reported checkpoint is, under which rule, and the whole trajectory that rule chose from. |
| `pipeline/` | How the evaluation inputs were made: the multi-CRF re-encode with its exact command line and encoder build, the face detection / track curation / deterministic re-crop code, and the DFD track-selection pipeline. |
| `figures/` | The figure script, the data it draws (rebuilt from `predictions/` and `curves/` on every release build), and the TikZ sources for the two diagrams. |
| `env/`, `environment.yml` | The environment the numbers were produced in — 141 conda and 74 pip packages pinned by version and build — plus a six-package CPU-only subset for checking the tables. |
| `audit/` | The self-audit that tried to kill this paper's own result: the four review passes as they were scoped, the checks they ran, the complete D1–D8 ledger with each defect's closure — and an explicit statement of what "independent" does and does not mean here. |
| `probes/` | The small design-time measurements the paper cites but no training run produces: the compression estimator's accuracy, the parameter counts, the band-energy premise. |
| `verify/` | The check described above, `expected.json` (what the paper prints, in machine-readable form), and `claim.py` — the per-claim version of the same check. |
| `revision-1/` | The analysis outputs the revised manuscript prints: the registered campaign's confirmatory and secondary statistics, the registered minimum detectable effects and ladder statistics, the exploratory analyses (other corpora, unseen codecs, own re-encodes, raw-weight re-selection, cost, frequency-path diagnostics), the curriculum re-runs, the post hoc re-evaluation of the shipped-recipe FaceShifter cells, and the table sources. In the exploratory files that compare arms (`revision-1/exploratory/e7_dfdc.json`, `e7_wdf.json`, `e8.json`, `e9.json`, `e12.json` and the `rev1/` copies), the contrast keys `D1`–`D6` are the contrasts the Supplementary Material labels X1–X6 (D1 = X1, …, D6 = X6); they are not the audit defects D1–D8. |
| `code/` | `code/ema-own-bn-stats/`: the research code's EMA batch-norm flag used by one curriculum re-run, with its tests — a record of the change, not a standalone package (its README says how far the tests run from here). |
| `CLAIMS-MAP.md` | One row per manuscript table cell, per load-bearing number in the text, and per present-tense claim this paper makes about this repository — each with the artifact it comes from and how it is checked (recomputed, read back, or why it cannot be; see *Reproducibility tiers*). Generated and re-checked on every build. |
| `CLAIMS-MAP-R1.md` | The same, for every number the revision added to the paper or its Supplementary Material, with the artifact and the command behind it. |
| `RELEASE-NOTES.md` | What changed from v1.0.0, each change with the reviewer comment behind it, and what v2.0.1 corrected after a language and consistency check of the revised manuscript. |
| `LICENSE`, `LICENSE-DATA` | MIT for code; CC BY 4.0 (full legal code included) for predictions, splits, rule texts and metadata. Read `LICENSE-DATA` before regenerating crops: derived imagery inherits the source datasets' agreement terms. |

## What is not here yet

Four entries the paper prints cannot be re-derived from this release at all —
the 95 % intervals and P(Δ>0) of the shipped-recipe held-out-manipulation table
(c23 and c40), the Xception held-out-manipulation comparison, and the campaign's
GPU-hour accounting; `CLAIMS-MAP.md` names each one and says why. Cells whose own
per-video scores were never saved (audit defect D8) are listed in
`predictions/GAPS.md`, with what the release holds for each instead. Every
other directory of the layout carries content.

## What is deliberately not here

**No dataset media, ever.** FaceForensics++, DeepFakeDetection (distributed
through the FaceForensics++ infrastructure) and Celeb-DF v2 are obtained under
signed end-user agreements, and none of them permits redistributing videos or
derived imagery. What this repository gives you instead is everything needed to
rebuild the evaluation inputs from data you obtain yourself: the video-ID lists,
the per-video crop coordinates (in the archival deposit), and the re-encode and
cropping pipeline. Crops are a deterministic function of source video plus stored
coordinates — regenerating them reproduces the original crops exactly.

**No model weights in git.** The trained checkpoints ship in the archival
deposit alongside the crop coordinates: the 37 files (6.0 GB) of v1.0.0, carried
unchanged, plus the selected `best.pt` of each of the 26 Revision-1 runs. The
revision adds no crop coordinates.

Archival deposit: **10.5281/zenodo.23484150**

## Reproducibility tiers

What each reported value needs to be rebuilt. Table and figure numbers are
the revised manuscript's; Tables S1–S29 and Fig. S1 are in the
Supplementary Material. `CLAIMS-MAP.md` and `CLAIMS-MAP-R1.md` give the
artifact and method row by row.

**Tier 1: this repository alone (CPU; no dataset, no checkpoint).**
`make verify` (or `python verify/verify.py`) checks every value it can;
`make verify-fresh` runs the same checks in an environment built from the
released lockfile. Each value is checked in one of two ways:

- **Recomputed** from the per-video scores in `predictions/` and the curves
  in `curves/`, with the released harness. This covers 54 table cells
  (check group `cells`), 4 derived means and gaps (`derived`),
  20 adjudicated contrasts re-run through the seeded paired
  bootstrap (`contrasts`), the held-out-manipulation contrasts (`faceshifter`),
  the figures drawn from predictions (`figures`) and 272 rows of
  the two claims maps (`claims-map`). Most of these values are in Tables 1, 2
  and 4, Figs. 2 and 3, Tables S1, S2 and S4 and Table S27.
- **Read back** from a shipped file (2,429 claims-map rows and
  11 values of `cells` and `derived`). Most are the revision's
  statistics: Tables 3, 5 and 6, Tables S5–S20, S25 and S26, Fig. S1 and the
  numbers in the text. The check confirms that each printed number is the one
  in the shipped file, without recomputing it.
  - The others are statistics stored in `predictions/` for evaluations whose
    per-video scores were never written (`predictions/GAPS.md`): the
    cross-dataset AUCs and intervals of Table S3, and the frame-level AUCs,
    intervals and P2 probe AUC of Supplementary Material §S2.
  - Every build re-runs `evaluation/analysis/` from the predictions.
  - The `revision-1/` outputs are shipped as they were computed, without the
    scripts that produced them. Where the per-video scores behind them are in
    `predictions/`, the harness can recompute them; `verify` does not.
  - Some values were recorded at the time rather than computed from scores:
    the timings in Table S16, the bitrates in Table S14 and the validation
    read-outs in Table S10.

The claims maps also hold 12 release claims, checked by confirming that
the files they name are present, and 32 rows that are *recorded* rather
than asserted: the row names its artifact, but no number is compared (prose
claims, approximate glosses, parameter counts printed with a unit).

Four entries cannot be re-derived at all: the intervals and P(Δ>0) of
Table S4, the Xception held-out comparison and the GPU-hour accounting (see
*What is not here yet*).

**Tier 2: regenerated predictions (GPU plus the source videos).** The archival
deposit holds per-video crop coordinates (48,294 records, carried from v1) for
FaceForensics++ at all seven compression levels c0–c40 (held-out FaceShifter
included), DFD at c23 and c40, Celeb-DF v2 and Celeb-DF v1. To rebuild the
predictions:

1. Obtain the videos under each corpus's agreement.
2. Re-encode them (Supplementary Material §S15; `pipeline/crf/`).
3. Regenerate the crops (`pipeline/faces/recrop_faces.py`). They are
   byte-identical to ours.
4. Re-score them with the deposited checkpoints: every `best*.pt` of the v1
   runs, plus the selected `best.pt` of each Revision-1 run.

The new scores match the released ones up to GPU numerics, not bit for bit
(layer 2 below). The deposit holds no per-epoch checkpoints. Scores taken at
another epoch than a run's selected one therefore exist only as shipped
predictions. That covers the raw-weight re-selection (E10, Table S15) and the
symmetric-selection secondary (Section VIII-A).

**Tier 3: predictions only (the corpus plus your own inference).** For these
test sets the release ships per-video predictions but no crop coordinates:

- the DFDC subset (1,000 videos drawn from the DFDC training release) and
  the WildDeepfake test split (E7);
- the track-curated Celeb-DF v2 re-crop (E12);
- the H.265/AV1 re-encodes (E8) and our x264 re-encodes x23/x40 (E9) of the
  FF++ test split.

These sets feed Tables S11–S13, and every number printed for them is in
reproducibility tier 1. To regenerate their predictions, obtain the corpus from its
distributor under its terms, extract the faces or re-encode yourself, and
run inference with the deposited checkpoints. The crops will not be
byte-identical to ours.

## Reproduction contract

Reproduction means different things at different layers, and the paper's claim of
bit-exactness applies to one of them. Precisely:

1. **Re-deriving the reported numbers from released predictions.** Every table
   cell, contrast, confidence interval and bootstrap that `verify` recomputes (see
   *Reproducibility tiers* above) is a function of the per-video scores in
   `predictions/` and nothing else. This is exact and
   costs no GPU: the released scores reproduce each cell's stored video-AUC, and
   the build fails if they do not — 69 manuscript-printed values are
   checked against the released artifacts on every build, and `verify/verify.py`
   repeats the check on your machine. The bootstrap is seeded and its input order
   fixed, so its intervals reproduce to the digit rather than merely in
   distribution.

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
checkable today.

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

Where an arm has several seeds, the paper's pooled contrasts average each video's
score across that arm's seeds before comparing — `evaluation/README.md` states
that and the rest of the statistics precisely.

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
also cite the archival deposit (10.5281/zenodo.23484150).

```
Abbas Aliyev and Samir Rustamov. A Controlled Audit of a Negative Result: Training Recipe, H.264 Compression Levels and a Frequency-Stream Deepfake Detector. IEEE Access, 2026.
Artifacts: https://github.com/Capta1n-n9m0/cafrl-negative
```

## Contact

Issues and questions: https://github.com/Capta1n-n9m0/cafrl-negative/issues
