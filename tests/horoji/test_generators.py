"""
Generator tests for Horoji Phase 2 (TASK_02).

Verifies:
- Generator scripts exist and are executable
- Generator execution succeeds on a valid repository state
- Generator outputs are deterministic (repeated runs produce identical logical content)
- Outputs include valid provenance metadata
- Outputs validate against their respective schemas
- Generators fail explicitly on malformed inputs
"""

import json
import os
import shutil
import subprocess
import sys
import textwrap

import pytest
import yaml

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MEMORY_ROOT = os.path.join(REPO_ROOT, ".project_memory")
GENERATORS_DIR = os.path.join(REPO_ROOT, "tools", "horoji", "generators")
DERIVED_CALLGRAPHS = os.path.join(MEMORY_ROOT, "derived", "callgraphs")
DERIVED_DEPS = os.path.join(MEMORY_ROOT, "derived", "dependencies")
DERIVED_IMPACT = os.path.join(MEMORY_ROOT, "derived", "impact_sets")


def memory_path(*parts: str) -> str:
    return os.path.join(MEMORY_ROOT, *parts)


def generator_path(name: str) -> str:
    return os.path.join(GENERATORS_DIR, name)


def load_schema(name: str) -> dict:
    path = memory_path("schemas", name)
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def validate_against_schema(data: dict, schema: dict) -> list[str]:
    """
    Minimal manual schema validation (mirrors test_authoritative_surfaces.py).

    Returns a list of error strings; an empty list means validation passed.
    """
    errors: list[str] = []
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
            errors.append(
                f"Field '{field}' must be a string, got {type(value).__name__}"
            )
        elif expected_type == "array":
            if not isinstance(value, list):
                errors.append(
                    f"Field '{field}' must be an array, got {type(value).__name__}"
                )
        elif expected_type == "object" and not isinstance(value, dict):
            errors.append(
                f"Field '{field}' must be an object, got {type(value).__name__}"
            )

    return errors


def run_generator(name: str, *extra_args: str) -> subprocess.CompletedProcess:
    """Run a generator script via the current Python interpreter."""
    script = generator_path(name)
    return subprocess.run(
        [sys.executable, script, *extra_args],
        capture_output=True,
        text=True,
    )


def yaml_files_in(directory: str) -> list[str]:
    """Return sorted list of .yaml files in directory (non-recursive)."""
    if not os.path.isdir(directory):
        return []
    return sorted(
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.endswith(".yaml")
    )


# ---------------------------------------------------------------------------
# 1. Generator entrypoints exist and are executable
# ---------------------------------------------------------------------------

REQUIRED_GENERATORS = ["horoji-callgraph", "horoji-deps", "horoji-impact"]


@pytest.mark.parametrize("name", REQUIRED_GENERATORS)
def test_generator_script_exists(name):
    assert os.path.isfile(generator_path(name)), (
        f"Required generator script is missing: {generator_path(name)}"
    )


@pytest.mark.parametrize("name", REQUIRED_GENERATORS)
def test_generator_script_is_readable(name):
    path = generator_path(name)
    assert os.access(path, os.R_OK), f"Generator script is not readable: {path}"


# ---------------------------------------------------------------------------
# 2. Derived artifact schemas exist
# ---------------------------------------------------------------------------

REQUIRED_DERIVED_SCHEMAS = [
    "callgraph.schema.json",
    "dependency.schema.json",
    "impact_set.schema.json",
]


@pytest.mark.parametrize("schema_name", REQUIRED_DERIVED_SCHEMAS)
def test_derived_schema_exists(schema_name):
    path = memory_path("schemas", schema_name)
    assert os.path.isfile(path), f"Derived artifact schema is missing: {path}"


@pytest.mark.parametrize("schema_name", REQUIRED_DERIVED_SCHEMAS)
def test_derived_schema_parses_as_valid_json(schema_name):
    schema = load_schema(schema_name)
    assert isinstance(schema, dict), (
        f"Schema did not parse to a dict: {schema_name}"
    )


