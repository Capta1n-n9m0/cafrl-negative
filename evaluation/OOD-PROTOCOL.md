# Out-of-distribution evaluation protocol

*(Companion to the paper's Appendix D. The manuscript states the protocol in
two sentences — what each corpus contributes, and that both are used as
distributed — and points here for the full statement. Nothing here is new
evidence; it is the procedure behind the cells in that appendix, whose numbers
are checked in the `T7` and `T8` blocks of `CLAIMS-MAP.md`.)*

## 1. What is evaluated, and on what

| corpus | role | videos | levels used |
|---|---|---|---|
| Celeb-DF v2 | the genuinely **cross-dataset** corpus | 518 (178 real, 340 synthesized) — the corpus's own official test list | as distributed (the corpus does not stratify compression) |
| DFD / DeepFakeDetection | **near-domain**: shares FaceForensics++'s capture and processing lineage | 3,431 (363 real actors, 3,068 manipulations) — the full released set as re-cropped here | c23 and c40, both **as published** by the FaceForensics++ authors |
| FaceShifter | the single **held-out manipulation** (FF++ footage, 2020 face swap) | 280 | c23 and c40, as published |

**No CRF variant was generated for any of these three sets.** Our own
re-encodes cover only the FaceForensics++ core sets — CRF {28, 32, 36} for
every video and CRF 18 for the test split — so every out-of-distribution cell
in the paper is scored at compression its corpus was distributed with, never
at compression we applied.

## 2. How each video is scored

Identically to every FaceForensics++ cell in the paper, so that the numbers sit
in the same units:

1. **Frame selection** — 32 frames per video, chosen deterministically by
   `linspace` over the frames in which a face was detected. The same rule is
   used by the re-crop, the index builder and the evaluation loader, so every
   arm sees the same frames.
2. **Face detection and track curation** — SCRFD (InsightFace `buffalo_l`);
   for DFD, automatic diff-vote track selection with dynamic-time-warping
   alignment against the corresponding real video, which is what keeps the
   crop on the manipulated identity in multi-person footage.
3. **Crop** — a similarity warp of the five detected landmarks onto fixed
   reference points in a 256×256 canvas (`cv2.warpAffine`,
   `BORDER_REPLICATE`), not a bounding-box crop.
4. **Pooling** — the per-frame sigmoid scores are mean-pooled to one score per
   video, and AUC is computed over videos.

The per-video crop metadata that makes this deterministic (per-frame bounding
boxes, five-point landmarks, detection confidences) is released alongside the
split identity lists; see the paper's Data Availability statement and
`pipeline/`.

## 3. What these cells can and cannot support

- **The cross-dataset and near-domain cells carry no per-video scores.** They
  were stored as summary statistics during the campaign (see
  `predictions/GAPS.md`), so **no paired contrast is computable for any of
  them** — unlike every FaceForensics++ contrast in the paper, they cannot be
  adjudicated, and are reported descriptively with marginal per-cell bootstrap
  intervals (widths 0.02–0.05).
- **The bands are wide.** Out of distribution the seed dominates the
  architecture by more than an order of magnitude: Fair-N's three Celeb-DF runs
  read 0.668, 0.571 and 0.703, a 13-point spread from seed alone, against the
  0.4-point spread the same arm shows at FaceForensics++ c40. With three seeds
  per arm, marginal intervals and no paired contrast, these cells can exclude a
  large effect and nothing finer.
- **The held-out-manipulation cells do carry per-video scores** and are
  adjudicated with the same 10,000-replicate paired video bootstrap used
  throughout; the gate applied to them was directional and frozen before any
  fair-variant FaceShifter number existed.
- **TrunkCtrl was not evaluated out of distribution.**

## 4. Where each number comes from

| number | artifact |
|---|---|
| the 3-seed means and t-bands, and the single-seed cells | `predictions/cross_dataset/` summaries; `CLAIMS-MAP.md` block `T7` |
| the held-out-manipulation cells, deltas and intervals | `predictions/faceshifter/`; `CLAIMS-MAP.md` block `T8`; `evaluation/analysis/` |
| the crop pipeline and the split lists | `pipeline/`, `splits/` |
