from copy import deepcopy

import pytest

from tools.run_semantic_federation_canary import CanaryError, run_canary


def _input(name, contract_id, source):
    return {"name": name, "contract_id": contract_id, "source": source}


def _output(name, contract_id):
    return {"name": name, "contract_id": contract_id}


def _requirement(requirement_id, action, inputs, outputs, transitions=()):
    return {
        "id": requirement_id,
        "semantic_action": action,
        "purpose": requirement_id,
        "inputs": inputs,
        "required_outputs": outputs,
        "invariants": [],
        "semantic_context": {
            "entity_types": ["biz:Appointment"],
            "role_bindings": [],
            "business_rules": [
                {
                    "id": "rule:long_appointment_requires_approval",
                    "scope": "biz:Appointment",
                    "priority": 1,
                    "when": {
                        "all": [
                            {
                                "compare": {
                                    "left": {"property": "rel:durationMinutes", "subject": "$appointment"},
                                    "operator": ">",
                                    "right": {"literal": 90},
                                }
                            }
                        ]
                    },
                    "conclude": {"approval_request": {"approver_type": "biz:Manager"}},
                    "provenance": {"source_clause": "clause:approval"},
                }
            ],
            "lifecycle_transitions": list(transitions),
            "configuration_values": [],
        },
        "provenance": {
            "source_clauses": [
                {"id": "clause:approval", "text": "Appointments over 90 minutes require manager approval."},
                {"id": "clause:reminder", "text": "Confirmed appointments get an email reminder 24 hours ahead."},
            ]
        },
    }


def _transition(transition_id, value=None):
    effects = [{"emit": {"event": "evt:test"}}]
    if value is not None:
        effects.insert(0, {"set": {"property": "rel:appointmentState", "subject": "$appointment", "value": value}})
    return {"id": transition_id, "trigger": "evt:test", "effects": effects}


def canary_fixture():
    external = {"kind": "external"}
    from_approval = {
        "kind": "requirement_output",
        "requirement_id": "req:approval",
        "output_name": "decision",
    }
    from_transition = {
        "kind": "requirement_output",
        "requirement_id": "req:transition",
        "output_name": "notification_request",
    }
    payload = {
        "schema_version": "1.0",
        "status": "supported",
        "source_system_spec": {"id": "spec:appointment", "version": "1.0", "semantic_spec_sha256": "a" * 64},
        "requirements": [
            _requirement(
                "req:approval",
                "approval.resolve",
                [_input("facts", "contract:facts/v1", external)],
                [_output("decision", "contract:decision/v1")],
                [
                    _transition("transition:appointment_requires_approval"),
                    _transition("transition:appointment_allow", "confirmed"),
                ],
            ),
            _requirement(
                "req:transition",
                "state.transition.plan",
                [_input("decision", "contract:decision/v1", from_approval)],
                [
                    _output("transition_result", "contract:transition/v1"),
                    _output("notification_request", "contract:notification-request/v1"),
                ],
                [
                    _transition("transition:appointment_approval_granted", "confirmed"),
                    _transition("transition:appointment_approval_rejected", "blocked"),
                    _transition("transition:schedule_appointment_reminder"),
                ],
            ),
            _requirement(
                "req:notify",
                "notification.email.send",
                [_input("notification_request", "contract:notification-request/v1", from_transition)],
                [_output("delivery", "contract:delivery/v1")],
            ),
        ],
    }
    payload["requirements"][1]["semantic_context"]["configuration_values"] = [
        {
            "path": ["cap:Notification", "cap:notification.defaultReminderOffsetMinutes"],
            "value": -1440,
        }
    ]
    payload["requirements"][2]["semantic_context"]["configuration_values"] = [
        {"path": ["cap:Notification", "delivery_channel"], "value": "email"}
    ]
    return payload


def assert_code(payload, code):
    with pytest.raises(CanaryError) as caught:
        run_canary(payload)
    assert caught.value.code == code


def test_canary_resolves_actions_preserves_branches_and_validates_graph():
    result = run_canary(canary_fixture())
    assert result["result"] == "pass"
    assert [row["action_id"] for row in result["resolved_actions"]] == [
        "approval.resolve",
        "state.transition.plan",
        "notification.email.send",
    ]
    assert result["graph_validation"]["order"] == ["req:approval", "req:transition", "req:notify"]
    assert result["semantic_parameters"]["approval_threshold_minutes"] == 90
    assert result["semantic_parameters"]["reminder_offset_minutes"] == -1440
    assert result["side_effects_executed"] is False


def test_missing_approval_branch_fails_visibly():
    payload = canary_fixture()
    payload["requirements"][0]["semantic_context"]["lifecycle_transitions"] = [
        _transition("transition:appointment_allow", "confirmed")
    ]
    assert_code(payload, "APPROVAL_BRANCH_MISSING")


def test_unresolved_action_fails_visibly():
    payload = canary_fixture()
    payload["requirements"][0]["semantic_action"] = "approval.missing"
    assert_code(payload, "UNRESOLVED_ACTION")


def test_incompatible_edge_fails_visibly():
    payload = canary_fixture()
    payload["requirements"][1]["inputs"][0]["contract_id"] = "contract:wrong/v1"
    assert_code(payload, "INCOMPATIBLE_GRAPH")


def test_missing_provenance_fails_visibly():
    payload = canary_fixture()
    payload["requirements"][0].pop("provenance")
    assert_code(payload, "PROVENANCE_MISSING")


def test_wrong_canary_parameter_fails_visibly():
    payload = canary_fixture()
    payload["requirements"][0]["semantic_context"]["business_rules"][0]["when"]["all"][0]["compare"]["right"]["literal"] = 75
    assert_code(payload, "CANARY_PARAMETER_MISMATCH")
