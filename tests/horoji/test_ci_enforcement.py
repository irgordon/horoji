"""
CI enforcement tests for Horoji Phase 5 (TASK_05).
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
WORKFLOW_FILE = os.path.join(REPO_ROOT, ".github", "workflows", "horoji-ci.yml")
CLI_CHECK = os.path.join(REPO_ROOT, "tools", "horoji", "cli", "horoji-check")

EXPECTED_STAGE_ORDER = [
    "bootstrap_presence",
    "bootstrap_parseability",
    "changed_files",
    "invalidation",
    "regeneration",
    "validate_authoritative",
    "validate_derived",
    "validate_repository_invariants",
    "stale_artifact_check",
    "result",
]


def _make_temp_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()

    shutil.copytree(Path(REPO_ROOT) / ".project_memory", repo / ".project_memory")
    shutil.copytree(Path(REPO_ROOT) / "tools", repo / "tools")
    return repo


def _run_ci_check(repo_root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            sys.executable,
            str(Path(repo_root) / "tools" / "horoji" / "cli" / "horoji-check"),
            "--repo-root",
            str(repo_root),
            *args,
        ],
        capture_output=True,
        text=True,
    )


def _parse_stage_docs(raw: str) -> list[dict]:
    docs = [doc for doc in yaml.safe_load_all(raw) if isinstance(doc, dict)]
    return docs


def test_ci_workflow_file_exists_and_parses():
    assert os.path.isfile(WORKFLOW_FILE), "Missing CI workflow for TASK_05"
    with open(WORKFLOW_FILE, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    assert isinstance(data, dict)
    assert "on" in data
    assert "pull_request" in data["on"]


def test_canonical_ci_entrypoint_exists_and_is_readable():
    assert os.path.isfile(CLI_CHECK), "Missing canonical CI entrypoint"
    assert os.access(CLI_CHECK, os.R_OK), "Canonical CI entrypoint is not readable"


def test_ci_stage_order_is_stable_for_success_path(tmp_path):
    repo = _make_temp_repo(tmp_path)
    result = _run_ci_check(repo, "--changed-file", "include/scheduler.h", "--derived-policy", "non_committed")
    assert result.returncode == 0, result.stdout + "\n" + result.stderr

    docs = _parse_stage_docs(result.stdout)
    stages = [doc.get("stage") for doc in docs]
    assert stages == EXPECTED_STAGE_ORDER


def test_missing_schema_anchor_fails_bootstrap_checks(tmp_path):
    repo = _make_temp_repo(tmp_path)
    target = repo / ".project_memory" / "schemas" / "contract.schema.json"
    target.unlink()

    result = _run_ci_check(repo, "--changed-file", "include/scheduler.h")
    assert result.returncode != 0

    docs = _parse_stage_docs(result.stdout)
    assert docs[0]["stage"] == "bootstrap_presence"
    assert docs[0]["status"] == "FAIL"
    assert docs[0]["reason"] == "missing_bootstrap_anchor"


def test_malformed_config_anchor_fails_parseability_checks(tmp_path):
    repo = _make_temp_repo(tmp_path)
    config = repo / ".project_memory" / "config" / "horoji.config.yaml"
    config.write_text("schema_version: [broken\n", encoding="utf-8")

    result = _run_ci_check(repo, "--changed-file", "include/scheduler.h")
    assert result.returncode != 0

    docs = _parse_stage_docs(result.stdout)
    stages = [doc["stage"] for doc in docs]
    assert "bootstrap_parseability" in stages
    parse_doc = next(doc for doc in docs if doc["stage"] == "bootstrap_parseability")
    assert parse_doc["status"] == "FAIL"
    assert parse_doc["reason"] == "malformed_bootstrap_anchor"


def test_invalidation_output_is_consumed_for_scope(tmp_path):
    repo = _make_temp_repo(tmp_path)
    result = _run_ci_check(repo, "--changed-file", "core/scheduler/runqueue.c", "--derived-policy", "non_committed")
    assert result.returncode == 0

    docs = _parse_stage_docs(result.stdout)
    invalidation = next(doc for doc in docs if doc["stage"] == "invalidation")
    assert "affected_artifacts=impact_sets" in invalidation.get("details", [])


def test_regeneration_invoked_when_required(tmp_path):
    repo = _make_temp_repo(tmp_path)
    result = _run_ci_check(repo, "--changed-file", "include/scheduler.h", "--derived-policy", "non_committed")
    assert result.returncode == 0

    docs = _parse_stage_docs(result.stdout)
    regen = next(doc for doc in docs if doc["stage"] == "regeneration")
    details = regen.get("details", [])
    assert "horoji-callgraph" in details
    assert "horoji-deps" in details
    assert "horoji-impact" in details


def test_validators_run_after_regeneration(tmp_path):
    repo = _make_temp_repo(tmp_path)
    result = _run_ci_check(repo, "--changed-file", "include/scheduler.h", "--derived-policy", "non_committed")
    assert result.returncode == 0

    docs = _parse_stage_docs(result.stdout)
    stages = [doc["stage"] for doc in docs]
    assert stages.index("regeneration") < stages.index("validate_authoritative")
    assert stages.index("regeneration") < stages.index("validate_derived")


def test_stale_derived_artifact_detection_fails_when_committed_policy_enabled(tmp_path):
    repo = _make_temp_repo(tmp_path)
    (repo / ".project_memory" / "derived" / "impact_sets" / "README_md.yaml").unlink()

    result = _run_ci_check(repo, "--changed-file", "README.md", "--derived-policy", "committed")
    assert result.returncode != 0

    docs = _parse_stage_docs(result.stdout)
    stale = next(doc for doc in docs if doc["stage"] == "stale_artifact_check")
    assert stale["status"] == "FAIL"
    assert stale["reason"] == "stale_derived_artifacts_detected"


def test_deterministic_logical_outcomes_for_repeated_runs(tmp_path):
    repo = _make_temp_repo(tmp_path)

    first = _run_ci_check(repo, "--changed-file", "include/scheduler.h", "--derived-policy", "non_committed")
    second = _run_ci_check(repo, "--changed-file", "include/scheduler.h", "--derived-policy", "non_committed")

    assert first.returncode == 0 and second.returncode == 0

    first_docs = _parse_stage_docs(first.stdout)
    second_docs = _parse_stage_docs(second.stdout)

    def normalize(docs: list[dict]) -> list[dict]:
        normalized = []
        for doc in docs:
            copy = dict(doc)
            details = []
            for item in copy.get("details", []):
                if isinstance(item, str) and item.startswith(("M .project_memory/", " D .project_memory/")):
                    continue
                details.append(item)
            copy["details"] = details
            normalized.append(copy)
        return normalized

    assert normalize(first_docs) == normalize(second_docs)


def test_missing_canonical_entrypoint_fails(tmp_path):
    repo = _make_temp_repo(tmp_path)
    entrypoint = repo / "tools" / "horoji" / "cli" / "horoji-check"
    entrypoint.unlink()

    result = subprocess.run([sys.executable, str(entrypoint)], capture_output=True, text=True)
    assert result.returncode != 0


def test_stage_order_violation_detection(tmp_path):
    repo = _make_temp_repo(tmp_path)
    result = _run_ci_check(repo, "--changed-file", "include/scheduler.h", "--derived-policy", "non_committed")
    assert result.returncode == 0

    docs = _parse_stage_docs(result.stdout)
    stages = [doc["stage"] for doc in docs]
    assert stages == EXPECTED_STAGE_ORDER
    assert stages != list(reversed(EXPECTED_STAGE_ORDER))
