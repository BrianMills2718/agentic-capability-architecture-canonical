# 0001 Adopt the code2 format, scoped to the capability catalog

Date: 2026-11-17
Status: accepted
Source: Brian, 2026-11-17: "option B is what i want" (active vision parts adopt the format now); scope choice inferred by agent.

## Context

The repository had no OpenSpec specs, Lockstep, or architecture model in the code2 format. Its Makefile held only capability and engagement targets; its tests (143, about 5 seconds, `pytest.ini`) were run by hand. AGENTS.md (2026-09-22 direction) forbids new experiments and machinery but allows ordinary maintenance.

## Decision

- One capability is specified: `capability-catalog` (`tools/capability_catalog.py`), with three scenarios marked `existing=True` on existing tests. Nothing else is specified; no behavior changes.
- Add `pyproject.toml` with only a dev group, `[tool.lockstep]` source `tools`, and `[tool.uv] package = false`. `requirements-dev.txt` and `pytest.ini` are unchanged (pytest.ini still governs pytest).
- Add `make check` (Lockstep, OpenSpec validation, the full existing pytest suite, import contracts) and `make fast`. The suite is short, so no `full` split is needed.

## Consequences

Commits run `make fast`; pushes run `make check`. Older capability manifests and docs stay as they are.

## Wrong if

`make check` grows beyond a few minutes, or a second capability needs a spec and the single-capability scope hides it from Lockstep.
