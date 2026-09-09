# Reuse and Promotion

The repository distinguishes **observing reusable potential** from **promoting internal shared implementation**.

Promotion is only one part of the broader capability model. A repeated requirement may be best satisfied by a native platform feature, established ecosystem package, external service, standard protocol, existing internal capability, or a local implementation. Do not create/promote internal code merely because demand repeated if a better existing provider already satisfies the requirement.

## Default internal lifecycle

```text
project-local behavior
        ↓
reuse observation
        ↓
candidate capability
        ↓
proven capability
        ↓
core capability
```

## Minimum promotion thresholds

The repository's current mechanical threshold gate uses:

- **Local / observed:** one project. Keep the implementation local by default.
- **Candidate:** there is a credible reuse hypothesis or a second use is emerging.
- **Proven:** at least two materially different projects have actually exercised the same generalized behavior.
- **Core:** at least a third materially different use has exercised the abstraction without breaking prior consumers, unless the capability is explicitly marked foundational.

`tools/check_reuse_evidence.py` applies only to **non-foundation capabilities already labeled `proven` or `core`**. It does not certify candidate evidence quality, discover actual consumers, or prove that a package import exercised the capability's distinctive semantics. Its output states how many promoted capabilities it actually evaluated so a vacuous pass is visible.

At the current stage, candidate capabilities remain below that mechanical promotion gate. Their evidence must be reviewed directly rather than inferred from a green threshold check.

### What counts as a materially different use?

An import is not enough. The consumer should exercise the generalized behavior that justifies the abstraction.

For example, a rule resolver whose distinctive value is multi-rule arbitration, conflict detection, or priority handling has **not** demonstrated those properties merely because several projects each call `resolve([one_rule])`. That pattern is evidence that the package is being consumed, but it may also be negative evidence that the abstraction is broader than current client needs.

Record both positive and negative evidence. If a consumer uses only a trivial subset, say so explicitly rather than promoting maturity from project count alone.

The minimum counts are **necessary thresholds under the current checker, not a complete maturity model**. Promotion review should also consider, where relevant:

- domain and runtime diversity;
- which distinctive invariants real consumers actually exercised;
- interface stability and migration history;
- independent-agent or independent-consumer use;
- compatibility/regression evidence;
- failed or rejected fits;
- security and operational incidents;
- licensing/deployment constraints;
- whether extraction actually reduces duplication/coupling rather than hiding important domain semantics.

## Record without promoting

Use:

```bash
python tools/record_reuse_candidate.py \
  --id scheduling.duration_approval \
  --project acme_reference \
  --description "Approval based on appointment duration" \
  --evidence "ACME needs >120 minute approval"
```

This puts the observation in `reuse_candidates.yml`; it does not change shared code.

A project `LEARNINGS.md` should also record sourcing/rejection lessons that do not imply internal promotion—for example, that a native feature already satisfies the requirement, that an internal capability was deliberately rejected because its semantics were too narrow, or that repeated clients imported a package without exercising the abstraction's differentiating behavior.

## Promotion rule

When a second materially different project appears to need similar behavior:

1. re-run the capability/provider assessment rather than assuming internal extraction is correct;
2. compare successful, partial, failed, and rejected uses;
3. identify the narrow common semantic behavior, if one exists;
4. verify that the real consumers actually exercise that common behavior;
5. extract/promote only the stable surface;
6. bind it to honest public interfaces/semantic exports;
7. add compatibility evidence protecting known consumers.

A third use is a deliberate stress test of the abstraction rather than an excuse to add more special cases.

If the common surface remains unclear, runtime-specific, weakly exercised, or more costly than an established alternative, leave it local/candidate. More shared code is not itself success.
