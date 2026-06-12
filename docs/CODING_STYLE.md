# CODING_STYLE.md

## Purpose

This file defines coding rules for Horoji.

Horoji must remain simple, readable, deterministic, and easy to audit. Code should make the repository's architectural facts easier to inspect, not harder to understand.

The preferred style is top-down readability: a reader should understand the main operation first, then inspect smaller helper functions only when needed.

## Core Rules

### 1. Keep Control Flow Simple

Write code that is easy to follow in one pass.

Prefer:

* early returns
* small functions
* clear condition names
* direct data flow
* explicit error handling

Avoid:

* deeply nested `if` blocks
* long `match` chains with hidden behavior
* complex boolean expressions
* clever iterator chains that hide intent
* recursion unless the domain clearly requires it

If a function needs more than two levels of nesting, split it.

### 2. Write Top-Down Code

Public entry points should read like a short procedure.

A reader should see:

1. what input is accepted
2. what is validated
3. what is loaded
4. what is derived
5. what is written or returned

Lower-level helpers should appear after the main operation when the language permits it.

Do not force readers to reconstruct the workflow from scattered abstractions.

### 3. Prefer Plain Data Structures

Use simple structs, enums, maps, and lists.

Avoid unnecessary abstractions such as:

* generic frameworks
* trait hierarchies without multiple real implementations
* service containers
* dependency injection layers
* macro-generated business logic
* dynamic dispatch where static dispatch is sufficient

Abstraction is allowed only when it removes proven duplication or protects a real boundary.

### 4. Make Trust Boundaries Explicit

Code must clearly distinguish:

* authoritative inputs
* derived outputs
* validation results
* provenance records
* invalid artifacts

Derived data must never be treated as authoritative.

Do not use names that blur this boundary. For example, prefer `DerivedMetadata` over `Metadata` when the value is not canonical truth.

### 5. Determinism Comes First

Code must produce identical output from identical input.

Do not use:

* random values
* wall-clock timestamps in derived artifacts
* unordered iteration in serialized output
* host-specific paths
* environment discovery
* network calls
* external downloads

When ordering matters, sort explicitly.

When serialization matters, use stable formats and deterministic field ordering where supported.

### 6. Validate at Boundaries

Validate data when it enters the system.

Do not pass unchecked data deep into the codebase.

Inputs from files, configuration, manifests, schemas, and generated artifacts must be validated before use.

Invalid input should fail closed with a clear error.

### 7. Keep Functions Small

A function should do one clear job.

Split a function when it performs multiple phases, such as:

* loading
* parsing
* validating
* deriving
* writing
* reporting

A useful function name should describe the operation without needing a comment.

### 8. Avoid Hidden Side Effects

A function that reads files, writes files, mutates state, or emits output must make that behavior obvious from its name or signature.

Prefer names like:

* `load_manifest`
* `write_derived_metadata`
* `validate_invariants`
* `derive_structure_index`

Avoid vague names like:

* `process`
* `handle`
* `run`
* `execute`
* `manage`

Generic names are allowed only at narrow entry points.

### 9. Keep Comments Minimal

Comments should explain why something exists, not restate what the code already says.

Use comments for:

* non-obvious invariants
* security boundaries
* deterministic ordering requirements
* compatibility constraints
* intentionally rejected alternatives

Avoid comments that narrate simple code.

Bad:

```text
// Loop through files
```

Better:

```text
// Sort before serialization so derived output is reproducible.
```

### 10. Prefer Explicit Errors

Errors must be specific enough to support repair.

Prefer errors that identify:

* the failed operation
* the artifact involved
* the invariant violated
* the expected condition

Avoid generic errors such as:

* `failed`
* `invalid`
* `something went wrong`
* `bad input`

Do not swallow errors.

Do not convert structured errors into plain strings too early.

### 11. Do Not Over-Generalize

Build only what Horoji needs now.

Do not add extension points, plugin systems, or configuration layers for hypothetical future use.

A second real use case may justify refactoring.

A first imagined use case does not.

### 12. Keep Repository Locality Obvious

Code must operate only inside the repository boundary.

Do not inspect:

* host filesystem state outside the repository
* user home directories
* system configuration
* global tool installations
* network resources

All required inputs must come from repository content, pinned tools, or explicit configuration.

### 13. Keep Tests Concrete

Tests should describe behavior directly.

Prefer tests that prove:

* deterministic output
* invalid input rejection
* trust-boundary enforcement
* schema validation
* provenance preservation
* incremental invalidation correctness

Avoid tests that only mirror implementation details.

