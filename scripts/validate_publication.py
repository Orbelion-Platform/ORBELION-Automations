"""Validate curated text and the exact visually approved architecture PNG."""
import hashlib
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {
    "README.md", "PUBLICATION_SCOPE.md", "SECURITY.md", ".gitignore",
    "docs/VERIFIED_CAPABILITIES.md", "docs/MAINTENANCE.md",
    "docs/ENGINEERING_CASE_STUDY.md", "docs/EXECUTION_EVIDENCE.md",
    "examples/synthetic_job.py", "tests/test_synthetic_job.py",
    ".github/workflows/validate.yml", "scripts/validate_publication.py",
    "docs/assets/automations-workflow.png",
}
APPROVED_PNG = {
    "docs/assets/automations-workflow.png":
        "183bad7978c4cc25c3d2ca2b532ca406894f83c81f437b9e0389b3a284f7fb85",
}
SKIP = {".git", "__pycache__", ".venv", ".pytest_cache"}
PATTERNS = [
    r"-----BEGIN " + r"(?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    r"gh[pousr]_[A-Za-z0-9]{30,}",
    r"github_pat_[A-Za-z0-9_]{30,}",
    r"sk-[A-Za-z0-9]{24,}",
]
seen = set()
for path in ROOT.rglob("*"):
    relative = path.relative_to(ROOT)
    if any(part in SKIP for part in relative.parts):
        continue
    if path.is_symlink():
        raise SystemExit(f"Symlink prohibited: {relative.as_posix()}")
    if not path.is_file():
        continue
    name = relative.as_posix()
    if name not in ALLOWED:
        raise SystemExit(f"Unapproved file: {name}")
    if name in APPROVED_PNG:
        data = path.read_bytes()
        if not data.startswith(b"\x89PNG\r\n\x1a\n"):
            raise SystemExit(f"Invalid PNG signature: {name}")
        if hashlib.sha256(data).hexdigest() != APPROVED_PNG[name]:
            raise SystemExit(f"Image changed; renewed visual review required: {name}")
    else:
        content = path.read_text(encoding="utf-8")
        if any(re.search(pattern, content) for pattern in PATTERNS):
            raise SystemExit(f"Potential credential: {name}")
        if path.suffix == ".md":
            for target in re.findall(r"\]\(([^)]+)\)", content):
                if "://" in target or target.startswith("#"):
                    continue
                linked = (path.parent / target.split("#", 1)[0]).resolve()
                if not linked.is_relative_to(ROOT) or not linked.is_file():
                    raise SystemExit(f"Broken or out-of-tree link in {name}: {target}")
    seen.add(name)
missing = ALLOWED - seen
if missing:
    raise SystemExit(f"Missing approved files: {sorted(missing)}")
print(f"PASS: {len(seen) - len(APPROVED_PNG)} approved text files, "
      f"{len(APPROVED_PNG)} approved image; local Markdown links resolve")
