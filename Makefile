.PHONY: capability-list capability-describe capability-catalog-check

capability-list:
	python tools/capability_catalog.py list --json

capability-describe:
	@test -n "$(ACTION)" || (echo "Usage: make capability-describe ACTION=approval.resolve" >&2; exit 2)
	python tools/capability_catalog.py describe "$(ACTION)" --json

capability-catalog-check:
	python tools/capability_catalog.py check
