"""
Agent integration tests for Horoji Phase 6 (TASK_06).
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CLI = os.path.join(REPO_ROOT, "tools", "horoji", "cli", "horoji")
WORKFLOWS_DIR = os.path.join(REPO_ROOT, ".github", "workflows")
DOC_FILE = os.path.join(REPO_ROOT, "docs", "AGENT_INTEGRATION.md")

REQUIRED_WORKFLOWS = [
    "agent-modify-subsystem.yml",
    "agent-generate-change.yml",
    "agent-validate-change.yml",
]

REQUIRED_CONTEXT_FIELDS = [
    "subsystem",
    "contract",
    "invariants",
    "ownership",
    "impact_set",
    "callgraph_slice",
    "history",
]


def _run_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, CLI, "--repo-root", REPO_ROOT, *args],
        capture_output=True,
        text=True,
    )


def _read_workflow(name: str) -> dict:
    path = os.path.join(WORKFLOWS_DIR, name)
    with open(path, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    assert isinstance(data, dict)
    return data


def _workflow_steps(workflow: dict) -> list[dict]:
    jobs = workflow.get("jobs", {})
    assert isinstance(jobs, dict) and len(jobs) == 1
    (_, job), = jobs.items()
    steps = job.get("steps", [])
    assert isinstance(steps, list)
    return [step for step in steps if isinstance(step, dict)]


def test_cli_entrypoint_exists_and_readable():
    assert os.path.isfile(CLI), "Missing TASK_06 CLI entrypoint"
    assert os.access(CLI, os.R_OK), "TASK_06 CLI entrypoint is not readable"


def test_required_workflow_templates_exist_and_parse():
    for name in REQUIRED_WORKFLOWS:
        path = os.path.join(WORKFLOWS_DIR, name)
        assert os.path.isfile(path), f"Missing workflow template: {name}"
        data = _read_workflow(name)
        assert "on" in data
        assert "workflow_dispatch" in data["on"]


def test_get_contract_returns_structured_output():
    result = _run_cli("get-contract", "horoji_cli")
    assert result.returncode == 0, result.stderr
    payload = yaml.safe_load(result.stdout)
    assert isinstance(payload, dict)
    assert payload.get("subsystem") == "horoji_cli"
    assert isinstance(payload.get("contract"), dict)


def test_get_invariants_returns_structured_output():
    result = _run_cli("get-invariants", "horoji_validators")
    assert result.returncode == 0, result.stderr
    payload = yaml.safe_load(result.stdout)
    assert isinstance(payload, dict)
    assert payload.get("subsystem") == "horoji_validators"
    assert isinstance(payload.get("invariants"), list)


def test_get_owner_returns_structured_output():
    result = _run_cli("get-owner", "tools/horoji/cli/horoji")
    assert result.returncode == 0, result.stderr
    payload = yaml.safe_load(result.stdout)
    assert isinstance(payload, dict)
    assert payload.get("file") == "tools/horoji/cli/horoji"
    assert isinstance(payload.get("owner"), (str, type(None)))
    assert isinstance(payload.get("matching_pattern"), (str, type(None)))


def test_get_impact_set_returns_structured_output():
    result = _run_cli("get-impact-set", "README.md")
    assert result.returncode == 0, result.stderr
    payload = yaml.safe_load(result.stdout)
    assert isinstance(payload, dict)
    assert payload.get("file") == "README.md"
    assert isinstance(payload.get("impact_set"), dict)


def test_get_context_returns_required_stable_fields():
    result = _run_cli("get-context", "horoji_cli")
    assert result.returncode == 0, result.stderr
    payload = yaml.safe_load(result.stdout)
    assert isinstance(payload, dict)
    assert sorted(payload.keys()) == sorted(REQUIRED_CONTEXT_FIELDS)


def test_validate_command_returns_structured_output():
    result = _run_cli("validate")
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    payload = yaml.safe_load(result.stdout)
    assert isinstance(payload, dict)
    assert payload.get("validator") == "validate-all"
    assert payload.get("status") == "PASS"


def test_log_agent_execution_is_structured_and_deterministic():
    args = (
        "log-agent-execution",
        "--agent-name",
        "copilot",
        "--agent-version",
        "1.2.3",
        "--timestamp",
        "2026-01-01T00:00:00Z",
        "--subsystem",
        "horoji_cli",
        "--action",
        "validate_change",
        "--status",
        "SUCCESS",
        "--detail",
        "z_detail",
        "--detail",
        "a_detail",
        "--detail",
        "z_detail",
    )
    first = _run_cli(*args)
    second = _run_cli(*args)
    assert first.returncode == 0 and second.returncode == 0
    assert first.stdout == second.stdout

    payload = yaml.safe_load(first.stdout)
    assert payload["result"]["status"] == "SUCCESS"
    assert payload["result"]["details"] == ["a_detail", "z_detail"]


def test_log_agent_execution_fails_on_invalid_status():
    result = _run_cli(
        "log-agent-execution",
        "--agent-name",
        "copilot",
        "--agent-version",
        "1.2.3",
        "--timestamp",
        "2026-01-01T00:00:00Z",
        "--subsystem",
        "horoji_cli",
        "--action",
        "validate_change",
        "--status",
        "MAYBE",
    )
    assert result.returncode != 0
    payload = yaml.safe_load(result.stderr)
    assert payload["error"]["type"] == "input_error"


def test_missing_context_command_fails():
    result = subprocess.run(
        [sys.executable, CLI, "--repo-root", REPO_ROOT, "get-context"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0


def test_get_context_with_unknown_subsystem_has_stable_shape():
    result = _run_cli("get-context", "unknown_subsystem")
    assert result.returncode == 0, result.stderr
    payload = yaml.safe_load(result.stdout)
    assert isinstance(payload, dict)
    assert sorted(payload.keys()) == sorted(REQUIRED_CONTEXT_FIELDS)
    assert payload["subsystem"] == "unknown_subsystem"
    assert payload["contract"] == {}


def test_malformed_context_output_negative_case(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("context: [broken\n", encoding="utf-8")
    with open(str(bad), "r", encoding="utf-8") as fh:
        try:
            yaml.safe_load(fh)
            parsed_ok = True
        except yaml.YAMLError:
            parsed_ok = False
    assert parsed_ok is False


def test_workflow_templates_contain_required_sequence_steps():
    for name in REQUIRED_WORKFLOWS:
        workflow = _read_workflow(name)
        steps = _workflow_steps(workflow)
        names = [str(step.get("name", "")) for step in steps]
        assert any("Retrieve Horoji context" in n for n in names)
        assert any("Invoke external agent" in n for n in names)
        assert any("Validate proposed change" in n for n in names)
        assert any("Handle failure" in n for n in names)


def test_agent_workflows_run_validation_after_agent_invocation():
    for name in REQUIRED_WORKFLOWS:
        workflow = _read_workflow(name)
        steps = _workflow_steps(workflow)
        names = [str(step.get("name", "")) for step in steps]
        invoke_index = next(i for i, n in enumerate(names) if "Invoke external agent" in n)
        validate_index = next(i for i, n in enumerate(names) if "Validate proposed change" in n)
        assert validate_index > invoke_index


def test_agent_workflows_include_standard_horoji_ci_enforcement():
    for name in REQUIRED_WORKFLOWS:
        workflow = _read_workflow(name)
        steps = _workflow_steps(workflow)
        run_snippets = [str(step.get("run", "")) for step in steps]
        assert any("horoji-check" in run for run in run_snippets)


def test_agent_workflows_do_not_include_direct_git_push_or_commit():
    for name in REQUIRED_WORKFLOWS:
        content = Path(os.path.join(WORKFLOWS_DIR, name)).read_text(encoding="utf-8")
        lowered = content.lower()
        assert "git push" not in lowered
        assert "git commit" not in lowered


def test_agent_workflow_logs_step_exists():
    for name in REQUIRED_WORKFLOWS:
        workflow = _read_workflow(name)
        steps = _workflow_steps(workflow)
        names = [str(step.get("name", "")) for step in steps]
        assert any("structured agent execution log" in n.lower() for n in names)


def test_docs_for_agent_integration_exist():
    assert os.path.isfile(DOC_FILE), "Missing TASK_06 documentation file"
    text = Path(DOC_FILE).read_text(encoding="utf-8")
    assert "get-context" in text
    assert "Local Reproducibility" in text
