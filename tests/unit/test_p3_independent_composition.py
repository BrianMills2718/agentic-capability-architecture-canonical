"""
P3 independent composition pilot: direct function tests with negative controls.

Tests exercise reusable composition boundaries:
- structural_adapter: field name mapping
- semantic_reject: forbidden semantic assumptions
- approval_gated_handoff: review-gated handoff preparation
- IdempotentLocalSink: deduplicating local sink

Each test includes positive and negative controls.
"""

import json
import sys
from pathlib import Path

IC_MODULE = Path(__file__).resolve().parent.parent.parent / "docs" / "experiments" / "independent-composition"
sys.path.insert(0, str(IC_MODULE))

import pytest

from python_baseline import (
    structural_adapter,
    semantic_reject,
    approval_gated_handoff,
    IdempotentLocalSink,
    run_normal_composition,
    run_structural_adapter_test,
    run_semantic_rejection_test,
    run_approval_binding_test,
    run_retry_duplicate_test,
)


@pytest.fixture
def cases_fixture():
    """Load frozen acceptance cases."""
    path = IC_MODULE / "fixtures" / "CASES.json"
    return json.loads(path.read_text())


class TestStructuralAdapter:
    """Direct tests of field mapping adapter function."""

    def test_adapter_maps_fields_correctly(self):
        """Positive: valid field mapping succeeds."""
        producer = {"source_id": "cand-001", "sender": "@user", "content": "text"}
        mapping = {"candidate_id": "source_id", "name": "sender", "text": "content"}

        result = structural_adapter(producer, mapping)

        assert result == {"candidate_id": "cand-001", "name": "@user", "text": "text"}

    def test_adapter_raises_on_missing_producer_key(self):
        """Negative: missing producer key raises KeyError."""
        producer = {"source_id": "cand-001", "sender": "@user"}
        mapping = {"candidate_id": "source_id", "text": "content"}

        with pytest.raises(KeyError, match="content"):
            structural_adapter(producer, mapping)

    def test_adapter_handles_empty_mapping(self):
        """Edge: empty mapping returns empty dict."""
        producer = {"a": 1, "b": 2}
        result = structural_adapter(producer, {})
        assert result == {}

    def test_adapter_preserves_value_types(self):
        """Adapter preserves value types without conversion."""
        producer = {
            "id": "cand-001",
            "score": 0.95,
            "signals": ["a", "b"],
            "metadata": {"key": "value"},
        }
        mapping = {"candidate_id": "id", "relevance": "score", "list": "signals", "obj": "metadata"}

        result = structural_adapter(producer, mapping)

        assert result["relevance"] == 0.95
        assert result["list"] == ["a", "b"]
        assert result["obj"] == {"key": "value"}


class TestSemanticReject:
    """Direct tests of semantic mismatch rejection function."""

    def test_rejects_user_id_to_account_mapping(self):
        """Negative control: rejects user_id without explicit lookup."""
        data = {"user_id": "x-user-42", "score": 0.9}
        patterns = [
            {
                "field": "user_id",
                "maps_to": "crm_account_id",
                "risk": "user_id should not map to crm_account_id without lookup",
            }
        ]

        rejection = semantic_reject(data, patterns)

        assert rejection is not None
        assert "user_id" in rejection or "crm_account_id" in rejection

    def test_rejects_confidence_as_business_relevance(self):
        """Negative control: rejects confidence as business_relevance_score."""
        data = {"confidence": 0.99, "model": "bert"}
        patterns = [
            {
                "field": "confidence",
                "maps_to": "business_relevance_score",
                "risk": "confidence != business_relevance_score",
            }
        ]

        rejection = semantic_reject(data, patterns)

        assert rejection is not None

    def test_accepts_when_no_risk_fields_present(self):
        """Positive: returns None when no risk patterns match."""
        data = {"candidate_id": "cand-001", "text": "some content"}
        patterns = [
            {"field": "user_id", "risk": "..."},
            {"field": "confidence", "risk": "..."},
        ]

        rejection = semantic_reject(data, patterns)

        assert rejection is None

    def test_multiple_forbidden_patterns(self):
        """Test multiple patterns; first match returns rejection."""
        data = {"user_id": "x-user-42", "confidence": 0.99}
        patterns = [
            {"field": "user_id", "risk": "user_id risk"},
            {"field": "confidence", "risk": "confidence risk"},
        ]

        rejection = semantic_reject(data, patterns)

        assert rejection is not None


class TestApprovalGatedHandoff:
    """Direct tests of approval-gated handoff preparation."""

    def test_handoff_created_on_shortlist(self):
        """Positive: shortlist decision creates handoff."""
        candidate = {"candidate_id": "cand-001", "name": "@user"}
        handoff = approval_gated_handoff(candidate, "shortlist")

        assert handoff is not None
        assert handoff["candidate_id"] == "cand-001"
        assert "handoff:" in handoff["handoff_id"]

    def test_no_handoff_on_reject(self):
        """Negative control: reject decision does not create handoff."""
        candidate = {"candidate_id": "cand-001"}
        handoff = approval_gated_handoff(candidate, "reject")

        assert handoff is None

    def test_no_handoff_on_unreviewed(self):
        """Negative control: unreviewed does not create handoff."""
        candidate = {"candidate_id": "cand-003"}
        handoff = approval_gated_handoff(candidate, "unreviewed")

        assert handoff is None

    def test_no_handoff_on_unknown_decision(self):
        """Negative control: unknown decision does not create handoff."""
        candidate = {"candidate_id": "cand-001"}
        handoff = approval_gated_handoff(candidate, "pending")

        assert handoff is None

    def test_high_score_does_not_bypass_approval_gate(self):
        """Negative control: even 0.99 score does not bypass gate."""
        candidate = {"candidate_id": "cand-020", "score": 0.99}
        handoff = approval_gated_handoff(candidate, "reject")

        assert handoff is None


