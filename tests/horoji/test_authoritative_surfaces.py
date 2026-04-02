"""
Authoritative surface tests for Horoji Phase 1 (TASK_01).

Verifies:
- Existence of at least one contract, invariant, ownership map, and architecture
  manifest file in the authoritative directories
- Manual schema validation: required fields exist and have correct types
- Negative cases: malformed authoritative metadata is correctly rejected
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


def memory_path(*parts: str) -> str:
    return os.path.join(MEMORY_ROOT, *parts)


def load_schema(name: str) -> dict:
    with open(memory_path("schemas", name), "r", encoding="utf-8") as f:
        return json.load(f)


def yaml_files_in(directory: str) -> list[str]:
    """Return all .yaml files in a directory (non-recursive)."""
    if not os.path.isdir(directory):
        return []
    return sorted(
        os.path.join(directory, fname)
        for fname in os.listdir(directory)
        if fname.endswith(".yaml")
    )


def validate_against_schema(data: dict, schema: dict) -> list[str]:
    """
    Minimal manual schema validation.

    Returns a list of error strings; an empty list means validation passed.
    Checks:
    - All required fields are present
    - String fields contain strings
    - Array fields contain lists (and items are strings where applicable)
    - Object fields contain dicts
    """
    errors = []
    required = schema.get("required", [])
    properties = schema.get("properties", {})

    for field in required:
        if field not in data:
            errors.append(f"Missing required field: '{field}'")

    for field, prop_schema in properties.items():
        if field not in data:
            continue
        value = data[field]
        expected_type = prop_schema.get("type")
        if expected_type == "string" and not isinstance(value, str):
            errors.append(f"Field '{field}' must be a string, got {type(value).__name__}")
        elif expected_type == "array":
            if not isinstance(value, list):
                errors.append(
                    f"Field '{field}' must be an array, got {type(value).__name__}"
                )
            else:
                item_schema = prop_schema.get("items", {})
                if item_schema.get("type") == "string":
                    for i, item in enumerate(value):
                        if not isinstance(item, str):
                            errors.append(
                                f"Field '{field}[{i}]' must be a string, "
                                f"got {type(item).__name__}"
                            )
        elif expected_type == "object" and not isinstance(value, dict):
            errors.append(
                f"Field '{field}' must be an object, got {type(value).__name__}"
            )

    return errors


# ---------------------------------------------------------------------------
# 1. Authoritative artifact existence
# ---------------------------------------------------------------------------

CONTRACTS_DIR = memory_path("authoritative", "contracts")
INVARIANTS_DIR = memory_path("authoritative", "invariants")
OWNERSHIP_DIR = memory_path("authoritative", "ownership")
MANIFEST_DIR = memory_path("authoritative", "architecture_manifest")


def test_at_least_one_contract_exists():
    contracts = yaml_files_in(CONTRACTS_DIR)
    assert len(contracts) >= 1, (
        f"Expected at least one contract .yaml file in {CONTRACTS_DIR}, found none"
    )


def test_at_least_one_invariant_exists():
    invariants = yaml_files_in(INVARIANTS_DIR)
    assert len(invariants) >= 1, (
        f"Expected at least one invariant .yaml file in {INVARIANTS_DIR}, found none"
    )


def test_at_least_one_ownership_map_exists():
    ownership_maps = yaml_files_in(OWNERSHIP_DIR)
    assert len(ownership_maps) >= 1, (
        f"Expected at least one ownership .yaml file in {OWNERSHIP_DIR}, found none"
    )


def test_architecture_manifest_exists():
    manifests = yaml_files_in(MANIFEST_DIR)
    assert len(manifests) >= 1, (
        f"Expected at least one architecture manifest .yaml file in {MANIFEST_DIR}, "
        f"found none"
    )


# ---------------------------------------------------------------------------
# 2. Contract schema validation
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def contract_schema() -> dict:
    return load_schema("contract.schema.json")


@pytest.fixture(scope="module")
def invariant_schema() -> dict:
    return load_schema("invariant.schema.json")


@pytest.fixture(scope="module")
def ownership_schema() -> dict:
    return load_schema("ownership.schema.json")


@pytest.mark.parametrize("contract_file", yaml_files_in(CONTRACTS_DIR))
def test_contract_parses_as_valid_yaml(contract_file):
    with open(contract_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict), (
        f"Contract file did not parse to a dict: {contract_file}"
    )


@pytest.mark.parametrize("contract_file", yaml_files_in(CONTRACTS_DIR))
def test_contract_passes_schema_validation(contract_file, contract_schema):
    with open(contract_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    errors = validate_against_schema(data, contract_schema)
    assert errors == [], (
        f"Contract {contract_file} failed schema validation:\n"
        + "\n".join(f"  - {e}" for e in errors)
    )


@pytest.mark.parametrize("contract_file", yaml_files_in(CONTRACTS_DIR))
def test_contract_has_at_least_one_export(contract_file):
    with open(contract_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    exports = data.get("exports", [])
    assert isinstance(exports, list) and len(exports) >= 1, (
        f"Contract {contract_file} must define at least one exported surface"
    )


@pytest.mark.parametrize("contract_file", yaml_files_in(CONTRACTS_DIR))
def test_contract_has_explicit_owner(contract_file):
    with open(contract_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert data.get("owner"), (
        f"Contract {contract_file} must define a non-empty 'owner' field"
    )


# ---------------------------------------------------------------------------
# 3. Invariant schema validation
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("invariant_file", yaml_files_in(INVARIANTS_DIR))
def test_invariant_parses_as_valid_yaml(invariant_file):
    with open(invariant_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict), (
        f"Invariant file did not parse to a dict: {invariant_file}"
    )


@pytest.mark.parametrize("invariant_file", yaml_files_in(INVARIANTS_DIR))
def test_invariant_passes_schema_validation(invariant_file, invariant_schema):
    with open(invariant_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    errors = validate_against_schema(data, invariant_schema)
    assert errors == [], (
        f"Invariant {invariant_file} failed schema validation:\n"
        + "\n".join(f"  - {e}" for e in errors)
    )


@pytest.mark.parametrize("invariant_file", yaml_files_in(INVARIANTS_DIR))
def test_invariant_enforcement_is_a_dict(invariant_file):
    with open(invariant_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    enforcement = data.get("enforcement")
    assert isinstance(enforcement, dict), (
        f"Invariant {invariant_file}: 'enforcement' must be a dict"
    )


# ---------------------------------------------------------------------------
# 4. Ownership schema validation
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("ownership_file", yaml_files_in(OWNERSHIP_DIR))
def test_ownership_parses_as_valid_yaml(ownership_file):
    with open(ownership_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict), (
        f"Ownership file did not parse to a dict: {ownership_file}"
    )


@pytest.mark.parametrize("ownership_file", yaml_files_in(OWNERSHIP_DIR))
def test_ownership_passes_schema_validation(ownership_file, ownership_schema):
    with open(ownership_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    errors = validate_against_schema(data, ownership_schema)
    assert errors == [], (
        f"Ownership {ownership_file} failed schema validation:\n"
        + "\n".join(f"  - {e}" for e in errors)
    )


@pytest.mark.parametrize("ownership_file", yaml_files_in(OWNERSHIP_DIR))
def test_ownership_has_explicit_owner(ownership_file):
    with open(ownership_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert data.get("owner"), (
        f"Ownership {ownership_file} must define a non-empty 'owner' field"
    )


# ---------------------------------------------------------------------------
# 5. Architecture manifest validation
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("manifest_file", yaml_files_in(MANIFEST_DIR))
def test_manifest_parses_as_valid_yaml(manifest_file):
    with open(manifest_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict), (
        f"Architecture manifest did not parse to a dict: {manifest_file}"
    )


@pytest.mark.parametrize("manifest_file", yaml_files_in(MANIFEST_DIR))
def test_manifest_has_schema_version(manifest_file):
    with open(manifest_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert "schema_version" in data, (
        f"Architecture manifest {manifest_file} is missing 'schema_version'"
    )


@pytest.mark.parametrize("manifest_file", yaml_files_in(MANIFEST_DIR))
def test_manifest_has_subsystems(manifest_file):
    with open(manifest_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    subsystems = data.get("subsystems")
    assert isinstance(subsystems, dict) and len(subsystems) >= 1, (
        f"Architecture manifest {manifest_file} must declare at least one subsystem"
    )


@pytest.mark.parametrize("manifest_file", yaml_files_in(MANIFEST_DIR))
def test_manifest_subsystem_entries_are_dicts(manifest_file):
    with open(manifest_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    subsystems = data.get("subsystems", {})
    for name, entry in subsystems.items():
        assert isinstance(entry, dict), (
            f"Architecture manifest {manifest_file}: subsystem '{name}' entry must be a dict"
        )


# ---------------------------------------------------------------------------
# 6. Negative tests — malformed metadata is correctly rejected
# ---------------------------------------------------------------------------

def test_contract_missing_required_field_fails_validation(contract_schema):
    """A contract lacking a required field must fail schema validation."""
    incomplete = {
        "schema_version": "1.0.0",
        "subsystem": "test_subsystem",
        # 'exports', 'allowed_dependencies', 'forbidden_dependencies', 'owner' missing
    }
    errors = validate_against_schema(incomplete, contract_schema)
    assert len(errors) > 0, (
        "Expected schema validation to fail for a contract missing required fields"
    )


def test_contract_wrong_type_for_exports_fails_validation(contract_schema):
    """A contract with a non-list 'exports' field must fail schema validation."""
    bad_contract = {
        "schema_version": "1.0.0",
        "subsystem": "test_subsystem",
        "exports": "not_a_list",
        "allowed_dependencies": [],
        "forbidden_dependencies": [],
        "owner": "test_owner",
    }
    errors = validate_against_schema(bad_contract, contract_schema)
    assert len(errors) > 0, (
        "Expected schema validation to fail when 'exports' is not a list"
    )


def test_invariant_missing_required_field_fails_validation(invariant_schema):
    """An invariant lacking required fields must fail schema validation."""
    incomplete = {
        "schema_version": "1.0.0",
        "id": "test_invariant",
        # 'subsystem', 'description', 'enforcement' missing
    }
    errors = validate_against_schema(incomplete, invariant_schema)
    assert len(errors) > 0, (
        "Expected schema validation to fail for an invariant missing required fields"
    )


def test_ownership_missing_required_field_fails_validation(ownership_schema):
    """An ownership mapping lacking required fields must fail schema validation."""
    incomplete = {
        "schema_version": "1.0.0",
        # 'pattern' and 'owner' missing
    }
    errors = validate_against_schema(incomplete, ownership_schema)
    assert len(errors) > 0, (
        "Expected schema validation to fail for an ownership map missing required fields"
    )


def test_malformed_contract_yaml_raises(tmp_path):
    """A syntactically invalid contract YAML file must raise a parse error."""
    bad_file = tmp_path / "bad_contract.yaml"
    bad_file.write_text(
        textwrap.dedent("""\
            subsystem: [unclosed bracket
            owner: test
        """),
        encoding="utf-8",
    )
    with pytest.raises(yaml.YAMLError):
        with open(str(bad_file), "r", encoding="utf-8") as f:
            yaml.safe_load(f)


def test_malformed_invariant_yaml_raises(tmp_path):
    """A syntactically invalid invariant YAML file must raise a parse error."""
    bad_file = tmp_path / "bad_invariant.yaml"
    bad_file.write_text(
        textwrap.dedent("""\
            id: test_invariant
            enforcement: {unclosed
        """),
        encoding="utf-8",
    )
    with pytest.raises(yaml.YAMLError):
        with open(str(bad_file), "r", encoding="utf-8") as f:
            yaml.safe_load(f)


def test_contract_non_dict_yaml_fails_type_check(tmp_path):
    """A contract file that is valid YAML but not a dict must be rejected."""
    bad_file = tmp_path / "list_contract.yaml"
    bad_file.write_text("- subsystem: test\n- owner: test\n", encoding="utf-8")
    with open(str(bad_file), "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert not isinstance(data, dict), "Sanity: parsed data should be a list, not a dict"


def test_ownership_non_dict_yaml_fails_type_check(tmp_path):
    """An ownership file that is valid YAML but a scalar must be rejected."""
    bad_file = tmp_path / "scalar_ownership.yaml"
    bad_file.write_text("just a string value\n", encoding="utf-8")
    with open(str(bad_file), "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert not isinstance(data, dict), (
        "Sanity: parsed data should be a scalar, not a dict"
    )
