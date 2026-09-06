# Composable Capability Base

A starter system for building software projects against an accumulating library of reusable capabilities.

## Goal

Every project should leave behind reusable code, tests, schemas, interfaces, integration knowledge, and agent instructions that make the next project faster and safer.

The system separates:

1. **Shared capabilities** — reusable functionality.
2. **Client/project configuration** — differences expressed as settings.
3. **Client/project custom extensions** — genuinely unique behavior.

The default workflow is:

Requirement → inspect capability base → configure → compose → extend locally if necessary → test → record learning → promote only when reuse is demonstrated.

## Initial structure

```text
capabilities/
    core/
    approvals/
    notifications/
    scheduling/
    _template/

clients/
    _template/
        manifest.yml
        config/
        custom/

tests/
    compatibility/

docs/
    WORKING_CONTEXT.md
    ARCHITECTURE.md
    DECISIONS.md

AGENTS.md
capability_registry.yml
```

This repository is intentionally small. It should grow from real projects rather than trying to become a universal framework up front.

## Current reference implementation

The repository now includes a minimal end-to-end reference project:

- shared `na_scheduling` Frappe app,
- shared `na_approvals` rule engine/Frappe app,
- `acme_reference` project manifest,
- ACME-specific `acme_rules` extension,
- pure and compatibility tests,
- Frappe integration tests ready for a Bench test site.

Run all local checks that do not require Frappe:

```bash
python tools/check_bootstrap.py
```

Create a fresh handoff ZIP:

```bash
python tools/export_zip.py
```

See `docs/REFERENCE_IMPLEMENTATION.md` and `docs/PROJECT_WORKFLOW.md` for the intended workflow.

## Reuse discipline

Create a new project layer with:

```bash
python tools/new_project.py my_project --capabilities core,scheduling,approvals
```

Record a potentially reusable idea without prematurely moving it into shared code:

```bash
python tools/record_reuse_candidate.py --id scheduling.example --project my_project --description "Example reusable behavior"
```

See `docs/REUSE_PROMOTION.md`.

## Proof status

The bootstrap architecture and local reference implementation are complete enough to use. Two external proof gates remain:

1. a green real-Frappe lifecycle run (`.github/workflows/frappe-integration.yml` or the local Bench runner), and
2. a genuinely fresh coding-agent acceptance run.

See `docs/NEXT_PROOF.md` and `docs/DEFINITION_OF_DONE.md`.
