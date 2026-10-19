# Claims map, Revision 1 — the numbers the revised manuscript adds

*A Controlled Audit of a Negative Result: Training Recipe, H.264 Compression Levels and a Frequency-Stream Deepfake Detector* (IEEE Access, revision 1).

**What this file is.** The manuscript was revised once in response to peer
review (Revision 1). This file maps every number that the revision added to the
main paper or to its Supplementary Material to the released artifact the number
comes out of — most of them under `revision-1/` — and to the command that
checks it against that artifact by recomputing the number or reading it back
(see *Reproducibility tiers* in `README.md`). It continues [`CLAIMS-MAP.md`](CLAIMS-MAP.md), the map of the
first submitted version. That map keeps its rows; where the revision changed how
one of them is printed, the row changed there and is not repeated here.

**How rows map to the manuscript.** Each section below is one region of the
manuscript: a table, whose `\label{}` is given under the heading, or the running
text under one section heading. Row ids have the form `R1.<file>-<region>.<n>`:
`<file>` is `main` (the main paper) or `supp` (the Supplementary Material),
`<region>` is the region's LaTeX label (with `:` written as `-`) or its heading,
and `<n>` counts the region's numbers in reading order. The "claim" column quotes
the printed number with the words around it, so a text search finds it in the
manuscript. Numbers that are not results of this study — recipe settings, seeds,
registered thresholds, values quoted from the literature — have no row.

**How it is checked.** Exactly as `CLAIMS-MAP.md` is. The rows live in
`verify/claims_map_r1.json`, which `verify/claims_map.json` names as its
continuation, so `verify/claim.py` and `verify/verify.py` read both files:

```bash
python verify/claim.py R1.main-tab-e13.5   # check one row of this file
python verify/claim.py --all               # every cheap row of both maps
python verify/verify.py --jobs 4           # the whole check
```

2353 rows. **2353 are checked against the paper on every build:**
70 are recomputed from the per-video scores in `predictions/` and
the curves in `curves/`, and 2283 are read back from a shipped file,
most of them from the analysis outputs under `revision-1/` (the check confirms
that the printed number is the one in that file, without recomputing it). 0 are *recorded* rather
than asserted (the release holds the artifact but defines no numeric
re-derivation for them), 0 are not derivable from this release,
0 are pending, and 0 are marked **differs**. An
undeclared disagreement with the manuscript fails the build and no release is
produced. Table, figure and section numbers refer to the revised manuscript (revision 1) and its Supplementary Material. The map is regenerated whenever the release is rebuilt; if a manuscript number moves, the build fails until the map and the manuscript agree.

**How to read the columns.** As in `CLAIMS-MAP.md`: "paper prints" is the value
at the manuscript's precision; "this release gives" is the released artifacts'
value to four decimals, and agreement is asserted at half a unit in the last
place the paper prints. A row whose source holds a fraction and whose paper
prints points carries a scale of 100. Bootstrap rows are shown at the value
pinned in `verify/expected.json`; `verify.py` recomputes them from the scores.

---

## R1.fig3-fig-flow — Revision 1 — Supplementary Material, Fig. S1 (fig3_campaign_flow.pdf), fig:flow

*Supplementary Material, Fig. S1 (fig3_campaign_flow.pdf), fig:flow; `\label{fig:flow}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.fig3-fig-flow.1` | 11.97 — “(11.97 M) vs. the” | 11.97 | 11.97 | `revision-1/tables/shapes.json` | `python verify/claim.py R1.fig3-fig-flow.1` |
| `R1.fig3-fig-flow.2` | 4.0 — ““SpatialBase” (4.0 M)” | 4.0 | 4.0088 | `probes/param_counts_arms.json` | `python verify/claim.py R1.fig3-fig-flow.2` |
| `R1.fig3-fig-flow.3` | 0.9586 — “losses): 0.9586 vs.” | 0.9586 | 0.9586 | `predictions/ffpp/f1_none_fair_s42.json` | `python verify/claim.py R1.fig3-fig-flow.3` |
| `R1.fig3-fig-flow.4` | 0.9590 — “SpatialBase 0.9590” | 0.9590 | 0.9590 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py R1.fig3-fig-flow.4` |
| `R1.fig3-fig-flow.5` | +0.0055 — “+γ-residual): +0.0055,” | +0.0055 | 0.0055 | `verify/expected.json` +2 | `python verify/claim.py R1.fig3-fig-flow.5 --bootstrap` |
| `R1.fig3-fig-flow.6` | .9224 — “.9224; ∆ +0.0366, CI” | 0.9224 | 0.9224 | `predictions/ffpp/a0.json` | `python verify/claim.py R1.fig3-fig-flow.6` |
| `R1.fig3-fig-flow.7` | +0.0366 — “.9224; ∆ +0.0366, CI” | +0.0366 | 0.0366 | `verify/expected.json` +2 | `python verify/claim.py R1.fig3-fig-flow.7 --bootstrap` |
| `R1.fig3-fig-flow.8` | +0.020 — “[+0.020, +0.054]).” | +0.020 | 0.0205 | `verify/expected.json` +2 | `python verify/claim.py R1.fig3-fig-flow.8 --bootstrap` |
| `R1.fig3-fig-flow.9` | +0.054 — “[+0.020, +0.054]).” | +0.054 | 0.0540 | `verify/expected.json` +2 | `python verify/claim.py R1.fig3-fig-flow.9 --bootstrap` |
| `R1.fig3-fig-flow.10` | −0.0009 — “Fair-N −0.0009 /” | -0.0009 | -0.0009 | `verify/expected.json` +6 | `python verify/claim.py R1.fig3-fig-flow.10 --bootstrap` |
| `R1.fig3-fig-flow.11` | +0.0022 — “Fair-W +0.0022, both” | +0.0022 | 0.0022 | `verify/expected.json` +6 | `python verify/claim.py R1.fig3-fig-flow.11 --bootstrap` |
| `R1.fig3-fig-flow.12` | +3.96 — “(+ at c40, s42);” | +3.96 | 3.9600 | `verify/expected.json` +2 | `python verify/claim.py R1.fig3-fig-flow.12 --bootstrap` |
| `R1.fig3-fig-flow.13` | 7.48 — “at c40 (averaged” | 7.48 | 7.4783 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.fig3-fig-flow.13` |
| `R1.fig3-fig-flow.14` | 1.88 — “by averaged over” | 1.88 | 1.8831 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.fig3-fig-flow.14` |

## R1.ga-graphical-abstract — Revision 1 — graphical abstract (graphical_abstract.pdf; not part of this release), graphical-abstract

*graphical abstract (graphical_abstract.pdf; not part of this release), graphical-abstract*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.ga-graphical-abstract.1` | +3.96 — “the fair recipe alone recovers + at c40 (seed 42)” | +3.96 | 3.9600 | `verify/expected.json` +2 | `python verify/claim.py R1.ga-graphical-abstract.1 --bootstrap` |
| `R1.ga-graphical-abstract.2` | −0.09 — “pooled c40 −0.09 / + , both CIs include 0” | -0.09 | -0.0900 | `verify/expected.json` +6 | `python verify/claim.py R1.ga-graphical-abstract.2 --bootstrap` |
| `R1.ga-graphical-abstract.3` | +0.22 — “pooled c40 −0.09 / + , both CIs include 0” | +0.22 | 0.2200 | `verify/expected.json` +6 | `python verify/claim.py R1.ga-graphical-abstract.3 --bootstrap` |
| `R1.ga-graphical-abstract.4` | +3.66 — “+” | +3.66 | 3.6600 | `verify/expected.json` +2 | `python verify/claim.py R1.ga-graphical-abstract.4 --bootstrap` |
| `R1.ga-graphical-abstract.5` | 4.0 — “SpatialBase (EfficientNet-B0, 4.0 M)” | 4.0 | 4.0088 | `probes/param_counts_arms.json` | `python verify/claim.py R1.ga-graphical-abstract.5` |
| `R1.ga-graphical-abstract.6` | 11.97 — “CAFRL as specified (11.97 M)” | 11.97 | 11.97 | `revision-1/tables/shapes.json` | `python verify/claim.py R1.ga-graphical-abstract.6` |
| `R1.ga-graphical-abstract.7` | 7.48 — “frames by at real c40 (averaged over c40 exposure; registered, paired test, 3 seeds per ar” | 7.48 | 7.4783 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.ga-graphical-abstract.7` |

## R1.main-main-preamble — Revision 1 — main paper, main-preamble

*main paper, main-preamble*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.main-main-preamble.1` | 85.27 — “pre-specified), yet a standalone frequency head scored 85.27 test-split AUC points at” | 85.27 | 85.27 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.main-main-preamble.1` |
| `R1.main-main-preamble.2` | 0.87 — “registered test (0.87 points, Holm-adjusted p = 0.084); the estimator stayed” | 0.87 | 0.8678 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-main-preamble.2` |
| `R1.main-main-preamble.3` | 0.084 — “registered test (0.87 points, Holm-adjusted p = 0.084); the estimator stayed” | 0.084 | 0.0842 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-main-preamble.3` |
| `R1.main-main-preamble.4` | 7.48 — “frames by 7.48 points at CRF 40 (averaged over CRF-40 exposure), and” | 7.48 | 7.4783 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-main-preamble.4` |
| `R1.main-main-preamble.5` | 1.88 — “CRF-40-level data added 1.88 points averaged over codec; flat robustness was” | 1.88 | 1.8831 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-main-preamble.5` |

## R1.main-sec-intro — Revision 1 — main paper, sec:intro

*main paper, sec:intro; `\label{sec:intro}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.main-sec-intro.1` | 12.8 — “those protocols our reproductions of three published detectors lose 12.8” | 12.8 | 12.85 | `predictions/ffpp/b1_xception_lit.json` | `python verify/claim.py R1.main-sec-intro.1` |
| `R1.main-sec-intro.2` | 13.2 — “(Xception), 13.2 (F3-Net) and 21.9 (FreqNet) points of video-level area under the receiver” | 13.2 | 13.19 | `predictions/ffpp/b2_f3net_lit.json` | `python verify/claim.py R1.main-sec-intro.2` |
| `R1.main-sec-intro.3` | 21.9 — “(Xception), 13.2 (F3-Net) and 21.9 (FreqNet) points of video-level area under the receiver” | 21.9 | 21.93 | `predictions/ffpp/b3_freqnet_lit.json` | `python verify/claim.py R1.main-sec-intro.3` |

## R1.main-Contributions — Revision 1 — main paper, §“Contributions”

*main paper, §“Contributions”*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.main-Contributions.1` | 0.70 — “${\approx}0.70$ cross-dataset on Celeb-DF~v2, with DFDC and WildDeepfake only” | 0.70 | 0.6952 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-Contributions.1` |
| `R1.main-Contributions.2` | 7.48 — “versions of the same uncompressed frames matched on mean crop PSNR, by 7.48\,pt averaged o” | 7.48 | 7.4783 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-Contributions.2` |
| `R1.main-Contributions.3` | 1.88 — “and including the c40-level data in training raised it by 1.88\,pt averaged” | 1.88 | 1.8831 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-Contributions.3` |
| `R1.main-Contributions.4` | 0.88 — “$R = 0.88$ \ci{0.75}{1.03} of its c40 gain, not detectably below 1 (T3): the” | 0.88 | 0.8848 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-Contributions.4` |
| `R1.main-Contributions.5` | 0.75 — “$R = 0.88$ \ci{0.75}{1.03} of its c40 gain, not detectably below 1 (T3): the” | 0.75 | 0.7548 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-Contributions.5` |
| `R1.main-Contributions.6` | 1.03 — “$R = 0.88$ \ci{0.75}{1.03} of its c40 gain, not detectably below 1 (T3): the” | 1.03 | 1.0280 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-Contributions.6` |

## R1.main-Statistical-reporting — Revision 1 — main paper, §“Statistical reporting”

*main paper, §“Statistical reporting”*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.main-Statistical-reporting.1` | +0.53 — “its seed-mean lean ($+0.53$\,pt). A reader deploying one trained model should” | +0.53 | 0.5340 | `revision-1/recompute.json` | `python verify/claim.py R1.main-Statistical-reporting.1` |
| `R1.main-Statistical-reporting.2` | 10,000 — “two-sided $p$ comes from the same $B = 10{,}000$ replicates as its interval,” | 10000 | 10000.00 | `revision-1/recompute.json` | `python verify/claim.py R1.main-Statistical-reporting.2` |

## R1.main-What-this-design-can-detect — Revision 1 — main paper, §“What this design can detect”

*main paper, §“What this design can detect”*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.main-What-this-design-can-detect.1` | 1.49 — “minimum detectable effects are 1.49 and 1.68\,pt (Fair-N pool $-$” | 1.49 | 1.4859 | `evaluation/analysis/mde.json` | `python verify/claim.py R1.main-What-this-design-can-detect.1` |
| `R1.main-What-this-design-can-detect.2` | 1.68 — “minimum detectable effects are 1.49 and 1.68\,pt (Fair-N pool $-$” | 1.68 | 1.6789 | `evaluation/analysis/mde.json` | `python verify/claim.py R1.main-What-this-design-can-detect.2` |
| `R1.main-What-this-design-can-detect.3` | 1.47 — “SpatialBase pool) and 1.47 and 1.62\,pt (Fair-W pool $-$ SpatialBase pool),” | 1.47 | 1.4721 | `evaluation/analysis/mde.json` | `python verify/claim.py R1.main-What-this-design-can-detect.3` |
| `R1.main-What-this-design-can-detect.4` | 1.62 — “SpatialBase pool) and 1.47 and 1.62\,pt (Fair-W pool $-$ SpatialBase pool),” | 1.62 | 1.6177 | `evaluation/analysis/mde.json` | `python verify/claim.py R1.main-What-this-design-can-detect.4` |

## R1.main-Confirmatory-and-descriptive-contrasts — Revision 1 — main paper, §“Confirmatory and descriptive contrasts”

*main paper, §“Confirmatory and descriptive contrasts”*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.main-Confirmatory-and-descriptive-contrasts.1` | 4.2\times10^{-3} — “Bonferroni threshold is $\alpha/12 = 4.2\times10^{-3}$, and the three” | 4.2e-3 | 0.0042 | `revision-1/recompute.json` | `python verify/claim.py R1.main-Confirmatory-and-descriptive-contrasts.1` |

## R1.main-sec-campaign — Revision 1 — main paper, sec:campaign

*main paper, sec:campaign; `\label{sec:campaign}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.main-sec-campaign.1` | 17 — “(published: 17, 11 and 8). T3 and T5 are recomputed with these runs and” | 17 | 17.00 | `curves/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py R1.main-sec-campaign.1` |
| `R1.main-sec-campaign.2` | 11 — “(published: 17, 11 and 8). T3 and T5 are recomputed with these runs and” | 11 | 11.00 | `curves/b7_effnet_b0_mq_fliponly_s1.json` | `python verify/claim.py R1.main-sec-campaign.2` |
| `R1.main-sec-campaign.3` | 8 — “(published: 17, 11 and 8). T3 and T5 are recomputed with these runs and” | 8 | 8.0000 | `curves/b7_effnet_b0_mq_fliponly_s2.json` | `python verify/claim.py R1.main-sec-campaign.3` |

## R1.main-tab-retests — Revision 1 — main paper, tab:retests

*main paper, tab:retests; `\label{tab:retests}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.main-tab-retests.1` | 0.9536 — “recipe-dominant: TrunkCtrl 0.9536; $\Delta$ $-0.0038$” | 0.9536 | 0.9536 | `predictions/ffpp/trunk_recipe_s42.json` +2 | `python verify/claim.py R1.main-tab-retests.1` |
| `R1.main-tab-retests.2` | -0.0038 — “recipe-dominant: TrunkCtrl 0.9536; $\Delta$ $-0.0038$” | -0.0038 | -0.0038 | `verify/expected.json` +4 | `python verify/claim.py R1.main-tab-retests.2 --bootstrap` |
| `R1.main-tab-retests.3` | -0.0116 — “\ci{-0.0116}{+0.0039} \\” | -0.0116 | -0.0116 | `verify/expected.json` +4 | `python verify/claim.py R1.main-tab-retests.3 --bootstrap` |
| `R1.main-tab-retests.4` | +0.0039 — “\ci{-0.0116}{+0.0039} \\” | +0.0039 | 0.0039 | `verify/expected.json` +4 | `python verify/claim.py R1.main-tab-retests.4 --bootstrap` |
| `R1.main-tab-retests.5` | -0.0004 — “neutral: $-0.0004$ \ci{-0.0092}{+0.0080}; $+0.0396$ over CAFRL$-$adv \\” | -0.0004 | -0.0004 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-retests.5` |
| `R1.main-tab-retests.6` | -0.0092 — “neutral: $-0.0004$ \ci{-0.0092}{+0.0080}; $+0.0396$ over CAFRL$-$adv \\” | -0.0092 | -0.0092 | `verify/expected.json` +2 | `python verify/claim.py R1.main-tab-retests.6 --bootstrap` |
| `R1.main-tab-retests.7` | +0.0080 — “neutral: $-0.0004$ \ci{-0.0092}{+0.0080}; $+0.0396$ over CAFRL$-$adv \\” | +0.0080 | 0.0080 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-retests.7` |
| `R1.main-tab-retests.8` | +0.0396 — “neutral: $-0.0004$ \ci{-0.0092}{+0.0080}; $+0.0396$ over CAFRL$-$adv \\” | +0.0396 | 0.0396 | `verify/expected.json` +2 | `python verify/claim.py R1.main-tab-retests.8 --bootstrap` |
| `R1.main-tab-retests.9` | +0.0055 — “D2, D4 & neutral: $+0.0055$ \ci{-0.0022}{+0.0134}; $\gamma$ deadlock” | +0.0055 | 0.0055 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-retests.9` |
| `R1.main-tab-retests.10` | -0.0022 — “D2, D4 & neutral: $+0.0055$ \ci{-0.0022}{+0.0134}; $\gamma$ deadlock” | -0.0022 | -0.0022 | `verify/expected.json` +2 | `python verify/claim.py R1.main-tab-retests.10 --bootstrap` |
| `R1.main-tab-retests.11` | +0.0134 — “D2, D4 & neutral: $+0.0055$ \ci{-0.0022}{+0.0134}; $\gamma$ deadlock” | +0.0134 | 0.0134 | `verify/expected.json` +2 | `python verify/claim.py R1.main-tab-retests.11 --bootstrap` |

## R1.main-sec-recipeartifact — Revision 1 — main paper, sec:recipeartifact

*main paper, sec:recipeartifact; `\label{sec:recipeartifact}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.main-sec-recipeartifact.1` | +0.0489 — “spatial controls; $\Delta$(TrunkCtrl $-$ spatial-residual) $+0.0489$, CI \ci{+0.0294}{+0.0” | +0.0489 | 0.0489 | `verify/expected.json` +4 | `python verify/claim.py R1.main-sec-recipeartifact.1 --bootstrap` |
| `R1.main-sec-recipeartifact.2` | +0.0054 — “the point differences above, $+0.0054$ \ci{-0.0040}{+0.0156} and $+0.0397$” | +0.0054 | 0.0054 | `revision-1/recompute.json` | `python verify/claim.py R1.main-sec-recipeartifact.2` |
| `R1.main-sec-recipeartifact.3` | -0.0040 — “the point differences above, $+0.0054$ \ci{-0.0040}{+0.0156} and $+0.0397$” | -0.0040 | -0.0040 | `revision-1/recompute.json` | `python verify/claim.py R1.main-sec-recipeartifact.3` |
| `R1.main-sec-recipeartifact.4` | +0.0156 — “the point differences above, $+0.0054$ \ci{-0.0040}{+0.0156} and $+0.0397$” | +0.0156 | 0.0156 | `revision-1/recompute.json` | `python verify/claim.py R1.main-sec-recipeartifact.4` |
| `R1.main-sec-recipeartifact.5` | +0.0397 — “the point differences above, $+0.0054$ \ci{-0.0040}{+0.0156} and $+0.0397$” | +0.0397 | 0.0397 | `revision-1/recompute.json` | `python verify/claim.py R1.main-sec-recipeartifact.5` |
| `R1.main-sec-recipeartifact.6` | +0.0196 — “\ci{+0.0196}{+0.0625} (EMA for spatial-residual, raw for SpatialBase and” | +0.0196 | 0.0196 | `revision-1/recompute.json` | `python verify/claim.py R1.main-sec-recipeartifact.6` |
| `R1.main-sec-recipeartifact.7` | +0.0625 — “\ci{+0.0196}{+0.0625} (EMA for spatial-residual, raw for SpatialBase and” | +0.0625 | 0.0625 | `revision-1/recompute.json` | `python verify/claim.py R1.main-sec-recipeartifact.7` |
| `R1.main-sec-recipeartifact.8` | 4.0 — “they classify from --- in their processing and in parameter count (4.0\,M” | 4.0 | 4.0088 | `probes/param_counts_arms.json` | `python verify/claim.py R1.main-sec-recipeartifact.8` |
| `R1.main-sec-recipeartifact.9` | 3.68 — “against 3.68\,M) --- so their tie does not isolate the cost of tapping the” | 3.68 | 3.6778 | `probes/param_counts_arms.json` | `python verify/claim.py R1.main-sec-recipeartifact.9` |

## R1.main-tab-e13 — Revision 1 — main paper, tab:e13

*main paper, tab:e13; `\label{tab:e13}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.main-tab-e13.1` | 10,000 — “140 source-identity clusters are resampled, $B = 10{,}000$; one run per” | 10000 | 10000.00 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-e13.1` |
| `R1.main-tab-e13.2` | 95.86 — “selected by Fair-N's rule. Fair-N's seed-42 run scores 95.86 at c40 and 97.14 on \auccomp.” | 95.86 | 95.86 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.2` |
| `R1.main-tab-e13.3` | 97.14 — “selected by Fair-N's rule. Fair-N's seed-42 run scores 95.86 at c40 and 97.14 on \auccomp.” | 97.14 | 97.14 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.3` |
| `R1.main-tab-e13.4` | 29 — “training curriculum (identical re-run, epoch 29)” | 29 | 29.00 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.main-tab-e13.4` |
| `R1.main-tab-e13.5` | -0.25 — “& $-0.25$ \ci{-1.16}{0.68} & 0.004 \ci{-0.62}{0.67} \\” | -0.25 | -0.2500 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.main-tab-e13.5` |
| `R1.main-tab-e13.6` | -1.16 — “& $-0.25$ \ci{-1.16}{0.68} & 0.004 \ci{-0.62}{0.67} \\” | -1.16 | -1.1620 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.main-tab-e13.6` |
| `R1.main-tab-e13.7` | 0.68 — “& $-0.25$ \ci{-1.16}{0.68} & 0.004 \ci{-0.62}{0.67} \\” | 0.68 | 0.6786 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.main-tab-e13.7` |
| `R1.main-tab-e13.8` | 0.004 — “& $-0.25$ \ci{-1.16}{0.68} & 0.004 \ci{-0.62}{0.67} \\” | 0.004 | 0.0035 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.main-tab-e13.8` |
| `R1.main-tab-e13.9` | -0.62 — “& $-0.25$ \ci{-1.16}{0.68} & 0.004 \ci{-0.62}{0.67} \\” | -0.62 | -0.6174 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.main-tab-e13.9` |
| `R1.main-tab-e13.10` | 0.67 — “& $-0.25$ \ci{-1.16}{0.68} & 0.004 \ci{-0.62}{0.67} \\” | 0.67 | 0.6681 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.main-tab-e13.10` |
| `R1.main-tab-e13.11` | -4.07 — “backbone learning rate & $-4.07$ \ci{-5.80}{-2.45} & $-2.71$ \ci{-3.97}{-1.58} \\” | -4.07 | -4.0663 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.11` |
| `R1.main-tab-e13.12` | -5.80 — “backbone learning rate & $-4.07$ \ci{-5.80}{-2.45} & $-2.71$ \ci{-3.97}{-1.58} \\” | -5.80 | -5.7985 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.12` |
| `R1.main-tab-e13.13` | -2.45 — “backbone learning rate & $-4.07$ \ci{-5.80}{-2.45} & $-2.71$ \ci{-3.97}{-1.58} \\” | -2.45 | -2.4489 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.13` |
| `R1.main-tab-e13.14` | -2.71 — “backbone learning rate & $-4.07$ \ci{-5.80}{-2.45} & $-2.71$ \ci{-3.97}{-1.58} \\” | -2.71 | -2.7140 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.14` |
| `R1.main-tab-e13.15` | -3.97 — “backbone learning rate & $-4.07$ \ci{-5.80}{-2.45} & $-2.71$ \ci{-3.97}{-1.58} \\” | -3.97 | -3.9697 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.15` |
| `R1.main-tab-e13.16` | -1.58 — “backbone learning rate & $-4.07$ \ci{-5.80}{-2.45} & $-2.71$ \ci{-3.97}{-1.58} \\” | -1.58 | -1.5816 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.16` |
| `R1.main-tab-e13.17` | 0.14 — “frequency-stream learning rate & 0.14 \ci{-1.00}{1.33} & $-0.08$ \ci{-0.82}{0.70} \\” | 0.14 | 0.1416 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.17` |
| `R1.main-tab-e13.18` | -1.00 — “frequency-stream learning rate & 0.14 \ci{-1.00}{1.33} & $-0.08$ \ci{-0.82}{0.70} \\” | -1.00 | -1.0026 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.18` |
| `R1.main-tab-e13.19` | 1.33 — “frequency-stream learning rate & 0.14 \ci{-1.00}{1.33} & $-0.08$ \ci{-0.82}{0.70} \\” | 1.33 | 1.3317 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.19` |
| `R1.main-tab-e13.20` | -0.08 — “frequency-stream learning rate & 0.14 \ci{-1.00}{1.33} & $-0.08$ \ci{-0.82}{0.70} \\” | -0.08 | -0.0804 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.20` |
| `R1.main-tab-e13.21` | -0.82 — “frequency-stream learning rate & 0.14 \ci{-1.00}{1.33} & $-0.08$ \ci{-0.82}{0.70} \\” | -0.82 | -0.8205 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.21` |
| `R1.main-tab-e13.22` | 0.70 — “frequency-stream learning rate & 0.14 \ci{-1.00}{1.33} & $-0.08$ \ci{-0.82}{0.70} \\” | 0.70 | 0.7035 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.22` |
| `R1.main-tab-e13.23` | 0.10 — “auxiliary-loss weights & 0.10 \ci{-0.94}{1.18} & 0.30 \ci{-0.31}{1.01} \\” | 0.10 | 0.1033 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.23` |
| `R1.main-tab-e13.24` | -0.94 — “auxiliary-loss weights & 0.10 \ci{-0.94}{1.18} & 0.30 \ci{-0.31}{1.01} \\” | -0.94 | -0.9401 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.24` |
| `R1.main-tab-e13.25` | 1.18 — “auxiliary-loss weights & 0.10 \ci{-0.94}{1.18} & 0.30 \ci{-0.31}{1.01} \\” | 1.18 | 1.1837 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.25` |
| `R1.main-tab-e13.26` | 0.30 — “auxiliary-loss weights & 0.10 \ci{-0.94}{1.18} & 0.30 \ci{-0.31}{1.01} \\” | 0.30 | 0.2956 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.26` |
| `R1.main-tab-e13.27` | -0.31 — “auxiliary-loss weights & 0.10 \ci{-0.94}{1.18} & 0.30 \ci{-0.31}{1.01} \\” | -0.31 | -0.3094 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.27` |
| `R1.main-tab-e13.28` | 1.01 — “auxiliary-loss weights & 0.10 \ci{-0.94}{1.18} & 0.30 \ci{-0.31}{1.01} \\” | 1.01 | 1.0064 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.28` |
| `R1.main-tab-e13.29` | 0.05 — “training length & 0.05 \ci{-1.02}{1.05} & $-0.13$ \ci{-0.93}{0.65} \\” | 0.05 | 0.0497 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.29` |
| `R1.main-tab-e13.30` | -1.02 — “training length & 0.05 \ci{-1.02}{1.05} & $-0.13$ \ci{-0.93}{0.65} \\” | -1.02 | -1.0166 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.30` |
| `R1.main-tab-e13.31` | 1.05 — “training length & 0.05 \ci{-1.02}{1.05} & $-0.13$ \ci{-0.93}{0.65} \\” | 1.05 | 1.0548 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.31` |
| `R1.main-tab-e13.32` | -0.13 — “training length & 0.05 \ci{-1.02}{1.05} & $-0.13$ \ci{-0.93}{0.65} \\” | -0.13 | -0.1279 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.32` |
| `R1.main-tab-e13.33` | -0.93 — “training length & 0.05 \ci{-1.02}{1.05} & $-0.13$ \ci{-0.93}{0.65} \\” | -0.93 | -0.9254 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.33` |
| `R1.main-tab-e13.34` | 0.65 — “training length & 0.05 \ci{-1.02}{1.05} & $-0.13$ \ci{-0.93}{0.65} \\” | 0.65 | 0.6483 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-tab-e13.34` |

- `R1.main-tab-e13.2` — weights: EMA
- `R1.main-tab-e13.3` — weights: EMA
- `R1.main-tab-e13.4` — weights: EMA
- `R1.main-tab-e13.5` — weights: EMA
- `R1.main-tab-e13.11` — weights: EMA
- `R1.main-tab-e13.12` — weights: EMA
- `R1.main-tab-e13.13` — weights: EMA
- `R1.main-tab-e13.14` — weights: EMA
- `R1.main-tab-e13.15` — weights: EMA
- `R1.main-tab-e13.16` — weights: EMA
- `R1.main-tab-e13.17` — weights: EMA
- `R1.main-tab-e13.18` — weights: EMA
- `R1.main-tab-e13.19` — weights: EMA
- `R1.main-tab-e13.20` — weights: EMA
- `R1.main-tab-e13.21` — weights: EMA
- `R1.main-tab-e13.22` — weights: EMA
- `R1.main-tab-e13.23` — weights: EMA
- `R1.main-tab-e13.24` — weights: EMA
- `R1.main-tab-e13.25` — weights: EMA
- `R1.main-tab-e13.26` — weights: EMA
- `R1.main-tab-e13.27` — weights: EMA
- `R1.main-tab-e13.28` — weights: EMA
- `R1.main-tab-e13.29` — weights: EMA
- `R1.main-tab-e13.30` — weights: EMA
- `R1.main-tab-e13.31` — weights: EMA
- `R1.main-tab-e13.32` — weights: EMA
- `R1.main-tab-e13.33` — weights: EMA
- `R1.main-tab-e13.34` — weights: EMA

## R1.main-sec-e13 — Revision 1 — main paper, sec:e13

*main paper, sec:e13; `\label{sec:e13}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.main-sec-e13.1` | -0.25 — “$-0.25$\,pt against Fair-N (fixed-seed interval \ci{-1.16}{0.68};” | -0.25 | -0.2500 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.main-sec-e13.1` |
| `R1.main-sec-e13.2` | -1.16 — “$-0.25$\,pt against Fair-N (fixed-seed interval \ci{-1.16}{0.68};” | -1.16 | -1.1620 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.main-sec-e13.2` |
| `R1.main-sec-e13.3` | 0.68 — “$-0.25$\,pt against Fair-N (fixed-seed interval \ci{-1.16}{0.68};” | 0.68 | 0.6786 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.main-sec-e13.3` |
| `R1.main-sec-e13.4` | -4.07 — “($2{\times}10^{-4}$ back to $10^{-5}$) changed c40 AUC by $-4.07$\,pt against” | -4.07 | -4.0663 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-sec-e13.4` |
| `R1.main-sec-e13.5` | -5.80 — “Fair-N (fixed-seed interval \ci{-5.80}{-2.45}; descriptive). In a one-seed” | -5.80 | -5.7985 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-sec-e13.5` |
| `R1.main-sec-e13.6` | -2.45 — “Fair-N (fixed-seed interval \ci{-5.80}{-2.45}; descriptive). In a one-seed” | -2.45 | -2.4489 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-sec-e13.6` |
| `R1.main-sec-e13.7` | 0.14 — “back to $10^{-4}$) changed c40 AUC by 0.14\,pt against Fair-N (fixed-seed” | 0.14 | 0.1416 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-sec-e13.7` |
| `R1.main-sec-e13.8` | -1.00 — “interval \ci{-1.00}{1.33}; descriptive). In a one-seed ablation, reverting” | -1.00 | -1.0026 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-sec-e13.8` |
| `R1.main-sec-e13.9` | 1.33 — “interval \ci{-1.00}{1.33}; descriptive). In a one-seed ablation, reverting” | 1.33 | 1.3317 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-sec-e13.9` |
| `R1.main-sec-e13.10` | 0.10 — “0.10\,pt against Fair-N (fixed-seed interval \ci{-0.94}{1.18}; descriptive).” | 0.10 | 0.1033 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-sec-e13.10` |
| `R1.main-sec-e13.11` | -0.94 — “0.10\,pt against Fair-N (fixed-seed interval \ci{-0.94}{1.18}; descriptive).” | -0.94 | -0.9401 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-sec-e13.11` |
| `R1.main-sec-e13.12` | 1.18 — “0.10\,pt against Fair-N (fixed-seed interval \ci{-0.94}{1.18}; descriptive).” | 1.18 | 1.1837 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-sec-e13.12` |
| `R1.main-sec-e13.13` | 0.05 — “with the learning-rate schedule stretched to match) changed c40 AUC by 0.05\,pt against” | 0.05 | 0.0497 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-sec-e13.13` |
| `R1.main-sec-e13.14` | -1.02 — “Fair-N (fixed-seed interval \ci{-1.02}{1.05}; descriptive).” | -1.02 | -1.0166 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-sec-e13.14` |
| `R1.main-sec-e13.15` | 1.05 — “Fair-N (fixed-seed interval \ci{-1.02}{1.05}; descriptive).” | 1.05 | 1.0548 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-sec-e13.15` |
| `R1.main-sec-e13.16` | 14 — “The first run of this arm diverged at epoch 14; we re-ran it with nothing” | 14 | 14.00 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.main-sec-e13.16` |

## R1.main-sec-redundancy — Revision 1 — main paper, sec:redundancy

*main paper, sec:redundancy; `\label{sec:redundancy}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.main-sec-redundancy.1` | +0.0055 — “= +0.0055$, CI \ci{-0.0022}{+0.0134}, $P(\Delta{>}0)=0.93$: a lean, not a” | +0.0055 | 0.0055 | `revision-1/recompute.json` | `python verify/claim.py R1.main-sec-redundancy.1` |
| `R1.main-sec-redundancy.2` | 85.27 — “$\gamma$ peaks; scored alone there, the standalone head reaches 85.27 AUC” | 85.27 | 85.27 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.main-sec-redundancy.2` |
| `R1.main-sec-redundancy.3` | 89.99 — “points at c40, and 89.99 at epoch 30 (the full model: 96.19 and 94.66). Its” | 89.99 | 89.99 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.main-sec-redundancy.3` |
| `R1.main-sec-redundancy.4` | 96.19 — “points at c40, and 89.99 at epoch 30 (the full model: 96.19 and 94.66). Its” | 96.19 | 96.19 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.main-sec-redundancy.4` |
| `R1.main-sec-redundancy.5` | 94.66 — “points at c40, and 89.99 at epoch 30 (the full model: 96.19 and 94.66). Its” | 94.66 | 94.66 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.main-sec-redundancy.5` |
| `R1.main-sec-redundancy.6` | 0.11 — “spatial and $f$ the head logit, averages 0.11 at c40. Added to SpatialBase's” | 0.11 | 0.1109 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.main-sec-redundancy.6` |
| `R1.main-sec-redundancy.7` | 0.01 — “SpatialBase's c40 AUC by 0.01\,pt \ci{-0.99}{1.02}, and it errs on 55\%” | 0.01 | 0.0051 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.main-sec-redundancy.7` |
| `R1.main-sec-redundancy.8` | -0.99 — “SpatialBase's c40 AUC by 0.01\,pt \ci{-0.99}{1.02}, and it errs on 55\%” | -0.99 | -0.9911 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.main-sec-redundancy.8` |
| `R1.main-sec-redundancy.9` | 1.02 — “SpatialBase's c40 AUC by 0.01\,pt \ci{-0.99}{1.02}, and it errs on 55\%” | 1.02 | 1.0209 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.main-sec-redundancy.9` |
| `R1.main-sec-redundancy.10` | 55 — “SpatialBase's c40 AUC by 0.01\,pt \ci{-0.99}{1.02}, and it errs on 55\%” | 55 | 54.58 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.main-sec-redundancy.10` |
| `R1.main-sec-redundancy.11` | 0.23 — “of the videos SpatialBase errs on (Jaccard index of the two error sets 0.23).” | 0.23 | 0.2281 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.main-sec-redundancy.11` |

## R1.main-tab-contrasts — Revision 1 — main paper, tab:contrasts

*main paper, tab:contrasts; `\label{tab:contrasts}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.main-tab-contrasts.1` | +0.0366 — “SpatialBase $-$ CAFRL as specified (s42) & $+0.0366$ & \ci{+0.020}{+0.054} & registered & ” | +0.0366 | 0.0366 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.1` |
| `R1.main-tab-contrasts.2` | +0.0182 — “SpatialBase $-$ CAFRL as specified (s42) & $+0.0366$ & \ci{+0.020}{+0.054} & registered & ” | +0.0182 | 0.0182 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.2` |
| `R1.main-tab-contrasts.3` | +0.0569 — “SpatialBase $-$ CAFRL as specified (s42) & $+0.0366$ & \ci{+0.020}{+0.054} & registered & ” | +0.0569 | 0.0569 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.3` |
| `R1.main-tab-contrasts.4` | +0.0396 — “Fair-N $-$ CAFRL$-$adv (s42) & $+0.0396$ & \ci{+0.0231}{+0.0570} & pre-\zb specified & sig” | +0.0396 | 0.0396 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.4` |
| `R1.main-tab-contrasts.5` | +0.0222 — “Fair-N $-$ CAFRL$-$adv (s42) & $+0.0396$ & \ci{+0.0231}{+0.0570} & pre-\zb specified & sig” | +0.0222 | 0.0222 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.5` |
| `R1.main-tab-contrasts.6` | +0.0580 — “Fair-N $-$ CAFRL$-$adv (s42) & $+0.0396$ & \ci{+0.0231}{+0.0570} & pre-\zb specified & sig” | +0.0580 | 0.0580 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.6` |
| `R1.main-tab-contrasts.7` | -0.0004 — “Fair-N $-$ SpatialBase (s42) & $-0.0004$ & \ci{-0.0092}{+0.0080} & pre-\zb specified & no ” | -0.0004 | -0.0004 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.7` |
| `R1.main-tab-contrasts.8` | -0.0095 — “Fair-N $-$ SpatialBase (s42) & $-0.0004$ & \ci{-0.0092}{+0.0080} & pre-\zb specified & no ” | -0.0095 | -0.0095 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.8` |
| `R1.main-tab-contrasts.9` | +0.0055 — “Fair-W $-$ SpatialBase (s42) & $+0.0055$ & \ci{-0.0022}{+0.0134} & pre-\zb specified & no ” | +0.0055 | 0.0055 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.9` |
| `R1.main-tab-contrasts.10` | +0.0055 — “Fair-W $-$ SpatialBase (s42) & $+0.0055$ & \ci{-0.0022}{+0.0134} & pre-\zb specified & no ” | +0.0055 | 0.0055 | `verify/expected.json` +2 | `python verify/claim.py R1.main-tab-contrasts.10 --bootstrap` |
| `R1.main-tab-contrasts.11` | -0.0026 — “Fair-W $-$ SpatialBase (s42) & $+0.0055$ & \ci{-0.0022}{+0.0134} & pre-\zb specified & no ” | -0.0026 | -0.0026 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.11` |
| `R1.main-tab-contrasts.12` | +0.0137 — “Fair-W $-$ SpatialBase (s42) & $+0.0055$ & \ci{-0.0022}{+0.0134} & pre-\zb specified & no ” | +0.0137 | 0.0137 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.12` |
| `R1.main-tab-contrasts.13` | -0.0009 — “\textbf{Fair-N pool $-$ SpatialBase pool (3 vs.\ 3)} & $\mathbf{-0.0009}$ & \ci{-0.0066}{+” | -0.0009 | -0.0009 | `verify/expected.json` +6 | `python verify/claim.py R1.main-tab-contrasts.13 --bootstrap` |
| `R1.main-tab-contrasts.14` | -0.0002 — “\textbf{Fair-N pool $-$ SpatialBase pool (3 vs.\ 3)} & $\mathbf{-0.0009}$ & \ci{-0.0066}{+” | -0.0002 | -0.0002 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.14` |
| `R1.main-tab-contrasts.15` | -0.0105 — “\textbf{Fair-N pool $-$ SpatialBase pool (3 vs.\ 3)} & $\mathbf{-0.0009}$ & \ci{-0.0066}{+” | -0.0105 | -0.0105 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.15` |
| `R1.main-tab-contrasts.16` | +0.0112 — “\textbf{Fair-N pool $-$ SpatialBase pool (3 vs.\ 3)} & $\mathbf{-0.0009}$ & \ci{-0.0066}{+” | +0.0112 | 0.0112 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.16` |
| `R1.main-tab-contrasts.17` | +0.0080 — “\textbf{Fair-W pool $-$ SpatialBase pool (3 vs.\ 3)} & $\mathbf{+0.0022}$ & \ci{-0.0035}{+” | +0.0080 | 0.0080 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.17` |
| `R1.main-tab-contrasts.18` | +0.0053 — “\textbf{Fair-W pool $-$ SpatialBase pool (3 vs.\ 3)} & $\mathbf{+0.0022}$ & \ci{-0.0035}{+” | +0.0053 | 0.0053 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.18` |
| `R1.main-tab-contrasts.19` | -0.0042 — “\textbf{Fair-W pool $-$ SpatialBase pool (3 vs.\ 3)} & $\mathbf{+0.0022}$ & \ci{-0.0035}{+” | -0.0042 | -0.0042 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.19` |
| `R1.main-tab-contrasts.20` | +0.0171 — “\textbf{Fair-W pool $-$ SpatialBase pool (3 vs.\ 3)} & $\mathbf{+0.0022}$ & \ci{-0.0035}{+” | +0.0171 | 0.0171 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.20` |
| `R1.main-tab-contrasts.21` | +0.0054 — “SpatialBase (s42) $-$ TrunkCtrl pool & $-0.0038$ & \ci{-0.0116}{+0.0039} & pre-\zb specifi” | +0.0054 | 0.0054 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.21` |
| `R1.main-tab-contrasts.22` | -0.0040 — “SpatialBase (s42) $-$ TrunkCtrl pool & $-0.0038$ & \ci{-0.0116}{+0.0039} & pre-\zb specifi” | -0.0040 | -0.0040 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.22` |
| `R1.main-tab-contrasts.23` | +0.0156 — “SpatialBase (s42) $-$ TrunkCtrl pool & $-0.0038$ & \ci{-0.0116}{+0.0039} & pre-\zb specifi” | +0.0156 | 0.0156 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.23` |
| `R1.main-tab-contrasts.24` | +0.0489 — “TrunkCtrl pool $-$ spatial-residual (s42) & $+0.0489$ & \ci{+0.0294}{+0.0705} & pre-\zb sp” | +0.0489 | 0.0489 | `verify/expected.json` +4 | `python verify/claim.py R1.main-tab-contrasts.24 --bootstrap` |
| `R1.main-tab-contrasts.25` | +0.0397 — “TrunkCtrl pool $-$ spatial-residual (s42) & $+0.0489$ & \ci{+0.0294}{+0.0705} & pre-\zb sp” | +0.0397 | 0.0397 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.25` |
| `R1.main-tab-contrasts.26` | +0.0196 — “TrunkCtrl pool $-$ spatial-residual (s42) & $+0.0489$ & \ci{+0.0294}{+0.0705} & pre-\zb sp” | +0.0196 | 0.0196 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.26` |
| `R1.main-tab-contrasts.27` | +0.0625 — “TrunkCtrl pool $-$ spatial-residual (s42) & $+0.0489$ & \ci{+0.0294}{+0.0705} & pre-\zb sp” | +0.0625 | 0.0625 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.27` |
| `R1.main-tab-contrasts.28` | +0.0014 — “Fair-N pool $-$ TrunkCtrl pool (3 vs.\ 3) & $+0.0014$ & \ci{-0.0051}{+0.0078} & post hoc &” | +0.0014 | 0.0014 | `verify/expected.json` +6 | `python verify/claim.py R1.main-tab-contrasts.28 --bootstrap` |
| `R1.main-tab-contrasts.29` | -0.0051 — “Fair-N pool $-$ TrunkCtrl pool (3 vs.\ 3) & $+0.0014$ & \ci{-0.0051}{+0.0078} & post hoc &” | -0.0051 | -0.0051 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.29` |
| `R1.main-tab-contrasts.30` | +0.0078 — “Fair-N pool $-$ TrunkCtrl pool (3 vs.\ 3) & $+0.0014$ & \ci{-0.0051}{+0.0078} & post hoc &” | +0.0078 | 0.0078 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.30` |
| `R1.main-tab-contrasts.31` | +0.0027 — “Fair-N pool $-$ TrunkCtrl pool (3 vs.\ 3) & $+0.0014$ & \ci{-0.0051}{+0.0078} & post hoc &” | +0.0027 | 0.0027 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.31` |
| `R1.main-tab-contrasts.32` | -0.0080 — “Fair-N pool $-$ TrunkCtrl pool (3 vs.\ 3) & $+0.0014$ & \ci{-0.0051}{+0.0078} & post hoc &” | -0.0080 | -0.0080 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.32` |
| `R1.main-tab-contrasts.33` | +0.0135 — “Fair-N pool $-$ TrunkCtrl pool (3 vs.\ 3) & $+0.0014$ & \ci{-0.0051}{+0.0078} & post hoc &” | +0.0135 | 0.0135 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-contrasts.33` |

## R1.main-sec-seeds — Revision 1 — main paper, sec:seeds

*main paper, sec:seeds; `\label{sec:seeds}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.main-sec-seeds.1` | -0.37 — “Fair-N $-$ SpatialBase at c40 was $-0.37$\,pt \ci{-1.57}{0.93} and Fair-W” | -0.37 | -0.3690 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.main-sec-seeds.1` |
| `R1.main-sec-seeds.2` | -1.57 — “Fair-N $-$ SpatialBase at c40 was $-0.37$\,pt \ci{-1.57}{0.93} and Fair-W” | -1.57 | -1.5744 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.main-sec-seeds.2` |
| `R1.main-sec-seeds.3` | 0.93 — “Fair-N $-$ SpatialBase at c40 was $-0.37$\,pt \ci{-1.57}{0.93} and Fair-W” | 0.93 | 0.9294 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.main-sec-seeds.3` |
| `R1.main-sec-seeds.4` | -0.72 — “$-$ SpatialBase $-0.72$\,pt \ci{-2.14}{0.69}: both intervals include zero, as” | -0.72 | -0.7198 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.main-sec-seeds.4` |
| `R1.main-sec-seeds.5` | -2.14 — “$-$ SpatialBase $-0.72$\,pt \ci{-2.14}{0.69}: both intervals include zero, as” | -2.14 | -2.1399 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.main-sec-seeds.5` |
| `R1.main-sec-seeds.6` | 0.69 — “$-$ SpatialBase $-0.72$\,pt \ci{-2.14}{0.69}: both intervals include zero, as” | 0.69 | 0.6858 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.main-sec-seeds.6` |

## R1.main-sec-ood — Revision 1 — main paper, sec:ood

*main paper, sec:ood; `\label{sec:ood}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.main-sec-ood.1` | +0.0333 — “primary reading, Fair-N's seed-42 lean, $+0.0333$ \ci{+0.0012}{+0.0661},” | +0.0333 | 0.0333 | `revision-1/recompute.json` | `python verify/claim.py R1.main-sec-ood.1` |
| `R1.main-sec-ood.2` | +0.0012 — “primary reading, Fair-N's seed-42 lean, $+0.0333$ \ci{+0.0012}{+0.0661},” | +0.0012 | 0.0012 | `revision-1/recompute.json` | `python verify/claim.py R1.main-sec-ood.2` |
| `R1.main-sec-ood.3` | +0.0661 — “primary reading, Fair-N's seed-42 lean, $+0.0333$ \ci{+0.0012}{+0.0661},” | +0.0661 | 0.0661 | `revision-1/recompute.json` | `python verify/claim.py R1.main-sec-ood.3` |
| `R1.main-sec-ood.4` | 0.042 — “$p = 0.042$, has an interval that excludes zero unadjusted, Holm-adjusted” | 0.042 | 0.0425 | `revision-1/recompute.json` | `python verify/claim.py R1.main-sec-ood.4` |
| `R1.main-sec-ood.5` | 0.38 — “$p = 0.38$). With all seeds pooled both fair variants sit \emph{below} the” | 0.38 | 0.3825 | `revision-1/recompute.json` | `python verify/claim.py R1.main-sec-ood.5` |
| `R1.main-sec-ood.6` | -0.0545 — “arm} (Fair-N $-0.0325$, CI \ci{-0.0545}{-0.0114}; Fair-W $-0.0317$,” | -0.0545 | -0.0545 | `revision-1/recompute.json` | `python verify/claim.py R1.main-sec-ood.6` |
| `R1.main-sec-ood.7` | -0.0114 — “arm} (Fair-N $-0.0325$, CI \ci{-0.0545}{-0.0114}; Fair-W $-0.0317$,” | -0.0114 | -0.0114 | `revision-1/recompute.json` | `python verify/claim.py R1.main-sec-ood.7` |
| `R1.main-sec-ood.8` | -0.0575 — “\ci{-0.0575}{-0.0065}), but significant for neither once the seeds are” | -0.0575 | -0.0575 | `revision-1/recompute.json` | `python verify/claim.py R1.main-sec-ood.8` |
| `R1.main-sec-ood.9` | -0.0065 — “\ci{-0.0575}{-0.0065}), but significant for neither once the seeds are” | -0.0065 | -0.0065 | `revision-1/recompute.json` | `python verify/claim.py R1.main-sec-ood.9` |

## R1.main-tab-confirmatory — Revision 1 — main paper, tab:confirmatory

*main paper, tab:confirmatory; `\label{tab:confirmatory}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.main-tab-confirmatory.1` | 10,000 — “$p$ come from one hierarchical bootstrap ($B = 10{,}000$; each arm's seeds,” | 10000 | 10000.00 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-confirmatory.1` |
| `R1.main-tab-confirmatory.2` | 9.52 — “of the gain, $1 - R$, at the registered grid gap of 9.52\,pt, the closest” | 9.52 | 9.5200 | `revision-1/registered/mde.json` | `python verify/claim.py R1.main-tab-confirmatory.2` |
| `R1.main-tab-confirmatory.3` | 9.75 — “below the observed 9.75\,pt). Sensitivity: the calibrated $t$-test across” | 9.75 | 9.7483 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.3` |
| `R1.main-tab-confirmatory.4` | 0.87 — “T1 & E1 $-$ Fair-N (c40) & 0.87 & \ci{0.02}{1.88} & 0.042 & 0.084 &” | 0.87 | 0.8678 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.4` |
| `R1.main-tab-confirmatory.5` | 0.02 — “T1 & E1 $-$ Fair-N (c40) & 0.87 & \ci{0.02}{1.88} & 0.042 & 0.084 &” | 0.02 | 0.0221 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.5` |
| `R1.main-tab-confirmatory.6` | 1.88 — “T1 & E1 $-$ Fair-N (c40) & 0.87 & \ci{0.02}{1.88} & 0.042 & 0.084 &” | 1.88 | 1.8767 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.6` |
| `R1.main-tab-confirmatory.7` | 0.042 — “T1 & E1 $-$ Fair-N (c40) & 0.87 & \ci{0.02}{1.88} & 0.042 & 0.084 &” | 0.042 | 0.0425 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-confirmatory.7` |
| `R1.main-tab-confirmatory.8` | 0.084 — “T1 & E1 $-$ Fair-N (c40) & 0.87 & \ci{0.02}{1.88} & 0.042 & 0.084 &” | 0.084 | 0.0842 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.8` |
| `R1.main-tab-confirmatory.9` | 1.78 — “no detectable difference & 1.78 / 1.43 & 0.070 \\” | 1.78 | 1.7816 | `revision-1/registered/mde.json` | `python verify/claim.py R1.main-tab-confirmatory.9` |
| `R1.main-tab-confirmatory.10` | 1.43 — “no detectable difference & 1.78 / 1.43 & 0.070 \\” | 1.43 | 1.4307 | `revision-1/registered/mde.json` | `python verify/claim.py R1.main-tab-confirmatory.10` |
| `R1.main-tab-confirmatory.11` | 0.070 — “no detectable difference & 1.78 / 1.43 & 0.070 \\” | 0.070 | 0.0700 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.11` |
| `R1.main-tab-confirmatory.12` | 0.73 — “T2 & E1 $-$ Fair-N (\auccomp) & 0.73 & \ci{0.12}{1.45} & 0.020 & 0.061 &” | 0.73 | 0.7302 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.12` |
| `R1.main-tab-confirmatory.13` | 0.12 — “T2 & E1 $-$ Fair-N (\auccomp) & 0.73 & \ci{0.12}{1.45} & 0.020 & 0.061 &” | 0.12 | 0.1175 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.13` |
| `R1.main-tab-confirmatory.14` | 1.45 — “T2 & E1 $-$ Fair-N (\auccomp) & 0.73 & \ci{0.12}{1.45} & 0.020 & 0.061 &” | 1.45 | 1.4503 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.14` |
| `R1.main-tab-confirmatory.15` | 0.020 — “T2 & E1 $-$ Fair-N (\auccomp) & 0.73 & \ci{0.12}{1.45} & 0.020 & 0.061 &” | 0.020 | 0.0205 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.15` |
| `R1.main-tab-confirmatory.16` | 0.061 — “T2 & E1 $-$ Fair-N (\auccomp) & 0.73 & \ci{0.12}{1.45} & 0.020 & 0.061 &” | 0.061 | 0.0615 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.16` |
| `R1.main-tab-confirmatory.17` | 1.37 — “no detectable difference & 1.37 / 1.10 & 0.095 \\” | 1.37 | 1.3698 | `revision-1/registered/mde.json` | `python verify/claim.py R1.main-tab-confirmatory.17` |
| `R1.main-tab-confirmatory.18` | 1.10 — “no detectable difference & 1.37 / 1.10 & 0.095 \\” | 1.10 | 1.1000 | `revision-1/registered/mde.json` | `python verify/claim.py R1.main-tab-confirmatory.18` |
| `R1.main-tab-confirmatory.19` | 0.095 — “no detectable difference & 1.37 / 1.10 & 0.095 \\” | 0.095 | 0.0954 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.19` |
| `R1.main-tab-confirmatory.20` | 0.88 — “T3 & retention $R$ against $R = 1$ (c40) & 0.88 & \ci{0.75}{1.03} &” | 0.88 | 0.8848 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.20` |
| `R1.main-tab-confirmatory.21` | 0.75 — “T3 & retention $R$ against $R = 1$ (c40) & 0.88 & \ci{0.75}{1.03} &” | 0.75 | 0.7548 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.21` |
| `R1.main-tab-confirmatory.22` | 1.03 — “T3 & retention $R$ against $R = 1$ (c40) & 0.88 & \ci{0.75}{1.03} &” | 1.03 | 1.0280 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.22` |
| `R1.main-tab-confirmatory.23` | 0.10 — “0.10 & 0.10 & no detectable difference & 0.22 / 0.18 & 0.095 \\” | 0.10 | 0.1041 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.23` |
| `R1.main-tab-confirmatory.24` | 0.10 — “0.10 & 0.10 & no detectable difference & 0.22 / 0.18 & 0.095 \\” | 0.10 | 0.1041 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.24` |
| `R1.main-tab-confirmatory.25` | 0.22 — “0.10 & 0.10 & no detectable difference & 0.22 / 0.18 & 0.095 \\” | 0.22 | 0.2200 | `revision-1/registered/mde.json` | `python verify/claim.py R1.main-tab-confirmatory.25` |
| `R1.main-tab-confirmatory.26` | 0.18 — “0.10 & 0.10 & no detectable difference & 0.22 / 0.18 & 0.095 \\” | 0.18 | 0.1800 | `revision-1/registered/mde.json` | `python verify/claim.py R1.main-tab-confirmatory.26` |
| `R1.main-tab-confirmatory.27` | 0.095 — “0.10 & 0.10 & no detectable difference & 0.22 / 0.18 & 0.095 \\” | 0.095 | 0.0954 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.27` |
| `R1.main-tab-confirmatory.28` | 7.48 — “(c40) & 7.48 & \ci{5.12}{9.94} & 0.00010 & 0.00050 & helps &” | 7.48 | 7.4783 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.28` |
| `R1.main-tab-confirmatory.29` | 5.12 — “(c40) & 7.48 & \ci{5.12}{9.94} & 0.00010 & 0.00050 & helps &” | 5.12 | 5.1229 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.29` |
| `R1.main-tab-confirmatory.30` | 9.94 — “(c40) & 7.48 & \ci{5.12}{9.94} & 0.00010 & 0.00050 & helps &” | 9.94 | 9.9443 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.30` |
| `R1.main-tab-confirmatory.31` | 0.00010 — “(c40) & 7.48 & \ci{5.12}{9.94} & 0.00010 & 0.00050 & helps &” | 0.00010 | 0.0001 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.31` |
| `R1.main-tab-confirmatory.32` | 0.00050 — “(c40) & 7.48 & \ci{5.12}{9.94} & 0.00010 & 0.00050 & helps &” | 0.00050 | 0.0005 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.32` |
| `R1.main-tab-confirmatory.33` | 1.46 — “1.46 / 1.18 & $5.6\times10^{-7}$ \\” | 1.46 | 1.4582 | `revision-1/registered/mde.json` | `python verify/claim.py R1.main-tab-confirmatory.33` |
| `R1.main-tab-confirmatory.34` | 1.18 — “1.46 / 1.18 & $5.6\times10^{-7}$ \\” | 1.18 | 1.1845 | `revision-1/registered/mde.json` | `python verify/claim.py R1.main-tab-confirmatory.34` |
| `R1.main-tab-confirmatory.35` | 5.6\times10^{-7} — “1.46 / 1.18 & $5.6\times10^{-7}$ \\” | 5.6e-7 | 0.0000 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.35` |
| `R1.main-tab-confirmatory.36` | 1.88 — “(c40) & 1.88 & \ci{0.79}{2.98} & 0.00050 & 0.0020 & helps &” | 1.88 | 1.8831 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.36` |
| `R1.main-tab-confirmatory.37` | 0.79 — “(c40) & 1.88 & \ci{0.79}{2.98} & 0.00050 & 0.0020 & helps &” | 0.79 | 0.7927 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.37` |
| `R1.main-tab-confirmatory.38` | 2.98 — “(c40) & 1.88 & \ci{0.79}{2.98} & 0.00050 & 0.0020 & helps &” | 2.98 | 2.9786 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.38` |
| `R1.main-tab-confirmatory.39` | 0.00050 — “(c40) & 1.88 & \ci{0.79}{2.98} & 0.00050 & 0.0020 & helps &” | 0.00050 | 0.0005 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.39` |
| `R1.main-tab-confirmatory.40` | 0.0020 — “(c40) & 1.88 & \ci{0.79}{2.98} & 0.00050 & 0.0020 & helps &” | 0.0020 | 0.0020 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.40` |
| `R1.main-tab-confirmatory.41` | 1.46 — “1.46 / 1.18 & 0.0016 \\” | 1.46 | 1.4582 | `revision-1/registered/mde.json` | `python verify/claim.py R1.main-tab-confirmatory.41` |
| `R1.main-tab-confirmatory.42` | 1.18 — “1.46 / 1.18 & 0.0016 \\” | 1.18 | 1.1845 | `revision-1/registered/mde.json` | `python verify/claim.py R1.main-tab-confirmatory.42` |
| `R1.main-tab-confirmatory.43` | 0.0016 — “1.46 / 1.18 & 0.0016 \\” | 0.0016 | 0.0016 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.43` |
| `R1.main-tab-confirmatory.44` | 7.19 — “denominator, SpatialBase $-$ anchor at c40, 9.75\,pt \ci{7.19}{12.40}; its” | 7.19 | 7.1888 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.44` |
| `R1.main-tab-confirmatory.45` | 12.40 — “denominator, SpatialBase $-$ anchor at c40, 9.75\,pt \ci{7.19}{12.40}; its” | 12.40 | 12.40 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.45` |
| `R1.main-tab-confirmatory.46` | 8.63 — “numerator, E2a $-$ anchor, 8.63\,pt \ci{6.16}{11.15}.} \\” | 8.63 | 8.6254 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.46` |
| `R1.main-tab-confirmatory.47` | 6.16 — “numerator, E2a $-$ anchor, 8.63\,pt \ci{6.16}{11.15}.} \\” | 6.16 | 6.1649 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.47` |
| `R1.main-tab-confirmatory.48` | 11.15 — “numerator, E2a $-$ anchor, 8.63\,pt \ci{6.16}{11.15}.} \\” | 11.15 | 11.15 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-tab-confirmatory.48` |

## R1.main-sec-adversary — Revision 1 — main paper, sec:adversary

*main paper, sec:adversary; `\label{sec:adversary}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.main-sec-adversary.1` | 0.87 — “difference in mean single-model video AUC at c40 ($\Delta = 0.87$\,pt,” | 0.87 | 0.8678 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-adversary.1` |
| `R1.main-sec-adversary.2` | 0.02 — “\ci{0.02}{1.88}, Holm $p = 0.084$). With 3 seeds per arm this test detects” | 0.02 | 0.0221 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-adversary.2` |
| `R1.main-sec-adversary.3` | 1.88 — “\ci{0.02}{1.88}, Holm $p = 0.084$). With 3 seeds per arm this test detects” | 1.88 | 1.8767 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-adversary.3` |
| `R1.main-sec-adversary.4` | 0.084 — “\ci{0.02}{1.88}, Holm $p = 0.084$). With 3 seeds per arm this test detects” | 0.084 | 0.0842 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-adversary.4` |
| `R1.main-sec-adversary.5` | 1.78 — “about 1.78\,pt with 80\,\% power at $\alpha = 0.01$ (1.43\,pt at” | 1.78 | 1.7816 | `revision-1/registered/mde.json` | `python verify/claim.py R1.main-sec-adversary.5` |
| `R1.main-sec-adversary.6` | 1.43 — “about 1.78\,pt with 80\,\% power at $\alpha = 0.01$ (1.43\,pt at” | 1.43 | 1.4307 | `revision-1/registered/mde.json` | `python verify/claim.py R1.main-sec-adversary.6` |
| `R1.main-sec-adversary.7` | 0.070 — “(calibrated sensitivity test: $p = 0.070$).” | 0.070 | 0.0700 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-adversary.7` |
| `R1.main-sec-adversary.8` | 0.73 — “difference in the mean AUC over c28--c40 (\auccomp) ($\Delta = 0.73$\,pt,” | 0.73 | 0.7302 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-adversary.8` |
| `R1.main-sec-adversary.9` | 0.12 — “\ci{0.12}{1.45}, Holm $p = 0.061$). With 3 seeds per arm this test detects” | 0.12 | 0.1175 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-adversary.9` |
| `R1.main-sec-adversary.10` | 1.45 — “\ci{0.12}{1.45}, Holm $p = 0.061$). With 3 seeds per arm this test detects” | 1.45 | 1.4503 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-adversary.10` |
| `R1.main-sec-adversary.11` | 0.061 — “\ci{0.12}{1.45}, Holm $p = 0.061$). With 3 seeds per arm this test detects” | 0.061 | 0.0615 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-adversary.11` |
| `R1.main-sec-adversary.12` | 1.37 — “about 1.37\,pt with 80\,\% power at $\alpha = 0.01$ (1.10\,pt at” | 1.37 | 1.3698 | `revision-1/registered/mde.json` | `python verify/claim.py R1.main-sec-adversary.12` |
| `R1.main-sec-adversary.13` | 1.10 — “about 1.37\,pt with 80\,\% power at $\alpha = 0.01$ (1.10\,pt at” | 1.10 | 1.1000 | `revision-1/registered/mde.json` | `python verify/claim.py R1.main-sec-adversary.13` |
| `R1.main-sec-adversary.14` | 0.095 — “(calibrated sensitivity test: $p = 0.095$).” | 0.095 | 0.0954 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-adversary.14` |
| `R1.main-sec-adversary.15` | 0.9531 — “est\_pm1 at the selected epoch was 0.9531 / 1.0000 / 1.0000 (Fair-N: 1.0000 /” | 0.9531 | 0.9531 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.main-sec-adversary.15` |
| `R1.main-sec-adversary.16` | 1.0000 — “est\_pm1 at the selected epoch was 0.9531 / 1.0000 / 1.0000 (Fair-N: 1.0000 /” | 1.0000 | 1.0000 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.main-sec-adversary.16` |
| `R1.main-sec-adversary.17` | 1.0000 — “est\_pm1 at the selected epoch was 0.9531 / 1.0000 / 1.0000 (Fair-N: 1.0000 /” | 1.0000 | 1.0000 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.main-sec-adversary.17` |
| `R1.main-sec-adversary.18` | 1.0000 — “est\_pm1 at the selected epoch was 0.9531 / 1.0000 / 1.0000 (Fair-N: 1.0000 /” | 1.0000 | 1.0000 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.main-sec-adversary.18` |
| `R1.main-sec-adversary.19` | 1.0000 — “1.0000 / 1.0000). Over its 30 epochs, E1's seed-2 run reached a lowest” | 1.0000 | 1.0000 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.main-sec-adversary.19` |
| `R1.main-sec-adversary.20` | 1.0000 — “1.0000 / 1.0000). Over its 30 epochs, E1's seed-2 run reached a lowest” | 1.0000 | 1.0000 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.main-sec-adversary.20` |
| `R1.main-sec-adversary.21` | 0.3672 — “accuracy of 0.3672 (epoch~2), below the registered reference of 0.7; the” | 0.3672 | 0.3672 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.main-sec-adversary.21` |
| `R1.main-sec-adversary.22` | 2 — “accuracy of 0.3672 (epoch~2), below the registered reference of 0.7; the” | 2 | 2.0000 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.main-sec-adversary.22` |
| `R1.main-sec-adversary.23` | 0.8359 — “lowest values of seeds 42 and 1 were 0.8359 and 0.9805, and at no selected” | 0.8359 | 0.8359 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.main-sec-adversary.23` |
| `R1.main-sec-adversary.24` | 0.9805 — “lowest values of seeds 42 and 1 were 0.8359 and 0.9805, and at no selected” | 0.9805 | 0.9805 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.main-sec-adversary.24` |
| `R1.main-sec-adversary.25` | 0.06 — “0.06\,pt (\ci{-1.13}{1.28}; raw weights), and the re-selection moved E1” | 0.06 | 0.0608 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.main-sec-adversary.25` |
| `R1.main-sec-adversary.26` | -1.13 — “0.06\,pt (\ci{-1.13}{1.28}; raw weights), and the re-selection moved E1” | -1.13 | -1.1254 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.main-sec-adversary.26` |
| `R1.main-sec-adversary.27` | 1.28 — “0.06\,pt (\ci{-1.13}{1.28}; raw weights), and the re-selection moved E1” | 1.28 | 1.2845 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.main-sec-adversary.27` |
| `R1.main-sec-adversary.28` | -1.15 — “itself by $-1.15$\,pt (\ci{-2.21}{-0.21}; raw $-$ EMA). A lean: on our own” | -1.15 | -1.1522 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.main-sec-adversary.28` |
| `R1.main-sec-adversary.29` | -2.21 — “itself by $-1.15$\,pt (\ci{-2.21}{-0.21}; raw $-$ EMA). A lean: on our own” | -2.21 | -2.2127 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.main-sec-adversary.29` |
| `R1.main-sec-adversary.30` | -0.21 — “itself by $-1.15$\,pt (\ci{-2.21}{-0.21}; raw $-$ EMA). A lean: on our own” | -0.21 | -0.2066 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.main-sec-adversary.30` |
| `R1.main-sec-adversary.31` | 1.51 — “CRF-40 re-encode of the c0 test masters, E1 $-$ Fair-N was 1.51\,pt” | 1.51 | 1.5055 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.main-sec-adversary.31` |
| `R1.main-sec-adversary.32` | 0.25 — “(\ci{0.25}{2.92}; EMA weights).” | 0.25 | 0.2508 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.main-sec-adversary.32` |
| `R1.main-sec-adversary.33` | 2.92 — “(\ci{0.25}{2.92}; EMA weights).” | 2.92 | 2.9245 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.main-sec-adversary.33` |

- `R1.main-sec-adversary.25` — weights: raw
- `R1.main-sec-adversary.26` — weights: raw
- `R1.main-sec-adversary.27` — weights: raw
- `R1.main-sec-adversary.28` — weights: raw and EMA
- `R1.main-sec-adversary.29` — weights: raw and EMA
- `R1.main-sec-adversary.30` — weights: raw and EMA
- `R1.main-sec-adversary.31` — weights: EMA
- `R1.main-sec-adversary.32` — weights: EMA
- `R1.main-sec-adversary.33` — weights: EMA

## R1.main-sec-data — Revision 1 — main paper, sec:data

*main paper, sec:data; `\label{sec:data}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.main-sec-data.1` | 0.019 — “3-seed mean; post hoc, the c0-anchored drop of the same runs is 0.019--0.025:” | 0.019 | 0.0189 | `predictions/ffpp/f2_spatres_full_s42.json` | `python verify/claim.py R1.main-sec-data.1` |
| `R1.main-sec-data.2` | 0.025 — “3-seed mean; post hoc, the c0-anchored drop of the same runs is 0.019--0.025:” | 0.025 | 0.0246 | `predictions/ffpp/trunk_recipe_s42.json` +2 | `python verify/claim.py R1.main-sec-data.2` |
| `R1.main-sec-data.3` | 0.021 — “SpatialBase 0.021, TrunkCtrl 0.025, Fair-N 0.023, Fair-W 0.019; CAFRL as” | 0.021 | 0.0210 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py R1.main-sec-data.3` |
| `R1.main-sec-data.4` | 0.023 — “SpatialBase 0.021, TrunkCtrl 0.025, Fair-N 0.023, Fair-W 0.019; CAFRL as” | 0.023 | 0.0227 | `predictions/ffpp/f1_none_fair_s42.json` | `python verify/claim.py R1.main-sec-data.4` |
| `R1.main-sec-data.5` | 0.037 — “specified 0.037 --- EMA weights for the CAFRL-family runs, raw for SpatialBase” | 0.037 | 0.0366 | `predictions/ffpp/a0.json` | `python verify/claim.py R1.main-sec-data.5` |

## R1.main-sec-datatests — Revision 1 — main paper, sec:datatests

*main paper, sec:datatests; `\label{sec:datatests}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.main-sec-datatests.1` | 0.75 — “Trained without c40, SpatialBase kept $R = 0.88$ (\ci{0.75}{1.03}) of the” | 0.75 | 0.7548 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-datatests.1` |
| `R1.main-sec-datatests.2` | 1.03 — “Trained without c40, SpatialBase kept $R = 0.88$ (\ci{0.75}{1.03}) of the” | 1.03 | 1.0280 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-datatests.2` |
| `R1.main-sec-datatests.3` | 0.10 — “c40 gain; $R$ is not detectably below 1 (Holm $p = 0.10$). At the observed gap” | 0.10 | 0.1041 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-datatests.3` |
| `R1.main-sec-datatests.4` | 9.75 — “of 9.75\,pt this test detects a loss of about 0.22 of the gain with 80\,\%” | 9.75 | 9.7483 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-datatests.4` |
| `R1.main-sec-datatests.5` | 0.22 — “of 9.75\,pt this test detects a loss of about 0.22 of the gain with 80\,\%” | 0.22 | 0.2200 | `revision-1/registered/mde.json` | `python verify/claim.py R1.main-sec-datatests.5` |
| `R1.main-sec-datatests.6` | 0.095 — “(calibrated sensitivity test: $p = 0.095$).” | 0.095 | 0.0954 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-datatests.6` |
| `R1.main-sec-datatests.7` | 7.48 — “7.48\,pt averaged over c40 exposure (\ci{5.12}{9.94}, Holm $p = 0.00050$). In” | 7.48 | 7.4783 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-datatests.7` |
| `R1.main-sec-datatests.8` | 5.12 — “7.48\,pt averaged over c40 exposure (\ci{5.12}{9.94}, Holm $p = 0.00050$). In” | 5.12 | 5.1229 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-datatests.8` |
| `R1.main-sec-datatests.9` | 9.94 — “7.48\,pt averaged over c40 exposure (\ci{5.12}{9.94}, Holm $p = 0.00050$). In” | 9.94 | 9.9443 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-datatests.9` |
| `R1.main-sec-datatests.10` | 0.00050 — “7.48\,pt averaged over c40 exposure (\ci{5.12}{9.94}, Holm $p = 0.00050$). In” | 0.00050 | 0.0005 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-datatests.10` |
| `R1.main-sec-datatests.11` | 5.6\times10^{-7} — “test: $p = 5.6\times10^{-7}$).” | 5.6e-7 | 0.0000 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-datatests.11` |
| `R1.main-sec-datatests.12` | 1.88 — “quality) raised the mean single-model c40 AUC by 1.88\,pt averaged over codec” | 1.88 | 1.8831 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-datatests.12` |
| `R1.main-sec-datatests.13` | 0.79 — “(\ci{0.79}{2.98}, Holm $p = 0.0020$). Robustness at c40 depends in part on” | 0.79 | 0.7927 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-datatests.13` |
| `R1.main-sec-datatests.14` | 2.98 — “(\ci{0.79}{2.98}, Holm $p = 0.0020$). Robustness at c40 depends in part on” | 2.98 | 2.9786 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-datatests.14` |
| `R1.main-sec-datatests.15` | 0.0020 — “(\ci{0.79}{2.98}, Holm $p = 0.0020$). Robustness at c40 depends in part on” | 0.0020 | 0.0020 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-datatests.15` |
| `R1.main-sec-datatests.16` | 0.0016 — “$p = 0.0016$).” | 0.0016 | 0.0016 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-datatests.16` |
| `R1.main-sec-datatests.17` | 0.94 — “R was 0.94 (\ci{0.79}{1.13}). With SpatialBase re-selected on c23 + c36, the” | 0.94 | 0.9438 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.main-sec-datatests.17` |
| `R1.main-sec-datatests.18` | 0.79 — “R was 0.94 (\ci{0.79}{1.13}). With SpatialBase re-selected on c23 + c36, the” | 0.79 | 0.7944 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.main-sec-datatests.18` |
| `R1.main-sec-datatests.19` | 1.13 — “R was 0.94 (\ci{0.79}{1.13}). With SpatialBase re-selected on c23 + c36, the” | 1.13 | 1.1330 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.main-sec-datatests.19` |
| `R1.main-sec-datatests.20` | 1.58 — “c40-exposure effect was 1.58\,pt (\ci{0.38}{2.73}; secondary,” | 1.58 | 1.5784 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.main-sec-datatests.20` |
| `R1.main-sec-datatests.21` | 0.38 — “c40-exposure effect was 1.58\,pt (\ci{0.38}{2.73}; secondary,” | 0.38 | 0.3769 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.main-sec-datatests.21` |
| `R1.main-sec-datatests.22` | 2.73 — “c40-exposure effect was 1.58\,pt (\ci{0.38}{2.73}; secondary,” | 2.73 | 2.7334 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.main-sec-datatests.22` |
| `R1.main-sec-datatests.23` | -1.52 — “effect with and without c40 exposure differed by $-1.52$\,pt” | -1.52 | -1.5204 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-datatests.23` |
| `R1.main-sec-datatests.24` | -3.59 — “(\ci{-3.59}{0.55}; descriptive, not tested). Third, E2b, SpatialBase trained” | -3.59 | -3.5940 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-datatests.24` |
| `R1.main-sec-datatests.25` | 0.55 — “(\ci{-3.59}{0.55}; descriptive, not tested). Third, E2b, SpatialBase trained” | 0.55 | 0.5472 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-datatests.25` |
| `R1.main-sec-datatests.26` | -11.68 — “c23-only anchor: SpatialBase $-$ anchor was $-11.68$\,pt (\ci{-14.98}{-8.57}).” | -11.68 | -11.68 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.main-sec-datatests.26` |
| `R1.main-sec-datatests.27` | -14.98 — “c23-only anchor: SpatialBase $-$ anchor was $-11.68$\,pt (\ci{-14.98}{-8.57}).” | -14.98 | -14.98 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.main-sec-datatests.27` |
| `R1.main-sec-datatests.28` | -8.57 — “c23-only anchor: SpatialBase $-$ anchor was $-11.68$\,pt (\ci{-14.98}{-8.57}).” | -8.57 | -8.5735 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.main-sec-datatests.28` |
| `R1.main-sec-datatests.29` | -1.92 — “On the WildDeepfake test split the same difference was $-1.92$\,pt” | -1.92 | -1.9235 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.main-sec-datatests.29` |
| `R1.main-sec-datatests.30` | -7.13 — “(\ci{-7.13}{2.74}), an interval that includes zero; because the DFDC and” | -7.13 | -7.1330 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.main-sec-datatests.30` |
| `R1.main-sec-datatests.31` | 2.74 — “(\ci{-7.13}{2.74}), an interval that includes zero; because the DFDC and” | 2.74 | 2.7352 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.main-sec-datatests.31` |
| `R1.main-sec-datatests.32` | -3.15 — “form, the c40 level in training, was $-3.15$\,pt (\ci{-6.54}{-0.04}) on the” | -3.15 | -3.1519 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.main-sec-datatests.32` |
| `R1.main-sec-datatests.33` | -6.54 — “form, the c40 level in training, was $-3.15$\,pt (\ci{-6.54}{-0.04}) on the” | -6.54 | -6.5385 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.main-sec-datatests.33` |
| `R1.main-sec-datatests.34` | -0.04 — “form, the c40 level in training, was $-3.15$\,pt (\ci{-6.54}{-0.04}) on the” | -0.04 | -0.0351 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.main-sec-datatests.34` |
| `R1.main-sec-datatests.35` | -2.97 — “original crops and $-2.97$\,pt (\ci{-6.46}{0.16}) on crops re-cut with a” | -2.97 | -2.9671 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.main-sec-datatests.35` |
| `R1.main-sec-datatests.36` | -6.46 — “original crops and $-2.97$\,pt (\ci{-6.46}{0.16}) on crops re-cut with a” | -6.46 | -6.4615 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.main-sec-datatests.36` |
| `R1.main-sec-datatests.37` | 0.16 — “original crops and $-2.97$\,pt (\ci{-6.46}{0.16}) on crops re-cut with a” | 0.16 | 0.1582 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.main-sec-datatests.37` |

- `R1.main-sec-datatests.26` — weights: raw
- `R1.main-sec-datatests.27` — weights: raw
- `R1.main-sec-datatests.28` — weights: raw
- `R1.main-sec-datatests.29` — weights: raw
- `R1.main-sec-datatests.30` — weights: raw
- `R1.main-sec-datatests.31` — weights: raw
- `R1.main-sec-datatests.32` — weights: raw
- `R1.main-sec-datatests.33` — weights: raw
- `R1.main-sec-datatests.34` — weights: raw
- `R1.main-sec-datatests.35` — weights: raw
- `R1.main-sec-datatests.36` — weights: raw
- `R1.main-sec-datatests.37` — weights: raw

## R1.main-Limitations — Revision 1 — main paper, §“Limitations”

*main paper, §“Limitations”*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.main-Limitations.1` | 0.881 — “Xception-mq, a single seed-42 run, reaches 0.881 and 0.688 at DFD-c23 and” | 0.881 | 0.8806 | `predictions/cross_dataset/b4_xception_mq.json` | `python verify/claim.py R1.main-Limitations.1` |
| `R1.main-Limitations.2` | 0.688 — “Xception-mq, a single seed-42 run, reaches 0.881 and 0.688 at DFD-c23 and” | 0.688 | 0.6880 | `predictions/cross_dataset/b4_xception_mq.json` | `python verify/claim.py R1.main-Limitations.2` |
| `R1.main-Limitations.3` | 0.825 — “DFD-c40 against the three-seed means of 0.825 and 0.650 of the 4.0\,M control,” | 0.825 | 0.8249 | `predictions/cross_dataset/b7_effnet_b0_mq_fliponly.json` +2 | `python verify/claim.py R1.main-Limitations.3` |
| `R1.main-Limitations.4` | 0.650 — “DFD-c40 against the three-seed means of 0.825 and 0.650 of the 4.0\,M control,” | 0.650 | 0.6504 | `predictions/cross_dataset/b7_effnet_b0_mq_fliponly.json` +2 | `python verify/claim.py R1.main-Limitations.4` |
| `R1.main-Limitations.5` | 1 — “frequency effect here, while at FF++ c40 it is within 1\,pt of the control,” | 1 | 0.8865 | `predictions/ffpp/b4_xception_mq.json` +1 | `python verify/claim.py R1.main-Limitations.5` |

- `R1.main-Limitations.1` — Table S3 lower block, Xception-mq, seed 42 (stored statistic; no per-video scores)
- `R1.main-Limitations.2` — Table S3 lower block, Xception-mq, seed 42 (stored statistic; no per-video scores)
- `R1.main-Limitations.3` — Table S3 upper block, SpatialBase 3-seed mean
- `R1.main-Limitations.4` — Table S3 upper block, SpatialBase 3-seed mean
- `R1.main-Limitations.5` — seed for seed (seed 42 vs. seed 42, sec:standing): the larger of the two Xception-mq c40 gaps to SpatialBase, standard policy 0.89 pt (the augmentation-matched one is 0.41 pt, 0.9631 vs. 0.9590); the printed bound rounds from it

## R1.main-sec-conclusionfinal — Revision 1 — main paper, sec:conclusionfinal

*main paper, sec:conclusionfinal; `\label{sec:conclusionfinal}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.main-sec-conclusionfinal.1` | +0.0366 — “specified at c40 was $+0.0366$, 95\% CI \ci{+0.020}{+0.054}” | +0.0366 | 0.0366 | `revision-1/recompute.json` | `python verify/claim.py R1.main-sec-conclusionfinal.1` |
| `R1.main-sec-conclusionfinal.2` | +0.020 — “specified at c40 was $+0.0366$, 95\% CI \ci{+0.020}{+0.054}” | +0.020 | 0.0205 | `verify/expected.json` +2 | `python verify/claim.py R1.main-sec-conclusionfinal.2 --bootstrap` |
| `R1.main-sec-conclusionfinal.3` | +0.054 — “specified at c40 was $+0.0366$, 95\% CI \ci{+0.020}{+0.054}” | +0.054 | 0.0540 | `verify/expected.json` +2 | `python verify/claim.py R1.main-sec-conclusionfinal.3 --bootstrap` |
| `R1.main-sec-conclusionfinal.4` | 0.002 — “the gate adjudicated it (the two further shipped-CAFRL seeds lie within 0.002” | 0.002 | 0.0019 | `predictions/ffpp/a0.json` +1 | `python verify/claim.py R1.main-sec-conclusionfinal.4` |
| `R1.main-sec-conclusionfinal.5` | +0.0396 — “$+0.0396$, CI \ci{+0.0231}{+0.0570}, over the shipped-recipe arm CAFRL$-$adv,” | +0.0396 | 0.0396 | `revision-1/recompute.json` | `python verify/claim.py R1.main-sec-conclusionfinal.5` |
| `R1.main-sec-conclusionfinal.6` | +0.0231 — “$+0.0396$, CI \ci{+0.0231}{+0.0570}, over the shipped-recipe arm CAFRL$-$adv,” | +0.0231 | 0.0231 | `verify/expected.json` +2 | `python verify/claim.py R1.main-sec-conclusionfinal.6 --bootstrap` |
| `R1.main-sec-conclusionfinal.7` | +0.0570 — “$+0.0396$, CI \ci{+0.0231}{+0.0570}, over the shipped-recipe arm CAFRL$-$adv,” | +0.0570 | 0.0570 | `verify/expected.json` +2 | `python verify/claim.py R1.main-sec-conclusionfinal.7 --bootstrap` |
| `R1.main-sec-conclusionfinal.8` | -0.0004 — “and Fair-N then showed no detectable difference from SpatialBase ($-0.0004$,” | -0.0004 | -0.0004 | `revision-1/recompute.json` | `python verify/claim.py R1.main-sec-conclusionfinal.8` |
| `R1.main-sec-conclusionfinal.9` | -0.0092 — “CI \ci{-0.0092}{+0.0080}); both seed 42, post-audit pre-specified” | -0.0092 | -0.0092 | `verify/expected.json` +2 | `python verify/claim.py R1.main-sec-conclusionfinal.9 --bootstrap` |
| `R1.main-sec-conclusionfinal.10` | +0.0080 — “CI \ci{-0.0092}{+0.0080}); both seed 42, post-audit pre-specified” | +0.0080 | 0.0080 | `verify/expected.json` +2 | `python verify/claim.py R1.main-sec-conclusionfinal.10 --bootstrap` |
| `R1.main-sec-conclusionfinal.11` | -0.0002 — “$-0.0002$ \ci{-0.0105}{+0.0112} and Fair-W $-$ SpatialBase $+0.0053$” | -0.0002 | -0.0002 | `revision-1/recompute.json` | `python verify/claim.py R1.main-sec-conclusionfinal.11` |
| `R1.main-sec-conclusionfinal.12` | -0.0105 — “$-0.0002$ \ci{-0.0105}{+0.0112} and Fair-W $-$ SpatialBase $+0.0053$” | -0.0105 | -0.0105 | `revision-1/recompute.json` | `python verify/claim.py R1.main-sec-conclusionfinal.12` |
| `R1.main-sec-conclusionfinal.13` | +0.0112 — “$-0.0002$ \ci{-0.0105}{+0.0112} and Fair-W $-$ SpatialBase $+0.0053$” | +0.0112 | 0.0112 | `revision-1/recompute.json` | `python verify/claim.py R1.main-sec-conclusionfinal.13` |
| `R1.main-sec-conclusionfinal.14` | +0.0053 — “$-0.0002$ \ci{-0.0105}{+0.0112} and Fair-W $-$ SpatialBase $+0.0053$” | +0.0053 | 0.0053 | `revision-1/recompute.json` | `python verify/claim.py R1.main-sec-conclusionfinal.14` |
| `R1.main-sec-conclusionfinal.15` | -0.0042 — “\ci{-0.0042}{+0.0171}; the pre-specified contrasts, conditional on the three” | -0.0042 | -0.0042 | `revision-1/recompute.json` | `python verify/claim.py R1.main-sec-conclusionfinal.15` |
| `R1.main-sec-conclusionfinal.16` | +0.0171 — “\ci{-0.0042}{+0.0171}; the pre-specified contrasts, conditional on the three” | +0.0171 | 0.0171 | `revision-1/recompute.json` | `python verify/claim.py R1.main-sec-conclusionfinal.16` |
| `R1.main-sec-conclusionfinal.17` | 85.27 — “85.27 AUC points at c40 at the selected checkpoints and 89.99 at epoch 30” | 85.27 | 85.27 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.main-sec-conclusionfinal.17` |
| `R1.main-sec-conclusionfinal.18` | 89.99 — “85.27 AUC points at c40 at the selected checkpoints and 89.99 at epoch 30” | 89.99 | 89.99 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.main-sec-conclusionfinal.18` |
| `R1.main-sec-conclusionfinal.19` | 0.919 — “detectable (CAFRL$-$adv 0.919 against the full model's 0.922 at c40) and” | 0.919 | 0.9190 | `predictions/ffpp/a1_none_s42.json` | `python verify/claim.py R1.main-sec-conclusionfinal.19` |
| `R1.main-sec-conclusionfinal.20` | 0.922 — “detectable (CAFRL$-$adv 0.919 against the full model's 0.922 at c40) and” | 0.922 | 0.9224 | `predictions/ffpp/a0.json` | `python verify/claim.py R1.main-sec-conclusionfinal.20` |
| `R1.main-sec-conclusionfinal.21` | 0.88 — “$0.88 \rightarrow {\approx}0.4$; D6). Restored at the fair recipe (E1,” | 0.88 | 0.8758 | `probes/p1_compression_estimator.json` | `python verify/claim.py R1.main-sec-conclusionfinal.21` |
| `R1.main-sec-conclusionfinal.22` | 0.87 — “difference in detection: $\Delta = 0.87$\,pt at c40 (\ci{0.02}{1.88}, Holm” | 0.87 | 0.8678 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-conclusionfinal.22` |
| `R1.main-sec-conclusionfinal.23` | 0.02 — “difference in detection: $\Delta = 0.87$\,pt at c40 (\ci{0.02}{1.88}, Holm” | 0.02 | 0.0221 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-conclusionfinal.23` |
| `R1.main-sec-conclusionfinal.24` | 1.88 — “difference in detection: $\Delta = 0.87$\,pt at c40 (\ci{0.02}{1.88}, Holm” | 1.88 | 1.8767 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-conclusionfinal.24` |
| `R1.main-sec-conclusionfinal.25` | 0.084 — “$p = 0.084$) and $0.73$\,pt on \auccomp{} (\ci{0.12}{1.45}, Holm” | 0.084 | 0.0842 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-conclusionfinal.25` |
| `R1.main-sec-conclusionfinal.26` | 0.73 — “$p = 0.084$) and $0.73$\,pt on \auccomp{} (\ci{0.12}{1.45}, Holm” | 0.73 | 0.7302 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-conclusionfinal.26` |
| `R1.main-sec-conclusionfinal.27` | 0.12 — “$p = 0.084$) and $0.73$\,pt on \auccomp{} (\ci{0.12}{1.45}, Holm” | 0.12 | 0.1175 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-conclusionfinal.27` |
| `R1.main-sec-conclusionfinal.28` | 1.45 — “$p = 0.084$) and $0.73$\,pt on \auccomp{} (\ci{0.12}{1.45}, Holm” | 1.45 | 1.4503 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-conclusionfinal.28` |
| `R1.main-sec-conclusionfinal.29` | 0.061 — “$p = 0.061$). Its estimator stayed accurate at the selected epochs ($\pm1$-level accuracy” | 0.061 | 0.0615 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-conclusionfinal.29` |
| `R1.main-sec-conclusionfinal.30` | 0.9531 — “0.9531 / 1.0000 / 1.0000), although one seed fell below the registered” | 0.9531 | 0.9531 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.main-sec-conclusionfinal.30` |
| `R1.main-sec-conclusionfinal.31` | 1.0000 — “0.9531 / 1.0000 / 1.0000), although one seed fell below the registered” | 1.0000 | 1.0000 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.main-sec-conclusionfinal.31` |
| `R1.main-sec-conclusionfinal.32` | 1.0000 — “0.9531 / 1.0000 / 1.0000), although one seed fell below the registered” | 1.0000 | 1.0000 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.main-sec-conclusionfinal.32` |
| `R1.main-sec-conclusionfinal.33` | 1.78 — “arm at one strength ($\lambda_{\max} = 0.5$); these tests detect about 1.78” | 1.78 | 1.7816 | `revision-1/registered/mde.json` | `python verify/claim.py R1.main-sec-conclusionfinal.33` |
| `R1.main-sec-conclusionfinal.34` | 1.37 — “and 1.37\,pt at 80\% power and $\alpha = 0.01$, and smaller effects in either direction ar” | 1.37 | 1.3698 | `revision-1/registered/mde.json` | `python verify/claim.py R1.main-sec-conclusionfinal.34` |
| `R1.main-sec-conclusionfinal.35` | 7.48 — “gave a higher mean single-model c40 AUC by 7.48\,pt averaged over c40” | 7.48 | 7.4783 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-conclusionfinal.35` |
| `R1.main-sec-conclusionfinal.36` | 5.12 — “exposure (\ci{5.12}{9.94}, Holm $p = 0.00050$; T4), and including the” | 5.12 | 5.1229 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-conclusionfinal.36` |
| `R1.main-sec-conclusionfinal.37` | 9.94 — “exposure (\ci{5.12}{9.94}, Holm $p = 0.00050$; T4), and including the” | 9.94 | 9.9443 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-conclusionfinal.37` |
| `R1.main-sec-conclusionfinal.38` | 0.00050 — “exposure (\ci{5.12}{9.94}, Holm $p = 0.00050$; T4), and including the” | 0.00050 | 0.0005 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-conclusionfinal.38` |
| `R1.main-sec-conclusionfinal.39` | 1.88 — “c40-level data raised it by 1.88\,pt averaged over codec (\ci{0.79}{2.98},” | 1.88 | 1.8831 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-conclusionfinal.39` |
| `R1.main-sec-conclusionfinal.40` | 0.79 — “c40-level data raised it by 1.88\,pt averaged over codec (\ci{0.79}{2.98},” | 0.79 | 0.7927 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-conclusionfinal.40` |
| `R1.main-sec-conclusionfinal.41` | 2.98 — “c40-level data raised it by 1.88\,pt averaged over codec (\ci{0.79}{2.98},” | 2.98 | 2.9786 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-conclusionfinal.41` |
| `R1.main-sec-conclusionfinal.42` | 0.0020 — “Holm $p = 0.0020$; T5); both registered, paired, three seeds per arm” | 0.0020 | 0.0020 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-conclusionfinal.42` |
| `R1.main-sec-conclusionfinal.43` | 0.88 — “kept $R = 0.88$ \ci{0.75}{1.03} of its c40 gain (T3), not detectably below 1,” | 0.88 | 0.8848 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-conclusionfinal.43` |
| `R1.main-sec-conclusionfinal.44` | 0.75 — “kept $R = 0.88$ \ci{0.75}{1.03} of its c40 gain (T3), not detectably below 1,” | 0.75 | 0.7548 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-conclusionfinal.44` |
| `R1.main-sec-conclusionfinal.45` | 1.03 — “kept $R = 0.88$ \ci{0.75}{1.03} of its c40 gain (T3), not detectably below 1,” | 1.03 | 1.0280 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.main-sec-conclusionfinal.45` |

- `R1.main-sec-conclusionfinal.4` — the larger of the two further shipped-CAFRL seeds' c40 deviations from a0 (a1_grl_s2: 0.0019; a1_grl_s1: 0.0002); the printed bound rounds from it

## R1.main-tab-appledger — Revision 1 — main paper, tab:appledger

*main paper, tab:appledger; `\label{tab:appledger}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.main-tab-appledger.1` | 0.0397 — “the 0.0451 trunk gap (TrunkCtrl 0.0397 above the shipped-recipe arm, the” | 0.0397 | 0.0397 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-appledger.1` |
| `R1.main-tab-appledger.2` | 0.0054 — “only difference whose interval excludes zero, and 0.0054 below” | 0.0054 | 0.0054 | `predictions/ffpp/b7_effnet_b0_mq_fliponly.json` +3 | `python verify/claim.py R1.main-tab-appledger.2` |
| `R1.main-tab-appledger.3` | +0.0054 — “$-0.0038$, CI \ci{-0.0116}{+0.0039}, and $+0.0054$ \ci{-0.0040}{+0.0156}” | +0.0054 | 0.0054 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-appledger.3` |
| `R1.main-tab-appledger.4` | -0.0040 — “$-0.0038$, CI \ci{-0.0116}{+0.0039}, and $+0.0054$ \ci{-0.0040}{+0.0156}” | -0.0040 | -0.0040 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-appledger.4` |
| `R1.main-tab-appledger.5` | +0.0156 — “$-0.0038$, CI \ci{-0.0116}{+0.0039}, and $+0.0054$ \ci{-0.0040}{+0.0156}” | +0.0156 | 0.0156 | `revision-1/recompute.json` | `python verify/claim.py R1.main-tab-appledger.5` |
| `R1.main-tab-appledger.6` | 4.0 — “differ in more than width (4.0\,M vs.\ 3.68\,M), so this does not isolate” | 4.0 | 4.0088 | `probes/param_counts_arms.json` | `python verify/claim.py R1.main-tab-appledger.6` |
| `R1.main-tab-appledger.7` | 3.68 — “differ in more than width (4.0\,M vs.\ 3.68\,M), so this does not isolate” | 3.68 | 3.6778 | `probes/param_counts_arms.json` | `python verify/claim.py R1.main-tab-appledger.7` |

## R1.supp-tab-appseeds — Revision 1 — Supplementary Material, tab:appseeds

*Supplementary Material, tab:appseeds; `\label{tab:appseeds}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-tab-appseeds.1` | +0.53 — “that difference is not tested. Fair-W's $+0.53$\,pt seed-mean lean is” | +0.53 | 0.5340 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-tab-appseeds.1` |

## R1.supp-app-seeds — Revision 1 — Supplementary Material, app:seeds

*Supplementary Material, app:seeds; `\label{app:seeds}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-app-seeds.1` | +0.0095 — “reads $+0.0095$ \ci{-0.0039}{+0.0230}, $+0.0001$ \ci{-0.0129}{+0.0127} and” | +0.0095 | 0.0095 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.1` |
| `R1.supp-app-seeds.2` | -0.0039 — “reads $+0.0095$ \ci{-0.0039}{+0.0230}, $+0.0001$ \ci{-0.0129}{+0.0127} and” | -0.0039 | -0.0039 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.2` |
| `R1.supp-app-seeds.3` | +0.0230 — “reads $+0.0095$ \ci{-0.0039}{+0.0230}, $+0.0001$ \ci{-0.0129}{+0.0127} and” | +0.0230 | 0.0230 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.3` |
| `R1.supp-app-seeds.4` | +0.0001 — “reads $+0.0095$ \ci{-0.0039}{+0.0230}, $+0.0001$ \ci{-0.0129}{+0.0127} and” | +0.0001 | 0.0001 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.4` |
| `R1.supp-app-seeds.5` | -0.0129 — “reads $+0.0095$ \ci{-0.0039}{+0.0230}, $+0.0001$ \ci{-0.0129}{+0.0127} and” | -0.0129 | -0.0129 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.5` |
| `R1.supp-app-seeds.6` | +0.0127 — “reads $+0.0095$ \ci{-0.0039}{+0.0230}, $+0.0001$ \ci{-0.0129}{+0.0127} and” | +0.0127 | 0.0127 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.6` |
| `R1.supp-app-seeds.7` | -0.0015 — “$-0.0015$ \ci{-0.0161}{+0.0113} (seeds 42, 1, 2; source-identity clusters),” | -0.0015 | -0.0015 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.7` |
| `R1.supp-app-seeds.8` | -0.0161 — “$-0.0015$ \ci{-0.0161}{+0.0113} (seeds 42, 1, 2; source-identity clusters),” | -0.0161 | -0.0161 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.8` |
| `R1.supp-app-seeds.9` | +0.0113 — “$-0.0015$ \ci{-0.0161}{+0.0113} (seeds 42, 1, 2; source-identity clusters),” | +0.0113 | 0.0113 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.9` |
| `R1.supp-app-seeds.10` | +0.0052 — “and at \auccomp{} $+0.0052$ \ci{-0.0035}{+0.0138}, $-0.0053$” | +0.0052 | 0.0052 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.10` |
| `R1.supp-app-seeds.11` | -0.0035 — “and at \auccomp{} $+0.0052$ \ci{-0.0035}{+0.0138}, $-0.0053$” | -0.0035 | -0.0035 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.11` |
| `R1.supp-app-seeds.12` | +0.0138 — “and at \auccomp{} $+0.0052$ \ci{-0.0035}{+0.0138}, $-0.0053$” | +0.0138 | 0.0138 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.12` |
| `R1.supp-app-seeds.13` | -0.0053 — “and at \auccomp{} $+0.0052$ \ci{-0.0035}{+0.0138}, $-0.0053$” | -0.0053 | -0.0053 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.13` |
| `R1.supp-app-seeds.14` | -0.0148 — “\ci{-0.0148}{+0.0035} and $+0.0004$ \ci{-0.0105}{+0.0103}. Pooled with the” | -0.0148 | -0.0148 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.14` |
| `R1.supp-app-seeds.15` | +0.0035 — “\ci{-0.0148}{+0.0035} and $+0.0004$ \ci{-0.0105}{+0.0103}. Pooled with the” | +0.0035 | 0.0035 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.15` |
| `R1.supp-app-seeds.16` | +0.0004 — “\ci{-0.0148}{+0.0035} and $+0.0004$ \ci{-0.0105}{+0.0103}. Pooled with the” | +0.0004 | 0.0004 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.16` |
| `R1.supp-app-seeds.17` | -0.0105 — “\ci{-0.0148}{+0.0035} and $+0.0004$ \ci{-0.0105}{+0.0103}. Pooled with the” | -0.0105 | -0.0105 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.17` |
| `R1.supp-app-seeds.18` | +0.0103 — “\ci{-0.0148}{+0.0035} and $+0.0004$ \ci{-0.0105}{+0.0103}. Pooled with the” | +0.0103 | 0.0103 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.18` |
| `R1.supp-app-seeds.19` | +0.0014 — “seeds fixed (video unit; point estimates) it is $+0.0014$” | +0.0014 | 0.0014 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.19` |
| `R1.supp-app-seeds.20` | -0.0051 — “\ci{-0.0051}{+0.0078} at c40 and $+0.0006$ \ci{-0.0031}{+0.0043} at” | -0.0051 | -0.0051 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.20` |
| `R1.supp-app-seeds.21` | +0.0078 — “\ci{-0.0051}{+0.0078} at c40 and $+0.0006$ \ci{-0.0031}{+0.0043} at” | +0.0078 | 0.0078 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.21` |
| `R1.supp-app-seeds.22` | +0.0006 — “\ci{-0.0051}{+0.0078} at c40 and $+0.0006$ \ci{-0.0031}{+0.0043} at” | +0.0006 | 0.0006 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.22` |
| `R1.supp-app-seeds.23` | -0.0031 — “\ci{-0.0051}{+0.0078} at c40 and $+0.0006$ \ci{-0.0031}{+0.0043} at” | -0.0031 | -0.0031 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.23` |
| `R1.supp-app-seeds.24` | +0.0043 — “\ci{-0.0051}{+0.0078} at c40 and $+0.0006$ \ci{-0.0031}{+0.0043} at” | +0.0043 | 0.0043 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.24` |
| `R1.supp-app-seeds.25` | +0.0027 — “on the mean single-model AUC, it is $+0.0027$ \ci{-0.0080}{+0.0135},” | +0.0027 | 0.0027 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.25` |
| `R1.supp-app-seeds.26` | -0.0080 — “on the mean single-model AUC, it is $+0.0027$ \ci{-0.0080}{+0.0135},” | -0.0080 | -0.0080 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.26` |
| `R1.supp-app-seeds.27` | +0.0135 — “on the mean single-model AUC, it is $+0.0027$ \ci{-0.0080}{+0.0135},” | +0.0135 | 0.0135 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.27` |
| `R1.supp-app-seeds.28` | 0.60 — “$p = 0.60$, at c40 and $+0.0001$ \ci{-0.0081}{+0.0077}, $p = 0.96$, at” | 0.60 | 0.6044 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.28` |
| `R1.supp-app-seeds.29` | +0.0001 — “$p = 0.60$, at c40 and $+0.0001$ \ci{-0.0081}{+0.0077}, $p = 0.96$, at” | +0.0001 | 0.0001 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.29` |
| `R1.supp-app-seeds.30` | -0.0081 — “$p = 0.60$, at c40 and $+0.0001$ \ci{-0.0081}{+0.0077}, $p = 0.96$, at” | -0.0081 | -0.0081 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.30` |
| `R1.supp-app-seeds.31` | +0.0077 — “$p = 0.60$, at c40 and $+0.0001$ \ci{-0.0081}{+0.0077}, $p = 0.96$, at” | +0.0077 | 0.0077 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.31` |
| `R1.supp-app-seeds.32` | 0.96 — “$p = 0.60$, at c40 and $+0.0001$ \ci{-0.0081}{+0.0077}, $p = 0.96$, at” | 0.96 | 0.9646 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.32` |
| `R1.supp-app-seeds.33` | -0.0081 — “$-0.0081$ to $-0.0068$ at its lower end and from $+0.0130$ to $+0.0141$ at its” | -0.0081 | -0.0081 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.33` |
| `R1.supp-app-seeds.34` | -0.0068 — “$-0.0081$ to $-0.0068$ at its lower end and from $+0.0130$ to $+0.0141$ at its” | -0.0068 | -0.0068 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.34` |
| `R1.supp-app-seeds.35` | +0.0130 — “$-0.0081$ to $-0.0068$ at its lower end and from $+0.0130$ to $+0.0141$ at its” | +0.0130 | 0.0130 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.35` |
| `R1.supp-app-seeds.36` | +0.0141 — “$-0.0081$ to $-0.0068$ at its lower end and from $+0.0130$ to $+0.0141$ at its” | +0.0141 | 0.0141 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.36` |
| `R1.supp-app-seeds.37` | 0.58 — “upper end ($p \ge 0.58$). All include 0.” | 0.58 | 0.5808 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-seeds.37` |

## R1.supp-The-published-frequency-architectures-on-CAFRL — Revision 1 — Supplementary Material, §“The published frequency architectures, on CAFRL'”

*Supplementary Material, §“The published frequency architectures, on CAFRL'”*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-The-published-frequency-architectures-on-CAFRL.1` | -0.0039 — “\item \textbf{F3-Net-mq $-$ SpatialBase} at c40 $= -0.0039$,” | -0.0039 | -0.0039 | `verify/expected.json` +2 | `python verify/claim.py R1.supp-The-published-frequency-architectures-on-CAFRL.1 --bootstrap` |
| `R1.supp-The-published-frequency-architectures-on-CAFRL.2` | -0.0001 — “95\% CI \ci{-0.0151}{+0.0068}; at \auccomp{} $= -0.0001$,” | -0.0001 | -0.0001 | `verify/expected.json` +2 | `python verify/claim.py R1.supp-The-published-frequency-architectures-on-CAFRL.2 --bootstrap` |
| `R1.supp-The-published-frequency-architectures-on-CAFRL.3` | -0.0803 — “\item \textbf{FreqNet-mq $-$ SpatialBase} at c40 $= -0.0803$,” | -0.0803 | -0.0803 | `verify/expected.json` +2 | `python verify/claim.py R1.supp-The-published-frequency-architectures-on-CAFRL.3 --bootstrap` |
| `R1.supp-The-published-frequency-architectures-on-CAFRL.4` | -0.0492 — “\ci{-0.1084}{-0.0543}; at \auccomp{} $= -0.0492$, \ci{-0.0671}{-0.0330}.” | -0.0492 | -0.0492 | `verify/expected.json` +2 | `python verify/claim.py R1.supp-The-published-frequency-architectures-on-CAFRL.4 --bootstrap` |

## R1.supp-Protocol — Revision 1 — Supplementary Material, §“Protocol”

*Supplementary Material, §“Protocol”*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-Protocol.1` | 0.5 — “against the 0.5-point spread the same arm shows at FF++ c40. Out of” | 0.5 | 0.4974 | `predictions/ffpp/f1_none_fair_s42.json` +1 | `python verify/claim.py R1.supp-Protocol.1` |

- `R1.supp-Protocol.1` — Fair-N's spread over its three seeds at FF++ c40 (Table S1: .9586 / .9567 / .9536), max (seed 42) minus min (seed 2)

## R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28 — Revision 1 — Supplementary Material, §“Unseen manipulation (FaceShifter, held out; n=28”

*Supplementary Material, §“Unseen manipulation (FaceShifter, held out; n=28”*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.1` | -0.0317 — “$-0.0325$, CI \ci{-0.0545}{-0.0114}; Fair-W pool $-$ SpatialBase pool $-0.0317$, CI” | -0.0317 | -0.0317 | `verify/expected.json` +6 | `python verify/claim.py R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.1 --bootstrap` |
| `R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.2` | +0.0222 — “(Fair-N s42 $+0.0222$, CI \ci{-0.0062}{+0.0508}; Fair-W s42 $-0.0226$, CI” | +0.0222 | 0.0222 | `verify/expected.json` +4 | `python verify/claim.py R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.2 --bootstrap` |
| `R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.3` | -0.0226 — “(Fair-N s42 $+0.0222$, CI \ci{-0.0062}{+0.0508}; Fair-W s42 $-0.0226$, CI” | -0.0226 | -0.0226 | `verify/expected.json` +4 | `python verify/claim.py R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.3 --bootstrap` |
| `R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.4` | -0.0209 — “pooled deficits read Fair-N $-0.0209$, CI \ci{-0.0809}{+0.0361}, $p = 0.49$,” | -0.0209 | -0.0209 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.4` |
| `R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.5` | -0.0809 — “pooled deficits read Fair-N $-0.0209$, CI \ci{-0.0809}{+0.0361}, $p = 0.49$,” | -0.0809 | -0.0809 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.5` |
| `R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.6` | +0.0361 — “pooled deficits read Fair-N $-0.0209$, CI \ci{-0.0809}{+0.0361}, $p = 0.49$,” | +0.0361 | 0.0361 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.6` |
| `R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.7` | 0.49 — “pooled deficits read Fair-N $-0.0209$, CI \ci{-0.0809}{+0.0361}, $p = 0.49$,” | 0.49 | 0.4859 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.7` |
| `R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.8` | -0.0246 — “and Fair-W $-0.0246$, CI \ci{-0.0739}{+0.0177}, $p = 0.28$; the single-seed” | -0.0246 | -0.0246 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.8` |
| `R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.9` | -0.0739 — “and Fair-W $-0.0246$, CI \ci{-0.0739}{+0.0177}, $p = 0.28$; the single-seed” | -0.0739 | -0.0739 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.9` |
| `R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.10` | +0.0177 — “and Fair-W $-0.0246$, CI \ci{-0.0739}{+0.0177}, $p = 0.28$; the single-seed” | +0.0177 | 0.0177 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.10` |
| `R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.11` | 0.28 — “and Fair-W $-0.0246$, CI \ci{-0.0739}{+0.0177}, $p = 0.28$; the single-seed” | 0.28 | 0.2795 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.11` |
| `R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.12` | +0.0333 — “leans read Fair-N s42 $+0.0333$, CI \ci{+0.0012}{+0.0661}, $p = 0.042$” | +0.0333 | 0.0333 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.12` |
| `R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.13` | +0.0012 — “leans read Fair-N s42 $+0.0333$, CI \ci{+0.0012}{+0.0661}, $p = 0.042$” | +0.0012 | 0.0012 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.13` |
| `R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.14` | +0.0661 — “leans read Fair-N s42 $+0.0333$, CI \ci{+0.0012}{+0.0661}, $p = 0.042$” | +0.0661 | 0.0661 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.14` |
| `R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.15` | 0.042 — “leans read Fair-N s42 $+0.0333$, CI \ci{+0.0012}{+0.0661}, $p = 0.042$” | 0.042 | 0.0425 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.15` |
| `R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.16` | 0.38 — “(Holm-adjusted $0.38$), an interval that excludes 0, and Fair-W s42” | 0.38 | 0.3825 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.16` |
| `R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.17` | -0.0115 — “$-0.0115$, CI \ci{-0.0479}{+0.0246}, $p = 0.51$. Both findings are reported” | -0.0115 | -0.0115 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.17` |
| `R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.18` | -0.0479 — “$-0.0115$, CI \ci{-0.0479}{+0.0246}, $p = 0.51$. Both findings are reported” | -0.0479 | -0.0479 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.18` |
| `R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.19` | +0.0246 — “$-0.0115$, CI \ci{-0.0479}{+0.0246}, $p = 0.51$. Both findings are reported” | +0.0246 | 0.0246 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.19` |
| `R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.20` | 0.51 — “$-0.0115$, CI \ci{-0.0479}{+0.0246}, $p = 0.51$. Both findings are reported” | 0.51 | 0.5128 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Unseen-manipulation-FaceShifter-held-out-n-28.20` |

## R1.supp-tab-appfaceshifter — Revision 1 — Supplementary Material, tab:appfaceshifter

*Supplementary Material, tab:appfaceshifter; `\label{tab:appfaceshifter}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-tab-appfaceshifter.1` | 10,000 — “come from the 10,000-replicate paired video bootstrap on those scores, so {\mathversion{no” | 10000 | 10000.00 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-tab-appfaceshifter.1` |
| `R1.supp-tab-appfaceshifter.2` | 0.8216 — “c23 & 0.8216 & 0.8230 & $-0.0080$ & \ci{-0.041}{+0.025} & 0.30 \\” | 0.8216 | 0.8216 | `predictions/faceshifter/a0.json` +2 | `python verify/claim.py R1.supp-tab-appfaceshifter.2` |
| `R1.supp-tab-appfaceshifter.3` | 0.8230 — “c23 & 0.8216 & 0.8230 & $-0.0080$ & \ci{-0.041}{+0.025} & 0.30 \\” | 0.8230 | 0.8230 | `predictions/faceshifter/b7_effnet_b0_mq_fliponly.json` +2 | `python verify/claim.py R1.supp-tab-appfaceshifter.3` |
| `R1.supp-tab-appfaceshifter.4` | -0.0080 — “c23 & 0.8216 & 0.8230 & $-0.0080$ & \ci{-0.041}{+0.025} & 0.30 \\” | -0.0080 | -0.0080 | `verify/expected.json` +6 | `python verify/claim.py R1.supp-tab-appfaceshifter.4 --bootstrap` |
| `R1.supp-tab-appfaceshifter.5` | 0.7575 — “c40 & 0.7575 & 0.7318 & $+0.0221$ & \ci{-0.021}{+0.064} & 0.84 \\” | 0.7575 | 0.7575 | `predictions/faceshifter/a0.json` +2 | `python verify/claim.py R1.supp-tab-appfaceshifter.5` |
| `R1.supp-tab-appfaceshifter.6` | 0.7318 — “c40 & 0.7575 & 0.7318 & $+0.0221$ & \ci{-0.021}{+0.064} & 0.84 \\” | 0.7318 | 0.7318 | `predictions/faceshifter/b7_effnet_b0_mq_fliponly.json` +2 | `python verify/claim.py R1.supp-tab-appfaceshifter.6` |
| `R1.supp-tab-appfaceshifter.7` | +0.0221 — “c40 & 0.7575 & 0.7318 & $+0.0221$ & \ci{-0.021}{+0.064} & 0.84 \\” | +0.0221 | 0.0221 | `verify/expected.json` +6 | `python verify/claim.py R1.supp-tab-appfaceshifter.7 --bootstrap` |

- `R1.supp-tab-appfaceshifter.2` — post hoc re-evaluation, EMA weights (predictions/faceshifter/, evaluation set faceshifter_shipped_posthoc)
- `R1.supp-tab-appfaceshifter.5` — post hoc re-evaluation, EMA weights

## R1.supp-tab-appclusters — Revision 1 — Supplementary Material, tab:appclusters

*Supplementary Material, tab:appclusters; `\label{tab:appclusters}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-tab-appclusters.1` | -0.0009 — “Fair-N pool $-$ SpatialBase pool (3v3) & $-0.0009$ & \ci{-0.0066}{+0.0045} & \ci{-0.0064}{” | -0.0009 | -0.0009 | `verify/expected.json` +6 | `python verify/claim.py R1.supp-tab-appclusters.1 --bootstrap` |
| `R1.supp-tab-appclusters.2` | +0.0489 — “TrunkCtrl pool $-$ spatial-residual (s42) & $+0.0489$ & \ci{+0.0294}{+0.0705} & \ci{+0.029” | +0.0489 | 0.0489 | `verify/expected.json` +4 | `python verify/claim.py R1.supp-tab-appclusters.2 --bootstrap` |
| `R1.supp-tab-appclusters.3` | -0.0317 — “Fair-W pool $-$ SpatialBase pool & $-0.0317$ & \ci{-0.0575}{-0.0065} & \ci{-0.0563}{-0.007” | -0.0317 | -0.0317 | `verify/expected.json` +6 | `python verify/claim.py R1.supp-tab-appclusters.3 --bootstrap` |

## R1.supp-Conditioning-on-the-seeds — Revision 1 — Supplementary Material, §“Conditioning on the seeds”

*Supplementary Material, §“Conditioning on the seeds”*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-Conditioning-on-the-seeds.1` | -0.0002 — “$-0.0002$, CI \ci{-0.0105}{+0.0112}, $p = 0.95$, and Fair-W $-$ SpatialBase” | -0.0002 | -0.0002 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Conditioning-on-the-seeds.1` |
| `R1.supp-Conditioning-on-the-seeds.2` | -0.0105 — “$-0.0002$, CI \ci{-0.0105}{+0.0112}, $p = 0.95$, and Fair-W $-$ SpatialBase” | -0.0105 | -0.0105 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Conditioning-on-the-seeds.2` |
| `R1.supp-Conditioning-on-the-seeds.3` | +0.0112 — “$-0.0002$, CI \ci{-0.0105}{+0.0112}, $p = 0.95$, and Fair-W $-$ SpatialBase” | +0.0112 | 0.0112 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Conditioning-on-the-seeds.3` |
| `R1.supp-Conditioning-on-the-seeds.4` | 0.95 — “$-0.0002$, CI \ci{-0.0105}{+0.0112}, $p = 0.95$, and Fair-W $-$ SpatialBase” | 0.95 | 0.9486 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Conditioning-on-the-seeds.4` |
| `R1.supp-Conditioning-on-the-seeds.5` | +0.0053 — “$+0.0053$, CI \ci{-0.0042}{+0.0171}, $p = 0.29$. It also moves the two” | +0.0053 | 0.0053 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Conditioning-on-the-seeds.5` |
| `R1.supp-Conditioning-on-the-seeds.6` | -0.0042 — “$+0.0053$, CI \ci{-0.0042}{+0.0171}, $p = 0.29$. It also moves the two” | -0.0042 | -0.0042 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Conditioning-on-the-seeds.6` |
| `R1.supp-Conditioning-on-the-seeds.7` | +0.0171 — “$+0.0053$, CI \ci{-0.0042}{+0.0171}, $p = 0.29$. It also moves the two” | +0.0171 | 0.0171 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Conditioning-on-the-seeds.7` |
| `R1.supp-Conditioning-on-the-seeds.8` | 0.29 — “$+0.0053$, CI \ci{-0.0042}{+0.0171}, $p = 0.29$. It also moves the two” | 0.29 | 0.2897 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Conditioning-on-the-seeds.8` |
| `R1.supp-Conditioning-on-the-seeds.9` | +0.0054 — “$-$ TrunkCtrl pool becomes $+0.0054$, CI \ci{-0.0040}{+0.0156}, $p = 0.27$,” | +0.0054 | 0.0054 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Conditioning-on-the-seeds.9` |
| `R1.supp-Conditioning-on-the-seeds.10` | -0.0040 — “$-$ TrunkCtrl pool becomes $+0.0054$, CI \ci{-0.0040}{+0.0156}, $p = 0.27$,” | -0.0040 | -0.0040 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Conditioning-on-the-seeds.10` |
| `R1.supp-Conditioning-on-the-seeds.11` | +0.0156 — “$-$ TrunkCtrl pool becomes $+0.0054$, CI \ci{-0.0040}{+0.0156}, $p = 0.27$,” | +0.0156 | 0.0156 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Conditioning-on-the-seeds.11` |
| `R1.supp-Conditioning-on-the-seeds.12` | 0.27 — “$-$ TrunkCtrl pool becomes $+0.0054$, CI \ci{-0.0040}{+0.0156}, $p = 0.27$,” | 0.27 | 0.2699 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Conditioning-on-the-seeds.12` |
| `R1.supp-Conditioning-on-the-seeds.13` | -0.0038 — “the opposite sign to the published $-0.0038$, and TrunkCtrl pool $-$” | -0.0038 | -0.0038 | `verify/expected.json` +4 | `python verify/claim.py R1.supp-Conditioning-on-the-seeds.13 --bootstrap` |
| `R1.supp-Conditioning-on-the-seeds.14` | +0.0397 — “spatial-residual (s42) becomes $+0.0397$, CI \ci{+0.0196}{+0.0625},” | +0.0397 | 0.0397 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Conditioning-on-the-seeds.14` |
| `R1.supp-Conditioning-on-the-seeds.15` | +0.0196 — “spatial-residual (s42) becomes $+0.0397$, CI \ci{+0.0196}{+0.0625},” | +0.0196 | 0.0196 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Conditioning-on-the-seeds.15` |
| `R1.supp-Conditioning-on-the-seeds.16` | +0.0625 — “spatial-residual (s42) becomes $+0.0397$, CI \ci{+0.0196}{+0.0625},” | +0.0625 | 0.0625 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Conditioning-on-the-seeds.16` |
| `R1.supp-Conditioning-on-the-seeds.17` | +0.0489 — “$p<1.0\times10^{-4}$, against the $+0.0489$ of” | +0.0489 | 0.0489 | `verify/expected.json` +4 | `python verify/claim.py R1.supp-Conditioning-on-the-seeds.17 --bootstrap` |

## R1.supp-Equivalence — Revision 1 — Supplementary Material, §“Equivalence”

*Supplementary Material, §“Equivalence”*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-Equivalence.1` | +0.0054 — “post hoc primary reading ($+0.0054$, \ci{-0.0040}{+0.0156}). An” | +0.0054 | 0.0054 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Equivalence.1` |
| `R1.supp-Equivalence.2` | -0.0040 — “post hoc primary reading ($+0.0054$, \ci{-0.0040}{+0.0156}). An” | -0.0040 | -0.0040 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Equivalence.2` |
| `R1.supp-Equivalence.3` | +0.0156 — “post hoc primary reading ($+0.0054$, \ci{-0.0040}{+0.0156}). An” | +0.0156 | 0.0156 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Equivalence.3` |
| `R1.supp-Equivalence.4` | 4.2\times10^{-3} — “$\alpha/12 = 4.2\times10^{-3}$, which Fair-N's $0.001$ clears and” | 4.2e-3 | 0.0042 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Equivalence.4` |
| `R1.supp-Equivalence.5` | +1.71 — “the Fair-W interval reaches $+1.64$\,pt ($+1.71$\,pt under the post hoc” | +1.71 | 1.7083 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Equivalence.5` |

## R1.supp-Multiplicity — Revision 1 — Supplementary Material, §“Multiplicity”

*Supplementary Material, §“Multiplicity”*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-Multiplicity.1` | 10,000 — “the bootstrap's own achieved significance level saturates at $1/B$ ($B = 10{,}000$ replica” | 10000 | 10000.00 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Multiplicity.1` |
| `R1.supp-Multiplicity.2` | 4.5 — “($z \approx 3.7$ to $4.5$) nothing turns on the approximation; for the borderline rows ---” | 4.5 | 4.5435 | `evaluation/analysis/multiplicity.json` | `python verify/claim.py R1.supp-Multiplicity.2` |
| `R1.supp-Multiplicity.3` | 4.2\times10^{-3} — “Bonferroni threshold is $\alpha/12 = 4.2\times10^{-3}$, and the three” | 4.2e-3 | 0.0042 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Multiplicity.3` |
| `R1.supp-Multiplicity.4` | 5.0\times10^{-4} — “survive: SpatialBase $-$ CAFRL as specified ($p = 5.0\times10^{-4}$, Holm” | 5.0e-4 | 0.0005 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Multiplicity.4` |
| `R1.supp-Multiplicity.5` | 5.0\times10^{-3} — “$5.0\times10^{-3}$), Fair-N $-$ (CAFRL$-$adv) and TrunkCtrl pool $-$” | 5.0e-3 | 0.0050 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Multiplicity.5` |
| `R1.supp-Multiplicity.6` | 1.2\times10^{-3} — “spatial-residual (both $p<1.0\times10^{-4}$, Holm $1.2\times10^{-3}$); Fair-N” | 1.2e-3 | 0.0012 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Multiplicity.6` |
| `R1.supp-Multiplicity.7` | 0.042 — “($p = 0.042$), has Holm $0.38$. With the seeds fixed and the source-identity” | 0.042 | 0.0425 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Multiplicity.7` |
| `R1.supp-Multiplicity.8` | 0.38 — “($p = 0.042$), has Holm $0.38$. With the seeds fixed and the source-identity” | 0.38 | 0.3825 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Multiplicity.8` |
| `R1.supp-Multiplicity.9` | 4.1\times10^{-3} — “FaceShifter deficit ($p = 4.1\times10^{-3}$, Holm $0.037$), while Fair-W's” | 4.1e-3 | 0.0041 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Multiplicity.9` |
| `R1.supp-Multiplicity.10` | 0.037 — “FaceShifter deficit ($p = 4.1\times10^{-3}$, Holm $0.037$), while Fair-W's” | 0.037 | 0.0369 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Multiplicity.10` |
| `R1.supp-Multiplicity.11` | 0.011 — “does not ($p = 0.011$, Holm $0.089$); we report both FaceShifter deficits as” | 0.011 | 0.0111 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Multiplicity.11` |
| `R1.supp-Multiplicity.12` | 0.089 — “does not ($p = 0.011$, Holm $0.089$); we report both FaceShifter deficits as” | 0.089 | 0.0888 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-Multiplicity.12` |

## R1.supp-tab-appcampaignarms — Revision 1 — Supplementary Material, tab:appcampaignarms

*Supplementary Material, tab:appcampaignarms; `\label{tab:appcampaignarms}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-tab-appcampaignarms.1` | 98.26 — “E1 (EMA) & 98.26 & 97.84 & 97.31 & \textbf{96.50} & 96.17 / 96.81 / 96.51 & 97.11 \\” | 98.26 | 98.26 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.1` |
| `R1.supp-tab-appcampaignarms.2` | 97.84 — “E1 (EMA) & 98.26 & 97.84 & 97.31 & \textbf{96.50} & 96.17 / 96.81 / 96.51 & 97.11 \\” | 97.84 | 97.84 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.2` |
| `R1.supp-tab-appcampaignarms.3` | 97.31 — “E1 (EMA) & 98.26 & 97.84 & 97.31 & \textbf{96.50} & 96.17 / 96.81 / 96.51 & 97.11 \\” | 97.31 | 97.31 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.3` |
| `R1.supp-tab-appcampaignarms.4` | 96.50 — “E1 (EMA) & 98.26 & 97.84 & 97.31 & \textbf{96.50} & 96.17 / 96.81 / 96.51 & 97.11 \\” | 96.50 | 96.50 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.4` |
| `R1.supp-tab-appcampaignarms.5` | 96.17 — “E1 (EMA) & 98.26 & 97.84 & 97.31 & \textbf{96.50} & 96.17 / 96.81 / 96.51 & 97.11 \\” | 96.17 | 96.17 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.5` |
| `R1.supp-tab-appcampaignarms.6` | 96.81 — “E1 (EMA) & 98.26 & 97.84 & 97.31 & \textbf{96.50} & 96.17 / 96.81 / 96.51 & 97.11 \\” | 96.81 | 96.81 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.6` |
| `R1.supp-tab-appcampaignarms.7` | 96.51 — “E1 (EMA) & 98.26 & 97.84 & 97.31 & \textbf{96.50} & 96.17 / 96.81 / 96.51 & 97.11 \\” | 96.51 | 96.51 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.7` |
| `R1.supp-tab-appcampaignarms.8` | 97.11 — “E1 (EMA) & 98.26 & 97.84 & 97.31 & \textbf{96.50} & 96.17 / 96.81 / 96.51 & 97.11 \\” | 97.11 | 97.11 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.8` |
| `R1.supp-tab-appcampaignarms.9` | 97.68 — “Fair-N (EMA) & 97.68 & 97.23 & 96.44 & \textbf{95.63} & 95.86 / 95.67 / 95.36 & 96.42 \\” | 97.68 | 97.68 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.9` |
| `R1.supp-tab-appcampaignarms.10` | 97.23 — “Fair-N (EMA) & 97.68 & 97.23 & 96.44 & \textbf{95.63} & 95.86 / 95.67 / 95.36 & 96.42 \\” | 97.23 | 97.23 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.10` |
| `R1.supp-tab-appcampaignarms.11` | 96.44 — “Fair-N (EMA) & 97.68 & 97.23 & 96.44 & \textbf{95.63} & 95.86 / 95.67 / 95.36 & 96.42 \\” | 96.44 | 96.44 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.11` |
| `R1.supp-tab-appcampaignarms.12` | 95.63 — “Fair-N (EMA) & 97.68 & 97.23 & 96.44 & \textbf{95.63} & 95.86 / 95.67 / 95.36 & 96.42 \\” | 95.63 | 95.63 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.12` |
| `R1.supp-tab-appcampaignarms.13` | 95.86 — “Fair-N (EMA) & 97.68 & 97.23 & 96.44 & \textbf{95.63} & 95.86 / 95.67 / 95.36 & 96.42 \\” | 95.86 | 95.86 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.13` |
| `R1.supp-tab-appcampaignarms.14` | 95.67 — “Fair-N (EMA) & 97.68 & 97.23 & 96.44 & \textbf{95.63} & 95.86 / 95.67 / 95.36 & 96.42 \\” | 95.67 | 95.67 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.14` |
| `R1.supp-tab-appcampaignarms.15` | 95.36 — “Fair-N (EMA) & 97.68 & 97.23 & 96.44 & \textbf{95.63} & 95.86 / 95.67 / 95.36 & 96.42 \\” | 95.36 | 95.36 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.15` |
| `R1.supp-tab-appcampaignarms.16` | 96.42 — “Fair-N (EMA) & 97.68 & 97.23 & 96.44 & \textbf{95.63} & 95.86 / 95.67 / 95.36 & 96.42 \\” | 96.42 | 96.42 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.16` |
| `R1.supp-tab-appcampaignarms.17` | 97.99 — “SpatialBase (raw) & 97.99 & 97.41 & 96.48 & \textbf{95.65} & 95.90 / 96.14 / 94.92 & 96.51” | 97.99 | 97.99 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.17` |
| `R1.supp-tab-appcampaignarms.18` | 97.41 — “SpatialBase (raw) & 97.99 & 97.41 & 96.48 & \textbf{95.65} & 95.90 / 96.14 / 94.92 & 96.51” | 97.41 | 97.41 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.18` |
| `R1.supp-tab-appcampaignarms.19` | 96.48 — “SpatialBase (raw) & 97.99 & 97.41 & 96.48 & \textbf{95.65} & 95.90 / 96.14 / 94.92 & 96.51” | 96.48 | 96.48 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.19` |
| `R1.supp-tab-appcampaignarms.20` | 95.65 — “SpatialBase (raw) & 97.99 & 97.41 & 96.48 & \textbf{95.65} & 95.90 / 96.14 / 94.92 & 96.51” | 95.65 | 95.65 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.20` |
| `R1.supp-tab-appcampaignarms.21` | 95.90 — “SpatialBase (raw) & 97.99 & 97.41 & 96.48 & \textbf{95.65} & 95.90 / 96.14 / 94.92 & 96.51” | 95.90 | 95.90 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.21` |
| `R1.supp-tab-appcampaignarms.22` | 96.14 — “SpatialBase (raw) & 97.99 & 97.41 & 96.48 & \textbf{95.65} & 95.90 / 96.14 / 94.92 & 96.51” | 96.14 | 96.14 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.22` |
| `R1.supp-tab-appcampaignarms.23` | 94.92 — “SpatialBase (raw) & 97.99 & 97.41 & 96.48 & \textbf{95.65} & 95.90 / 96.14 / 94.92 & 96.51” | 94.92 | 94.92 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.23` |
| `R1.supp-tab-appcampaignarms.24` | 96.51 — “SpatialBase (raw) & 97.99 & 97.41 & 96.48 & \textbf{95.65} & 95.90 / 96.14 / 94.92 & 96.51” | 96.51 | 96.51 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.24` |
| `R1.supp-tab-appcampaignarms.25` | 98.36 — “E2a (raw) & 98.36 & 97.85 & 97.17 & \textbf{94.53} & 94.09 / 94.60 / 94.90 & 95.33 \\” | 98.36 | 98.36 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.25` |
| `R1.supp-tab-appcampaignarms.26` | 97.85 — “E2a (raw) & 98.36 & 97.85 & 97.17 & \textbf{94.53} & 94.09 / 94.60 / 94.90 & 95.33 \\” | 97.85 | 97.85 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.26` |
| `R1.supp-tab-appcampaignarms.27` | 97.17 — “E2a (raw) & 98.36 & 97.85 & 97.17 & \textbf{94.53} & 94.09 / 94.60 / 94.90 & 95.33 \\” | 97.17 | 97.17 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.27` |
| `R1.supp-tab-appcampaignarms.28` | 94.53 — “E2a (raw) & 98.36 & 97.85 & 97.17 & \textbf{94.53} & 94.09 / 94.60 / 94.90 & 95.33 \\” | 94.53 | 94.53 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.28` |
| `R1.supp-tab-appcampaignarms.29` | 94.09 — “E2a (raw) & 98.36 & 97.85 & 97.17 & \textbf{94.53} & 94.09 / 94.60 / 94.90 & 95.33 \\” | 94.09 | 94.09 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.29` |
| `R1.supp-tab-appcampaignarms.30` | 94.60 — “E2a (raw) & 98.36 & 97.85 & 97.17 & \textbf{94.53} & 94.09 / 94.60 / 94.90 & 95.33 \\” | 94.60 | 94.60 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.30` |
| `R1.supp-tab-appcampaignarms.31` | 94.90 — “E2a (raw) & 98.36 & 97.85 & 97.17 & \textbf{94.53} & 94.09 / 94.60 / 94.90 & 95.33 \\” | 94.90 | 94.90 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.31` |
| `R1.supp-tab-appcampaignarms.32` | 95.33 — “E2a (raw) & 98.36 & 97.85 & 97.17 & \textbf{94.53} & 94.09 / 94.60 / 94.90 & 95.33 \\” | 95.33 | 95.33 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.32` |
| `R1.supp-tab-appcampaignarms.33` | 98.62 — “anchor (raw) & 98.62 & 97.12 & 93.00 & \textbf{85.90} & 86.65 / 85.72 / 85.35 & 87.31 \\” | 98.62 | 98.62 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.33` |
| `R1.supp-tab-appcampaignarms.34` | 97.12 — “anchor (raw) & 98.62 & 97.12 & 93.00 & \textbf{85.90} & 86.65 / 85.72 / 85.35 & 87.31 \\” | 97.12 | 97.12 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.34` |
| `R1.supp-tab-appcampaignarms.35` | 93.00 — “anchor (raw) & 98.62 & 97.12 & 93.00 & \textbf{85.90} & 86.65 / 85.72 / 85.35 & 87.31 \\” | 93.00 | 93.00 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.35` |
| `R1.supp-tab-appcampaignarms.36` | 85.90 — “anchor (raw) & 98.62 & 97.12 & 93.00 & \textbf{85.90} & 86.65 / 85.72 / 85.35 & 87.31 \\” | 85.90 | 85.90 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.36` |
| `R1.supp-tab-appcampaignarms.37` | 86.65 — “anchor (raw) & 98.62 & 97.12 & 93.00 & \textbf{85.90} & 86.65 / 85.72 / 85.35 & 87.31 \\” | 86.65 | 86.65 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.37` |
| `R1.supp-tab-appcampaignarms.38` | 85.72 — “anchor (raw) & 98.62 & 97.12 & 93.00 & \textbf{85.90} & 86.65 / 85.72 / 85.35 & 87.31 \\” | 85.72 | 85.72 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.38` |
| `R1.supp-tab-appcampaignarms.39` | 85.35 — “anchor (raw) & 98.62 & 97.12 & 93.00 & \textbf{85.90} & 86.65 / 85.72 / 85.35 & 87.31 \\” | 85.35 | 85.35 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.39` |
| `R1.supp-tab-appcampaignarms.40` | 87.31 — “anchor (raw) & 98.62 & 97.12 & 93.00 & \textbf{85.90} & 86.65 / 85.72 / 85.35 & 87.31 \\” | 87.31 | 87.31 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.40` |
| `R1.supp-tab-appcampaignarms.41` | 96.73 — “E3a (raw) & 96.73 & 94.88 & 92.54 & \textbf{88.93} & 88.89 / 89.25 / 88.66 & 90.17 \\” | 96.73 | 96.73 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.41` |
| `R1.supp-tab-appcampaignarms.42` | 94.88 — “E3a (raw) & 96.73 & 94.88 & 92.54 & \textbf{88.93} & 88.89 / 89.25 / 88.66 & 90.17 \\” | 94.88 | 94.88 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.42` |
| `R1.supp-tab-appcampaignarms.43` | 92.54 — “E3a (raw) & 96.73 & 94.88 & 92.54 & \textbf{88.93} & 88.89 / 89.25 / 88.66 & 90.17 \\” | 92.54 | 92.54 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.43` |
| `R1.supp-tab-appcampaignarms.44` | 88.93 — “E3a (raw) & 96.73 & 94.88 & 92.54 & \textbf{88.93} & 88.89 / 89.25 / 88.66 & 90.17 \\” | 88.93 | 88.93 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.44` |
| `R1.supp-tab-appcampaignarms.45` | 88.89 — “E3a (raw) & 96.73 & 94.88 & 92.54 & \textbf{88.93} & 88.89 / 89.25 / 88.66 & 90.17 \\” | 88.89 | 88.89 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.45` |
| `R1.supp-tab-appcampaignarms.46` | 89.25 — “E3a (raw) & 96.73 & 94.88 & 92.54 & \textbf{88.93} & 88.89 / 89.25 / 88.66 & 90.17 \\” | 89.25 | 89.25 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.46` |
| `R1.supp-tab-appcampaignarms.47` | 88.66 — “E3a (raw) & 96.73 & 94.88 & 92.54 & \textbf{88.93} & 88.89 / 89.25 / 88.66 & 90.17 \\” | 88.66 | 88.66 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.47` |
| `R1.supp-tab-appcampaignarms.48` | 90.17 — “E3a (raw) & 96.73 & 94.88 & 92.54 & \textbf{88.93} & 88.89 / 89.25 / 88.66 & 90.17 \\” | 90.17 | 90.17 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.48` |
| `R1.supp-tab-appcampaignarms.49` | 96.52 — “E3b (raw) & 96.52 & 94.22 & 91.05 & \textbf{86.29} & 85.88 / 86.20 / 86.79 & 87.84 \\” | 96.52 | 96.52 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.49` |
| `R1.supp-tab-appcampaignarms.50` | 94.22 — “E3b (raw) & 96.52 & 94.22 & 91.05 & \textbf{86.29} & 85.88 / 86.20 / 86.79 & 87.84 \\” | 94.22 | 94.22 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.50` |
| `R1.supp-tab-appcampaignarms.51` | 91.05 — “E3b (raw) & 96.52 & 94.22 & 91.05 & \textbf{86.29} & 85.88 / 86.20 / 86.79 & 87.84 \\” | 91.05 | 91.05 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.51` |
| `R1.supp-tab-appcampaignarms.52` | 86.29 — “E3b (raw) & 96.52 & 94.22 & 91.05 & \textbf{86.29} & 85.88 / 86.20 / 86.79 & 87.84 \\” | 86.29 | 86.29 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.52` |
| `R1.supp-tab-appcampaignarms.53` | 85.88 — “E3b (raw) & 96.52 & 94.22 & 91.05 & \textbf{86.29} & 85.88 / 86.20 / 86.79 & 87.84 \\” | 85.88 | 85.88 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.53` |
| `R1.supp-tab-appcampaignarms.54` | 86.20 — “E3b (raw) & 96.52 & 94.22 & 91.05 & \textbf{86.29} & 85.88 / 86.20 / 86.79 & 87.84 \\” | 86.20 | 86.20 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.54` |
| `R1.supp-tab-appcampaignarms.55` | 86.79 — “E3b (raw) & 96.52 & 94.22 & 91.05 & \textbf{86.29} & 85.88 / 86.20 / 86.79 & 87.84 \\” | 86.79 | 86.79 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.55` |
| `R1.supp-tab-appcampaignarms.56` | 87.84 — “E3b (raw) & 96.52 & 94.22 & 91.05 & \textbf{86.29} & 85.88 / 86.20 / 86.79 & 87.84 \\” | 87.84 | 87.84 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignarms.56` |

## R1.supp-Secondary-analyses — Revision 1 — Supplementary Material, §“Secondary analyses”

*Supplementary Material, §“Secondary analyses”*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-Secondary-analyses.1` | 95.11 — “At c40, E2b's seeds scored 95.11 / 94.44 / 91.65, and at c36” | 95.11 | 95.11 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-Secondary-analyses.1` |
| `R1.supp-Secondary-analyses.2` | 94.44 — “At c40, E2b's seeds scored 95.11 / 94.44 / 91.65, and at c36” | 94.44 | 94.44 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-Secondary-analyses.2` |
| `R1.supp-Secondary-analyses.3` | 91.65 — “At c40, E2b's seeds scored 95.11 / 94.44 / 91.65, and at c36” | 91.65 | 91.65 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-Secondary-analyses.3` |
| `R1.supp-Secondary-analyses.4` | 97.96 — “97.96 / 97.76 / 96.19.” | 97.96 | 97.96 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-Secondary-analyses.4` |
| `R1.supp-Secondary-analyses.5` | 97.76 — “97.96 / 97.76 / 96.19.” | 97.76 | 97.76 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-Secondary-analyses.5` |
| `R1.supp-Secondary-analyses.6` | 96.19 — “97.96 / 97.76 / 96.19.” | 96.19 | 96.19 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-Secondary-analyses.6` |

## R1.supp-tab-appcampaignsec — Revision 1 — Supplementary Material, tab:appcampaignsec

*Supplementary Material, tab:appcampaignsec; `\label{tab:appcampaignsec}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-tab-appcampaignsec.1` | 10,000 — “($B = 10{,}000$; seeds, then 140 source-identity clusters). {\mathversion{normal}$\Delta$}” | 10000 | 10000.00 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.1` |
| `R1.supp-tab-appcampaignsec.2` | 0.87 — “T1: E1 $-$ Fair-N (c40) & 0.87 \ci{0.02}{1.88} & 0.70 \ci{-0.20}{1.93} \\” | 0.87 | 0.8678 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.2` |
| `R1.supp-tab-appcampaignsec.3` | 0.02 — “T1: E1 $-$ Fair-N (c40) & 0.87 \ci{0.02}{1.88} & 0.70 \ci{-0.20}{1.93} \\” | 0.02 | 0.0221 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.3` |
| `R1.supp-tab-appcampaignsec.4` | 1.88 — “T1: E1 $-$ Fair-N (c40) & 0.87 \ci{0.02}{1.88} & 0.70 \ci{-0.20}{1.93} \\” | 1.88 | 1.8767 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.4` |
| `R1.supp-tab-appcampaignsec.5` | 0.70 — “T1: E1 $-$ Fair-N (c40) & 0.87 \ci{0.02}{1.88} & 0.70 \ci{-0.20}{1.93} \\” | 0.70 | 0.6952 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.5` |
| `R1.supp-tab-appcampaignsec.6` | -0.20 — “T1: E1 $-$ Fair-N (c40) & 0.87 \ci{0.02}{1.88} & 0.70 \ci{-0.20}{1.93} \\” | -0.20 | -0.2041 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.6` |
| `R1.supp-tab-appcampaignsec.7` | 1.93 — “T1: E1 $-$ Fair-N (c40) & 0.87 \ci{0.02}{1.88} & 0.70 \ci{-0.20}{1.93} \\” | 1.93 | 1.9324 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.7` |
| `R1.supp-tab-appcampaignsec.8` | 0.73 — “T2: E1 $-$ Fair-N (\auccomp) & 0.73 \ci{0.12}{1.45} & 0.47 \ci{-0.14}{1.45} \\” | 0.73 | 0.7302 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.8` |
| `R1.supp-tab-appcampaignsec.9` | 0.12 — “T2: E1 $-$ Fair-N (\auccomp) & 0.73 \ci{0.12}{1.45} & 0.47 \ci{-0.14}{1.45} \\” | 0.12 | 0.1175 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.9` |
| `R1.supp-tab-appcampaignsec.10` | 1.45 — “T2: E1 $-$ Fair-N (\auccomp) & 0.73 \ci{0.12}{1.45} & 0.47 \ci{-0.14}{1.45} \\” | 1.45 | 1.4503 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.10` |
| `R1.supp-tab-appcampaignsec.11` | 0.47 — “T2: E1 $-$ Fair-N (\auccomp) & 0.73 \ci{0.12}{1.45} & 0.47 \ci{-0.14}{1.45} \\” | 0.47 | 0.4723 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.11` |
| `R1.supp-tab-appcampaignsec.12` | -0.14 — “T2: E1 $-$ Fair-N (\auccomp) & 0.73 \ci{0.12}{1.45} & 0.47 \ci{-0.14}{1.45} \\” | -0.14 | -0.1436 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.12` |
| `R1.supp-tab-appcampaignsec.13` | 0.88 — “T3: retention $R$ (c40) & 0.88 \ci{0.75}{1.03} & 0.87 \ci{0.72}{1.05} \\” | 0.88 | 0.8848 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.13` |
| `R1.supp-tab-appcampaignsec.14` | 0.75 — “T3: retention $R$ (c40) & 0.88 \ci{0.75}{1.03} & 0.87 \ci{0.72}{1.05} \\” | 0.75 | 0.7548 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.14` |
| `R1.supp-tab-appcampaignsec.15` | 1.03 — “T3: retention $R$ (c40) & 0.88 \ci{0.75}{1.03} & 0.87 \ci{0.72}{1.05} \\” | 1.03 | 1.0280 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.15` |
| `R1.supp-tab-appcampaignsec.16` | 0.87 — “T3: retention $R$ (c40) & 0.88 \ci{0.75}{1.03} & 0.87 \ci{0.72}{1.05} \\” | 0.87 | 0.8716 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.16` |
| `R1.supp-tab-appcampaignsec.17` | 0.72 — “T3: retention $R$ (c40) & 0.88 \ci{0.75}{1.03} & 0.87 \ci{0.72}{1.05} \\” | 0.72 | 0.7235 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.17` |
| `R1.supp-tab-appcampaignsec.18` | 1.05 — “T3: retention $R$ (c40) & 0.88 \ci{0.75}{1.03} & 0.87 \ci{0.72}{1.05} \\” | 1.05 | 1.0458 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.18` |
| `R1.supp-tab-appcampaignsec.19` | 7.48 — “T4: codec effect (c40) & 7.48 \ci{5.12}{9.94} & 6.92 \ci{4.66}{9.72} \\” | 7.48 | 7.4783 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.19` |
| `R1.supp-tab-appcampaignsec.20` | 5.12 — “T4: codec effect (c40) & 7.48 \ci{5.12}{9.94} & 6.92 \ci{4.66}{9.72} \\” | 5.12 | 5.1229 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.20` |
| `R1.supp-tab-appcampaignsec.21` | 9.94 — “T4: codec effect (c40) & 7.48 \ci{5.12}{9.94} & 6.92 \ci{4.66}{9.72} \\” | 9.94 | 9.9443 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.21` |
| `R1.supp-tab-appcampaignsec.22` | 6.92 — “T4: codec effect (c40) & 7.48 \ci{5.12}{9.94} & 6.92 \ci{4.66}{9.72} \\” | 6.92 | 6.9165 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.22` |
| `R1.supp-tab-appcampaignsec.23` | 4.66 — “T4: codec effect (c40) & 7.48 \ci{5.12}{9.94} & 6.92 \ci{4.66}{9.72} \\” | 4.66 | 4.6594 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.23` |
| `R1.supp-tab-appcampaignsec.24` | 9.72 — “T4: codec effect (c40) & 7.48 \ci{5.12}{9.94} & 6.92 \ci{4.66}{9.72} \\” | 9.72 | 9.7157 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.24` |
| `R1.supp-tab-appcampaignsec.25` | 1.88 — “T5: c40-exposure effect (c40) & 1.88 \ci{0.79}{2.98} & 1.75 \ci{0.50}{3.12} \\” | 1.88 | 1.8831 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.25` |
| `R1.supp-tab-appcampaignsec.26` | 0.79 — “T5: c40-exposure effect (c40) & 1.88 \ci{0.79}{2.98} & 1.75 \ci{0.50}{3.12} \\” | 0.79 | 0.7927 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.26` |
| `R1.supp-tab-appcampaignsec.27` | 2.98 — “T5: c40-exposure effect (c40) & 1.88 \ci{0.79}{2.98} & 1.75 \ci{0.50}{3.12} \\” | 2.98 | 2.9786 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.27` |
| `R1.supp-tab-appcampaignsec.28` | 1.75 — “T5: c40-exposure effect (c40) & 1.88 \ci{0.79}{2.98} & 1.75 \ci{0.50}{3.12} \\” | 1.75 | 1.7545 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.28` |
| `R1.supp-tab-appcampaignsec.29` | 0.50 — “T5: c40-exposure effect (c40) & 1.88 \ci{0.79}{2.98} & 1.75 \ci{0.50}{3.12} \\” | 0.50 | 0.4967 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.29` |
| `R1.supp-tab-appcampaignsec.30` | 3.12 — “T5: c40-exposure effect (c40) & 1.88 \ci{0.79}{2.98} & 1.75 \ci{0.50}{3.12} \\” | 3.12 | 3.1174 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.30` |
| `R1.supp-tab-appcampaignsec.31` | -1.52 — “$-1.52$ \ci{-3.59}{0.55} & $-1.15$ \ci{-3.69}{1.11} \\” | -1.52 | -1.5204 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.31` |
| `R1.supp-tab-appcampaignsec.32` | -3.59 — “$-1.52$ \ci{-3.59}{0.55} & $-1.15$ \ci{-3.69}{1.11} \\” | -3.59 | -3.5940 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.32` |
| `R1.supp-tab-appcampaignsec.33` | 0.55 — “$-1.52$ \ci{-3.59}{0.55} & $-1.15$ \ci{-3.69}{1.11} \\” | 0.55 | 0.5472 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.33` |
| `R1.supp-tab-appcampaignsec.34` | -1.15 — “$-1.52$ \ci{-3.59}{0.55} & $-1.15$ \ci{-3.69}{1.11} \\” | -1.15 | -1.1467 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.34` |
| `R1.supp-tab-appcampaignsec.35` | -3.69 — “$-1.52$ \ci{-3.59}{0.55} & $-1.15$ \ci{-3.69}{1.11} \\” | -3.69 | -3.6876 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.35` |
| `R1.supp-tab-appcampaignsec.36` | 1.11 — “$-1.52$ \ci{-3.59}{0.55} & $-1.15$ \ci{-3.69}{1.11} \\” | 1.11 | 1.1097 | `revision-1/stats/confirmatory.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.36` |
| `R1.supp-tab-appcampaignsec.37` | 0.94 — “T3: retention $R$ (c40) & 0.88 \ci{0.75}{1.03} & control: 0.94 \ci{0.79}{1.13} \\” | 0.94 | 0.9438 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.37` |
| `R1.supp-tab-appcampaignsec.38` | 0.79 — “T3: retention $R$ (c40) & 0.88 \ci{0.75}{1.03} & control: 0.94 \ci{0.79}{1.13} \\” | 0.79 | 0.7944 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.38` |
| `R1.supp-tab-appcampaignsec.39` | 1.13 — “T3: retention $R$ (c40) & 0.88 \ci{0.75}{1.03} & control: 0.94 \ci{0.79}{1.13} \\” | 1.13 | 1.1330 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.39` |
| `R1.supp-tab-appcampaignsec.40` | 1.58 — “T5: c40-exposure effect (c40) & 1.88 \ci{0.79}{2.98} & control: 1.58 \ci{0.38}{2.73} \\” | 1.58 | 1.5784 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.40` |
| `R1.supp-tab-appcampaignsec.41` | 0.38 — “T5: c40-exposure effect (c40) & 1.88 \ci{0.79}{2.98} & control: 1.58 \ci{0.38}{2.73} \\” | 0.38 | 0.3769 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.41` |
| `R1.supp-tab-appcampaignsec.42` | 2.73 — “T5: c40-exposure effect (c40) & 1.88 \ci{0.79}{2.98} & control: 1.58 \ci{0.38}{2.73} \\” | 2.73 | 2.7334 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.42` |
| `R1.supp-tab-appcampaignsec.43` | 93.73 — “E2b, AUC at c40 & 93.73 \ci{90.96}{96.03} & 95.30 \ci{91.85}{96.75} \\” | 93.73 | 93.73 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.43` |
| `R1.supp-tab-appcampaignsec.44` | 90.96 — “E2b, AUC at c40 & 93.73 \ci{90.96}{96.03} & 95.30 \ci{91.85}{96.75} \\” | 90.96 | 90.96 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.44` |
| `R1.supp-tab-appcampaignsec.45` | 96.03 — “E2b, AUC at c40 & 93.73 \ci{90.96}{96.03} & 95.30 \ci{91.85}{96.75} \\” | 96.03 | 96.03 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.45` |
| `R1.supp-tab-appcampaignsec.46` | 95.30 — “E2b, AUC at c40 & 93.73 \ci{90.96}{96.03} & 95.30 \ci{91.85}{96.75} \\” | 95.30 | 95.30 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.46` |
| `R1.supp-tab-appcampaignsec.47` | 91.85 — “E2b, AUC at c40 & 93.73 \ci{90.96}{96.03} & 95.30 \ci{91.85}{96.75} \\” | 91.85 | 91.85 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.47` |
| `R1.supp-tab-appcampaignsec.48` | 96.75 — “E2b, AUC at c40 & 93.73 \ci{90.96}{96.03} & 95.30 \ci{91.85}{96.75} \\” | 96.75 | 96.75 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.48` |
| `R1.supp-tab-appcampaignsec.49` | 97.30 — “E2b, AUC at c36 & 97.30 \ci{95.66}{98.55} & 98.01 \ci{96.18}{98.85} \\” | 97.30 | 97.30 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.49` |
| `R1.supp-tab-appcampaignsec.50` | 95.66 — “E2b, AUC at c36 & 97.30 \ci{95.66}{98.55} & 98.01 \ci{96.18}{98.85} \\” | 95.66 | 95.66 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.50` |
| `R1.supp-tab-appcampaignsec.51` | 98.55 — “E2b, AUC at c36 & 97.30 \ci{95.66}{98.55} & 98.01 \ci{96.18}{98.85} \\” | 98.55 | 98.55 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.51` |
| `R1.supp-tab-appcampaignsec.52` | 98.01 — “E2b, AUC at c36 & 97.30 \ci{95.66}{98.55} & 98.01 \ci{96.18}{98.85} \\” | 98.01 | 98.01 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.52` |
| `R1.supp-tab-appcampaignsec.53` | 96.18 — “E2b, AUC at c36 & 97.30 \ci{95.66}{98.55} & 98.01 \ci{96.18}{98.85} \\” | 96.18 | 96.18 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.53` |
| `R1.supp-tab-appcampaignsec.54` | 98.85 — “E2b, AUC at c36 & 97.30 \ci{95.66}{98.55} & 98.01 \ci{96.18}{98.85} \\” | 98.85 | 98.85 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.54` |
| `R1.supp-tab-appcampaignsec.55` | -0.80 — “E2b $-$ E2a (c40) & $-0.80$ \ci{-3.17}{1.17} & $-0.03$ \ci{-3.07}{1.40} \\” | -0.80 | -0.7955 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.55` |
| `R1.supp-tab-appcampaignsec.56` | -3.17 — “E2b $-$ E2a (c40) & $-0.80$ \ci{-3.17}{1.17} & $-0.03$ \ci{-3.07}{1.40} \\” | -3.17 | -3.1744 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.56` |
| `R1.supp-tab-appcampaignsec.57` | 1.17 — “E2b $-$ E2a (c40) & $-0.80$ \ci{-3.17}{1.17} & $-0.03$ \ci{-3.07}{1.40} \\” | 1.17 | 1.1714 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.57` |
| `R1.supp-tab-appcampaignsec.58` | -0.03 — “E2b $-$ E2a (c40) & $-0.80$ \ci{-3.17}{1.17} & $-0.03$ \ci{-3.07}{1.40} \\” | -0.03 | -0.0306 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.58` |
| `R1.supp-tab-appcampaignsec.59` | -3.07 — “E2b $-$ E2a (c40) & $-0.80$ \ci{-3.17}{1.17} & $-0.03$ \ci{-3.07}{1.40} \\” | -3.07 | -3.0651 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.59` |
| `R1.supp-tab-appcampaignsec.60` | 1.40 — “E2b $-$ E2a (c40) & $-0.80$ \ci{-3.17}{1.17} & $-0.03$ \ci{-3.07}{1.40} \\” | 1.40 | 1.4031 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.60` |
| `R1.supp-tab-appcampaignsec.61` | -1.92 — “E2b $-$ SpatialBase (c40) & $-1.92$ \ci{-4.47}{0.26} & $-1.21$ \ci{-4.24}{0.47} \\” | -1.92 | -1.9184 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.61` |
| `R1.supp-tab-appcampaignsec.62` | -4.47 — “E2b $-$ SpatialBase (c40) & $-1.92$ \ci{-4.47}{0.26} & $-1.21$ \ci{-4.24}{0.47} \\” | -4.47 | -4.4685 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.62` |
| `R1.supp-tab-appcampaignsec.63` | 0.26 — “E2b $-$ SpatialBase (c40) & $-1.92$ \ci{-4.47}{0.26} & $-1.21$ \ci{-4.24}{0.47} \\” | 0.26 | 0.2649 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.63` |
| `R1.supp-tab-appcampaignsec.64` | -1.21 — “E2b $-$ SpatialBase (c40) & $-1.92$ \ci{-4.47}{0.26} & $-1.21$ \ci{-4.24}{0.47} \\” | -1.21 | -1.2117 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.64` |
| `R1.supp-tab-appcampaignsec.65` | -4.24 — “E2b $-$ SpatialBase (c40) & $-1.92$ \ci{-4.47}{0.26} & $-1.21$ \ci{-4.24}{0.47} \\” | -4.24 | -4.2450 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.65` |
| `R1.supp-tab-appcampaignsec.66` | 0.47 — “E2b $-$ SpatialBase (c40) & $-1.92$ \ci{-4.47}{0.26} & $-1.21$ \ci{-4.24}{0.47} \\” | 0.47 | 0.4720 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.66` |
| `R1.supp-tab-appcampaignsec.67` | 0.13 — “E2b $-$ E2a (c36) & 0.13 \ci{-1.12}{1.21} & 0.33 \ci{-1.10}{1.28} \\” | 0.13 | 0.1335 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.67` |
| `R1.supp-tab-appcampaignsec.68` | -1.12 — “E2b $-$ E2a (c36) & 0.13 \ci{-1.12}{1.21} & 0.33 \ci{-1.10}{1.28} \\” | -1.12 | -1.1212 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.68` |
| `R1.supp-tab-appcampaignsec.69` | 1.21 — “E2b $-$ E2a (c36) & 0.13 \ci{-1.12}{1.21} & 0.33 \ci{-1.10}{1.28} \\” | 1.21 | 1.2147 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.69` |
| `R1.supp-tab-appcampaignsec.70` | 0.33 — “E2b $-$ E2a (c36) & 0.13 \ci{-1.12}{1.21} & 0.33 \ci{-1.10}{1.28} \\” | 0.33 | 0.3291 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.70` |
| `R1.supp-tab-appcampaignsec.71` | -1.10 — “E2b $-$ E2a (c36) & 0.13 \ci{-1.12}{1.21} & 0.33 \ci{-1.10}{1.28} \\” | -1.10 | -1.1033 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.71` |
| `R1.supp-tab-appcampaignsec.72` | 1.28 — “E2b $-$ E2a (c36) & 0.13 \ci{-1.12}{1.21} & 0.33 \ci{-1.10}{1.28} \\” | 1.28 | 1.2781 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.72` |
| `R1.supp-tab-appcampaignsec.73` | 0.82 — “E2b $-$ SpatialBase (c36) & 0.82 \ci{-0.53}{2.09} & 0.73 \ci{-0.65}{2.02} \\” | 0.82 | 0.8227 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.73` |
| `R1.supp-tab-appcampaignsec.74` | -0.53 — “E2b $-$ SpatialBase (c36) & 0.82 \ci{-0.53}{2.09} & 0.73 \ci{-0.65}{2.02} \\” | -0.53 | -0.5290 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.74` |
| `R1.supp-tab-appcampaignsec.75` | 2.09 — “E2b $-$ SpatialBase (c36) & 0.82 \ci{-0.53}{2.09} & 0.73 \ci{-0.65}{2.02} \\” | 2.09 | 2.0859 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.75` |
| `R1.supp-tab-appcampaignsec.76` | 0.73 — “E2b $-$ SpatialBase (c36) & 0.82 \ci{-0.53}{2.09} & 0.73 \ci{-0.65}{2.02} \\” | 0.73 | 0.7258 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.76` |
| `R1.supp-tab-appcampaignsec.77` | -0.65 — “E2b $-$ SpatialBase (c36) & 0.82 \ci{-0.53}{2.09} & 0.73 \ci{-0.65}{2.02} \\” | -0.65 | -0.6518 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.77` |
| `R1.supp-tab-appcampaignsec.78` | 2.02 — “E2b $-$ SpatialBase (c36) & 0.82 \ci{-0.53}{2.09} & 0.73 \ci{-0.65}{2.02} \\” | 2.02 | 2.0191 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignsec.78` |

## R1.supp-tab-appcampaignots — Revision 1 — Supplementary Material, tab:appcampaignots

*Supplementary Material, tab:appcampaignots; `\label{tab:appcampaignots}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-tab-appcampaignots.1` | 85.08 — “E1 (EMA) & 85.08 (83.14 / 86.17 / 85.94) & 67.08 (65.59 / 66.87 / 68.77) & 68.98 (68.69 / ” | 85.08 | 85.08 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.1` |
| `R1.supp-tab-appcampaignots.2` | 83.14 — “E1 (EMA) & 85.08 (83.14 / 86.17 / 85.94) & 67.08 (65.59 / 66.87 / 68.77) & 68.98 (68.69 / ” | 83.14 | 83.14 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.2` |
| `R1.supp-tab-appcampaignots.3` | 86.17 — “E1 (EMA) & 85.08 (83.14 / 86.17 / 85.94) & 67.08 (65.59 / 66.87 / 68.77) & 68.98 (68.69 / ” | 86.17 | 86.17 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.3` |
| `R1.supp-tab-appcampaignots.4` | 85.94 — “E1 (EMA) & 85.08 (83.14 / 86.17 / 85.94) & 67.08 (65.59 / 66.87 / 68.77) & 68.98 (68.69 / ” | 85.94 | 85.94 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.4` |
| `R1.supp-tab-appcampaignots.5` | 67.08 — “E1 (EMA) & 85.08 (83.14 / 86.17 / 85.94) & 67.08 (65.59 / 66.87 / 68.77) & 68.98 (68.69 / ” | 67.08 | 67.08 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.5` |
| `R1.supp-tab-appcampaignots.6` | 65.59 — “E1 (EMA) & 85.08 (83.14 / 86.17 / 85.94) & 67.08 (65.59 / 66.87 / 68.77) & 68.98 (68.69 / ” | 65.59 | 65.59 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.6` |
| `R1.supp-tab-appcampaignots.7` | 66.87 — “E1 (EMA) & 85.08 (83.14 / 86.17 / 85.94) & 67.08 (65.59 / 66.87 / 68.77) & 68.98 (68.69 / ” | 66.87 | 66.87 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.7` |
| `R1.supp-tab-appcampaignots.8` | 68.77 — “E1 (EMA) & 85.08 (83.14 / 86.17 / 85.94) & 67.08 (65.59 / 66.87 / 68.77) & 68.98 (68.69 / ” | 68.77 | 68.77 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.8` |
| `R1.supp-tab-appcampaignots.9` | 68.98 — “E1 (EMA) & 85.08 (83.14 / 86.17 / 85.94) & 67.08 (65.59 / 66.87 / 68.77) & 68.98 (68.69 / ” | 68.98 | 68.98 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.9` |
| `R1.supp-tab-appcampaignots.10` | 68.69 — “E1 (EMA) & 85.08 (83.14 / 86.17 / 85.94) & 67.08 (65.59 / 66.87 / 68.77) & 68.98 (68.69 / ” | 68.69 | 68.69 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.10` |
| `R1.supp-tab-appcampaignots.11` | 69.26 — “E1 (EMA) & 85.08 (83.14 / 86.17 / 85.94) & 67.08 (65.59 / 66.87 / 68.77) & 68.98 (68.69 / ” | 69.26 | 69.26 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.11` |
| `R1.supp-tab-appcampaignots.12` | 68.99 — “E1 (EMA) & 85.08 (83.14 / 86.17 / 85.94) & 67.08 (65.59 / 66.87 / 68.77) & 68.98 (68.69 / ” | 68.99 | 68.99 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.12` |
| `R1.supp-tab-appcampaignots.13` | 78.65 — “E1 (EMA) & 85.08 (83.14 / 86.17 / 85.94) & 67.08 (65.59 / 66.87 / 68.77) & 68.98 (68.69 / ” | 78.65 | 78.65 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.13` |
| `R1.supp-tab-appcampaignots.14` | 77.23 — “E1 (EMA) & 85.08 (83.14 / 86.17 / 85.94) & 67.08 (65.59 / 66.87 / 68.77) & 68.98 (68.69 / ” | 77.23 | 77.23 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.14` |
| `R1.supp-tab-appcampaignots.15` | 81.15 — “E1 (EMA) & 85.08 (83.14 / 86.17 / 85.94) & 67.08 (65.59 / 66.87 / 68.77) & 68.98 (68.69 / ” | 81.15 | 81.15 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.15` |
| `R1.supp-tab-appcampaignots.16` | 77.57 — “E1 (EMA) & 85.08 (83.14 / 86.17 / 85.94) & 67.08 (65.59 / 66.87 / 68.77) & 68.98 (68.69 / ” | 77.57 | 77.57 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.16` |
| `R1.supp-tab-appcampaignots.17` | 75.03 — “E1 (EMA) & 85.08 (83.14 / 86.17 / 85.94) & 67.08 (65.59 / 66.87 / 68.77) & 68.98 (68.69 / ” | 75.03 | 75.03 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.17` |
| `R1.supp-tab-appcampaignots.18` | 74.54 — “E1 (EMA) & 85.08 (83.14 / 86.17 / 85.94) & 67.08 (65.59 / 66.87 / 68.77) & 68.98 (68.69 / ” | 74.54 | 74.54 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.18` |
| `R1.supp-tab-appcampaignots.19` | 79.68 — “E1 (EMA) & 85.08 (83.14 / 86.17 / 85.94) & 67.08 (65.59 / 66.87 / 68.77) & 68.98 (68.69 / ” | 79.68 | 79.68 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.19` |
| `R1.supp-tab-appcampaignots.20` | 70.86 — “E1 (EMA) & 85.08 (83.14 / 86.17 / 85.94) & 67.08 (65.59 / 66.87 / 68.77) & 68.98 (68.69 / ” | 70.86 | 70.86 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.20` |
| `R1.supp-tab-appcampaignots.21` | 79.19 — “Fair-N (EMA) & 79.19 (82.81 / 75.17 / 79.58) & 65.95 (68.30 / 66.90 / 62.64) & 64.73 (66.7” | 79.19 | 79.19 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.21` |
| `R1.supp-tab-appcampaignots.22` | 82.81 — “Fair-N (EMA) & 79.19 (82.81 / 75.17 / 79.58) & 65.95 (68.30 / 66.90 / 62.64) & 64.73 (66.7” | 82.81 | 82.81 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.22` |
| `R1.supp-tab-appcampaignots.23` | 75.17 — “Fair-N (EMA) & 79.19 (82.81 / 75.17 / 79.58) & 65.95 (68.30 / 66.90 / 62.64) & 64.73 (66.7” | 75.17 | 75.17 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.23` |
| `R1.supp-tab-appcampaignots.24` | 79.58 — “Fair-N (EMA) & 79.19 (82.81 / 75.17 / 79.58) & 65.95 (68.30 / 66.90 / 62.64) & 64.73 (66.7” | 79.58 | 79.58 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.24` |
| `R1.supp-tab-appcampaignots.25` | 65.95 — “Fair-N (EMA) & 79.19 (82.81 / 75.17 / 79.58) & 65.95 (68.30 / 66.90 / 62.64) & 64.73 (66.7” | 65.95 | 65.95 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.25` |
| `R1.supp-tab-appcampaignots.26` | 68.30 — “Fair-N (EMA) & 79.19 (82.81 / 75.17 / 79.58) & 65.95 (68.30 / 66.90 / 62.64) & 64.73 (66.7” | 68.30 | 68.30 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.26` |
| `R1.supp-tab-appcampaignots.27` | 66.90 — “Fair-N (EMA) & 79.19 (82.81 / 75.17 / 79.58) & 65.95 (68.30 / 66.90 / 62.64) & 64.73 (66.7” | 66.90 | 66.90 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.27` |
| `R1.supp-tab-appcampaignots.28` | 62.64 — “Fair-N (EMA) & 79.19 (82.81 / 75.17 / 79.58) & 65.95 (68.30 / 66.90 / 62.64) & 64.73 (66.7” | 62.64 | 62.64 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.28` |
| `R1.supp-tab-appcampaignots.29` | 64.73 — “Fair-N (EMA) & 79.19 (82.81 / 75.17 / 79.58) & 65.95 (68.30 / 66.90 / 62.64) & 64.73 (66.7” | 64.73 | 64.73 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.29` |
| `R1.supp-tab-appcampaignots.30` | 66.76 — “Fair-N (EMA) & 79.19 (82.81 / 75.17 / 79.58) & 65.95 (68.30 / 66.90 / 62.64) & 64.73 (66.7” | 66.76 | 66.76 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.30` |
| `R1.supp-tab-appcampaignots.31` | 57.09 — “Fair-N (EMA) & 79.19 (82.81 / 75.17 / 79.58) & 65.95 (68.30 / 66.90 / 62.64) & 64.73 (66.7” | 57.09 | 57.09 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.31` |
| `R1.supp-tab-appcampaignots.32` | 70.35 — “Fair-N (EMA) & 79.19 (82.81 / 75.17 / 79.58) & 65.95 (68.30 / 66.90 / 62.64) & 64.73 (66.7” | 70.35 | 70.35 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.32` |
| `R1.supp-tab-appcampaignots.33` | 79.92 — “Fair-N (EMA) & 79.19 (82.81 / 75.17 / 79.58) & 65.95 (68.30 / 66.90 / 62.64) & 64.73 (66.7” | 79.92 | 79.92 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.33` |
| `R1.supp-tab-appcampaignots.34` | 80.31 — “Fair-N (EMA) & 79.19 (82.81 / 75.17 / 79.58) & 65.95 (68.30 / 66.90 / 62.64) & 64.73 (66.7” | 80.31 | 80.31 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.34` |
| `R1.supp-tab-appcampaignots.35` | 82.71 — “Fair-N (EMA) & 79.19 (82.81 / 75.17 / 79.58) & 65.95 (68.30 / 66.90 / 62.64) & 64.73 (66.7” | 82.71 | 82.71 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.35` |
| `R1.supp-tab-appcampaignots.36` | 76.73 — “Fair-N (EMA) & 79.19 (82.81 / 75.17 / 79.58) & 65.95 (68.30 / 66.90 / 62.64) & 64.73 (66.7” | 76.73 | 76.73 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.36` |
| `R1.supp-tab-appcampaignots.37` | 71.09 — “Fair-N (EMA) & 79.19 (82.81 / 75.17 / 79.58) & 65.95 (68.30 / 66.90 / 62.64) & 64.73 (66.7” | 71.09 | 71.09 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.37` |
| `R1.supp-tab-appcampaignots.38` | 76.51 — “Fair-N (EMA) & 79.19 (82.81 / 75.17 / 79.58) & 65.95 (68.30 / 66.90 / 62.64) & 64.73 (66.7” | 76.51 | 76.51 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.38` |
| `R1.supp-tab-appcampaignots.39` | 71.19 — “Fair-N (EMA) & 79.19 (82.81 / 75.17 / 79.58) & 65.95 (68.30 / 66.90 / 62.64) & 64.73 (66.7” | 71.19 | 71.19 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.39` |
| `R1.supp-tab-appcampaignots.40` | 65.56 — “Fair-N (EMA) & 79.19 (82.81 / 75.17 / 79.58) & 65.95 (68.30 / 66.90 / 62.64) & 64.73 (66.7” | 65.56 | 65.56 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.40` |
| `R1.supp-tab-appcampaignots.41` | 82.49 — “SpatialBase (raw) & 82.49 (80.41 / 82.33 / 84.74) & 65.04 (64.61 / 64.07 / 66.46) & 68.59 ” | 82.49 | 82.49 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.41` |
| `R1.supp-tab-appcampaignots.42` | 80.41 — “SpatialBase (raw) & 82.49 (80.41 / 82.33 / 84.74) & 65.04 (64.61 / 64.07 / 66.46) & 68.59 ” | 80.41 | 80.41 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.42` |
| `R1.supp-tab-appcampaignots.43` | 82.33 — “SpatialBase (raw) & 82.49 (80.41 / 82.33 / 84.74) & 65.04 (64.61 / 64.07 / 66.46) & 68.59 ” | 82.33 | 82.33 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.43` |
| `R1.supp-tab-appcampaignots.44` | 84.74 — “SpatialBase (raw) & 82.49 (80.41 / 82.33 / 84.74) & 65.04 (64.61 / 64.07 / 66.46) & 68.59 ” | 84.74 | 84.74 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.44` |
| `R1.supp-tab-appcampaignots.45` | 65.04 — “SpatialBase (raw) & 82.49 (80.41 / 82.33 / 84.74) & 65.04 (64.61 / 64.07 / 66.46) & 68.59 ” | 65.04 | 65.04 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.45` |
| `R1.supp-tab-appcampaignots.46` | 64.61 — “SpatialBase (raw) & 82.49 (80.41 / 82.33 / 84.74) & 65.04 (64.61 / 64.07 / 66.46) & 68.59 ” | 64.61 | 64.61 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.46` |
| `R1.supp-tab-appcampaignots.47` | 64.07 — “SpatialBase (raw) & 82.49 (80.41 / 82.33 / 84.74) & 65.04 (64.61 / 64.07 / 66.46) & 68.59 ” | 64.07 | 64.07 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.47` |
| `R1.supp-tab-appcampaignots.48` | 66.46 — “SpatialBase (raw) & 82.49 (80.41 / 82.33 / 84.74) & 65.04 (64.61 / 64.07 / 66.46) & 68.59 ” | 66.46 | 66.46 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.48` |
| `R1.supp-tab-appcampaignots.49` | 68.59 — “SpatialBase (raw) & 82.49 (80.41 / 82.33 / 84.74) & 65.04 (64.61 / 64.07 / 66.46) & 68.59 ” | 68.59 | 68.59 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.49` |
| `R1.supp-tab-appcampaignots.50` | 69.90 — “SpatialBase (raw) & 82.49 (80.41 / 82.33 / 84.74) & 65.04 (64.61 / 64.07 / 66.46) & 68.59 ” | 69.90 | 69.90 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.50` |
| `R1.supp-tab-appcampaignots.51` | 68.74 — “SpatialBase (raw) & 82.49 (80.41 / 82.33 / 84.74) & 65.04 (64.61 / 64.07 / 66.46) & 68.59 ” | 68.74 | 68.74 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.51` |
| `R1.supp-tab-appcampaignots.52` | 67.13 — “SpatialBase (raw) & 82.49 (80.41 / 82.33 / 84.74) & 65.04 (64.61 / 64.07 / 66.46) & 68.59 ” | 67.13 | 67.13 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.52` |
| `R1.supp-tab-appcampaignots.53` | 82.30 — “SpatialBase (raw) & 82.49 (80.41 / 82.33 / 84.74) & 65.04 (64.61 / 64.07 / 66.46) & 68.59 ” | 82.30 | 82.30 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.53` |
| `R1.supp-tab-appcampaignots.54` | 80.82 — “SpatialBase (raw) & 82.49 (80.41 / 82.33 / 84.74) & 65.04 (64.61 / 64.07 / 66.46) & 68.59 ” | 80.82 | 80.82 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.54` |
| `R1.supp-tab-appcampaignots.55` | 84.11 — “SpatialBase (raw) & 82.49 (80.41 / 82.33 / 84.74) & 65.04 (64.61 / 64.07 / 66.46) & 68.59 ” | 84.11 | 84.11 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.55` |
| `R1.supp-tab-appcampaignots.56` | 81.95 — “SpatialBase (raw) & 82.49 (80.41 / 82.33 / 84.74) & 65.04 (64.61 / 64.07 / 66.46) & 68.59 ” | 81.95 | 81.95 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.56` |
| `R1.supp-tab-appcampaignots.57` | 73.18 — “SpatialBase (raw) & 82.49 (80.41 / 82.33 / 84.74) & 65.04 (64.61 / 64.07 / 66.46) & 68.59 ” | 73.18 | 73.18 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.57` |
| `R1.supp-tab-appcampaignots.58` | 71.76 — “SpatialBase (raw) & 82.49 (80.41 / 82.33 / 84.74) & 65.04 (64.61 / 64.07 / 66.46) & 68.59 ” | 71.76 | 71.76 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.58` |
| `R1.supp-tab-appcampaignots.59` | 74.69 — “SpatialBase (raw) & 82.49 (80.41 / 82.33 / 84.74) & 65.04 (64.61 / 64.07 / 66.46) & 68.59 ” | 74.69 | 74.69 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.59` |
| `R1.supp-tab-appcampaignots.60` | 73.08 — “SpatialBase (raw) & 82.49 (80.41 / 82.33 / 84.74) & 65.04 (64.61 / 64.07 / 66.46) & 68.59 ” | 73.08 | 73.08 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.60` |
| `R1.supp-tab-appcampaignots.61` | 84.54 — “E2a (raw) & 84.54 (85.61 / 83.05 / 84.96) & 66.41 (67.62 / 65.74 / 65.87) & 69.57 (67.68 /” | 84.54 | 84.54 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.61` |
| `R1.supp-tab-appcampaignots.62` | 85.61 — “E2a (raw) & 84.54 (85.61 / 83.05 / 84.96) & 66.41 (67.62 / 65.74 / 65.87) & 69.57 (67.68 /” | 85.61 | 85.61 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.62` |
| `R1.supp-tab-appcampaignots.63` | 83.05 — “E2a (raw) & 84.54 (85.61 / 83.05 / 84.96) & 66.41 (67.62 / 65.74 / 65.87) & 69.57 (67.68 /” | 83.05 | 83.05 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.63` |
| `R1.supp-tab-appcampaignots.64` | 84.96 — “E2a (raw) & 84.54 (85.61 / 83.05 / 84.96) & 66.41 (67.62 / 65.74 / 65.87) & 69.57 (67.68 /” | 84.96 | 84.96 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.64` |
| `R1.supp-tab-appcampaignots.65` | 66.41 — “E2a (raw) & 84.54 (85.61 / 83.05 / 84.96) & 66.41 (67.62 / 65.74 / 65.87) & 69.57 (67.68 /” | 66.41 | 66.41 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.65` |
| `R1.supp-tab-appcampaignots.66` | 67.62 — “E2a (raw) & 84.54 (85.61 / 83.05 / 84.96) & 66.41 (67.62 / 65.74 / 65.87) & 69.57 (67.68 /” | 67.62 | 67.62 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.66` |
| `R1.supp-tab-appcampaignots.67` | 65.74 — “E2a (raw) & 84.54 (85.61 / 83.05 / 84.96) & 66.41 (67.62 / 65.74 / 65.87) & 69.57 (67.68 /” | 65.74 | 65.74 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.67` |
| `R1.supp-tab-appcampaignots.68` | 65.87 — “E2a (raw) & 84.54 (85.61 / 83.05 / 84.96) & 66.41 (67.62 / 65.74 / 65.87) & 69.57 (67.68 /” | 65.87 | 65.87 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.68` |
| `R1.supp-tab-appcampaignots.69` | 69.57 — “E2a (raw) & 84.54 (85.61 / 83.05 / 84.96) & 66.41 (67.62 / 65.74 / 65.87) & 69.57 (67.68 /” | 69.57 | 69.57 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.69` |
| `R1.supp-tab-appcampaignots.70` | 67.68 — “E2a (raw) & 84.54 (85.61 / 83.05 / 84.96) & 66.41 (67.62 / 65.74 / 65.87) & 69.57 (67.68 /” | 67.68 | 67.68 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.70` |
| `R1.supp-tab-appcampaignots.71` | 69.17 — “E2a (raw) & 84.54 (85.61 / 83.05 / 84.96) & 66.41 (67.62 / 65.74 / 65.87) & 69.57 (67.68 /” | 69.17 | 69.17 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.71` |
| `R1.supp-tab-appcampaignots.72` | 71.86 — “E2a (raw) & 84.54 (85.61 / 83.05 / 84.96) & 66.41 (67.62 / 65.74 / 65.87) & 69.57 (67.68 /” | 71.86 | 71.86 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.72` |
| `R1.supp-tab-appcampaignots.73` | 79.80 — “E2a (raw) & 84.54 (85.61 / 83.05 / 84.96) & 66.41 (67.62 / 65.74 / 65.87) & 69.57 (67.68 /” | 79.80 | 79.80 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.73` |
| `R1.supp-tab-appcampaignots.74` | 83.73 — “E2a (raw) & 84.54 (85.61 / 83.05 / 84.96) & 66.41 (67.62 / 65.74 / 65.87) & 69.57 (67.68 /” | 83.73 | 83.73 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.74` |
| `R1.supp-tab-appcampaignots.75` | 76.82 — “E2a (raw) & 84.54 (85.61 / 83.05 / 84.96) & 66.41 (67.62 / 65.74 / 65.87) & 69.57 (67.68 /” | 76.82 | 76.82 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.75` |
| `R1.supp-tab-appcampaignots.76` | 78.86 — “E2a (raw) & 84.54 (85.61 / 83.05 / 84.96) & 66.41 (67.62 / 65.74 / 65.87) & 69.57 (67.68 /” | 78.86 | 78.86 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.76` |
| `R1.supp-tab-appcampaignots.77` | 79.42 — “E2a (raw) & 84.54 (85.61 / 83.05 / 84.96) & 66.41 (67.62 / 65.74 / 65.87) & 69.57 (67.68 /” | 79.42 | 79.42 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.77` |
| `R1.supp-tab-appcampaignots.78` | 81.12 — “E2a (raw) & 84.54 (85.61 / 83.05 / 84.96) & 66.41 (67.62 / 65.74 / 65.87) & 69.57 (67.68 /” | 81.12 | 81.12 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.78` |
| `R1.supp-tab-appcampaignots.79` | 77.01 — “E2a (raw) & 84.54 (85.61 / 83.05 / 84.96) & 66.41 (67.62 / 65.74 / 65.87) & 69.57 (67.68 /” | 77.01 | 77.01 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.79` |
| `R1.supp-tab-appcampaignots.80` | 80.12 — “E2a (raw) & 84.54 (85.61 / 83.05 / 84.96) & 66.41 (67.62 / 65.74 / 65.87) & 69.57 (67.68 /” | 80.12 | 80.12 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.80` |
| `R1.supp-tab-appcampaignots.81` | 92.07 — “anchor (raw) & 92.07 (93.90 / 91.59 / 90.71) & 69.45 (69.63 / 65.79 / 72.93) & 69.58 (66.0” | 92.07 | 92.07 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.81` |
| `R1.supp-tab-appcampaignots.82` | 93.90 — “anchor (raw) & 92.07 (93.90 / 91.59 / 90.71) & 69.45 (69.63 / 65.79 / 72.93) & 69.58 (66.0” | 93.90 | 93.90 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.82` |
| `R1.supp-tab-appcampaignots.83` | 91.59 — “anchor (raw) & 92.07 (93.90 / 91.59 / 90.71) & 69.45 (69.63 / 65.79 / 72.93) & 69.58 (66.0” | 91.59 | 91.59 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.83` |
| `R1.supp-tab-appcampaignots.84` | 90.71 — “anchor (raw) & 92.07 (93.90 / 91.59 / 90.71) & 69.45 (69.63 / 65.79 / 72.93) & 69.58 (66.0” | 90.71 | 90.71 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.84` |
| `R1.supp-tab-appcampaignots.85` | 69.45 — “anchor (raw) & 92.07 (93.90 / 91.59 / 90.71) & 69.45 (69.63 / 65.79 / 72.93) & 69.58 (66.0” | 69.45 | 69.45 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.85` |
| `R1.supp-tab-appcampaignots.86` | 69.63 — “anchor (raw) & 92.07 (93.90 / 91.59 / 90.71) & 69.45 (69.63 / 65.79 / 72.93) & 69.58 (66.0” | 69.63 | 69.63 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.86` |
| `R1.supp-tab-appcampaignots.87` | 65.79 — “anchor (raw) & 92.07 (93.90 / 91.59 / 90.71) & 69.45 (69.63 / 65.79 / 72.93) & 69.58 (66.0” | 65.79 | 65.79 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.87` |
| `R1.supp-tab-appcampaignots.88` | 72.93 — “anchor (raw) & 92.07 (93.90 / 91.59 / 90.71) & 69.45 (69.63 / 65.79 / 72.93) & 69.58 (66.0” | 72.93 | 72.93 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.88` |
| `R1.supp-tab-appcampaignots.89` | 69.58 — “anchor (raw) & 92.07 (93.90 / 91.59 / 90.71) & 69.45 (69.63 / 65.79 / 72.93) & 69.58 (66.0” | 69.58 | 69.58 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.89` |
| `R1.supp-tab-appcampaignots.90` | 66.04 — “anchor (raw) & 92.07 (93.90 / 91.59 / 90.71) & 69.45 (69.63 / 65.79 / 72.93) & 69.58 (66.0” | 66.04 | 66.04 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.90` |
| `R1.supp-tab-appcampaignots.91` | 69.76 — “anchor (raw) & 92.07 (93.90 / 91.59 / 90.71) & 69.45 (69.63 / 65.79 / 72.93) & 69.58 (66.0” | 69.76 | 69.76 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.91` |
| `R1.supp-tab-appcampaignots.92` | 72.94 — “anchor (raw) & 92.07 (93.90 / 91.59 / 90.71) & 69.45 (69.63 / 65.79 / 72.93) & 69.58 (66.0” | 72.94 | 72.94 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.92` |
| `R1.supp-tab-appcampaignots.93` | 82.54 — “anchor (raw) & 92.07 (93.90 / 91.59 / 90.71) & 69.45 (69.63 / 65.79 / 72.93) & 69.58 (66.0” | 82.54 | 82.54 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.93` |
| `R1.supp-tab-appcampaignots.94` | 80.90 — “anchor (raw) & 92.07 (93.90 / 91.59 / 90.71) & 69.45 (69.63 / 65.79 / 72.93) & 69.58 (66.0” | 80.90 | 80.90 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.94` |
| `R1.supp-tab-appcampaignots.95` | 84.15 — “anchor (raw) & 92.07 (93.90 / 91.59 / 90.71) & 69.45 (69.63 / 65.79 / 72.93) & 69.58 (66.0” | 84.15 | 84.15 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.95` |
| `R1.supp-tab-appcampaignots.96` | 82.56 — “anchor (raw) & 92.07 (93.90 / 91.59 / 90.71) & 69.45 (69.63 / 65.79 / 72.93) & 69.58 (66.0” | 82.56 | 82.56 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.96` |
| `R1.supp-tab-appcampaignots.97` | 74.83 — “anchor (raw) & 92.07 (93.90 / 91.59 / 90.71) & 69.45 (69.63 / 65.79 / 72.93) & 69.58 (66.0” | 74.83 | 74.83 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.97` |
| `R1.supp-tab-appcampaignots.98` | 74.68 — “anchor (raw) & 92.07 (93.90 / 91.59 / 90.71) & 69.45 (69.63 / 65.79 / 72.93) & 69.58 (66.0” | 74.68 | 74.68 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.98` |
| `R1.supp-tab-appcampaignots.99` | 75.44 — “anchor (raw) & 92.07 (93.90 / 91.59 / 90.71) & 69.45 (69.63 / 65.79 / 72.93) & 69.58 (66.0” | 75.44 | 75.44 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.99` |
| `R1.supp-tab-appcampaignots.100` | 74.37 — “anchor (raw) & 92.07 (93.90 / 91.59 / 90.71) & 69.45 (69.63 / 65.79 / 72.93) & 69.58 (66.0” | 74.37 | 74.37 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.100` |
| `R1.supp-tab-appcampaignots.101` | 81.21 — “E3a (raw) & 81.21 (80.37 / 82.37 / 80.90) & 55.73 (58.75 / 53.41 / 55.03) & 68.68 (69.51 /” | 81.21 | 81.21 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.101` |
| `R1.supp-tab-appcampaignots.102` | 80.37 — “E3a (raw) & 81.21 (80.37 / 82.37 / 80.90) & 55.73 (58.75 / 53.41 / 55.03) & 68.68 (69.51 /” | 80.37 | 80.37 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.102` |
| `R1.supp-tab-appcampaignots.103` | 82.37 — “E3a (raw) & 81.21 (80.37 / 82.37 / 80.90) & 55.73 (58.75 / 53.41 / 55.03) & 68.68 (69.51 /” | 82.37 | 82.37 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.103` |
| `R1.supp-tab-appcampaignots.104` | 80.90 — “E3a (raw) & 81.21 (80.37 / 82.37 / 80.90) & 55.73 (58.75 / 53.41 / 55.03) & 68.68 (69.51 /” | 80.90 | 80.90 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.104` |
| `R1.supp-tab-appcampaignots.105` | 55.73 — “E3a (raw) & 81.21 (80.37 / 82.37 / 80.90) & 55.73 (58.75 / 53.41 / 55.03) & 68.68 (69.51 /” | 55.73 | 55.73 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.105` |
| `R1.supp-tab-appcampaignots.106` | 58.75 — “E3a (raw) & 81.21 (80.37 / 82.37 / 80.90) & 55.73 (58.75 / 53.41 / 55.03) & 68.68 (69.51 /” | 58.75 | 58.75 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.106` |
| `R1.supp-tab-appcampaignots.107` | 53.41 — “E3a (raw) & 81.21 (80.37 / 82.37 / 80.90) & 55.73 (58.75 / 53.41 / 55.03) & 68.68 (69.51 /” | 53.41 | 53.41 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.107` |
| `R1.supp-tab-appcampaignots.108` | 55.03 — “E3a (raw) & 81.21 (80.37 / 82.37 / 80.90) & 55.73 (58.75 / 53.41 / 55.03) & 68.68 (69.51 /” | 55.03 | 55.03 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.108` |
| `R1.supp-tab-appcampaignots.109` | 68.68 — “E3a (raw) & 81.21 (80.37 / 82.37 / 80.90) & 55.73 (58.75 / 53.41 / 55.03) & 68.68 (69.51 /” | 68.68 | 68.68 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.109` |
| `R1.supp-tab-appcampaignots.110` | 69.51 — “E3a (raw) & 81.21 (80.37 / 82.37 / 80.90) & 55.73 (58.75 / 53.41 / 55.03) & 68.68 (69.51 /” | 69.51 | 69.51 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.110` |
| `R1.supp-tab-appcampaignots.111` | 72.93 — “E3a (raw) & 81.21 (80.37 / 82.37 / 80.90) & 55.73 (58.75 / 53.41 / 55.03) & 68.68 (69.51 /” | 72.93 | 72.93 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.111` |
| `R1.supp-tab-appcampaignots.112` | 63.60 — “E3a (raw) & 81.21 (80.37 / 82.37 / 80.90) & 55.73 (58.75 / 53.41 / 55.03) & 68.68 (69.51 /” | 63.60 | 63.60 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.112` |
| `R1.supp-tab-appcampaignots.113` | 79.51 — “E3a (raw) & 81.21 (80.37 / 82.37 / 80.90) & 55.73 (58.75 / 53.41 / 55.03) & 68.68 (69.51 /” | 79.51 | 79.51 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.113` |
| `R1.supp-tab-appcampaignots.114` | 79.27 — “E3a (raw) & 81.21 (80.37 / 82.37 / 80.90) & 55.73 (58.75 / 53.41 / 55.03) & 68.68 (69.51 /” | 79.27 | 79.27 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.114` |
| `R1.supp-tab-appcampaignots.115` | 80.24 — “E3a (raw) & 81.21 (80.37 / 82.37 / 80.90) & 55.73 (58.75 / 53.41 / 55.03) & 68.68 (69.51 /” | 80.24 | 80.24 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.115` |
| `R1.supp-tab-appcampaignots.116` | 79.01 — “E3a (raw) & 81.21 (80.37 / 82.37 / 80.90) & 55.73 (58.75 / 53.41 / 55.03) & 68.68 (69.51 /” | 79.01 | 79.01 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.116` |
| `R1.supp-tab-appcampaignots.117` | 70.38 — “E3a (raw) & 81.21 (80.37 / 82.37 / 80.90) & 55.73 (58.75 / 53.41 / 55.03) & 68.68 (69.51 /” | 70.38 | 70.38 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.117` |
| `R1.supp-tab-appcampaignots.118` | 73.99 — “E3a (raw) & 81.21 (80.37 / 82.37 / 80.90) & 55.73 (58.75 / 53.41 / 55.03) & 68.68 (69.51 /” | 73.99 | 73.99 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.118` |
| `R1.supp-tab-appcampaignots.119` | 70.49 — “E3a (raw) & 81.21 (80.37 / 82.37 / 80.90) & 55.73 (58.75 / 53.41 / 55.03) & 68.68 (69.51 /” | 70.49 | 70.49 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.119` |
| `R1.supp-tab-appcampaignots.120` | 66.67 — “E3a (raw) & 81.21 (80.37 / 82.37 / 80.90) & 55.73 (58.75 / 53.41 / 55.03) & 68.68 (69.51 /” | 66.67 | 66.67 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.120` |
| `R1.supp-tab-appcampaignots.121` | 83.28 — “E3b (raw) & 83.28 (83.48 / 78.97 / 87.38) & 54.60 (53.01 / 52.79 / 58.01) & 74.01 (74.28 /” | 83.28 | 83.28 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.121` |
| `R1.supp-tab-appcampaignots.122` | 83.48 — “E3b (raw) & 83.28 (83.48 / 78.97 / 87.38) & 54.60 (53.01 / 52.79 / 58.01) & 74.01 (74.28 /” | 83.48 | 83.48 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.122` |
| `R1.supp-tab-appcampaignots.123` | 78.97 — “E3b (raw) & 83.28 (83.48 / 78.97 / 87.38) & 54.60 (53.01 / 52.79 / 58.01) & 74.01 (74.28 /” | 78.97 | 78.97 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.123` |
| `R1.supp-tab-appcampaignots.124` | 87.38 — “E3b (raw) & 83.28 (83.48 / 78.97 / 87.38) & 54.60 (53.01 / 52.79 / 58.01) & 74.01 (74.28 /” | 87.38 | 87.38 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.124` |
| `R1.supp-tab-appcampaignots.125` | 54.60 — “E3b (raw) & 83.28 (83.48 / 78.97 / 87.38) & 54.60 (53.01 / 52.79 / 58.01) & 74.01 (74.28 /” | 54.60 | 54.60 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.125` |
| `R1.supp-tab-appcampaignots.126` | 53.01 — “E3b (raw) & 83.28 (83.48 / 78.97 / 87.38) & 54.60 (53.01 / 52.79 / 58.01) & 74.01 (74.28 /” | 53.01 | 53.01 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.126` |
| `R1.supp-tab-appcampaignots.127` | 52.79 — “E3b (raw) & 83.28 (83.48 / 78.97 / 87.38) & 54.60 (53.01 / 52.79 / 58.01) & 74.01 (74.28 /” | 52.79 | 52.79 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.127` |
| `R1.supp-tab-appcampaignots.128` | 58.01 — “E3b (raw) & 83.28 (83.48 / 78.97 / 87.38) & 54.60 (53.01 / 52.79 / 58.01) & 74.01 (74.28 /” | 58.01 | 58.01 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.128` |
| `R1.supp-tab-appcampaignots.129` | 74.01 — “E3b (raw) & 83.28 (83.48 / 78.97 / 87.38) & 54.60 (53.01 / 52.79 / 58.01) & 74.01 (74.28 /” | 74.01 | 74.01 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.129` |
| `R1.supp-tab-appcampaignots.130` | 74.28 — “E3b (raw) & 83.28 (83.48 / 78.97 / 87.38) & 54.60 (53.01 / 52.79 / 58.01) & 74.01 (74.28 /” | 74.28 | 74.28 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.130` |
| `R1.supp-tab-appcampaignots.131` | 72.56 — “E3b (raw) & 83.28 (83.48 / 78.97 / 87.38) & 54.60 (53.01 / 52.79 / 58.01) & 74.01 (74.28 /” | 72.56 | 72.56 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.131` |
| `R1.supp-tab-appcampaignots.132` | 75.18 — “E3b (raw) & 83.28 (83.48 / 78.97 / 87.38) & 54.60 (53.01 / 52.79 / 58.01) & 74.01 (74.28 /” | 75.18 | 75.18 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.132` |
| `R1.supp-tab-appcampaignots.133` | 79.43 — “E3b (raw) & 83.28 (83.48 / 78.97 / 87.38) & 54.60 (53.01 / 52.79 / 58.01) & 74.01 (74.28 /” | 79.43 | 79.43 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.133` |
| `R1.supp-tab-appcampaignots.134` | 77.14 — “E3b (raw) & 83.28 (83.48 / 78.97 / 87.38) & 54.60 (53.01 / 52.79 / 58.01) & 74.01 (74.28 /” | 77.14 | 77.14 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.134` |
| `R1.supp-tab-appcampaignots.135` | 82.01 — “E3b (raw) & 83.28 (83.48 / 78.97 / 87.38) & 54.60 (53.01 / 52.79 / 58.01) & 74.01 (74.28 /” | 82.01 | 82.01 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.135` |
| `R1.supp-tab-appcampaignots.136` | 79.13 — “E3b (raw) & 83.28 (83.48 / 78.97 / 87.38) & 54.60 (53.01 / 52.79 / 58.01) & 74.01 (74.28 /” | 79.13 | 79.13 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.136` |
| `R1.supp-tab-appcampaignots.137` | 71.54 — “E3b (raw) & 83.28 (83.48 / 78.97 / 87.38) & 54.60 (53.01 / 52.79 / 58.01) & 74.01 (74.28 /” | 71.54 | 71.54 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.137` |
| `R1.supp-tab-appcampaignots.138` | 72.09 — “E3b (raw) & 83.28 (83.48 / 78.97 / 87.38) & 54.60 (53.01 / 52.79 / 58.01) & 74.01 (74.28 /” | 72.09 | 72.09 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.138` |
| `R1.supp-tab-appcampaignots.139` | 72.33 — “E3b (raw) & 83.28 (83.48 / 78.97 / 87.38) & 54.60 (53.01 / 52.79 / 58.01) & 74.01 (74.28 /” | 72.33 | 72.33 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.139` |
| `R1.supp-tab-appcampaignots.140` | 70.20 — “E3b (raw) & 83.28 (83.48 / 78.97 / 87.38) & 54.60 (53.01 / 52.79 / 58.01) & 74.01 (74.28 /” | 70.20 | 70.20 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.140` |
| `R1.supp-tab-appcampaignots.141` | 88.52 — “E2b (raw) & 88.52 (87.75 / 88.87 / 88.94) & 68.62 (69.36 / 67.08 / 69.41) & 69.21 (69.22 /” | 88.52 | 88.52 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.141` |
| `R1.supp-tab-appcampaignots.142` | 87.75 — “E2b (raw) & 88.52 (87.75 / 88.87 / 88.94) & 68.62 (69.36 / 67.08 / 69.41) & 69.21 (69.22 /” | 87.75 | 87.75 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.142` |
| `R1.supp-tab-appcampaignots.143` | 88.87 — “E2b (raw) & 88.52 (87.75 / 88.87 / 88.94) & 68.62 (69.36 / 67.08 / 69.41) & 69.21 (69.22 /” | 88.87 | 88.87 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.143` |
| `R1.supp-tab-appcampaignots.144` | 88.94 — “E2b (raw) & 88.52 (87.75 / 88.87 / 88.94) & 68.62 (69.36 / 67.08 / 69.41) & 69.21 (69.22 /” | 88.94 | 88.94 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.144` |
| `R1.supp-tab-appcampaignots.145` | 68.62 — “E2b (raw) & 88.52 (87.75 / 88.87 / 88.94) & 68.62 (69.36 / 67.08 / 69.41) & 69.21 (69.22 /” | 68.62 | 68.62 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.145` |
| `R1.supp-tab-appcampaignots.146` | 69.36 — “E2b (raw) & 88.52 (87.75 / 88.87 / 88.94) & 68.62 (69.36 / 67.08 / 69.41) & 69.21 (69.22 /” | 69.36 | 69.36 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.146` |
| `R1.supp-tab-appcampaignots.147` | 67.08 — “E2b (raw) & 88.52 (87.75 / 88.87 / 88.94) & 68.62 (69.36 / 67.08 / 69.41) & 69.21 (69.22 /” | 67.08 | 67.08 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.147` |
| `R1.supp-tab-appcampaignots.148` | 69.41 — “E2b (raw) & 88.52 (87.75 / 88.87 / 88.94) & 68.62 (69.36 / 67.08 / 69.41) & 69.21 (69.22 /” | 69.41 | 69.41 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.148` |
| `R1.supp-tab-appcampaignots.149` | 69.21 — “E2b (raw) & 88.52 (87.75 / 88.87 / 88.94) & 68.62 (69.36 / 67.08 / 69.41) & 69.21 (69.22 /” | 69.21 | 69.21 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.149` |
| `R1.supp-tab-appcampaignots.150` | 69.22 — “E2b (raw) & 88.52 (87.75 / 88.87 / 88.94) & 68.62 (69.36 / 67.08 / 69.41) & 69.21 (69.22 /” | 69.22 | 69.22 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.150` |
| `R1.supp-tab-appcampaignots.151` | 70.82 — “E2b (raw) & 88.52 (87.75 / 88.87 / 88.94) & 68.62 (69.36 / 67.08 / 69.41) & 69.21 (69.22 /” | 70.82 | 70.82 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.151` |
| `R1.supp-tab-appcampaignots.152` | 67.58 — “E2b (raw) & 88.52 (87.75 / 88.87 / 88.94) & 68.62 (69.36 / 67.08 / 69.41) & 69.21 (69.22 /” | 67.58 | 67.58 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.152` |
| `R1.supp-tab-appcampaignots.153` | 83.90 — “E2b (raw) & 88.52 (87.75 / 88.87 / 88.94) & 68.62 (69.36 / 67.08 / 69.41) & 69.21 (69.22 /” | 83.90 | 83.90 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.153` |
| `R1.supp-tab-appcampaignots.154` | 83.15 — “E2b (raw) & 88.52 (87.75 / 88.87 / 88.94) & 68.62 (69.36 / 67.08 / 69.41) & 69.21 (69.22 /” | 83.15 | 83.15 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.154` |
| `R1.supp-tab-appcampaignots.155` | 85.73 — “E2b (raw) & 88.52 (87.75 / 88.87 / 88.94) & 68.62 (69.36 / 67.08 / 69.41) & 69.21 (69.22 /” | 85.73 | 85.73 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.155` |
| `R1.supp-tab-appcampaignots.156` | 82.83 — “E2b (raw) & 88.52 (87.75 / 88.87 / 88.94) & 68.62 (69.36 / 67.08 / 69.41) & 69.21 (69.22 /” | 82.83 | 82.83 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.156` |
| `R1.supp-tab-appcampaignots.157` | 79.16 — “E2b (raw) & 88.52 (87.75 / 88.87 / 88.94) & 68.62 (69.36 / 67.08 / 69.41) & 69.21 (69.22 /” | 79.16 | 79.16 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.157` |
| `R1.supp-tab-appcampaignots.158` | 78.96 — “E2b (raw) & 88.52 (87.75 / 88.87 / 88.94) & 68.62 (69.36 / 67.08 / 69.41) & 69.21 (69.22 /” | 78.96 | 78.96 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.158` |
| `R1.supp-tab-appcampaignots.159` | 81.85 — “E2b (raw) & 88.52 (87.75 / 88.87 / 88.94) & 68.62 (69.36 / 67.08 / 69.41) & 69.21 (69.22 /” | 81.85 | 81.85 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.159` |
| `R1.supp-tab-appcampaignots.160` | 76.69 — “E2b (raw) & 88.52 (87.75 / 88.87 / 88.94) & 68.62 (69.36 / 67.08 / 69.41) & 69.21 (69.22 /” | 76.69 | 76.69 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignots.160` |

## R1.supp-tab-appcampaignfs — Revision 1 — Supplementary Material, tab:appcampaignfs

*Supplementary Material, tab:appcampaignfs; `\label{tab:appcampaignfs}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-tab-appcampaignfs.1` | 10,000 — “percentile intervals ($B = 10{,}000$; seeds, then 140 source-identity” | 10000 | 10000.00 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.1` |
| `R1.supp-tab-appcampaignfs.2` | -1.27 — “T1: E1 $-$ Fair-N & $-1.27$ \ci{-5.39}{2.87} & 3.94 \ci{-2.88}{10.95} \\” | -1.27 | -1.2687 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.2` |
| `R1.supp-tab-appcampaignfs.3` | -5.39 — “T1: E1 $-$ Fair-N & $-1.27$ \ci{-5.39}{2.87} & 3.94 \ci{-2.88}{10.95} \\” | -5.39 | -5.3895 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.3` |
| `R1.supp-tab-appcampaignfs.4` | 2.87 — “T1: E1 $-$ Fair-N & $-1.27$ \ci{-5.39}{2.87} & 3.94 \ci{-2.88}{10.95} \\” | 2.87 | 2.8692 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.4` |
| `R1.supp-tab-appcampaignfs.5` | 3.94 — “T1: E1 $-$ Fair-N & $-1.27$ \ci{-5.39}{2.87} & 3.94 \ci{-2.88}{10.95} \\” | 3.94 | 3.9422 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.5` |
| `R1.supp-tab-appcampaignfs.6` | -2.88 — “T1: E1 $-$ Fair-N & $-1.27$ \ci{-5.39}{2.87} & 3.94 \ci{-2.88}{10.95} \\” | -2.88 | -2.8793 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.6` |
| `R1.supp-tab-appcampaignfs.7` | 10.95 — “T1: E1 $-$ Fair-N & $-1.27$ \ci{-5.39}{2.87} & 3.94 \ci{-2.88}{10.95} \\” | 10.95 | 10.95 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.7` |
| `R1.supp-tab-appcampaignfs.8` | -0.24 — “T3 denominator & $-0.24$ \ci{-4.57}{4.10} & $-1.65$ \ci{-7.21}{3.76} \\” | -0.24 | -0.2432 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.8` |
| `R1.supp-tab-appcampaignfs.9` | -4.57 — “T3 denominator & $-0.24$ \ci{-4.57}{4.10} & $-1.65$ \ci{-7.21}{3.76} \\” | -4.57 | -4.5715 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.9` |
| `R1.supp-tab-appcampaignfs.10` | 4.10 — “T3 denominator & $-0.24$ \ci{-4.57}{4.10} & $-1.65$ \ci{-7.21}{3.76} \\” | 4.10 | 4.1023 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.10` |
| `R1.supp-tab-appcampaignfs.11` | -1.65 — “T3 denominator & $-0.24$ \ci{-4.57}{4.10} & $-1.65$ \ci{-7.21}{3.76} \\” | -1.65 | -1.6531 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.11` |
| `R1.supp-tab-appcampaignfs.12` | -7.21 — “T3 denominator & $-0.24$ \ci{-4.57}{4.10} & $-1.65$ \ci{-7.21}{3.76} \\” | -7.21 | -7.2076 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.12` |
| `R1.supp-tab-appcampaignfs.13` | 3.76 — “T3 denominator & $-0.24$ \ci{-4.57}{4.10} & $-1.65$ \ci{-7.21}{3.76} \\” | 3.76 | 3.7568 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.13` |
| `R1.supp-tab-appcampaignfs.14` | 1.58 — “T4: codec effect & 1.58 \ci{-2.58}{5.55} & 5.33 \ci{-0.08}{10.83} \\” | 1.58 | 1.5816 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.14` |
| `R1.supp-tab-appcampaignfs.15` | -2.58 — “T4: codec effect & 1.58 \ci{-2.58}{5.55} & 5.33 \ci{-0.08}{10.83} \\” | -2.58 | -2.5801 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.15` |
| `R1.supp-tab-appcampaignfs.16` | 5.55 — “T4: codec effect & 1.58 \ci{-2.58}{5.55} & 5.33 \ci{-0.08}{10.83} \\” | 5.55 | 5.5546 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.16` |
| `R1.supp-tab-appcampaignfs.17` | 5.33 — “T4: codec effect & 1.58 \ci{-2.58}{5.55} & 5.33 \ci{-0.08}{10.83} \\” | 5.33 | 5.3342 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.17` |
| `R1.supp-tab-appcampaignfs.18` | -0.08 — “T4: codec effect & 1.58 \ci{-2.58}{5.55} & 5.33 \ci{-0.08}{10.83} \\” | -0.08 | -0.0757 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.18` |
| `R1.supp-tab-appcampaignfs.19` | 10.83 — “T4: codec effect & 1.58 \ci{-2.58}{5.55} & 5.33 \ci{-0.08}{10.83} \\” | 10.83 | 10.83 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.19` |
| `R1.supp-tab-appcampaignfs.20` | 1.29 — “T5: c40-exposure effect & 1.29 \ci{-1.59}{4.18} & $-3.70$ \ci{-7.29}{-0.25} \\” | 1.29 | 1.2857 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.20` |
| `R1.supp-tab-appcampaignfs.21` | -1.59 — “T5: c40-exposure effect & 1.29 \ci{-1.59}{4.18} & $-3.70$ \ci{-7.29}{-0.25} \\” | -1.59 | -1.5911 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.21` |
| `R1.supp-tab-appcampaignfs.22` | 4.18 — “T5: c40-exposure effect & 1.29 \ci{-1.59}{4.18} & $-3.70$ \ci{-7.29}{-0.25} \\” | 4.18 | 4.1845 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.22` |
| `R1.supp-tab-appcampaignfs.23` | -3.70 — “T5: c40-exposure effect & 1.29 \ci{-1.59}{4.18} & $-3.70$ \ci{-7.29}{-0.25} \\” | -3.70 | -3.6981 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.23` |
| `R1.supp-tab-appcampaignfs.24` | -7.29 — “T5: c40-exposure effect & 1.29 \ci{-1.59}{4.18} & $-3.70$ \ci{-7.29}{-0.25} \\” | -7.29 | -7.2911 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.24` |
| `R1.supp-tab-appcampaignfs.25` | -0.25 — “T5: c40-exposure effect & 1.29 \ci{-1.59}{4.18} & $-3.70$ \ci{-7.29}{-0.25} \\” | -0.25 | -0.2490 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.25` |
| `R1.supp-tab-appcampaignfs.26` | -1.05 — “T1: E1 $-$ Fair-N & $-1.05$ \ci{-5.70}{3.55} & 4.29 \ci{-2.99}{11.63} \\” | -1.05 | -1.0510 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.26` |
| `R1.supp-tab-appcampaignfs.27` | -5.70 — “T1: E1 $-$ Fair-N & $-1.05$ \ci{-5.70}{3.55} & 4.29 \ci{-2.99}{11.63} \\” | -5.70 | -5.6991 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.27` |
| `R1.supp-tab-appcampaignfs.28` | 3.55 — “T1: E1 $-$ Fair-N & $-1.05$ \ci{-5.70}{3.55} & 4.29 \ci{-2.99}{11.63} \\” | 3.55 | 3.5459 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.28` |
| `R1.supp-tab-appcampaignfs.29` | 4.29 — “T1: E1 $-$ Fair-N & $-1.05$ \ci{-5.70}{3.55} & 4.29 \ci{-2.99}{11.63} \\” | 4.29 | 4.2857 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.29` |
| `R1.supp-tab-appcampaignfs.30` | -2.99 — “T1: E1 $-$ Fair-N & $-1.05$ \ci{-5.70}{3.55} & 4.29 \ci{-2.99}{11.63} \\” | -2.99 | -2.9949 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.30` |
| `R1.supp-tab-appcampaignfs.31` | 11.63 — “T1: E1 $-$ Fair-N & $-1.05$ \ci{-5.70}{3.55} & 4.29 \ci{-2.99}{11.63} \\” | 11.63 | 11.63 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.31` |
| `R1.supp-tab-appcampaignfs.32` | -0.33 — “T3 denominator & $-0.33$ \ci{-4.97}{4.28} & $-2.53$ \ci{-8.19}{3.74} \\” | -0.33 | -0.3316 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.32` |
| `R1.supp-tab-appcampaignfs.33` | -4.97 — “T3 denominator & $-0.33$ \ci{-4.97}{4.28} & $-2.53$ \ci{-8.19}{3.74} \\” | -4.97 | -4.9745 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.33` |
| `R1.supp-tab-appcampaignfs.34` | 4.28 — “T3 denominator & $-0.33$ \ci{-4.97}{4.28} & $-2.53$ \ci{-8.19}{3.74} \\” | 4.28 | 4.2758 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.34` |
| `R1.supp-tab-appcampaignfs.35` | -2.53 — “T3 denominator & $-0.33$ \ci{-4.97}{4.28} & $-2.53$ \ci{-8.19}{3.74} \\” | -2.53 | -2.5255 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.35` |
| `R1.supp-tab-appcampaignfs.36` | -8.19 — “T3 denominator & $-0.33$ \ci{-4.97}{4.28} & $-2.53$ \ci{-8.19}{3.74} \\” | -8.19 | -8.1940 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.36` |
| `R1.supp-tab-appcampaignfs.37` | 3.74 — “T3 denominator & $-0.33$ \ci{-4.97}{4.28} & $-2.53$ \ci{-8.19}{3.74} \\” | 3.74 | 3.7398 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.37` |
| `R1.supp-tab-appcampaignfs.38` | 1.05 — “T4: codec effect & 1.05 \ci{-3.30}{5.47} & 4.92 \ci{-0.66}{10.92} \\” | 1.05 | 1.0459 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.38` |
| `R1.supp-tab-appcampaignfs.39` | -3.30 — “T4: codec effect & 1.05 \ci{-3.30}{5.47} & 4.92 \ci{-0.66}{10.92} \\” | -3.30 | -3.2985 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.39` |
| `R1.supp-tab-appcampaignfs.40` | 5.47 — “T4: codec effect & 1.05 \ci{-3.30}{5.47} & 4.92 \ci{-0.66}{10.92} \\” | 5.47 | 5.4694 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.40` |
| `R1.supp-tab-appcampaignfs.41` | 4.92 — “T4: codec effect & 1.05 \ci{-3.30}{5.47} & 4.92 \ci{-0.66}{10.92} \\” | 4.92 | 4.9158 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.41` |
| `R1.supp-tab-appcampaignfs.42` | -0.66 — “T4: codec effect & 1.05 \ci{-3.30}{5.47} & 4.92 \ci{-0.66}{10.92} \\” | -0.66 | -0.6610 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.42` |
| `R1.supp-tab-appcampaignfs.43` | 10.92 — “T4: codec effect & 1.05 \ci{-3.30}{5.47} & 4.92 \ci{-0.66}{10.92} \\” | 10.92 | 10.92 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.43` |
| `R1.supp-tab-appcampaignfs.44` | 1.45 — “T5: c40-exposure effect & 1.45 \ci{-1.60}{4.62} & $-3.50$ \ci{-7.70}{0.06} \\” | 1.45 | 1.4490 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.44` |
| `R1.supp-tab-appcampaignfs.45` | -1.60 — “T5: c40-exposure effect & 1.45 \ci{-1.60}{4.62} & $-3.50$ \ci{-7.70}{0.06} \\” | -1.60 | -1.6047 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.45` |
| `R1.supp-tab-appcampaignfs.46` | 4.62 — “T5: c40-exposure effect & 1.45 \ci{-1.60}{4.62} & $-3.50$ \ci{-7.70}{0.06} \\” | 4.62 | 4.6200 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.46` |
| `R1.supp-tab-appcampaignfs.47` | -3.50 — “T5: c40-exposure effect & 1.45 \ci{-1.60}{4.62} & $-3.50$ \ci{-7.70}{0.06} \\” | -3.50 | -3.5026 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.47` |
| `R1.supp-tab-appcampaignfs.48` | -7.70 — “T5: c40-exposure effect & 1.45 \ci{-1.60}{4.62} & $-3.50$ \ci{-7.70}{0.06} \\” | -7.70 | -7.7015 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.48` |
| `R1.supp-tab-appcampaignfs.49` | 0.06 — “T5: c40-exposure effect & 1.45 \ci{-1.60}{4.62} & $-3.50$ \ci{-7.70}{0.06} \\” | 0.06 | 0.0587 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcampaignfs.49` |

## R1.supp-The-pm1-point-check-post-hoc — Revision 1 — Supplementary Material, §“The pm1-point check (post hoc)”

*Supplementary Material, §“The pm1-point check (post hoc)”*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-The-pm1-point-check-post-hoc.1` | 0.15 — “margin: T1 \ci{0.15}{1.68}, T2 \ci{0.21}{1.32}, T4 \ci{5.48}{9.56} and T5” | 0.15 | 0.1488 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-The-pm1-point-check-post-hoc.1` |
| `R1.supp-The-pm1-point-check-post-hoc.2` | 1.68 — “margin: T1 \ci{0.15}{1.68}, T2 \ci{0.21}{1.32}, T4 \ci{5.48}{9.56} and T5” | 1.68 | 1.6786 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-The-pm1-point-check-post-hoc.2` |
| `R1.supp-The-pm1-point-check-post-hoc.3` | 0.21 — “margin: T1 \ci{0.15}{1.68}, T2 \ci{0.21}{1.32}, T4 \ci{5.48}{9.56} and T5” | 0.21 | 0.2120 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-The-pm1-point-check-post-hoc.3` |
| `R1.supp-The-pm1-point-check-post-hoc.4` | 1.32 — “margin: T1 \ci{0.15}{1.68}, T2 \ci{0.21}{1.32}, T4 \ci{5.48}{9.56} and T5” | 1.32 | 1.3187 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-The-pm1-point-check-post-hoc.4` |
| `R1.supp-The-pm1-point-check-post-hoc.5` | 5.48 — “margin: T1 \ci{0.15}{1.68}, T2 \ci{0.21}{1.32}, T4 \ci{5.48}{9.56} and T5” | 5.48 | 5.4757 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-The-pm1-point-check-post-hoc.5` |
| `R1.supp-The-pm1-point-check-post-hoc.6` | 9.56 — “margin: T1 \ci{0.15}{1.68}, T2 \ci{0.21}{1.32}, T4 \ci{5.48}{9.56} and T5” | 9.56 | 9.5604 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-The-pm1-point-check-post-hoc.6` |
| `R1.supp-The-pm1-point-check-post-hoc.7` | 0.97 — “\ci{0.97}{2.78}\,pt (90\% intervals; T3 is a ratio and is not checked).” | 0.97 | 0.9681 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-The-pm1-point-check-post-hoc.7` |
| `R1.supp-The-pm1-point-check-post-hoc.8` | 2.78 — “\ci{0.97}{2.78}\,pt (90\% intervals; T3 is a ratio and is not checked).” | 2.78 | 2.7773 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-The-pm1-point-check-post-hoc.8` |

## R1.supp-tab-apphealth — Revision 1 — Supplementary Material, tab:apphealth

*Supplementary Material, tab:apphealth; `\label{tab:apphealth}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-tab-apphealth.1` | 4 — “E1, seed 42 & 4 & 0.9531 & 0.8359 (3) & 0.16925 & 0.29139 & 0.99149 / 0.97037 & 0.99189 / ” | 4 | 4.0000 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.1` |
| `R1.supp-tab-apphealth.2` | 0.9531 — “E1, seed 42 & 4 & 0.9531 & 0.8359 (3) & 0.16925 & 0.29139 & 0.99149 / 0.97037 & 0.99189 / ” | 0.9531 | 0.9531 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.2` |
| `R1.supp-tab-apphealth.3` | 0.8359 — “E1, seed 42 & 4 & 0.9531 & 0.8359 (3) & 0.16925 & 0.29139 & 0.99149 / 0.97037 & 0.99189 / ” | 0.8359 | 0.8359 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.3` |
| `R1.supp-tab-apphealth.4` | 3 — “E1, seed 42 & 4 & 0.9531 & 0.8359 (3) & 0.16925 & 0.29139 & 0.99149 / 0.97037 & 0.99189 / ” | 3 | 3.0000 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.4` |
| `R1.supp-tab-apphealth.5` | 0.16925 — “E1, seed 42 & 4 & 0.9531 & 0.8359 (3) & 0.16925 & 0.29139 & 0.99149 / 0.97037 & 0.99189 / ” | 0.16925 | 0.1693 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.5` |
| `R1.supp-tab-apphealth.6` | 0.29139 — “E1, seed 42 & 4 & 0.9531 & 0.8359 (3) & 0.16925 & 0.29139 & 0.99149 / 0.97037 & 0.99189 / ” | 0.29139 | 0.2914 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.6` |
| `R1.supp-tab-apphealth.7` | 0.99149 — “E1, seed 42 & 4 & 0.9531 & 0.8359 (3) & 0.16925 & 0.29139 & 0.99149 / 0.97037 & 0.99189 / ” | 0.99149 | 0.9915 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.7` |
| `R1.supp-tab-apphealth.8` | 0.97037 — “E1, seed 42 & 4 & 0.9531 & 0.8359 (3) & 0.16925 & 0.29139 & 0.99149 / 0.97037 & 0.99189 / ” | 0.97037 | 0.9704 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.8` |
| `R1.supp-tab-apphealth.9` | 0.99189 — “E1, seed 42 & 4 & 0.9531 & 0.8359 (3) & 0.16925 & 0.29139 & 0.99149 / 0.97037 & 0.99189 / ” | 0.99189 | 0.9919 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.9` |
| `R1.supp-tab-apphealth.10` | 0.96614 — “E1, seed 42 & 4 & 0.9531 & 0.8359 (3) & 0.16925 & 0.29139 & 0.99149 / 0.97037 & 0.99189 / ” | 0.96614 | 0.9661 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.10` |
| `R1.supp-tab-apphealth.11` | 3 — “E1, seed 1 & 3 & 1.0000 & 0.9805 (6) & 0.16672 & 0.23106 & 0.99102 / 0.96407 & 0.99079 / 0” | 3 | 3.0000 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.11` |
| `R1.supp-tab-apphealth.12` | 1.0000 — “E1, seed 1 & 3 & 1.0000 & 0.9805 (6) & 0.16672 & 0.23106 & 0.99102 / 0.96407 & 0.99079 / 0” | 1.0000 | 1.0000 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.12` |
| `R1.supp-tab-apphealth.13` | 0.9805 — “E1, seed 1 & 3 & 1.0000 & 0.9805 (6) & 0.16672 & 0.23106 & 0.99102 / 0.96407 & 0.99079 / 0” | 0.9805 | 0.9805 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.13` |
| `R1.supp-tab-apphealth.14` | 6 — “E1, seed 1 & 3 & 1.0000 & 0.9805 (6) & 0.16672 & 0.23106 & 0.99102 / 0.96407 & 0.99079 / 0” | 6 | 6.0000 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.14` |
| `R1.supp-tab-apphealth.15` | 0.16672 — “E1, seed 1 & 3 & 1.0000 & 0.9805 (6) & 0.16672 & 0.23106 & 0.99102 / 0.96407 & 0.99079 / 0” | 0.16672 | 0.1667 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.15` |
| `R1.supp-tab-apphealth.16` | 0.23106 — “E1, seed 1 & 3 & 1.0000 & 0.9805 (6) & 0.16672 & 0.23106 & 0.99102 / 0.96407 & 0.99079 / 0” | 0.23106 | 0.2311 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.16` |
| `R1.supp-tab-apphealth.17` | 0.99102 — “E1, seed 1 & 3 & 1.0000 & 0.9805 (6) & 0.16672 & 0.23106 & 0.99102 / 0.96407 & 0.99079 / 0” | 0.99102 | 0.9910 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.17` |
| `R1.supp-tab-apphealth.18` | 0.96407 — “E1, seed 1 & 3 & 1.0000 & 0.9805 (6) & 0.16672 & 0.23106 & 0.99102 / 0.96407 & 0.99079 / 0” | 0.96407 | 0.9641 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.18` |
| `R1.supp-tab-apphealth.19` | 0.99079 — “E1, seed 1 & 3 & 1.0000 & 0.9805 (6) & 0.16672 & 0.23106 & 0.99102 / 0.96407 & 0.99079 / 0” | 0.99079 | 0.9908 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.19` |
| `R1.supp-tab-apphealth.20` | 0.94705 — “E1, seed 1 & 3 & 1.0000 & 0.9805 (6) & 0.16672 & 0.23106 & 0.99102 / 0.96407 & 0.99079 / 0” | 0.94705 | 0.9470 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.20` |
| `R1.supp-tab-apphealth.21` | 6 — “E1, seed 2 & 6 & 1.0000 & 0.3672 (2) & 0.16588 & 0.38080 & 0.99172 / 0.96352 & 0.98737 / 0” | 6 | 6.0000 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.21` |
| `R1.supp-tab-apphealth.22` | 1.0000 — “E1, seed 2 & 6 & 1.0000 & 0.3672 (2) & 0.16588 & 0.38080 & 0.99172 / 0.96352 & 0.98737 / 0” | 1.0000 | 1.0000 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.22` |
| `R1.supp-tab-apphealth.23` | 0.3672 — “E1, seed 2 & 6 & 1.0000 & 0.3672 (2) & 0.16588 & 0.38080 & 0.99172 / 0.96352 & 0.98737 / 0” | 0.3672 | 0.3672 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.23` |
| `R1.supp-tab-apphealth.24` | 2 — “E1, seed 2 & 6 & 1.0000 & 0.3672 (2) & 0.16588 & 0.38080 & 0.99172 / 0.96352 & 0.98737 / 0” | 2 | 2.0000 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.24` |
| `R1.supp-tab-apphealth.25` | 0.16588 — “E1, seed 2 & 6 & 1.0000 & 0.3672 (2) & 0.16588 & 0.38080 & 0.99172 / 0.96352 & 0.98737 / 0” | 0.16588 | 0.1659 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.25` |
| `R1.supp-tab-apphealth.26` | 0.38080 — “E1, seed 2 & 6 & 1.0000 & 0.3672 (2) & 0.16588 & 0.38080 & 0.99172 / 0.96352 & 0.98737 / 0” | 0.38080 | 0.3808 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.26` |
| `R1.supp-tab-apphealth.27` | 0.99172 — “E1, seed 2 & 6 & 1.0000 & 0.3672 (2) & 0.16588 & 0.38080 & 0.99172 / 0.96352 & 0.98737 / 0” | 0.99172 | 0.9917 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.27` |
| `R1.supp-tab-apphealth.28` | 0.96352 — “E1, seed 2 & 6 & 1.0000 & 0.3672 (2) & 0.16588 & 0.38080 & 0.99172 / 0.96352 & 0.98737 / 0” | 0.96352 | 0.9635 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.28` |
| `R1.supp-tab-apphealth.29` | 0.98737 — “E1, seed 2 & 6 & 1.0000 & 0.3672 (2) & 0.16588 & 0.38080 & 0.99172 / 0.96352 & 0.98737 / 0” | 0.98737 | 0.9874 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.29` |
| `R1.supp-tab-apphealth.30` | 0.95105 — “E1, seed 2 & 6 & 1.0000 & 0.3672 (2) & 0.16588 & 0.38080 & 0.99172 / 0.96352 & 0.98737 / 0” | 0.95105 | 0.9510 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.30` |
| `R1.supp-tab-apphealth.31` | 5 — “Fair-N, seed 42 & 5 & 1.0000 & 0.8945 (19) & --- & 0.00000 & 0.99009 / 0.96397 & --- \\” | 5 | 5.0000 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.31` |
| `R1.supp-tab-apphealth.32` | 1.0000 — “Fair-N, seed 42 & 5 & 1.0000 & 0.8945 (19) & --- & 0.00000 & 0.99009 / 0.96397 & --- \\” | 1.0000 | 1.0000 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.32` |
| `R1.supp-tab-apphealth.33` | 0.8945 — “Fair-N, seed 42 & 5 & 1.0000 & 0.8945 (19) & --- & 0.00000 & 0.99009 / 0.96397 & --- \\” | 0.8945 | 0.8945 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.33` |
| `R1.supp-tab-apphealth.34` | 19 — “Fair-N, seed 42 & 5 & 1.0000 & 0.8945 (19) & --- & 0.00000 & 0.99009 / 0.96397 & --- \\” | 19 | 19.00 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.34` |
| `R1.supp-tab-apphealth.35` | 0.00000 — “Fair-N, seed 42 & 5 & 1.0000 & 0.8945 (19) & --- & 0.00000 & 0.99009 / 0.96397 & --- \\” | 0.00000 | 0.0000 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.35` |
| `R1.supp-tab-apphealth.36` | 0.99009 — “Fair-N, seed 42 & 5 & 1.0000 & 0.8945 (19) & --- & 0.00000 & 0.99009 / 0.96397 & --- \\” | 0.99009 | 0.9901 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.36` |
| `R1.supp-tab-apphealth.37` | 0.96397 — “Fair-N, seed 42 & 5 & 1.0000 & 0.8945 (19) & --- & 0.00000 & 0.99009 / 0.96397 & --- \\” | 0.96397 | 0.9640 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.37` |
| `R1.supp-tab-apphealth.38` | 13 — “Fair-N, seed 1 & 13 & 1.0000 & 0.9727 (8) & --- & 0.31757 & 0.99126 / 0.96524 & --- \\” | 13 | 13.00 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.38` |
| `R1.supp-tab-apphealth.39` | 1.0000 — “Fair-N, seed 1 & 13 & 1.0000 & 0.9727 (8) & --- & 0.31757 & 0.99126 / 0.96524 & --- \\” | 1.0000 | 1.0000 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.39` |
| `R1.supp-tab-apphealth.40` | 0.9727 — “Fair-N, seed 1 & 13 & 1.0000 & 0.9727 (8) & --- & 0.31757 & 0.99126 / 0.96524 & --- \\” | 0.9727 | 0.9727 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.40` |
| `R1.supp-tab-apphealth.41` | 8 — “Fair-N, seed 1 & 13 & 1.0000 & 0.9727 (8) & --- & 0.31757 & 0.99126 / 0.96524 & --- \\” | 8 | 8.0000 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.41` |
| `R1.supp-tab-apphealth.42` | 0.31757 — “Fair-N, seed 1 & 13 & 1.0000 & 0.9727 (8) & --- & 0.31757 & 0.99126 / 0.96524 & --- \\” | 0.31757 | 0.3176 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.42` |
| `R1.supp-tab-apphealth.43` | 0.99126 — “Fair-N, seed 1 & 13 & 1.0000 & 0.9727 (8) & --- & 0.31757 & 0.99126 / 0.96524 & --- \\” | 0.99126 | 0.9913 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.43` |
| `R1.supp-tab-apphealth.44` | 0.96524 — “Fair-N, seed 1 & 13 & 1.0000 & 0.9727 (8) & --- & 0.31757 & 0.99126 / 0.96524 & --- \\” | 0.96524 | 0.9652 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.44` |
| `R1.supp-tab-apphealth.45` | 12 — “Fair-N, seed 2 & 12 & 1.0000 & 0.8438 (11) & --- & 0.23106 & 0.98968 / 0.96383 & --- \\” | 12 | 12.00 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.45` |
| `R1.supp-tab-apphealth.46` | 1.0000 — “Fair-N, seed 2 & 12 & 1.0000 & 0.8438 (11) & --- & 0.23106 & 0.98968 / 0.96383 & --- \\” | 1.0000 | 1.0000 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.46` |
| `R1.supp-tab-apphealth.47` | 0.8438 — “Fair-N, seed 2 & 12 & 1.0000 & 0.8438 (11) & --- & 0.23106 & 0.98968 / 0.96383 & --- \\” | 0.8438 | 0.8438 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.47` |
| `R1.supp-tab-apphealth.48` | 11 — “Fair-N, seed 2 & 12 & 1.0000 & 0.8438 (11) & --- & 0.23106 & 0.98968 / 0.96383 & --- \\” | 11 | 11.00 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.48` |
| `R1.supp-tab-apphealth.49` | 0.23106 — “Fair-N, seed 2 & 12 & 1.0000 & 0.8438 (11) & --- & 0.23106 & 0.98968 / 0.96383 & --- \\” | 0.23106 | 0.2311 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.49` |
| `R1.supp-tab-apphealth.50` | 0.98968 — “Fair-N, seed 2 & 12 & 1.0000 & 0.8438 (11) & --- & 0.23106 & 0.98968 / 0.96383 & --- \\” | 0.98968 | 0.9897 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.50` |
| `R1.supp-tab-apphealth.51` | 0.96383 — “Fair-N, seed 2 & 12 & 1.0000 & 0.8438 (11) & --- & 0.23106 & 0.98968 / 0.96383 & --- \\” | 0.96383 | 0.9638 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-apphealth.51` |

## R1.supp-app-exploratory — Revision 1 — Supplementary Material, app:exploratory

*Supplementary Material, app:exploratory; `\label{app:exploratory}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-app-exploratory.1` | 10,000 — “hierarchical bootstrap of the registered tests ($B = 10{,}000$; each arm's” | 10000 | 10000.00 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-exploratory.1` |
| `R1.supp-app-exploratory.2` | 4 — “(one WildDeepfake sequence: 4), and a video with several face tracks takes” | 4 | 4.0000 | `predictions/wilddeepfake/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py R1.supp-app-exploratory.2` |

## R1.supp-Other-corpora-DFDC-WildDeepfake-and-Celeb-DF-r — Revision 1 — Supplementary Material, §“Other corpora: DFDC, WildDeepfake and Celeb-DF r”

*Supplementary Material, §“Other corpora: DFDC, WildDeepfake and Celeb-DF r”*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-Other-corpora-DFDC-WildDeepfake-and-Celeb-DF-r.1` | 4 — “in only 4 frames and is scored on those crops. On Celeb-DF, 36 of the 518 videos have” | 4 | 4.0000 | `predictions/wilddeepfake/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py R1.supp-Other-corpora-DFDC-WildDeepfake-and-Celeb-DF-r.1` |
| `R1.supp-Other-corpora-DFDC-WildDeepfake-and-Celeb-DF-r.2` | 36 — “in only 4 frames and is scored on those crops. On Celeb-DF, 36 of the 518 videos have” | 36 | 36.00 | `predictions/celebdf_v2_recrop/track/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py R1.supp-Other-corpora-DFDC-WildDeepfake-and-Celeb-DF-r.2` |
| `R1.supp-Other-corpora-DFDC-WildDeepfake-and-Celeb-DF-r.3` | 518 — “in only 4 frames and is scored on those crops. On Celeb-DF, 36 of the 518 videos have” | 518 | 518.00 | `predictions/celebdf_v2_recrop/track/b7_effnet_b0_mq_fliponly.json` | `python verify/claim.py R1.supp-Other-corpora-DFDC-WildDeepfake-and-Celeb-DF-r.3` |

## R1.supp-tab-appexpcorpora — Revision 1 — Supplementary Material, tab:appexpcorpora

*Supplementary Material, tab:appexpcorpora; `\label{tab:appexpcorpora}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-tab-appexpcorpora.1` | 10,000 — “($B = 10{,}000$; seeds, then the clusters: 500 real--fake pairs on DFDC, 115” | 10000 | 10000.00 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.1` |
| `R1.supp-tab-appexpcorpora.2` | 73.07 — “E1 (EMA) & 73.07 \ci{68.93}{77.58} & 71.22 \ci{63.37}{77.74} & 68.98 \ci{64.05}{73.70} & 6” | 73.07 | 73.07 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.2` |
| `R1.supp-tab-appexpcorpora.3` | 68.93 — “E1 (EMA) & 73.07 \ci{68.93}{77.58} & 71.22 \ci{63.37}{77.74} & 68.98 \ci{64.05}{73.70} & 6” | 68.93 | 68.93 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.3` |
| `R1.supp-tab-appexpcorpora.4` | 77.58 — “E1 (EMA) & 73.07 \ci{68.93}{77.58} & 71.22 \ci{63.37}{77.74} & 68.98 \ci{64.05}{73.70} & 6” | 77.58 | 77.58 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.4` |
| `R1.supp-tab-appexpcorpora.5` | 71.22 — “E1 (EMA) & 73.07 \ci{68.93}{77.58} & 71.22 \ci{63.37}{77.74} & 68.98 \ci{64.05}{73.70} & 6” | 71.22 | 71.22 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.5` |
| `R1.supp-tab-appexpcorpora.6` | 63.37 — “E1 (EMA) & 73.07 \ci{68.93}{77.58} & 71.22 \ci{63.37}{77.74} & 68.98 \ci{64.05}{73.70} & 6” | 63.37 | 63.37 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.6` |
| `R1.supp-tab-appexpcorpora.7` | 77.74 — “E1 (EMA) & 73.07 \ci{68.93}{77.58} & 71.22 \ci{63.37}{77.74} & 68.98 \ci{64.05}{73.70} & 6” | 77.74 | 77.74 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.7` |
| `R1.supp-tab-appexpcorpora.8` | 68.98 — “E1 (EMA) & 73.07 \ci{68.93}{77.58} & 71.22 \ci{63.37}{77.74} & 68.98 \ci{64.05}{73.70} & 6” | 68.98 | 68.98 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.8` |
| `R1.supp-tab-appexpcorpora.9` | 64.05 — “E1 (EMA) & 73.07 \ci{68.93}{77.58} & 71.22 \ci{63.37}{77.74} & 68.98 \ci{64.05}{73.70} & 6” | 64.05 | 64.05 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.9` |
| `R1.supp-tab-appexpcorpora.10` | 73.70 — “E1 (EMA) & 73.07 \ci{68.93}{77.58} & 71.22 \ci{63.37}{77.74} & 68.98 \ci{64.05}{73.70} & 6” | 73.70 | 73.70 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.10` |
| `R1.supp-tab-appexpcorpora.11` | 68.91 — “E1 (EMA) & 73.07 \ci{68.93}{77.58} & 71.22 \ci{63.37}{77.74} & 68.98 \ci{64.05}{73.70} & 6” | 68.91 | 68.91 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.11` |
| `R1.supp-tab-appexpcorpora.12` | 64.01 — “E1 (EMA) & 73.07 \ci{68.93}{77.58} & 71.22 \ci{63.37}{77.74} & 68.98 \ci{64.05}{73.70} & 6” | 64.01 | 64.01 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.12` |
| `R1.supp-tab-appexpcorpora.13` | 73.46 — “E1 (EMA) & 73.07 \ci{68.93}{77.58} & 71.22 \ci{63.37}{77.74} & 68.98 \ci{64.05}{73.70} & 6” | 73.46 | 73.46 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.13` |
| `R1.supp-tab-appexpcorpora.14` | -0.07 — “E1 (EMA) & 73.07 \ci{68.93}{77.58} & 71.22 \ci{63.37}{77.74} & 68.98 \ci{64.05}{73.70} & 6” | -0.07 | -0.0677 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.14` |
| `R1.supp-tab-appexpcorpora.15` | -1.19 — “E1 (EMA) & 73.07 \ci{68.93}{77.58} & 71.22 \ci{63.37}{77.74} & 68.98 \ci{64.05}{73.70} & 6” | -1.19 | -1.1943 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.15` |
| `R1.supp-tab-appexpcorpora.16` | 1.16 — “E1 (EMA) & 73.07 \ci{68.93}{77.58} & 71.22 \ci{63.37}{77.74} & 68.98 \ci{64.05}{73.70} & 6” | 1.16 | 1.1561 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.16` |
| `R1.supp-tab-appexpcorpora.17` | 66.71 — “Fair-N (EMA) & 66.71 \ci{59.00}{73.50} & 69.36 \ci{61.35}{76.55} & 64.73 \ci{56.24}{72.24}” | 66.71 | 66.71 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.17` |
| `R1.supp-tab-appexpcorpora.18` | 59.00 — “Fair-N (EMA) & 66.71 \ci{59.00}{73.50} & 69.36 \ci{61.35}{76.55} & 64.73 \ci{56.24}{72.24}” | 59.00 | 59.00 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.18` |
| `R1.supp-tab-appexpcorpora.19` | 73.50 — “Fair-N (EMA) & 66.71 \ci{59.00}{73.50} & 69.36 \ci{61.35}{76.55} & 64.73 \ci{56.24}{72.24}” | 73.50 | 73.50 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.19` |
| `R1.supp-tab-appexpcorpora.20` | 69.36 — “Fair-N (EMA) & 66.71 \ci{59.00}{73.50} & 69.36 \ci{61.35}{76.55} & 64.73 \ci{56.24}{72.24}” | 69.36 | 69.36 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.20` |
| `R1.supp-tab-appexpcorpora.21` | 61.35 — “Fair-N (EMA) & 66.71 \ci{59.00}{73.50} & 69.36 \ci{61.35}{76.55} & 64.73 \ci{56.24}{72.24}” | 61.35 | 61.35 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.21` |
| `R1.supp-tab-appexpcorpora.22` | 76.55 — “Fair-N (EMA) & 66.71 \ci{59.00}{73.50} & 69.36 \ci{61.35}{76.55} & 64.73 \ci{56.24}{72.24}” | 76.55 | 76.55 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.22` |
| `R1.supp-tab-appexpcorpora.23` | 64.73 — “Fair-N (EMA) & 66.71 \ci{59.00}{73.50} & 69.36 \ci{61.35}{76.55} & 64.73 \ci{56.24}{72.24}” | 64.73 | 64.73 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.23` |
| `R1.supp-tab-appexpcorpora.24` | 56.24 — “Fair-N (EMA) & 66.71 \ci{59.00}{73.50} & 69.36 \ci{61.35}{76.55} & 64.73 \ci{56.24}{72.24}” | 56.24 | 56.24 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.24` |
| `R1.supp-tab-appexpcorpora.25` | 72.24 — “Fair-N (EMA) & 66.71 \ci{59.00}{73.50} & 69.36 \ci{61.35}{76.55} & 64.73 \ci{56.24}{72.24}” | 72.24 | 72.24 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.25` |
| `R1.supp-tab-appexpcorpora.26` | 64.86 — “Fair-N (EMA) & 66.71 \ci{59.00}{73.50} & 69.36 \ci{61.35}{76.55} & 64.73 \ci{56.24}{72.24}” | 64.86 | 64.86 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.26` |
| `R1.supp-tab-appexpcorpora.27` | 56.20 — “Fair-N (EMA) & 66.71 \ci{59.00}{73.50} & 69.36 \ci{61.35}{76.55} & 64.73 \ci{56.24}{72.24}” | 56.20 | 56.20 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.27` |
| `R1.supp-tab-appexpcorpora.28` | 72.39 — “Fair-N (EMA) & 66.71 \ci{59.00}{73.50} & 69.36 \ci{61.35}{76.55} & 64.73 \ci{56.24}{72.24}” | 72.39 | 72.39 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.28` |
| `R1.supp-tab-appexpcorpora.29` | 0.13 — “Fair-N (EMA) & 66.71 \ci{59.00}{73.50} & 69.36 \ci{61.35}{76.55} & 64.73 \ci{56.24}{72.24}” | 0.13 | 0.1250 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.29` |
| `R1.supp-tab-appexpcorpora.30` | -0.46 — “Fair-N (EMA) & 66.71 \ci{59.00}{73.50} & 69.36 \ci{61.35}{76.55} & 64.73 \ci{56.24}{72.24}” | -0.46 | -0.4602 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.30` |
| `R1.supp-tab-appexpcorpora.31` | 0.98 — “Fair-N (EMA) & 66.71 \ci{59.00}{73.50} & 69.36 \ci{61.35}{76.55} & 64.73 \ci{56.24}{72.24}” | 0.98 | 0.9756 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.31` |
| `R1.supp-tab-appexpcorpora.32` | 71.64 — “Fair-W (EMA) & 71.64 \ci{68.70}{74.64} & 70.44 \ci{61.77}{77.59} & 68.08 \ci{62.55}{73.37}” | 71.64 | 71.64 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.32` |
| `R1.supp-tab-appexpcorpora.33` | 68.70 — “Fair-W (EMA) & 71.64 \ci{68.70}{74.64} & 70.44 \ci{61.77}{77.59} & 68.08 \ci{62.55}{73.37}” | 68.70 | 68.70 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.33` |
| `R1.supp-tab-appexpcorpora.34` | 74.64 — “Fair-W (EMA) & 71.64 \ci{68.70}{74.64} & 70.44 \ci{61.77}{77.59} & 68.08 \ci{62.55}{73.37}” | 74.64 | 74.64 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.34` |
| `R1.supp-tab-appexpcorpora.35` | 70.44 — “Fair-W (EMA) & 71.64 \ci{68.70}{74.64} & 70.44 \ci{61.77}{77.59} & 68.08 \ci{62.55}{73.37}” | 70.44 | 70.44 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.35` |
| `R1.supp-tab-appexpcorpora.36` | 61.77 — “Fair-W (EMA) & 71.64 \ci{68.70}{74.64} & 70.44 \ci{61.77}{77.59} & 68.08 \ci{62.55}{73.37}” | 61.77 | 61.77 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.36` |
| `R1.supp-tab-appexpcorpora.37` | 77.59 — “Fair-W (EMA) & 71.64 \ci{68.70}{74.64} & 70.44 \ci{61.77}{77.59} & 68.08 \ci{62.55}{73.37}” | 77.59 | 77.59 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.37` |
| `R1.supp-tab-appexpcorpora.38` | 68.08 — “Fair-W (EMA) & 71.64 \ci{68.70}{74.64} & 70.44 \ci{61.77}{77.59} & 68.08 \ci{62.55}{73.37}” | 68.08 | 68.08 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.38` |
| `R1.supp-tab-appexpcorpora.39` | 62.55 — “Fair-W (EMA) & 71.64 \ci{68.70}{74.64} & 70.44 \ci{61.77}{77.59} & 68.08 \ci{62.55}{73.37}” | 62.55 | 62.55 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.39` |
| `R1.supp-tab-appexpcorpora.40` | 73.37 — “Fair-W (EMA) & 71.64 \ci{68.70}{74.64} & 70.44 \ci{61.77}{77.59} & 68.08 \ci{62.55}{73.37}” | 73.37 | 73.37 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.40` |
| `R1.supp-tab-appexpcorpora.41` | 68.25 — “Fair-W (EMA) & 71.64 \ci{68.70}{74.64} & 70.44 \ci{61.77}{77.59} & 68.08 \ci{62.55}{73.37}” | 68.25 | 68.25 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.41` |
| `R1.supp-tab-appexpcorpora.42` | 62.73 — “Fair-W (EMA) & 71.64 \ci{68.70}{74.64} & 70.44 \ci{61.77}{77.59} & 68.08 \ci{62.55}{73.37}” | 62.73 | 62.73 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.42` |
| `R1.supp-tab-appexpcorpora.43` | 73.40 — “Fair-W (EMA) & 71.64 \ci{68.70}{74.64} & 70.44 \ci{61.77}{77.59} & 68.08 \ci{62.55}{73.37}” | 73.40 | 73.40 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.43` |
| `R1.supp-tab-appexpcorpora.44` | 0.16 — “Fair-W (EMA) & 71.64 \ci{68.70}{74.64} & 70.44 \ci{61.77}{77.59} & 68.08 \ci{62.55}{73.37}” | 0.16 | 0.1647 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.44` |
| `R1.supp-tab-appexpcorpora.45` | -0.63 — “Fair-W (EMA) & 71.64 \ci{68.70}{74.64} & 70.44 \ci{61.77}{77.59} & 68.08 \ci{62.55}{73.37}” | -0.63 | -0.6288 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.45` |
| `R1.supp-tab-appexpcorpora.46` | 1.00 — “Fair-W (EMA) & 71.64 \ci{68.70}{74.64} & 70.44 \ci{61.77}{77.59} & 68.08 \ci{62.55}{73.37}” | 1.00 | 1.0011 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.46` |
| `R1.supp-tab-appexpcorpora.47` | 72.30 — “CAFRL as specified (EMA) & 72.30 \ci{69.90}{74.83} & 69.42 \ci{61.54}{75.86} & 70.47 \ci{6” | 72.30 | 72.30 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.47` |
| `R1.supp-tab-appexpcorpora.48` | 69.90 — “CAFRL as specified (EMA) & 72.30 \ci{69.90}{74.83} & 69.42 \ci{61.54}{75.86} & 70.47 \ci{6” | 69.90 | 69.90 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.48` |
| `R1.supp-tab-appexpcorpora.49` | 74.83 — “CAFRL as specified (EMA) & 72.30 \ci{69.90}{74.83} & 69.42 \ci{61.54}{75.86} & 70.47 \ci{6” | 74.83 | 74.83 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.49` |
| `R1.supp-tab-appexpcorpora.50` | 69.42 — “CAFRL as specified (EMA) & 72.30 \ci{69.90}{74.83} & 69.42 \ci{61.54}{75.86} & 70.47 \ci{6” | 69.42 | 69.42 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.50` |
| `R1.supp-tab-appexpcorpora.51` | 61.54 — “CAFRL as specified (EMA) & 72.30 \ci{69.90}{74.83} & 69.42 \ci{61.54}{75.86} & 70.47 \ci{6” | 61.54 | 61.54 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.51` |
| `R1.supp-tab-appexpcorpora.52` | 75.86 — “CAFRL as specified (EMA) & 72.30 \ci{69.90}{74.83} & 69.42 \ci{61.54}{75.86} & 70.47 \ci{6” | 75.86 | 75.86 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.52` |
| `R1.supp-tab-appexpcorpora.53` | 70.47 — “CAFRL as specified (EMA) & 72.30 \ci{69.90}{74.83} & 69.42 \ci{61.54}{75.86} & 70.47 \ci{6” | 70.47 | 70.47 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.53` |
| `R1.supp-tab-appexpcorpora.54` | 65.31 — “CAFRL as specified (EMA) & 72.30 \ci{69.90}{74.83} & 69.42 \ci{61.54}{75.86} & 70.47 \ci{6” | 65.31 | 65.31 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.54` |
| `R1.supp-tab-appexpcorpora.55` | 75.36 — “CAFRL as specified (EMA) & 72.30 \ci{69.90}{74.83} & 69.42 \ci{61.54}{75.86} & 70.47 \ci{6” | 75.36 | 75.36 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.55` |
| `R1.supp-tab-appexpcorpora.56` | 70.21 — “CAFRL as specified (EMA) & 72.30 \ci{69.90}{74.83} & 69.42 \ci{61.54}{75.86} & 70.47 \ci{6” | 70.21 | 70.21 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.56` |
| `R1.supp-tab-appexpcorpora.57` | 64.93 — “CAFRL as specified (EMA) & 72.30 \ci{69.90}{74.83} & 69.42 \ci{61.54}{75.86} & 70.47 \ci{6” | 64.93 | 64.93 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.57` |
| `R1.supp-tab-appexpcorpora.58` | 75.12 — “CAFRL as specified (EMA) & 72.30 \ci{69.90}{74.83} & 69.42 \ci{61.54}{75.86} & 70.47 \ci{6” | 75.12 | 75.12 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.58` |
| `R1.supp-tab-appexpcorpora.59` | -0.26 — “CAFRL as specified (EMA) & 72.30 \ci{69.90}{74.83} & 69.42 \ci{61.54}{75.86} & 70.47 \ci{6” | -0.26 | -0.2638 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.59` |
| `R1.supp-tab-appexpcorpora.60` | -1.13 — “CAFRL as specified (EMA) & 72.30 \ci{69.90}{74.83} & 69.42 \ci{61.54}{75.86} & 70.47 \ci{6” | -1.13 | -1.1296 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.60` |
| `R1.supp-tab-appexpcorpora.61` | 0.42 — “CAFRL as specified (EMA) & 72.30 \ci{69.90}{74.83} & 69.42 \ci{61.54}{75.86} & 70.47 \ci{6” | 0.42 | 0.4189 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.61` |
| `R1.supp-tab-appexpcorpora.62` | 69.76 — “SpatialBase (raw) & 69.76 \ci{67.62}{71.98} & 70.64 \ci{62.49}{77.39} & 68.59 \ci{63.63}{7” | 69.76 | 69.76 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.62` |
| `R1.supp-tab-appexpcorpora.63` | 67.62 — “SpatialBase (raw) & 69.76 \ci{67.62}{71.98} & 70.64 \ci{62.49}{77.39} & 68.59 \ci{63.63}{7” | 67.62 | 67.62 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.63` |
| `R1.supp-tab-appexpcorpora.64` | 71.98 — “SpatialBase (raw) & 69.76 \ci{67.62}{71.98} & 70.64 \ci{62.49}{77.39} & 68.59 \ci{63.63}{7” | 71.98 | 71.98 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.64` |
| `R1.supp-tab-appexpcorpora.65` | 70.64 — “SpatialBase (raw) & 69.76 \ci{67.62}{71.98} & 70.64 \ci{62.49}{77.39} & 68.59 \ci{63.63}{7” | 70.64 | 70.64 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.65` |
| `R1.supp-tab-appexpcorpora.66` | 62.49 — “SpatialBase (raw) & 69.76 \ci{67.62}{71.98} & 70.64 \ci{62.49}{77.39} & 68.59 \ci{63.63}{7” | 62.49 | 62.49 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.66` |
| `R1.supp-tab-appexpcorpora.67` | 77.39 — “SpatialBase (raw) & 69.76 \ci{67.62}{71.98} & 70.64 \ci{62.49}{77.39} & 68.59 \ci{63.63}{7” | 77.39 | 77.39 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.67` |
| `R1.supp-tab-appexpcorpora.68` | 68.59 — “SpatialBase (raw) & 69.76 \ci{67.62}{71.98} & 70.64 \ci{62.49}{77.39} & 68.59 \ci{63.63}{7” | 68.59 | 68.59 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.68` |
| `R1.supp-tab-appexpcorpora.69` | 63.63 — “SpatialBase (raw) & 69.76 \ci{67.62}{71.98} & 70.64 \ci{62.49}{77.39} & 68.59 \ci{63.63}{7” | 63.63 | 63.63 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.69` |
| `R1.supp-tab-appexpcorpora.70` | 73.53 — “SpatialBase (raw) & 69.76 \ci{67.62}{71.98} & 70.64 \ci{62.49}{77.39} & 68.59 \ci{63.63}{7” | 73.53 | 73.53 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.70` |
| `R1.supp-tab-appexpcorpora.71` | 68.89 — “SpatialBase (raw) & 69.76 \ci{67.62}{71.98} & 70.64 \ci{62.49}{77.39} & 68.59 \ci{63.63}{7” | 68.89 | 68.89 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.71` |
| `R1.supp-tab-appexpcorpora.72` | 63.98 — “SpatialBase (raw) & 69.76 \ci{67.62}{71.98} & 70.64 \ci{62.49}{77.39} & 68.59 \ci{63.63}{7” | 63.98 | 63.98 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.72` |
| `R1.supp-tab-appexpcorpora.73` | 73.68 — “SpatialBase (raw) & 69.76 \ci{67.62}{71.98} & 70.64 \ci{62.49}{77.39} & 68.59 \ci{63.63}{7” | 73.68 | 73.68 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.73` |
| `R1.supp-tab-appexpcorpora.74` | 0.29 — “SpatialBase (raw) & 69.76 \ci{67.62}{71.98} & 70.64 \ci{62.49}{77.39} & 68.59 \ci{63.63}{7” | 0.29 | 0.2936 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.74` |
| `R1.supp-tab-appexpcorpora.75` | -0.34 — “SpatialBase (raw) & 69.76 \ci{67.62}{71.98} & 70.64 \ci{62.49}{77.39} & 68.59 \ci{63.63}{7” | -0.34 | -0.3432 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.75` |
| `R1.supp-tab-appexpcorpora.76` | 1.22 — “SpatialBase (raw) & 69.76 \ci{67.62}{71.98} & 70.64 \ci{62.49}{77.39} & 68.59 \ci{63.63}{7” | 1.22 | 1.2192 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.76` |
| `R1.supp-tab-appexpcorpora.77` | 70.13 — “TrunkCtrl (raw) & 70.13 \ci{67.71}{72.73} & 70.81 \ci{62.72}{77.60} & 68.25 \ci{63.05}{73.” | 70.13 | 70.13 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.77` |
| `R1.supp-tab-appexpcorpora.78` | 67.71 — “TrunkCtrl (raw) & 70.13 \ci{67.71}{72.73} & 70.81 \ci{62.72}{77.60} & 68.25 \ci{63.05}{73.” | 67.71 | 67.71 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.78` |
| `R1.supp-tab-appexpcorpora.79` | 72.73 — “TrunkCtrl (raw) & 70.13 \ci{67.71}{72.73} & 70.81 \ci{62.72}{77.60} & 68.25 \ci{63.05}{73.” | 72.73 | 72.73 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.79` |
| `R1.supp-tab-appexpcorpora.80` | 70.81 — “TrunkCtrl (raw) & 70.13 \ci{67.71}{72.73} & 70.81 \ci{62.72}{77.60} & 68.25 \ci{63.05}{73.” | 70.81 | 70.81 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.80` |
| `R1.supp-tab-appexpcorpora.81` | 62.72 — “TrunkCtrl (raw) & 70.13 \ci{67.71}{72.73} & 70.81 \ci{62.72}{77.60} & 68.25 \ci{63.05}{73.” | 62.72 | 62.72 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.81` |
| `R1.supp-tab-appexpcorpora.82` | 77.60 — “TrunkCtrl (raw) & 70.13 \ci{67.71}{72.73} & 70.81 \ci{62.72}{77.60} & 68.25 \ci{63.05}{73.” | 77.60 | 77.60 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.82` |
| `R1.supp-tab-appexpcorpora.83` | 68.25 — “TrunkCtrl (raw) & 70.13 \ci{67.71}{72.73} & 70.81 \ci{62.72}{77.60} & 68.25 \ci{63.05}{73.” | 68.25 | 68.25 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.83` |
| `R1.supp-tab-appexpcorpora.84` | 63.05 — “TrunkCtrl (raw) & 70.13 \ci{67.71}{72.73} & 70.81 \ci{62.72}{77.60} & 68.25 \ci{63.05}{73.” | 63.05 | 63.05 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.84` |
| `R1.supp-tab-appexpcorpora.85` | 73.26 — “TrunkCtrl (raw) & 70.13 \ci{67.71}{72.73} & 70.81 \ci{62.72}{77.60} & 68.25 \ci{63.05}{73.” | 73.26 | 73.26 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.85` |
| `R1.supp-tab-appexpcorpora.86` | 68.46 — “TrunkCtrl (raw) & 70.13 \ci{67.71}{72.73} & 70.81 \ci{62.72}{77.60} & 68.25 \ci{63.05}{73.” | 68.46 | 68.46 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.86` |
| `R1.supp-tab-appexpcorpora.87` | 63.20 — “TrunkCtrl (raw) & 70.13 \ci{67.71}{72.73} & 70.81 \ci{62.72}{77.60} & 68.25 \ci{63.05}{73.” | 63.20 | 63.20 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.87` |
| `R1.supp-tab-appexpcorpora.88` | 73.47 — “TrunkCtrl (raw) & 70.13 \ci{67.71}{72.73} & 70.81 \ci{62.72}{77.60} & 68.25 \ci{63.05}{73.” | 73.47 | 73.47 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.88` |
| `R1.supp-tab-appexpcorpora.89` | 0.22 — “TrunkCtrl (raw) & 70.13 \ci{67.71}{72.73} & 70.81 \ci{62.72}{77.60} & 68.25 \ci{63.05}{73.” | 0.22 | 0.2170 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.89` |
| `R1.supp-tab-appexpcorpora.90` | -0.82 — “TrunkCtrl (raw) & 70.13 \ci{67.71}{72.73} & 70.81 \ci{62.72}{77.60} & 68.25 \ci{63.05}{73.” | -0.82 | -0.8222 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.90` |
| `R1.supp-tab-appexpcorpora.91` | 1.60 — “TrunkCtrl (raw) & 70.13 \ci{67.71}{72.73} & 70.81 \ci{62.72}{77.60} & 68.25 \ci{63.05}{73.” | 1.60 | 1.5960 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.91` |
| `R1.supp-tab-appexpcorpora.92` | 70.59 — “E2a (raw) & 70.59 \ci{68.64}{72.60} & 71.04 \ci{62.67}{78.06} & 69.57 \ci{64.19}{74.61} & ” | 70.59 | 70.59 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.92` |
| `R1.supp-tab-appexpcorpora.93` | 68.64 — “E2a (raw) & 70.59 \ci{68.64}{72.60} & 71.04 \ci{62.67}{78.06} & 69.57 \ci{64.19}{74.61} & ” | 68.64 | 68.64 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.93` |
| `R1.supp-tab-appexpcorpora.94` | 72.60 — “E2a (raw) & 70.59 \ci{68.64}{72.60} & 71.04 \ci{62.67}{78.06} & 69.57 \ci{64.19}{74.61} & ” | 72.60 | 72.60 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.94` |
| `R1.supp-tab-appexpcorpora.95` | 71.04 — “E2a (raw) & 70.59 \ci{68.64}{72.60} & 71.04 \ci{62.67}{78.06} & 69.57 \ci{64.19}{74.61} & ” | 71.04 | 71.04 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.95` |
| `R1.supp-tab-appexpcorpora.96` | 62.67 — “E2a (raw) & 70.59 \ci{68.64}{72.60} & 71.04 \ci{62.67}{78.06} & 69.57 \ci{64.19}{74.61} & ” | 62.67 | 62.67 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.96` |
| `R1.supp-tab-appexpcorpora.97` | 78.06 — “E2a (raw) & 70.59 \ci{68.64}{72.60} & 71.04 \ci{62.67}{78.06} & 69.57 \ci{64.19}{74.61} & ” | 78.06 | 78.06 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.97` |
| `R1.supp-tab-appexpcorpora.98` | 69.57 — “E2a (raw) & 70.59 \ci{68.64}{72.60} & 71.04 \ci{62.67}{78.06} & 69.57 \ci{64.19}{74.61} & ” | 69.57 | 69.57 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.98` |
| `R1.supp-tab-appexpcorpora.99` | 64.19 — “E2a (raw) & 70.59 \ci{68.64}{72.60} & 71.04 \ci{62.67}{78.06} & 69.57 \ci{64.19}{74.61} & ” | 64.19 | 64.19 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.99` |
| `R1.supp-tab-appexpcorpora.100` | 74.61 — “E2a (raw) & 70.59 \ci{68.64}{72.60} & 71.04 \ci{62.67}{78.06} & 69.57 \ci{64.19}{74.61} & ” | 74.61 | 74.61 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.100` |
| `R1.supp-tab-appexpcorpora.101` | 69.67 — “E2a (raw) & 70.59 \ci{68.64}{72.60} & 71.04 \ci{62.67}{78.06} & 69.57 \ci{64.19}{74.61} & ” | 69.67 | 69.67 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.101` |
| `R1.supp-tab-appexpcorpora.102` | 64.35 — “E2a (raw) & 70.59 \ci{68.64}{72.60} & 71.04 \ci{62.67}{78.06} & 69.57 \ci{64.19}{74.61} & ” | 64.35 | 64.35 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.102` |
| `R1.supp-tab-appexpcorpora.103` | 74.70 — “E2a (raw) & 70.59 \ci{68.64}{72.60} & 71.04 \ci{62.67}{78.06} & 69.57 \ci{64.19}{74.61} & ” | 74.70 | 74.70 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.103` |
| `R1.supp-tab-appexpcorpora.104` | 0.10 — “E2a (raw) & 70.59 \ci{68.64}{72.60} & 71.04 \ci{62.67}{78.06} & 69.57 \ci{64.19}{74.61} & ” | 0.10 | 0.1024 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.104` |
| `R1.supp-tab-appexpcorpora.105` | -0.32 — “E2a (raw) & 70.59 \ci{68.64}{72.60} & 71.04 \ci{62.67}{78.06} & 69.57 \ci{64.19}{74.61} & ” | -0.32 | -0.3213 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.105` |
| `R1.supp-tab-appexpcorpora.106` | 0.59 — “E2a (raw) & 70.59 \ci{68.64}{72.60} & 71.04 \ci{62.67}{78.06} & 69.57 \ci{64.19}{74.61} & ” | 0.59 | 0.5916 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.106` |
| `R1.supp-tab-appexpcorpora.107` | 74.82 — “E2b (raw) & 74.82 \ci{72.67}{77.13} & 73.48 \ci{65.23}{80.37} & 69.21 \ci{64.29}{74.10} & ” | 74.82 | 74.82 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.107` |
| `R1.supp-tab-appexpcorpora.108` | 72.67 — “E2b (raw) & 74.82 \ci{72.67}{77.13} & 73.48 \ci{65.23}{80.37} & 69.21 \ci{64.29}{74.10} & ” | 72.67 | 72.67 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.108` |
| `R1.supp-tab-appexpcorpora.109` | 77.13 — “E2b (raw) & 74.82 \ci{72.67}{77.13} & 73.48 \ci{65.23}{80.37} & 69.21 \ci{64.29}{74.10} & ” | 77.13 | 77.13 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.109` |
| `R1.supp-tab-appexpcorpora.110` | 73.48 — “E2b (raw) & 74.82 \ci{72.67}{77.13} & 73.48 \ci{65.23}{80.37} & 69.21 \ci{64.29}{74.10} & ” | 73.48 | 73.48 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.110` |
| `R1.supp-tab-appexpcorpora.111` | 65.23 — “E2b (raw) & 74.82 \ci{72.67}{77.13} & 73.48 \ci{65.23}{80.37} & 69.21 \ci{64.29}{74.10} & ” | 65.23 | 65.23 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.111` |
| `R1.supp-tab-appexpcorpora.112` | 80.37 — “E2b (raw) & 74.82 \ci{72.67}{77.13} & 73.48 \ci{65.23}{80.37} & 69.21 \ci{64.29}{74.10} & ” | 80.37 | 80.37 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.112` |
| `R1.supp-tab-appexpcorpora.113` | 69.21 — “E2b (raw) & 74.82 \ci{72.67}{77.13} & 73.48 \ci{65.23}{80.37} & 69.21 \ci{64.29}{74.10} & ” | 69.21 | 69.21 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.113` |
| `R1.supp-tab-appexpcorpora.114` | 64.29 — “E2b (raw) & 74.82 \ci{72.67}{77.13} & 73.48 \ci{65.23}{80.37} & 69.21 \ci{64.29}{74.10} & ” | 64.29 | 64.29 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.114` |
| `R1.supp-tab-appexpcorpora.115` | 74.10 — “E2b (raw) & 74.82 \ci{72.67}{77.13} & 73.48 \ci{65.23}{80.37} & 69.21 \ci{64.29}{74.10} & ” | 74.10 | 74.10 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.115` |
| `R1.supp-tab-appexpcorpora.116` | 69.23 — “E2b (raw) & 74.82 \ci{72.67}{77.13} & 73.48 \ci{65.23}{80.37} & 69.21 \ci{64.29}{74.10} & ” | 69.23 | 69.23 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.116` |
| `R1.supp-tab-appexpcorpora.117` | 64.35 — “E2b (raw) & 74.82 \ci{72.67}{77.13} & 73.48 \ci{65.23}{80.37} & 69.21 \ci{64.29}{74.10} & ” | 64.35 | 64.35 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.117` |
| `R1.supp-tab-appexpcorpora.118` | 74.05 — “E2b (raw) & 74.82 \ci{72.67}{77.13} & 73.48 \ci{65.23}{80.37} & 69.21 \ci{64.29}{74.10} & ” | 74.05 | 74.05 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.118` |
| `R1.supp-tab-appexpcorpora.119` | 0.02 — “E2b (raw) & 74.82 \ci{72.67}{77.13} & 73.48 \ci{65.23}{80.37} & 69.21 \ci{64.29}{74.10} & ” | 0.02 | 0.0220 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.119` |
| `R1.supp-tab-appexpcorpora.120` | -0.41 — “E2b (raw) & 74.82 \ci{72.67}{77.13} & 73.48 \ci{65.23}{80.37} & 69.21 \ci{64.29}{74.10} & ” | -0.41 | -0.4086 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.120` |
| `R1.supp-tab-appexpcorpora.121` | 0.49 — “E2b (raw) & 74.82 \ci{72.67}{77.13} & 73.48 \ci{65.23}{80.37} & 69.21 \ci{64.29}{74.10} & ” | 0.49 | 0.4906 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.121` |
| `R1.supp-tab-appexpcorpora.122` | 81.44 — “anchor (raw) & 81.44 \ci{78.45}{84.78} & 72.56 \ci{65.21}{78.97} & 69.58 \ci{63.70}{74.97}” | 81.44 | 81.44 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.122` |
| `R1.supp-tab-appexpcorpora.123` | 78.45 — “anchor (raw) & 81.44 \ci{78.45}{84.78} & 72.56 \ci{65.21}{78.97} & 69.58 \ci{63.70}{74.97}” | 78.45 | 78.45 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.123` |
| `R1.supp-tab-appexpcorpora.124` | 84.78 — “anchor (raw) & 81.44 \ci{78.45}{84.78} & 72.56 \ci{65.21}{78.97} & 69.58 \ci{63.70}{74.97}” | 84.78 | 84.78 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.124` |
| `R1.supp-tab-appexpcorpora.125` | 72.56 — “anchor (raw) & 81.44 \ci{78.45}{84.78} & 72.56 \ci{65.21}{78.97} & 69.58 \ci{63.70}{74.97}” | 72.56 | 72.56 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.125` |
| `R1.supp-tab-appexpcorpora.126` | 65.21 — “anchor (raw) & 81.44 \ci{78.45}{84.78} & 72.56 \ci{65.21}{78.97} & 69.58 \ci{63.70}{74.97}” | 65.21 | 65.21 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.126` |
| `R1.supp-tab-appexpcorpora.127` | 78.97 — “anchor (raw) & 81.44 \ci{78.45}{84.78} & 72.56 \ci{65.21}{78.97} & 69.58 \ci{63.70}{74.97}” | 78.97 | 78.97 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.127` |
| `R1.supp-tab-appexpcorpora.128` | 69.58 — “anchor (raw) & 81.44 \ci{78.45}{84.78} & 72.56 \ci{65.21}{78.97} & 69.58 \ci{63.70}{74.97}” | 69.58 | 69.58 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.128` |
| `R1.supp-tab-appexpcorpora.129` | 63.70 — “anchor (raw) & 81.44 \ci{78.45}{84.78} & 72.56 \ci{65.21}{78.97} & 69.58 \ci{63.70}{74.97}” | 63.70 | 63.70 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.129` |
| `R1.supp-tab-appexpcorpora.130` | 74.97 — “anchor (raw) & 81.44 \ci{78.45}{84.78} & 72.56 \ci{65.21}{78.97} & 69.58 \ci{63.70}{74.97}” | 74.97 | 74.97 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.130` |
| `R1.supp-tab-appexpcorpora.131` | 69.37 — “anchor (raw) & 81.44 \ci{78.45}{84.78} & 72.56 \ci{65.21}{78.97} & 69.58 \ci{63.70}{74.97}” | 69.37 | 69.37 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.131` |
| `R1.supp-tab-appexpcorpora.132` | 63.59 — “anchor (raw) & 81.44 \ci{78.45}{84.78} & 72.56 \ci{65.21}{78.97} & 69.58 \ci{63.70}{74.97}” | 63.59 | 63.59 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.132` |
| `R1.supp-tab-appexpcorpora.133` | 74.56 — “anchor (raw) & 81.44 \ci{78.45}{84.78} & 72.56 \ci{65.21}{78.97} & 69.58 \ci{63.70}{74.97}” | 74.56 | 74.56 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.133` |
| `R1.supp-tab-appexpcorpora.134` | -0.21 — “anchor (raw) & 81.44 \ci{78.45}{84.78} & 72.56 \ci{65.21}{78.97} & 69.58 \ci{63.70}{74.97}” | -0.21 | -0.2137 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.134` |
| `R1.supp-tab-appexpcorpora.135` | -0.92 — “anchor (raw) & 81.44 \ci{78.45}{84.78} & 72.56 \ci{65.21}{78.97} & 69.58 \ci{63.70}{74.97}” | -0.92 | -0.9188 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.135` |
| `R1.supp-tab-appexpcorpora.136` | 0.34 — “anchor (raw) & 81.44 \ci{78.45}{84.78} & 72.56 \ci{65.21}{78.97} & 69.58 \ci{63.70}{74.97}” | 0.34 | 0.3356 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.136` |
| `R1.supp-tab-appexpcorpora.137` | 71.41 — “E3a (raw) & 71.41 \ci{68.89}{73.96} & 72.72 \ci{64.85}{79.28} & 68.68 \ci{61.99}{74.63} & ” | 71.41 | 71.41 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.137` |
| `R1.supp-tab-appexpcorpora.138` | 68.89 — “E3a (raw) & 71.41 \ci{68.89}{73.96} & 72.72 \ci{64.85}{79.28} & 68.68 \ci{61.99}{74.63} & ” | 68.89 | 68.89 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.138` |
| `R1.supp-tab-appexpcorpora.139` | 73.96 — “E3a (raw) & 71.41 \ci{68.89}{73.96} & 72.72 \ci{64.85}{79.28} & 68.68 \ci{61.99}{74.63} & ” | 73.96 | 73.96 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.139` |
| `R1.supp-tab-appexpcorpora.140` | 72.72 — “E3a (raw) & 71.41 \ci{68.89}{73.96} & 72.72 \ci{64.85}{79.28} & 68.68 \ci{61.99}{74.63} & ” | 72.72 | 72.72 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.140` |
| `R1.supp-tab-appexpcorpora.141` | 64.85 — “E3a (raw) & 71.41 \ci{68.89}{73.96} & 72.72 \ci{64.85}{79.28} & 68.68 \ci{61.99}{74.63} & ” | 64.85 | 64.85 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.141` |
| `R1.supp-tab-appexpcorpora.142` | 79.28 — “E3a (raw) & 71.41 \ci{68.89}{73.96} & 72.72 \ci{64.85}{79.28} & 68.68 \ci{61.99}{74.63} & ” | 79.28 | 79.28 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.142` |
| `R1.supp-tab-appexpcorpora.143` | 68.68 — “E3a (raw) & 71.41 \ci{68.89}{73.96} & 72.72 \ci{64.85}{79.28} & 68.68 \ci{61.99}{74.63} & ” | 68.68 | 68.68 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.143` |
| `R1.supp-tab-appexpcorpora.144` | 61.99 — “E3a (raw) & 71.41 \ci{68.89}{73.96} & 72.72 \ci{64.85}{79.28} & 68.68 \ci{61.99}{74.63} & ” | 61.99 | 61.99 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.144` |
| `R1.supp-tab-appexpcorpora.145` | 74.63 — “E3a (raw) & 71.41 \ci{68.89}{73.96} & 72.72 \ci{64.85}{79.28} & 68.68 \ci{61.99}{74.63} & ” | 74.63 | 74.63 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.145` |
| `R1.supp-tab-appexpcorpora.146` | 68.98 — “E3a (raw) & 71.41 \ci{68.89}{73.96} & 72.72 \ci{64.85}{79.28} & 68.68 \ci{61.99}{74.63} & ” | 68.98 | 68.98 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.146` |
| `R1.supp-tab-appexpcorpora.147` | 61.99 — “E3a (raw) & 71.41 \ci{68.89}{73.96} & 72.72 \ci{64.85}{79.28} & 68.68 \ci{61.99}{74.63} & ” | 61.99 | 61.99 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.147` |
| `R1.supp-tab-appexpcorpora.148` | 75.07 — “E3a (raw) & 71.41 \ci{68.89}{73.96} & 72.72 \ci{64.85}{79.28} & 68.68 \ci{61.99}{74.63} & ” | 75.07 | 75.07 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.148` |
| `R1.supp-tab-appexpcorpora.149` | 0.30 — “E3a (raw) & 71.41 \ci{68.89}{73.96} & 72.72 \ci{64.85}{79.28} & 68.68 \ci{61.99}{74.63} & ” | 0.30 | 0.2996 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.149` |
| `R1.supp-tab-appexpcorpora.150` | -0.61 — “E3a (raw) & 71.41 \ci{68.89}{73.96} & 72.72 \ci{64.85}{79.28} & 68.68 \ci{61.99}{74.63} & ” | -0.61 | -0.6100 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.150` |
| `R1.supp-tab-appexpcorpora.151` | 1.75 — “E3a (raw) & 71.41 \ci{68.89}{73.96} & 72.72 \ci{64.85}{79.28} & 68.68 \ci{61.99}{74.63} & ” | 1.75 | 1.7454 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.151` |
| `R1.supp-tab-appexpcorpora.152` | 72.26 — “E3b (raw) & 72.26 \ci{69.45}{74.99} & 71.18 \ci{63.21}{77.79} & 74.01 \ci{69.20}{78.33} & ” | 72.26 | 72.26 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.152` |
| `R1.supp-tab-appexpcorpora.153` | 69.45 — “E3b (raw) & 72.26 \ci{69.45}{74.99} & 71.18 \ci{63.21}{77.79} & 74.01 \ci{69.20}{78.33} & ” | 69.45 | 69.45 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.153` |
| `R1.supp-tab-appexpcorpora.154` | 74.99 — “E3b (raw) & 72.26 \ci{69.45}{74.99} & 71.18 \ci{63.21}{77.79} & 74.01 \ci{69.20}{78.33} & ” | 74.99 | 74.99 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.154` |
| `R1.supp-tab-appexpcorpora.155` | 71.18 — “E3b (raw) & 72.26 \ci{69.45}{74.99} & 71.18 \ci{63.21}{77.79} & 74.01 \ci{69.20}{78.33} & ” | 71.18 | 71.18 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.155` |
| `R1.supp-tab-appexpcorpora.156` | 63.21 — “E3b (raw) & 72.26 \ci{69.45}{74.99} & 71.18 \ci{63.21}{77.79} & 74.01 \ci{69.20}{78.33} & ” | 63.21 | 63.21 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.156` |
| `R1.supp-tab-appexpcorpora.157` | 77.79 — “E3b (raw) & 72.26 \ci{69.45}{74.99} & 71.18 \ci{63.21}{77.79} & 74.01 \ci{69.20}{78.33} & ” | 77.79 | 77.79 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.157` |
| `R1.supp-tab-appexpcorpora.158` | 74.01 — “E3b (raw) & 72.26 \ci{69.45}{74.99} & 71.18 \ci{63.21}{77.79} & 74.01 \ci{69.20}{78.33} & ” | 74.01 | 74.01 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.158` |
| `R1.supp-tab-appexpcorpora.159` | 69.20 — “E3b (raw) & 72.26 \ci{69.45}{74.99} & 71.18 \ci{63.21}{77.79} & 74.01 \ci{69.20}{78.33} & ” | 69.20 | 69.20 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.159` |
| `R1.supp-tab-appexpcorpora.160` | 78.33 — “E3b (raw) & 72.26 \ci{69.45}{74.99} & 71.18 \ci{63.21}{77.79} & 74.01 \ci{69.20}{78.33} & ” | 78.33 | 78.33 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.160` |
| `R1.supp-tab-appexpcorpora.161` | 74.13 — “E3b (raw) & 72.26 \ci{69.45}{74.99} & 71.18 \ci{63.21}{77.79} & 74.01 \ci{69.20}{78.33} & ” | 74.13 | 74.13 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.161` |
| `R1.supp-tab-appexpcorpora.162` | 69.20 — “E3b (raw) & 72.26 \ci{69.45}{74.99} & 71.18 \ci{63.21}{77.79} & 74.01 \ci{69.20}{78.33} & ” | 69.20 | 69.20 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.162` |
| `R1.supp-tab-appexpcorpora.163` | 78.56 — “E3b (raw) & 72.26 \ci{69.45}{74.99} & 71.18 \ci{63.21}{77.79} & 74.01 \ci{69.20}{78.33} & ” | 78.56 | 78.56 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.163` |
| `R1.supp-tab-appexpcorpora.164` | 0.12 — “E3b (raw) & 72.26 \ci{69.45}{74.99} & 71.18 \ci{63.21}{77.79} & 74.01 \ci{69.20}{78.33} & ” | 0.12 | 0.1212 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.164` |
| `R1.supp-tab-appexpcorpora.165` | -0.57 — “E3b (raw) & 72.26 \ci{69.45}{74.99} & 71.18 \ci{63.21}{77.79} & 74.01 \ci{69.20}{78.33} & ” | -0.57 | -0.5668 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.165` |
| `R1.supp-tab-appexpcorpora.166` | 0.82 — “E3b (raw) & 72.26 \ci{69.45}{74.99} & 71.18 \ci{63.21}{77.79} & 74.01 \ci{69.20}{78.33} & ” | 0.82 | 0.8173 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.166` |
| `R1.supp-tab-appexpcorpora.167` | 6.36 — “X1 & 6.36 \ci{-1.33}{14.82} & 1.86 \ci{-2.28}{6.61} & 4.25 \ci{-1.57}{11.51} & 4.06 \ci{-1” | 6.36 | 6.3587 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.167` |
| `R1.supp-tab-appexpcorpora.168` | -1.33 — “X1 & 6.36 \ci{-1.33}{14.82} & 1.86 \ci{-2.28}{6.61} & 4.25 \ci{-1.57}{11.51} & 4.06 \ci{-1” | -1.33 | -1.3293 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.168` |
| `R1.supp-tab-appexpcorpora.169` | 14.82 — “X1 & 6.36 \ci{-1.33}{14.82} & 1.86 \ci{-2.28}{6.61} & 4.25 \ci{-1.57}{11.51} & 4.06 \ci{-1” | 14.82 | 14.82 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.169` |
| `R1.supp-tab-appexpcorpora.170` | 1.86 — “X1 & 6.36 \ci{-1.33}{14.82} & 1.86 \ci{-2.28}{6.61} & 4.25 \ci{-1.57}{11.51} & 4.06 \ci{-1” | 1.86 | 1.8597 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.170` |
| `R1.supp-tab-appexpcorpora.171` | -2.28 — “X1 & 6.36 \ci{-1.33}{14.82} & 1.86 \ci{-2.28}{6.61} & 4.25 \ci{-1.57}{11.51} & 4.06 \ci{-1” | -2.28 | -2.2758 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.171` |
| `R1.supp-tab-appexpcorpora.172` | 6.61 — “X1 & 6.36 \ci{-1.33}{14.82} & 1.86 \ci{-2.28}{6.61} & 4.25 \ci{-1.57}{11.51} & 4.06 \ci{-1” | 6.61 | 6.6131 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.172` |
| `R1.supp-tab-appexpcorpora.173` | 4.25 — “X1 & 6.36 \ci{-1.33}{14.82} & 1.86 \ci{-2.28}{6.61} & 4.25 \ci{-1.57}{11.51} & 4.06 \ci{-1” | 4.25 | 4.2504 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.173` |
| `R1.supp-tab-appexpcorpora.174` | -1.57 — “X1 & 6.36 \ci{-1.33}{14.82} & 1.86 \ci{-2.28}{6.61} & 4.25 \ci{-1.57}{11.51} & 4.06 \ci{-1” | -1.57 | -1.5670 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.174` |
| `R1.supp-tab-appexpcorpora.175` | 11.51 — “X1 & 6.36 \ci{-1.33}{14.82} & 1.86 \ci{-2.28}{6.61} & 4.25 \ci{-1.57}{11.51} & 4.06 \ci{-1” | 11.51 | 11.51 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.175` |
| `R1.supp-tab-appexpcorpora.176` | 4.06 — “X1 & 6.36 \ci{-1.33}{14.82} & 1.86 \ci{-2.28}{6.61} & 4.25 \ci{-1.57}{11.51} & 4.06 \ci{-1” | 4.06 | 4.0576 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.176` |
| `R1.supp-tab-appexpcorpora.177` | -1.71 — “X1 & 6.36 \ci{-1.33}{14.82} & 1.86 \ci{-2.28}{6.61} & 4.25 \ci{-1.57}{11.51} & 4.06 \ci{-1” | -1.71 | -1.7071 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.177` |
| `R1.supp-tab-appexpcorpora.178` | 11.51 — “X1 & 6.36 \ci{-1.33}{14.82} & 1.86 \ci{-2.28}{6.61} & 4.25 \ci{-1.57}{11.51} & 4.06 \ci{-1” | 11.51 | 11.51 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.178` |
| `R1.supp-tab-appexpcorpora.179` | -3.05 — “X2 & $-3.05$ \ci{-10.73}{3.51} & $-1.28$ \ci{-5.76}{2.48} & $-3.86$ \ci{-11.38}{2.71} & $-” | -3.05 | -3.0520 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.179` |
| `R1.supp-tab-appexpcorpora.180` | -10.73 — “X2 & $-3.05$ \ci{-10.73}{3.51} & $-1.28$ \ci{-5.76}{2.48} & $-3.86$ \ci{-11.38}{2.71} & $-” | -10.73 | -10.73 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.180` |
| `R1.supp-tab-appexpcorpora.181` | 3.51 — “X2 & $-3.05$ \ci{-10.73}{3.51} & $-1.28$ \ci{-5.76}{2.48} & $-3.86$ \ci{-11.38}{2.71} & $-” | 3.51 | 3.5087 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.181` |
| `R1.supp-tab-appexpcorpora.182` | -1.28 — “X2 & $-3.05$ \ci{-10.73}{3.51} & $-1.28$ \ci{-5.76}{2.48} & $-3.86$ \ci{-11.38}{2.71} & $-” | -1.28 | -1.2793 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.182` |
| `R1.supp-tab-appexpcorpora.183` | -5.76 — “X2 & $-3.05$ \ci{-10.73}{3.51} & $-1.28$ \ci{-5.76}{2.48} & $-3.86$ \ci{-11.38}{2.71} & $-” | -5.76 | -5.7648 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.183` |
| `R1.supp-tab-appexpcorpora.184` | 2.48 — “X2 & $-3.05$ \ci{-10.73}{3.51} & $-1.28$ \ci{-5.76}{2.48} & $-3.86$ \ci{-11.38}{2.71} & $-” | 2.48 | 2.4772 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.184` |
| `R1.supp-tab-appexpcorpora.185` | -3.86 — “X2 & $-3.05$ \ci{-10.73}{3.51} & $-1.28$ \ci{-5.76}{2.48} & $-3.86$ \ci{-11.38}{2.71} & $-” | -3.86 | -3.8632 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.185` |
| `R1.supp-tab-appexpcorpora.186` | -11.38 — “X2 & $-3.05$ \ci{-10.73}{3.51} & $-1.28$ \ci{-5.76}{2.48} & $-3.86$ \ci{-11.38}{2.71} & $-” | -11.38 | -11.38 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.186` |
| `R1.supp-tab-appexpcorpora.187` | 2.71 — “X2 & $-3.05$ \ci{-10.73}{3.51} & $-1.28$ \ci{-5.76}{2.48} & $-3.86$ \ci{-11.38}{2.71} & $-” | 2.71 | 2.7079 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.187` |
| `R1.supp-tab-appexpcorpora.188` | -4.03 — “X2 & $-3.05$ \ci{-10.73}{3.51} & $-1.28$ \ci{-5.76}{2.48} & $-3.86$ \ci{-11.38}{2.71} & $-” | -4.03 | -4.0317 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.188` |
| `R1.supp-tab-appexpcorpora.189` | -11.62 — “X2 & $-3.05$ \ci{-10.73}{3.51} & $-1.28$ \ci{-5.76}{2.48} & $-3.86$ \ci{-11.38}{2.71} & $-” | -11.62 | -11.62 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.189` |
| `R1.supp-tab-appexpcorpora.190` | 2.52 — “X2 & $-3.05$ \ci{-10.73}{3.51} & $-1.28$ \ci{-5.76}{2.48} & $-3.86$ \ci{-11.38}{2.71} & $-” | 2.52 | 2.5218 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.190` |
| `R1.supp-tab-appexpcorpora.191` | 1.88 — “X3 & 1.88 \ci{-0.90}{4.60} & $-0.20$ \ci{-3.96}{3.35} & $-0.51$ \ci{-4.17}{3.16} & $-0.64$” | 1.88 | 1.8759 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.191` |
| `R1.supp-tab-appexpcorpora.192` | -0.90 — “X3 & 1.88 \ci{-0.90}{4.60} & $-0.20$ \ci{-3.96}{3.35} & $-0.51$ \ci{-4.17}{3.16} & $-0.64$” | -0.90 | -0.9038 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.192` |
| `R1.supp-tab-appexpcorpora.193` | 4.60 — “X3 & 1.88 \ci{-0.90}{4.60} & $-0.20$ \ci{-3.96}{3.35} & $-0.51$ \ci{-4.17}{3.16} & $-0.64$” | 4.60 | 4.5968 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.193` |
| `R1.supp-tab-appexpcorpora.194` | -0.20 — “X3 & 1.88 \ci{-0.90}{4.60} & $-0.20$ \ci{-3.96}{3.35} & $-0.51$ \ci{-4.17}{3.16} & $-0.64$” | -0.20 | -0.2002 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.194` |
| `R1.supp-tab-appexpcorpora.195` | -3.96 — “X3 & 1.88 \ci{-0.90}{4.60} & $-0.20$ \ci{-3.96}{3.35} & $-0.51$ \ci{-4.17}{3.16} & $-0.64$” | -3.96 | -3.9605 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.195` |
| `R1.supp-tab-appexpcorpora.196` | 3.35 — “X3 & 1.88 \ci{-0.90}{4.60} & $-0.20$ \ci{-3.96}{3.35} & $-0.51$ \ci{-4.17}{3.16} & $-0.64$” | 3.35 | 3.3471 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.196` |
| `R1.supp-tab-appexpcorpora.197` | -0.51 — “X3 & 1.88 \ci{-0.90}{4.60} & $-0.20$ \ci{-3.96}{3.35} & $-0.51$ \ci{-4.17}{3.16} & $-0.64$” | -0.51 | -0.5122 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.197` |
| `R1.supp-tab-appexpcorpora.198` | -4.17 — “X3 & 1.88 \ci{-0.90}{4.60} & $-0.20$ \ci{-3.96}{3.35} & $-0.51$ \ci{-4.17}{3.16} & $-0.64$” | -4.17 | -4.1686 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.198` |
| `R1.supp-tab-appexpcorpora.199` | 3.16 — “X3 & 1.88 \ci{-0.90}{4.60} & $-0.20$ \ci{-3.96}{3.35} & $-0.51$ \ci{-4.17}{3.16} & $-0.64$” | 3.16 | 3.1554 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.199` |
| `R1.supp-tab-appexpcorpora.200` | -0.64 — “X3 & 1.88 \ci{-0.90}{4.60} & $-0.20$ \ci{-3.96}{3.35} & $-0.51$ \ci{-4.17}{3.16} & $-0.64$” | -0.64 | -0.6411 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.200` |
| `R1.supp-tab-appexpcorpora.201` | -4.12 — “X3 & 1.88 \ci{-0.90}{4.60} & $-0.20$ \ci{-3.96}{3.35} & $-0.51$ \ci{-4.17}{3.16} & $-0.64$” | -4.12 | -4.1212 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.201` |
| `R1.supp-tab-appexpcorpora.202` | 2.93 — “X3 & 1.88 \ci{-0.90}{4.60} & $-0.20$ \ci{-3.96}{3.35} & $-0.51$ \ci{-4.17}{3.16} & $-0.64$” | 2.93 | 2.9264 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.202` |
| `R1.supp-tab-appexpcorpora.203` | -11.68 — “X4 & $-11.68$ \ci{-14.98}{-8.57} & $-1.92$ \ci{-7.13}{2.74} & $-0.99$ \ci{-6.29}{4.47} & $” | -11.68 | -11.68 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.203` |
| `R1.supp-tab-appexpcorpora.204` | -14.98 — “X4 & $-11.68$ \ci{-14.98}{-8.57} & $-1.92$ \ci{-7.13}{2.74} & $-0.99$ \ci{-6.29}{4.47} & $” | -14.98 | -14.98 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.204` |
| `R1.supp-tab-appexpcorpora.205` | -8.57 — “X4 & $-11.68$ \ci{-14.98}{-8.57} & $-1.92$ \ci{-7.13}{2.74} & $-0.99$ \ci{-6.29}{4.47} & $” | -8.57 | -8.5735 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.205` |
| `R1.supp-tab-appexpcorpora.206` | -1.92 — “X4 & $-11.68$ \ci{-14.98}{-8.57} & $-1.92$ \ci{-7.13}{2.74} & $-0.99$ \ci{-6.29}{4.47} & $” | -1.92 | -1.9235 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.206` |
| `R1.supp-tab-appexpcorpora.207` | -7.13 — “X4 & $-11.68$ \ci{-14.98}{-8.57} & $-1.92$ \ci{-7.13}{2.74} & $-0.99$ \ci{-6.29}{4.47} & $” | -7.13 | -7.1330 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.207` |
| `R1.supp-tab-appexpcorpora.208` | 2.74 — “X4 & $-11.68$ \ci{-14.98}{-8.57} & $-1.92$ \ci{-7.13}{2.74} & $-0.99$ \ci{-6.29}{4.47} & $” | 2.74 | 2.7352 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.208` |
| `R1.supp-tab-appexpcorpora.209` | -0.99 — “X4 & $-11.68$ \ci{-14.98}{-8.57} & $-1.92$ \ci{-7.13}{2.74} & $-0.99$ \ci{-6.29}{4.47} & $” | -0.99 | -0.9865 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.209` |
| `R1.supp-tab-appexpcorpora.210` | -6.29 — “X4 & $-11.68$ \ci{-14.98}{-8.57} & $-1.92$ \ci{-7.13}{2.74} & $-0.99$ \ci{-6.29}{4.47} & $” | -6.29 | -6.2899 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.210` |
| `R1.supp-tab-appexpcorpora.211` | 4.47 — “X4 & $-11.68$ \ci{-14.98}{-8.57} & $-1.92$ \ci{-7.13}{2.74} & $-0.99$ \ci{-6.29}{4.47} & $” | 4.47 | 4.4703 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.211` |
| `R1.supp-tab-appexpcorpora.212` | -0.48 — “X4 & $-11.68$ \ci{-14.98}{-8.57} & $-1.92$ \ci{-7.13}{2.74} & $-0.99$ \ci{-6.29}{4.47} & $” | -0.48 | -0.4792 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.212` |
| `R1.supp-tab-appexpcorpora.213` | -5.57 — “X4 & $-11.68$ \ci{-14.98}{-8.57} & $-1.92$ \ci{-7.13}{2.74} & $-0.99$ \ci{-6.29}{4.47} & $” | -5.57 | -5.5667 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.213` |
| `R1.supp-tab-appexpcorpora.214` | 4.83 — “X4 & $-11.68$ \ci{-14.98}{-8.57} & $-1.92$ \ci{-7.13}{2.74} & $-0.99$ \ci{-6.29}{4.47} & $” | 4.83 | 4.8320 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.214` |
| `R1.supp-tab-appexpcorpora.215` | -1.66 — “X5 & $-1.66$ \ci{-3.68}{0.43} & $-1.11$ \ci{-4.80}{2.59} & $-2.26$ \ci{-6.35}{2.02} & $-2.” | -1.66 | -1.6566 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.215` |
| `R1.supp-tab-appexpcorpora.216` | -3.68 — “X5 & $-1.66$ \ci{-3.68}{0.43} & $-1.11$ \ci{-4.80}{2.59} & $-2.26$ \ci{-6.35}{2.02} & $-2.” | -3.68 | -3.6812 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.216` |
| `R1.supp-tab-appexpcorpora.217` | 0.43 — “X5 & $-1.66$ \ci{-3.68}{0.43} & $-1.11$ \ci{-4.80}{2.59} & $-2.26$ \ci{-6.35}{2.02} & $-2.” | 0.43 | 0.4298 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.217` |
| `R1.supp-tab-appexpcorpora.218` | -1.11 — “X5 & $-1.66$ \ci{-3.68}{0.43} & $-1.11$ \ci{-4.80}{2.59} & $-2.26$ \ci{-6.35}{2.02} & $-2.” | -1.11 | -1.1103 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.218` |
| `R1.supp-tab-appexpcorpora.219` | -4.80 — “X5 & $-1.66$ \ci{-3.68}{0.43} & $-1.11$ \ci{-4.80}{2.59} & $-2.26$ \ci{-6.35}{2.02} & $-2.” | -4.80 | -4.8039 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.219` |
| `R1.supp-tab-appexpcorpora.220` | 2.59 — “X5 & $-1.66$ \ci{-3.68}{0.43} & $-1.11$ \ci{-4.80}{2.59} & $-2.26$ \ci{-6.35}{2.02} & $-2.” | 2.59 | 2.5859 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.220` |
| `R1.supp-tab-appexpcorpora.221` | -2.26 — “X5 & $-1.66$ \ci{-3.68}{0.43} & $-1.11$ \ci{-4.80}{2.59} & $-2.26$ \ci{-6.35}{2.02} & $-2.” | -2.26 | -2.2607 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.221` |
| `R1.supp-tab-appexpcorpora.222` | -6.35 — “X5 & $-1.66$ \ci{-3.68}{0.43} & $-1.11$ \ci{-4.80}{2.59} & $-2.26$ \ci{-6.35}{2.02} & $-2.” | -6.35 | -6.3519 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.222` |
| `R1.supp-tab-appexpcorpora.223` | 2.02 — “X5 & $-1.66$ \ci{-3.68}{0.43} & $-1.11$ \ci{-4.80}{2.59} & $-2.26$ \ci{-6.35}{2.02} & $-2.” | 2.02 | 2.0232 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.223` |
| `R1.supp-tab-appexpcorpora.224` | -2.27 — “X5 & $-1.66$ \ci{-3.68}{0.43} & $-1.11$ \ci{-4.80}{2.59} & $-2.26$ \ci{-6.35}{2.02} & $-2.” | -2.27 | -2.2731 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.224` |
| `R1.supp-tab-appexpcorpora.225` | -6.40 — “X5 & $-1.66$ \ci{-3.68}{0.43} & $-1.11$ \ci{-4.80}{2.59} & $-2.26$ \ci{-6.35}{2.02} & $-2.” | -6.40 | -6.3980 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.225` |
| `R1.supp-tab-appexpcorpora.226` | 2.01 — “X5 & $-1.66$ \ci{-3.68}{0.43} & $-1.11$ \ci{-4.80}{2.59} & $-2.26$ \ci{-6.35}{2.02} & $-2.” | 2.01 | 2.0094 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.226` |
| `R1.supp-tab-appexpcorpora.227` | -0.84 — “X6 & $-0.84$ \ci{-2.38}{0.71} & 0.56 \ci{-2.14}{3.30} & $-3.15$ \ci{-6.54}{-0.04} & $-2.97” | -0.84 | -0.8385 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.227` |
| `R1.supp-tab-appexpcorpora.228` | -2.38 — “X6 & $-0.84$ \ci{-2.38}{0.71} & 0.56 \ci{-2.14}{3.30} & $-3.15$ \ci{-6.54}{-0.04} & $-2.97” | -2.38 | -2.3765 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.228` |
| `R1.supp-tab-appexpcorpora.229` | 0.71 — “X6 & $-0.84$ \ci{-2.38}{0.71} & 0.56 \ci{-2.14}{3.30} & $-3.15$ \ci{-6.54}{-0.04} & $-2.97” | 0.71 | 0.7059 | `revision-1/exploratory/rev1/e7_dfdc.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.229` |
| `R1.supp-tab-appexpcorpora.230` | 0.56 — “X6 & $-0.84$ \ci{-2.38}{0.71} & 0.56 \ci{-2.14}{3.30} & $-3.15$ \ci{-6.54}{-0.04} & $-2.97” | 0.56 | 0.5646 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.230` |
| `R1.supp-tab-appexpcorpora.231` | -2.14 — “X6 & $-0.84$ \ci{-2.38}{0.71} & 0.56 \ci{-2.14}{3.30} & $-3.15$ \ci{-6.54}{-0.04} & $-2.97” | -2.14 | -2.1436 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.231` |
| `R1.supp-tab-appexpcorpora.232` | 3.30 — “X6 & $-0.84$ \ci{-2.38}{0.71} & 0.56 \ci{-2.14}{3.30} & $-3.15$ \ci{-6.54}{-0.04} & $-2.97” | 3.30 | 3.2998 | `revision-1/exploratory/rev1/e7_wdf.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.232` |
| `R1.supp-tab-appexpcorpora.233` | -3.15 — “X6 & $-0.84$ \ci{-2.38}{0.71} & 0.56 \ci{-2.14}{3.30} & $-3.15$ \ci{-6.54}{-0.04} & $-2.97” | -3.15 | -3.1519 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.233` |
| `R1.supp-tab-appexpcorpora.234` | -6.54 — “X6 & $-0.84$ \ci{-2.38}{0.71} & 0.56 \ci{-2.14}{3.30} & $-3.15$ \ci{-6.54}{-0.04} & $-2.97” | -6.54 | -6.5385 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.234` |
| `R1.supp-tab-appexpcorpora.235` | -0.04 — “X6 & $-0.84$ \ci{-2.38}{0.71} & 0.56 \ci{-2.14}{3.30} & $-3.15$ \ci{-6.54}{-0.04} & $-2.97” | -0.04 | -0.0351 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.235` |
| `R1.supp-tab-appexpcorpora.236` | -2.97 — “X6 & $-0.84$ \ci{-2.38}{0.71} & 0.56 \ci{-2.14}{3.30} & $-3.15$ \ci{-6.54}{-0.04} & $-2.97” | -2.97 | -2.9671 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.236` |
| `R1.supp-tab-appexpcorpora.237` | -6.46 — “X6 & $-0.84$ \ci{-2.38}{0.71} & 0.56 \ci{-2.14}{3.30} & $-3.15$ \ci{-6.54}{-0.04} & $-2.97” | -6.46 | -6.4615 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.237` |
| `R1.supp-tab-appexpcorpora.238` | 0.16 — “X6 & $-0.84$ \ci{-2.38}{0.71} & 0.56 \ci{-2.14}{3.30} & $-3.15$ \ci{-6.54}{-0.04} & $-2.97” | 0.16 | 0.1582 | `revision-1/exploratory/e12.json` | `python verify/claim.py R1.supp-tab-appexpcorpora.238` |

- `R1.supp-tab-appexpcorpora.2` — weights: EMA
- `R1.supp-tab-appexpcorpora.3` — weights: EMA
- `R1.supp-tab-appexpcorpora.4` — weights: EMA
- `R1.supp-tab-appexpcorpora.5` — weights: EMA
- `R1.supp-tab-appexpcorpora.6` — weights: EMA
- `R1.supp-tab-appexpcorpora.7` — weights: EMA
- `R1.supp-tab-appexpcorpora.8` — weights: EMA
- `R1.supp-tab-appexpcorpora.9` — weights: EMA
- `R1.supp-tab-appexpcorpora.10` — weights: EMA
- `R1.supp-tab-appexpcorpora.11` — weights: EMA
- `R1.supp-tab-appexpcorpora.12` — weights: EMA
- `R1.supp-tab-appexpcorpora.13` — weights: EMA
- `R1.supp-tab-appexpcorpora.14` — weights: EMA
- `R1.supp-tab-appexpcorpora.15` — weights: EMA
- `R1.supp-tab-appexpcorpora.16` — weights: EMA
- `R1.supp-tab-appexpcorpora.17` — weights: EMA
- `R1.supp-tab-appexpcorpora.18` — weights: EMA
- `R1.supp-tab-appexpcorpora.19` — weights: EMA
- `R1.supp-tab-appexpcorpora.20` — weights: EMA
- `R1.supp-tab-appexpcorpora.21` — weights: EMA
- `R1.supp-tab-appexpcorpora.22` — weights: EMA
- `R1.supp-tab-appexpcorpora.23` — weights: EMA
- `R1.supp-tab-appexpcorpora.24` — weights: EMA
- `R1.supp-tab-appexpcorpora.25` — weights: EMA
- `R1.supp-tab-appexpcorpora.26` — weights: EMA
- `R1.supp-tab-appexpcorpora.27` — weights: EMA
- `R1.supp-tab-appexpcorpora.28` — weights: EMA
- `R1.supp-tab-appexpcorpora.29` — weights: EMA
- `R1.supp-tab-appexpcorpora.30` — weights: EMA
- `R1.supp-tab-appexpcorpora.31` — weights: EMA
- `R1.supp-tab-appexpcorpora.32` — weights: EMA
- `R1.supp-tab-appexpcorpora.33` — weights: EMA
- `R1.supp-tab-appexpcorpora.34` — weights: EMA
- `R1.supp-tab-appexpcorpora.35` — weights: EMA
- `R1.supp-tab-appexpcorpora.36` — weights: EMA
- `R1.supp-tab-appexpcorpora.37` — weights: EMA
- `R1.supp-tab-appexpcorpora.38` — weights: EMA
- `R1.supp-tab-appexpcorpora.39` — weights: EMA
- `R1.supp-tab-appexpcorpora.40` — weights: EMA
- `R1.supp-tab-appexpcorpora.41` — weights: EMA
- `R1.supp-tab-appexpcorpora.42` — weights: EMA
- `R1.supp-tab-appexpcorpora.43` — weights: EMA
- `R1.supp-tab-appexpcorpora.44` — weights: EMA
- `R1.supp-tab-appexpcorpora.45` — weights: EMA
- `R1.supp-tab-appexpcorpora.46` — weights: EMA
- `R1.supp-tab-appexpcorpora.47` — weights: EMA
- `R1.supp-tab-appexpcorpora.48` — weights: EMA
- `R1.supp-tab-appexpcorpora.49` — weights: EMA
- `R1.supp-tab-appexpcorpora.50` — weights: EMA
- `R1.supp-tab-appexpcorpora.51` — weights: EMA
- `R1.supp-tab-appexpcorpora.52` — weights: EMA
- `R1.supp-tab-appexpcorpora.53` — weights: EMA
- `R1.supp-tab-appexpcorpora.54` — weights: EMA
- `R1.supp-tab-appexpcorpora.55` — weights: EMA
- `R1.supp-tab-appexpcorpora.56` — weights: EMA
- `R1.supp-tab-appexpcorpora.57` — weights: EMA
- `R1.supp-tab-appexpcorpora.58` — weights: EMA
- `R1.supp-tab-appexpcorpora.59` — weights: EMA
- `R1.supp-tab-appexpcorpora.60` — weights: EMA
- `R1.supp-tab-appexpcorpora.61` — weights: EMA
- `R1.supp-tab-appexpcorpora.62` — weights: raw
- `R1.supp-tab-appexpcorpora.63` — weights: raw
- `R1.supp-tab-appexpcorpora.64` — weights: raw
- `R1.supp-tab-appexpcorpora.65` — weights: raw
- `R1.supp-tab-appexpcorpora.66` — weights: raw
- `R1.supp-tab-appexpcorpora.67` — weights: raw
- `R1.supp-tab-appexpcorpora.68` — weights: raw
- `R1.supp-tab-appexpcorpora.69` — weights: raw
- `R1.supp-tab-appexpcorpora.70` — weights: raw
- `R1.supp-tab-appexpcorpora.71` — weights: raw
- `R1.supp-tab-appexpcorpora.72` — weights: raw
- `R1.supp-tab-appexpcorpora.73` — weights: raw
- `R1.supp-tab-appexpcorpora.74` — weights: raw
- `R1.supp-tab-appexpcorpora.75` — weights: raw
- `R1.supp-tab-appexpcorpora.76` — weights: raw
- `R1.supp-tab-appexpcorpora.77` — weights: raw
- `R1.supp-tab-appexpcorpora.78` — weights: raw
- `R1.supp-tab-appexpcorpora.79` — weights: raw
- `R1.supp-tab-appexpcorpora.80` — weights: raw
- `R1.supp-tab-appexpcorpora.81` — weights: raw
- `R1.supp-tab-appexpcorpora.82` — weights: raw
- `R1.supp-tab-appexpcorpora.83` — weights: raw
- `R1.supp-tab-appexpcorpora.84` — weights: raw
- `R1.supp-tab-appexpcorpora.85` — weights: raw
- `R1.supp-tab-appexpcorpora.86` — weights: raw
- `R1.supp-tab-appexpcorpora.87` — weights: raw
- `R1.supp-tab-appexpcorpora.88` — weights: raw
- `R1.supp-tab-appexpcorpora.89` — weights: raw
- `R1.supp-tab-appexpcorpora.90` — weights: raw
- `R1.supp-tab-appexpcorpora.91` — weights: raw
- `R1.supp-tab-appexpcorpora.92` — weights: raw
- `R1.supp-tab-appexpcorpora.93` — weights: raw
- `R1.supp-tab-appexpcorpora.94` — weights: raw
- `R1.supp-tab-appexpcorpora.95` — weights: raw
- `R1.supp-tab-appexpcorpora.96` — weights: raw
- `R1.supp-tab-appexpcorpora.97` — weights: raw
- `R1.supp-tab-appexpcorpora.98` — weights: raw
- `R1.supp-tab-appexpcorpora.99` — weights: raw
- `R1.supp-tab-appexpcorpora.100` — weights: raw
- `R1.supp-tab-appexpcorpora.101` — weights: raw
- `R1.supp-tab-appexpcorpora.102` — weights: raw
- `R1.supp-tab-appexpcorpora.103` — weights: raw
- `R1.supp-tab-appexpcorpora.104` — weights: raw
- `R1.supp-tab-appexpcorpora.105` — weights: raw
- `R1.supp-tab-appexpcorpora.106` — weights: raw
- `R1.supp-tab-appexpcorpora.107` — weights: raw
- `R1.supp-tab-appexpcorpora.108` — weights: raw
- `R1.supp-tab-appexpcorpora.109` — weights: raw
- `R1.supp-tab-appexpcorpora.110` — weights: raw
- `R1.supp-tab-appexpcorpora.111` — weights: raw
- `R1.supp-tab-appexpcorpora.112` — weights: raw
- `R1.supp-tab-appexpcorpora.113` — weights: raw
- `R1.supp-tab-appexpcorpora.114` — weights: raw
- `R1.supp-tab-appexpcorpora.115` — weights: raw
- `R1.supp-tab-appexpcorpora.116` — weights: raw
- `R1.supp-tab-appexpcorpora.117` — weights: raw
- `R1.supp-tab-appexpcorpora.118` — weights: raw
- `R1.supp-tab-appexpcorpora.119` — weights: raw
- `R1.supp-tab-appexpcorpora.120` — weights: raw
- `R1.supp-tab-appexpcorpora.121` — weights: raw
- `R1.supp-tab-appexpcorpora.122` — weights: raw
- `R1.supp-tab-appexpcorpora.123` — weights: raw
- `R1.supp-tab-appexpcorpora.124` — weights: raw
- `R1.supp-tab-appexpcorpora.125` — weights: raw
- `R1.supp-tab-appexpcorpora.126` — weights: raw
- `R1.supp-tab-appexpcorpora.127` — weights: raw
- `R1.supp-tab-appexpcorpora.128` — weights: raw
- `R1.supp-tab-appexpcorpora.129` — weights: raw
- `R1.supp-tab-appexpcorpora.130` — weights: raw
- `R1.supp-tab-appexpcorpora.131` — weights: raw
- `R1.supp-tab-appexpcorpora.132` — weights: raw
- `R1.supp-tab-appexpcorpora.133` — weights: raw
- `R1.supp-tab-appexpcorpora.134` — weights: raw
- `R1.supp-tab-appexpcorpora.135` — weights: raw
- `R1.supp-tab-appexpcorpora.136` — weights: raw
- `R1.supp-tab-appexpcorpora.137` — weights: raw
- `R1.supp-tab-appexpcorpora.138` — weights: raw
- `R1.supp-tab-appexpcorpora.139` — weights: raw
- `R1.supp-tab-appexpcorpora.140` — weights: raw
- `R1.supp-tab-appexpcorpora.141` — weights: raw
- `R1.supp-tab-appexpcorpora.142` — weights: raw
- `R1.supp-tab-appexpcorpora.143` — weights: raw
- `R1.supp-tab-appexpcorpora.144` — weights: raw
- `R1.supp-tab-appexpcorpora.145` — weights: raw
- `R1.supp-tab-appexpcorpora.146` — weights: raw
- `R1.supp-tab-appexpcorpora.147` — weights: raw
- `R1.supp-tab-appexpcorpora.148` — weights: raw
- `R1.supp-tab-appexpcorpora.149` — weights: raw
- `R1.supp-tab-appexpcorpora.150` — weights: raw
- `R1.supp-tab-appexpcorpora.151` — weights: raw
- `R1.supp-tab-appexpcorpora.152` — weights: raw
- `R1.supp-tab-appexpcorpora.153` — weights: raw
- `R1.supp-tab-appexpcorpora.154` — weights: raw
- `R1.supp-tab-appexpcorpora.155` — weights: raw
- `R1.supp-tab-appexpcorpora.156` — weights: raw
- `R1.supp-tab-appexpcorpora.157` — weights: raw
- `R1.supp-tab-appexpcorpora.158` — weights: raw
- `R1.supp-tab-appexpcorpora.159` — weights: raw
- `R1.supp-tab-appexpcorpora.160` — weights: raw
- `R1.supp-tab-appexpcorpora.161` — weights: raw
- `R1.supp-tab-appexpcorpora.162` — weights: raw
- `R1.supp-tab-appexpcorpora.163` — weights: raw
- `R1.supp-tab-appexpcorpora.164` — weights: raw
- `R1.supp-tab-appexpcorpora.165` — weights: raw
- `R1.supp-tab-appexpcorpora.166` — weights: raw
- `R1.supp-tab-appexpcorpora.167` — weights: EMA
- `R1.supp-tab-appexpcorpora.168` — weights: EMA
- `R1.supp-tab-appexpcorpora.169` — weights: EMA
- `R1.supp-tab-appexpcorpora.170` — weights: EMA
- `R1.supp-tab-appexpcorpora.171` — weights: EMA
- `R1.supp-tab-appexpcorpora.172` — weights: EMA
- `R1.supp-tab-appexpcorpora.173` — weights: EMA
- `R1.supp-tab-appexpcorpora.174` — weights: EMA
- `R1.supp-tab-appexpcorpora.175` — weights: EMA
- `R1.supp-tab-appexpcorpora.176` — weights: EMA
- `R1.supp-tab-appexpcorpora.177` — weights: EMA
- `R1.supp-tab-appexpcorpora.178` — weights: EMA
- `R1.supp-tab-appexpcorpora.179` — weights: EMA and raw
- `R1.supp-tab-appexpcorpora.180` — weights: EMA and raw
- `R1.supp-tab-appexpcorpora.181` — weights: EMA and raw
- `R1.supp-tab-appexpcorpora.182` — weights: EMA and raw
- `R1.supp-tab-appexpcorpora.183` — weights: EMA and raw
- `R1.supp-tab-appexpcorpora.184` — weights: EMA and raw
- `R1.supp-tab-appexpcorpora.185` — weights: EMA and raw
- `R1.supp-tab-appexpcorpora.186` — weights: EMA and raw
- `R1.supp-tab-appexpcorpora.187` — weights: EMA and raw
- `R1.supp-tab-appexpcorpora.188` — weights: EMA and raw
- `R1.supp-tab-appexpcorpora.189` — weights: EMA and raw
- `R1.supp-tab-appexpcorpora.190` — weights: EMA and raw
- `R1.supp-tab-appexpcorpora.191` — weights: EMA and raw
- `R1.supp-tab-appexpcorpora.192` — weights: EMA and raw
- `R1.supp-tab-appexpcorpora.193` — weights: EMA and raw
- `R1.supp-tab-appexpcorpora.194` — weights: EMA and raw
- `R1.supp-tab-appexpcorpora.195` — weights: EMA and raw
- `R1.supp-tab-appexpcorpora.196` — weights: EMA and raw
- `R1.supp-tab-appexpcorpora.197` — weights: EMA and raw
- `R1.supp-tab-appexpcorpora.198` — weights: EMA and raw
- `R1.supp-tab-appexpcorpora.199` — weights: EMA and raw
- `R1.supp-tab-appexpcorpora.200` — weights: EMA and raw
- `R1.supp-tab-appexpcorpora.201` — weights: EMA and raw
- `R1.supp-tab-appexpcorpora.202` — weights: EMA and raw
- `R1.supp-tab-appexpcorpora.203` — weights: raw
- `R1.supp-tab-appexpcorpora.204` — weights: raw
- `R1.supp-tab-appexpcorpora.205` — weights: raw
- `R1.supp-tab-appexpcorpora.206` — weights: raw
- `R1.supp-tab-appexpcorpora.207` — weights: raw
- `R1.supp-tab-appexpcorpora.208` — weights: raw
- `R1.supp-tab-appexpcorpora.209` — weights: raw
- `R1.supp-tab-appexpcorpora.210` — weights: raw
- `R1.supp-tab-appexpcorpora.211` — weights: raw
- `R1.supp-tab-appexpcorpora.212` — weights: raw
- `R1.supp-tab-appexpcorpora.213` — weights: raw
- `R1.supp-tab-appexpcorpora.214` — weights: raw
- `R1.supp-tab-appexpcorpora.215` — weights: raw
- `R1.supp-tab-appexpcorpora.216` — weights: raw
- `R1.supp-tab-appexpcorpora.217` — weights: raw
- `R1.supp-tab-appexpcorpora.218` — weights: raw
- `R1.supp-tab-appexpcorpora.219` — weights: raw
- `R1.supp-tab-appexpcorpora.220` — weights: raw
- `R1.supp-tab-appexpcorpora.221` — weights: raw
- `R1.supp-tab-appexpcorpora.222` — weights: raw
- `R1.supp-tab-appexpcorpora.223` — weights: raw
- `R1.supp-tab-appexpcorpora.224` — weights: raw
- `R1.supp-tab-appexpcorpora.225` — weights: raw
- `R1.supp-tab-appexpcorpora.226` — weights: raw
- `R1.supp-tab-appexpcorpora.227` — weights: raw
- `R1.supp-tab-appexpcorpora.228` — weights: raw
- `R1.supp-tab-appexpcorpora.229` — weights: raw
- `R1.supp-tab-appexpcorpora.230` — weights: raw
- `R1.supp-tab-appexpcorpora.231` — weights: raw
- `R1.supp-tab-appexpcorpora.232` — weights: raw
- `R1.supp-tab-appexpcorpora.233` — weights: raw
- `R1.supp-tab-appexpcorpora.234` — weights: raw
- `R1.supp-tab-appexpcorpora.235` — weights: raw
- `R1.supp-tab-appexpcorpora.236` — weights: raw
- `R1.supp-tab-appexpcorpora.237` — weights: raw
- `R1.supp-tab-appexpcorpora.238` — weights: raw

## R1.supp-tab-appexpcodecs — Revision 1 — Supplementary Material, tab:appexpcodecs

*Supplementary Material, tab:appexpcodecs; `\label{tab:appexpcodecs}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-tab-appexpcodecs.1` | 10,000 — “($B = 10{,}000$; seeds, then 140 source-identity clusters).” | 10000 | 10000.00 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.1` |
| `R1.supp-tab-appexpcodecs.2` | 98.58 — “E1 (EMA) & 98.58 & 96.94 & 94.69 & 98.09 & 95.30 & 92.27 \\” | 98.58 | 98.58 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.2` |
| `R1.supp-tab-appexpcodecs.3` | 96.94 — “E1 (EMA) & 98.58 & 96.94 & 94.69 & 98.09 & 95.30 & 92.27 \\” | 96.94 | 96.94 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.3` |
| `R1.supp-tab-appexpcodecs.4` | 94.69 — “E1 (EMA) & 98.58 & 96.94 & 94.69 & 98.09 & 95.30 & 92.27 \\” | 94.69 | 94.69 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.4` |
| `R1.supp-tab-appexpcodecs.5` | 98.09 — “E1 (EMA) & 98.58 & 96.94 & 94.69 & 98.09 & 95.30 & 92.27 \\” | 98.09 | 98.09 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.5` |
| `R1.supp-tab-appexpcodecs.6` | 95.30 — “E1 (EMA) & 98.58 & 96.94 & 94.69 & 98.09 & 95.30 & 92.27 \\” | 95.30 | 95.30 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.6` |
| `R1.supp-tab-appexpcodecs.7` | 92.27 — “E1 (EMA) & 98.58 & 96.94 & 94.69 & 98.09 & 95.30 & 92.27 \\” | 92.27 | 92.27 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.7` |
| `R1.supp-tab-appexpcodecs.8` | 98.29 — “Fair-N (EMA) & 98.29 & 95.84 & 93.48 & 97.47 & 94.34 & 91.05 \\” | 98.29 | 98.29 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.8` |
| `R1.supp-tab-appexpcodecs.9` | 95.84 — “Fair-N (EMA) & 98.29 & 95.84 & 93.48 & 97.47 & 94.34 & 91.05 \\” | 95.84 | 95.84 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.9` |
| `R1.supp-tab-appexpcodecs.10` | 93.48 — “Fair-N (EMA) & 98.29 & 95.84 & 93.48 & 97.47 & 94.34 & 91.05 \\” | 93.48 | 93.48 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.10` |
| `R1.supp-tab-appexpcodecs.11` | 97.47 — “Fair-N (EMA) & 98.29 & 95.84 & 93.48 & 97.47 & 94.34 & 91.05 \\” | 97.47 | 97.47 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.11` |
| `R1.supp-tab-appexpcodecs.12` | 94.34 — “Fair-N (EMA) & 98.29 & 95.84 & 93.48 & 97.47 & 94.34 & 91.05 \\” | 94.34 | 94.34 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.12` |
| `R1.supp-tab-appexpcodecs.13` | 91.05 — “Fair-N (EMA) & 98.29 & 95.84 & 93.48 & 97.47 & 94.34 & 91.05 \\” | 91.05 | 91.05 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.13` |
| `R1.supp-tab-appexpcodecs.14` | 98.33 — “Fair-W (EMA) & 98.33 & 96.52 & 94.27 & 97.83 & 94.35 & 91.48 \\” | 98.33 | 98.33 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.14` |
| `R1.supp-tab-appexpcodecs.15` | 96.52 — “Fair-W (EMA) & 98.33 & 96.52 & 94.27 & 97.83 & 94.35 & 91.48 \\” | 96.52 | 96.52 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.15` |
| `R1.supp-tab-appexpcodecs.16` | 94.27 — “Fair-W (EMA) & 98.33 & 96.52 & 94.27 & 97.83 & 94.35 & 91.48 \\” | 94.27 | 94.27 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.16` |
| `R1.supp-tab-appexpcodecs.17` | 97.83 — “Fair-W (EMA) & 98.33 & 96.52 & 94.27 & 97.83 & 94.35 & 91.48 \\” | 97.83 | 97.83 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.17` |
| `R1.supp-tab-appexpcodecs.18` | 94.35 — “Fair-W (EMA) & 98.33 & 96.52 & 94.27 & 97.83 & 94.35 & 91.48 \\” | 94.35 | 94.35 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.18` |
| `R1.supp-tab-appexpcodecs.19` | 91.48 — “Fair-W (EMA) & 98.33 & 96.52 & 94.27 & 97.83 & 94.35 & 91.48 \\” | 91.48 | 91.48 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.19` |
| `R1.supp-tab-appexpcodecs.20` | 97.37 — “CAFRL as specified (EMA) & 97.37 & 94.79 & 92.22 & 96.65 & 92.58 & 88.69 \\” | 97.37 | 97.37 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.20` |
| `R1.supp-tab-appexpcodecs.21` | 94.79 — “CAFRL as specified (EMA) & 97.37 & 94.79 & 92.22 & 96.65 & 92.58 & 88.69 \\” | 94.79 | 94.79 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.21` |
| `R1.supp-tab-appexpcodecs.22` | 92.22 — “CAFRL as specified (EMA) & 97.37 & 94.79 & 92.22 & 96.65 & 92.58 & 88.69 \\” | 92.22 | 92.22 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.22` |
| `R1.supp-tab-appexpcodecs.23` | 96.65 — “CAFRL as specified (EMA) & 97.37 & 94.79 & 92.22 & 96.65 & 92.58 & 88.69 \\” | 96.65 | 96.65 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.23` |
| `R1.supp-tab-appexpcodecs.24` | 92.58 — “CAFRL as specified (EMA) & 97.37 & 94.79 & 92.22 & 96.65 & 92.58 & 88.69 \\” | 92.58 | 92.58 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.24` |
| `R1.supp-tab-appexpcodecs.25` | 88.69 — “CAFRL as specified (EMA) & 97.37 & 94.79 & 92.22 & 96.65 & 92.58 & 88.69 \\” | 88.69 | 88.69 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.25` |
| `R1.supp-tab-appexpcodecs.26` | 98.39 — “SpatialBase (raw) & 98.39 & 96.90 & 94.94 & 98.03 & 95.69 & 93.02 \\” | 98.39 | 98.39 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.26` |
| `R1.supp-tab-appexpcodecs.27` | 96.90 — “SpatialBase (raw) & 98.39 & 96.90 & 94.94 & 98.03 & 95.69 & 93.02 \\” | 96.90 | 96.90 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.27` |
| `R1.supp-tab-appexpcodecs.28` | 94.94 — “SpatialBase (raw) & 98.39 & 96.90 & 94.94 & 98.03 & 95.69 & 93.02 \\” | 94.94 | 94.94 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.28` |
| `R1.supp-tab-appexpcodecs.29` | 98.03 — “SpatialBase (raw) & 98.39 & 96.90 & 94.94 & 98.03 & 95.69 & 93.02 \\” | 98.03 | 98.03 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.29` |
| `R1.supp-tab-appexpcodecs.30` | 95.69 — “SpatialBase (raw) & 98.39 & 96.90 & 94.94 & 98.03 & 95.69 & 93.02 \\” | 95.69 | 95.69 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.30` |
| `R1.supp-tab-appexpcodecs.31` | 93.02 — “SpatialBase (raw) & 98.39 & 96.90 & 94.94 & 98.03 & 95.69 & 93.02 \\” | 93.02 | 93.02 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.31` |
| `R1.supp-tab-appexpcodecs.32` | 98.43 — “TrunkCtrl (raw) & 98.43 & 96.53 & 93.99 & 97.97 & 94.92 & 91.84 \\” | 98.43 | 98.43 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.32` |
| `R1.supp-tab-appexpcodecs.33` | 96.53 — “TrunkCtrl (raw) & 98.43 & 96.53 & 93.99 & 97.97 & 94.92 & 91.84 \\” | 96.53 | 96.53 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.33` |
| `R1.supp-tab-appexpcodecs.34` | 93.99 — “TrunkCtrl (raw) & 98.43 & 96.53 & 93.99 & 97.97 & 94.92 & 91.84 \\” | 93.99 | 93.99 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.34` |
| `R1.supp-tab-appexpcodecs.35` | 97.97 — “TrunkCtrl (raw) & 98.43 & 96.53 & 93.99 & 97.97 & 94.92 & 91.84 \\” | 97.97 | 97.97 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.35` |
| `R1.supp-tab-appexpcodecs.36` | 94.92 — “TrunkCtrl (raw) & 98.43 & 96.53 & 93.99 & 97.97 & 94.92 & 91.84 \\” | 94.92 | 94.92 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.36` |
| `R1.supp-tab-appexpcodecs.37` | 91.84 — “TrunkCtrl (raw) & 98.43 & 96.53 & 93.99 & 97.97 & 94.92 & 91.84 \\” | 91.84 | 91.84 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.37` |
| `R1.supp-tab-appexpcodecs.38` | 98.67 — “E2a (raw) & 98.67 & 97.29 & 95.26 & 98.31 & 95.80 & 92.72 \\” | 98.67 | 98.67 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.38` |
| `R1.supp-tab-appexpcodecs.39` | 97.29 — “E2a (raw) & 98.67 & 97.29 & 95.26 & 98.31 & 95.80 & 92.72 \\” | 97.29 | 97.29 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.39` |
| `R1.supp-tab-appexpcodecs.40` | 95.26 — “E2a (raw) & 98.67 & 97.29 & 95.26 & 98.31 & 95.80 & 92.72 \\” | 95.26 | 95.26 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.40` |
| `R1.supp-tab-appexpcodecs.41` | 98.31 — “E2a (raw) & 98.67 & 97.29 & 95.26 & 98.31 & 95.80 & 92.72 \\” | 98.31 | 98.31 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.41` |
| `R1.supp-tab-appexpcodecs.42` | 95.80 — “E2a (raw) & 98.67 & 97.29 & 95.26 & 98.31 & 95.80 & 92.72 \\” | 95.80 | 95.80 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.42` |
| `R1.supp-tab-appexpcodecs.43` | 92.72 — “E2a (raw) & 98.67 & 97.29 & 95.26 & 98.31 & 95.80 & 92.72 \\” | 92.72 | 92.72 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.43` |
| `R1.supp-tab-appexpcodecs.44` | 98.79 — “E2b (raw) & 98.79 & 97.40 & 94.30 & 98.42 & 95.68 & 92.38 \\” | 98.79 | 98.79 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.44` |
| `R1.supp-tab-appexpcodecs.45` | 97.40 — “E2b (raw) & 98.79 & 97.40 & 94.30 & 98.42 & 95.68 & 92.38 \\” | 97.40 | 97.40 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.45` |
| `R1.supp-tab-appexpcodecs.46` | 94.30 — “E2b (raw) & 98.79 & 97.40 & 94.30 & 98.42 & 95.68 & 92.38 \\” | 94.30 | 94.30 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.46` |
| `R1.supp-tab-appexpcodecs.47` | 98.42 — “E2b (raw) & 98.79 & 97.40 & 94.30 & 98.42 & 95.68 & 92.38 \\” | 98.42 | 98.42 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.47` |
| `R1.supp-tab-appexpcodecs.48` | 95.68 — “E2b (raw) & 98.79 & 97.40 & 94.30 & 98.42 & 95.68 & 92.38 \\” | 95.68 | 95.68 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.48` |
| `R1.supp-tab-appexpcodecs.49` | 92.38 — “E2b (raw) & 98.79 & 97.40 & 94.30 & 98.42 & 95.68 & 92.38 \\” | 92.38 | 92.38 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.49` |
| `R1.supp-tab-appexpcodecs.50` | 99.07 — “anchor (raw) & 99.07 & 96.42 & 89.59 & 98.68 & 94.37 & 89.03 \\” | 99.07 | 99.07 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.50` |
| `R1.supp-tab-appexpcodecs.51` | 96.42 — “anchor (raw) & 99.07 & 96.42 & 89.59 & 98.68 & 94.37 & 89.03 \\” | 96.42 | 96.42 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.51` |
| `R1.supp-tab-appexpcodecs.52` | 89.59 — “anchor (raw) & 99.07 & 96.42 & 89.59 & 98.68 & 94.37 & 89.03 \\” | 89.59 | 89.59 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.52` |
| `R1.supp-tab-appexpcodecs.53` | 98.68 — “anchor (raw) & 99.07 & 96.42 & 89.59 & 98.68 & 94.37 & 89.03 \\” | 98.68 | 98.68 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.53` |
| `R1.supp-tab-appexpcodecs.54` | 94.37 — “anchor (raw) & 99.07 & 96.42 & 89.59 & 98.68 & 94.37 & 89.03 \\” | 94.37 | 94.37 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.54` |
| `R1.supp-tab-appexpcodecs.55` | 89.03 — “anchor (raw) & 99.07 & 96.42 & 89.59 & 98.68 & 94.37 & 89.03 \\” | 89.03 | 89.03 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.55` |
| `R1.supp-tab-appexpcodecs.56` | 98.05 — “E3a (raw) & 98.05 & 96.00 & 92.08 & 97.83 & 95.55 & 92.47 \\” | 98.05 | 98.05 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.56` |
| `R1.supp-tab-appexpcodecs.57` | 96.00 — “E3a (raw) & 98.05 & 96.00 & 92.08 & 97.83 & 95.55 & 92.47 \\” | 96.00 | 96.00 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.57` |
| `R1.supp-tab-appexpcodecs.58` | 92.08 — “E3a (raw) & 98.05 & 96.00 & 92.08 & 97.83 & 95.55 & 92.47 \\” | 92.08 | 92.08 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.58` |
| `R1.supp-tab-appexpcodecs.59` | 97.83 — “E3a (raw) & 98.05 & 96.00 & 92.08 & 97.83 & 95.55 & 92.47 \\” | 97.83 | 97.83 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.59` |
| `R1.supp-tab-appexpcodecs.60` | 95.55 — “E3a (raw) & 98.05 & 96.00 & 92.08 & 97.83 & 95.55 & 92.47 \\” | 95.55 | 95.55 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.60` |
| `R1.supp-tab-appexpcodecs.61` | 92.47 — “E3a (raw) & 98.05 & 96.00 & 92.08 & 97.83 & 95.55 & 92.47 \\” | 92.47 | 92.47 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.61` |
| `R1.supp-tab-appexpcodecs.62` | 98.31 — “E3b (raw) & 98.31 & 95.99 & 90.84 & 98.05 & 95.52 & 91.80 \\” | 98.31 | 98.31 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.62` |
| `R1.supp-tab-appexpcodecs.63` | 95.99 — “E3b (raw) & 98.31 & 95.99 & 90.84 & 98.05 & 95.52 & 91.80 \\” | 95.99 | 95.99 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.63` |
| `R1.supp-tab-appexpcodecs.64` | 90.84 — “E3b (raw) & 98.31 & 95.99 & 90.84 & 98.05 & 95.52 & 91.80 \\” | 90.84 | 90.84 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.64` |
| `R1.supp-tab-appexpcodecs.65` | 98.05 — “E3b (raw) & 98.31 & 95.99 & 90.84 & 98.05 & 95.52 & 91.80 \\” | 98.05 | 98.05 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.65` |
| `R1.supp-tab-appexpcodecs.66` | 95.52 — “E3b (raw) & 98.31 & 95.99 & 90.84 & 98.05 & 95.52 & 91.80 \\” | 95.52 | 95.52 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.66` |
| `R1.supp-tab-appexpcodecs.67` | 91.80 — “E3b (raw) & 98.31 & 95.99 & 90.84 & 98.05 & 95.52 & 91.80 \\” | 91.80 | 91.80 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.67` |
| `R1.supp-tab-appexpcodecs.68` | 0.28 — “X1 & 0.28 \ci{-0.17}{0.88} & 1.10 \ci{-0.15}{2.61} & 1.21 \ci{-0.49}{3.09} & 0.63 \ci{-0.3” | 0.28 | 0.2815 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.68` |
| `R1.supp-tab-appexpcodecs.69` | -0.17 — “X1 & 0.28 \ci{-0.17}{0.88} & 1.10 \ci{-0.15}{2.61} & 1.21 \ci{-0.49}{3.09} & 0.63 \ci{-0.3” | -0.17 | -0.1726 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.69` |
| `R1.supp-tab-appexpcodecs.70` | 0.88 — “X1 & 0.28 \ci{-0.17}{0.88} & 1.10 \ci{-0.15}{2.61} & 1.21 \ci{-0.49}{3.09} & 0.63 \ci{-0.3” | 0.88 | 0.8776 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.70` |
| `R1.supp-tab-appexpcodecs.71` | 1.10 — “X1 & 0.28 \ci{-0.17}{0.88} & 1.10 \ci{-0.15}{2.61} & 1.21 \ci{-0.49}{3.09} & 0.63 \ci{-0.3” | 1.10 | 1.1033 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.71` |
| `R1.supp-tab-appexpcodecs.72` | -0.15 — “X1 & 0.28 \ci{-0.17}{0.88} & 1.10 \ci{-0.15}{2.61} & 1.21 \ci{-0.49}{3.09} & 0.63 \ci{-0.3” | -0.15 | -0.1450 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.72` |
| `R1.supp-tab-appexpcodecs.73` | 2.61 — “X1 & 0.28 \ci{-0.17}{0.88} & 1.10 \ci{-0.15}{2.61} & 1.21 \ci{-0.49}{3.09} & 0.63 \ci{-0.3” | 2.61 | 2.6089 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.73` |
| `R1.supp-tab-appexpcodecs.74` | 1.21 — “X1 & 0.28 \ci{-0.17}{0.88} & 1.10 \ci{-0.15}{2.61} & 1.21 \ci{-0.49}{3.09} & 0.63 \ci{-0.3” | 1.21 | 1.2088 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.74` |
| `R1.supp-tab-appexpcodecs.75` | -0.49 — “X1 & 0.28 \ci{-0.17}{0.88} & 1.10 \ci{-0.15}{2.61} & 1.21 \ci{-0.49}{3.09} & 0.63 \ci{-0.3” | -0.49 | -0.4881 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.75` |
| `R1.supp-tab-appexpcodecs.76` | 3.09 — “X1 & 0.28 \ci{-0.17}{0.88} & 1.10 \ci{-0.15}{2.61} & 1.21 \ci{-0.49}{3.09} & 0.63 \ci{-0.3” | 3.09 | 3.0851 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.76` |
| `R1.supp-tab-appexpcodecs.77` | 0.63 — “X1 & 0.28 \ci{-0.17}{0.88} & 1.10 \ci{-0.15}{2.61} & 1.21 \ci{-0.49}{3.09} & 0.63 \ci{-0.3” | 0.63 | 0.6267 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.77` |
| `R1.supp-tab-appexpcodecs.78` | -0.37 — “X1 & 0.28 \ci{-0.17}{0.88} & 1.10 \ci{-0.15}{2.61} & 1.21 \ci{-0.49}{3.09} & 0.63 \ci{-0.3” | -0.37 | -0.3737 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.78` |
| `R1.supp-tab-appexpcodecs.79` | 1.99 — “X1 & 0.28 \ci{-0.17}{0.88} & 1.10 \ci{-0.15}{2.61} & 1.21 \ci{-0.49}{3.09} & 0.63 \ci{-0.3” | 1.99 | 1.9932 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.79` |
| `R1.supp-tab-appexpcodecs.80` | 0.96 — “X1 & 0.28 \ci{-0.17}{0.88} & 1.10 \ci{-0.15}{2.61} & 1.21 \ci{-0.49}{3.09} & 0.63 \ci{-0.3” | 0.96 | 0.9566 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.80` |
| `R1.supp-tab-appexpcodecs.81` | -0.45 — “X1 & 0.28 \ci{-0.17}{0.88} & 1.10 \ci{-0.15}{2.61} & 1.21 \ci{-0.49}{3.09} & 0.63 \ci{-0.3” | -0.45 | -0.4460 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.81` |
| `R1.supp-tab-appexpcodecs.82` | 2.75 — “X1 & 0.28 \ci{-0.17}{0.88} & 1.10 \ci{-0.15}{2.61} & 1.21 \ci{-0.49}{3.09} & 0.63 \ci{-0.3” | 2.75 | 2.7483 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.82` |
| `R1.supp-tab-appexpcodecs.83` | 1.22 — “X1 & 0.28 \ci{-0.17}{0.88} & 1.10 \ci{-0.15}{2.61} & 1.21 \ci{-0.49}{3.09} & 0.63 \ci{-0.3” | 1.22 | 1.2164 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.83` |
| `R1.supp-tab-appexpcodecs.84` | -0.81 — “X1 & 0.28 \ci{-0.17}{0.88} & 1.10 \ci{-0.15}{2.61} & 1.21 \ci{-0.49}{3.09} & 0.63 \ci{-0.3” | -0.81 | -0.8087 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.84` |
| `R1.supp-tab-appexpcodecs.85` | 3.52 — “X1 & 0.28 \ci{-0.17}{0.88} & 1.10 \ci{-0.15}{2.61} & 1.21 \ci{-0.49}{3.09} & 0.63 \ci{-0.3” | 3.52 | 3.5243 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.85` |
| `R1.supp-tab-appexpcodecs.86` | -0.10 — “X2 & $-0.10$ \ci{-0.70}{0.44} & $-1.06$ \ci{-2.58}{0.25} & $-1.45$ \ci{-3.51}{0.37} & $-0.” | -0.10 | -0.0961 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.86` |
| `R1.supp-tab-appexpcodecs.87` | -0.70 — “X2 & $-0.10$ \ci{-0.70}{0.44} & $-1.06$ \ci{-2.58}{0.25} & $-1.45$ \ci{-3.51}{0.37} & $-0.” | -0.70 | -0.7011 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.87` |
| `R1.supp-tab-appexpcodecs.88` | 0.44 — “X2 & $-0.10$ \ci{-0.70}{0.44} & $-1.06$ \ci{-2.58}{0.25} & $-1.45$ \ci{-3.51}{0.37} & $-0.” | 0.44 | 0.4426 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.88` |
| `R1.supp-tab-appexpcodecs.89` | -1.06 — “X2 & $-0.10$ \ci{-0.70}{0.44} & $-1.06$ \ci{-2.58}{0.25} & $-1.45$ \ci{-3.51}{0.37} & $-0.” | -1.06 | -1.0595 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.89` |
| `R1.supp-tab-appexpcodecs.90` | -2.58 — “X2 & $-0.10$ \ci{-0.70}{0.44} & $-1.06$ \ci{-2.58}{0.25} & $-1.45$ \ci{-3.51}{0.37} & $-0.” | -2.58 | -2.5766 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.90` |
| `R1.supp-tab-appexpcodecs.91` | 0.25 — “X2 & $-0.10$ \ci{-0.70}{0.44} & $-1.06$ \ci{-2.58}{0.25} & $-1.45$ \ci{-3.51}{0.37} & $-0.” | 0.25 | 0.2479 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.91` |
| `R1.supp-tab-appexpcodecs.92` | -1.45 — “X2 & $-0.10$ \ci{-0.70}{0.44} & $-1.06$ \ci{-2.58}{0.25} & $-1.45$ \ci{-3.51}{0.37} & $-0.” | -1.45 | -1.4515 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.92` |
| `R1.supp-tab-appexpcodecs.93` | -3.51 — “X2 & $-0.10$ \ci{-0.70}{0.44} & $-1.06$ \ci{-2.58}{0.25} & $-1.45$ \ci{-3.51}{0.37} & $-0.” | -3.51 | -3.5103 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.93` |
| `R1.supp-tab-appexpcodecs.94` | 0.37 — “X2 & $-0.10$ \ci{-0.70}{0.44} & $-1.06$ \ci{-2.58}{0.25} & $-1.45$ \ci{-3.51}{0.37} & $-0.” | 0.37 | 0.3742 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.94` |
| `R1.supp-tab-appexpcodecs.95` | -0.57 — “X2 & $-0.10$ \ci{-0.70}{0.44} & $-1.06$ \ci{-2.58}{0.25} & $-1.45$ \ci{-3.51}{0.37} & $-0.” | -0.57 | -0.5685 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.95` |
| `R1.supp-tab-appexpcodecs.96` | -1.99 — “X2 & $-0.10$ \ci{-0.70}{0.44} & $-1.06$ \ci{-2.58}{0.25} & $-1.45$ \ci{-3.51}{0.37} & $-0.” | -1.99 | -1.9945 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.96` |
| `R1.supp-tab-appexpcodecs.97` | 0.42 — “X2 & $-0.10$ \ci{-0.70}{0.44} & $-1.06$ \ci{-2.58}{0.25} & $-1.45$ \ci{-3.51}{0.37} & $-0.” | 0.42 | 0.4205 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.97` |
| `R1.supp-tab-appexpcodecs.98` | -1.35 — “X2 & $-0.10$ \ci{-0.70}{0.44} & $-1.06$ \ci{-2.58}{0.25} & $-1.45$ \ci{-3.51}{0.37} & $-0.” | -1.35 | -1.3478 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.98` |
| `R1.supp-tab-appexpcodecs.99` | -3.10 — “X2 & $-0.10$ \ci{-0.70}{0.44} & $-1.06$ \ci{-2.58}{0.25} & $-1.45$ \ci{-3.51}{0.37} & $-0.” | -3.10 | -3.0952 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.99` |
| `R1.supp-tab-appexpcodecs.100` | 0.18 — “X2 & $-0.10$ \ci{-0.70}{0.44} & $-1.06$ \ci{-2.58}{0.25} & $-1.45$ \ci{-3.51}{0.37} & $-0.” | 0.18 | 0.1769 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.100` |
| `R1.supp-tab-appexpcodecs.101` | -1.97 — “X2 & $-0.10$ \ci{-0.70}{0.44} & $-1.06$ \ci{-2.58}{0.25} & $-1.45$ \ci{-3.51}{0.37} & $-0.” | -1.97 | -1.9728 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.101` |
| `R1.supp-tab-appexpcodecs.102` | -4.31 — “X2 & $-0.10$ \ci{-0.70}{0.44} & $-1.06$ \ci{-2.58}{0.25} & $-1.45$ \ci{-3.51}{0.37} & $-0.” | -4.31 | -4.3075 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.102` |
| `R1.supp-tab-appexpcodecs.103` | 0.22 — “X2 & $-0.10$ \ci{-0.70}{0.44} & $-1.06$ \ci{-2.58}{0.25} & $-1.45$ \ci{-3.51}{0.37} & $-0.” | 0.22 | 0.2182 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.103` |
| `R1.supp-tab-appexpcodecs.104` | -0.06 — “X3 & $-0.06$ \ci{-0.84}{0.55} & $-0.38$ \ci{-1.57}{0.59} & $-0.67$ \ci{-2.35}{0.88} & $-0.” | -0.06 | -0.0565 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.104` |
| `R1.supp-tab-appexpcodecs.105` | -0.84 — “X3 & $-0.06$ \ci{-0.84}{0.55} & $-0.38$ \ci{-1.57}{0.59} & $-0.67$ \ci{-2.35}{0.88} & $-0.” | -0.84 | -0.8376 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.105` |
| `R1.supp-tab-appexpcodecs.106` | 0.55 — “X3 & $-0.06$ \ci{-0.84}{0.55} & $-0.38$ \ci{-1.57}{0.59} & $-0.67$ \ci{-2.35}{0.88} & $-0.” | 0.55 | 0.5464 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.106` |
| `R1.supp-tab-appexpcodecs.107` | -0.38 — “X3 & $-0.06$ \ci{-0.84}{0.55} & $-0.38$ \ci{-1.57}{0.59} & $-0.67$ \ci{-2.35}{0.88} & $-0.” | -0.38 | -0.3818 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.107` |
| `R1.supp-tab-appexpcodecs.108` | -1.57 — “X3 & $-0.06$ \ci{-0.84}{0.55} & $-0.38$ \ci{-1.57}{0.59} & $-0.67$ \ci{-2.35}{0.88} & $-0.” | -1.57 | -1.5655 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.108` |
| `R1.supp-tab-appexpcodecs.109` | 0.59 — “X3 & $-0.06$ \ci{-0.84}{0.55} & $-0.38$ \ci{-1.57}{0.59} & $-0.67$ \ci{-2.35}{0.88} & $-0.” | 0.59 | 0.5859 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.109` |
| `R1.supp-tab-appexpcodecs.110` | -0.67 — “X3 & $-0.06$ \ci{-0.84}{0.55} & $-0.38$ \ci{-1.57}{0.59} & $-0.67$ \ci{-2.35}{0.88} & $-0.” | -0.67 | -0.6671 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.110` |
| `R1.supp-tab-appexpcodecs.111` | -2.35 — “X3 & $-0.06$ \ci{-0.84}{0.55} & $-0.38$ \ci{-1.57}{0.59} & $-0.67$ \ci{-2.35}{0.88} & $-0.” | -2.35 | -2.3504 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.111` |
| `R1.supp-tab-appexpcodecs.112` | 0.88 — “X3 & $-0.06$ \ci{-0.84}{0.55} & $-0.38$ \ci{-1.57}{0.59} & $-0.67$ \ci{-2.35}{0.88} & $-0.” | 0.88 | 0.8784 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.112` |
| `R1.supp-tab-appexpcodecs.113` | -0.20 — “X3 & $-0.06$ \ci{-0.84}{0.55} & $-0.38$ \ci{-1.57}{0.59} & $-0.67$ \ci{-2.35}{0.88} & $-0.” | -0.20 | -0.2020 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.113` |
| `R1.supp-tab-appexpcodecs.114` | -1.05 — “X3 & $-0.06$ \ci{-0.84}{0.55} & $-0.38$ \ci{-1.57}{0.59} & $-0.67$ \ci{-2.35}{0.88} & $-0.” | -1.05 | -1.0464 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.114` |
| `R1.supp-tab-appexpcodecs.115` | 0.42 — “X3 & $-0.06$ \ci{-0.84}{0.55} & $-0.38$ \ci{-1.57}{0.59} & $-0.67$ \ci{-2.35}{0.88} & $-0.” | 0.42 | 0.4179 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.115` |
| `R1.supp-tab-appexpcodecs.116` | -1.34 — “X3 & $-0.06$ \ci{-0.84}{0.55} & $-0.38$ \ci{-1.57}{0.59} & $-0.67$ \ci{-2.35}{0.88} & $-0.” | -1.34 | -1.3393 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.116` |
| `R1.supp-tab-appexpcodecs.117` | -2.82 — “X3 & $-0.06$ \ci{-0.84}{0.55} & $-0.38$ \ci{-1.57}{0.59} & $-0.67$ \ci{-2.35}{0.88} & $-0.” | -2.82 | -2.8197 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.117` |
| `R1.supp-tab-appexpcodecs.118` | -0.11 — “X3 & $-0.06$ \ci{-0.84}{0.55} & $-0.38$ \ci{-1.57}{0.59} & $-0.67$ \ci{-2.35}{0.88} & $-0.” | -0.11 | -0.1071 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.118` |
| `R1.supp-tab-appexpcodecs.119` | -1.54 — “X3 & $-0.06$ \ci{-0.84}{0.55} & $-0.38$ \ci{-1.57}{0.59} & $-0.67$ \ci{-2.35}{0.88} & $-0.” | -1.54 | -1.5421 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.119` |
| `R1.supp-tab-appexpcodecs.120` | -3.32 — “X3 & $-0.06$ \ci{-0.84}{0.55} & $-0.38$ \ci{-1.57}{0.59} & $-0.67$ \ci{-2.35}{0.88} & $-0.” | -3.32 | -3.3215 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.120` |
| `R1.supp-tab-appexpcodecs.121` | 0.07 — “X3 & $-0.06$ \ci{-0.84}{0.55} & $-0.38$ \ci{-1.57}{0.59} & $-0.67$ \ci{-2.35}{0.88} & $-0.” | 0.07 | 0.0655 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.121` |
| `R1.supp-tab-appexpcodecs.122` | -0.68 — “X4 & $-0.68$ \ci{-1.30}{-0.17} & 0.48 \ci{-0.67}{1.62} & 5.34 \ci{3.14}{7.65} & $-0.64$ \c” | -0.68 | -0.6841 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.122` |
| `R1.supp-tab-appexpcodecs.123` | -1.30 — “X4 & $-0.68$ \ci{-1.30}{-0.17} & 0.48 \ci{-0.67}{1.62} & 5.34 \ci{3.14}{7.65} & $-0.64$ \c” | -1.30 | -1.3027 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.123` |
| `R1.supp-tab-appexpcodecs.124` | -0.17 — “X4 & $-0.68$ \ci{-1.30}{-0.17} & 0.48 \ci{-0.67}{1.62} & 5.34 \ci{3.14}{7.65} & $-0.64$ \c” | -0.17 | -0.1747 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.124` |
| `R1.supp-tab-appexpcodecs.125` | 0.48 — “X4 & $-0.68$ \ci{-1.30}{-0.17} & 0.48 \ci{-0.67}{1.62} & 5.34 \ci{3.14}{7.65} & $-0.64$ \c” | 0.48 | 0.4783 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.125` |
| `R1.supp-tab-appexpcodecs.126` | -0.67 — “X4 & $-0.68$ \ci{-1.30}{-0.17} & 0.48 \ci{-0.67}{1.62} & 5.34 \ci{3.14}{7.65} & $-0.64$ \c” | -0.67 | -0.6748 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.126` |
| `R1.supp-tab-appexpcodecs.127` | 1.62 — “X4 & $-0.68$ \ci{-1.30}{-0.17} & 0.48 \ci{-0.67}{1.62} & 5.34 \ci{3.14}{7.65} & $-0.64$ \c” | 1.62 | 1.6238 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.127` |
| `R1.supp-tab-appexpcodecs.128` | 5.34 — “X4 & $-0.68$ \ci{-1.30}{-0.17} & 0.48 \ci{-0.67}{1.62} & 5.34 \ci{3.14}{7.65} & $-0.64$ \c” | 5.34 | 5.3431 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.128` |
| `R1.supp-tab-appexpcodecs.129` | 3.14 — “X4 & $-0.68$ \ci{-1.30}{-0.17} & 0.48 \ci{-0.67}{1.62} & 5.34 \ci{3.14}{7.65} & $-0.64$ \c” | 3.14 | 3.1395 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.129` |
| `R1.supp-tab-appexpcodecs.130` | 7.65 — “X4 & $-0.68$ \ci{-1.30}{-0.17} & 0.48 \ci{-0.67}{1.62} & 5.34 \ci{3.14}{7.65} & $-0.64$ \c” | 7.65 | 7.6480 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.130` |
| `R1.supp-tab-appexpcodecs.131` | -0.64 — “X4 & $-0.68$ \ci{-1.30}{-0.17} & 0.48 \ci{-0.67}{1.62} & 5.34 \ci{3.14}{7.65} & $-0.64$ \c” | -0.64 | -0.6446 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.131` |
| `R1.supp-tab-appexpcodecs.132` | -1.32 — “X4 & $-0.68$ \ci{-1.30}{-0.17} & 0.48 \ci{-0.67}{1.62} & 5.34 \ci{3.14}{7.65} & $-0.64$ \c” | -1.32 | -1.3189 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.132` |
| `R1.supp-tab-appexpcodecs.133` | 0.03 — “X4 & $-0.68$ \ci{-1.30}{-0.17} & 0.48 \ci{-0.67}{1.62} & 5.34 \ci{3.14}{7.65} & $-0.64$ \c” | 0.03 | 0.0306 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.133` |
| `R1.supp-tab-appexpcodecs.134` | 1.32 — “X4 & $-0.68$ \ci{-1.30}{-0.17} & 0.48 \ci{-0.67}{1.62} & 5.34 \ci{3.14}{7.65} & $-0.64$ \c” | 1.32 | 1.3193 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.134` |
| `R1.supp-tab-appexpcodecs.135` | -0.40 — “X4 & $-0.68$ \ci{-1.30}{-0.17} & 0.48 \ci{-0.67}{1.62} & 5.34 \ci{3.14}{7.65} & $-0.64$ \c” | -0.40 | -0.3993 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.135` |
| `R1.supp-tab-appexpcodecs.136` | 3.19 — “X4 & $-0.68$ \ci{-1.30}{-0.17} & 0.48 \ci{-0.67}{1.62} & 5.34 \ci{3.14}{7.65} & $-0.64$ \c” | 3.19 | 3.1896 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.136` |
| `R1.supp-tab-appexpcodecs.137` | 3.99 — “X4 & $-0.68$ \ci{-1.30}{-0.17} & 0.48 \ci{-0.67}{1.62} & 5.34 \ci{3.14}{7.65} & $-0.64$ \c” | 3.99 | 3.9894 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.137` |
| `R1.supp-tab-appexpcodecs.138` | 1.59 — “X4 & $-0.68$ \ci{-1.30}{-0.17} & 0.48 \ci{-0.67}{1.62} & 5.34 \ci{3.14}{7.65} & $-0.64$ \c” | 1.59 | 1.5926 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.138` |
| `R1.supp-tab-appexpcodecs.139` | 6.43 — “X4 & $-0.68$ \ci{-1.30}{-0.17} & 0.48 \ci{-0.67}{1.62} & 5.34 \ci{3.14}{7.65} & $-0.64$ \c” | 6.43 | 6.4265 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.139` |
| `R1.supp-tab-appexpcodecs.140` | 0.35 — “X5 & 0.35 \ci{-0.18}{0.91} & 1.10 \ci{0.02}{2.21} & 3.64 \ci{1.82}{5.49} & 0.23 \ci{-0.39}” | 0.35 | 0.3484 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.140` |
| `R1.supp-tab-appexpcodecs.141` | -0.18 — “X5 & 0.35 \ci{-0.18}{0.91} & 1.10 \ci{0.02}{2.21} & 3.64 \ci{1.82}{5.49} & 0.23 \ci{-0.39}” | -0.18 | -0.1828 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.141` |
| `R1.supp-tab-appexpcodecs.142` | 0.91 — “X5 & 0.35 \ci{-0.18}{0.91} & 1.10 \ci{0.02}{2.21} & 3.64 \ci{1.82}{5.49} & 0.23 \ci{-0.39}” | 0.91 | 0.9099 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.142` |
| `R1.supp-tab-appexpcodecs.143` | 1.10 — “X5 & 0.35 \ci{-0.18}{0.91} & 1.10 \ci{0.02}{2.21} & 3.64 \ci{1.82}{5.49} & 0.23 \ci{-0.39}” | 1.10 | 1.0980 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.143` |
| `R1.supp-tab-appexpcodecs.144` | 0.02 — “X5 & 0.35 \ci{-0.18}{0.91} & 1.10 \ci{0.02}{2.21} & 3.64 \ci{1.82}{5.49} & 0.23 \ci{-0.39}” | 0.02 | 0.0234 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.144` |
| `R1.supp-tab-appexpcodecs.145` | 2.21 — “X5 & 0.35 \ci{-0.18}{0.91} & 1.10 \ci{0.02}{2.21} & 3.64 \ci{1.82}{5.49} & 0.23 \ci{-0.39}” | 2.21 | 2.2113 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.145` |
| `R1.supp-tab-appexpcodecs.146` | 3.64 — “X5 & 0.35 \ci{-0.18}{0.91} & 1.10 \ci{0.02}{2.21} & 3.64 \ci{1.82}{5.49} & 0.23 \ci{-0.39}” | 3.64 | 3.6382 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.146` |
| `R1.supp-tab-appexpcodecs.147` | 1.82 — “X5 & 0.35 \ci{-0.18}{0.91} & 1.10 \ci{0.02}{2.21} & 3.64 \ci{1.82}{5.49} & 0.23 \ci{-0.39}” | 1.82 | 1.8244 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.147` |
| `R1.supp-tab-appexpcodecs.148` | 5.49 — “X5 & 0.35 \ci{-0.18}{0.91} & 1.10 \ci{0.02}{2.21} & 3.64 \ci{1.82}{5.49} & 0.23 \ci{-0.39}” | 5.49 | 5.4947 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.148` |
| `R1.supp-tab-appexpcodecs.149` | 0.23 — “X5 & 0.35 \ci{-0.18}{0.91} & 1.10 \ci{0.02}{2.21} & 3.64 \ci{1.82}{5.49} & 0.23 \ci{-0.39}” | 0.23 | 0.2317 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.149` |
| `R1.supp-tab-appexpcodecs.150` | -0.39 — “X5 & 0.35 \ci{-0.18}{0.91} & 1.10 \ci{0.02}{2.21} & 3.64 \ci{1.82}{5.49} & 0.23 \ci{-0.39}” | -0.39 | -0.3852 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.150` |
| `R1.supp-tab-appexpcodecs.151` | 0.93 — “X5 & 0.35 \ci{-0.18}{0.91} & 1.10 \ci{0.02}{2.21} & 3.64 \ci{1.82}{5.49} & 0.23 \ci{-0.39}” | 0.93 | 0.9295 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.151` |
| `R1.supp-tab-appexpcodecs.152` | 0.21 — “X5 & 0.35 \ci{-0.18}{0.91} & 1.10 \ci{0.02}{2.21} & 3.64 \ci{1.82}{5.49} & 0.23 \ci{-0.39}” | 0.21 | 0.2098 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.152` |
| `R1.supp-tab-appexpcodecs.153` | -1.15 — “X5 & 0.35 \ci{-0.18}{0.91} & 1.10 \ci{0.02}{2.21} & 3.64 \ci{1.82}{5.49} & 0.23 \ci{-0.39}” | -1.15 | -1.1480 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.153` |
| `R1.supp-tab-appexpcodecs.154` | 1.63 — “X5 & 0.35 \ci{-0.18}{0.91} & 1.10 \ci{0.02}{2.21} & 3.64 \ci{1.82}{5.49} & 0.23 \ci{-0.39}” | 1.63 | 1.6340 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.154` |
| `R1.supp-tab-appexpcodecs.155` | 0.74 — “X5 & 0.35 \ci{-0.18}{0.91} & 1.10 \ci{0.02}{2.21} & 3.64 \ci{1.82}{5.49} & 0.23 \ci{-0.39}” | 0.74 | 0.7383 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.155` |
| `R1.supp-tab-appexpcodecs.156` | -1.19 — “X5 & 0.35 \ci{-0.18}{0.91} & 1.10 \ci{0.02}{2.21} & 3.64 \ci{1.82}{5.49} & 0.23 \ci{-0.39}” | -1.19 | -1.1873 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.156` |
| `R1.supp-tab-appexpcodecs.157` | 2.72 — “X5 & 0.35 \ci{-0.18}{0.91} & 1.10 \ci{0.02}{2.21} & 3.64 \ci{1.82}{5.49} & 0.23 \ci{-0.39}” | 2.72 | 2.7194 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.157` |
| `R1.supp-tab-appexpcodecs.158` | -0.27 — “X6 & $-0.27$ \ci{-0.59}{0.03} & $-0.19$ \ci{-0.69}{0.34} & 0.46 \ci{-0.45}{1.40} & $-0.24$” | -0.27 | -0.2664 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.158` |
| `R1.supp-tab-appexpcodecs.159` | -0.59 — “X6 & $-0.27$ \ci{-0.59}{0.03} & $-0.19$ \ci{-0.69}{0.34} & 0.46 \ci{-0.45}{1.40} & $-0.24$” | -0.59 | -0.5906 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.159` |
| `R1.supp-tab-appexpcodecs.160` | 0.03 — “X6 & $-0.27$ \ci{-0.59}{0.03} & $-0.19$ \ci{-0.69}{0.34} & 0.46 \ci{-0.45}{1.40} & $-0.24$” | 0.03 | 0.0336 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.160` |
| `R1.supp-tab-appexpcodecs.161` | -0.19 — “X6 & $-0.27$ \ci{-0.59}{0.03} & $-0.19$ \ci{-0.69}{0.34} & 0.46 \ci{-0.45}{1.40} & $-0.24$” | -0.19 | -0.1869 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.161` |
| `R1.supp-tab-appexpcodecs.162` | -0.69 — “X6 & $-0.27$ \ci{-0.59}{0.03} & $-0.19$ \ci{-0.69}{0.34} & 0.46 \ci{-0.45}{1.40} & $-0.24$” | -0.69 | -0.6886 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.162` |
| `R1.supp-tab-appexpcodecs.163` | 0.34 — “X6 & $-0.27$ \ci{-0.59}{0.03} & $-0.19$ \ci{-0.69}{0.34} & 0.46 \ci{-0.45}{1.40} & $-0.24$” | 0.34 | 0.3368 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.163` |
| `R1.supp-tab-appexpcodecs.164` | 0.46 — “X6 & $-0.27$ \ci{-0.59}{0.03} & $-0.19$ \ci{-0.69}{0.34} & 0.46 \ci{-0.45}{1.40} & $-0.24$” | 0.46 | 0.4571 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.164` |
| `R1.supp-tab-appexpcodecs.165` | -0.45 — “X6 & $-0.27$ \ci{-0.59}{0.03} & $-0.19$ \ci{-0.69}{0.34} & 0.46 \ci{-0.45}{1.40} & $-0.24$” | -0.45 | -0.4486 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.165` |
| `R1.supp-tab-appexpcodecs.166` | 1.40 — “X6 & $-0.27$ \ci{-0.59}{0.03} & $-0.19$ \ci{-0.69}{0.34} & 0.46 \ci{-0.45}{1.40} & $-0.24$” | 1.40 | 1.3997 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.166` |
| `R1.supp-tab-appexpcodecs.167` | -0.24 — “X6 & $-0.27$ \ci{-0.59}{0.03} & $-0.19$ \ci{-0.69}{0.34} & 0.46 \ci{-0.45}{1.40} & $-0.24$” | -0.24 | -0.2436 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.167` |
| `R1.supp-tab-appexpcodecs.168` | -0.66 — “X6 & $-0.27$ \ci{-0.59}{0.03} & $-0.19$ \ci{-0.69}{0.34} & 0.46 \ci{-0.45}{1.40} & $-0.24$” | -0.66 | -0.6594 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.168` |
| `R1.supp-tab-appexpcodecs.169` | 0.14 — “X6 & $-0.27$ \ci{-0.59}{0.03} & $-0.19$ \ci{-0.69}{0.34} & 0.46 \ci{-0.45}{1.40} & $-0.24$” | 0.14 | 0.1403 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.169` |
| `R1.supp-tab-appexpcodecs.170` | -0.04 — “X6 & $-0.27$ \ci{-0.59}{0.03} & $-0.19$ \ci{-0.69}{0.34} & 0.46 \ci{-0.45}{1.40} & $-0.24$” | -0.04 | -0.0436 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.170` |
| `R1.supp-tab-appexpcodecs.171` | -0.79 — “X6 & $-0.27$ \ci{-0.59}{0.03} & $-0.19$ \ci{-0.69}{0.34} & 0.46 \ci{-0.45}{1.40} & $-0.24$” | -0.79 | -0.7881 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.171` |
| `R1.supp-tab-appexpcodecs.172` | 0.72 — “X6 & $-0.27$ \ci{-0.59}{0.03} & $-0.19$ \ci{-0.69}{0.34} & 0.46 \ci{-0.45}{1.40} & $-0.24$” | 0.72 | 0.7222 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.172` |
| `R1.supp-tab-appexpcodecs.173` | 0.48 — “X6 & $-0.27$ \ci{-0.59}{0.03} & $-0.19$ \ci{-0.69}{0.34} & 0.46 \ci{-0.45}{1.40} & $-0.24$” | 0.48 | 0.4802 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.173` |
| `R1.supp-tab-appexpcodecs.174` | -0.61 — “X6 & $-0.27$ \ci{-0.59}{0.03} & $-0.19$ \ci{-0.69}{0.34} & 0.46 \ci{-0.45}{1.40} & $-0.24$” | -0.61 | -0.6105 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.174` |
| `R1.supp-tab-appexpcodecs.175` | 1.58 — “X6 & $-0.27$ \ci{-0.59}{0.03} & $-0.19$ \ci{-0.69}{0.34} & 0.46 \ci{-0.45}{1.40} & $-0.24$” | 1.58 | 1.5814 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.175` |
| `R1.supp-tab-appexpcodecs.176` | 0.9886 — “bitrate achieved / target, median & 0.9886 & 0.9951 & 1.0170 & 0.9393 & 0.9819 & 1.0084 \\” | 0.9886 | 0.9886 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.176` |
| `R1.supp-tab-appexpcodecs.177` | 0.9951 — “bitrate achieved / target, median & 0.9886 & 0.9951 & 1.0170 & 0.9393 & 0.9819 & 1.0084 \\” | 0.9951 | 0.9951 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.177` |
| `R1.supp-tab-appexpcodecs.178` | 1.0170 — “bitrate achieved / target, median & 0.9886 & 0.9951 & 1.0170 & 0.9393 & 0.9819 & 1.0084 \\” | 1.0170 | 1.0170 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.178` |
| `R1.supp-tab-appexpcodecs.179` | 0.9393 — “bitrate achieved / target, median & 0.9886 & 0.9951 & 1.0170 & 0.9393 & 0.9819 & 1.0084 \\” | 0.9393 | 0.9393 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.179` |
| `R1.supp-tab-appexpcodecs.180` | 0.9819 — “bitrate achieved / target, median & 0.9886 & 0.9951 & 1.0170 & 0.9393 & 0.9819 & 1.0084 \\” | 0.9819 | 0.9819 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.180` |
| `R1.supp-tab-appexpcodecs.181` | 1.0084 — “bitrate achieved / target, median & 0.9886 & 0.9951 & 1.0170 & 0.9393 & 0.9819 & 1.0084 \\” | 1.0084 | 1.0084 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.181` |
| `R1.supp-tab-appexpcodecs.182` | 0 — “videos outside $\pm10$\% of target & 0 & 0 & 19 & 113 & 96 & 119 \\” | 0 | 0.0000 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.182` |
| `R1.supp-tab-appexpcodecs.183` | 0 — “videos outside $\pm10$\% of target & 0 & 0 & 19 & 113 & 96 & 119 \\” | 0 | 0.0000 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.183` |
| `R1.supp-tab-appexpcodecs.184` | 19 — “videos outside $\pm10$\% of target & 0 & 0 & 19 & 113 & 96 & 119 \\” | 19 | 19.00 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.184` |
| `R1.supp-tab-appexpcodecs.185` | 113 — “videos outside $\pm10$\% of target & 0 & 0 & 19 & 113 & 96 & 119 \\” | 113 | 113.00 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.185` |
| `R1.supp-tab-appexpcodecs.186` | 96 — “videos outside $\pm10$\% of target & 0 & 0 & 19 & 113 & 96 & 119 \\” | 96 | 96.00 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.186` |
| `R1.supp-tab-appexpcodecs.187` | 119 — “videos outside $\pm10$\% of target & 0 & 0 & 19 & 113 & 96 & 119 \\” | 119 | 119.00 | `revision-1/exploratory/e8.json` | `python verify/claim.py R1.supp-tab-appexpcodecs.187` |

- `R1.supp-tab-appexpcodecs.2` — weights: EMA
- `R1.supp-tab-appexpcodecs.3` — weights: EMA
- `R1.supp-tab-appexpcodecs.4` — weights: EMA
- `R1.supp-tab-appexpcodecs.5` — weights: EMA
- `R1.supp-tab-appexpcodecs.6` — weights: EMA
- `R1.supp-tab-appexpcodecs.7` — weights: EMA
- `R1.supp-tab-appexpcodecs.8` — weights: EMA
- `R1.supp-tab-appexpcodecs.9` — weights: EMA
- `R1.supp-tab-appexpcodecs.10` — weights: EMA
- `R1.supp-tab-appexpcodecs.11` — weights: EMA
- `R1.supp-tab-appexpcodecs.12` — weights: EMA
- `R1.supp-tab-appexpcodecs.13` — weights: EMA
- `R1.supp-tab-appexpcodecs.14` — weights: EMA
- `R1.supp-tab-appexpcodecs.15` — weights: EMA
- `R1.supp-tab-appexpcodecs.16` — weights: EMA
- `R1.supp-tab-appexpcodecs.17` — weights: EMA
- `R1.supp-tab-appexpcodecs.18` — weights: EMA
- `R1.supp-tab-appexpcodecs.19` — weights: EMA
- `R1.supp-tab-appexpcodecs.20` — weights: EMA
- `R1.supp-tab-appexpcodecs.21` — weights: EMA
- `R1.supp-tab-appexpcodecs.22` — weights: EMA
- `R1.supp-tab-appexpcodecs.23` — weights: EMA
- `R1.supp-tab-appexpcodecs.24` — weights: EMA
- `R1.supp-tab-appexpcodecs.25` — weights: EMA
- `R1.supp-tab-appexpcodecs.26` — weights: raw
- `R1.supp-tab-appexpcodecs.27` — weights: raw
- `R1.supp-tab-appexpcodecs.28` — weights: raw
- `R1.supp-tab-appexpcodecs.29` — weights: raw
- `R1.supp-tab-appexpcodecs.30` — weights: raw
- `R1.supp-tab-appexpcodecs.31` — weights: raw
- `R1.supp-tab-appexpcodecs.32` — weights: raw
- `R1.supp-tab-appexpcodecs.33` — weights: raw
- `R1.supp-tab-appexpcodecs.34` — weights: raw
- `R1.supp-tab-appexpcodecs.35` — weights: raw
- `R1.supp-tab-appexpcodecs.36` — weights: raw
- `R1.supp-tab-appexpcodecs.37` — weights: raw
- `R1.supp-tab-appexpcodecs.38` — weights: raw
- `R1.supp-tab-appexpcodecs.39` — weights: raw
- `R1.supp-tab-appexpcodecs.40` — weights: raw
- `R1.supp-tab-appexpcodecs.41` — weights: raw
- `R1.supp-tab-appexpcodecs.42` — weights: raw
- `R1.supp-tab-appexpcodecs.43` — weights: raw
- `R1.supp-tab-appexpcodecs.44` — weights: raw
- `R1.supp-tab-appexpcodecs.45` — weights: raw
- `R1.supp-tab-appexpcodecs.46` — weights: raw
- `R1.supp-tab-appexpcodecs.47` — weights: raw
- `R1.supp-tab-appexpcodecs.48` — weights: raw
- `R1.supp-tab-appexpcodecs.49` — weights: raw
- `R1.supp-tab-appexpcodecs.50` — weights: raw
- `R1.supp-tab-appexpcodecs.51` — weights: raw
- `R1.supp-tab-appexpcodecs.52` — weights: raw
- `R1.supp-tab-appexpcodecs.53` — weights: raw
- `R1.supp-tab-appexpcodecs.54` — weights: raw
- `R1.supp-tab-appexpcodecs.55` — weights: raw
- `R1.supp-tab-appexpcodecs.56` — weights: raw
- `R1.supp-tab-appexpcodecs.57` — weights: raw
- `R1.supp-tab-appexpcodecs.58` — weights: raw
- `R1.supp-tab-appexpcodecs.59` — weights: raw
- `R1.supp-tab-appexpcodecs.60` — weights: raw
- `R1.supp-tab-appexpcodecs.61` — weights: raw
- `R1.supp-tab-appexpcodecs.62` — weights: raw
- `R1.supp-tab-appexpcodecs.63` — weights: raw
- `R1.supp-tab-appexpcodecs.64` — weights: raw
- `R1.supp-tab-appexpcodecs.65` — weights: raw
- `R1.supp-tab-appexpcodecs.66` — weights: raw
- `R1.supp-tab-appexpcodecs.67` — weights: raw
- `R1.supp-tab-appexpcodecs.68` — weights: EMA
- `R1.supp-tab-appexpcodecs.69` — weights: EMA
- `R1.supp-tab-appexpcodecs.70` — weights: EMA
- `R1.supp-tab-appexpcodecs.71` — weights: EMA
- `R1.supp-tab-appexpcodecs.72` — weights: EMA
- `R1.supp-tab-appexpcodecs.73` — weights: EMA
- `R1.supp-tab-appexpcodecs.74` — weights: EMA
- `R1.supp-tab-appexpcodecs.75` — weights: EMA
- `R1.supp-tab-appexpcodecs.76` — weights: EMA
- `R1.supp-tab-appexpcodecs.77` — weights: EMA
- `R1.supp-tab-appexpcodecs.78` — weights: EMA
- `R1.supp-tab-appexpcodecs.79` — weights: EMA
- `R1.supp-tab-appexpcodecs.80` — weights: EMA
- `R1.supp-tab-appexpcodecs.81` — weights: EMA
- `R1.supp-tab-appexpcodecs.82` — weights: EMA
- `R1.supp-tab-appexpcodecs.83` — weights: EMA
- `R1.supp-tab-appexpcodecs.84` — weights: EMA
- `R1.supp-tab-appexpcodecs.85` — weights: EMA
- `R1.supp-tab-appexpcodecs.86` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.87` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.88` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.89` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.90` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.91` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.92` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.93` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.94` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.95` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.96` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.97` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.98` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.99` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.100` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.101` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.102` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.103` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.104` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.105` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.106` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.107` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.108` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.109` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.110` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.111` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.112` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.113` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.114` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.115` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.116` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.117` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.118` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.119` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.120` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.121` — weights: EMA and raw
- `R1.supp-tab-appexpcodecs.122` — weights: raw
- `R1.supp-tab-appexpcodecs.123` — weights: raw
- `R1.supp-tab-appexpcodecs.124` — weights: raw
- `R1.supp-tab-appexpcodecs.125` — weights: raw
- `R1.supp-tab-appexpcodecs.126` — weights: raw
- `R1.supp-tab-appexpcodecs.127` — weights: raw
- `R1.supp-tab-appexpcodecs.128` — weights: raw
- `R1.supp-tab-appexpcodecs.129` — weights: raw
- `R1.supp-tab-appexpcodecs.130` — weights: raw
- `R1.supp-tab-appexpcodecs.131` — weights: raw
- `R1.supp-tab-appexpcodecs.132` — weights: raw
- `R1.supp-tab-appexpcodecs.133` — weights: raw
- `R1.supp-tab-appexpcodecs.134` — weights: raw
- `R1.supp-tab-appexpcodecs.135` — weights: raw
- `R1.supp-tab-appexpcodecs.136` — weights: raw
- `R1.supp-tab-appexpcodecs.137` — weights: raw
- `R1.supp-tab-appexpcodecs.138` — weights: raw
- `R1.supp-tab-appexpcodecs.139` — weights: raw
- `R1.supp-tab-appexpcodecs.140` — weights: raw
- `R1.supp-tab-appexpcodecs.141` — weights: raw
- `R1.supp-tab-appexpcodecs.142` — weights: raw
- `R1.supp-tab-appexpcodecs.143` — weights: raw
- `R1.supp-tab-appexpcodecs.144` — weights: raw
- `R1.supp-tab-appexpcodecs.145` — weights: raw
- `R1.supp-tab-appexpcodecs.146` — weights: raw
- `R1.supp-tab-appexpcodecs.147` — weights: raw
- `R1.supp-tab-appexpcodecs.148` — weights: raw
- `R1.supp-tab-appexpcodecs.149` — weights: raw
- `R1.supp-tab-appexpcodecs.150` — weights: raw
- `R1.supp-tab-appexpcodecs.151` — weights: raw
- `R1.supp-tab-appexpcodecs.152` — weights: raw
- `R1.supp-tab-appexpcodecs.153` — weights: raw
- `R1.supp-tab-appexpcodecs.154` — weights: raw
- `R1.supp-tab-appexpcodecs.155` — weights: raw
- `R1.supp-tab-appexpcodecs.156` — weights: raw
- `R1.supp-tab-appexpcodecs.157` — weights: raw
- `R1.supp-tab-appexpcodecs.158` — weights: raw
- `R1.supp-tab-appexpcodecs.159` — weights: raw
- `R1.supp-tab-appexpcodecs.160` — weights: raw
- `R1.supp-tab-appexpcodecs.161` — weights: raw
- `R1.supp-tab-appexpcodecs.162` — weights: raw
- `R1.supp-tab-appexpcodecs.163` — weights: raw
- `R1.supp-tab-appexpcodecs.164` — weights: raw
- `R1.supp-tab-appexpcodecs.165` — weights: raw
- `R1.supp-tab-appexpcodecs.166` — weights: raw
- `R1.supp-tab-appexpcodecs.167` — weights: raw
- `R1.supp-tab-appexpcodecs.168` — weights: raw
- `R1.supp-tab-appexpcodecs.169` — weights: raw
- `R1.supp-tab-appexpcodecs.170` — weights: raw
- `R1.supp-tab-appexpcodecs.171` — weights: raw
- `R1.supp-tab-appexpcodecs.172` — weights: raw
- `R1.supp-tab-appexpcodecs.173` — weights: raw
- `R1.supp-tab-appexpcodecs.174` — weights: raw
- `R1.supp-tab-appexpcodecs.175` — weights: raw
- `R1.supp-tab-appexpcodecs.176` — weights: -
- `R1.supp-tab-appexpcodecs.177` — weights: -
- `R1.supp-tab-appexpcodecs.178` — weights: -
- `R1.supp-tab-appexpcodecs.179` — weights: -
- `R1.supp-tab-appexpcodecs.180` — weights: -
- `R1.supp-tab-appexpcodecs.181` — weights: -
- `R1.supp-tab-appexpcodecs.182` — weights: -
- `R1.supp-tab-appexpcodecs.183` — weights: -
- `R1.supp-tab-appexpcodecs.184` — weights: -
- `R1.supp-tab-appexpcodecs.185` — weights: -
- `R1.supp-tab-appexpcodecs.186` — weights: -
- `R1.supp-tab-appexpcodecs.187` — weights: -

## R1.supp-tab-appexpladder — Revision 1 — Supplementary Material, tab:appexpladder

*Supplementary Material, tab:appexpladder; `\label{tab:appexpladder}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-tab-appexpladder.1` | 10,000 — “estimand) with 95\% percentile intervals ($B = 10{,}000$; seeds, then 140” | 10000 | 10000.00 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-tab-appexpladder.1` |
| `R1.supp-tab-appexpladder.2` | 98.77 — “E1 (EMA) & 98.77 \ci{97.94}{99.43} & 95.86 \ci{94.21}{97.27} & $-0.06$ \ci{-0.23}{0.08} & ” | 98.77 | 98.77 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.2` |
| `R1.supp-tab-appexpladder.3` | 97.94 — “E1 (EMA) & 98.77 \ci{97.94}{99.43} & 95.86 \ci{94.21}{97.27} & $-0.06$ \ci{-0.23}{0.08} & ” | 97.94 | 97.94 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.3` |
| `R1.supp-tab-appexpladder.4` | 99.43 — “E1 (EMA) & 98.77 \ci{97.94}{99.43} & 95.86 \ci{94.21}{97.27} & $-0.06$ \ci{-0.23}{0.08} & ” | 99.43 | 99.43 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.4` |
| `R1.supp-tab-appexpladder.5` | 95.86 — “E1 (EMA) & 98.77 \ci{97.94}{99.43} & 95.86 \ci{94.21}{97.27} & $-0.06$ \ci{-0.23}{0.08} & ” | 95.86 | 95.86 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.5` |
| `R1.supp-tab-appexpladder.6` | 94.21 — “E1 (EMA) & 98.77 \ci{97.94}{99.43} & 95.86 \ci{94.21}{97.27} & $-0.06$ \ci{-0.23}{0.08} & ” | 94.21 | 94.21 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.6` |
| `R1.supp-tab-appexpladder.7` | 97.27 — “E1 (EMA) & 98.77 \ci{97.94}{99.43} & 95.86 \ci{94.21}{97.27} & $-0.06$ \ci{-0.23}{0.08} & ” | 97.27 | 97.27 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.7` |
| `R1.supp-tab-appexpladder.8` | -0.06 — “E1 (EMA) & 98.77 \ci{97.94}{99.43} & 95.86 \ci{94.21}{97.27} & $-0.06$ \ci{-0.23}{0.08} & ” | -0.06 | -0.0629 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.8` |
| `R1.supp-tab-appexpladder.9` | -0.23 — “E1 (EMA) & 98.77 \ci{97.94}{99.43} & 95.86 \ci{94.21}{97.27} & $-0.06$ \ci{-0.23}{0.08} & ” | -0.23 | -0.2266 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.9` |
| `R1.supp-tab-appexpladder.10` | 0.08 — “E1 (EMA) & 98.77 \ci{97.94}{99.43} & 95.86 \ci{94.21}{97.27} & $-0.06$ \ci{-0.23}{0.08} & ” | 0.08 | 0.0791 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.10` |
| `R1.supp-tab-appexpladder.11` | -0.64 — “E1 (EMA) & 98.77 \ci{97.94}{99.43} & 95.86 \ci{94.21}{97.27} & $-0.06$ \ci{-0.23}{0.08} & ” | -0.64 | -0.6407 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.11` |
| `R1.supp-tab-appexpladder.12` | -1.45 — “E1 (EMA) & 98.77 \ci{97.94}{99.43} & 95.86 \ci{94.21}{97.27} & $-0.06$ \ci{-0.23}{0.08} & ” | -1.45 | -1.4481 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.12` |
| `R1.supp-tab-appexpladder.13` | 0.07 — “E1 (EMA) & 98.77 \ci{97.94}{99.43} & 95.86 \ci{94.21}{97.27} & $-0.06$ \ci{-0.23}{0.08} & ” | 0.07 | 0.0723 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.13` |
| `R1.supp-tab-appexpladder.14` | 98.30 — “Fair-N (EMA) & 98.30 \ci{97.20}{99.16} & 94.35 \ci{92.26}{96.19} & $-0.44$ \ci{-1.24}{0.09” | 98.30 | 98.30 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.14` |
| `R1.supp-tab-appexpladder.15` | 97.20 — “Fair-N (EMA) & 98.30 \ci{97.20}{99.16} & 94.35 \ci{92.26}{96.19} & $-0.44$ \ci{-1.24}{0.09” | 97.20 | 97.20 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.15` |
| `R1.supp-tab-appexpladder.16` | 99.16 — “Fair-N (EMA) & 98.30 \ci{97.20}{99.16} & 94.35 \ci{92.26}{96.19} & $-0.44$ \ci{-1.24}{0.09” | 99.16 | 99.16 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.16` |
| `R1.supp-tab-appexpladder.17` | 94.35 — “Fair-N (EMA) & 98.30 \ci{97.20}{99.16} & 94.35 \ci{92.26}{96.19} & $-0.44$ \ci{-1.24}{0.09” | 94.35 | 94.35 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.17` |
| `R1.supp-tab-appexpladder.18` | 92.26 — “Fair-N (EMA) & 98.30 \ci{97.20}{99.16} & 94.35 \ci{92.26}{96.19} & $-0.44$ \ci{-1.24}{0.09” | 92.26 | 92.26 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.18` |
| `R1.supp-tab-appexpladder.19` | 96.19 — “Fair-N (EMA) & 98.30 \ci{97.20}{99.16} & 94.35 \ci{92.26}{96.19} & $-0.44$ \ci{-1.24}{0.09” | 96.19 | 96.19 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.19` |
| `R1.supp-tab-appexpladder.20` | -0.44 — “Fair-N (EMA) & 98.30 \ci{97.20}{99.16} & 94.35 \ci{92.26}{96.19} & $-0.44$ \ci{-1.24}{0.09” | -0.44 | -0.4422 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.20` |
| `R1.supp-tab-appexpladder.21` | -1.24 — “Fair-N (EMA) & 98.30 \ci{97.20}{99.16} & 94.35 \ci{92.26}{96.19} & $-0.44$ \ci{-1.24}{0.09” | -1.24 | -1.2419 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.21` |
| `R1.supp-tab-appexpladder.22` | 0.09 — “Fair-N (EMA) & 98.30 \ci{97.20}{99.16} & 94.35 \ci{92.26}{96.19} & $-0.44$ \ci{-1.24}{0.09” | 0.09 | 0.0948 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.22` |
| `R1.supp-tab-appexpladder.23` | -1.28 — “Fair-N (EMA) & 98.30 \ci{97.20}{99.16} & 94.35 \ci{92.26}{96.19} & $-0.44$ \ci{-1.24}{0.09” | -1.28 | -1.2785 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.23` |
| `R1.supp-tab-appexpladder.24` | -2.42 — “Fair-N (EMA) & 98.30 \ci{97.20}{99.16} & 94.35 \ci{92.26}{96.19} & $-0.44$ \ci{-1.24}{0.09” | -2.42 | -2.4218 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.24` |
| `R1.supp-tab-appexpladder.25` | -0.25 — “Fair-N (EMA) & 98.30 \ci{97.20}{99.16} & 94.35 \ci{92.26}{96.19} & $-0.44$ \ci{-1.24}{0.09” | -0.25 | -0.2534 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.25` |
| `R1.supp-tab-appexpladder.26` | 98.64 — “Fair-W (EMA) & 98.64 \ci{97.69}{99.39} & 95.28 \ci{93.44}{96.85} & $-0.13$ \ci{-0.39}{0.05” | 98.64 | 98.64 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.26` |
| `R1.supp-tab-appexpladder.27` | 97.69 — “Fair-W (EMA) & 98.64 \ci{97.69}{99.39} & 95.28 \ci{93.44}{96.85} & $-0.13$ \ci{-0.39}{0.05” | 97.69 | 97.69 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.27` |
| `R1.supp-tab-appexpladder.28` | 99.39 — “Fair-W (EMA) & 98.64 \ci{97.69}{99.39} & 95.28 \ci{93.44}{96.85} & $-0.13$ \ci{-0.39}{0.05” | 99.39 | 99.39 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.28` |
| `R1.supp-tab-appexpladder.29` | 95.28 — “Fair-W (EMA) & 98.64 \ci{97.69}{99.39} & 95.28 \ci{93.44}{96.85} & $-0.13$ \ci{-0.39}{0.05” | 95.28 | 95.28 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.29` |
| `R1.supp-tab-appexpladder.30` | 93.44 — “Fair-W (EMA) & 98.64 \ci{97.69}{99.39} & 95.28 \ci{93.44}{96.85} & $-0.13$ \ci{-0.39}{0.05” | 93.44 | 93.44 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.30` |
| `R1.supp-tab-appexpladder.31` | 96.85 — “Fair-W (EMA) & 98.64 \ci{97.69}{99.39} & 95.28 \ci{93.44}{96.85} & $-0.13$ \ci{-0.39}{0.05” | 96.85 | 96.85 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.31` |
| `R1.supp-tab-appexpladder.32` | -0.13 — “Fair-W (EMA) & 98.64 \ci{97.69}{99.39} & 95.28 \ci{93.44}{96.85} & $-0.13$ \ci{-0.39}{0.05” | -0.13 | -0.1259 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.32` |
| `R1.supp-tab-appexpladder.33` | -0.39 — “Fair-W (EMA) & 98.64 \ci{97.69}{99.39} & 95.28 \ci{93.44}{96.85} & $-0.13$ \ci{-0.39}{0.05” | -0.39 | -0.3907 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.33` |
| `R1.supp-tab-appexpladder.34` | 0.05 — “Fair-W (EMA) & 98.64 \ci{97.69}{99.39} & 95.28 \ci{93.44}{96.85} & $-0.13$ \ci{-0.39}{0.05” | 0.05 | 0.0536 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.34` |
| `R1.supp-tab-appexpladder.35` | -0.91 — “Fair-W (EMA) & 98.64 \ci{97.69}{99.39} & 95.28 \ci{93.44}{96.85} & $-0.13$ \ci{-0.39}{0.05” | -0.91 | -0.9060 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.35` |
| `R1.supp-tab-appexpladder.36` | -1.81 — “Fair-W (EMA) & 98.64 \ci{97.69}{99.39} & 95.28 \ci{93.44}{96.85} & $-0.13$ \ci{-0.39}{0.05” | -1.81 | -1.8138 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.36` |
| `R1.supp-tab-appexpladder.37` | -0.13 — “Fair-W (EMA) & 98.64 \ci{97.69}{99.39} & 95.28 \ci{93.44}{96.85} & $-0.13$ \ci{-0.39}{0.05” | -0.13 | -0.1314 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.37` |
| `R1.supp-tab-appexpladder.38` | 97.46 — “CAFRL as specified (EMA) & 97.46 \ci{96.02}{98.63} & 92.15 \ci{89.73}{94.32} & $-0.06$ \ci” | 97.46 | 97.46 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.38` |
| `R1.supp-tab-appexpladder.39` | 96.02 — “CAFRL as specified (EMA) & 97.46 \ci{96.02}{98.63} & 92.15 \ci{89.73}{94.32} & $-0.06$ \ci” | 96.02 | 96.02 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.39` |
| `R1.supp-tab-appexpladder.40` | 98.63 — “CAFRL as specified (EMA) & 97.46 \ci{96.02}{98.63} & 92.15 \ci{89.73}{94.32} & $-0.06$ \ci” | 98.63 | 98.63 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.40` |
| `R1.supp-tab-appexpladder.41` | 92.15 — “CAFRL as specified (EMA) & 97.46 \ci{96.02}{98.63} & 92.15 \ci{89.73}{94.32} & $-0.06$ \ci” | 92.15 | 92.15 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.41` |
| `R1.supp-tab-appexpladder.42` | 89.73 — “CAFRL as specified (EMA) & 97.46 \ci{96.02}{98.63} & 92.15 \ci{89.73}{94.32} & $-0.06$ \ci” | 89.73 | 89.73 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.42` |
| `R1.supp-tab-appexpladder.43` | 94.32 — “CAFRL as specified (EMA) & 97.46 \ci{96.02}{98.63} & 92.15 \ci{89.73}{94.32} & $-0.06$ \ci” | 94.32 | 94.32 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.43` |
| `R1.supp-tab-appexpladder.44` | -0.06 — “CAFRL as specified (EMA) & 97.46 \ci{96.02}{98.63} & 92.15 \ci{89.73}{94.32} & $-0.06$ \ci” | -0.06 | -0.0582 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.44` |
| `R1.supp-tab-appexpladder.45` | -0.41 — “CAFRL as specified (EMA) & 97.46 \ci{96.02}{98.63} & 92.15 \ci{89.73}{94.32} & $-0.06$ \ci” | -0.41 | -0.4116 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.45` |
| `R1.supp-tab-appexpladder.46` | 0.33 — “CAFRL as specified (EMA) & 97.46 \ci{96.02}{98.63} & 92.15 \ci{89.73}{94.32} & $-0.06$ \ci” | 0.33 | 0.3312 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.46` |
| `R1.supp-tab-appexpladder.47` | -0.02 — “CAFRL as specified (EMA) & 97.46 \ci{96.02}{98.63} & 92.15 \ci{89.73}{94.32} & $-0.06$ \ci” | -0.02 | -0.0187 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.47` |
| `R1.supp-tab-appexpladder.48` | -0.84 — “CAFRL as specified (EMA) & 97.46 \ci{96.02}{98.63} & 92.15 \ci{89.73}{94.32} & $-0.06$ \ci” | -0.84 | -0.8440 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.48` |
| `R1.supp-tab-appexpladder.49` | 0.81 — “CAFRL as specified (EMA) & 97.46 \ci{96.02}{98.63} & 92.15 \ci{89.73}{94.32} & $-0.06$ \ci” | 0.81 | 0.8057 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.49` |
| `R1.supp-tab-appexpladder.50` | 98.59 — “SpatialBase (raw) & 98.59 \ci{97.64}{99.31} & 94.91 \ci{92.92}{96.59} & $-0.001$ \ci{-0.11” | 98.59 | 98.59 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.50` |
| `R1.supp-tab-appexpladder.51` | 97.64 — “SpatialBase (raw) & 98.59 \ci{97.64}{99.31} & 94.91 \ci{92.92}{96.59} & $-0.001$ \ci{-0.11” | 97.64 | 97.64 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.51` |
| `R1.supp-tab-appexpladder.52` | 99.31 — “SpatialBase (raw) & 98.59 \ci{97.64}{99.31} & 94.91 \ci{92.92}{96.59} & $-0.001$ \ci{-0.11” | 99.31 | 99.31 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.52` |
| `R1.supp-tab-appexpladder.53` | 94.91 — “SpatialBase (raw) & 98.59 \ci{97.64}{99.31} & 94.91 \ci{92.92}{96.59} & $-0.001$ \ci{-0.11” | 94.91 | 94.91 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.53` |
| `R1.supp-tab-appexpladder.54` | 92.92 — “SpatialBase (raw) & 98.59 \ci{97.64}{99.31} & 94.91 \ci{92.92}{96.59} & $-0.001$ \ci{-0.11” | 92.92 | 92.92 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.54` |
| `R1.supp-tab-appexpladder.55` | 96.59 — “SpatialBase (raw) & 98.59 \ci{97.64}{99.31} & 94.91 \ci{92.92}{96.59} & $-0.001$ \ci{-0.11” | 96.59 | 96.59 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.55` |
| `R1.supp-tab-appexpladder.56` | -0.001 — “SpatialBase (raw) & 98.59 \ci{97.64}{99.31} & 94.91 \ci{92.92}{96.59} & $-0.001$ \ci{-0.11” | -0.001 | -0.0013 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.56` |
| `R1.supp-tab-appexpladder.57` | -0.11 — “SpatialBase (raw) & 98.59 \ci{97.64}{99.31} & 94.91 \ci{92.92}{96.59} & $-0.001$ \ci{-0.11” | -0.11 | -0.1071 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.57` |
| `R1.supp-tab-appexpladder.58` | 0.10 — “SpatialBase (raw) & 98.59 \ci{97.64}{99.31} & 94.91 \ci{92.92}{96.59} & $-0.001$ \ci{-0.11” | 0.10 | 0.1033 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.58` |
| `R1.supp-tab-appexpladder.59` | -0.74 — “SpatialBase (raw) & 98.59 \ci{97.64}{99.31} & 94.91 \ci{92.92}{96.59} & $-0.001$ \ci{-0.11” | -0.74 | -0.7402 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.59` |
| `R1.supp-tab-appexpladder.60` | -1.51 — “SpatialBase (raw) & 98.59 \ci{97.64}{99.31} & 94.91 \ci{92.92}{96.59} & $-0.001$ \ci{-0.11” | -1.51 | -1.5077 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.60` |
| `R1.supp-tab-appexpladder.61` | -0.10 — “SpatialBase (raw) & 98.59 \ci{97.64}{99.31} & 94.91 \ci{92.92}{96.59} & $-0.001$ \ci{-0.11” | -0.10 | -0.0982 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.61` |
| `R1.supp-tab-appexpladder.62` | 98.62 — “TrunkCtrl (raw) & 98.62 \ci{97.69}{99.36} & 94.91 \ci{93.14}{96.50} & $-0.02$ \ci{-0.13}{0” | 98.62 | 98.62 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.62` |
| `R1.supp-tab-appexpladder.63` | 97.69 — “TrunkCtrl (raw) & 98.62 \ci{97.69}{99.36} & 94.91 \ci{93.14}{96.50} & $-0.02$ \ci{-0.13}{0” | 97.69 | 97.69 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.63` |
| `R1.supp-tab-appexpladder.64` | 99.36 — “TrunkCtrl (raw) & 98.62 \ci{97.69}{99.36} & 94.91 \ci{93.14}{96.50} & $-0.02$ \ci{-0.13}{0” | 99.36 | 99.36 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.64` |
| `R1.supp-tab-appexpladder.65` | 94.91 — “TrunkCtrl (raw) & 98.62 \ci{97.69}{99.36} & 94.91 \ci{93.14}{96.50} & $-0.02$ \ci{-0.13}{0” | 94.91 | 94.91 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.65` |
| `R1.supp-tab-appexpladder.66` | 93.14 — “TrunkCtrl (raw) & 98.62 \ci{97.69}{99.36} & 94.91 \ci{93.14}{96.50} & $-0.02$ \ci{-0.13}{0” | 93.14 | 93.14 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.66` |
| `R1.supp-tab-appexpladder.67` | 96.50 — “TrunkCtrl (raw) & 98.62 \ci{97.69}{99.36} & 94.91 \ci{93.14}{96.50} & $-0.02$ \ci{-0.13}{0” | 96.50 | 96.50 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.67` |
| `R1.supp-tab-appexpladder.68` | -0.02 — “TrunkCtrl (raw) & 98.62 \ci{97.69}{99.36} & 94.91 \ci{93.14}{96.50} & $-0.02$ \ci{-0.13}{0” | -0.02 | -0.0170 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.68` |
| `R1.supp-tab-appexpladder.69` | -0.13 — “TrunkCtrl (raw) & 98.62 \ci{97.69}{99.36} & 94.91 \ci{93.14}{96.50} & $-0.02$ \ci{-0.13}{0” | -0.13 | -0.1297 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.69` |
| `R1.supp-tab-appexpladder.70` | 0.09 — “TrunkCtrl (raw) & 98.62 \ci{97.69}{99.36} & 94.91 \ci{93.14}{96.50} & $-0.02$ \ci{-0.13}{0” | 0.09 | 0.0867 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.70` |
| `R1.supp-tab-appexpladder.71` | -0.45 — “TrunkCtrl (raw) & 98.62 \ci{97.69}{99.36} & 94.91 \ci{93.14}{96.50} & $-0.02$ \ci{-0.13}{0” | -0.45 | -0.4494 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.71` |
| `R1.supp-tab-appexpladder.72` | -1.41 — “TrunkCtrl (raw) & 98.62 \ci{97.69}{99.36} & 94.91 \ci{93.14}{96.50} & $-0.02$ \ci{-0.13}{0” | -1.41 | -1.4150 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.72` |
| `R1.supp-tab-appexpladder.73` | 0.53 — “TrunkCtrl (raw) & 98.62 \ci{97.69}{99.36} & 94.91 \ci{93.14}{96.50} & $-0.02$ \ci{-0.13}{0” | 0.53 | 0.5302 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.73` |
| `R1.supp-tab-appexpladder.74` | 98.81 — “E2a (raw) & 98.81 \ci{97.99}{99.46} & 95.91 \ci{94.30}{97.30} & $-0.05$ \ci{-0.17}{0.05} &” | 98.81 | 98.81 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.74` |
| `R1.supp-tab-appexpladder.75` | 97.99 — “E2a (raw) & 98.81 \ci{97.99}{99.46} & 95.91 \ci{94.30}{97.30} & $-0.05$ \ci{-0.17}{0.05} &” | 97.99 | 97.99 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.75` |
| `R1.supp-tab-appexpladder.76` | 99.46 — “E2a (raw) & 98.81 \ci{97.99}{99.46} & 95.91 \ci{94.30}{97.30} & $-0.05$ \ci{-0.17}{0.05} &” | 99.46 | 99.46 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.76` |
| `R1.supp-tab-appexpladder.77` | 95.91 — “E2a (raw) & 98.81 \ci{97.99}{99.46} & 95.91 \ci{94.30}{97.30} & $-0.05$ \ci{-0.17}{0.05} &” | 95.91 | 95.91 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.77` |
| `R1.supp-tab-appexpladder.78` | 94.30 — “E2a (raw) & 98.81 \ci{97.99}{99.46} & 95.91 \ci{94.30}{97.30} & $-0.05$ \ci{-0.17}{0.05} &” | 94.30 | 94.30 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.78` |
| `R1.supp-tab-appexpladder.79` | 97.30 — “E2a (raw) & 98.81 \ci{97.99}{99.46} & 95.91 \ci{94.30}{97.30} & $-0.05$ \ci{-0.17}{0.05} &” | 97.30 | 97.30 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.79` |
| `R1.supp-tab-appexpladder.80` | -0.05 — “E2a (raw) & 98.81 \ci{97.99}{99.46} & 95.91 \ci{94.30}{97.30} & $-0.05$ \ci{-0.17}{0.05} &” | -0.05 | -0.0548 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.80` |
| `R1.supp-tab-appexpladder.81` | -0.17 — “E2a (raw) & 98.81 \ci{97.99}{99.46} & 95.91 \ci{94.30}{97.30} & $-0.05$ \ci{-0.17}{0.05} &” | -0.17 | -0.1679 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.81` |
| `R1.supp-tab-appexpladder.82` | 0.05 — “E2a (raw) & 98.81 \ci{97.99}{99.46} & 95.91 \ci{94.30}{97.30} & $-0.05$ \ci{-0.17}{0.05} &” | 0.05 | 0.0549 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.82` |
| `R1.supp-tab-appexpladder.83` | 1.38 — “E2a (raw) & 98.81 \ci{97.99}{99.46} & 95.91 \ci{94.30}{97.30} & $-0.05$ \ci{-0.17}{0.05} &” | 1.38 | 1.3814 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.83` |
| `R1.supp-tab-appexpladder.84` | 0.51 — “E2a (raw) & 98.81 \ci{97.99}{99.46} & 95.91 \ci{94.30}{97.30} & $-0.05$ \ci{-0.17}{0.05} &” | 0.51 | 0.5063 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.84` |
| `R1.supp-tab-appexpladder.85` | 2.37 — “E2a (raw) & 98.81 \ci{97.99}{99.46} & 95.91 \ci{94.30}{97.30} & $-0.05$ \ci{-0.17}{0.05} &” | 2.37 | 2.3683 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.85` |
| `R1.supp-tab-appexpladder.86` | 99.00 — “E2b (raw) & 99.00 \ci{98.21}{99.60} & 94.70 \ci{92.50}{96.61} & 0.03 \ci{-0.09}{0.20} & 0.” | 99.00 | 99.00 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.86` |
| `R1.supp-tab-appexpladder.87` | 98.21 — “E2b (raw) & 99.00 \ci{98.21}{99.60} & 94.70 \ci{92.50}{96.61} & 0.03 \ci{-0.09}{0.20} & 0.” | 98.21 | 98.21 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.87` |
| `R1.supp-tab-appexpladder.88` | 99.60 — “E2b (raw) & 99.00 \ci{98.21}{99.60} & 94.70 \ci{92.50}{96.61} & 0.03 \ci{-0.09}{0.20} & 0.” | 99.60 | 99.60 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.88` |
| `R1.supp-tab-appexpladder.89` | 94.70 — “E2b (raw) & 99.00 \ci{98.21}{99.60} & 94.70 \ci{92.50}{96.61} & 0.03 \ci{-0.09}{0.20} & 0.” | 94.70 | 94.70 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.89` |
| `R1.supp-tab-appexpladder.90` | 92.50 — “E2b (raw) & 99.00 \ci{98.21}{99.60} & 94.70 \ci{92.50}{96.61} & 0.03 \ci{-0.09}{0.20} & 0.” | 92.50 | 92.50 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.90` |
| `R1.supp-tab-appexpladder.91` | 96.61 — “E2b (raw) & 99.00 \ci{98.21}{99.60} & 94.70 \ci{92.50}{96.61} & 0.03 \ci{-0.09}{0.20} & 0.” | 96.61 | 96.61 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.91` |
| `R1.supp-tab-appexpladder.92` | 0.03 — “E2b (raw) & 99.00 \ci{98.21}{99.60} & 94.70 \ci{92.50}{96.61} & 0.03 \ci{-0.09}{0.20} & 0.” | 0.03 | 0.0285 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.92` |
| `R1.supp-tab-appexpladder.93` | -0.09 — “E2b (raw) & 99.00 \ci{98.21}{99.60} & 94.70 \ci{92.50}{96.61} & 0.03 \ci{-0.09}{0.20} & 0.” | -0.09 | -0.0927 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.93` |
| `R1.supp-tab-appexpladder.94` | 0.20 — “E2b (raw) & 99.00 \ci{98.21}{99.60} & 94.70 \ci{92.50}{96.61} & 0.03 \ci{-0.09}{0.20} & 0.” | 0.20 | 0.1960 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.94` |
| `R1.supp-tab-appexpladder.95` | 0.97 — “E2b (raw) & 99.00 \ci{98.21}{99.60} & 94.70 \ci{92.50}{96.61} & 0.03 \ci{-0.09}{0.20} & 0.” | 0.97 | 0.9685 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.95` |
| `R1.supp-tab-appexpladder.96` | -0.19 — “E2b (raw) & 99.00 \ci{98.21}{99.60} & 94.70 \ci{92.50}{96.61} & 0.03 \ci{-0.09}{0.20} & 0.” | -0.19 | -0.1888 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.96` |
| `R1.supp-tab-appexpladder.97` | 2.19 — “E2b (raw) & 99.00 \ci{98.21}{99.60} & 94.70 \ci{92.50}{96.61} & 0.03 \ci{-0.09}{0.20} & 0.” | 2.19 | 2.1896 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.97` |
| `R1.supp-tab-appexpladder.98` | 99.32 — “anchor (raw) & 99.32 \ci{98.60}{99.81} & 85.54 \ci{82.52}{88.41} & $-0.05$ \ci{-0.19}{0.08” | 99.32 | 99.32 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.98` |
| `R1.supp-tab-appexpladder.99` | 98.60 — “anchor (raw) & 99.32 \ci{98.60}{99.81} & 85.54 \ci{82.52}{88.41} & $-0.05$ \ci{-0.19}{0.08” | 98.60 | 98.60 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.99` |
| `R1.supp-tab-appexpladder.100` | 99.81 — “anchor (raw) & 99.32 \ci{98.60}{99.81} & 85.54 \ci{82.52}{88.41} & $-0.05$ \ci{-0.19}{0.08” | 99.81 | 99.81 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.100` |
| `R1.supp-tab-appexpladder.101` | 85.54 — “anchor (raw) & 99.32 \ci{98.60}{99.81} & 85.54 \ci{82.52}{88.41} & $-0.05$ \ci{-0.19}{0.08” | 85.54 | 85.54 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.101` |
| `R1.supp-tab-appexpladder.102` | 82.52 — “anchor (raw) & 99.32 \ci{98.60}{99.81} & 85.54 \ci{82.52}{88.41} & $-0.05$ \ci{-0.19}{0.08” | 82.52 | 82.52 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.102` |
| `R1.supp-tab-appexpladder.103` | 88.41 — “anchor (raw) & 99.32 \ci{98.60}{99.81} & 85.54 \ci{82.52}{88.41} & $-0.05$ \ci{-0.19}{0.08” | 88.41 | 88.41 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.103` |
| `R1.supp-tab-appexpladder.104` | -0.05 — “anchor (raw) & 99.32 \ci{98.60}{99.81} & 85.54 \ci{82.52}{88.41} & $-0.05$ \ci{-0.19}{0.08” | -0.05 | -0.0514 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.104` |
| `R1.supp-tab-appexpladder.105` | -0.19 — “anchor (raw) & 99.32 \ci{98.60}{99.81} & 85.54 \ci{82.52}{88.41} & $-0.05$ \ci{-0.19}{0.08” | -0.19 | -0.1866 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.105` |
| `R1.supp-tab-appexpladder.106` | 0.08 — “anchor (raw) & 99.32 \ci{98.60}{99.81} & 85.54 \ci{82.52}{88.41} & $-0.05$ \ci{-0.19}{0.08” | 0.08 | 0.0765 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.106` |
| `R1.supp-tab-appexpladder.107` | -0.36 — “anchor (raw) & 99.32 \ci{98.60}{99.81} & 85.54 \ci{82.52}{88.41} & $-0.05$ \ci{-0.19}{0.08” | -0.36 | -0.3635 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.107` |
| `R1.supp-tab-appexpladder.108` | -2.65 — “anchor (raw) & 99.32 \ci{98.60}{99.81} & 85.54 \ci{82.52}{88.41} & $-0.05$ \ci{-0.19}{0.08” | -2.65 | -2.6506 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.108` |
| `R1.supp-tab-appexpladder.109` | 1.70 — “anchor (raw) & 99.32 \ci{98.60}{99.81} & 85.54 \ci{82.52}{88.41} & $-0.05$ \ci{-0.19}{0.08” | 1.70 | 1.7028 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.109` |
| `R1.supp-tab-appexpladder.110` | 97.85 — “E3a (raw) & 97.85 \ci{96.67}{98.81} & 88.38 \ci{85.56}{91.04} & $-0.25$ \ci{-0.45}{-0.07} ” | 97.85 | 97.85 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.110` |
| `R1.supp-tab-appexpladder.111` | 96.67 — “E3a (raw) & 97.85 \ci{96.67}{98.81} & 88.38 \ci{85.56}{91.04} & $-0.25$ \ci{-0.45}{-0.07} ” | 96.67 | 96.67 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.111` |
| `R1.supp-tab-appexpladder.112` | 98.81 — “E3a (raw) & 97.85 \ci{96.67}{98.81} & 88.38 \ci{85.56}{91.04} & $-0.25$ \ci{-0.45}{-0.07} ” | 98.81 | 98.81 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.112` |
| `R1.supp-tab-appexpladder.113` | 88.38 — “E3a (raw) & 97.85 \ci{96.67}{98.81} & 88.38 \ci{85.56}{91.04} & $-0.25$ \ci{-0.45}{-0.07} ” | 88.38 | 88.38 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.113` |
| `R1.supp-tab-appexpladder.114` | 85.56 — “E3a (raw) & 97.85 \ci{96.67}{98.81} & 88.38 \ci{85.56}{91.04} & $-0.25$ \ci{-0.45}{-0.07} ” | 85.56 | 85.56 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.114` |
| `R1.supp-tab-appexpladder.115` | 91.04 — “E3a (raw) & 97.85 \ci{96.67}{98.81} & 88.38 \ci{85.56}{91.04} & $-0.25$ \ci{-0.45}{-0.07} ” | 91.04 | 91.04 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.115` |
| `R1.supp-tab-appexpladder.116` | -0.25 — “E3a (raw) & 97.85 \ci{96.67}{98.81} & 88.38 \ci{85.56}{91.04} & $-0.25$ \ci{-0.45}{-0.07} ” | -0.25 | -0.2496 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.116` |
| `R1.supp-tab-appexpladder.117` | -0.45 — “E3a (raw) & 97.85 \ci{96.67}{98.81} & 88.38 \ci{85.56}{91.04} & $-0.25$ \ci{-0.45}{-0.07} ” | -0.45 | -0.4528 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.117` |
| `R1.supp-tab-appexpladder.118` | -0.07 — “E3a (raw) & 97.85 \ci{96.67}{98.81} & 88.38 \ci{85.56}{91.04} & $-0.25$ \ci{-0.45}{-0.07} ” | -0.07 | -0.0701 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.118` |
| `R1.supp-tab-appexpladder.119` | -0.56 — “E3a (raw) & 97.85 \ci{96.67}{98.81} & 88.38 \ci{85.56}{91.04} & $-0.25$ \ci{-0.45}{-0.07} ” | -0.56 | -0.5561 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.119` |
| `R1.supp-tab-appexpladder.120` | -1.79 — “E3a (raw) & 97.85 \ci{96.67}{98.81} & 88.38 \ci{85.56}{91.04} & $-0.25$ \ci{-0.45}{-0.07} ” | -1.79 | -1.7947 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.120` |
| `R1.supp-tab-appexpladder.121` | 0.69 — “E3a (raw) & 97.85 \ci{96.67}{98.81} & 88.38 \ci{85.56}{91.04} & $-0.25$ \ci{-0.45}{-0.07} ” | 0.69 | 0.6939 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.121` |
| `R1.supp-tab-appexpladder.122` | 98.13 — “E3b (raw) & 98.13 \ci{97.00}{99.05} & 86.39 \ci{83.18}{89.33} & $-0.12$ \ci{-0.31}{0.02} &” | 98.13 | 98.13 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.122` |
| `R1.supp-tab-appexpladder.123` | 97.00 — “E3b (raw) & 98.13 \ci{97.00}{99.05} & 86.39 \ci{83.18}{89.33} & $-0.12$ \ci{-0.31}{0.02} &” | 97.00 | 97.00 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.123` |
| `R1.supp-tab-appexpladder.124` | 99.05 — “E3b (raw) & 98.13 \ci{97.00}{99.05} & 86.39 \ci{83.18}{89.33} & $-0.12$ \ci{-0.31}{0.02} &” | 99.05 | 99.05 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.124` |
| `R1.supp-tab-appexpladder.125` | 86.39 — “E3b (raw) & 98.13 \ci{97.00}{99.05} & 86.39 \ci{83.18}{89.33} & $-0.12$ \ci{-0.31}{0.02} &” | 86.39 | 86.39 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.125` |
| `R1.supp-tab-appexpladder.126` | 83.18 — “E3b (raw) & 98.13 \ci{97.00}{99.05} & 86.39 \ci{83.18}{89.33} & $-0.12$ \ci{-0.31}{0.02} &” | 83.18 | 83.18 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.126` |
| `R1.supp-tab-appexpladder.127` | 89.33 — “E3b (raw) & 98.13 \ci{97.00}{99.05} & 86.39 \ci{83.18}{89.33} & $-0.12$ \ci{-0.31}{0.02} &” | 89.33 | 89.33 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.127` |
| `R1.supp-tab-appexpladder.128` | -0.12 — “E3b (raw) & 98.13 \ci{97.00}{99.05} & 86.39 \ci{83.18}{89.33} & $-0.12$ \ci{-0.31}{0.02} &” | -0.12 | -0.1241 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.128` |
| `R1.supp-tab-appexpladder.129` | -0.31 — “E3b (raw) & 98.13 \ci{97.00}{99.05} & 86.39 \ci{83.18}{89.33} & $-0.12$ \ci{-0.31}{0.02} &” | -0.31 | -0.3053 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.129` |
| `R1.supp-tab-appexpladder.130` | 0.02 — “E3b (raw) & 98.13 \ci{97.00}{99.05} & 86.39 \ci{83.18}{89.33} & $-0.12$ \ci{-0.31}{0.02} &” | 0.02 | 0.0225 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.130` |
| `R1.supp-tab-appexpladder.131` | 0.10 — “E3b (raw) & 98.13 \ci{97.00}{99.05} & 86.39 \ci{83.18}{89.33} & $-0.12$ \ci{-0.31}{0.02} &” | 0.10 | 0.1016 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.131` |
| `R1.supp-tab-appexpladder.132` | -1.32 — “E3b (raw) & 98.13 \ci{97.00}{99.05} & 86.39 \ci{83.18}{89.33} & $-0.12$ \ci{-0.31}{0.02} &” | -1.32 | -1.3202 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.132` |
| `R1.supp-tab-appexpladder.133` | 1.49 — “E3b (raw) & 98.13 \ci{97.00}{99.05} & 86.39 \ci{83.18}{89.33} & $-0.12$ \ci{-0.31}{0.02} &” | 1.49 | 1.4902 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.133` |
| `R1.supp-tab-appexpladder.134` | 0.47 — “X1 & 0.47 \ci{-0.08}{1.29} & 1.51 \ci{0.25}{2.92} & --- & --- \\” | 0.47 | 0.4690 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.134` |
| `R1.supp-tab-appexpladder.135` | -0.08 — “X1 & 0.47 \ci{-0.08}{1.29} & 1.51 \ci{0.25}{2.92} & --- & --- \\” | -0.08 | -0.0757 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.135` |
| `R1.supp-tab-appexpladder.136` | 1.29 — “X1 & 0.47 \ci{-0.08}{1.29} & 1.51 \ci{0.25}{2.92} & --- & --- \\” | 1.29 | 1.2895 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.136` |
| `R1.supp-tab-appexpladder.137` | 1.51 — “X1 & 0.47 \ci{-0.08}{1.29} & 1.51 \ci{0.25}{2.92} & --- & --- \\” | 1.51 | 1.5055 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.137` |
| `R1.supp-tab-appexpladder.138` | 0.25 — “X1 & 0.47 \ci{-0.08}{1.29} & 1.51 \ci{0.25}{2.92} & --- & --- \\” | 0.25 | 0.2508 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.138` |
| `R1.supp-tab-appexpladder.139` | 2.92 — “X1 & 0.47 \ci{-0.08}{1.29} & 1.51 \ci{0.25}{2.92} & --- & --- \\” | 2.92 | 2.9245 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.139` |
| `R1.supp-tab-appexpladder.140` | -0.30 — “X2 & $-0.30$ \ci{-1.13}{0.28} & $-0.56$ \ci{-2.12}{1.05} & --- & --- \\” | -0.30 | -0.2972 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.140` |
| `R1.supp-tab-appexpladder.141` | -1.13 — “X2 & $-0.30$ \ci{-1.13}{0.28} & $-0.56$ \ci{-2.12}{1.05} & --- & --- \\” | -1.13 | -1.1263 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.141` |
| `R1.supp-tab-appexpladder.142` | 0.28 — “X2 & $-0.30$ \ci{-1.13}{0.28} & $-0.56$ \ci{-2.12}{1.05} & --- & --- \\” | 0.28 | 0.2768 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.142` |
| `R1.supp-tab-appexpladder.143` | -0.56 — “X2 & $-0.30$ \ci{-1.13}{0.28} & $-0.56$ \ci{-2.12}{1.05} & --- & --- \\” | -0.56 | -0.5621 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.143` |
| `R1.supp-tab-appexpladder.144` | -2.12 — “X2 & $-0.30$ \ci{-1.13}{0.28} & $-0.56$ \ci{-2.12}{1.05} & --- & --- \\” | -2.12 | -2.1238 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.144` |
| `R1.supp-tab-appexpladder.145` | 1.05 — “X2 & $-0.30$ \ci{-1.13}{0.28} & $-0.56$ \ci{-2.12}{1.05} & --- & --- \\” | 1.05 | 1.0472 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.145` |
| `R1.supp-tab-appexpladder.146` | 0.05 — “X3 & 0.05 \ci{-0.47}{0.53} & 0.37 \ci{-0.99}{1.93} & --- & --- \\” | 0.05 | 0.0472 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.146` |
| `R1.supp-tab-appexpladder.147` | -0.47 — “X3 & 0.05 \ci{-0.47}{0.53} & 0.37 \ci{-0.99}{1.93} & --- & --- \\” | -0.47 | -0.4699 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.147` |
| `R1.supp-tab-appexpladder.148` | 0.53 — “X3 & 0.05 \ci{-0.47}{0.53} & 0.37 \ci{-0.99}{1.93} & --- & --- \\” | 0.53 | 0.5277 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.148` |
| `R1.supp-tab-appexpladder.149` | 0.37 — “X3 & 0.05 \ci{-0.47}{0.53} & 0.37 \ci{-0.99}{1.93} & --- & --- \\” | 0.37 | 0.3682 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.149` |
| `R1.supp-tab-appexpladder.150` | -0.99 — “X3 & 0.05 \ci{-0.47}{0.53} & 0.37 \ci{-0.99}{1.93} & --- & --- \\” | -0.99 | -0.9903 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.150` |
| `R1.supp-tab-appexpladder.151` | 1.93 — “X3 & 0.05 \ci{-0.47}{0.53} & 0.37 \ci{-0.99}{1.93} & --- & --- \\” | 1.93 | 1.9273 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.151` |
| `R1.supp-tab-appexpladder.152` | -0.72 — “X4 & $-0.72$ \ci{-1.23}{-0.32} & 9.37 \ci{6.53}{12.32} & --- & --- \\” | -0.72 | -0.7215 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.152` |
| `R1.supp-tab-appexpladder.153` | -1.23 — “X4 & $-0.72$ \ci{-1.23}{-0.32} & 9.37 \ci{6.53}{12.32} & --- & --- \\” | -1.23 | -1.2313 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.153` |
| `R1.supp-tab-appexpladder.154` | -0.32 — “X4 & $-0.72$ \ci{-1.23}{-0.32} & 9.37 \ci{6.53}{12.32} & --- & --- \\” | -0.32 | -0.3214 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.154` |
| `R1.supp-tab-appexpladder.155` | 9.37 — “X4 & $-0.72$ \ci{-1.23}{-0.32} & 9.37 \ci{6.53}{12.32} & --- & --- \\” | 9.37 | 9.3716 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.155` |
| `R1.supp-tab-appexpladder.156` | 6.53 — “X4 & $-0.72$ \ci{-1.23}{-0.32} & 9.37 \ci{6.53}{12.32} & --- & --- \\” | 6.53 | 6.5332 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.156` |
| `R1.supp-tab-appexpladder.157` | 12.32 — “X4 & $-0.72$ \ci{-1.23}{-0.32} & 9.37 \ci{6.53}{12.32} & --- & --- \\” | 12.32 | 12.32 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.157` |
| `R1.supp-tab-appexpladder.158` | 0.72 — “X5 & 0.72 \ci{0.24}{1.28} & 8.03 \ci{5.70}{10.52} & --- & --- \\” | 0.72 | 0.7166 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.158` |
| `R1.supp-tab-appexpladder.159` | 0.24 — “X5 & 0.72 \ci{0.24}{1.28} & 8.03 \ci{5.70}{10.52} & --- & --- \\” | 0.24 | 0.2368 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.159` |
| `R1.supp-tab-appexpladder.160` | 1.28 — “X5 & 0.72 \ci{0.24}{1.28} & 8.03 \ci{5.70}{10.52} & --- & --- \\” | 1.28 | 1.2825 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.160` |
| `R1.supp-tab-appexpladder.161` | 8.03 — “X5 & 0.72 \ci{0.24}{1.28} & 8.03 \ci{5.70}{10.52} & --- & --- \\” | 8.03 | 8.0261 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.161` |
| `R1.supp-tab-appexpladder.162` | 5.70 — “X5 & 0.72 \ci{0.24}{1.28} & 8.03 \ci{5.70}{10.52} & --- & --- \\” | 5.70 | 5.7036 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.162` |
| `R1.supp-tab-appexpladder.163` | 10.52 — “X5 & 0.72 \ci{0.24}{1.28} & 8.03 \ci{5.70}{10.52} & --- & --- \\” | 10.52 | 10.52 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.163` |
| `R1.supp-tab-appexpladder.164` | -0.25 — “X6 & $-0.25$ \ci{-0.58}{0.07} & 0.49 \ci{-0.78}{1.67} & --- & --- \\” | -0.25 | -0.2498 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.164` |
| `R1.supp-tab-appexpladder.165` | -0.58 — “X6 & $-0.25$ \ci{-0.58}{0.07} & 0.49 \ci{-0.78}{1.67} & --- & --- \\” | -0.58 | -0.5761 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.165` |
| `R1.supp-tab-appexpladder.166` | 0.07 — “X6 & $-0.25$ \ci{-0.58}{0.07} & 0.49 \ci{-0.78}{1.67} & --- & --- \\” | 0.07 | 0.0695 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.166` |
| `R1.supp-tab-appexpladder.167` | 0.49 — “X6 & $-0.25$ \ci{-0.58}{0.07} & 0.49 \ci{-0.78}{1.67} & --- & --- \\” | 0.49 | 0.4934 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.167` |
| `R1.supp-tab-appexpladder.168` | -0.78 — “X6 & $-0.25$ \ci{-0.58}{0.07} & 0.49 \ci{-0.78}{1.67} & --- & --- \\” | -0.78 | -0.7779 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.168` |
| `R1.supp-tab-appexpladder.169` | 1.67 — “X6 & $-0.25$ \ci{-0.58}{0.07} & 0.49 \ci{-0.78}{1.67} & --- & --- \\” | 1.67 | 1.6737 | `revision-1/exploratory/rev1/e9.json` | `python verify/claim.py R1.supp-tab-appexpladder.169` |

- `R1.supp-tab-appexpladder.2` — weights: EMA
- `R1.supp-tab-appexpladder.3` — weights: EMA
- `R1.supp-tab-appexpladder.4` — weights: EMA
- `R1.supp-tab-appexpladder.5` — weights: EMA
- `R1.supp-tab-appexpladder.6` — weights: EMA
- `R1.supp-tab-appexpladder.7` — weights: EMA
- `R1.supp-tab-appexpladder.8` — weights: EMA
- `R1.supp-tab-appexpladder.9` — weights: EMA
- `R1.supp-tab-appexpladder.10` — weights: EMA
- `R1.supp-tab-appexpladder.11` — weights: EMA
- `R1.supp-tab-appexpladder.12` — weights: EMA
- `R1.supp-tab-appexpladder.13` — weights: EMA
- `R1.supp-tab-appexpladder.14` — weights: EMA
- `R1.supp-tab-appexpladder.15` — weights: EMA
- `R1.supp-tab-appexpladder.16` — weights: EMA
- `R1.supp-tab-appexpladder.17` — weights: EMA
- `R1.supp-tab-appexpladder.18` — weights: EMA
- `R1.supp-tab-appexpladder.19` — weights: EMA
- `R1.supp-tab-appexpladder.20` — weights: EMA
- `R1.supp-tab-appexpladder.21` — weights: EMA
- `R1.supp-tab-appexpladder.22` — weights: EMA
- `R1.supp-tab-appexpladder.23` — weights: EMA
- `R1.supp-tab-appexpladder.24` — weights: EMA
- `R1.supp-tab-appexpladder.25` — weights: EMA
- `R1.supp-tab-appexpladder.26` — weights: EMA
- `R1.supp-tab-appexpladder.27` — weights: EMA
- `R1.supp-tab-appexpladder.28` — weights: EMA
- `R1.supp-tab-appexpladder.29` — weights: EMA
- `R1.supp-tab-appexpladder.30` — weights: EMA
- `R1.supp-tab-appexpladder.31` — weights: EMA
- `R1.supp-tab-appexpladder.32` — weights: EMA
- `R1.supp-tab-appexpladder.33` — weights: EMA
- `R1.supp-tab-appexpladder.34` — weights: EMA
- `R1.supp-tab-appexpladder.35` — weights: EMA
- `R1.supp-tab-appexpladder.36` — weights: EMA
- `R1.supp-tab-appexpladder.37` — weights: EMA
- `R1.supp-tab-appexpladder.38` — weights: EMA
- `R1.supp-tab-appexpladder.39` — weights: EMA
- `R1.supp-tab-appexpladder.40` — weights: EMA
- `R1.supp-tab-appexpladder.41` — weights: EMA
- `R1.supp-tab-appexpladder.42` — weights: EMA
- `R1.supp-tab-appexpladder.43` — weights: EMA
- `R1.supp-tab-appexpladder.44` — weights: EMA
- `R1.supp-tab-appexpladder.45` — weights: EMA
- `R1.supp-tab-appexpladder.46` — weights: EMA
- `R1.supp-tab-appexpladder.47` — weights: EMA
- `R1.supp-tab-appexpladder.48` — weights: EMA
- `R1.supp-tab-appexpladder.49` — weights: EMA
- `R1.supp-tab-appexpladder.50` — weights: raw
- `R1.supp-tab-appexpladder.51` — weights: raw
- `R1.supp-tab-appexpladder.52` — weights: raw
- `R1.supp-tab-appexpladder.53` — weights: raw
- `R1.supp-tab-appexpladder.54` — weights: raw
- `R1.supp-tab-appexpladder.55` — weights: raw
- `R1.supp-tab-appexpladder.56` — weights: raw
- `R1.supp-tab-appexpladder.57` — weights: raw
- `R1.supp-tab-appexpladder.58` — weights: raw
- `R1.supp-tab-appexpladder.59` — weights: raw
- `R1.supp-tab-appexpladder.60` — weights: raw
- `R1.supp-tab-appexpladder.61` — weights: raw
- `R1.supp-tab-appexpladder.62` — weights: raw
- `R1.supp-tab-appexpladder.63` — weights: raw
- `R1.supp-tab-appexpladder.64` — weights: raw
- `R1.supp-tab-appexpladder.65` — weights: raw
- `R1.supp-tab-appexpladder.66` — weights: raw
- `R1.supp-tab-appexpladder.67` — weights: raw
- `R1.supp-tab-appexpladder.68` — weights: raw
- `R1.supp-tab-appexpladder.69` — weights: raw
- `R1.supp-tab-appexpladder.70` — weights: raw
- `R1.supp-tab-appexpladder.71` — weights: raw
- `R1.supp-tab-appexpladder.72` — weights: raw
- `R1.supp-tab-appexpladder.73` — weights: raw
- `R1.supp-tab-appexpladder.74` — weights: raw
- `R1.supp-tab-appexpladder.75` — weights: raw
- `R1.supp-tab-appexpladder.76` — weights: raw
- `R1.supp-tab-appexpladder.77` — weights: raw
- `R1.supp-tab-appexpladder.78` — weights: raw
- `R1.supp-tab-appexpladder.79` — weights: raw
- `R1.supp-tab-appexpladder.80` — weights: raw
- `R1.supp-tab-appexpladder.81` — weights: raw
- `R1.supp-tab-appexpladder.82` — weights: raw
- `R1.supp-tab-appexpladder.83` — weights: raw
- `R1.supp-tab-appexpladder.84` — weights: raw
- `R1.supp-tab-appexpladder.85` — weights: raw
- `R1.supp-tab-appexpladder.86` — weights: raw
- `R1.supp-tab-appexpladder.87` — weights: raw
- `R1.supp-tab-appexpladder.88` — weights: raw
- `R1.supp-tab-appexpladder.89` — weights: raw
- `R1.supp-tab-appexpladder.90` — weights: raw
- `R1.supp-tab-appexpladder.91` — weights: raw
- `R1.supp-tab-appexpladder.92` — weights: raw
- `R1.supp-tab-appexpladder.93` — weights: raw
- `R1.supp-tab-appexpladder.94` — weights: raw
- `R1.supp-tab-appexpladder.95` — weights: raw
- `R1.supp-tab-appexpladder.96` — weights: raw
- `R1.supp-tab-appexpladder.97` — weights: raw
- `R1.supp-tab-appexpladder.98` — weights: raw
- `R1.supp-tab-appexpladder.99` — weights: raw
- `R1.supp-tab-appexpladder.100` — weights: raw
- `R1.supp-tab-appexpladder.101` — weights: raw
- `R1.supp-tab-appexpladder.102` — weights: raw
- `R1.supp-tab-appexpladder.103` — weights: raw
- `R1.supp-tab-appexpladder.104` — weights: raw
- `R1.supp-tab-appexpladder.105` — weights: raw
- `R1.supp-tab-appexpladder.106` — weights: raw
- `R1.supp-tab-appexpladder.107` — weights: raw
- `R1.supp-tab-appexpladder.108` — weights: raw
- `R1.supp-tab-appexpladder.109` — weights: raw
- `R1.supp-tab-appexpladder.110` — weights: raw
- `R1.supp-tab-appexpladder.111` — weights: raw
- `R1.supp-tab-appexpladder.112` — weights: raw
- `R1.supp-tab-appexpladder.113` — weights: raw
- `R1.supp-tab-appexpladder.114` — weights: raw
- `R1.supp-tab-appexpladder.115` — weights: raw
- `R1.supp-tab-appexpladder.116` — weights: raw
- `R1.supp-tab-appexpladder.117` — weights: raw
- `R1.supp-tab-appexpladder.118` — weights: raw
- `R1.supp-tab-appexpladder.119` — weights: raw
- `R1.supp-tab-appexpladder.120` — weights: raw
- `R1.supp-tab-appexpladder.121` — weights: raw
- `R1.supp-tab-appexpladder.122` — weights: raw
- `R1.supp-tab-appexpladder.123` — weights: raw
- `R1.supp-tab-appexpladder.124` — weights: raw
- `R1.supp-tab-appexpladder.125` — weights: raw
- `R1.supp-tab-appexpladder.126` — weights: raw
- `R1.supp-tab-appexpladder.127` — weights: raw
- `R1.supp-tab-appexpladder.128` — weights: raw
- `R1.supp-tab-appexpladder.129` — weights: raw
- `R1.supp-tab-appexpladder.130` — weights: raw
- `R1.supp-tab-appexpladder.131` — weights: raw
- `R1.supp-tab-appexpladder.132` — weights: raw
- `R1.supp-tab-appexpladder.133` — weights: raw
- `R1.supp-tab-appexpladder.134` — weights: EMA
- `R1.supp-tab-appexpladder.135` — weights: EMA
- `R1.supp-tab-appexpladder.136` — weights: EMA
- `R1.supp-tab-appexpladder.137` — weights: EMA
- `R1.supp-tab-appexpladder.138` — weights: EMA
- `R1.supp-tab-appexpladder.139` — weights: EMA
- `R1.supp-tab-appexpladder.140` — weights: EMA and raw
- `R1.supp-tab-appexpladder.141` — weights: EMA and raw
- `R1.supp-tab-appexpladder.142` — weights: EMA and raw
- `R1.supp-tab-appexpladder.143` — weights: EMA and raw
- `R1.supp-tab-appexpladder.144` — weights: EMA and raw
- `R1.supp-tab-appexpladder.145` — weights: EMA and raw
- `R1.supp-tab-appexpladder.146` — weights: EMA and raw
- `R1.supp-tab-appexpladder.147` — weights: EMA and raw
- `R1.supp-tab-appexpladder.148` — weights: EMA and raw
- `R1.supp-tab-appexpladder.149` — weights: EMA and raw
- `R1.supp-tab-appexpladder.150` — weights: EMA and raw
- `R1.supp-tab-appexpladder.151` — weights: EMA and raw
- `R1.supp-tab-appexpladder.152` — weights: raw
- `R1.supp-tab-appexpladder.153` — weights: raw
- `R1.supp-tab-appexpladder.154` — weights: raw
- `R1.supp-tab-appexpladder.155` — weights: raw
- `R1.supp-tab-appexpladder.156` — weights: raw
- `R1.supp-tab-appexpladder.157` — weights: raw
- `R1.supp-tab-appexpladder.158` — weights: raw
- `R1.supp-tab-appexpladder.159` — weights: raw
- `R1.supp-tab-appexpladder.160` — weights: raw
- `R1.supp-tab-appexpladder.161` — weights: raw
- `R1.supp-tab-appexpladder.162` — weights: raw
- `R1.supp-tab-appexpladder.163` — weights: raw
- `R1.supp-tab-appexpladder.164` — weights: raw
- `R1.supp-tab-appexpladder.165` — weights: raw
- `R1.supp-tab-appexpladder.166` — weights: raw
- `R1.supp-tab-appexpladder.167` — weights: raw
- `R1.supp-tab-appexpladder.168` — weights: raw
- `R1.supp-tab-appexpladder.169` — weights: raw

## R1.supp-tab-appladder — Revision 1 — Supplementary Material, tab:appladder

*Supplementary Material, tab:appladder; `\label{tab:appladder}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-tab-appladder.1` | 18 — “c18 & ours & 18 & 1602 [964] & 41.17 $\pm$ 0.99 & 0.9885 $\pm$ 0.0030 \\” | 18 | 18.00 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.1` |
| `R1.supp-tab-appladder.2` | 1602 — “c18 & ours & 18 & 1602 [964] & 41.17 $\pm$ 0.99 & 0.9885 $\pm$ 0.0030 \\” | 1602 | 1602.24 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.2` |
| `R1.supp-tab-appladder.3` | 964 — “c18 & ours & 18 & 1602 [964] & 41.17 $\pm$ 0.99 & 0.9885 $\pm$ 0.0030 \\” | 964 | 963.76 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.3` |
| `R1.supp-tab-appladder.4` | 41.17 — “c18 & ours & 18 & 1602 [964] & 41.17 $\pm$ 0.99 & 0.9885 $\pm$ 0.0030 \\” | 41.17 | 41.17 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.4` |
| `R1.supp-tab-appladder.5` | 0.99 — “c18 & ours & 18 & 1602 [964] & 41.17 $\pm$ 0.99 & 0.9885 $\pm$ 0.0030 \\” | 0.99 | 0.9897 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.5` |
| `R1.supp-tab-appladder.6` | 0.9885 — “c18 & ours & 18 & 1602 [964] & 41.17 $\pm$ 0.99 & 0.9885 $\pm$ 0.0030 \\” | 0.9885 | 0.9885 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.6` |
| `R1.supp-tab-appladder.7` | 0.0030 — “c18 & ours & 18 & 1602 [964] & 41.17 $\pm$ 0.99 & 0.9885 $\pm$ 0.0030 \\” | 0.0030 | 0.0030 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.7` |
| `R1.supp-tab-appladder.8` | 885 — “c23 & distributed & --- & 885 [554] & 39.88 $\pm$ 1.71 & 0.9826 $\pm$ 0.0056 \\” | 885 | 885.37 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.8` |
| `R1.supp-tab-appladder.9` | 554 — “c23 & distributed & --- & 885 [554] & 39.88 $\pm$ 1.71 & 0.9826 $\pm$ 0.0056 \\” | 554 | 553.76 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.9` |
| `R1.supp-tab-appladder.10` | 39.88 — “c23 & distributed & --- & 885 [554] & 39.88 $\pm$ 1.71 & 0.9826 $\pm$ 0.0056 \\” | 39.88 | 39.88 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.10` |
| `R1.supp-tab-appladder.11` | 1.71 — “c23 & distributed & --- & 885 [554] & 39.88 $\pm$ 1.71 & 0.9826 $\pm$ 0.0056 \\” | 1.71 | 1.7125 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.11` |
| `R1.supp-tab-appladder.12` | 0.9826 — “c23 & distributed & --- & 885 [554] & 39.88 $\pm$ 1.71 & 0.9826 $\pm$ 0.0056 \\” | 0.9826 | 0.9826 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.12` |
| `R1.supp-tab-appladder.13` | 0.0056 — “c23 & distributed & --- & 885 [554] & 39.88 $\pm$ 1.71 & 0.9826 $\pm$ 0.0056 \\” | 0.0056 | 0.0056 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.13` |
| `R1.supp-tab-appladder.14` | 23 — “x23 & ours & 23 & 882 [540] & 39.35 $\pm$ 1.33 & 0.9822 $\pm$ 0.0053 \\” | 23 | 23.00 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.14` |
| `R1.supp-tab-appladder.15` | 882 — “x23 & ours & 23 & 882 [540] & 39.35 $\pm$ 1.33 & 0.9822 $\pm$ 0.0053 \\” | 882 | 881.79 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.15` |
| `R1.supp-tab-appladder.16` | 540 — “x23 & ours & 23 & 882 [540] & 39.35 $\pm$ 1.33 & 0.9822 $\pm$ 0.0053 \\” | 540 | 539.52 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.16` |
| `R1.supp-tab-appladder.17` | 39.35 — “x23 & ours & 23 & 882 [540] & 39.35 $\pm$ 1.33 & 0.9822 $\pm$ 0.0053 \\” | 39.35 | 39.35 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.17` |
| `R1.supp-tab-appladder.18` | 1.33 — “x23 & ours & 23 & 882 [540] & 39.35 $\pm$ 1.33 & 0.9822 $\pm$ 0.0053 \\” | 1.33 | 1.3276 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.18` |
| `R1.supp-tab-appladder.19` | 0.9822 — “x23 & ours & 23 & 882 [540] & 39.35 $\pm$ 1.33 & 0.9822 $\pm$ 0.0053 \\” | 0.9822 | 0.9822 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.19` |
| `R1.supp-tab-appladder.20` | 0.0053 — “x23 & ours & 23 & 882 [540] & 39.35 $\pm$ 1.33 & 0.9822 $\pm$ 0.0053 \\” | 0.0053 | 0.0053 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.20` |
| `R1.supp-tab-appladder.21` | 28 — “c28 & ours & 28 & 457 [290] & 37.10 $\pm$ 1.62 & 0.9711 $\pm$ 0.0092 \\” | 28 | 28.00 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.21` |
| `R1.supp-tab-appladder.22` | 457 — “c28 & ours & 28 & 457 [290] & 37.10 $\pm$ 1.62 & 0.9711 $\pm$ 0.0092 \\” | 457 | 457.18 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.22` |
| `R1.supp-tab-appladder.23` | 290 — “c28 & ours & 28 & 457 [290] & 37.10 $\pm$ 1.62 & 0.9711 $\pm$ 0.0092 \\” | 290 | 289.80 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.23` |
| `R1.supp-tab-appladder.24` | 37.10 — “c28 & ours & 28 & 457 [290] & 37.10 $\pm$ 1.62 & 0.9711 $\pm$ 0.0092 \\” | 37.10 | 37.10 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.24` |
| `R1.supp-tab-appladder.25` | 1.62 — “c28 & ours & 28 & 457 [290] & 37.10 $\pm$ 1.62 & 0.9711 $\pm$ 0.0092 \\” | 1.62 | 1.6160 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.25` |
| `R1.supp-tab-appladder.26` | 0.9711 — “c28 & ours & 28 & 457 [290] & 37.10 $\pm$ 1.62 & 0.9711 $\pm$ 0.0092 \\” | 0.9711 | 0.9711 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.26` |
| `R1.supp-tab-appladder.27` | 0.0092 — “c28 & ours & 28 & 457 [290] & 37.10 $\pm$ 1.62 & 0.9711 $\pm$ 0.0092 \\” | 0.0092 | 0.0092 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.27` |
| `R1.supp-tab-appladder.28` | 32 — “c32 & ours & 32 & 270 [179] & 35.16 $\pm$ 1.78 & 0.9571 $\pm$ 0.0141 \\” | 32 | 32.00 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.28` |
| `R1.supp-tab-appladder.29` | 270 — “c32 & ours & 32 & 270 [179] & 35.16 $\pm$ 1.78 & 0.9571 $\pm$ 0.0141 \\” | 270 | 269.70 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.29` |
| `R1.supp-tab-appladder.30` | 179 — “c32 & ours & 32 & 270 [179] & 35.16 $\pm$ 1.78 & 0.9571 $\pm$ 0.0141 \\” | 179 | 179.27 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.30` |
| `R1.supp-tab-appladder.31` | 35.16 — “c32 & ours & 32 & 270 [179] & 35.16 $\pm$ 1.78 & 0.9571 $\pm$ 0.0141 \\” | 35.16 | 35.16 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.31` |
| `R1.supp-tab-appladder.32` | 1.78 — “c32 & ours & 32 & 270 [179] & 35.16 $\pm$ 1.78 & 0.9571 $\pm$ 0.0141 \\” | 1.78 | 1.7818 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.32` |
| `R1.supp-tab-appladder.33` | 0.9571 — “c32 & ours & 32 & 270 [179] & 35.16 $\pm$ 1.78 & 0.9571 $\pm$ 0.0141 \\” | 0.9571 | 0.9571 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.33` |
| `R1.supp-tab-appladder.34` | 0.0141 — “c32 & ours & 32 & 270 [179] & 35.16 $\pm$ 1.78 & 0.9571 $\pm$ 0.0141 \\” | 0.0141 | 0.0141 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.34` |
| `R1.supp-tab-appladder.35` | 36 — “c36 & ours & 36 & 167 [115] & 33.09 $\pm$ 1.90 & 0.9365 $\pm$ 0.0208 \\” | 36 | 36.00 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.35` |
| `R1.supp-tab-appladder.36` | 167 — “c36 & ours & 36 & 167 [115] & 33.09 $\pm$ 1.90 & 0.9365 $\pm$ 0.0208 \\” | 167 | 167.35 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.36` |
| `R1.supp-tab-appladder.37` | 115 — “c36 & ours & 36 & 167 [115] & 33.09 $\pm$ 1.90 & 0.9365 $\pm$ 0.0208 \\” | 115 | 114.99 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.37` |
| `R1.supp-tab-appladder.38` | 33.09 — “c36 & ours & 36 & 167 [115] & 33.09 $\pm$ 1.90 & 0.9365 $\pm$ 0.0208 \\” | 33.09 | 33.09 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.38` |
| `R1.supp-tab-appladder.39` | 1.90 — “c36 & ours & 36 & 167 [115] & 33.09 $\pm$ 1.90 & 0.9365 $\pm$ 0.0208 \\” | 1.90 | 1.8953 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.39` |
| `R1.supp-tab-appladder.40` | 0.9365 — “c36 & ours & 36 & 167 [115] & 33.09 $\pm$ 1.90 & 0.9365 $\pm$ 0.0208 \\” | 0.9365 | 0.9365 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.40` |
| `R1.supp-tab-appladder.41` | 0.0208 — “c36 & ours & 36 & 167 [115] & 33.09 $\pm$ 1.90 & 0.9365 $\pm$ 0.0208 \\” | 0.0208 | 0.0208 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.41` |
| `R1.supp-tab-appladder.42` | 113 — “c40 & distributed & --- & 113 [79] & 30.70 $\pm$ 1.97 & 0.9062 $\pm$ 0.0298 \\” | 113 | 112.83 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.42` |
| `R1.supp-tab-appladder.43` | 79 — “c40 & distributed & --- & 113 [79] & 30.70 $\pm$ 1.97 & 0.9062 $\pm$ 0.0298 \\” | 79 | 79.40 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.43` |
| `R1.supp-tab-appladder.44` | 30.70 — “c40 & distributed & --- & 113 [79] & 30.70 $\pm$ 1.97 & 0.9062 $\pm$ 0.0298 \\” | 30.70 | 30.70 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.44` |
| `R1.supp-tab-appladder.45` | 1.97 — “c40 & distributed & --- & 113 [79] & 30.70 $\pm$ 1.97 & 0.9062 $\pm$ 0.0298 \\” | 1.97 | 1.9731 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.45` |
| `R1.supp-tab-appladder.46` | 0.9062 — “c40 & distributed & --- & 113 [79] & 30.70 $\pm$ 1.97 & 0.9062 $\pm$ 0.0298 \\” | 0.9062 | 0.9062 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.46` |
| `R1.supp-tab-appladder.47` | 0.0298 — “c40 & distributed & --- & 113 [79] & 30.70 $\pm$ 1.97 & 0.9062 $\pm$ 0.0298 \\” | 0.0298 | 0.0298 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.47` |
| `R1.supp-tab-appladder.48` | 40 — “x40 & ours & 40 & 109 [76] & 30.91 $\pm$ 1.95 & 0.9076 $\pm$ 0.0293 \\” | 40 | 40.00 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.48` |
| `R1.supp-tab-appladder.49` | 109 — “x40 & ours & 40 & 109 [76] & 30.91 $\pm$ 1.95 & 0.9076 $\pm$ 0.0293 \\” | 109 | 108.68 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.49` |
| `R1.supp-tab-appladder.50` | 76 — “x40 & ours & 40 & 109 [76] & 30.91 $\pm$ 1.95 & 0.9076 $\pm$ 0.0293 \\” | 76 | 76.45 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.50` |
| `R1.supp-tab-appladder.51` | 30.91 — “x40 & ours & 40 & 109 [76] & 30.91 $\pm$ 1.95 & 0.9076 $\pm$ 0.0293 \\” | 30.91 | 30.91 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.51` |
| `R1.supp-tab-appladder.52` | 1.95 — “x40 & ours & 40 & 109 [76] & 30.91 $\pm$ 1.95 & 0.9076 $\pm$ 0.0293 \\” | 1.95 | 1.9531 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.52` |
| `R1.supp-tab-appladder.53` | 0.9076 — “x40 & ours & 40 & 109 [76] & 30.91 $\pm$ 1.95 & 0.9076 $\pm$ 0.0293 \\” | 0.9076 | 0.9076 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.53` |
| `R1.supp-tab-appladder.54` | 0.0293 — “x40 & ours & 40 & 109 [76] & 30.91 $\pm$ 1.95 & 0.9076 $\pm$ 0.0293 \\” | 0.0293 | 0.0293 | `revision-1/registered/ladder_stats.json` | `python verify/claim.py R1.supp-tab-appladder.54` |

## R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1 — Revision 1 — Supplementary Material, §“CAFRL-family arms re-selected on raw weights (E1”

*Supplementary Material, §“CAFRL-family arms re-selected on raw weights (E1”*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.1` | 4 — “4, 11, 8 (Fair-N), 16, 13, 9 (Fair-W) and 4, 8, 23 (E1), seeds 42 / 1 / 2. The extended” | 4 | 4.0000 | `revision-1/exploratory/raw_reselection/f1_none_fair_s42.json` | `python verify/claim.py R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.1` |
| `R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.2` | 11 — “4, 11, 8 (Fair-N), 16, 13, 9 (Fair-W) and 4, 8, 23 (E1), seeds 42 / 1 / 2. The extended” | 11 | 11.00 | `revision-1/exploratory/raw_reselection/f1_none_fair_s1.json` | `python verify/claim.py R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.2` |
| `R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.3` | 8 — “4, 11, 8 (Fair-N), 16, 13, 9 (Fair-W) and 4, 8, 23 (E1), seeds 42 / 1 / 2. The extended” | 8 | 8.0000 | `revision-1/exploratory/raw_reselection/f1_none_fair_s2.json` | `python verify/claim.py R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.3` |
| `R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.4` | 16 — “4, 11, 8 (Fair-N), 16, 13, 9 (Fair-W) and 4, 8, 23 (E1), seeds 42 / 1 / 2. The extended” | 16 | 16.00 | `revision-1/exploratory/raw_reselection/f2_spatres_full_s42.json` | `python verify/claim.py R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.4` |
| `R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.5` | 13 — “4, 11, 8 (Fair-N), 16, 13, 9 (Fair-W) and 4, 8, 23 (E1), seeds 42 / 1 / 2. The extended” | 13 | 13.00 | `revision-1/exploratory/raw_reselection/f2_spatres_full_s1.json` | `python verify/claim.py R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.5` |
| `R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.6` | 9 — “4, 11, 8 (Fair-N), 16, 13, 9 (Fair-W) and 4, 8, 23 (E1), seeds 42 / 1 / 2. The extended” | 9 | 9.0000 | `revision-1/exploratory/raw_reselection/f2_spatres_full_s2.json` | `python verify/claim.py R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.6` |
| `R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.7` | 4 — “4, 11, 8 (Fair-N), 16, 13, 9 (Fair-W) and 4, 8, 23 (E1), seeds 42 / 1 / 2. The extended” | 4 | 4.0000 | `revision-1/exploratory/raw_reselection/r1_fairn_grl_s42.json` | `python verify/claim.py R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.7` |
| `R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.8` | 8 — “4, 11, 8 (Fair-N), 16, 13, 9 (Fair-W) and 4, 8, 23 (E1), seeds 42 / 1 / 2. The extended” | 8 | 8.0000 | `revision-1/exploratory/raw_reselection/r1_fairn_grl_s1.json` | `python verify/claim.py R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.8` |
| `R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.9` | 23 — “4, 11, 8 (Fair-N), 16, 13, 9 (Fair-W) and 4, 8, 23 (E1), seeds 42 / 1 / 2. The extended” | 23 | 23.00 | `revision-1/exploratory/raw_reselection/r1_fairn_grl_s2.json` | `python verify/claim.py R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.9` |
| `R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.10` | 0.00008 — “next-best epoch --- Fair-N seed~1 (0.00008), Fair-W seed~1 (0.00010) and E1 seed~2 (0.0002” | 0.00008 | 0.0001 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.10` |
| `R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.11` | 0.00010 — “next-best epoch --- Fair-N seed~1 (0.00008), Fair-W seed~1 (0.00010) and E1 seed~2 (0.0002” | 0.00010 | 0.0001 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.11` |
| `R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.12` | 0.00022 — “next-best epoch --- Fair-N seed~1 (0.00008), Fair-W seed~1 (0.00010) and E1 seed~2 (0.0002” | 0.00022 | 0.0002 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.12` |

- `R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.10` — weights: raw
- `R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.11` — weights: raw
- `R1.supp-CAFRL-family-arms-re-selected-on-raw-weights-E1.12` — weights: raw

## R1.supp-tab-appexprawsel — Revision 1 — Supplementary Material, tab:appexprawsel

*Supplementary Material, tab:appexprawsel; `\label{tab:appexprawsel}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-tab-appexprawsel.1` | 10,000 — “and \auccomp, with 95\% percentile intervals ($B = 10{,}000$; seeds, then” | 10000 | 10000.00 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-tab-appexprawsel.1` |
| `R1.supp-tab-appexprawsel.2` | 95.63 — “Fair-N (EMA) & 95.63 \ci{93.92}{97.08} & 96.75 \ci{95.39}{97.91} \\” | 95.63 | 95.63 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.2` |
| `R1.supp-tab-appexprawsel.3` | 93.92 — “Fair-N (EMA) & 95.63 \ci{93.92}{97.08} & 96.75 \ci{95.39}{97.91} \\” | 93.92 | 93.92 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.3` |
| `R1.supp-tab-appexprawsel.4` | 97.08 — “Fair-N (EMA) & 95.63 \ci{93.92}{97.08} & 96.75 \ci{95.39}{97.91} \\” | 97.08 | 97.08 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.4` |
| `R1.supp-tab-appexprawsel.5` | 96.75 — “Fair-N (EMA) & 95.63 \ci{93.92}{97.08} & 96.75 \ci{95.39}{97.91} \\” | 96.75 | 96.75 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.5` |
| `R1.supp-tab-appexprawsel.6` | 95.39 — “Fair-N (EMA) & 95.63 \ci{93.92}{97.08} & 96.75 \ci{95.39}{97.91} \\” | 95.39 | 95.39 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.6` |
| `R1.supp-tab-appexprawsel.7` | 97.91 — “Fair-N (EMA) & 95.63 \ci{93.92}{97.08} & 96.75 \ci{95.39}{97.91} \\” | 97.91 | 97.91 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.7` |
| `R1.supp-tab-appexprawsel.8` | 95.28 — “Fair-N (raw) & 95.28 \ci{93.54}{96.79} & 96.68 \ci{95.37}{97.80} \\” | 95.28 | 95.28 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.8` |
| `R1.supp-tab-appexprawsel.9` | 93.54 — “Fair-N (raw) & 95.28 \ci{93.54}{96.79} & 96.68 \ci{95.37}{97.80} \\” | 93.54 | 93.54 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.9` |
| `R1.supp-tab-appexprawsel.10` | 96.79 — “Fair-N (raw) & 95.28 \ci{93.54}{96.79} & 96.68 \ci{95.37}{97.80} \\” | 96.79 | 96.79 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.10` |
| `R1.supp-tab-appexprawsel.11` | 96.68 — “Fair-N (raw) & 95.28 \ci{93.54}{96.79} & 96.68 \ci{95.37}{97.80} \\” | 96.68 | 96.68 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.11` |
| `R1.supp-tab-appexprawsel.12` | 95.37 — “Fair-N (raw) & 95.28 \ci{93.54}{96.79} & 96.68 \ci{95.37}{97.80} \\” | 95.37 | 95.37 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.12` |
| `R1.supp-tab-appexprawsel.13` | 97.80 — “Fair-N (raw) & 95.28 \ci{93.54}{96.79} & 96.68 \ci{95.37}{97.80} \\” | 97.80 | 97.80 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.13` |
| `R1.supp-tab-appexprawsel.14` | 96.19 — “Fair-W (EMA) & 96.19 \ci{94.70}{97.47} & 97.19 \ci{95.85}{98.26} \\” | 96.19 | 96.19 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.14` |
| `R1.supp-tab-appexprawsel.15` | 94.70 — “Fair-W (EMA) & 96.19 \ci{94.70}{97.47} & 97.19 \ci{95.85}{98.26} \\” | 94.70 | 94.70 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.15` |
| `R1.supp-tab-appexprawsel.16` | 97.47 — “Fair-W (EMA) & 96.19 \ci{94.70}{97.47} & 97.19 \ci{95.85}{98.26} \\” | 97.47 | 97.47 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.16` |
| `R1.supp-tab-appexprawsel.17` | 97.19 — “Fair-W (EMA) & 96.19 \ci{94.70}{97.47} & 97.19 \ci{95.85}{98.26} \\” | 97.19 | 97.19 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.17` |
| `R1.supp-tab-appexprawsel.18` | 95.85 — “Fair-W (EMA) & 96.19 \ci{94.70}{97.47} & 97.19 \ci{95.85}{98.26} \\” | 95.85 | 95.85 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.18` |
| `R1.supp-tab-appexprawsel.19` | 98.26 — “Fair-W (EMA) & 96.19 \ci{94.70}{97.47} & 97.19 \ci{95.85}{98.26} \\” | 98.26 | 98.26 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.19` |
| `R1.supp-tab-appexprawsel.20` | 94.93 — “Fair-W (raw) & 94.93 \ci{92.96}{96.66} & 96.38 \ci{94.74}{97.71} \\” | 94.93 | 94.93 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.20` |
| `R1.supp-tab-appexprawsel.21` | 92.96 — “Fair-W (raw) & 94.93 \ci{92.96}{96.66} & 96.38 \ci{94.74}{97.71} \\” | 92.96 | 92.96 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.21` |
| `R1.supp-tab-appexprawsel.22` | 96.66 — “Fair-W (raw) & 94.93 \ci{92.96}{96.66} & 96.38 \ci{94.74}{97.71} \\” | 96.66 | 96.66 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.22` |
| `R1.supp-tab-appexprawsel.23` | 96.38 — “Fair-W (raw) & 94.93 \ci{92.96}{96.66} & 96.38 \ci{94.74}{97.71} \\” | 96.38 | 96.38 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.23` |
| `R1.supp-tab-appexprawsel.24` | 94.74 — “Fair-W (raw) & 94.93 \ci{92.96}{96.66} & 96.38 \ci{94.74}{97.71} \\” | 94.74 | 94.74 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.24` |
| `R1.supp-tab-appexprawsel.25` | 97.71 — “Fair-W (raw) & 94.93 \ci{92.96}{96.66} & 96.38 \ci{94.74}{97.71} \\” | 97.71 | 97.71 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.25` |
| `R1.supp-tab-appexprawsel.26` | 96.50 — “E1 (EMA) & 96.50 \ci{95.14}{97.72} & 97.48 \ci{96.37}{98.43} \\” | 96.50 | 96.50 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.26` |
| `R1.supp-tab-appexprawsel.27` | 95.14 — “E1 (EMA) & 96.50 \ci{95.14}{97.72} & 97.48 \ci{96.37}{98.43} \\” | 95.14 | 95.14 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.27` |
| `R1.supp-tab-appexprawsel.28` | 97.72 — “E1 (EMA) & 96.50 \ci{95.14}{97.72} & 97.48 \ci{96.37}{98.43} \\” | 97.72 | 97.72 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.28` |
| `R1.supp-tab-appexprawsel.29` | 97.48 — “E1 (EMA) & 96.50 \ci{95.14}{97.72} & 97.48 \ci{96.37}{98.43} \\” | 97.48 | 97.48 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.29` |
| `R1.supp-tab-appexprawsel.30` | 96.37 — “E1 (EMA) & 96.50 \ci{95.14}{97.72} & 97.48 \ci{96.37}{98.43} \\” | 96.37 | 96.37 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.30` |
| `R1.supp-tab-appexprawsel.31` | 98.43 — “E1 (EMA) & 96.50 \ci{95.14}{97.72} & 97.48 \ci{96.37}{98.43} \\” | 98.43 | 98.43 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.31` |
| `R1.supp-tab-appexprawsel.32` | 95.34 — “E1 (raw) & 95.34 \ci{93.69}{96.81} & 96.74 \ci{95.49}{97.84} \\” | 95.34 | 95.34 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.32` |
| `R1.supp-tab-appexprawsel.33` | 93.69 — “E1 (raw) & 95.34 \ci{93.69}{96.81} & 96.74 \ci{95.49}{97.84} \\” | 93.69 | 93.69 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.33` |
| `R1.supp-tab-appexprawsel.34` | 96.81 — “E1 (raw) & 95.34 \ci{93.69}{96.81} & 96.74 \ci{95.49}{97.84} \\” | 96.81 | 96.81 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.34` |
| `R1.supp-tab-appexprawsel.35` | 96.74 — “E1 (raw) & 95.34 \ci{93.69}{96.81} & 96.74 \ci{95.49}{97.84} \\” | 96.74 | 96.74 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.35` |
| `R1.supp-tab-appexprawsel.36` | 95.49 — “E1 (raw) & 95.34 \ci{93.69}{96.81} & 96.74 \ci{95.49}{97.84} \\” | 95.49 | 95.49 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.36` |
| `R1.supp-tab-appexprawsel.37` | 97.84 — “E1 (raw) & 95.34 \ci{93.69}{96.81} & 96.74 \ci{95.49}{97.84} \\” | 97.84 | 97.84 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.37` |
| `R1.supp-tab-appexprawsel.38` | 95.65 — “SpatialBase (raw) & 95.65 \ci{94.01}{97.04} & 96.88 \ci{95.60}{97.94} \\” | 95.65 | 95.65 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.38` |
| `R1.supp-tab-appexprawsel.39` | 94.01 — “SpatialBase (raw) & 95.65 \ci{94.01}{97.04} & 96.88 \ci{95.60}{97.94} \\” | 94.01 | 94.01 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.39` |
| `R1.supp-tab-appexprawsel.40` | 97.04 — “SpatialBase (raw) & 95.65 \ci{94.01}{97.04} & 96.88 \ci{95.60}{97.94} \\” | 97.04 | 97.04 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.40` |
| `R1.supp-tab-appexprawsel.41` | 96.88 — “SpatialBase (raw) & 95.65 \ci{94.01}{97.04} & 96.88 \ci{95.60}{97.94} \\” | 96.88 | 96.88 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.41` |
| `R1.supp-tab-appexprawsel.42` | 95.60 — “SpatialBase (raw) & 95.65 \ci{94.01}{97.04} & 96.88 \ci{95.60}{97.94} \\” | 95.60 | 95.60 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.42` |
| `R1.supp-tab-appexprawsel.43` | 97.94 — “SpatialBase (raw) & 95.65 \ci{94.01}{97.04} & 96.88 \ci{95.60}{97.94} \\” | 97.94 | 97.94 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.43` |
| `R1.supp-tab-appexprawsel.44` | 95.36 — “TrunkCtrl (raw) & 95.36 \ci{93.74}{96.77} & 96.74 \ci{95.46}{97.85} \\” | 95.36 | 95.36 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.44` |
| `R1.supp-tab-appexprawsel.45` | 93.74 — “TrunkCtrl (raw) & 95.36 \ci{93.74}{96.77} & 96.74 \ci{95.46}{97.85} \\” | 93.74 | 93.74 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.45` |
| `R1.supp-tab-appexprawsel.46` | 96.77 — “TrunkCtrl (raw) & 95.36 \ci{93.74}{96.77} & 96.74 \ci{95.46}{97.85} \\” | 96.77 | 96.77 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.46` |
| `R1.supp-tab-appexprawsel.47` | 96.74 — “TrunkCtrl (raw) & 95.36 \ci{93.74}{96.77} & 96.74 \ci{95.46}{97.85} \\” | 96.74 | 96.74 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.47` |
| `R1.supp-tab-appexprawsel.48` | 95.46 — “TrunkCtrl (raw) & 95.36 \ci{93.74}{96.77} & 96.74 \ci{95.46}{97.85} \\” | 95.46 | 95.46 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.48` |
| `R1.supp-tab-appexprawsel.49` | 97.85 — “TrunkCtrl (raw) & 95.36 \ci{93.74}{96.77} & 96.74 \ci{95.46}{97.85} \\” | 97.85 | 97.85 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.49` |
| `R1.supp-tab-appexprawsel.50` | -0.37 — “Fair-N raw $-$ SpatialBase & $-0.37$ \ci{-1.57}{0.93} & $-0.20$ \ci{-1.02}{0.67} \\” | -0.37 | -0.3690 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.50` |
| `R1.supp-tab-appexprawsel.51` | -1.57 — “Fair-N raw $-$ SpatialBase & $-0.37$ \ci{-1.57}{0.93} & $-0.20$ \ci{-1.02}{0.67} \\” | -1.57 | -1.5744 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.51` |
| `R1.supp-tab-appexprawsel.52` | 0.93 — “Fair-N raw $-$ SpatialBase & $-0.37$ \ci{-1.57}{0.93} & $-0.20$ \ci{-1.02}{0.67} \\” | 0.93 | 0.9294 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.52` |
| `R1.supp-tab-appexprawsel.53` | -0.20 — “Fair-N raw $-$ SpatialBase & $-0.37$ \ci{-1.57}{0.93} & $-0.20$ \ci{-1.02}{0.67} \\” | -0.20 | -0.2032 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.53` |
| `R1.supp-tab-appexprawsel.54` | -1.02 — “Fair-N raw $-$ SpatialBase & $-0.37$ \ci{-1.57}{0.93} & $-0.20$ \ci{-1.02}{0.67} \\” | -1.02 | -1.0169 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.54` |
| `R1.supp-tab-appexprawsel.55` | 0.67 — “Fair-N raw $-$ SpatialBase & $-0.37$ \ci{-1.57}{0.93} & $-0.20$ \ci{-1.02}{0.67} \\” | 0.67 | 0.6748 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.55` |
| `R1.supp-tab-appexprawsel.56` | -0.72 — “Fair-W raw $-$ SpatialBase & $-0.72$ \ci{-2.14}{0.69} & $-0.51$ \ci{-1.70}{0.48} \\” | -0.72 | -0.7198 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.56` |
| `R1.supp-tab-appexprawsel.57` | -2.14 — “Fair-W raw $-$ SpatialBase & $-0.72$ \ci{-2.14}{0.69} & $-0.51$ \ci{-1.70}{0.48} \\” | -2.14 | -2.1399 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.57` |
| `R1.supp-tab-appexprawsel.58` | 0.69 — “Fair-W raw $-$ SpatialBase & $-0.72$ \ci{-2.14}{0.69} & $-0.51$ \ci{-1.70}{0.48} \\” | 0.69 | 0.6858 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.58` |
| `R1.supp-tab-appexprawsel.59` | -0.51 — “Fair-W raw $-$ SpatialBase & $-0.72$ \ci{-2.14}{0.69} & $-0.51$ \ci{-1.70}{0.48} \\” | -0.51 | -0.5068 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.59` |
| `R1.supp-tab-appexprawsel.60` | -1.70 — “Fair-W raw $-$ SpatialBase & $-0.72$ \ci{-2.14}{0.69} & $-0.51$ \ci{-1.70}{0.48} \\” | -1.70 | -1.7042 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.60` |
| `R1.supp-tab-appexprawsel.61` | 0.48 — “Fair-W raw $-$ SpatialBase & $-0.72$ \ci{-2.14}{0.69} & $-0.51$ \ci{-1.70}{0.48} \\” | 0.48 | 0.4809 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.61` |
| `R1.supp-tab-appexprawsel.62` | 0.06 — “E1 raw $-$ Fair-N raw & 0.06 \ci{-1.13}{1.28} & 0.06 \ci{-0.67}{0.78} \\” | 0.06 | 0.0608 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.62` |
| `R1.supp-tab-appexprawsel.63` | -1.13 — “E1 raw $-$ Fair-N raw & 0.06 \ci{-1.13}{1.28} & 0.06 \ci{-0.67}{0.78} \\” | -1.13 | -1.1254 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.63` |
| `R1.supp-tab-appexprawsel.64` | 1.28 — “E1 raw $-$ Fair-N raw & 0.06 \ci{-1.13}{1.28} & 0.06 \ci{-0.67}{0.78} \\” | 1.28 | 1.2845 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.64` |
| `R1.supp-tab-appexprawsel.65` | 0.06 — “E1 raw $-$ Fair-N raw & 0.06 \ci{-1.13}{1.28} & 0.06 \ci{-0.67}{0.78} \\” | 0.06 | 0.0572 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.65` |
| `R1.supp-tab-appexprawsel.66` | -0.67 — “E1 raw $-$ Fair-N raw & 0.06 \ci{-1.13}{1.28} & 0.06 \ci{-0.67}{0.78} \\” | -0.67 | -0.6721 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.66` |
| `R1.supp-tab-appexprawsel.67` | 0.78 — “E1 raw $-$ Fair-N raw & 0.06 \ci{-1.13}{1.28} & 0.06 \ci{-0.67}{0.78} \\” | 0.78 | 0.7826 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.67` |
| `R1.supp-tab-appexprawsel.68` | -0.35 — “Fair-N raw $-$ Fair-N EMA & $-0.35$ \ci{-1.47}{0.73} & $-0.07$ \ci{-0.87}{0.75} \\” | -0.35 | -0.3452 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.68` |
| `R1.supp-tab-appexprawsel.69` | -1.47 — “Fair-N raw $-$ Fair-N EMA & $-0.35$ \ci{-1.47}{0.73} & $-0.07$ \ci{-0.87}{0.75} \\” | -1.47 | -1.4690 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.69` |
| `R1.supp-tab-appexprawsel.70` | 0.73 — “Fair-N raw $-$ Fair-N EMA & $-0.35$ \ci{-1.47}{0.73} & $-0.07$ \ci{-0.87}{0.75} \\” | 0.73 | 0.7305 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.70` |
| `R1.supp-tab-appexprawsel.71` | -0.07 — “Fair-N raw $-$ Fair-N EMA & $-0.35$ \ci{-1.47}{0.73} & $-0.07$ \ci{-0.87}{0.75} \\” | -0.07 | -0.0680 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.71` |
| `R1.supp-tab-appexprawsel.72` | -0.87 — “Fair-N raw $-$ Fair-N EMA & $-0.35$ \ci{-1.47}{0.73} & $-0.07$ \ci{-0.87}{0.75} \\” | -0.87 | -0.8698 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.72` |
| `R1.supp-tab-appexprawsel.73` | 0.75 — “Fair-N raw $-$ Fair-N EMA & $-0.35$ \ci{-1.47}{0.73} & $-0.07$ \ci{-0.87}{0.75} \\” | 0.75 | 0.7460 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.73` |
| `R1.supp-tab-appexprawsel.74` | -1.25 — “Fair-W raw $-$ Fair-W EMA & $-1.25$ \ci{-2.54}{-0.003} & $-0.82$ \ci{-1.85}{0.07} \\” | -1.25 | -1.2538 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.74` |
| `R1.supp-tab-appexprawsel.75` | -2.54 — “Fair-W raw $-$ Fair-W EMA & $-1.25$ \ci{-2.54}{-0.003} & $-0.82$ \ci{-1.85}{0.07} \\” | -2.54 | -2.5379 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.75` |
| `R1.supp-tab-appexprawsel.76` | -0.003 — “Fair-W raw $-$ Fair-W EMA & $-1.25$ \ci{-2.54}{-0.003} & $-0.82$ \ci{-1.85}{0.07} \\” | -0.003 | -0.0026 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.76` |
| `R1.supp-tab-appexprawsel.77` | -0.82 — “Fair-W raw $-$ Fair-W EMA & $-1.25$ \ci{-2.54}{-0.003} & $-0.82$ \ci{-1.85}{0.07} \\” | -0.82 | -0.8163 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.77` |
| `R1.supp-tab-appexprawsel.78` | -1.85 — “Fair-W raw $-$ Fair-W EMA & $-1.25$ \ci{-2.54}{-0.003} & $-0.82$ \ci{-1.85}{0.07} \\” | -1.85 | -1.8483 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.78` |
| `R1.supp-tab-appexprawsel.79` | 0.07 — “Fair-W raw $-$ Fair-W EMA & $-1.25$ \ci{-2.54}{-0.003} & $-0.82$ \ci{-1.85}{0.07} \\” | 0.07 | 0.0669 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.79` |
| `R1.supp-tab-appexprawsel.80` | -1.15 — “E1 raw $-$ E1 EMA & $-1.15$ \ci{-2.21}{-0.21} & $-0.74$ \ci{-1.35}{-0.19} \\” | -1.15 | -1.1522 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.80` |
| `R1.supp-tab-appexprawsel.81` | -2.21 — “E1 raw $-$ E1 EMA & $-1.15$ \ci{-2.21}{-0.21} & $-0.74$ \ci{-1.35}{-0.19} \\” | -2.21 | -2.2127 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.81` |
| `R1.supp-tab-appexprawsel.82` | -0.21 — “E1 raw $-$ E1 EMA & $-1.15$ \ci{-2.21}{-0.21} & $-0.74$ \ci{-1.35}{-0.19} \\” | -0.21 | -0.2066 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.82` |
| `R1.supp-tab-appexprawsel.83` | -0.74 — “E1 raw $-$ E1 EMA & $-1.15$ \ci{-2.21}{-0.21} & $-0.74$ \ci{-1.35}{-0.19} \\” | -0.74 | -0.7411 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.83` |
| `R1.supp-tab-appexprawsel.84` | -1.35 — “E1 raw $-$ E1 EMA & $-1.15$ \ci{-2.21}{-0.21} & $-0.74$ \ci{-1.35}{-0.19} \\” | -1.35 | -1.3532 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.84` |
| `R1.supp-tab-appexprawsel.85` | -0.19 — “E1 raw $-$ E1 EMA & $-1.15$ \ci{-2.21}{-0.21} & $-0.74$ \ci{-1.35}{-0.19} \\” | -0.19 | -0.1857 | `revision-1/exploratory/rev1/e10.json` | `python verify/claim.py R1.supp-tab-appexprawsel.85` |
| `R1.supp-tab-appexprawsel.86` | 92.31 — “CAFRL as specified, mean of 3 (raw) & 92.31 & 94.70 \\” | 92.31 | 92.31 | `revision-1/exploratory/e10_ext.json` | `python verify/claim.py R1.supp-tab-appexprawsel.86` |
| `R1.supp-tab-appexprawsel.87` | 94.70 — “CAFRL as specified, mean of 3 (raw) & 92.31 & 94.70 \\” | 94.70 | 94.70 | `revision-1/exploratory/e10_ext.json` | `python verify/claim.py R1.supp-tab-appexprawsel.87` |
| `R1.supp-tab-appexprawsel.88` | 92.17 — “CAFRL as specified, mean of 3 (EMA) & 92.17 & 94.71 \\” | 92.17 | 92.17 | `revision-1/exploratory/e10_ext.json` | `python verify/claim.py R1.supp-tab-appexprawsel.88` |
| `R1.supp-tab-appexprawsel.89` | 94.71 — “CAFRL as specified, mean of 3 (EMA) & 92.17 & 94.71 \\” | 94.71 | 94.71 | `revision-1/exploratory/e10_ext.json` | `python verify/claim.py R1.supp-tab-appexprawsel.89` |
| `R1.supp-tab-appexprawsel.90` | 91.88 — “CAFRL$-$adv, seed 42 (raw) & 91.88 & 93.67 \\” | 91.88 | 91.88 | `revision-1/exploratory/e10_ext.json` | `python verify/claim.py R1.supp-tab-appexprawsel.90` |
| `R1.supp-tab-appexprawsel.91` | 93.67 — “CAFRL$-$adv, seed 42 (raw) & 91.88 & 93.67 \\” | 93.67 | 93.67 | `revision-1/exploratory/e10_ext.json` | `python verify/claim.py R1.supp-tab-appexprawsel.91` |
| `R1.supp-tab-appexprawsel.92` | 91.90 — “CAFRL$-$adv, seed 42 (EMA) & 91.90 & 93.94 \\” | 91.90 | 91.90 | `revision-1/exploratory/e10_ext.json` | `python verify/claim.py R1.supp-tab-appexprawsel.92` |
| `R1.supp-tab-appexprawsel.93` | 93.94 — “CAFRL$-$adv, seed 42 (EMA) & 91.90 & 93.94 \\” | 93.94 | 93.94 | `revision-1/exploratory/e10_ext.json` | `python verify/claim.py R1.supp-tab-appexprawsel.93` |
| `R1.supp-tab-appexprawsel.94` | 91.26 — “spatial-residual, seed 42 (raw) & 91.26 & 93.50 \\” | 91.26 | 91.26 | `revision-1/exploratory/e10_ext.json` | `python verify/claim.py R1.supp-tab-appexprawsel.94` |
| `R1.supp-tab-appexprawsel.95` | 93.50 — “spatial-residual, seed 42 (raw) & 91.26 & 93.50 \\” | 93.50 | 93.50 | `revision-1/exploratory/e10_ext.json` | `python verify/claim.py R1.supp-tab-appexprawsel.95` |
| `R1.supp-tab-appexprawsel.96` | 91.39 — “spatial-residual, seed 42 (EMA) & 91.39 & 93.81 \\” | 91.39 | 91.39 | `revision-1/exploratory/e10_ext.json` | `python verify/claim.py R1.supp-tab-appexprawsel.96` |
| `R1.supp-tab-appexprawsel.97` | 93.81 — “spatial-residual, seed 42 (EMA) & 91.39 & 93.81 \\” | 93.81 | 93.81 | `revision-1/exploratory/e10_ext.json` | `python verify/claim.py R1.supp-tab-appexprawsel.97` |

- `R1.supp-tab-appexprawsel.2` — weights: EMA
- `R1.supp-tab-appexprawsel.3` — weights: EMA
- `R1.supp-tab-appexprawsel.4` — weights: EMA
- `R1.supp-tab-appexprawsel.5` — weights: EMA
- `R1.supp-tab-appexprawsel.6` — weights: EMA
- `R1.supp-tab-appexprawsel.7` — weights: EMA
- `R1.supp-tab-appexprawsel.8` — weights: raw
- `R1.supp-tab-appexprawsel.9` — weights: raw
- `R1.supp-tab-appexprawsel.10` — weights: raw
- `R1.supp-tab-appexprawsel.11` — weights: raw
- `R1.supp-tab-appexprawsel.12` — weights: raw
- `R1.supp-tab-appexprawsel.13` — weights: raw
- `R1.supp-tab-appexprawsel.14` — weights: EMA
- `R1.supp-tab-appexprawsel.15` — weights: EMA
- `R1.supp-tab-appexprawsel.16` — weights: EMA
- `R1.supp-tab-appexprawsel.17` — weights: EMA
- `R1.supp-tab-appexprawsel.18` — weights: EMA
- `R1.supp-tab-appexprawsel.19` — weights: EMA
- `R1.supp-tab-appexprawsel.20` — weights: raw
- `R1.supp-tab-appexprawsel.21` — weights: raw
- `R1.supp-tab-appexprawsel.22` — weights: raw
- `R1.supp-tab-appexprawsel.23` — weights: raw
- `R1.supp-tab-appexprawsel.24` — weights: raw
- `R1.supp-tab-appexprawsel.25` — weights: raw
- `R1.supp-tab-appexprawsel.26` — weights: EMA
- `R1.supp-tab-appexprawsel.27` — weights: EMA
- `R1.supp-tab-appexprawsel.28` — weights: EMA
- `R1.supp-tab-appexprawsel.29` — weights: EMA
- `R1.supp-tab-appexprawsel.30` — weights: EMA
- `R1.supp-tab-appexprawsel.31` — weights: EMA
- `R1.supp-tab-appexprawsel.32` — weights: raw
- `R1.supp-tab-appexprawsel.33` — weights: raw
- `R1.supp-tab-appexprawsel.34` — weights: raw
- `R1.supp-tab-appexprawsel.35` — weights: raw
- `R1.supp-tab-appexprawsel.36` — weights: raw
- `R1.supp-tab-appexprawsel.37` — weights: raw
- `R1.supp-tab-appexprawsel.38` — weights: raw
- `R1.supp-tab-appexprawsel.39` — weights: raw
- `R1.supp-tab-appexprawsel.40` — weights: raw
- `R1.supp-tab-appexprawsel.41` — weights: raw
- `R1.supp-tab-appexprawsel.42` — weights: raw
- `R1.supp-tab-appexprawsel.43` — weights: raw
- `R1.supp-tab-appexprawsel.44` — weights: raw
- `R1.supp-tab-appexprawsel.45` — weights: raw
- `R1.supp-tab-appexprawsel.46` — weights: raw
- `R1.supp-tab-appexprawsel.47` — weights: raw
- `R1.supp-tab-appexprawsel.48` — weights: raw
- `R1.supp-tab-appexprawsel.49` — weights: raw
- `R1.supp-tab-appexprawsel.50` — weights: raw
- `R1.supp-tab-appexprawsel.51` — weights: raw
- `R1.supp-tab-appexprawsel.52` — weights: raw
- `R1.supp-tab-appexprawsel.53` — weights: raw
- `R1.supp-tab-appexprawsel.54` — weights: raw
- `R1.supp-tab-appexprawsel.55` — weights: raw
- `R1.supp-tab-appexprawsel.56` — weights: raw
- `R1.supp-tab-appexprawsel.57` — weights: raw
- `R1.supp-tab-appexprawsel.58` — weights: raw
- `R1.supp-tab-appexprawsel.59` — weights: raw
- `R1.supp-tab-appexprawsel.60` — weights: raw
- `R1.supp-tab-appexprawsel.61` — weights: raw
- `R1.supp-tab-appexprawsel.62` — weights: raw
- `R1.supp-tab-appexprawsel.63` — weights: raw
- `R1.supp-tab-appexprawsel.64` — weights: raw
- `R1.supp-tab-appexprawsel.65` — weights: raw
- `R1.supp-tab-appexprawsel.66` — weights: raw
- `R1.supp-tab-appexprawsel.67` — weights: raw
- `R1.supp-tab-appexprawsel.68` — weights: raw and EMA
- `R1.supp-tab-appexprawsel.69` — weights: raw and EMA
- `R1.supp-tab-appexprawsel.70` — weights: raw and EMA
- `R1.supp-tab-appexprawsel.71` — weights: raw and EMA
- `R1.supp-tab-appexprawsel.72` — weights: raw and EMA
- `R1.supp-tab-appexprawsel.73` — weights: raw and EMA
- `R1.supp-tab-appexprawsel.74` — weights: raw and EMA
- `R1.supp-tab-appexprawsel.75` — weights: raw and EMA
- `R1.supp-tab-appexprawsel.76` — weights: raw and EMA
- `R1.supp-tab-appexprawsel.77` — weights: raw and EMA
- `R1.supp-tab-appexprawsel.78` — weights: raw and EMA
- `R1.supp-tab-appexprawsel.79` — weights: raw and EMA
- `R1.supp-tab-appexprawsel.80` — weights: raw and EMA
- `R1.supp-tab-appexprawsel.81` — weights: raw and EMA
- `R1.supp-tab-appexprawsel.82` — weights: raw and EMA
- `R1.supp-tab-appexprawsel.83` — weights: raw and EMA
- `R1.supp-tab-appexprawsel.84` — weights: raw and EMA
- `R1.supp-tab-appexprawsel.85` — weights: raw and EMA

## R1.supp-Cost-E10b-descriptive — Revision 1 — Supplementary Material, §“Cost (E10b, descriptive)”

*Supplementary Material, §“Cost (E10b, descriptive)”*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-Cost-E10b-descriptive.1` | 3,840 — “CPU was shared during timing. The 3{,}840 parameters of every CAFRL-family model” | 3840 | 3840.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-Cost-E10b-descriptive.1` |

## R1.supp-tab-appexpcost — Revision 1 — Supplementary Material, tab:appexpcost

*Supplementary Material, tab:appexpcost; `\label{tab:appexpcost}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-tab-appexpcost.1` | 11,971,561 — “CAFRL as specified (EMA) & 11{,}971{,}561 & 11{,}967{,}721 & 8.904 & 15.47 (0.53) & 20.48 ” | 11971561 | 11971561.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.1` |
| `R1.supp-tab-appexpcost.2` | 11,967,721 — “CAFRL as specified (EMA) & 11{,}971{,}561 & 11{,}967{,}721 & 8.904 & 15.47 (0.53) & 20.48 ” | 11967721 | 11967721.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.2` |
| `R1.supp-tab-appexpcost.3` | 8.904 — “CAFRL as specified (EMA) & 11{,}971{,}561 & 11{,}967{,}721 & 8.904 & 15.47 (0.53) & 20.48 ” | 8.904 | 8.9042 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.3` |
| `R1.supp-tab-appexpcost.4` | 15.47 — “CAFRL as specified (EMA) & 11{,}971{,}561 & 11{,}967{,}721 & 8.904 & 15.47 (0.53) & 20.48 ” | 15.47 | 15.47 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.4` |
| `R1.supp-tab-appexpcost.5` | 0.53 — “CAFRL as specified (EMA) & 11{,}971{,}561 & 11{,}967{,}721 & 8.904 & 15.47 (0.53) & 20.48 ” | 0.53 | 0.5350 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.5` |
| `R1.supp-tab-appexpcost.6` | 20.48 — “CAFRL as specified (EMA) & 11{,}971{,}561 & 11{,}967{,}721 & 8.904 & 15.47 (0.53) & 20.48 ” | 20.48 | 20.48 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.6` |
| `R1.supp-tab-appexpcost.7` | 1563 — “CAFRL as specified (EMA) & 11{,}971{,}561 & 11{,}967{,}721 & 8.904 & 15.47 (0.53) & 20.48 ” | 1563 | 1562.57 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.7` |
| `R1.supp-tab-appexpcost.8` | 608 — “CAFRL as specified (EMA) & 11{,}971{,}561 & 11{,}967{,}721 & 8.904 & 15.47 (0.53) & 20.48 ” | 608 | 607.81 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.8` |
| `R1.supp-tab-appexpcost.9` | 11,971,561 — “E1 (EMA) & 11{,}971{,}561 & 11{,}967{,}721 & 8.904 & 16.02 (0.34) & 20.55 & 1557 & 613 \\” | 11971561 | 11971561.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.9` |
| `R1.supp-tab-appexpcost.10` | 11,967,721 — “E1 (EMA) & 11{,}971{,}561 & 11{,}967{,}721 & 8.904 & 16.02 (0.34) & 20.55 & 1557 & 613 \\” | 11967721 | 11967721.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.10` |
| `R1.supp-tab-appexpcost.11` | 8.904 — “E1 (EMA) & 11{,}971{,}561 & 11{,}967{,}721 & 8.904 & 16.02 (0.34) & 20.55 & 1557 & 613 \\” | 8.904 | 8.9042 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.11` |
| `R1.supp-tab-appexpcost.12` | 16.02 — “E1 (EMA) & 11{,}971{,}561 & 11{,}967{,}721 & 8.904 & 16.02 (0.34) & 20.55 & 1557 & 613 \\” | 16.02 | 16.02 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.12` |
| `R1.supp-tab-appexpcost.13` | 0.34 — “E1 (EMA) & 11{,}971{,}561 & 11{,}967{,}721 & 8.904 & 16.02 (0.34) & 20.55 & 1557 & 613 \\” | 0.34 | 0.3379 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.13` |
| `R1.supp-tab-appexpcost.14` | 20.55 — “E1 (EMA) & 11{,}971{,}561 & 11{,}967{,}721 & 8.904 & 16.02 (0.34) & 20.55 & 1557 & 613 \\” | 20.55 | 20.55 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.14` |
| `R1.supp-tab-appexpcost.15` | 1557 — “E1 (EMA) & 11{,}971{,}561 & 11{,}967{,}721 & 8.904 & 16.02 (0.34) & 20.55 & 1557 & 613 \\” | 1557 | 1557.49 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.15` |
| `R1.supp-tab-appexpcost.16` | 613 — “E1 (EMA) & 11{,}971{,}561 & 11{,}967{,}721 & 8.904 & 16.02 (0.34) & 20.55 & 1557 & 613 \\” | 613 | 613.49 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.16` |
| `R1.supp-tab-appexpcost.17` | 10,652,643 — “Fair-N (EMA) & 10{,}652{,}643 & 10{,}648{,}803 & 8.902 & 15.97 (2.20) & 20.07 & 1594 & 607” | 10652643 | 10652643.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.17` |
| `R1.supp-tab-appexpcost.18` | 10,648,803 — “Fair-N (EMA) & 10{,}652{,}643 & 10{,}648{,}803 & 8.902 & 15.97 (2.20) & 20.07 & 1594 & 607” | 10648803 | 10648803.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.18` |
| `R1.supp-tab-appexpcost.19` | 8.902 — “Fair-N (EMA) & 10{,}652{,}643 & 10{,}648{,}803 & 8.902 & 15.97 (2.20) & 20.07 & 1594 & 607” | 8.902 | 8.9016 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.19` |
| `R1.supp-tab-appexpcost.20` | 15.97 — “Fair-N (EMA) & 10{,}652{,}643 & 10{,}648{,}803 & 8.902 & 15.97 (2.20) & 20.07 & 1594 & 607” | 15.97 | 15.97 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.20` |
| `R1.supp-tab-appexpcost.21` | 2.20 — “Fair-N (EMA) & 10{,}652{,}643 & 10{,}648{,}803 & 8.902 & 15.97 (2.20) & 20.07 & 1594 & 607” | 2.20 | 2.2005 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.21` |
| `R1.supp-tab-appexpcost.22` | 20.07 — “Fair-N (EMA) & 10{,}652{,}643 & 10{,}648{,}803 & 8.902 & 15.97 (2.20) & 20.07 & 1594 & 607” | 20.07 | 20.07 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.22` |
| `R1.supp-tab-appexpcost.23` | 1594 — “Fair-N (EMA) & 10{,}652{,}643 & 10{,}648{,}803 & 8.902 & 15.97 (2.20) & 20.07 & 1594 & 607” | 1594 | 1594.32 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.23` |
| `R1.supp-tab-appexpcost.24` | 607 — “Fair-N (EMA) & 10{,}652{,}643 & 10{,}648{,}803 & 8.902 & 15.97 (2.20) & 20.07 & 1594 & 607” | 607 | 607.47 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.24` |
| `R1.supp-tab-appexpcost.25` | 10,652,643 — “CAFRL$-$adv (EMA) & 10{,}652{,}643 & 10{,}648{,}803 & 8.902 & 15.43 (0.33) & 20.06 & 1595 ” | 10652643 | 10652643.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.25` |
| `R1.supp-tab-appexpcost.26` | 10,648,803 — “CAFRL$-$adv (EMA) & 10{,}652{,}643 & 10{,}648{,}803 & 8.902 & 15.43 (0.33) & 20.06 & 1595 ” | 10648803 | 10648803.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.26` |
| `R1.supp-tab-appexpcost.27` | 8.902 — “CAFRL$-$adv (EMA) & 10{,}652{,}643 & 10{,}648{,}803 & 8.902 & 15.43 (0.33) & 20.06 & 1595 ” | 8.902 | 8.9016 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.27` |
| `R1.supp-tab-appexpcost.28` | 15.43 — “CAFRL$-$adv (EMA) & 10{,}652{,}643 & 10{,}648{,}803 & 8.902 & 15.43 (0.33) & 20.06 & 1595 ” | 15.43 | 15.43 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.28` |
| `R1.supp-tab-appexpcost.29` | 0.33 — “CAFRL$-$adv (EMA) & 10{,}652{,}643 & 10{,}648{,}803 & 8.902 & 15.43 (0.33) & 20.06 & 1595 ” | 0.33 | 0.3273 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.29` |
| `R1.supp-tab-appexpcost.30` | 20.06 — “CAFRL$-$adv (EMA) & 10{,}652{,}643 & 10{,}648{,}803 & 8.902 & 15.43 (0.33) & 20.06 & 1595 ” | 20.06 | 20.06 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.30` |
| `R1.supp-tab-appexpcost.31` | 1595 — “CAFRL$-$adv (EMA) & 10{,}652{,}643 & 10{,}648{,}803 & 8.902 & 15.43 (0.33) & 20.06 & 1595 ” | 1595 | 1594.87 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.31` |
| `R1.supp-tab-appexpcost.32` | 613 — “CAFRL$-$adv (EMA) & 10{,}652{,}643 & 10{,}648{,}803 & 8.902 & 15.43 (0.33) & 20.06 & 1595 ” | 613 | 613.24 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.32` |
| `R1.supp-tab-appexpcost.33` | 10,288,055 — “spatial-residual (EMA) & 10{,}288{,}055 & 10{,}284{,}215 & 8.852 & 13.75 (0.47) & 18.02 & ” | 10288055 | 10288055.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.33` |
| `R1.supp-tab-appexpcost.34` | 10,284,215 — “spatial-residual (EMA) & 10{,}288{,}055 & 10{,}284{,}215 & 8.852 & 13.75 (0.47) & 18.02 & ” | 10284215 | 10284215.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.34` |
| `R1.supp-tab-appexpcost.35` | 8.852 — “spatial-residual (EMA) & 10{,}288{,}055 & 10{,}284{,}215 & 8.852 & 13.75 (0.47) & 18.02 & ” | 8.852 | 8.8519 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.35` |
| `R1.supp-tab-appexpcost.36` | 13.75 — “spatial-residual (EMA) & 10{,}288{,}055 & 10{,}284{,}215 & 8.852 & 13.75 (0.47) & 18.02 & ” | 13.75 | 13.75 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.36` |
| `R1.supp-tab-appexpcost.37` | 0.47 — “spatial-residual (EMA) & 10{,}288{,}055 & 10{,}284{,}215 & 8.852 & 13.75 (0.47) & 18.02 & ” | 0.47 | 0.4739 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.37` |
| `R1.supp-tab-appexpcost.38` | 18.02 — “spatial-residual (EMA) & 10{,}288{,}055 & 10{,}284{,}215 & 8.852 & 13.75 (0.47) & 18.02 & ” | 18.02 | 18.02 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.38` |
| `R1.supp-tab-appexpcost.39` | 1776 — “spatial-residual (EMA) & 10{,}288{,}055 & 10{,}284{,}215 & 8.852 & 13.75 (0.47) & 18.02 & ” | 1776 | 1775.52 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.39` |
| `R1.supp-tab-appexpcost.40` | 611 — “spatial-residual (EMA) & 10{,}288{,}055 & 10{,}284{,}215 & 8.852 & 13.75 (0.47) & 18.02 & ” | 611 | 610.52 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.40` |
| `R1.supp-tab-appexpcost.41` | 9,628,081 — “Fair-W (EMA) & 9{,}628{,}081 & 9{,}624{,}241 & 8.933 & 16.97 (5.05) & 18.08 & 1770 & 668 \” | 9628081 | 9628081.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.41` |
| `R1.supp-tab-appexpcost.42` | 9,624,241 — “Fair-W (EMA) & 9{,}628{,}081 & 9{,}624{,}241 & 8.933 & 16.97 (5.05) & 18.08 & 1770 & 668 \” | 9624241 | 9624241.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.42` |
| `R1.supp-tab-appexpcost.43` | 8.933 — “Fair-W (EMA) & 9{,}628{,}081 & 9{,}624{,}241 & 8.933 & 16.97 (5.05) & 18.08 & 1770 & 668 \” | 8.933 | 8.9332 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.43` |
| `R1.supp-tab-appexpcost.44` | 16.97 — “Fair-W (EMA) & 9{,}628{,}081 & 9{,}624{,}241 & 8.933 & 16.97 (5.05) & 18.08 & 1770 & 668 \” | 16.97 | 16.97 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.44` |
| `R1.supp-tab-appexpcost.45` | 5.05 — “Fair-W (EMA) & 9{,}628{,}081 & 9{,}624{,}241 & 8.933 & 16.97 (5.05) & 18.08 & 1770 & 668 \” | 5.05 | 5.0540 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.45` |
| `R1.supp-tab-appexpcost.46` | 18.08 — “Fair-W (EMA) & 9{,}628{,}081 & 9{,}624{,}241 & 8.933 & 16.97 (5.05) & 18.08 & 1770 & 668 \” | 18.08 | 18.08 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.46` |
| `R1.supp-tab-appexpcost.47` | 1770 — “Fair-W (EMA) & 9{,}628{,}081 & 9{,}624{,}241 & 8.933 & 16.97 (5.05) & 18.08 & 1770 & 668 \” | 1770 | 1769.64 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.47` |
| `R1.supp-tab-appexpcost.48` | 668 — “Fair-W (EMA) & 9{,}628{,}081 & 9{,}624{,}241 & 8.933 & 16.97 (5.05) & 18.08 & 1770 & 668 \” | 668 | 667.73 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.48` |
| `R1.supp-tab-appexpcost.49` | 3,677,821 — “TrunkCtrl (raw) & 3{,}677{,}821 & 3{,}677{,}821 & 0.962 & 7.33 (0.56) & 8.35 & 3831 & 497 ” | 3677821 | 3677821.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.49` |
| `R1.supp-tab-appexpcost.50` | 3,677,821 — “TrunkCtrl (raw) & 3{,}677{,}821 & 3{,}677{,}821 & 0.962 & 7.33 (0.56) & 8.35 & 3831 & 497 ” | 3677821 | 3677821.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.50` |
| `R1.supp-tab-appexpcost.51` | 0.962 — “TrunkCtrl (raw) & 3{,}677{,}821 & 3{,}677{,}821 & 0.962 & 7.33 (0.56) & 8.35 & 3831 & 497 ” | 0.962 | 0.9622 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.51` |
| `R1.supp-tab-appexpcost.52` | 7.33 — “TrunkCtrl (raw) & 3{,}677{,}821 & 3{,}677{,}821 & 0.962 & 7.33 (0.56) & 8.35 & 3831 & 497 ” | 7.33 | 7.3276 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.52` |
| `R1.supp-tab-appexpcost.53` | 0.56 — “TrunkCtrl (raw) & 3{,}677{,}821 & 3{,}677{,}821 & 0.962 & 7.33 (0.56) & 8.35 & 3831 & 497 ” | 0.56 | 0.5560 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.53` |
| `R1.supp-tab-appexpcost.54` | 8.35 — “TrunkCtrl (raw) & 3{,}677{,}821 & 3{,}677{,}821 & 0.962 & 7.33 (0.56) & 8.35 & 3831 & 497 ” | 8.35 | 8.3519 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.54` |
| `R1.supp-tab-appexpcost.55` | 3831 — “TrunkCtrl (raw) & 3{,}677{,}821 & 3{,}677{,}821 & 0.962 & 7.33 (0.56) & 8.35 & 3831 & 497 ” | 3831 | 3831.46 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.55` |
| `R1.supp-tab-appexpcost.56` | 497 — “TrunkCtrl (raw) & 3{,}677{,}821 & 3{,}677{,}821 & 0.962 & 7.33 (0.56) & 8.35 & 3831 & 497 ” | 497 | 497.18 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.56` |
| `R1.supp-tab-appexpcost.57` | 4,008,829 — “SpatialBase (raw) & 4{,}008{,}829 & 4{,}008{,}829 & 1.004 & 7.56 (0.40) & 8.34 & 3838 & 56” | 4008829 | 4008829.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.57` |
| `R1.supp-tab-appexpcost.58` | 4,008,829 — “SpatialBase (raw) & 4{,}008{,}829 & 4{,}008{,}829 & 1.004 & 7.56 (0.40) & 8.34 & 3838 & 56” | 4008829 | 4008829.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.58` |
| `R1.supp-tab-appexpcost.59` | 1.004 — “SpatialBase (raw) & 4{,}008{,}829 & 4{,}008{,}829 & 1.004 & 7.56 (0.40) & 8.34 & 3838 & 56” | 1.004 | 1.0041 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.59` |
| `R1.supp-tab-appexpcost.60` | 7.56 — “SpatialBase (raw) & 4{,}008{,}829 & 4{,}008{,}829 & 1.004 & 7.56 (0.40) & 8.34 & 3838 & 56” | 7.56 | 7.5639 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.60` |
| `R1.supp-tab-appexpcost.61` | 0.40 — “SpatialBase (raw) & 4{,}008{,}829 & 4{,}008{,}829 & 1.004 & 7.56 (0.40) & 8.34 & 3838 & 56” | 0.40 | 0.3990 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.61` |
| `R1.supp-tab-appexpcost.62` | 8.34 — “SpatialBase (raw) & 4{,}008{,}829 & 4{,}008{,}829 & 1.004 & 7.56 (0.40) & 8.34 & 3838 & 56” | 8.34 | 8.3370 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.62` |
| `R1.supp-tab-appexpcost.63` | 3838 — “SpatialBase (raw) & 4{,}008{,}829 & 4{,}008{,}829 & 1.004 & 7.56 (0.40) & 8.34 & 3838 & 56” | 3838 | 3838.30 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.63` |
| `R1.supp-tab-appexpcost.64` | 562 — “SpatialBase (raw) & 4{,}008{,}829 & 4{,}008{,}829 & 1.004 & 7.56 (0.40) & 8.34 & 3838 & 56” | 562 | 562.45 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.64` |
| `R1.supp-tab-appexpcost.65` | 20,809,001 — “Xception (raw) & 20{,}809{,}001 & 20{,}809{,}001 & 11.901 & 5.32 (0.59) & 19.42 & 1648 & 1” | 20809001 | 20809001.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.65` |
| `R1.supp-tab-appexpcost.66` | 20,809,001 — “Xception (raw) & 20{,}809{,}001 & 20{,}809{,}001 & 11.901 & 5.32 (0.59) & 19.42 & 1648 & 1” | 20809001 | 20809001.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.66` |
| `R1.supp-tab-appexpcost.67` | 11.901 — “Xception (raw) & 20{,}809{,}001 & 20{,}809{,}001 & 11.901 & 5.32 (0.59) & 19.42 & 1648 & 1” | 11.901 | 11.90 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.67` |
| `R1.supp-tab-appexpcost.68` | 5.32 — “Xception (raw) & 20{,}809{,}001 & 20{,}809{,}001 & 11.901 & 5.32 (0.59) & 19.42 & 1648 & 1” | 5.32 | 5.3216 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.68` |
| `R1.supp-tab-appexpcost.69` | 0.59 — “Xception (raw) & 20{,}809{,}001 & 20{,}809{,}001 & 11.901 & 5.32 (0.59) & 19.42 & 1648 & 1” | 0.59 | 0.5932 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.69` |
| `R1.supp-tab-appexpcost.70` | 19.42 — “Xception (raw) & 20{,}809{,}001 & 20{,}809{,}001 & 11.901 & 5.32 (0.59) & 19.42 & 1648 & 1” | 19.42 | 19.42 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.70` |
| `R1.supp-tab-appexpcost.71` | 1648 — “Xception (raw) & 20{,}809{,}001 & 20{,}809{,}001 & 11.901 & 5.32 (0.59) & 19.42 & 1648 & 1” | 1648 | 1647.90 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.71` |
| `R1.supp-tab-appexpcost.72` | 1001 — “Xception (raw) & 20{,}809{,}001 & 20{,}809{,}001 & 11.901 & 5.32 (0.59) & 19.42 & 1648 & 1” | 1001 | 1001.06 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.72` |
| `R1.supp-tab-appexpcost.73` | 21,007,337 — “F3-Net (raw) & 21{,}007{,}337 & 21{,}007{,}337 & 12.763 & 6.06 (0.28) & 22.02 & 1453 & 107” | 21007337 | 21007337.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.73` |
| `R1.supp-tab-appexpcost.74` | 21,007,337 — “F3-Net (raw) & 21{,}007{,}337 & 21{,}007{,}337 & 12.763 & 6.06 (0.28) & 22.02 & 1453 & 107” | 21007337 | 21007337.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.74` |
| `R1.supp-tab-appexpcost.75` | 12.763 — “F3-Net (raw) & 21{,}007{,}337 & 21{,}007{,}337 & 12.763 & 6.06 (0.28) & 22.02 & 1453 & 107” | 12.763 | 12.76 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.75` |
| `R1.supp-tab-appexpcost.76` | 6.06 — “F3-Net (raw) & 21{,}007{,}337 & 21{,}007{,}337 & 12.763 & 6.06 (0.28) & 22.02 & 1453 & 107” | 6.06 | 6.0618 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.76` |
| `R1.supp-tab-appexpcost.77` | 0.28 — “F3-Net (raw) & 21{,}007{,}337 & 21{,}007{,}337 & 12.763 & 6.06 (0.28) & 22.02 & 1453 & 107” | 0.28 | 0.2822 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.77` |
| `R1.supp-tab-appexpcost.78` | 22.02 — “F3-Net (raw) & 21{,}007{,}337 & 21{,}007{,}337 & 12.763 & 6.06 (0.28) & 22.02 & 1453 & 107” | 22.02 | 22.02 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.78` |
| `R1.supp-tab-appexpcost.79` | 1453 — “F3-Net (raw) & 21{,}007{,}337 & 21{,}007{,}337 & 12.763 & 6.06 (0.28) & 22.02 & 1453 & 107” | 1453 | 1452.91 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.79` |
| `R1.supp-tab-appexpcost.80` | 1075 — “F3-Net (raw) & 21{,}007{,}337 & 21{,}007{,}337 & 12.763 & 6.06 (0.28) & 22.02 & 1453 & 107” | 1075 | 1074.82 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.80` |
| `R1.supp-tab-appexpcost.81` | 5,086,273 — “FreqNet (raw) & 5{,}086{,}273 & 5{,}086{,}273 & 2.959 & 3.47 (0.05) & 16.11 & 1986 & 1471 ” | 5086273 | 5086273.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.81` |
| `R1.supp-tab-appexpcost.82` | 5,086,273 — “FreqNet (raw) & 5{,}086{,}273 & 5{,}086{,}273 & 2.959 & 3.47 (0.05) & 16.11 & 1986 & 1471 ” | 5086273 | 5086273.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.82` |
| `R1.supp-tab-appexpcost.83` | 2.959 — “FreqNet (raw) & 5{,}086{,}273 & 5{,}086{,}273 & 2.959 & 3.47 (0.05) & 16.11 & 1986 & 1471 ” | 2.959 | 2.9591 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.83` |
| `R1.supp-tab-appexpcost.84` | 3.47 — “FreqNet (raw) & 5{,}086{,}273 & 5{,}086{,}273 & 2.959 & 3.47 (0.05) & 16.11 & 1986 & 1471 ” | 3.47 | 3.4688 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.84` |
| `R1.supp-tab-appexpcost.85` | 0.05 — “FreqNet (raw) & 5{,}086{,}273 & 5{,}086{,}273 & 2.959 & 3.47 (0.05) & 16.11 & 1986 & 1471 ” | 0.05 | 0.0542 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.85` |
| `R1.supp-tab-appexpcost.86` | 16.11 — “FreqNet (raw) & 5{,}086{,}273 & 5{,}086{,}273 & 2.959 & 3.47 (0.05) & 16.11 & 1986 & 1471 ” | 16.11 | 16.11 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.86` |
| `R1.supp-tab-appexpcost.87` | 1986 — “FreqNet (raw) & 5{,}086{,}273 & 5{,}086{,}273 & 2.959 & 3.47 (0.05) & 16.11 & 1986 & 1471 ” | 1986 | 1986.46 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.87` |
| `R1.supp-tab-appexpcost.88` | 1471 — “FreqNet (raw) & 5{,}086{,}273 & 5{,}086{,}273 & 2.959 & 3.47 (0.05) & 16.11 & 1986 & 1471 ” | 1471 | 1471.24 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appexpcost.88` |

- `R1.supp-tab-appexpcost.1` — weights: EMA
- `R1.supp-tab-appexpcost.2` — weights: EMA
- `R1.supp-tab-appexpcost.3` — weights: EMA
- `R1.supp-tab-appexpcost.4` — weights: EMA
- `R1.supp-tab-appexpcost.5` — weights: EMA
- `R1.supp-tab-appexpcost.6` — weights: EMA
- `R1.supp-tab-appexpcost.7` — weights: EMA
- `R1.supp-tab-appexpcost.9` — weights: EMA
- `R1.supp-tab-appexpcost.10` — weights: EMA
- `R1.supp-tab-appexpcost.11` — weights: EMA
- `R1.supp-tab-appexpcost.12` — weights: EMA
- `R1.supp-tab-appexpcost.13` — weights: EMA
- `R1.supp-tab-appexpcost.14` — weights: EMA
- `R1.supp-tab-appexpcost.15` — weights: EMA
- `R1.supp-tab-appexpcost.17` — weights: EMA
- `R1.supp-tab-appexpcost.18` — weights: EMA
- `R1.supp-tab-appexpcost.19` — weights: EMA
- `R1.supp-tab-appexpcost.20` — weights: EMA
- `R1.supp-tab-appexpcost.21` — weights: EMA
- `R1.supp-tab-appexpcost.22` — weights: EMA
- `R1.supp-tab-appexpcost.23` — weights: EMA
- `R1.supp-tab-appexpcost.25` — weights: EMA
- `R1.supp-tab-appexpcost.26` — weights: EMA
- `R1.supp-tab-appexpcost.27` — weights: EMA
- `R1.supp-tab-appexpcost.28` — weights: EMA
- `R1.supp-tab-appexpcost.29` — weights: EMA
- `R1.supp-tab-appexpcost.30` — weights: EMA
- `R1.supp-tab-appexpcost.31` — weights: EMA
- `R1.supp-tab-appexpcost.33` — weights: EMA
- `R1.supp-tab-appexpcost.34` — weights: EMA
- `R1.supp-tab-appexpcost.35` — weights: EMA
- `R1.supp-tab-appexpcost.36` — weights: EMA
- `R1.supp-tab-appexpcost.37` — weights: EMA
- `R1.supp-tab-appexpcost.38` — weights: EMA
- `R1.supp-tab-appexpcost.39` — weights: EMA
- `R1.supp-tab-appexpcost.41` — weights: EMA
- `R1.supp-tab-appexpcost.42` — weights: EMA
- `R1.supp-tab-appexpcost.43` — weights: EMA
- `R1.supp-tab-appexpcost.44` — weights: EMA
- `R1.supp-tab-appexpcost.45` — weights: EMA
- `R1.supp-tab-appexpcost.46` — weights: EMA
- `R1.supp-tab-appexpcost.47` — weights: EMA
- `R1.supp-tab-appexpcost.49` — weights: raw
- `R1.supp-tab-appexpcost.50` — weights: raw
- `R1.supp-tab-appexpcost.51` — weights: raw
- `R1.supp-tab-appexpcost.52` — weights: raw
- `R1.supp-tab-appexpcost.53` — weights: raw
- `R1.supp-tab-appexpcost.54` — weights: raw
- `R1.supp-tab-appexpcost.55` — weights: raw
- `R1.supp-tab-appexpcost.57` — weights: raw
- `R1.supp-tab-appexpcost.58` — weights: raw
- `R1.supp-tab-appexpcost.59` — weights: raw
- `R1.supp-tab-appexpcost.60` — weights: raw
- `R1.supp-tab-appexpcost.61` — weights: raw
- `R1.supp-tab-appexpcost.62` — weights: raw
- `R1.supp-tab-appexpcost.63` — weights: raw
- `R1.supp-tab-appexpcost.65` — weights: raw
- `R1.supp-tab-appexpcost.66` — weights: raw
- `R1.supp-tab-appexpcost.67` — weights: raw
- `R1.supp-tab-appexpcost.68` — weights: raw
- `R1.supp-tab-appexpcost.69` — weights: raw
- `R1.supp-tab-appexpcost.70` — weights: raw
- `R1.supp-tab-appexpcost.71` — weights: raw
- `R1.supp-tab-appexpcost.73` — weights: raw
- `R1.supp-tab-appexpcost.74` — weights: raw
- `R1.supp-tab-appexpcost.75` — weights: raw
- `R1.supp-tab-appexpcost.76` — weights: raw
- `R1.supp-tab-appexpcost.77` — weights: raw
- `R1.supp-tab-appexpcost.78` — weights: raw
- `R1.supp-tab-appexpcost.79` — weights: raw
- `R1.supp-tab-appexpcost.81` — weights: raw
- `R1.supp-tab-appexpcost.82` — weights: raw
- `R1.supp-tab-appexpcost.83` — weights: raw
- `R1.supp-tab-appexpcost.84` — weights: raw
- `R1.supp-tab-appexpcost.85` — weights: raw
- `R1.supp-tab-appexpcost.86` — weights: raw
- `R1.supp-tab-appexpcost.87` — weights: raw

## R1.supp-Frequency-path-diagnostics-E11 — Revision 1 — Supplementary Material, §“Frequency-path diagnostics (E11)”

*Supplementary Material, §“Frequency-path diagnostics (E11)”*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-Frequency-path-diagnostics-E11.1` | 0.1109 — “head logit, $\gamma$ Fair-W's learned residual weight, logit $= s + \gamma f$), averaged p” | 0.1109 | 0.1109 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-Frequency-path-diagnostics-E11.1` |
| `R1.supp-Frequency-path-diagnostics-E11.2` | 0.1015 — “head logit, $\gamma$ Fair-W's learned residual weight, logit $= s + \gamma f$), averaged p” | 0.1015 | 0.1015 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-Frequency-path-diagnostics-E11.2` |
| `R1.supp-Frequency-path-diagnostics-E11.3` | 0.1520 — “head logit, $\gamma$ Fair-W's learned residual weight, logit $= s + \gamma f$), averaged p” | 0.1520 | 0.1520 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-Frequency-path-diagnostics-E11.3` |
| `R1.supp-Frequency-path-diagnostics-E11.4` | 0.5867 — “0.5867, 0.1630 and 0.4279; between the head and SpatialBase of the same seed index, they w” | 0.5867 | 0.5867 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-Frequency-path-diagnostics-E11.4` |
| `R1.supp-Frequency-path-diagnostics-E11.5` | 0.1630 — “0.5867, 0.1630 and 0.4279; between the head and SpatialBase of the same seed index, they w” | 0.1630 | 0.1630 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-Frequency-path-diagnostics-E11.5` |
| `R1.supp-Frequency-path-diagnostics-E11.6` | 0.4279 — “0.5867, 0.1630 and 0.4279; between the head and SpatialBase of the same seed index, they w” | 0.4279 | 0.4279 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-Frequency-path-diagnostics-E11.6` |
| `R1.supp-Frequency-path-diagnostics-E11.7` | 0.6024 — “0.6024, 0.2281 and 0.5458. (e, f) Table~ gives the mean band gate at” | 0.6024 | 0.6024 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-Frequency-path-diagnostics-E11.7` |
| `R1.supp-Frequency-path-diagnostics-E11.8` | 0.2281 — “0.6024, 0.2281 and 0.5458. (e, f) Table~ gives the mean band gate at” | 0.2281 | 0.2281 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-Frequency-path-diagnostics-E11.8` |
| `R1.supp-Frequency-path-diagnostics-E11.9` | 0.5458 — “0.6024, 0.2281 and 0.5458. (e, f) Table~ gives the mean band gate at” | 0.5458 | 0.5458 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-Frequency-path-diagnostics-E11.9` |
| `R1.supp-Frequency-path-diagnostics-E11.10` | 25 — “within one bin and of those it did not. Both groups have at least ten videos per class in ” | 25 | 25.00 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-Frequency-path-diagnostics-E11.10` |
| `R1.supp-Frequency-path-diagnostics-E11.11` | 60 — “the 60 run-level cells; in 16 of these 25 the second group's AUC is the lower one. Both ta” | 60 | 60.00 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-Frequency-path-diagnostics-E11.11` |
| `R1.supp-Frequency-path-diagnostics-E11.12` | 16 — “the 60 run-level cells; in 16 of these 25 the second group's AUC is the lower one. Both ta” | 16 | 16.00 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-Frequency-path-diagnostics-E11.12` |

- `R1.supp-Frequency-path-diagnostics-E11.4` — weights: EMA
- `R1.supp-Frequency-path-diagnostics-E11.5` — weights: EMA
- `R1.supp-Frequency-path-diagnostics-E11.6` — weights: EMA
- `R1.supp-Frequency-path-diagnostics-E11.7` — weights: EMA and raw
- `R1.supp-Frequency-path-diagnostics-E11.8` — weights: EMA and raw
- `R1.supp-Frequency-path-diagnostics-E11.9` — weights: EMA and raw

## R1.supp-tab-appexpdiag — Revision 1 — Supplementary Material, tab:appexpdiag

*Supplementary Material, tab:appexpdiag; `\label{tab:appexpdiag}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-tab-appexpdiag.1` | 10,000 — “($B = 10{,}000$; seeds, then 140 source-identity clusters; one bootstrap at” | 10000 | 10000.00 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-tab-appexpdiag.1` |
| `R1.supp-tab-appexpdiag.2` | 96.19 — “Fair-W, full model (selected epoch) & 96.19 \ci{94.74}{97.45} & 97.19 \ci{95.85}{98.26} \\” | 96.19 | 96.19 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.2` |
| `R1.supp-tab-appexpdiag.3` | 94.74 — “Fair-W, full model (selected epoch) & 96.19 \ci{94.74}{97.45} & 97.19 \ci{95.85}{98.26} \\” | 94.74 | 94.74 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.3` |
| `R1.supp-tab-appexpdiag.4` | 97.45 — “Fair-W, full model (selected epoch) & 96.19 \ci{94.74}{97.45} & 97.19 \ci{95.85}{98.26} \\” | 97.45 | 97.45 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.4` |
| `R1.supp-tab-appexpdiag.5` | 97.19 — “Fair-W, full model (selected epoch) & 96.19 \ci{94.74}{97.45} & 97.19 \ci{95.85}{98.26} \\” | 97.19 | 97.19 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.5` |
| `R1.supp-tab-appexpdiag.6` | 95.85 — “Fair-W, full model (selected epoch) & 96.19 \ci{94.74}{97.45} & 97.19 \ci{95.85}{98.26} \\” | 95.85 | 95.85 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.6` |
| `R1.supp-tab-appexpdiag.7` | 98.26 — “Fair-W, full model (selected epoch) & 96.19 \ci{94.74}{97.45} & 97.19 \ci{95.85}{98.26} \\” | 98.26 | 98.26 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.7` |
| `R1.supp-tab-appexpdiag.8` | 85.27 — “Fair-W frequency head alone (selected epoch) & 85.27 \ci{81.34}{88.97} & 90.08 \ci{87.22}{” | 85.27 | 85.27 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.8` |
| `R1.supp-tab-appexpdiag.9` | 81.34 — “Fair-W frequency head alone (selected epoch) & 85.27 \ci{81.34}{88.97} & 90.08 \ci{87.22}{” | 81.34 | 81.34 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.9` |
| `R1.supp-tab-appexpdiag.10` | 88.97 — “Fair-W frequency head alone (selected epoch) & 85.27 \ci{81.34}{88.97} & 90.08 \ci{87.22}{” | 88.97 | 88.97 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.10` |
| `R1.supp-tab-appexpdiag.11` | 90.08 — “Fair-W frequency head alone (selected epoch) & 85.27 \ci{81.34}{88.97} & 90.08 \ci{87.22}{” | 90.08 | 90.08 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.11` |
| `R1.supp-tab-appexpdiag.12` | 87.22 — “Fair-W frequency head alone (selected epoch) & 85.27 \ci{81.34}{88.97} & 90.08 \ci{87.22}{” | 87.22 | 87.22 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.12` |
| `R1.supp-tab-appexpdiag.13` | 92.71 — “Fair-W frequency head alone (selected epoch) & 85.27 \ci{81.34}{88.97} & 90.08 \ci{87.22}{” | 92.71 | 92.71 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.13` |
| `R1.supp-tab-appexpdiag.14` | -10.92 — “head alone $-$ full model (selected epoch) & $-10.92$ \ci{-14.41}{-7.65} & $-7.11$ \ci{-9.” | -10.92 | -10.92 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.14` |
| `R1.supp-tab-appexpdiag.15` | -14.41 — “head alone $-$ full model (selected epoch) & $-10.92$ \ci{-14.41}{-7.65} & $-7.11$ \ci{-9.” | -14.41 | -14.41 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.15` |
| `R1.supp-tab-appexpdiag.16` | -7.65 — “head alone $-$ full model (selected epoch) & $-10.92$ \ci{-14.41}{-7.65} & $-7.11$ \ci{-9.” | -7.65 | -7.6498 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.16` |
| `R1.supp-tab-appexpdiag.17` | -7.11 — “head alone $-$ full model (selected epoch) & $-10.92$ \ci{-14.41}{-7.65} & $-7.11$ \ci{-9.” | -7.11 | -7.1110 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.17` |
| `R1.supp-tab-appexpdiag.18` | -9.50 — “head alone $-$ full model (selected epoch) & $-10.92$ \ci{-14.41}{-7.65} & $-7.11$ \ci{-9.” | -9.50 | -9.5030 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.18` |
| `R1.supp-tab-appexpdiag.19` | -4.96 — “head alone $-$ full model (selected epoch) & $-10.92$ \ci{-14.41}{-7.65} & $-7.11$ \ci{-9.” | -4.96 | -4.9607 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.19` |
| `R1.supp-tab-appexpdiag.20` | 94.66 — “Fair-W, full model (epoch 30) & 94.66 \ci{92.62}{96.46} & 96.19 \ci{94.59}{97.54} \\” | 94.66 | 94.66 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.20` |
| `R1.supp-tab-appexpdiag.21` | 92.62 — “Fair-W, full model (epoch 30) & 94.66 \ci{92.62}{96.46} & 96.19 \ci{94.59}{97.54} \\” | 92.62 | 92.62 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.21` |
| `R1.supp-tab-appexpdiag.22` | 96.46 — “Fair-W, full model (epoch 30) & 94.66 \ci{92.62}{96.46} & 96.19 \ci{94.59}{97.54} \\” | 96.46 | 96.46 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.22` |
| `R1.supp-tab-appexpdiag.23` | 96.19 — “Fair-W, full model (epoch 30) & 94.66 \ci{92.62}{96.46} & 96.19 \ci{94.59}{97.54} \\” | 96.19 | 96.19 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.23` |
| `R1.supp-tab-appexpdiag.24` | 94.59 — “Fair-W, full model (epoch 30) & 94.66 \ci{92.62}{96.46} & 96.19 \ci{94.59}{97.54} \\” | 94.59 | 94.59 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.24` |
| `R1.supp-tab-appexpdiag.25` | 97.54 — “Fair-W, full model (epoch 30) & 94.66 \ci{92.62}{96.46} & 96.19 \ci{94.59}{97.54} \\” | 97.54 | 97.54 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.25` |
| `R1.supp-tab-appexpdiag.26` | 89.99 — “Fair-W frequency head alone (epoch 30) & 89.99 \ci{86.94}{92.83} & 93.37 \ci{90.96}{95.55}” | 89.99 | 89.99 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.26` |
| `R1.supp-tab-appexpdiag.27` | 86.94 — “Fair-W frequency head alone (epoch 30) & 89.99 \ci{86.94}{92.83} & 93.37 \ci{90.96}{95.55}” | 86.94 | 86.94 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.27` |
| `R1.supp-tab-appexpdiag.28` | 92.83 — “Fair-W frequency head alone (epoch 30) & 89.99 \ci{86.94}{92.83} & 93.37 \ci{90.96}{95.55}” | 92.83 | 92.83 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.28` |
| `R1.supp-tab-appexpdiag.29` | 93.37 — “Fair-W frequency head alone (epoch 30) & 89.99 \ci{86.94}{92.83} & 93.37 \ci{90.96}{95.55}” | 93.37 | 93.37 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.29` |
| `R1.supp-tab-appexpdiag.30` | 90.96 — “Fair-W frequency head alone (epoch 30) & 89.99 \ci{86.94}{92.83} & 93.37 \ci{90.96}{95.55}” | 90.96 | 90.96 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.30` |
| `R1.supp-tab-appexpdiag.31` | 95.55 — “Fair-W frequency head alone (epoch 30) & 89.99 \ci{86.94}{92.83} & 93.37 \ci{90.96}{95.55}” | 95.55 | 95.55 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.31` |
| `R1.supp-tab-appexpdiag.32` | -4.68 — “head alone $-$ full model (epoch 30) & $-4.68$ \ci{-7.16}{-2.37} & $-2.82$ \ci{-4.69}{-1.1” | -4.68 | -4.6764 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.32` |
| `R1.supp-tab-appexpdiag.33` | -7.16 — “head alone $-$ full model (epoch 30) & $-4.68$ \ci{-7.16}{-2.37} & $-2.82$ \ci{-4.69}{-1.1” | -7.16 | -7.1612 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.33` |
| `R1.supp-tab-appexpdiag.34` | -2.37 — “head alone $-$ full model (epoch 30) & $-4.68$ \ci{-7.16}{-2.37} & $-2.82$ \ci{-4.69}{-1.1” | -2.37 | -2.3720 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.34` |
| `R1.supp-tab-appexpdiag.35` | -2.82 — “head alone $-$ full model (epoch 30) & $-4.68$ \ci{-7.16}{-2.37} & $-2.82$ \ci{-4.69}{-1.1” | -2.82 | -2.8178 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.35` |
| `R1.supp-tab-appexpdiag.36` | -4.69 — “head alone $-$ full model (epoch 30) & $-4.68$ \ci{-7.16}{-2.37} & $-2.82$ \ci{-4.69}{-1.1” | -4.69 | -4.6862 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.36` |
| `R1.supp-tab-appexpdiag.37` | -1.14 — “head alone $-$ full model (epoch 30) & $-4.68$ \ci{-7.16}{-2.37} & $-2.82$ \ci{-4.69}{-1.1” | -1.14 | -1.1403 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.37` |
| `R1.supp-tab-appexpdiag.38` | 95.21 — “Fair-W spatial part $+$ head & 95.21 \ci{93.27}{96.87} & 96.51 \ci{94.86}{97.90} \\” | 95.21 | 95.21 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.38` |
| `R1.supp-tab-appexpdiag.39` | 93.27 — “Fair-W spatial part $+$ head & 95.21 \ci{93.27}{96.87} & 96.51 \ci{94.86}{97.90} \\” | 93.27 | 93.27 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.39` |
| `R1.supp-tab-appexpdiag.40` | 96.87 — “Fair-W spatial part $+$ head & 95.21 \ci{93.27}{96.87} & 96.51 \ci{94.86}{97.90} \\” | 96.87 | 96.87 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.40` |
| `R1.supp-tab-appexpdiag.41` | 96.51 — “Fair-W spatial part $+$ head & 95.21 \ci{93.27}{96.87} & 96.51 \ci{94.86}{97.90} \\” | 96.51 | 96.51 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.41` |
| `R1.supp-tab-appexpdiag.42` | 94.86 — “Fair-W spatial part $+$ head & 95.21 \ci{93.27}{96.87} & 96.51 \ci{94.86}{97.90} \\” | 94.86 | 94.86 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.42` |
| `R1.supp-tab-appexpdiag.43` | 97.90 — “Fair-W spatial part $+$ head & 95.21 \ci{93.27}{96.87} & 96.51 \ci{94.86}{97.90} \\” | 97.90 | 97.90 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.43` |
| `R1.supp-tab-appexpdiag.44` | 95.66 — “SpatialBase $+$ Fair-W head & 95.66 \ci{94.10}{97.02} & 96.92 \ci{95.62}{97.99} \\” | 95.66 | 95.66 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.44` |
| `R1.supp-tab-appexpdiag.45` | 94.10 — “SpatialBase $+$ Fair-W head & 95.66 \ci{94.10}{97.02} & 96.92 \ci{95.62}{97.99} \\” | 94.10 | 94.10 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.45` |
| `R1.supp-tab-appexpdiag.46` | 97.02 — “SpatialBase $+$ Fair-W head & 95.66 \ci{94.10}{97.02} & 96.92 \ci{95.62}{97.99} \\” | 97.02 | 97.02 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.46` |
| `R1.supp-tab-appexpdiag.47` | 96.92 — “SpatialBase $+$ Fair-W head & 95.66 \ci{94.10}{97.02} & 96.92 \ci{95.62}{97.99} \\” | 96.92 | 96.92 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.47` |
| `R1.supp-tab-appexpdiag.48` | 95.62 — “SpatialBase $+$ Fair-W head & 95.66 \ci{94.10}{97.02} & 96.92 \ci{95.62}{97.99} \\” | 95.62 | 95.62 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.48` |
| `R1.supp-tab-appexpdiag.49` | 97.99 — “SpatialBase $+$ Fair-W head & 95.66 \ci{94.10}{97.02} & 96.92 \ci{95.62}{97.99} \\” | 97.99 | 97.99 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.49` |
| `R1.supp-tab-appexpdiag.50` | -0.98 — “Fair-W spatial part $+$ head $-$ Fair-W & $-0.98$ \ci{-2.10}{-0.06} & $-0.68$ \ci{-1.54}{-” | -0.98 | -0.9792 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.50` |
| `R1.supp-tab-appexpdiag.51` | -2.10 — “Fair-W spatial part $+$ head $-$ Fair-W & $-0.98$ \ci{-2.10}{-0.06} & $-0.68$ \ci{-1.54}{-” | -2.10 | -2.0991 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.51` |
| `R1.supp-tab-appexpdiag.52` | -0.06 — “Fair-W spatial part $+$ head $-$ Fair-W & $-0.98$ \ci{-2.10}{-0.06} & $-0.68$ \ci{-1.54}{-” | -0.06 | -0.0599 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.52` |
| `R1.supp-tab-appexpdiag.53` | -0.68 — “Fair-W spatial part $+$ head $-$ Fair-W & $-0.98$ \ci{-2.10}{-0.06} & $-0.68$ \ci{-1.54}{-” | -0.68 | -0.6827 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.53` |
| `R1.supp-tab-appexpdiag.54` | -1.54 — “Fair-W spatial part $+$ head $-$ Fair-W & $-0.98$ \ci{-2.10}{-0.06} & $-0.68$ \ci{-1.54}{-” | -1.54 | -1.5431 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.54` |
| `R1.supp-tab-appexpdiag.55` | -0.02 — “Fair-W spatial part $+$ head $-$ Fair-W & $-0.98$ \ci{-2.10}{-0.06} & $-0.68$ \ci{-1.54}{-” | -0.02 | -0.0177 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.55` |
| `R1.supp-tab-appexpdiag.56` | -0.45 — “Fair-W spatial part $+$ head $-$ SpatialBase & $-0.45$ \ci{-1.89}{0.93} & $-0.37$ \ci{-1.6” | -0.45 | -0.4452 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.56` |
| `R1.supp-tab-appexpdiag.57` | -1.89 — “Fair-W spatial part $+$ head $-$ SpatialBase & $-0.45$ \ci{-1.89}{0.93} & $-0.37$ \ci{-1.6” | -1.89 | -1.8857 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.57` |
| `R1.supp-tab-appexpdiag.58` | 0.93 — “Fair-W spatial part $+$ head $-$ SpatialBase & $-0.45$ \ci{-1.89}{0.93} & $-0.37$ \ci{-1.6” | 0.93 | 0.9324 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.58` |
| `R1.supp-tab-appexpdiag.59` | -0.37 — “Fair-W spatial part $+$ head $-$ SpatialBase & $-0.45$ \ci{-1.89}{0.93} & $-0.37$ \ci{-1.6” | -0.37 | -0.3732 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.59` |
| `R1.supp-tab-appexpdiag.60` | -1.60 — “Fair-W spatial part $+$ head $-$ SpatialBase & $-0.45$ \ci{-1.89}{0.93} & $-0.37$ \ci{-1.6” | -1.60 | -1.6048 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.60` |
| `R1.supp-tab-appexpdiag.61` | 0.68 — “Fair-W spatial part $+$ head $-$ SpatialBase & $-0.45$ \ci{-1.89}{0.93} & $-0.37$ \ci{-1.6” | 0.68 | 0.6818 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.61` |
| `R1.supp-tab-appexpdiag.62` | -0.53 — “SpatialBase $+$ Fair-W head $-$ Fair-W & $-0.53$ \ci{-1.49}{0.31} & $-0.27$ \ci{-1.07}{0.4” | -0.53 | -0.5289 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.62` |
| `R1.supp-tab-appexpdiag.63` | -1.49 — “SpatialBase $+$ Fair-W head $-$ Fair-W & $-0.53$ \ci{-1.49}{0.31} & $-0.27$ \ci{-1.07}{0.4” | -1.49 | -1.4949 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.63` |
| `R1.supp-tab-appexpdiag.64` | 0.31 — “SpatialBase $+$ Fair-W head $-$ Fair-W & $-0.53$ \ci{-1.49}{0.31} & $-0.27$ \ci{-1.07}{0.4” | 0.31 | 0.3108 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.64` |
| `R1.supp-tab-appexpdiag.65` | -0.27 — “SpatialBase $+$ Fair-W head $-$ Fair-W & $-0.53$ \ci{-1.49}{0.31} & $-0.27$ \ci{-1.07}{0.4” | -0.27 | -0.2732 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.65` |
| `R1.supp-tab-appexpdiag.66` | -1.07 — “SpatialBase $+$ Fair-W head $-$ Fair-W & $-0.53$ \ci{-1.49}{0.31} & $-0.27$ \ci{-1.07}{0.4” | -1.07 | -1.0727 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.66` |
| `R1.supp-tab-appexpdiag.67` | 0.48 — “SpatialBase $+$ Fair-W head $-$ Fair-W & $-0.53$ \ci{-1.49}{0.31} & $-0.27$ \ci{-1.07}{0.4” | 0.48 | 0.4813 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.67` |
| `R1.supp-tab-appexpdiag.68` | 0.01 — “SpatialBase $+$ Fair-W head $-$ SpatialBase & 0.01 \ci{-0.99}{1.02} & 0.04 \ci{-0.71}{0.77” | 0.01 | 0.0051 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.68` |
| `R1.supp-tab-appexpdiag.69` | -0.99 — “SpatialBase $+$ Fair-W head $-$ SpatialBase & 0.01 \ci{-0.99}{1.02} & 0.04 \ci{-0.71}{0.77” | -0.99 | -0.9911 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.69` |
| `R1.supp-tab-appexpdiag.70` | 1.02 — “SpatialBase $+$ Fair-W head $-$ SpatialBase & 0.01 \ci{-0.99}{1.02} & 0.04 \ci{-0.71}{0.77” | 1.02 | 1.0209 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.70` |
| `R1.supp-tab-appexpdiag.71` | 0.04 — “SpatialBase $+$ Fair-W head $-$ SpatialBase & 0.01 \ci{-0.99}{1.02} & 0.04 \ci{-0.71}{0.77” | 0.04 | 0.0364 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.71` |
| `R1.supp-tab-appexpdiag.72` | -0.71 — “SpatialBase $+$ Fair-W head $-$ SpatialBase & 0.01 \ci{-0.99}{1.02} & 0.04 \ci{-0.71}{0.77” | -0.71 | -0.7105 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.72` |
| `R1.supp-tab-appexpdiag.73` | 0.77 — “SpatialBase $+$ Fair-W head $-$ SpatialBase & 0.01 \ci{-0.99}{1.02} & 0.04 \ci{-0.71}{0.77” | 0.77 | 0.7695 | `revision-1/exploratory/e11.json` | `python verify/claim.py R1.supp-tab-appexpdiag.73` |

- `R1.supp-tab-appexpdiag.2` — weights: EMA
- `R1.supp-tab-appexpdiag.3` — weights: EMA
- `R1.supp-tab-appexpdiag.4` — weights: EMA
- `R1.supp-tab-appexpdiag.5` — weights: EMA
- `R1.supp-tab-appexpdiag.6` — weights: EMA
- `R1.supp-tab-appexpdiag.7` — weights: EMA
- `R1.supp-tab-appexpdiag.9` — weights: EMA
- `R1.supp-tab-appexpdiag.10` — weights: EMA
- `R1.supp-tab-appexpdiag.11` — weights: EMA
- `R1.supp-tab-appexpdiag.12` — weights: EMA
- `R1.supp-tab-appexpdiag.13` — weights: EMA
- `R1.supp-tab-appexpdiag.14` — weights: EMA
- `R1.supp-tab-appexpdiag.15` — weights: EMA
- `R1.supp-tab-appexpdiag.16` — weights: EMA
- `R1.supp-tab-appexpdiag.17` — weights: EMA
- `R1.supp-tab-appexpdiag.18` — weights: EMA
- `R1.supp-tab-appexpdiag.19` — weights: EMA
- `R1.supp-tab-appexpdiag.20` — weights: EMA
- `R1.supp-tab-appexpdiag.21` — weights: EMA
- `R1.supp-tab-appexpdiag.22` — weights: EMA
- `R1.supp-tab-appexpdiag.23` — weights: EMA
- `R1.supp-tab-appexpdiag.24` — weights: EMA
- `R1.supp-tab-appexpdiag.25` — weights: EMA
- `R1.supp-tab-appexpdiag.27` — weights: EMA
- `R1.supp-tab-appexpdiag.28` — weights: EMA
- `R1.supp-tab-appexpdiag.29` — weights: EMA
- `R1.supp-tab-appexpdiag.30` — weights: EMA
- `R1.supp-tab-appexpdiag.31` — weights: EMA
- `R1.supp-tab-appexpdiag.32` — weights: EMA
- `R1.supp-tab-appexpdiag.33` — weights: EMA
- `R1.supp-tab-appexpdiag.34` — weights: EMA
- `R1.supp-tab-appexpdiag.35` — weights: EMA
- `R1.supp-tab-appexpdiag.36` — weights: EMA
- `R1.supp-tab-appexpdiag.37` — weights: EMA
- `R1.supp-tab-appexpdiag.38` — weights: EMA
- `R1.supp-tab-appexpdiag.39` — weights: EMA
- `R1.supp-tab-appexpdiag.40` — weights: EMA
- `R1.supp-tab-appexpdiag.41` — weights: EMA
- `R1.supp-tab-appexpdiag.42` — weights: EMA
- `R1.supp-tab-appexpdiag.43` — weights: EMA
- `R1.supp-tab-appexpdiag.44` — weights: raw and EMA
- `R1.supp-tab-appexpdiag.45` — weights: raw and EMA
- `R1.supp-tab-appexpdiag.46` — weights: raw and EMA
- `R1.supp-tab-appexpdiag.47` — weights: raw and EMA
- `R1.supp-tab-appexpdiag.48` — weights: raw and EMA
- `R1.supp-tab-appexpdiag.49` — weights: raw and EMA
- `R1.supp-tab-appexpdiag.50` — weights: EMA
- `R1.supp-tab-appexpdiag.51` — weights: EMA
- `R1.supp-tab-appexpdiag.52` — weights: EMA
- `R1.supp-tab-appexpdiag.53` — weights: EMA
- `R1.supp-tab-appexpdiag.54` — weights: EMA
- `R1.supp-tab-appexpdiag.55` — weights: EMA
- `R1.supp-tab-appexpdiag.56` — weights: EMA and raw
- `R1.supp-tab-appexpdiag.57` — weights: EMA and raw
- `R1.supp-tab-appexpdiag.58` — weights: EMA and raw
- `R1.supp-tab-appexpdiag.59` — weights: EMA and raw
- `R1.supp-tab-appexpdiag.60` — weights: EMA and raw
- `R1.supp-tab-appexpdiag.61` — weights: EMA and raw
- `R1.supp-tab-appexpdiag.62` — weights: raw and EMA
- `R1.supp-tab-appexpdiag.63` — weights: raw and EMA
- `R1.supp-tab-appexpdiag.64` — weights: raw and EMA
- `R1.supp-tab-appexpdiag.65` — weights: raw and EMA
- `R1.supp-tab-appexpdiag.66` — weights: raw and EMA
- `R1.supp-tab-appexpdiag.67` — weights: raw and EMA
- `R1.supp-tab-appexpdiag.68` — weights: raw and EMA
- `R1.supp-tab-appexpdiag.69` — weights: raw and EMA
- `R1.supp-tab-appexpdiag.70` — weights: raw and EMA
- `R1.supp-tab-appexpdiag.71` — weights: raw and EMA
- `R1.supp-tab-appexpdiag.72` — weights: raw and EMA
- `R1.supp-tab-appexpdiag.73` — weights: raw and EMA

## R1.supp-tab-appexpbandgate — Revision 1 — Supplementary Material, tab:appexpbandgate

*Supplementary Material, tab:appexpbandgate; `\label{tab:appexpbandgate}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-tab-appexpbandgate.1` | 1.90 — “c0 & (1.90, 1.26, 2.06, 2.11) & (2.21, 1.55, 4.97, 9.70) & (0.68, 1.24, 2.24, 1.09) & (0.8” | 1.90 | 1.9011 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.1` |
| `R1.supp-tab-appexpbandgate.2` | 1.26 — “c0 & (1.90, 1.26, 2.06, 2.11) & (2.21, 1.55, 4.97, 9.70) & (0.68, 1.24, 2.24, 1.09) & (0.8” | 1.26 | 1.2640 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.2` |
| `R1.supp-tab-appexpbandgate.3` | 2.06 — “c0 & (1.90, 1.26, 2.06, 2.11) & (2.21, 1.55, 4.97, 9.70) & (0.68, 1.24, 2.24, 1.09) & (0.8” | 2.06 | 2.0619 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.3` |
| `R1.supp-tab-appexpbandgate.4` | 2.11 — “c0 & (1.90, 1.26, 2.06, 2.11) & (2.21, 1.55, 4.97, 9.70) & (0.68, 1.24, 2.24, 1.09) & (0.8” | 2.11 | 2.1066 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.4` |
| `R1.supp-tab-appexpbandgate.5` | 2.21 — “c0 & (1.90, 1.26, 2.06, 2.11) & (2.21, 1.55, 4.97, 9.70) & (0.68, 1.24, 2.24, 1.09) & (0.8” | 2.21 | 2.2132 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.5` |
| `R1.supp-tab-appexpbandgate.6` | 1.55 — “c0 & (1.90, 1.26, 2.06, 2.11) & (2.21, 1.55, 4.97, 9.70) & (0.68, 1.24, 2.24, 1.09) & (0.8” | 1.55 | 1.5468 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.6` |
| `R1.supp-tab-appexpbandgate.7` | 4.97 — “c0 & (1.90, 1.26, 2.06, 2.11) & (2.21, 1.55, 4.97, 9.70) & (0.68, 1.24, 2.24, 1.09) & (0.8” | 4.97 | 4.9721 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.7` |
| `R1.supp-tab-appexpbandgate.8` | 9.70 — “c0 & (1.90, 1.26, 2.06, 2.11) & (2.21, 1.55, 4.97, 9.70) & (0.68, 1.24, 2.24, 1.09) & (0.8” | 9.70 | 9.6964 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.8` |
| `R1.supp-tab-appexpbandgate.9` | 0.68 — “c0 & (1.90, 1.26, 2.06, 2.11) & (2.21, 1.55, 4.97, 9.70) & (0.68, 1.24, 2.24, 1.09) & (0.8” | 0.68 | 0.6827 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.9` |
| `R1.supp-tab-appexpbandgate.10` | 1.24 — “c0 & (1.90, 1.26, 2.06, 2.11) & (2.21, 1.55, 4.97, 9.70) & (0.68, 1.24, 2.24, 1.09) & (0.8” | 1.24 | 1.2402 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.10` |
| `R1.supp-tab-appexpbandgate.11` | 2.24 — “c0 & (1.90, 1.26, 2.06, 2.11) & (2.21, 1.55, 4.97, 9.70) & (0.68, 1.24, 2.24, 1.09) & (0.8” | 2.24 | 2.2355 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.11` |
| `R1.supp-tab-appexpbandgate.12` | 1.09 — “c0 & (1.90, 1.26, 2.06, 2.11) & (2.21, 1.55, 4.97, 9.70) & (0.68, 1.24, 2.24, 1.09) & (0.8” | 1.09 | 1.0947 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.12` |
| `R1.supp-tab-appexpbandgate.13` | 0.82 — “c0 & (1.90, 1.26, 2.06, 2.11) & (2.21, 1.55, 4.97, 9.70) & (0.68, 1.24, 2.24, 1.09) & (0.8” | 0.82 | 0.8163 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.13` |
| `R1.supp-tab-appexpbandgate.14` | 0.89 — “c0 & (1.90, 1.26, 2.06, 2.11) & (2.21, 1.55, 4.97, 9.70) & (0.68, 1.24, 2.24, 1.09) & (0.8” | 0.89 | 0.8935 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.14` |
| `R1.supp-tab-appexpbandgate.15` | 1.10 — “c0 & (1.90, 1.26, 2.06, 2.11) & (2.21, 1.55, 4.97, 9.70) & (0.68, 1.24, 2.24, 1.09) & (0.8” | 1.10 | 1.0986 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.15` |
| `R1.supp-tab-appexpbandgate.16` | 0.25 — “c0 & (1.90, 1.26, 2.06, 2.11) & (2.21, 1.55, 4.97, 9.70) & (0.68, 1.24, 2.24, 1.09) & (0.8” | 0.25 | 0.2529 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.16` |
| `R1.supp-tab-appexpbandgate.17` | 1.06 — “c18 & (1.06, 2.83, 1.95, 1.75) & (2.40, 3.20, 7.25, 14.40) & (0.84, 1.55, 3.11, 1.23) & (0” | 1.06 | 1.0554 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.17` |
| `R1.supp-tab-appexpbandgate.18` | 2.83 — “c18 & (1.06, 2.83, 1.95, 1.75) & (2.40, 3.20, 7.25, 14.40) & (0.84, 1.55, 3.11, 1.23) & (0” | 2.83 | 2.8346 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.18` |
| `R1.supp-tab-appexpbandgate.19` | 1.95 — “c18 & (1.06, 2.83, 1.95, 1.75) & (2.40, 3.20, 7.25, 14.40) & (0.84, 1.55, 3.11, 1.23) & (0” | 1.95 | 1.9532 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.19` |
| `R1.supp-tab-appexpbandgate.20` | 1.75 — “c18 & (1.06, 2.83, 1.95, 1.75) & (2.40, 3.20, 7.25, 14.40) & (0.84, 1.55, 3.11, 1.23) & (0” | 1.75 | 1.7527 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.20` |
| `R1.supp-tab-appexpbandgate.21` | 2.40 — “c18 & (1.06, 2.83, 1.95, 1.75) & (2.40, 3.20, 7.25, 14.40) & (0.84, 1.55, 3.11, 1.23) & (0” | 2.40 | 2.4033 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.21` |
| `R1.supp-tab-appexpbandgate.22` | 3.20 — “c18 & (1.06, 2.83, 1.95, 1.75) & (2.40, 3.20, 7.25, 14.40) & (0.84, 1.55, 3.11, 1.23) & (0” | 3.20 | 3.2033 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.22` |
| `R1.supp-tab-appexpbandgate.23` | 7.25 — “c18 & (1.06, 2.83, 1.95, 1.75) & (2.40, 3.20, 7.25, 14.40) & (0.84, 1.55, 3.11, 1.23) & (0” | 7.25 | 7.2540 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.23` |
| `R1.supp-tab-appexpbandgate.24` | 14.40 — “c18 & (1.06, 2.83, 1.95, 1.75) & (2.40, 3.20, 7.25, 14.40) & (0.84, 1.55, 3.11, 1.23) & (0” | 14.40 | 14.40 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.24` |
| `R1.supp-tab-appexpbandgate.25` | 0.84 — “c18 & (1.06, 2.83, 1.95, 1.75) & (2.40, 3.20, 7.25, 14.40) & (0.84, 1.55, 3.11, 1.23) & (0” | 0.84 | 0.8422 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.25` |
| `R1.supp-tab-appexpbandgate.26` | 1.55 — “c18 & (1.06, 2.83, 1.95, 1.75) & (2.40, 3.20, 7.25, 14.40) & (0.84, 1.55, 3.11, 1.23) & (0” | 1.55 | 1.5510 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.26` |
| `R1.supp-tab-appexpbandgate.27` | 3.11 — “c18 & (1.06, 2.83, 1.95, 1.75) & (2.40, 3.20, 7.25, 14.40) & (0.84, 1.55, 3.11, 1.23) & (0” | 3.11 | 3.1117 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.27` |
| `R1.supp-tab-appexpbandgate.28` | 1.23 — “c18 & (1.06, 2.83, 1.95, 1.75) & (2.40, 3.20, 7.25, 14.40) & (0.84, 1.55, 3.11, 1.23) & (0” | 1.23 | 1.2319 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.28` |
| `R1.supp-tab-appexpbandgate.29` | 0.82 — “c18 & (1.06, 2.83, 1.95, 1.75) & (2.40, 3.20, 7.25, 14.40) & (0.84, 1.55, 3.11, 1.23) & (0” | 0.82 | 0.8186 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.29` |
| `R1.supp-tab-appexpbandgate.30` | 0.89 — “c18 & (1.06, 2.83, 1.95, 1.75) & (2.40, 3.20, 7.25, 14.40) & (0.84, 1.55, 3.11, 1.23) & (0” | 0.89 | 0.8936 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.30` |
| `R1.supp-tab-appexpbandgate.31` | 1.10 — “c18 & (1.06, 2.83, 1.95, 1.75) & (2.40, 3.20, 7.25, 14.40) & (0.84, 1.55, 3.11, 1.23) & (0” | 1.10 | 1.0984 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.31` |
| `R1.supp-tab-appexpbandgate.32` | 0.26 — “c18 & (1.06, 2.83, 1.95, 1.75) & (2.40, 3.20, 7.25, 14.40) & (0.84, 1.55, 3.11, 1.23) & (0” | 0.26 | 0.2553 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.32` |
| `R1.supp-tab-appexpbandgate.33` | 1.63 — “c23 & (1.63, 0.51, 1.92, 2.43) & (2.83, 2.23, 6.42, 13.40) & (0.46, 1.13, 1.99, 1.26) & (0” | 1.63 | 1.6288 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.33` |
| `R1.supp-tab-appexpbandgate.34` | 0.51 — “c23 & (1.63, 0.51, 1.92, 2.43) & (2.83, 2.23, 6.42, 13.40) & (0.46, 1.13, 1.99, 1.26) & (0” | 0.51 | 0.5082 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.34` |
| `R1.supp-tab-appexpbandgate.35` | 1.92 — “c23 & (1.63, 0.51, 1.92, 2.43) & (2.83, 2.23, 6.42, 13.40) & (0.46, 1.13, 1.99, 1.26) & (0” | 1.92 | 1.9171 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.35` |
| `R1.supp-tab-appexpbandgate.36` | 2.43 — “c23 & (1.63, 0.51, 1.92, 2.43) & (2.83, 2.23, 6.42, 13.40) & (0.46, 1.13, 1.99, 1.26) & (0” | 2.43 | 2.4313 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.36` |
| `R1.supp-tab-appexpbandgate.37` | 2.83 — “c23 & (1.63, 0.51, 1.92, 2.43) & (2.83, 2.23, 6.42, 13.40) & (0.46, 1.13, 1.99, 1.26) & (0” | 2.83 | 2.8317 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.37` |
| `R1.supp-tab-appexpbandgate.38` | 2.23 — “c23 & (1.63, 0.51, 1.92, 2.43) & (2.83, 2.23, 6.42, 13.40) & (0.46, 1.13, 1.99, 1.26) & (0” | 2.23 | 2.2280 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.38` |
| `R1.supp-tab-appexpbandgate.39` | 6.42 — “c23 & (1.63, 0.51, 1.92, 2.43) & (2.83, 2.23, 6.42, 13.40) & (0.46, 1.13, 1.99, 1.26) & (0” | 6.42 | 6.4157 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.39` |
| `R1.supp-tab-appexpbandgate.40` | 13.40 — “c23 & (1.63, 0.51, 1.92, 2.43) & (2.83, 2.23, 6.42, 13.40) & (0.46, 1.13, 1.99, 1.26) & (0” | 13.40 | 13.40 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.40` |
| `R1.supp-tab-appexpbandgate.41` | 0.46 — “c23 & (1.63, 0.51, 1.92, 2.43) & (2.83, 2.23, 6.42, 13.40) & (0.46, 1.13, 1.99, 1.26) & (0” | 0.46 | 0.4585 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.41` |
| `R1.supp-tab-appexpbandgate.42` | 1.13 — “c23 & (1.63, 0.51, 1.92, 2.43) & (2.83, 2.23, 6.42, 13.40) & (0.46, 1.13, 1.99, 1.26) & (0” | 1.13 | 1.1308 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.42` |
| `R1.supp-tab-appexpbandgate.43` | 1.99 — “c23 & (1.63, 0.51, 1.92, 2.43) & (2.83, 2.23, 6.42, 13.40) & (0.46, 1.13, 1.99, 1.26) & (0” | 1.99 | 1.9948 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.43` |
| `R1.supp-tab-appexpbandgate.44` | 1.26 — “c23 & (1.63, 0.51, 1.92, 2.43) & (2.83, 2.23, 6.42, 13.40) & (0.46, 1.13, 1.99, 1.26) & (0” | 1.26 | 1.2585 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.44` |
| `R1.supp-tab-appexpbandgate.45` | 0.81 — “c23 & (1.63, 0.51, 1.92, 2.43) & (2.83, 2.23, 6.42, 13.40) & (0.46, 1.13, 1.99, 1.26) & (0” | 0.81 | 0.8123 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.45` |
| `R1.supp-tab-appexpbandgate.46` | 0.89 — “c23 & (1.63, 0.51, 1.92, 2.43) & (2.83, 2.23, 6.42, 13.40) & (0.46, 1.13, 1.99, 1.26) & (0” | 0.89 | 0.8939 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.46` |
| `R1.supp-tab-appexpbandgate.47` | 1.10 — “c23 & (1.63, 0.51, 1.92, 2.43) & (2.83, 2.23, 6.42, 13.40) & (0.46, 1.13, 1.99, 1.26) & (0” | 1.10 | 1.0983 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.47` |
| `R1.supp-tab-appexpbandgate.48` | 0.25 — “c23 & (1.63, 0.51, 1.92, 2.43) & (2.83, 2.23, 6.42, 13.40) & (0.46, 1.13, 1.99, 1.26) & (0” | 0.25 | 0.2510 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.48` |
| `R1.supp-tab-appexpbandgate.49` | 1.15 — “c28 & (1.15, 2.50, 2.40, 1.50) & (2.58, 3.28, 6.66, 12.81) & (0.63, 1.76, 4.00, 1.31) & (0” | 1.15 | 1.1500 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.49` |
| `R1.supp-tab-appexpbandgate.50` | 2.50 — “c28 & (1.15, 2.50, 2.40, 1.50) & (2.58, 3.28, 6.66, 12.81) & (0.63, 1.76, 4.00, 1.31) & (0” | 2.50 | 2.4992 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.50` |
| `R1.supp-tab-appexpbandgate.51` | 2.40 — “c28 & (1.15, 2.50, 2.40, 1.50) & (2.58, 3.28, 6.66, 12.81) & (0.63, 1.76, 4.00, 1.31) & (0” | 2.40 | 2.4009 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.51` |
| `R1.supp-tab-appexpbandgate.52` | 1.50 — “c28 & (1.15, 2.50, 2.40, 1.50) & (2.58, 3.28, 6.66, 12.81) & (0.63, 1.76, 4.00, 1.31) & (0” | 1.50 | 1.4974 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.52` |
| `R1.supp-tab-appexpbandgate.53` | 2.58 — “c28 & (1.15, 2.50, 2.40, 1.50) & (2.58, 3.28, 6.66, 12.81) & (0.63, 1.76, 4.00, 1.31) & (0” | 2.58 | 2.5805 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.53` |
| `R1.supp-tab-appexpbandgate.54` | 3.28 — “c28 & (1.15, 2.50, 2.40, 1.50) & (2.58, 3.28, 6.66, 12.81) & (0.63, 1.76, 4.00, 1.31) & (0” | 3.28 | 3.2821 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.54` |
| `R1.supp-tab-appexpbandgate.55` | 6.66 — “c28 & (1.15, 2.50, 2.40, 1.50) & (2.58, 3.28, 6.66, 12.81) & (0.63, 1.76, 4.00, 1.31) & (0” | 6.66 | 6.6560 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.55` |
| `R1.supp-tab-appexpbandgate.56` | 12.81 — “c28 & (1.15, 2.50, 2.40, 1.50) & (2.58, 3.28, 6.66, 12.81) & (0.63, 1.76, 4.00, 1.31) & (0” | 12.81 | 12.81 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.56` |
| `R1.supp-tab-appexpbandgate.57` | 0.63 — “c28 & (1.15, 2.50, 2.40, 1.50) & (2.58, 3.28, 6.66, 12.81) & (0.63, 1.76, 4.00, 1.31) & (0” | 0.63 | 0.6283 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.57` |
| `R1.supp-tab-appexpbandgate.58` | 1.76 — “c28 & (1.15, 2.50, 2.40, 1.50) & (2.58, 3.28, 6.66, 12.81) & (0.63, 1.76, 4.00, 1.31) & (0” | 1.76 | 1.7584 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.58` |
| `R1.supp-tab-appexpbandgate.59` | 4.00 — “c28 & (1.15, 2.50, 2.40, 1.50) & (2.58, 3.28, 6.66, 12.81) & (0.63, 1.76, 4.00, 1.31) & (0” | 4.00 | 4.0039 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.59` |
| `R1.supp-tab-appexpbandgate.60` | 1.31 — “c28 & (1.15, 2.50, 2.40, 1.50) & (2.58, 3.28, 6.66, 12.81) & (0.63, 1.76, 4.00, 1.31) & (0” | 1.31 | 1.3099 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.60` |
| `R1.supp-tab-appexpbandgate.61` | 0.81 — “c28 & (1.15, 2.50, 2.40, 1.50) & (2.58, 3.28, 6.66, 12.81) & (0.63, 1.76, 4.00, 1.31) & (0” | 0.81 | 0.8113 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.61` |
| `R1.supp-tab-appexpbandgate.62` | 0.89 — “c28 & (1.15, 2.50, 2.40, 1.50) & (2.58, 3.28, 6.66, 12.81) & (0.63, 1.76, 4.00, 1.31) & (0” | 0.89 | 0.8944 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.62` |
| `R1.supp-tab-appexpbandgate.63` | 1.10 — “c28 & (1.15, 2.50, 2.40, 1.50) & (2.58, 3.28, 6.66, 12.81) & (0.63, 1.76, 4.00, 1.31) & (0” | 1.10 | 1.0978 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.63` |
| `R1.supp-tab-appexpbandgate.64` | 0.25 — “c28 & (1.15, 2.50, 2.40, 1.50) & (2.58, 3.28, 6.66, 12.81) & (0.63, 1.76, 4.00, 1.31) & (0” | 0.25 | 0.2517 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.64` |
| `R1.supp-tab-appexpbandgate.65` | 1.15 — “c32 & (1.15, 2.12, 2.58, 1.26) & (2.55, 3.35, 6.39, 11.86) & (0.62, 1.94, 4.67, 1.35) & (0” | 1.15 | 1.1529 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.65` |
| `R1.supp-tab-appexpbandgate.66` | 2.12 — “c32 & (1.15, 2.12, 2.58, 1.26) & (2.55, 3.35, 6.39, 11.86) & (0.62, 1.94, 4.67, 1.35) & (0” | 2.12 | 2.1240 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.66` |
| `R1.supp-tab-appexpbandgate.67` | 2.58 — “c32 & (1.15, 2.12, 2.58, 1.26) & (2.55, 3.35, 6.39, 11.86) & (0.62, 1.94, 4.67, 1.35) & (0” | 2.58 | 2.5804 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.67` |
| `R1.supp-tab-appexpbandgate.68` | 1.26 — “c32 & (1.15, 2.12, 2.58, 1.26) & (2.55, 3.35, 6.39, 11.86) & (0.62, 1.94, 4.67, 1.35) & (0” | 1.26 | 1.2568 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.68` |
| `R1.supp-tab-appexpbandgate.69` | 2.55 — “c32 & (1.15, 2.12, 2.58, 1.26) & (2.55, 3.35, 6.39, 11.86) & (0.62, 1.94, 4.67, 1.35) & (0” | 2.55 | 2.5479 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.69` |
| `R1.supp-tab-appexpbandgate.70` | 3.35 — “c32 & (1.15, 2.12, 2.58, 1.26) & (2.55, 3.35, 6.39, 11.86) & (0.62, 1.94, 4.67, 1.35) & (0” | 3.35 | 3.3511 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.70` |
| `R1.supp-tab-appexpbandgate.71` | 6.39 — “c32 & (1.15, 2.12, 2.58, 1.26) & (2.55, 3.35, 6.39, 11.86) & (0.62, 1.94, 4.67, 1.35) & (0” | 6.39 | 6.3910 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.71` |
| `R1.supp-tab-appexpbandgate.72` | 11.86 — “c32 & (1.15, 2.12, 2.58, 1.26) & (2.55, 3.35, 6.39, 11.86) & (0.62, 1.94, 4.67, 1.35) & (0” | 11.86 | 11.86 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.72` |
| `R1.supp-tab-appexpbandgate.73` | 0.62 — “c32 & (1.15, 2.12, 2.58, 1.26) & (2.55, 3.35, 6.39, 11.86) & (0.62, 1.94, 4.67, 1.35) & (0” | 0.62 | 0.6182 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.73` |
| `R1.supp-tab-appexpbandgate.74` | 1.94 — “c32 & (1.15, 2.12, 2.58, 1.26) & (2.55, 3.35, 6.39, 11.86) & (0.62, 1.94, 4.67, 1.35) & (0” | 1.94 | 1.9400 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.74` |
| `R1.supp-tab-appexpbandgate.75` | 4.67 — “c32 & (1.15, 2.12, 2.58, 1.26) & (2.55, 3.35, 6.39, 11.86) & (0.62, 1.94, 4.67, 1.35) & (0” | 4.67 | 4.6719 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.75` |
| `R1.supp-tab-appexpbandgate.76` | 1.35 — “c32 & (1.15, 2.12, 2.58, 1.26) & (2.55, 3.35, 6.39, 11.86) & (0.62, 1.94, 4.67, 1.35) & (0” | 1.35 | 1.3468 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.76` |
| `R1.supp-tab-appexpbandgate.77` | 0.81 — “c32 & (1.15, 2.12, 2.58, 1.26) & (2.55, 3.35, 6.39, 11.86) & (0.62, 1.94, 4.67, 1.35) & (0” | 0.81 | 0.8057 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.77` |
| `R1.supp-tab-appexpbandgate.78` | 0.90 — “c32 & (1.15, 2.12, 2.58, 1.26) & (2.55, 3.35, 6.39, 11.86) & (0.62, 1.94, 4.67, 1.35) & (0” | 0.90 | 0.8952 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.78` |
| `R1.supp-tab-appexpbandgate.79` | 1.10 — “c32 & (1.15, 2.12, 2.58, 1.26) & (2.55, 3.35, 6.39, 11.86) & (0.62, 1.94, 4.67, 1.35) & (0” | 1.10 | 1.0974 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.79` |
| `R1.supp-tab-appexpbandgate.80` | 0.25 — “c32 & (1.15, 2.12, 2.58, 1.26) & (2.55, 3.35, 6.39, 11.86) & (0.62, 1.94, 4.67, 1.35) & (0” | 0.25 | 0.2493 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.80` |
| `R1.supp-tab-appexpbandgate.81` | 1.04 — “c36 & (1.04, 1.83, 2.83, 0.97) & (2.56, 3.36, 6.25, 10.85) & (0.59, 1.99, 5.09, 1.38) & (0” | 1.04 | 1.0425 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.81` |
| `R1.supp-tab-appexpbandgate.82` | 1.83 — “c36 & (1.04, 1.83, 2.83, 0.97) & (2.56, 3.36, 6.25, 10.85) & (0.59, 1.99, 5.09, 1.38) & (0” | 1.83 | 1.8328 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.82` |
| `R1.supp-tab-appexpbandgate.83` | 2.83 — “c36 & (1.04, 1.83, 2.83, 0.97) & (2.56, 3.36, 6.25, 10.85) & (0.59, 1.99, 5.09, 1.38) & (0” | 2.83 | 2.8349 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.83` |
| `R1.supp-tab-appexpbandgate.84` | 0.97 — “c36 & (1.04, 1.83, 2.83, 0.97) & (2.56, 3.36, 6.25, 10.85) & (0.59, 1.99, 5.09, 1.38) & (0” | 0.97 | 0.9652 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.84` |
| `R1.supp-tab-appexpbandgate.85` | 2.56 — “c36 & (1.04, 1.83, 2.83, 0.97) & (2.56, 3.36, 6.25, 10.85) & (0.59, 1.99, 5.09, 1.38) & (0” | 2.56 | 2.5595 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.85` |
| `R1.supp-tab-appexpbandgate.86` | 3.36 — “c36 & (1.04, 1.83, 2.83, 0.97) & (2.56, 3.36, 6.25, 10.85) & (0.59, 1.99, 5.09, 1.38) & (0” | 3.36 | 3.3639 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.86` |
| `R1.supp-tab-appexpbandgate.87` | 6.25 — “c36 & (1.04, 1.83, 2.83, 0.97) & (2.56, 3.36, 6.25, 10.85) & (0.59, 1.99, 5.09, 1.38) & (0” | 6.25 | 6.2526 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.87` |
| `R1.supp-tab-appexpbandgate.88` | 10.85 — “c36 & (1.04, 1.83, 2.83, 0.97) & (2.56, 3.36, 6.25, 10.85) & (0.59, 1.99, 5.09, 1.38) & (0” | 10.85 | 10.85 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.88` |
| `R1.supp-tab-appexpbandgate.89` | 0.59 — “c36 & (1.04, 1.83, 2.83, 0.97) & (2.56, 3.36, 6.25, 10.85) & (0.59, 1.99, 5.09, 1.38) & (0” | 0.59 | 0.5939 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.89` |
| `R1.supp-tab-appexpbandgate.90` | 1.99 — “c36 & (1.04, 1.83, 2.83, 0.97) & (2.56, 3.36, 6.25, 10.85) & (0.59, 1.99, 5.09, 1.38) & (0” | 1.99 | 1.9881 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.90` |
| `R1.supp-tab-appexpbandgate.91` | 5.09 — “c36 & (1.04, 1.83, 2.83, 0.97) & (2.56, 3.36, 6.25, 10.85) & (0.59, 1.99, 5.09, 1.38) & (0” | 5.09 | 5.0895 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.91` |
| `R1.supp-tab-appexpbandgate.92` | 1.38 — “c36 & (1.04, 1.83, 2.83, 0.97) & (2.56, 3.36, 6.25, 10.85) & (0.59, 1.99, 5.09, 1.38) & (0” | 1.38 | 1.3756 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.92` |
| `R1.supp-tab-appexpbandgate.93` | 0.80 — “c36 & (1.04, 1.83, 2.83, 0.97) & (2.56, 3.36, 6.25, 10.85) & (0.59, 1.99, 5.09, 1.38) & (0” | 0.80 | 0.7980 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.93` |
| `R1.supp-tab-appexpbandgate.94` | 0.90 — “c36 & (1.04, 1.83, 2.83, 0.97) & (2.56, 3.36, 6.25, 10.85) & (0.59, 1.99, 5.09, 1.38) & (0” | 0.90 | 0.8966 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.94` |
| `R1.supp-tab-appexpbandgate.95` | 1.10 — “c36 & (1.04, 1.83, 2.83, 0.97) & (2.56, 3.36, 6.25, 10.85) & (0.59, 1.99, 5.09, 1.38) & (0” | 1.10 | 1.0971 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.95` |
| `R1.supp-tab-appexpbandgate.96` | 0.25 — “c36 & (1.04, 1.83, 2.83, 0.97) & (2.56, 3.36, 6.25, 10.85) & (0.59, 1.99, 5.09, 1.38) & (0” | 0.25 | 0.2461 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.96` |
| `R1.supp-tab-appexpbandgate.97` | 1.37 — “c40 & (1.37, 0.85, 2.78, 1.01) & (2.52, 3.16, 5.91, 7.84) & (0.45, 1.63, 4.58, 1.55) & (0.” | 1.37 | 1.3667 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.97` |
| `R1.supp-tab-appexpbandgate.98` | 0.85 — “c40 & (1.37, 0.85, 2.78, 1.01) & (2.52, 3.16, 5.91, 7.84) & (0.45, 1.63, 4.58, 1.55) & (0.” | 0.85 | 0.8485 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.98` |
| `R1.supp-tab-appexpbandgate.99` | 2.78 — “c40 & (1.37, 0.85, 2.78, 1.01) & (2.52, 3.16, 5.91, 7.84) & (0.45, 1.63, 4.58, 1.55) & (0.” | 2.78 | 2.7806 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.99` |
| `R1.supp-tab-appexpbandgate.100` | 1.01 — “c40 & (1.37, 0.85, 2.78, 1.01) & (2.52, 3.16, 5.91, 7.84) & (0.45, 1.63, 4.58, 1.55) & (0.” | 1.01 | 1.0107 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.100` |
| `R1.supp-tab-appexpbandgate.101` | 2.52 — “c40 & (1.37, 0.85, 2.78, 1.01) & (2.52, 3.16, 5.91, 7.84) & (0.45, 1.63, 4.58, 1.55) & (0.” | 2.52 | 2.5242 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.101` |
| `R1.supp-tab-appexpbandgate.102` | 3.16 — “c40 & (1.37, 0.85, 2.78, 1.01) & (2.52, 3.16, 5.91, 7.84) & (0.45, 1.63, 4.58, 1.55) & (0.” | 3.16 | 3.1562 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.102` |
| `R1.supp-tab-appexpbandgate.103` | 5.91 — “c40 & (1.37, 0.85, 2.78, 1.01) & (2.52, 3.16, 5.91, 7.84) & (0.45, 1.63, 4.58, 1.55) & (0.” | 5.91 | 5.9058 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.103` |
| `R1.supp-tab-appexpbandgate.104` | 7.84 — “c40 & (1.37, 0.85, 2.78, 1.01) & (2.52, 3.16, 5.91, 7.84) & (0.45, 1.63, 4.58, 1.55) & (0.” | 7.84 | 7.8386 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.104` |
| `R1.supp-tab-appexpbandgate.105` | 0.45 — “c40 & (1.37, 0.85, 2.78, 1.01) & (2.52, 3.16, 5.91, 7.84) & (0.45, 1.63, 4.58, 1.55) & (0.” | 0.45 | 0.4484 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.105` |
| `R1.supp-tab-appexpbandgate.106` | 1.63 — “c40 & (1.37, 0.85, 2.78, 1.01) & (2.52, 3.16, 5.91, 7.84) & (0.45, 1.63, 4.58, 1.55) & (0.” | 1.63 | 1.6349 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.106` |
| `R1.supp-tab-appexpbandgate.107` | 4.58 — “c40 & (1.37, 0.85, 2.78, 1.01) & (2.52, 3.16, 5.91, 7.84) & (0.45, 1.63, 4.58, 1.55) & (0.” | 4.58 | 4.5844 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.107` |
| `R1.supp-tab-appexpbandgate.108` | 1.55 — “c40 & (1.37, 0.85, 2.78, 1.01) & (2.52, 3.16, 5.91, 7.84) & (0.45, 1.63, 4.58, 1.55) & (0.” | 1.55 | 1.5493 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.108` |
| `R1.supp-tab-appexpbandgate.109` | 0.78 — “c40 & (1.37, 0.85, 2.78, 1.01) & (2.52, 3.16, 5.91, 7.84) & (0.45, 1.63, 4.58, 1.55) & (0.” | 0.78 | 0.7820 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.109` |
| `R1.supp-tab-appexpbandgate.110` | 0.90 — “c40 & (1.37, 0.85, 2.78, 1.01) & (2.52, 3.16, 5.91, 7.84) & (0.45, 1.63, 4.58, 1.55) & (0.” | 0.90 | 0.9001 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.110` |
| `R1.supp-tab-appexpbandgate.111` | 1.10 — “c40 & (1.37, 0.85, 2.78, 1.01) & (2.52, 3.16, 5.91, 7.84) & (0.45, 1.63, 4.58, 1.55) & (0.” | 1.10 | 1.0973 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.111` |
| `R1.supp-tab-appexpbandgate.112` | 0.24 — “c40 & (1.37, 0.85, 2.78, 1.01) & (2.52, 3.16, 5.91, 7.84) & (0.45, 1.63, 4.58, 1.55) & (0.” | 0.24 | 0.2381 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpbandgate.112` |

## R1.supp-tab-appexpestimator — Revision 1 — Supplementary Material, tab:appexpestimator

*Supplementary Material, tab:appexpestimator; `\label{tab:appexpestimator}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-tab-appexpestimator.1` | 0.8931 — “(a) & Fair-N s42 & 0.8931 & 0.9735 & 0.8899 & 0.9433 & 0.9813 & 0.9993 \\” | 0.8931 | 0.8931 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.1` |
| `R1.supp-tab-appexpestimator.2` | 0.9735 — “(a) & Fair-N s42 & 0.8931 & 0.9735 & 0.8899 & 0.9433 & 0.9813 & 0.9993 \\” | 0.9735 | 0.9735 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.2` |
| `R1.supp-tab-appexpestimator.3` | 0.8899 — “(a) & Fair-N s42 & 0.8931 & 0.9735 & 0.8899 & 0.9433 & 0.9813 & 0.9993 \\” | 0.8899 | 0.8899 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.3` |
| `R1.supp-tab-appexpestimator.4` | 0.9433 — “(a) & Fair-N s42 & 0.8931 & 0.9735 & 0.8899 & 0.9433 & 0.9813 & 0.9993 \\” | 0.9433 | 0.9433 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.4` |
| `R1.supp-tab-appexpestimator.5` | 0.9813 — “(a) & Fair-N s42 & 0.8931 & 0.9735 & 0.8899 & 0.9433 & 0.9813 & 0.9993 \\” | 0.9813 | 0.9813 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.5` |
| `R1.supp-tab-appexpestimator.6` | 0.9993 — “(a) & Fair-N s42 & 0.8931 & 0.9735 & 0.8899 & 0.9433 & 0.9813 & 0.9993 \\” | 0.9993 | 0.9993 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.6` |
| `R1.supp-tab-appexpestimator.7` | 0.9860 — “& Fair-N s1 & 0.9860 & 0.9987 & 0.6929 & 0.9505 & 0.9481 & 0.9823 \\” | 0.9860 | 0.9860 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.7` |
| `R1.supp-tab-appexpestimator.8` | 0.9987 — “& Fair-N s1 & 0.9860 & 0.9987 & 0.6929 & 0.9505 & 0.9481 & 0.9823 \\” | 0.9987 | 0.9987 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.8` |
| `R1.supp-tab-appexpestimator.9` | 0.6929 — “& Fair-N s1 & 0.9860 & 0.9987 & 0.6929 & 0.9505 & 0.9481 & 0.9823 \\” | 0.6929 | 0.6929 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.9` |
| `R1.supp-tab-appexpestimator.10` | 0.9505 — “& Fair-N s1 & 0.9860 & 0.9987 & 0.6929 & 0.9505 & 0.9481 & 0.9823 \\” | 0.9505 | 0.9505 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.10` |
| `R1.supp-tab-appexpestimator.11` | 0.9481 — “& Fair-N s1 & 0.9860 & 0.9987 & 0.6929 & 0.9505 & 0.9481 & 0.9823 \\” | 0.9481 | 0.9481 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.11` |
| `R1.supp-tab-appexpestimator.12` | 0.9823 — “& Fair-N s1 & 0.9860 & 0.9987 & 0.6929 & 0.9505 & 0.9481 & 0.9823 \\” | 0.9823 | 0.9823 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.12` |
| `R1.supp-tab-appexpestimator.13` | 0.9433 — “& Fair-N s2 & 0.9433 & 0.9957 & 0.7538 & 0.9045 & 0.9504 & 0.9906 \\” | 0.9433 | 0.9433 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.13` |
| `R1.supp-tab-appexpestimator.14` | 0.9957 — “& Fair-N s2 & 0.9433 & 0.9957 & 0.7538 & 0.9045 & 0.9504 & 0.9906 \\” | 0.9957 | 0.9957 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.14` |
| `R1.supp-tab-appexpestimator.15` | 0.7538 — “& Fair-N s2 & 0.9433 & 0.9957 & 0.7538 & 0.9045 & 0.9504 & 0.9906 \\” | 0.7538 | 0.7538 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.15` |
| `R1.supp-tab-appexpestimator.16` | 0.9045 — “& Fair-N s2 & 0.9433 & 0.9957 & 0.7538 & 0.9045 & 0.9504 & 0.9906 \\” | 0.9045 | 0.9045 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.16` |
| `R1.supp-tab-appexpestimator.17` | 0.9504 — “& Fair-N s2 & 0.9433 & 0.9957 & 0.7538 & 0.9045 & 0.9504 & 0.9906 \\” | 0.9504 | 0.9504 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.17` |
| `R1.supp-tab-appexpestimator.18` | 0.9906 — “& Fair-N s2 & 0.9433 & 0.9957 & 0.7538 & 0.9045 & 0.9504 & 0.9906 \\” | 0.9906 | 0.9906 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.18` |
| `R1.supp-tab-appexpestimator.19` | 0.8896 — “& Fair-W s42 & 0.8896 & 0.9997 & 0.9612 & 0.9674 & 0.8507 & 0.9328 \\” | 0.8896 | 0.8896 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.19` |
| `R1.supp-tab-appexpestimator.20` | 0.9997 — “& Fair-W s42 & 0.8896 & 0.9997 & 0.9612 & 0.9674 & 0.8507 & 0.9328 \\” | 0.9997 | 0.9997 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.20` |
| `R1.supp-tab-appexpestimator.21` | 0.9612 — “& Fair-W s42 & 0.8896 & 0.9997 & 0.9612 & 0.9674 & 0.8507 & 0.9328 \\” | 0.9612 | 0.9612 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.21` |
| `R1.supp-tab-appexpestimator.22` | 0.9674 — “& Fair-W s42 & 0.8896 & 0.9997 & 0.9612 & 0.9674 & 0.8507 & 0.9328 \\” | 0.9674 | 0.9674 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.22` |
| `R1.supp-tab-appexpestimator.23` | 0.8507 — “& Fair-W s42 & 0.8896 & 0.9997 & 0.9612 & 0.9674 & 0.8507 & 0.9328 \\” | 0.8507 | 0.8507 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.23` |
| `R1.supp-tab-appexpestimator.24` | 0.9328 — “& Fair-W s42 & 0.8896 & 0.9997 & 0.9612 & 0.9674 & 0.8507 & 0.9328 \\” | 0.9328 | 0.9328 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.24` |
| `R1.supp-tab-appexpestimator.25` | 0.9735 — “& Fair-W s1 & 0.9735 & 0.9999 & 0.9095 & 0.8765 & 0.8975 & 0.9826 \\” | 0.9735 | 0.9735 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.25` |
| `R1.supp-tab-appexpestimator.26` | 0.9999 — “& Fair-W s1 & 0.9735 & 0.9999 & 0.9095 & 0.8765 & 0.8975 & 0.9826 \\” | 0.9999 | 0.9999 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.26` |
| `R1.supp-tab-appexpestimator.27` | 0.9095 — “& Fair-W s1 & 0.9735 & 0.9999 & 0.9095 & 0.8765 & 0.8975 & 0.9826 \\” | 0.9095 | 0.9095 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.27` |
| `R1.supp-tab-appexpestimator.28` | 0.8765 — “& Fair-W s1 & 0.9735 & 0.9999 & 0.9095 & 0.8765 & 0.8975 & 0.9826 \\” | 0.8765 | 0.8765 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.28` |
| `R1.supp-tab-appexpestimator.29` | 0.8975 — “& Fair-W s1 & 0.9735 & 0.9999 & 0.9095 & 0.8765 & 0.8975 & 0.9826 \\” | 0.8975 | 0.8975 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.29` |
| `R1.supp-tab-appexpestimator.30` | 0.9826 — “& Fair-W s1 & 0.9735 & 0.9999 & 0.9095 & 0.8765 & 0.8975 & 0.9826 \\” | 0.9826 | 0.9826 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.30` |
| `R1.supp-tab-appexpestimator.31` | 0.9450 — “& Fair-W s2 & 0.9450 & 0.9926 & 0.5601 & 0.8286 & 0.6440 & 0.9372 \\” | 0.9450 | 0.9450 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.31` |
| `R1.supp-tab-appexpestimator.32` | 0.9926 — “& Fair-W s2 & 0.9450 & 0.9926 & 0.5601 & 0.8286 & 0.6440 & 0.9372 \\” | 0.9926 | 0.9926 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.32` |
| `R1.supp-tab-appexpestimator.33` | 0.5601 — “& Fair-W s2 & 0.9450 & 0.9926 & 0.5601 & 0.8286 & 0.6440 & 0.9372 \\” | 0.5601 | 0.5601 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.33` |
| `R1.supp-tab-appexpestimator.34` | 0.8286 — “& Fair-W s2 & 0.9450 & 0.9926 & 0.5601 & 0.8286 & 0.6440 & 0.9372 \\” | 0.8286 | 0.8286 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.34` |
| `R1.supp-tab-appexpestimator.35` | 0.6440 — “& Fair-W s2 & 0.9450 & 0.9926 & 0.5601 & 0.8286 & 0.6440 & 0.9372 \\” | 0.6440 | 0.6440 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.35` |
| `R1.supp-tab-appexpestimator.36` | 0.9372 — “& Fair-W s2 & 0.9450 & 0.9926 & 0.5601 & 0.8286 & 0.6440 & 0.9372 \\” | 0.9372 | 0.9372 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.36` |
| `R1.supp-tab-appexpestimator.37` | 0.9382 — “& E1 s42 & 0.9382 & 0.9353 & 0.7001 & 0.6925 & 0.9922 & 1.0000 \\” | 0.9382 | 0.9382 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.37` |
| `R1.supp-tab-appexpestimator.38` | 0.9353 — “& E1 s42 & 0.9382 & 0.9353 & 0.7001 & 0.6925 & 0.9922 & 1.0000 \\” | 0.9353 | 0.9353 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.38` |
| `R1.supp-tab-appexpestimator.39` | 0.7001 — “& E1 s42 & 0.9382 & 0.9353 & 0.7001 & 0.6925 & 0.9922 & 1.0000 \\” | 0.7001 | 0.7001 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.39` |
| `R1.supp-tab-appexpestimator.40` | 0.6925 — “& E1 s42 & 0.9382 & 0.9353 & 0.7001 & 0.6925 & 0.9922 & 1.0000 \\” | 0.6925 | 0.6925 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.40` |
| `R1.supp-tab-appexpestimator.41` | 0.9922 — “& E1 s42 & 0.9382 & 0.9353 & 0.7001 & 0.6925 & 0.9922 & 1.0000 \\” | 0.9922 | 0.9922 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.41` |
| `R1.supp-tab-appexpestimator.42` | 1.0000 — “& E1 s42 & 0.9382 & 0.9353 & 0.7001 & 0.6925 & 0.9922 & 1.0000 \\” | 1.0000 | 1.0000 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.42` |
| `R1.supp-tab-appexpestimator.43` | 0.9650 — “& E1 s1 & 0.9650 & 0.9897 & 0.6248 & 0.8366 & 0.8929 & 0.9536 \\” | 0.9650 | 0.9650 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.43` |
| `R1.supp-tab-appexpestimator.44` | 0.9897 — “& E1 s1 & 0.9650 & 0.9897 & 0.6248 & 0.8366 & 0.8929 & 0.9536 \\” | 0.9897 | 0.9897 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.44` |
| `R1.supp-tab-appexpestimator.45` | 0.6248 — “& E1 s1 & 0.9650 & 0.9897 & 0.6248 & 0.8366 & 0.8929 & 0.9536 \\” | 0.6248 | 0.6248 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.45` |
| `R1.supp-tab-appexpestimator.46` | 0.8366 — “& E1 s1 & 0.9650 & 0.9897 & 0.6248 & 0.8366 & 0.8929 & 0.9536 \\” | 0.8366 | 0.8366 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.46` |
| `R1.supp-tab-appexpestimator.47` | 0.8929 — “& E1 s1 & 0.9650 & 0.9897 & 0.6248 & 0.8366 & 0.8929 & 0.9536 \\” | 0.8929 | 0.8929 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.47` |
| `R1.supp-tab-appexpestimator.48` | 0.9536 — “& E1 s1 & 0.9650 & 0.9897 & 0.6248 & 0.8366 & 0.8929 & 0.9536 \\” | 0.9536 | 0.9536 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.48` |
| `R1.supp-tab-appexpestimator.49` | 0.7148 — “& E1 s2 & 0.7148 & 0.9775 & 0.9628 & 0.9216 & 0.9811 & 0.9984 \\” | 0.7148 | 0.7148 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.49` |
| `R1.supp-tab-appexpestimator.50` | 0.9775 — “& E1 s2 & 0.7148 & 0.9775 & 0.9628 & 0.9216 & 0.9811 & 0.9984 \\” | 0.9775 | 0.9775 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.50` |
| `R1.supp-tab-appexpestimator.51` | 0.9628 — “& E1 s2 & 0.7148 & 0.9775 & 0.9628 & 0.9216 & 0.9811 & 0.9984 \\” | 0.9628 | 0.9628 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.51` |
| `R1.supp-tab-appexpestimator.52` | 0.9216 — “& E1 s2 & 0.7148 & 0.9775 & 0.9628 & 0.9216 & 0.9811 & 0.9984 \\” | 0.9216 | 0.9216 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.52` |
| `R1.supp-tab-appexpestimator.53` | 0.9811 — “& E1 s2 & 0.7148 & 0.9775 & 0.9628 & 0.9216 & 0.9811 & 0.9984 \\” | 0.9811 | 0.9811 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.53` |
| `R1.supp-tab-appexpestimator.54` | 0.9984 — “& E1 s2 & 0.7148 & 0.9775 & 0.9628 & 0.9216 & 0.9811 & 0.9984 \\” | 0.9984 | 0.9984 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.54` |
| `R1.supp-tab-appexpestimator.55` | 0.1746 — “& CAFRL as specified s42 & 0.1746 & 0.8633 & 0.8840 & 0.8608 & 0.2017 & 0.1537 \\” | 0.1746 | 0.1746 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.55` |
| `R1.supp-tab-appexpestimator.56` | 0.8633 — “& CAFRL as specified s42 & 0.1746 & 0.8633 & 0.8840 & 0.8608 & 0.2017 & 0.1537 \\” | 0.8633 | 0.8633 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.56` |
| `R1.supp-tab-appexpestimator.57` | 0.8840 — “& CAFRL as specified s42 & 0.1746 & 0.8633 & 0.8840 & 0.8608 & 0.2017 & 0.1537 \\” | 0.8840 | 0.8840 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.57` |
| `R1.supp-tab-appexpestimator.58` | 0.8608 — “& CAFRL as specified s42 & 0.1746 & 0.8633 & 0.8840 & 0.8608 & 0.2017 & 0.1537 \\” | 0.8608 | 0.8608 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.58` |
| `R1.supp-tab-appexpestimator.59` | 0.2017 — “& CAFRL as specified s42 & 0.1746 & 0.8633 & 0.8840 & 0.8608 & 0.2017 & 0.1537 \\” | 0.2017 | 0.2017 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.59` |
| `R1.supp-tab-appexpestimator.60` | 0.1537 — “& CAFRL as specified s42 & 0.1746 & 0.8633 & 0.8840 & 0.8608 & 0.2017 & 0.1537 \\” | 0.1537 | 0.1537 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.60` |
| `R1.supp-tab-appexpestimator.61` | 99.50 — “(b) & Fair-N s42 & 99.50 / 98.26 & 98.83 / n/r & 98.10 / n/r & 97.84 / n/r & 97.01 / n/r &” | 99.50 | 99.50 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.61` |
| `R1.supp-tab-appexpestimator.62` | 98.26 — “(b) & Fair-N s42 & 99.50 / 98.26 & 98.83 / n/r & 98.10 / n/r & 97.84 / n/r & 97.01 / n/r &” | 98.26 | 98.26 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.62` |
| `R1.supp-tab-appexpestimator.63` | 98.83 — “(b) & Fair-N s42 & 99.50 / 98.26 & 98.83 / n/r & 98.10 / n/r & 97.84 / n/r & 97.01 / n/r &” | 98.83 | 98.83 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.63` |
| `R1.supp-tab-appexpestimator.64` | 98.10 — “(b) & Fair-N s42 & 99.50 / 98.26 & 98.83 / n/r & 98.10 / n/r & 97.84 / n/r & 97.01 / n/r &” | 98.10 | 98.10 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.64` |
| `R1.supp-tab-appexpestimator.65` | 97.84 — “(b) & Fair-N s42 & 99.50 / 98.26 & 98.83 / n/r & 98.10 / n/r & 97.84 / n/r & 97.01 / n/r &” | 97.84 | 97.84 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.65` |
| `R1.supp-tab-appexpestimator.66` | 97.01 — “(b) & Fair-N s42 & 99.50 / 98.26 & 98.83 / n/r & 98.10 / n/r & 97.84 / n/r & 97.01 / n/r &” | 97.01 | 97.01 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.66` |
| `R1.supp-tab-appexpestimator.67` | 95.86 — “(b) & Fair-N s42 & 99.50 / 98.26 & 98.83 / n/r & 98.10 / n/r & 97.84 / n/r & 97.01 / n/r &” | 95.86 | 95.86 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.67` |
| `R1.supp-tab-appexpestimator.68` | 99.52 — “& Fair-N s1 & 99.52 / n/r & 98.79 / n/r & 97.01 / 96.71 & 97.21 / n/r & 96.37 / n/r & 95.7” | 99.52 | 99.52 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.68` |
| `R1.supp-tab-appexpestimator.69` | 98.79 — “& Fair-N s1 & 99.52 / n/r & 98.79 / n/r & 97.01 / 96.71 & 97.21 / n/r & 96.37 / n/r & 95.7” | 98.79 | 98.79 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.69` |
| `R1.supp-tab-appexpestimator.70` | 97.01 — “& Fair-N s1 & 99.52 / n/r & 98.79 / n/r & 97.01 / 96.71 & 97.21 / n/r & 96.37 / n/r & 95.7” | 97.01 | 97.01 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.70` |
| `R1.supp-tab-appexpestimator.71` | 96.71 — “& Fair-N s1 & 99.52 / n/r & 98.79 / n/r & 97.01 / 96.71 & 97.21 / n/r & 96.37 / n/r & 95.7” | 96.71 | 96.71 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.71` |
| `R1.supp-tab-appexpestimator.72` | 97.21 — “& Fair-N s1 & 99.52 / n/r & 98.79 / n/r & 97.01 / 96.71 & 97.21 / n/r & 96.37 / n/r & 95.7” | 97.21 | 97.21 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.72` |
| `R1.supp-tab-appexpestimator.73` | 96.37 — “& Fair-N s1 & 99.52 / n/r & 98.79 / n/r & 97.01 / 96.71 & 97.21 / n/r & 96.37 / n/r & 95.7” | 96.37 | 96.37 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.73` |
| `R1.supp-tab-appexpestimator.74` | 95.79 — “& Fair-N s1 & 99.52 / n/r & 98.79 / n/r & 97.01 / 96.71 & 97.21 / n/r & 96.37 / n/r & 95.7” | 95.79 | 95.79 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.74` |
| `R1.supp-tab-appexpestimator.75` | 99.26 — “& Fair-N s2 & 99.26 / n/r & 98.62 / n/r & 97.94 / 98.57 & 96.95 / n/r & 96.10 / n/r & 95.3” | 99.26 | 99.26 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.75` |
| `R1.supp-tab-appexpestimator.76` | 98.62 — “& Fair-N s2 & 99.26 / n/r & 98.62 / n/r & 97.94 / 98.57 & 96.95 / n/r & 96.10 / n/r & 95.3” | 98.62 | 98.62 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.76` |
| `R1.supp-tab-appexpestimator.77` | 97.94 — “& Fair-N s2 & 99.26 / n/r & 98.62 / n/r & 97.94 / 98.57 & 96.95 / n/r & 96.10 / n/r & 95.3” | 97.94 | 97.94 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.77` |
| `R1.supp-tab-appexpestimator.78` | 98.57 — “& Fair-N s2 & 99.26 / n/r & 98.62 / n/r & 97.94 / 98.57 & 96.95 / n/r & 96.10 / n/r & 95.3” | 98.57 | 98.57 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.78` |
| `R1.supp-tab-appexpestimator.79` | 96.95 — “& Fair-N s2 & 99.26 / n/r & 98.62 / n/r & 97.94 / 98.57 & 96.95 / n/r & 96.10 / n/r & 95.3” | 96.95 | 96.95 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.79` |
| `R1.supp-tab-appexpestimator.80` | 96.10 — “& Fair-N s2 & 99.26 / n/r & 98.62 / n/r & 97.94 / 98.57 & 96.95 / n/r & 96.10 / n/r & 95.3” | 96.10 | 96.10 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.80` |
| `R1.supp-tab-appexpestimator.81` | 95.36 — “& Fair-N s2 & 99.26 / n/r & 98.62 / n/r & 97.94 / 98.57 & 96.95 / n/r & 96.10 / n/r & 95.3” | 95.36 | 95.36 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.81` |
| `R1.supp-tab-appexpestimator.82` | 99.38 — “& Fair-W s42 & 99.38 / 98.10 & 98.94 / n/r & 98.33 / n/r & 97.79 / n/r & 97.21 / 96.15 & 9” | 99.38 | 99.38 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.82` |
| `R1.supp-tab-appexpestimator.83` | 98.10 — “& Fair-W s42 & 99.38 / 98.10 & 98.94 / n/r & 98.33 / n/r & 97.79 / n/r & 97.21 / 96.15 & 9” | 98.10 | 98.10 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.83` |
| `R1.supp-tab-appexpestimator.84` | 98.94 — “& Fair-W s42 & 99.38 / 98.10 & 98.94 / n/r & 98.33 / n/r & 97.79 / n/r & 97.21 / 96.15 & 9” | 98.94 | 98.94 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.84` |
| `R1.supp-tab-appexpestimator.85` | 98.33 — “& Fair-W s42 & 99.38 / 98.10 & 98.94 / n/r & 98.33 / n/r & 97.79 / n/r & 97.21 / 96.15 & 9” | 98.33 | 98.33 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.85` |
| `R1.supp-tab-appexpestimator.86` | 97.79 — “& Fair-W s42 & 99.38 / 98.10 & 98.94 / n/r & 98.33 / n/r & 97.79 / n/r & 97.21 / 96.15 & 9” | 97.79 | 97.79 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.86` |
| `R1.supp-tab-appexpestimator.87` | 97.21 — “& Fair-W s42 & 99.38 / 98.10 & 98.94 / n/r & 98.33 / n/r & 97.79 / n/r & 97.21 / 96.15 & 9” | 97.21 | 97.21 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.87` |
| `R1.supp-tab-appexpestimator.88` | 96.15 — “& Fair-W s42 & 99.38 / 98.10 & 98.94 / n/r & 98.33 / n/r & 97.79 / n/r & 97.21 / 96.15 & 9” | 96.15 | 96.15 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.88` |
| `R1.supp-tab-appexpestimator.89` | 96.47 — “& Fair-W s42 & 99.38 / 98.10 & 98.94 / n/r & 98.33 / n/r & 97.79 / n/r & 97.21 / 96.15 & 9” | 96.47 | 96.47 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.89` |
| `R1.supp-tab-appexpestimator.90` | 99.35 — “& Fair-W s1 & 99.35 / n/r & 98.64 / n/r & 98.03 / n/r & 97.41 / 94.62 & 96.93 / 94.72 & 96” | 99.35 | 99.35 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.90` |
| `R1.supp-tab-appexpestimator.91` | 98.64 — “& Fair-W s1 & 99.35 / n/r & 98.64 / n/r & 98.03 / n/r & 97.41 / 94.62 & 96.93 / 94.72 & 96” | 98.64 | 98.64 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.91` |
| `R1.supp-tab-appexpestimator.92` | 98.03 — “& Fair-W s1 & 99.35 / n/r & 98.64 / n/r & 98.03 / n/r & 97.41 / 94.62 & 96.93 / 94.72 & 96” | 98.03 | 98.03 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.92` |
| `R1.supp-tab-appexpestimator.93` | 97.41 — “& Fair-W s1 & 99.35 / n/r & 98.64 / n/r & 98.03 / n/r & 97.41 / 94.62 & 96.93 / 94.72 & 96” | 97.41 | 97.41 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.93` |
| `R1.supp-tab-appexpestimator.94` | 94.62 — “& Fair-W s1 & 99.35 / n/r & 98.64 / n/r & 98.03 / n/r & 97.41 / 94.62 & 96.93 / 94.72 & 96” | 94.62 | 94.62 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.94` |
| `R1.supp-tab-appexpestimator.95` | 96.93 — “& Fair-W s1 & 99.35 / n/r & 98.64 / n/r & 98.03 / n/r & 97.41 / 94.62 & 96.93 / 94.72 & 96” | 96.93 | 96.93 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.95` |
| `R1.supp-tab-appexpestimator.96` | 94.72 — “& Fair-W s1 & 99.35 / n/r & 98.64 / n/r & 98.03 / n/r & 97.41 / 94.62 & 96.93 / 94.72 & 96” | 94.72 | 94.72 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.96` |
| `R1.supp-tab-appexpestimator.97` | 96.01 — “& Fair-W s1 & 99.35 / n/r & 98.64 / n/r & 98.03 / n/r & 97.41 / 94.62 & 96.93 / 94.72 & 96” | 96.01 | 96.01 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.97` |
| `R1.supp-tab-appexpestimator.98` | 99.48 — “& Fair-W s2 & 99.48 / 97.96 & 98.71 / n/r & 98.56 / 97.46 & 97.96 / 92.81 & 98.01 / 94.55 ” | 99.48 | 99.48 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.98` |
| `R1.supp-tab-appexpestimator.99` | 97.96 — “& Fair-W s2 & 99.48 / 97.96 & 98.71 / n/r & 98.56 / 97.46 & 97.96 / 92.81 & 98.01 / 94.55 ” | 97.96 | 97.96 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.99` |
| `R1.supp-tab-appexpestimator.100` | 98.71 — “& Fair-W s2 & 99.48 / 97.96 & 98.71 / n/r & 98.56 / 97.46 & 97.96 / 92.81 & 98.01 / 94.55 ” | 98.71 | 98.71 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.100` |
| `R1.supp-tab-appexpestimator.101` | 98.56 — “& Fair-W s2 & 99.48 / 97.96 & 98.71 / n/r & 98.56 / 97.46 & 97.96 / 92.81 & 98.01 / 94.55 ” | 98.56 | 98.56 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.101` |
| `R1.supp-tab-appexpestimator.102` | 97.46 — “& Fair-W s2 & 99.48 / 97.96 & 98.71 / n/r & 98.56 / 97.46 & 97.96 / 92.81 & 98.01 / 94.55 ” | 97.46 | 97.46 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.102` |
| `R1.supp-tab-appexpestimator.103` | 97.96 — “& Fair-W s2 & 99.48 / 97.96 & 98.71 / n/r & 98.56 / 97.46 & 97.96 / 92.81 & 98.01 / 94.55 ” | 97.96 | 97.96 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.103` |
| `R1.supp-tab-appexpestimator.104` | 92.81 — “& Fair-W s2 & 99.48 / 97.96 & 98.71 / n/r & 98.56 / 97.46 & 97.96 / 92.81 & 98.01 / 94.55 ” | 92.81 | 92.81 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.104` |
| `R1.supp-tab-appexpestimator.105` | 98.01 — “& Fair-W s2 & 99.48 / 97.96 & 98.71 / n/r & 98.56 / 97.46 & 97.96 / 92.81 & 98.01 / 94.55 ” | 98.01 | 98.01 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.105` |
| `R1.supp-tab-appexpestimator.106` | 94.55 — “& Fair-W s2 & 99.48 / 97.96 & 98.71 / n/r & 98.56 / 97.46 & 97.96 / 92.81 & 98.01 / 94.55 ” | 94.55 | 94.55 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.106` |
| `R1.supp-tab-appexpestimator.107` | 96.32 — “& Fair-W s2 & 99.48 / 97.96 & 98.71 / n/r & 98.56 / 97.46 & 97.96 / 92.81 & 98.01 / 94.55 ” | 96.32 | 96.32 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.107` |
| `R1.supp-tab-appexpestimator.108` | 99.48 — “& E1 s42 & 99.48 / 94.67 & 98.83 / n/r & 98.35 / 97.85 & 97.87 / 97.84 & 97.22 / n/r & 96.” | 99.48 | 99.48 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.108` |
| `R1.supp-tab-appexpestimator.109` | 94.67 — “& E1 s42 & 99.48 / 94.67 & 98.83 / n/r & 98.35 / 97.85 & 97.87 / 97.84 & 97.22 / n/r & 96.” | 94.67 | 94.67 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.109` |
| `R1.supp-tab-appexpestimator.110` | 98.83 — “& E1 s42 & 99.48 / 94.67 & 98.83 / n/r & 98.35 / 97.85 & 97.87 / 97.84 & 97.22 / n/r & 96.” | 98.83 | 98.83 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.110` |
| `R1.supp-tab-appexpestimator.111` | 98.35 — “& E1 s42 & 99.48 / 94.67 & 98.83 / n/r & 98.35 / 97.85 & 97.87 / 97.84 & 97.22 / n/r & 96.” | 98.35 | 98.35 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.111` |
| `R1.supp-tab-appexpestimator.112` | 97.85 — “& E1 s42 & 99.48 / 94.67 & 98.83 / n/r & 98.35 / 97.85 & 97.87 / 97.84 & 97.22 / n/r & 96.” | 97.85 | 97.85 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.112` |
| `R1.supp-tab-appexpestimator.113` | 97.87 — “& E1 s42 & 99.48 / 94.67 & 98.83 / n/r & 98.35 / 97.85 & 97.87 / 97.84 & 97.22 / n/r & 96.” | 97.87 | 97.87 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.113` |
| `R1.supp-tab-appexpestimator.114` | 97.84 — “& E1 s42 & 99.48 / 94.67 & 98.83 / n/r & 98.35 / 97.85 & 97.87 / 97.84 & 97.22 / n/r & 96.” | 97.84 | 97.84 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.114` |
| `R1.supp-tab-appexpestimator.115` | 97.22 — “& E1 s42 & 99.48 / 94.67 & 98.83 / n/r & 98.35 / 97.85 & 97.87 / 97.84 & 97.22 / n/r & 96.” | 97.22 | 97.22 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.115` |
| `R1.supp-tab-appexpestimator.116` | 96.17 — “& E1 s42 & 99.48 / 94.67 & 98.83 / n/r & 98.35 / 97.85 & 97.87 / 97.84 & 97.22 / n/r & 96.” | 96.17 | 96.17 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.116` |
| `R1.supp-tab-appexpestimator.117` | 99.39 — “& E1 s1 & 99.39 / n/r & 98.96 / n/r & 97.94 / 98.94 & 97.66 / 99.00 & 97.42 / 99.37 & 96.7” | 99.39 | 99.39 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.117` |
| `R1.supp-tab-appexpestimator.118` | 98.96 — “& E1 s1 & 99.39 / n/r & 98.96 / n/r & 97.94 / 98.94 & 97.66 / 99.00 & 97.42 / 99.37 & 96.7” | 98.96 | 98.96 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.118` |
| `R1.supp-tab-appexpestimator.119` | 97.94 — “& E1 s1 & 99.39 / n/r & 98.96 / n/r & 97.94 / 98.94 & 97.66 / 99.00 & 97.42 / 99.37 & 96.7” | 97.94 | 97.94 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.119` |
| `R1.supp-tab-appexpestimator.120` | 98.94 — “& E1 s1 & 99.39 / n/r & 98.96 / n/r & 97.94 / 98.94 & 97.66 / 99.00 & 97.42 / 99.37 & 96.7” | 98.94 | 98.94 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.120` |
| `R1.supp-tab-appexpestimator.121` | 97.66 — “& E1 s1 & 99.39 / n/r & 98.96 / n/r & 97.94 / 98.94 & 97.66 / 99.00 & 97.42 / 99.37 & 96.7” | 97.66 | 97.66 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.121` |
| `R1.supp-tab-appexpestimator.122` | 99.00 — “& E1 s1 & 99.39 / n/r & 98.96 / n/r & 97.94 / 98.94 & 97.66 / 99.00 & 97.42 / 99.37 & 96.7” | 99.00 | 99.00 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.122` |
| `R1.supp-tab-appexpestimator.123` | 97.42 — “& E1 s1 & 99.39 / n/r & 98.96 / n/r & 97.94 / 98.94 & 97.66 / 99.00 & 97.42 / 99.37 & 96.7” | 97.42 | 97.42 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.123` |
| `R1.supp-tab-appexpestimator.124` | 99.37 — “& E1 s1 & 99.39 / n/r & 98.96 / n/r & 97.94 / 98.94 & 97.66 / 99.00 & 97.42 / 99.37 & 96.7” | 99.37 | 99.37 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.124` |
| `R1.supp-tab-appexpestimator.125` | 96.78 — “& E1 s1 & 99.39 / n/r & 98.96 / n/r & 97.94 / 98.94 & 97.66 / 99.00 & 97.42 / 99.37 & 96.7” | 96.78 | 96.78 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.125` |
| `R1.supp-tab-appexpestimator.126` | 99.39 — “& E1 s2 & 99.39 / 98.89 & 98.79 / n/r & 98.27 / n/r & 97.69 / 98.86 & 97.10 / n/r & 96.51 ” | 99.39 | 99.39 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.126` |
| `R1.supp-tab-appexpestimator.127` | 98.89 — “& E1 s2 & 99.39 / 98.89 & 98.79 / n/r & 98.27 / n/r & 97.69 / 98.86 & 97.10 / n/r & 96.51 ” | 98.89 | 98.89 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.127` |
| `R1.supp-tab-appexpestimator.128` | 98.79 — “& E1 s2 & 99.39 / 98.89 & 98.79 / n/r & 98.27 / n/r & 97.69 / 98.86 & 97.10 / n/r & 96.51 ” | 98.79 | 98.79 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.128` |
| `R1.supp-tab-appexpestimator.129` | 98.27 — “& E1 s2 & 99.39 / 98.89 & 98.79 / n/r & 98.27 / n/r & 97.69 / 98.86 & 97.10 / n/r & 96.51 ” | 98.27 | 98.27 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.129` |
| `R1.supp-tab-appexpestimator.130` | 97.69 — “& E1 s2 & 99.39 / 98.89 & 98.79 / n/r & 98.27 / n/r & 97.69 / 98.86 & 97.10 / n/r & 96.51 ” | 97.69 | 97.69 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.130` |
| `R1.supp-tab-appexpestimator.131` | 98.86 — “& E1 s2 & 99.39 / 98.89 & 98.79 / n/r & 98.27 / n/r & 97.69 / 98.86 & 97.10 / n/r & 96.51 ” | 98.86 | 98.86 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.131` |
| `R1.supp-tab-appexpestimator.132` | 97.10 — “& E1 s2 & 99.39 / 98.89 & 98.79 / n/r & 98.27 / n/r & 97.69 / 98.86 & 97.10 / n/r & 96.51 ” | 97.10 | 97.10 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.132` |
| `R1.supp-tab-appexpestimator.133` | 96.51 — “& E1 s2 & 99.39 / 98.89 & 98.79 / n/r & 98.27 / n/r & 97.69 / 98.86 & 97.10 / n/r & 96.51 ” | 96.51 | 96.51 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.133` |
| `R1.supp-tab-appexpestimator.134` | 99.72 — “& CAFRL as specified s42 & 99.72 / 98.09 & 97.31 / 98.06 & 96.55 / 97.40 & 95.25 / 98.70 &” | 99.72 | 99.72 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.134` |
| `R1.supp-tab-appexpestimator.135` | 98.09 — “& CAFRL as specified s42 & 99.72 / 98.09 & 97.31 / 98.06 & 96.55 / 97.40 & 95.25 / 98.70 &” | 98.09 | 98.09 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.135` |
| `R1.supp-tab-appexpestimator.136` | 97.31 — “& CAFRL as specified s42 & 99.72 / 98.09 & 97.31 / 98.06 & 96.55 / 97.40 & 95.25 / 98.70 &” | 97.31 | 97.31 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.136` |
| `R1.supp-tab-appexpestimator.137` | 98.06 — “& CAFRL as specified s42 & 99.72 / 98.09 & 97.31 / 98.06 & 96.55 / 97.40 & 95.25 / 98.70 &” | 98.06 | 98.06 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.137` |
| `R1.supp-tab-appexpestimator.138` | 96.55 — “& CAFRL as specified s42 & 99.72 / 98.09 & 97.31 / 98.06 & 96.55 / 97.40 & 95.25 / 98.70 &” | 96.55 | 96.55 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.138` |
| `R1.supp-tab-appexpestimator.139` | 97.40 — “& CAFRL as specified s42 & 99.72 / 98.09 & 97.31 / 98.06 & 96.55 / 97.40 & 95.25 / 98.70 &” | 97.40 | 97.40 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.139` |
| `R1.supp-tab-appexpestimator.140` | 95.25 — “& CAFRL as specified s42 & 99.72 / 98.09 & 97.31 / 98.06 & 96.55 / 97.40 & 95.25 / 98.70 &” | 95.25 | 95.25 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.140` |
| `R1.supp-tab-appexpestimator.141` | 98.70 — “& CAFRL as specified s42 & 99.72 / 98.09 & 97.31 / 98.06 & 96.55 / 97.40 & 95.25 / 98.70 &” | 98.70 | 98.70 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.141` |
| `R1.supp-tab-appexpestimator.142` | 96.57 — “& CAFRL as specified s42 & 99.72 / 98.09 & 97.31 / 98.06 & 96.55 / 97.40 & 95.25 / 98.70 &” | 96.57 | 96.57 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.142` |
| `R1.supp-tab-appexpestimator.143` | 94.22 — “& CAFRL as specified s42 & 99.72 / 98.09 & 97.31 / 98.06 & 96.55 / 97.40 & 95.25 / 98.70 &” | 94.22 | 94.22 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.143` |
| `R1.supp-tab-appexpestimator.144` | 92.41 — “& CAFRL as specified s42 & 99.72 / 98.09 & 97.31 / 98.06 & 96.55 / 97.40 & 95.25 / 98.70 &” | 92.41 | 92.41 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.144` |
| `R1.supp-tab-appexpestimator.145` | 92.41 — “& CAFRL as specified s42 & 99.72 / 98.09 & 97.31 / 98.06 & 96.55 / 97.40 & 95.25 / 98.70 &” | 92.41 | 92.41 | `revision-1/tables/e11_tables.json` | `python verify/claim.py R1.supp-tab-appexpestimator.145` |

## R1.supp-app-curriculum — Revision 1 — Supplementary Material, app:curriculum

*Supplementary Material, app:curriculum; `\label{app:curriculum}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-app-curriculum.1` | 13 — “its EMA weights collapsed (its raw weights kept their validation AUC); its epoch-13” | 13 | 13.00 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-app-curriculum.1` |
| `R1.supp-app-curriculum.2` | 10,000 — “source-identity clusters are resampled, $B = 10{,}000$; the registered rows” | 10000 | 10000.00 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-app-curriculum.2` |
| `R1.supp-app-curriculum.3` | 0.991 — “recur: V1's EMA validation AUC at epoch 14 was 0.991 / 0.917 at c23 / c40,” | 0.991 | 0.9906 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.3` |
| `R1.supp-app-curriculum.4` | 0.917 — “recur: V1's EMA validation AUC at epoch 14 was 0.991 / 0.917 at c23 / c40,” | 0.917 | 0.9173 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.4` |
| `R1.supp-app-curriculum.5` | 0.363 — “against 0.363 / the first run. CAFRL trained in bfloat16 is not” | 0.363 | 0.3633 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.5` |
| `R1.supp-app-curriculum.6` | 27 — “weights are the same (both epoch 27), so their raw@sel and raw-best rows are” | 27 | 27.00 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.6` |
| `R1.supp-app-curriculum.7` | 29 — “weights, selected epoch 29; trained all 30 epochs), reverting the training” | 29 | 29.00 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.7` |
| `R1.supp-app-curriculum.8` | -0.25 — “curriculum changed c40 AUC by $-0.25$\,pt against Fair-N (fixed-seed interval” | -0.25 | -0.2500 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.8` |
| `R1.supp-app-curriculum.9` | -1.16 — “\ci{-1.16}{0.68}; descriptive) and \auccomp{} by 0.004\,pt (\ci{-0.62}{0.67}).” | -1.16 | -1.1620 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.9` |
| `R1.supp-app-curriculum.10` | 0.68 — “\ci{-1.16}{0.68}; descriptive) and \auccomp{} by 0.004\,pt (\ci{-0.62}{0.67}).” | 0.68 | 0.6786 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.10` |
| `R1.supp-app-curriculum.11` | 0.004 — “\ci{-1.16}{0.68}; descriptive) and \auccomp{} by 0.004\,pt (\ci{-0.62}{0.67}).” | 0.004 | 0.0035 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.11` |
| `R1.supp-app-curriculum.12` | -0.62 — “\ci{-1.16}{0.68}; descriptive) and \auccomp{} by 0.004\,pt (\ci{-0.62}{0.67}).” | -0.62 | -0.6174 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.12` |
| `R1.supp-app-curriculum.13` | 0.67 — “\ci{-1.16}{0.68}; descriptive) and \auccomp{} by 0.004\,pt (\ci{-0.62}{0.67}).” | 0.67 | 0.6681 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.13` |
| `R1.supp-app-curriculum.14` | 29 — “weights at the EMA-selected epoch 29; trained all 30 epochs), reverting the” | 29 | 29.00 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.14` |
| `R1.supp-app-curriculum.15` | -0.22 — “training curriculum changed c40 AUC by $-0.22$\,pt against Fair-N (fixed-seed” | -0.22 | -0.2219 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.15` |
| `R1.supp-app-curriculum.16` | -1.15 — “interval \ci{-1.15}{0.73}; descriptive) and \auccomp{} by 0.03\,pt” | -1.15 | -1.1467 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.16` |
| `R1.supp-app-curriculum.17` | 0.73 — “interval \ci{-1.15}{0.73}; descriptive) and \auccomp{} by 0.03\,pt” | 0.73 | 0.7258 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.17` |
| `R1.supp-app-curriculum.18` | 0.03 — “interval \ci{-1.15}{0.73}; descriptive) and \auccomp{} by 0.03\,pt” | 0.03 | 0.0325 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.18` |
| `R1.supp-app-curriculum.19` | -0.59 — “(\ci{-0.59}{0.70}).” | -0.59 | -0.5934 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.19` |
| `R1.supp-app-curriculum.20` | 0.70 — “(\ci{-0.59}{0.70}).” | 0.70 | 0.7009 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.20` |
| `R1.supp-app-curriculum.21` | 28 — “weights, raw-selected epoch 28; trained all 30 epochs), reverting the” | 28 | 28.00 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.21` |
| `R1.supp-app-curriculum.22` | -0.26 — “training curriculum changed c40 AUC by $-0.26$\,pt against Fair-N (fixed-seed” | -0.26 | -0.2602 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.22` |
| `R1.supp-app-curriculum.23` | -1.16 — “interval \ci{-1.16}{0.66}; descriptive) and \auccomp{} by 0.02\,pt” | -1.16 | -1.1569 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.23` |
| `R1.supp-app-curriculum.24` | 0.66 — “interval \ci{-1.16}{0.66}; descriptive) and \auccomp{} by 0.02\,pt” | 0.66 | 0.6595 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.24` |
| `R1.supp-app-curriculum.25` | 0.02 — “interval \ci{-1.16}{0.66}; descriptive) and \auccomp{} by 0.02\,pt” | 0.02 | 0.0233 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.25` |
| `R1.supp-app-curriculum.26` | -0.60 — “(\ci{-0.60}{0.69}).” | -0.60 | -0.5995 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.26` |
| `R1.supp-app-curriculum.27` | 0.69 — “(\ci{-0.60}{0.69}).” | 0.69 | 0.6898 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.27` |
| `R1.supp-app-curriculum.28` | -0.36 — “c40 AUC by $-0.36$\,pt against Fair-N (fixed-seed interval \ci{-1.22}{0.46};” | -0.36 | -0.3622 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.28` |
| `R1.supp-app-curriculum.29` | -1.22 — “c40 AUC by $-0.36$\,pt against Fair-N (fixed-seed interval \ci{-1.22}{0.46};” | -1.22 | -1.2207 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.29` |
| `R1.supp-app-curriculum.30` | 0.46 — “c40 AUC by $-0.36$\,pt against Fair-N (fixed-seed interval \ci{-1.22}{0.46};” | 0.46 | 0.4605 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.30` |
| `R1.supp-app-curriculum.31` | -0.05 — “descriptive) and \auccomp{} by $-0.05$\,pt (\ci{-0.64}{0.54}).” | -0.05 | -0.0504 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.31` |
| `R1.supp-app-curriculum.32` | -0.64 — “descriptive) and \auccomp{} by $-0.05$\,pt (\ci{-0.64}{0.54}).” | -0.64 | -0.6365 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.32` |
| `R1.supp-app-curriculum.33` | 0.54 — “descriptive) and \auccomp{} by $-0.05$\,pt (\ci{-0.64}{0.54}).” | 0.54 | 0.5424 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.33` |
| `R1.supp-app-curriculum.34` | 27 — “stop (seed 42; raw weights at the EMA-selected epoch 27; the divergence” | 27 | 27.00 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.34` |
| `R1.supp-app-curriculum.35` | -0.41 — “changed c40 AUC by $-0.41$\,pt against Fair-N (fixed-seed interval” | -0.41 | -0.4145 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.35` |
| `R1.supp-app-curriculum.36` | -1.28 — “\ci{-1.28}{0.44}; descriptive) and \auccomp{} by $-0.11$\,pt” | -1.28 | -1.2795 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.36` |
| `R1.supp-app-curriculum.37` | 0.44 — “\ci{-1.28}{0.44}; descriptive) and \auccomp{} by $-0.11$\,pt” | 0.44 | 0.4376 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.37` |
| `R1.supp-app-curriculum.38` | -0.11 — “\ci{-1.28}{0.44}; descriptive) and \auccomp{} by $-0.11$\,pt” | -0.11 | -0.1126 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.38` |
| `R1.supp-app-curriculum.39` | -0.73 — “(\ci{-0.73}{0.52}).” | -0.73 | -0.7341 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.39` |
| `R1.supp-app-curriculum.40` | 0.52 — “(\ci{-0.73}{0.52}).” | 0.52 | 0.5242 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.40` |
| `R1.supp-app-curriculum.41` | 27 — “stop (seed 42; raw weights, raw-selected epoch 27; the divergence rule was” | 27 | 27.00 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.41` |
| `R1.supp-app-curriculum.42` | -0.41 — “c40 AUC by $-0.41$\,pt against Fair-N (fixed-seed interval \ci{-1.28}{0.44};” | -0.41 | -0.4145 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.42` |
| `R1.supp-app-curriculum.43` | -1.28 — “c40 AUC by $-0.41$\,pt against Fair-N (fixed-seed interval \ci{-1.28}{0.44};” | -1.28 | -1.2795 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.43` |
| `R1.supp-app-curriculum.44` | 0.44 — “c40 AUC by $-0.41$\,pt against Fair-N (fixed-seed interval \ci{-1.28}{0.44};” | 0.44 | 0.4376 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.44` |
| `R1.supp-app-curriculum.45` | -0.11 — “descriptive) and \auccomp{} by $-0.11$\,pt (\ci{-0.73}{0.52}).” | -0.11 | -0.1126 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.45` |
| `R1.supp-app-curriculum.46` | -0.73 — “descriptive) and \auccomp{} by $-0.11$\,pt (\ci{-0.73}{0.52}).” | -0.73 | -0.7341 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.46` |
| `R1.supp-app-curriculum.47` | 0.52 — “descriptive) and \auccomp{} by $-0.11$\,pt (\ci{-0.73}{0.52}).” | 0.52 | 0.5242 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.47` |
| `R1.supp-app-curriculum.48` | 27 — “its own batch-norm statistics (seed 42; EMA weights, selected epoch 27; trained” | 27 | 27.00 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.48` |
| `R1.supp-app-curriculum.49` | -0.69 — “$-0.69$\,pt against Fair-N (fixed-seed interval \ci{-1.63}{0.21};” | -0.69 | -0.6901 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.49` |
| `R1.supp-app-curriculum.50` | -1.63 — “$-0.69$\,pt against Fair-N (fixed-seed interval \ci{-1.63}{0.21};” | -1.63 | -1.6263 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.50` |
| `R1.supp-app-curriculum.51` | 0.21 — “$-0.69$\,pt against Fair-N (fixed-seed interval \ci{-1.63}{0.21};” | 0.21 | 0.2092 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.51` |
| `R1.supp-app-curriculum.52` | -0.22 — “descriptive) and \auccomp{} by $-0.22$\,pt (\ci{-0.86}{0.42}).” | -0.22 | -0.2235 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.52` |
| `R1.supp-app-curriculum.53` | -0.86 — “descriptive) and \auccomp{} by $-0.22$\,pt (\ci{-0.86}{0.42}).” | -0.86 | -0.8623 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.53` |
| `R1.supp-app-curriculum.54` | 0.42 — “descriptive) and \auccomp{} by $-0.22$\,pt (\ci{-0.86}{0.42}).” | 0.42 | 0.4187 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.54` |
| `R1.supp-app-curriculum.55` | 27 — “its own batch-norm statistics (seed 42; raw weights at the EMA-selected epoch 27;” | 27 | 27.00 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.55` |
| `R1.supp-app-curriculum.56` | -0.80 — “$-0.80$\,pt against Fair-N (fixed-seed interval \ci{-1.78}{0.10};” | -0.80 | -0.8048 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.56` |
| `R1.supp-app-curriculum.57` | -1.78 — “$-0.80$\,pt against Fair-N (fixed-seed interval \ci{-1.78}{0.10};” | -1.78 | -1.7755 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.57` |
| `R1.supp-app-curriculum.58` | 0.10 — “$-0.80$\,pt against Fair-N (fixed-seed interval \ci{-1.78}{0.10};” | 0.10 | 0.0970 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.58` |
| `R1.supp-app-curriculum.59` | -0.34 — “descriptive) and \auccomp{} by $-0.34$\,pt (\ci{-1.01}{0.32}).” | -0.34 | -0.3351 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.59` |
| `R1.supp-app-curriculum.60` | -1.01 — “descriptive) and \auccomp{} by $-0.34$\,pt (\ci{-1.01}{0.32}).” | -1.01 | -1.0099 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.60` |
| `R1.supp-app-curriculum.61` | 0.32 — “descriptive) and \auccomp{} by $-0.34$\,pt (\ci{-1.01}{0.32}).” | 0.32 | 0.3195 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.61` |
| `R1.supp-app-curriculum.62` | 27 — “its own batch-norm statistics (seed 42; raw weights, raw-selected epoch 27;” | 27 | 27.00 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.62` |
| `R1.supp-app-curriculum.63` | -0.80 — “$-0.80$\,pt against Fair-N (fixed-seed interval \ci{-1.78}{0.10};” | -0.80 | -0.8048 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.63` |
| `R1.supp-app-curriculum.64` | -1.78 — “$-0.80$\,pt against Fair-N (fixed-seed interval \ci{-1.78}{0.10};” | -1.78 | -1.7755 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.64` |
| `R1.supp-app-curriculum.65` | 0.10 — “$-0.80$\,pt against Fair-N (fixed-seed interval \ci{-1.78}{0.10};” | 0.10 | 0.0970 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.65` |
| `R1.supp-app-curriculum.66` | -0.34 — “descriptive) and \auccomp{} by $-0.34$\,pt (\ci{-1.01}{0.32}).” | -0.34 | -0.3351 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.66` |
| `R1.supp-app-curriculum.67` | -1.01 — “descriptive) and \auccomp{} by $-0.34$\,pt (\ci{-1.01}{0.32}).” | -1.01 | -1.0099 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.67` |
| `R1.supp-app-curriculum.68` | 0.32 — “descriptive) and \auccomp{} by $-0.34$\,pt (\ci{-1.01}{0.32}).” | 0.32 | 0.3195 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-app-curriculum.68` |

- `R1.supp-app-curriculum.1` — weights: EMA
- `R1.supp-app-curriculum.3` — weights: EMA (logged validation)
- `R1.supp-app-curriculum.4` — weights: EMA (logged validation)
- `R1.supp-app-curriculum.5` — weights: EMA (logged validation)
- `R1.supp-app-curriculum.6` — weights: EMA (post hoc)
- `R1.supp-app-curriculum.7` — weights: EMA
- `R1.supp-app-curriculum.8` — weights: EMA
- `R1.supp-app-curriculum.10` — weights: EMA
- `R1.supp-app-curriculum.14` — weights: raw@sel
- `R1.supp-app-curriculum.15` — weights: raw@sel
- `R1.supp-app-curriculum.16` — weights: raw@sel
- `R1.supp-app-curriculum.17` — weights: raw@sel
- `R1.supp-app-curriculum.18` — weights: raw@sel
- `R1.supp-app-curriculum.19` — weights: raw@sel
- `R1.supp-app-curriculum.20` — weights: raw@sel
- `R1.supp-app-curriculum.21` — weights: raw-best
- `R1.supp-app-curriculum.22` — weights: raw-best
- `R1.supp-app-curriculum.23` — weights: raw-best
- `R1.supp-app-curriculum.24` — weights: raw-best
- `R1.supp-app-curriculum.25` — weights: raw-best
- `R1.supp-app-curriculum.26` — weights: raw-best
- `R1.supp-app-curriculum.27` — weights: raw-best
- `R1.supp-app-curriculum.28` — weights: EMA (post hoc)
- `R1.supp-app-curriculum.29` — weights: EMA (post hoc)
- `R1.supp-app-curriculum.30` — weights: EMA (post hoc)
- `R1.supp-app-curriculum.31` — weights: EMA (post hoc)
- `R1.supp-app-curriculum.32` — weights: EMA (post hoc)
- `R1.supp-app-curriculum.33` — weights: EMA (post hoc)
- `R1.supp-app-curriculum.34` — weights: raw@sel (post hoc)
- `R1.supp-app-curriculum.35` — weights: raw@sel (post hoc)
- `R1.supp-app-curriculum.36` — weights: raw@sel (post hoc)
- `R1.supp-app-curriculum.37` — weights: raw@sel (post hoc)
- `R1.supp-app-curriculum.38` — weights: raw@sel (post hoc)
- `R1.supp-app-curriculum.39` — weights: raw@sel (post hoc)
- `R1.supp-app-curriculum.40` — weights: raw@sel (post hoc)
- `R1.supp-app-curriculum.41` — weights: raw-best (post hoc)
- `R1.supp-app-curriculum.42` — weights: raw-best (post hoc)
- `R1.supp-app-curriculum.43` — weights: raw-best (post hoc)
- `R1.supp-app-curriculum.44` — weights: raw-best (post hoc)
- `R1.supp-app-curriculum.45` — weights: raw-best (post hoc)
- `R1.supp-app-curriculum.46` — weights: raw-best (post hoc)
- `R1.supp-app-curriculum.47` — weights: raw-best (post hoc)
- `R1.supp-app-curriculum.48` — weights: EMA (post hoc)
- `R1.supp-app-curriculum.49` — weights: EMA (post hoc)
- `R1.supp-app-curriculum.50` — weights: EMA (post hoc)
- `R1.supp-app-curriculum.51` — weights: EMA (post hoc)
- `R1.supp-app-curriculum.52` — weights: EMA (post hoc)
- `R1.supp-app-curriculum.53` — weights: EMA (post hoc)
- `R1.supp-app-curriculum.54` — weights: EMA (post hoc)
- `R1.supp-app-curriculum.55` — weights: raw@sel (post hoc)
- `R1.supp-app-curriculum.56` — weights: raw@sel (post hoc)
- `R1.supp-app-curriculum.57` — weights: raw@sel (post hoc)
- `R1.supp-app-curriculum.58` — weights: raw@sel (post hoc)
- `R1.supp-app-curriculum.59` — weights: raw@sel (post hoc)
- `R1.supp-app-curriculum.60` — weights: raw@sel (post hoc)
- `R1.supp-app-curriculum.61` — weights: raw@sel (post hoc)
- `R1.supp-app-curriculum.62` — weights: raw-best (post hoc)
- `R1.supp-app-curriculum.63` — weights: raw-best (post hoc)
- `R1.supp-app-curriculum.64` — weights: raw-best (post hoc)
- `R1.supp-app-curriculum.65` — weights: raw-best (post hoc)
- `R1.supp-app-curriculum.66` — weights: raw-best (post hoc)
- `R1.supp-app-curriculum.67` — weights: raw-best (post hoc)
- `R1.supp-app-curriculum.68` — weights: raw-best (post hoc)

## R1.supp-tab-appcurriculum — Revision 1 — Supplementary Material, tab:appcurriculum

*Supplementary Material, tab:appcurriculum; `\label{tab:appcurriculum}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-tab-appcurriculum.1` | 10,000 — “source-identity clusters, $B = 10{,}000$). Weights: EMA, the registered” | 10000 | 10000.00 | `revision-1/recompute.json` | `python verify/claim.py R1.supp-tab-appcurriculum.1` |
| `R1.supp-tab-appcurriculum.2` | 95.86 — “Fair-N, seed 42 (reference; registered) & EMA & --- & --- & 95.86 & 97.14 & --- & --- \\” | 95.86 | 95.86 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.supp-tab-appcurriculum.2` |
| `R1.supp-tab-appcurriculum.3` | 97.14 — “Fair-N, seed 42 (reference; registered) & EMA & --- & --- & 95.86 & 97.14 & --- & --- \\” | 97.14 | 97.14 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.supp-tab-appcurriculum.3` |
| `R1.supp-tab-appcurriculum.4` | 13 — “& EMA & 13 & stopped at epoch 14 (divergence) & 93.51 & 96.99 & $-2.35$ \ci{-4.25}{-0.52} ” | 13 | 13.00 | `revision-1/stats/secondaries.null.json` | `python verify/claim.py R1.supp-tab-appcurriculum.4` |
| `R1.supp-tab-appcurriculum.5` | 93.51 — “& EMA & 13 & stopped at epoch 14 (divergence) & 93.51 & 96.99 & $-2.35$ \ci{-4.25}{-0.52} ” | 93.51 | 93.51 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.supp-tab-appcurriculum.5` |
| `R1.supp-tab-appcurriculum.6` | 96.99 — “& EMA & 13 & stopped at epoch 14 (divergence) & 93.51 & 96.99 & $-2.35$ \ci{-4.25}{-0.52} ” | 96.99 | 96.99 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.supp-tab-appcurriculum.6` |
| `R1.supp-tab-appcurriculum.7` | -2.35 — “& EMA & 13 & stopped at epoch 14 (divergence) & 93.51 & 96.99 & $-2.35$ \ci{-4.25}{-0.52} ” | -2.35 | -2.3469 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.supp-tab-appcurriculum.7` |
| `R1.supp-tab-appcurriculum.8` | -4.25 — “& EMA & 13 & stopped at epoch 14 (divergence) & 93.51 & 96.99 & $-2.35$ \ci{-4.25}{-0.52} ” | -4.25 | -4.2462 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.supp-tab-appcurriculum.8` |
| `R1.supp-tab-appcurriculum.9` | -0.52 — “& EMA & 13 & stopped at epoch 14 (divergence) & 93.51 & 96.99 & $-2.35$ \ci{-4.25}{-0.52} ” | -0.52 | -0.5217 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.supp-tab-appcurriculum.9` |
| `R1.supp-tab-appcurriculum.10` | -0.15 — “& EMA & 13 & stopped at epoch 14 (divergence) & 93.51 & 96.99 & $-2.35$ \ci{-4.25}{-0.52} ” | -0.15 | -0.1508 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.supp-tab-appcurriculum.10` |
| `R1.supp-tab-appcurriculum.11` | -1.00 — “& EMA & 13 & stopped at epoch 14 (divergence) & 93.51 & 96.99 & $-2.35$ \ci{-4.25}{-0.52} ” | -1.00 | -1.0000 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.supp-tab-appcurriculum.11` |
| `R1.supp-tab-appcurriculum.12` | 0.70 — “& EMA & 13 & stopped at epoch 14 (divergence) & 93.51 & 96.99 & $-2.35$ \ci{-4.25}{-0.52} ” | 0.70 | 0.7044 | `revision-1/stats/e13_descriptive.json` | `python verify/claim.py R1.supp-tab-appcurriculum.12` |
| `R1.supp-tab-appcurriculum.13` | 29 — “V1, identical re-run (reported run) & EMA & 29 & all 30 epochs & 95.61 & 97.14 & $-0.25$ \” | 29 | 29.00 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.13` |
| `R1.supp-tab-appcurriculum.14` | 95.61 — “V1, identical re-run (reported run) & EMA & 29 & all 30 epochs & 95.61 & 97.14 & $-0.25$ \” | 95.61 | 95.61 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.14` |
| `R1.supp-tab-appcurriculum.15` | 97.14 — “V1, identical re-run (reported run) & EMA & 29 & all 30 epochs & 95.61 & 97.14 & $-0.25$ \” | 97.14 | 97.14 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.15` |
| `R1.supp-tab-appcurriculum.16` | -0.25 — “V1, identical re-run (reported run) & EMA & 29 & all 30 epochs & 95.61 & 97.14 & $-0.25$ \” | -0.25 | -0.2500 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.16` |
| `R1.supp-tab-appcurriculum.17` | -1.16 — “V1, identical re-run (reported run) & EMA & 29 & all 30 epochs & 95.61 & 97.14 & $-0.25$ \” | -1.16 | -1.1620 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.17` |
| `R1.supp-tab-appcurriculum.18` | 0.68 — “V1, identical re-run (reported run) & EMA & 29 & all 30 epochs & 95.61 & 97.14 & $-0.25$ \” | 0.68 | 0.6786 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.18` |
| `R1.supp-tab-appcurriculum.19` | 0.004 — “V1, identical re-run (reported run) & EMA & 29 & all 30 epochs & 95.61 & 97.14 & $-0.25$ \” | 0.004 | 0.0035 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.19` |
| `R1.supp-tab-appcurriculum.20` | -0.62 — “V1, identical re-run (reported run) & EMA & 29 & all 30 epochs & 95.61 & 97.14 & $-0.25$ \” | -0.62 | -0.6174 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.20` |
| `R1.supp-tab-appcurriculum.21` | 0.67 — “V1, identical re-run (reported run) & EMA & 29 & all 30 epochs & 95.61 & 97.14 & $-0.25$ \” | 0.67 | 0.6681 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.21` |
| `R1.supp-tab-appcurriculum.22` | 29 — “V1, identical re-run & raw@sel & 29 & all 30 epochs & 95.64 & 97.17 & $-0.22$ \ci{-1.15}{0” | 29 | 29.00 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.22` |
| `R1.supp-tab-appcurriculum.23` | 95.64 — “V1, identical re-run & raw@sel & 29 & all 30 epochs & 95.64 & 97.17 & $-0.22$ \ci{-1.15}{0” | 95.64 | 95.64 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.23` |
| `R1.supp-tab-appcurriculum.24` | 97.17 — “V1, identical re-run & raw@sel & 29 & all 30 epochs & 95.64 & 97.17 & $-0.22$ \ci{-1.15}{0” | 97.17 | 97.17 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.24` |
| `R1.supp-tab-appcurriculum.25` | -0.22 — “V1, identical re-run & raw@sel & 29 & all 30 epochs & 95.64 & 97.17 & $-0.22$ \ci{-1.15}{0” | -0.22 | -0.2219 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.25` |
| `R1.supp-tab-appcurriculum.26` | -1.15 — “V1, identical re-run & raw@sel & 29 & all 30 epochs & 95.64 & 97.17 & $-0.22$ \ci{-1.15}{0” | -1.15 | -1.1467 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.26` |
| `R1.supp-tab-appcurriculum.27` | 0.73 — “V1, identical re-run & raw@sel & 29 & all 30 epochs & 95.64 & 97.17 & $-0.22$ \ci{-1.15}{0” | 0.73 | 0.7258 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.27` |
| `R1.supp-tab-appcurriculum.28` | 0.03 — “V1, identical re-run & raw@sel & 29 & all 30 epochs & 95.64 & 97.17 & $-0.22$ \ci{-1.15}{0” | 0.03 | 0.0325 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.28` |
| `R1.supp-tab-appcurriculum.29` | -0.59 — “V1, identical re-run & raw@sel & 29 & all 30 epochs & 95.64 & 97.17 & $-0.22$ \ci{-1.15}{0” | -0.59 | -0.5934 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.29` |
| `R1.supp-tab-appcurriculum.30` | 0.70 — “V1, identical re-run & raw@sel & 29 & all 30 epochs & 95.64 & 97.17 & $-0.22$ \ci{-1.15}{0” | 0.70 | 0.7009 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.30` |
| `R1.supp-tab-appcurriculum.31` | 28 — “V1, identical re-run & raw-best & 28 & all 30 epochs & 95.60 & 97.16 & $-0.26$ \ci{-1.16}{” | 28 | 28.00 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.31` |
| `R1.supp-tab-appcurriculum.32` | 95.60 — “V1, identical re-run & raw-best & 28 & all 30 epochs & 95.60 & 97.16 & $-0.26$ \ci{-1.16}{” | 95.60 | 95.60 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.32` |
| `R1.supp-tab-appcurriculum.33` | 97.16 — “V1, identical re-run & raw-best & 28 & all 30 epochs & 95.60 & 97.16 & $-0.26$ \ci{-1.16}{” | 97.16 | 97.16 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.33` |
| `R1.supp-tab-appcurriculum.34` | -0.26 — “V1, identical re-run & raw-best & 28 & all 30 epochs & 95.60 & 97.16 & $-0.26$ \ci{-1.16}{” | -0.26 | -0.2602 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.34` |
| `R1.supp-tab-appcurriculum.35` | -1.16 — “V1, identical re-run & raw-best & 28 & all 30 epochs & 95.60 & 97.16 & $-0.26$ \ci{-1.16}{” | -1.16 | -1.1569 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.35` |
| `R1.supp-tab-appcurriculum.36` | 0.66 — “V1, identical re-run & raw-best & 28 & all 30 epochs & 95.60 & 97.16 & $-0.26$ \ci{-1.16}{” | 0.66 | 0.6595 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.36` |
| `R1.supp-tab-appcurriculum.37` | 0.02 — “V1, identical re-run & raw-best & 28 & all 30 epochs & 95.60 & 97.16 & $-0.26$ \ci{-1.16}{” | 0.02 | 0.0233 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.37` |
| `R1.supp-tab-appcurriculum.38` | -0.60 — “V1, identical re-run & raw-best & 28 & all 30 epochs & 95.60 & 97.16 & $-0.26$ \ci{-1.16}{” | -0.60 | -0.5995 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.38` |
| `R1.supp-tab-appcurriculum.39` | 0.69 — “V1, identical re-run & raw-best & 28 & all 30 epochs & 95.60 & 97.16 & $-0.26$ \ci{-1.16}{” | 0.69 | 0.6898 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.39` |
| `R1.supp-tab-appcurriculum.40` | 27 — “V2, without the divergence stop (post hoc) & EMA & 27 & divergence rule never met; all 30 ” | 27 | 27.00 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.40` |
| `R1.supp-tab-appcurriculum.41` | 95.50 — “V2, without the divergence stop (post hoc) & EMA & 27 & divergence rule never met; all 30 ” | 95.50 | 95.50 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.41` |
| `R1.supp-tab-appcurriculum.42` | 97.09 — “V2, without the divergence stop (post hoc) & EMA & 27 & divergence rule never met; all 30 ” | 97.09 | 97.09 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.42` |
| `R1.supp-tab-appcurriculum.43` | -0.36 — “V2, without the divergence stop (post hoc) & EMA & 27 & divergence rule never met; all 30 ” | -0.36 | -0.3622 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.43` |
| `R1.supp-tab-appcurriculum.44` | -1.22 — “V2, without the divergence stop (post hoc) & EMA & 27 & divergence rule never met; all 30 ” | -1.22 | -1.2207 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.44` |
| `R1.supp-tab-appcurriculum.45` | 0.46 — “V2, without the divergence stop (post hoc) & EMA & 27 & divergence rule never met; all 30 ” | 0.46 | 0.4605 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.45` |
| `R1.supp-tab-appcurriculum.46` | -0.05 — “V2, without the divergence stop (post hoc) & EMA & 27 & divergence rule never met; all 30 ” | -0.05 | -0.0504 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.46` |
| `R1.supp-tab-appcurriculum.47` | -0.64 — “V2, without the divergence stop (post hoc) & EMA & 27 & divergence rule never met; all 30 ” | -0.64 | -0.6365 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.47` |
| `R1.supp-tab-appcurriculum.48` | 0.54 — “V2, without the divergence stop (post hoc) & EMA & 27 & divergence rule never met; all 30 ” | 0.54 | 0.5424 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.48` |
| `R1.supp-tab-appcurriculum.49` | 27 — “V2, without the divergence stop (post hoc) & raw@sel & 27 & divergence rule never met; all” | 27 | 27.00 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.49` |
| `R1.supp-tab-appcurriculum.50` | 95.44 — “V2, without the divergence stop (post hoc) & raw@sel & 27 & divergence rule never met; all” | 95.44 | 95.44 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.50` |
| `R1.supp-tab-appcurriculum.51` | 97.03 — “V2, without the divergence stop (post hoc) & raw@sel & 27 & divergence rule never met; all” | 97.03 | 97.03 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.51` |
| `R1.supp-tab-appcurriculum.52` | -0.41 — “V2, without the divergence stop (post hoc) & raw@sel & 27 & divergence rule never met; all” | -0.41 | -0.4145 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.52` |
| `R1.supp-tab-appcurriculum.53` | -1.28 — “V2, without the divergence stop (post hoc) & raw@sel & 27 & divergence rule never met; all” | -1.28 | -1.2795 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.53` |
| `R1.supp-tab-appcurriculum.54` | 0.44 — “V2, without the divergence stop (post hoc) & raw@sel & 27 & divergence rule never met; all” | 0.44 | 0.4376 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.54` |
| `R1.supp-tab-appcurriculum.55` | -0.11 — “V2, without the divergence stop (post hoc) & raw@sel & 27 & divergence rule never met; all” | -0.11 | -0.1126 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.55` |
| `R1.supp-tab-appcurriculum.56` | -0.73 — “V2, without the divergence stop (post hoc) & raw@sel & 27 & divergence rule never met; all” | -0.73 | -0.7341 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.56` |
| `R1.supp-tab-appcurriculum.57` | 0.52 — “V2, without the divergence stop (post hoc) & raw@sel & 27 & divergence rule never met; all” | 0.52 | 0.5242 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.57` |
| `R1.supp-tab-appcurriculum.58` | 27 — “V2, without the divergence stop (post hoc) & raw-best & 27 & divergence rule never met; al” | 27 | 27.00 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.58` |
| `R1.supp-tab-appcurriculum.59` | 95.44 — “V2, without the divergence stop (post hoc) & raw-best & 27 & divergence rule never met; al” | 95.44 | 95.44 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.59` |
| `R1.supp-tab-appcurriculum.60` | 97.03 — “V2, without the divergence stop (post hoc) & raw-best & 27 & divergence rule never met; al” | 97.03 | 97.03 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.60` |
| `R1.supp-tab-appcurriculum.61` | -0.41 — “V2, without the divergence stop (post hoc) & raw-best & 27 & divergence rule never met; al” | -0.41 | -0.4145 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.61` |
| `R1.supp-tab-appcurriculum.62` | -1.28 — “V2, without the divergence stop (post hoc) & raw-best & 27 & divergence rule never met; al” | -1.28 | -1.2795 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.62` |
| `R1.supp-tab-appcurriculum.63` | 0.44 — “V2, without the divergence stop (post hoc) & raw-best & 27 & divergence rule never met; al” | 0.44 | 0.4376 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.63` |
| `R1.supp-tab-appcurriculum.64` | -0.11 — “V2, without the divergence stop (post hoc) & raw-best & 27 & divergence rule never met; al” | -0.11 | -0.1126 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.64` |
| `R1.supp-tab-appcurriculum.65` | -0.73 — “V2, without the divergence stop (post hoc) & raw-best & 27 & divergence rule never met; al” | -0.73 | -0.7341 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.65` |
| `R1.supp-tab-appcurriculum.66` | 0.52 — “V2, without the divergence stop (post hoc) & raw-best & 27 & divergence rule never met; al” | 0.52 | 0.5242 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.66` |
| `R1.supp-tab-appcurriculum.67` | 27 — “V3, EMA keeps its own batch-norm statistics (post hoc) & EMA & 27 & all 30 epochs & 95.17 ” | 27 | 27.00 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.67` |
| `R1.supp-tab-appcurriculum.68` | 95.17 — “V3, EMA keeps its own batch-norm statistics (post hoc) & EMA & 27 & all 30 epochs & 95.17 ” | 95.17 | 95.17 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.68` |
| `R1.supp-tab-appcurriculum.69` | 96.92 — “V3, EMA keeps its own batch-norm statistics (post hoc) & EMA & 27 & all 30 epochs & 95.17 ” | 96.92 | 96.92 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.69` |
| `R1.supp-tab-appcurriculum.70` | -0.69 — “V3, EMA keeps its own batch-norm statistics (post hoc) & EMA & 27 & all 30 epochs & 95.17 ” | -0.69 | -0.6901 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.70` |
| `R1.supp-tab-appcurriculum.71` | -1.63 — “V3, EMA keeps its own batch-norm statistics (post hoc) & EMA & 27 & all 30 epochs & 95.17 ” | -1.63 | -1.6263 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.71` |
| `R1.supp-tab-appcurriculum.72` | 0.21 — “V3, EMA keeps its own batch-norm statistics (post hoc) & EMA & 27 & all 30 epochs & 95.17 ” | 0.21 | 0.2092 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.72` |
| `R1.supp-tab-appcurriculum.73` | -0.22 — “V3, EMA keeps its own batch-norm statistics (post hoc) & EMA & 27 & all 30 epochs & 95.17 ” | -0.22 | -0.2235 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.73` |
| `R1.supp-tab-appcurriculum.74` | -0.86 — “V3, EMA keeps its own batch-norm statistics (post hoc) & EMA & 27 & all 30 epochs & 95.17 ” | -0.86 | -0.8623 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.74` |
| `R1.supp-tab-appcurriculum.75` | 0.42 — “V3, EMA keeps its own batch-norm statistics (post hoc) & EMA & 27 & all 30 epochs & 95.17 ” | 0.42 | 0.4187 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.75` |
| `R1.supp-tab-appcurriculum.76` | 27 — “V3, EMA keeps its own batch-norm statistics (post hoc) & raw@sel & 27 & all 30 epochs & 95” | 27 | 27.00 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.76` |
| `R1.supp-tab-appcurriculum.77` | 95.05 — “V3, EMA keeps its own batch-norm statistics (post hoc) & raw@sel & 27 & all 30 epochs & 95” | 95.05 | 95.05 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.77` |
| `R1.supp-tab-appcurriculum.78` | 96.80 — “V3, EMA keeps its own batch-norm statistics (post hoc) & raw@sel & 27 & all 30 epochs & 95” | 96.80 | 96.80 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.78` |
| `R1.supp-tab-appcurriculum.79` | -0.80 — “V3, EMA keeps its own batch-norm statistics (post hoc) & raw@sel & 27 & all 30 epochs & 95” | -0.80 | -0.8048 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.79` |
| `R1.supp-tab-appcurriculum.80` | -1.78 — “V3, EMA keeps its own batch-norm statistics (post hoc) & raw@sel & 27 & all 30 epochs & 95” | -1.78 | -1.7755 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.80` |
| `R1.supp-tab-appcurriculum.81` | 0.10 — “V3, EMA keeps its own batch-norm statistics (post hoc) & raw@sel & 27 & all 30 epochs & 95” | 0.10 | 0.0970 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.81` |
| `R1.supp-tab-appcurriculum.82` | -0.34 — “V3, EMA keeps its own batch-norm statistics (post hoc) & raw@sel & 27 & all 30 epochs & 95” | -0.34 | -0.3351 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.82` |
| `R1.supp-tab-appcurriculum.83` | -1.01 — “V3, EMA keeps its own batch-norm statistics (post hoc) & raw@sel & 27 & all 30 epochs & 95” | -1.01 | -1.0099 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.83` |
| `R1.supp-tab-appcurriculum.84` | 0.32 — “V3, EMA keeps its own batch-norm statistics (post hoc) & raw@sel & 27 & all 30 epochs & 95” | 0.32 | 0.3195 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.84` |
| `R1.supp-tab-appcurriculum.85` | 27 — “V3, EMA keeps its own batch-norm statistics (post hoc) & raw-best & 27 & all 30 epochs & 9” | 27 | 27.00 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.85` |
| `R1.supp-tab-appcurriculum.86` | 95.05 — “V3, EMA keeps its own batch-norm statistics (post hoc) & raw-best & 27 & all 30 epochs & 9” | 95.05 | 95.05 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.86` |
| `R1.supp-tab-appcurriculum.87` | 96.80 — “V3, EMA keeps its own batch-norm statistics (post hoc) & raw-best & 27 & all 30 epochs & 9” | 96.80 | 96.80 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.87` |
| `R1.supp-tab-appcurriculum.88` | -0.80 — “V3, EMA keeps its own batch-norm statistics (post hoc) & raw-best & 27 & all 30 epochs & 9” | -0.80 | -0.8048 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.88` |
| `R1.supp-tab-appcurriculum.89` | -1.78 — “V3, EMA keeps its own batch-norm statistics (post hoc) & raw-best & 27 & all 30 epochs & 9” | -1.78 | -1.7755 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.89` |
| `R1.supp-tab-appcurriculum.90` | 0.10 — “V3, EMA keeps its own batch-norm statistics (post hoc) & raw-best & 27 & all 30 epochs & 9” | 0.10 | 0.0970 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.90` |
| `R1.supp-tab-appcurriculum.91` | -0.34 — “V3, EMA keeps its own batch-norm statistics (post hoc) & raw-best & 27 & all 30 epochs & 9” | -0.34 | -0.3351 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.91` |
| `R1.supp-tab-appcurriculum.92` | -1.01 — “V3, EMA keeps its own batch-norm statistics (post hoc) & raw-best & 27 & all 30 epochs & 9” | -1.01 | -1.0099 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.92` |
| `R1.supp-tab-appcurriculum.93` | 0.32 — “V3, EMA keeps its own batch-norm statistics (post hoc) & raw-best & 27 & all 30 epochs & 9” | 0.32 | 0.3195 | `revision-1/curriculum/analysis.json` | `python verify/claim.py R1.supp-tab-appcurriculum.93` |

- `R1.supp-tab-appcurriculum.2` — weights: EMA
- `R1.supp-tab-appcurriculum.3` — weights: EMA
- `R1.supp-tab-appcurriculum.4` — weights: EMA
- `R1.supp-tab-appcurriculum.5` — weights: EMA
- `R1.supp-tab-appcurriculum.6` — weights: EMA
- `R1.supp-tab-appcurriculum.7` — weights: EMA
- `R1.supp-tab-appcurriculum.8` — weights: EMA
- `R1.supp-tab-appcurriculum.9` — weights: EMA
- `R1.supp-tab-appcurriculum.10` — weights: EMA
- `R1.supp-tab-appcurriculum.11` — weights: EMA
- `R1.supp-tab-appcurriculum.12` — weights: EMA
- `R1.supp-tab-appcurriculum.13` — weights: EMA
- `R1.supp-tab-appcurriculum.14` — weights: EMA
- `R1.supp-tab-appcurriculum.15` — weights: EMA
- `R1.supp-tab-appcurriculum.16` — weights: EMA
- `R1.supp-tab-appcurriculum.22` — weights: raw@sel
- `R1.supp-tab-appcurriculum.23` — weights: raw@sel
- `R1.supp-tab-appcurriculum.24` — weights: raw@sel
- `R1.supp-tab-appcurriculum.25` — weights: raw@sel
- `R1.supp-tab-appcurriculum.26` — weights: raw@sel
- `R1.supp-tab-appcurriculum.27` — weights: raw@sel
- `R1.supp-tab-appcurriculum.28` — weights: raw@sel
- `R1.supp-tab-appcurriculum.29` — weights: raw@sel
- `R1.supp-tab-appcurriculum.30` — weights: raw@sel
- `R1.supp-tab-appcurriculum.31` — weights: raw-best
- `R1.supp-tab-appcurriculum.32` — weights: raw-best
- `R1.supp-tab-appcurriculum.33` — weights: raw-best
- `R1.supp-tab-appcurriculum.34` — weights: raw-best
- `R1.supp-tab-appcurriculum.35` — weights: raw-best
- `R1.supp-tab-appcurriculum.36` — weights: raw-best
- `R1.supp-tab-appcurriculum.37` — weights: raw-best
- `R1.supp-tab-appcurriculum.38` — weights: raw-best
- `R1.supp-tab-appcurriculum.39` — weights: raw-best
- `R1.supp-tab-appcurriculum.40` — weights: EMA (post hoc)
- `R1.supp-tab-appcurriculum.41` — weights: EMA (post hoc)
- `R1.supp-tab-appcurriculum.42` — weights: EMA (post hoc)
- `R1.supp-tab-appcurriculum.43` — weights: EMA (post hoc)
- `R1.supp-tab-appcurriculum.44` — weights: EMA (post hoc)
- `R1.supp-tab-appcurriculum.45` — weights: EMA (post hoc)
- `R1.supp-tab-appcurriculum.46` — weights: EMA (post hoc)
- `R1.supp-tab-appcurriculum.47` — weights: EMA (post hoc)
- `R1.supp-tab-appcurriculum.48` — weights: EMA (post hoc)
- `R1.supp-tab-appcurriculum.49` — weights: raw@sel (post hoc)
- `R1.supp-tab-appcurriculum.50` — weights: raw@sel (post hoc)
- `R1.supp-tab-appcurriculum.51` — weights: raw@sel (post hoc)
- `R1.supp-tab-appcurriculum.52` — weights: raw@sel (post hoc)
- `R1.supp-tab-appcurriculum.53` — weights: raw@sel (post hoc)
- `R1.supp-tab-appcurriculum.54` — weights: raw@sel (post hoc)
- `R1.supp-tab-appcurriculum.55` — weights: raw@sel (post hoc)
- `R1.supp-tab-appcurriculum.56` — weights: raw@sel (post hoc)
- `R1.supp-tab-appcurriculum.57` — weights: raw@sel (post hoc)
- `R1.supp-tab-appcurriculum.58` — weights: raw-best (post hoc)
- `R1.supp-tab-appcurriculum.59` — weights: raw-best (post hoc)
- `R1.supp-tab-appcurriculum.60` — weights: raw-best (post hoc)
- `R1.supp-tab-appcurriculum.61` — weights: raw-best (post hoc)
- `R1.supp-tab-appcurriculum.62` — weights: raw-best (post hoc)
- `R1.supp-tab-appcurriculum.63` — weights: raw-best (post hoc)
- `R1.supp-tab-appcurriculum.64` — weights: raw-best (post hoc)
- `R1.supp-tab-appcurriculum.65` — weights: raw-best (post hoc)
- `R1.supp-tab-appcurriculum.66` — weights: raw-best (post hoc)
- `R1.supp-tab-appcurriculum.67` — weights: EMA (post hoc)
- `R1.supp-tab-appcurriculum.68` — weights: EMA (post hoc)
- `R1.supp-tab-appcurriculum.69` — weights: EMA (post hoc)
- `R1.supp-tab-appcurriculum.70` — weights: EMA (post hoc)
- `R1.supp-tab-appcurriculum.71` — weights: EMA (post hoc)
- `R1.supp-tab-appcurriculum.72` — weights: EMA (post hoc)
- `R1.supp-tab-appcurriculum.73` — weights: EMA (post hoc)
- `R1.supp-tab-appcurriculum.74` — weights: EMA (post hoc)
- `R1.supp-tab-appcurriculum.75` — weights: EMA (post hoc)
- `R1.supp-tab-appcurriculum.76` — weights: raw@sel (post hoc)
- `R1.supp-tab-appcurriculum.77` — weights: raw@sel (post hoc)
- `R1.supp-tab-appcurriculum.78` — weights: raw@sel (post hoc)
- `R1.supp-tab-appcurriculum.79` — weights: raw@sel (post hoc)
- `R1.supp-tab-appcurriculum.80` — weights: raw@sel (post hoc)
- `R1.supp-tab-appcurriculum.81` — weights: raw@sel (post hoc)
- `R1.supp-tab-appcurriculum.82` — weights: raw@sel (post hoc)
- `R1.supp-tab-appcurriculum.83` — weights: raw@sel (post hoc)
- `R1.supp-tab-appcurriculum.84` — weights: raw@sel (post hoc)
- `R1.supp-tab-appcurriculum.85` — weights: raw-best (post hoc)
- `R1.supp-tab-appcurriculum.86` — weights: raw-best (post hoc)
- `R1.supp-tab-appcurriculum.87` — weights: raw-best (post hoc)
- `R1.supp-tab-appcurriculum.88` — weights: raw-best (post hoc)
- `R1.supp-tab-appcurriculum.89` — weights: raw-best (post hoc)
- `R1.supp-tab-appcurriculum.90` — weights: raw-best (post hoc)
- `R1.supp-tab-appcurriculum.91` — weights: raw-best (post hoc)
- `R1.supp-tab-appcurriculum.92` — weights: raw-best (post hoc)
- `R1.supp-tab-appcurriculum.93` — weights: raw-best (post hoc)

## R1.supp-app-objective — Revision 1 — Supplementary Material, app:objective

*Supplementary Material, app:objective; `\label{app:objective}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-app-objective.1` | 11,971,561 — “one architecture (11{,}971{,}561 parameters) and differ only in the recipe and” | 11971561 | 11971561.00 | `revision-1/tables/shapes.json` | `python verify/claim.py R1.supp-app-objective.1` |
| `R1.supp-app-objective.2` | 10,652,643 — “(10{,}652{,}643), and Fair-W keeps the trunk's full 1280-channel head with a” | 10652643 | 10652643.00 | `revision-1/tables/shapes.json` | `python verify/claim.py R1.supp-app-objective.2` |
| `R1.supp-app-objective.3` | 9,628,081 — “$\gamma$-weighted frequency residual and no CMAM (9{,}628{,}081).” | 9628081 | 9628081.00 | `revision-1/tables/shapes.json` | `python verify/claim.py R1.supp-app-objective.3` |

## R1.supp-tab-appobjweights — Revision 1 — Supplementary Material, tab:appobjweights

*Supplementary Material, tab:appobjweights; `\label{tab:appobjweights}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-tab-appobjweights.1` | 11,971,561 — “parameters & -- & 11{,}971{,}561 & 11{,}971{,}561 & 10{,}652{,}643 & 9{,}628{,}081 \\” | 11971561 | 11971561.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appobjweights.1` |
| `R1.supp-tab-appobjweights.2` | 11,971,561 — “parameters & -- & 11{,}971{,}561 & 11{,}971{,}561 & 10{,}652{,}643 & 9{,}628{,}081 \\” | 11971561 | 11971561.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appobjweights.2` |
| `R1.supp-tab-appobjweights.3` | 10,652,643 — “parameters & -- & 11{,}971{,}561 & 11{,}971{,}561 & 10{,}652{,}643 & 9{,}628{,}081 \\” | 10652643 | 10652643.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appobjweights.3` |
| `R1.supp-tab-appobjweights.4` | 9,628,081 — “parameters & -- & 11{,}971{,}561 & 11{,}971{,}561 & 10{,}652{,}643 & 9{,}628{,}081 \\” | 9628081 | 9628081.00 | `revision-1/exploratory/cost_table.json` | `python verify/claim.py R1.supp-tab-appobjweights.4` |

## R1.supp-app-facetracks — Revision 1 — Supplementary Material, app:facetracks

*Supplementary Material, app:facetracks; `\label{app:facetracks}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-app-facetracks.1` | 31 — “FaceForensics++ originals isolated 31 whose crop switched between people. For” | 31 | 31.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-app-facetracks.1` |
| `R1.supp-app-facetracks.2` | 134 — “had 134 tracks in all. Eight had a single track and kept their original” | 134 | 134.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-app-facetracks.2` |
| `R1.supp-app-facetracks.3` | 23 — “crops; the other 23 had 2 to 26 tracks each. The proposal was changed for” | 23 | 23.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-app-facetracks.3` |
| `R1.supp-app-facetracks.4` | 26 — “crops; the other 23 had 2 to 26 tracks each. The proposal was changed for” | 26 | 26.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-app-facetracks.4` |
| `R1.supp-app-facetracks.5` | 363 — “a visual check of ten over-inclusions at 0.40. Of 363 source takes, 226 had” | 363 | 363.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-app-facetracks.5` |
| `R1.supp-app-facetracks.6` | 226 — “a visual check of ten over-inclusions at 0.40. Of 363 source takes, 226 had” | 226 | 226.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-app-facetracks.6` |
| `R1.supp-app-facetracks.7` | 135 — “one track, 135 were selected by this rule (4 of them keeping more than one” | 135 | 135.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-app-facetracks.7` |
| `R1.supp-app-facetracks.8` | 4 — “one track, 135 were selected by this rule (4 of them keeping more than one” | 4 | 4.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-app-facetracks.8` |
| `R1.supp-app-facetracks.9` | 2 — “track), and 2 without a manipulated counterpart took the longest track.” | 2 | 2.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-app-facetracks.9` |

## R1.supp-tab-appfacetracks — Revision 1 — Supplementary Material, tab:appfacetracks

*Supplementary Material, tab:appfacetracks; `\label{tab:appfacetracks}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-tab-appfacetracks.1` | 57,091 — “\caption{Face-crop metadata counts (all 57{,}091 per-video metadata files of” | 57091 | 57091.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.1` |
| `R1.supp-tab-appfacetracks.2` | 178 — “test); Celeb-DF~v2: all videos, of which the test split has 178 real and” | 178 | 178.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.2` |
| `R1.supp-tab-appfacetracks.3` | 340 — “340 fake; DFD counts are identical at c23 and c40. Cells with three values give c0; c23; c” | 340 | 340.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.3` |
| `R1.supp-tab-appfacetracks.4` | 23 — “FF++ real & 1{,}000 & 23 (2) & 55; 55; 60 / 509{,}128 & 6; 6; 7 & 219; 213; 191 & 0 \\” | 23 | 23.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.4` |
| `R1.supp-tab-appfacetracks.5` | 2 — “FF++ real & 1{,}000 & 23 (2) & 55; 55; 60 / 509{,}128 & 6; 6; 7 & 219; 213; 191 & 0 \\” | 2 | 2.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.5` |
| `R1.supp-tab-appfacetracks.6` | 55 — “FF++ real & 1{,}000 & 23 (2) & 55; 55; 60 / 509{,}128 & 6; 6; 7 & 219; 213; 191 & 0 \\” | 55 | 55.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.6` |
| `R1.supp-tab-appfacetracks.7` | 55 — “FF++ real & 1{,}000 & 23 (2) & 55; 55; 60 / 509{,}128 & 6; 6; 7 & 219; 213; 191 & 0 \\” | 55 | 55.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.7` |
| `R1.supp-tab-appfacetracks.8` | 60 — “FF++ real & 1{,}000 & 23 (2) & 55; 55; 60 / 509{,}128 & 6; 6; 7 & 219; 213; 191 & 0 \\” | 60 | 60.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.8` |
| `R1.supp-tab-appfacetracks.9` | 509,128 — “FF++ real & 1{,}000 & 23 (2) & 55; 55; 60 / 509{,}128 & 6; 6; 7 & 219; 213; 191 & 0 \\” | 509128 | 509128.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.9` |
| `R1.supp-tab-appfacetracks.10` | 6 — “FF++ real & 1{,}000 & 23 (2) & 55; 55; 60 / 509{,}128 & 6; 6; 7 & 219; 213; 191 & 0 \\” | 6 | 6.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.10` |
| `R1.supp-tab-appfacetracks.11` | 6 — “FF++ real & 1{,}000 & 23 (2) & 55; 55; 60 / 509{,}128 & 6; 6; 7 & 219; 213; 191 & 0 \\” | 6 | 6.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.11` |
| `R1.supp-tab-appfacetracks.12` | 7 — “FF++ real & 1{,}000 & 23 (2) & 55; 55; 60 / 509{,}128 & 6; 6; 7 & 219; 213; 191 & 0 \\” | 7 | 7.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.12` |
| `R1.supp-tab-appfacetracks.13` | 219 — “FF++ real & 1{,}000 & 23 (2) & 55; 55; 60 / 509{,}128 & 6; 6; 7 & 219; 213; 191 & 0 \\” | 219 | 219.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.13` |
| `R1.supp-tab-appfacetracks.14` | 213 — “FF++ real & 1{,}000 & 23 (2) & 55; 55; 60 / 509{,}128 & 6; 6; 7 & 219; 213; 191 & 0 \\” | 213 | 213.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.14` |
| `R1.supp-tab-appfacetracks.15` | 191 — “FF++ real & 1{,}000 & 23 (2) & 55; 55; 60 / 509{,}128 & 6; 6; 7 & 219; 213; 191 & 0 \\” | 191 | 191.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.15` |
| `R1.supp-tab-appfacetracks.16` | 0 — “FF++ real & 1{,}000 & 23 (2) & 55; 55; 60 / 509{,}128 & 6; 6; 7 & 219; 213; 191 & 0 \\” | 0 | 0.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.16` |
| `R1.supp-tab-appfacetracks.17` | 23 — “FF++ Deepfakes & 1{,}000 & 23 (2) & 61; 62; 66 / 509{,}128 & 6; 6; 7 & 219; 213; 197 & 0 \” | 23 | 23.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.17` |
| `R1.supp-tab-appfacetracks.18` | 2 — “FF++ Deepfakes & 1{,}000 & 23 (2) & 61; 62; 66 / 509{,}128 & 6; 6; 7 & 219; 213; 197 & 0 \” | 2 | 2.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.18` |
| `R1.supp-tab-appfacetracks.19` | 61 — “FF++ Deepfakes & 1{,}000 & 23 (2) & 61; 62; 66 / 509{,}128 & 6; 6; 7 & 219; 213; 197 & 0 \” | 61 | 61.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.19` |
| `R1.supp-tab-appfacetracks.20` | 62 — “FF++ Deepfakes & 1{,}000 & 23 (2) & 61; 62; 66 / 509{,}128 & 6; 6; 7 & 219; 213; 197 & 0 \” | 62 | 62.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.20` |
| `R1.supp-tab-appfacetracks.21` | 66 — “FF++ Deepfakes & 1{,}000 & 23 (2) & 61; 62; 66 / 509{,}128 & 6; 6; 7 & 219; 213; 197 & 0 \” | 66 | 66.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.21` |
| `R1.supp-tab-appfacetracks.22` | 509,128 — “FF++ Deepfakes & 1{,}000 & 23 (2) & 61; 62; 66 / 509{,}128 & 6; 6; 7 & 219; 213; 197 & 0 \” | 509128 | 509128.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.22` |
| `R1.supp-tab-appfacetracks.23` | 6 — “FF++ Deepfakes & 1{,}000 & 23 (2) & 61; 62; 66 / 509{,}128 & 6; 6; 7 & 219; 213; 197 & 0 \” | 6 | 6.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.23` |
| `R1.supp-tab-appfacetracks.24` | 6 — “FF++ Deepfakes & 1{,}000 & 23 (2) & 61; 62; 66 / 509{,}128 & 6; 6; 7 & 219; 213; 197 & 0 \” | 6 | 6.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.24` |
| `R1.supp-tab-appfacetracks.25` | 7 — “FF++ Deepfakes & 1{,}000 & 23 (2) & 61; 62; 66 / 509{,}128 & 6; 6; 7 & 219; 213; 197 & 0 \” | 7 | 7.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.25` |
| `R1.supp-tab-appfacetracks.26` | 219 — “FF++ Deepfakes & 1{,}000 & 23 (2) & 61; 62; 66 / 509{,}128 & 6; 6; 7 & 219; 213; 197 & 0 \” | 219 | 219.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.26` |
| `R1.supp-tab-appfacetracks.27` | 213 — “FF++ Deepfakes & 1{,}000 & 23 (2) & 61; 62; 66 / 509{,}128 & 6; 6; 7 & 219; 213; 197 & 0 \” | 213 | 213.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.27` |
| `R1.supp-tab-appfacetracks.28` | 197 — “FF++ Deepfakes & 1{,}000 & 23 (2) & 61; 62; 66 / 509{,}128 & 6; 6; 7 & 219; 213; 197 & 0 \” | 197 | 197.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.28` |
| `R1.supp-tab-appfacetracks.29` | 0 — “FF++ Deepfakes & 1{,}000 & 23 (2) & 61; 62; 66 / 509{,}128 & 6; 6; 7 & 219; 213; 197 & 0 \” | 0 | 0.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.29` |
| `R1.supp-tab-appfacetracks.30` | 23 — “FF++ Face2Face & 1{,}000 & 23 (2) & 2{,}087; 2{,}089; 2{,}090 / 509{,}128 & 13; 14; 14 & 2” | 23 | 23.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.30` |
| `R1.supp-tab-appfacetracks.31` | 2 — “FF++ Face2Face & 1{,}000 & 23 (2) & 2{,}087; 2{,}089; 2{,}090 / 509{,}128 & 13; 14; 14 & 2” | 2 | 2.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.31` |
| `R1.supp-tab-appfacetracks.32` | 2,087 — “FF++ Face2Face & 1{,}000 & 23 (2) & 2{,}087; 2{,}089; 2{,}090 / 509{,}128 & 13; 14; 14 & 2” | 2087 | 2087.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.32` |
| `R1.supp-tab-appfacetracks.33` | 2,089 — “FF++ Face2Face & 1{,}000 & 23 (2) & 2{,}087; 2{,}089; 2{,}090 / 509{,}128 & 13; 14; 14 & 2” | 2089 | 2089.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.33` |
| `R1.supp-tab-appfacetracks.34` | 2,090 — “FF++ Face2Face & 1{,}000 & 23 (2) & 2{,}087; 2{,}089; 2{,}090 / 509{,}128 & 13; 14; 14 & 2” | 2090 | 2090.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.34` |
| `R1.supp-tab-appfacetracks.35` | 509,128 — “FF++ Face2Face & 1{,}000 & 23 (2) & 2{,}087; 2{,}089; 2{,}090 / 509{,}128 & 13; 14; 14 & 2” | 509128 | 509128.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.35` |
| `R1.supp-tab-appfacetracks.36` | 13 — “FF++ Face2Face & 1{,}000 & 23 (2) & 2{,}087; 2{,}089; 2{,}090 / 509{,}128 & 13; 14; 14 & 2” | 13 | 13.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.36` |
| `R1.supp-tab-appfacetracks.37` | 14 — “FF++ Face2Face & 1{,}000 & 23 (2) & 2{,}087; 2{,}089; 2{,}090 / 509{,}128 & 13; 14; 14 & 2” | 14 | 14.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.37` |
| `R1.supp-tab-appfacetracks.38` | 14 — “FF++ Face2Face & 1{,}000 & 23 (2) & 2{,}087; 2{,}089; 2{,}090 / 509{,}128 & 13; 14; 14 & 2” | 14 | 14.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.38` |
| `R1.supp-tab-appfacetracks.39` | 210 — “FF++ Face2Face & 1{,}000 & 23 (2) & 2{,}087; 2{,}089; 2{,}090 / 509{,}128 & 13; 14; 14 & 2” | 210 | 210.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.39` |
| `R1.supp-tab-appfacetracks.40` | 203 — “FF++ Face2Face & 1{,}000 & 23 (2) & 2{,}087; 2{,}089; 2{,}090 / 509{,}128 & 13; 14; 14 & 2” | 203 | 203.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.40` |
| `R1.supp-tab-appfacetracks.41` | 186 — “FF++ Face2Face & 1{,}000 & 23 (2) & 2{,}087; 2{,}089; 2{,}090 / 509{,}128 & 13; 14; 14 & 2” | 186 | 186.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.41` |
| `R1.supp-tab-appfacetracks.42` | 0 — “FF++ Face2Face & 1{,}000 & 23 (2) & 2{,}087; 2{,}089; 2{,}090 / 509{,}128 & 13; 14; 14 & 2” | 0 | 0.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.42` |
| `R1.supp-tab-appfacetracks.43` | 23 — “FF++ FaceSwap & 1{,}000 & 23 (2) & 51; 51; 55 / 406{,}140 & 5; 5; 6 & 204; 198; 179 & 0 \\” | 23 | 23.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.43` |
| `R1.supp-tab-appfacetracks.44` | 2 — “FF++ FaceSwap & 1{,}000 & 23 (2) & 51; 51; 55 / 406{,}140 & 5; 5; 6 & 204; 198; 179 & 0 \\” | 2 | 2.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.44` |
| `R1.supp-tab-appfacetracks.45` | 51 — “FF++ FaceSwap & 1{,}000 & 23 (2) & 51; 51; 55 / 406{,}140 & 5; 5; 6 & 204; 198; 179 & 0 \\” | 51 | 51.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.45` |
| `R1.supp-tab-appfacetracks.46` | 51 — “FF++ FaceSwap & 1{,}000 & 23 (2) & 51; 51; 55 / 406{,}140 & 5; 5; 6 & 204; 198; 179 & 0 \\” | 51 | 51.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.46` |
| `R1.supp-tab-appfacetracks.47` | 55 — “FF++ FaceSwap & 1{,}000 & 23 (2) & 51; 51; 55 / 406{,}140 & 5; 5; 6 & 204; 198; 179 & 0 \\” | 55 | 55.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.47` |
| `R1.supp-tab-appfacetracks.48` | 406,140 — “FF++ FaceSwap & 1{,}000 & 23 (2) & 51; 51; 55 / 406{,}140 & 5; 5; 6 & 204; 198; 179 & 0 \\” | 406140 | 406140.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.48` |
| `R1.supp-tab-appfacetracks.49` | 5 — “FF++ FaceSwap & 1{,}000 & 23 (2) & 51; 51; 55 / 406{,}140 & 5; 5; 6 & 204; 198; 179 & 0 \\” | 5 | 5.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.49` |
| `R1.supp-tab-appfacetracks.50` | 5 — “FF++ FaceSwap & 1{,}000 & 23 (2) & 51; 51; 55 / 406{,}140 & 5; 5; 6 & 204; 198; 179 & 0 \\” | 5 | 5.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.50` |
| `R1.supp-tab-appfacetracks.51` | 6 — “FF++ FaceSwap & 1{,}000 & 23 (2) & 51; 51; 55 / 406{,}140 & 5; 5; 6 & 204; 198; 179 & 0 \\” | 6 | 6.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.51` |
| `R1.supp-tab-appfacetracks.52` | 204 — “FF++ FaceSwap & 1{,}000 & 23 (2) & 51; 51; 55 / 406{,}140 & 5; 5; 6 & 204; 198; 179 & 0 \\” | 204 | 204.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.52` |
| `R1.supp-tab-appfacetracks.53` | 198 — “FF++ FaceSwap & 1{,}000 & 23 (2) & 51; 51; 55 / 406{,}140 & 5; 5; 6 & 204; 198; 179 & 0 \\” | 198 | 198.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.53` |
| `R1.supp-tab-appfacetracks.54` | 179 — “FF++ FaceSwap & 1{,}000 & 23 (2) & 51; 51; 55 / 406{,}140 & 5; 5; 6 & 204; 198; 179 & 0 \\” | 179 | 179.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.54` |
| `R1.supp-tab-appfacetracks.55` | 0 — “FF++ FaceSwap & 1{,}000 & 23 (2) & 51; 51; 55 / 406{,}140 & 5; 5; 6 & 204; 198; 179 & 0 \\” | 0 | 0.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.55` |
| `R1.supp-tab-appfacetracks.56` | 23 — “FF++ NeuralTextures & 1{,}000 & 23 (2) & 50; 50; 55 / 406{,}137 & 5; 5; 6 & 211; 202; 186 ” | 23 | 23.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.56` |
| `R1.supp-tab-appfacetracks.57` | 2 — “FF++ NeuralTextures & 1{,}000 & 23 (2) & 50; 50; 55 / 406{,}137 & 5; 5; 6 & 211; 202; 186 ” | 2 | 2.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.57` |
| `R1.supp-tab-appfacetracks.58` | 50 — “FF++ NeuralTextures & 1{,}000 & 23 (2) & 50; 50; 55 / 406{,}137 & 5; 5; 6 & 211; 202; 186 ” | 50 | 50.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.58` |
| `R1.supp-tab-appfacetracks.59` | 50 — “FF++ NeuralTextures & 1{,}000 & 23 (2) & 50; 50; 55 / 406{,}137 & 5; 5; 6 & 211; 202; 186 ” | 50 | 50.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.59` |
| `R1.supp-tab-appfacetracks.60` | 55 — “FF++ NeuralTextures & 1{,}000 & 23 (2) & 50; 50; 55 / 406{,}137 & 5; 5; 6 & 211; 202; 186 ” | 55 | 55.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.60` |
| `R1.supp-tab-appfacetracks.61` | 406,137 — “FF++ NeuralTextures & 1{,}000 & 23 (2) & 50; 50; 55 / 406{,}137 & 5; 5; 6 & 211; 202; 186 ” | 406137 | 406137.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.61` |
| `R1.supp-tab-appfacetracks.62` | 5 — “FF++ NeuralTextures & 1{,}000 & 23 (2) & 50; 50; 55 / 406{,}137 & 5; 5; 6 & 211; 202; 186 ” | 5 | 5.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.62` |
| `R1.supp-tab-appfacetracks.63` | 5 — “FF++ NeuralTextures & 1{,}000 & 23 (2) & 50; 50; 55 / 406{,}137 & 5; 5; 6 & 211; 202; 186 ” | 5 | 5.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.63` |
| `R1.supp-tab-appfacetracks.64` | 6 — “FF++ NeuralTextures & 1{,}000 & 23 (2) & 50; 50; 55 / 406{,}137 & 5; 5; 6 & 211; 202; 186 ” | 6 | 6.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.64` |
| `R1.supp-tab-appfacetracks.65` | 211 — “FF++ NeuralTextures & 1{,}000 & 23 (2) & 50; 50; 55 / 406{,}137 & 5; 5; 6 & 211; 202; 186 ” | 211 | 211.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.65` |
| `R1.supp-tab-appfacetracks.66` | 202 — “FF++ NeuralTextures & 1{,}000 & 23 (2) & 50; 50; 55 / 406{,}137 & 5; 5; 6 & 211; 202; 186 ” | 202 | 202.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.66` |
| `R1.supp-tab-appfacetracks.67` | 186 — “FF++ NeuralTextures & 1{,}000 & 23 (2) & 50; 50; 55 / 406{,}137 & 5; 5; 6 & 211; 202; 186 ” | 186 | 186.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.67` |
| `R1.supp-tab-appfacetracks.68` | 0 — “FF++ NeuralTextures & 1{,}000 & 23 (2) & 50; 50; 55 / 406{,}137 & 5; 5; 6 & 211; 202; 186 ” | 0 | 0.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.68` |
| `R1.supp-tab-appfacetracks.69` | 23 — “FF++ FaceShifter & 1{,}000 & 23 (2) & 56; 56; 61 / 509{,}128 & 6; 6; 7 & 224; 215; 190 & 0” | 23 | 23.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.69` |
| `R1.supp-tab-appfacetracks.70` | 2 — “FF++ FaceShifter & 1{,}000 & 23 (2) & 56; 56; 61 / 509{,}128 & 6; 6; 7 & 224; 215; 190 & 0” | 2 | 2.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.70` |
| `R1.supp-tab-appfacetracks.71` | 56 — “FF++ FaceShifter & 1{,}000 & 23 (2) & 56; 56; 61 / 509{,}128 & 6; 6; 7 & 224; 215; 190 & 0” | 56 | 56.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.71` |
| `R1.supp-tab-appfacetracks.72` | 56 — “FF++ FaceShifter & 1{,}000 & 23 (2) & 56; 56; 61 / 509{,}128 & 6; 6; 7 & 224; 215; 190 & 0” | 56 | 56.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.72` |
| `R1.supp-tab-appfacetracks.73` | 61 — “FF++ FaceShifter & 1{,}000 & 23 (2) & 56; 56; 61 / 509{,}128 & 6; 6; 7 & 224; 215; 190 & 0” | 61 | 61.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.73` |
| `R1.supp-tab-appfacetracks.74` | 509,128 — “FF++ FaceShifter & 1{,}000 & 23 (2) & 56; 56; 61 / 509{,}128 & 6; 6; 7 & 224; 215; 190 & 0” | 509128 | 509128.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.74` |
| `R1.supp-tab-appfacetracks.75` | 6 — “FF++ FaceShifter & 1{,}000 & 23 (2) & 56; 56; 61 / 509{,}128 & 6; 6; 7 & 224; 215; 190 & 0” | 6 | 6.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.75` |
| `R1.supp-tab-appfacetracks.76` | 6 — “FF++ FaceShifter & 1{,}000 & 23 (2) & 56; 56; 61 / 509{,}128 & 6; 6; 7 & 224; 215; 190 & 0” | 6 | 6.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.76` |
| `R1.supp-tab-appfacetracks.77` | 7 — “FF++ FaceShifter & 1{,}000 & 23 (2) & 56; 56; 61 / 509{,}128 & 6; 6; 7 & 224; 215; 190 & 0” | 7 | 7.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.77` |
| `R1.supp-tab-appfacetracks.78` | 224 — “FF++ FaceShifter & 1{,}000 & 23 (2) & 56; 56; 61 / 509{,}128 & 6; 6; 7 & 224; 215; 190 & 0” | 224 | 224.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.78` |
| `R1.supp-tab-appfacetracks.79` | 215 — “FF++ FaceShifter & 1{,}000 & 23 (2) & 56; 56; 61 / 509{,}128 & 6; 6; 7 & 224; 215; 190 & 0” | 215 | 215.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.79` |
| `R1.supp-tab-appfacetracks.80` | 190 — “FF++ FaceShifter & 1{,}000 & 23 (2) & 56; 56; 61 / 509{,}128 & 6; 6; 7 & 224; 215; 190 & 0” | 190 | 190.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.80` |
| `R1.supp-tab-appfacetracks.81` | 0 — “FF++ FaceShifter & 1{,}000 & 23 (2) & 56; 56; 61 / 509{,}128 & 6; 6; 7 & 224; 215; 190 & 0” | 0 | 0.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.81` |
| `R1.supp-tab-appfacetracks.82` | 363 — “DFD real (source takes) & 363 & 363 (4) & 1{,}222 / 315{,}381 & 75 & -- & 0 \\” | 363 | 363.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.82` |
| `R1.supp-tab-appfacetracks.83` | 363 — “DFD real (source takes) & 363 & 363 (4) & 1{,}222 / 315{,}381 & 75 & -- & 0 \\” | 363 | 363.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.83` |
| `R1.supp-tab-appfacetracks.84` | 4 — “DFD real (source takes) & 363 & 363 (4) & 1{,}222 / 315{,}381 & 75 & -- & 0 \\” | 4 | 4.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.84` |
| `R1.supp-tab-appfacetracks.85` | 1,222 — “DFD real (source takes) & 363 & 363 (4) & 1{,}222 / 315{,}381 & 75 & -- & 0 \\” | 1222 | 1222.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.85` |
| `R1.supp-tab-appfacetracks.86` | 315,381 — “DFD real (source takes) & 363 & 363 (4) & 1{,}222 / 315{,}381 & 75 & -- & 0 \\” | 315381 | 315381.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.86` |
| `R1.supp-tab-appfacetracks.87` | 75 — “DFD real (source takes) & 363 & 363 (4) & 1{,}222 / 315{,}381 & 75 & -- & 0 \\” | 75 | 75.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.87` |
| `R1.supp-tab-appfacetracks.88` | 0 — “DFD real (source takes) & 363 & 363 (4) & 1{,}222 / 315{,}381 & 75 & -- & 0 \\” | 0 | 0.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.88` |
| `R1.supp-tab-appfacetracks.89` | 3,068 — “DFD manipulated & 3{,}068 & 3{,}068 (45) & 92 / 2{,}242{,}692 & 50 & -- & 19 \\” | 3068 | 3068.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.89` |
| `R1.supp-tab-appfacetracks.90` | 3,068 — “DFD manipulated & 3{,}068 & 3{,}068 (45) & 92 / 2{,}242{,}692 & 50 & -- & 19 \\” | 3068 | 3068.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.90` |
| `R1.supp-tab-appfacetracks.91` | 45 — “DFD manipulated & 3{,}068 & 3{,}068 (45) & 92 / 2{,}242{,}692 & 50 & -- & 19 \\” | 45 | 45.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.91` |
| `R1.supp-tab-appfacetracks.92` | 92 — “DFD manipulated & 3{,}068 & 3{,}068 (45) & 92 / 2{,}242{,}692 & 50 & -- & 19 \\” | 92 | 92.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.92` |
| `R1.supp-tab-appfacetracks.93` | 2,242,692 — “DFD manipulated & 3{,}068 & 3{,}068 (45) & 92 / 2{,}242{,}692 & 50 & -- & 19 \\” | 2242692 | 2242692.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.93` |
| `R1.supp-tab-appfacetracks.94` | 50 — “DFD manipulated & 3{,}068 & 3{,}068 (45) & 92 / 2{,}242{,}692 & 50 & -- & 19 \\” | 50 | 50.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.94` |
| `R1.supp-tab-appfacetracks.95` | 19 — “DFD manipulated & 3{,}068 & 3{,}068 (45) & 92 / 2{,}242{,}692 & 50 & -- & 19 \\” | 19 | 19.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.95` |
| `R1.supp-tab-appfacetracks.96` | 890 — “Celeb-DF~v2 real & 890 & 0 & 69 / 358{,}790 & 9 & 67 & 1 \\” | 890 | 890.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.96` |
| `R1.supp-tab-appfacetracks.97` | 0 — “Celeb-DF~v2 real & 890 & 0 & 69 / 358{,}790 & 9 & 67 & 1 \\” | 0 | 0.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.97` |
| `R1.supp-tab-appfacetracks.98` | 69 — “Celeb-DF~v2 real & 890 & 0 & 69 / 358{,}790 & 9 & 67 & 1 \\” | 69 | 69.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.98` |
| `R1.supp-tab-appfacetracks.99` | 358,790 — “Celeb-DF~v2 real & 890 & 0 & 69 / 358{,}790 & 9 & 67 & 1 \\” | 358790 | 358790.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.99` |
| `R1.supp-tab-appfacetracks.100` | 9 — “Celeb-DF~v2 real & 890 & 0 & 69 / 358{,}790 & 9 & 67 & 1 \\” | 9 | 9.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.100` |
| `R1.supp-tab-appfacetracks.101` | 67 — “Celeb-DF~v2 real & 890 & 0 & 69 / 358{,}790 & 9 & 67 & 1 \\” | 67 | 67.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.101` |
| `R1.supp-tab-appfacetracks.102` | 1 — “Celeb-DF~v2 real & 890 & 0 & 69 / 358{,}790 & 9 & 67 & 1 \\” | 1 | 1.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.102` |
| `R1.supp-tab-appfacetracks.103` | 5,639 — “Celeb-DF~v2 fake & 5{,}639 & 0 & 0 / 2{,}116{,}768 & 0 & 402 & 0 \\” | 5639 | 5639.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.103` |
| `R1.supp-tab-appfacetracks.104` | 0 — “Celeb-DF~v2 fake & 5{,}639 & 0 & 0 / 2{,}116{,}768 & 0 & 402 & 0 \\” | 0 | 0.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.104` |
| `R1.supp-tab-appfacetracks.105` | 0 — “Celeb-DF~v2 fake & 5{,}639 & 0 & 0 / 2{,}116{,}768 & 0 & 402 & 0 \\” | 0 | 0.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.105` |
| `R1.supp-tab-appfacetracks.106` | 2,116,768 — “Celeb-DF~v2 fake & 5{,}639 & 0 & 0 / 2{,}116{,}768 & 0 & 402 & 0 \\” | 2116768 | 2116768.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.106` |
| `R1.supp-tab-appfacetracks.107` | 0 — “Celeb-DF~v2 fake & 5{,}639 & 0 & 0 / 2{,}116{,}768 & 0 & 402 & 0 \\” | 0 | 0.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.107` |
| `R1.supp-tab-appfacetracks.108` | 402 — “Celeb-DF~v2 fake & 5{,}639 & 0 & 0 / 2{,}116{,}768 & 0 & 402 & 0 \\” | 402 | 402.00 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.108` |
| `R1.supp-tab-appfacetracks.109` | 0 — “Celeb-DF~v2 fake & 5{,}639 & 0 & 0 / 2{,}116{,}768 & 0 & 402 & 0 \\” | 0 | 0.0000 | `revision-1/tables/face_track_counts.json` | `python verify/claim.py R1.supp-tab-appfacetracks.109` |

## R1.supp-tab-notation — Revision 1 — Supplementary Material, tab:notation

*Supplementary Material, tab:notation; `\label{tab:notation}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-tab-notation.1` | 1.32 — “--- and include every trained parameter, among them CAFRL's 1.32\,M” | 1.32 | 1.3189 | `probes/param_counts_arms.json` | `python verify/claim.py R1.supp-tab-notation.1` |
| `R1.supp-tab-notation.2` | 10.65 — “discriminator, which the prediction does not use (10.65\,M without it). The last” | 10.65 | 10.65 | `revision-1/tables/shapes.json` | `python verify/claim.py R1.supp-tab-notation.2` |
| `R1.supp-tab-notation.3` | 4.0 — “the backbone-matched, smaller control & 4.0\,M & fair & 3 &” | 4.0 | 4.0088 | `probes/param_counts_arms.json` | `python verify/claim.py R1.supp-tab-notation.3` |
| `R1.supp-tab-notation.4` | 11.97 — “\textbf{E1} & Fair-N $+$ the GRL adversary & 11.97\,M & fair & 3 &” | 11.97 | 11.97 | `revision-1/tables/shapes.json` | `python verify/claim.py R1.supp-tab-notation.4` |

## R1.supp-app-repro — Revision 1 — Supplementary Material, app:repro

*Supplementary Material, app:repro; `\label{app:repro}`*

| id | claim | paper prints | this release gives | artifact | command |
|---|---|---|---|---|---|
| `R1.supp-app-repro.1` | 53 — “selected epoch (53 runs); the evaluation harness (paired bootstrap, seed” | 53 | 53.00 | `curves/selection.json` | `python verify/claim.py R1.supp-app-repro.1` |

- `R1.supp-app-repro.1` — the released runs with a configuration, validation curve and selected epoch (27 of v1.0.0 plus 26 of Revision 1)

---

*Generated by the release build from its export manifest; every number in the "this release gives" column was recomputed from the released artifacts while this file was written. A disagreement with the manuscript fails the build unless it is declared here as a **differs** row, which states both numbers and where the reconciliation is queued. Run `python verify/verify.py` to repeat the whole check yourself.*
