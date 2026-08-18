"""Deterministic frame selection — linspace over the available list (phase1.md Step 1.3).

A single source of truth shared by the re-crop (`recrop_faces.py`), the index
builder (`index.py`), and the eval-mode dataset iterator (`ffpp_faces.py`), so
the 32 chosen frames are identical everywhere.

Rule:
1. ``n = min(32, len(available))``;
2. ``np.linspace(0, len(available) - 1, n).round()`` indexes **into the sorted
   available list** — i.e. pick ``n`` evenly-spaced *positions*, then map each to
   the frame index actually stored there.

Because the linspace is taken over positions in ``available`` (not over the full
``[0, num_frames_total)`` range with a snap-to-nearest step), the picks are always
``n`` distinct frames whenever ``len(available) >= n`` — the spacing between
consecutive position targets is ``>= 1`` so rounding can never collapse two onto
one. This is byte-identical to a plain ``linspace(0, num_frames_total - 1, n)``
when ``available == [0 .. num_frames_total - 1]`` (the overwhelming majority of
videos), but it does not collapse in detection gaps the way a snap-to-nearest rule
does.

Result: exactly ``min(32, len(available))`` distinct sorted indices. Videos with
genuinely <32 detected frames are the only ones below 32 — they go on an
allow-list the caller logs.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np


def select_frames(
    num_frames_total: int,
    available: Sequence[int],
    n: int = 32,
) -> list[int]:
    """Pick up to ``n`` frame indices via linspace over the available list.

    Args:
        num_frames_total: total frame count of the source video. Kept for
            signature/caller compatibility; not used by the selection itself
            (the rule indexes into ``available``).
        available: frame indices that actually have a stored c0 crop (any order;
            de-duplicated and sorted internally).
        n: target number of frames (32 by protocol).

    Returns:
        Sorted unique frame indices, length ``min(n, len(available))``. Always
        exactly ``n`` distinct frames when ``len(available) >= n``.
    """
    avail = np.asarray(sorted(set(int(a) for a in available)), dtype=np.int64)
    if avail.size == 0:
        return []

    n = min(n, avail.size)
    pos = np.round(np.linspace(0, avail.size - 1, n)).astype(np.int64)
    picks = avail[pos]
    # pos is non-decreasing and (for avail.size >= n) strictly increasing, so the
    # picks are already sorted + distinct; the set/sorted is belt-and-braces.
    return sorted(set(int(x) for x in picks))
