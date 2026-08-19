# `preregistration/` — the decision rules, frozen before the runs they governed

| file | what it is |
|---|---|
| `PREREGISTRATION-A1.md` | The frozen win-rule for the planned ablation campaign — the primary endpoint, the comparison, the decision thresholds — committed and git-tagged before any of the data it adjudicates existed. Verbatim. |
| `STOP-GATE.md` | The gate that stopped the campaign, quoted from the execution plan that was committed before any of those runs existed. |
| `retest-gates.md` | The decision rule of every audit re-test (Phases 5.1–5.6), each quoted from the plan or journal entry that was written before its run executed. |
| `tag-phase5-prereg-a1.txt` | The tagged commit's own content: hash, dates, author, message, diffstat. |
| `history-excerpts.md` | The commit and artifact timeline that places each rule before the runs it governed — and an explicit statement of what that evidence is and is not. |

**Rule texts are never edited here.** They are quoted whole, including the parts
that are awkward in hindsight, because a tidied rule is not evidence. The one
exception is mechanical and announced in place: two tooling trailer lines are
removed from the quoted commit message in `tag-phase5-prereg-a1.txt`, and that
file says so where it happens. Hashes, dates, authorship, subject, body and
diffstat are untouched.

## Reading internal planning vocabulary

These are working documents, written for the people executing the campaign, and
they use that register. Two habits are worth translating:

- **"the human"** means the author. The campaign was run by one researcher with
  tool assistance, and the plans use "the human" for the decisions reserved to
  the author — anything that would re-interpret a frozen threshold, escalate a
  gate, or change a claim.
- **"delegated", "the agent", "surfaces to the human", "not self-adjudicated"**
  describe how execution was orchestrated: routine work (launching runs,
  checking GPU state, collecting scalars, drafting analyses) was delegated to
  language-model agents under author direction, while every adjudication against
  a frozen rule stayed with the author. Several rules say this explicitly, in
  advance — the sentence in `PREREGISTRATION-A1.md` stating that a pinned
  threshold cannot be "improved" after data is observed, and must instead park
  and surface, is one of them.

`../audit/README.md` states the same thing in the paper's own terms, for the
self-audit specifically: what was author-directed, what was tool-assisted, and
what "independent" does and does not mean.

## What this evidence is worth

The repository was private during the campaign, so these are author-controlled
version-control records, not a third-party registry. `history-excerpts.md` says
so in those words. What does not depend on trusting the timeline: every number
these rules adjudicate is recomputable from `../predictions/` — run
`python ../verify/verify.py`, or `../CLAIMS-MAP.md` for one claim at a time.
