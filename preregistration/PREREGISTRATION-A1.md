# PRE-REGISTRATION — A1 GRL-vs-HSIC-vs-both(-vs-contrastive) bake-off win-rule

**Status:** FROZEN. Committed + git-tagged **before any A1 run completes** (the A1 runs are endpoint-agnostic — each just saves 50 EMA checkpoints; this rule is computed POST-HOC on the saved `best.pt`, so freezing it first is genuinely non-circular). This document is the verbatim, binding rule. The machinery that implements it is `src/evaluation/metrics.py` (`paired_auc_delta`, `paired_auc_comp_delta`, `auc_comp`, `seed_band`), `src/scripts/eval_battery.py`, and `src/evaluation/aggregate_runs.py`. **Any re-interpretation of a pinned threshold AFTER A1 data is observed PARKS and surfaces to the human — it cannot be autonomously "improved".**

**Source:** `docs/phases/phase5.md` Step 5.2 (CRUX-3), authored + adversarially validated 2026-06-24. This file transcribes that rule verbatim and PINS the two thresholds the prose left to the implementer (criteria 3 and 4), so the frozen machinery is unambiguous.

---

## Arms & seeds
- Arms: **{none, grl, hsic, both}** (+ **contrastive** as the 5th arm IFF its loss builds+validates — code-gated A1e; if it slips, report it descriptively and the 4-arm rule stands unchanged). The best-vs-runner-up logic extends to 5 arms unchanged.
- **3 seeds per arm: {42, 1, 2}.** **A0 = grl seed-42** (reused — verified sound in Step 5.0: A0's config == the canonical grl config field-for-field; the post-A0 val-loss support is training-path-inert). Report ALL raw per-seed AUCs.
- **One selector, fixed for ALL arms:** the **EMA best-by-val-AUC checkpoint `best.pt`**, selected on the official FF++ **val** split (never test). `best_valloss.pt` is a tracked sidecar that **must NOT vary the selection across arms** (`phase4-asbuilt §G3`).

## Endpoints
- **PRIMARY:** `AUC_comp` = per-arm **3-seed-mean** of the **video-level mean-pool AUC over {c28, c32, c36, c40}** of the FF++ official test split.
- **Co-primary invariance contrast:** the clean-anchored drop **Δ = AUC@c23 − AUC_comp** (smaller = more invariant).
- **Secondaries:** worst-case **AUC@c40**; **crf_slope** over {0,18,23,28,32,36,40}.
- A **frame-level** column is reported separately for literature comparability. **Frame-level and video-level are NEVER mixed in one table** (a tabulator presentation constraint).

## Decisive test (PRIMARY) — paired video-resampling bootstrap
For the **best vs runner-up** arm (ranked by 3-seed-mean `AUC_comp`): draw a **SHARED video-index vector per replicate** (identical across both arms ⇒ pairing); score each arm's **seed-pooled** per-video predictions on it; record `Δ_r = AUC_comp(best) − AUC_comp(runner-up)`; **B = 10,000** replicates; the decision statistic is the **95% percentile CI of {Δ_r}**.
- Seed-pooling: per arm, per level, average the per-video pooled scores across the 3 seeds (aligned BY VIDEO KEY), then resample.
- **Marginal per-arm CI overlap is DEMOTED to a descriptive sidecar** — it is statistically wrong for paired data (≈ p<0.006-strict) and manufactures FALSE NULLs. It is NEVER the inter-arm test.

## Seed variance (source B) — the honest across-seed band
Treat the **seed as the experimental unit**. Per arm: `seed-mean ± t_{.975,2}·s/√3` where `s` = across-seed sample std (ddof=1) and **t_{.975, 2 dof} = 4.30** ⇒ half-width `= 4.30·s/√3 ≈ 2.48·s` for 3 seeds. (4.30 is the t-multiplier, THEN divided by √3 — not already absorbing /√3.) The single-run video-resampling bootstrap CI (source A: test-set noise) is reported per-seed as context but is NOT the inter-arm test.

## WIN requires ALL of (criteria 1–4)
1. **(1)** the arm has the **strictly highest 3-seed-mean `AUC_comp`** (gap > 0).
2. **(2)** the **paired-Δ bootstrap CI vs the runner-up excludes 0 on the positive side** (`ci_lo > 0`; equivalently paired p<0.05).
3. **(3)** the seed-mean gap **> the across-seed band `4.30·s/√3`**. **PINNED:** the band = `max(half_width_best, half_width_runnerup)` (the larger single-arm half-width — conservative, symmetric, errs against a false win).
4. **(4)** **no c23 regression beyond the ~0.5-pt noise band AND the winner is at least as invariant.** **PINNED:** `best.c23_mean ≥ runnerup.c23_mean − 0.005` **AND** `best.drop_mean ≤ runnerup.drop_mean` (can't win compressed by sacrificing clean accuracy, and can't win by being a uniformly-better detector that is LESS invariant).

Else → **NULL.**

## Multiplicity
- Confirmatory = **exactly one** paired test (best vs runner-up) → **no family-wise correction**.
- All other pairwise Δ's (all-pairs among the arms) are **exploratory → Holm-corrected and labeled as such**.

## Pre-registered escalation (CRUX-1 tripwire)
If **any** arm's per-seed `AUC_comp` std (ddof=1) **> 0.005 (0.5 pt)**, that arm is **escalated to 5 seeds BEFORE adjudicating** (the aggregator FLAGS this; do not adjudicate on 3 high-variance seeds).

## Consistency check (descriptive, pre-registered)
The winning mechanism must **not reverse the sign of its drop advantage on DFD-c40 + FaceShifter-unseen** (both reachable now; DFD-c40 cell wired in Step 5.3).

## Effect-size framing
Report the winning Δ against the literature's **~+0.58 AUC-points adversarial prior** (`gap-synthesis finding 2`) — a "win" is contextualized, not categorical.

## NULL outcome (likely, acceptable — do NOT p-hack)
If no arm satisfies (1)–(4): the registered conclusion is **"no compression-invariance mechanism dominates within seed+test noise"**; the paper's headline rests on **compression-LEVEL conditioning + curriculum**, and none/grl/hsic/both is reported as an honest ablation.

## INTEGRITY (verbatim)
The rule is **SYMMETRIC — it MUST be able to declare GRL (A0) the LOSER.** There is **NO parsimony tiebreak that favours GRL.** The aggregator emits the paired Δ + the seed band + the full per-arm table as standard rows **regardless of WIN/NULL** — the table looks identical whether GRL wins or loses. (Verified: `paired_auc_delta` is antisymmetric, Δ(a,b) = −Δ(b,a); the aggregator ranking is order-invariant; a tie returns NULL not a GRL win.)

## Validation performed before freezing (Step 5.2 verify clauses)
- **Self-paired correctness (free, hard assertion):** `paired_auc_delta(A0, A0) ≡ 0` per replicate ⇒ CI = [0,0]. Verified on synthetic data (`test_paired_delta.py`) and to be re-confirmed on A0's REAL per-video preds via `eval_battery.py --run a0`.
- **Antisymmetry / symmetry:** `Δ(a,b) = −Δ(b,a)` exactly (same seed). Verified.
- **Aggregator skeleton:** seed-mean + `4.30·s/√3` band + 4-criterion decision emitted on a 1-arm dummy (→ INSUFFICIENT_ARMS), a clear-WIN 2-arm case (all criteria True), a NULL tie (gap < band ⇒ NULL), and order-invariance. Verified.
- **seed_band:** half-width = `4.30·s/√3 ≈ 2.48·s` (hand-checked).

## What is OUT OF SCOPE of this rule (never altered)
The standard eval protocol (train FF++ c23 all methods; intra FF++ c23/c40 + DFD c23/c40; cross CelebDF-v2/DFDC/WildDeepfake; **video-level AUC primary**) is never altered. The A1 decision is **NOT gated on cross-dataset data** — its primary endpoint is intra-FF++ `AUC_comp`, ready now. Cross-dataset is the per-arm comprehensive layer + the consistency check.

---

*Frozen by the Phase-5 build, session 1 (2026-06-24). Git tag: `phase5-prereg-a1` (the tagged commit pins this file + the machinery at freeze time).*
