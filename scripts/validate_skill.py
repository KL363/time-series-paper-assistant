"""Check the lingerskill bundle and its explicit-invocation configuration.

Usage: python scripts/validate_skill.py /path/to/checkout
Add --strict-directory-name when checking an installed skill directory.
This is a lightweight project-specific check, not an official validator.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


REQUIRED_RESOURCES = (
    "references/stages-00-02.md",
    "references/stages-03-04.md",
    "references/stages-05-08.md",
    "references/prompt-library.md",
    "references/user-guide.zh-CN.md",
    "agents/openai.yaml",
)


def referenced_paths(markdown: str):
    """Yield bundle paths in code spans and relative Markdown links."""
    yield from re.findall(r"`((?:references|scripts|assets|agents)/[^`\n]+)`", markdown)
    for target in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", markdown):
        # Optional link titles are not part of the path. Angle brackets allow spaces.
        target = target.strip()
        if target.startswith("<"):
            target = target[1:].split(">", 1)[0]
        else:
            target = target.split(maxsplit=1)[0] if target else ""
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        yield unquote(parsed.path)


def validate(root: Path, *, strict_directory_name: bool = False) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    manifest = root / "SKILL.md"
    if not manifest.is_file():
        return ["Missing SKILL.md"]
    data = manifest.read_text(encoding="utf-8")
    lines = data.splitlines()
    if not lines or lines[0] != "---":
        return ["SKILL.md must begin with YAML frontmatter"]
    try:
        closing = lines.index("---", 1)
    except ValueError:
        return ["SKILL.md lacks closing YAML frontmatter marker"]
    try:
        import yaml
    except ImportError:
        return ["PyYAML not installed (needed for this optional validator)"]
    try:
        meta = yaml.safe_load("\n".join(lines[1:closing]))
    except yaml.YAMLError as exc:
        return [f"Invalid YAML in SKILL.md frontmatter: {exc}"]
    if not isinstance(meta, dict):
        return ["Frontmatter must be a YAML map"]
    name, desc = meta.get("name"), meta.get("description")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        errors.append("Invalid frontmatter name")
    if strict_directory_name and name != root.name:
        errors.append("Name must match installed skill directory (--strict-directory-name)")
    if not isinstance(desc, str) or not (1 <= len(desc) <= 1024):
        errors.append("Invalid frontmatter description")

    for p in sorted(set(referenced_paths(data))):
        path = (root / p).resolve()
        try:
            path.relative_to(root)
        except ValueError:
            errors.append(f"Bundle reference escapes skill directory in SKILL.md: {p}")
            continue
        if not path.exists():
            errors.append(f"Broken path in SKILL.md: {p}")
    for needed in REQUIRED_RESOURCES:
        if not (root / needed).is_file():
            errors.append(f"Missing required bundle resource: {needed}")

    agent_manifest = root / "agents/openai.yaml"
    if agent_manifest.is_file():
        try:
            agent = yaml.safe_load(agent_manifest.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            errors.append(f"Invalid YAML in agents/openai.yaml: {exc}")
            agent = None
        if not isinstance(agent, dict):
            errors.append("agents/openai.yaml must be a YAML map")
        else:
            policy = agent.get("policy")
            if not isinstance(policy, dict) or policy.get("allow_implicit_invocation") is not False:
                errors.append("agents/openai.yaml must set policy.allow_implicit_invocation to false")
            interface = agent.get("interface")
            prompt = interface.get("default_prompt") if isinstance(interface, dict) else None
            if not isinstance(prompt, str) or not isinstance(name, str) or not re.search(
                r"\$" + re.escape(name) + r"(?![a-zA-Z0-9_-])", prompt
            ):
                errors.append("agents/openai.yaml default_prompt must contain $<frontmatter name>")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--strict-directory-name", action="store_true", help="Require an installed directory to match the skill name")
    args = parser.parse_args()
    target = args.root.resolve()
    problems = validate(target, strict_directory_name=args.strict_directory_name)
    if problems:
        for p in problems:
            print("ERROR:", p)
        raise SystemExit(1)
    print(f"PASS: valid local structure: {target}")
