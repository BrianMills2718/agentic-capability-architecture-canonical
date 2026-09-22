# ACA-PLAN-002 A3/A4 Result — Control vs Reuse

Recorded: 2026-09-22  
Plan: ACA-PLAN-002  
Status: read-only control/reuse tranche complete; A5 effect-safety canary deferred.

## Question

Does access to accumulated Product N capability work let a fresh worker deliver Product N+1 more correctly or economically than competent ordinary engineering after publication, discovery, and adaptation cost are considered?

This result separates:

- delivery correctness;
- worker time/model usage;
- actual asset use versus rejection;
- publication cost, which remained incompletely measured in A1.

It does not claim a universal result from one pair.

## Frozen instrument

The scored pair used the A2 instrument frozen before either worker began:

- public brief sha256: `6e0d914556a7865937543c5c818de3bf5c0de82bc67f90a511d16cd0090d1245`
- provider replay helper sha256: `7dcb4e375a99265a8c2a7314fe6afa1948d0069ee0dfe32dea7e1a8cf373e416`
- public sample sha256: `5eebc807ee9f4e7c39967eb216138bebc12677f0b58820ba95649373a4922a44`
- Product N revision: `ab2cfba0e8c43f0198716dee4414dedf2212d478`
- private treatment wheel sha256: `0cd030d9379d4ca823d8471b504a367cf1270a21598801442a6bc283bd279dcd`
- model/harness: direct Claude Code subscription CLI, `claude-sonnet-5`
- Python: 3.12
- live provider calls: none
- production effects: none

The held-out evaluator was authored outside the scored worker repositories and validated before scoring with a passing reference plus a deliberately broken mutant. Scored workers did not receive evaluator or hidden-fixture content.

### Setup-invalid attempt retained

The first attempted control launch did not reach the model API and produced no implementation. The isolation wrapper had hidden all of `/mnt`; on WSL, `/etc/resolv.conf` resolves through `/mnt/wsl/resolv.conf`, so the wrapper broke DNS and Claude returned `EAI_AGAIN`.

Classification: **harness/setup defect**, not control failure.

Repair: hide the Windows drive mount (`/mnt/c`) while preserving `/mnt/wsl`. The exact repaired namespace preflight reached `claude-sonnet-5` successfully. The setup-invalid attempt is not included in scored metrics.

## Scored submissions

| Metric | Control — ordinary engineering | Treatment — Product N asset available |
| --- | ---: | ---: |
| Worker session | `76878539-eda2-4f21-9a2b-4e981791bf52` | `83cf052d-1220-407d-a002-607292229531` |
| Frozen commit | `dbe7023c93e7bfbbe83f40d300932279b34bbee2` | `3c5ee95829722c570e1643dc98376655941e759d` |
| Wall time | 295 s | 374 s |
| Worker exit | 0 | 0 |
| Submission-local tests | 12 passed | 5 passed |
| Solution LOC | 343 | 377 |
| Test LOC | 230 | 213 |
| Hidden behavioral checks | 33 / 35 | 35 / 35 |
| Treatment provenance | n/a | passed |
| Incremental cash charged by experiment | $0 | $0 |
| Claude reported list-basis model cost* | $0.7371982 | $1.3181074 |
| Asset outcome | not available | **rejected** |

\* The Claude JSON reports an equivalent/list-basis model cost. These runs used the existing Claude subscription, so the experiment incurred no separate metered model charge. The list-basis number is retained only as a comparable usage signal.

### Control result

The control built the product directly from the public behavior contract.

Its hidden score was **33/35**. The only failed checks were:

- `warning_for_missing_text`
- `warning_for_missing_handle`

All other hidden checks passed, including partial provider failure, global post identity/conflict handling, author aggregation, provenance, ranking/limit semantics, deterministic output, credential secrecy, all-query-failure behavior, and network blocking.

This is a near-pass, but the frozen evaluator required all mandatory checks, so the first control submission was **not accepted**.

### Treatment result

The treatment passed **35/35 behavioral checks** and its treatment-provenance check.

However, it did **not consume** the retained Product N `collect()` capability. It inspected the pinned asset and explicitly rejected it in `reuse_decision.json`.

