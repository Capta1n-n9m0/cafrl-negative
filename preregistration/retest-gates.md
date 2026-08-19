# Pre-registered decision rules of the audit re-tests (Phases 5.1–5.6)

After the campaign concluded, a self-audit found eight defects (D1–D8), four
of which were biased *against* the hypothesis under test. Five re-tests were
then planned. Each re-test's decision rule was written down **before its run
executed**; all five plans were committed in a single commit on 2026-07-02
at 08:03 UTC, before the earliest re-test run artifact (2026-07-02 12:52
UTC). The rules are quoted verbatim below, in plan order, followed by the
two gates that were journaled rather than planned (the FaceShifter re-check
and the Phase-5.6 confirmation seeds).

**Reading the excerpts.** These are internal planning documents, quoted
without edits. They name runs by their internal identifiers — `a0` (CAFRL
as specified), `b7` (the capacity- and augmentation-matched spatial
control), `T`/`trunk_recipe_*` (CAFRL's spatial trunk under the fair
recipe), `F1`/`f1_none_fair_*` and `F2`/`f2_spatres_full_*` (the two fair
frequency re-tests) — all of which appear in `configs/RUNS.md` with their
launch commands. They also cross-reference source files and internal
analysis documents that are not part of this release; those references are
left intact rather than rewritten, because the point of the excerpt is what
the rule said at the time it was frozen, not a tidied restatement of it.
Every *number* these rules adjudicate is recomputable from `predictions/`.

---

## Phase 5.1 — SplitBN eval-routing probe (defect D5) — question

*Quoted verbatim from `docs/phases/phase5.1.md`.*

## Question

At eval, `SplitBatchNorm2d` sends **compressed** inputs through the **clean** BN branch (`src/models/norms.py:131-133` — "Inference: always the clean set, mask ignored"), while training routed them through the compressed branch. Measured branch divergence on `runs/a0/best.pt`: up to ~0.5σ per channel on the last DCT-path alignment BN. **How much of CAFRL's compressed-cell deficit is this train/eval mismatch?**

---

## Phase 5.1 — pre-registered decision rule

*Quoted verbatim from `docs/phases/phase5.1.md`.*

## Pre-registered decision rule (fix before running)

- **MATERIAL** if oracle-routed eval improves c40 video-AUC by **≥ +0.005** on `a0` or `a1_none_s42`. Then: (a) routed eval becomes the reported protocol for Phases 5.3/5.4 (both routings still logged); (b) D5's contribution to the 3.7 pt gap is quantified in the final synthesis.
- **IMMATERIAL** if all deltas < +0.005 → D5 is retired as a false-negative mechanism; status-quo eval stays; one line in the synthesis.
- **Negative controls (must hold):** flag-off eval is **bit-identical** to the stored `report.json` scores (max |Δscore| = 0); c0/c23 cells move by < 0.001 under routing (clean cells route to the clean branch either way).

---

## Phase 5.2 — trunk-recipe control (defects D3+D4) — question

*Quoted verbatim from `docs/phases/phase5.2.md`.*

## Question

The 4.5 pt gap between the pure-spatial spatres arm (0.914 @c40) and the plain backbone b7 (0.959) was attributed to an "architecturally bottlenecked spatial path" (`docs/22` §3.3). But spatres also carried the *entire CAFRL recipe*: backbone LR 1e-5 (20× below b7), 10-epoch freeze, curriculum-deferred heavy data, the aux-loss stack, and the GRL. **Train CAFRL's exact spatial trunk with the baseline's exact recipe** and read off how the 4.5 pt splits into architecture vs recipe.

---

## Phase 5.2 — pre-registered decision rule

*Quoted verbatim from `docs/phases/phase5.2.md`.*

## Pre-registered decision rule (fix before running)

Let `T` = trunk-recipe test c40 video-AUC (seed 42). Comparators: b7 = 0.959, spatres = 0.914 (`docs/22` §3.3). Adjudicate with `paired_auc_delta` (10k video bootstrap) on the identical 700-video test set, not point estimates:

