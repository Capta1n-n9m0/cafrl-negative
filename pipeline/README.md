# `pipeline/` — how the evaluation inputs were made

No video or image data is in this repository, and none can be: FaceForensics++,
DeepFakeDetection (distributed through the FaceForensics++ infrastructure) and
Celeb-DF v2 are released under end-user agreements that do not permit
redistributing the videos or imagery derived from them. What can be released is
the procedure, and that is what this directory is: the code that turned source
videos into the exact tensors every reported number was computed on.

Rebuilding the inputs from data you obtain yourself takes three steps.

1. **Obtain the source videos** under the datasets' own agreements.
2. **Re-encode** the FF++ originals to the compression ladder (`crf/`). The paper's
   c28/c32/c36 levels — and c18 for the test split — are real H.264 re-encodes of
   the lossless sources, not JPEG approximations; the exact command line and the
   encoder build that produced them are in `VERSIONS.md`.
3. **Crop faces** (`faces/`). Detection and multi-person track curation run once on
   the lossless source; every other compression level re-applies the *same*
   landmark warp at the *same* frame indices, so views of a frame across levels are
   geometrically identical by construction. Given the source video and the stored
   per-video crop coordinates (in the archival deposit), the crops regenerate
   deterministically — this was verified byte-for-byte.

### `crf/` — Multi-CRF re-encoding

* `generate_crf_variants.py`
### `faces/` — Face detection, track curation, and the deterministic re-crop

* `extract_faces.py`
* `reextract_tracks.py`
* `propagate_tracks.py`
* `recrop_faces.py`
* `assess_extraction.py`
### `dfd/` — DFD track selection (diff-vote + DTW alignment)

* `index.py`
* `align.py`
* `detect_targets.py`
* `select_track.py`
* `extract.py`
* `audit.py`
### `src/` — Shared modules the pipeline scripts import

* `__init__.py`
* `__init__.py`
* `constants.py`
* `face_align.py`
* `frame_select.py`

## Frame selection and pooling

32 frames per video, uniformly spaced over the frames where the curated track was
detected; the same indices at every compression level. A video's score is the mean
over its frames, and the pooling key is `(video_id, method)`.

## Caveat worth stating plainly

These scripts are the working code of a research campaign, not a packaged tool.
They read paths from a configuration block at the top of each file (local paths
have been replaced by `${PLACEHOLDER}` names), they assume the FF++ directory
layout, and several were written to be re-runnable against a partially complete
output tree. They are released because the procedure is part of the claim, and a
reader who wants to know exactly what "deterministic re-crop of curated
multi-person face tracks" means should be able to read the code that did it.
