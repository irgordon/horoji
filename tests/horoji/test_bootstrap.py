"""
Bootstrap tests for Horoji Phase 0 (TASK_00).

Verifies:
- Required directory existence
- Required schema file existence and valid JSON parseability
- Required config file existence and valid YAML parseability
- Negative cases: missing or malformed files are correctly detected
"""

import json
import os
import textwrap

import pytest
import yaml

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MEMORY_ROOT = os.path.join(REPO_ROOT, ".project_memory")
TOOLS_ROOT = os.path.join(REPO_ROOT, "tools", "horoji")


def memory_path(*parts: str) -> str:
    return os.path.join(MEMORY_ROOT, *parts)


def tools_path(*parts: str) -> str:
    return os.path.join(TOOLS_ROOT, *parts)


# ---------------------------------------------------------------------------
# 1. Required directory existence
# ---------------------------------------------------------------------------

REQUIRED_DIRECTORIES = [
    # .project_memory layout
    memory_path("authoritative", "contracts"),
    memory_path("authoritative", "invariants"),
    memory_path("authoritative", "ownership"),
    memory_path("authoritative", "architecture_manifest"),
    memory_path("derived", "callgraphs"),
    memory_path("derived", "dependencies"),
    memory_path("derived", "impact_sets"),
    memory_path("derived", "summaries"),
    memory_path("derived", "embeddings"),
    memory_path("history", "adr"),
    memory_path("history", "decisions"),
    memory_path("schemas"),
    memory_path("config"),
    # tools/horoji layout
    tools_path("cli"),
    tools_path("generators"),
    tools_path("validators"),
    tools_path("invalidation"),
    # tests/horoji
    os.path.join(REPO_ROOT, "tests", "horoji"),
]


@pytest.mark.parametrize("directory", REQUIRED_DIRECTORIES)
def test_required_directory_exists(directory):
    assert os.path.isdir(directory), f"Required directory is missing: {directory}"


# ---------------------------------------------------------------------------
# 2. Required schema files exist and parse as valid JSON
# ---------------------------------------------------------------------------

REQUIRED_SCHEMA_FILES = [
    memory_path("schemas", "contract.schema.json"),
    memory_path("schemas", "invariant.schema.json"),
    memory_path("schemas", "ownership.schema.json"),
    memory_path("schemas", "provenance.schema.json"),
]


@pytest.mark.parametrize("schema_file", REQUIRED_SCHEMA_FILES)
def test_schema_file_exists(schema_file):
    assert os.path.isfile(schema_file), f"Required schema file is missing: {schema_file}"


@pytest.mark.parametrize("schema_file", REQUIRED_SCHEMA_FILES)
def test_schema_file_parses_as_valid_json(schema_file):
    with open(schema_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, dict), f"Schema file did not parse to a dict: {schema_file}"


@pytest.mark.parametrize("schema_file", REQUIRED_SCHEMA_FILES)
def test_schema_file_has_schema_version(schema_file):
    with open(schema_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "schema_version" in data, (
        f"Schema file is missing 'schema_version' field: {schema_file}"
    )


@pytest.mark.parametrize("schema_file", REQUIRED_SCHEMA_FILES)
def test_schema_file_has_required_keys(schema_file):
    with open(schema_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "required" in data, (
        f"Schema file is missing 'required' field (top-level keys not declared): {schema_file}"
    )
    assert isinstance(data["required"], list), (
        f"'required' field must be a list in: {schema_file}"
    )
    assert len(data["required"]) > 0, (
        f"'required' field must not be empty in: {schema_file}"
    )


# ---------------------------------------------------------------------------
# 3. Required config files exist and parse as valid YAML
# ---------------------------------------------------------------------------

REQUIRED_CONFIG_FILES = [
    memory_path("config", "horoji.config.yaml"),
    memory_path("config", "invalidation_rules.yaml"),
]


@pytest.mark.parametrize("config_file", REQUIRED_CONFIG_FILES)
def test_config_file_exists(config_file):
    assert os.path.isfile(config_file), f"Required config file is missing: {config_file}"


@pytest.mark.parametrize("config_file", REQUIRED_CONFIG_FILES)
def test_config_file_parses_as_valid_yaml(config_file):
    with open(config_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert data is not None, f"Config file parsed to None (empty?): {config_file}"


@pytest.mark.parametrize("config_file", REQUIRED_CONFIG_FILES)
def test_config_file_has_schema_version(config_file):
    with open(config_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert "schema_version" in data, (
        f"Config file is missing 'schema_version' field: {config_file}"
    )


# ---------------------------------------------------------------------------
# 4. Negative tests — missing or malformed anchors are correctly detected
# ---------------------------------------------------------------------------

def test_missing_schema_file_is_detected(tmp_path):
    """Verify that absence of a schema file is correctly flagged."""
    missing = str(tmp_path / "nonexistent.schema.json")
    assert not os.path.isfile(missing), "File should not exist for this negative test"


def test_malformed_json_schema_raises(tmp_path):
    """Verify that a malformed JSON schema file raises a parse error."""
    bad_file = tmp_path / "bad.schema.json"
    bad_file.write_text("{ this is not valid json }", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        with open(str(bad_file), "r", encoding="utf-8") as f:
            json.load(f)


def test_malformed_yaml_config_raises(tmp_path):
    """Verify that a malformed YAML config file raises a parse error."""
    bad_file = tmp_path / "bad.config.yaml"
    bad_file.write_text(
        textwrap.dedent("""\
            key: [unclosed bracket
            another: value
        """),
        encoding="utf-8",
    )
    with pytest.raises(yaml.YAMLError):
        with open(str(bad_file), "r", encoding="utf-8") as f:
            yaml.safe_load(f)


def test_schema_missing_required_field_is_detected(tmp_path):
    """Verify that a schema file without a 'required' declaration is flagged."""
    incomplete = tmp_path / "incomplete.schema.json"
    incomplete.write_text(
        json.dumps({"schema_version": "1.0.0", "type": "object"}),
        encoding="utf-8",
    )
    with open(str(incomplete), "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "required" not in data


def test_config_missing_schema_version_is_detected(tmp_path):
    """Verify that a config file without a 'schema_version' key is flagged."""
    incomplete = tmp_path / "incomplete.config.yaml"
    incomplete.write_text("horoji:\n  version: '1.0.0'\n", encoding="utf-8")
    with open(str(incomplete), "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert "schema_version" not in data
