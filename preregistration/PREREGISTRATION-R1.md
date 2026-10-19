# PRE-REGISTRATION R1 — Revision 1 campaign (E1, E2, E3 + anchor, E13)

**Status:** APPROVED by the user at checkpoint C1 on 2026-10-11 (decision 2026-10-11 · "C1: the
W0 pre-registration and all its recommendations are approved"; written 2026-10-10, wave W0,
stage S4). It is **FROZEN** by the tag `phase6-prereg` that wave W7 puts on the commit that
holds it. After the tag, nothing here changes; a correction is a dated note elsewhere. Any
re-reading of a rule after campaign data are seen stops and goes to the user.

**State at writing:** no new run exists (`ls -d runs/r1_*` and `ls -d ~/sdd/exp3-cafrl-runs/r1_*`:
no match, 2026-10-10; checked again 2026-10-11, no match and no `phase6*` tag). No test-set metric of any new arm has been computed or viewed. Smoke
runs were pipeline checks only (lesson L9); no smoke validation or test metric appears here
(their step times appear, as the basis of the budget and the §8 thresholds).

**Refreshed 2026-10-11 (stage S4b):** the analysis code the first draft listed as missing (§15)
now exists, and the hashes below are the current files. Nothing in the registered defaults or
alternatives changed.

**Run plan:** [`docs/phases/phase6.md`](../../docs/phases/phase6.md).

**Machinery** (what the `phase6-prereg` tag freezes; sha256 computed with `sha256sum` on
2026-10-11; the code hashes equal the files at the S4b commit, which commits the code first and
these documents after it):

| File | Role | sha256 |
|---|---|---|
| `src/evaluation/phase6_stats.py` | confirmatory tests, sensitivity test, seed-count rules, E13 intervals | `a301d024befa13e4001b7aa471e914cded6c0f6ca1fa9b446b753c86cbabb074` |
| `src/scripts/phase6_mde.py` | MDEs, at any per-arm seed count | `bc1c246e4267e6558d73a29ecbb2af2f39c325296b1f6aa92e5ee7ed7f637abc` |
| `src/scripts/phase6_monitor.py` | W7 anomaly monitor (§8) | `2b84e37cc3401a564576c0578edd7220b53eba8b4d710fff00f5ddf2a9bfb9e0` |
| `src/scripts/phase6_data/jpeg_official_targets.py` | generator of the C1 alternative calibration | `30a469266f153d0a13177351a8af1334f85ca7636678e6256d45dbe7790ab18f` |
| `runs/phase6_build/launch.sh` | W7 launcher | `5bd84d11005122d9cc62dcefb7b15959c49a2914d432cb445ec4821c59a64d3c` |
| `runs/phase6_build/launch_queue.txt` | the 23-job queue | `f6fca51536e7fdbd66d9469c71aa179921c5b2ececbae93c037bf2840cfc1f03` |
| `configs/phase6/MANIFEST.json` | per-YAML sha256 of the 23 configs | `6d69442d9421c27436fd769711f9a73f1866c35d3ba5d247e954f75717637e93` |
| `runs/phase6_build/jpeg_calibration.json` | JPEG QFs, official targets (chosen at C1, 2026-10-11); was `f14c3b9cf5f49e2236a9e80520327752cc0123fd61096cdd31bdd8f62a18fbc2` (registered default before C1) | `a7286bbd8457adb9716a3f2c2397c18c02a8e0326bcb8795604b9dc60b82ec19` |
| `runs/phase6_build/jpeg_calibration.official-targets.json` | JPEG QFs, C1 alternative (§13) | `a7286bbd8457adb9716a3f2c2397c18c02a8e0326bcb8795604b9dc60b82ec19` |
| `runs/phase6_build/mde.json` | MDEs at k = 3 (§5) | `7f48465b4a5744781af1ef68c70298dcb33f1712626033ccc8b9a8dca8e2bc55` |
| `runs/phase6_build/mde_k2.json` | MDEs at k = 2 (§5) | `4a82b2eec4c7f3313f5a39d8dd3f8a2fbd523fcc524ef3b9c4204a8081d30d50` |
| `runs/phase6_build/mde.md` | MDE tables, k = 3 and a k = 2 section | `f1fa371d14ae02b6122f74f75fb58df065d9963c2e39f836f7afec80af7266b4` |

*2026-10-11 (W7-P, C1 applied):* `jpeg_calibration.json` is now a byte-identical copy of
`jpeg_calibration.official-targets.json` (Run plan step 0b); the two rows carry the same hash.

The 23 YAMLs are covered through `MANIFEST.json`: it lists each YAML's sha256, and all 23 were
checked equal on 2026-10-11 (23 entries, 23 equal, no YAML on disk unlisted) by re-hashing every
`configs[].config` against `configs[].sha256`; `pytest src/tests/test_phase6_configs.py` makes the
same check.

