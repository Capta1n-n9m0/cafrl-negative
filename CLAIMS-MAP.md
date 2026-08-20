# Claims map — every printed number, and the artifact that produces it

*Data Diversity, Not Frequency Invariance: A Controlled and Self-Audited Study of Compression-Robust Deepfake Detection* (IEEE Access submission, version B).

One row per manuscript table cell, per load-bearing number in the running text,
and per present-tense claim the paper makes about this repository. Each row
names the artifact the number comes out of and the exact command that recomputes
it from that artifact.

Rows use the manuscript's names for the trained configurations (SpatialBase,
CAFRL as specified, CAFRL−adv, spatial-residual, TrunkCtrl, Fair-N, Fair-W);
the directories and files under `configs/`, `predictions/` and `curves/` use
this study's internal run identifiers (`b7_effnet_b0_mq_fliponly`, `a0`,
`f1_none_fair_s42`, …). Table 1 of the manuscript is the crosswalk between the
two, and every row below names the run it reads. Row ids (`T1.1`, `T3.5`, …) are
stable handles for `verify/claim.py`, not manuscript table numbers; each section
heading names the manuscript table it maps.

376 rows and 14 release claims, 390 entries in all.
**347 are recomputed from the released artifacts and checked against the
paper on every build.** 6 are printed in the paper but *not* derivable
from this release, each with its reason stated in place. 2 — both of
them release claims — depend on the archival deposit, which is minted
immediately before submission. The remaining 35 are *recorded*
rather than asserted: prose claims whose artifact is a document, approximate
glosses ("≈0.4", "40–120×") whose underlying series is released in full, and two
parameter counts that no released artifact pins.

No row is marked **differs**: every checked number in the manuscript agrees
with this release's own recomputation. Three last-digit disagreements found
when this map was first generated — the harmonized benchmark's Xception-mq
AUC_comp, Appendix C's augmentation-recovery frame-AUC, and γ's peak — were
resolved in favour of the artifact: the release's value was kept and the paper
was corrected to it.

**What the paper now reads here rather than printing.** The revision's final
page pass moved material into this repository instead of deleting it, so a
number of mapped rows check something the manuscript points at rather than
prints:

- the published-anchor calibration *table* and the F3-Net/FreqNet adaptation
  statement in full — `evaluation/CALIBRATION.md`. The six frame-level
  reproduction numbers and their anchors were restored to the paper's
  Appendix C in the W9 revision and are printed there;
- the complete harmonized baseline benchmark over all seven CRF levels —
  `evaluation/BENCHMARK.md`. Its compressed form (c23–c40 and AUC_comp, eight
  rows) was restored to the paper's Appendix C in W9 and is printed there;
- the full out-of-distribution evaluation protocol — `evaluation/OOD-PROTOCOL.md`,
  stated in two sentences in Appendix D;
- the marginal intervals of the cross-dataset cells, and the seed-42 values of
  the four arms that were also run at three seeds — the paper's cross-dataset
  table now prints the 3-seed block and the one single-seed arm.

The numbers are unchanged and still checked below.

Run any row yourself:

```bash
python verify/claim.py --list          # every row, with its id
python verify/claim.py T4.7            # recompute one row
python verify/claim.py --all           # every cheap row, as a report
python verify/claim.py T3.1 --bootstrap  # a contrast row, 10,000 replicates
python verify/verify.py --jobs 4       # the whole check, tables and figures
```

This file is **generated**, not written: the release build expands the
declarations in its export manifest (which lives in the authors' working
repository, not here), runs `verify/claim.py` inside this tree to recompute every row
from the released artifacts, and writes the results into the "this release
gives" column. An undeclared disagreement fails the build and no release is
produced. Table and section numbers refer to the submitted manuscript. The map is regenerated whenever the release is rebuilt; if a manuscript number moves, the build fails until the map and the manuscript agree.

**How to read the columns.** "paper prints" is the value as it appears in the
manuscript, at the manuscript's precision. "this release gives" is what the
released artifacts produce, to four decimals — agreement is asserted at half a
unit in the last place the paper prints. "artifact" is the first artifact the
row reads, with a count of the others. Bootstrap rows are shown at the value
pinned in `verify/expected.json`; `verify.py` recomputes them from the scores at
10,000 replicates on every run.

---


## T0 — Notation — every arm this paper compares

*Section IV; `\label{tab:notation}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `T0.1` | SpatialBase — parameters | 4.0 M | 4.0088 | `probes/param_counts_arms.json` | `python verify/claim.py T0.1` |
| `T0.2` | CAFRL as specified — parameters | 11.97 M | 11.97 | `probes/param_counts_arms.json` | `python verify/claim.py T0.2` |
| `T0.3` | CAFRL−adv — parameters | 10.65 M | 10.65 | `probes/param_counts_arms.json` | `python verify/claim.py T0.3` |
| `T0.4` | spatial-residual — parameters | 10.29 M | 10.29 | `probes/param_counts_arms.json` | `python verify/claim.py T0.4` |
| `T0.5` | TrunkCtrl — parameters | 3.68 M | 3.6778 | `probes/param_counts_arms.json` | `python verify/claim.py T0.5` |
| `T0.6` | Fair-N — parameters | 10.65 M | 10.65 | `probes/param_counts_arms.json` | `python verify/claim.py T0.6` |
| `T0.7` | Fair-W — parameters | 9.63 M | 9.6281 | `probes/param_counts_arms.json` | `python verify/claim.py T0.7` |
| `T0.8` | Xception-mq — parameters | 20.8 M | 20.81 | `probes/param_counts_arms.json` | `python verify/claim.py T0.8` |
| `T0.9` | Xception-mq (flip-only) — parameters | 20.8 M | 20.81 | `probes/param_counts_arms.json` | `python verify/claim.py T0.9` |
| `T0.10` | F3-Net-mq — parameters | 21.0 M | 21.01 | `probes/param_counts_arms.json` | `python verify/claim.py T0.10` |
| `T0.11` | FreqNet-mq — parameters | 5.1 M | 5.0863 | `probes/param_counts_arms.json` | `python verify/claim.py T0.11` |
| `T0.12` | Xception (lit) — parameters | 20.8 M | 20.81 | `probes/param_counts_arms.json` | `python verify/claim.py T0.12` |
| `T0.13` | F3-Net (lit) — parameters | 21.0 M | 21.01 | `probes/param_counts_arms.json` | `python verify/claim.py T0.13` |
| `T0.14` | FreqNet (lit) — parameters | 5.1 M | 5.0863 | `probes/param_counts_arms.json` | `python verify/claim.py T0.14` |
| `T0.15` | Xception-JPEG — parameters | 20.8 M | 20.81 | `probes/param_counts_arms.json` | `python verify/claim.py T0.15` |
| `T0.16` | CAFRL as specified — parameters at inference (discriminator dropped) | 10.65 M | 10.65 | `probes/param_counts_arms.json` | `python verify/claim.py T0.16` |

## T1 — The STOP-gate comparison (video-AUC, FF++ test)

*Section V-A (the STOP-gate fires); `\label{tab:stopgate}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `T1.1` | SpatialBase EffNet-B0 spatial — params | 4.0 M | recorded | `configs/runs/b7_effnet_b0_mq_fliponly.yaml` | `python verify/claim.py T1.1` |
| `T1.2` | SpatialBase — c23 | 0.987 | 0.9867 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py T1.2` |
| `T1.3` | SpatialBase — c40 | 0.959 | 0.9590 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py T1.3` |
| `T1.4` | SpatialBase — AUC_comp | 0.971 | 0.9709 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py T1.4` |
| `T1.5` | CAFRL as specified (grl) — params | 11.97 M | 11.97 | `probes/param_counts_cafrl.json` | `python verify/claim.py T1.5` |
| `T1.6` | CAFRL as specified (grl) — c23 | 0.974 | 0.9738 | `predictions/ffpp/a0.json` | `python verify/claim.py T1.6` |
| `T1.7` | CAFRL as specified (grl) — c40 | 0.922 | 0.9224 | `predictions/ffpp/a0.json` | `python verify/claim.py T1.7` |
| `T1.8` | CAFRL as specified (grl) — AUC_comp | 0.948 | 0.9477 | `predictions/ffpp/a0.json` | `python verify/claim.py T1.8` |
| `T1.9` | Xception-mq — params | 20.8 M | recorded | `configs/runs/b4_xception_mq.yaml` | `python verify/claim.py T1.9` |
| `T1.10` | Xception-mq — c23 | 0.987 | 0.9872 | `predictions/ffpp/b4_xception_mq.json` | `python verify/claim.py T1.10` |
| `T1.11` | Xception-mq — c40 | 0.968 | 0.9679 | `predictions/ffpp/b4_xception_mq.json` | `python verify/claim.py T1.11` |
| `T1.12` | Xception-mq — AUC_comp | 0.976 | 0.9765 | `predictions/ffpp/b4_xception_mq.json` | `python verify/claim.py T1.12` |

- `T1.1` — The standard EfficientNet-B0 count with a binary head, as built by the released config. No released artifact pins it; a per-arm parameter table is added in revision.
- `T1.9` — The standard Xception count with a binary head, as built by the released config; not pinned by a released artifact.
- `T1.12` — Corrected in the manuscript (W1, 2026-08-19) from 0.977 to the released recomputation: mean video-AUC over c28-c40 is 0.97645.

## T2 — The audit ledger (D1-D4, named in Section VI's prose)

*Section VI (the self-audit); the condensed table was replaced by prose in the W9 duplication pass, Appendix B remaining the authoritative telling; `\label{sec:audit}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `T2.1` | The D1–D8 ledger (all rows) | prose | recorded | `audit/LEDGER-D1-D8.md` | `python verify/claim.py T2.1` |

- `T2.1` — The full ledger, in two halves: the defects as first stated (2026-07-02) and their closure status after the re-tests.

## T3 — The adjudicated contrasts (10k paired video bootstrap)

