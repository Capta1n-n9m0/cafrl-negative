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

## Before you run any of this

These scripts are the working code of a research campaign, not a packaged tool.
Two things must be set up, and neither is done for you.

**1. Roots.** Every local path was replaced by a `${PLACEHOLDER}` name when this
code was exported, so the constants below are *literal strings*, not expanded
variables — edit them, or export the corresponding directories and expand them
yourself, before running anything. The full inventory, regenerated on every
release build:

| placeholder | what it is | where it appears |
|---|---|---|
| `${HOME}` | the authors' home directory | `pipeline/dfd/align.py:122`, `pipeline/dfd/align.py:123`, `pipeline/dfd/audit.py:12`, `pipeline/dfd/detect_targets.py:38` (+9 more) |
| `${METADATA_CSV}` | the per-video FF++ metadata CSV | `pipeline/dfd/index.py:23` |

Some files in the same directory read a root through `Path.home() / "sdb" / ...`
instead; those are the authors' original storage layout and need editing too.

**2. Imports.** The shared modules these scripts import live at `pipeline/src/`,
so the `pipeline/` directory must be on the import path:

```bash
PYTHONPATH=pipeline python pipeline/crf/generate_crf_variants.py --help
```

The two DFD scripts that import `reextract_tracks` additionally need
`pipeline/faces` on the path. A few module-level constants resolve relative to
the *original* repository layout (`assess_extraction.py`'s metadata path, and
`generate_crf_variants.py`'s default `--metadata-csv`); point them at the
FF++ metadata CSV you build yourself.

Code comments in this directory also cite internal design documents by name
(`docs/…`, `implementation-plan.md`) and modules that are not part of this
release. They are left as written; nothing in this repository depends on them.

They are released because the procedure is part of the claim, and a reader who
wants to know exactly what "deterministic re-crop of curated multi-person face
tracks" means should be able to read the code that did it.