**MDE provenance.** `mde.json` and `mde_k2.json` record, in their `code_sha256` fields, the
code that produced them: `mde.json` the pre-S2b `phase6_mde.py` (`85bf1ce7…`) and
`phase6_stats.py` (`5bd2fefa…`); `mde_k2.json` the pre-fix `phase6_mde.py` (`88f92ecb…`) and the S2b-era
`phase6_stats.py` (`5a191919…`). The
k = 3 values are unchanged under the current code: S2b regenerated `mde.json` and found 0
numeric differences, only the provenance fields differed (`steps/S2b.md` §3–4). Both files are
kept as registered (decision proposed in S2b, "Phase 6: mde.json stays as registered; k = 2
MDEs live in mde_k2.json").

**Sources of record:** kickoff `docs/phases/next-session-prompt.md` §3; `paper/revision-1/plan.md`
§2–§4; `docs/decisions.md` (the entries dated 2026-10-10 and 2026-10-11 starting "Revision 1" or
"Phase 6"). Decisions are cited by date + title; their dates are in the §13 table.

Plain names: **Fair-N** = CAFRL without invariance loss under the fair recipe
(`runs/f1_none_fair_s{42,1,2}`). **b7 / SpatialBase-all** = EfficientNet-B0 on all six H.264
levels, flip-only (`runs/b7_effnet_b0_mq_fliponly{,_s1,_s2}`). **Anchor** = SpatialBase on c23
only. **"Pending C1"** marks a registered default the user may flip at C1 with a one-line
change; every such item is in the table of §13.
*2026-10-11 (W7-P):* C1 resolved every "pending C1" marker in this document; §13 records
each outcome. Only the JPEG targets flipped; every other marked item is the registered default.

---

## 1. Arms and runs

23 runs, configs `configs/phase6/<run>.yaml` (`MANIFEST.json` sha256
`6d69442d9421c27436fd769711f9a73f1866c35d3ba5d247e954f75717637e93`). Full arm table with diffs:
`docs/phases/phase6.md` §Arm table.

| Arm | Runs | Seeds | Role |
|---|---|---|---|
| E1 `r1_fairn_grl` | 3 | 42, 1, 2 | Fair-N + adversarial loss, λmax 0.5, ramp from step 0 |
| E2a `r1_sb_noc40` | 3 | 42, 1, 2 | SpatialBase on c0–c36; never touches c40 |
| E2b `r1_sb_noc36c40` | 3 | 42, 1, 2 | SpatialBase on c0–c32 (descriptive only) |
| E3a `r1_sb_jpeg_all` | 3 | 42, 1, 2 | c0 frames, PSNR-matched JPEG for every level |
| E3b `r1_sb_jpeg_noc40` | 3 | 42, 1, 2 | as E3a without the c40-matched QF |
| Anchor `r1_sb_c23only` | 3 | 42, 1, 2 | SpatialBase on c23 only |
| E13 `r1_abl_{curriculum,lrbb,lrfreq,aux,ep50}` | 5 | 42 | Fair-N with one recipe change reverted (descriptive) |

Existing comparators (frozen, read only): Fair-N ×3 and b7 ×3 per-video test predictions.

**JPEG quality factors of E3a/E3b** (chosen at C1, 2026-10-11: the official-encode targets):
c23 60, c28 33, c32 23, c36 16, c40 10 (`runs/phase6_build/jpeg_calibration.json` →
`level_to_qf`, status final, sha256
`a7286bbd8457adb9716a3f2c2397c18c02a8e0326bcb8795604b9dc60b82ec19`; c23/c40 matched on mean crop
PSNR to the official FF++ c23/c40 encodes, aligned; c28–c36 to the regenerated crops).
*History:* the registered default before C1 was c23 54, c28 33, c32 23,
c36 16, c40 11, matched on mean crop PSNR to our x23/x40 re-encodes and the regenerated
c28–c36 crops (the file then had sha256
`f14c3b9cf5f49e2236a9e80520327752cc0123fd61096cdd31bdd8f62a18fbc2`). Alternative, recommended in
decision "Phase 6: JPEG targets for c23/c40 — the 0.5 dB trigger fired": the official-encode
targets, QF c23 60 and c40 10. That file is built and validated:
`runs/phase6_build/jpeg_calibration.official-targets.json`, sha256
`a7286bbd8457adb9716a3f2c2397c18c02a8e0326bcb8795604b9dc60b82ec19`. If C1 chooses it, it is copied
over `jpeg_calibration.json` before the tag, and the registered hash becomes that one
(2026-10-11). Related, also pending C1:
decision "Phase 6: official c23/c40 PSNR measured aligned, calibration stays on our re-encodes".
*2026-10-11 (W7-P):* C1 chose the official targets; the file was copied (step 0b) and the
registered hash is now `a7286bbd…2ec19`. The related decision's default (targets from our
re-encodes) is superseded by that choice for c23/c40 (§13).

