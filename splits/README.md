# Evaluation-set video-ID lists

What was scored, for every reported cell. Media is never redistributed here — these
are identifiers, labels, and evaluation order.

| file | eval set | videos | notes |
|---|---|---|---|
| `ffpp_test_c0.json` | ffpp_test@c0 | 700 | 560 fake / 140 real |
| `ffpp_test_c18.json` | ffpp_test@c18 | 700 | 560 fake / 140 real |
| `ffpp_test_c23.json` | ffpp_test@c23 | 700 | 560 fake / 140 real |
| `ffpp_test_c28.json` | ffpp_test@c28 | 700 | 560 fake / 140 real |
| `ffpp_test_c32.json` | ffpp_test@c32 | 700 | 560 fake / 140 real |
| `ffpp_test_c36.json` | ffpp_test@c36 | 700 | 560 fake / 140 real |
| `ffpp_test_c40.json` | ffpp_test@c40 | 700 | 560 fake / 140 real |
| `faceshifter_n280_c23.json` | faceshifter@c23 | 280 | 140 fake / 140 real |
| `faceshifter_n280_c40.json` | faceshifter@c40 | 280 | 140 fake / 140 real |
| `celebdf_v2_test.json` | celebdf_v2_test | 518 | 340 fake / 178 real |
| `dfd_eval_c23.json` | dfd@c23 | 3431 | 3068 fake / 363 real |
| `dfd_eval_c40.json` | dfd@c40 | 3431 | 3068 fake / 363 real |

**Order matters.** In `ffpp_test_*.json` and `faceshifter_n280_*.json` the `videos`
array is in *evaluation order*, and every released run was evaluated on that same
ordered list (the build verifies this run-by-run). The paired video bootstrap draws
one shared index vector per replicate and applies it to both arms, so position `i`
of one run's `score` array and position `i` of another's refer to the same video.
`keys_sha256` in both the split file and each prediction file pins that order.

**Labels.** `label = 1` means fake throughout, including for Celeb-DF v2, whose
official list uses the opposite convention (see the note in that file).

**FF++ identifiers.** `video_id` is `{target}_{source}` for manipulated videos and
the bare ID for pristine ones; `method` is the manipulation (empty for reals). The
pooling key is the pair `(video_id, method)`, so the same source video appearing
under several manipulations stays distinct.

`ffpp_official/` holds the official FaceForensics++ `[target, source]` ID-pair
split lists, unmodified, as loaded by the training code.
