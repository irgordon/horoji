"""Clean-clone installability and entrypoint smoke tests."""

from __future__ import annotations

import os
import subprocess
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PUBLIC_CLI = os.path.join(REPO_ROOT, "tools", "horoji", "cli", "horoji")
HOROJI_CHECK = os.path.join(REPO_ROOT, "tools", "horoji", "cli", "horoji-check")
VALIDATE_ALL = os.path.join(REPO_ROOT, "tools", "horoji", "validators", "validate-all")

PUBLIC_COMMANDS = [
    "get-contract",
    "get-invariants",
    "get-owner",
    "get-impact-set",
    "get-context",
    "validate",
    "log-agent-execution",
]


def run_entrypoint(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *args],
        capture_output=True,
        text=True,
    )


def test_public_cli_help_documents_current_command_surface():
    result = run_entrypoint(PUBLIC_CLI, "--help")

    assert result.returncode == 0
    for command in PUBLIC_COMMANDS:
        assert command in result.stdout
    assert "regenerate" not in result.stdout
    assert "invalidate" not in result.stdout
    assert "Public commands are intentionally small" in result.stdout


def test_public_cli_query_help_is_available():
    result = run_entrypoint(PUBLIC_CLI, "--repo-root", REPO_ROOT, "get-context", "--help")

    assert result.returncode == 0
    assert "subsystem" in result.stdout
    assert "Authoritative records remain" in result.stdout
    assert "derived projections" in result.stdout


def test_documented_public_query_examples_succeed():
    examples = [
        ("get-contract", "horoji_cli"),
        ("get-context", "horoji_cli"),
        ("get-owner", "tools/horoji/cli/horoji"),
    ]

    for command, value in examples:
        result = run_entrypoint(PUBLIC_CLI, "--repo-root", REPO_ROOT, command, value)
        assert result.returncode == 0, result.stdout + result.stderr


def test_public_cli_rejects_unsupported_command_clearly():
    result = run_entrypoint(PUBLIC_CLI, "--repo-root", REPO_ROOT, "regenerate")

    assert result.returncode != 0
    assert "invalid choice" in result.stderr


def test_public_cli_rejects_invalid_repo_root_clearly(tmp_path):
    result = run_entrypoint(PUBLIC_CLI, "--repo-root", str(tmp_path), "get-contract", "horoji_cli")

    assert result.returncode != 0
    assert "invalid_repo_root" in result.stderr
    assert ".project_memory" in result.stderr


def test_horoji_check_help_is_available():
    result = run_entrypoint(HOROJI_CHECK, "--help")

    assert result.returncode == 0
    assert "--repo-root" in result.stdout
    assert "--derived-policy" in result.stdout
    assert "--auto-diff" in result.stdout
    assert "Derived artifact policy" in result.stdout


def test_horoji_check_rejects_invalid_derived_policy_clearly():
    result = run_entrypoint(
        HOROJI_CHECK,
        "--repo-root",
        REPO_ROOT,
        "--changed-file",
        "README.md",
        "--derived-policy",
        "invalid",
    )

    assert result.returncode != 0
    assert "invalid choice" in result.stderr
    assert "committed" in result.stderr
    assert "non_committed" in result.stderr


def test_validate_all_help_is_available():
    result = run_entrypoint(VALIDATE_ALL, "--help")

    assert result.returncode == 0
    assert "--repo-root" in result.stdout
