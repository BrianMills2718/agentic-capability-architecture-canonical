#!/usr/bin/env python3
"""Run repository-wide checks that do not require a Frappe installation."""
from pathlib import Path
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def discover_frappe_apps() -> list[Path]:
    return sorted({
        pyproject.parent
        for pyproject in ROOT.rglob("pyproject.toml")
        if "frappe_app" in pyproject.parts
        and not any(part in {"build", "dist", "__pycache__"} or part.endswith(".egg-info") for part in pyproject.parts)
    })


def test_environment(apps: list[Path]) -> dict[str, str]:
    env = os.environ.copy()
    paths = [str(app) for app in apps]
    existing = env.get("PYTHONPATH")
    if existing:
        paths.append(existing)
    env["PYTHONPATH"] = os.pathsep.join(paths)
    return env


def discover_test_targets(apps: list[Path]) -> list[Path]:
    targets = [ROOT / "tests"]
    seen = {targets[0].resolve()}
    for app in apps:
        for tests_dir in sorted(app.rglob("tests")):
            if not tests_dir.is_dir():
                continue
            if not any(tests_dir.rglob("test*.py")):
                continue
            resolved = tests_dir.resolve()
            if resolved not in seen:
                targets.append(tests_dir)
                seen.add(resolved)
    return targets


def run(*args, env=None):
    print("+", " ".join(map(str, args)))
    subprocess.run(args, cwd=ROOT, env=env, check=True)


def main():
    run(sys.executable, "tools/check_documentation_contract.py")
    run(sys.executable, "tools/validate_schemas.py")
    run(sys.executable, "tools/validate_registry.py")
    run(sys.executable, "tools/check_reuse_evidence.py")

    for manifest in sorted((ROOT / "clients").glob("*/manifest.yml")):
        if manifest.parent.name == "_template":
            continue
        run(sys.executable, "tools/validate_project.py", str(manifest.relative_to(ROOT)))

    run(sys.executable, "tools/check_frappe_packages.py")

    apps = discover_frappe_apps()
    env = test_environment(apps)
    targets = discover_test_targets(apps)
    print("Discovered Frappe app test roots:")
    for target in targets[1:]:
        print("  -", target.relative_to(ROOT))
    run(
        sys.executable,
        "-m",
        "pytest",
        *(str(path.relative_to(ROOT)) for path in targets),
        env=env,
    )

    print("LOCAL BOOTSTRAP CHECKS PASSED")
    print("Note: Frappe lifecycle tests still require a Bench test site or CI service stack.")


if __name__ == "__main__":
    main()