Test names should describe the rule being protected.

### 14. Avoid Negative Patterns

Do not introduce:

* global mutable state
* implicit environment dependencies
* hidden caches
* reflection-based behavior
* runtime code generation
* broad catch-all error handling
* silent fallback behavior
* mixed authoritative and derived data models
* deeply nested logic
* abstraction layers with only one caller
* comments that compensate for unclear code

If code needs a long explanation to be safe, simplify the code first.

## Naming Rules

Use names that expose the domain boundary.

Preferred terms:

* `Authoritative`
* `Derived`
* `Invariant`
* `Provenance`
* `Validation`
* `Invalidation`
* `Projection`
* `RepositoryRoot`

Avoid vague terms:

* `Thing`
* `Data`
* `Manager`
* `Handler`
* `Processor`
* `Util`
* `Helper`
* `Context`

Use `Helper` only when no stronger domain name exists.

## File Organization

Each file should have a narrow purpose.

Avoid large mixed files that combine:

* parsing
* validation
* derivation
* persistence
* command handling
* test fixtures

Split by responsibility, not by personal preference.

A reader should be able to answer: "What rule does this file protect?"

## Review Standard

Before merging code, ask:

1. Can a new contributor read the main flow without tracing five abstractions?
2. Are authoritative and derived artifacts clearly separated?
3. Is output deterministic?
4. Are invalid states rejected early?
5. Are errors specific and repairable?
6. Is every abstraction justified by current code?
7. Could comments be removed because the code is clear enough?

If the answer is no, simplify before merging.

## Python Good and Bad Examples

These examples show the expected Python style for Horoji.

The goal is not clever Python. The goal is readable, deterministic, auditable code.

### Example 1: Keep the Main Flow Top-Down

Bad:

```python
def run(repo):
    data = parse(load(repo))
    if data:
        for item in data:
            if item.kind == "derived":
                if item.valid:
                    write(item)
```

Good:

```python
def run(repo: RepositoryRoot) -> None:
    manifest = load_manifest(repo)
    validated_manifest = validate_manifest(manifest)
    derived_metadata = derive_metadata(validated_manifest)

    write_derived_metadata(repo, derived_metadata)
```

### Example 2: Use Early Returns

Bad:

```python
def validate_artifact(artifact):
    if artifact.exists():
        if artifact.schema_valid:
            if artifact.provenance:
                return True
            else:
                return False
        else:
            return False
    else:
        return False
```

Good:

```python
def validate_artifact(artifact: Artifact) -> bool:
    if not artifact.exists():
        return False

    if not artifact.schema_valid:
        return False

    if artifact.provenance is None:
        return False

    return True
```

### Example 3: Sort Before Serialization

Bad:

```python
def write_index(path, records):
    payload = {"records": records}
    path.write_text(json.dumps(payload))
```

Good:

```python
def write_index(path: Path, records: list[StructuralRecord]) -> None:
    sorted_records = sorted(records, key=lambda record: record.path)

    payload = {"records": [record.to_dict() for record in sorted_records]}

    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
```

### Example 4: Do Not Hide Repository Boundary Checks

Bad:

```python
def read_file(path):
    return Path(path).read_text()
```

Good:

```python
def read_repo_file(repo_root: Path, relative_path: Path) -> str:
    full_path = (repo_root / relative_path).resolve()

    if not full_path.is_relative_to(repo_root.resolve()):
        raise RepositoryBoundaryError(relative_path)

    return full_path.read_text(encoding="utf-8")
```

### Example 5: Avoid Vague Utility Functions

Bad:

```python
def process(data):
    return [x for x in data if x.get("valid")]
```

Good:

```python
def collect_valid_invariants(
    invariant_records: list[InvariantRecord],
) -> list[InvariantRecord]:
    return [
        record
        for record in invariant_records
        if record.validation_status == "valid"
    ]
```

### Example 6: Do Not Use Bare Dictionaries for Domain Data

Bad:

```python
artifact = {
    "path": "docs/ARCHITECTURE.md",
    "type": "derived",
    "valid": True,
}
```

Good:

```python
@dataclass(frozen=True)
class ArtifactRecord:
    path: str
    trust_level: TrustLevel
    validation_status: ValidationStatus
```

Typed records protect meaning. A plain dictionary allows invalid states too easily.

### Example 7: Do Not Catch Everything

Bad:

```python
def load_config(path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}
```

Good:

