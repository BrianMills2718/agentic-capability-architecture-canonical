# A2 Protocol — Frozen Control/Reuse Instrument

Plan: ACA-PLAN-002, stage A2.
Recorded: 2026-09-21.
Authoring baseline: canonical `867f558a2238af7754d15ede46918d0546ab38e9` (PR #64 merged).
Status: **A2 complete.** Public task, private treatment artifact, replacement held-out evaluator, negative controls, and worker isolation/model preflight are frozen. No scored A3 worker has started.

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

Frozen scored harness for both arms:

- direct Claude Code subscription CLI: `claude -p --permission-mode auto --permission-prompts none --model sonnet --output-format json`;
- fresh session for every scored worker;
- resolved model in non-scored preflight: `claude-sonnet-5`; the same command/model alias is required for both arms;
- Python 3.12 task environment;
- separate consumer repository outside ACA and Product N;
- each scored Claude process runs inside an unprivileged Linux user+mount+PID namespace (`unshare --user --map-root-user --mount --pid --fork --kill-child`), with its repo bind-mounted as the working surface;
- worker-visible host paths containing ACA/Product N/Claude history/held-out state are over-mounted with empty tmpfs mounts; only the existing Claude credential file is rebound read-only into an otherwise empty Claude config mount;
- 30-minute active-worker ceiling per submission;
- subscription-first resource use;
- incremental cash target: **$0**;
- hard incremental metered/provider cap: **$2 per worker**;
- no new subscription or infrastructure purchase;
- no live provider call.

The original `ask-agent claude --edit` route was rejected during preflight because its non-interactive `acceptEdits` policy denied pytest and git commands. Direct Claude Code `auto` mode is a harness/configuration repair, not an ACA change. A first direct preflight proved execution worked but also proved same-user path isolation did not. The final namespace preflight then ran Python 3.12.3, pytest (1 pass), preserved a multi-word CLI argument, wrote/committed files, and resolved `claude-sonnet-5` while reporting namespace PID 1 and no held-out-state visibility. A deliberately detached child scheduled to write after worker exit was killed by namespace teardown; its marker file never appeared.

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

The evaluator was authored outside both worker repositories. Preflight showed that ordinary same-user path placement was not an enforceable blind. The scored boundary therefore combines two ordinary OS controls rather than trusting path discipline: (1) the frozen replacement held-out packet lives on the Windows host at a coordinator-only path while scored workers run in WSL with `/mnt` hidden; no held-out plaintext or non-scored reference remains in the WSL worker filesystem; and (2) each worker runs in an unprivileged user/mount/PID namespace whose mount view hides ACA worktrees, Product N source, Claude history/state, Windows mounts, and coordinator local state. Namespace teardown uses `--kill-child`, so worker descendants cannot survive into the later host-side score phase. The earlier AES-encrypted WSL holdout is retained only as superseded historical evidence; its unavailable key is not part of the scored recovery path.

Before A3:

- record evaluator content hash;
- record held-out replay content hash;
- ensure no plaintext evaluator/hidden fixture exists anywhere available to the worker during its run;
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

Disposable preflights confirmed:

- shell execution: PASS;
- Python 3.12.3 / pytest execution: PASS;
- writing files/committing: PASS;
- multi-word argument preservation: PASS;
- model/session/cost metadata returned in JSON: PASS (`claude-sonnet-5`);
- plain same-user path isolation: FAIL, retained as an instrument failure rather than ignored;
- namespace mount isolation: PASS (`heldout_visible=no`, Claude config history hidden, ACA/Product N paths hidden);
- namespace process isolation: PASS (worker was PID 1; a detached delayed child did not survive `--kill-child` teardown);
- Claude subscription auth in the isolated mount view: PASS using the existing credential file rebound read-only, with no credential contents copied into experiment artifacts.

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

- `A2_PUBLIC_BRIEF.md` sha256 `6e0d914556a7865937543c5c818de3bf5c0de82bc67f90a511d16cd0090d1245`
- `provider_replay.py` sha256 `7dcb4e375a99265a8c2a7314fe6afa1948d0069ee0dfe32dea7e1a8cf373e416`
- `public_sample.json` sha256 `5eebc807ee9f4e7c39967eb216138bebc12677f0b58820ba95649373a4922a44`

Replacement held-out artifact hashes (stored on the Windows host and absent from the WSL worker filesystem during scored execution):

- evaluator sha256 `9012158262447f3266a9031b92ac92d343b35af8cf588947a8e1d9b04bb3e644`
- hidden request sha256 `b74bc639db9c5d7e8d7d21d72d92108ca822738e56de5f6a7c8e564c75aa59d0`
- hidden replay sha256 `992ca05a4f5b579be06e0495f965dc55d96ff149107db99574efbe4f0b13bf7a`
- negative-control procedure sha256 `d06cf8f971979c54ac38bf52de2f7aa314100e34507e3020e0906d8e7c2ebc86`
- treatment provenance hook sha256 `53a4cb616ab6f0a087ad7756a1439343405435ca9a539de05f3b21b001a86c56`

The earlier encrypted archive `aca-a2-heldout-20260921.enc` is superseded and will not be used for A3 scoring because its decryption key is unavailable in the current recoverable execution path.

Instrument validation before scoring:

- a reference implementation written only from the public brief passed **35/35 behavioral checks** with the treatment hook skipped;
- a deliberate combined mutant (dropped failed dispositions, swallowed warnings, prospect/follower ranking, credential leak, nondeterministic extra output) failed **16 checks**, proving the evaluator turns red on multiple independent defects;
- treatment provenance checks were exercised separately: explicit reasoned rejection passes without a use claim; declared use passes only when runtime instrumentation observes the retained Product N `collect()` call; declared use without that call fails as bypass;
- the evaluator installs a socket guard before each black-box run and fails any live network attempt.

## Gates before A3

- [x] Public task and replay artifacts hashed/frozen.
- [x] Public replay support tests pass (13 focused tests).
- [x] Held-out evaluator and hidden replay authored independently from the scored workers.
- [x] Held-out hashes recorded.
- [x] Evaluator reference pass and negative control pass.
- [x] Worker execution/model/isolation preflight passes; the initial same-user path failure is repaired by a host-side Windows holdout plus user/mount/PID namespace isolation and child-process teardown.
- [x] Same scored command/model is available to both arms (`claude-sonnet-5`, direct Claude Code auto mode).
- [x] Product N rights confirmed for private reuse arm.
- [x] Authorized retained Product N artifact frozen with exact hash/revision.
- [x] No scored worker has seen hidden evaluator content (no scored worker has started).

All A2 gates are now satisfied. A3 may start with the control and reuse workers as fresh sessions. The Windows-held evaluator remains outside the scored namespace and is used only after each worker exits and its submission is frozen.