**Level mix of the SpatialBase arms** (registered default, pending C1; decision "Phase 6 build:
compensated singles quota for asymmetric level sets"): the baseline trainer solves the singles
quota so the whole-plan group mix is 0.3 / 0.4 / 0.3 (clean / medium / heavy). For c0–c36
(E2a, E3b) the heavy group rises from 25.6 % under the old code to 30 %; for c0–c32 (E2b) the
mix renormalizes to 0.4286 / 0.5714 (`steps/S0.md` §3.4). Alternative: the old rule (25.6 %),
disclosed. The six-level and c23-only plans are identical under both rules (`steps/S2.md` §2).

**Checkpoint selection** is fixed per arm before training and never varies afterwards:
CAFRL arms (E1, E13) = EMA weights, best mean val AUC over c23 + c40 (Fair-N's rule);
SpatialBase arms = best mean val AUC over their selector levels on real H.264 validation crops
(b7, E3a, anchor c23 + c40; E2a, E3b c23 + c36; E2b c23 + c32). Never the test split.

**Lesson L2, stated:** the E13 curriculum arm uses baby_step, which ignores the YAML
`w_cons`/`w_phase` and applies its own hard-coded values (phase B 0.5/0.3, phase C 0.3/0.3,
phase A 0/0 with the backbone frozen; `src/training/curriculum.py:132-150`). The arm therefore
reverts the curriculum *together with* those weights; it cannot separate them.

## 2. Hypotheses (each can come out against us)

The paper's current narrative is `docs/24-fair-retest-conclusion.md` §6, lowered by the
reviewers (`paper/revision-1/plan.md` §4).

- **E1 — the adversary under the fair recipe.** Null: E1 and Fair-N have the same mean
  single-model AUC at c40 (T1) and on AUC_comp (T2). Current narrative (docs/24 §6 item 4,
  context only): the adversarial invariance "added nothing". **Against us:** T1 or T2 reads
  *helps*; the paper then says the adversary contributes under the fair recipe.
- **E2 — leaving c40 out.** Null: retention R = 1, i.e. the c40 gain of multi-level training
  over c23-only training survives fully without c40 (T3). Testing against R = 1 makes "the
  gain survives" the claim that must resist rejection. **Against us:** R significantly below 1
  limits the robustness claim to the training levels; *not estimable* means the c40 gain of
  multi-level over c23-only training is not established at all. E2b is descriptive.
- **Anchor's role.** The anchor is not tested on its own. It is the zero point of R: the
  denominator b7 − anchor at c40. Expectation from the narrative: the denominator is clearly
  positive. **Against us:** its 95 % interval includes 0 (T3 reads not estimable).
- **E3 — codec versus image quality** (the 2×2: H.264-all = b7 ×3, H.264-no-c40 = E2a,
  JPEG-all = E3a, JPEG-no-c40 = E3b). Null for T4: real H.264 and PSNR-matched JPEG training
  give the same c40 AUC. Current narrative (docs/24 §6 item 3, context only; from an unmatched,
  single-seed Xception JPEG arm): real compression variants beat synthetic JPEG. **Against
  us:** T4 reads *harms* (JPEG better) or *no detectable difference*. Null for T5: including
  the c40-level data does not change c40 AUC. T5 *helps* narrows robustness to exposure to
  that level; *no detectable difference* gives no evidence that c40 exposure is needed.
  **Against us** (narrative item 3, docs/24 §6: robustness bought by training on varied real
  compression levels): T5 reads *no detectable difference* (c40-level data are not shown to be
  needed, so "diversity of levels" is not shown to be what buys c40 robustness) or *harms*
  (including c40-level data lowers c40 AUC).
- **E13 — which recipe change did the work.** Descriptive, no null test. Current narrative
  (docs/24 §6 item 1, context only): CAFRL-as-specified lost to its recipe. **Against us:** no
  single reverted change moves c40 AUC or AUC_comp outside Fair-N s42's fixed-seed interval;
  then the paper says no single change accounts for the recipe effect.

## 3. Endpoints

- **Unit:** video-level AUC on the official FF++ test split (700 videos from 70 test pairs: 140 real, 560 fake;
  `mde.json` → `n_videos` 700; `steps/S0.md` §3.1). Frame scores are pooled per `(video_id, method)` key (lesson
  L8; FF++ files are `{target}_{source}.mp4`).
- **c40:** video AUC at c40. **AUC_comp:** mean of the video AUCs at c28, c32, c36, c40,
  levels weighted equally, the same video resample at every level (`phase6_stats.COMP_LEVELS`).
- **Primary estimand** (decision "Phase 6 analysis: the primary estimand is the mean
  single-model AUC", pending C1): per arm, the mean over seeds of each seed's AUC.
  Alternative: the ensemble AUC (AUC of the per-video mean score over seeds). The ensemble is
  always reported as secondary (§6).
- Frame-level and video-level numbers are never mixed in one table.

## 4. Confirmatory family — exactly five tests, Holm

Kickoff §3 and decisions "Revision 1 W0: build defaults" (6), "Phase 6 analysis: endpoints of
the E2/E3 tests" (pending C1). Weights as built in `phase6_stats.CONFIRMATORY`.

| Test | Contrast | Endpoint | Null |
|---|---|---|---|
| **T1** | E1 − Fair-N | c40 | 0 |
| **T2** | E1 − Fair-N | AUC_comp | 0 |
| **T3** | R = (E2a − anchor) / (b7 − anchor) | c40 | R = 1 |
| **T4** codec effect | ½[(b7 − E3a) + (E2a − E3b)] = H.264 minus JPEG, averaged over c40 exposure | c40 | 0 |
| **T5** c40-exposure effect | ½[(b7 − E2a) + (E3a − E3b)] = with minus without c40, averaged over codec | c40 | 0 |

The interaction (b7 − E3a) − (E2a − E3b) at c40 is **descriptive**, outside the family.

**Primary interval and p-value** (one engine for all five, `phase6_stats.hierarchical_bootstrap`):
- B = 10,000 replicates, `numpy.random.default_rng(0)` (the module's `RNG_SEED`, recorded in the
  output), arms drawn in the fixed order E1, FairN, b7, E2a, anchor, E3a, E3b.
- Each replicate: per arm, resample its k seeds with replacement (the same draw at every
  level); then **one** resample of the 140 source-identity clusters (`mde.json` →
  `n_clusters`), shared by every arm and level; a one-class draw is redrawn.
- Interval: 95 % percentile of the replicates. Point estimate: the un-resampled value.
- p-value (decision "Phase 6 analysis: bootstrap p-value form, not-estimable retention, MDE as
  specified, seed-variance floor", pending C1):
  p = min(1, (2·min(#{T* − T0 ≤ 0}, #{T* − T0 ≥ 0}) + 1)/(B + 1)), ties on both tails;
  T0 = 0 for T1, T2, T4, T5 and T0 = 1 for T3 (R* − 1). Alternative: 2·(min + 1)/(B + 1).
- **Retention:** R* = numerator*/denominator* per replicate (0/0 set to 1, counted on both
  tails). T3 reads **not estimable** if the denominator's 95 % percentile interval includes 0;
  it then enters Holm with **p = 1** (alternative: Holm over four).
- **Multiplicity:** Holm step-down over the five p-values at family α = 0.05.
- **Reading rule:** not estimable → "not estimable"; Holm-adjusted p < 0.05 → *helps* or
  *harms* by the side of the null holding the larger bootstrap mass (for T3: R > 1 or R < 1);
  otherwise **"no detectable difference"**. There is **no confirmatory equivalence test**
  (decision "Revision 1 W0: no confirmatory equivalence tests").

**Command (after C1 only; refuses without `--post-c1` and the tag):**
`python -m src.evaluation.phase6_stats --post-c1 --manifest runs/phase6_build/stats/manifest.json --mde runs/phase6_build/mde.json --out runs/phase6_build/stats/confirmatory.json`,
where the manifest maps E1 → `runs/r1_fairn_grl_s{42,1,2}/report.json`, FairN →
`runs/f1_none_fair_s{42,1,2}/report.json`, b7 → `runs/b7_effnet_b0_mq_fliponly{,_s1,_s2}/report.json`,
E2a → `runs/r1_sb_noc40_s*`, anchor → `runs/r1_sb_c23only_s*`, E3a → `runs/r1_sb_jpeg_all_s*`,
E3b → `runs/r1_sb_jpeg_noc40_s*` (each `report.json`, seeds 42, 1, 2).

**Stopped runs stay in the analysis** (proposed by S4 fixer, pending C1). A run stopped under §8
for NaN/inf, divergence or any other anomaly is **not dropped**. Its last saved `best.pt` (the
best-validation checkpoint under the arm's unchanged selection rule, written before the stop) is
evaluated by hand on every cell with the run's standard evaluation commands (config header;
`eval_battery` + `eval_faceshifter`, then `phase6_check_report.py`), logged in the journal. The
run then enters T1–T5 and every secondary analysis like a completed run, flagged in every table
as "stopped at epoch N (reason)". A run is **failed** only if it has no `best.pt` (or the
by-hand evaluation of it cannot complete); it is reported as failed (§10) and its arm uses the
remaining seeds under the next rule. Alternative: drop the stopped run and test on k = 2 seeds.
Direction of the alternative: the arm most likely to stop is E1 (the adversary is what is under
test); dropping its unstable seeds biases T1/T2 away from *harms*, toward the narrative.

**Fewer than 3 seeds** (proposed by S4, pending C1): if a run of an arm is failed in the sense
above and is not replaced under §8, the tests use the seeds that exist (k = 2) and the
as-specified MDE is recomputed at that k with `phase6_mde.py`'s method and reported. If an arm
in a test has fewer than 2 seeds, that test reads **not estimable** and enters Holm with p = 1.
Alternative: hold the analysis until a replacement seed exists. Both rules are in the code
(S2b, commit f70dc43): `phase6_stats.py` writes the per-arm seed counts and the < 2-seed rule
under the output key `seed_count_rule`, and flags `mde_seed_count_mismatch` when the attached
MDE file was computed at other seed counts; `phase6_mde.py --k-arm ARM=K` computes the MDE at
unequal k (the W7 step is in `docs/phases/phase6.md`, Run plan).

**Reading rules at the seed counts that ran** (2026-10-11; decision "Phase 6 analysis: MDE and
degenerate-test reading rules"). Each choice gives the larger MDE or p-value:
- A "no detectable difference" sentence quotes the **larger** of the as-specified MDEs at the
  seed counts that actually ran (k = 2 or 3) and at k = 3.
- When any arm ends with k ≠ 3 seeds, W7 recomputes the MDE with `phase6_mde.py --k-arm`
  before writing any sentence, and attaches that file to the analysis.
- A sensitivity test (§6.1) with SE = 0 reads "degenerate (SE = 0; not evaluable)" and enters
  its Holm column with p = 1.

## 5. Minimum detectable effects

80 % power, k = 3 seeds per arm, AUC points (`runs/phase6_build/mde.md`; `mde.json` →
`tests_by_id.<T>`). **Headline = MDE of the test as specified** (the conservative bootstrap
that will run), with each family's seed variance floored at the test-set interaction d.
Beside it: the design MDE (a test calibrated to the true SE). α = 0.01 is Holm's worst-case
first step (0.05/5); α = 0.05 is its last step.

| Test | Variance from | **As specified α 0.01 / 0.05** | Design (true variance) α 0.01 / 0.05 | Actual α of the test at nominal 0.05 |
|---|---|---|---|---|
| T1 (c40) | Fair-N (floor binds) | **1.78 / 1.43** | 1.27 / 1.05 | 0.003 |
| T2 (AUC_comp) | Fair-N (floor binds) | **1.37 / 1.10** | 0.98 / 0.80 | 0.003 |
| T4 (c40) | b7 | **1.46 / 1.18** | 1.27 / 1.04 | 0.019 |
| T5 (c40) | b7 | **1.46 / 1.18** | 1.27 / 1.04 | 0.019 |

**T3's MDE depends on the anchor gap** G = b7 − anchor at c40, which no run has measured yet.
MDE = 1 − R (lower side), as specified (design in brackets), α 0.01 / 0.05:

| G (pt) | 1.00 | 2.00 | 3.00 | 5.00 | 7.50 | 9.52 | 10.50 |
|---|---|---|---|---|---|---|---|
| MDE | > 2 / > 2 | 1.25 / 0.88 (0.96 / 0.75) | 0.70 / 0.56 (0.61 / 0.49) | 0.42 / 0.34 (0.37 / 0.30) | 0.28 / 0.23 (0.25 / 0.20) | 0.22 / 0.18 (0.20 / 0.16) | 0.20 / 0.16 (0.18 / 0.14) |
| P(not estimable) | 0.647 | 0.059 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

Gap proxies from published single-seed pairs on other backbones: Xception 10.50 pt, F3-Net
9.52 pt (`mde.md`). With the anchor's seed σ doubled, at G = 10.5: 0.20 / 0.16
(`mde.json` → `tests_by_id.T3.sensitivity_anchor_sigma_x2_as_specified`).

Inputs: b7 seed σ (ddof 1, pt) c28 0.240, c32 0.446, c36 0.561, **c40 0.645**, AUC_comp 0.472;
Fair-N c28 0.524, c32 0.411, c36 0.504, c40 0.251, AUC_comp 0.342 (`mde.md`). The floor binds for
T1 because Fair-N's c40 σ (0.251) is below √d_T1 ≈ 0.457 pt, and for T2 because Fair-N's
AUC_comp σ (0.342) is below √d_T2 ≈ 0.351 pt (`mde.json` → `tests_by_id.T1.d` = 2.087e-5,
`tests_by_id.T2.d` = 1.234e-5). E1 is assumed to have Fair-N's variance; an
active adversary may add seed variance, which would raise the true MDE.

**Rule:** every "no detectable difference" reading quotes the **as-specified** MDE of that test
(for T3, at the grid gap closest to the observed G from below, i.e. the larger MDE), never the
design MDE alone (decision "Phase 6 analysis: the conservative bootstrap is kept, with a
calibrated sensitivity test", pending C1).

**Fewer than 3 seeds** (2026-10-11; decision "Phase 6 analysis: MDE and degenerate-test
reading rules"). If an arm ends with k = 2 (§4), the sentence quotes the larger of the MDE at
the seed counts that ran and the k = 3 MDE above. Pre-computed k = 2 tables are in
`runs/phase6_build/mde_k2.json` and the "Fewer than 3 seeds (k = 2)" section of `mde.md`. They
are simulation outputs from the published Fair-N and b7 predictions, not run metrics. Headline
as-specified values, α 0.01 / 0.05, AUC points:

| Scenario (other arms at 3) | T1 | T2 | T4 / T5 |
|---|---|---|---|
| every arm at 3 (reference, table above) | 1.78 / 1.43 | 1.37 / 1.10 | 1.46 / 1.18 |
| E1 at 2 | 1.92 / 1.54 | 1.48 / 1.19 | 1.46 / 1.18 |
| one of E2a, E3a, E3b at 2 | 1.78 / 1.43 | 1.37 / 1.10 | 1.51 / 1.23 |
| all five new arms at 2 | 1.92 / 1.54 | 1.48 / 1.19 | 1.61 / 1.32 |

T3 at k = 2 is tabulated by gap in `mde.md` (k = 2 section). For the anchor at 2, simulation
noise can put a k = 2 cell 0.01 below its k = 3 value; the larger of the two is quoted. These
tables cover the listed scenarios only: for the seed counts that actually ran, W7 recomputes with
`--k-arm` (§4) and quotes the larger value.

## 6. Secondary analyses (pre-specified, never confirmatory)

1. **Calibrated sensitivity test** (same decision, pending C1; the concrete form below is S4's
   reading of "a t-based seed component, df = 2 per arm" and is part of that pending item).
   For T1, T2, T4, T5: the same point estimate Δ̂; SE² = Σ_a w_a² s_a²/k_a, with s_a² the
   across-seed variance (ddof 1) of arm a's per-seed endpoint on the full test set (it already
   contains the model × test-set interaction); t = Δ̂/SE, two-sided p from a t distribution
   with Welch–Satterthwaite degrees of freedom from df = k_a − 1 = 2 per arm. For T3 (only when
   estimable): the same t-test on E2a − b7 at c40, because R = 1 exactly when E2a = b7 given a
   positive denominator. Holm over the five sensitivity p-values (a not-estimable T3 enters with p = 1), reported in a separate
   labelled column beside each confirmatory result. The verdict is always the primary reading;
   where the two disagree, the paper says so in the same sentence. The test is built in
   `phase6_stats.py` (S2b, commit f70dc43), output key `sensitivity_calibrated_t`, with its own
   Holm column. If every arm's across-seed variance is exactly 0 there is no t: the row reads
   **"degenerate (SE = 0; not evaluable)"**, never "no detectable difference", and enters the
   sensitivity Holm with p = 1 (2026-10-11; decision "Phase 6 analysis: MDE and degenerate-test
   reading rules").
2. **Ensemble estimand.** Every contrast also with the ensemble AUC, from the same draws.
3. **Symmetric-selection control for E2** (decision "Phase 6: symmetric-selection control for
   E2, pre-specified, run only after C1", pending C1). b7 ×3 re-selected under the c23 + c36
   rule from its HDD epoch snapshots; T3 and T5 recomputed with this b7 in place of the
   published b7. About 1–2 GPU-h plus a small restore, in W7 only if approved. Direction known
   in advance: the no-c40 arms lose c40 selection while b7 and the anchor keep it, which lowers
   measured retention (`steps/S0.md` M5).
4. **Interaction** of codec × exposure at c40, descriptive, with its interval.
5. **E2b** (c0–c32): c40 and c36 AUC against E2a and b7 with hierarchical-bootstrap
   intervals; no p-value, outside Holm.
6. **Other test sets:** per-arm AUCs on DFD c23/c40, Celeb-DF v2 (518) and FaceShifter c23/c40,
   with per-seed values; any contrast there is labelled exploratory.
7. **±1-point equivalence: POST HOC.** Whether a contrast's 90 % interval lies inside ±1 AUC
   point is reported only as a labelled post-hoc exploration, never confirmatory, never in the
   abstract or a contribution sentence.
8. **E13, descriptive (one seed).** Each ablation arm minus Fair-N s42, at c40 and AUC_comp,
   with fixed-seed 95 % intervals (the same engine with one seed per arm: source-cluster
   resample only, B = 10,000). Effect sizes only; no p-value, no test, no "helps/harms"
   verdict. The curriculum arm's confound is stated with it (c36/c40 only in epochs 26–30;
   decision "Phase 6: E13 curriculum arm keeps the literal phase bounds", pending C1).
   Code (the S4b commit): `phase6_stats.py --e13`, one joint bootstrap over Fair-N s42 and the
   five ablations (fixed arm order, `RNG_SEED` 0, B = 10,000, source-cluster resample shared by
   all arms and both endpoints). Its output is labelled descriptive and has no p-value, no Holm,
   no reading and no verdict key. Estimates are AUC differences on the 0–1 scale (×100 = the
   points quoted in §9). An ablation run that does not exist is listed as `available: false`
   with no estimate; Fair-N s42 is required. Command (after C1 only; same `--post-c1` and tag
   guard as §4):
   `python -m src.evaluation.phase6_stats --post-c1 --e13 --manifest runs/phase6_build/stats/manifest_e13.json --out runs/phase6_build/stats/e13_descriptive.json`,
   where the manifest maps `FairN_s42` → `runs/f1_none_fair_s42/report.json` and `abl_curriculum`,
   `abl_lrbb`, `abl_lrfreq`, `abl_aux`, `abl_ep50` → `runs/r1_abl_<change>_s42/report.json`
   (format: `steps/S4b.builder1.md` §2).

## 7. Health gates (reported, never used to drop a run)

- **E1:** est_pm1 (the compression-level estimator's within-±1-level accuracy), disc_bal_acc
  (the discriminator's balanced accuracy) and λ, logged every 50 steps and per epoch
  (`train.step_log_detail: true`). Reference value, from the Phase 5.3 health gate
  (`docs/phases/phase5.3.md`): est_pm1 ≥ 0.7. Context only (published): under the original
  recipe the adversary drove est_pm1 from 87.6 % to about 0.4 (docs/24 §6 item 4).
- If est_pm1 falls below 0.7 in a seed, that is reported with the result. If it does so in
  every E1 seed, the paper reports it (decision "Revision 1 W0: adversary tested as designed,
  ramp from step 0", Revisit if) and nothing is re-tuned.
- **All CAFRL arms:** raw and EMA validation AUC per epoch (`train.val_raw: true`).
- **SpatialBase arms:** the logged level and (level, QF) counters.
- No health signal removes a run from any analysis. A run stopped under §8 is evaluated from its
  last `best.pt` and stays in every analysis, flagged (§4, "Stopped runs stay in the analysis").

## 8. Anomaly and stop rules for W7

Checked by the W7 session from `runs/phase6_build/launch_logs/<run>.train.log` (the EPOCH lines
carry train loss and validation AUCs) and the launcher state. **Epoch time:** SpatialBase arms
print it at the end of each EPOCH line (`src/scripts/train_baseline.py:592-595`, `| %.1fs`); the
CAFRL EPOCH line (E1, E13) has no duration (`src/training/trainer.py:492-497`), so for those arms
epoch time = the difference of the `asctime` timestamps of consecutive EPOCH lines (epoch 1: from
the first line of the log). Validation numbers
may be read; test numbers may not, until all runs are done.

| Anomaly (definition) | Action |
|---|---|
| **NaN or inf** in any logged loss or validation value | Stop that worker (SIGTERM; the launcher writes `.failed stage=signal-TERM`). Report. Evaluate its last `best.pt` by hand; the run stays in every analysis, flagged (§4, pending C1). |
| **Divergence:** the logged validation AUC at c23 below 0.60 at the end of any epoch ≥ 5 (EMA value for CAFRL arms), or the logged classification loss (`train_cls` for CAFRL arms, `train_loss` for SpatialBase) above 2× its epoch-1 value at the end of any epoch ≥ 5 | Stop that worker. Report. Evaluate its last `best.pt` by hand; the run stays in every analysis, flagged (§4, pending C1). For E1 the report also says this is evidence about the adversary's stability. |
| **Missing prediction file:** the launcher's `.failed stage=eval-check` | The launcher has already stopped that worker. Report; follow the launcher's recovery notes (evaluation is re-run by hand if training finished, or if the run was stopped under the two rows above, from its last `best.pt`). |
| **Over budget:** a run's mean epoch time over its first 3 epochs above 1.3 × its projected epoch (E1 1,352.7 s; E2a 677.7; E2b 653.9; E3a 709.7; E3b 664.3; anchor 569.1; E13 lr_backbone 1,202.6, lr_freq 1,221.6, aux 1,207.6, epochs-50 1,214.9; curriculum 926.6 for epochs 1–10 and 1,211.7 from epoch 11, checked again at epoch 13) | Report at once with a new calendar. The running job is **not** killed (a slow run is not a defect; pending C1, alternative "stop the worker", see §13). Trimming arms is the user's decision. |
| **Campaign over budget:** projected total above 158.4 GPU-h (the kickoff's 132 + 20 %) | Science decision for the user (kickoff "Budget overrun > 20 %"); report, do not trim. |
| Any `.failed` for another stage (train crash, signal) | That worker has stopped. Report. |

The thresholds are 1.3 × the projected epochs in `smoke/budget.md` (curriculum: 712.8 s phase A,
932.1 s mean of the other four E13 arms; `steps/S3.md` §6); 158.4 = 1.2 × 132 (kickoff).

**Note 2026-10-11 — a metric an arm does not compute.** Decision "Phase 6: a metric an arm
does not compute is not a NaN anomaly": `disc_bal_acc` (and any adversary-only readout) is
ignored in arms without an adversary (E2, E3, the anchor and the five E13 arms). Every other NaN
or inf in a logged loss or validation value is still an anomaly under the first row of the table.
These arms log `disc_bal_acc` as NaN by design; it is NaN on every line of all five E13 smoke
logs. Read literally, "any NaN" would stop every E13 run at epoch 1.
*As built*, the monitor's exemption is narrower than the decision's wording:
- It covers only the key `disc_bal_acc`, and only on CAFRL arms other than E1 (the five E13
  arms). It covers no other adversary-only readout, such as `disc_chance`.
- An inf in `disc_bal_acc`, or any non-finite `disc_bal_acc` in E1, stays an ANOMALY.
- The SpatialBase arms (E2, E3, anchor) get no exemption, because their trainer logs no
  adversary readout at all. Their EPOCH and STEP lines carry no `disc_*` key, and no smoke log
  of those arms has any non-finite key.

On every smoke log the two readings give the same result. They could differ only if a future
log showed a NaN in another adversary-only readout, and then the code flags more than the
decision requires (the conservative direction). The code is not changed; this note records the
difference (`src/scripts/phase6_monitor.py`, `STRUCTURAL_NAN_KEYS`, `ADVERSARY_ARMS`,
`parse_log`).

**The W7 monitor** (built in S2b, commit f70dc43) applies this section's rules. It reads only
`*.train.log` / `train.log` files and the launcher's `.failed` / `.done` markers. It never
reads a report, a prediction file or test data, prints no AUC, and kills nothing; W7 acts on
its output. Command (cwd `experiments/exp3-cafrl`, `conda activate cv`, CPU only):

```bash
python -m src.scripts.phase6_monitor runs/phase6_build/launch_logs/*.train.log \
    [--json <file>] [--state-dir runs/phase6_build/launch_state] [--summary runs/phase6_build/smoke/summary.json]
```

States and exit codes. With several logs the overall code is the most severe over all runs:

| State | Exit code | Meaning |
|---|---|---|
| OK | 0 | nothing triggered |
| NO-DATA | 5 | no EPOCH line parsed yet; expected only during epoch 1, an error after it |
| OVER-BUDGET | 10 | report only, with a new calendar |
| DIVERGED | 20 | a divergence rule |
| ANOMALY | 30 | NaN/inf |
| FAILED | 40 | launcher `.failed` marker |
| ERROR | 2 | unreadable or malformed log, unknown arm, or a threshold that differs from this section |

The precedence is FAILED > ANOMALY > DIVERGED > OVER-BUDGET > NO-DATA > OK. The monitor
re-derives the thresholds from `smoke/summary.json` and refuses (ERROR 2) if they differ from
the numbers in the table above. **Read each run's line, not only the overall exit code.** With
several logs, one run's OVER-BUDGET (10) hides another run's NO-DATA (5) in the overall code.

**Re-runs:** no re-run with a changed seed or config without a recorded decision. A run that
failed for an infrastructure reason (no NaN, no divergence: e.g. I/O, a killed process) may be
re-run once with the identical config after its partial output is moved aside, logged in the
journal. A NaN or divergent run is never silently replaced: it stays in the record (§10) and in the
analysis through its last `best.pt` (§4). An infrastructure failure whose identical re-run also
fails is treated the same way (the re-run's last `best.pt`, flagged; failed only if none exists).

## 9. Outcome-to-wording table

Placeholders: {Δ} = estimate in AUC points, [{lo}, {hi}] = 95 % primary interval, {p} =
Holm-adjusted p, {p_t} = Holm-adjusted sensitivity p. "Single-model AUC" = the primary estimand.
Every sentence ends with the sensitivity clause "(calibrated sensitivity test: p = {p_t})".
If any run in a test was stopped (§4), the sentence adds "({n} of the {k} seeds of {arm} were
stopped at epoch {N} ({reason}) and evaluated from their last saved checkpoint)". No
sentence may go beyond `paper/revision-1/plan.md` §4 and `docs/24` §6: no "falsified", no
"equivalent" in a central claim, no "codec diversity", no "88 %", no strict "redundant", no
general statement about frequency, no adversarial-invariance verdict beyond E1.

| Test | Helps | Harms | No detectable difference | Not estimable |
|---|---|---|---|---|
| **T1** E1 vs Fair-N, c40 | "Under the fair recipe, adding the adversarial compression-invariance loss (λmax 0.5, ramped from the first step) raised the mean single-model video AUC at c40 by {Δ} pt ([{lo}, {hi}], Holm p = {p}; 3 seeds per arm). In this architecture and recipe the adversary contributes; our earlier finding that it added nothing held only under the original recipe." | "Under the fair recipe, adding the adversarial loss lowered the mean single-model video AUC at c40 by {\|Δ\|} pt ([{lo}, {hi}], Holm p = {p}). In this architecture and recipe the adversary costs c40 accuracy." | "Under the fair recipe, adding the adversarial loss produced no detectable difference in mean single-model video AUC at c40 (Δ = {Δ} pt, [{lo}, {hi}], Holm p = {p}). With 3 seeds per arm this test detects about 1.78 pt with 80 % power at α = 0.01 (1.43 pt at α = 0.05); smaller effects in either direction are not excluded." | generic (below) |
| **T2** E1 vs Fair-N, AUC_comp | as T1 with "the mean AUC over c28–c40 (AUC_comp)" | as T1 with AUC_comp | as T1 with AUC_comp and "about 1.37 pt … (1.10 pt at α = 0.05)" | generic (below) |
| **T3** retention vs R = 1 | (R > 1) "Trained without c40, SpatialBase kept R = {R} ([{lo}, {hi}]) of the c40 gain that multi-level training gives over c23-only training, more than the full gain (Holm p = {p})." | (R < 1) "Trained without c40, SpatialBase kept R = {R} ([{lo}, {hi}]) of the c40 gain that multi-level training gives over c23-only training; R is below 1 (Holm p = {p}). Part of the c40 robustness depends on c40-level data in training, so the robustness claim holds within the training levels and only partly beyond them." If the interval also includes 0, add: "We cannot exclude that none of the gain is kept." | "Trained without c40, SpatialBase kept R = {R} ([{lo}, {hi}]) of the c40 gain; R is not detectably below 1 (Holm p = {p}). At the observed gap of {G} pt this test detects a loss of about {MDE_R} of the gain with 80 % power at α = 0.01 (`mde.md`); a smaller loss is not excluded." | "SpatialBase trained on all six levels and the c23-only anchor did not differ detectably at c40 (b7 − anchor [{lo}, {hi}] pt), so retention is not estimable; the three arms' c40 AUCs are reported descriptively. The c40 gain of multi-level H.264 training over c23-only training is therefore not established on this test set." |
| **T4** codec, c40 | "At matched mean crop PSNR, training on real H.264 levels gave a higher mean single-model c40 AUC than training on JPEG versions of the same c0 frames, by {Δ} pt averaged over c40 exposure ([{lo}, {hi}], Holm p = {p}). In this design (EfficientNet-B0, FF++, JPEG matched on mean PSNR), the codec of the training data matters, not only its image quality." | "At matched mean crop PSNR, JPEG training data gave a higher mean single-model c40 AUC than real H.264 data, by {\|Δ\|} pt ([{lo}, {hi}], Holm p = {p}). The H.264 advantage reported in the submitted version, from an unmatched single-seed JPEG arm, does not hold in the matched design." | "At matched mean crop PSNR, real H.264 and JPEG training data gave no detectable difference in mean single-model c40 AUC (Δ = {Δ} pt, [{lo}, {hi}], Holm p = {p}). This test detects about 1.46 pt with 80 % power at α = 0.01 (1.18 pt at α = 0.05). We therefore do not attribute the c40 robustness to the H.264 codec specifically; smaller codec effects are not excluded." | generic (below) |
| **T5** c40 exposure, c40 | "Including the c40-level data in training (H.264 c40 or its matched JPEG quality) raised the mean single-model c40 AUC by {Δ} pt averaged over codec ([{lo}, {hi}], Holm p = {p}). Robustness at c40 depends in part on exposure to that quality level in training." | "Including the c40-level data in training lowered the mean single-model c40 AUC by {\|Δ\|} pt averaged over codec ([{lo}, {hi}], Holm p = {p})." | "Leaving the c40-level data out of training produced no detectable difference in mean single-model c40 AUC averaged over codec (Δ = {Δ} pt, [{lo}, {hi}], Holm p = {p}). This test detects about 1.46 pt with 80 % power at α = 0.01 (1.18 pt at α = 0.05); smaller effects are not excluded." | generic (below) |

**Not estimable, any test** (§4: an arm with fewer than 2 seeds; for T3 also the denominator
rule, which has its own sentence above): "Test {T} could not be estimated because arm {A} has
fewer than 2 completed seeds ({reason}); its arms' AUCs are reported descriptively and no
conclusion is drawn on {question}." The sentence stays under the ceiling: no reading of the
contrast, in either direction.

**Reading rules for the sentences above** (2026-10-11; decision "Phase 6 analysis: MDE and
degenerate-test reading rules"):
- The MDE values printed in the "no detectable difference" column are the k = 3 values.
- If any arm of the test ended with k ≠ 3 seeds, W7 first recomputes the MDE with
  `phase6_mde.py --k-arm` (§4). The sentence then quotes the larger of that value and the k = 3
  value, and "3 seeds per arm" becomes the seed counts that ran.
- For T3 the same rule applies at the grid gap chosen in §5.
- If the sensitivity test of a row is degenerate, the clause reads "(calibrated sensitivity test:
  degenerate, SE = 0; not evaluable)". It never reads "no detectable difference", and its p is
  1 in the sensitivity Holm column.

Fixed sentences for the rest: interaction — "The codec effect with and without c40 exposure
differed by {Δ} pt ([{lo}, {hi}]; descriptive, not tested)." E13 — "In a one-seed ablation,
reverting {change} changed c40 AUC by {Δ} pt against Fair-N (fixed-seed interval [{lo}, {hi}];
descriptive)." E1 health — "With the adversary, est_pm1 at the selected epoch was {x} (Fair-N:
{y})." If the symmetric-selection control runs: "With b7 re-selected on c23 + c36, R was {R}
([{lo}, {hi}])", reported beside T3 and T5, never replacing them.

## 10. Reported whatever happens

All 23 runs, including any failed or stopped run with its stage, reason and logs. Every cell:
7 FF++ levels, DFD c23/c40, Celeb-DF, FaceShifter c23/c40, per seed and per arm, both
estimands. All five tests with estimate, interval, raw and Holm p, reading, as-specified MDE,
and the sensitivity column. The denominator of T3 with its interval. E2b, the interaction, E13
and the health logs (est_pm1, disc_bal_acc, λ, raw versus EMA validation). Measured GPU-h
against the budget. Deviations from this document, dated.

## 11. Out of scope

- The inference-only additions E7–E12 (DFDC subset, WildDeepfake, H.265/AV1 test sets, ladder
  statistics, symmetric selection for CAFRL, cost table, diagnostics, Celeb-DF re-crop). They
  evaluate these runs too, but their analysis is not registered here.
- More seeds; DCT-only, FFT-only and pixel-domain controls; a parameter-matched baseline;
  diffusion-generated video (answered by text, plan §2).
- The A1 rule (`PREREGISTRATION-A1.md`, tag `phase5-prereg-a1`) and every frozen artifact:
  existing `runs/*/report.json` and `best.pt`, `configs/phase5/`, `paper/reviews/`,
  `paper/revision-1/reviews/`, release `v1.0.0`, the Zenodo deposit.
- Any claim about frequency features in general.

## 12. Evidence tiers

| Tier | Meaning | Where existing analyses sit (proposed; W2 fixes the paper's labels) |
|---|---|---|
| **Registered** | rule fixed and tagged before the data existed | A1 bake-off (`PREREGISTRATION-A1.md`, tag `phase5-prereg-a1`); this document's §4 family and §6 items 1–6, 8 once tagged `phase6-prereg` |
| **Post-audit pre-specified** | rule written before the run, but after the self-audit had seen earlier results; not tagged | Phases 5.1–5.3 decision rules (`docs/phases/phase5.{1,2,3}.md`, "fix before running") and the Phase 5.6 confirmation seeds (`docs/26`) |
| **Post hoc** | chosen after seeing results | the ±1-point equivalence readings; re-analyses of stored predictions in W3 (e.g. Fair-N vs TrunkCtrl per video, resampling-unit sensitivity); the submitted unmatched JPEG comparison |

## 13. Decisions ratified at C1

Each row is written above as its registered default and flips by a one-line change.

*2026-10-11 (W7-P):* first written as "Open decisions for C1". The user ratified every row at C1
on 2026-10-11 (decision "C1: the W0 pre-registration and all its recommendations are
approved"); the last column records the outcome. Only the JPEG-target choice flips (the
official-PSNR row follows from it).

| Decision (date · title) | Registered default | Alternative | Effect on the analysis | Ratified at C1 (2026-10-11) |
|---|---|---|---|---|
| 2026-10-10 · Phase 6 analysis: the primary estimand is the mean single-model AUC | mean over seeds of per-seed AUC; ensemble secondary | ensemble AUC primary | changes the point estimate and intervals of all five tests | registered default kept |
| 2026-10-10 · Phase 6 analysis: endpoints of the E2/E3 tests | T3–T5 at c40; T4/T5 = 2×2 main effects; T3 vs R = 1; not estimable if denominator CI includes 0 | AUC_comp endpoints, simple effects, or R vs 0 | changes what T3–T5 measure | registered default kept |
| 2026-10-10 · Phase 6: E13 curriculum arm keeps the literal phase bounds | (10, 25) inside 30 epochs | scaled (6, 15) | one E13 config; descriptive only | registered default kept |
| 2026-10-10 · Phase 6: official c23/c40 PSNR measured aligned, calibration stays on our re-encodes | targets from x23/x40 | official targets | see next row | **alternative: official targets** (follows from the JPEG row below) |
| 2026-10-10 · Phase 6: JPEG targets for c23/c40 — the 0.5 dB trigger fired (recommendation: switch to official targets) | QF c23 54, c40 11 (file sha256 `f14c3b9c…8fbc2`) | **recommended:** official targets, QF c23 60, c40 10 (built: `jpeg_calibration.official-targets.json`, sha256 `a7286bbd…2ec19`; copied over `jpeg_calibration.json` before the tag, `docs/phases/phase6.md` Run plan step 0b) | changes E3a (c23, c40) and E3b (c23) training data; T4/T5 | **alternative chosen: official targets** (QF c23 60, c40 10; file copied, sha256 `a7286bbd…2ec19`) |
| 2026-10-10 · Phase 6: symmetric-selection control for E2, pre-specified, run only after C1 | run in W7 (≈ 1–2 GPU-h) as a secondary | do not run; disclose the direction only | adds a secondary T3/T5 comparator | registered default kept: run in W7 |
| 2026-10-10 · Phase 6 analysis: bootstrap p-value form, not-estimable retention, MDE as specified, seed-variance floor | balanced p form; not estimable → p = 1 in Holm over 5; MDE as specified; σ² floored at d | 2·(min + 1)/(B + 1); Holm over 4; design MDE headline; raw σ² | p-values, family size, quoted MDEs | registered default kept |
| 2026-10-10 · Phase 6 analysis: the conservative bootstrap is kept, with a calibrated sensitivity test | keep the bootstrap; add the t-based sensitivity test in the §6.1 form | recalibrate the primary test | primary α (0.003–0.019 at nominal 0.05 now) | registered default kept |
| 2026-10-10 · Phase 6 build: the failed x23/x40 alignment rule stays failed; alignment rests on shift evidence | FAILED, accepted on shift evidence | a formal replacement rule (e.g. residual shift < 0.1 px at x23) | none on the tests; x23/x40 feed only the calibration and E9 | registered default kept |
| 2026-10-10 · Phase 6 build: smoke letter-FAILs that cannot discriminate stay failed (JPEG single-crop PSNR; curriculum-arm step time) | FAILED, recorded; curriculum calendar at 7.31 GPU-h | mean-based replacement rules | none on the tests | registered default kept |
| 2026-10-10 · Phase 6 build: compensated singles quota for asymmetric level sets (listed for visibility) | heavy group 30 % for c0–c36 | old rule (25.6 %), disclosed | E2a/E3b training mix | registered default kept |
| 2026-10-10 · Phase 6 analysis: stopped runs stay in the analysis; fewer than 3 seeds (§4, §7, §8) | (a) a run stopped for NaN/divergence/other anomaly is evaluated from its last `best.pt` and enters T1–T5 and all secondaries, flagged "stopped at epoch N (reason)"; failed only without a `best.pt`. (b) after a failed run, test with k = 2; < 2 seeds → not estimable, p = 1 | (a) drop the stopped run, test on k = 2; (b) wait for a replacement seed | (a) the alternative removes the seeds most likely to stop, E1's, and biases T1/T2 away from *harms* (toward the narrative); (b) family behaviour after a failed run | registered default kept |
| 2026-10-10 · Phase 6: W7 anomaly rules (divergence defined; over-budget runs reported, not killed) (§8) | divergence = c23 val AUC < 0.60 or classification loss > 2× epoch 1, at any epoch ≥ 5; an over-budget run is reported at once with a new calendar and keeps running | over budget: stop the worker (the S4 brief's wording) | over-budget rule: calendar only, no effect on any test | registered default kept |
| 2026-10-11 · Phase 6: a metric an arm does not compute is not a NaN anomaly (listed for visibility; §8 note) | `disc_bal_acc` NaN in arms without an adversary is not an anomaly (as built: E13 arms only, key `disc_bal_acc` only; see the §8 note) | the literal rule: any NaN stops the run | under the literal rule every E13 run stops at epoch 1; no effect on any test | registered default kept |
| 2026-10-11 · Phase 6 analysis: MDE and degenerate-test reading rules (§4, §5, §6.1, §9) | quote the larger MDE of the seed counts that ran (recomputed with `--k-arm` when k ≠ 3); SE = 0 → "degenerate (SE = 0; not evaluable)", p = 1 in its Holm column | quote the k = 3 MDE whatever ran | wording of "no detectable difference" sentences and the sensitivity column only | registered default kept |

## 14. Number traps

- **b7's test-split seed σ at c40 is ≈ 0.645 pt** (`mde.json` → `sigma_b7_c40_pt` =
  0.6453), never 0.63. `docs/24` printed the older 0.63 until 2026-10-11, when it was corrected to ≈ 0.645.
- MDEs here are the as-specified values; the design MDEs are smaller and are never quoted
  alone.
- The anchor runs 5,760 steps per epoch, b7 6,583 (`steps/S0.md` §3.1).

## 15. Known gaps (state 2026-10-11)

First written 2026-10-10 (stage S4) as five gaps. Refreshed by stage S4b.

**Closed:**
- **The §6.1 sensitivity test.** Built in `phase6_stats.py` with tests (S2b, commit f70dc43;
  output key `sensitivity_calibrated_t`; `src/tests/test_phase6_stats_s2b.py`).
- **The < 2-seed rule (§4).** Built in `phase6_stats.py` with tests (S2b, commit f70dc43; output
  key `seed_count_rule`). A test with an arm below 2 seeds is never evaluated: it reads not
  estimable with p = 1 in both Holm columns.
- **The MDE at unequal k (§4, §5).** Built in `phase6_mde.py` (`--k-seeds`, `--k-arm ARM=K`,
  `--k2-section`) with tests (S2b, commit f70dc43; `src/tests/test_phase6_mde_s2b.py`). The k = 2
  tables are in `mde_k2.json` and `mde.md`.
- **The §6.8 E13 descriptive intervals** (not listed at writing; found by the S2b verifier).
  Built as `phase6_stats.py --e13` with tests (the S4b commit; `src/tests/test_phase6_e13.py`).
  The primary confirmatory output stays byte-identical on the S2b fixture.
- **A monitor for the §8 rules.** Built as `src/scripts/phase6_monitor.py` with tests (S2b, commit
  f70dc43; `src/tests/test_phase6_monitor.py`).
- **The JPEG-target switch.** *Closed 2026-10-11 (W7-P):* C1 chose the official targets;
  `jpeg_calibration.official-targets.json` was copied over `jpeg_calibration.json` (Run plan step
  0b), sha256 `a7286bbd8457adb9716a3f2c2397c18c02a8e0326bcb8795604b9dc60b82ec19`; §1, §13 and
  Gate A carry it. The history as first written:
  - If C1 switches the JPEG targets, the alternative file already
  exists (`jpeg_calibration.official-targets.json`, sha256 `a7286bbd…2ec19`). It is copied over
  `jpeg_calibration.json` and committed before the tag (`docs/phases/phase6.md`, Run plan step
  0b). §1, §13 and Gate A then carry its hash.
  - After the copy, `src/tests/test_phase6_jpeg_official_targets.py::test_real_alternative_file`
    fails by construction: it asserts the registered QFs (c23 54, c40 11) and the source file's
    old sha256 (`derived_from.sha256`). This was checked on 2026-10-11 by running the test against
    a scratch copy, with the real files untouched; the other tests in that file pass. W7 updates
    that test with a dated note in the same commit. *Done 2026-10-11 (W7-P):* the test now pins
    the copied file's hash and QFs and still fails against the old file.
  - The JPEG-arm test in `test_phase6_configs.py` (path, status "final", QF map per arm) and the
    launcher's checks (path, status, sha256 recorded by the first worker) accept the copied file
    unchanged.
  - The copied file's `note` field still calls itself "C1 alternative"; that is cosmetic, and
    the hash in §1 identifies it.

**Still open:**
- **By-hand evaluation of a stopped run.** The launcher has no mode for evaluating a stopped
  run's `best.pt` (§4), so the W7 session runs and logs it by hand. It uses the existing
  evaluation commands (`eval_battery` + `eval_faceshifter`, `--baseline` for SpatialBase arms,
  on a free GPU), then `phase6_check_report.py`.
- **The anomaly exemption.** The monitor's exemption is narrower than the wording of decision
  "Phase 6: a metric an arm does not compute is not a NaN anomaly" (§8 note). It is
  conservative and equal in effect on every smoke log, so the code is not changed. The user may
  confirm either reading at C1 (§13). *2026-10-11 (W7-P):* C1 kept the registered default (§13).
