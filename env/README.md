# `env/` — the environment the numbers were produced in

141 conda packages and 74 pip packages, captured from the live
environment rather than re-solved, so these files describe what actually ran.

| file | what it is | use it when |
|---|---|---|
| `../environment.yml` | Readable spec, every package pinned to version and build. | You want to re-run training or a GPU evaluation pass. |
| `conda-linux-64.explicit.txt` | The lockfile: the same conda packages as resolved URLs with MD5 checksums, no solving involved. `conda create -n cafrl --file conda-linux-64.explicit.txt`. | You want the conda side installed exactly, byte for byte. |
| `pip-freeze.txt` | The pip-installed packages with exact versions. | Alongside the explicit file, to complete the environment. |
| `environment.full.yml` | conda's own `env export`. | Belt and braces. |
| `environment-verify.yml` | CPU-only subset: Python, NumPy, SciPy, scikit-learn, matplotlib, PyYAML at the same versions. | You want to check the paper's tables. This is what `verify/` runs under. |

### On the lockfile format

There is no `conda-lock.yml` here, deliberately. A lock file of that kind is
produced by *re-solving* an abstract specification, and this environment's exact
pin set no longer re-solves against the live channel indexes — package builds age
out of them, and a solver asked to satisfy the set today either fails or quietly
substitutes a different build. `conda list --explicit --md5` involves no solver
at all: it is the list of package archives that are installed, by URL and
checksum, and `conda create --file` installs exactly those. For the purpose the
lockfile serves here — saying precisely what produced the numbers — that is the
stronger artifact, and it is what is shipped.

Key versions:

| package | version |
|---|---|
| python | 3.11.15 |
| pytorch | 2.5.1 |
| torchvision | 0.20.1 |
| numpy | 2.4.6 |
| scipy | 1.17.1 |
| scikit-learn | 1.8.0 |
| opencv-python | 4.13.0.92 |
| ffmpeg | 4.2.2 |
| x264 | 1!157.20191217 |
| timm | 1.0.27 |
| decord | 0.6.0 |
| insightface | 0.7.3 |
| tensorboard | 2.20.0 |

## What reproducing means at each layer

The paper's claim of bit-exactness applies to one layer only; the honest version
of the rest is stated in the top-level README under *Reproduction contract*, and
in short:

1. **Tables from released predictions** — exact, CPU-only, seeded bootstrap.
   Reproducible to the digit.
2. **Predictions from a released checkpoint** — needs the crops and a GPU. Training
   and evaluation ran in bfloat16 mixed precision with float32 islands in the
   frequency and loss paths, so scores differ in the low decimals across GPU,
   driver and framework builds. A fifth-decimal AUC difference here is numerics,
   not a discrepancy.
3. **A run retrained from its configuration** — bit-exact only in the deterministic
   mode (float32, single-worker loading). Under the production recipe an
   interrupted-and-resumed run diverges by up to 4e-3 in loss. Across independent
   seeds, expect the between-seed spread the paper reports (≈0.6 points of c40
   video-AUC for the spatial backbone, ≈0.25 for the fair CAFRL variants) — which
   is why the headline contrasts are three seeds against three.
