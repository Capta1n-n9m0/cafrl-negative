# `evaluation/analysis/` — the statistics added in revision

Five analyses that the first version of the paper did not carry, each answering a
question about the *inference* rather than about the numbers: whether the neutral
verdicts are equivalence claims that survive an equivalence test, what size of
effect the design could have detected at all, how much of the reported precision
depends on the three random seeds that happened to be run, whether the intervals
survive the identity structure of FaceForensics++, and whether the significant
results survive an adjustment for the size of the contrast family.

Everything here reads only this repository: the per-video scores in
`../../predictions/` and the frozen harness in `../src/`. No dataset, no
checkpoint, no GPU, no network.

```bash
conda env create -f ../../env/environment-verify.yml   # CPU only
conda activate cafrl-verify
python run_all.py --jobs 8            # ~2 minutes at 8 jobs, ~12 single-threaded
```

| script | question | output |
|---|---|---|
| `cluster_bootstrap.py` | do the intervals survive a coarser exchangeability unit? | `cluster_bootstrap.json` |
| `seed_uncertainty.py` | how wide are they if the seeds are resampled too? | `seed_uncertainty.json` |
| `equivalence.py` | is "no difference" defensible as an equivalence claim? | `equivalence.json` |
| `mde.py` | what effect size could this design have detected? | `mde.json` |
| `multiplicity.py` | do the significant results survive Bonferroni/Holm? | `multiplicity.json` |

`stats_common.py` holds what they share: the contrast definitions (by released run
id), the cluster definitions, and the bootstrap engines.

## The recipe is the published one

Per-video scores in **sorted pooling-key order**, seeds pooled by **per-video
mean**, **10,000** replicates, **RNG seed 0**, **percentile** intervals — the same
recipe `../rederive.py` and `../../verify/verify.py` use, so these analyses extend
the published intervals rather than competing with them. Under the plain
video-resampling scheme the engine here reproduces the frozen harness replicate
for replicate; `cluster_bootstrap.py --self-check` asserts it before doing
anything else (agreement is at the 1e-16 level, and the only difference is that
the AUC is computed from ranks rather than through scikit-learn, for speed).

Each `(contrast, scheme)` task seeds its own generator from 0, so results do not
depend on `--jobs`.

## The exchangeability unit

The published intervals resample **videos**. The official FaceForensics++ test
split is 70 identity pairs; each of its 140 identities appears once as a
manipulation *target* (the footage and head pose) and once as a *source* (the
swapped-in face), and contributes one real video. Four different clusterings
follow, and `cluster_bootstrap.py` runs all of them:

| scheme | unit | FF++ test |
|---|---|---|
| `video` | one evaluated video — **what the paper publishes** | 700 units |
| `source` | the swapped-in face identity — **the primary clustered unit** | 140 clusters of 5 |
| `target` | the footage identity | 140 clusters of 5 |
| `basevideo` | one manipulated base video (its four methods); reals alone | 280 clusters |
| `pair` | the unordered identity pair of the split — the coarsest unit | 70 clusters of 10 |

The cluster labels are derived from the released prediction keys alone: a
manipulated video is named `{target}_{source}` and a real video by its own
identity (the convention is documented in `../src/data/splits.py`). No external
metadata file is required, and the derivation is asserted to partition the
evaluation set exactly.

## The equivalence margin

`equivalence.py` tests against **δ = 1 AUC point**, and the margin is **post hoc**
— chosen after the results existed. Its justification is on the paper's own
scale: re-running the plain spatial baseline at a different random seed moves its
c40 video-AUC by more than a point (95% three-seed band ±1.60 pt), and widening
the spatial trunk — a real architectural change — is worth about a point. A
difference below either is beneath the resolution at which this study can act.
Equivalence is concluded when the whole 90% percentile interval lies inside
(−δ, +δ).

The script reports the verdict under **every** resampling unit, including the
two-level one, because the answer is not the same in all of them; `equivalence.json`
also reports, for each unit, the smallest margin at which equivalence *would* have
been concluded.

## What the outputs are for

The JSON files beside the scripts are the artifacts the manuscript's revised
statistics sections cite; `../../CLAIMS-MAP.md` maps each printed value to its key
in them. They are regenerated on every build of this repository, so a number in
the paper and a number in the JSON cannot drift apart.
