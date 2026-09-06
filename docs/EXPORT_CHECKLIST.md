# Final ZIP Checklist

Before treating an exported ZIP as the authoritative handoff, confirm:

- [ ] `README.md` explains the repository purpose.
- [ ] `AGENTS.md` contains the current coding-agent rules.
- [ ] `capability_registry.yml` reflects all shared capabilities.
- [ ] Every real project has a manifest.
- [ ] Shared capability manifests/interfaces are current.
- [ ] Project-specific code is under the relevant project/client directory.
- [ ] `docs/WORKING_CONTEXT.md` reflects the current design.
- [ ] `docs/DECISIONS.md` includes important architectural decisions.
- [ ] `CHANGELOG.md` records material bootstrap changes.
- [ ] Local tests pass with `python tools/check_bootstrap.py`.
- [ ] Frappe integration tests have been run in a real test site before production use.
- [ ] Fresh-agent acceptance test has been run before declaring the bootstrap complete.
- [ ] `python tools/export_zip.py` has been run after the final changes.
