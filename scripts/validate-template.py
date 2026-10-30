#!/usr/bin/env python3
"""Validate the repository-root MAF plugin, guidance and maintenance artifacts."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from maf_knowledge import load_coverage

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
REFERENCES = ROOT / "resources" / "references"
PROFILES = ROOT / "resources" / "profiles"
MATRIX = ROOT / "resources" / "docs" / "capabilities" / "maf-dotnet-1.24.md"
CATALOG = ROOT / "resources" / "docs" / "patterns" / "v4.md"
ROUTING = ROOT / "resources" / "evaluations" / "skill-routing" / "v1.jsonl"

REQUIRED_SKILLS = {
    "maf-adoption", "maf-agents", "maf-architecture", "maf-context-memory",
    "maf-devui", "maf-hosting", "maf-middleware", "maf-observability",
    "maf-provider-integration", "maf-review", "maf-security", "maf-testing",
    "maf-tools", "maf-workflows",
}
PLAYBOOK_HEADINGS = [
    "Intent", "Responsibility classification", "Recommended abstraction",
    "State and trust boundaries", "Maturity/provider constraints",
    "Illustrative C# fragment", "Implementation prompt", "Review checklist",
    "Acceptance/evaluation criteria",
]
PROFILE_BUDGETS = {
    "AGENTS.md": 12_000,
    "resources/profiles/ai-first/AGENTS.md": 12_000,
    "resources/profiles/application-with-ai-module/AGENTS.ai-module.md": 7_000,
    "resources/profiles/application-with-ai-module/AGENTS.root-fragment.md": 3_000,
}


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def parse_frontmatter(path: Path, errors: list[str]) -> tuple[str, str] | None:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail(f"{path.relative_to(ROOT)}: missing or malformed YAML frontmatter", errors)
        return None
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    name, description = values.get("name", ""), values.get("description", "")
    if not re.fullmatch(r"[a-z0-9-]{1,63}", name):
        fail(f"{path.relative_to(ROOT)}: invalid skill name {name!r}", errors)
    if not description:
        fail(f"{path.relative_to(ROOT)}: missing description", errors)
    elif len(description) > 500:
        fail(f"{path.relative_to(ROOT)}: description exceeds 500 characters", errors)
    return name, description


def validate_local_links(path: Path, errors: list[str], root: Path | None = None) -> None:
    root = ROOT if root is None else root
    text = path.read_text(encoding="utf-8")
    candidates = set(re.findall(r"`((?:\.\./|references/)[^`]+\.md)`", text))
    candidates.update(
        target for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text)
        if not re.match(r"(?:[a-zA-Z][a-zA-Z0-9+.-]*:|#)", target)
    )
    for candidate in candidates:
        clean = candidate.split("#", 1)[0]
        if not clean:
            continue
        target = (path.parent / clean).resolve()
        try:
            target.relative_to(root.resolve())
        except ValueError:
            fail(f"{path.relative_to(root)}: reference escapes plugin: {candidate}", errors)
            continue
        if not target.exists():
            fail(f"{path.relative_to(root)}: missing local reference {candidate}", errors)


def validate_plugin(root: Path, errors: list[str]) -> None:
    """Validate a direct plugin checkout or an isolated installed copy, read-only."""
    for name in ("plugin.json", "VERSION", "LICENSE", "skills", "resources"):
        path = root / name
        if not path.exists():
            fail(f"Missing plugin component: {name}", errors)
        elif name in {"skills", "resources"} and not path.is_dir():
            fail(f"Plugin component must be a directory: {name}", errors)
        elif name not in {"skills", "resources"} and not path.is_file():
            fail(f"Plugin component must be a file: {name}", errors)
        if path.is_symlink():
            fail(f"Plugin component must not be a symlink: {name}", errors)
    trees = (root / "skills", root / "resources")
    symlinks = [p for tree in trees for p in tree.rglob("*") if p.is_symlink()]
    for path in symlinks:
        fail(f"Plugin resource must not be a symlink: {path.relative_to(root)}", errors)
    if symlinks or any((root / name).is_symlink() for name in ("plugin.json", "VERSION", "LICENSE", "skills", "resources")):
        return
    manifest_path = root / "plugin.json"
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (ValueError, OSError) as exc:
            fail(f"Invalid plugin.json: {exc}", errors)
        else:
            if not isinstance(manifest, dict):
                fail("plugin.json must contain an object", errors)
            else:
                if manifest.get("name") != "maf-dotnet":
                    fail("plugin.json name must be maf-dotnet", errors)
                version = (root / "VERSION").read_text(encoding="utf-8").strip() if (root / "VERSION").is_file() else ""
                if not re.fullmatch(r"\d+\.\d+\.\d+", version) or manifest.get("version") != version:
                    fail("plugin.json version must match Semantic Versioning in VERSION", errors)
                for field in ("description", "license", "repository"):
                    if not isinstance(manifest.get(field), str) or not manifest[field].strip():
                        fail(f"plugin.json requires a nonempty {field}", errors)
                if manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
                    fail("plugin.json must declare the portable Agent Plugins schema", errors)
    skills = root / "skills"
    names = {path.parent.name for path in skills.glob("*/SKILL.md")}
    for name in sorted(REQUIRED_SKILLS - names):
        fail(f"Missing plugin skill: {name}", errors)
    for name in sorted(names - REQUIRED_SKILLS):
        fail(f"Unexpected plugin skill: {name}", errors)
    for path in skills.rglob("SKILL.md"):
        if len(path.relative_to(skills).parts) != 2:
            fail(f"Nested plugin skill is not supported: {path.relative_to(root)}", errors)
    for tree in trees:
        for path in sorted(tree.rglob("*.md")):
            validate_local_links(path, errors, root)


def validate_matrix(errors: list[str]) -> None:
    if not MATRIX.is_file():
        fail(f"Missing capability matrix: {MATRIX.relative_to(ROOT)}", errors)
        return
    text = MATRIX.read_text(encoding="utf-8")
    for metadata in ("Matrix version:", "Last verified MAF release:", "Verification date:"):
        if metadata not in text:
            fail(f"{MATRIX.relative_to(ROOT)}: missing {metadata}", errors)
    header = "| Feature | .NET availability | Maturity | Required package/boundary | Provider or hosting restrictions | Official source | Verified release | Verified date |"
    if header not in text:
        fail(f"{MATRIX.relative_to(ROOT)}: incomplete matrix header", errors)
    rows = [line for line in text.splitlines() if line.startswith("| ")][1:]
    if len(rows) < 20:
        fail(f"{MATRIX.relative_to(ROOT)}: expected at least 20 feature rows, found {len(rows)}", errors)
    for number, row in enumerate(rows, 1):
        if len(row.split("|")) != 10:
            fail(f"{MATRIX.relative_to(ROOT)}: row {number} does not have 8 fields", errors)
        if any(marker in row for marker in ("TBD", "TODO", "????")):
            fail(f"{MATRIX.relative_to(ROOT)}: row {number} has incomplete metadata", errors)
        if "http" not in row or "2026-" not in row or "dotnet-" not in row:
            fail(f"{MATRIX.relative_to(ROOT)}: row {number} lacks source/release/date metadata", errors)


def validate_catalog(errors: list[str]) -> None:
    if not CATALOG.is_file():
        fail(f"Missing pattern catalog: {CATALOG.relative_to(ROOT)}", errors)
        return
    text = CATALOG.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^## (\d+)\. .+$", text, re.MULTILINE))
    if len(matches) != 17 or [int(m.group(1)) for m in matches] != list(range(1, 18)):
        fail(f"{CATALOG.relative_to(ROOT)}: expected numbered playbooks 1 through 17", errors)
        return
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section = text[match.end():end]
        for heading in PLAYBOOK_HEADINGS:
            if f"### {heading}\n" not in section:
                fail(f"{CATALOG.relative_to(ROOT)}: playbook {index + 1} missing {heading!r}", errors)


def validate_routing(known_skills: set[str], errors: list[str]) -> None:
    if not ROUTING.is_file():
        fail(f"Missing routing dataset: {ROUTING.relative_to(ROOT)}", errors)
        return
    ids: set[str] = set()
    records: list[dict[str, object]] = []
    for number, line in enumerate(ROUTING.read_text(encoding="utf-8").splitlines(), 1):
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"{ROUTING.relative_to(ROOT)}:{number}: invalid JSON: {exc}", errors)
            continue
        if not isinstance(record, dict):
            fail(f"{ROUTING.relative_to(ROOT)}:{number}: fixture must be a JSON object", errors)
            continue
        records.append(record)
        fixture_id = record.get("id")
        if not isinstance(fixture_id, str) or fixture_id in ids:
            fail(f"{ROUTING.relative_to(ROOT)}:{number}: missing/duplicate id", errors)
        else:
            ids.add(fixture_id)
        for field in ("expected_skills", "must_not_route"):
            values = record.get(field)
            if not isinstance(values, list) or any(not isinstance(v, str) or v not in known_skills for v in values):
                fail(f"{ROUTING.relative_to(ROOT)}:{number}: invalid {field}", errors)
    required_ids = {
        "rag-two-step", "consequential-tool", "deterministic-routing", "hosting-choice",
        "security-review", "provider-migration", "old-package", "generic-dotnet-nullability",
    }
    missing = required_ids - ids
    if missing:
        fail(f"{ROUTING.relative_to(ROOT)}: missing required fixtures: {', '.join(sorted(missing))}", errors)
    if not any(not record.get("expected_skills") for record in records):
        fail(f"{ROUTING.relative_to(ROOT)}: needs at least one negative routing fixture", errors)


def validate_hygiene(errors: list[str]) -> None:
    # Validate publishable files, including tracked files even when ignored.
    # Local ignored caches/configuration are not part of the guidance pack.
    if (ROOT / ".git").exists():
        result = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            check=True, capture_output=True,
        )
        paths = [ROOT / name for name in result.stdout.decode("utf-8").split("\0") if name]
        paths = [path for path in paths if path.exists() or path.is_symlink()]
    else:
        # Exported packs have no Git index; validate every delivered file.
        paths = [path for path in ROOT.rglob("*") if path.is_file()]
    forbidden_names = {".DS_Store", "Thumbs.db"}
    forbidden_suffixes = {
        ".pyc", ".dll", ".exe", ".nupkg", ".snupkg",
        ".cs", ".csproj", ".fsproj", ".vbproj", ".sln",
    }
    forbidden_dirs = {"__pycache__", "bin", "obj"}
    for path in paths:
        relative = path.relative_to(ROOT)
        if ".git" in relative.parts:
            continue
        if path.name in forbidden_names or path.suffix.lower() in forbidden_suffixes:
            fail(f"Forbidden generated/copied artifact: {relative}", errors)
        if any(part in forbidden_dirs for part in relative.parts[:-1]):
            fail(f"Forbidden generated directory contains: {relative}", errors)
    if (ROOT / "scripts" / "install-guidance.py").exists():
        fail("Obsolete installer must not exist", errors)
    for path in paths:
        if path.name == "marketplace.json":
            fail("Marketplace catalog belongs in a separate repository", errors)
    for skill_file in (path for path in paths if path.name == "SKILL.md"):
        try:
            skill_file.relative_to(ROOT / "skills")
        except ValueError:
            fail(f"Runtime/copied skill outside plugin skill root: {skill_file.relative_to(ROOT)}", errors)
    secret_patterns = [
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    ]
    for path in paths:
        if not path.is_file() or ".git" in path.relative_to(ROOT).parts:
            continue
        if path.suffix.lower() not in {".md", ".py", ".sh", ".toml", ".json", ".jsonl", ".yml", ".yaml"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if any(pattern.search(text) for pattern in secret_patterns):
            fail(f"Potential committed secret in {path.relative_to(ROOT)}", errors)


def main() -> int:
    errors: list[str] = []
    skill_files = sorted(SKILLS.glob("*/SKILL.md"))
    names: dict[str, Path] = {}
    descriptions: dict[str, Path] = {}
    for skill_file in skill_files:
        parsed = parse_frontmatter(skill_file, errors)
        if not parsed:
            continue
        name, description = parsed
        if name in names:
            fail(f"Duplicate skill name {name!r}", errors)
        names[name] = skill_file
        if description in descriptions:
            fail(f"Duplicate skill description in {skill_file.relative_to(ROOT)}", errors)
        descriptions[description] = skill_file
        if skill_file.parent.name != name:
            fail(f"{skill_file.relative_to(ROOT)}: directory must match skill name", errors)
    missing = REQUIRED_SKILLS - set(names)
    extra = set(names) - REQUIRED_SKILLS
    if missing:
        fail(f"Missing required skills: {', '.join(sorted(missing))}", errors)
    if extra:
        fail(f"Unexpected skills (update routing contract deliberately): {', '.join(sorted(extra))}", errors)
    if (SKILLS / "maf-implementation").exists():
        fail("Generic maf-implementation skill is forbidden", errors)

    for required in ("official-sources.md", "provider-neutrality.md", "langgraph-crosswalk.md", "application-boundaries.md"):
        if not (REFERENCES / required).is_file():
            fail(f"Missing shared reference: resources/references/{required}", errors)
    for markdown in ROOT.rglob("*.md"):
        if ".git" not in markdown.relative_to(ROOT).parts:
            validate_local_links(markdown, errors)

    for relative, budget in PROFILE_BUDGETS.items():
        path = ROOT / relative
        if not path.is_file():
            fail(f"Missing profile instruction: {relative}", errors)
        elif len(path.read_bytes()) > budget:
            fail(f"{relative}: exceeds {budget}-byte instruction budget", errors)
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip() if (ROOT / "VERSION").is_file() else ""
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail("VERSION must contain Semantic Versioning x.y.z", errors)
    if version and f"## [{version}]" not in (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"):
        fail("CHANGELOG does not contain current VERSION", errors)

    try:
        load_coverage(ROOT / "resources/docs/capabilities/coverage.json")
    except ValueError as exc:
        fail(str(exc), errors)
    validate_matrix(errors)
    validate_catalog(errors)
    validate_routing(set(names), errors)
    validate_hygiene(errors)
    validate_plugin(ROOT, errors)

    entrypoint_links = {
        ROOT / "README.md": ["resources/docs/capabilities/maf-dotnet-1.24.md", "resources/docs/patterns/v4.md", "resources/evaluations/skill-routing/v1.jsonl"],
        ROOT / "resources" / "docs" / "patterns" / "README.md": ["v4.md"],
    }
    for path, required_targets in entrypoint_links.items():
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        for target in required_targets:
            if target not in text:
                fail(f"{path.relative_to(ROOT)}: missing required catalog/evaluation link {target}", errors)

    smoke_gate = ROOT / "docs" / "releases" / "fresh-session-smoke-test.md"
    smoke_text = smoke_gate.read_text(encoding="utf-8") if smoke_gate.is_file() else ""
    for required_phrase in ("mandatory manual release gate", "existing application", "AI-first", "generic .NET"):
        if required_phrase not in smoke_text:
            fail(f"{smoke_gate.relative_to(ROOT)}: missing release-gate requirement {required_phrase!r}", errors)

    required_ci = [ROOT / ".github" / "workflows" / "validate.yml", ROOT / ".github" / "workflows" / "source-audit.yml"]
    for workflow in required_ci:
        if not workflow.is_file():
            fail(f"Missing CI workflow: {workflow.relative_to(ROOT)}", errors)

    if errors:
        print("Template validation FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Template validation OK: {len(skill_files)} skills, 17 playbooks, routing v1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
