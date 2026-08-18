# Encoder versions and the exact re-encode command

The compression ladder is real H.264. Which encoder build produced it matters:
rate-control and psychovisual defaults differ between x264 releases, so the same
CRF value from a different build is not the same video. These strings were read
from the binaries in the project environment, which has not been rebuilt since the
encoding was performed; `docs/15-phase1-build.md` records the same FFmpeg version at encode time.

## FFmpeg

```
ffmpeg version 4.2.2 Copyright (c) 2000-2019 the FFmpeg developers
    libavutil      56. 31.100 / 56. 31.100
    libavcodec     58. 54.100 / 58. 54.100
    libavformat    58. 29.100 / 58. 29.100
    libavdevice    58.  8.100 / 58.  8.100
    libavfilter     7. 57.100 /  7. 57.100
    libavresample   4.  0.  0 /  4.  0.  0
    libswscale      5.  5.100 /  5.  5.100
    libswresample   3.  5.100 /  3.  5.100
    libpostproc    55.  5.100 / 55.  5.100
```

## x264

Read out of a probe encode's SEI header — the build string every encoded file
carries:

```
x264 - core 157 - H.264/MPEG-4 AVC codec - Copyleft 2003-2018 - http://www.videolan.org/x264.html
```

Encoder settings actually applied. This line comes from a small probe encode made
with the same binary and the same flags, so read `crf` and `threads` as
per-invocation values (the ladder uses crf 18/28/32/36 and `-threads 8`); every
other setting is what `-preset medium` fixes and is what the ladder was encoded
with:

```
    cabac=1 ref=3 deblock=1:0:0 analyse=0x3:0x113 me=hex subme=7 psy=1 psy_rd=1.00:0.00 mixed_ref=1 me_range=16 chroma_me=1 trellis=1 8x8dct=1 cqm=0 deadzone=21,11 fast_pskip=1 chroma_qp_offset=-2 threads=2 lookahead_threads=1 sliced_threads=0 nr=0 decimate=1 interlaced=0 bluray_compat=0 constrained_intra=0 bframes=3 b_pyramid=2 b_adapt=1 b_bias=0 direct=1 weightb=1 open_gop=0 weightp=2 keyint=250 keyint_min=25 scenecut=40 intra_refresh=0 rc_lookahead=40 rc=crf mbtree=1 crf=23.0 qcomp=0.60 qpmin=0 qpmax=69 qpstep=4 ip_ratio=1.40 aq=1:1.00
```

## The command

Per source video and target level, with `CRF` ∈ {18, 28, 32, 36} (28/32/36 for all
videos, 18 for the test split only; the distributed c23 and c40 encodes are used
as published, and c0 is the lossless source):

```bash
ffmpeg -y -i <source.mp4> \
       -c:v libx264 -crf <CRF> -preset medium -pix_fmt yuv420p \
       -threads 8 -vsync passthrough -an <out.mp4>
```

Three choices in that line carry weight:

* `-preset medium` — FaceForensics++ never published a preset, so one is fixed
  here for a reproducible speed/quality operating point (it is also x264's
  default).
* `-vsync passthrough` (`-fps_mode passthrough` on FFmpeg ≥ 5, the identical
  option after its rename) — copy each source frame one-to-one. Without it,
  libx264's constant-frame-rate muxing can duplicate frames on the odd variable
  frame-rate sources in FF++, which would break the frame-index correspondence
  the cross-level crops depend on.
* `-pix_fmt yuv420p` — 8-bit 4:2:0, the standard delivery format.

Every output is verified against its source's frame count before being accepted;
a mismatch is re-encoded once and then flagged rather than silently used.