The worker recorded two categories of reason:

1. **Environment/publication friction:** the supplied wheel's model surface depended on Pydantic while the scored worker was constrained to the offline task environment.
2. **Semantic mismatch:** the retained Product N behavior included prospecting-specific candidate ranking and aggregation semantics that conflicted with the frozen Product N+1 behavior, including:
   - prospect/founder/follower-oriented prefilter ranking instead of recency + handle ordering;
   - profile ownership semantics inconsistent with the first-valid-occurrence rule;
   - no required conflicting-global-post warning behavior;
   - all-query-failure behavior inconsistent with the required result document.

The worker concluded that adapting around those differences would require implementing essentially the Product N+1 aggregation/ranking core anyway, and chose a small local implementation instead.

The treatment provenance evaluator accepted that as a legitimate **rejection**, not a silent bypass.

## Paired comparison

Relative to control, the treatment took:

- **79 seconds longer**
- **26.8% more wall time**
- approximately **78.8% more list-basis model cost**
- 34 more solution LOC

The treatment did improve first-submission correctness from 33/35 to 35/35.

That correctness difference cannot honestly be called a successful **reuse** result, because the retained asset was rejected and not executed by the submitted solution. It is, at most, preliminary evidence that exposing a candidate asset can help a worker make an explicit fit/rejection decision while still delivering locally.

The experiment therefore supports two different statements:

### Supported

- a fresh treatment worker can inspect a plausible accumulated asset and **reject it for concrete semantic and operational reasons** rather than force reuse;
- the A1 publication audit correctly identified real publication/dependency debt;
- ordinary local/provider-native implementation remained sufficient for the Product N+1 task;
- no ACA runtime, workflow engine, registry service, semantic compiler, or other new infrastructure was needed.

### Not supported

- that the retained Product N asset reduced delivery time;
- that it reduced model/context cost;
- that it reduced implementation surface;
- that actual Product N behavior was composed into Product N+1;
- that accumulated capability work economically compounded in this case;
- that the treatment correctness advantage was caused by reusable code rather than extra scrutiny/context.

## Frozen economic criterion

The plan proposed a practical positive threshold of at least **20% accepted-delivery-time improvement in both fresh pairs**, with no increase in marginal model/tool spending or human intervention.

The first pair already fails that criterion: treatment was 26.8% slower and used materially more model context/list-basis cost.

A second pair cannot make the condition "improvement in both pairs" true. The optional confirmation pair is therefore **not run**. This is a stop-rule application, not post-hoc threshold tuning.

## First-use versus later-use economics

A1 did not instrument publication/normalization active engineering time precisely enough to compute an honest first-use dollar/time return. That remains **unknown**, not zero.

The later-use worker comparison is directly observed and unfavorable to reuse economics in this case:

- control: 295 s
- treatment: 374 s

Because the treatment rejected the asset, the extra treatment effort included asset inspection/rejection rather than adapter implementation.

## A4 decision

Classification: **no demonstrated reuse advantage for this asset/task; useful selection/rejection evidence**.

Decision:

- do not promote the Product N collection boundary on this evidence;
- do not create an ACA abstraction to make this asset fit;
- keep the current prior-art-first architecture posture;
- prefer the simpler local/provider-native implementation for this Product N+1 behavior;
- retain the rejection evidence so a later agent does not rediscover the same mismatch blindly.

## A5 effect-safety canary

Deferred.

The scored Product N+1 task is read-only and this experiment makes no new effectful-composition readiness claim. Under ACA-PLAN-002, A5 is not required to close the read-only tranche.

If a real future product needs effectful reuse, ADR-014 exact-action approval binding plus durable idempotency/retry behavior should be tested then, using established application/runtime mechanisms.

## A6 closeout

Read-only tranche outcome: **complete, bounded negative for economic reuse; positive for explicit rejection discipline.**

No new ACA machinery was added or justified.

The next useful evidence should come from either:

1. a real product where a pre-existing capability has a plausible semantic fit and can be discovered without being named; or
2. a real recurring failure that survives native contracts, ordinary packaging, examples, consumer contracts, provider/runtime features, and consumer-local adapters.

Do not continue refining the Twitter case merely to obtain a positive reuse result.
