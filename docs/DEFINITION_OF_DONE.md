# Definition of Done

## Bootstrap completion checklist

- [x] Agent rules are stable enough to guide a new coding session.
- [x] Capability registry schema is defined and usable.
- [x] Project/client manifest schema is defined and usable.
- [x] Shared/config/custom layering is enforced by convention and examples.
- [x] Scheduling reference capability exists.
- [x] At least one composable companion capability exists.
- [x] A project-specific extension demonstrates customization without modifying shared code.
- [x] Rule priorities and explicit conflicts resolve deterministically.
- [x] Pure unit tests cover rule behavior.
- [ ] Frappe hook integration tests have produced a confirmed green run against a real Bench/site.
- [ ] Persistence tests have produced a confirmed green run for ALLOW, REQUIRE_APPROVAL, and BLOCK against a real Bench/site.
- [x] Compatibility tests exist for shared capability changes.
- [x] Capability promotion lifecycle (local → candidate → proven → core) is documented.
- [x] New-project agent workflow is documented and repeatable.
- [x] Reusable knowledge capture is part of the workflow.
- [x] A final export script/checklist produces a complete ZIP.
- [x] A fresh-agent acceptance sandbox and independent evaluator exist.
- [x] The acceptance harness has both positive and negative rehearsal evidence.
- [ ] A genuinely fresh coding-agent run has passed both the evaluator and human review.

## Current automated local evidence

At the latest snapshot:

- 17 local tests pass;
- repository schemas, registry synchronization, promotion evidence, and reference project manifests validate;
- all Python sources compile;
- all 4 current Frappe-style app packages build successfully;
- the Frappe lifecycle proof is packaged as `.github/workflows/frappe-integration.yml` and a local Bench runner, but still requires a green external Bench execution.

## Final acceptance test

Start a fresh project with a coding agent that has no access to this conversation or a previous agent thread.

Without manually reminding it of the architecture, the agent should:

1. inspect the capability registry,
2. reuse/configure existing capabilities where possible,
3. compose them through a project manifest,
4. isolate new bespoke behavior,
5. add appropriate tests,
6. preserve existing consumers,
7. update reusable knowledge,
8. and leave the capability base stronger than before.

The bootstrap is complete only when:

1. the real Frappe hook/persistence integration suite has a confirmed green run, and
2. the genuinely fresh agent acceptance run passes both automated evaluation and human review.

The capability base itself then continues to grow indefinitely through future projects.