*Section VII-C (seed confirmation); `\label{tab:contrasts}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `T3.1` | SpatialBase − CAFRL as specified (STOP-gate) — Δ and CI | +0.0366 [+0.020, +0.054] | 0.0366 | `verify/expected.json` +2 | `python verify/claim.py T3.1 --bootstrap` |
| `T3.2` | Fair-N − CAFRL−adv (what the fair recipe bought) — Δ and CI | +0.0396 [+0.0231, +0.0570] | 0.0396 | `verify/expected.json` +2 | `python verify/claim.py T3.2 --bootstrap` |
| `T3.3` | Fair-N − SpatialBase (single seed) — Δ and CI | -0.0004 [-0.0092, +0.0080] | -0.0004 | `verify/expected.json` +2 | `python verify/claim.py T3.3 --bootstrap` |
| `T3.4` | Fair-W − SpatialBase (single seed) — Δ and CI | +0.0056 [-0.0022, +0.0134] | 0.0056 | `verify/expected.json` +2 | `python verify/claim.py T3.4 --bootstrap` |
| `T3.5` | Fair-N pool − SpatialBase pool (3v3) — Δ and CI | -0.0010 [-0.0066, +0.0045] | -0.0010 | `verify/expected.json` +6 | `python verify/claim.py T3.5 --bootstrap` |
| `T3.6` | Fair-W pool − SpatialBase pool (3v3) — Δ and CI | +0.0022 [-0.0035, +0.0080] | 0.0022 | `verify/expected.json` +6 | `python verify/claim.py T3.6 --bootstrap` |
| `T3.7` | SpatialBase − TrunkCtrl (architecture share, pooled) — Δ and CI | -0.0038 [-0.0116, +0.0039] | -0.0038 | `verify/expected.json` +4 | `python verify/claim.py T3.7 --bootstrap` |
| `T3.8` | TrunkCtrl − spatial-residual (recipe share, pooled) — Δ and CI | +0.0490 [+0.0294, +0.0705] | 0.0490 | `verify/expected.json` +4 | `python verify/claim.py T3.8 --bootstrap` |

- `T3.1` — The lower bound is reprinted from this release's recomputation (+0.0205, which rounds to +0.020); the manuscript's earlier +0.021 came from a different draw, a Monte-Carlo difference of ~5e-4. Corrected in the manuscript (W1, 2026-08-19). Every other endpoint reproduces exactly.
- `T3.7` — Asymmetric as run and as printed: the single frozen b7 (seed 42) against the three-seed pool of T, which is what the Phase-5.2 rule specified. Pooling b7's seeds as well moves the point estimate to about +0.002; the verdict is unchanged. The manuscript states this in the table caption (W1, 2026-08-19).

## T4 — CRF sweep, all key arms (video-AUC, FF++ test)

*Section VIII (what buys compression robustness); `\label{tab:sweep}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `T4.1` | SpatialBase EffNet-B0 spatial (fair) — c0 | 0.9919 | 0.9919 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py T4.1` |
| `T4.2` | SpatialBase EffNet-B0 spatial (fair) — c18 | 0.9892 | 0.9892 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py T4.2` |
| `T4.3` | SpatialBase EffNet-B0 spatial (fair) — c23 | 0.9867 | 0.9867 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py T4.3` |
| `T4.4` | SpatialBase EffNet-B0 spatial (fair) — c28 | 0.981 | 0.9810 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py T4.4` |
| `T4.5` | SpatialBase EffNet-B0 spatial (fair) — c32 | 0.9758 | 0.9758 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py T4.5` |
| `T4.6` | SpatialBase EffNet-B0 spatial (fair) — c36 | 0.9678 | 0.9678 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py T4.6` |
| `T4.7` | SpatialBase EffNet-B0 spatial (fair) — c40 | 0.959 | 0.9590 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py T4.7` |
| `T4.8` | SpatialBase EffNet-B0 spatial (fair) — auc_comp | 0.9709 | 0.9709 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py T4.8` |
| `T4.9` | Fair-W full trunk + freq residual (fair) — c0 | 0.9929 | 0.9929 | `predictions/ffpp/f2_spatres_full_s42.json` | `python verify/claim.py T4.9` |
| `T4.10` | Fair-W full trunk + freq residual (fair) — c18 | 0.9902 | 0.9902 | `predictions/ffpp/f2_spatres_full_s42.json` | `python verify/claim.py T4.10` |
| `T4.11` | Fair-W full trunk + freq residual (fair) — c23 | 0.9894 | 0.9894 | `predictions/ffpp/f2_spatres_full_s42.json` | `python verify/claim.py T4.11` |
| `T4.12` | Fair-W full trunk + freq residual (fair) — c28 | 0.9821 | 0.9821 | `predictions/ffpp/f2_spatres_full_s42.json` | `python verify/claim.py T4.12` |
| `T4.13` | Fair-W full trunk + freq residual (fair) — c32 | 0.9774 | 0.9774 | `predictions/ffpp/f2_spatres_full_s42.json` | `python verify/claim.py T4.13` |
| `T4.14` | Fair-W full trunk + freq residual (fair) — c36 | 0.9719 | 0.9719 | `predictions/ffpp/f2_spatres_full_s42.json` | `python verify/claim.py T4.14` |
| `T4.15` | Fair-W full trunk + freq residual (fair) — c40 | 0.9645 | 0.9645 | `predictions/ffpp/f2_spatres_full_s42.json` | `python verify/claim.py T4.15` |
| `T4.16` | Fair-W full trunk + freq residual (fair) — auc_comp | 0.974 | 0.9740 | `predictions/ffpp/f2_spatres_full_s42.json` | `python verify/claim.py T4.16` |
| `T4.17` | Fair-N narrow trunk, full freq stack (fair) — c0 | 0.9941 | 0.9941 | `predictions/ffpp/f1_none_fair_s42.json` | `python verify/claim.py T4.17` |
| `T4.18` | Fair-N narrow trunk, full freq stack (fair) — c18 | 0.9901 | 0.9901 | `predictions/ffpp/f1_none_fair_s42.json` | `python verify/claim.py T4.18` |
| `T4.19` | Fair-N narrow trunk, full freq stack (fair) — c23 | 0.9881 | 0.9881 | `predictions/ffpp/f1_none_fair_s42.json` | `python verify/claim.py T4.19` |
| `T4.20` | Fair-N narrow trunk, full freq stack (fair) — c28 | 0.9798 | 0.9798 | `predictions/ffpp/f1_none_fair_s42.json` | `python verify/claim.py T4.20` |
| `T4.21` | Fair-N narrow trunk, full freq stack (fair) — c32 | 0.977 | 0.9770 | `predictions/ffpp/f1_none_fair_s42.json` | `python verify/claim.py T4.21` |
| `T4.22` | Fair-N narrow trunk, full freq stack (fair) — c36 | 0.9702 | 0.9702 | `predictions/ffpp/f1_none_fair_s42.json` | `python verify/claim.py T4.22` |
| `T4.23` | Fair-N narrow trunk, full freq stack (fair) — c40 | 0.9586 | 0.9586 | `predictions/ffpp/f1_none_fair_s42.json` | `python verify/claim.py T4.23` |
| `T4.24` | Fair-N narrow trunk, full freq stack (fair) — auc_comp | 0.9714 | 0.9714 | `predictions/ffpp/f1_none_fair_s42.json` | `python verify/claim.py T4.24` |
| `T4.25` | TrunkCtrl trunk-recipe control (fair, 3-seed mean) — c0 | 0.992 | 0.9920 | `predictions/ffpp/trunk_recipe_s42.json` +2 | `python verify/claim.py T4.25` |
| `T4.26` | TrunkCtrl trunk-recipe control (fair, 3-seed mean) — c18 | 0.9886 | 0.9886 | `predictions/ffpp/trunk_recipe_s42.json` +2 | `python verify/claim.py T4.26` |
| `T4.27` | TrunkCtrl trunk-recipe control (fair, 3-seed mean) — c23 | 0.9863 | 0.9863 | `predictions/ffpp/trunk_recipe_s42.json` +2 | `python verify/claim.py T4.27` |
| `T4.28` | TrunkCtrl trunk-recipe control (fair, 3-seed mean) — c28 | 0.9796 | 0.9796 | `predictions/ffpp/trunk_recipe_s42.json` +2 | `python verify/claim.py T4.28` |
| `T4.29` | TrunkCtrl trunk-recipe control (fair, 3-seed mean) — c32 | 0.9719 | 0.9719 | `predictions/ffpp/trunk_recipe_s42.json` +2 | `python verify/claim.py T4.29` |
| `T4.30` | TrunkCtrl trunk-recipe control (fair, 3-seed mean) — c36 | 0.9644 | 0.9644 | `predictions/ffpp/trunk_recipe_s42.json` +2 | `python verify/claim.py T4.30` |
| `T4.31` | TrunkCtrl trunk-recipe control (fair, 3-seed mean) — c40 | 0.9536 | 0.9536 | `predictions/ffpp/trunk_recipe_s42.json` +2 | `python verify/claim.py T4.31` |
| `T4.32` | TrunkCtrl trunk-recipe control (fair, 3-seed mean) — auc_comp | 0.9674 | 0.9674 | `predictions/ffpp/trunk_recipe_s42.json` +2 | `python verify/claim.py T4.32` |
| `T4.33` | CAFRL-grl (shipped) — c0 | 0.9843 | 0.9843 | `predictions/ffpp/a0.json` | `python verify/claim.py T4.33` |
| `T4.34` | CAFRL-grl (shipped) — c18 | 0.9791 | 0.9791 | `predictions/ffpp/a0.json` | `python verify/claim.py T4.34` |
| `T4.35` | CAFRL-grl (shipped) — c23 | 0.9738 | 0.9738 | `predictions/ffpp/a0.json` | `python verify/claim.py T4.35` |
| `T4.36` | CAFRL-grl (shipped) — c28 | 0.9659 | 0.9659 | `predictions/ffpp/a0.json` | `python verify/claim.py T4.36` |
| `T4.37` | CAFRL-grl (shipped) — c32 | 0.9572 | 0.9572 | `predictions/ffpp/a0.json` | `python verify/claim.py T4.37` |
| `T4.38` | CAFRL-grl (shipped) — c36 | 0.9451 | 0.9451 | `predictions/ffpp/a0.json` | `python verify/claim.py T4.38` |
| `T4.39` | CAFRL-grl (shipped) — c40 | 0.9224 | 0.9224 | `predictions/ffpp/a0.json` | `python verify/claim.py T4.39` |
| `T4.40` | CAFRL-grl (shipped) — auc_comp | 0.9477 | 0.9477 | `predictions/ffpp/a0.json` | `python verify/claim.py T4.40` |
| `T4.41` | CAFRL−adv (shipped) — c0 | 0.9923 | 0.9923 | `predictions/ffpp/a1_none_s42.json` | `python verify/claim.py T4.41` |
| `T4.42` | CAFRL−adv (shipped) — c18 | 0.9818 | 0.9818 | `predictions/ffpp/a1_none_s42.json` | `python verify/claim.py T4.42` |
| `T4.43` | CAFRL−adv (shipped) — c23 | 0.9697 | 0.9697 | `predictions/ffpp/a1_none_s42.json` | `python verify/claim.py T4.43` |
| `T4.44` | CAFRL−adv (shipped) — c28 | 0.959 | 0.9590 | `predictions/ffpp/a1_none_s42.json` | `python verify/claim.py T4.44` |
| `T4.45` | CAFRL−adv (shipped) — c32 | 0.9484 | 0.9484 | `predictions/ffpp/a1_none_s42.json` | `python verify/claim.py T4.45` |
| `T4.46` | CAFRL−adv (shipped) — c36 | 0.9311 | 0.9311 | `predictions/ffpp/a1_none_s42.json` | `python verify/claim.py T4.46` |
| `T4.47` | CAFRL−adv (shipped) — c40 | 0.919 | 0.9190 | `predictions/ffpp/a1_none_s42.json` | `python verify/claim.py T4.47` |
| `T4.48` | CAFRL−adv (shipped) — auc_comp | 0.9394 | 0.9394 | `predictions/ffpp/a1_none_s42.json` | `python verify/claim.py T4.48` |
| `T4.49` | spatial-residual (shipped, γ→0) — c0 | 0.9714 | 0.9714 | `predictions/ffpp/cafrl_spatres_s42.json` | `python verify/claim.py T4.49` |
| `T4.50` | spatial-residual (shipped, γ→0) — c18 | 0.9702 | 0.9702 | `predictions/ffpp/cafrl_spatres_s42.json` | `python verify/claim.py T4.50` |
| `T4.51` | spatial-residual (shipped, γ→0) — c23 | 0.9686 | 0.9686 | `predictions/ffpp/cafrl_spatres_s42.json` | `python verify/claim.py T4.51` |
| `T4.52` | spatial-residual (shipped, γ→0) — c28 | 0.9583 | 0.9583 | `predictions/ffpp/cafrl_spatres_s42.json` | `python verify/claim.py T4.52` |
| `T4.53` | spatial-residual (shipped, γ→0) — c32 | 0.9495 | 0.9495 | `predictions/ffpp/cafrl_spatres_s42.json` | `python verify/claim.py T4.53` |
| `T4.54` | spatial-residual (shipped, γ→0) — c36 | 0.9307 | 0.9307 | `predictions/ffpp/cafrl_spatres_s42.json` | `python verify/claim.py T4.54` |
| `T4.55` | spatial-residual (shipped, γ→0) — c40 | 0.9139 | 0.9139 | `predictions/ffpp/cafrl_spatres_s42.json` | `python verify/claim.py T4.55` |
| `T4.56` | spatial-residual (shipped, γ→0) — auc_comp | 0.9381 | 0.9381 | `predictions/ffpp/cafrl_spatres_s42.json` | `python verify/claim.py T4.56` |

