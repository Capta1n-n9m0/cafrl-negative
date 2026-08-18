"""Face alignment — similarity transform from 5-point landmarks.

The as-built face extraction warps each detected face to fixed reference
5-point landmarks via a similarity transform (`cv2.warpAffine`,
`BORDER_REPLICATE`) — *not* a bbox/margin crop. The deterministic re-crop
(`src/scripts/recrop_faces.py`) must reuse the **identical** warp so that
cross-compression views of the same `frame_idx` are geometrically identical by
construction.

This module is the single source of truth for that warp. It was lifted verbatim
out of `src/scripts/extract_faces.py` (no behaviour change); `extract_faces.py`
now imports from here.
"""

from __future__ import annotations

import cv2
import numpy as np

# Reference 5-point landmarks (left eye, right eye, nose, left mouth, right
# mouth) in a 256×256 output canvas. Scaled linearly for other output sizes.
REFERENCE_LANDMARKS_256 = np.array([
    [89.0, 105.0],   # left eye
    [167.0, 105.0],  # right eye
    [128.0, 150.0],  # nose
    [96.0, 195.0],   # left mouth
    [160.0, 195.0],  # right mouth
], dtype=np.float32)


def estimate_similarity_transform(
    src: np.ndarray, dst: np.ndarray,
) -> np.ndarray:
    """Estimate 2x3 similarity transform matrix from point correspondences."""
    src_mean = src.mean(axis=0)
    dst_mean = dst.mean(axis=0)
    src_c = src - src_mean
    dst_c = dst - dst_mean

    denom = (src_c ** 2).sum()
    if denom < 1e-10:
        return np.eye(2, 3, dtype=np.float32)

    a = (dst_c[:, 0] * src_c[:, 0] + dst_c[:, 1] * src_c[:, 1]).sum() / denom
    b = (dst_c[:, 1] * src_c[:, 0] - dst_c[:, 0] * src_c[:, 1]).sum() / denom

    return np.array([
        [a, -b, dst_mean[0] - a * src_mean[0] + b * src_mean[1]],
        [b,  a, dst_mean[1] - b * src_mean[0] - a * src_mean[1]],
    ], dtype=np.float32)


def align_face(
    img: np.ndarray,
    landmarks: np.ndarray,
    output_size: int = 256,
) -> np.ndarray:
    ref = REFERENCE_LANDMARKS_256 * (output_size / 256.0)
    M = estimate_similarity_transform(landmarks, ref)
    return cv2.warpAffine(
        img, M, (output_size, output_size),
        borderMode=cv2.BORDER_REPLICATE,
    )
