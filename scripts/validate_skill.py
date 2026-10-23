"""Lightweight local structure check for an Agent Skills directory.

Usage: python scripts/validate_skill.py /path/to/time-series-paper-auditor
This is a simple project-specific check, not an official validator.
"""

from __future__ import annotations
import re
import sys
from pathlib import Path


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    manifest = root / "SKILL.md"
    if not manifest.is_file():
        return ["Missing SKILL.md"]
    data = manifest.read_text(encoding="utf-8")
    if not data.startswith("---\n"):
        return ["SKILL.md must begin with YAML frontmatter"]
    blocks = data.split("---\n", 2)
    if len(blocks) < 3:
        return ["SKILL.md lacks closing YAML frontmatter marker"]
    try:
        import yaml
    except ImportError:
        errors.append("PyYAML not installed (needed for this optional validator)")
        return errors
    meta = yaml.safe_load(blocks[1])
    if not isinstance(meta, dict):
        return ["Frontmatter must be a YAML map"]
    name, desc = meta.get("name"), meta.get("description")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        errors.append("Invalid frontmatter name")
    if name != root.name:
        errors.append("Name must match skill directory")
    if not isinstance(desc, str) or not (1 <= len(desc) <= 1024):
        errors.append("Invalid frontmatter description")

    for p in re.findall(r"`((?:references|scripts|assets)/[^`\s]+)`", data):
        if not (root / p).is_file():
            errors.append(f"Broken path in SKILL.md: {p}")
    for needed in (
        "references/prompt-library.md", "references/user-guide.zh-CN.md",
        "assets/paper-card-template.md", "assets/module-card-template.md",
        "assets/research-hypothesis-template.md", "scripts/trace_shapes.py",
    ):
        if not (root / needed).is_file():
            errors.append(f"Missing required bundle resource: {needed}")
    return errors


if __name__ == "__main__":
    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    problems = validate(target)
    if problems:
        for p in problems:
            print("ERROR:", p)
        raise SystemExit(1)
    print(f"PASS: valid local structure: {target}")
