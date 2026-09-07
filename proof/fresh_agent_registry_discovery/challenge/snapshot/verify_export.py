from pathlib import Path
import hashlib
import yaml

ROOT = Path(__file__).resolve().parent
GENERATED_PARTS = {"__pycache__", ".pytest_cache", "build", "dist"}

def is_source_path(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    return not any(
        part in GENERATED_PARTS or part.endswith(".egg-info") or part.endswith(".pyc")
        for part in relative.parts
    )

def tree_digest(path: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(path.rglob("*")):
        if p.is_file() and is_source_path(p, path):
            h.update(str(p.relative_to(path)).encode("utf-8") + b"\0")
            h.update(p.read_bytes())
            h.update(b"\0")
    return h.hexdigest()

def main():
    registry = yaml.safe_load((ROOT / "capability_registry.yml").read_text(encoding="utf-8"))
    for name, entry in registry["capabilities"].items():
        package = ROOT / entry["path"]
        actual = tree_digest(package)
        if actual != entry["sha256_tree"]:
            raise SystemExit(f"snapshot digest mismatch: {name}: {actual}")
    print("PORTABLE EXPORT VERIFIED")

if __name__ == "__main__":
    main()
