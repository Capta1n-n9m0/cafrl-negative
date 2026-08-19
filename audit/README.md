# `audit/` — the self-audit that tried to kill this paper's own result

The campaign reached a negative result and stopped. Four days later it was
audited — not for whether the numbers were right, but for whether the *negative
was a mistake*: whether the thing being tested had been given a fair chance to
succeed. It had not, in four specific ways. This directory is the record of that
audit, released because the paper's third contribution is the apparatus, and an
apparatus you cannot inspect is a claim, not an apparatus.

| file | what it is |
|---|---|
| `AUDIT-PASSES.md` | The four review passes as they were scoped before they ran, the checks they performed with their outcomes, and the audit's own note on how its claims were verified. All verbatim. |
| `LEDGER-D1-D8.md` | The complete ledger, in two halves: the eight defects exactly as first written on 2026-07-02 — before any re-test ran, when the conclusion could still have reversed — and the closure status of each after the pre-registered re-tests executed. |

The four passes, in one table (their scopes are quoted verbatim in
`AUDIT-PASSES.md`, which is the authoritative version):

| # | pass | surface it attacked |
|---|---|---|
| 1 | **Training-recipe parity** | the baseline training driver against the CAFRL trainer stack, and the configuration of every compared run |
| 2 | **Frequency-path implementation** | the frequency modules and loss terms against their as-built contracts, plus checkpoint forensics (the fusion gate's per-epoch trajectory read out of all 50 epoch checkpoints of the shipped spatial-residual run) |
| 3 | **Evaluation symmetry and numbers** | the evaluation harness end to end, including GPU re-runs of the decisive cells from the stored checkpoints and a from-scratch reproduction of the held-out-manipulation seed check |
| 4 | **Journals and diagnostics** | the campaign journal and campaign ledger, pre-registration compliance, and the training-diagnostic scalars of every compared run |

The decision rules those re-tests were adjudicated under are in
`../preregistration/retest-gates.md`, quoted from plan documents committed
before the runs they governed. Every number either half of the ledger turns on
is recomputable from `../predictions/` — see `../CLAIMS-MAP.md`.

## What "four independent review passes" means, precisely

The manuscript describes the self-audit as four independent review passes. That
phrase does real work in the paper, so here is its exact content.

**What is true.** The four passes ran in parallel on 2026-07-02. Each was
confined to a different failure surface (the table in `AUDIT-PASSES.md`), each
started from the artifacts — configs, checkpoints, training scalars, evaluation
code — rather than from the campaign's conclusions, and none could see the
others' findings while it worked. Each was required to cite file and line, or an
artifact, for every claim; the highest-stakes findings were then verified by
re-execution (checkpoints re-loaded, decisive evaluation cells re-run on GPU,
training scalars re-read). 8 defects were found, 4 of
them biased *against* the hypothesis the campaign had just rejected.

**What is not true.** The passes were not performed by people outside the author
team, and they were not blind to the paper's existence. They were run by the
author with tool assistance — four parallel language-model agents, each given
one scope and the repository — and their reports were merged by the author into
the audit document quoted here. No external reviewer saw the campaign before
submission. "Independent" therefore means *independent of each other, and of the
conclusion under audit* — separate scopes, separate evidence, no shared
findings — not *independent of the authors*.

**What is not here.** The individual agent reports were working notes and were
not retained as separate artifacts; the merged audit document is the record. The
record also does not attribute each defect to the pass that found it, and this
release does not invent that mapping. Nor were there separate checklist
documents: each pass's checklist is its scope statement plus the enumerated
verifications reproduced in `AUDIT-PASSES.md`, which is what it was given and
what it reported against.

**Why say all of this.** The audit's value does not rest on who performed it. It
rests on what it produced being checkable: eight named defects with their
evidence, four re-tests with rules frozen before they ran, and a released set of
predictions from which every adjudicated number can be recomputed by a stranger.
That is the part worth trusting, and it is the part in this repository.
