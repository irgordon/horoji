# Page 4: Workflow Diagrams

Previous: [Key Terms and Options](page-3-key-terms-and-options.md)
Next: [First-Hour Walkthrough](page-5-first-hour-walkthrough.md)

These diagrams show how the main pieces connect.

## System Map

```mermaid
flowchart TD
    User["Developer or agent"] --> PublicCLI["Public CLI: horoji"]
    User --> CheckCLI["Check CLI: horoji-check"]
    PublicCLI --> Memory["Horoji memory"]
    Memory --> Authoritative["Authoritative files"]
    Memory --> Derived["Derived files"]
    CheckCLI --> Invalidation["Invalidation"]
    Invalidation --> Generators["Generators"]
    Generators --> Derived
    CheckCLI --> Validators["Validators"]
    Validators --> Authoritative
    Validators --> Derived
    CI["GitHub Actions CI"] --> CheckCLI
    CI --> Tests["pytest"]
```

## Authoritative vs Derived Flow

```mermaid
flowchart LR
    Source["Repository source and docs"] --> Authoritative["Reviewed authoritative facts"]
    Authoritative --> Generators["Generators"]
    Source --> Generators
    Generators --> Derived["Generated derived maps"]
    Authoritative --> Validators["Validators"]
    Derived --> Validators
    Validators --> Result["Pass or fail"]
```

## Change Validation Workflow

```mermaid
flowchart TD
    Change["Changed file"] --> Impact["Impact calculation"]
    Impact --> Scope["Affected artifact classes"]
    Scope --> Regen{"Regeneration needed?"}
    Regen -- "yes" --> Generate["Run generators"]
    Regen -- "no" --> Validate["Run validators"]
    Generate --> Validate
    Validate --> Policy["Committed derived policy"]
    Policy --> Tests["Run tests"]
    Tests --> Result["Result"]
```

## Agent Workflow

```mermaid
flowchart TD
    ReadDocs["Read AGENTS.md and docs"] --> Query["Query Horoji context"]
    Query --> Bound["Choose bounded change"]
    Bound --> Edit["Make change"]
    Edit --> Validate["Run validation and tests"]
    Validate --> Report["Report files, commands, validation, notes"]
```

## Release Gate Workflow

```mermaid
flowchart TD
    Clean["Clean tree"] --> ValidateAll["validate-all"]
    ValidateAll --> Pytest["pytest"]
    Pytest --> HorojiCheck["horoji-check committed policy"]
    HorojiCheck --> Changelog["Changelog entry"]
    Changelog --> Decision["Decision record"]
    Decision --> Tag["Release or RC tag"]
```

## Keep Diagrams Simple

The diagrams are maps, not proof.

Use the formal governance docs for exact release and validation rules.
