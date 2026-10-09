---
schema_version: "1.0"
artifact_type: design_plan
id: capability-catalogue-aca
plan_id: capability-catalogue-aca
status: proposed
planning_path: requested
method_conformance_receipt: docs/plans/capability-catalogue-aca.receipt.json
goal:
  outcome: "catalog-info.yaml lists this repository's three reuse candidates and its capability-* make targets as Backstage Component capabilities, each pointing at its reuse_candidates.yml or capability_registry.yml entry"
  canonical_example: "The AES collector reads documents_to_text from this file with source reuse_candidates.yml#documents_to_text and reports that entry's status as candidate"
  forbidden_substitutes: "claiming success from a check's last line or exit status alone; a change outside the listed files; a commit without the saved check output"
  boundaries: "only these files: catalog-info.yaml; no irreversible action and no spend; Brian's request as quoted is the scope"
  done_when: "The AES collector run on this checkout reports descriptor=present, 4 capabilities, source_missing False for each, and this repository's own checks (tools/capability_catalog.py check, pytest) exit 0 The check's full output is committed as docs/plans/capability-catalogue-aca.check.txt, and the commit is tagged [Goal capability-catalogue-aca] with an Asked: line quoting the request."
  do_not_gate_on: "Brian's review of the plan page; work outside the listed files"
---

# Backstage descriptor for the AES capability catalogue

## Actor and result

**Actor:** Brian, who asked for this change.

**Request (verbatim):** Brian 2026-10-08 the catalogue "should really be a part of agentic engineering system canonical and company planning which is what my ecosystem is moving towards"

**Desired result:** catalog-info.yaml lists this repository's three reuse candidates and its capability-* make targets as Backstage Component capabilities, each pointing at its reuse_candidates.yml or capability_registry.yml entry

**Stable example:** The AES collector reads documents_to_text from this file with source reuse_candidates.yml#documents_to_text and reports that entry's status as candidate

## Authority and non-goals

**Authority:** Brian asked for this change in his own repository; one agent makes it.

**Non-goals:** nothing outside the files listed under Vertical and reset. No irreversible action and no spend.

## Success and disproof

**Success evidence:** The AES collector run on this checkout reports descriptor=present, 4 capabilities, source_missing False for each, and this repository's own checks (tools/capability_catalog.py check, pytest) exit 0

**Trace review:** the run whose full trace is judged is the success check above, run once on the commit that makes the change; no model, agent or LLM pipeline runs under this plan. Where the trace lives: the check's complete output, with the exact command and its exit status, is saved as `docs/plans/capability-catalogue-aca.check.txt` and committed with the change. What must be seen in it beyond the final result: the command ran against the files listed under Vertical and reset at that commit, each check or test it reports appears by name with its result and none is skipped, and the exit status matches; for each model element listed under System model, the output shows what that line says. Success and disproof are both judged from that file.

**Disproof:** The collector reports the descriptor invalid or a source entry missing

## System model

System model: exempt -- adds one read-only descriptor file; no stored state or view changes in this repository

## Uncertainties

| Uncertainty | Owner or resolving evidence |
| --- | --- |
| Whether the change needs files beyond the list below; if so it is out of scope for this plan | Resolved before editing: git status --short lists only catalog-info.yaml |

## Vertical and reset

One vertical over these files (and the saved check output, `docs/plans/capability-catalogue-aca.check.txt`):

- `catalog-info.yaml`

The vertical delivers: catalog-info.yaml lists this repository's three reuse candidates and its capability-* make targets as Backstage Component capabilities, each pointing at its reuse_candidates.yml or capability_registry.yml entry It is done when this holds: The AES collector run on this checkout reports descriptor=present, 4 capabilities, source_missing False for each, and this repository's own checks (tools/capability_catalog.py check, pytest) exit 0

Make the change, run the success check, commit. Reset: `git revert` of the commit. Not pursued: anything outside these files.

## Activation facts

No shared mechanism, no comparison, no LLM at the centre, no irreversible action or spend: a bounded change Brian asked for.
