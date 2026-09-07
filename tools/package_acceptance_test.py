#!/usr/bin/env python3
"""Build the fresh-agent sandbox ZIP and separate control/evaluator ZIP."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = Path("/mnt/data") if Path("/mnt/data").exists() else ROOT.parent


def zip_tree(source: Path, destination: Path, top_name: str):
    if destination.exists():
        destination.unlink()
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(source.rglob("*")):
            if path.is_file():
                zf.write(path, arcname=str(Path(top_name) / path.relative_to(source)))
    with zipfile.ZipFile(destination) as zf:
        bad = zf.testzip()
        if bad:
            raise SystemExit(f"bad ZIP member: {bad}")


def main():
    with tempfile.TemporaryDirectory(prefix="capability_acceptance_") as td:
        td = Path(td)
        sandbox = td / "fresh_agent_acceptance_sandbox"
        subprocess.run([str(ROOT / "tools/create_acceptance_sandbox.py"), str(sandbox)], check=True)
        zip_tree(sandbox, OUTDIR / "fresh_agent_acceptance_sandbox.zip", sandbox.name)

        control = td / "acceptance_test_control"
        (control / "acceptance_baselines").mkdir(parents=True)
        shutil.copy(ROOT / "tests/acceptance/FRESH_AGENT_PROMPT.txt", control / "PROMPT.txt")
        shutil.copy(ROOT / "tools/evaluate_acceptance.py", control / "evaluate_acceptance.py")
        shutil.copy(ROOT / "tests/acceptance/baseline_hashes.json", control / "acceptance_baselines/baseline_hashes.json")
        shutil.copy(ROOT / "tests/acceptance/shared_runtime_hashes.json", control / "acceptance_baselines/shared_runtime_hashes.json")
        shutil.copy(ROOT / "docs/ACCEPTANCE_RUNBOOK.md", control / "RUNBOOK.md")
        (control / "README.md").write_text(
            "Keep this control package outside the fresh agent workspace. Run evaluate_acceptance.py only after the agent finishes.\n",
            encoding="utf-8",
        )
        (control / "requirements.txt").write_text("PyYAML\n", encoding="utf-8")
        zip_tree(control, OUTDIR / "acceptance_test_control.zip", control.name)

    print(OUTDIR / "fresh_agent_acceptance_sandbox.zip")
    print(OUTDIR / "acceptance_test_control.zip")


if __name__ == "__main__":
    main()
