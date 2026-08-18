"""CAFRL configuration package."""

from __future__ import annotations

from .defaults import (
    Config,
    DataConfig,
    DCTConfig,
    DiscriminatorConfig,
    EstimatorConfig,
    EvalConfig,
    FusionConfig,
    InvarianceArm,
    LossConfig,
    ModelConfig,
    PathsConfig,
    PhaseConfig,
    TrainConfig,
    resolve_path,
)
from .load import dump_config, load_config, to_dict

__all__ = [
    "Config",
    "DataConfig",
    "DCTConfig",
    "DiscriminatorConfig",
    "EstimatorConfig",
    "EvalConfig",
    "FusionConfig",
    "InvarianceArm",
    "LossConfig",
    "ModelConfig",
    "PathsConfig",
    "PhaseConfig",
    "TrainConfig",
    "resolve_path",
    "dump_config",
    "load_config",
    "to_dict",
]