- `T4.25` — Every cell in this row is the mean of the three seeds' per-level video-AUCs; the AUC_comp cell is the mean of the three seeds' AUC_comp (identical to four decimals either way).
- `T4.26` — Every cell in this row is the mean of the three seeds' per-level video-AUCs; the AUC_comp cell is the mean of the three seeds' AUC_comp (identical to four decimals either way).
- `T4.27` — Every cell in this row is the mean of the three seeds' per-level video-AUCs; the AUC_comp cell is the mean of the three seeds' AUC_comp (identical to four decimals either way).
- `T4.28` — Every cell in this row is the mean of the three seeds' per-level video-AUCs; the AUC_comp cell is the mean of the three seeds' AUC_comp (identical to four decimals either way).
- `T4.29` — Every cell in this row is the mean of the three seeds' per-level video-AUCs; the AUC_comp cell is the mean of the three seeds' AUC_comp (identical to four decimals either way).
- `T4.30` — Every cell in this row is the mean of the three seeds' per-level video-AUCs; the AUC_comp cell is the mean of the three seeds' AUC_comp (identical to four decimals either way).
- `T4.31` — Every cell in this row is the mean of the three seeds' per-level video-AUCs; the AUC_comp cell is the mean of the three seeds' AUC_comp (identical to four decimals either way).
- `T4.32` — Every cell in this row is the mean of the three seeds' per-level video-AUCs; the AUC_comp cell is the mean of the three seeds' AUC_comp (identical to four decimals either way).

## T5 — Per-seed c40 video-AUC and 3-seed bands

*Appendix A; `\label{tab:appseeds}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `T5.1` | SpatialBase — c40 seed 42 | 0.959 | 0.9590 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py T5.1` |
| `T5.2` | SpatialBase — c40 seed 1 | 0.9614 | 0.9614 | `predictions/ffpp/b7_effnet_b0_mq_fliponly_s1.json` | `python verify/claim.py T5.2` |
| `T5.3` | SpatialBase — c40 seed 2 | 0.9492 | 0.9492 | `predictions/ffpp/b7_effnet_b0_mq_fliponly_s2.json` | `python verify/claim.py T5.3` |
| `T5.4` | SpatialBase — c40 3-seed mean | 0.9565 | 0.9565 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` +2 | `python verify/claim.py T5.4` |
| `T5.5` | SpatialBase — c40 3-seed band (half-width) | 0.016 | 0.0160 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` +2 | `python verify/claim.py T5.5` |
| `T5.6` | SpatialBase — AUC_comp 3-seed mean | 0.9688 | 0.9688 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` +2 | `python verify/claim.py T5.6` |
| `T5.7` | Fair-N — c40 seed 42 | 0.9586 | 0.9586 | `predictions/ffpp/f1_none_fair_s42.json` | `python verify/claim.py T5.7` |
| `T5.8` | Fair-N — c40 seed 1 | 0.9567 | 0.9567 | `predictions/ffpp/f1_none_fair_s1.json` | `python verify/claim.py T5.8` |
| `T5.9` | Fair-N — c40 seed 2 | 0.9536 | 0.9536 | `predictions/ffpp/f1_none_fair_s2.json` | `python verify/claim.py T5.9` |
| `T5.10` | Fair-N — c40 3-seed mean | 0.9563 | 0.9563 | `predictions/ffpp/f1_none_fair_s42.json` +2 | `python verify/claim.py T5.10` |
| `T5.11` | Fair-N — c40 3-seed band (half-width) | 0.0062 | 0.0062 | `predictions/ffpp/f1_none_fair_s42.json` +2 | `python verify/claim.py T5.11` |
| `T5.12` | Fair-N — AUC_comp 3-seed mean | 0.9675 | 0.9675 | `predictions/ffpp/f1_none_fair_s42.json` +2 | `python verify/claim.py T5.12` |
| `T5.13` | Fair-W — c40 seed 42 | 0.9645 | 0.9645 | `predictions/ffpp/f2_spatres_full_s42.json` | `python verify/claim.py T5.13` |
| `T5.14` | Fair-W — c40 seed 1 | 0.9602 | 0.9602 | `predictions/ffpp/f2_spatres_full_s1.json` | `python verify/claim.py T5.14` |
| `T5.15` | Fair-W — c40 seed 2 | 0.9609 | 0.9609 | `predictions/ffpp/f2_spatres_full_s2.json` | `python verify/claim.py T5.15` |
| `T5.16` | Fair-W — c40 3-seed mean | 0.9619 | 0.9619 | `predictions/ffpp/f2_spatres_full_s42.json` +2 | `python verify/claim.py T5.16` |
| `T5.17` | Fair-W — c40 3-seed band (half-width) | 0.0058 | 0.0058 | `predictions/ffpp/f2_spatres_full_s42.json` +2 | `python verify/claim.py T5.17` |
| `T5.18` | Fair-W — AUC_comp 3-seed mean | 0.9719 | 0.9719 | `predictions/ffpp/f2_spatres_full_s42.json` +2 | `python verify/claim.py T5.18` |
| `T5.19` | TrunkCtrl — c40 seed 42 | 0.9491 | 0.9491 | `predictions/ffpp/trunk_recipe_s42.json` | `python verify/claim.py T5.19` |
| `T5.20` | TrunkCtrl — c40 seed 1 | 0.9566 | 0.9566 | `predictions/ffpp/trunk_recipe_s1.json` | `python verify/claim.py T5.20` |
| `T5.21` | TrunkCtrl — c40 seed 2 | 0.9551 | 0.9551 | `predictions/ffpp/trunk_recipe_s2.json` | `python verify/claim.py T5.21` |
| `T5.22` | TrunkCtrl — c40 3-seed mean | 0.9536 | 0.9536 | `predictions/ffpp/trunk_recipe_s42.json` +2 | `python verify/claim.py T5.22` |
| `T5.23` | TrunkCtrl — c40 3-seed band (half-width) | 0.0098 | 0.0098 | `predictions/ffpp/trunk_recipe_s42.json` +2 | `python verify/claim.py T5.23` |
| `T5.24` | TrunkCtrl — AUC_comp 3-seed mean | 0.9674 | 0.9674 | `predictions/ffpp/trunk_recipe_s42.json` +2 | `python verify/claim.py T5.24` |

## T6 — The D1–D8 audit ledger (full)

*Appendix B; `\label{tab:appledger}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `T6.1` | The eight defects, why each mattered, and how each was closed | prose | recorded | `audit/LEDGER-D1-D8.md` | `python verify/claim.py T6.1` |
| `T6.2` | "four independent review passes (training parity, the frequency-path implementation, evaluation symmetry, run diagnostics)" | prose | recorded | `audit/AUDIT-PASSES.md` | `python verify/claim.py T6.2` |

- `T6.2` — The four pass scopes verbatim, the checks they ran with outcomes, and an explicit statement of what their independence does and does not mean (audit/README.md).

## T7 — Cross-dataset evaluation (video-AUC)

