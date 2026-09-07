# Agentic Capability Architecture

Research and working implementation for an agent-native software architecture in which each project leaves behind reusable capability, tests, evidence, and architectural knowledge for the next project.

## North star

Instead of asking a coding agent to regenerate an application from scratch, give it a machine-readable capability base that lets it:

1. inspect what already exists;
2. reuse, configure, and compose proven behavior;
3. identify genuinely local gaps;
4. implement only those gaps;
5. validate compatibility and runtime behavior;
6. contribute new reuse evidence back to the capability base.

The larger hypothesis is that many applications may be compositions of a relatively small number of configurable semantic primitives plus higher-order capabilities, while important domain semantics remain local.

## Current layers

```text
semantic primitives
    ↓
evidence-backed capabilities
    ↓
typed project composition / state models
    ↓
project-native implementation adapters
```
## Current registered capabilities

```text
core            CORE
approvals       PROVEN
notifications   PROVEN
scheduling      CANDIDATE
```

## Real projects

The repository contains production-shaped Frappe implementations for:

1. Client Intake + Booking
2. Internal Procurement
3. IT Access Control
4. Facility Maintenance
5. Service Desk
6. Shared Resource Reservation

The latest seven-site proof demonstrated isolated project compositions and preserved older regression suites while adding the non-appointment Resource Reservation use case.

## Primitive-model research

See `docs/PRIMITIVE_CAPABILITY_THESIS.md` and the experimental files under `architecture/primitive_model/` where present.

The visual graph is not intended to be the architecture. The underlying typed model is the source; node/port, state-transition, deployment, and evidence diagrams are views over it.
## Capability-network research

The repository also contains the isolated fresh-agent registry-discovery challenge under `proof/fresh_agent_registry_discovery/challenge/`.

That challenge exposes multiple portable capabilities and asks an independent coding agent to discover and select the relevant ones before coding. It is intended to test whether the architecture works without conversational coaching.

## Start here

- `AGENTS.md` — rules for coding agents
- `capability_registry.yml` — current capability registry
- `reuse_candidates.yml` — evidence pipeline for emerging reuse
- `docs/WORKING_CONTEXT.md` — implementation history/context
- `docs/SESSION_CONTEXT_2026-09-06.md` — current strategic handoff
- `docs/ROADMAP.md` — current direction where present
- `docs/PRIMITIVE_CAPABILITY_THESIS.md` — primitive/capability hypothesis
- `docs/PROOF_LEDGER_EXTENDED.md` — proof references

## Status

This is an experimental research/code repository, not a claim that one universal primitive language or workflow engine has been validated.

The governing discipline is: **do not force everything to be reusable; make everything eligible to become reusable, then promote only after materially different uses provide evidence.**
