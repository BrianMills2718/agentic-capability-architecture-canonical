"""Tests for Engineering Signal Digest consumer."""

import json
import sys
from pathlib import Path

import pytest

# Add the independent-composition module to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "docs" / "experiments" / "independent-composition"))

from engineering_signal_digest import (
    SignalItem,
    EngineeringSignalDigest,
    AdapterError,
    adapt_candidates_to_signals,
    generate_digest,
)


class TestSignalItem:
    """Test SignalItem dataclass."""

    def test_signal_item_creation(self):
        """Test basic signal item creation."""
        sig = SignalItem(
            signal_id="sig-abc123",
            author="@user1",
            text="Some engineering insight",
            source_url="https://x.com/i/status/123",
        )
        assert sig.signal_id == "sig-abc123"
        assert sig.author == "@user1"
        assert sig.text == "Some engineering insight"
        assert sig.source_url == "https://x.com/i/status/123"


class TestEngineeringSignalDigest:
    """Test digest aggregation."""

    def test_digest_creation(self):
        """Test digest creation with items."""
        items = [
            SignalItem(
                signal_id="sig-1",
                author="@alice",
                text="Python is great",
                source_url="https://x.com/i/status/1",
            ),
            SignalItem(
                signal_id="sig-2",
                author="@bob",
                text="Rust is fast",
                source_url="https://x.com/i/status/2",
            ),
        ]
        digest = EngineeringSignalDigest(
            query="programming languages",
            item_count=2,
            unique_author_count=2,
            items=items,
        )
        assert digest.query == "programming languages"
        assert digest.item_count == 2
        assert digest.unique_author_count == 2
        assert len(digest.items) == 2

    def test_digest_to_dict(self):
        """Test digest serialization to dict."""
        items = [
            SignalItem(
                signal_id="sig-1",
                author="@alice",
                text="Test",
                source_url="https://x.com/i/status/1",
            ),
        ]
        digest = EngineeringSignalDigest(
            query="test",
            item_count=1,
            unique_author_count=1,
            items=items,
        )
        result = digest.to_dict()
        assert result["query"] == "test"
        assert result["item_count"] == 1
        assert result["unique_author_count"] == 1
        assert len(result["items"]) == 1
        assert result["items"][0]["author"] == "@alice"

    def test_digest_to_json(self):
        """Test digest JSON serialization."""
        items = [
            SignalItem(
                signal_id="sig-1",
                author="@alice",
                text="Test",
                source_url="https://x.com/i/status/1",
            ),
        ]
        digest = EngineeringSignalDigest(
            query="test",
            item_count=1,
            unique_author_count=1,
            items=items,
        )
        json_str = digest.to_json()
        parsed = json.loads(json_str)
        assert parsed["query"] == "test"
        assert parsed["item_count"] == 1


