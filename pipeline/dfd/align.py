"""Temporal alignment of a DFD fake to its target real via banded subsequence-DTW.

A DFD fake reuses the target's actual frames outside the swapped inner face
(verified: matched-frame cosine ~1.0), but ~90% are shorter than the target —
trailing truncation, a contiguous subclip, or frames dropped throughout. We
recover, for each fake frame i, the target frame ``t(i)`` it corresponds to.

Model: every fake frame maps to a strictly-increasing target frame (a subsequence
of the target). With N<=M that forces ``t(i) ∈ [i, i + (M-N)]`` — a tight band of
width ``D+1`` where ``D = M-N`` — so the DP is O(N·(D+1)) in offset coordinates
``k = t(i) - i`` (prefix-min along k). Mean path cost (1 - cosine) is the quality
flag: ~0 means clean alignment; high means backgrounds don't match (flag it).

Fingerprints are low-res mean-subtracted unit-norm grayscale frames so cosine
similarity = dot product and the background/body (not the small swapped face)
dominates the match.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from decord import VideoReader, cpu

FW, FH = 64, 36          # fingerprint resolution (16:9)


def fingerprints(path: Path, indices: list[int] | None = None,
                 fw: int = FW, fh: int = FH) -> np.ndarray:
    """Decode frames at low res -> mean-subtracted, unit-norm grayscale [N, fw*fh]."""
    vr = VideoReader(str(path), ctx=cpu(0), width=fw, height=fh)
    if indices is None:
        indices = list(range(len(vr)))
    frames = vr.get_batch(indices).asnumpy()
    gray = frames.mean(axis=3).reshape(len(indices), -1).astype(np.float32)
    gray -= gray.mean(axis=1, keepdims=True)
    gray /= np.clip(np.linalg.norm(gray, axis=1, keepdims=True), 1e-6, None)
    return gray


def _running_argmin(a: np.ndarray) -> np.ndarray:
    """For each j, index k<=j of the minimum of a[:j+1] (ties -> latest)."""
    cummin = np.minimum.accumulate(a)
    hit = np.where(a <= cummin + 1e-12, np.arange(len(a)), -1)
    return np.maximum.accumulate(hit)


@dataclass
class Alignment:
    t: np.ndarray          # t[i] = target frame for fake frame i (len N_fake)
    mean_cost: float       # mean (1 - cosine) along the path; ~0 is good
    max_cost: float        # worst single-frame cost along the path
    n_fake: int
    n_target: int
    max_gap: int           # largest jump t[i+1]-t[i] (1 = consecutive)
    n_gaps: int            # number of dropped-frame jumps (>1)
    offset0: int           # t[0]
    offsetN: int           # t[-1] - (N-1)


def align(fake_path: Path, target_path: Path,
          fk: np.ndarray | None = None, tgt: np.ndarray | None = None) -> Alignment:
    """Align a fake to its target. Pass cached fingerprints to avoid re-decoding."""
    if fk is None:
        fk = fingerprints(fake_path)
    if tgt is None:
        tgt = fingerprints(target_path)
    n, m = len(fk), len(tgt)

    if n > m:
        # No fake is longer than its target in DFD; clamp defensively.
        t = np.minimum(np.arange(n), m - 1)
        cost = 1.0 - (fk * tgt[t]).sum(axis=1)
        return Alignment(t, float(cost.mean()), float(cost.max()), n, m,
                         int(np.diff(t).max(initial=1)), int((np.diff(t) > 1).sum()),
                         int(t[0]), int(t[-1] - (n - 1)))

    D = m - n                              # band width - 1
    INF = 1e9
    # cost_band[i, k] = 1 - cos(fk[i], tgt[i+k]), k in [0, D]
    cost_band = np.empty((n, D + 1), dtype=np.float32)
    for i in range(n):
        win = tgt[i:i + D + 1]             # [D+1, dim]
        cost_band[i] = 1.0 - win @ fk[i]

    dp = np.empty((n, D + 1), dtype=np.float64)
    bk = np.full((n, D + 1), -1, dtype=np.int32)
    dp[0] = cost_band[0]
    for i in range(1, n):
        prev = dp[i - 1]
        dp[i] = cost_band[i] + np.minimum.accumulate(prev)   # min over k'<=k
        bk[i] = _running_argmin(prev)

    k = int(np.argmin(dp[n - 1]))
    ks = np.empty(n, dtype=np.int64)
    for i in range(n - 1, -1, -1):
        ks[i] = k
        k = bk[i, k]
    t = np.arange(n) + ks
    path_cost = cost_band[np.arange(n), ks]
    gaps = np.diff(t)
    return Alignment(
        t=t, mean_cost=float(path_cost.mean()), max_cost=float(path_cost.max()),
        n_fake=n, n_target=m,
        max_gap=int(gaps.max(initial=1)), n_gaps=int((gaps > 1).sum()),
        offset0=int(t[0]), offsetN=int(t[-1] - (n - 1)),
    )


# --------------------------------------------------------------------------
# Self-check against the probe_dtw cases
# --------------------------------------------------------------------------
_CASES = [
    ("22_23__secret_conversation__10R2HRAU.mp4", "22__secret_conversation.mp4"),
    ("20_01__walking_and_outside_surprised__OTGHOG4Z.mp4", "20__walking_and_outside_surprised.mp4"),
    ("08_28__kitchen_pan__LVT0XNQG.mp4", "08__kitchen_pan.mp4"),
    ("26_25__talking_angry_couch__XKQAYTLI.mp4", "26__talking_angry_couch.mp4"),
    ("15_18__walking_down_street_outside_angry__V5VHLCOW.mp4", "15__walking_down_street_outside_angry.mp4"),
    ("03_21__kitchen_still__V53E3RVB.mp4", "03__kitchen_still.mp4"),
]
_FAKE_DIR = Path("${HOME}/sdc/datasets/ffpp_original/manipulated_sequences/DeepFakeDetection/c23/videos")
_REAL_DIR = Path("${HOME}/sdc/datasets/ffpp_original/original_sequences/actors/c23/videos")


def _selfcheck() -> None:
    print(f"{'fake':<52}{'N':>5}{'M':>5}{'off0':>6}{'offN':>6}{'maxgap':>7}{'ngaps':>6}{'meanC':>8}")
    print("-" * 90)
    for fake, real in _CASES:
        a = align(_FAKE_DIR / fake, _REAL_DIR / real)
        print(f"{fake:<52}{a.n_fake:>5}{a.n_target:>5}{a.offset0:>6}{a.offsetN:>6}"
              f"{a.max_gap:>7}{a.n_gaps:>6}{a.mean_cost:>8.4f}")


if __name__ == "__main__":
    _selfcheck()