```python
def load_config(path: Path) -> HorojiConfig:
    try:
        raw_config = path.read_text(encoding="utf-8")
    except FileNotFoundError as error:
        raise ConfigNotFoundError(path) from error

    try:
        decoded_config = json.loads(raw_config)
    except json.JSONDecodeError as error:
        raise ConfigParseError(path, error.lineno, error.colno) from error

    return validate_config(decoded_config)
```

Silent fallback hides failure. Horoji should fail closed when canonical inputs are missing or invalid.

### Example 8: Keep Comments Focused on Boundaries

Bad:

```python
# Create a list
records = []

# Loop over files
for file in files:
    # Add record
    records.append(build_record(file))
```

Good:

```python
# Stable ordering prevents nondeterministic derived output.
for file in sorted(files):
    records.append(build_record(file))
```

### Example 9: Avoid Boolean Traps

Bad:

```python
def write_artifact(path, data, authoritative=False):
    ...
```

Good:

```python
def write_authoritative_artifact(path: Path, data: bytes) -> None:
    ...


def write_derived_artifact(path: Path, data: bytes) -> None:
    ...
```

Separate functions make the trust boundary visible.

### Example 10: Avoid Hidden Environment Discovery

Bad:

```python
def find_repo_root():
    return Path.cwd()
```

Good:

```python
def open_repository(repo_root: Path) -> Repository:
    resolved_root = repo_root.resolve()

    if not (resolved_root / ".git").exists():
        raise RepositoryRootError(resolved_root)

    return Repository(root=resolved_root)
```

Horoji should use explicit repository paths. It should not guess from the host environment.

### Example 11: Avoid Deeply Nested Derivation Logic

Bad:

```python
def derive(records):
    output = []
    for record in records:
        if record.trust_level == "authoritative":
            if record.schema_valid:
                for dependency in record.dependencies:
                    if dependency.exists:
                        if dependency.valid:
                            output.append(make_projection(record, dependency))
    return output
```

Good:

```python
def derive_projections(records: list[ArtifactRecord]) -> list[ProjectionRecord]:
    projections: list[ProjectionRecord] = []

    for record in records:
        if not is_projection_source(record):
            continue

        projections.extend(derive_record_projections(record))

    return projections


def is_projection_source(record: ArtifactRecord) -> bool:
    return (
        record.trust_level == TrustLevel.AUTHORITATIVE
        and record.validation_status == ValidationStatus.VALID
    )
```

### Example 12: Avoid Clever One-Liners

Bad:

```python
records = {p: h(p) for p in sorted([x for x in files if x.suffix in exts])}
```

Good:

```python
def hash_supported_files(
    files: list[Path],
    supported_extensions: set[str],
) -> dict[Path, str]:
    supported_files = [
        file
        for file in files
        if file.suffix in supported_extensions
    ]

    sorted_files = sorted(supported_files)

    return {
        file: hash_file(file)
        for file in sorted_files
    }
```

Readable code is easier to audit than compressed code.

### Example 13: Prefer Narrow Exceptions

Bad:

```python
raise ValueError("invalid")
```

Good:

```python
class InvariantViolationError(Exception):
    def __init__(self, invariant_id: str, artifact_path: str) -> None:
        super().__init__(
            f"invariant {invariant_id} failed for artifact {artifact_path}"
        )
```

Specific errors make failures repairable.

### Example 14: Keep I/O at the Edges

Bad:

```python
def validate_manifest(path):
    data = json.loads(path.read_text())
    return data["version"] == 1
```

Good:

```python
def load_manifest(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_manifest(manifest: dict[str, object]) -> Manifest:
    return Manifest.from_dict(manifest)
```

Separate loading from validation. This makes tests smaller and behavior clearer.

### Example 15: Make Incremental Invalidation Explicit

Bad:

```python
def update_everything(repo):
    generate_all(repo)
```

Good:

```python
def update_invalidated_artifacts(
    repo: Repository,
    changed_paths: list[Path],
) -> None:
    invalidated_artifacts = find_invalidated_artifacts(repo, changed_paths)

    for artifact in sorted(invalidated_artifacts, key=lambda item: item.path):
        regenerate_artifact(repo, artifact)
```

Full regeneration is allowed, but invalidation logic should remain explicit when used.

## Python Review Checklist

Before merging Python code, check:

1. Does the main function read top-down?
2. Are repository boundaries explicit?
3. Are derived and authoritative artifacts separated?
4. Is serialized output deterministic?
5. Are unordered collections sorted before output?
6. Are errors specific?
7. Are comments limited to non-obvious rules?
8. Is there any hidden environment discovery?
9. Is there any broad `except Exception` fallback?
10. Could a simpler function replace an abstraction?
