from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "experiments"
    / "independent-composition"
    / "twitterapi_io_collection.py"
)
spec = importlib.util.spec_from_file_location("twitterapi_io_collection", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


def test_normalize_tweet_preserves_source_identity_and_text():
    result = module.normalize_tweet(
        {
            "id": "123",
            "text": "Building with coding agents.",
            "author": {"userName": "builder"},
        }
    )
    assert result == {
        "source_candidate_id": "x-post:123",
        "author_handle": "@builder",
        "tweet_text": "Building with coding agents.",
        "provider_post_id": "123",
        "source_url": "https://x.com/i/status/123",
    }


def test_normalize_tweet_rejects_missing_author():
    with pytest.raises(module.ProviderAccessError, match="author object"):
        module.normalize_tweet({"id": "123", "text": "hello"})


def test_search_candidates_uses_read_only_endpoint_and_api_key_header():
    observed = {}

    def opener(request, timeout):
        observed["url"] = request.full_url
        observed["headers"] = dict(request.header_items())
        observed["timeout"] = timeout
        return FakeResponse(
            {
                "tweets": [
                    {
                        "id": "123",
                        "text": "Building with coding agents.",
                        "author": {"userName": "builder"},
                    }
                ]
            }
        )

    result = module.search_candidates(
        '"agentic engineering" lang:en',
        api_key="test-key",
        timeout_seconds=7,
        opener=opener,
    )

    assert result[0]["source_candidate_id"] == "x-post:123"
    assert observed["url"].startswith(
        "https://api.twitterapi.io/twitter/tweet/advanced_search?"
    )
    assert "queryType=Latest" in observed["url"]
    assert observed["headers"]["X-api-key"] == "test-key"
    assert observed["timeout"] == 7


def test_search_candidates_requires_credential():
    with pytest.raises(module.ProviderAccessError, match="missing"):
        module.search_candidates("test", api_key=" ")


def test_search_candidates_rejects_missing_tweets_list():
    def opener(request, timeout):
        return FakeResponse({"status": "ok"})

    with pytest.raises(module.ProviderAccessError, match="tweets list"):
        module.search_candidates("test", api_key="test-key", opener=opener)


def test_provider_error_does_not_echo_api_key():
    def opener(request, timeout):
        raise RuntimeError("network unavailable")

    with pytest.raises(module.ProviderAccessError) as exc:
        module.search_candidates(
            "test",
            api_key="super-secret-value",
            opener=opener,
        )

    assert "super-secret-value" not in str(exc.value)
