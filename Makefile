.PHONY: capability-list capability-describe capability-catalog-check engagement-new engagement-validate engagement-close semantic-federation-canary

capability-list:
	python tools/capability_catalog.py list --json

capability-describe:
	@test -n "$(ACTION)" || (echo "Usage: make capability-describe ACTION=approval.resolve" >&2; exit 2)
	python tools/capability_catalog.py describe "$(ACTION)" --json

capability-catalog-check:
	python tools/capability_catalog.py check

semantic-federation-canary:
	@test -n "$(COMPILER_REPO)" -a -n "$(COMPILER_REVISION)" || (echo "Usage: make semantic-federation-canary COMPILER_REPO=/path/to/compiler COMPILER_REVISION=<sha> [OUTPUT=proof/semantic_federation_canary/conformance.json]" >&2; exit 2)
	python tools/run_semantic_federation_canary.py \
		--compiler-repo "$(COMPILER_REPO)" \
		--compiler-revision "$(COMPILER_REVISION)" \
		--requirements-path "$(or $(REQUIREMENTS_PATH),14_target_neutral/examples/APPOINTMENT_BEHAVIOR_REQUIREMENTS_V1_0.json)" \
		$(if $(OUTPUT),--output "$(OUTPUT)",)

engagement-new:
	@test -n "$(ID)" -a -n "$(TASK)" || (echo "Usage: make engagement-new ID=job_001 TASK=/path/to/TASK.md [OUTPUT=/path]" >&2; exit 2)
	python tools/engagement.py new "$(ID)" --task "$(TASK)" $(if $(OUTPUT),--output "$(OUTPUT)",)

engagement-validate:
	@test -n "$(WORKSPACE)" || (echo "Usage: make engagement-validate WORKSPACE=/path/to/workspace" >&2; exit 2)
	python tools/engagement.py validate "$(WORKSPACE)" --require-ready

engagement-close:
	@test -n "$(WORKSPACE)" || (echo "Usage: make engagement-close WORKSPACE=/path/to/workspace" >&2; exit 2)
	python tools/engagement.py close "$(WORKSPACE)"
