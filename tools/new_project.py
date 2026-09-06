#!/usr/bin/env python3
"""Create a project/client layer without creating a new shared capability."""
from pathlib import Path
import argparse
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project")
    parser.add_argument("--capabilities", default="core", help="comma-separated registered capabilities")
    parser.add_argument("--purpose", default="")
    args = parser.parse_args()

    if not re.fullmatch(r"[a-z][a-z0-9_]*", args.project):
        raise SystemExit("project must use lowercase letters, digits, and underscores")

    registry = yaml.safe_load((ROOT / "capability_registry.yml").read_text(encoding="utf-8"))
    known = registry["capabilities"]
    requested = [x.strip() for x in args.capabilities.split(",") if x.strip()]
    unknown = [x for x in requested if x not in known]
    if unknown:
        raise SystemExit("unknown capabilities: " + ", ".join(unknown))

    project_dir = ROOT / "clients" / args.project
    if project_dir.exists():
        raise SystemExit(f"project already exists: {args.project}")
    (project_dir / "config").mkdir(parents=True)
    (project_dir / "custom").mkdir()

    manifest = {
        "project": args.project,
        "purpose": args.purpose,
        "capabilities": {name: f"^{known[name]['version']}" for name in requested},
        "configuration": {},
        "custom_extensions": [],
        "notes": [],
    }
    (project_dir / "manifest.yml").write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    (project_dir / "README.md").write_text(
        f"# {args.project}\n\nCreated from the capability base. Document project-specific behavior and reusable learning here.\n",
        encoding="utf-8",
    )
    (project_dir / "custom" / "README.md").write_text(
        "# Project-specific extensions\n\nKeep unique behavior here; do not edit shared capabilities for project-only requirements.\n",
        encoding="utf-8",
    )
    print(project_dir.relative_to(ROOT))

if __name__ == "__main__":
    main()
