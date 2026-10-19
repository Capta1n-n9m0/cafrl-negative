"""Config loading: YAML deep-merge into the dataclass tree + resolved dump.

``load_config`` merges an optional YAML override file onto the defaults in
``defaults.py``. Unknown keys are a hard error (typo protection) that names the
offending dotted path; type mismatches are also a hard error. ``dump_config``
(and ``Config.dump`` via a thin wrapper) writes the fully-resolved config —
including ``~`` expansion of path fields and enum-as-string — to ``run_dir`` for
reproducibility.
"""

from __future__ import annotations

import dataclasses
import typing
from enum import Enum
from pathlib import Path
from typing import Any, get_args, get_origin

import yaml

from . import defaults as _defaults_module
from .defaults import Config, PathsConfig, resolve_path


def _resolved_field_types(obj: Any) -> dict[str, Any]:
    """Return real (not string) field types for a dataclass instance.

    ``from __future__ import annotations`` stores annotations as strings;
    ``get_type_hints`` resolves them against the defining module's namespace.
    """
    return typing.get_type_hints(type(obj), globalns=vars(_defaults_module))


# ---------------------------------------------------------------------------
# Deep merge
# ---------------------------------------------------------------------------

def _coerce_scalar(value: Any, target_type: Any, path: str) -> Any:
    """Coerce/validate a scalar override ``value`` to the dataclass field type.

    Handles ``X | None`` unions, enums (from their string value), tuples (from
    YAML lists), and the int/float/bool/str primitives. Raises ``TypeError`` with
    the dotted ``path`` on a mismatch.
    """
    # Unwrap Optional / unions: accept the first member type that fits.
    origin = get_origin(target_type)
    if origin is not None and origin is not tuple:
        # typing.Union (incl. ``X | None``) — get_origin returns types.UnionType
        # or typing.Union depending on syntax; both expose members via get_args.
        args = get_args(target_type)
        if args:
            if value is None and type(None) in args:
                return None
            non_none = [a for a in args if a is not type(None)]
            last_err: Exception | None = None
            for candidate in non_none:
                try:
                    return _coerce_scalar(value, candidate, path)
                except TypeError as exc:  # noqa: PERF203 - tiny union
                    last_err = exc
            raise TypeError(
                f"config value for '{path}' = {value!r} does not match any of "
                f"{target_type}"
            ) from last_err

    # Enums: build from the string value.
    if isinstance(target_type, type) and issubclass(target_type, Enum):
        try:
            return target_type(value)
        except ValueError as exc:
            allowed = [e.value for e in target_type]
            raise TypeError(
                f"config value for '{path}' = {value!r} is not a valid "
                f"{target_type.__name__}; allowed: {allowed}"
            ) from exc

    # Tuples (from YAML lists).
    if target_type is tuple or origin is tuple:
        if not isinstance(value, (list, tuple)):
            raise TypeError(
                f"config value for '{path}' = {value!r} must be a list/tuple"
            )
        elem_types = get_args(target_type)
        if elem_types and not (len(elem_types) == 2 and elem_types[1] is Ellipsis):
            # Fixed-length tuple type, e.g. tuple[int, int].
            if len(value) != len(elem_types):
                raise TypeError(
                    f"config value for '{path}' expects {len(elem_types)} "
                    f"elements, got {len(value)}"
                )
            return tuple(
                _coerce_scalar(v, t, f"{path}[{i}]")
                for i, (v, t) in enumerate(zip(value, elem_types))
            )
        if elem_types:  # homogeneous tuple[T, ...]
            elem_t = elem_types[0]
            return tuple(
                _coerce_scalar(v, elem_t, f"{path}[{i}]")
                for i, v in enumerate(value)
            )
        return tuple(value)

    # Primitives.
    if target_type is bool:
        if not isinstance(value, bool):
            raise TypeError(f"config value for '{path}' = {value!r} must be a bool")
        return value
    if target_type is int:
        # bool is a subclass of int — reject it to avoid silent coercion.
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"config value for '{path}' = {value!r} must be an int")
        return value
    if target_type is float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"config value for '{path}' = {value!r} must be a float")
        return float(value)
    if target_type is str:
        if not isinstance(value, str):
            raise TypeError(f"config value for '{path}' = {value!r} must be a str")
        return value

    # Fallback: accept as-is (e.g. Any / untyped).
    return value


def _merge_into(obj: Any, overrides: dict[str, Any], path: str) -> None:
    """Recursively apply ``overrides`` (a nested dict) onto a dataclass ``obj``.

    Mutates ``obj`` in place. Unknown keys raise ``KeyError`` naming the dotted
    path; nested dicts targeting non-dataclass fields raise ``TypeError``.
    """
    fields = {f.name: f for f in dataclasses.fields(obj)}
    field_types = _resolved_field_types(obj)
    for key, value in overrides.items():
        dotted = f"{path}.{key}" if path else key
        if key not in fields:
            valid = sorted(fields.keys())
            raise KeyError(
                f"unknown config key '{dotted}'. Valid keys at this level: {valid}"
            )
        field = fields[key]
        current = getattr(obj, field.name)
        if dataclasses.is_dataclass(current) and not isinstance(current, type):
            if not isinstance(value, dict):
                raise TypeError(
                    f"config key '{dotted}' is a nested section; expected a "
                    f"mapping, got {type(value).__name__}"
                )
            _merge_into(current, value, dotted)
        else:
            if isinstance(value, dict):
                raise TypeError(
                    f"config key '{dotted}' is a scalar field; got a mapping "
                    f"{value!r}"
                )
            target_type = field_types.get(field.name, field.type)
            setattr(obj, field.name, _coerce_scalar(value, target_type, dotted))


