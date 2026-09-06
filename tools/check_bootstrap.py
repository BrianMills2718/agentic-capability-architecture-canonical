#!/usr/bin/env python3
"""Run local checks that do not require a Frappe installation."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(*args):
    print("+", " ".join(map(str, args)))
    subprocess.run(args, cwd=ROOT, check=True)


def main():
    run(sys.executable, "tools/validate_schemas.py")
    run(sys.executable, "tools/validate_registry.py")
    run(sys.executable, "tools/check_reuse_evidence.py")

    for manifest in sorted((ROOT / "clients").glob("*/manifest.yml")):
        if manifest.parent.name == "_template":
            continue
        run(sys.executable, "tools/validate_project.py", str(manifest.relative_to(ROOT)))

    run(sys.executable, "tools/check_frappe_packages.py")
    run(sys.executable, "-m", "pytest")

    print("LOCAL BOOTSTRAP CHECKS PASSED")
    print("Note: Frappe integration tests require a Bench test site and are not run here.")


if __name__ == "__main__":
    main()
