#!/usr/bin/env python3
"""Small live-composition runner for ACA P3.

This intentionally stops at an explicit human review boundary unless review
decisions are supplied by the caller. It performs no outreach and no production
CRM mutation.

CLI usage:
  live_pipeline.py '<query>'
  live_pipeline.py '<query>' --review-threshold 0.75
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from python_baseline import IdempotentLocalSink, approval_gated_handoff
from twitterapi_io_collection import ProviderAccessError, search_candidates


SIGNALS: tuple[tuple[str, float, str], ...] = (
    ("agentic", 0.35, "agentic topic"),
    ("coding agent", 0.35, "explicit coding-agent topic"),
    ("developer", 0.15, "developer context"),
    ("engineering", 0.15, "engineering context"),
    ("tool", 0.15, "tooling context"),
    ("workflow", 0.15, "workflow context"),
    ("code review", 0.25, "code-review context"),
)


def deterministic_score(candidate: dict[str, Any]) -> dict[str, Any]:
    """Temporary deterministic scorer for composition testing, not prediction."""
    text = str(candidate.get("tweet_text") or "").casefold()
    score = 0.0
    signals: list[str] = []
    for needle, weight, label in SIGNALS:
        if needle in text:
            score += weight
            signals.append(label)
    score = min(round(score, 2), 1.0)
    return {
        **candidate,
        "relevance_score": score,
        "signals": signals,
        "scoring_method": "p3-deterministic-integration-v1",
    }


def compose_run(
    candidates: list[dict[str, Any]],
    *,
    review_threshold: float = 0.7,
    review_decisions: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Score, route to review, and optionally prepare approved local handoffs."""
    scored = [deterministic_score(candidate) for candidate in candidates]
    review_queue = [
        candidate
        for candidate in scored
        if candidate["relevance_score"] >= review_threshold
    ]

    sink = IdempotentLocalSink()
    handoffs: list[dict[str, Any]] = []
    if review_decisions is not None:
        for candidate in review_queue:
            decision = review_decisions.get(candidate["source_candidate_id"], "unreviewed")
            handoff = approval_gated_handoff(
                {"candidate_id": candidate["source_candidate_id"]},
                decision,
            )
            if handoff:
                handoffs.append(sink.record_handoff(handoff))

    return {
        "candidate_count": len(candidates),
        "scored_count": len(scored),
        "review_threshold": review_threshold,
        "review_count": len(review_queue),
        "review_queue": review_queue,
        "handoff_count": sink.get_total_effects(),
        "handoffs": handoffs,
        "assertions": {
            "production_crm_write": False,
            "outbound_message_sent": False,
            "score_alone_authorizes_handoff": False,
        },
        "nonclaims": [
            "deterministic integration score is not a conversion or commercial-value prediction",
            "collection success does not establish provider coverage or long-term reliability",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Live composition runner for ACA P3 Twitter Prospector."
    )
    parser.add_argument("query", help="Twitter search query")
    parser.add_argument(
        "--review-threshold",
        type=float,
        default=0.7,
        help="Minimum relevance score to route to review (default: 0.7)",
    )

    args = parser.parse_args()

    try:
        candidates = search_candidates(args.query)
    except ProviderAccessError as exc:
        print(json.dumps({"ok": False, "stage": "collection", "error": str(exc)}))
        return 1

    receipt = compose_run(candidates, review_threshold=args.review_threshold)
    print(
        json.dumps(
            {
                "ok": True,
                "query": args.query,
                "scoring_revision": "p3-deterministic-integration-v1",
                **receipt,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
