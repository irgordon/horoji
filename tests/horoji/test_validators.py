"""
Validator tests for Horoji Phase 4 (TASK_04).
"""

import os
import shutil
import subprocess
import sys

import pytest
import yaml

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
VALIDATORS_DIR = os.path.join(REPO_ROOT, "tools", "horoji", "validators")

REQUIRED_VALIDATORS = [
    "validate-contracts",
    "validate-invariants",
    "validate-ownership",
    "validate-provenance",
    "validate-scheduler_non_blocking",
    "validate-all",
]


def validator_path(name: str) -> str:
    return os.path.join(VALIDATORS_DIR, name)


def run_validator(name: str, *, repo_root: str | None = None, extra_args: list[str] | None = None) -> subprocess.CompletedProcess:
    args = [sys.executable, validator_path(name)]
    if repo_root is not None:
        args.extend(["--repo-root", repo_root])
    if extra_args:
        args.extend(extra_args)
    return subprocess.run(args, capture_output=True, text=True)


def parse_yaml_output(raw: str) -> dict:
    data = yaml.safe_load(raw)
    assert isinstance(data, dict), f"Expected mapping YAML output, got: {raw}"
    return data


def make_temp_repo(tmp_path) -> str:
    repo = tmp_path / "repo"
    repo.mkdir()
    shutil.copytree(os.path.join(REPO_ROOT, ".project_memory"), repo / ".project_memory")
    tools_horoji = repo / "tools" / "horoji"
    tools_horoji.mkdir(parents=True, exist_ok=True)
    return str(repo)


@pytest.mark.parametrize("name", REQUIRED_VALIDATORS)
def test_validator_entrypoint_exists(name):
    assert os.path.isfile(validator_path(name)), f"Missing validator script: {name}"


@pytest.mark.parametrize("name", REQUIRED_VALIDATORS)
def test_validator_entrypoint_is_readable(name):
    assert os.access(validator_path(name), os.R_OK), f"Validator script not readable: {name}"


@pytest.mark.parametrize(
    "name",
    [
        "validate-contracts",
        "validate-invariants",
        "validate-ownership",
        "validate-provenance",
        "validate-scheduler_non_blocking",
    ],
)
def test_validator_succeeds_on_valid_repository_state(name):
    result = run_validator(name)
    assert result.returncode == 0, f"{name} failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    data = parse_yaml_output(result.stdout)
    assert data["validator"] == name
    assert data["status"] == "PASS"


def test_validate_all_succeeds_and_aggregates_results():
    result = run_validator("validate-all")
    assert result.returncode == 0, f"validate-all failed:\n{result.stdout}\n{result.stderr}"
    data = parse_yaml_output(result.stdout)
    assert data["validator"] == "validate-all"
    assert data["status"] == "PASS"
    assert data["reason"] == "all_validators_passed"
    results = data.get("results")
    assert isinstance(results, list) and len(results) == 5
    expected_order = [
        "validate-contracts",
        "validate-invariants",
        "validate-ownership",
        "validate-provenance",
        "validate-scheduler_non_blocking",
    ]
    assert [item.get("validator") for item in results] == expected_order


def test_validate_all_output_is_deterministic():
    first = run_validator("validate-all")
    second = run_validator("validate-all")
    assert first.returncode == 0 and second.returncode == 0
    assert parse_yaml_output(first.stdout) == parse_yaml_output(second.stdout)


def test_validate_contracts_fails_on_malformed_contract_artifact(tmp_path):
    repo = make_temp_repo(tmp_path)
    bad_contract = os.path.join(repo, ".project_memory", "authoritative", "contracts", "bad.yaml")
    with open(bad_contract, "w", encoding="utf-8") as fh:
        fh.write("subsystem: [unclosed\n")

    result = run_validator("validate-contracts", repo_root=repo)
    assert result.returncode != 0
    data = parse_yaml_output(result.stdout)
    assert data["status"] == "ERROR"
    assert data["reason"] == "parse_error"


def test_validate_contracts_fails_on_overlapping_allowed_and_forbidden(tmp_path):
    repo = make_temp_repo(tmp_path)
    contract_file = os.path.join(
        repo,
        ".project_memory",
        "authoritative",
        "contracts",
        "horoji_validators.yaml",
    )
    with open(contract_file, "r", encoding="utf-8") as fh:
        contract = yaml.safe_load(fh)
    contract["allowed_dependencies"] = ["network"]
    contract["forbidden_dependencies"] = ["network"]
    with open(contract_file, "w", encoding="utf-8") as fh:
        yaml.safe_dump(contract, fh, sort_keys=False)

    result = run_validator("validate-contracts", repo_root=repo)
    assert result.returncode != 0
    data = parse_yaml_output(result.stdout)
    assert data["status"] == "FAIL"
    assert data["reason"] == "dependency_sets_not_disjoint"