class TestAdapterStructure:
    """Test structural adapter from search_candidates to signals."""

    def test_adapt_single_candidate(self):
        """Test adapter with a single candidate."""
        candidates = [
            {
                "source_candidate_id": "x-post:123",
                "author_handle": "@alice",
                "tweet_text": "Great insight",
                "provider_post_id": "123",
                "source_url": "https://x.com/i/status/123",
            }
        ]
        signals = adapt_candidates_to_signals(candidates)
        assert len(signals) == 1
        assert signals[0].signal_id == "x-post:123"
        assert signals[0].author == "@alice"
        assert signals[0].text == "Great insight"
        assert signals[0].source_url == "https://x.com/i/status/123"

    def test_adapt_multiple_candidates(self):
        """Test adapter with multiple candidates."""
        candidates = [
            {
                "source_candidate_id": "x-post:1",
                "author_handle": "@alice",
                "tweet_text": "First",
                "provider_post_id": "1",
                "source_url": "https://x.com/i/status/1",
            },
            {
                "source_candidate_id": "x-post:2",
                "author_handle": "@bob",
                "tweet_text": "Second",
                "provider_post_id": "2",
                "source_url": "https://x.com/i/status/2",
            },
        ]
        signals = adapt_candidates_to_signals(candidates)
        assert len(signals) == 2
        assert signals[0].signal_id == "x-post:1"
        assert signals[1].signal_id == "x-post:2"

    def test_deduplication_by_source_candidate_id(self):
        """Test that duplicate source_candidate_id entries are deduplicated."""
        candidates = [
            {
                "source_candidate_id": "x-post:1",
                "author_handle": "@alice",
                "tweet_text": "First",
                "provider_post_id": "1",
                "source_url": "https://x.com/i/status/1",
            },
            {
                "source_candidate_id": "x-post:1",
                "author_handle": "@alice",
                "tweet_text": "First",
                "provider_post_id": "1",
                "source_url": "https://x.com/i/status/1",
            },
        ]
        signals = adapt_candidates_to_signals(candidates)
        assert len(signals) == 1

    def test_deduplication_preserves_order(self):
        """Test that deduplication preserves first occurrence order."""
        candidates = [
            {
                "source_candidate_id": "x-post:1",
                "author_handle": "@alice",
                "tweet_text": "Alice",
                "provider_post_id": "1",
                "source_url": "https://x.com/i/status/1",
            },
            {
                "source_candidate_id": "x-post:2",
                "author_handle": "@bob",
                "tweet_text": "Bob",
                "provider_post_id": "2",
                "source_url": "https://x.com/i/status/2",
            },
            {
                "source_candidate_id": "x-post:3",
                "author_handle": "@charlie",
                "tweet_text": "Charlie",
                "provider_post_id": "3",
                "source_url": "https://x.com/i/status/3",
            },
        ]
        signals = adapt_candidates_to_signals(candidates)
        assert len(signals) == 3
        assert signals[0].signal_id == "x-post:1"
        assert signals[1].signal_id == "x-post:2"
        assert signals[2].signal_id == "x-post:3"

    def test_empty_candidates_list(self):
        """Test adapter with empty candidates list."""
        candidates: list[dict] = []
        signals = adapt_candidates_to_signals(candidates)
        assert len(signals) == 0


class TestAdapterErrorHandling:
    """Test negative controls: required fields must not be silently invented."""

    def test_missing_source_candidate_id(self):
        """Test that missing source_candidate_id raises AdapterError."""
        candidates = [
            {
                "source_candidate_id": "",
                "author_handle": "@alice",
                "tweet_text": "Text",
                "source_url": "https://x.com/i/status/1",
            }
        ]
        with pytest.raises(AdapterError, match="source_candidate_id"):
            adapt_candidates_to_signals(candidates)

    def test_missing_author_handle(self):
        """Test that missing author_handle raises AdapterError."""
        candidates = [
            {
                "source_candidate_id": "x-post:1",
                "author_handle": "",
                "tweet_text": "Text",
                "source_url": "https://x.com/i/status/1",
            }
        ]
        with pytest.raises(AdapterError, match="author_handle"):
            adapt_candidates_to_signals(candidates)

    def test_missing_tweet_text(self):
        """Test that missing tweet_text raises AdapterError."""
        candidates = [
            {
                "source_candidate_id": "x-post:1",
                "author_handle": "@alice",
                "tweet_text": "",
                "source_url": "https://x.com/i/status/1",
            }
        ]
        with pytest.raises(AdapterError, match="tweet_text"):
            adapt_candidates_to_signals(candidates)

    def test_missing_source_url(self):
        """Test that missing source_url raises AdapterError."""
        candidates = [
            {
                "source_candidate_id": "x-post:1",
                "author_handle": "@alice",
                "tweet_text": "Text",
                "source_url": "",
            }
        ]
        with pytest.raises(AdapterError, match="source_url"):
            adapt_candidates_to_signals(candidates)

    def test_whitespace_only_fields_treated_as_missing(self):
        """Test that whitespace-only fields are treated as missing."""
        candidates = [
            {
                "source_candidate_id": "   ",
                "author_handle": "@alice",
                "tweet_text": "Text",
                "source_url": "https://x.com/i/status/1",
            }
        ]
        with pytest.raises(AdapterError, match="source_candidate_id"):
            adapt_candidates_to_signals(candidates)


