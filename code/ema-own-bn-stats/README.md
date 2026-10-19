# `code/ema-own-bn-stats/` — the EMA batch-norm flag of the V3 re-run

These files are the research code's EMA implementation, the trainer that wires the
flag into it, and their tests, copied unchanged from the research code. They are
here because the supplement names the flag and prints the V3 numbers.

## What the flag does

`train.ema_own_bn_stats` (in `configs/base/defaults.py`; default `False`) changes
one thing in `ModelEMA` (`src/training/scheduler.py`):

- **Off (default, every run except V3):** the EMA shadow copies the live model's
  batch-norm running statistics verbatim — the original code path, unchanged.
- **On (only `r1x_abl_curriculum_emafix_s42`, V3):** the EMA shadow keeps
  batch-norm statistics computed from its own forward pass with the EMA weights,
  and the buffer copy from the live model skips those batch-norm layers.

The post hoc diagnosis behind it (on the validation split only) traced the first
curriculum run's EMA collapse to the EMA weights being scored with batch-norm
statistics copied from the live model. V3 is a post hoc re-run reported in the
supplement only; the main text reports the canonical curriculum run (V1), which
trained with the flag off. The three re-run configurations are in
`configs/runs/r1x_*.yaml` and `configs/launch-r1x/`; their per-video predictions
are under `predictions/`.

## The tests, and how to run them

| file | what it checks |
|---|---|
| `src/tests/test_ema_own_bn_stats.py` | the flag's wiring: off keeps the original verbatim buffer copy; on changes only the EMA's batch-norm statistics |
| `src/tests/test_ema_bn_window.py` | the window of training steps over which the EMA's own batch-norm statistics are collected; with the flag off nothing is collected |
| `src/tests/test_phase6x_configs.py` | the three re-run configs differ from the registered curriculum arm only where declared |

These files are a record of the change, not a standalone package. The tests import
modules of the research code base that this release does not include (the training
loop, the model and the data modules), and `test_phase6x_configs.py` reads the
configs at their research-repository paths. In the research repository they run on
CPU from its root:

```bash
python -m pytest -q src/tests/test_ema_own_bn_stats.py \
    src/tests/test_ema_bn_window.py src/tests/test_phase6x_configs.py
```

To read the change: every flag-dependent branch in `src/training/scheduler.py` and
`src/training/trainer.py` is marked `W5b V3` in the source.
