#!/usr/bin/env python3
"""Common helpers for Horoji validators."""

from __future__ import annotations

import json
import os
import re
import sys
from typing import Any

import yaml

EXPECTED_JSON_LOAD_ERRORS = (OSError, json.JSONDecodeError, ValueError)
EXPECTED_YAML_LOAD_ERRORS = (OSError, yaml.YAMLError)


def compute_repo_root(script_file: str, repo_root_override: str | None = None) -> str:
    if repo_root_override:
        return os.path.abspath(repo_root_override)
    return os.path.abspath(os.path.join(os.path.dirname(script_file), "..", "..", ".."))


def memory_root(repo_root: str) -> str:
    return os.path.join(repo_root, ".project_memory")


def yaml_files_in(directory: str) -> list[str]:
    if not os.path.isdir(directory):
        return []
    return sorted(
        os.path.join(directory, name)
        for name in os.listdir(directory)
        if name.endswith(".yaml")
    )


def yaml_files_recursive(directory: str) -> list[str]:
    result: list[str] = []
    if not os.path.isdir(directory):
        return result
    for root, dirs, files in os.walk(directory):
        dirs.sort()
        result.extend(
            os.path.join(root, name)
            for name in sorted(files)
            if name.endswith(".yaml")
        )
    return result


def load_yaml(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_json(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be a mapping: {path}")
    return data


def normalize_path(path: str, repo_root: str) -> str:
    rel = os.path.relpath(path, repo_root)
    return rel.replace(os.sep, "/")


def _is_type(value: Any, expected: str) -> bool:
    if expected == "string":
        return isinstance(value, str)
    if expected == "array":
        return isinstance(value, list)
    if expected == "object":
        return isinstance(value, dict)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    return True


def validate_against_schema(data: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    errors: list[str] = []

    expected_type = schema.get("type")
    if expected_type and not _is_type(data, expected_type):
        errors.append(
            f"{path}: expected type '{expected_type}', got '{type(data).__name__}'"
        )
        return errors

    if not isinstance(data, dict):
        return errors

    properties = schema.get("properties", {})
    errors.extend(_validate_required_fields(data, schema, path))
    errors.extend(_validate_unknown_fields(data, properties, schema, path))
    errors.extend(_validate_declared_properties(data, properties, path))

    return errors


def _validate_required_fields(data: dict[str, Any], schema: dict[str, Any], path: str) -> list[str]:
    return [
        f"{path}: missing required field '{field}'"
        for field in schema.get("required", [])
        if field not in data
    ]


def _validate_unknown_fields(
    data: dict[str, Any],
    properties: dict[str, Any],
    schema: dict[str, Any],
    path: str,
) -> list[str]:
    if schema.get("additionalProperties", True) is not False:
        return []
    return [
        f"{path}: unknown field '{key}'"
        for key in sorted(data)
        if key not in properties
    ]


def _validate_declared_properties(
    data: dict[str, Any],
    properties: dict[str, Any],
    path: str,
) -> list[str]:
    errors: list[str] = []
    for field, field_schema in properties.items():
        if field in data:
            errors.extend(_validate_property_value(data[field], field_schema, f"{path}.{field}"))
    return errors


def _validate_property_value(value: Any, field_schema: dict[str, Any], field_path: str) -> list[str]:
    field_type = field_schema.get("type")
    if field_type and not _is_type(value, field_type):
        return [
            f"{field_path}: expected type '{field_type}', got '{type(value).__name__}'"
        ]

    errors: list[str] = []
    errors.extend(_validate_enum_value(value, field_schema, field_path))
    errors.extend(_validate_string_length(value, field_type, field_schema, field_path))
    errors.extend(_validate_array_items(value, field_type, field_schema, field_path))
    errors.extend(_validate_object_value(value, field_type, field_schema, field_path))
    return errors


def _validate_enum_value(value: Any, field_schema: dict[str, Any], field_path: str) -> list[str]:
    if "enum" not in field_schema or value in field_schema["enum"]:
        return []
    return [f"{field_path}: value '{value}' not in enum {field_schema['enum']}"]


def _validate_string_length(
    value: Any,
    field_type: str | None,
    field_schema: dict[str, Any],
    field_path: str,
) -> list[str]:
    if field_type != "string" or "minLength" not in field_schema:
        return []
    if not isinstance(value, str) or len(value) >= field_schema["minLength"]:
        return []
    return [
        f"{field_path}: string length {len(value)} is less than minimum {field_schema['minLength']}"
    ]


def _validate_array_items(
    value: Any,
    field_type: str | None,
    field_schema: dict[str, Any],
    field_path: str,
) -> list[str]:
    if field_type != "array" or not isinstance(value, list):
        return []

    errors: list[str] = []
    item_schema = field_schema.get("items", {})
    item_type = item_schema.get("type")
    for idx, item in enumerate(value):
        errors.extend(_validate_array_item(item, item_schema, item_type, f"{field_path}[{idx}]"))
    return errors


def _validate_array_item(
    item: Any,
    item_schema: dict[str, Any],
    item_type: str | None,
    item_path: str,
) -> list[str]:
    errors: list[str] = []
    if item_type and not _is_type(item, item_type):
        errors.append(
            f"{item_path}: expected type '{item_type}', got '{type(item).__name__}'"
        )
    if isinstance(item_schema, dict) and item_schema.get("type") == "object":
        errors.extend(validate_against_schema(item, item_schema, item_path))
    return errors


def _validate_object_value(
    value: Any,
    field_type: str | None,
    field_schema: dict[str, Any],
    field_path: str,
) -> list[str]:
    if field_type == "object" and isinstance(value, dict):
        return validate_against_schema(value, field_schema, field_path)
    return []


def emit_yaml(data: dict[str, Any], stream: Any = sys.stdout) -> None:
    yaml.safe_dump(data, stream, sort_keys=True)


def make_result(
    validator: str,
    status: str,
    target: str,
    reason: str,
    details: list[Any] | None = None,
) -> dict[str, Any]:
    return {
        "validator": validator,
        "status": status,
        "target": target,
        "reason": reason,
        "details": details or [],
    }


def is_valid_identifier(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9_./-]+", value))
