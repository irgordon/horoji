#!/usr/bin/env python3
"""Common helpers for Horoji validators."""

from __future__ import annotations

import json
import os
import re
import sys
from typing import Any

import yaml


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
        for name in sorted(files):
            if name.endswith(".yaml"):
                result.append(os.path.join(root, name))
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

    required = schema.get("required", [])
    for field in required:
        if field not in data:
            errors.append(f"{path}: missing required field '{field}'")

    additional_properties = schema.get("additionalProperties", True)
    properties = schema.get("properties", {})
    if additional_properties is False:
        for key in sorted(data):
            if key not in properties:
                errors.append(f"{path}: unknown field '{key}'")

    for field, field_schema in properties.items():
        if field not in data:
            continue
        value = data[field]
        field_path = f"{path}.{field}"

        field_type = field_schema.get("type")
        if field_type and not _is_type(value, field_type):
            errors.append(
                f"{field_path}: expected type '{field_type}', got '{type(value).__name__}'"
            )
            continue

        if "enum" in field_schema and value not in field_schema["enum"]:
            errors.append(
                f"{field_path}: value '{value}' not in enum {field_schema['enum']}"
            )

        if field_type == "string" and "minLength" in field_schema:
            if isinstance(value, str) and len(value) < field_schema["minLength"]:
                errors.append(
                    f"{field_path}: string length {len(value)} is less than minimum {field_schema['minLength']}"
                )

        if field_type == "array":
            if isinstance(value, list):
                item_schema = field_schema.get("items", {})
                item_type = item_schema.get("type")
                for idx, item in enumerate(value):
                    item_path = f"{field_path}[{idx}]"
                    if item_type and not _is_type(item, item_type):
                        errors.append(
                            f"{item_path}: expected type '{item_type}', got '{type(item).__name__}'"
                        )
                    if isinstance(item_schema, dict) and item_schema.get("type") == "object":
                        errors.extend(validate_against_schema(item, item_schema, item_path))

        if field_type == "object" and isinstance(value, dict):
            errors.extend(validate_against_schema(value, field_schema, field_path))

    return errors


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
