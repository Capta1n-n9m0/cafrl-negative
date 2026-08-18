# The frozen A0-beats-baselines STOP-gate (verbatim)

The STOP-gate that halted the campaign is quoted verbatim below from the
Phase-5 execution plan, which was committed **before any Phase-5 run
existed** (see `history-excerpts.md` for the commit timeline). It answers
the question of what the gate said, given that its comparator (the
capacity-matched b7 control) was constructed mid-campaign: the frozen rule
binds a *comparison type* — "the strongest baseline", adjudicated by a
paired-Δ bootstrap CI — not a named checkpoint.

**Reading the excerpt.** It is internal planning prose, quoted without
edits, so it uses the run names of the internal record and refers to files
that are not part of this release. `A0` is the reference CAFRL run exactly
as specified — released here as `a0`. `B1`–`B6` are the baseline
reproductions (`b1`…`b6`), and `b7` is the capacity- and
augmentation-matched EfficientNet-B0 spatial control added later under the
gate's own confound-control provision. Every run named here is in
`configs/RUNS.md` with its launch command and its role in the paper.

---

*Quoted verbatim from `docs/phases/phase5.md`.*

## Step 5.4 — B-series runs + the A0-beats-baselines STOP-GATE

Run **B1–B6** (the 6 baseline runs). Tabulate video-level + frame-level (separate tables).

**The STOP-and-analyze gate (a Gate-5 item, `plan §8`):** **A0 must beat the B-series at c40 video-AUC BEFORE burning ablation compute.** **Binding decision rule (mirrors the A1 win-rule, CRUX-3 — do NOT re-open the paired-vs-marginal ambiguity):** the contrast is the **paired video-resampling bootstrap** `paired_auc_delta(A0, best_baseline)` at c40 video-AUC, B=10k shared indices; **A0 passes iff the 95% CI of Δ = AUC(A0) − AUC(best_baseline) excludes 0 on the positive side** (paired p<0.05). Marginal per-arm non-overlapping CIs are a **descriptive presentation fallback only**, never the binding rule. A0 = grl/estimated/cmam is the full model; if it cannot beat plain Xception/F3-Net/FreqNet at the compression level the whole thesis is about, **stop and analyze** — do not launch the A-series sweeps. This is the cheapest possible sanity check on the entire premise.

**Verify:**
- The Step 5.1 anchor checks passed (Xception/F3-Net within ~2 pts).
- The A0-vs-best-baseline c40 video-AUC contrast is computed with `paired_auc_delta` and recorded; **A0 passes iff the paired-Δ 95% CI excludes 0 (positive side)** (the binding rule above); **if A0 does not pass, HALT** and write the analysis (candidate causes: harness bug, A0 mis-selection, the gain genuinely being "just the data" — which B4–B6 would then reveal).

---

## The Gate-5 checklist the STOP-gate belongs to (same frozen document)

*Quoted verbatim from `docs/phases/phase5.md`.*

## Gate 5 checklist (the parent plan's two items + the intermediate stop-gates)

- [ ] **Xception/F3-Net reproductions within ~2 pts of the §6 frame-level anchors** (Xception 0.9637/0.8261, F3-Net 0.9635/0.8271); FreqNet = first harmonized entry, no anchor (sanity-bounded only). *(Step 5.1)*
- [ ] **A0 beats the B-series at c40 video-AUC — binding rule: the paired-Δ bootstrap CI `paired_auc_delta(A0, best_baseline)` excludes 0 on the positive side (marginal-CI is descriptive fallback only) — a STOP-and-analyze gate fired BEFORE the ablation sweep** (`plan §8`); if it fails, HALT and analyze. *(Step 5.4)*
- [ ] **Win-rule machinery frozen / committed (pre-registered) and validated on A0** (self-paired Δ(A0,A0)≈0 with symmetric CI) **before A1 adjudication.** *(Step 5.2)*
- [ ] **A1 win-rule decision emitted (WIN or NULL)** per the panel-hardened rule, **with the paired Δ + seed band tabulated regardless of outcome** (the SYMMETRIC integrity clause — the rule can declare GRL the loser). *(Step 5.5)*
- [ ] **Every reported §6 cell has a bootstrap CI; frame-level and video-level NEVER mixed in one table; primary selector = `mean(val AUC@c23,c40)` honored** (`phase4-asbuilt §G3`). *(Step 5.9)*
- [ ] **Standard eval protocol preserved** — train FF++ c23 all methods; intra FF++ c23/c40 + DFD c23/c40; cross CelebDF-v2/DFDC/WildDeepfake; video-level AUC primary. *(Steps 5.3, 5.9)*

---

*Assembled verbatim by the release build from the working repository's frozen documents; see `history-excerpts.md` for the commit dates that place each rule before the runs it governed.*

