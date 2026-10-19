# Release notes

## v2.0.1 — corrections to the revised manuscript

This version goes with the corrected revised manuscript. After v2.0.0 was
released, a language and consistency check of the manuscript and its
Supplementary Material found unclear wording, labels used for two different
things, and one misprinted number. The manuscript was corrected and frozen again.
No result changed. No data, run, checkpoint, per-video prediction, analysis
output or statistic of v2.0.0 changed, and every number the paper prints keeps
its value except one misprint in the text (item 1), whose source values are
unchanged.

Archival deposit of this version: **10.5281/zenodo.23484150** (version DOI).
The v2.0.0 deposit (DOI 10.5281/zenodo.23466627) and the v1.0.0 deposit
(DOI 10.5281/zenodo.22032529) stay published unchanged.

### Changed

1. **`evaluation/OOD-PROTOCOL.md`**: "the 0.4-point spread the same arm shows at
   FaceForensics++ c40" now reads "0.5-point spread". Fair-N's three c40 video
   AUCs are 0.9586, 0.9567 and 0.9536 (Supplementary Material, Table S1): a
   spread of 0.0050, that is 0.5 points. The values did not change; the text
   misprinted their spread.
2. **`evaluation/CALIBRATION.md`**: "land 3.5 and 4.7 frame-AUC points below it
   at c40" could be read as "below the c23 anchor". The two detectors land that
   far below their c40 anchor, and the sentence now says so, as the
   Supplementary Material does. Same numbers.
