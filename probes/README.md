# `probes/` — the design-time measurements the paper cites

Not every number in the paper comes out of a training run's evaluation. Three
come from small measurements taken while the model was being built: the
compression estimator's accuracy (the conditioning premise the whole design
rests on, and the number defect D6 says the adversary destroyed), the parameter
counts, and the band-energy check behind the frequency streams. They are tiny
JSON artifacts, so they are released rather than described.

| file | what it is |
|---|---|
| `p1_compression_estimator.json` | Probe P1 — compression-level estimator accuracy (Phase 1). The conditioning premise: a 6-bin compression-level classifier trained on the training split reaches +/-1-bin accuracy 0.876 on held-out crops, which is the "0.88" the manuscript contrasts with the ~0.4 the GRL arm degrades to (defect D6). The degraded side is the per-epoch `diag/est_pm1_acc` series in `curves/a0.json`. |
| `p1_compression_estimator_reconfirm.json` | Probe P1, re-confirmed on the canonical estimator module (Phase 2). The same probe re-run against the estimator module as finally built (1,370,790 parameters): +/-1-bin 0.855. The design decision (estimated rather than oracle conditioning) was taken on this number. |
| `param_counts_cafrl.json` | CAFRL parameter counts by arm and conditioning (Phase 3). Component-level trainable-parameter counts for all 16 arm x conditioning combinations. The manuscript's 11.97 M is `grl/estimated`, the default arm. The baselines' counts, and the counts of the arms as their runs actually configured them, are in `param_counts_arms.json`. |
| `param_counts_arms.json` | Parameter counts of every arm the manuscript compares. Built by `count_params.py` (released beside this file as `param_counts_arms.py`) from the configuration each released run used, with no pretrained weights loaded, so every parameter count the paper prints is derivable rather than asserted. States its counting convention: the ImageNet 1000-way classifier is replaced by a single-logit head, which is why EfficientNet-B0 reads 4.0 M rather than 5.3 M and Xception 20.8 M rather than 22.9 M; where an arm carries an adversarial discriminator the file also records the inference-time count, which excludes it. |
| `param_counts_arms.py` | The generator behind `param_counts_arms.json`. Needs the training environment (it constructs the models), not the CPU-only verification environment, so it is released for inspection rather than as part of `make verify`. |
| `param_counts_modules.json` | Frequency-module parameter counts against their design budgets (Phase 2).  |
| `band_energy.json` | Band-energy premise check on real crops (Phase 2). The measurement behind the frequency design's premise that compression attenuates high-frequency DCT bands: per-level band energies computed on real FF++ crops. Released because the design threat it speaks to (what exactly the frequency streams can see after re-encoding) is a fair question to ask of a negative result about frequency. |

Each file is the probe's own output, copied verbatim apart from local paths
being replaced with `${...}` placeholders. `../CLAIMS-MAP.md` names which
manuscript claim each one substantiates; `python ../verify/claim.py M1.6` reads
the estimator number straight out of the first file.
