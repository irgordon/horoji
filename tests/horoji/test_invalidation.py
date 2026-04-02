"""
Invalidation engine tests for Horoji Phase 3 (TASK_03).
"""

import os
import subprocess
import sys
import textwrap

import pytest
import yaml

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INVALIDATION_DIR = os.path.join(REPO_ROOT, "tools", "horoji", "invalidation")
CONFIG_DIR = os.path.join(REPO_ROOT, ".project_memory", "config")


def invalidation_path(name: str) -> str:
    return os.path.join(INVALIDATION_DIR, name)


def config_path(name: str) -> str:
    return os.path.join(CONFIG_DIR, name)


def run_invalidator(*extra_args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, invalidation_path("horoji-invalidate"), *extra_args],
        capture_output=True,
        text=True,
    )


def parse_yaml_output(raw: str) -> dict:
    data = yaml.safe_load(raw)
    assert isinstance(data, dict), f"Output did not parse to a mapping:\n{raw}"
    return data


def test_invalidation_script_exists():
    assert os.path.isfile(invalidation_path("horoji-invalidate")), (
        "Required invalidation script is missing"
    )


def test_invalidation_script_is_readable():
    path = invalidation_path("horoji-invalidate")
    assert os.access(path, os.R_OK), f"Invalidation script is not readable: {path}"


def test_invalidation_rules_config_exists():
    path = config_path("invalidation_rules.yaml")
    assert os.path.isfile(path), f"Invalidation rules config missing: {path}"


