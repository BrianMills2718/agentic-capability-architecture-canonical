#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, os, subprocess, sys, yaml

ROOT = Path(__file__).resolve().parents[1]
BASE = json.loads((ROOT / ".acceptance/baseline_hashes.json").read_text())
SHARED = json.loads((ROOT / ".acceptance/shared_runtime_hashes.json").read_text())


def text(path):
    try:
        return path.read_text(encoding="utf-8").lower()
    except Exception:
        return ""


def has(path, needles):
    body = text(path)
    return any(n.lower() in body for n in needles)


def fail(errors):
    print("ACCEPTANCE FAILED")
    for error in errors:
        print("-", error)
    raise SystemExit(1)


def clean_env():
    env = os.environ.copy()
    apps = sorted({
        p.parent for p in ROOT.rglob("pyproject.toml")
        if "frappe_app" in p.parts
        and not any(part in {"build", "dist", "__pycache__"} or part.endswith(".egg-info") for part in p.parts)
    })
    paths = [str(p) for p in apps]
    if env.get("PYTHONPATH"):
        paths.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(paths)
    return env


def main():
    errors=[]
    manifest_path=ROOT / "clients/beta_reference/manifest.yml"
    if not manifest_path.exists():
        fail(["beta manifest missing"])
    manifest=yaml.safe_load(manifest_path.read_text()) or {}
    if manifest.get("project") != "beta_reference": errors.append("wrong project name")
    caps=set((manifest.get("capabilities") or {}).keys())
    for cap in ("core","scheduling","approvals","notifications"):
        if cap not in caps: errors.append(f"missing reused capability: {cap}")
    if not (manifest.get("custom_extensions") or []): errors.append("missing project-local extension")

    beta_root=ROOT / "clients/beta_reference"
    beta_files=[p for p in beta_root.rglob("*") if p.is_file()]
    beta_py=[p for p in beta_files if p.suffix==".py"]
    if not any(has(p,["90"]) for p in beta_files): errors.append("90-minute rule missing")
    if not any(has(p,["na_approvals","resolve(","apply_resolution"]) for p in beta_py): errors.append("shared approval resolver not used")
    if not any(has(p,["na_notifications","send_email"]) for p in beta_py): errors.append("shared notification transport not used")
    if not any(has(p,["scheduler_events","enqueue_at(","cron","scheduled_job","schedule_reminder"]) for p in beta_py): errors.append("automatic reminder trigger missing")

    tests=[p for p in ROOT.rglob("test*.py") if "beta" in str(p).lower() or "beta_reference" in text(p)]
    if not tests: errors.append("beta tests missing")
    if tests and not any(has(p,["scheduler_events","schedule","reminder"]) for p in tests): errors.append("trigger wiring test missing")
    dedupe=["idempot","already_sent","reminder_sent","delivery_key","delivery record","delivery_record","frappe.db.exists","unique delivery","dedup"]
    if not any(has(p,dedupe) for p in beta_py): errors.append("durable reminder deduplication missing")
    if tests and not any(has(p,["idempot","duplicate","twice","second run","only once","already sent"]) for p in tests): errors.append("duplicate-delivery regression test missing")

    learn=beta_root / "LEARNINGS.md"
    if not learn.exists(): errors.append("reuse assessment missing")

    for rel, expected in SHARED.items():
        p=ROOT/rel
        if not p.exists(): errors.append(f"shared runtime removed: {rel}")
        elif hashlib.sha256(p.read_bytes()).hexdigest()!=expected: errors.append(f"shared runtime changed: {rel}")
    for rel, expected in BASE.items():
        p=ROOT/rel
        if not p.exists(): errors.append(f"ACME file removed: {rel}")
        elif hashlib.sha256(p.read_bytes()).hexdigest()!=expected: errors.append(f"ACME behavior changed: {rel}")
    for p in beta_files:
        if p.suffix==".py" and "def resolve(" in text(p): errors.append(f"duplicated approval resolver: {p.relative_to(ROOT)}")
        if p.name=="appointment.json": errors.append("duplicated Appointment DocType")
    if errors: fail(errors)

    env=clean_env()
    commands=[
        [sys.executable,"tools/validate_registry.py"],
        [sys.executable,"tools/validate_project.py","clients/beta_reference/manifest.yml"],
        [sys.executable,"tools/check_bootstrap.py"],
        [sys.executable,"-m","pytest","-q",*[str(p.relative_to(ROOT)) for p in tests]],
    ]
    for cmd in commands:
        print("+", " ".join(cmd))
        r=subprocess.run(cmd,cwd=ROOT,env=env)
        if r.returncode: fail([f"command failed ({r.returncode}): {' '.join(cmd)}"])
    print("ACCEPTANCE PASSED")

if __name__=="__main__": main()
