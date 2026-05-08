from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()

EXCLUDED_PARTS = {
    ".git",
    ".pytest_cache",
    "__pycache__",
}

# Public proof should not accidentally expose private/local project markers.
# Keep generic words such as "email" and "calendar" allowed for boundary docs.
FORBIDDEN_PATTERNS = [
    r"Tenormusica",
    r"curiosity[-_ ]?wiki",
    r"LLMWIKI",
    r"llmwiki",
    r"proof_asset",
    r"public AI secretary proof",
    r"GitHub Issue",
    r"C:\\\\Users",
    r"DBJ",
    r"dragonrondo",
    r"Ezlize",
    r"Google Calendar",
    r"Gmail",
]

TEXT_SUFFIXES = {
    ".md",
    ".py",
    ".json",
    ".yml",
    ".yaml",
    ".txt",
    ".toml",
    ".ini",
}


def should_scan(path: Path) -> bool:
    if path.resolve() == SELF:
        return False
    if any(part in EXCLUDED_PARTS for part in path.parts):
        return False
    return path.is_file() and path.suffix.lower() in TEXT_SUFFIXES


def main() -> int:
    compiled = [(pattern, re.compile(pattern, re.IGNORECASE)) for pattern in FORBIDDEN_PATTERNS]
    findings: list[str] = []

    for path in sorted(ROOT.rglob("*")):
        if not should_scan(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = path.relative_to(ROOT)
        for line_number, line in enumerate(text.splitlines(), start=1):
            for label, pattern in compiled:
                if pattern.search(line):
                    findings.append(f"{rel}:{line_number}: matched {label!r}")

    if findings:
        print("Public boundary check failed. Remove or generalize private/local markers:")
        for finding in findings[:50]:
            print(f"- {finding}")
        if len(findings) > 50:
            print(f"... and {len(findings) - 50} more")
        return 1

    print("Public boundary check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
