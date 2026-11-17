# capability-catalog Specification

## Purpose
Characterize the existing verified semantic-action catalog (`tools/capability_catalog.py`), which AGENTS.md names as the strongest callable-action claim in the repository. This is existing behavior; no new behavior is required.

## Requirements

### Requirement: verified-semantic-exports

The catalog SHALL admit a semantic export only when its action is declared in `provides`, its target is declared in `public_interfaces`, and the target resolves to a real top-level function or class in the capability's runtime source.

Source: inferred by agent, 2026-11-17: restates the module docstring and AGENTS.md "Machine-readable truth hierarchy" item 1 (Brian, 2026-11-17: "option B is what i want").

#### Scenario: Export resolves to public callable

- **WHEN** an exact action id such as `state.transition.plan` is resolved
- **THEN** the catalog returns its capability, declared public interface and source file, and an unknown id is an error

#### Scenario: Export names non-public interface

- **WHEN** a manifest exports an action whose target is not in its `public_interfaces`
- **THEN** building the catalog fails with a non-public interface error

#### Scenario: Export target missing

- **WHEN** a manifest exports a target that is not a top-level function or class in its runtime source
- **THEN** building the catalog fails with a does-not-resolve error
