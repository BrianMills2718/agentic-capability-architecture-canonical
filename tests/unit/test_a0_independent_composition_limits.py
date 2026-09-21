"""ACA-PLAN-002 A0 probes: make the limits of the P3/P5 pilot code executable.

These are characterization tests. They pin what the pilot fixtures actually do so
that prose claims ("durable idempotency", "approval binding", "semantic
compatibility checking", "resilient to null") cannot drift above the code. A
passing test here documents a *limitation*, not production safety. If a limit is
later removed, the corresponding test should be updated deliberately.

The one behavior change made in A0 is the explicit-None regression test for the
Engineering Signal Digest adapter.
"""

import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

IC_DIR = (
    Path(__file__).resolve().parent.parent.parent
    / "docs"
    / "experiments"
    / "independent-composition"
)
sys.path.insert(0, str(IC_DIR))

from engineering_signal_digest import AdapterError, adapt_candidates_to_signals
from live_pipeline import compose_run
from python_baseline import (
    IdempotentLocalSink,
    approval_gated_handoff,
    semantic_reject,
)
from twitterapi_io_collection import search_candidates

REQUIRED_FIELDS = ("source_candidate_id", "author_handle", "tweet_text", "source_url")


def _candidate(**overrides):
    base = {
        "source_candidate_id": "x-post:1",
        "author_handle": "@builder",
        "tweet_text": "text",
        "provider_post_id": "1",
        "source_url": "https://x.com/i/status/1",
    }
    base.update(overrides)
    return base


# --- Engineering Signal Digest adapter: null handling (regression) -----------


@pytest.mark.parametrize("field", REQUIRED_FIELDS)
def test_adapter_rejects_explicit_none_with_adapter_error(field):
    """Regression: an explicit None used to escape as AttributeError from .strip()."""
    with pytest.raises(AdapterError, match=field):
        adapt_candidates_to_signals([_candidate(**{field: None})])


@pytest.mark.parametrize("field", REQUIRED_FIELDS)
def test_adapter_rejects_non_string_with_adapter_error(field):
    with pytest.raises(AdapterError, match=field):
        adapt_candidates_to_signals([_candidate(**{field: 123})])


def test_adapter_none_error_reports_original_value_type():
    with pytest.raises(AdapterError) as exc:
        adapt_candidates_to_signals([_candidate(author_handle=None)])
    assert "author_handle" in str(exc.value)
    assert "NoneType" in str(exc.value)


def test_adapter_still_accepts_a_valid_candidate():
    signals = adapt_candidates_to_signals([_candidate()])
    assert [s.signal_id for s in signals] == ["x-post:1"]


# --- Boundary: malformed list entries are dropped without a trace -------------


class _FakeResponse:
    def __init__(self, body: bytes):
        self._body = body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def read(self):
        return self._body


def test_search_candidates_drops_non_object_tweets_without_returned_signal():
    """Limitation: a non-dict entry is absent from the returned candidate list.

    The boundary returns only a list of candidates and exposes no warning or
    per-item disposition in that return value, so the consumer cannot infer the
    dropped malformed item from the returned contract alone.
    """
    body = b'{"tweets": ["not-an-object", {"id": "1", "text": "hi", "author": {"userName": "a"}}]}'

    def opener(request, timeout):
        return _FakeResponse(body)

    result = search_candidates("q", api_key="k", opener=opener)
    assert [c["source_candidate_id"] for c in result] == ["x-post:1"]


# --- IdempotentLocalSink: process-local, not durable --------------------------

HANDOFF = {
    "candidate_id": "cand-030",
    "handoff_id": "handoff:cand-030:v1",
    "status": "prepared-local-only",
}


def test_sink_dedup_does_not_span_sink_instances():
    """A second sink instance has no memory of the first: the effect repeats."""
    first, second = IdempotentLocalSink(), IdempotentLocalSink()
    assert first.record_handoff(HANDOFF)["new_record"] is True
    assert second.record_handoff(HANDOFF)["new_record"] is True


def test_sink_dedup_does_not_survive_a_new_process():
    """Same logical handoff in two interpreter processes yields two 'new' effects."""
    script = textwrap.dedent(
        f"""
        import sys
        sys.path.insert(0, {str(IC_DIR)!r})
        from python_baseline import IdempotentLocalSink
        print(IdempotentLocalSink().record_handoff({HANDOFF!r})["new_record"])
        """
    )
    outputs = [
        subprocess.run(
            [sys.executable, "-c", script], capture_output=True, text=True, check=True
        ).stdout.strip()
        for _ in range(2)
    ]
    assert outputs == ["True", "True"]


def test_compose_run_creates_a_fresh_sink_per_call():
    """Repeating the same approved run re-creates the handoff; no state is shared."""
    candidates = [_candidate(tweet_text="Agentic engineering developer workflow tooling")]
    decisions = {"x-post:1": "shortlist"}
    first = compose_run(candidates, review_threshold=0.5, review_decisions=decisions)
    second = compose_run(candidates, review_threshold=0.5, review_decisions=decisions)
    assert first["handoffs"][0]["new_record"] is True
    assert second["handoffs"][0]["new_record"] is True


def test_sink_hides_conflicting_content_for_the_same_handoff_id():
    """Same key, different content: reported as a duplicate, conflict undetected."""
    sink = IdempotentLocalSink()
    sink.record_handoff(HANDOFF)
    conflicting = {**HANDOFF, "status": "sent"}
    receipt = sink.record_handoff(conflicting)
    assert receipt["new_record"] is False
    assert sink.recorded_ids[HANDOFF["handoff_id"]]["status"] == "prepared-local-only"


# --- approval_gated_handoff: a string gate, not an exact-action binding -------


def test_approval_gate_is_not_bound_to_the_payload():
    """The 'shortlist' decision is a bare string; changed candidate content still passes.

    This is not ADR-014 exact-action binding (`approval.action.bind/verify`), which
    the pilot code does not use.
    """
    approved = approval_gated_handoff({"candidate_id": "c1", "note": "A"}, "shortlist")
    changed = approval_gated_handoff({"candidate_id": "c1", "note": "B"}, "shortlist")
    assert approved == changed
    assert "note" not in approved


# --- semantic_reject: field-presence check only --------------------------------


def test_semantic_reject_fires_on_field_presence_alone():
    """Rejection depends only on the field name being present, not on any mapping."""
    pattern = [{"field": "user_id", "maps_to": "crm_account_id", "risk": "r"}]
    # Nobody is mapping user_id to anything, and the value is None: still rejected.
    assert semantic_reject({"user_id": None}, pattern) == "Semantic risk: r"


def test_semantic_reject_ignores_maps_to():
    """`maps_to` is documentation only; a different target gives the same result."""
    a = semantic_reject({"user_id": "u"}, [{"field": "user_id", "maps_to": "x", "risk": "r"}])
    b = semantic_reject({"user_id": "u"}, [{"field": "user_id", "maps_to": "y", "risk": "r"}])
    assert a == b == "Semantic risk: r"


def test_semantic_reject_silently_ignores_pattern_without_risk():
    """A pattern with no `risk` string never rejects, even when the field is present."""
    assert semantic_reject({"user_id": "u"}, [{"field": "user_id", "maps_to": "crm"}]) is None


def test_semantic_reject_does_not_detect_a_renamed_field():
    """Same meaning under another key passes: no semantic equivalence is checked."""
    pattern = [{"field": "user_id", "maps_to": "crm_account_id", "risk": "r"}]
    assert semantic_reject({"uid": "x-user-42"}, pattern) is None
