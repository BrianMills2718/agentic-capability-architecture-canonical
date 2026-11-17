# Agent engagement and knowledge-capture rules

Moved word for word from the root [AGENTS.md](../AGENTS.md) on 2026-11-17 to keep the root under the 12,000-byte instruction cap. These rules bind every agent working in this repository or an engagement workspace generated from it.

## Knowledge capture

Useful reusable assets include:

- semantic requirement/capability identity;
- selected and rejected providers with reasons;
- verified public interfaces and code;
- tests and compatibility evidence;
- schemas/configuration;
- integration adapters;
- deployment recipes;
- migration knowledge;
- failure cases and incidents;
- architecture decisions;
- agent instructions.

Do not assume future agents will infer an important constraint from old code.

Every project must finish with `clients/<project>/LEARNINGS.md`. Record either a plausible reuse candidate/reusable constraint/integration lesson or an explicit `No promotion candidate yet` assessment.

This requirement preserves evidence; it does not force abstraction.

## Paid/client engagement workflow

For contractor, agency, or client-paid work, do not put the engagement implementation directly in this canonical repository. Generate an isolated workspace with `python tools/engagement.py new ...`. Client work product stays local to the engagement.

Before implementation, the worker must make `CAPABILITY_PLAN.yml` ready and explicitly record selected providers, each selection's smallest viable local alternative and net-value reason, rejected providers, composition, exact internal exports/interfaces, and residual local gaps.

For internal selections, treat only verified semantic exports/public interfaces as executable boundaries. A broad `provides` label is not enough.

At closeout, generalized evidence may be proposed through `EVIDENCE_PROPOSAL.yml`; client-confidential material and client-owned code are prohibited from canonical evidence intake. `python tools/engagement.py close ...` produces proposal-only output for human review and never promotes code automatically.

### Current trust boundary

The engagement tooling is a **planning and evidence discipline for a cooperative worker**, not an adversarial sandbox/security product.

- The snapshot checksum and validator are shipped in the same workspace. They detect ordinary changes relative to that shipped state, but a malicious worker who controls both can re-attest modified content.
- The self-check validates contracts and declared internal exports/interfaces; it does not prove exhaustive provider research or detect every semantic reimplementation.
- Evidence “sanitization” is a human-reviewed declaration. The tool does not automatically redact credentials, confidential text, or client-owned code from free-text fields.

Do not describe these controls more strongly than they are.

Business metrics (`METRICS.yml`) remain engagement-local. They exist to test whether reuse/composition rates rise and marginal delivery effort falls across materially similar work; there is not yet a canonical cohort time series proving that claim.

