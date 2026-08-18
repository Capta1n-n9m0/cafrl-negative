# `curves/` — per-epoch validation curves and the selection outcome

Tables and figures in the paper report a model at a *selected* checkpoint, so the
release has to show the whole trajectory selection ran over, say which epoch was
taken, and let you recompute that choice. This directory does all three, for each
of the 27 released runs.

## The selection rule

> Best-by-validation on the selection metric sel = 0.5 * (video-AUC at c23 + video-AUC at c40), computed on the official FF++ validation split after every epoch; the checkpoint of the epoch with the highest sel is kept. CAFRL arms evaluate the EMA weights, baseline and control arms the raw weights (they train no EMA). No test-split quantity enters selection.

The rule is the trainer's, not a per-arm choice: it lives in the training code
that predates the campaign, and no released run selects on anything else. No
test-split quantity enters selection. `selection.json` states the rule once and
lists every run's outcome.

## What is in a curve file

`<run>.json` carries a single `epochs` axis and every epoch-level scalar the run
logged: the validation AUCs at c23 and c40, the selection metric itself, training
losses, learning rates, and — for CAFRL arms — the diagnostics the paper's
mechanism section reads (residual gate γ, compression-estimator accuracy, band
gates, standalone frequency-head AUC). Per-batch (step-indexed) series are not
included; their per-epoch aggregates are. Each file lists by name what it left
out — for every run that is the `loss_step/*` traces, and for the adversarial arms
also the gradient-reversal strength λ, which is logged per step and is in any case
a closed-form function of training progress fixed by the configuration.

Each file also records its selection outcome twice: the epoch and metric value
stored in the checkpoint's own metadata, and the same quantity recomputed as the
argmax of the released curve. The build fails if those disagree, so the selected
epochs quoted in the paper are recomputable from what is published here.

Raw TensorBoard event files are deliberately not shipped: they are opaque
binaries that can embed local paths, and this JSON is the whole of their
epoch-level content.

| run | epochs | selected epoch | selection metric | weights evaluated |
|---|---|---|---|---|
| `a0` | 50 | 34 | 0.94645 | EMA |
| `a1_grl_s1` | 50 | 29 | 0.94423 | EMA |
| `a1_grl_s2` | 50 | 34 | 0.94503 | EMA |
| `a1_none_s42` | 50 | 34 | 0.94675 | EMA |
| `cafrl_spatres_s42` | 50 | 29 | 0.93619 | EMA |
| `trunk_recipe_s42` | 30 | 4 | 0.97714 | raw |
| `trunk_recipe_s1` | 30 | 10 | 0.97751 | raw |
| `trunk_recipe_s2` | 30 | 8 | 0.97555 | raw |
| `f1_none_fair_s42` | 30 | 5 | 0.97703 | EMA |
| `f1_none_fair_s1` | 30 | 13 | 0.97825 | EMA |
| `f1_none_fair_s2` | 30 | 12 | 0.97675 | EMA |
| `f2_spatres_full_s42` | 30 | 5 | 0.97981 | EMA |
| `f2_spatres_full_s1` | 30 | 6 | 0.97762 | EMA |
| `f2_spatres_full_s2` | 30 | 7 | 0.97945 | EMA |
| `b7_effnet_b0_mq_fliponly` | 30 | 17 | 0.97581 | raw |
| `b7_effnet_b0_mq_fliponly_s1` | 30 | 11 | 0.97535 | raw |
| `b7_effnet_b0_mq_fliponly_s2` | 30 | 8 | 0.97578 | raw |
| `b1_xception_lit` | 30 | 22 | 0.93082 | raw |
| `b1_xception_lit_fliponly` | 30 | 28 | 0.92827 | raw |
| `b2_f3net_lit` | 30 | 6 | 0.93151 | raw |
| `b2_f3net_lit_fliponly` | 30 | 21 | 0.91961 | raw |
| `b3_freqnet_lit` | 30 | 26 | 0.88499 | raw |
| `b4_xception_mq` | 30 | 3 | 0.98075 | raw |
| `b4b_xception_mq_fliponly` | 30 | 3 | 0.97874 | raw |
| `b5_f3net_mq` | 30 | 9 | 0.97617 | raw |
| `b6_freqnet_mq` | 30 | 26 | 0.92050 | raw |
| `p2a_xcep_jpeg` | 30 | 9 | 0.94318 | raw |

## Reading Fig. 4(a) against these curves

F2's selected epoch is early (epoch 5 of 30), which is where the residual gate γ
peaks. That is worth knowing when reading the mechanism claim, and it is why
these curves are released: γ's full trajectory, at every epoch of all three
seeds, is in `f2_spatres_full_*.json` under `diag/residual_gamma`, alongside the
validation metric that did the selecting. The claim the paper makes from it — that
the gate does not collapse, in contrast to the shipped recipe — can be checked at
any epoch you like, not only the selected one.