def load_config(overrides: Path | str | None = None) -> Config:
    """Load the default ``Config`` and deep-merge a YAML override file onto it.

    Unknown keys and type mismatches are hard errors. Pass ``None`` for the
    pristine defaults.
    """
    cfg = Config()
    if overrides is None:
        return cfg
    override_path = Path(overrides)
    if not override_path.is_file():
        raise FileNotFoundError(f"override file not found: {override_path}")
    with override_path.open("r") as fh:
        data = yaml.safe_load(fh)
    if data is None:  # empty / comments-only file
        return cfg
    if not isinstance(data, dict):
        raise TypeError(
            f"override file {override_path} must contain a top-level mapping, "
            f"got {type(data).__name__}"
        )
    # A dumped run config (Phase 6) may carry top-level run-metadata records:
    # ``provenance`` (git commit, CLI, ...; src/train.py and train_baseline) and,
    # for SpatialBase runs, ``baseline`` / ``baseline_run`` (train_baseline's
    # resolved hyper-parameters and run options). They are metadata, not Config
    # fields: skip them so a run's own config.yaml still loads (eval_battery /
    # eval_faceshifter read it). Only these exact names, and only as mappings;
    # every other unknown key stays a hard error (typo protection).
    for meta_key in RUN_METADATA_KEYS:
        if meta_key in data:
            if not isinstance(data[meta_key], dict):
                raise TypeError(
                    f"'{meta_key}' in {override_path} must be a mapping, got "
                    f"{type(data[meta_key]).__name__}"
                )
    data = {k: v for k, v in data.items() if k not in RUN_METADATA_KEYS}
    _merge_into(cfg, data, "")
    return cfg


# ---------------------------------------------------------------------------
# Dump (resolved)
# ---------------------------------------------------------------------------

# Top-level key of the run-provenance record in a dumped config.yaml.
PROVENANCE_KEY = "provenance"

# Top-level run-metadata blocks ``load_config`` skips (whitelist by name):
# the provenance record, and train_baseline's ``baseline:`` / ``baseline_run:``
# blocks (S2 2c fixer, finding 1: eval of new SpatialBase runs).
RUN_METADATA_KEYS: frozenset[str] = frozenset(
    {PROVENANCE_KEY, "baseline", "baseline_run"}
)

# Path fields are resolved (``~`` expanded) on dump for reproducibility.
_PATH_FIELDS = {f.name for f in dataclasses.fields(PathsConfig)}


def _to_plain(obj: Any, *, resolve_paths: bool, is_paths_section: bool = False) -> Any:
    """Convert a dataclass tree to plain Python types for YAML serialization."""
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        is_paths = isinstance(obj, PathsConfig)
        out: dict[str, Any] = {}
        for f in dataclasses.fields(obj):
            out[f.name] = _to_plain(
                getattr(obj, f.name),
                resolve_paths=resolve_paths,
                is_paths_section=is_paths,
            )
        return out
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, tuple):
        return [
            _to_plain(v, resolve_paths=resolve_paths) for v in obj
        ]
    if isinstance(obj, list):
        return [_to_plain(v, resolve_paths=resolve_paths) for v in obj]
    return obj


def to_dict(cfg: Config, *, resolve_paths: bool = False) -> dict[str, Any]:
    """Serialize ``cfg`` to a plain nested dict (enums→str, tuples→list).

    With ``resolve_paths=True`` the ``paths.*`` fields are ``~``-expanded.
    """
    plain = _to_plain(cfg, resolve_paths=resolve_paths)
    if resolve_paths:
        for name in _PATH_FIELDS:
            plain["paths"][name] = str(resolve_path(plain["paths"][name]))
    return plain


def dump_config(
    cfg: Config, run_dir: Path | str, filename: str = "config.yaml",
    *, provenance: dict[str, Any] | None = None,
) -> Path:
    """Write the fully-resolved config as YAML into ``run_dir`` and return the path.

    ``provenance`` (optional, Phase 6) is appended as a top-level ``provenance:``
    mapping (git commit, dirty flag, CLI). ``load_config`` skips that key, so the
    file still round-trips. Without it the output is exactly the old dump.
    """
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    out_path = run_dir / filename
    plain = to_dict(cfg, resolve_paths=True)
    if provenance is not None:
        if PROVENANCE_KEY in plain:  # pragma: no cover - Config has no such field
            raise KeyError(f"Config already has a '{PROVENANCE_KEY}' section")
        plain[PROVENANCE_KEY] = dict(provenance)
    with out_path.open("w") as fh:
        yaml.safe_dump(plain, fh, sort_keys=False, default_flow_style=False)
    return out_path
