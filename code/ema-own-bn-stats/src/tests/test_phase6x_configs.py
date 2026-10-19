"""W5b (POST HOC) curriculum-retrain configs in ``configs/phase6x/`` — W5b-S0 builder.

Why: the three post-hoc runs V1–V3 (plan ``docs/phases/phase6-w5b-plan.md`` §2) must be the
registered E13 curriculum arm ``configs/phase6/r1_abl_curriculum_s42.yaml`` (frozen) with
exactly the declared change and nothing else:

* V1 ``r1x_abl_curriculum_rerun_s42`` and V2 ``r1x_abl_curriculum_nostop_s42``: no config
  change at all (their stop rules live in the W5b watcher, not in the YAML) — the YAML body is
  byte-identical to the parent's body and the resolved configs are equal;
* V3 ``r1x_abl_curriculum_emafix_s42``: exactly ``train.ema_own_bn_stats: true`` (the EMA-only
  fix of the W5b-S0 diagnosis).

The diff is computed on the RESOLVED config (defaults merged through the real ``load_config``),
in the style of ``test_phase6_configs.py``, so a typo, a stray key or a changed default cannot
slip in. ``MANIFEST.json`` must hash every YAML, and the parent hash in every header and in the
manifest must equal both the parent file and its entry in the frozen ``configs/phase6/MANIFEST.json``.
Config files only: no data, no GPU, no run dir. Run from ``experiments/exp3-cafrl``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest
import yaml

from src.config.load import load_config, to_dict

CFG_DIR = Path("configs/phase6x")
PARENT = Path("configs/phase6/r1_abl_curriculum_s42.yaml")
PARENT_MANIFEST = Path("configs/phase6/MANIFEST.json")
PARENT_SHA = "81e3eb7f272322c578cfd7792eb8700d4d75e438791fd671817a85c64634450c"

DECLARED: dict[str, dict[str, Any]] = {
    "r1x_abl_curriculum_rerun_s42": {},
    "r1x_abl_curriculum_nostop_s42": {},
    "r1x_abl_curriculum_emafix_s42": {"train.ema_own_bn_stats": True},
}
VARIANT = {"r1x_abl_curriculum_rerun_s42": "V1", "r1x_abl_curriculum_nostop_s42": "V2",
           "r1x_abl_curriculum_emafix_s42": "V3"}
RUNS = list(DECLARED)


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _flatten(d: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in d.items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            out.update(_flatten(v, key + "."))
        else:
            out[key] = list(v) if isinstance(v, tuple) else v
    return out


def _resolved(path: Path) -> dict[str, Any]:
    return _flatten(to_dict(load_config(path)))


def _diff(new: dict[str, Any], old: dict[str, Any]) -> dict[str, Any]:
    assert set(new) == set(old), sorted(set(new) ^ set(old))
    return {k: new[k] for k in sorted(new) if new[k] != old[k]}


def _body(path: Path) -> str:
    """The YAML without its comment lines (every header line starts with '#')."""
    return "".join(ln for ln in path.read_text().splitlines(keepends=True)
                   if not ln.startswith("#"))


# ---------------------------------------------------------------------------
# Inventory and hashes
# ---------------------------------------------------------------------------

def test_exactly_the_three_configs_exist() -> None:
    assert sorted(p.stem for p in CFG_DIR.glob("*.yaml")) == sorted(RUNS)


def test_parent_is_the_frozen_registered_config() -> None:
    assert _sha(PARENT) == PARENT_SHA
    entries = [c for c in json.loads(PARENT_MANIFEST.read_text())["configs"]
               if c["config"] == str(PARENT)]
    assert len(entries) == 1 and entries[0]["sha256"] == PARENT_SHA
    assert entries[0]["run"] == "r1_abl_curriculum_s42"


def test_manifest_hashes_every_yaml_and_names_the_parent() -> None:
    man = json.loads((CFG_DIR / "MANIFEST.json").read_text())
    assert man["parent"]["config"] == str(PARENT)
    assert man["parent"]["sha256"] == PARENT_SHA
    rows = man["configs"]
    assert sorted(r["run"] for r in rows) == sorted(RUNS)
    listed = {r["config"] for r in rows}
    on_disk = {str(p) for p in CFG_DIR.glob("*.yaml")}
    assert listed == on_disk
    for r in rows:
        p = Path(r["config"])
        assert p == CFG_DIR / f"{r['run']}.yaml"
        assert _sha(p) == r["sha256"], r["run"]
        assert r["parent"] == str(PARENT)
        assert r["declared_diff"] == DECLARED[r["run"]], r["run"]
        assert r["variant"] == VARIANT[r["run"]]
        assert r["seed"] == 42 and r["trainer"] == "cafrl"


def test_every_header_states_parent_hash_diff_and_post_hoc() -> None:
    for run in RUNS:
        text = (CFG_DIR / f"{run}.yaml").read_text()
        assert text.startswith(f"# Phase 6x (W5b, POST HOC) — {VARIANT[run]} {run}:"), run
        assert f"# Parent: {PARENT}" in text and PARENT_SHA in text, run
        assert "# Diff vs the parent" in text and "# Stop rule" in text, run
        assert "POST HOC" in text and f"--name {run}" in text, run
        assert f"--config configs/phase6x/{run}.yaml" in text, run


# ---------------------------------------------------------------------------
# Body and resolved-config diffs against the frozen parent
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("run", ["r1x_abl_curriculum_rerun_s42",
                                 "r1x_abl_curriculum_nostop_s42"])
def test_v1_v2_body_is_byte_identical_to_the_parent_body(run: str) -> None:
    assert _body(CFG_DIR / f"{run}.yaml") == _body(PARENT)


def test_v3_body_differs_by_exactly_one_added_line() -> None:
    new = _body(CFG_DIR / "r1x_abl_curriculum_emafix_s42.yaml").splitlines()
    old = _body(PARENT).splitlines()
    assert len(new) == len(old) + 1
    added = [ln for ln in new if ln not in old]
    assert added == ["  ema_own_bn_stats: true"]
    assert [ln for ln in new if ln != "  ema_own_bn_stats: true"] == old
    data = yaml.safe_load((CFG_DIR / "r1x_abl_curriculum_emafix_s42.yaml").read_text())
    assert data["train"]["ema_own_bn_stats"] is True


@pytest.mark.parametrize("run", RUNS)
def test_resolved_diff_vs_frozen_parent_is_exactly_declared(run: str) -> None:
    new = _resolved(CFG_DIR / f"{run}.yaml")
    old = _resolved(PARENT)
    assert _diff(new, old) == DECLARED[run], run
    assert new["train.seed"] == 42 and new["train.epochs"] == 30
    assert new["train.curriculum"] == "baby_step"
    assert new["train.phase_bounds"] == [10, 25]
    assert new["train.val_raw"] is True


def test_parent_resolves_with_the_fix_off() -> None:
    """The new field defaults to False, so the frozen parent (and V1/V2) run the original EMA."""
    assert load_config(PARENT).train.ema_own_bn_stats is False
    for run in ("r1x_abl_curriculum_rerun_s42", "r1x_abl_curriculum_nostop_s42"):
        assert load_config(CFG_DIR / f"{run}.yaml").train.ema_own_bn_stats is False
    assert load_config(CFG_DIR / "r1x_abl_curriculum_emafix_s42.yaml").train.ema_own_bn_stats is True
