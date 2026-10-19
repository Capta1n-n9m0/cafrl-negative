"""Publication figures for the paper.

Fig 2 — CRF-sweep curves: (a) shipped-recipe falsification, (b) fair-recipe re-test.
Fig 4 — Fair-W mechanism panel: (a) residual-gate γ trajectories, (b) standalone freq-head AUC.

Reads per-run ``report.json`` sweeps + TensorBoard scalars + (for the shipped
spatial-residual γ-collapse contrast) the raw ``epoch_*.pt`` checkpoints.
In this release the extracted values ship as ``figures/figure_data.json``,
rebuilt from ``predictions/`` and ``curves/``; the extraction path is never
taken, because that cache is always present.

Usage:  python figures/make_figures.py
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path

# --- release build: paths repointed at the release tree ------------
# The extraction path below (`extract()`) reads run directories that are
# not part of this repository; it never executes here, because CACHE —
# `figure_data.json`, assembled from predictions/ and curves/ — is always
# present. Everything from `style()` down is the paper's code verbatim.
RELEASE_ROOT = Path(__file__).resolve().parents[1]
RUNS = RELEASE_ROOT / "runs-not-released"
OUT = RELEASE_ROOT / "figures"
CACHE = OUT / "figure_data.json"

LEVELS = ["c0", "c18", "c23", "c28", "c32", "c36", "c40"]
CRF_X = [0, 18, 23, 28, 32, 36, 40]

# ---------------------------------------------------------------- palette ---
# Validated for colour-vision-deficiency separation (light surface
# #fcfcfb): panel A set worst
# all-pairs CVD ΔE 24.2, panel B set 16.6. Contrast WARNs (aqua/yellow/magenta
# sub-3:1) get relief via per-series markers + legend + the paper's tables.
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
SURFACE = "#ffffff"  # journal page

C_B7 = "#2a78d6"      # slot 1 blue    — SpatialBase (the anchor, both panels)
C_CAFRL = "#1baf7a"   # slot 2 aqua    — CAFRL as specified
C_NONE = "#eda100"    # slot 3 yellow  — CAFRL−adv
C_SPATRES = "#008300" # slot 4 green   — spatial-residual (shipped recipe)
C_F1 = "#4a3aa7"      # slot 5 violet  — Fair-N (narrow trunk)
C_F2 = "#e34948"      # slot 6 red     — Fair-W (full trunk)
C_TRUNK = "#e87ba4"   # slot 7 magenta — TrunkCtrl


@dataclass(frozen=True)
class Arm:
    label: str
    runs: tuple[str, ...]  # 1 run = plain line; 3 runs = seed mean ± t-band
    color: str
    marker: str
    linestyle: str = "-"   # hue alone is not separable in grayscale print


# Panel A is the falsification exactly as the STOP-gate adjudicated it: one
# run per arm at seed 42, so every plotted point is a printed table cell
# (Tables 1 and 4) and the annotated c40 gap is the adjudicated paired Δ.
# Panel B reports the fair-recipe re-tests as 3-seed means ± the 95% t-band.
PANEL_A = (
    Arm("SpatialBase (EffNet-B0)", ("b7_effnet_b0_mq_fliponly",), C_B7, "o", "-"),
    Arm("CAFRL as specified", ("a0",), C_CAFRL, "s", "--"),
    Arm("CAFRL−adv (no adversary)", ("a1_none_s42",), C_NONE, "^", "-."),
    Arm("spatial-residual (γ→0)", ("cafrl_spatres_s42",), C_SPATRES, "D", (0, (1, 1.4))),
)
PANEL_B = (
    Arm("SpatialBase (EffNet-B0)", ("b7_effnet_b0_mq_fliponly", "b7_effnet_b0_mq_fliponly_s1", "b7_effnet_b0_mq_fliponly_s2"), C_B7, "o", "-"),
    Arm("Fair-N (narrow trunk)", ("f1_none_fair_s42", "f1_none_fair_s1", "f1_none_fair_s2"), C_F1, "s", "--"),
    Arm("Fair-W (full trunk)", ("f2_spatres_full_s42", "f2_spatres_full_s1", "f2_spatres_full_s2"), C_F2, "^", "-."),
    Arm("TrunkCtrl", ("trunk_recipe_s42", "trunk_recipe_s1", "trunk_recipe_s2"), C_TRUNK, "D", (0, (1, 1.4))),
)
# Extra runs kept in the cached extraction although no panel plots them: the
# two further shipped-CAFRL seeds, quoted in Fig. 2's caption as the spread
# around panel (a)'s single-seed curve.
EXTRA_SWEEP_RUNS = ("a1_grl_s1", "a1_grl_s2")

F2_RUNS = ("f2_spatres_full_s42", "f2_spatres_full_s1", "f2_spatres_full_s2")
F2_SELECTED_EPOCH = 5  # EMA best-by-val selection, all three seeds


def seed_band(vals: list[float]) -> float:
    """Frozen 3-seed 95% t-band: 4.30 * s / sqrt(3) (metrics.seed_band, k=3)."""
    if len(vals) < 2:
        return 0.0
    mean = sum(vals) / len(vals)
    s = math.sqrt(sum((v - mean) ** 2 for v in vals) / (len(vals) - 1))
    return 4.30 * s / math.sqrt(len(vals))


# ------------------------------------------------------------- extraction ---

def extract() -> dict:
    import torch
    from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

    data: dict = {"sweeps": {}, "f2_tb": {}, "spatres_gamma": {}}

    runs = [r for arm in PANEL_A + PANEL_B for r in arm.runs] + list(EXTRA_SWEEP_RUNS)
    for run in runs:
        if run in data["sweeps"]:
            continue
        rep = json.loads((RUNS / run / "report.json").read_text())
        data["sweeps"][run] = {lv: rep["sweep"][lv]["video_auc"] for lv in LEVELS}

    for run in F2_RUNS:
        ea = EventAccumulator(str(RUNS / run / "tb"))
        ea.Reload()
        per_run: dict[str, dict[int, float]] = {}
        for tag in ("diag/residual_gamma", "auc/freq_c23", "auc/freq_c40"):
            per_run[tag] = {int(e.step): float(e.value) for e in ea.Scalars(tag)}
        data["f2_tb"][run] = per_run

    for ep in range(1, 51):
        ckpt = RUNS / "cafrl_spatres_s42" / f"epoch_{ep}.pt"
        payload = torch.load(ckpt, map_location="cpu", weights_only=False)
        data["spatres_gamma"][str(ep)] = float(payload["model"]["fusion.residual_gamma"])

    return data


def load_data(refresh: bool) -> dict:
    if CACHE.exists() and not refresh:
        return json.loads(CACHE.read_text())
    data = extract()
    OUT.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(data))
    return data


# ---------------------------------------------------------------- styling ---

def style() -> None:
    import matplotlib as mpl

    mpl.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 8,
        "text.color": INK,
        "axes.edgecolor": AXIS,
        "axes.labelcolor": INK2,
        "axes.linewidth": 0.8,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": GRID,
        "grid.linewidth": 0.6,
        "grid.linestyle": "-",
        "axes.axisbelow": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "legend.frameon": False,
        "legend.fontsize": 7,
        "lines.linewidth": 1.6,
        "lines.markersize": 4.5,
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "pdf.fonttype": 42,
    })


def draw_arm(ax, arm: Arm, sweeps: dict) -> None:
    ys = [[sweeps[r][lv] for r in arm.runs] for lv in LEVELS]
    mean = [sum(v) / len(v) for v in ys]
    if len(arm.runs) >= 3:
        band = [seed_band(v) for v in ys]
        # Four overlapping translucent bands print as mud (CEL-13): keep them
        # readable by thinning them; the line style carries the identity.
        ax.fill_between(CRF_X, [m - b for m, b in zip(mean, band)],
                        [m + b for m, b in zip(mean, band)],
                        color=arm.color, alpha=0.07, linewidth=0)
    ax.plot(CRF_X, mean, color=arm.color, marker=arm.marker, label=arm.label,
            linestyle=arm.linestyle,
            markeredgecolor=SURFACE, markeredgewidth=0.8, clip_on=False)


def fig2(data: dict) -> Path:
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.75), sharey=True)
    for ax, arms, title in zip(
        axes, (PANEL_A, PANEL_B),
        ("(a)  Shipped recipe — the STOP-gate result (seed 42)",
         "(b)  Fair recipe — the re-test (3-seed means)"),
    ):
        for arm in arms:
            draw_arm(ax, arm, data["sweeps"])
        ax.set_title(title, fontsize=8, loc="left", color=INK, pad=8)
        ax.set_xticks(CRF_X)
        ax.set_xticklabels(LEVELS)
        ax.set_xlabel("H.264 compression (CRF)")
        ax.set_xlim(-1.5, 41.5)
        ax.legend(loc="lower left", handlelength=1.6, borderaxespad=0.2)
    axes[0].set_ylabel("Video-level AUC (FF++ test)")
    axes[0].set_ylim(0.90, 1.001)

    # The one annotation: the c40 gap in (a) that the fair recipe closes in (b).
    # Both endpoints are the seed-42 runs, so the arrow spans exactly the
    # adjudicated STOP-gate contrast Δ(SpatialBase − CAFRL as specified) = +0.0366.
    b7_c40 = data["sweeps"][PANEL_A[0].runs[0]]["c40"]
    cafrl_c40 = data["sweeps"][PANEL_A[1].runs[0]]["c40"]
    axes[0].annotate(
        "", xy=(40, b7_c40), xytext=(40, cafrl_c40),
        arrowprops=dict(arrowstyle="<->", color=INK2, lw=0.8, shrinkA=2, shrinkB=2),
        annotation_clip=False)
    axes[0].text(38.6, (b7_c40 + cafrl_c40) / 2,
                 f"Δ = {(b7_c40 - cafrl_c40) * 100:.2f} pt\n(paired, s42)",
                 ha="right", va="center", fontsize=7, color=INK2, linespacing=1.35,
                 bbox=dict(facecolor=SURFACE, edgecolor="none", pad=1.2, alpha=0.82))

    fig.tight_layout(w_pad=2.0)
    out = OUT / "fig2_crf_sweep"
    fig.savefig(out.with_suffix(".pdf"))
    fig.savefig(out.with_suffix(".png"), dpi=300)
    plt.close(fig)
    return out.with_suffix(".png")


def fig4(data: dict) -> Path:
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(3.45, 4.4))
    epochs = list(range(1, 31))

    # (a) |γ| trajectories: Fair-W seeds (accent) vs the shipped spatial-residual (context).
    sp = [abs(data["spatres_gamma"][str(ep)]) for ep in epochs]
    ax1.plot(epochs, sp, color=MUTED, linestyle="--", linewidth=1.3,
             label="shipped recipe")
    for i, run in enumerate(F2_RUNS):
        g = {int(k): v for k, v in data["f2_tb"][run]["diag/residual_gamma"].items()}
        xs = sorted(g)
        ax1.plot(xs, [abs(g[x]) for x in xs], color=C_F2,
                 alpha=1.0 if i == 0 else 0.45,
                 linewidth=1.6 if i == 0 else 1.1,
                 label="Fair-W (3 seeds)" if i == 0 else None)
    ax1.axvline(F2_SELECTED_EPOCH, color=AXIS, linewidth=0.8)
    ax1.text(F2_SELECTED_EPOCH - 0.6, 0.002, "selected ckpt (s42, ep 5)", fontsize=6.5,
             color=MUTED, rotation=90, va="bottom", ha="right")
    ax1.set_ylabel("Residual gate  |γ|")
    ax1.set_ylim(0, 0.16)
    ax1.set_xlim(1, 30)
    ax1.set_title("(a)  The γ deadlock, broken", fontsize=8, loc="left", color=INK, pad=8)
    ax1.legend(loc="upper right")

    # (b) standalone freq-head val-AUC (seed mean ± min–max): informative all run.
    for tag, color, label in (("auc/freq_c23", INK2, "freq head @ c23"),
                              ("auc/freq_c40", C_F2, "freq head @ c40")):
        per_seed = [{int(k): v for k, v in data["f2_tb"][r][tag].items()} for r in F2_RUNS]
        xs = sorted(per_seed[0])
        mean = [sum(s[x] for s in per_seed) / 3 for x in xs]
        lo = [min(s[x] for s in per_seed) for x in xs]
        hi = [max(s[x] for s in per_seed) for x in xs]
        ax2.fill_between(xs, lo, hi, color=color, alpha=0.12, linewidth=0)
        ax2.plot(xs, mean, color=color, label=label)
    ax2.axhline(0.5, color=AXIS, linewidth=0.8, linestyle="--")
    ax2.text(1.8, 0.512, "chance", fontsize=6.5, color=MUTED, ha="left")
    ax2.axvline(F2_SELECTED_EPOCH, color=AXIS, linewidth=0.8)
    ax2.set_ylabel("Standalone freq-head AUC (val)\n3-seed mean, min–max band")
    ax2.set_xlabel("Epoch")
    ax2.set_ylim(0.45, 1.0)
    ax2.set_xlim(1, 30)
    ax2.set_title("(b)  The standalone head is discriminative", fontsize=8, loc="left", color=INK, pad=8)
    ax2.legend(loc="lower right")

    fig.tight_layout(h_pad=2.0)
    out = OUT / "fig4_mechanism"
    fig.savefig(out.with_suffix(".pdf"))
    fig.savefig(out.with_suffix(".png"), dpi=300)
    plt.close(fig)
    return out.with_suffix(".png")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh-cache", action="store_true")
    args = parser.parse_args()
    data = load_data(refresh=args.refresh_cache)
    style()
    print(fig2(data))
    print(fig4(data))


if __name__ == "__main__":
    main()
