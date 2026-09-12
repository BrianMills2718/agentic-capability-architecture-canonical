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


def _reuse_receipt_v2() -> dict[str, object]:
    return {
        "schema_version": "2.0",
        "message_kind": "reuse_receipt",
        "request_id": "aes-demo-1",
        "catalog_revision": "20b43074cbe012005e23f30fdf07d7553709657b",
        "semantic_action_id": "state.transition.plan",
        "observed_result": "succeeded",
        "evidence": [{
            "kind": "observation",
            "artifact_ref": {
                "repository_record_id": "consumer-repo",
                "revision": "0123456789abcdef0123456789abcdef01234567",
                "relative_path": "evidence/runs/aes-demo-1.json",
            },
        }],
        "adaptations": [],
        "failure_reason": None,
    }


def test_v2_reuse_receipt_requires_portable_revision_bound_evidence() -> None:
    validator = _validator()
    receipt = _reuse_receipt_v2()

    assert not list(validator.iter_errors(receipt))


def test_v1_reuse_receipt_remains_valid_for_legacy_evidence_strings() -> None:
    validator = _validator()
    receipt = _reuse_receipt_v2()
    receipt["schema_version"] = "1.0"
    receipt["evidence"] = [{"kind": "observation", "reference": "runs/aes-demo-1.json"}]

    assert not list(validator.iter_errors(receipt))


def test_v2_reuse_receipt_rejects_machine_local_or_ambiguous_evidence() -> None:
    validator = _validator()
    bad_refs = [
        {"repository_record_id": "consumer-repo", "revision": "0123456789abcdef0123456789abcdef01234567", "relative_path": "/tmp/run.json"},
        {"repository_record_id": "consumer-repo", "revision": "0123456789abcdef0123456789abcdef01234567", "relative_path": "../run.json"},
        {"repository_record_id": "consumer-repo", "revision": "main", "relative_path": "evidence/run.json"},
        {"repository_record_id": "consumer-repo", "revision": "0123456", "relative_path": "evidence/run.json"},
        {"repository_record_id": "consumer-repo", "revision": "sha256:not-a-digest", "relative_path": "evidence/run.json"},
        {"repository_record_id": "consumer-repo", "revision": "0123456789abcdef0123456789abcdef01234567", "relative_path": "evidence\\run.json"},
        {"repository_record_id": "consumer-repo", "revision": "0123456789abcdef0123456789abcdef01234567", "relative_path": "evidence//run.json"},
        {"repository_record_id": "consumer-repo", "revision": "0123456789abcdef0123456789abcdef01234567", "relative_path": "evidence/./run.json"},
        {"repository_record_id": "consumer-repo", "revision": "0123456789abcdef0123456789abcdef01234567", "relative_path": "evidence/../run.json"},
        {"repository_record_id": "consumer-repo", "revision": "0123456789abcdef0123456789abcdef01234567", "relative_path": "evidence/run/"},
    ]

    for artifact_ref in bad_refs:
        receipt = _reuse_receipt_v2()
        receipt["evidence"] = [{"kind": "observation", "artifact_ref": artifact_ref}]
        assert list(validator.iter_errors(receipt)), artifact_ref


def test_v2_reuse_receipt_rejects_unknown_evidence_reference_fields() -> None:
    validator = _validator()
    receipt = _reuse_receipt_v2()
    receipt["evidence"] = [{
        "kind": "observation",
        "artifact_ref": {
            "repository_record_id": "consumer-repo",
            "revision": "0123456789abcdef0123456789abcdef01234567",
            "relative_path": "evidence/run.json",
            "checkout_path": "/tmp/consumer",
        },
    }]

    assert list(validator.iter_errors(receipt))
