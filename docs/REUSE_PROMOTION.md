# Reuse and Promotion

The repository distinguishes **observing reusable potential** from **promoting shared infrastructure**.

## Default lifecycle

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

## Evidence thresholds

- **Local / observed:** one project. Keep the behavior local.
- **Candidate:** there is a credible reuse hypothesis or a second use is emerging.
- **Proven:** at least two materially different projects depend on the same generalized behavior.
- **Core:** at least a third materially different use has exercised the abstraction without breaking prior consumers, unless the capability is explicitly marked foundational.

The tool `tools/check_reuse_evidence.py` prevents `proven`/`core` labels from getting ahead of evidence.

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

## Promotion rule

When a second materially different project needs similar behavior, compare the two uses before extracting. Generalize the shared behavior, add both projects to the capability's evidence, and protect both with compatibility tests.

A third use is a deliberate stress test of the abstraction rather than an excuse to add more special cases.