class TestGenerateDigest:
    """Test digest generation with mocked search function."""

    def test_generate_digest_with_mock_search(self):
        """Test full digest generation with mock search function."""
        mock_candidates = [
            {
                "source_candidate_id": "x-post:1",
                "author_handle": "@alice",
                "tweet_text": "Python tip",
                "provider_post_id": "1",
                "source_url": "https://x.com/i/status/1",
            },
            {
                "source_candidate_id": "x-post:2",
                "author_handle": "@bob",
                "tweet_text": "Rust guide",
                "provider_post_id": "2",
                "source_url": "https://x.com/i/status/2",
            },
        ]

        def mock_search(query: str) -> list[dict]:
            return mock_candidates

        digest = generate_digest("programming", mock_search)
        assert digest.query == "programming"
        assert digest.item_count == 2
        assert digest.unique_author_count == 2

    def test_generate_digest_empty_results(self):
        """Test digest generation with no results."""
        def mock_search(query: str) -> list[dict]:
            return []

        digest = generate_digest("obscure topic", mock_search)
        assert digest.query == "obscure topic"
        assert digest.item_count == 0
        assert digest.unique_author_count == 0
        assert len(digest.items) == 0

    def test_generate_digest_unique_author_count(self):
        """Test that unique_author_count counts distinct authors."""
        mock_candidates = [
            {
                "source_candidate_id": "x-post:1",
                "author_handle": "@alice",
                "tweet_text": "First",
                "provider_post_id": "1",
                "source_url": "https://x.com/i/status/1",
            },
            {
                "source_candidate_id": "x-post:2",
                "author_handle": "@alice",
                "tweet_text": "Second",
                "provider_post_id": "2",
                "source_url": "https://x.com/i/status/2",
            },
            {
                "source_candidate_id": "x-post:3",
                "author_handle": "@bob",
                "tweet_text": "Third",
                "provider_post_id": "3",
                "source_url": "https://x.com/i/status/3",
            },
        ]

        def mock_search(query: str) -> list[dict]:
            return mock_candidates

        digest = generate_digest("test", mock_search)
        assert digest.item_count == 3
        assert digest.unique_author_count == 2  # Only @alice and @bob

    def test_signal_ids_use_source_candidate_id(self):
        """Test that signal_ids are sourced directly from source_candidate_id."""
        mock_candidates = [
            {
                "source_candidate_id": "x-post:1",
                "author_handle": "@alice",
                "tweet_text": "First",
                "provider_post_id": "1",
                "source_url": "https://x.com/i/status/1",
            },
            {
                "source_candidate_id": "x-post:2",
                "author_handle": "@bob",
                "tweet_text": "Second",
                "provider_post_id": "2",
                "source_url": "https://x.com/i/status/2",
            },
        ]

        def mock_search(query: str) -> list[dict]:
            return mock_candidates

        digest = generate_digest("test", mock_search)
        assert digest.items[0].signal_id == "x-post:1"
        assert digest.items[1].signal_id == "x-post:2"


class TestIdentityPreservation:
    """Test that boundary identity is correctly preserved."""

    def test_source_candidate_id_becomes_signal_id(self):
        """Test that source_candidate_id from boundary becomes signal_id in digest."""
        candidates = [
            {
                "source_candidate_id": "x-post:123",
                "author_handle": "@alice",
                "tweet_text": "Insight",
                "provider_post_id": "123",
                "source_url": "https://x.com/i/status/123",
            },
        ]
        signals = adapt_candidates_to_signals(candidates)
        assert signals[0].signal_id == "x-post:123"

    def test_source_url_preserved(self):
        """Test that source URLs are preserved in signals."""
        candidates = [
            {
                "source_candidate_id": "x-post:123",
                "author_handle": "@alice",
                "tweet_text": "Insight",
                "provider_post_id": "123",
                "source_url": "https://x.com/i/status/123",
            },
        ]
        signals = adapt_candidates_to_signals(candidates)
        assert signals[0].source_url == "https://x.com/i/status/123"

    def test_author_preserved(self):
        """Test that author handles are preserved exactly."""
        candidates = [
            {
                "source_candidate_id": "x-post:1",
                "author_handle": "@alice",
                "tweet_text": "Text",
                "provider_post_id": "1",
                "source_url": "https://x.com/i/status/1",
            },
        ]
        signals = adapt_candidates_to_signals(candidates)
        assert signals[0].author == "@alice"

    def test_text_preserved(self):
        """Test that tweet text is preserved exactly."""
        text = "This is a very specific engineering insight about distributed systems"
        candidates = [
            {
                "source_candidate_id": "x-post:1",
                "author_handle": "@alice",
                "tweet_text": text,
                "provider_post_id": "1",
                "source_url": "https://x.com/i/status/1",
            },
        ]
        signals = adapt_candidates_to_signals(candidates)
        assert signals[0].text == text
