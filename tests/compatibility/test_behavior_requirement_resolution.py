from copy import deepcopy

import yaml

from tools.resolve_behavior_requirements import ResolutionError, resolve


def requirements_fixture():
    return {
        "schema_version": "1.0",
        "source_system_spec": {"id": "spec:test", "path": "spec.yml"},
        "requirements": [
            {
                "id": "req:approval",
                "semantic_action": "policy.resolve",
                "purpose": "resolve policy",
                "inputs": [{"facts": "x"}, {"rules": "y"}],
                "required_outputs": ["decision"],
                "invariants": ["domain invariant preserved"],
                "provenance": {"source_clause": "clause:test"},
            },
            {
                "id": "req:transition",
                "semantic_action": "state.transition",
                "purpose": "transition state",
                "inputs": [
                    {"state_ref": "x"},
                    {"transition_spec": "y"},
                    {"actor_ref": "z"},
                ],
                "required_outputs": ["transition_result"],
                "provenance": {"source_clause": "clause:test"},
            },
            {
                "id": "req:notify",
                "semantic_action": "notification.send",
                "purpose": "notify",
                "inputs": [
                    {"recipients": "x"},
                    {"subject": "y"},
                    {"message": "z"},
                ],
                "required_outputs": ["delivery_ref"],
                "provenance": {"source_clause": "clause:test"},
            },
        ],
    }


def publication_fixture():
    return yaml.safe_load(
        open("architecture/publication/capability_publication_v1.yaml").read()
    )


def test_resolves_all_published_actions_and_preserves_provenance():
    result = resolve(requirements_fixture(), publication_fixture())
    assert [b["semantic_action"] for b in result["bindings"]] == [
        "policy.resolve",
        "state.transition",
        "notification.send",
    ]
    assert result["bindings"][0]["selected_implementation"] == "na_approvals.engine.resolve"
    assert result["bindings"][0]["provenance"]["source_clause"] == "clause:test"
    assert result["bindings"][0]["requirement_invariants"] == ["domain invariant preserved"]


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
    reqs["requirements"][0]["inputs"] = [{"facts": "x"}]
    try:
        resolve(reqs, publication_fixture())
    except ResolutionError as exc:
        assert exc.code == "INPUT_CONTRACT_MISMATCH"
        assert "rules" in exc.detail
    else:
        raise AssertionError("expected typed resolution failure")


def test_missing_output_fails_typed():
    reqs = requirements_fixture()
    reqs["requirements"][0]["required_outputs"] = ["decision", "audit_ref"]
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
