#!/usr/bin/env python3
"""Create a clean ZIP snapshot of the complete capability-base workspace."""
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT.parent / f"{ROOT.name}.zip"

EXCLUDED_PARTS = {"__pycache__", ".pytest_cache", ".git", ".venv", "node_modules", "build", "dist"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def include(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if any(part in EXCLUDED_PARTS or part.endswith(".egg-info") for part in rel.parts):
        return False
    if path.suffix in EXCLUDED_SUFFIXES:
        return False
    return path.is_file()


def main():
    if OUT.exists():
        OUT.unlink()

    files = [p for p in sorted(ROOT.rglob("*")) if include(p)]

    manifest_path = ROOT / "FILE_MANIFEST.txt"
    manifest_path.write_text(
        "\n".join(str(p.relative_to(ROOT)) for p in files if p != manifest_path) + "\n",
        encoding="utf-8",
    )

    files = [p for p in sorted(ROOT.rglob("*")) if include(p)]

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            zf.write(path, arcname=str(Path(ROOT.name) / path.relative_to(ROOT)))

    print(f"Created {OUT}")
    print(f"Included {len(files)} files")


if __name__ == "__main__":
    main()
