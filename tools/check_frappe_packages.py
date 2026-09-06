#!/usr/bin/env python3
"""Validate and build every Frappe-style package without installing Frappe."""
from pathlib import Path
import re
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
        and not any(part in {"build", "dist", "__pycache__"} or part.endswith(".egg-info") for part in pyproject.parts)
    }
    return sorted(apps)


def scrub_module_name(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def validate_frappe_module_layout(app: Path) -> None:
    modules_files = list(app.glob("*/modules.txt"))
    if not modules_files:
        raise SystemExit(f"Missing Frappe modules.txt: {app.relative_to(ROOT)}")

    for modules_file in modules_files:
        package_root = modules_file.parent
        for raw in modules_file.read_text(encoding="utf-8").splitlines():
            module = raw.strip()
            if not module:
                continue
            expected = package_root / scrub_module_name(module) / "__init__.py"
            if not expected.exists():
                raise SystemExit(
                    "Missing Frappe module package marker for "
                    f"{module!r}: {expected.relative_to(ROOT)}"
                )


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

    for app in apps:
        validate_frappe_module_layout(app)

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
        print(f"OK: {len(apps)} Frappe app packages have valid module layout and build successfully")
    finally:
        for app in apps:
            clean_generated(app)


if __name__ == "__main__":
    main()