*Appendix D-A (Table 9; intervals released-only after the W8a trim, and the four replicated arms' seed-42 values released-only after the W8b cut A); `\label{tab:appcrossdataset}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `T7.1` | CAFRL (shipped, A0) — celebdf_v2 | 0.698 | 0.6979 | `predictions/cross_dataset/a0.json` | `python verify/claim.py T7.1` |
| `T7.2` | CAFRL (shipped, A0) — dfd_c23 | 0.82 | 0.8200 | `predictions/cross_dataset/a0.json` | `python verify/claim.py T7.2` |
| `T7.3` | CAFRL (shipped, A0) — dfd_c40 | 0.631 | 0.6307 | `predictions/cross_dataset/a0.json` | `python verify/claim.py T7.3` |
| `T7.4` | EffNet-B0 backbone (SpatialBase) — celebdf_v2 | 0.699 | 0.6990 | `predictions/cross_dataset/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py T7.4` |
| `T7.5` | EffNet-B0 backbone (SpatialBase) — dfd_c23 | 0.804 | 0.8041 | `predictions/cross_dataset/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py T7.5` |
| `T7.6` | EffNet-B0 backbone (SpatialBase) — dfd_c40 | 0.646 | 0.6461 | `predictions/cross_dataset/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py T7.6` |
| `T7.7` | Xception-mq — celebdf_v2 | 0.702 | 0.7023 | `predictions/cross_dataset/b4_xception_mq.json` | `python verify/claim.py T7.7` |
| `T7.8` | Xception-mq — dfd_c23 | 0.881 | 0.8806 | `predictions/cross_dataset/b4_xception_mq.json` | `python verify/claim.py T7.8` |
| `T7.9` | Xception-mq — dfd_c40 | 0.688 | 0.6880 | `predictions/cross_dataset/b4_xception_mq.json` | `python verify/claim.py T7.9` |
| `T7.10` | CAFRL (shipped, A0) — CI lower — celebdf_v2 | 0.648 | 0.6484 | `predictions/cross_dataset/a0.json` | `python verify/claim.py T7.10` |
| `T7.11` | CAFRL (shipped, A0) — CI lower — dfd_c23 | 0.8 | 0.8002 | `predictions/cross_dataset/a0.json` | `python verify/claim.py T7.11` |
| `T7.12` | CAFRL (shipped, A0) — CI lower — dfd_c40 | 0.602 | 0.6018 | `predictions/cross_dataset/a0.json` | `python verify/claim.py T7.12` |
| `T7.13` | CAFRL (shipped, A0) — CI upper — celebdf_v2 | 0.745 | 0.7449 | `predictions/cross_dataset/a0.json` | `python verify/claim.py T7.13` |
| `T7.14` | CAFRL (shipped, A0) — CI upper — dfd_c23 | 0.839 | 0.8391 | `predictions/cross_dataset/a0.json` | `python verify/claim.py T7.14` |
| `T7.15` | CAFRL (shipped, A0) — CI upper — dfd_c40 | 0.659 | 0.6589 | `predictions/cross_dataset/a0.json` | `python verify/claim.py T7.15` |
| `T7.16` | EffNet-B0 backbone (SpatialBase) — CI lower — celebdf_v2 | 0.649 | 0.6494 | `predictions/cross_dataset/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py T7.16` |
| `T7.17` | EffNet-B0 backbone (SpatialBase) — CI lower — dfd_c23 | 0.783 | 0.7829 | `predictions/cross_dataset/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py T7.17` |
| `T7.18` | EffNet-B0 backbone (SpatialBase) — CI lower — dfd_c40 | 0.617 | 0.6174 | `predictions/cross_dataset/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py T7.18` |
| `T7.19` | EffNet-B0 backbone (SpatialBase) — CI upper — celebdf_v2 | 0.745 | 0.7450 | `predictions/cross_dataset/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py T7.19` |
| `T7.20` | EffNet-B0 backbone (SpatialBase) — CI upper — dfd_c23 | 0.824 | 0.8245 | `predictions/cross_dataset/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py T7.20` |
| `T7.21` | EffNet-B0 backbone (SpatialBase) — CI upper — dfd_c40 | 0.674 | 0.6736 | `predictions/cross_dataset/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py T7.21` |
| `T7.22` | Xception-mq — CI lower — celebdf_v2 | 0.653 | 0.6533 | `predictions/cross_dataset/b4_xception_mq.json` | `python verify/claim.py T7.22` |
| `T7.23` | Xception-mq — CI lower — dfd_c23 | 0.864 | 0.8639 | `predictions/cross_dataset/b4_xception_mq.json` | `python verify/claim.py T7.23` |
| `T7.24` | Xception-mq — CI lower — dfd_c40 | 0.66 | 0.6595 | `predictions/cross_dataset/b4_xception_mq.json` | `python verify/claim.py T7.24` |
| `T7.25` | Xception-mq — CI upper — celebdf_v2 | 0.748 | 0.7479 | `predictions/cross_dataset/b4_xception_mq.json` | `python verify/claim.py T7.25` |
| `T7.26` | Xception-mq — CI upper — dfd_c23 | 0.896 | 0.8962 | `predictions/cross_dataset/b4_xception_mq.json` | `python verify/claim.py T7.26` |
| `T7.27` | Xception-mq — CI upper — dfd_c40 | 0.715 | 0.7154 | `predictions/cross_dataset/b4_xception_mq.json` | `python verify/claim.py T7.27` |
| `T7.28` | Fair-N (s42) — celebdf_v2 | 0.668 | 0.6676 | `predictions/cross_dataset/f1_none_fair_s42.json` | `python verify/claim.py T7.28` |
| `T7.29` | Fair-N (s42) — dfd_c23 | 0.828 | 0.8281 | `predictions/cross_dataset/f1_none_fair_s42.json` | `python verify/claim.py T7.29` |
| `T7.30` | Fair-N (s42) — dfd_c40 | 0.683 | 0.6830 | `predictions/cross_dataset/f1_none_fair_s42.json` | `python verify/claim.py T7.30` |
| `T7.31` | Fair-N (s42) — CI lower — celebdf_v2 | 0.615 | 0.6154 | `predictions/cross_dataset/f1_none_fair_s42.json` | `python verify/claim.py T7.31` |
| `T7.32` | Fair-N (s42) — CI lower — dfd_c23 | 0.808 | 0.8080 | `predictions/cross_dataset/f1_none_fair_s42.json` | `python verify/claim.py T7.32` |
| `T7.33` | Fair-N (s42) — CI lower — dfd_c40 | 0.656 | 0.6557 | `predictions/cross_dataset/f1_none_fair_s42.json` | `python verify/claim.py T7.33` |
| `T7.34` | Fair-N (s42) — CI upper — celebdf_v2 | 0.716 | 0.7164 | `predictions/cross_dataset/f1_none_fair_s42.json` | `python verify/claim.py T7.34` |
| `T7.35` | Fair-N (s42) — CI upper — dfd_c23 | 0.848 | 0.8475 | `predictions/cross_dataset/f1_none_fair_s42.json` | `python verify/claim.py T7.35` |
| `T7.36` | Fair-N (s42) — CI upper — dfd_c40 | 0.709 | 0.7095 | `predictions/cross_dataset/f1_none_fair_s42.json` | `python verify/claim.py T7.36` |
| `T7.37` | Fair-W (s42) — celebdf_v2 | 0.684 | 0.6839 | `predictions/cross_dataset/f2_spatres_full_s42.json` | `python verify/claim.py T7.37` |
| `T7.38` | Fair-W (s42) — dfd_c23 | 0.834 | 0.8336 | `predictions/cross_dataset/f2_spatres_full_s42.json` | `python verify/claim.py T7.38` |
| `T7.39` | Fair-W (s42) — dfd_c40 | 0.649 | 0.6490 | `predictions/cross_dataset/f2_spatres_full_s42.json` | `python verify/claim.py T7.39` |
| `T7.40` | Fair-W (s42) — CI lower — celebdf_v2 | 0.634 | 0.6336 | `predictions/cross_dataset/f2_spatres_full_s42.json` | `python verify/claim.py T7.40` |
| `T7.41` | Fair-W (s42) — CI lower — dfd_c23 | 0.814 | 0.8144 | `predictions/cross_dataset/f2_spatres_full_s42.json` | `python verify/claim.py T7.41` |
| `T7.42` | Fair-W (s42) — CI lower — dfd_c40 | 0.621 | 0.6214 | `predictions/cross_dataset/f2_spatres_full_s42.json` | `python verify/claim.py T7.42` |
| `T7.43` | Fair-W (s42) — CI upper — celebdf_v2 | 0.731 | 0.7313 | `predictions/cross_dataset/f2_spatres_full_s42.json` | `python verify/claim.py T7.43` |
| `T7.44` | Fair-W (s42) — CI upper — dfd_c23 | 0.852 | 0.8520 | `predictions/cross_dataset/f2_spatres_full_s42.json` | `python verify/claim.py T7.44` |
| `T7.45` | Fair-W (s42) — CI upper — dfd_c40 | 0.676 | 0.6759 | `predictions/cross_dataset/f2_spatres_full_s42.json` | `python verify/claim.py T7.45` |
| `T7.46` | CAFRL as specified — 3-seed mean — celebdf_v2 | 0.705 | 0.7047 | `predictions/cross_dataset/a0.json` +2 | `python verify/claim.py T7.46` |
| `T7.47` | CAFRL as specified — 3-seed mean — dfd_c23 | 0.819 | 0.8188 | `predictions/cross_dataset/a0.json` +2 | `python verify/claim.py T7.47` |
| `T7.48` | CAFRL as specified — 3-seed mean — dfd_c40 | 0.635 | 0.6351 | `predictions/cross_dataset/a0.json` +2 | `python verify/claim.py T7.48` |
| `T7.49` | CAFRL as specified — 3-seed band — celebdf_v2 | 0.051 | 0.0514 | `predictions/cross_dataset/a0.json` +2 | `python verify/claim.py T7.49` |
| `T7.50` | CAFRL as specified — 3-seed band — dfd_c23 | 0.04 | 0.0397 | `predictions/cross_dataset/a0.json` +2 | `python verify/claim.py T7.50` |
| `T7.51` | CAFRL as specified — 3-seed band — dfd_c40 | 0.035 | 0.0352 | `predictions/cross_dataset/a0.json` +2 | `python verify/claim.py T7.51` |
| `T7.52` | SpatialBase — 3-seed mean — celebdf_v2 | 0.686 | 0.6859 | `predictions/cross_dataset/b7_effnet_b0_mq_fliponly.json` +2 | `python verify/claim.py T7.52` |
| `T7.53` | SpatialBase — 3-seed mean — dfd_c23 | 0.825 | 0.8249 | `predictions/cross_dataset/b7_effnet_b0_mq_fliponly.json` +2 | `python verify/claim.py T7.53` |
| `T7.54` | SpatialBase — 3-seed mean — dfd_c40 | 0.65 | 0.6504 | `predictions/cross_dataset/b7_effnet_b0_mq_fliponly.json` +2 | `python verify/claim.py T7.54` |
| `T7.55` | SpatialBase — 3-seed band — celebdf_v2 | 0.035 | 0.0345 | `predictions/cross_dataset/b7_effnet_b0_mq_fliponly.json` +2 | `python verify/claim.py T7.55` |
| `T7.56` | SpatialBase — 3-seed band — dfd_c23 | 0.054 | 0.0538 | `predictions/cross_dataset/b7_effnet_b0_mq_fliponly.json` +2 | `python verify/claim.py T7.56` |
| `T7.57` | SpatialBase — 3-seed band — dfd_c40 | 0.031 | 0.0311 | `predictions/cross_dataset/b7_effnet_b0_mq_fliponly.json` +2 | `python verify/claim.py T7.57` |
| `T7.58` | Fair-N — 3-seed mean — celebdf_v2 | 0.647 | 0.6473 | `predictions/cross_dataset/f1_none_fair_s42.json` +2 | `python verify/claim.py T7.58` |
| `T7.59` | Fair-N — 3-seed mean — dfd_c23 | 0.792 | 0.7919 | `predictions/cross_dataset/f1_none_fair_s42.json` +2 | `python verify/claim.py T7.59` |
| `T7.60` | Fair-N — 3-seed mean — dfd_c40 | 0.659 | 0.6595 | `predictions/cross_dataset/f1_none_fair_s42.json` +2 | `python verify/claim.py T7.60` |
| `T7.61` | Fair-N — 3-seed band — celebdf_v2 | 0.17 | 0.1703 | `predictions/cross_dataset/f1_none_fair_s42.json` +2 | `python verify/claim.py T7.61` |
| `T7.62` | Fair-N — 3-seed band — dfd_c23 | 0.095 | 0.0953 | `predictions/cross_dataset/f1_none_fair_s42.json` +2 | `python verify/claim.py T7.62` |
| `T7.63` | Fair-N — 3-seed band — dfd_c40 | 0.073 | 0.0732 | `predictions/cross_dataset/f1_none_fair_s42.json` +2 | `python verify/claim.py T7.63` |
| `T7.64` | Fair-W — 3-seed mean — celebdf_v2 | 0.681 | 0.6808 | `predictions/cross_dataset/f2_spatres_full_s42.json` +2 | `python verify/claim.py T7.64` |
| `T7.65` | Fair-W — 3-seed mean — dfd_c23 | 0.835 | 0.8351 | `predictions/cross_dataset/f2_spatres_full_s42.json` +2 | `python verify/claim.py T7.65` |
| `T7.66` | Fair-W — 3-seed mean — dfd_c40 | 0.664 | 0.6644 | `predictions/cross_dataset/f2_spatres_full_s42.json` +2 | `python verify/claim.py T7.66` |
| `T7.67` | Fair-W — 3-seed band — celebdf_v2 | 0.048 | 0.0481 | `predictions/cross_dataset/f2_spatres_full_s42.json` +2 | `python verify/claim.py T7.67` |
| `T7.68` | Fair-W — 3-seed band — dfd_c23 | 0.057 | 0.0569 | `predictions/cross_dataset/f2_spatres_full_s42.json` +2 | `python verify/claim.py T7.68` |
| `T7.69` | Fair-W — 3-seed band — dfd_c40 | 0.054 | 0.0536 | `predictions/cross_dataset/f2_spatres_full_s42.json` +2 | `python verify/claim.py T7.69` |
| `T7.70` | Fair-N Celeb-DF per seed (s42 / s1 / s2) — celebdf_v2 | 0.668 | 0.6676 | `predictions/cross_dataset/f1_none_fair_s42.json` | `python verify/claim.py T7.70` |
| `T7.71` | Fair-N Celeb-DF — seed 1 — celebdf_v2 | 0.571 | 0.5709 | `predictions/cross_dataset/f1_none_fair_s1.json` | `python verify/claim.py T7.71` |
| `T7.72` | Fair-N Celeb-DF — seed 2 — celebdf_v2 | 0.703 | 0.7035 | `predictions/cross_dataset/f1_none_fair_s2.json` | `python verify/claim.py T7.72` |

- `T7.1` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.2` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.3` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.4` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.5` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.6` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.7` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.8` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.9` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.10` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.11` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.12` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.13` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.14` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.15` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.16` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.17` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.18` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.19` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.20` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.21` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.22` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.23` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.24` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.25` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.26` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.27` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.28` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.29` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.30` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.31` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.32` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.33` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.34` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.35` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.36` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.37` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.38` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.39` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.40` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.41` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.42` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.43` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.44` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.45` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.46` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.47` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.48` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.49` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.50` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.51` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.52` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.53` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.54` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.55` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.56` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.57` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.58` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.59` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.60` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.61` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.62` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.63` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.64` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.65` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.66` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.67` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.68` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.69` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.70` — The three runs read 0.668, 0.571 and 0.703; the other two are the rows below.
- `T7.71` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.
- `T7.72` — These cells carry the reported statistics (video-AUC, frame-AUC, frame-BCE and the marginal bootstrap CI) but no per-video scores — see predictions/GAPS.md. The map checks the released statistic against the printed value; it cannot re-derive it from scores.

## T8 — FaceShifter (held out), shipped recipe, seed-pooled

*Appendix D-B; `\label{tab:appfaceshifter}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `T8.1` | c23 — CAFRL (3-seed) | 0.822 | **not derivable** | `predictions/GAPS.md` | — |
| `T8.2` | c23 — backbone (3-seed) | 0.823 | 0.8230 | `predictions/faceshifter/b7_effnet_b0_mq_fliponly.json` +2 | `python verify/claim.py T8.2` |
| `T8.3` | c23 — paired Δ, CI, P(Δ>0) | -0.008 [-0.041, +0.025], P 0.30 | **not derivable** | `predictions/GAPS.md` | — |
| `T8.4` | c40 — CAFRL (3-seed) | 0.758 | **not derivable** | `predictions/GAPS.md` | — |
| `T8.5` | c40 — backbone (3-seed) | 0.732 | 0.7318 | `predictions/faceshifter/b7_effnet_b0_mq_fliponly.json` +2 | `python verify/claim.py T8.5` |
| `T8.6` | c40 — paired Δ, CI, P(Δ>0) | +0.022 [-0.021, +0.064], P 0.84 | **not derivable** | `predictions/GAPS.md` | — |

- `T8.1`, `T8.3`, `T8.4`, `T8.6` — **not derivable from this release.** The shipped-recipe FaceShifter evaluation (June out-of-distribution follow-up) saved no per-video predictions — this is audit defect D8, and the fair-recipe re-check that fixed it is what makes `predictions/faceshifter/` exist. The backbone column of that table is re-derivable (b7's FaceShifter predictions were regenerated from the frozen checkpoints); the CAFRL column and the paired statistics are not. Closing this needs a forward pass of the frozen a0/a1_grl checkpoints over the FaceShifter cell, which needs the crops.

## AppB2 — Harmonized baseline benchmark (video-AUC, FF++ test)

*Appendix C (Table 9 of the manuscript, compressed levels c23-c40 + AUC_comp); the complete seven-level matrix is evaluation/BENCHMARK.md; `\label{tab:appbench}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `AppB2.1` | Xception (lit) — c0 | 0.9949 | 0.9949 | `predictions/ffpp/b1_xception_lit.json` | `python verify/claim.py AppB2.1` |
| `AppB2.2` | Xception (lit) — c18 | 0.9948 | 0.9948 | `predictions/ffpp/b1_xception_lit.json` | `python verify/claim.py AppB2.2` |
| `AppB2.3` | Xception (lit) — c23 | 0.9944 | 0.9944 | `predictions/ffpp/b1_xception_lit.json` | `python verify/claim.py AppB2.3` |
| `AppB2.4` | Xception (lit) — c28 | 0.989 | 0.9890 | `predictions/ffpp/b1_xception_lit.json` | `python verify/claim.py AppB2.4` |
| `AppB2.5` | Xception (lit) — c32 | 0.9778 | 0.9778 | `predictions/ffpp/b1_xception_lit.json` | `python verify/claim.py AppB2.5` |
| `AppB2.6` | Xception (lit) — c36 | 0.928 | 0.9280 | `predictions/ffpp/b1_xception_lit.json` | `python verify/claim.py AppB2.6` |
| `AppB2.7` | Xception (lit) — c40 | 0.866 | 0.8660 | `predictions/ffpp/b1_xception_lit.json` | `python verify/claim.py AppB2.7` |
| `AppB2.8` | Xception (lit) — auc_comp | 0.9402 | 0.9402 | `predictions/ffpp/b1_xception_lit.json` | `python verify/claim.py AppB2.8` |
| `AppB2.9` | F3-Net (lit) — c0 | 0.9925 | 0.9925 | `predictions/ffpp/b2_f3net_lit.json` | `python verify/claim.py AppB2.9` |
| `AppB2.10` | F3-Net (lit) — c18 | 0.9924 | 0.9924 | `predictions/ffpp/b2_f3net_lit.json` | `python verify/claim.py AppB2.10` |
| `AppB2.11` | F3-Net (lit) — c23 | 0.9917 | 0.9917 | `predictions/ffpp/b2_f3net_lit.json` | `python verify/claim.py AppB2.11` |
| `AppB2.12` | F3-Net (lit) — c28 | 0.9835 | 0.9835 | `predictions/ffpp/b2_f3net_lit.json` | `python verify/claim.py AppB2.12` |
| `AppB2.13` | F3-Net (lit) — c32 | 0.9654 | 0.9654 | `predictions/ffpp/b2_f3net_lit.json` | `python verify/claim.py AppB2.13` |
| `AppB2.14` | F3-Net (lit) — c36 | 0.921 | 0.9210 | `predictions/ffpp/b2_f3net_lit.json` | `python verify/claim.py AppB2.14` |
| `AppB2.15` | F3-Net (lit) — c40 | 0.8599 | 0.8599 | `predictions/ffpp/b2_f3net_lit.json` | `python verify/claim.py AppB2.15` |
| `AppB2.16` | F3-Net (lit) — auc_comp | 0.9325 | 0.9325 | `predictions/ffpp/b2_f3net_lit.json` | `python verify/claim.py AppB2.16` |
| `AppB2.17` | FreqNet (lit) — c0 | 0.9808 | 0.9808 | `predictions/ffpp/b3_freqnet_lit.json` | `python verify/claim.py AppB2.17` |
| `AppB2.18` | FreqNet (lit) — c18 | 0.9899 | 0.9899 | `predictions/ffpp/b3_freqnet_lit.json` | `python verify/claim.py AppB2.18` |
| `AppB2.19` | FreqNet (lit) — c23 | 0.9877 | 0.9877 | `predictions/ffpp/b3_freqnet_lit.json` | `python verify/claim.py AppB2.19` |
| `AppB2.20` | FreqNet (lit) — c28 | 0.9652 | 0.9652 | `predictions/ffpp/b3_freqnet_lit.json` | `python verify/claim.py AppB2.20` |
| `AppB2.21` | FreqNet (lit) — c32 | 0.9274 | 0.9274 | `predictions/ffpp/b3_freqnet_lit.json` | `python verify/claim.py AppB2.21` |
| `AppB2.22` | FreqNet (lit) — c36 | 0.8541 | 0.8541 | `predictions/ffpp/b3_freqnet_lit.json` | `python verify/claim.py AppB2.22` |
| `AppB2.23` | FreqNet (lit) — c40 | 0.7684 | 0.7684 | `predictions/ffpp/b3_freqnet_lit.json` | `python verify/claim.py AppB2.23` |
| `AppB2.24` | FreqNet (lit) — auc_comp | 0.8788 | 0.8788 | `predictions/ffpp/b3_freqnet_lit.json` | `python verify/claim.py AppB2.24` |
| `AppB2.25` | Xception-mq (std aug) — c0 | 0.9921 | 0.9921 | `predictions/ffpp/b4_xception_mq.json` | `python verify/claim.py AppB2.25` |
| `AppB2.26` | Xception-mq (std aug) — c18 | 0.9899 | 0.9899 | `predictions/ffpp/b4_xception_mq.json` | `python verify/claim.py AppB2.26` |
| `AppB2.27` | Xception-mq (std aug) — c23 | 0.9872 | 0.9872 | `predictions/ffpp/b4_xception_mq.json` | `python verify/claim.py AppB2.27` |
| `AppB2.28` | Xception-mq (std aug) — c28 | 0.9838 | 0.9838 | `predictions/ffpp/b4_xception_mq.json` | `python verify/claim.py AppB2.28` |
| `AppB2.29` | Xception-mq (std aug) — c32 | 0.9803 | 0.9803 | `predictions/ffpp/b4_xception_mq.json` | `python verify/claim.py AppB2.29` |
| `AppB2.30` | Xception-mq (std aug) — c36 | 0.9739 | 0.9739 | `predictions/ffpp/b4_xception_mq.json` | `python verify/claim.py AppB2.30` |
| `AppB2.31` | Xception-mq (std aug) — c40 | 0.9679 | 0.9679 | `predictions/ffpp/b4_xception_mq.json` | `python verify/claim.py AppB2.31` |
| `AppB2.32` | Xception-mq (std aug) — auc_comp | 0.9765 | 0.9765 | `predictions/ffpp/b4_xception_mq.json` | `python verify/claim.py AppB2.32` |
| `AppB2.33` | Xception-mq (flip-only) — c0 | 0.9918 | 0.9918 | `predictions/ffpp/b4b_xception_mq_fliponly.json` | `python verify/claim.py AppB2.33` |
| `AppB2.34` | Xception-mq (flip-only) — c18 | 0.9893 | 0.9893 | `predictions/ffpp/b4b_xception_mq_fliponly.json` | `python verify/claim.py AppB2.34` |
| `AppB2.35` | Xception-mq (flip-only) — c23 | 0.9869 | 0.9869 | `predictions/ffpp/b4b_xception_mq_fliponly.json` | `python verify/claim.py AppB2.35` |
| `AppB2.36` | Xception-mq (flip-only) — c28 | 0.982 | 0.9820 | `predictions/ffpp/b4b_xception_mq_fliponly.json` | `python verify/claim.py AppB2.36` |
| `AppB2.37` | Xception-mq (flip-only) — c32 | 0.9772 | 0.9772 | `predictions/ffpp/b4b_xception_mq_fliponly.json` | `python verify/claim.py AppB2.37` |
| `AppB2.38` | Xception-mq (flip-only) — c36 | 0.9691 | 0.9691 | `predictions/ffpp/b4b_xception_mq_fliponly.json` | `python verify/claim.py AppB2.38` |
| `AppB2.39` | Xception-mq (flip-only) — c40 | 0.9631 | 0.9631 | `predictions/ffpp/b4b_xception_mq_fliponly.json` | `python verify/claim.py AppB2.39` |
| `AppB2.40` | Xception-mq (flip-only) — auc_comp | 0.9728 | 0.9728 | `predictions/ffpp/b4b_xception_mq_fliponly.json` | `python verify/claim.py AppB2.40` |
| `AppB2.41` | F3-Net-mq — c0 | 0.9911 | 0.9911 | `predictions/ffpp/b5_f3net_mq.json` | `python verify/claim.py AppB2.41` |
| `AppB2.42` | F3-Net-mq — c18 | 0.9902 | 0.9902 | `predictions/ffpp/b5_f3net_mq.json` | `python verify/claim.py AppB2.42` |
| `AppB2.43` | F3-Net-mq — c23 | 0.9885 | 0.9885 | `predictions/ffpp/b5_f3net_mq.json` | `python verify/claim.py AppB2.43` |
| `AppB2.44` | F3-Net-mq — c28 | 0.9831 | 0.9831 | `predictions/ffpp/b5_f3net_mq.json` | `python verify/claim.py AppB2.44` |
| `AppB2.45` | F3-Net-mq — c32 | 0.9766 | 0.9766 | `predictions/ffpp/b5_f3net_mq.json` | `python verify/claim.py AppB2.45` |
| `AppB2.46` | F3-Net-mq — c36 | 0.9683 | 0.9683 | `predictions/ffpp/b5_f3net_mq.json` | `python verify/claim.py AppB2.46` |
| `AppB2.47` | F3-Net-mq — c40 | 0.9551 | 0.9551 | `predictions/ffpp/b5_f3net_mq.json` | `python verify/claim.py AppB2.47` |
| `AppB2.48` | F3-Net-mq — auc_comp | 0.9708 | 0.9708 | `predictions/ffpp/b5_f3net_mq.json` | `python verify/claim.py AppB2.48` |
| `AppB2.49` | FreqNet-mq — c0 | 0.98 | 0.9800 | `predictions/ffpp/b6_freqnet_mq.json` | `python verify/claim.py AppB2.49` |
| `AppB2.50` | FreqNet-mq — c18 | 0.9745 | 0.9745 | `predictions/ffpp/b6_freqnet_mq.json` | `python verify/claim.py AppB2.50` |
| `AppB2.51` | FreqNet-mq — c23 | 0.9693 | 0.9693 | `predictions/ffpp/b6_freqnet_mq.json` | `python verify/claim.py AppB2.51` |
| `AppB2.52` | FreqNet-mq — c28 | 0.9566 | 0.9566 | `predictions/ffpp/b6_freqnet_mq.json` | `python verify/claim.py AppB2.52` |
| `AppB2.53` | FreqNet-mq — c32 | 0.9383 | 0.9383 | `predictions/ffpp/b6_freqnet_mq.json` | `python verify/claim.py AppB2.53` |
| `AppB2.54` | FreqNet-mq — c36 | 0.9131 | 0.9131 | `predictions/ffpp/b6_freqnet_mq.json` | `python verify/claim.py AppB2.54` |
| `AppB2.55` | FreqNet-mq — c40 | 0.8787 | 0.8787 | `predictions/ffpp/b6_freqnet_mq.json` | `python verify/claim.py AppB2.55` |
| `AppB2.56` | FreqNet-mq — auc_comp | 0.9217 | 0.9217 | `predictions/ffpp/b6_freqnet_mq.json` | `python verify/claim.py AppB2.56` |
| `AppB2.57` | SpatialBase — c0 | 0.9919 | 0.9919 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py AppB2.57` |
| `AppB2.58` | SpatialBase — c18 | 0.9892 | 0.9892 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py AppB2.58` |
| `AppB2.59` | SpatialBase — c23 | 0.9867 | 0.9867 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py AppB2.59` |
| `AppB2.60` | SpatialBase — c28 | 0.981 | 0.9810 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py AppB2.60` |
| `AppB2.61` | SpatialBase — c32 | 0.9758 | 0.9758 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py AppB2.61` |
| `AppB2.62` | SpatialBase — c36 | 0.9678 | 0.9678 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py AppB2.62` |
| `AppB2.63` | SpatialBase — c40 | 0.959 | 0.9590 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py AppB2.63` |
| `AppB2.64` | SpatialBase — auc_comp | 0.9709 | 0.9709 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py AppB2.64` |

- `AppB2.1` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.2` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.3` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.4` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.5` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.6` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.7` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.8` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.9` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.10` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.11` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.12` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.13` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.14` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.15` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.16` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.17` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.18` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.19` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.20` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.21` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.22` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.23` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.24` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.25` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.26` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.27` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.28` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.29` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.30` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.31` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.32` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.33` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.34` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.35` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.36` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.37` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.38` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.39` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.40` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.41` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.42` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.43` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.44` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.45` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.46` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.47` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.48` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.49` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.50` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.51` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.52` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.53` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.54` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.55` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.56` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.57` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.58` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.59` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.60` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.61` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.62` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.63` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.
- `AppB2.64` — Every cell is recomputed from the released per-video scores. All eight rows are descriptive: none was pre-registered and none enters the confirmatory family. The SpatialBase row repeats the sweep table's.

## AppC — Baseline reproduction and the augmentation confound

*Appendix C; `\label{app:baselines}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `AppC.1` | Xception, literature protocol, c40 | 0.866 | 0.8660 | `predictions/ffpp/b1_xception_lit.json` | `python verify/claim.py AppC.1` |
| `AppC.2` | F3-Net, literature protocol, c40 | 0.86 | 0.8599 | `predictions/ffpp/b2_f3net_lit.json` | `python verify/claim.py AppC.2` |
| `AppC.3` | FreqNet, literature protocol, c40 | 0.768 | 0.7684 | `predictions/ffpp/b3_freqnet_lit.json` | `python verify/claim.py AppC.3` |
| `AppC.4` | Multi-CRF training moves Xception c23 0.994 -> 0.987 | 0.994 | 0.9944 | `predictions/ffpp/b1_xception_lit.json` | `python verify/claim.py AppC.4` |
| `AppC.5` | ... to Xception-mq c23 0.987 | 0.987 | 0.9872 | `predictions/ffpp/b4_xception_mq.json` | `python verify/claim.py AppC.5` |
| `AppC.6` | Multi-CRF training moves F3-Net c23 0.992 -> 0.989 | 0.992 | 0.9917 | `predictions/ffpp/b2_f3net_lit.json` | `python verify/claim.py AppC.6` |
| `AppC.7` | ... to F3-Net-mq c23 0.989 | 0.989 | 0.9885 | `predictions/ffpp/b5_f3net_mq.json` | `python verify/claim.py AppC.7` |
| `AppC.8` | FreqNet gains most from multi-CRF: 0.768 -> 0.879 at c40 | 0.879 | 0.8787 | `predictions/ffpp/b6_freqnet_mq.json` | `python verify/claim.py AppC.8` |
| `AppC.9` | Augmentation recovery, example 1: 0.764 (flip-only frame-AUC, c40) | 0.764 | 0.7642 | `predictions/ffpp/b1_xception_lit_fliponly.json` | `python verify/claim.py AppC.9` |
| `AppC.10` | Augmentation recovery, example 1: → 0.791 (with augmentation) | 0.791 | 0.7915 | `predictions/ffpp/b1_xception_lit.json` | `python verify/claim.py AppC.10` |
| `AppC.11` | Augmentation recovery, example 2: 0.725 (flip-only frame-AUC, c40) | 0.725 | 0.7250 | `predictions/ffpp/b2_f3net_lit_fliponly.json` | `python verify/claim.py AppC.11` |
| `AppC.12` | Augmentation recovery, example 2: → 0.780 (with augmentation) | 0.78 | 0.7802 | `predictions/ffpp/b2_f3net_lit.json` | `python verify/claim.py AppC.12` |
| `AppC.13` | Augmentation confound control: Xception-mq 0.968 (with augmentation) | 0.968 | 0.9679 | `predictions/ffpp/b4_xception_mq.json` | `python verify/claim.py AppC.13` |
| `AppC.14` | Augmentation confound control: → 0.963 flip-only | 0.963 | 0.9631 | `predictions/ffpp/b4b_xception_mq_fliponly.json` | `python verify/claim.py AppC.14` |
| `AppC.15` | Synthetic JPEG augmentation at real c40 | 0.89 | 0.8898 | `predictions/p2_probe/p2a_xcep_jpeg.json` | `python verify/claim.py AppC.15` |
| `AppC.16` | Real CRF re-encodes at real c40 (same recipe) | 0.963 | 0.9631 | `predictions/ffpp/b4b_xception_mq_fliponly.json` | `python verify/claim.py AppC.16` |
| `AppC.17` | The +7.3 pt real-CRF vs synthetic-JPEG gap | 0.073 | 0.0733 | `predictions/ffpp/b4b_xception_mq_fliponly.json` +1 | `python verify/claim.py AppC.17` |
| `AppC.18` | Synthetic-JPEG arm — marginal CI | [0.8608, 0.9161] | recorded | `predictions/p2_probe/p2a_xcep_jpeg.json` | `python verify/claim.py AppC.18` |
| `AppC.19` | Real-CRF arm — marginal CI lower | 0.9484 | 0.9484 | `predictions/ffpp/b4b_xception_mq_fliponly.json` | `python verify/claim.py AppC.19` |
| `AppC.20` | Real-CRF arm — marginal CI upper | 0.9758 | 0.9758 | `predictions/ffpp/b4b_xception_mq_fliponly.json` | `python verify/claim.py AppC.20` |
| `AppC.21` | Calibration (evaluation/CALIBRATION.md) — Xception (lit), frame-AUC c23 | 0.9901 | 0.9901 | `predictions/ffpp/b1_xception_lit.json` | `python verify/claim.py AppC.21` |
| `AppC.22` | Calibration (evaluation/CALIBRATION.md) — Xception (lit), frame-AUC c40 | 0.7915 | 0.7915 | `predictions/ffpp/b1_xception_lit.json` | `python verify/claim.py AppC.22` |
| `AppC.23` | Calibration (evaluation/CALIBRATION.md) — F3-Net (lit), frame-AUC c23 | 0.985 | 0.9850 | `predictions/ffpp/b2_f3net_lit.json` | `python verify/claim.py AppC.23` |
| `AppC.24` | Calibration (evaluation/CALIBRATION.md) — F3-Net (lit), frame-AUC c40 | 0.7802 | 0.7802 | `predictions/ffpp/b2_f3net_lit.json` | `python verify/claim.py AppC.24` |
| `AppC.25` | Calibration (evaluation/CALIBRATION.md) — FreqNet (lit), frame-AUC c23 | 0.9673 | 0.9673 | `predictions/ffpp/b3_freqnet_lit.json` | `python verify/claim.py AppC.25` |
| `AppC.26` | Calibration (evaluation/CALIBRATION.md) — FreqNet (lit), frame-AUC c40 | 0.6802 | 0.6802 | `predictions/ffpp/b3_freqnet_lit.json` | `python verify/claim.py AppC.26` |
| `AppC.27` | Calibration shortfall at c40: Xception 3.5 frame-AUC points below the anchor | 0.035 | recorded | `predictions/ffpp/b1_xception_lit.json` | `python verify/claim.py AppC.27` |
| `AppC.28` | Calibration shortfall at c40: F3-Net 4.7 frame-AUC points below the anchor | 0.047 | recorded | `predictions/ffpp/b2_f3net_lit.json` | `python verify/claim.py AppC.28` |
| `AppC.29` | Augmentation recovery, Xception: +2.7 frame-AUC points at c40 | 0.027 | recorded | `predictions/ffpp/b1_xception_lit_fliponly.json` | `python verify/claim.py AppC.29` |
| `AppC.30` | Augmentation recovery, F3-Net: +5.5 frame-AUC points at c40 | 0.055 | recorded | `predictions/ffpp/b2_f3net_lit_fliponly.json` | `python verify/claim.py AppC.30` |
| `AppC.31` | F3-Net-mq − SpatialBase at c40 — Δ and CI | -0.0040 [-0.0151, +0.0068] | -0.0040 | `verify/expected.json` +2 | `python verify/claim.py AppC.31 --bootstrap` |
| `AppC.32` | FreqNet-mq − SpatialBase at c40 — Δ and CI | -0.0804 [-0.1084, -0.0543] | -0.0804 | `verify/expected.json` +2 | `python verify/claim.py AppC.32 --bootstrap` |
| `AppC.33` | F3-Net-mq − Xception-mq at c40 — Δ and CI | -0.0128 [-0.0236, -0.0029] | -0.0128 | `verify/expected.json` +2 | `python verify/claim.py AppC.33 --bootstrap` |
| `AppC.34` | F3-Net-mq − SpatialBase at AUC_comp — Δ and CI | -0.0002 [-0.0073, +0.0066] | recorded | `predictions/ffpp/b5_f3net_mq.json` | `python verify/claim.py AppC.34` |
| `AppC.35` | FreqNet-mq − SpatialBase at AUC_comp — Δ and CI | -0.0493 [-0.0671, -0.0330] | recorded | `predictions/ffpp/b6_freqnet_mq.json` | `python verify/claim.py AppC.35` |
| `AppC.36` | F3-Net-mq − Xception-mq at AUC_comp — Δ and CI | -0.0057 [-0.0124, +0.0007] | recorded | `predictions/ffpp/b5_f3net_mq.json` | `python verify/claim.py AppC.36` |

- `AppC.10` — Corrected in the manuscript (W1, 2026-08-19) from 0.792 to the released frame-AUC 0.79150.
- `AppC.15` — Marginal statistic only — this arm has no per-video scores (predictions/GAPS.md), so the +7.3 pt comparison is two marginal AUCs with non-overlapping CIs, not a paired delta.
- `AppC.18` — Stored as `cells.ci` in that file ([0.86080240, 0.91608638]); this arm kept no per-video scores (predictions/GAPS.md), so the interval is the one the campaign computed, not one this release can recompute.
- `AppC.27` — 0.8261 (DeepfakeBench Table 3) minus the released 0.79150. The anchor is a citation, not a released artifact.
- `AppC.28` — 0.8271 (DeepfakeBench Table 3) minus the released 0.78018.
- `AppC.29` — 0.79150 minus 0.76418, both released frame-AUCs checked by the four rows above and by the two flip-only rows.
- `AppC.30` — 0.78018 minus 0.72497, both released frame-AUCs.
- `AppC.34` — The AUC_comp endpoint of the same paired bootstrap (10k replicates, seed 0, sorted-key order), computed with the released harness's `paired_auc_comp_delta`; the contrast checker pins level-wise deltas only, so this endpoint is recorded rather than asserted.
- `AppC.35` — As above, for the FreqNet arm.
- `AppC.36` — As above, for the augmentation-matched Xception pair.

## X1 — Key numbers in the running text

*Sections VII-D, VIII and IX; Appendix D*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `X1.1` | Clean-anchored drop, SpatialBase (0.016) | 0.016 | 0.0158 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py X1.1` |
| `X1.2` | Clean-anchored drop, TrunkCtrl (0.019) | 0.019 | 0.0190 | `predictions/ffpp/trunk_recipe_s42.json` +2 | `python verify/claim.py X1.2` |
| `X1.3` | Clean-anchored drop, Fair-N (0.017) | 0.017 | 0.0167 | `predictions/ffpp/f1_none_fair_s42.json` | `python verify/claim.py X1.3` |
| `X1.4` | Clean-anchored drop, Fair-W (0.015) | 0.015 | 0.0154 | `predictions/ffpp/f2_spatres_full_s42.json` | `python verify/claim.py X1.4` |
| `X1.5` | Clean-anchored drop, shipped CAFRL (0.026) | 0.026 | 0.0261 | `predictions/ffpp/a0.json` | `python verify/claim.py X1.5` |
| `X1.6` | FaceShifter fair 3-seed mean, Fair-N c23 | 0.799 | 0.7992 | `predictions/faceshifter/f1_none_fair_s42.json` +2 | `python verify/claim.py X1.6` |
| `X1.7` | FaceShifter fair 3-seed mean, Fair-N c40 | 0.711 | 0.7109 | `predictions/faceshifter/f1_none_fair_s42.json` +2 | `python verify/claim.py X1.7` |
| `X1.8` | FaceShifter fair 3-seed mean, Fair-W c23 | 0.768 | 0.7681 | `predictions/faceshifter/f2_spatres_full_s42.json` +2 | `python verify/claim.py X1.8` |
| `X1.9` | FaceShifter fair 3-seed mean, Fair-W c40 | 0.707 | 0.7071 | `predictions/faceshifter/f2_spatres_full_s42.json` +2 | `python verify/claim.py X1.9` |
| `X1.10` | FaceShifter SpatialBase 3-seed mean, c23 | 0.823 | 0.8230 | `predictions/faceshifter/b7_effnet_b0_mq_fliponly.json` +2 | `python verify/claim.py X1.10` |
| `X1.11` | FaceShifter SpatialBase 3-seed mean, c40 | 0.732 | 0.7318 | `predictions/faceshifter/b7_effnet_b0_mq_fliponly.json` +2 | `python verify/claim.py X1.11` |
| `X1.12` | Fair variants sit below the backbone: Fair-N pool Δ ≈ -0.033 at c40 | -0.0325 | -0.0325 | `verify/expected.json` +6 | `python verify/claim.py X1.12 --bootstrap` |
| `X1.13` | Fair variants sit below the backbone: Fair-W pool Δ ≈ -0.032 at c40 | -0.0318 | -0.0318 | `verify/expected.json` +6 | `python verify/claim.py X1.13 --bootstrap` |
| `X1.14` | Sign-inconsistent single-seed leans: Fair-N +0.022 | +0.0220 | 0.0220 | `verify/expected.json` +4 | `python verify/claim.py X1.14 --bootstrap` |
| `X1.15` | Sign-inconsistent single-seed leans: Fair-W -0.023 | -0.0227 | -0.0227 | `verify/expected.json` +4 | `python verify/claim.py X1.15 --bootstrap` |
| `X1.16` | Xception overfits: ~11 pt below smaller models on unseen FaceShifter at c23 | ~11 pt | **not derivable** | `predictions/GAPS.md` | — |
| `X1.17` | Campaign training hours (~270 saved, ~35 re-tests, ~31 confirmation seeds) | training hours | **not derivable** | `predictions/GAPS.md` | — |

- `X1.16` — **not derivable from this release.** Same cause: the Xception FaceShifter numbers come from the June follow-up and were never persisted as predictions. The Xception FaceShifter cells come from the same June follow-up as the FaceShifter table's CAFRL column and were never saved as predictions. The paper now also prints the paired interval recorded in the campaign journal for this observation (+0.113, CI [+0.064, +0.162], single seed, n=280), with an explicit note that it is journal-recorded and not re-derivable from this release.
- `X1.17` — **not derivable from this release.** Compute accounting is recorded in the internal campaign journal, which is not part of this release, and no audited ledger of total consumed compute was kept -- the paper says so rather than reconstructing one. What is released is every run's configuration, its per-epoch curve and its selected epoch, which is what a reader would need to price it. Wall-clock accounting lives in the internal campaign journal, which is not part of this release; the run count and their configurations are (configs/RUNS.md). The manuscript states these as wall-clock training hours on the 2xA100 node and says explicitly that no audited ledger of total consumed compute exists.

## M1 — Mechanism claims, from the released training curves

*Sections VI–VIII and Fig. 4*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `M1.1` | γ grows to its peak 0.146 (deadlock broken, Fair-W) | 0.146 | 0.1464 | `curves/f2_spatres_full_s42.json` | `python verify/claim.py M1.1` |
| `M1.2` | γ decays to ≈0.03 by the end of training (Fair-W) | 0.031 | 0.0307 | `curves/f2_spatres_full_s42.json` | `python verify/claim.py M1.2` |
| `M1.3` | γ at the selected epoch (Fair-W) | 0.14 | 0.1400 | `curves/f2_spatres_full_s42.json` | `python verify/claim.py M1.3` |
| `M1.4` | Frequency head is individually discriminative: ≈0.98 at c23 (Fair-W) | 0.98 | recorded | `curves/f2_spatres_full_s42.json` | `python verify/claim.py M1.4` |
| `M1.5` | Frequency head is individually discriminative: ≈0.91 at c40 (Fair-W) | 0.91 | recorded | `curves/f2_spatres_full_s42.json` | `python verify/claim.py M1.5` |
| `M1.6` | The estimator's ±1-bin accuracy without the adversary (the 0.88 premise) | 0.876 | 0.8758 | `probes/p1_compression_estimator.json` | `python verify/claim.py M1.6` |
| `M1.7` | The estimator's ±1-bin accuracy under the GRL falls to ≈0.4 (defect D6) | 0.4 | recorded | `curves/a0.json` | `python verify/claim.py M1.7` |
| `M1.8` | The consistency loss ran 40–120× the classification loss (defect D1) | 40–120x | recorded | `curves/a0.json` | `python verify/claim.py M1.8` |
| `M1.9` | The band-energy premise the frequency design rests on | measurement | recorded | `probes/band_energy.json` | `python verify/claim.py M1.9` |

- `M1.1` — Corrected in the manuscript (W1, 2026-08-19) from 0.145 to the released series peak 0.14636 (epoch 6, seed 42; seeds 1 and 2 peak at 0.158 and 0.151).
- `M1.4` — The manuscript quotes the plateau the head reaches over the second half of training, together with its epoch-1 and selected-epoch values (3-seed means: 0.81/0.71 at epoch 1, 0.97/0.85 at the selected epoch, c23/c40); the released series carries every epoch of every seed.
- `M1.7` — The released a0 curve starts at 1.00 and ends at 0.33, passing through ≈0.4 in the adversarial phase; the fair arms stay healthy (F1 min 0.89, F2 min 0.93 — same tag in their curve files).
- `M1.8` — Released as two series in curves/a0.json — loss/cons and loss/cls — so the ratio is computable per epoch. The raw ratio peaks at about 134x at epoch 13; the manuscript's 40–120x is the range around the compressed-phase onset.
- `M1.9` — Per-level band energies on real crops (Phase 2).

## AppE — Statistical robustness (cluster and two-level bootstraps, equivalence, multiplicity)

*Appendix E and Section IV (statistical reporting); `\label{app:stats}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `AppE.1` | SpatialBase − CAFRL as specified (s42) — clustered CI lower | 0.0182 | 0.0182 | `evaluation/analysis/cluster_bootstrap.json` | `python verify/claim.py AppE.1` |
| `AppE.2` | SpatialBase − CAFRL as specified (s42) — clustered CI upper | 0.0569 | 0.0569 | `evaluation/analysis/cluster_bootstrap.json` | `python verify/claim.py AppE.2` |
| `AppE.3` | Fair-N − CAFRL−adv (s42) — clustered CI lower | 0.0222 | 0.0222 | `evaluation/analysis/cluster_bootstrap.json` | `python verify/claim.py AppE.3` |
| `AppE.4` | Fair-N − CAFRL−adv (s42) — clustered CI upper | 0.058 | 0.0580 | `evaluation/analysis/cluster_bootstrap.json` | `python verify/claim.py AppE.4` |
| `AppE.5` | Fair-N − SpatialBase (s42) — clustered CI lower | -0.0095 | -0.0095 | `evaluation/analysis/cluster_bootstrap.json` | `python verify/claim.py AppE.5` |
| `AppE.6` | Fair-N − SpatialBase (s42) — clustered CI upper | 0.008 | 0.0080 | `evaluation/analysis/cluster_bootstrap.json` | `python verify/claim.py AppE.6` |
| `AppE.7` | Fair-W − SpatialBase (s42) — clustered CI lower | -0.0026 | -0.0026 | `evaluation/analysis/cluster_bootstrap.json` | `python verify/claim.py AppE.7` |
| `AppE.8` | Fair-W − SpatialBase (s42) — clustered CI upper | 0.0137 | 0.0137 | `evaluation/analysis/cluster_bootstrap.json` | `python verify/claim.py AppE.8` |
| `AppE.9` | Fair-N pool − SpatialBase pool (3v3) — clustered CI lower | -0.0064 | -0.0064 | `evaluation/analysis/cluster_bootstrap.json` | `python verify/claim.py AppE.9` |
| `AppE.10` | Fair-N pool − SpatialBase pool (3v3) — clustered CI upper | 0.0046 | 0.0046 | `evaluation/analysis/cluster_bootstrap.json` | `python verify/claim.py AppE.10` |
| `AppE.11` | Fair-W pool − SpatialBase pool (3v3) — clustered CI lower | -0.0042 | -0.0042 | `evaluation/analysis/cluster_bootstrap.json` | `python verify/claim.py AppE.11` |
| `AppE.12` | Fair-W pool − SpatialBase pool (3v3) — clustered CI upper | 0.0085 | 0.0085 | `evaluation/analysis/cluster_bootstrap.json` | `python verify/claim.py AppE.12` |
| `AppE.13` | SpatialBase (s42) − TrunkCtrl pool — clustered CI lower | -0.0119 | -0.0119 | `evaluation/analysis/cluster_bootstrap.json` | `python verify/claim.py AppE.13` |
| `AppE.14` | SpatialBase (s42) − TrunkCtrl pool — clustered CI upper | 0.0042 | 0.0042 | `evaluation/analysis/cluster_bootstrap.json` | `python verify/claim.py AppE.14` |
| `AppE.15` | TrunkCtrl pool − spatial-residual (s42) — clustered CI lower | 0.0296 | 0.0296 | `evaluation/analysis/cluster_bootstrap.json` | `python verify/claim.py AppE.15` |
| `AppE.16` | TrunkCtrl pool − spatial-residual (s42) — clustered CI upper | 0.0715 | 0.0715 | `evaluation/analysis/cluster_bootstrap.json` | `python verify/claim.py AppE.16` |
| `AppE.17` | FaceShifter: Fair-N pool − SpatialBase pool — clustered CI lower | -0.0546 | -0.0546 | `evaluation/analysis/cluster_bootstrap.json` | `python verify/claim.py AppE.17` |
| `AppE.18` | FaceShifter: Fair-N pool − SpatialBase pool — clustered CI upper | -0.0109 | -0.0109 | `evaluation/analysis/cluster_bootstrap.json` | `python verify/claim.py AppE.18` |
| `AppE.19` | FaceShifter: Fair-W pool − SpatialBase pool — clustered CI lower | -0.0563 | -0.0563 | `evaluation/analysis/cluster_bootstrap.json` | `python verify/claim.py AppE.19` |
| `AppE.20` | FaceShifter: Fair-W pool − SpatialBase pool — clustered CI upper | -0.007 | -0.0070 | `evaluation/analysis/cluster_bootstrap.json` | `python verify/claim.py AppE.20` |
| `AppE.21` | FaceShifter: Fair-N (s42) − SpatialBase pool — clustered CI lower | -0.0045 | -0.0045 | `evaluation/analysis/cluster_bootstrap.json` | `python verify/claim.py AppE.21` |
| `AppE.22` | FaceShifter: Fair-N (s42) − SpatialBase pool — clustered CI upper | 0.05 | 0.0500 | `evaluation/analysis/cluster_bootstrap.json` | `python verify/claim.py AppE.22` |
| `AppE.23` | FaceShifter: Fair-W (s42) − SpatialBase pool — clustered CI lower | -0.0534 | -0.0534 | `evaluation/analysis/cluster_bootstrap.json` | `python verify/claim.py AppE.23` |
| `AppE.24` | FaceShifter: Fair-W (s42) − SpatialBase pool — clustered CI upper | 0.0082 | 0.0082 | `evaluation/analysis/cluster_bootstrap.json` | `python verify/claim.py AppE.24` |
| `AppE.25` | Seeds resampled: Fair-N − SpatialBase, CI lower | -0.0119 | -0.0119 | `evaluation/analysis/seed_uncertainty.json` | `python verify/claim.py AppE.25` |
| `AppE.26` | Seeds resampled: Fair-N − SpatialBase, CI upper | 0.0123 | 0.0123 | `evaluation/analysis/seed_uncertainty.json` | `python verify/claim.py AppE.26` |
| `AppE.27` | Seeds resampled: Fair-W − SpatialBase, CI lower | -0.0065 | -0.0065 | `evaluation/analysis/seed_uncertainty.json` | `python verify/claim.py AppE.27` |
| `AppE.28` | Seeds resampled: Fair-W − SpatialBase, CI upper | 0.0164 | 0.0164 | `evaluation/analysis/seed_uncertainty.json` | `python verify/claim.py AppE.28` |
| `AppE.29` | Equivalence margin (post hoc) | 0.01 | 0.0100 | `evaluation/analysis/equivalence.json` | `python verify/claim.py AppE.29` |
| `AppE.30` | TOST Fair-N: 90% CI lower (video unit) | -0.0057 | -0.0057 | `evaluation/analysis/equivalence.json` | `python verify/claim.py AppE.30` |
| `AppE.31` | TOST Fair-N: 90% CI upper (video unit) | 0.0036 | 0.0036 | `evaluation/analysis/equivalence.json` | `python verify/claim.py AppE.31` |
| `AppE.32` | TOST Fair-N: p (video unit) | 0.001 | 0.0010 | `evaluation/analysis/equivalence.json` | `python verify/claim.py AppE.32` |
| `AppE.33` | TOST Fair-W: 90% CI lower (video unit) | -0.0025 | -0.0025 | `evaluation/analysis/equivalence.json` | `python verify/claim.py AppE.33` |
| `AppE.34` | TOST Fair-W: 90% CI upper (video unit) | 0.0071 | 0.0071 | `evaluation/analysis/equivalence.json` | `python verify/claim.py AppE.34` |
| `AppE.35` | TOST Fair-W: p (video unit) | 0.006 | 0.0064 | `evaluation/analysis/equivalence.json` | `python verify/claim.py AppE.35` |
| `AppE.36` | TOST worst case over the four cluster units (Fair-W) | 0.01 | 0.0103 | `evaluation/analysis/equivalence.json` | `python verify/claim.py AppE.36` |
| `AppE.37` | Tightest margin concluded, Fair-N | 0.006 | 0.0058 | `evaluation/analysis/equivalence.json` | `python verify/claim.py AppE.37` |
| `AppE.38` | Tightest margin concluded, Fair-W | 0.008 | 0.0075 | `evaluation/analysis/equivalence.json` | `python verify/claim.py AppE.38` |
| `AppE.39` | Seeds resampled: Fair-W 90% CI upper | 0.0131 | 0.0131 | `evaluation/analysis/equivalence.json` | `python verify/claim.py AppE.39` |
| `AppE.40` | Seeds resampled: Fair-W TOST p | 0.11 | 0.1077 | `evaluation/analysis/equivalence.json` | `python verify/claim.py AppE.40` |
| `AppE.41` | MDE, video unit (80% power) | 0.83 | 0.8300 | `evaluation/analysis/mde.json` | `python verify/claim.py AppE.41` |
| `AppE.42` | MDE, source-identity cluster unit (80% power) | 0.91 | 0.9100 | `evaluation/analysis/mde.json` | `python verify/claim.py AppE.42` |
| `AppE.43` | MDE, seed as the experimental unit (80% power) | 0.0149 | 0.0149 | `evaluation/analysis/mde.json` | `python verify/claim.py AppE.43` |
| `AppE.44` | MDE implied by the two-level bootstrap | 1.65 | 1.6500 | `evaluation/analysis/mde.json` | `python verify/claim.py AppE.44` |
| `AppE.45` | Smallest observed across-seed SD (Fair-W) | 0.0023 | 0.0023 | `evaluation/analysis/mde.json` | `python verify/claim.py AppE.45` |
| `AppE.46` | Largest observed across-seed SD (SpatialBase) | 0.0065 | 0.0065 | `evaluation/analysis/mde.json` | `python verify/claim.py AppE.46` |
| `AppE.47` | Bonferroni threshold over the 13-comparison family | 0.0038 | 0.0038 | `evaluation/analysis/multiplicity.json` | `python verify/claim.py AppE.47` |
| `AppE.48` | p, STOP-gate contrast (cluster unit) | 0.0002 | 0.0002 | `evaluation/analysis/multiplicity.json` | `python verify/claim.py AppE.48` |
| `AppE.49` | p, fair-recipe recovery (cluster unit) | 1.4e-05 | 0.0000 | `evaluation/analysis/multiplicity.json` | `python verify/claim.py AppE.49` |
| `AppE.50` | p, recipe share (cluster unit) | 5.5e-06 | 0.0000 | `evaluation/analysis/multiplicity.json` | `python verify/claim.py AppE.50` |
| `AppE.51` | p, real-CRF vs synthetic-JPEG training gap (unpaired) | 3.3e-06 | 0.0000 | `evaluation/analysis/multiplicity.json` | `python verify/claim.py AppE.51` |
| `AppE.52` | p, FaceShifter Fair-N pooled deficit | 0.0037 | 0.0037 | `evaluation/analysis/multiplicity.json` | `python verify/claim.py AppE.52` |
| `AppE.53` | p, FaceShifter Fair-W pooled deficit | 0.012 | 0.0121 | `evaluation/analysis/multiplicity.json` | `python verify/claim.py AppE.53` |

- `AppE.37` — Printed in the paper as 0.6 AUC points.
- `AppE.38` — Printed in the paper as 0.8 AUC points.
- `AppE.41` — In AUC points; printed in Section IV as 0.83.
- `AppE.43` — Printed in the paper as 1.5 AUC points; the Fair-W pair gives 1.47.
- `AppE.44` — Printed in the paper as 1.7 AUC points.

## Release claims

The present-tense claims the manuscript makes about this repository.

| id | claim | where | status | artifacts |
|---|---|---|---|---|
| `R1` | Per-video predictions for every reported cell | Reproducibility statement; Abstract; contribution C4 | checked | `predictions/ffpp/a0.json`, `predictions/ffpp/a1_grl_s1.json`, `predictions/ffpp/a1_grl_s2.json` … (+47) |
| `R2` | The frozen pre-registered decision rules, verbatim, with their git history | Reproducibility statement; Section IV-C; Abstract | checked | `preregistration/PREREGISTRATION-A1.md`, `preregistration/STOP-GATE.md`, `preregistration/retest-gates.md` … (+2) |
| `R3` | The full D1–D8 audit ledger | Abstract; Appendix B | checked | `audit/LEDGER-D1-D8.md`, `audit/AUDIT-PASSES.md`, `audit/README.md` |
| `R4` | Configurations for every arm in the tables | Reproducibility statement | checked | `configs/runs/a0.yaml`, `configs/runs/a1_grl_s1.yaml`, `configs/runs/a1_grl_s2.yaml` … (+61) |
| `R5` | The evaluation harness (paired bootstrap, seed pooling) | Reproducibility statement; Section IV-B | checked | `evaluation/src/evaluation/metrics.py`, `evaluation/src/evaluation/aggregate_runs.py`, `evaluation/rederive.py` … (+2) |
| `R6` | The figure-generation scripts | Reproducibility statement | checked | `figures/make_figures.py`, `figures/figure_data.json`, `figures/fig1_architecture.tex` … (+1) |
| `R7` | The multi-CRF re-encode pipeline, with exact commands and encoder versions | Reproducibility statement; Data availability | checked | `pipeline/crf/generate_crf_variants.py`, `pipeline/faces/assess_extraction.py`, `pipeline/faces/extract_faces.py` … (+11) |
| `R8` | Video-ID lists for every evaluation set | Section IV-B; Table 4 caption | checked | `splits/celebdf_v2_test.json`, `splits/dfd_eval_c23.json`, `splits/dfd_eval_c40.json` … (+13) |
| `R9` | Checkpoint and selector provenance, and the per-epoch validation curves behind it | Reproducibility statement; Section IV-A | checked | `curves/a0.json`, `curves/a1_grl_s1.json`, `curves/a1_grl_s2.json` … (+27) |
| `R10` | Environment pins and a stated reproduction tolerance | Release README (reproduction-tolerance contract) | checked | `environment.yml`, `env/conda-linux-64.explicit.txt`, `env/pip-freeze.txt` … (+2) |
| `R11` | A check anyone can run: the paper's tables re-derived from the released artifacts | Contribution C3 | checked | `verify/verify.py`, `verify/expected.json`, `verify/claim.py` … (+3) |
| `R12` | Licences: code MIT, data CC BY 4.0 | Release README | checked | `LICENSE`, `LICENSE-DATA` |
| `R13` | Model checkpoints for every released run | Release README; Data availability | pending | — |
| `R14` | Per-video crop coordinates for byte-identical crop regeneration | Data availability | pending | — |

- `R1` — Three groups of cells carry the reported statistics only, with the reason stated: the cross-dataset cells, the JPEG-augmentation probe, and the shipped-recipe FaceShifter cells (predictions/GAPS.md).
- `R2` — The repository was private during the campaign, so the timeline is author-controlled version-control evidence, not third-party registration — history-excerpts.md says so in those words.
- `R6` — One plotted series — the shipped spatial-residual run's per-epoch γ in Fig. 4(a) — is published as data because it was read from per-epoch checkpoints that are archival only (figures/README.md).
- `R13` — **pending.** In the Zenodo deposit, minted immediately before submission. Not in git: ~6.5 GB of weights.
- `R14` — **pending.** In the Zenodo deposit (48,294 per-video meta.json, ~7 GB raw), minted before submission. The crops themselves are not redistributable under the FF++/DFD agreements.

---

*Generated by the release build from its export manifest; every number in the "this release gives" column was recomputed from the released artifacts while this file was written. A disagreement with the manuscript fails the build unless it is declared here as a **differs** row, which states both numbers and where the reconciliation is queued. Run `python verify/verify.py` to repeat the whole check yourself.*
