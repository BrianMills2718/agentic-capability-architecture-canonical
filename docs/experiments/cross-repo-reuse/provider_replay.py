#!/usr/bin/env python3
"""Requests-compatible synthetic TwitterAPI.io replay transport for ACA-PLAN-002 A2.

This is test infrastructure, not an ACA capability. It performs no network I/O and
never records header values.
"""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any

import requests


class ReplayFixtureError(ValueError):
    """Raised when the synthetic replay fixture is malformed."""


class ReplayResponse:
    def __init__(self, *, status_code: int, body: Any, text: str = "") -> None:
        self.status_code = status_code
        self._body = deepcopy(body)
        self.text = text or ("" if status_code < 400 else f"synthetic HTTP {status_code}")

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError(f"synthetic provider HTTP {self.status_code}")

    def json(self) -> Any:
        return deepcopy(self._body)


class ReplaySession:
    """A minimal requests.Session-compatible GET transport backed by exact queries."""

    def __init__(self, routes: dict[str, dict[str, Any]]) -> None:
        self._routes = deepcopy(routes)
        self.calls: list[dict[str, Any]] = []

    @classmethod
    def from_path(cls, path: str | Path) -> "ReplaySession":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or payload.get("schema_version") != 1:
            raise ReplayFixtureError("replay fixture must be an object with schema_version=1")
        routes = payload.get("routes")
        if not isinstance(routes, dict) or not routes:
            raise ReplayFixtureError("replay fixture routes must be a non-empty object")
        for query, route in routes.items():
            if not isinstance(query, str) or not query:
                raise ReplayFixtureError("route query keys must be non-empty strings")
            if not isinstance(route, dict):
                raise ReplayFixtureError(f"route for {query!r} must be an object")
            status = route.get("status_code")
            if not isinstance(status, int) or not 100 <= status <= 599:
                raise ReplayFixtureError(f"route for {query!r} has invalid status_code")
            if "body" not in route:
                raise ReplayFixtureError(f"route for {query!r} is missing body")
        return cls(routes)

    def get(
        self,
        url: str,
        *,
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        timeout: float | None = None,
    ) -> ReplayResponse:
        params = dict(params or {})
        query = params.get("query")
        if not isinstance(query, str):
            query = ""
        self.calls.append(
            {
                "url": str(url),
                "query": query,
                "params": deepcopy(params),
                "timeout": timeout,
                "header_names": sorted(str(key) for key in (headers or {})),
            }
        )
        route = self._routes.get(query)
        if route is None:
            return ReplayResponse(
                status_code=404,
                body={"error": "unmapped synthetic query"},
                text="unmapped synthetic query",
            )
        return ReplayResponse(
            status_code=int(route["status_code"]),
            body=route["body"],
            text=str(route.get("text") or ""),
        )
