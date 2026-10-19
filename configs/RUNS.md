# Run configurations

`runs/` holds the **effective, as-run** configuration written by the trainer into
each run directory: the fully resolved values that run actually used. `launch/`
holds the launch-time YAML overrides for the CAFRL arms, and `base/` the base YAML
plus the dataclass definitions that supply every default.

Absolute paths in the `paths:` block have been replaced with placeholders
(`${FACES_ROOT}`, `${DATASET_ROOT}`, …); nothing else is modified.

**Read the caveat for baseline runs.** Baselines and controls are launched through
`train_baseline.py`, which selects the architecture, the data protocol and the
augmentation policy from *command-line flags* rather than from the YAML — so their
`config.yaml` still shows the CAFRL model block it inherited from the base config.
The authoritative description of each such run is the launch command and the
protocol/augmentation fields recorded in its prediction files; both are in the
table below.

| run | model | protocol | augmentation | seed | manuscript role | launch |
|---|---|---|---|---|---|---|
| `a0` | cafrl | mq | flip-only | 42 | CAFRL exactly as specified (the reference run; called A0 in the internal record). | `torchrun --nproc_per_node=2 -m src.train --name a0` |
| `a1_grl_s1` | cafrl | mq | flip-only | 1 | CAFRL-grl, seed 1 — the shipped-recipe seed band and the FaceShifter seed pool. | `python -m src.train --config configs/phase5/a1_grl_s1.yaml --name a1_grl_s1` |
| `a1_grl_s2` | cafrl | mq | flip-only | 2 | CAFRL-grl, seed 2 — the shipped-recipe seed band and the FaceShifter seed pool. | `python -m src.train --config configs/phase5/a1_grl_s2.yaml --name a1_grl_s2` |
| `a1_none_s42` | cafrl | mq | flip-only | 42 | CAFRL with the adversarial invariance removed, shipped recipe — shows the deficit is not the GRL. | `python -m src.train --config configs/phase5/a1_none_s42.yaml --name a1_none_s42` |
| `cafrl_spatres_s42` | cafrl | mq | flip-only | 42 | The do-no-harm spatial-residual redesign under the shipped recipe (gamma -> 0). | `python -m src.train --config configs/phase5/cafrl_spatres_s42.yaml --name cafrl_spatres_s42` |
| `trunk_recipe_s42` | cafrl_trunk | mq | flip-only | 42 | CAFRL's spatial trunk alone, trained with the fair baseline recipe — the architecture-vs-recipe split. | `python -m src.scripts.train_baseline --model cafrl_trunk --protocol mq --no-aug --name trunk_recipe_s42` |
| `trunk_recipe_s1` | cafrl_trunk | mq | flip-only | 1 | Trunk-recipe control, seed 1. | `python -m src.scripts.train_baseline --model cafrl_trunk --protocol mq --no-aug --name trunk_recipe_s1 --seed 1` |
| `trunk_recipe_s2` | cafrl_trunk | mq | flip-only | 2 | Trunk-recipe control, seed 2. | `python -m src.scripts.train_baseline --model cafrl_trunk --protocol mq --no-aug --name trunk_recipe_s2 --seed 2` |
| `f1_none_fair_s42` | cafrl | mq | flip-only | 42 | F1 — the full frequency stack on the narrow trunk, trained with the fair recipe (Phase 5.3). | `CUDA_VISIBLE_DEVICES=1 python -m src.train --config configs/phase5/f1_none_fair_s42.yaml --name f1_none_fair_s42` |
| `f1_none_fair_s1` | cafrl | mq | flip-only | 1 | F1 confirmation seed 1 (Phase 5.6). | `python -m src.train --config configs/phase5/f1_none_fair_s1.yaml --name f1_none_fair_s1` |
| `f1_none_fair_s2` | cafrl | mq | flip-only | 2 | F1 confirmation seed 2 (Phase 5.6). | `python -m src.train --config configs/phase5/f1_none_fair_s2.yaml --name f1_none_fair_s2` |
| `f2_spatres_full_s42` | cafrl | mq | flip-only | 42 | F2 — the frequency residual on the full 1280-d trunk, fair recipe (Phase 5.4). | `CUDA_VISIBLE_DEVICES=1 python -m src.train --config configs/phase5/f2_spatres_full_s42.yaml --name f2_spatres_full_s42` |
| `f2_spatres_full_s1` | cafrl | mq | flip-only | 1 | F2 confirmation seed 1 (Phase 5.6). | `python -m src.train --config configs/phase5/f2_spatres_full_s1.yaml --name f2_spatres_full_s1` |
| `f2_spatres_full_s2` | cafrl | mq | flip-only | 2 | F2 confirmation seed 2 (Phase 5.6). | `python -m src.train --config configs/phase5/f2_spatres_full_s2.yaml --name f2_spatres_full_s2` |
| `b7_effnet_b0_mq_fliponly` | effnet_b0 | mq | flip-only | 42 | b7 — the 4.0 M capacity- and augmentation-matched spatial backbone that fired the STOP-gate. | `python -m src.scripts.train_baseline --model effnet_b0 --protocol mq --no-aug --name b7_effnet_b0_mq_fliponly` |
| `b7_effnet_b0_mq_fliponly_s1` | effnet_b0 | mq | flip-only | 1 | b7 seed 1. | `python -m src.scripts.train_baseline --model effnet_b0 --protocol mq --no-aug --name b7_effnet_b0_mq_fliponly_s1 --seed 1` |
| `b7_effnet_b0_mq_fliponly_s2` | effnet_b0 | mq | flip-only | 2 | b7 seed 2. | `python -m src.scripts.train_baseline --model effnet_b0 --protocol mq --no-aug --name b7_effnet_b0_mq_fliponly_s2 --seed 2` |
| `b1_xception_lit` | xception | lit | standard policy | 42 | Xception under the literature protocol with the standard augmentation policy (the anchor-matching run). | `python -m src.scripts.train_baseline --model xception --protocol lit --name b1_xception_lit` |
| `b1_xception_lit_fliponly` | xception | lit | flip-only | 42 | Xception, literature protocol, flip-only — the under-reproducing arm that exposed the augmentation confound. | `python -m src.scripts.train_baseline --model xception --protocol lit --no-aug --name b1_xception_lit_fliponly` |
| `b2_f3net_lit` | f3net | lit | standard policy | 42 | F3-Net (documented FAD-only port) under the literature protocol with augmentation. | `python -m src.scripts.train_baseline --model f3net --protocol lit --name b2_f3net_lit` |
| `b2_f3net_lit_fliponly` | f3net | lit | flip-only | 42 | F3-Net, literature protocol, flip-only. | `python -m src.scripts.train_baseline --model f3net --protocol lit --no-aug --name b2_f3net_lit_fliponly` |
| `b3_freqnet_lit` | freqnet | lit | standard policy | 42 | FreqNet under the literature protocol — the first published video-level c40 number for it. | `python -m src.scripts.train_baseline --model freqnet --protocol lit --name b3_freqnet_lit` |
| `b4_xception_mq` | xception | mq | standard policy | 42 | Xception on multi-CRF data with augmentation — the strongest baseline overall. | `python -m src.scripts.train_baseline --model xception --protocol mq --name b4_xception_mq` |
| `b4b_xception_mq_fliponly` | xception | mq | flip-only | 42 | Xception on multi-CRF data, flip-only — the augmentation-matched control, and the real-CRF arm of the +7.3 pt compression-diversification contrast. | `python -m src.scripts.train_baseline --model xception --protocol mq --no-aug --name b4b_xception_mq_fliponly` |
| `b5_f3net_mq` | f3net | mq | standard policy | 42 | F3-Net on multi-CRF data with augmentation. *(not in the manuscript)* | `python -m src.scripts.train_baseline --model f3net --protocol mq --name b5_f3net_mq` |
| `b6_freqnet_mq` | freqnet | mq | standard policy | 42 | FreqNet on multi-CRF data with augmentation. *(not in the manuscript)* | `python -m src.scripts.train_baseline --model freqnet --protocol mq --name b6_freqnet_mq` |
| `p2a_xcep_jpeg` | xception | lit | flip-only | 42 | P2a — synthetic JPEG-quality augmentation instead of real CRF re-encodes; the 0.890 side of the +7.3 pt contrast against b4b_xception_mq_fliponly (0.963). | `python -m src.scripts.train_baseline --model xception --no-aug --p2 jpeg-aug --name p2a_xcep_jpeg` |
| `r1_fairn_grl_s42` | cafrl | mq | flip-only | 42 | E1 — Fair-N plus the adversarial (GRL) compression-invariance loss, fair recipe, seed 42 (registered tests T1/T2). | `python -m src.train --config configs/phase6/r1_fairn_grl_s42.yaml --name r1_fairn_grl_s42` |
| `r1_fairn_grl_s1` | cafrl | mq | flip-only | 1 | E1 — Fair-N plus the adversarial (GRL) compression-invariance loss, fair recipe, seed 1 (registered tests T1/T2). | `python -m src.train --config configs/phase6/r1_fairn_grl_s1.yaml --name r1_fairn_grl_s1` |
| `r1_fairn_grl_s2` | cafrl | mq | flip-only | 2 | E1 — Fair-N plus the adversarial (GRL) compression-invariance loss, fair recipe, seed 2 (registered tests T1/T2). | `python -m src.train --config configs/phase6/r1_fairn_grl_s2.yaml --name r1_fairn_grl_s2` |
| `r1_sb_noc40_s42` | effnet_b0 | mq | flip-only | 42 | E2a — SpatialBase trained without the c40 level (c0–c36), seed 42 (registered tests T3, T5). | `python -m src.scripts.train_baseline --config configs/phase6/r1_sb_noc40_s42.yaml --name r1_sb_noc40_s42` |
| `r1_sb_noc40_s1` | effnet_b0 | mq | flip-only | 1 | E2a — SpatialBase trained without the c40 level (c0–c36), seed 1 (registered tests T3, T5). | `python -m src.scripts.train_baseline --config configs/phase6/r1_sb_noc40_s1.yaml --name r1_sb_noc40_s1` |
| `r1_sb_noc40_s2` | effnet_b0 | mq | flip-only | 2 | E2a — SpatialBase trained without the c40 level (c0–c36), seed 2 (registered tests T3, T5). | `python -m src.scripts.train_baseline --config configs/phase6/r1_sb_noc40_s2.yaml --name r1_sb_noc40_s2` |
| `r1_sb_noc36c40_s42` | effnet_b0 | mq | flip-only | 42 | E2b — SpatialBase trained without c36 and c40 (c0–c32), seed 42 (secondary). | `python -m src.scripts.train_baseline --config configs/phase6/r1_sb_noc36c40_s42.yaml --name r1_sb_noc36c40_s42` |
| `r1_sb_noc36c40_s1` | effnet_b0 | mq | flip-only | 1 | E2b — SpatialBase trained without c36 and c40 (c0–c32), seed 1 (secondary). | `python -m src.scripts.train_baseline --config configs/phase6/r1_sb_noc36c40_s1.yaml --name r1_sb_noc36c40_s1` |
| `r1_sb_noc36c40_s2` | effnet_b0 | mq | flip-only | 2 | E2b — SpatialBase trained without c36 and c40 (c0–c32), seed 2 (secondary). | `python -m src.scripts.train_baseline --config configs/phase6/r1_sb_noc36c40_s2.yaml --name r1_sb_noc36c40_s2` |
| `r1_sb_jpeg_all_s42` | effnet_b0 | mq | flip-only | 42 | E3a — SpatialBase trained on c0 frames with PSNR-matched JPEG in place of every H.264 level, seed 42 (registered tests T4, T5). | `python -m src.scripts.train_baseline --config configs/phase6/r1_sb_jpeg_all_s42.yaml --name r1_sb_jpeg_all_s42` |
| `r1_sb_jpeg_all_s1` | effnet_b0 | mq | flip-only | 1 | E3a — SpatialBase trained on c0 frames with PSNR-matched JPEG in place of every H.264 level, seed 1 (registered tests T4, T5). | `python -m src.scripts.train_baseline --config configs/phase6/r1_sb_jpeg_all_s1.yaml --name r1_sb_jpeg_all_s1` |
| `r1_sb_jpeg_all_s2` | effnet_b0 | mq | flip-only | 2 | E3a — SpatialBase trained on c0 frames with PSNR-matched JPEG in place of every H.264 level, seed 2 (registered tests T4, T5). | `python -m src.scripts.train_baseline --config configs/phase6/r1_sb_jpeg_all_s2.yaml --name r1_sb_jpeg_all_s2` |
| `r1_sb_jpeg_noc40_s42` | effnet_b0 | mq | flip-only | 42 | E3b — E2a with PSNR-matched JPEG in place of the H.264 levels (no c40-matched quality), seed 42 (registered tests T4, T5). | `python -m src.scripts.train_baseline --config configs/phase6/r1_sb_jpeg_noc40_s42.yaml --name r1_sb_jpeg_noc40_s42` |
| `r1_sb_jpeg_noc40_s1` | effnet_b0 | mq | flip-only | 1 | E3b — E2a with PSNR-matched JPEG in place of the H.264 levels (no c40-matched quality), seed 1 (registered tests T4, T5). | `python -m src.scripts.train_baseline --config configs/phase6/r1_sb_jpeg_noc40_s1.yaml --name r1_sb_jpeg_noc40_s1` |
| `r1_sb_jpeg_noc40_s2` | effnet_b0 | mq | flip-only | 2 | E3b — E2a with PSNR-matched JPEG in place of the H.264 levels (no c40-matched quality), seed 2 (registered tests T4, T5). | `python -m src.scripts.train_baseline --config configs/phase6/r1_sb_jpeg_noc40_s2.yaml --name r1_sb_jpeg_noc40_s2` |
| `r1_sb_c23only_s42` | effnet_b0 | mq | flip-only | 42 | Anchor — SpatialBase trained on c23 only, seed 42 (the reference point of the registered ratio test T3). | `python -m src.scripts.train_baseline --config configs/phase6/r1_sb_c23only_s42.yaml --name r1_sb_c23only_s42` |
| `r1_sb_c23only_s1` | effnet_b0 | mq | flip-only | 1 | Anchor — SpatialBase trained on c23 only, seed 1 (the reference point of the registered ratio test T3). | `python -m src.scripts.train_baseline --config configs/phase6/r1_sb_c23only_s1.yaml --name r1_sb_c23only_s1` |
| `r1_sb_c23only_s2` | effnet_b0 | mq | flip-only | 2 | Anchor — SpatialBase trained on c23 only, seed 2 (the reference point of the registered ratio test T3). | `python -m src.scripts.train_baseline --config configs/phase6/r1_sb_c23only_s2.yaml --name r1_sb_c23only_s2` |
| `r1_abl_lrbb_s42` | cafrl | mq | flip-only | 42 | E13 — Fair-N with one recipe change reverted: the backbone learning rate set back to the shipped value (1e-5); one seed, descriptive. | `python -m src.train --config configs/phase6/r1_abl_lrbb_s42.yaml --name r1_abl_lrbb_s42` |
| `r1_abl_lrfreq_s42` | cafrl | mq | flip-only | 42 | E13 — Fair-N with one recipe change reverted: the frequency-path learning rate set back to the shipped value (1e-4); one seed, descriptive. | `python -m src.train --config configs/phase6/r1_abl_lrfreq_s42.yaml --name r1_abl_lrfreq_s42` |
| `r1_abl_aux_s42` | cafrl | mq | flip-only | 42 | E13 — Fair-N with one recipe change reverted: the auxiliary losses switched back on at their shipped weights; one seed, descriptive. | `python -m src.train --config configs/phase6/r1_abl_aux_s42.yaml --name r1_abl_aux_s42` |
| `r1_abl_ep50_s42` | cafrl | mq | flip-only | 42 | E13 — Fair-N with one recipe change reverted: the training length set back to the shipped 50 epochs; one seed, descriptive. | `python -m src.train --config configs/phase6/r1_abl_ep50_s42.yaml --name r1_abl_ep50_s42` |
| `r1_abl_curriculum_s42` | cafrl | mq | flip-only | 42 | E13 — Fair-N with the shipped three-phase curriculum restored; the first run, stopped at epoch 14 by the registered divergence rule and scored from its epoch-13 checkpoint. Reported in one supplement row; the main text reports the identical re-run. | `python -m src.train --config configs/phase6/r1_abl_curriculum_s42.yaml --name r1_abl_curriculum_s42` |
| `r1x_abl_curriculum_rerun_s42` | cafrl | mq | flip-only | 42 | E13 curriculum arm — the identical re-run of the stopped first run (same configuration, nothing changed); the canonical curriculum run the paper reports. | `python -m src.train --config configs/phase6x/r1x_abl_curriculum_rerun_s42.yaml --name r1x_abl_curriculum_rerun_s42` |
| `r1x_abl_curriculum_nostop_s42` | cafrl | mq | flip-only | 42 | Curriculum arm re-run without the divergence stop rule, all 30 epochs (post hoc; supplement only). | `python -m src.train --config configs/phase6x/r1x_abl_curriculum_nostop_s42.yaml --name r1x_abl_curriculum_nostop_s42` |
| `r1x_abl_curriculum_emafix_s42` | cafrl | mq | flip-only | 42 | Curriculum arm re-run with the EMA-only fix (train.ema_own_bn_stats: the EMA keeps batch-norm statistics computed from its own weights; post hoc; supplement only). | `python -m src.train --config configs/phase6x/r1x_abl_curriculum_emafix_s42.yaml --name r1x_abl_curriculum_emafix_s42` |

Runs marked *(not in the manuscript)* are released for completeness: they were run
and their numbers exist, but no cell of the current manuscript prints them.

## Configurations for arms that never ran

`launch/` also contains configurations for the A1 bake-off arms (`a1_hsic_*`,
`a1_both_*`) and the A2/A3/A6 ablation sweeps. Those experiments were gated behind
the STOP-gate, which fired, so they were never executed — about 270 GPU-hours that
the gate saved. They are released because the fact that they were fully specified
and then deliberately not run is part of what the paper claims about the protocol.

## Known errors in these files

Released as they were run, including their mistakes; the corrections are here rather than in the files.

- `configs/launch/f2_spatres_full_s42.yaml` carries a stale capacity comment ("F2 ~13.3M vs b7 4.0M"). The correct trainable-parameter count of that arm is **9,628,081** (~9.6 M), which is what the two confirmation seeds' configs (`..._s1.yaml`, `..._s2.yaml`) state. The comment has no effect on the run; the three configs are otherwise identical apart from the seed, and the counts are reproducible by building the model from any of them.
- Comments in these files cite internal planning documents and phase numbers that are not part of this release. They are left as written.
