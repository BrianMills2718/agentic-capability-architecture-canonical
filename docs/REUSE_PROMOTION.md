# Reuse and Promotion

The repository distinguishes **observing reusable potential** from **promoting internal shared implementation**.

Promotion is only one part of the broader sourcing model. A repeated requirement may be best satisfied by a native platform feature, established ecosystem package, external service, standard protocol, existing internal capability, or a local implementation. Do not create/promote internal code merely because demand repeated if a better existing provider already satisfies the requirement.

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

The repository's current mechanical checks use these minimum thresholds:

- **Local / observed:** one project. Keep the implementation local by default.
- **Candidate:** there is a credible reuse hypothesis or a second use is emerging.
- **Proven:** at least two materially different projects depend on the same generalized behavior.
- **Core:** at least a third materially different use has exercised the abstraction without breaking prior consumers, unless the capability is explicitly marked foundational.

`tools/check_reuse_evidence.py` prevents `proven`/`core` labels from getting ahead of those minimum reuse-count thresholds.

Those counts are **necessary evidence under the current checker, not a complete maturity model**. Promotion review should also consider, where relevant:

- domain and runtime diversity;
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

A project `LEARNINGS.md` should also record sourcing/rejection lessons that do not imply internal promotion—for example, that a native Frappe feature already satisfies the requirement or that an internal capability was deliberately rejected because its semantics were too narrow.

## Promotion rule

When a second materially different project needs similar behavior:

1. re-run the sourcing assessment rather than assuming internal extraction is correct;
2. compare the successful and failed/rejected uses;
3. identify the narrow common semantic behavior, if one exists;
4. extract/promote only that stable behavior;
5. bind it to honest public interfaces;
6. add compatibility evidence protecting known consumers.

A third use is a deliberate stress test of the abstraction rather than an excuse to add more special cases.

If the common surface remains unclear, runtime-specific, or more costly than an established external/native alternative, leave it local/candidate. More shared code is not itself success.
