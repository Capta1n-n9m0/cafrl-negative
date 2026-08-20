# The complete D1–D8 audit ledger, and how each defect was closed

The manuscript's Section VI names D1-D4 in prose and points here. This
is the full text: first the defects exactly as the audit stated them on
2026-07-02 — before any re-test had run, when it was still possible that
the negative would be overturned — and then the final closure status of
each after the pre-registered re-tests (Phases 5.1–5.6) had executed.

Reading the two halves together is the point: the first half is the
strongest case that could be made *against* the campaign's own
conclusion, written by the people who had just reached it, and the second
half is what the re-tests did to that case. Four of the eight defects
(D1–D4) were biased *against* the hypothesis under test; repairing them
recovered 3.96 points for the frequency arm, and the conclusion still did
not reverse.

**Reading the excerpts.** Internal analysis documents, quoted without
edits — including their internal register, in which "the human" means the
author and "delegated"/"the agent" means work executed with tool
assistance under the author's direction (`README.md` in this directory
states exactly what that covered). They cite source files, internal
documents (`docs/21`, `docs/22`)
and run names that are not part of this release; the run names are in
`configs/RUNS.md`, and every number is recomputable from `predictions/`
via `verify/verify.py`. The decision rules the re-tests were adjudicated
under are in `preregistration/retest-gates.md`, quoted from the plans that
were committed before those runs executed.

---

## The defects as first stated (2026-07-02, before any re-test)

*Quoted verbatim from `docs/23-false-negative-audit.md`.*

## 2. The defects (ranked by how much they undermine `docs/22` §3.3)

### D1 — The consistency loss dominated classification 40–120:1, in EVERY arm (including CAFRL-none)

