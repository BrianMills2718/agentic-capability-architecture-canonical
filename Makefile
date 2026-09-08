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
