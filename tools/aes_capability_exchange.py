#!/usr/bin/env python3
"""Resolve AES selection requests through the verified semantic-action catalog."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

from jsonschema import Draft202012Validator

try:  # Package import for tests and library callers.
    from tools.capability_catalog import build_catalog
except ModuleNotFoundError:  # Direct-script invocation adds tools/ to sys.path.
    from capability_catalog import build_catalog


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "aes_capability_exchange.schema.json"


class ExchangeError(ValueError):
    """Raised when an exchange message is malformed or stale."""


def _validator(root: Path) -> Draft202012Validator:
    schema = json.loads((root / "schemas" / SCHEMA_PATH.name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def _validate(message: dict[str, Any], root: Path) -> None:
    errors = sorted(_validator(root).iter_errors(message), key=lambda error: list(error.path))
    if errors:
        raise ExchangeError(f"invalid exchange message: {errors[0].message}")


def catalog_revision(root: Path = ROOT) -> str:
    """Return the immutable source revision backing the catalog response."""

    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def resolve_selection_request(request: dict[str, Any], root: Path = ROOT) -> dict[str, Any]:
    """Select exact requested action IDs, retaining gaps rather than guessing."""

    _validate(request, root)
    if request["message_kind"] != "selection_request":
        raise ExchangeError("expected a selection_request message")

    actual_revision = catalog_revision(root)
    if request["catalog_revision"] != actual_revision:
        raise ExchangeError(
            "catalog revision mismatch: "
            f"request={request['catalog_revision']}, actual={actual_revision}"
        )

    actions = {
        action["action_id"]: action
        for action in build_catalog(root)["semantic_actions"]
    }
    selected = []
    uncovered_gaps = []
    for action_id in request["capability_categories"]:
        action = actions.get(action_id)
        if action is None:
            uncovered_gaps.append(action_id)
            continue
        selected.append(
            {
                "semantic_action_id": action_id,
                "owner": action["capability"],
                "version": action["capability_version"],
                "public_interface": action["public_interface"],
                "evidence": [
                    {"kind": "artifact", "reference": action["manifest"]},
                    {"kind": "artifact", "reference": action["source_file"]},
                ],
                "limitations": [
                    "Selection is exact semantic-action ID matching; runtime constraints are retained but not evaluated.",
                ],
            }
        )

    response = {
        "schema_version": "1.0",
        "message_kind": "selection_response",
        "request_id": request["request_id"],
        "catalog_revision": actual_revision,
        "selected": selected,
        "rejected": [],
        "uncovered_gaps": uncovered_gaps,
    }
    _validate(response, root)
    return response


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        request = json.loads(args.request.read_text(encoding="utf-8"))
        if not isinstance(request, dict):
            raise ExchangeError("request must be a JSON object")
        response = resolve_selection_request(request)
        args.output.write_text(json.dumps(response, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except (ExchangeError, OSError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps({"ok": True, "output": str(args.output.resolve())}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
