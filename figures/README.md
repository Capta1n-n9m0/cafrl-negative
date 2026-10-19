# `figures/` — figure sources and the data behind them

Two of the paper's four figures (three in the main text, one in the
Supplementary Material) are drawn from measurements; both can be
regenerated here from released artifacts alone.

| file | what it is |
|---|---|
| `make_figures.py` | The paper's figure script. Draws Fig. 2 (compression sweeps, both recipes) and Fig. 3 (frequency-path read-outs; Fig. 4 in the submitted manuscript). Identical to the version that produced the published figures except for a marked three-line patch at the top that repoints its paths at this repository. |
| `figure_data.json` | Everything the script plots, in one file. |
| `fig1_architecture.tex` | Fig. 1, the architecture diagram (standalone TikZ; `pdflatex fig1_architecture.tex`). |
| `fig3_campaign_flow.tex` | Fig. S1 of the Supplementary Material (Fig. 3 in the submitted manuscript), the campaign flow with its gates and GPU-hour economics (standalone TikZ). |

```bash
python make_figures.py     # writes fig2_crf_sweep.{pdf,png}, fig4_mechanism.{pdf,png}
```

Needs matplotlib and nothing else — no GPU, no dataset.

## Where `figure_data.json` comes from

* `sweeps` — the video-AUC of 17 runs at each compression level, taken
  from `../predictions/`. The release build recomputes these from the released
  per-video scores and fails if they differ from what the published figure was
  drawn from.
* `f2_tb` — per-epoch trajectories for 3 runs (residual gate γ,
  standalone frequency-head AUC), taken from `../curves/`.
* `spatres_gamma` — 50 per-epoch values of the shipped
  spatial-residual run's fusion gate, the "collapsed" contrast curve in Fig. 3(a).
  Per-epoch values of the shipped spatial-residual run's fusion gate, read from that run's 50 per-epoch checkpoints. Those checkpoints are archival (only best*.pt ships in the deposit), so this series is released as data with its provenance stated rather than as something the release can recompute. Everything else in figure_data.json is rebuilt from predictions/ and curves/ and checked against this file on every build.

So Fig. 2 and Fig. 3(b) are fully re-derivable from this repository; Fig. 3(a) is
re-derivable except for its context curve, which is published as data.
