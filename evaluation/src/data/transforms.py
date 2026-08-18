"""Image transforms (phase1.md Step 1.6).

Deliberately minimal. Two operations only:

* ``maybe_flip`` — horizontal flip applied **iff** the flag is set. The flip
  *decision* (``p=0.5``) is made in the sampler (``SampleSpec.flip``) so the two
  views of a paired sample always share it; this module only *applies* it.
* ``to_tensor`` — HWC uint8/float → CHW ``float32`` in ``[0, 1]``.

**No rotation / rescale / crop / JPEG-or-quality augmentation** — on purpose
(implementation-plan.md §4.5): a CRF-label task plus a frequency-domain model
demand strict frequency hygiene. JPEG/quality aug would corrupt the very CRF
labels the estimator predicts; rotation/rescale interpolation damages the high
frequency bands the DCT/phase streams read; a random crop would break the stored
similarity-warp geometry that makes cross-level paired views line up. Per-stream
channel prep (BT.601 Y for DCT/phase, ImageNet norm for the spatial branch)
lives inside the model, not here, so all three streams see one consistent input.
"""

from __future__ import annotations

import numpy as np


def maybe_flip(img: np.ndarray, flip: bool) -> np.ndarray:
    """Horizontally flip ``img`` iff ``flip``.

    Works for HWC (flip axis 1) and CHW (flip axis 2) layouts; the layout is
    inferred from whether the first axis looks like a channel count (1 or 3).
    Returns a contiguous array (a no-op copy-free passthrough when ``flip`` is
    ``False``). The decision is made upstream in the sampler so paired views
    share it — this only applies it.
    """
    if not flip:
        return img
    if img.ndim == 3 and img.shape[0] in (1, 3):  # CHW
        return np.ascontiguousarray(img[:, :, ::-1])
    # HWC (or HW)
    return np.ascontiguousarray(img[:, ::-1])


def to_tensor(img: np.ndarray) -> np.ndarray:
    """HWC uint8/float → CHW ``float32`` in ``[0, 1]``.

    Integer input (e.g. ``uint8`` ``cv2.imread`` output) is scaled by ``1/255``;
    floating input is assumed already in ``[0, 1]`` and only cast. HWC input
    (last axis is the 1- or 3-channel axis) is transposed to CHW; input that is
    already CHW (first axis is the channel axis) is passed through. No
    normalization beyond ``[0, 1]`` — per-stream stats live in the model.
    """
    arr = np.asarray(img)
    if arr.ndim == 3 and arr.shape[-1] in (1, 3) and arr.shape[0] not in (1, 3):
        arr = np.transpose(arr, (2, 0, 1))  # HWC -> CHW
    if np.issubdtype(arr.dtype, np.integer):
        return arr.astype(np.float32) / 255.0
    return arr.astype(np.float32)
