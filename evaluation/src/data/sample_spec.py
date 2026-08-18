"""``SampleSpec`` — the unit of work the sampler hands to the dataset.

Kept in its own module so the Step-1.5 sampler and the Step-1.4 dataset can both
import it without a cycle. The ``source`` field is reserved for the Phase-4 MBRS
3-way source mix (real-H.264 / in-graph ``Q_d`` / clean); it defaults to
``"real"`` so nothing built now needs to know about it.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SampleSpec:
    """A single (video, level, frame) draw, plus augmentation/pairing flags.

    Attributes:
        video_id: FF++ stem — ``{target}_{source}`` (fake) or ``{id}`` (real).
        set: faces-tree set name (``real`` or a method, e.g. ``Deepfakes``).
        level: compression level (``c0``, ``c23``, ``c28``, ...).
        frame_idx: frame index whose crop to load.
        flip: horizontal-flip flag (decided in the sampler so paired views share
            it).
        pair_id: id grouping the two views of a paired sample; ``None`` for
            singles.
        is_anchor: for a paired sample, ``True`` on the anchor view and ``False``
            on the other view. The anchor is the alignment target the consistency
            loss stop-grads (G4/Huang: c23 when the pair contains it, else the
            lower-CRF side — decided in the sampler, see ``sampler.py``).
            Meaningless (and ``False``) for singles (``pair_id is None``).
        source: Phase-4 MBRS source channel; ``"real"`` (real H.264), ``"qd"``
            (in-graph differentiable quantizer), or ``"clean"``. Default
            ``"real"``.
    """

    video_id: str
    set: str
    level: str
    frame_idx: int
    flip: bool = False
    pair_id: int | None = None
    is_anchor: bool = False
    source: str = "real"
