# The harmonized baseline benchmark

*(Companion to the paper's Appendix C. The manuscript states this benchmark's
reading in prose — what multi-CRF training buys each architecture — and points
here for the complete matrix. Every cell below is recomputed by
`verify/verify.py` from the per-video scores in `predictions/ffpp/` — see the
`AppB2` block of `CLAIMS-MAP.md`.)*

Every baseline was run across both training protocols on one harness, one
metric and one test split: the FaceForensics++ official test split, 700 videos
per compression level, video-level AUC (32 frames per video, mean-pooled),
single runs at seed 42.

- **prot.** — `lit` is the literature protocol (c23-trained, evaluated across
  the sweep); `mq` is multi-CRF training, the same data CAFRL and SpatialBase
  see.
- **aug** — `std` is the standard augmentation policy (random crop,
  translation, rotation, colour jitter, Gaussian blur, deliberately *without*
  JPEG compression); `flip` is horizontal flip only.
- **params** — the model as trained here, with the ImageNet 1000-way
  classifier replaced by a single-logit head.
- **AUC_comp** — the compression-averaged AUC defined in the paper's Section
  IV-B.

| model | prot. | aug | params | c0 | c18 | c23 | c28 | c32 | c36 | **c40** | AUC_comp | released run id |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Xception | lit | std | 20.8 M | .9949 | .9948 | .9944 | .9890 | .9778 | .9280 | **.8660** | .9402 | `b1_xception_lit` |
| F3-Net | lit | std | 21.0 M | .9925 | .9924 | .9917 | .9835 | .9654 | .9210 | **.8599** | .9325 | `b2_f3net_lit` |
| FreqNet | lit | std | 5.1 M | .9808 | .9899 | .9877 | .9652 | .9274 | .8541 | **.7684** | .8788 | `b3_freqnet_lit` |
| Xception-mq | mq | std | 20.8 M | .9921 | .9899 | .9872 | .9838 | .9803 | .9739 | **.9679** | .9765 | `b4_xception_mq` |
| Xception-mq | mq | flip | 20.8 M | .9918 | .9893 | .9869 | .9820 | .9772 | .9691 | **.9631** | .9728 | `b4b_xception_mq_fliponly` |
| F3-Net-mq | mq | std | 21.0 M | .9911 | .9902 | .9885 | .9831 | .9766 | .9683 | **.9551** | .9708 | `b5_f3net_mq` |
| FreqNet-mq | mq | std | 5.1 M | .9800 | .9745 | .9693 | .9566 | .9383 | .9131 | **.8787** | .9217 | `b6_freqnet_mq` |
| **SpatialBase** | mq | flip | **4.0 M** | .9919 | .9892 | .9867 | .9810 | .9758 | .9678 | **.9590** | .9709 | `b7_effnet_b0_mq_fliponly` |

**How to read it.** All eight rows are **descriptive**: none was
pre-registered, and none enters the confirmatory family of the paper's Section
IV-D. Multi-CRF training moves Xception from 0.866 to 0.968 at c40 and F3-Net
from 0.860 to 0.955, at a cost of under a point at c23 (0.994 → 0.987 and
0.992 → 0.989); FreqNet gains the most in absolute terms (0.768 → 0.879) and
still finishes far below everything else. The SpatialBase row is the same run
as the paper's CRF-sweep table.

**What is not matched here.** The two `mq` frequency arms were trained with
the standard augmentation policy while SpatialBase is flip-only, so any
comparison between them is run in the frequency baselines' favour; the two
Xception-mq runs bound that advantage at ≈0.5 pt at c40 (0.9679 std vs 0.9631
flip-only). The paired contrasts the paper draws from these rows, with their
intervals, are in the paper's Appendix C and in `CLAIMS-MAP.md`.

**Calibration against published anchors** — the frame-level check of the three
`lit` rows against DeepfakeBench's Table 3, and the two documented
reimplementation simplifications — is in `evaluation/CALIBRATION.md`.
