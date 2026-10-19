"""Build-time generator: per-arm parameter counts for the manuscript's arms.

The manuscript prints a parameter count for every arm it compares. Two of the
sources that back them were already released (`probes/param_counts_cafrl.json`
covers the CAFRL arm x conditioning grid), but the counts that belong to
*specific released runs* -- the two fair variants, the trunk control and the
four baseline architectures -- had no artifact at all. This script builds each
model from the configuration the run actually used and counts its parameters,
so every printed count is derivable rather than asserted.

It runs in the project environment (it needs torch/timm to construct the
models), not in the release's CPU-only verification environment: the models are
built with `pretrained=False`, so no weights are downloaded and the count is a
pure function of the architecture code plus the released config.

    conda run -n cv python count_params.py            # writes generated/param_counts_arms.json

The output is copied into the release tree by the manifest's `probes:` section.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP3 = HERE.parent.parent           # experiments/exp3-cafrl
OUT = HERE / "generated" / "param_counts_arms.json"

# (manuscript arm name, released run id, how it is built)
BASELINE_ARMS = [
    ("SpatialBase", "b7_effnet_b0_mq_fliponly", "effnet_b0"),
    ("TrunkCtrl", "trunk_recipe_s42", "cafrl_trunk"),
    ("Xception-mq", "b4_xception_mq", "xception"),
    ("Xception-mq (flip-only)", "b4b_xception_mq_fliponly", "xception"),
    ("Xception (lit)", "b1_xception_lit", "xception"),
    ("Xception-JPEG", "p2a_xcep_jpeg", "xception"),
    ("F3-Net-mq", "b5_f3net_mq", "f3net"),
    ("F3-Net (lit)", "b2_f3net_lit", "f3net"),
    ("FreqNet-mq", "b6_freqnet_mq", "freqnet"),
    ("FreqNet (lit)", "b3_freqnet_lit", "freqnet"),
]

CAFRL_ARMS = [
    ("CAFRL as specified", "a0", "runs/a0/config.yaml"),
    ("CAFRL-adv", "a1_none_s42", "configs/phase5/a1_none_s42.yaml"),
    ("spatial-residual", "cafrl_spatres_s42", "configs/phase5/cafrl_spatres_s42.yaml"),
    ("Fair-N", "f1_none_fair_s42", "configs/phase5/f1_none_fair_s42.yaml"),
    ("Fair-W", "f2_spatres_full_s42", "configs/phase5/f2_spatres_full_s42.yaml"),
]


def main() -> int:
    sys.path.insert(0, str(EXP3))
    from src.baselines import build_baseline
    from src.config.load import load_config
    from src.models.cafrl import CAFRL

    arms: dict[str, dict] = {}

    for name, run, key in BASELINE_ARMS:
        model = build_baseline(key, pretrained=False)
        total = sum(p.numel() for p in model.parameters())
        arms[name] = {
            "run": run, "built_from": f"src.baselines.build_baseline({key!r})",
            "total": total, "millions": round(total / 1e6, 4),
        }

    for name, run, cfg_path in CAFRL_ARMS:
        cfg = load_config(str(EXP3 / cfg_path))
        model = CAFRL(cfg.model, pretrained_backbone=False)
        total = sum(p.numel() for p in model.parameters())
        arms[name] = {
            "run": run, "built_from": f"src.models.CAFRL({cfg_path})",
            "total": total, "millions": round(total / 1e6, 4),
            "components": {k: sum(p.numel() for p in m.parameters())
                           for k, m in model.named_children()
                           if sum(p.numel() for p in m.parameters())},
        }

    # The discriminator sits on the gradient-reversal branch and runs in every forward
    # pass, evaluation included; the prediction does not use its output. Recorded so the
    # manuscript's "1.32 M discriminator, which the prediction does not use (10.65 M
    # without it)" is derivable.
    for name, body in arms.items():
        disc = body.get("components", {}).get("discriminator", 0)
        if disc:
            body["inference_total"] = body["total"] - disc
            body["inference_millions"] = round(body["inference_total"] / 1e6, 4)

    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=EXP3,
                                capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        commit = None

    payload = {
        "what": "Trainable-parameter counts of every arm the manuscript compares, "
                "built from the configuration each released run used.",
        "convention": "Every model is counted as trained here: the ImageNet 1000-way "
                      "classifier is replaced by a single-logit head, which is why "
                      "EfficientNet-B0 reads 4.0 M rather than its usual 5.3 M and "
                      "Xception 20.8 M rather than 22.9 M. Counts include every "
                      "trained parameter; where an arm carries an adversarial "
                      "discriminator, `inference_total` excludes it (the branch is "
                      "discarded at test time).",
        "pretrained_weights_loaded": False,
        "source_commit": commit,
        "arms": arms,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"wrote {OUT}")
    for name, body in arms.items():
        print(f"  {name:26s} {body['total']:>10,d}  ({body['millions']:.4f} M)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