- **RECIPE-DOMINANT** if Δ(b7 − T) @c40 CI includes 0 or T ≥ 0.949 → ≥ ~80% of the trunk gap was recipe → `docs/22`'s "bottlenecked spatial path" architecture claim is retracted; D3 confirmed as a major contributor to the headline gap.
- **ARCHITECTURE-DOMINANT** if T ≤ 0.924 (within 1 pt of spatres) → the 320-tap/256-proj genuinely cripples the trunk; D4's architecture reading confirmed; the fair frequency test (5.4) becomes *more* important (frequency was paired with a genuinely weak trunk).
- **MIXED** otherwise → report the split: recipe share = (T − 0.914), architecture share = (0.959 − T), both with paired CIs.
- Also report Δ(T − spatres) explicitly = the recipe+aux bundle effect at fixed architecture. (Caveat to record: spatres's recipe bundle includes the aux losses and GRL, so "recipe" here means the whole non-architecture bundle — that is exactly the quantity `docs/22` failed to isolate.)

---

## Phase 5.3 — the fair frequency test, arm F1 (defects D1+D3) — question

*Quoted verbatim from `docs/phases/phase5.3.md`.*

## Question

No Phase-5 arm ever trained frequency features free of compression-invariance pressure: the curriculum **hardcodes** `w_cons`/`w_phase` (`src/training/curriculum.py:117-126` — the YAML `loss:` values are overridden per phase), and the consistency term ran at 40–120× the classification loss (D1). Every arm also carried the 20×-slower backbone and curriculum-deferred heavy data (D3). **Run the first CAFRL where the frequency path is trained only by the task, at the baseline's optimization recipe.** This is the experiment `docs/22`'s conclusion 1 *assumed* had been run.

---

## Phase 5.3 — pre-registered decision rule

*Quoted verbatim from `docs/phases/phase5.3.md`.*

## Pre-registered decision rule (fix before running)

Primary contrast: `paired_auc_delta(F1, b7)` @c40 + AUC_comp{c28..c40}, 10k video bootstrap, identical 700-video test set.

- **REVIVAL** if Δ(F1 − b7) @c40 CI excludes 0 in F1's favor → frequency + level-conditioning helps when not sabotaged → escalate: 3 seeds mandatory (5.5) before any claim; the A-series program is potentially back on the table.
- **NEUTRAL** if the CI includes 0 → the negative *narrows*: "frequency adds nothing, but the 'actively hurts by ~4 pt' magnitude was a recipe artifact." `docs/22` conclusions 1/3 get rewritten accordingly.
- **CONFIRMED-NEGATIVE** if F1 still loses with CI excluding 0 → the falsification is now genuinely established at matched recipe with zero invariance pressure — the referee-proof version. Publish with confidence.

Secondary readouts (report, no gate): Δ(F1 − a1_none 0.919) = the recipe+loss-calibration effect on the full model; Δ(F1 − trunk-recipe from 5.2) = frequency's marginal value at the *bottlenecked* trunk, matched recipe (the clean within-architecture frequency readout).

Health gates (must hold for the run to count): `diag/est_pm1_acc` ≥ 0.7 throughout (no GRL ⇒ estimator must stay healthy; if it collapses anyway, D6's GRL attribution is revisited); no loss-spike divergence; val AUC plateaus by ~ep 25 (if still rising at 30, extend to 40 — pre-authorized once, recorded).

---

## Phase 5.4 — full-trunk frequency residual, arm F2 (defects D2+D4) — question

*Quoted verbatim from `docs/phases/phase5.4.md`.*

## Question

Every CAFRL-with-frequency variant carried the bottlenecked 320→256 trunk (D4: the trunk handicap −4.5 pt exceeds the whole −3.7 pt deficit), and the one "does the model want frequency?" probe was structurally deadlocked (D2: at γ=0 the frequency path receives zero label gradient, so γ→0 is self-sealing). **Give frequency its only remaining honest shot: a full-strength spatial path (b7's own representation) + a frequency residual that always receives label gradient.** If frequency loses *here*, the negative is total and final.

---

## Phase 5.4 — pre-registered decision rule

*Quoted verbatim from `docs/phases/phase5.4.md`.*

## Pre-registered decision rule (fix before running)

Primary contrast: `paired_auc_delta(F2, b7)` @c40 + AUC_comp, 10k video bootstrap.

- **FREQUENCY-REAL** if Δ(F2 − b7) @c40 CI excludes 0 in F2's favor → frequency contributes beyond a full-strength spatial model → 3 seeds mandatory (5.5) before claiming; the paper becomes "frequency helps, but only on a non-crippled trunk and without invariance losses" — a *constructive* result.
- **NEUTRAL** if the CI includes 0 → frequency is redundant given a strong spatial path on diverse data. Combined with a CONFIRMED-NEGATIVE or NEUTRAL F1 (5.3), this closes the question: the negative is final, now genuinely established.
- **HARMFUL** if F2 < b7 with CI excluding 0 → the strongest form of the negative (frequency hurts even with label supervision, full trunk, no invariance pressure). Publish confidently.

Mechanistic readouts (report, no gate): the per-epoch **γ trajectory** and the **standalone val-AUC of `freq_logit`** — pre-registered interpretations: freq-AUC ≈ 0.5 all run ⇒ the frequency features carry no task signal (physics verdict); freq-AUC high but γ→0 ⇒ frequency is informative but redundant with spatial (redundancy verdict). These two curves are the paper's mechanism figure regardless of outcome.

---

## Phase 5.5 — pre-registered seed policy

*Quoted verbatim from `docs/phases/phase5.5.md`.*

## 1. Seed policy (pre-registered now)

- **Any reversal** (5.3 REVIVAL or 5.4 FREQUENCY-REAL): **3 seeds mandatory** for that arm before any claim leaves the journal; adjudicate seed-pooled with `aggregate_runs.py` (the FaceShifter §3.5 machinery).
- **Any headline contrast** with |Δ| point estimate ≥ 1 pt @c40 but CI including 0: +2 seeds for the ambiguous arm.
- Everything else: single seed stands (b7's observed seed σ < 0.2 pt and CAFRL's ≈ 0.35 pt justify this; record the justification in the synthesis).
- `metrics.seed_band`: fix the hardcoded t=4.30/√k for k≠3 (D8) before any new seed-band is quoted.

---

## Phase 5.5 — pre-registered optional-probe triggers

*Quoted verbatim from `docs/phases/phase5.5.md`.*

## 2. Optional probes (run only if their trigger fires)

| probe | trigger | design |
|---|---|---|
| **FaceShifter re-check** | 5.3 or 5.4 produced a non-losing CAFRL variant | the unseen-manipulation axis was the one suggestive OOD signal (+2.6 pt c40 lean, P=0.84); re-run it with the fair variant (3 seeds exist for b7; per-video preds must be SAVED this time — D8) |
| **γ re-init resume** | 5.4 was NOT built/run | resume `cafrl_spatres_s42` from an epoch ≥ 26 checkpoint with γ re-initialized and `w_freq_aux=0.2`; ~2 GPU-h; a cheap direct test of the D2 deadlock |
| **Routing table** | 5.1 verdict = MATERIAL | oracle-vs-estimated routing deltas as a small paper table (deployability of the fix) |

---

## Phase 5.5 — the FaceShifter re-check gate (journaled before the eval ran)

*Quoted verbatim from `runs/phase5_build/journal.md`.*

### §2a FaceShifter re-check — design + PRE-STATED GATE (written BEFORE the eval runs)

**Why:** the unseen-manipulation axis was the campaign's one suggestive OOD signal (§3.5 seed-confirmation: shipped-recipe CAFRL 3-seed pooled Δ(+c40) = +0.022, CI [−0.021,+0.064], P=0.84 — a lean, NOT confirmed). 5.3/5.4 produced the first *non-losing* CAFRL variants; the re-check asks whether the FAIR-recipe frequency variants show anything different on the axis where frequency invariance was most plausibly useful.

**Design (same harness as §3.5):** evaluate `runs/f1_none_fair_s42/best.pt` and `runs/f2_spatres_full_s42/best.pt` (EMA, the frozen mean-val-AUC selector's checkpoints — no re-selection) on the FaceShifter c23 and c40 cells: FF++ test split, n=280 videos (140 real + 140 FaceShifter fakes — FaceShifter was held out of ALL training), 32 linspace frames, per-video mean-pool, video-AUC. **Per-video predictions SAVED to disk this time (D8)** — for F1/F2 AND for the re-run b7 comparator inferences (b7 s42/s1/s2 FaceShifter preds were never saved; they are re-generated from the frozen `best.pt` checkpoints, which the audit already showed reproduce §3.5 to 4 decimals). Contrasts, each a 10k paired video bootstrap on the identical 280-video set:
1. Δ(F1 − b7-3-seed-pool) and Δ(F2 − b7-3-seed-pool) @ c23 and c40 — pool = per-video mean score across b7 s42/s1/s2 (the §3.5 method);
2. Δ(F1 − b7_s42) and Δ(F2 − b7_s42) — the single-seed-vs-single-seed symmetric reading.

**PRE-STATED GATE (frozen now, before any FaceShifter number for F1/F2 exists):** an unseen-manipulation generalization **claim** is made ONLY if the paired-Δ 95% CI **excludes 0** (in the appropriate direction) on the pooled contrast. Otherwise the result is a **reported lean, not a claim** — exactly the §3.5 discipline. **Asymmetry noted explicitly and in advance:** F1/F2 are single-seed; the b7 pool is a 3-seed per-video-mean ensemble, which is variance-reduced and therefore mildly flattered (the same asymmetry documented for Δ(F1 − trunk-pool) in §PHASE 5.3); contrast (2) is the apples-to-apples reading. Neither reading elevates a lean into a claim without its CI excluding 0. If F1/F2 vs the pool and vs s42 disagree in sign, both are reported and neither is claimed. No seed escalation follows from this probe under any outcome (the plan's seed policy §1 governs and did not fire); at most, a CI-excluding-0 result would be flagged to the human as a candidate for optional confirmation seeds.

**Execution:** delegated (eval-only, minutes of GPU); GPU state unknown at delegation → the agent checks `nvidia-smi` first and uses a free GPU. Frozen artifacts untouched; new prediction files are CREATED (never overwriting any `report.json`).

---

## Phase 5.6 — confirmation seeds: purpose and standing

*Quoted verbatim from `runs/phase5_build/journal.md`.*

### §1 Purpose & standing (frozen before any run)

These four runs — `f1_none_fair_{s1,s2}` and `f2_spatres_full_{s1,s2}` — are **human-directed OPTIONAL confirmation seeds**, **NOT rule-mandated**. The pre-registered escalation rules that *would* have mandated seeds did **not** fire in 5.3/5.4 (5.3 was NEUTRAL not REVIVAL; 5.4 was NEUTRAL not FREQUENCY-REAL; §PHASE 5.5 §1 recorded "single seed stands"). The human has elected to run them anyway as **descriptive tightening for the paper's tables** — to convert the single-seed F1/F2 points into per-arm 3-seed means ± seed band and to make every F-vs-b7 contrast a symmetric **3v3** (removing the 1-seed-vs-3-seed-ensemble asymmetry caveat noted in `docs/24` §5, and pinning F2's within-2σ +0.56 pt lean).

**HARD standing rule (from §9): the pre-registered 5.3/5.4 NEUTRAL verdicts and the Branch-A claim set STAND regardless of the seed outcomes. Nothing in this session re-opens adjudication autonomously.** The seeds tighten error bars; they do not adjudicate.

---

## Phase 5.6 — confirmation seeds: quoting rule

*Quoted verbatim from `runs/phase5_build/journal.md`.*

### §2 Quoting rule (frozen before any number exists — this is what the paper will report)

- **Per-arm 3-seed means ± seed band.** For F1 (seeds 42/1/2) and F2 (seeds 42/1/2): the seed-mean c40 video-AUC and AUC_comp, with the **seed band = `metrics.seed_band` at k=3 = 4.30·s/√3** (the frozen t-quantile constant; §PHASE 5.5 §3 landed the k≠3 fix but k=3 stays bit-identical at 4.30). Reported alongside b7's own 3-seed band ({0.9590, 0.9614, 0.9492}, from the §5.5 backfill).
- **Pooled 3v3 contrasts** vs the **b7 3-seed pool** (`b7_effnet_b0_mq_fliponly{,_s1,_s2}`): per-video **mean-pooled** scores across each arm's 3 seeds (aligned by video key, `aggregate_runs.seed_pool_level`), then **`paired_auc_delta` @c40** + **`paired_auc_comp_delta` over {c28,c32,c36,c40}**, **10k paired video bootstrap** (seed=0), on the **identical 700-video FF++ test set** (140 real + 560 fake, `(video_id, method)` mean-pool). Two contrasts: Δ(F1-pool − b7-pool) and Δ(F2-pool − b7-pool).
- Secondary (report, no gate): per-arm seed-std AUC_comp (the `aggregate_runs` escalation tripwire statistic), and — descriptive-only, NON-claim-bearing — FaceShifter c23/c40 seed bands for the OOD appendix (the FaceShifter axis is CLOSED, `docs/24` §5).

---

## Phase 5.6 — confirmation seeds: anomaly rule

*Quoted verbatim from `runs/phase5_build/journal.md`.*

### §3 ANOMALY RULE (frozen before any number exists — the STOP condition)

**If EITHER of the following occurs, STOP and surface to the human BEFORE touching any doc/claim:**
1. **Any pooled contrast CI excludes 0** (either direction) — i.e. Δ(F1-pool − b7-pool) or Δ(F2-pool − b7-pool) @c40 or on AUC_comp has a 95% CI that does not include 0.
2. **The `aggregate_runs` seed-std tripwire fires** — any arm's per-seed AUC_comp std (ddof=1) > 0.005 (0.5 pt).

Otherwise (both pooled contrasts CI-incl-0 AND both arms' seed-std ≤ 0.5 pt): the seeds **confirm** the pre-registered NEUTRAL; write the seed-pooled numbers next to this rule (below), append a seed-pooled addendum to `docs/24` §3, and close out. **No verdict text is rewritten under any outcome** — a CI-excluding-0 surprise is escalated to the human, not self-adjudicated.

---

*Assembled verbatim by the release build from the working repository's frozen documents; see `preregistration/history-excerpts.md` for the commit dates that place each rule before the runs it governed.*

