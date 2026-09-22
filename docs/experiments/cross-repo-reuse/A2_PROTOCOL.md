# A2 Protocol — Frozen Control/Reuse Instrument

Plan: ACA-PLAN-002, stage A2.
Recorded: 2026-09-21.
Authoring baseline: canonical `867f558a2238af7754d15ede46918d0546ab38e9` (PR #64 merged).
Status: public and held-out instrument frozen; **A3 remains blocked only on worker-isolation/model preflight** before the first scored pair.

## Question

For the same accepted Product N+1 behavior, does access to an accumulated Product N asset reduce delivery effort or defects compared with competent ordinary engineering, after publication/adaptation cost is accounted for?

A2 does not score that question. It freezes the instrument.

## Public task

The shared task is [A2_PUBLIC_BRIEF.md](A2_PUBLIC_BRIEF.md).

It intentionally exercises nontrivial behavior:

- multiple exact labeled queries;
- independent per-query disposition;
- partial success;
- aggregation/deduplication across successful queries;
- malformed-item and failed-query warnings;
- stable source provenance;
- a Product N+1 ranking/limit rule that is **not** prospecting-specific.

The last item matters: a reuse worker must not silently inherit unrelated Product N ranking semantics.

## Common provider transport

Both arms receive:

- `provider_replay.py`;
- `public_sample.json`;
- provider-native endpoint/response documentation relevant to the task;
- a synthetic `TWITTERAPI_IO_API_KEY`.

The scored evaluator supplies different hidden replay data through the same requests-compatible seam.

No live provider calls are allowed in scored runs.

## Conditions

### C — ordinary engineering

Receives only the common public task, provider documentation/replay support, ordinary packages/tools, and the normal pre-code planning discipline.

The worker may implement the smallest correct local/provider-native solution.

### R — accumulated asset available

Receives everything in C plus the **authorized, retained, pinned** Product N artifact and its normal publication documentation/tests.

The worker may use, adapt, or reject the asset. Rejection is not a failure if the reason is economically/semantically sound.

The user confirmed authorization on 2026-09-22 for private experimental reuse/repackaging of the Product N source. The retained private wheel is stored outside the public ACA repository and is not publicly distributed.

Frozen treatment asset:

- Product N revision: `ab2cfba0e8c43f0198716dee4414dedf2212d478`
- wheel sha256: `0cd030d9379d4ca823d8471b504a367cf1270a21598801442a6bc283bd279dcd`
- source hashes remain those recorded in A1.

The treatment evaluator uses a separate provenance hook. An explicit, reasoned rejection of the asset is allowed; silent bypass while claiming reuse is not.

## Worker harness

Planned scored harness for both arms:

- `ask-agent claude`;
- fresh session for every scored worker;
- same model/harness resolution for paired runs;
- Python 3.12 task environment;
- separate consumer repository/worktree outside ACA and Product N;
- 30-minute active-worker ceiling per submission;
- subscription-first resource use;
- incremental cash target: **$0**;
- hard incremental metered/provider cap: **$2 per worker**;
- no new subscription or infrastructure purchase;
- no live provider call.

Record the exact model resolved by the first non-scored preflight and require the same model family/configuration for the paired scored run.

## Worker context

Workers receive required business behavior and public examples. They do **not** receive:

- held-out replay data;
- evaluator code or expected outputs;
- another worker's source/results;
- coordinator-authored patches;
- prior P3/P5 result narratives;
- the expected capability choice.

Normal inspection of material legitimately included in that arm is allowed.

## Submission freeze

The first submission is immutable for scoring.

At the ceiling:

1. record Git revision, session ID, elapsed/active time, harness/model, and available token/tool usage;
2. stop the worker;
3. evaluate the exact commit once against the held-out suite;
4. record failures without patching the scored commit.

Later assisted repair is diagnostic work, not a retroactive blind success.

## Held-out evaluator

The evaluator is authored and stored outside both worker-accessible repositories/paths until scoring is complete.

Before A3:

- record evaluator content hash;
- record held-out replay content hash;
- prove the worker sandbox cannot read the evaluator path;
- run evaluator negative controls;
- verify the evaluator itself never makes live provider calls.

Hidden cases must cover at least:

1. dropped query disposition;
2. whole-run failure when one query fails;
3. broken cross-query dedup/provenance;
4. swallowed malformed/conflict warning;
5. wrong Product N+1 ranking or candidate-limit violation;
6. synthetic credential leakage;
7. treatment claiming reuse while bypassing the retained provider asset.

The last check is treatment-specific and must not require the control to import ACA/Product N code.

## Non-scored preflight

Before A3, use a disposable trivial repository/session to confirm:

- shell execution;
- Python/pytest execution;
- dependency availability;
- writing files/committing;
- multi-word argument preservation;
- evaluator path is outside worker-readable scope;
- usage/time capture works.

A setup-invalid scored run does not count as an arm result; retain it and fix the instrument before restarting under the remaining budget.

## Metrics

For each scored submission retain:

- accepted/rejected;
- first-pass hidden evaluator results;
- wall and active-worker time;
- session/model/harness;
- tool/model usage visible from the subscription harness;
- incremental cash actually charged, if any;
- human interventions/minutes;
- discovery/installation/adaptation/debug time where observable;
- consumer-local code and adapter surface;
- selected/rejected reusable assets and reasons;
- retained failure/rework evidence.

Publication cost from A1 is tracked separately and included in first-use economics.

## Decision discipline

No A2/A3 result can justify a new ACA runtime/catalog/workflow engine.

Use the research agenda's prior-art-first rule. If a named failure survives ordinary contracts/docs/adapters/provider-native features, freeze that failure before testing any new ACA field/mechanism.

## Freeze record

Public artifacts:

- `A2_PUBLIC_BRIEF.md` sha256 `f6063e1ff192a07cf7ff5e280f91691c7b46ccbf82ce14d1d57fcb927be310c4`
- `provider_replay.py` sha256 `7dcb4e375a99265a8c2a7314fe6afa1948d0069ee0dfe32dea7e1a8cf373e416`
- `public_sample.json` sha256 `5eebc807ee9f4e7c39967eb216138bebc12677f0b58820ba95649373a4922a44`

Held-out artifacts are stored outside worker-accessible repositories under the coordinator's local state and are referenced here by hash only:

- evaluator sha256 `684753fa57e7f0f935354e7fb9532d13d839532d1bdf21d1677abea241752de1`
- hidden request sha256 `0a499dd5a05541036a5a1b52b23a3ff7d2608a272e5f64048c9c66653d863dde`
- hidden replay sha256 `cc96a677fd0511e01f1ef65db50c4207bc4209fa927f29ff81958071bfac6499`
- negative-control procedure sha256 `5dfca8edbf871b8ffb201c0fa4255b41825e9d73cb9163fb303fb91f8d1817a8`
- treatment provenance hook sha256 `b6650f47e5ed027532df7dd238691bda1cb74ba8ee962ccbc0fcfd953ce16d65`

Instrument validation before scoring:

- an independently written reference initially failed 12 checks, exposing a global post-identity interpretation error; after correcting that public-brief interpretation it passed **40/40 behavioral checks** with the treatment hook skipped;
- a deliberate combined mutant (dropped failed dispositions, swallowed warnings, credential leak, nondeterministic extra output) failed **13 checks**, proving the evaluator turns red on multiple independent defects;
- the evaluator's network guard is self-tested before every score and blocks live network access.

## Gates before A3

- [x] Public task and replay artifacts hashed/frozen.
- [x] Public replay support tests pass (13 focused tests).
- [x] Held-out evaluator and hidden replay authored independently from the scored workers.
- [x] Held-out hashes recorded.
- [x] Evaluator reference pass and negative control pass.
- [ ] Worker isolation/preflight passes.
- [ ] Same scored model/harness available to both arms.
- [x] Product N rights confirmed for private reuse arm.
- [x] Authorized retained Product N artifact frozen with exact hash/revision.
- [x] No scored worker has seen hidden evaluator content (no scored worker has started).

Until the two remaining preflight items are satisfied, A3 has **not** started.
