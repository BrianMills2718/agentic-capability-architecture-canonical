#!/usr/bin/env python3
"""Protect the repository's small set of documentation authority/freshness invariants.

This is intentionally not a general Markdown linter. It checks only contracts that
have repeatedly drifted and could mislead a fresh coding agent about navigation,
architecture authority, proof status, or sourcing policy.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    path = ROOT / relative
    if not path.exists():
        raise FileNotFoundError(relative)
    return path.read_text(encoding="utf-8")


def main() -> None:
    errors: list[str] = []

    required_snippets = {
        "README.md": [
            "https://github.com/BrianMills2718/vision/blob/main/wiki/index.md",
            "docs/README.md",
            "Off-the-shelf wins ties",
            "cumulative capability ecosystem",
            "Each project is both a **consumer and a contributor**",
        ],
        "docs/ARCHITECTURE_CHARTER.md": [
            "Cumulative growth contract",
            "consumer and a contributor",
        ],
        "docs/README.md": [
            "Global navigation authority",
            "Current architecture and operating rules",
            "Historical evidence and preserved context",
        ],
        "docs/ARCHITECTURE.md": ["Compatibility Pointer"],
        "docs/NEXT_PROOF.md": ["Supersedes the original bootstrap proof plan"],
        "docs/FRESH_AGENT_PROOF.md": ["Status: historical iteration log"],
        "docs/ACCEPTANCE_RUNBOOK.md": ["Status: historical bootstrap fixture"],
        "docs/ACCEPTANCE_TEST.md": ["Status: historical bootstrap fixture"],
        "docs/ACCEPTANCE_REHEARSAL_RESULT.md": ["Status: historical harness evidence"],
        "docs/FRAPPE_CI_PROOF.md": ["Status: baseline proof record"],
        "docs/WORKING_CONTEXT.md": ["Status: historical accumulated implementation context"],
        "docs/SESSION_CONTEXT_2026-09-06.md": ["Status: historical checkpoint"],
        "docs/EXPORT_CHECKLIST.md": ["The original bootstrap Frappe and fresh-agent acceptance gates have already passed"],
    }

    for relative, snippets in required_snippets.items():
        try:
            text = read(relative)
        except FileNotFoundError:
            errors.append(f"missing required documentation file: {relative}")
            continue
        for snippet in snippets:
            if snippet not in text:
                errors.append(f"{relative}: missing documentation contract text: {snippet!r}")

    forbidden_by_file = {
        "README.md": [
            "## Start here",
            "## Current registered capabilities",
            "No repo has been picked as canonical",
        ],
        "docs/EXPORT_CHECKLIST.md": [
            "Fresh-agent acceptance test has been run before declaring the bootstrap complete",
        ],
    }
    for relative, snippets in forbidden_by_file.items():
        text = read(relative)
        for snippet in snippets:
            if snippet in text:
                errors.append(f"{relative}: stale/duplicated authority text remains: {snippet!r}")

    stale_phrases = [
        "Only two proof gates remain before the bootstrap is considered complete",
        "A fifth genuinely fresh run is required",
        "The other outstanding proof remains execution of the authored Frappe lifecycle tests",
        "The remaining framework-level proof is automated in",
    ]
    for path in sorted((ROOT / "docs").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for phrase in stale_phrases:
            if phrase in text:
                errors.append(f"{path.relative_to(ROOT)}: obsolete status phrase remains: {phrase!r}")

    if errors:
        raise SystemExit("Documentation contract check failed:\n- " + "\n- ".join(errors))

    print("OK: documentation authority, historical labels, and proof-status guardrails are current")


if __name__ == "__main__":
    main()
