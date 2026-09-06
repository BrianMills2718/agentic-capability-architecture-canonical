#!/usr/bin/env python3
"""Build every Frappe-style package in the repository without installing Frappe."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def discover_apps() -> list[Path]:
    apps = {
        pyproject.parent
        for pyproject in ROOT.rglob("pyproject.toml")
        if "frappe_app" in pyproject.parts
    }
    return sorted(apps)


def clean_generated(app: Path) -> None:
    for path in app.glob("*.egg-info"):
        if path.is_dir():
            shutil.rmtree(path)
    for name in ("build", "dist"):
        path = app / name
        if path.exists():
            shutil.rmtree(path)


def main():
    apps = discover_apps()
    if not apps:
        raise SystemExit("No Frappe app packages found")

    try:
        with tempfile.TemporaryDirectory(prefix="capability-wheels-") as out:
            for app in apps:
                print(f"Building package: {app.relative_to(ROOT)}")
                subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "wheel",
                        "--quiet",
                        "--no-deps",
                        "--no-build-isolation",
                        "--wheel-dir",
                        out,
                        str(app),
                    ],
                    check=True,
                )
        print(f"OK: {len(apps)} Frappe app packages build successfully")
    finally:
        for app in apps:
            clean_generated(app)


if __name__ == "__main__":
    main()
