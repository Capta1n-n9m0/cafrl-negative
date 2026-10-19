# Freeze-before-results, revision 1: the commit and artifact timeline

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


The revision's pre-registration is frozen by the annotated tag `phase6-prereg` (tagger date 2026-10-11 12:20:18Z); `tag-phase6-prereg.txt` is its `git show`.

## Rule documents — when each was committed

| document | what it fixes | first committed (author date, UTC) | commit |
|---|---|---|---|
| `PREREGISTRATION-R1.md` | The Revision-1 pre-registration (tests T1–T5, E13, the anomaly rules). | 2026-10-10T23:15:49+00:00 | `9446ecc1d5` |
| `MANIFEST.json` | The 23 registered campaign configs, by sha256. | 2026-10-10T20:50:09+00:00 | `3c74663db3` |
| `MANIFEST.json` | The three curriculum re-run configs (not registered; written after the first curriculum run stopped). | 2026-10-16T12:51:47+00:00 | `8d61a3a928` |

## Run artifacts — first and selected checkpoints of the campaign runs

Filesystem timestamps of each run's first epoch checkpoint (`epoch_1.pt`, kept in the working repository; not released), its selected checkpoint (`best.pt`) and its evaluation report.

| run | epoch-1 checkpoint written | selected checkpoint written | evaluation report written |
|---|---|---|---|
| `r1_fairn_grl_s42` | 2026-10-11 12:41:58Z | 2026-10-11 13:30:08Z | 2026-10-11 20:33:33Z |
| `r1_fairn_grl_s1` | 2026-10-11 12:42:40Z | 2026-10-11 13:14:56Z | 2026-10-11 20:31:22Z |
| `r1_fairn_grl_s2` | 2026-10-11 20:48:07Z | 2026-10-11 22:07:28Z | 2026-10-12 04:35:14Z |
| `r1_sb_noc40_s42` | 2026-10-11 20:43:15Z | 2026-10-11 22:49:43Z | 2026-10-12 01:10:33Z |
| `r1_sb_noc40_s1` | 2026-10-12 01:19:32Z | 2026-10-12 02:31:04Z | 2026-10-12 05:45:44Z |
| `r1_sb_noc40_s2` | 2026-10-12 04:44:13Z | 2026-10-12 07:12:24Z | 2026-10-12 09:04:43Z |
| `r1_sb_noc36c40_s42` | 2026-10-12 05:54:45Z | 2026-10-12 07:41:54Z | 2026-10-12 10:22:10Z |
| `r1_sb_noc36c40_s1` | 2026-10-12 09:13:50Z | 2026-10-12 10:51:05Z | 2026-10-12 13:39:14Z |
| `r1_sb_noc36c40_s2` | 2026-10-12 10:31:39Z | 2026-10-12 10:40:33Z | 2026-10-12 14:49:20Z |
| `r1_sb_jpeg_all_s42` | 2026-10-12 13:48:57Z | 2026-10-12 16:52:13Z | 2026-10-12 18:09:33Z |
| `r1_sb_jpeg_all_s1` | 2026-10-12 14:58:51Z | 2026-10-12 16:45:32Z | 2026-10-12 19:19:15Z |
| `r1_sb_jpeg_all_s2` | 2026-10-12 18:18:53Z | 2026-10-12 21:35:30Z | 2026-10-12 22:44:20Z |
| `r1_sb_jpeg_noc40_s42` | 2026-10-12 19:29:02Z | 2026-10-12 20:47:12Z | 2026-10-12 23:47:23Z |
| `r1_sb_jpeg_noc40_s1` | 2026-10-12 22:53:58Z | 2026-10-13 00:05:05Z | 2026-10-13 03:12:31Z |
| `r1_sb_jpeg_noc40_s2` | 2026-10-12 23:56:51Z | 2026-10-13 01:06:31Z | 2026-10-13 04:14:56Z |
| `r1_sb_c23only_s42` | 2026-10-13 03:20:46Z | 2026-10-13 05:43:42Z | 2026-10-13 07:17:39Z |
| `r1_sb_c23only_s1` | 2026-10-13 04:23:08Z | 2026-10-13 06:05:53Z | 2026-10-13 08:18:33Z |
| `r1_sb_c23only_s2` | 2026-10-13 07:26:21Z | 2026-10-13 09:56:41Z | 2026-10-13 11:20:57Z |
| `r1_abl_lrbb_s42` | 2026-10-13 11:37:16Z | 2026-10-13 12:41:19Z | 2026-10-13 19:38:35Z |
| `r1_abl_lrfreq_s42` | 2026-10-13 11:48:40Z | 2026-10-13 13:39:54Z | 2026-10-13 19:44:12Z |
| `r1_abl_aux_s42` | 2026-10-13 20:00:16Z | 2026-10-13 23:40:13Z | 2026-10-14 03:44:08Z |
| `r1_abl_ep50_s42` | 2026-10-13 20:04:42Z | 2026-10-13 21:51:44Z | 2026-10-14 08:43:34Z |
| `r1_abl_curriculum_s42` | 2026-10-13 08:31:11Z | 2026-10-13 11:04:12Z | 2026-10-13 11:30:46Z |
| `r1x_abl_curriculum_rerun_s42` | 2026-10-16 13:54:42Z | 2026-10-16 20:40:02Z | 2026-10-17 04:26:36Z |
| `r1x_abl_curriculum_nostop_s42` | 2026-10-16 13:54:50Z | 2026-10-16 20:05:43Z | 2026-10-17 04:26:34Z |
| `r1x_abl_curriculum_emafix_s42` | 2026-10-16 21:05:31Z | 2026-10-17 03:24:06Z | 2026-10-17 04:35:44Z |

## The ordering that matters

* The earliest epoch-1 checkpoint of any registered campaign run (`r1_fairn_grl_s42`, 2026-10-11 12:41:58Z) was written after the tag `phase6-prereg` (2026-10-11 12:20:18Z). The pre-registration itself records that no campaign run existed when it was written.
* The three curriculum re-runs (`r1x_*`) are not registered runs: they were planned after the first curriculum run stopped, and their configurations say so. They are listed for completeness.

