# Changelog

All notable changes to Horoji are recorded in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Added — TASK_00: Horoji Bootstrap (Phase 0)

- Created canonical `.project_memory/` directory skeleton:
  - `authoritative/contracts/`
  - `authoritative/invariants/`
  - `authoritative/ownership/`
  - `authoritative/architecture_manifest/`
  - `derived/callgraphs/`
  - `derived/dependencies/`
  - `derived/impact_sets/`
  - `derived/summaries/`
  - `derived/embeddings/`
  - `history/adr/`
  - `history/decisions/`
  - `schemas/`
  - `config/`
- Created schema anchor files under `.project_memory/schemas/`:
  - `contract.schema.json` — JSON Schema for subsystem contract artifacts
  - `invariant.schema.json` — JSON Schema for invariant artifacts
  - `ownership.schema.json` — JSON Schema for ownership mapping artifacts
  - `provenance.schema.json` — JSON Schema for provenance metadata
- Created config anchor files under `.project_memory/config/`:
  - `horoji.config.yaml` — versioned Horoji configuration surface
  - `invalidation_rules.yaml` — versioned invalidation rules placeholder
- Created tool stub directories under `tools/horoji/`:
  - `cli/`
  - `generators/`
  - `validators/`
  - `invalidation/`
- Created `tests/horoji/test_bootstrap.py` with:
  - Positive tests for required directory and file presence
  - JSON schema parseability and structural validity tests
  - YAML config parseability and structural validity tests
  - Negative tests for missing files and malformed content detection

Horoji enforcement, generation, invalidation, CLI semantics, CI gating, and agent
integration remain deferred to later tasks (TASK_01 through TASK_06).
