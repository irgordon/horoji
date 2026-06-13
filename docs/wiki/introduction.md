# Horoji Wiki

Horoji helps developers and AI coding agents understand a repository before
they change it.

It keeps reviewed project facts in one place. It also builds useful generated
maps from those facts. Then it checks that the maps still match the repository.

Use this wiki if you are new to Horoji and want to know:

- what problem Horoji solves
- which files matter first
- which commands to run
- what generated files mean
- how CI and release checks work
- what to do when validation fails

This wiki explains the system in plain language. The formal rules still live
in the governance docs under `docs/` and the authoritative metadata under
`.project_memory/authoritative/`.

## Start Here

If you have one hour, read these pages in order:

1. [Problem and Mental Model](page-1-problem-and-mental-model.md)
2. [Major Components](page-2-major-components.md)
3. [Key Terms and Options](page-3-key-terms-and-options.md)
4. [First-Hour Walkthrough](page-5-first-hour-walkthrough.md)
5. [Troubleshooting](page-7-troubleshooting.md)

Then use the diagrams and release page when you need the bigger picture.

## Pages

- [Page 1: Problem and Mental Model](page-1-problem-and-mental-model.md)
- [Page 2: Major Components](page-2-major-components.md)
- [Page 3: Key Terms and Options](page-3-key-terms-and-options.md)
- [Page 4: Workflow Diagrams](page-4-workflow-diagrams.md)
- [Page 5: First-Hour Walkthrough](page-5-first-hour-walkthrough.md)
- [Page 6: What to Edit](page-6-what-to-edit.md)
- [Page 7: Troubleshooting](page-7-troubleshooting.md)
- [Page 8: Release and CI Flow](page-8-release-and-ci-flow.md)

## What Horoji Is

Horoji is a local project memory layer.

It helps answer questions like:

- Who owns this file?
- What rules apply before I edit it?
- What other parts of the project may be affected?
- Are generated memory files stale?
- Did an agent stay inside the expected scope?

## What Horoji Is Not

Horoji is not a chatbot, reasoning engine, release approval system, or source
of truth replacement.

The source of truth stays in the repository source files, governance docs, and
authoritative project memory files.

Horoji helps organize and check that truth.

Next: [Problem and Mental Model](page-1-problem-and-mental-model.md)
