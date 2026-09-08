# Next Proof — Current Status

> **Supersedes the original bootstrap proof plan.** The two gates previously listed here—real Frappe lifecycle proof and genuinely fresh coding-agent acceptance—have both passed. Their evidence is indexed in [`PROOF_LEDGER_EXTENDED.md`](PROOF_LEDGER_EXTENDED.md).

## Remaining high-value proof

The current open proof question is the isolated fresh-agent registry-discovery challenge under:

```text
proof/fresh_agent_registry_discovery/challenge/
```

The goal is narrower and more useful than repeating the original bootstrap acceptance test:

> Can a genuinely separate coding agent, without the source monorepo or this conversation, discover portable capability metadata, select the relevant capabilities, reject irrelevant ones, resolve dependency closure, and compose a correct implementation from the exposed interfaces/evidence?

## Required isolation

The run should use a genuinely separate coding-agent session and should not provide:

- this conversation;
- hidden evaluator logic or answer keys;
- source-monorepo context that the challenge intentionally withholds;
- hints that name the expected capability choices.

The challenge should expose only the intended portable snapshot/task surface.

## What to measure

Record at least:

- which capabilities/providers the agent considered;
- which were selected and rejected, with reasons where visible;
- whether dependency closure was resolved correctly;
- whether the agent used the declared public interfaces rather than reconstructing hidden source behavior;
- whether the implementation passes the independent consumer/evaluator tests;
- unnecessary bespoke code or semantic leakage;
- human intervention required.

## Interpretation

A pass strengthens the claim that machine-readable capability metadata/evidence can guide an uncoached agent outside the source repository.

A failure is equally useful if it identifies a concrete discovery, interface, evidence, packaging, or instruction gap. Fix the smallest demonstrated gap; do not respond by adding a generalized planner, protocol, registry, or runtime without evidence that the simpler architecture is insufficient.

## Separate future experiment

If provider selection becomes materially ambiguous, a later controlled comparison may test ordinary documented APIs versus capability metadata/typed interfaces versus those interfaces plus primitive composition. Do not build competing production architectures solely to manufacture that experiment.
