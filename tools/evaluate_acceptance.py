#!/usr/bin/env python3
"""Evaluate a completed fresh-agent acceptance sandbox structurally."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import yaml


def _baseline_dir() -> Path:
    repo_root = Path(__file__).resolve().parents[1]
    normal = repo_root / "tests" / "acceptance"
    if (normal / "baseline_hashes.json").exists():
        return normal

    packaged = Path(__file__).resolve().parent / "acceptance_baselines"
    if (packaged / "baseline_hashes.json").exists():
        return packaged

    raise RuntimeError("acceptance baselines not found")


BASELINES = _baseline_dir()
BASELINE = json.loads((BASELINES / "baseline_hashes.json").read_text(encoding="utf-8"))
SHARED_RUNTIME_BASELINE = json.loads(
    (BASELINES / "shared_runtime_hashes.json").read_text(encoding="utf-8")
)


def fail(errors):
    print("ACCEPTANCE FAILED")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)


def text_of(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    try:
        return path.read_text(encoding="utf-8").lower()
    except UnicodeDecodeError:
        return ""


def contains_any(path: Path, needles):
    text = text_of(path)
    return any(needle.lower() in text for needle in needles)


def clean_test_environment(root: Path):
    import os
    env = os.environ.copy()
    apps = sorted({
        p.parent for p in root.rglob("pyproject.toml")
        if "frappe_app" in p.parts
        and not any(part in {"build", "dist", "__pycache__"} or part.endswith(".egg-info") for part in p.parts)
    })
    paths = [str(app) for app in apps]
    existing = env.get("PYTHONPATH")
    if existing:
        paths.append(existing)
    env["PYTHONPATH"] = os.pathsep.join(paths)
    return env


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: evaluate_acceptance.py <acceptance-sandbox>")

    root = Path(sys.argv[1]).expanduser().resolve()
    errors = []
    manifest_path = root / "clients/beta_reference/manifest.yml"

    if not manifest_path.exists():
        fail(["clients/beta_reference/manifest.yml does not exist"])

    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    if manifest.get("project") != "beta_reference":
        errors.append("manifest project must be beta_reference")

    caps = set((manifest.get("capabilities") or {}).keys())
    for cap in ("core", "scheduling", "approvals", "notifications"):
        if cap not in caps:
            errors.append(f"beta_reference must reuse registered capability: {cap}")

    custom_extensions = manifest.get("custom_extensions") or []
    if not custom_extensions:
        errors.append("beta_reference must isolate its project-specific behavior in a custom extension")

    beta_root = root / "clients/beta_reference"
    beta_files = [p for p in beta_root.rglob("*") if p.is_file()]

    if not any(contains_any(p, ["90"]) for p in beta_files):
        errors.append("beta_reference does not visibly encode the 90-minute project rule")

    beta_python = [p for p in beta_files if p.suffix == ".py"]
    if not any(
        contains_any(p, ["na_approvals", "resolve(", "apply_resolution"])
        for p in beta_python
    ):
        errors.append("beta_reference does not visibly use the shared approval resolver")

    if not any(
        contains_any(p, ["na_notifications", "send_email"])
        for p in beta_python
    ):
        errors.append("beta_reference does not visibly use the shared notification email capability")

    trigger_tokens = ["scheduler_events", "enqueue_at(", "cron", "scheduled_job", "schedule_reminder"]
    if not any(contains_any(p, trigger_tokens) for p in beta_python):
        errors.append(
            "beta_reference has an email reminder helper but no visible automatic trigger/scheduler path"
        )

    trigger_tests = [p for p in root.rglob("test*.py") if "beta" in str(p).lower()]
    if trigger_tests and not any(
        contains_any(p, ["scheduler_events", "schedule", "reminder"])
        for p in trigger_tests
    ):
        errors.append("beta_reference does not test reminder trigger/wiring")

    # Scheduled email delivery is retryable. Require visible durable deduplication and
    # a regression test that addresses repeated execution/duplicate delivery.
    durable_dedupe_tokens = [
        "idempot", "already_sent", "reminder_sent", "delivery_key",
        "delivery record", "delivery_record", "frappe.db.exists",
        "unique delivery", "dedup",
    ]
    if not any(contains_any(p, durable_dedupe_tokens) for p in beta_python):
        errors.append(
            "beta_reference reminder scheduler has no visible durable idempotency/deduplication state"
        )

    duplicate_test_tokens = ["idempot", "duplicate", "twice", "second run", "only once", "already sent"]
    if trigger_tests and not any(contains_any(p, duplicate_test_tokens) for p in trigger_tests):
        errors.append(
            "beta_reference does not test repeated scheduler execution / duplicate reminder prevention"
        )

    for rel, expected in SHARED_RUNTIME_BASELINE.items():
        path = root / rel
        if not path.exists():
            errors.append(f"shared runtime file was removed: {rel}")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            errors.append(f"shared runtime changed instead of being reused: {rel}")

    for path in beta_files:
        if path.suffix == ".py" and contains_any(path, ["def resolve("]):
            errors.append(f"beta project duplicated an approval resolver: {path.relative_to(root)}")
        if path.name == "appointment.json":
            errors.append(f"beta project duplicated the Appointment DocType: {path.relative_to(root)}")

    test_candidates = []
    for p in root.rglob("test*.py"):
        rel = str(p.relative_to(root)).lower()
        body = text_of(p)
        if "beta" in rel or "beta_reference" in body:
            test_candidates.append(p)

    if not test_candidates:
        errors.append("no beta_reference-specific tests were added")

    readme = beta_root / "README.md"
    learnings = beta_root / "LEARNINGS.md"
    notes = manifest.get("notes") or manifest.get("reuse_notes")
    if not learnings.exists() and not notes and not contains_any(readme, ["reuse", "candidate", "learning"]):
        errors.append("no reusable learning/candidate note was recorded for beta_reference")

    for rel, expected in BASELINE.items():
        path = root / rel
        if not path.exists():
            errors.append(f"existing ACME file was removed: {rel}")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            errors.append(f"existing ACME project behavior changed: {rel}")

    if errors:
        fail(errors)

    beta_test_paths = [str(p.relative_to(root)) for p in test_candidates]
    commands = [
        [sys.executable, "tools/validate_registry.py"],
        [sys.executable, "tools/validate_project.py", "clients/beta_reference/manifest.yml"],
        [sys.executable, "tools/check_bootstrap.py"],
        [sys.executable, "-m", "pytest", "-q", *beta_test_paths],
    ]
    env = clean_test_environment(root)
    for command in commands:
        print("+", " ".join(command))
        result = subprocess.run(command, cwd=root, env=env)
        if result.returncode:
            fail([f"command failed ({result.returncode}): {' '.join(command)}"])

    print("ACCEPTANCE PASSED")
    print(
        "The fresh-agent result reused unchanged shared runtime, isolated beta-specific "
        "behavior, used shared approvals/notifications, preserved ACME, recorded learning, "
        "and passed local tests."
    )


if __name__ == "__main__":
    main()
