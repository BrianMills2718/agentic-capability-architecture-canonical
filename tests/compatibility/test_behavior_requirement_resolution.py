from copy import deepcopy

import yaml

from tools.capability_catalog import build_publication
from tools.resolve_behavior_requirements import ResolutionError, resolve


def _io(name: str, contract_id: str, source=None) -> dict:
    item = {"name": name, "contract_id": contract_id}
    if source is not None:
        item["source"] = source
    return item


def _external() -> dict:
    return {"kind": "external"}


def _from(requirement_id: str, output_name: str) -> dict:
    return {"kind": "requirement_output", "requirement_id": requirement_id, "output_name": output_name}


def requirements_fixture():
    return {
        "schema_version": "1.0",
        "source_system_spec": {"id": "spec:test", "path": "spec.yml"},
        "requirements": [
            {
                "id": "req:approval",
                "semantic_action": "policy.resolve",
                "purpose": "resolve policy",
                "inputs": [_io("facts", "test.facts/1", _external()), _io("rules", "test.rules/1", _external())],
                "required_outputs": [_io("decision", "test.decision/1")],
                "invariants": ["domain invariant preserved"],
                "provenance": {"source_clause": "clause:test"},
            },
            {
                "id": "req:transition",
                "semantic_action": "state.transition",
                "purpose": "transition state",
                "inputs": [
                    _io("decision", "test.decision/1", _from("req:approval", "decision")),
                    _io("state_ref", "test.state/1", _external()),
                    _io("transition_spec", "test.transition-spec/1", _external()),
                    _io("actor_ref", "test.actor/1", _external()),
                ],
                "required_outputs": [_io("transition_result", "test.transition/1")],
                "provenance": {"source_clause": "clause:test"},
            },
            {
                "id": "req:notify",
                "semantic_action": "notification.send",
                "purpose": "notify",
                "inputs": [
                    _io("transition_result", "test.transition/1", _from("req:transition", "transition_result")),
                    _io("recipients", "test.recipients/1", _external()),
                    _io("subject", "test.subject/1", _external()),
                    _io("message", "test.message/1", _external()),
                ],
                "required_outputs": [_io("delivery_ref", "test.delivery/1")],
                "provenance": {"source_clause": "clause:test"},
            },
        ],
    }


def publication_fixture():
    return build_publication()


def test_manifest_derived_publication_matches_legacy_bindings():
    derived = publication_fixture()
    legacy = yaml.safe_load(open("architecture/publication/capability_publication_v1.yaml").read())

    def essential(publication):
        return {
            action["semantic_action"]: (
                action["capability_owner"],
                action["selected_implementation"],
                action["composition_implementation_ref"],
                tuple(action["semantic_contract"]["inputs"]),
                tuple(action["semantic_contract"]["outputs"]),
            )
            for action in publication["published_actions"]
        }

    assert essential(derived) == essential(legacy)


def test_resolves_all_published_actions_and_preserves_contracts_sources_and_provenance():
    result = resolve(requirements_fixture(), publication_fixture())
    assert [b["semantic_action"] for b in result["bindings"]] == ["policy.resolve", "state.transition", "notification.send"]
    first = result["bindings"][0]
    assert first["selected_implementation"] == "na_approvals.engine.resolve"
    assert first["composition_implementation_ref"] == "na_approvals.engine.resolve/1"
    assert first["provenance"]["source_clause"] == "clause:test"
    assert first["requirement_invariants"] == ["domain invariant preserved"]
    assert first["input_contracts"] == {"facts": "test.facts/1", "rules": "test.rules/1"}
    assert first["input_sources"] == {"facts": _external(), "rules": _external()}
    assert first["output_contracts"] == {"decision": "test.decision/1"}


def test_unknown_action_fails_typed():
    reqs = requirements_fixture()
    reqs["requirements"][0]["semantic_action"] = "unknown.action"
    try:
        resolve(reqs, publication_fixture())
    except ResolutionError as exc:
        assert exc.code == "UNKNOWN_SEMANTIC_ACTION"
    else:
        raise AssertionError("expected typed resolution failure")


def test_missing_input_fails_typed():
    reqs = requirements_fixture()
    reqs["requirements"][0]["inputs"] = [_io("facts", "test.facts/1", _external())]
    try:
        resolve(reqs, publication_fixture())
    except ResolutionError as exc:
        assert exc.code == "INPUT_CONTRACT_MISMATCH"
        assert "rules" in exc.detail
    else:
        raise AssertionError("expected typed resolution failure")


def test_missing_input_source_fails_typed():
    reqs = requirements_fixture()
    reqs["requirements"][0]["inputs"][0].pop("source")
    try:
        resolve(reqs, publication_fixture())
    except ResolutionError as exc:
        assert exc.code == "INPUT_SOURCE_MISSING"
        assert "facts" in exc.detail
    else:
        raise AssertionError("expected typed resolution failure")


def test_missing_output_fails_typed():
    reqs = requirements_fixture()
    reqs["requirements"][0]["required_outputs"] = [_io("decision", "test.decision/1"), _io("audit_ref", "test.audit/1")]
    try:
        resolve(reqs, publication_fixture())
    except ResolutionError as exc:
        assert exc.code == "OUTPUT_CONTRACT_MISMATCH"
        assert "audit_ref" in exc.detail
    else:
        raise AssertionError("expected typed resolution failure")


def test_duplicate_publication_fails_typed():
    publication = publication_fixture()
    publication["published_actions"].append(deepcopy(publication["published_actions"][0]))
    try:
        resolve(requirements_fixture(), publication)
    except ResolutionError as exc:
        assert exc.code == "AMBIGUOUS_PUBLICATION"
    else:
        raise AssertionError("expected typed resolution failure")


def test_shipment_exception_reuses_only_core_and_notifications():
    requirements = {
        "schema_version": "1.0",
        "source_system_spec": {"id": "spec:shipment-exception-v1", "path": "shipment.yml"},
        "requirements": [
            {
                "id": "req:shipment-transition",
                "semantic_action": "state.transition",
                "purpose": "acknowledge shipment exception",
                "inputs": [
                    _io("state_ref", "shipment.state/1", _external()),
                    _io("transition_spec", "shipment.transition-spec/1", _external()),
                    _io("actor_ref", "shipment.actor/1", _external()),
                ],
                "required_outputs": [_io("transition_result", "shipment.transition-result/1")],
                "provenance": {"source_clause": "clause:shipment-exception-acknowledge"},
            },
            {
                "id": "req:shipment-notify",
                "semantic_action": "notification.send",
                "purpose": "notify shipment owner",
                "inputs": [
                    _io("recipients", "notification.recipients/1", _external()),
                    _io("subject", "notification.subject/1", _external()),
                    _io("message", "notification.message/1", _external()),
                    _io("transition_result", "shipment.transition-result/1", _from("req:shipment-transition", "transition_result")),
                ],
                "required_outputs": [_io("delivery_ref", "notification.delivery-ref/1")],
                "provenance": {"source_clause": "clause:shipment-exception-notify"},
            },
        ],
    }
    result = resolve(requirements, publication_fixture())
    assert [binding["semantic_action"] for binding in result["bindings"]] == ["state.transition", "notification.send"]
    assert [binding["capability_owner"] for binding in result["bindings"]] == ["core", "notifications"]
    assert all(binding["capability_owner"] not in {"approvals", "scheduling"} for binding in result["bindings"])
