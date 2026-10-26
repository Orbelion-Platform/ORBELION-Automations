"""Validate the curated public tree, including untracked candidate files."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = ["README.md","PUBLICATION_SCOPE.md","SECURITY.md","docs/VERIFIED_CAPABILITIES.md","docs/MAINTENANCE.md",".gitignore","examples/synthetic_job.py","tests/test_synthetic_job.py",".github/workflows/validate.yml","scripts/validate_publication.py"]
SKIP = {".git", "__pycache__", ".venv", ".pytest_cache"}
PATTERNS = [r"-----BEGIN " + r"(?:RSA |EC |OPENSSH )?PRIVATE KEY-----", r"gh[pousr]_[A-Za-z0-9]{30,}", r"github_pat_[A-Za-z0-9_]{30,}", r"sk-[A-Za-z0-9]{24,}"]
seen = set()
for path in ROOT.rglob("*"):
    relative = path.relative_to(ROOT)
    if any(part in SKIP for part in relative.parts) or not path.is_file():
        continue
    name = relative.as_posix()
    if name not in ALLOWED:
        raise SystemExit(f"Unapproved file: {name}")
    if path.is_symlink():
        raise SystemExit(f"Symlink prohibited: {name}")
    content = path.read_text(encoding="utf-8")
    if any(re.search(pattern, content) for pattern in PATTERNS):
        raise SystemExit(f"Potential credential: {name}")
    seen.add(name)
missing = set(ALLOWED) - seen
if missing:
    raise SystemExit(f"Missing approved files: {sorted(missing)}")
print(f"PASS: {len(seen)} approved text files")
