"""Public CLI output stability tests."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PUBLIC_CLI = os.path.join(REPO_ROOT, "tools", "horoji", "cli", "horoji")


def run_public_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, PUBLIC_CLI, "--repo-root", REPO_ROOT, *args],
        capture_output=True,
        text=True,
    )


def run_public_cli_with_repo(repo_root: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, PUBLIC_CLI, "--repo-root", repo_root, *args],
        capture_output=True,
        text=True,
    )


def load_stdout_yaml(result: subprocess.CompletedProcess) -> dict:
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    payload = yaml.safe_load(result.stdout)
    assert isinstance(payload, dict)
    return payload


def load_stderr_yaml(result: subprocess.CompletedProcess) -> dict:
    assert result.returncode != 0
    assert result.stdout == ""
    payload = yaml.safe_load(result.stderr)
    assert isinstance(payload, dict)
    return payload


def test_get_contract_output_shape_is_stable():
    payload = load_stdout_yaml(run_public_cli("get-contract", "horoji_cli"))

    assert sorted(payload) == ["contract", "found", "message", "subsystem"]
    assert payload["subsystem"] == "horoji_cli"
    assert payload["found"] is True
    assert payload["message"] == "contract found for subsystem: horoji_cli"
    assert sorted(payload["contract"]) == [
        "allowed_dependencies",
        "exports",
        "forbidden_dependencies",
        "owner",
        "schema_version",
        "subsystem",
    ]
    assert payload["contract"]["exports"] == [
        "get-contract",
        "get-invariants",
        "get-owner",
        "get-impact-set",
        "get-context",
        "validate",
        "log-agent-execution",
    ]


def test_get_owner_output_shape_is_stable():
    payload = load_stdout_yaml(run_public_cli("get-owner", "tools/horoji/cli/horoji"))

    assert sorted(payload) == ["file", "found", "matching_pattern", "message", "owner"]
    assert payload == {
        "file": "tools/horoji/cli/horoji",
        "found": True,
        "matching_pattern": "tools/horoji/cli/**",
        "message": "owner found for path: tools/horoji/cli/horoji",
        "owner": "horoji_cli",
    }


def test_get_context_output_shape_is_stable():
    payload = load_stdout_yaml(run_public_cli("get-context", "horoji_cli"))

    assert sorted(payload) == [
        "callgraph_slice",
        "contract",
        "history",
        "impact_set",
        "invariants",
        "ownership",
        "subsystem",
    ]
    assert payload["subsystem"] == "horoji_cli"
    assert isinstance(payload["contract"], dict)
    assert isinstance(payload["invariants"], list)
    assert isinstance(payload["ownership"], list)
    assert isinstance(payload["impact_set"], list)
    assert isinstance(payload["callgraph_slice"], dict)
    assert isinstance(payload["history"], list)


def test_unsupported_command_error_shape_is_stable():
    result = run_public_cli("regenerate")

    assert result.returncode == 2
    assert result.stdout == ""
    assert "invalid choice: 'regenerate'" in result.stderr
    assert "get-contract" in result.stderr
    assert "log-agent-execution" in result.stderr


def test_missing_query_results_are_repairable():
    contract = load_stdout_yaml(run_public_cli("get-contract", "unknown_subsystem"))
    owner = load_stdout_yaml(run_public_cli("get-owner", "unknown/path.py"))
    impact_set = load_stdout_yaml(run_public_cli("get-impact-set", "unknown/path.py"))

    assert contract["found"] is False
    assert contract["message"] == "no contract found for subsystem: unknown_subsystem"
    assert contract["contract"] == {}

    assert owner["found"] is False
    assert owner["message"] == "no owner found for path: unknown/path.py"
    assert owner["owner"] is None
    assert owner["matching_pattern"] is None

    assert impact_set["found"] is False
    assert impact_set["message"] == "no impact set found for path: unknown/path.py"
    assert impact_set["impact_set"] == {}


def test_invalid_repo_root_error_shape_is_stable(tmp_path: Path):
    result = run_public_cli_with_repo(str(tmp_path), "get-contract", "horoji_cli")
    payload = load_stderr_yaml(result)

    assert sorted(payload) == ["error"]
    assert payload["error"]["type"] == "invalid_repo_root"
    assert ".project_memory" in payload["error"]["message"]
    assert str(tmp_path) in payload["error"]["message"]
