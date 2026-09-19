#!/usr/bin/env python3
"""Minimal read-only TwitterAPI.io collection boundary for the P3 pilot."""

from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from typing import Any, Callable

API_BASE = "https://api.twitterapi.io"
SEARCH_PATH = "/twitter/tweet/advanced_search"


class ProviderAccessError(RuntimeError):
    """Provider/configuration failure with credential-safe context."""


def normalize_tweet(tweet: dict[str, Any]) -> dict[str, Any]:
    """Normalize one TwitterAPI.io tweet into the pilot collection shape."""
    post_id = str(tweet.get("id") or "").strip()
    text = str(tweet.get("text") or "").strip()
    author = tweet.get("author")
    if not isinstance(author, dict):
        raise ProviderAccessError("TwitterAPI.io search result omitted author object")
    handle = str(author.get("userName") or "").strip()
    if not post_id or not text or not handle:
        raise ProviderAccessError(
            "TwitterAPI.io search result omitted post id, text, or author handle"
        )

    return {
        "source_candidate_id": f"x-post:{post_id}",
        "author_handle": f"@{handle.lstrip('@')}",
        "tweet_text": text,
        "provider_post_id": post_id,
        "source_url": str(
            tweet.get("url")
            or tweet.get("twitterUrl")
            or f"https://x.com/i/status/{post_id}"
        ),
    }


def search_candidates(
    query: str,
    *,
    api_key: str | None = None,
    timeout_seconds: float = 30.0,
    opener: Callable[..., Any] = urllib.request.urlopen,
) -> list[dict[str, Any]]:
    """Read candidate posts through the ordinary TwitterAPI.io HTTP contract."""
    key = (api_key or os.environ.get("TWITTERAPI_IO_API_KEY", "")).strip()
    if not key:
        raise ProviderAccessError(
            "TWITTERAPI_IO_API_KEY is missing; live collection is unavailable"
        )

    params = urllib.parse.urlencode({"query": query, "queryType": "Latest"})
    request = urllib.request.Request(
        f"{API_BASE}{SEARCH_PATH}?{params}",
        headers={"X-API-Key": key},
        method="GET",
    )

    try:
        with opener(request, timeout=timeout_seconds) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except ProviderAccessError:
        raise
    except Exception as exc:
        raise ProviderAccessError(
            f"TwitterAPI.io read-only search failed: {type(exc).__name__}"
        ) from exc

    if not isinstance(payload, dict):
        raise ProviderAccessError("TwitterAPI.io search returned non-object JSON")
    tweets = payload.get("tweets")
    if not isinstance(tweets, list):
        raise ProviderAccessError("TwitterAPI.io search omitted the tweets list")

    candidates: list[dict[str, Any]] = []
    for tweet in tweets:
        if not isinstance(tweet, dict):
            continue
        candidates.append(normalize_tweet(tweet))
    return candidates


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: twitterapi_io_collection.py '<query>'", file=sys.stderr)
        return 2
    try:
        candidates = search_candidates(sys.argv[1])
    except ProviderAccessError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        return 1
    print(
        json.dumps(
            {
                "ok": True,
                "provider": "twitterapi.io",
                "endpoint": SEARCH_PATH,
                "candidate_count": len(candidates),
                "candidates": candidates,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
