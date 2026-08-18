# Freeze-before-results: the commit and artifact timeline

The manuscript states that the STOP-gate and the win-rule were frozen before any
result existed, and that each audit re-test's decision rule was written down before
its run executed. This file is the evidence, in the only form the authors can
provide honestly.

**What this is.** Commit hashes and author dates from the version-controlled
research repository for each rule document, paired with the filesystem timestamps
of the run artifacts those rules governed.

**What this is not.** It is not third-party registration. The repository was
private during the campaign, so these timestamps are author-controlled records,
not a registry's. A reader who wants an external guarantee should read the claim
as: the rules and their history are published here in full, and every number they
adjudicate can be recomputed from the released predictions. The rules were frozen
in our version-controlled records before the runs; we are not asking anyone to take
that on faith about the numbers, only about the ordering.


## Rule documents — when each was committed

| document | what it fixes | first committed (author date, UTC) | commit |
|---|---|---|---|
| `phase5.md` | The Phase-5 execution plan containing the STOP-gate. | 2026-06-24T11:11:49+00:00 | `95d79da744` |
| `PREREGISTRATION-A1.md` | The frozen A1 win-rule (the tagged commit). | 2026-06-24T14:50:44+00:00 | `65a8ebb200` |
| `phase5.1.md` | Re-test plan 5.1 (SplitBN eval-routing probe). | 2026-07-02T08:03:28+00:00 | `7f37cec013` |
| `phase5.2.md` | Re-test plan 5.2 (trunk-recipe control). | 2026-07-02T08:03:28+00:00 | `7f37cec013` |
| `phase5.3.md` | Re-test plan 5.3 (fair frequency test, F1). | 2026-07-02T08:03:28+00:00 | `7f37cec013` |
| `phase5.4.md` | Re-test plan 5.4 (full-trunk frequency residual, F2). | 2026-07-02T08:03:28+00:00 | `7f37cec013` |
| `phase5.5.md` | Re-test plan 5.5 (consolidation: seeds, probes, corrections). | 2026-07-02T08:03:28+00:00 | `7f37cec013` |
| `journal.md` | The campaign journal (every gate and result, capture-as-it-happens). | 2026-06-24T14:50:44+00:00 | `65a8ebb200` |

## Run artifacts — when the runs they governed produced their weights

Checkpoint (`best.pt`) and evaluation-report timestamps, from the frozen run directories. Every rule above predates every run below that it governs.

| run | checkpoint written | evaluation report written |
|---|---|---|
| `a0` | 2026-06-16 08:00:46Z | 2026-06-24 14:18:25Z |
| `b1_xception_lit` | 2026-06-25 02:52:36Z | 2026-06-25 04:06:02Z |
| `b2_f3net_lit` | 2026-06-25 00:36:18Z | 2026-06-25 04:20:21Z |
| `b3_freqnet_lit` | 2026-06-25 07:06:09Z | 2026-06-25 07:35:16Z |
| `b4_xception_mq` | 2026-06-25 04:37:38Z | 2026-06-26 19:24:39Z |
| `b4b_xception_mq_fliponly` | 2026-06-25 13:19:52Z | 2026-06-25 17:59:57Z |
| `b5_f3net_mq` | 2026-06-25 09:09:36Z | 2026-06-25 12:56:03Z |
| `b6_freqnet_mq` | 2026-06-25 12:18:54Z | 2026-06-25 12:59:12Z |
| `b7_effnet_b0_mq_fliponly` | 2026-06-25 22:16:56Z | 2026-06-26 19:19:48Z |
| `p2a_xcep_jpeg` | 2026-06-25 15:21:10Z | 2026-06-25 20:43:16Z |
| `a1_none_s42` | 2026-06-26 05:05:40Z | 2026-06-26 07:33:34Z |
| `cafrl_spatres_s42` | 2026-06-26 11:39:40Z | 2026-06-26 14:42:43Z |
| `trunk_recipe_s42` | 2026-07-02 12:52:31Z | 2026-07-02 16:42:48Z |
| `f1_none_fair_s42` | 2026-07-03 09:40:13Z | 2026-07-03 16:13:13Z |
| `f2_spatres_full_s42` | 2026-07-03 20:53:19Z | 2026-07-04 03:25:38Z |

## The ordering that matters

* The Phase-5 plan containing the **STOP-gate** was committed on 2026-06-24, before the first baseline checkpoint (2026-06-25).
* The **A1 win-rule** was committed and tagged `phase5-prereg-a1` on 2026-06-24 at 14:50 UTC — after the reference run A0 had trained but before any comparison it adjudicates existed. The rule is computed post-hoc on saved checkpoints, which is why freezing it at that point is non-circular; the file says so itself.
* All five **audit re-test plans** were committed together on 2026-07-02 at 08:03 UTC, before the earliest re-test checkpoint (2026-07-02 12:52 UTC).
* The **FaceShifter re-check gate** and the **confirmation-seed rules** were journaled before their runs; both texts are in `retest-gates.md`.