class TestIdempotentLocalSink:
    """Direct tests of idempotent local sink."""

    def test_first_call_records_handoff(self):
        """Positive: first record_handoff for ID creates effect."""
        sink = IdempotentLocalSink()
        handoff = {
            "candidate_id": "cand-030",
            "handoff_id": "handoff:cand-030:v1",
            "status": "prepared",
        }

        receipt = sink.record_handoff(handoff)

        assert receipt["new_record"] is True
        assert receipt["total_recorded"] == 1

    def test_second_call_deduplicates(self):
        """Negative control: second call for same ID does not increase count."""
        sink = IdempotentLocalSink()
        handoff = {
            "candidate_id": "cand-030",
            "handoff_id": "handoff:cand-030:v1",
            "status": "prepared",
        }

        sink.record_handoff(handoff)
        receipt2 = sink.record_handoff(handoff)

        assert receipt2["new_record"] is False
        assert receipt2["total_recorded"] == 1

    def test_different_ids_increase_count(self):
        """Positive: different IDs each create separate effects."""
        sink = IdempotentLocalSink()

        for i in range(3):
            handoff = {
                "candidate_id": f"cand-{i:03d}",
                "handoff_id": f"handoff:cand-{i:03d}:v1",
                "status": "prepared",
            }
            sink.record_handoff(handoff)

        assert sink.get_total_effects() == 3

    def test_repeated_invocation_max_one_effect(self):
        """Negative control: 2 invocations for same ID ≤ 1 effect."""
        sink = IdempotentLocalSink()
        handoff = {
            "candidate_id": "cand-030",
            "handoff_id": "handoff:cand-030:v1",
            "status": "prepared",
        }

        for _ in range(2):
            sink.record_handoff(handoff)

        effects = sink.get_total_effects()
        assert effects <= 1


class TestNormalCompositionCase:
    """Test normal-composition case execution."""

    def test_normal_composition_passes(self, cases_fixture):
        """Complete normal-composition case passes."""
        result = run_normal_composition(cases_fixture)
        assert result["passed"] is True
        assert result["review_ids"] == ["cand-001", "cand-002"]
        assert result["shortlist_ids"] == ["cand-001"]

    def test_normal_case_derives_shortlist_from_explicit_review_decisions(self, cases_fixture):
        """Shortlist must derive from explicit review decisions, not hardcoded IDs."""
        review_decisions = {
            "cand-001": "shortlist",
            "cand-002": "reject",
            "cand-003": "unreviewed",
        }
        result = run_normal_composition(cases_fixture, review_decisions=review_decisions)
        assert result["passed"]
        assert result["shortlist_ids"] == ["cand-001"]

    def test_different_review_decision_changes_handoff(self, cases_fixture):
        """Negative control: different review decision changes handoff result."""
        review_decisions_alt = {
            "cand-001": "reject",
            "cand-002": "shortlist",
            "cand-003": "unreviewed",
        }
        result = run_normal_composition(cases_fixture, review_decisions=review_decisions_alt)
        # cand-001 now rejects despite high score; cand-002 now shortlists
        assert result["shortlist_ids"] == ["cand-002"]
        assert "cand-001" not in result["shortlist_ids"]

    def test_score_alone_does_not_determine_shortlist(self, cases_fixture):
        """Negative control: score (0.91, 0.78) does not determine shortlist without review decision."""
        review_decisions_none = {
            "cand-001": "reject",
            "cand-002": "reject",
            "cand-003": "unreviewed",
        }
        result = run_normal_composition(cases_fixture, review_decisions=review_decisions_none)
        # Even though cand-001 scores 0.91, reject decision prevents handoff
        assert result["shortlist_ids"] == []


class TestStructuralAdapterCase:
    """Test structural-adapter case."""

    def test_structural_adapter_case_passes(self, cases_fixture):
        """Structural adapter maps fields correctly."""
        result = run_structural_adapter_test(cases_fixture)
        assert result["passed"] is True


class TestSemanticRejectionCase:
    """Test semantic-mismatch case."""

    def test_semantic_mismatch_is_rejected(self, cases_fixture):
        """Semantic mismatch is correctly rejected."""
        result = run_semantic_rejection_test(cases_fixture)
        assert result["passed"] is True
        assert "rejected_reason" in result


class TestApprovalBindingCase:
    """Test approval-binding case."""

    def test_approval_binding_enforced(self, cases_fixture):
        """Score 0.99 with reject decision produces no handoff."""
        result = run_approval_binding_test(cases_fixture)
        assert result["passed"] is True
        assert result["handoff_created"] is False


class TestRetryDuplicateCase:
    """Test retry-duplicate case."""

    def test_retry_duplicate_is_idempotent(self, cases_fixture):
        """Repeated handoff preparation creates at most 1 effect."""
        result = run_retry_duplicate_test(cases_fixture)
        assert result["passed"] is True
        assert result["total_effects"] <= result["expected_max"]
