# Baseline calibration and adaptation choices

*(Companion to the paper's baseline appendix, which is Supplementary Material §S2. The manuscript states the calibration
verdict and points here for the table and for the two documented
simplifications; this file is where they live in full. Every "ours" number
below is recomputed by `verify/verify.py` from the per-video scores in
`predictions/` — see the `AppC` block of `CLAIMS-MAP.md`.)*

## 1. Published anchors versus our reproductions

Three cautions govern this table, and they are the reason it is kept apart
from every other table of the study.

1. It is **frame-level AUC throughout**. That is the unit the published
   anchors are in; video-level AUC — the unit of every other table in the
   paper and of every file in `predictions/` — is not comparable to it.
2. The FaceForensics++ paper itself reports **accuracy, not AUC** (c23
   95.73 %, c40 81.00 %, all four manipulations, a separate model trained at
   each quality level), so it cannot supply an AUC anchor. The anchors used
   here are DeepfakeBench's Table 3: frame-level AUC obtained in one harness
   under the same c23-trained protocol our literature arm uses.
3. **FreqNet has no FF++ anchor at all.** It is trained on ProGAN images and
   evaluated as image-level accuracy and average precision, so the row below
   is, to our knowledge, its first FF++ c23/c40 entry on a video benchmark.

| detector | anchor c23 | anchor c40 | ours c23 | ours c40 | released run id |
|---|---|---|---|---|---|
| Xception | 0.9637 | 0.8261 | 0.9901 | 0.7915 | `b1_xception_lit` |
| F3-Net   | 0.9635 | 0.8271 | 0.9850 | 0.7802 | `b2_f3net_lit` |
| FreqNet  | — | — | 0.9673 | 0.6802 | `b3_freqnet_lit` |

Our arms are the literature protocol (c23-trained, standard augmentation),
single runs at seed 42.

**How to read the residual.** Both reproducible detectors clear their c23
anchor and land 3.5 and 4.7 frame-AUC points below their c40 anchor. That residual
was accepted, before the STOP-gate ran, as reproduction variance against a
recipe whose exact augmentation parameters, schedule and test-time averaging
are not published: our c23 sits *above* the anchor, so the models are trained,
not broken, and at the gate's own metric — video-level c40 — the strongest
literature baseline reaches 0.866, which CAFRL as specified (0.922) clears
comfortably. Pushing the residual further by tuning against a published number
would have been tuning against the very comparison the gate was about to make.

**Augmentation recovery.** Initial reproductions with flip-only augmentation
under-reproduced the published c40 anchors by 6–10 frame-AUC points while
overfitting (training loss → 0). Adding the standard augmentation policy —
random crop, translation, rotation, colour jitter and Gaussian blur,
deliberately *without* JPEG compression, which would corrupt the compression
signal under study — recovered them: +2.7 frame-AUC points at c40 for Xception
(0.764 → 0.791, `b1_xception_lit_fliponly` → `b1_xception_lit`) and +5.5 for
F3-Net (0.725 → 0.780, `b2_f3net_lit_fliponly` → `b2_f3net_lit`).

## 2. What "F3-Net" and "FreqNet" mean here

Both are reimplementations against the published designs, and both carry a
documented simplification that the cells above should be read with.

**F3-Net** is its FAD branch — the full-image DCT, three learnable band-pass
filters with the published low/mid/high spectral initialization, the inverse
DCT, the 9-channel stack and the 3→9 widening of the first convolution of an
ImageNet-pretrained Xception — **without** the LFS branch and the MixBlock
cross-attention. That scope was chosen before the runs, on the published
finding that FAD alone lands within ≈0.1 AUC point of full F3-Net on
FaceForensics++, and the anchor check in §1 was pre-declared as its fairness
adjudicator.

**FreqNet** is the full design — the high-frequency filtering (FFT, centred
low-frequency removal, inverse FFT) at both image and intermediate feature
level, the frequency-domain spectral convolutions, and the from-scratch
all-convolutional {64, 128, 256, 512} backbone with no ImageNet pretraining —
with a single-logit head in place of the two-way one, and with its FFT
arithmetic forced to `float32` because complex tensors are not representable
in bfloat16. FreqNet's published evaluation is a different problem — ProGAN
-generated images scored by accuracy and average precision — so its rows are an
adaptation to a video face-forgery benchmark rather than a reproduction of a
published number.

Both take 256×256 crops and the same recipe as every other baseline: AdamW,
lr 2×10⁻⁴, weight decay 10⁻⁴, 30 epochs, one warm-up epoch, cosine schedule,
batch 32, BCE. The configurations are in `configs/`; the exact architecture
code is not part of this release's CPU-only re-derivation path (it is the
training-side code), but every score those models produced is in
`predictions/`.

## 3. Where each number comes from

| number | artifact |
|---|---|
| ours c23 / c40 (frame-AUC), three literature arms | `predictions/ffpp/b{1,2,3}_*_lit.json` |
| the flip-only pair behind the augmentation recovery | `predictions/ffpp/b{1,2}_*_lit_fliponly.json` |
| the video-level sweeps for the same runs | `evaluation/BENCHMARK.md`; `CLAIMS-MAP.md` block `AppB2` |
| the published anchors | citations (DeepfakeBench Table 3; FaceForensics++; FreqNet), not artifacts of this release |
