#!/usr/bin/env python3
"""Small structural validator for the repo-scoped Codex skill set."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"
REFERENCES = ROOT / ".agents" / "references"
PROFILES = ROOT / "profiles"


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def parse_frontmatter(path: Path, errors: list[str]) -> tuple[str, str] | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{path.relative_to(ROOT)}: missing YAML frontmatter", errors)
        return None
    try:
        _, frontmatter, _ = text.split("---", 2)
    except ValueError:
        fail(f"{path.relative_to(ROOT)}: malformed YAML frontmatter", errors)
        return None

    values: dict[str, str] = {}
    for line in frontmatter.strip().splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()

    name = values.get("name", "")
    description = values.get("description", "")
    if not name:
        fail(f"{path.relative_to(ROOT)}: missing name", errors)
    if not description:
        fail(f"{path.relative_to(ROOT)}: missing description", errors)
    return name, description


def validate_relative_markdown_refs(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    # Skills deliberately name local references in inline code. Validate those paths.
    candidates = re.findall(r"`((?:\.\./|references/)[^`]+\.md)`", text)
    for candidate in candidates:
        target = (path.parent / candidate).resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            fail(f"{path.relative_to(ROOT)}: reference escapes repo: {candidate}", errors)
            continue
        if not target.is_file():
            fail(f"{path.relative_to(ROOT)}: missing reference {candidate}", errors)


def main() -> int:
    errors: list[str] = []
    skill_files = sorted(SKILLS.glob("*/SKILL.md"))
    if not skill_files:
        fail("No skills found", errors)

    names: dict[str, Path] = {}
    for skill_file in skill_files:
        parsed = parse_frontmatter(skill_file, errors)
        validate_relative_markdown_refs(skill_file, errors)
        if not parsed:
            continue
        name, description = parsed
        if name in names:
            fail(
                f"Duplicate skill name {name!r}: {names[name].relative_to(ROOT)} and {skill_file.relative_to(ROOT)}",
                errors,
            )
        names[name] = skill_file
        if skill_file.parent.name != name:
            fail(
                f"{skill_file.relative_to(ROOT)}: directory name must match skill name {name!r}",
                errors,
            )
        if len(description) > 700:
            fail(f"{skill_file.relative_to(ROOT)}: description is too broad/long ({len(description)} chars)", errors)

    # Generic implementation skill is deliberately forbidden in v2.
    if (SKILLS / "maf-implementation").exists():
        fail("maf-implementation must not exist in v2; route by MAF abstraction instead", errors)

    for md in sorted(SKILLS.rglob("*.md")):
        validate_relative_markdown_refs(md, errors)

    required = {
        "maf-architecture",
        "maf-agents",
        "maf-tools",
        "maf-workflows",
        "maf-context-memory",
        "maf-middleware",
        "maf-provider-integration",
        "maf-observability",
        "maf-devui",
        "maf-testing",
        "maf-review",
    }
    missing = required - set(names)
    if missing:
        fail(f"Missing required skills: {', '.join(sorted(missing))}", errors)

    required_references = {
        "official-sources.md",
        "provider-neutrality.md",
        "langgraph-crosswalk.md",
        "application-boundaries.md",
    }
    for filename in sorted(required_references):
        if not (REFERENCES / filename).is_file():
            fail(f"Missing shared reference: .agents/references/{filename}", errors)

    required_profile_files = [
        PROFILES / "README.md",
        PROFILES / "ai-first" / "AGENTS.md",
        PROFILES / "application-with-ai-module" / "AGENTS.root-fragment.md",
        PROFILES / "application-with-ai-module" / "AGENTS.ai-module.md",
        PROFILES / "application-with-ai-module" / "README.md",
    ]
    for profile_file in required_profile_files:
        if not profile_file.is_file():
            fail(f"Missing adoption profile file: {profile_file.relative_to(ROOT)}", errors)

    root_agents = ROOT / "AGENTS.md"
    ai_first_agents = PROFILES / "ai-first" / "AGENTS.md"
    if root_agents.is_file() and ai_first_agents.is_file() and root_agents.read_bytes() != ai_first_agents.read_bytes():
        fail("Root AGENTS.md must stay in sync with profiles/ai-first/AGENTS.md", errors)

    installer = ROOT / "scripts" / "install-guidance.py"
    if not installer.is_file():
        fail("Missing scripts/install-guidance.py", errors)

    if errors:
        print("Template validation FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Template validation OK: {len(skill_files)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
