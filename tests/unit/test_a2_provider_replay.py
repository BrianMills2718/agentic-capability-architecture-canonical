"""Focused tests for the ACA-PLAN-002 A2 provider replay seam."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
import requests

ROOT = Path(__file__).resolve().parents[2]
A2_DIR = ROOT / "docs" / "experiments" / "cross-repo-reuse"
sys.path.insert(0, str(A2_DIR))

from provider_replay import ReplayFixtureError, ReplaySession


SAMPLE = A2_DIR / "public_sample.json"


def test_sample_fixture_replays_exact_multiword_query() -> None:
    session = ReplaySession.from_path(SAMPLE)
    response = session.get(
        "https://api.twitterapi.io/twitter/tweet/advanced_search",
        headers={"X-API-Key": "synthetic-secret"},
        params={"query": "distributed systems observability", "queryType": "Latest"},
        timeout=30.0,
    )
    response.raise_for_status()
    payload = response.json()

    assert len(payload["tweets"]) == 3
    assert session.calls[0]["query"] == "distributed systems observability"
    assert session.calls[0]["params"]["query"] == "distributed systems observability"


def test_request_log_records_header_names_not_values() -> None:
    session = ReplaySession.from_path(SAMPLE)
    session.get(
        "https://api.twitterapi.io/twitter/tweet/advanced_search",
        headers={"X-API-Key": "do-not-record-me", "Accept": "application/json"},
        params={"query": "agentic developer tools"},
        timeout=5,
    )

    call = session.calls[0]
    assert call["header_names"] == ["Accept", "X-API-Key"]
    assert "do-not-record-me" not in json.dumps(call)


def test_failure_route_raises_requests_http_error_without_secret() -> None:
    session = ReplaySession.from_path(SAMPLE)
    response = session.get(
        "https://api.twitterapi.io/twitter/tweet/advanced_search",
        headers={"X-API-Key": "secret-value"},
        params={"query": "synthetic provider failure"},
        timeout=2,
    )

    assert response.status_code == 503
    with pytest.raises(requests.HTTPError, match="503") as exc:
        response.raise_for_status()
    assert "secret-value" not in str(exc.value)


def test_unknown_query_is_explicit_404_not_network_fallback() -> None:
    session = ReplaySession.from_path(SAMPLE)
    response = session.get(
        "https://api.twitterapi.io/twitter/tweet/advanced_search",
        params={"query": "not in fixture"},
        timeout=1,
    )

    assert response.status_code == 404
    assert response.json() == {"error": "unmapped synthetic query"}
    with pytest.raises(requests.HTTPError, match="404"):
        response.raise_for_status()


def test_response_json_is_defensive_copy() -> None:
    session = ReplaySession.from_path(SAMPLE)
    response = session.get(
        "https://api.twitterapi.io/twitter/tweet/advanced_search",
        params={"query": "agentic developer tools"},
    )

    first = response.json()
    first["tweets"].clear()
    second = response.json()
    assert len(second["tweets"]) == 2


@pytest.mark.parametrize(
    "payload",
    [
        [],
        {},
        {"schema_version": 2, "routes": {"q": {"status_code": 200, "body": {}}}},
        {"schema_version": 1, "routes": {}},
        {"schema_version": 1, "routes": {"q": "bad"}},
        {"schema_version": 1, "routes": {"q": {"status_code": 999, "body": {}}}},
        {"schema_version": 1, "routes": {"q": {"status_code": 200}}},
    ],
)
def test_invalid_replay_fixture_fails_loudly(tmp_path: Path, payload) -> None:
    path = tmp_path / "fixture.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ReplayFixtureError):
        ReplaySession.from_path(path)


def test_sample_contains_success_duplicate_malformed_and_failure_conditions() -> None:
    fixture = json.loads(SAMPLE.read_text(encoding="utf-8"))
    routes = fixture["routes"]

    systems = routes["distributed systems observability"]["body"]["tweets"]
    agents = routes["agentic developer tools"]["body"]["tweets"]

    assert any("author" not in tweet for tweet in systems)
    assert {tweet["id"] for tweet in systems if "author" in tweet} & {
        tweet["id"] for tweet in agents if "author" in tweet
    }
    assert routes["synthetic provider failure"]["status_code"] == 503