def test_invalidation_rules_config_parses_as_yaml():
    with open(config_path("invalidation_rules.yaml"), "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    assert isinstance(data, dict), "invalidation_rules.yaml must parse to a mapping"
    assert isinstance(data.get("rules"), list), "'rules' must be a list"


def test_case_single_file_change_invalidates_impact_sets():
    result = run_invalidator("--changed-file", "core/scheduler/runqueue.c")
    assert result.returncode == 0, f"Invalidator failed:\n{result.stderr}"
    data = parse_yaml_output(result.stdout)
    inv = data.get("invalidation_result", {})
    assert inv.get("affected_artifacts") == ["impact_sets"]
    assert inv.get("scope") == "conservative"


def test_case_header_change_invalidates_three_artifacts():
    result = run_invalidator("--changed-file", "include/scheduler.h")
    assert result.returncode == 0, f"Invalidator failed:\n{result.stderr}"
    data = parse_yaml_output(result.stdout)
    inv = data.get("invalidation_result", {})
    assert inv.get("affected_artifacts") == [
        "callgraphs",
        "dependencies",
        "impact_sets",
    ]
    assert inv.get("reason") == ["header_change_detected"]
    assert inv.get("scope") == "conservative"


def test_case_unknown_file_pattern_triggers_full_regeneration():
    result = run_invalidator("--changed-file", "README.md")
    assert result.returncode == 0, f"Invalidator failed:\n{result.stderr}"
    data = parse_yaml_output(result.stdout)
    inv = data.get("invalidation_result", {})
    assert inv.get("affected_artifacts") == [
        "callgraphs",
        "dependencies",
        "impact_sets",
    ]
    assert inv.get("scope") == "full_regeneration"
    assert inv.get("reason") == ["unknown_change_pattern_detected"]


def test_output_is_deterministic_for_same_inputs():
    args = [
        "--changed-file",
        "include/scheduler.h",
        "--changed-file",
        "core/scheduler/runqueue.c",
    ]
    first = run_invalidator(*args)
    second = run_invalidator(*args)
    assert first.returncode == 0 and second.returncode == 0, (
        f"Runs failed.\nfirst stderr: {first.stderr}\nsecond stderr: {second.stderr}"
    )
    first_data = parse_yaml_output(first.stdout)
    second_data = parse_yaml_output(second.stdout)
    assert first_data == second_data, "Invalidation output changed across identical runs"


def test_input_order_is_normalized():
    first = run_invalidator(
        "--changed-file",
        "include/scheduler.h",
        "--changed-file",
        "core/scheduler/runqueue.c",
    )
    second = run_invalidator(
        "--changed-file",
        "core/scheduler/runqueue.c",
        "--changed-file",
        "include/scheduler.h",
    )
    assert first.returncode == 0 and second.returncode == 0
    assert parse_yaml_output(first.stdout) == parse_yaml_output(second.stdout)


def test_reads_changed_files_from_explicit_file(tmp_path):
    changed = tmp_path / "changed_files.txt"
    changed.write_text(
        "include/scheduler.h\ncore/scheduler/runqueue.c\n",
        encoding="utf-8",
    )
    result = run_invalidator("--changed-files-file", str(changed))
    assert result.returncode == 0, f"Invalidator failed:\n{result.stderr}"
    data = parse_yaml_output(result.stdout)
    inv = data["invalidation_result"]
    assert inv["affected_artifacts"] == ["callgraphs", "dependencies", "impact_sets"]
    assert inv["scope"] == "conservative"


def test_fails_when_changed_files_input_is_missing():
    result = run_invalidator()
    assert result.returncode != 0
    assert "input_error" in result.stderr


def test_fails_when_rules_file_is_missing(tmp_path):
    runner = tmp_path / "run_missing_rules.py"
    runner.write_text(
        textwrap.dedent(
            f"""\
            import importlib.util
            import sys

            spec = importlib.util.spec_from_file_location(
                "invalidate_mod",
                {repr(invalidation_path("horoji-invalidate"))},
            )
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            mod.RULES_FILE = {repr(str(tmp_path / "missing.yaml"))}
            sys.argv = [
                "horoji-invalidate",
                "--changed-file",
                "include/scheduler.h",
            ]
            mod.main()
            """
        ),
        encoding="utf-8",
    )
    result = subprocess.run([sys.executable, str(runner)], capture_output=True, text=True)
    assert result.returncode != 0
    assert "configuration_error" in result.stderr


def test_fails_when_rules_file_is_malformed(tmp_path):
    bad_rules = tmp_path / "bad_rules.yaml"
    bad_rules.write_text("rules: [unclosed\n", encoding="utf-8")

    runner = tmp_path / "run_bad_rules.py"
    runner.write_text(
        textwrap.dedent(
            f"""\
            import importlib.util
            import sys

            spec = importlib.util.spec_from_file_location(
                "invalidate_mod",
                {repr(invalidation_path("horoji-invalidate"))},
            )
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            mod.RULES_FILE = {repr(str(bad_rules))}
            sys.argv = [
                "horoji-invalidate",
                "--changed-file",
                "include/scheduler.h",
            ]
            mod.main()
            """
        ),
        encoding="utf-8",
    )
    result = subprocess.run([sys.executable, str(runner)], capture_output=True, text=True)
    assert result.returncode != 0
    assert "configuration_error" in result.stderr


def test_fails_when_rule_structure_is_invalid(tmp_path):
    bad_rules = tmp_path / "bad_structure.yaml"
    bad_rules.write_text(
        textwrap.dedent(
            """\
            schema_version: "1.0.0"
            rules:
              - trigger: "include/**/*.h"
                invalidate:
                  - callgraphs
            """
        ),
        encoding="utf-8",
    )

    runner = tmp_path / "run_bad_structure.py"
    runner.write_text(
        textwrap.dedent(
            f"""\
            import importlib.util
            import sys

            spec = importlib.util.spec_from_file_location(
                "invalidate_mod",
                {repr(invalidation_path("horoji-invalidate"))},
            )
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            mod.RULES_FILE = {repr(str(bad_rules))}
            sys.argv = [
                "horoji-invalidate",
                "--changed-file",
                "include/scheduler.h",
            ]
            mod.main()
            """
        ),
        encoding="utf-8",
    )
    result = subprocess.run([sys.executable, str(runner)], capture_output=True, text=True)
    assert result.returncode != 0
    assert "configuration_error" in result.stderr