3. **`README.md`**: the summary paragraph follows the corrected abstract ("Five
   separate findings follow."). The `revision-1/` entry adds a note: the
   Supplementary Material now labels its six exploratory contrasts X1–X6, so
   that they no longer share labels with the audit defects D1–D8. The JSON keys
   of the exploratory files keep the names `D1`–`D6` (D1 = X1, …, D6 = X6).
4. **`figures/fig3_campaign_flow.tex`** (Fig. S1 of the Supplementary Material):
   the figure names four of the six arm families, so it now marks them as
   examples ("e.g."), and "vs" is written "vs.". The figure was rebuilt from
   this source; it shows the same numbers.
5. **`CLAIMS-MAP.md`, `CLAIMS-MAP-R1.md` and their JSON files in `verify/`**:
   regenerated against the corrected manuscript; they record its new SHA-256.
   The Revision-1 map gains 9 rows, one per number of the corrected text that
   it did not yet check (the five values of the corrected sentence on trunk
   scale, the 0.5-point spread, the 1.32 M discriminator, the 10,000 bootstrap
   replicates and the 53 released runs), so `make verify` now passes 2879
   checks instead of 2870.
6. **Parameter counts**: the `CLAIMS-MAP.md` label of CAFRL's 10.65 M count and
   the comment in `probes/param_counts_arms.py` now use the paper's wording: the
   counts include CAFRL's 1.32 M discriminator, which the prediction does not
   use (10.65 M without it). The discriminator still runs in every forward
   pass, evaluation included; the prediction does not use its output. No count
   changed.

### Deposit

The v2.0.1 Zenodo version keeps every file of the v2.0.0 version unchanged:
`checkpoints.tar` (the 37 checkpoints of the 27 v1.0.0 runs) and its manifest,
`crop-coordinates.tar.zst`, and the 26 per-run `<run>.best.pt` files of the
Revision-1 runs with their manifest. Three files differ: the source tarball
`cafrl-negative-v2.0.1.tar.gz` takes the place of `cafrl-negative-v2.0.0.tar.gz`
(which stays in the v2.0.0 record), and `README-DEPOSIT.md` and `SHA256SUMS` are
written for this version. It adds no checkpoints and no crop coordinates.

## v2.0.0 — the revised manuscript (IEEE Access, revision 1)

This version goes with the revised manuscript, *A Controlled Audit of a Negative
Result: Training Recipe, H.264 Compression Levels and a Frequency-Stream Deepfake
Detector*. The revision answers one round of peer review. Every entry below names
the reviewer comment behind it as a ledger ID: `AE.1` is the associate editor,
`R1.n` and `R2.n` are comments of reviewers 1 and 2, numbered in reading order.
Where a v1.0.0 value or text changed, the entry also names the decision
that changed it (date and title).

Archival deposit of v2.0.0: 10.5281/zenodo.23466627 (version DOI).
The v1.0.0 deposit, DOI 10.5281/zenodo.22032529, stays published unchanged.

Nothing in v1.0.0 was removed. The v1.0.0 files that changed are listed under
*Changed* with the reason; every other v1.0.0 file is byte-identical.

### Which weights

CAFRL-family arms (CAFRL as specified, Fair-N, Fair-W, E1, the E13 ablations, the
curriculum re-runs) are scored on their exponential-moving-average (EMA) weights
unless a file says otherwise. Spatial controls and baselines train no EMA and are
scored on their raw weights. Files ending `_raw_atsel`, `_raw_best` and
`_raw_reselected` hold raw-weight scores of CAFRL-family arms, at the EMA-selected
epoch, at the best raw epoch, and under raw-weight re-selection.

### Added

1. **The registered revision campaign: 18 runs** (configs, per-epoch curves,
   per-video predictions). E1, the adversarial invariance loss at the fair recipe
   (`r1_fairn_grl_*`, 3 seeds; R1.2, R2.1). E2, the control trained without the
   heaviest levels (`r1_sb_noc40_*`, `r1_sb_noc36c40_*`; R1.36, R2.2). E3, the
   control trained on JPEG versions of the same frames (`r1_sb_jpeg_all_*`,
   `r1_sb_jpeg_noc40_*`; R2.3). The c23-only anchor (`r1_sb_c23only_*`; R1.36).
   The registration they ran under: `preregistration/PREREGISTRATION-R1.md`, the
   content of the tag `phase6-prereg` and its timeline `history-excerpts-r1.md`
   (R1.35, R1.46).
2. **The one-seed recipe ablation E13: 5 runs** (`r1_abl_*_s42`; R1.23), tier
   descriptive.
3. **The three curriculum re-runs V1–V3** (`r1x_abl_curriculum_{rerun,nostop,emafix}_s42`),
   with per-video predictions for all three weight sets (EMA, raw at the selected
   epoch, raw best) and their configs (`configs/launch-r1x/`). V1 is the identical
   re-run of the stopped curriculum arm and is the canonical curriculum run; V2
   and V3 are post hoc. Decision 2026-10-17 "C2b: the supplement names the EMA
   fix, and the release gains the V1–V3 files" (R1.23).
4. **`code/ema-own-bn-stats/`**: the EMA batch-norm flag `train.ema_own_bn_stats`
   (on only in V3) and its tests, as a record of the change (same decision).
5. **Exploratory predictions, predictions only**: DFDC subset and WildDeepfake
   (E7; R2.7), Celeb-DF v2 re-cropped (E12; R1.39), unseen codecs and our own
   re-encodes of the FF++ test split (E8, E9; R2.2, R1.20), and raw-weight
   re-selection of the CAFRL-family arms (E10; R2.8). No frames, crops or crop
   coordinates of these data are released (decision 2026-10-18 "W6: the Zenodo v2
   deposit adds the new best checkpoints, not new crops").
6. **`revision-1/`**: the analysis outputs the revised manuscript prints — the
   confirmatory tests T1–T5 of E1–E3 and the secondary analyses (`stats/`; R1.2,
   R2.1, R1.36, R2.3),
   with a strict-JSON twin `secondaries.null.json` beside the original (every bare
   NaN is null, every other value identical; decision 2026-10-16 "C2:
   secondaries.json gets a strict-JSON twin; small items"); the registered minimum
   detectable effects and ladder statistics (`registered/`; R1.32); the
   exploratory analyses (`exploratory/`: cost, R1.10; frequency-path diagnostics,
   R1.26, R1.27, R1.28; ladder and codec statistics, R1.20, R2.2); the table
   sources (`tables/`: tensor shapes, R1.15); the post hoc re-evaluation of the
   shipped-recipe FaceShifter checkpoints (`faceshifter-shipped/`, EMA weights as
   published; R1.42); the curriculum record (`curriculum/`); and the point
   estimates and seed-resampled intervals of the original contrasts
   (`point-estimates.json`, `recompute.json`; R1.42, R1.31, R1.34). The outputs
   are shipped as they were computed, without the scripts that produced them
   (decision 2026-10-19 "W6 ruling: the Revision-1 analysis scripts are not
   shipped in v2.0.0").
7. **`CLAIMS-MAP-R1.md`** and `verify/claims_map_r1.json`: every number the
   revision added to the paper or its Supplementary Material, mapped to an
   artifact and a command, and checked by `verify/verify.py` like the v1 rows.
   This includes the numbers printed in Fig. S1 and in the graphical abstract
   (R1.21). The minimum-detectable-effect rows read `revision-1/registered/mde.json`.
8. **Harness additions**: `evaluation/src/data/jpeg_levels.py` and the off-by-default
   options the E2/E3 runs need. Default options reproduce the old code bit for bit
   (decision 2026-10-10 "Phase 6 build: default options must reproduce the old
   code bit for bit").
9. **This file.**

### Changed

1. **Every Δ is a point estimate** (the un-resampled difference, not the bootstrap
   mean). Intervals and P values are unchanged. Decision 2026-10-17 "W4a-1 ruling:
   every Δ is printed as a point estimate" (R1.42). Values in `verify/expected.json`
   and `CLAIMS-MAP.md`: T3.4 +0.0056 → +0.0055; T3.5 −0.0010 → −0.0009; T3.8
   +0.0490 → +0.0489; AppC.31 −0.0040 → −0.0039; AppC.32 −0.0804 → −0.0803;
   X1.13 −0.0318 → −0.0317; X1.14 +0.0220 → +0.0222; X1.15 −0.0227 → −0.0226;
   AppC.34 −0.0002 → −0.0001 and AppC.35 −0.0493 → −0.0492, both now checked
   (were recorded); AppC.36 unchanged, now checked. The three interval endpoints
   +0.0068, −0.0543 and −0.0671 stay as published (decision 2026-10-18 "W4a-2
   ruling: published numbers stay where nothing new can be derived"). The
   Fair-N/Fair-W numbers here use EMA weights. `verify/` now checks each Δ at the
   printed precision, so the tolerance key `bootstrap_delta_abs` is removed;
   `bootstrap_ci_abs` stays.
2. **Table S4 (FaceShifter, shipped recipe) is re-derivable** from the post hoc
   re-evaluation (Added 6), printed at 4 decimals. Decision 2026-10-17 "W4a-1
   ruling: Table S4 gets 4 decimals from a post hoc GPU evaluation" (R1.42). The
   CAFRL cells (EMA weights) and both Δ are now checked; the 95 % intervals and
   P(Δ>0) stay as published and remain not derivable (decision 2026-10-18 "W4a-2
   ruling: published numbers stay where nothing new can be derived"). The rows
   were split, so their ids moved:

   | v1.0.0 id | v1.0.0 meaning | v2.0.0 id |
   |---|---|---|
   | T8.1 | c23 CAFRL, 0.822 (not derivable) | T8.1, 0.8216 (checked) |
   | T8.2 | c23 backbone, 0.823 | T8.2, 0.8230 |
   | T8.3 | c23 Δ, interval and P (not derivable) | T8.3 Δ −0.0080 (checked) + T8.4 interval and P (not derivable) |
   | T8.4 | c40 CAFRL, 0.758 (not derivable) | T8.5, 0.7575 (checked) |
   | T8.5 | c40 backbone, 0.732 | T8.6, 0.7318 |
   | T8.6 | c40 Δ, interval and P (not derivable) | T8.7 Δ +0.0221 (checked) + T8.8 interval and P (not derivable) |

   A reader who cited `python verify/claim.py T8.4` against v1.0.0 should use T8.5
   here. `make verify` now skips 6 checks instead of 8 (T8.4, T8.8, X1.16, X1.17,
   and the two deposit claims R13, R14). `predictions/GAPS.md` is re-worded to
   match.
3. **Display precision only, values unchanged**: these v1 rows now show the
   trailing zero the manuscript prints — T1.3 (0.9590), T5.1, T5.5, T8.2, AppC.2,
   AppC.15, AppC.23, M1.3, AppE.4, AppE.6, AppE.20, AppE.42, AppE.54.
4. **Claims map**: the v1 rows stay in `CLAIMS-MAP.md`, which gains one link line
   to `CLAIMS-MAP-R1.md`; the revision's rows are only there (decision
   2026-10-18 "W6: Revision-1 claims get their own claims map"). Its
   counts change with the items above. The manuscript it is checked against is
   now the revised one, labelled "IEEE Access, revision 1".
5. **Table, figure, section and contribution numbers** in `CLAIMS-MAP.md`,
   `figures/README.md`, `curves/README.md`, the reading note of
   `preregistration/retest-gates.md` and the release claims now refer to
   the revised manuscript (R1.48, page compression; R2.10, contributions methods
   first, decision 2026-10-18 "W4b-2 ruling: the contribution labels stay methods
   first"). Map, submitted → revised: Table 1 (notation) → Table S28; Table 2
   (STOP-gate) → Table 1; Table 3 (contrasts) → Table 4; Table 4 (CRF sweep) →
   Table S27; Table 5 (control audit) → Table S29; Table 6 unchanged; Fig. 3
   (campaign flow) → Fig. S1; Fig. 4 → Fig. 3; Section VII-C (seed confirmation)
   → VII-D; Section VII-D (generalization) → VII-E; contribution C3 (protocol) →
   C1. The FaceShifter table's title follows its new caption.
6. **Release claims**: R1's caveat now says that only the interval and P of the
   shipped-recipe FaceShifter cells lack per-video scores (decision "W4a-1 ruling:
   Table S4 gets 4 decimals from a post hoc GPU evaluation"); R13 and R14 describe
   the v2 deposit (Deposit, below); the `where` of R2, R4, R6, R7, R9, R11, R13
   and R14 points to the revised text. R1, R4 and R9 match more files because
   their patterns now also match the added Revision-1 files.
7. **Environment**: unchanged. The v1.0.0 environment files are shipped byte for
   byte rather than re-captured (decision 2026-10-18 "W6: the release keeps the
   v1 environment files").
8. **Harness code**: `evaluation/src/config/{defaults,load}.py`,
   `configs/base/defaults.py`, `evaluation/src/data/ffpp_faces.py` and
   `evaluation/src/evaluation/evaluator.py` are the current research code. They
   add the options the revision's runs use; their defaults reproduce the old code
   bit for bit (decision 2026-10-10 "Phase 6 build: default options must
   reproduce the old code bit for bit"). `verify/verify.py`, `verify/claim.py`,
   `verify/README.md` and `evaluation/rederive.py` change for items 1 and 4.
9. **Figures**: `figures/fig3_campaign_flow.tex` (now Fig. S1) and the panel
   titles in `figures/make_figures.py` follow the revised wording (decision
   2026-10-17 "W4a-1 ruling: W4b may edit the figure sources"; R1.21, R2.9).
10. **README**: the new title, status, tag and deposit; the counts; the deposit
    contents; rows for `revision-1/`, `code/`, `CLAIMS-MAP-R1.md` and this file
    (R1.1 for the title); a new *Reproducibility tiers* section (R1.45).
11. **Mechanical**: run, file and contrast counts in `configs/RUNS.md`,
    `curves/README.md`, `curves/selection.json` and `evaluation/README.md` (v1
    entries unchanged, new ones appended); the run count in the `derived_from` line
    of nine `splits/*.json`; timing fields only in
    `evaluation/analysis/cluster_bootstrap.json` and `seed_uncertainty.json`.
12. **v1 text that claimed more than the release supports** (decision
    2026-10-19 "W6 ruling: the release README quotes the revised abstract"; R1.45
    for the recompute and read-back lines):
    - README summary: the v1 paragraph is replaced by sentences quoted word for word from the revised abstract.
    - README *Reproduction contract*: "independently checkable today" → "checkable today".
    - README summary: "every number the paper prints can be recomputed" → recomputed or read back, four cannot be re-derived, with a pointer to *Reproducibility tiers*.
    - README *Check it yourself*: "checks every number the revision added" → checks each one by recomputing or reading it back, with the same pointer.
    - README *Reproduction contract*, layer 1: "Every table cell … in the paper is a function of the per-video scores" → every one that `verify` recomputes.
    - `CLAIMS-MAP.md` header: "the exact command that recomputes it" → the command that checks it (recomputes it, reads it back from a shipped file, or the row states why it cannot be checked), and "… are recomputed from the released artifacts and checked against the paper" → the checked entries split into recomputed from per-video scores and curves, read back from a shipped file (an analysis output, or a statistic stored in `predictions/` where per-video scores were never written: the cross-dataset AUCs and intervals, the frame-level AUCs, the P2 probe), and release claims whose files are present, with a pointer to *Reproducibility tiers* (R1.45).
    - `CLAIMS-MAP.md` header: "two parameter counts that no released artifact pins" → also names the parameter counts printed with a unit ("4.0 M"), whose released value in `probes/` is shown but not compared; "agrees with this release's own recomputation" → "agrees with the value this release gives"; "runs `verify/claim.py` … to recompute every row" → "to check every row".
    - `verify/claims_map.json`, `note`: "the command that recomputes it" → the command that checks it (recomputing the number, reading it back from a shipped file, or stating why it cannot be checked), with a pointer to *Reproducibility tiers*.
    - README *Check it yourself*: "table cells recomputed from the released per-video scores" → recomputed where per-video scores were written and read back from the stored statistic where they were not.
    - README *Reproducibility tiers* (new in v2.0.0, item 10): the recomputed counts cover only the checks whose AUCs come from per-video scores; the read-back tier adds the statistics stored in `predictions/` (Table S3's cross-dataset AUCs and intervals; the frame-level AUCs, intervals and P2 probe AUC of §S2) and counts only rows whose number is compared; "Tables S1–S4" → "Tables S1, S2 and S4"; a new sentence counts the release claims checked by file presence and the rows that are recorded rather than asserted.
13. **v1 text that was stale or incomplete** (W6 pre-freeze fixes, 2026-10-19):
    - README *What is not here yet*: now points to `predictions/GAPS.md` for the cells whose own per-video scores were never saved (audit defect D8).
    - README *Reproducibility tiers* (new in v2.0.0, item 10): "a tier-1 value" → "in reproducibility tier 1" (the paper's wording).
    - `predictions/GAPS.md`: gains an entry for the Xception-mq FaceShifter comparison (claims-map row X1.16), never saved and not re-derivable; its opening sentence names that exception.
    - `predictions/GAPS.md`: the statement that crops are "not currently on local disk" is removed; the file now says only that crops are not redistributable and how they are regenerated.
    - Release claims R13 and R14: the quotes now quote the revised manuscript verbatim (Reproducibility statement; Data availability).
    - Release claim R14: its `where` now names Data availability, the source of its quote.
    - README layout table, `CLAIMS-MAP.md` row: "the command that recomputes it" → how it is checked (recomputed, read back, or why it cannot be), with a pointer to *Reproducibility tiers*.
    - `predictions/GAPS.md`: "the cells listed here carry the reported statistics only" → "most cells listed here …" (the Xception-mq entry carries none, and the shipped-recipe FaceShifter cells have post hoc re-scores).
    - `CLAIMS-MAP-R1.md` header (Revision-1 text, new in v2.0.0): "the command that recomputes it" → the command that checks it by recomputing the number or reading it back, and "recomputed from the released artifacts" → the checked rows split into recomputed and read back, matching *Reproducibility tiers*; `verify/claims_map_r1.json`, `note`, likewise.

### Known issues

- `verify/claim.py` (v1 tool) prints "recomputed from released scores" also for cells whose value is read back from a statistic stored in `predictions/`; the claims map rows say which kind each is.

### Files copied as written

Three files of this release are copies of frozen research files written before
the decision that V1 is not post hoc, and they call it post hoc:
`configs/launch-r1x/r1x_abl_curriculum_rerun_s42.yaml` (header comment),
`code/ema-own-bn-stats/src/tests/test_phase6x_configs.py` (docstring) and
`revision-1/curriculum/analysis.json`. They are not edited, because they are
frozen. The paper and the claims maps do not label V1 post hoc: V1 is the
identical re-run of the stopped curriculum arm and the canonical curriculum run
(decision 2026-10-18 "W4b-2 ruling: V1 is not labelled post hoc anywhere"). V2 and
V3 are post hoc.

### Deposit

The v2 Zenodo version keeps the v1 files (`checkpoints.tar` with the 37
checkpoints of the 27 v1 runs, its manifest, and `crop-coordinates.tar.zst`) and
adds the v2.0.0 tarball and `checkpoints-r1.tar`: the selected `best.pt` of each
of the 26 Revision-1 runs, no `best_valloss.pt`. It adds no crop coordinates
(decision 2026-10-18 "W6: the Zenodo v2 deposit adds the new best checkpoints,
not new crops").

## v1.0.0 — the submitted manuscript

First release, with the manuscript as submitted to IEEE Access. Deposit DOI
10.5281/zenodo.22032529.
