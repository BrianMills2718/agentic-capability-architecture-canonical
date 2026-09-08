.PHONY: help check test proof doctor catalog

help:
	@printf '%s\n' \
	  'make check    - validate catalog and resolver compatibility' \
	  'make test     - run focused compatibility tests' \
	  'make proof    - run maintained semantic/provider/runtime proof tests' \
	  'make doctor   - verify required local tools are available' \
	  'make catalog  - print manifest-derived capability catalog as JSON'

check:
	python tools/capability_catalog.py publication --json >/dev/null
	python tools/validate_capability_publication.py
	python -m pytest -q tests/compatibility/test_behavior_requirement_resolution.py

test:
	python -m pytest -q tests/compatibility/test_behavior_requirement_resolution.py tests/compatibility/test_runtime_execution_receipts.py

proof:
	python -m pytest -q tests/compatibility/test_behavior_requirement_resolution.py tests/compatibility/test_milestone1_runtime_smoke.py tests/compatibility/test_runtime_execution_receipts.py

doctor:
	@command -v python >/dev/null || { echo 'python not found' >&2; exit 2; }
	@python -c 'import yaml' >/dev/null 2>&1 || { echo 'PyYAML not installed' >&2; exit 2; }
	@python -c 'import pytest' >/dev/null 2>&1 || { echo 'pytest not installed' >&2; exit 2; }
	@echo 'ok'

catalog:
	python tools/capability_catalog.py list --json