def test_validate_invariants_fails_on_malformed_invariant_artifact(tmp_path):
    repo = make_temp_repo(tmp_path)
    bad_invariant = os.path.join(repo, ".project_memory", "authoritative", "invariants", "bad.yaml")
    with open(bad_invariant, "w", encoding="utf-8") as fh:
        fh.write("id: bad\nenforcement: {broken\n")

    result = run_validator("validate-invariants", repo_root=repo)
    assert result.returncode != 0
    data = parse_yaml_output(result.stdout)
    assert data["status"] == "ERROR"
    assert data["reason"] == "parse_error"


def test_validate_invariants_fails_on_duplicate_invariant_ids(tmp_path):
    repo = make_temp_repo(tmp_path)
    duplicate = os.path.join(repo, ".project_memory", "authoritative", "invariants", "duplicate.yaml")
    with open(
        os.path.join(repo, ".project_memory", "authoritative", "invariants", "validators_no_network.yaml"),
        "r",
        encoding="utf-8",
    ) as fh:
        base = yaml.safe_load(fh)
    with open(duplicate, "w", encoding="utf-8") as fh:
        yaml.safe_dump(base, fh, sort_keys=False)

    result = run_validator("validate-invariants", repo_root=repo)
    assert result.returncode != 0
    data = parse_yaml_output(result.stdout)
    assert data["status"] == "FAIL"
    assert data["reason"] == "duplicate_invariant_id"


def test_validate_ownership_fails_on_malformed_ownership_artifact(tmp_path):
    repo = make_temp_repo(tmp_path)
    bad_owner = os.path.join(repo, ".project_memory", "authoritative", "ownership", "bad.yaml")
    with open(bad_owner, "w", encoding="utf-8") as fh:
        fh.write("pattern: tools/**\nowner: [broken\n")

    result = run_validator("validate-ownership", repo_root=repo)
    assert result.returncode != 0
    data = parse_yaml_output(result.stdout)
    assert data["status"] == "ERROR"
    assert data["reason"] == "parse_error"


def test_validate_ownership_fails_on_overlapping_conflicting_ownership(tmp_path):
    repo = make_temp_repo(tmp_path)
    overlap = os.path.join(repo, ".project_memory", "authoritative", "ownership", "conflict.yaml")
    with open(overlap, "w", encoding="utf-8") as fh:
        yaml.safe_dump(
            {
                "schema_version": "1.0.0",
                "pattern": "tools/horoji/**",
                "owner": "horoji_memory",
                "review_required": ["horoji_governance"],
            },
            fh,
            sort_keys=False,
        )

    result = run_validator("validate-ownership", repo_root=repo)
    assert result.returncode != 0
    data = parse_yaml_output(result.stdout)
    assert data["status"] == "FAIL"
    assert data["reason"] == "overlapping_ownership_conflict"


def test_validate_provenance_fails_on_missing_provenance(tmp_path):
    repo = make_temp_repo(tmp_path)
    artifact = os.path.join(repo, ".project_memory", "derived", "callgraphs", "horoji_cli.yaml")
    with open(artifact, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    data.pop("provenance", None)
    with open(artifact, "w", encoding="utf-8") as fh:
        yaml.safe_dump(data, fh, sort_keys=False)

    result = run_validator("validate-provenance", repo_root=repo)
    assert result.returncode != 0
    out = parse_yaml_output(result.stdout)
    assert out["status"] == "FAIL"
    assert out["reason"] == "missing_provenance"


def test_validate_scheduler_non_blocking_fails_on_forbidden_call(tmp_path):
    repo = make_temp_repo(tmp_path)
    scheduler_file = os.path.join(repo, "tools", "horoji", "validators", "scheduler_surface.py")
    os.makedirs(os.path.dirname(scheduler_file), exist_ok=True)
    with open(scheduler_file, "w", encoding="utf-8") as fh:
        fh.write("def run():\n    sleep()\n")

    result = run_validator("validate-scheduler_non_blocking", repo_root=repo)
    assert result.returncode != 0
    out = parse_yaml_output(result.stdout)
    assert out["status"] == "FAIL"
    assert out["reason"] == "blocking_call_detected"
    assert out["target"].endswith("scheduler_surface.py")


def test_validator_output_shape_is_machine_readable():
    result = run_validator("validate-contracts")
    assert result.returncode == 0
    out = parse_yaml_output(result.stdout)
    assert set(["validator", "status", "target", "reason", "details"]).issubset(out.keys())