`src/losses/consistency.py:51` computes the clean-anchored L1 **summed over 256 channels** (the spec's literal `‖·‖₁` — the *contract itself* is the defect), weighted `w_cons=0.5`, and — unlike HSIC, which the trainer magnitude-matches to CE (`trainer.py:560-565`) — it was never calibrated. A0's own TensorBoard: `loss/cls` 0.16–0.39 throughout; `loss/cons` **35.9–37.9 raw at the Phase-B onset** (weighted ≈18–19, i.e. **50–60× the classification term at exactly the epoch compressed data arrives**), still 5–30× afterwards. Corroborating: `loss/phase_geo` collapses 0.24→0.003 at ep 11 (trivially satisfied), and `diag/disc_balanced_acc` hits exact chance from ep 12, *before* the GRL λ is meaningful (0.12) — z_freq's level information was crushed by the consistency hammer, not by the adversary.

**Consequence:** the causal-chain link *"removing the GRL doesn't recover → not the invariance"* is void. `a1_none_s42` removed only the GRL; `w_cons` stayed. **No run in the campaign ever trained frequency features free of compression-invariance pressure.**

### D2 — γ→0 was a curriculum-shock collapse plus a structural deadlock, not "the model's free choice"

Loaded from every `runs/cafrl_spatres_s42/epoch_*.pt`:

| epoch | γ | ‖freq_head.W‖ | interpretation |
|---|---|---|---|
| 1→10 | −0.066 → **−0.135** (steadily growing) | 1.66 → 2.70 | Phase A: the model was actively **using** frequency |
| 11→12 | −0.135 → −0.050 → −0.003 | 2.70 → 1.35 | **Phase-B onset: collapse within ~1.5 epochs** |
| 13→50 | ~−0.0007 flatline | decays to 0.46 | deadlocked; never recovers |

Epoch 11 is the Phase A→B boundary, where **four shocks land simultaneously**: compressed data enters; the GRL λ-ramp starts (this run kept `invariance_arm: grl`); compressed samples first hit the never-warmed compressed SplitBN branch; the backbone unfreezes. And the deadlock is structural: at γ≈0 the classification gradient into the entire frequency path is ∝γ = **zero**, and the aux losses that still reach it (adversarial, consistency, phase, diversity) carry **no label signal** — `freq_logit` can never become discriminative, so γ has no reason to regrow (γ sits in the wd=0 group, so the flatline is purely gradient-driven, not decay-pinned). The published inference "given a free choice, the model discards frequency" (`docs/22:75,77`) is contradicted by the run's own artifacts: the probe is structurally incapable of answering that question.

### D3 — The comparison was capacity-matched but never optimization-matched

| | CAFRL A0 | baseline b7 |
|---|---|---|
| backbone LR | **1e-5**, frozen epochs 1–10 | **2e-4, full fine-tune from epoch 1** (20×) |
| heavy data (c36/c40) | from epoch 26 only, after cosine LR ≤50% and falling | all six levels from epoch 1 at peak LR |
| c40 exposure | ≈0.72 M samples | ≈0.87 M samples (+20%) |
| optimizer steps | 164,600 @ global batch 64 | 197,520 @ batch 32 (+20%) |
| aux losses | up to ~2.8× the cls weight | plain BCE |

The compression-graded deficit shape (−1.3 pt c23 → −3.7 pt c40) is exactly what this asymmetry predicts, independently of frequency. The journal's *"a −4pt fusion dilution won't be recovered by LR/epoch/loss-weight retuning"* (journal.md L126) was **asserted, never tested** — no recipe-matched CAFRL run exists — even though the human's directive at that decision point was "diagnose + retune" (L115). Estimated share: 1–3 of the 3.7 c40 points are plausibly recipe, not architecture.

### D4 — The spatial-trunk handicap exceeds the entire deficit; at fixed trunk, frequency *helped*

CAFRL's spatial path taps `features_only` stage-4 (320 ch, 8×8) → 1×1-proj 256, discarding EffNet-B0's `conv_head` (320→1280) and the 1280-d pooled representation the baseline keeps (`backbone.py:83-95`). From the campaign's own table: spatial-residual-with-γ≈0 *is* the bottlenecked spatial path alone → 0.914 @c40 vs full backbone 0.959 → **the trunk handicap alone is −4.5 pt, more than full CAFRL's −3.7 pt deficit**. Holding the trunk fixed: full CAFRL 0.922 > CAFRL-none 0.919 > spatial-only 0.914 — frequency **added** +0.8 pt at c40 despite D1/D2/D5 all working against it (caveat: CAFRL seed σ ≈ 0.35 pt, so +0.8 is a ~2σ lean, not proof). The fair experiment — full 1280-d trunk + frequency fusion — **was never run**, so "no version of CAFRL-with-frequency beats the backbone" is true only because every version carried the crippled trunk. ("Matched capacity" matched parameter count, not representational width.)

### D5 — SplitBN "eval-forces-clean" is a train/eval mismatch on exactly the compressed eval cells

During training, compressed samples (bins 2–5) route through the compressed BN branch; at eval the whole batch uses the **clean** branch regardless (`norms.py:131-133`). Measured on `runs/a0/best.pt` (EMA): the last DCT-path alignment BN shows per-channel standardized mean shifts of mean 0.21σ / p95 0.47σ / max 0.96σ between branches. Affects all 6 phase-stream + 4 fusion-alignment SplitBNs — every frequency feature entering the classifier. The baseline has no counterpart. Mitigating context (why this is a thumb on the scale, not the gap): it is CAFRL's own pre-registered AR-AT recipe; model selection ran through the same eval path; and the spatres control (whose active logit path has no SplitBN) still loses by 4.5 pt. Direction is nonetheless anti-CAFRL, specifically at c28–c40, specifically on the frequency contribution being judged. Estimated magnitude: tenths of a point up to ~1 pt at c40.

### D6 — The GRL silently destroyed CAFRL's own conditioning signal (undocumented pathology in A0)

`runs/a0` TB: `diag/est_exact_acc` drops to 0.0 from epoch 15 and never recovers; `diag/est_pm1_acc` — the pre-registered P1 premise (87.6%, the basis for the "estimated conditioning" default) — collapses in Phase C to an oscillating 0.15–0.85 (mean ≈0.4). Printed on every `a0_train.log` epoch line; mentioned in no document. The control pattern proves GRL-mediation: `a1_none` keeps est_pm1 = 1.0 throughout; `a1_grl_s1/s2` degrade partially; `cafrl_spatres` (gates→0) recovers. The adversarial gradient, coupled through the FiLM gates into the jointly-trained estimator, partially destroyed the very signal the architecture conditions on — "condition-then-remove" is self-defeating as configured. Contained (the negative doesn't rest on A0 alone — the estimator-healthy `a1_none` still loses), but it must be reported, and it invalidates the "A0 was a healthy reference run" reading in part.

### D7 — "Disc at chance = invariance working" (`docs/21` §1) is a misreading

`runs/a0` TB per-bin recalls: from Phase B on, the discriminator predicts **bin 1 for everything** (recall_bin1 = 1.0, all others 0.0, epochs 29–50 without exception); balanced accuracy pinned at exactly 1/4 then 1/6 — the signature of a **constant predictor**, not a probing adversary hovering at chance. Consistent with true invariance *or* with a dead adversary (and D1 suggests z_freq was crushed by the consistency loss before λ mattered); no independent probe (fresh disc on frozen z_freq) distinguishes them. `docs/21`'s "not a degenerate disc" assertion is wrong as written.

### D8 — Minor hygiene (none affects conclusions)

- `docs/22` §7 overstates: `b7_*_s1/_s2` and `a1_grl_s1/s2` have **no** `report.json` (the FaceShifter confirmation's per-video preds weren't saved — now independently reproduced, but save them going forward).
- Baseline reports lack provenance fields (`ckpt`/`selector`); the baseline eval was an uncommitted inline sweep (proven bit-exact from `best.pt`, but commit the driver).
- `metrics.py:478-499` `seed_band` hardcodes t=4.30 (df=2) yet divides by √k for any k — wrong for k≠3; only ever used with 3.
- `aggregate_runs.py:97-98` log-format args misordered (branch never fired).
- b7 trained its full net at 2e-4 while its warmup=1 evaluates to factor 1.0 at epoch 1 (effectively no warmup) — cosmetic.

---

## The audit's own verdict on which claims survived it

*Quoted verbatim from `docs/23-false-negative-audit.md`.*

## 3. What survives vs what doesn't

**Survives:** the STOP-gate *decision* (stopping the ~270 GPU-h A1–A6 campaign on this evidence was correct process); "plain spatial + multi-CRF data ≈ 0.96 @c40" (robust, replicated); "the compression-robustness lever is data diversity" (baselines with no frequency machinery achieve the flat curve); P2; "the GRL adds nothing" (and per D6, actively harms its own conditioning signal).

**Does not survive as stated:** *"frequency is genuinely unwanted (γ→0)"* (D2); *"not the invariance machinery"* (D1); *"CAFRL's machinery actively hurts by ~4 pt at matched everything"* (D3/D4/D5 — matched capacity ≠ matched optimization ≠ matched representational width); *"CAFRL's spatial path is itself a bottlenecked backbone"* as an architecture claim (D3 — never isolated from the recipe); `docs/21`'s invariance-working narrative (D6/D7).

---

## The audit's reconciliation, in both directions

*Quoted verbatim from `docs/23-false-negative-audit.md`.*

## 4. Reconciliation — what this means

This is **not** a full reversal. Honest framing in both directions:

- *Against CAFRL:* nothing in this audit shows frequency **will** win under fair conditions — only that it was never fairly tested. Even a fully repaired CAFRL is fighting for ≲1 pt against 0.959–0.968 spatial baselines, and the fixed-trunk +0.8 pt lean is within ~2σ of seed noise.
- *Against the current write-up:* the negative-result paper as framed in `docs/22` §3.3/§6.3 ("frequency unwanted", "machinery hurts", "bottlenecked architecture", "γ→0 = free choice") would not survive a referee who runs this audit. Either the controls below get run, or the claims soften to what the data shows: *"CAFRL as specified — including its curriculum, loss calibration, and LR policy — loses to a simply-trained backbone."*

The strategic pivot to Exp1 can still be the right call — but after this audit it is a judgment call, not a forced conclusion.

---

## Final closure status after the re-tests (2026-07-04)

*Quoted verbatim from `docs/24-fair-retest-conclusion.md`.*

## 4. The D1–D8 final ledger

| defect | finding (docs/23) | re-test | closed how |
|---|---|---|---|
| **D1** consistency loss 40–120× cls in every arm | the spec's literal ‖·‖₁ over 256 ch, never magnitude-matched; curriculum hardcodes w_cons past the YAML | **5.3 (F1)**: zero invariance losses, flat curriculum | **CONFIRMED as principal cause** (+3.96 pt recovered, sig). Fix landed: `curriculum: "flat"` YAML-governed weights; aux-dominance WARN (>10× cls) in `diagnostics.py`; margin notes in phase3-asbuilt §B7 + implementation-plan §3. |
| **D2** γ→0 = shock-collapse + structural deadlock, not free choice | at γ=0 the freq path gets zero label gradient; γ can never regrow | **5.4 (F2)**: aux BCE on `freq_logit` | **CONFIRMED — deadlock broken**: γ grows to 0.145, holds 0.140 at selection; freq-head standalone AUC 0.91–0.98. "Free choice" claim retracted (docs/22 §9.2). γ logging landed in 5.4. |
| **D3** capacity-matched but never optimization-matched | 20× backbone-LR gap, 10-ep freeze, curriculum-deferred heavy data | **5.2 + 5.3** | **CONFIRMED** — recipe ≈88 % of the trunk gap; fair recipe erases the model-level deficit. |
| **D4** trunk handicap (−4.5 pt) exceeded the whole deficit | 320-tap/256-proj discards the 1280-d rep | **5.2** (recipe-dominant) + **5.4** (full trunk) | **CLOSED — real but small**: the "handicap" was ~88 % recipe; genuine trunk width is worth ~+1.0 pt at a fair recipe, and frequency on the full trunk is still NEUTRAL. The architecture claim is retracted. |
| **D5** SplitBN eval-forces-clean train/eval mismatch | branch divergence up to 0.96σ on freq-path BNs | **5.1** (routing probe) | **RETIRED — IMMATERIAL**: oracle c40 Δ = −0.0009 (a0) / −0.0040 (a1_none), both ≤ 0; the clean eval mildly *flattered* CAFRL. Status-quo eval stays; no routing table (the 5.1-MATERIAL trigger never fired). |
| **D6** GRL destroyed the estimator conditioning | est_pm1 87.6 % premise → ~0.4 in Phase C; est_exact → 0 from ep 15 | four-way control pattern (a1_none ≈1.0 · F1 min 0.89 · F2 min 0.93 · grl arms degrade) + 5.1 misrouting corroboration (659/700 vs 274/700) | **CLOSED — documented** (docs/21 §6.1 addendum); est_pm1<0.7 WARN guardrail added; design lesson: "condition-then-remove" is self-defeating as configured. |
| **D7** "disc at chance = invariance working" misread | recall_bin1 = 1.0 eps 29–50 — a constant predictor | — (documentation defect) | **CLOSED** — docs/21 §6.2 addendum: constant predictor; invariance-vs-dead-adversary indeterminate from this run. |
| **D8** artifact hygiene | missing report.json ×4; seed_band k≠3; aggregate_runs args; unsaved FaceShifter preds; uncommitted baseline driver | Phase 5.5 §3.5 + 5.2 | **CLOSED**: report.json backfilled for a1_grl_s1/s2 + b7_s1/s2 (per-video scores + provenance); `seed_band` t-quantile fixed for k≠3 (k=3 bit-identical at the frozen 4.30); `aggregate_runs` arg order fixed (+tests); baseline driver committed (5.2); FaceShifter driver committed with preds saved (5.5). |

---

*Assembled verbatim by the release build from the working repository's frozen documents; see `preregistration/history-excerpts.md` for the commit dates that place each rule before the runs it governed.*