@pytest.mark.parametrize("schema_name", REQUIRED_DERIVED_SCHEMAS)
def test_derived_schema_has_schema_version(schema_name):
    schema = load_schema(schema_name)
    assert "schema_version" in schema, (
        f"Schema missing 'schema_version': {schema_name}"
    )


@pytest.mark.parametrize("schema_name", REQUIRED_DERIVED_SCHEMAS)
def test_derived_schema_has_required_field(schema_name):
    schema = load_schema(schema_name)
    assert "required" in schema and isinstance(schema["required"], list), (
        f"Schema missing or invalid 'required' list: {schema_name}"
    )


# ---------------------------------------------------------------------------
# 3. Generator execution succeeds on valid repository state
# ---------------------------------------------------------------------------

def test_callgraph_generator_succeeds():
    result = run_generator("horoji-callgraph")
    assert result.returncode == 0, (
        f"horoji-callgraph exited non-zero.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    )


def test_deps_generator_succeeds():
    result = run_generator("horoji-deps")
    assert result.returncode == 0, (
        f"horoji-deps exited non-zero.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    )


def test_impact_generator_succeeds():
    result = run_generator(
        "horoji-impact", "--file", ".project_memory/config/horoji.config.yaml"
    )
    assert result.returncode == 0, (
        f"horoji-impact exited non-zero.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    )


# ---------------------------------------------------------------------------
# 4. Generator outputs are written to the derived subtree
# ---------------------------------------------------------------------------

def test_callgraph_outputs_exist_in_derived_dir():
    outputs = yaml_files_in(DERIVED_CALLGRAPHS)
    assert len(outputs) >= 1, (
        f"Expected at least one callgraph artifact in {DERIVED_CALLGRAPHS}"
    )


def test_deps_outputs_exist_in_derived_dir():
    outputs = yaml_files_in(DERIVED_DEPS)
    assert len(outputs) >= 1, (
        f"Expected at least one dependency artifact in {DERIVED_DEPS}"
    )


def test_impact_outputs_exist_in_derived_dir():
    outputs = yaml_files_in(DERIVED_IMPACT)
    assert len(outputs) >= 1, (
        f"Expected at least one impact_set artifact in {DERIVED_IMPACT}"
    )


# ---------------------------------------------------------------------------
# 5. Outputs include valid provenance metadata
# ---------------------------------------------------------------------------

PROVENANCE_REQUIRED_FIELDS = [
    "artifact_type",
    "trust_level",
    "generator",
    "schema_version",
    "input_commit",
    "generated_at",
]


@pytest.mark.parametrize("artifact_file", yaml_files_in(DERIVED_CALLGRAPHS))
def test_callgraph_artifact_has_provenance(artifact_file):
    with open(artifact_file, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    assert isinstance(data, dict), f"Callgraph artifact is not a dict: {artifact_file}"
    assert "provenance" in data, f"Callgraph artifact missing 'provenance': {artifact_file}"
    provenance = data["provenance"]
    assert isinstance(provenance, dict), (
        f"Provenance must be a mapping in: {artifact_file}"
    )
    for field in PROVENANCE_REQUIRED_FIELDS:
        assert field in provenance, (
            f"Provenance missing field '{field}' in: {artifact_file}"
        )


@pytest.mark.parametrize("artifact_file", yaml_files_in(DERIVED_DEPS))
def test_dependency_artifact_has_provenance(artifact_file):
    with open(artifact_file, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    assert isinstance(data, dict), f"Dependency artifact is not a dict: {artifact_file}"
    assert "provenance" in data, f"Dependency artifact missing 'provenance': {artifact_file}"
    provenance = data["provenance"]
    assert isinstance(provenance, dict), (
        f"Provenance must be a mapping in: {artifact_file}"
    )
    for field in PROVENANCE_REQUIRED_FIELDS:
        assert field in provenance, (
            f"Provenance missing field '{field}' in: {artifact_file}"
        )


@pytest.mark.parametrize("artifact_file", yaml_files_in(DERIVED_IMPACT))
def test_impact_artifact_has_provenance(artifact_file):
    with open(artifact_file, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    assert isinstance(data, dict), f"Impact artifact is not a dict: {artifact_file}"
    assert "provenance" in data, f"Impact artifact missing 'provenance': {artifact_file}"
    provenance = data["provenance"]
    assert isinstance(provenance, dict), (
        f"Provenance must be a mapping in: {artifact_file}"
    )
    for field in PROVENANCE_REQUIRED_FIELDS:
        assert field in provenance, (
            f"Provenance missing field '{field}' in: {artifact_file}"
        )


# ---------------------------------------------------------------------------
# 6. Outputs validate against their schemas
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def callgraph_schema() -> dict:
    return load_schema("callgraph.schema.json")


@pytest.fixture(scope="module")
def dependency_schema() -> dict:
    return load_schema("dependency.schema.json")


@pytest.fixture(scope="module")
def impact_set_schema() -> dict:
    return load_schema("impact_set.schema.json")


@pytest.mark.parametrize("artifact_file", yaml_files_in(DERIVED_CALLGRAPHS))
def test_callgraph_artifact_passes_schema_validation(artifact_file, callgraph_schema):
    with open(artifact_file, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    errors = validate_against_schema(data, callgraph_schema)
    assert errors == [], (
        f"Callgraph artifact {artifact_file} failed schema validation:\n"
        + "\n".join(f"  - {e}" for e in errors)
    )


@pytest.mark.parametrize("artifact_file", yaml_files_in(DERIVED_DEPS))
def test_dependency_artifact_passes_schema_validation(artifact_file, dependency_schema):
    with open(artifact_file, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    errors = validate_against_schema(data, dependency_schema)
    assert errors == [], (
        f"Dependency artifact {artifact_file} failed schema validation:\n"
        + "\n".join(f"  - {e}" for e in errors)
    )


@pytest.mark.parametrize("artifact_file", yaml_files_in(DERIVED_IMPACT))
def test_impact_artifact_passes_schema_validation(artifact_file, impact_set_schema):
    with open(artifact_file, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    errors = validate_against_schema(data, impact_set_schema)
    assert errors == [], (
        f"Impact artifact {artifact_file} failed schema validation:\n"
        + "\n".join(f"  - {e}" for e in errors)
    )


# ---------------------------------------------------------------------------
# 7. Provenance trust_level is "derived"
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("artifact_file", yaml_files_in(DERIVED_CALLGRAPHS))
def test_callgraph_provenance_trust_level_is_derived(artifact_file):
    with open(artifact_file, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    assert data["provenance"]["trust_level"] == "derived", (
        f"Callgraph provenance trust_level must be 'derived': {artifact_file}"
    )


@pytest.mark.parametrize("artifact_file", yaml_files_in(DERIVED_DEPS))
def test_dependency_provenance_trust_level_is_derived(artifact_file):
    with open(artifact_file, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    assert data["provenance"]["trust_level"] == "derived", (
        f"Dependency provenance trust_level must be 'derived': {artifact_file}"
    )


@pytest.mark.parametrize("artifact_file", yaml_files_in(DERIVED_IMPACT))
def test_impact_provenance_trust_level_is_derived(artifact_file):
    with open(artifact_file, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    assert data["provenance"]["trust_level"] == "derived", (
        f"Impact provenance trust_level must be 'derived': {artifact_file}"
    )


# ---------------------------------------------------------------------------
# 8. Outputs are deterministic (repeated execution produces identical logical content)
# ---------------------------------------------------------------------------

def _strip_timestamp(data: dict) -> dict:
    """Return a copy of artifact dict with generated_at removed (for logical comparison)."""
    result = dict(data)
    if "provenance" in result and isinstance(result["provenance"], dict):
        result["provenance"] = {
            k: v
            for k, v in result["provenance"].items()
            if k != "generated_at"
        }
    return result


def test_callgraph_generator_is_deterministic():
    """Running horoji-callgraph twice must produce logically identical outputs."""
    result1 = run_generator("horoji-callgraph")
    assert result1.returncode == 0, f"First run failed: {result1.stderr}"

    outputs_first = {}
    for fpath in yaml_files_in(DERIVED_CALLGRAPHS):
        with open(fpath, "r", encoding="utf-8") as fh:
            outputs_first[os.path.basename(fpath)] = _strip_timestamp(yaml.safe_load(fh))

    result2 = run_generator("horoji-callgraph")
    assert result2.returncode == 0, f"Second run failed: {result2.stderr}"

    outputs_second = {}
    for fpath in yaml_files_in(DERIVED_CALLGRAPHS):
        with open(fpath, "r", encoding="utf-8") as fh:
            outputs_second[os.path.basename(fpath)] = _strip_timestamp(yaml.safe_load(fh))

    assert outputs_first == outputs_second, (
        "horoji-callgraph produced different logical outputs on repeated execution"
    )


def test_deps_generator_is_deterministic():
    """Running horoji-deps twice must produce logically identical outputs."""
    result1 = run_generator("horoji-deps")
    assert result1.returncode == 0, f"First run failed: {result1.stderr}"

    outputs_first = {}
    for fpath in yaml_files_in(DERIVED_DEPS):
        with open(fpath, "r", encoding="utf-8") as fh:
            outputs_first[os.path.basename(fpath)] = _strip_timestamp(yaml.safe_load(fh))

    result2 = run_generator("horoji-deps")
    assert result2.returncode == 0, f"Second run failed: {result2.stderr}"

    outputs_second = {}
    for fpath in yaml_files_in(DERIVED_DEPS):
        with open(fpath, "r", encoding="utf-8") as fh:
            outputs_second[os.path.basename(fpath)] = _strip_timestamp(yaml.safe_load(fh))

    assert outputs_first == outputs_second, (
        "horoji-deps produced different logical outputs on repeated execution"
    )


def test_impact_generator_is_deterministic():
    """Running horoji-impact for the same file twice produces logically identical output."""
    file_path = ".project_memory/config/horoji.config.yaml"

    result1 = run_generator("horoji-impact", "--file", file_path)
    assert result1.returncode == 0, f"First run failed: {result1.stderr}"

    outputs_first = {}
    for fpath in yaml_files_in(DERIVED_IMPACT):
        with open(fpath, "r", encoding="utf-8") as fh:
            outputs_first[os.path.basename(fpath)] = _strip_timestamp(yaml.safe_load(fh))

    result2 = run_generator("horoji-impact", "--file", file_path)
    assert result2.returncode == 0, f"Second run failed: {result2.stderr}"

    outputs_second = {}
    for fpath in yaml_files_in(DERIVED_IMPACT):
        with open(fpath, "r", encoding="utf-8") as fh:
            outputs_second[os.path.basename(fpath)] = _strip_timestamp(yaml.safe_load(fh))

    assert outputs_first == outputs_second, (
        "horoji-impact produced different logical outputs on repeated execution"
    )


# ---------------------------------------------------------------------------
# 9. Generators fail explicitly on malformed inputs
# ---------------------------------------------------------------------------

def test_callgraph_fails_on_unknown_subsystem():
    """horoji-callgraph --subsystem nonexistent must exit non-zero."""
    result = run_generator("horoji-callgraph", "--subsystem", "nonexistent")
    assert result.returncode != 0, (
        "horoji-callgraph should fail for unknown subsystem but exited 0"
    )
    assert "ERROR" in result.stderr, (
        "horoji-callgraph must emit a structured error on stderr"
    )


def test_deps_fails_on_unknown_subsystem():
    """horoji-deps --subsystem nonexistent must exit non-zero."""
    result = run_generator("horoji-deps", "--subsystem", "nonexistent")
    assert result.returncode != 0, (
        "horoji-deps should fail for unknown subsystem but exited 0"
    )
    assert "ERROR" in result.stderr, (
        "horoji-deps must emit a structured error on stderr"
    )


def test_impact_fails_without_file_argument():
    """horoji-impact with no --file argument must exit non-zero."""
    result = run_generator("horoji-impact")
    assert result.returncode != 0, (
        "horoji-impact should fail when no --file argument is given but exited 0"
    )


def test_callgraph_fails_on_missing_config(tmp_path):
    """horoji-callgraph must exit non-zero when config file is absent."""
    # Run from a temp directory that mirrors the layout but lacks the config file.
    # We test this by patching the environment via monkeypatching the script's REPO_ROOT.
    # Instead: pass an env that points REPO_ROOT at tmp_path which has no config.
    # Simplest approach: directly invoke the generator module with a bad repo root.
    bad_script = tmp_path / "bad_callgraph.py"
    bad_script.write_text(
        textwrap.dedent(f"""\
            import sys, os
            sys.path.insert(0, {repr(str(REPO_ROOT))})
            # Override REPO_ROOT before importing generator logic
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "gen",
                {repr(generator_path("horoji-callgraph"))},
            )
            mod = importlib.util.load_from_spec(spec)
            spec.loader.exec_module(mod)
            mod.REPO_ROOT = {repr(str(tmp_path))}
            mod.MEMORY_ROOT = {repr(str(tmp_path / ".project_memory"))}
            mod.CONFIG_FILE = {repr(str(tmp_path / ".project_memory" / "config" / "horoji.config.yaml"))}
            mod.main()
        """),
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, str(bad_script)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0, (
        "Generator must exit non-zero when required config is missing"
    )


def test_callgraph_fails_on_malformed_manifest(tmp_path):
    """horoji-callgraph must exit non-zero when the manifest is malformed YAML."""
    # Build a minimal project_memory tree with a malformed manifest.
    pm = tmp_path / ".project_memory"
    (pm / "config").mkdir(parents=True)
    (pm / "authoritative" / "architecture_manifest").mkdir(parents=True)
    (pm / "derived" / "callgraphs").mkdir(parents=True)
    (pm / "schemas").mkdir(parents=True)

    # Valid config
    (pm / "config" / "horoji.config.yaml").write_text(
        "schema_version: '1.0.0'\nhoroji:\n  version: '1.0.0'\n",
        encoding="utf-8",
    )
    # Malformed manifest
    (pm / "authoritative" / "architecture_manifest" / "manifest.yaml").write_text(
        "subsystems: [unclosed bracket\n",
        encoding="utf-8",
    )
    # Copy the real schema
    real_schema = memory_path("schemas", "callgraph.schema.json")
    shutil.copy(real_schema, pm / "schemas" / "callgraph.schema.json")

    bad_script = tmp_path / "run_gen.py"
    bad_script.write_text(
        textwrap.dedent(f"""\
            import sys
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "gen",
                {repr(generator_path("horoji-callgraph"))},
            )
            mod = importlib.util.load_from_spec(spec)
            spec.loader.exec_module(mod)
            mod.REPO_ROOT = {repr(str(tmp_path))}
            mod.MEMORY_ROOT = {repr(str(pm))}
            mod.CONFIG_FILE = str({repr(str(pm))} + "/config/horoji.config.yaml")
            mod.MANIFEST_FILE = str({repr(str(pm))} + "/authoritative/architecture_manifest/manifest.yaml")
            mod.SCHEMA_FILE = str({repr(str(pm))} + "/schemas/callgraph.schema.json")
            mod.DERIVED_CALLGRAPHS = str({repr(str(pm))} + "/derived/callgraphs")
            mod.main()
        """),
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, str(bad_script)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0, (
        "horoji-callgraph must exit non-zero when manifest is malformed"
    )


# ---------------------------------------------------------------------------
# 10. Derived artifacts do not overwrite authoritative data
# ---------------------------------------------------------------------------

def test_derived_callgraph_not_in_authoritative_dir():
    auth_dirs = [
        memory_path("authoritative", "contracts"),
        memory_path("authoritative", "invariants"),
        memory_path("authoritative", "ownership"),
        memory_path("authoritative", "architecture_manifest"),
    ]
    for auth_dir in auth_dirs:
        for fname in os.listdir(auth_dir):
            if fname.endswith(".yaml"):
                # Ensure none of these came from a generator
                fpath = os.path.join(auth_dir, fname)
                with open(fpath, "r", encoding="utf-8") as fh:
                    data = yaml.safe_load(fh)
                if isinstance(data, dict) and "provenance" in data:
                    prov = data.get("provenance", {})
                    assert prov.get("trust_level") != "derived", (
                        f"Derived artifact found in authoritative directory: {fpath}"
                    )


def test_callgraph_outputs_only_in_derived_dir():
    """Callgraph artifacts must only live under derived/callgraphs."""
    auth_base = memory_path("authoritative")
    outputs = yaml_files_in(DERIVED_CALLGRAPHS)
    for out in outputs:
        assert not out.startswith(auth_base), (
            f"Callgraph artifact written into authoritative directory: {out}"
        )


# ---------------------------------------------------------------------------
# 11. Impact set correctness — known ownership rules
# ---------------------------------------------------------------------------

def test_impact_of_memory_file_includes_dependents():
    """
    A file owned by horoji_memory should impact horoji_memory plus all subsystems
    that declare depends_on: horoji_memory (i.e. the whole system per manifest).
    """
    result = run_generator(
        "horoji-impact",
        "--file",
        ".project_memory/authoritative/contracts/horoji_memory.yaml",
    )
    assert result.returncode == 0, f"horoji-impact failed: {result.stderr}"

    safe = "_project_memory_authoritative_contracts_horoji_memory_yaml.yaml"
    fpath = os.path.join(DERIVED_IMPACT, safe)
    assert os.path.isfile(fpath), f"Expected impact artifact not found: {fpath}"

    with open(fpath, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    impacted = data.get("impacted_subsystems", [])
    assert "horoji_memory" in impacted, (
        "horoji_memory must be in impacted_subsystems for its own file"
    )
    # All other subsystems depend on horoji_memory per the manifest
    for dep_subsystem in ["horoji_cli", "horoji_generators", "horoji_validators",
                          "horoji_invalidation"]:
        assert dep_subsystem in impacted, (
            f"Expected {dep_subsystem} in impacted_subsystems (depends on horoji_memory)"
        )


def test_impact_of_unknown_file_has_empty_impacted_subsystems():
    """A file with no ownership match produces an empty impacted_subsystems list."""
    result = run_generator(
        "horoji-impact",
        "--file",
        "README.md",
    )
    assert result.returncode == 0, f"horoji-impact failed: {result.stderr}"

    safe = "README_md.yaml"
    fpath = os.path.join(DERIVED_IMPACT, safe)
    assert os.path.isfile(fpath), f"Expected impact artifact not found: {fpath}"

    with open(fpath, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    impacted = data.get("impacted_subsystems", [])
    assert impacted == [], (
        f"File with no ownership match should produce empty impacted_subsystems, got {impacted}"
    )


# ---------------------------------------------------------------------------
# 12. Negative tests — schema validation detects malformed derived artifacts
# ---------------------------------------------------------------------------

def test_callgraph_schema_rejects_missing_provenance(callgraph_schema):
    incomplete = {
        "subsystem": "horoji_cli",
        "nodes": [],
        "edges": [],
    }
    errors = validate_against_schema(incomplete, callgraph_schema)
    assert len(errors) > 0, (
        "Expected schema validation to fail for callgraph missing 'provenance'"
    )


def test_dependency_schema_rejects_missing_depends_on(dependency_schema):
    incomplete = {
        "provenance": {
            "artifact_type": "dependency",
            "trust_level": "derived",
            "generator": "horoji-deps",
            "schema_version": "1.0.0",
            "input_commit": "abc",
            "generated_at": "2024-01-01T00:00:00Z",
        },
        "subsystem": "horoji_cli",
    }
    errors = validate_against_schema(incomplete, dependency_schema)
    assert len(errors) > 0, (
        "Expected schema validation to fail for dependency missing 'depends_on'"
    )


def test_impact_schema_rejects_missing_file(impact_set_schema):
    incomplete = {
        "provenance": {
            "artifact_type": "impact_set",
            "trust_level": "derived",
            "generator": "horoji-impact",
            "schema_version": "1.0.0",
            "input_commit": "abc",
            "generated_at": "2024-01-01T00:00:00Z",
        },
        "impacted_subsystems": [],
    }
    errors = validate_against_schema(incomplete, impact_set_schema)
    assert len(errors) > 0, (
        "Expected schema validation to fail for impact_set missing 'file'"
    )
