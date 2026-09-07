#!/usr/bin/env python3
"""Create a clean repository copy for a genuinely fresh coding-agent test."""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT.parent / f"{ROOT.name}_acceptance_sandbox"
PROMPT_SOURCE = ROOT / "tests" / "acceptance" / "FRESH_AGENT_PROMPT.txt"

# These files describe or score the acceptance test and must not be visible to the agent.
EXCLUDED_RELATIVE = {
    Path("tests/acceptance"),
    Path("tools/evaluate_acceptance.py"),
    Path("tools/create_acceptance_sandbox.py"),
    Path("tools/package_acceptance_test.py"),
    Path("docs/ACCEPTANCE_TEST.md"),
    Path("docs/ACCEPTANCE_RUNBOOK.md"),
    Path("docs/ACCEPTANCE_REHEARSAL_RESULT.md"),
    Path("docs/FRESH_AGENT_PROOF.md"),
    Path("docs/NEXT_PROOF.md"),
    Path("docs/DEFINITION_OF_DONE.md"),
}
GENERATED_NAMES = {"__pycache__", ".pytest_cache", "build", "dist"}


def ignored(directory, names):
    directory = Path(directory)
    out = set()
    for name in names:
        path = directory / name
        try:
            rel = path.relative_to(ROOT)
        except ValueError:
            continue
        if rel in EXCLUDED_RELATIVE:
            out.add(name)
        if name in GENERATED_NAMES or name.endswith(".egg-info") or name.endswith(".pyc"):
            out.add(name)
    return out


def init_git(output: Path):
    if shutil.which("git") is None:
        return
    subprocess.run(["git", "init", "-q"], cwd=output, check=True)
    subprocess.run(["git", "config", "user.name", "Acceptance Baseline"], cwd=output, check=True)
    subprocess.run(["git", "config", "user.email", "acceptance-baseline@example.invalid"], cwd=output, check=True)
    subprocess.run(["git", "add", "."], cwd=output, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "Fresh-agent acceptance baseline"], cwd=output, check=True)


def main():
    output = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else DEFAULT_OUTPUT.resolve()
    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(ROOT, output, ignore=ignored)
    beta = output / "clients" / "beta_reference"
    if beta.exists():
        shutil.rmtree(beta)
    (output / "ACCEPTANCE_PROMPT.txt").write_text(PROMPT_SOURCE.read_text(encoding="utf-8"), encoding="utf-8")
    init_git(output)
    print(output)


if __name__ == "__main__":
    main()
