#!/usr/bin/env python3
"""Engineering Signal Digest: a focused consumer of search_candidates boundary."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, asdict
from typing import Any, Callable


class AdapterError(RuntimeError):
    """Adapter validation error: required field missing from search_candidates result."""


@dataclass
class SignalItem:
    """A single signal item in the digest."""
    signal_id: str
    author: str
    text: str
    source_url: str


@dataclass
class EngineeringSignalDigest:
    """Aggregated signals for an engineering topic query."""
    query: str
    item_count: int
    unique_author_count: int
    items: list[SignalItem]

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return {
            "query": self.query,
            "item_count": self.item_count,
            "unique_author_count": self.unique_author_count,
            "items": [asdict(item) for item in self.items],
        }

    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON."""
        return json.dumps(self.to_dict(), indent=indent)


def adapt_candidates_to_signals(
    candidates: list[dict[str, Any]],
) -> list[SignalItem]:
    """Adapt search_candidates output to signal items with deduplication by source_candidate_id.

    Raises AdapterError if a candidate is missing required fields:
    source_candidate_id, author_handle, tweet_text, or source_url.
    """
    seen_candidates: set[str] = set()
    signals: list[SignalItem] = []

    for candidate in candidates:
        # Validate required fields from search_candidates boundary
        source_candidate_id = candidate.get("source_candidate_id", "").strip()
        author_handle = candidate.get("author_handle", "").strip()
        tweet_text = candidate.get("tweet_text", "").strip()
        source_url = candidate.get("source_url", "").strip()

        if not source_candidate_id:
            raise AdapterError("search_candidates result missing required source_candidate_id")
        if not author_handle:
            raise AdapterError("search_candidates result missing required author_handle")
        if not tweet_text:
            raise AdapterError("search_candidates result missing required tweet_text")
        if not source_url:
            raise AdapterError("search_candidates result missing required source_url")

        # Deduplicate by source_candidate_id (durable identity from boundary)
        if source_candidate_id in seen_candidates:
            continue

        seen_candidates.add(source_candidate_id)

        signals.append(
            SignalItem(
                signal_id=source_candidate_id,
                author=author_handle,
                text=tweet_text,
                source_url=source_url,
            )
        )

    return signals


def generate_digest(
    query: str,
    search_fn: Callable[[str], list[dict[str, Any]]],
) -> EngineeringSignalDigest:
    """Generate a signal digest for an engineering topic query.

    Args:
        query: The topic query string
        search_fn: A callable that takes query and returns search_candidates results

    Returns:
        EngineeringSignalDigest with aggregated signals
    """
    candidates = search_fn(query)
    signals = adapt_candidates_to_signals(candidates)

    unique_authors = {sig.author for sig in signals}
    unique_author_count = len(unique_authors)

    return EngineeringSignalDigest(
        query=query,
        item_count=len(signals),
        unique_author_count=unique_author_count,
        items=signals,
    )


def main() -> int:
    """CLI entry point."""
    if len(sys.argv) != 2:
        print("usage: engineering_signal_digest.py '<query>'", file=sys.stderr)
        return 2

    # Import the upstream boundary for CLI use
    try:
        from twitterapi_io_collection import search_candidates
    except ImportError as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": f"Cannot import twitterapi_io_collection: {exc}",
                }
            )
        )
        return 1

    try:
        digest = generate_digest(sys.argv[1], search_candidates)
        print(json.dumps({"ok": True, "digest": digest.to_dict()}, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
