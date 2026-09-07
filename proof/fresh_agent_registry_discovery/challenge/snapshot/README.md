# Portable Capability Snapshot

This directory is generated from the canonical capability registry. It contains a dependency-closed set of runtime packages, capability metadata, stable source-tree digests, and an offline verifier.

Requested: core, approvals, notifications, scheduling

Resolved: core, approvals, notifications, scheduling

Verify after copying or installation:

```bash
python verify_export.py
```

Generated installer metadata such as `*.egg-info`, build directories, and caches are deliberately excluded from source digests.
