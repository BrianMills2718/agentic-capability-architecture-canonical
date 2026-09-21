#!/usr/bin/env bash
set -euo pipefail

# Source-free A1 verification recipe.
# Reads Product N only at the pinned private revision supplied by the caller,
# creates an ephemeral publication-only package in /tmp, verifies the retained
# collect() behavior against synthetic provider responses, prints evidence, and
# removes the temporary private source on exit.

PRODUCT_N_REPO="${1:-/home/brian/code/inside-success/repos/twitter-prospecting}"
PRODUCT_N_REV="ab2cfba0e8c43f0198716dee4414dedf2212d478"
CLIENT_PATH="apps/twitter_prospecting/twitter_client.py"
MODELS_PATH="apps/twitter_prospecting/models.py"
EXPECTED_CLIENT_SHA="a9be9aabcd5dd8be0a688c07313e0ef71d4b446e12f20d1cdd435ec907df468e"
EXPECTED_MODELS_SHA="aef6fa1dd7263fbb04a4ec246e472b8260c45cf54673f319762fbd4b62ff0149"

if [[ ! -d "${PRODUCT_N_REPO}/.git" ]]; then
  echo "ERROR: Product N repository not found: ${PRODUCT_N_REPO}" >&2
  exit 2
fi
git -C "${PRODUCT_N_REPO}" cat-file -e "${PRODUCT_N_REV}^{commit}"

WORKDIR="$(mktemp -d /tmp/aca-a1-publication-check.XXXXXX)"
trap 'rm -rf "$WORKDIR"' EXIT
PKG_DIR="$WORKDIR/src/twitter_prospecting_provider"
mkdir -p "$PKG_DIR" "$WORKDIR/dist"

git -C "${PRODUCT_N_REPO}" show "${PRODUCT_N_REV}:${CLIENT_PATH}" > "$PKG_DIR/twitter_client.py"
git -C "${PRODUCT_N_REPO}" show "${PRODUCT_N_REV}:${MODELS_PATH}" > "$PKG_DIR/models.py"

client_sha="$(sha256sum "$PKG_DIR/twitter_client.py" | awk '{print $1}')"
models_sha="$(sha256sum "$PKG_DIR/models.py" | awk '{print $1}')"
[[ "$client_sha" == "$EXPECTED_CLIENT_SHA" ]]
[[ "$models_sha" == "$EXPECTED_MODELS_SHA" ]]

cat > "$PKG_DIR/__init__.py" <<'PY'
from .models import SearchQuery
from .twitter_client import SearchCollection, TwitterApiError, TwitterApiIoClient

__all__ = [
    "SearchQuery",
    "SearchCollection",
    "TwitterApiError",
    "TwitterApiIoClient",
]
PY

cat > "$WORKDIR/pyproject.toml" <<'TOML'
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "inside-success-twitter-provider-a1"
version = "0.0.0+a1.ab2cfba"
requires-python = ">=3.12"
dependencies = ["requests>=2.32,<3", "pydantic>=2.8,<3"]

[tool.setuptools.packages.find]
where = ["src"]
TOML

python -m venv --system-site-packages "$WORKDIR/venv"
# Build tooling is test-only and pinned for reproducibility; this does not install
# or contact the Twitter provider.
"$WORKDIR/venv/bin/python" -m pip install --quiet "wheel==0.48.0"
"$WORKDIR/venv/bin/python" - <<'PY'
import pydantic
import requests
import setuptools
import wheel
print("BUILD_ENV_OK")
print("requests", requests.__version__)
print("pydantic", pydantic.__version__)
print("setuptools", setuptools.__version__)
print("wheel", wheel.__version__)
PY

"$WORKDIR/venv/bin/python" -m pip wheel   --no-deps   --no-build-isolation   -w "$WORKDIR/dist"   "$WORKDIR" >/dev/null

wheel_path="$(find "$WORKDIR/dist" -maxdepth 1 -type f -name '*.whl' -print -quit)"
[[ -n "$wheel_path" ]]
wheel_sha="$(sha256sum "$wheel_path" | awk '{print $1}')"
wheel_size="$(stat -c %s "$wheel_path")"

"$WORKDIR/venv/bin/python" -m pip install --quiet --no-deps "$wheel_path"

# Run outside Product N and outside the generated source tree so the import must
# resolve from the installed wheel.
cd /tmp
"$WORKDIR/venv/bin/python" - <<'PY'
from typing import Any

import requests
from twitter_prospecting_provider import SearchQuery, TwitterApiIoClient
import twitter_prospecting_provider.twitter_client as provider_module


class FakeResponse:
    def __init__(self, payload: dict[str, Any], status_code: int = 200) -> None:
        self._payload = payload
        self.status_code = status_code
        self.text = "provider error"

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError("bad response")

    def json(self) -> dict[str, Any]:
        return self._payload


class FakeSession:
    def get(self, url, *, headers, params, timeout):
        if "broken" in str(params.get("query")):
            return FakeResponse({}, status_code=503)
        return FakeResponse(
            {
                "tweets": [
                    {
                        "id": "10",
                        "text": "We opened our third location.",
                        "createdAt": "2026-07-23T12:00:00Z",
                        "author": {
                            "userName": "operator",
                            "name": "Real Operator",
                            "description": "Founder and owner",
                            "followers": 2200,
                            "canDm": True,
                        },
                    },
                    {"id": "11", "text": "Malformed author is isolated."},
                ]
            }
        )


def query(label: str, query_text: str) -> SearchQuery:
    return SearchQuery(
        label=label,
        query=query_text,
        rationale="Exercise independent provider-call handling.",
        evidence_goal="business_substance",
    )


client = TwitterApiIoClient("synthetic-key", session=FakeSession())
result = client.collect(
    [
        query("valid search", '"we opened" founder'),
        query("failed search", "broken provider query"),
    ],
    candidate_limit=5,
)

assert len(result.candidates) == 1
assert result.candidates[0].profile.handle == "operator"
assert [execution.error is None for execution in result.executions] == [True, False]
assert any("missing author" in warning for warning in result.warnings)
assert any("HTTP 503" in warning for warning in result.warnings)

print("A1_TEMP_BUNDLE_PASS")
print("installed_module", provider_module.__file__)
print("candidates", len(result.candidates))
print("executions", len(result.executions))
print("warnings", len(result.warnings))
PY

echo "product_n_revision $PRODUCT_N_REV"
echo "twitter_client_sha256 $client_sha"
echo "models_sha256 $models_sha"
echo "wheel_name $(basename "$wheel_path")"
echo "wheel_sha256 $wheel_sha"
echo "wheel_size_bytes $wheel_size"
echo "python_version $("$WORKDIR/venv/bin/python" --version 2>&1)"
echo "TEMP_PRIVATE_SOURCE_CLEANUP_ON_EXIT yes"
