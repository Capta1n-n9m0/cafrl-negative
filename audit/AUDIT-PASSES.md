# The self-audit: what the four passes were, and what they checked

The manuscript reports that the campaign's own conclusion was audited in
four independent review passes. This file is the primary record of those
passes, quoted verbatim from the audit document written on the day they
ran (2026-07-02): the four pass scopes, the enumerated verifications that
survived them, and the audit's own provenance note on how its claims were
checked.

**What "independent" means here, precisely.** The four passes ran in
parallel, each confined to a different false-negative surface, each
starting from the artifacts rather than from the campaign's conclusions,
and none of them able to see the others' findings while it worked. They
were executed by the author, with tool assistance (four parallel
language-model agents, each given one of the scopes below and the
repository to work from), and their file-and-line-cited reports were then
merged by the author into the audit document quoted here. They were not
performed by people outside the author team, and no external reviewer saw
the campaign before submission. `README.md` in this directory states what
follows from that and what does not.

**A note on vocabulary.** These internal documents say "the human" where
this release says "the author", and "delegated"/"the agent" for work that
was executed with tool assistance under the author's direction. Nothing is
rewritten to hide that; `README.md` in this directory and
`../preregistration/README.md` explain the usage.

**What is not here.** The individual agent reports were working notes and
were not retained as separate artifacts; the audit document is the merged
record. The record also does not attribute individual defects to
individual passes, so this release does not invent that mapping. What it
*does* carry is every check's outcome and every defect's evidence, and —
in `predictions/`, `curves/` and `evaluation/` — the material to re-run
the checks that produced the numbers.

---

## The four passes, as scoped before they ran

*Quoted verbatim from `docs/23-false-negative-audit.md`.*

## Method

Four independent audit agents ran in parallel on 2026-07-02, each attacking a different false-negative surface:

1. **Training-recipe parity** — `train_baseline.py` vs the CAFRL trainer stack, configs of every compared run.
2. **Frequency-path implementation** — all of `src/models/` + `src/losses/` against the phase-2/3 as-built contracts, plus direct checkpoint forensics (γ trajectory loaded from all 50 `cafrl_spatres_s42` epoch checkpoints).
3. **Eval symmetry & numbers** — the §6 harness end-to-end, **including GPU re-runs of the decisive eval cells from the stored `best.pt` checkpoints** and a from-scratch reproduction of the §3.5 FaceShifter seed-confirmation.
4. **Journals & diagnostics** — `runs/phase5_build/{journal,CAMPAIGN}.md`, pre-registration compliance, and the TensorBoard scalars of every compared run.

---

## What the passes checked and confirmed (the checklist, with outcomes)

*Quoted verbatim from `docs/23-false-negative-audit.md`.*

## 1. What the audit CONFIRMS (the negative's solid core)

- **Numbers are faithful.** A0 c40 re-ran from `runs/a0/best.pt` to 0.922436 and b7 to 0.959005 with per-video score Δ = 0.0 vs the stored predictions; every quoted video-AUC and both AUC_comp values recompute exactly from `report.json` `video_scores`/`video_labels`. The §3.5 FaceShifter table reproduces to 4 decimals from fresh GPU inference on the six checkpoints.
- **Eval is symmetric.** Both model families are scored by the same `Evaluator` on identical video sets (identical `video_keys` sets *and order*, n=700 = 140 real + 560 fake), identical crop files (same parquet index, same 32 linspace frames), identical pooling (`(video_id, method)` mean-pool), identical AUC/bootstrap code. `data:` config sections of `runs/a0` vs `runs/b7_*` diff to zero.
- **No leakage.** Both trainers select `best.pt` by mean **val**-AUC (c23+c40) on the official FF++ val split; train/val/test ID-pair sets verified programmatically disjoint; fake membership tested by unordered pair (closes the `t_s`/`s_t` loophole).
- **Statistics are right.** `paired_auc_delta` resamples videos with shared indices (self-paired ≡ [0,0] verified live). Recomputed STOP-gate contrast: **Δ(backbone−A0) @c40 = +0.0366, 95% CI [+0.021, +0.054], P(Δ>0)=1.000**.
- **The baseline is not a lucky draw.** b7's three seeds end at val c40 0.9582/0.9585/0.9592 (spread <0.2 pt); Xception-mq-flip-only independently lands 0.963 — two architectures replicate "plain spatial + mq data ≈ 0.96".
- **The process was honest.** The STOP-gate was pre-registered before any baseline data (with the "or non-overlapping CIs" escape hatch explicitly closed); both mid-campaign confounds (augmentation, capacity) were self-surfaced and resolved *in CAFRL's favor*; configs between compared runs differ by exactly the one intended line (`a0`↔`a1_none_s42`: `invariance_arm`; `a0`↔`cafrl_spatres_s42`: `fusion.kind`); no run crashed and was silently re-run.
- **P2 stands:** real-CRF training (0.963) ≫ synthetic JPEG-aug (0.890) at real c40.
- **"The GRL adds nothing" stands** as an *internal, recipe-matched* comparison (grl 0.922 vs none 0.919).

---

## The audit's own provenance note

*Quoted verbatim from `docs/23-false-negative-audit.md`; 1 line naming an internal tooling file removed, nothing else altered.*

## Notes

- Audit provenance: the four agents produced file:line-cited reports; the highest-stakes claims were verified by artifact (checkpoint loads for γ and BN stats; GPU re-runs for every headline eval cell; TB scalar reads for D1/D6/D7). File:line citations are current as of 2026-07-02.
- `docs/21` and `docs/22` are deliberately left unedited until the 5.1–5.4 results land; Phase 5.5 owns the corrections/addenda so they can be written once, with the final numbers.

---

*Assembled verbatim by the release build from the working repository's frozen documents; see `preregistration/history-excerpts.md` for the commit dates that place each rule before the runs it governed.*

