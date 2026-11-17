.PHONY: capability-list capability-describe capability-catalog-check engagement-new engagement-validate engagement-close

capability-list:
	python tools/capability_catalog.py list --json

capability-describe:
	@test -n "$(ACTION)" || (echo "Usage: make capability-describe ACTION=approval.resolve" >&2; exit 2)
	python tools/capability_catalog.py describe "$(ACTION)" --json

capability-catalog-check:
	python tools/capability_catalog.py check

engagement-new:
	@test -n "$(ID)" -a -n "$(TASK)" || (echo "Usage: make engagement-new ID=job_001 TASK=/path/to/TASK.md [OUTPUT=/path]" >&2; exit 2)
	python tools/engagement.py new "$(ID)" --task "$(TASK)" $(if $(OUTPUT),--output "$(OUTPUT)",)

engagement-validate:
	@test -n "$(WORKSPACE)" || (echo "Usage: make engagement-validate WORKSPACE=/path/to/workspace" >&2; exit 2)
	python tools/engagement.py validate "$(WORKSPACE)" --require-ready

engagement-close:
	@test -n "$(WORKSPACE)" || (echo "Usage: make engagement-close WORKSPACE=/path/to/workspace" >&2; exit 2)
	python tools/engagement.py close "$(WORKSPACE)"

.PHONY: fast check docs-specs
unexport GIT_DIR GIT_INDEX_FILE GIT_WORK_TREE GIT_PREFIX GIT_COMMON_DIR GIT_OBJECT_DIRECTORY
docs-specs:
	@mkdir -p docs/specs/capability-catalog
	@ln -sfn ../../../openspec/specs/capability-catalog/spec.md docs/specs/capability-catalog/spec.md
fast:
	uv run lockstep check trace
	uv run lockstep check sources
	uv run lockstep check project --check
	openspec validate --all --strict --no-interactive
check: docs-specs fast
	uv run python -m pytest
	uv run lockstep check arch check
