"""Tests for exact AES capability selection through the live catalog."""

from __future__ import annotations

import subprocess

import pytest

from tools.aes_capability_exchange import ExchangeError, catalog_revision, resolve_selection_request


def _request() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "message_kind": "selection_request",
        "request_id": "aes-catalog-test",
        "catalog_revision": catalog_revision(),
        "outcomes": ["produce one planned state transition"],
        "constraints": [],
        "capability_categories": ["state.transition.plan"],
        "evidence_level": "tested",
        "runtime_constraints": [],
    }


def test_exact_catalog_action_is_selected_from_verified_exports() -> None:
    response = resolve_selection_request(_request())

    assert response["uncovered_gaps"] == []
    assert response["selected"] == [{
        "semantic_action_id": "state.transition.plan",
        "owner": "core",
        "version": "0.1.0",
        "public_interface": "na_core.transitions.plan_transition",
        "evidence": [
            {"kind": "artifact", "reference": "capabilities/core/capability.yml"},
            {
                "kind": "artifact",
                "reference": "capabilities/core/frappe_app/na_core/na_core/transitions.py",
            },
        ],
        "limitations": [
            "Selection is exact semantic-action ID matching; runtime constraints are retained but not evaluated.",
        ],
    }]


def test_unknown_exact_action_is_reported_as_uncovered_without_guessing() -> None:
    request = _request()
    request["capability_categories"] = ["state.transition.unknown"]

    response = resolve_selection_request(request)

    assert response["selected"] == []
    assert response["uncovered_gaps"] == ["state.transition.unknown"]


def test_stale_catalog_revision_fails_loudly() -> None:
    request = _request()
    request["catalog_revision"] = "not-the-current-revision"

    with pytest.raises(ExchangeError, match="catalog revision mismatch"):
        resolve_selection_request(request)
