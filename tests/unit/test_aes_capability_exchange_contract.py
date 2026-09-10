"""Contract tests for the AES-to-catalog capability exchange."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


SCHEMA = Path(__file__).resolve().parents[2] / "schemas" / "aes_capability_exchange.schema.json"


def _validator() -> Draft202012Validator:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def test_selection_response_and_reuse_receipt_validate() -> None:
    validator = _validator()
    response = {
        "schema_version": "1.0",
        "message_kind": "selection_response",
        "request_id": "aes-demo-1",
        "catalog_revision": "catalog@abc123",
        "selected": [{
            "semantic_action_id": "state.transition.plan",
            "owner": "na_core",
            "version": "1.0.0",
            "public_interface": "na_core.transitions.plan",
            "evidence": [{"kind": "test", "reference": "tests/test_transitions.py::test_plan"}],
            "limitations": ["No external consumer evidence yet"]
        }],
        "rejected": [{"candidate": "legacy.transition", "reason": "not a verified export"}],
        "uncovered_gaps": []
    }
    receipt = {
        "schema_version": "1.0",
        "message_kind": "reuse_receipt",
        "request_id": "aes-demo-1",
        "catalog_revision": "catalog@abc123",
        "semantic_action_id": "state.transition.plan",
        "observed_result": "succeeded",
        "evidence": [{"kind": "observation", "reference": "runs/aes-demo-1.json"}],
        "adaptations": [],
        "failure_reason": None
    }

    assert not list(validator.iter_errors(response))
    assert not list(validator.iter_errors(receipt))


def test_exchange_rejects_untyped_response_fields() -> None:
    validator = _validator()
    malformed = {
        "schema_version": "1.0",
        "message_kind": "selection_response",
        "request_id": "aes-demo-1",
        "catalog_revision": "catalog@abc123",
        "selected": [],
        "rejected": [],
        "uncovered_gaps": [],
        "untyped": "not allowed"
    }

    assert list(validator.iter_errors(malformed))
