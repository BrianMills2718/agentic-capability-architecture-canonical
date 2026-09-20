from __future__ import annotations

import importlib.util
from pathlib import Path


MODULE_DIR = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "experiments"
    / "independent-composition"
)
import sys
sys.path.insert(0, str(MODULE_DIR))

spec = importlib.util.spec_from_file_location("live_pipeline", MODULE_DIR / "live_pipeline.py")
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def candidate(candidate_id: str, text: str):
    return {
        "source_candidate_id": candidate_id,
        "author_handle": "@builder",
        "tweet_text": text,
        "provider_post_id": candidate_id,
        "source_url": f"https://x.com/i/status/{candidate_id}",
    }


def test_deterministic_score_is_explicit_and_bounded():
    result = module.deterministic_score(
        candidate("1", "Agentic engineering developer workflow tooling")
    )
    assert 0 <= result["relevance_score"] <= 1
    assert result["relevance_score"] >= 0.7
    assert result["scoring_method"] == "p3-deterministic-integration-v1"
    assert result["signals"]


def test_low_signal_candidate_stays_below_review_threshold():
    receipt = module.compose_run([candidate("1", "A general research announcement.")])
    assert receipt["review_count"] == 0
    assert receipt["handoff_count"] == 0


def test_score_routes_to_review_but_does_not_authorize_handoff():
    receipt = module.compose_run(
        [candidate("1", "Agentic engineering developer workflow tooling")]
    )
    assert receipt["review_count"] == 1
    assert receipt["handoff_count"] == 0
    assert receipt["assertions"]["score_alone_authorizes_handoff"] is False


def test_explicit_shortlist_can_prepare_local_handoff():
    receipt = module.compose_run(
        [candidate("1", "Agentic engineering developer workflow tooling")],
        review_decisions={"1": "shortlist"},
    )
    assert receipt["review_count"] == 1
    assert receipt["handoff_count"] == 1
    assert receipt["handoffs"][0]["new_record"] is True


def test_explicit_reject_blocks_handoff():
    receipt = module.compose_run(
        [candidate("1", "Agentic engineering developer workflow tooling")],
        review_decisions={"1": "reject"},
    )
    assert receipt["review_count"] == 1
    assert receipt["handoff_count"] == 0


def test_pipeline_receipt_keeps_external_effects_disabled():
    receipt = module.compose_run([])
    assert receipt["assertions"]["production_crm_write"] is False
    assert receipt["assertions"]["outbound_message_sent"] is False


def test_custom_review_threshold_reduces_review_queue():
    """Threshold behavior is independent of CLI: higher threshold = fewer reviews."""
    candidates = [
        candidate("1", "Agentic engineering"),  # score ~0.7
        candidate("2", "Engineering tooling"),  # score ~0.3
    ]
    receipt_low = module.compose_run(candidates, review_threshold=0.3)
    receipt_high = module.compose_run(candidates, review_threshold=0.8)
    assert receipt_low["review_count"] >= receipt_high["review_count"]


def test_threshold_does_not_affect_approval_requirement():
    """Score does not authorize handoff regardless of threshold.

    Threshold only controls routing to review, not approval gating.
    """
    candidates = [candidate("1", "Agentic engineering")]
    receipt = module.compose_run(candidates, review_threshold=0.5)
    assert receipt["review_count"] == 1
    assert receipt["handoff_count"] == 0  # score still doesn't authorize


def test_threshold_zero_routes_all_to_review():
    """Threshold 0.0 routes any scored candidate to review."""
    candidates = [
        candidate("1", "General announcement"),  # low score
        candidate("2", "Agentic engineering"),   # high score
    ]
    receipt = module.compose_run(candidates, review_threshold=0.0)
    assert receipt["review_count"] == 2


def test_threshold_one_blocks_all_review():
    """Threshold 1.0 blocks all candidates from review (no score can reach 1.0+)."""
    candidates = [
        candidate("1", "Agentic engineering developer workflow tooling"),  # max ~0.95
    ]
    receipt = module.compose_run(candidates, review_threshold=1.0)
    assert receipt["review_count"] == 0
    assert receipt["handoff_count"] == 0
