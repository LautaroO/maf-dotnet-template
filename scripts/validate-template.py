#!/usr/bin/env python3
"""Validate the repository-root MAF plugin, guidance and maintenance artifacts."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
REFERENCES = ROOT / "resources" / "references"
PROFILES = ROOT / "resources" / "profiles"
ROUTING = ROOT / "resources" / "evaluations" / "skill-routing" / "v2.jsonl"

PROFILE_BUDGETS = {
    "AGENTS.md": 12_000,
    "resources/profiles/ai-first/AGENTS.md": 12_000,
    "resources/profiles/application-with-ai-module/AGENTS.ai-module.md": 7_000,
    "resources/profiles/application-with-ai-module/AGENTS.root-fragment.md": 3_000,
}


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def parse_frontmatter(path: Path, errors: list[str], root: Path | None = None) -> tuple[str, str] | None:
    root = ROOT if root is None else root
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail(f"{path.relative_to(root)}: missing or malformed YAML frontmatter", errors)
        return None
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    name, description = values.get("name", ""), values.get("description", "")
    if not re.fullmatch(r"[a-z0-9-]{1,63}", name):
        fail(f"{path.relative_to(root)}: invalid skill name {name!r}", errors)
    if not description:
        fail(f"{path.relative_to(root)}: missing description", errors)
    elif len(description) > 500:
        fail(f"{path.relative_to(root)}: description exceeds 500 characters", errors)
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


def load_skill_contract(root: Path, errors: list[str]) -> dict | None:
    path = root / "resources/skill-contract.json"
    try:
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError("contract must be contained, not a symlink")
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or type(data.get("schema_version")) is not int or data["schema_version"] != 1:
            raise ValueError("expected schema_version 1 object")
        names = data.get("skills")
        if not isinstance(names,list) or not names or any(not isinstance(n,str) or not re.fullmatch(r"[a-z0-9-]{1,63}",n) for n in names) or len(set(names)) != len(names):
            raise ValueError("skills must be nonempty unique valid names")
        retired = data.get("retired_routes")
        if not isinstance(retired,dict) or any(not isinstance(old,str) or not re.fullmatch(r"[a-z0-9-]{1,63}",old) or old in names or not isinstance(new,str) or new not in names for old,new in retired.items()):
            raise ValueError("invalid retired route or target")
        for field in ("routing_dataset","pattern_catalog"):
            value=data.get(field)
            if not isinstance(value,str) or not value or Path(value).is_absolute() or not (root/value).resolve().is_relative_to(root.resolve()) or not (root/value).is_file():
                raise ValueError(f"{field} must name an existing contained file")
        return data
    except (OSError,ValueError) as exc:
        fail(f"resources/skill-contract.json: {exc}",errors)
        return None


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
    contract = load_skill_contract(root,errors)
    expected = set(contract['skills']) if contract else set()
    names = set()
    descriptions = set()
    for path in skills.glob("*/SKILL.md"):
        parsed = parse_frontmatter(path,errors,root)
        if not parsed: continue
        name,description = parsed
        if name != path.parent.name or name in names or description in descriptions:
            fail(f"Invalid/duplicate skill identity: {path.relative_to(root)}",errors)
        names.add(name); descriptions.add(description)
    if contract:
        for name in sorted(expected - names): fail(f"Missing plugin skill: {name}",errors)
        for name in sorted(names - expected): fail(f"Unexpected plugin skill: {name}",errors)
    for path in skills.rglob("SKILL.md"):
        if len(path.relative_to(skills).parts) != 2:
            fail(f"Nested plugin skill is not supported: {path.relative_to(root)}", errors)
    for tree in trees:
        for path in sorted(tree.rglob("*.md")):
            validate_local_links(path, errors, root)


def validate_catalog(errors: list[str]) -> None:
    contract=load_skill_contract(ROOT,errors)
    if not contract:return
    catalog=ROOT/contract['pattern_catalog']
    text=catalog.read_text(encoding='utf-8')
    matches=list(re.finditer(r"^## ([a-z0-9]+(?:-[a-z0-9]+)*): .+$",text,re.MULTILINE))
    if not matches:
        fail(f"{catalog.relative_to(ROOT)}: expected nonempty pattern catalog",errors);return
    ids=set()
    for index,match in enumerate(matches):
        ident=match.group(1)
        if ident in ids:fail(f"{catalog.relative_to(ROOT)}: duplicate pattern {ident}",errors)
        ids.add(ident)
        end=matches[index+1].start() if index+1<len(matches) else len(text)
        section=text[match.end():end]
        for heading in ("When it fits","Responsibilities and boundaries","Alternatives","Failure behavior","Acceptance examples"):
            value=re.search(r"^### "+re.escape(heading)+r"\n(.*?)(?=^### |\Z)",section,re.MULTILINE|re.DOTALL)
            if not value or not value.group(1).strip():fail(f"{catalog.relative_to(ROOT)}: {ident} missing {heading!r}",errors)


def validate_routing(known_skills: set[str], errors: list[str], routing: Path | None = None) -> None:
    routing = ROUTING if routing is None else routing
    if not routing.is_file():
        fail(f"Missing routing dataset: {routing.relative_to(ROOT)}", errors)
        return
    ids: set[str] = set()
    records: list[dict[str, object]] = []
    for number, line in enumerate(routing.read_text(encoding="utf-8").splitlines(), 1):
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"{routing.relative_to(ROOT)}:{number}: invalid JSON: {exc}", errors)
            continue
        if not isinstance(record, dict):
            fail(f"{routing.relative_to(ROOT)}:{number}: fixture must be a JSON object", errors)
            continue
        records.append(record)
        fixture_id = record.get("id")
        if not isinstance(fixture_id, str) or fixture_id in ids:
            fail(f"{routing.relative_to(ROOT)}:{number}: missing/duplicate id", errors)
        else:
            ids.add(fixture_id)
        for field in ("expected_skills", "must_not_route"):
            values = record.get(field)
            if not isinstance(values, list) or any(not isinstance(v, str) or v not in known_skills for v in values):
                fail(f"{routing.relative_to(ROOT)}:{number}: invalid {field}", errors)
            elif len(set(values)) != len(values):
                fail(f"{routing.relative_to(ROOT)}:{number}: duplicate {field}", errors)
        expected=record.get("expected_skills",[])
        prohibited=record.get("must_not_route",[])
        if isinstance(expected,list) and isinstance(prohibited,list) and any(isinstance(n,str) and n in prohibited for n in expected):
            fail(f"{routing.relative_to(ROOT)}:{number}: conflicting routes",errors)
        if "assertions" in record and (not isinstance(record["assertions"],list) or any(not isinstance(v,str) or not v.strip() for v in record["assertions"])):
            fail(f"{routing.relative_to(ROOT)}:{number}: invalid assertions",errors)
    required_ids = {
        "rag-two-step", "consequential-tool", "deterministic-routing", "hosting-choice",
        "security-review", "provider-migration", "old-package", "generic-dotnet-nullability",
    }
    missing = required_ids - ids
    if missing:
        fail(f"{routing.relative_to(ROOT)}: missing required fixtures: {', '.join(sorted(missing))}", errors)
    if not any(not record.get("expected_skills") for record in records):
        fail(f"{routing.relative_to(ROOT)}: needs at least one negative routing fixture", errors)


def validate_cases(errors: list[str], cases_path: Path | None = None) -> None:
    path = ROOT / 'resources/evaluations/skill-routing/architectural-assistant-cases.json' if cases_path is None else cases_path
    try:
        data=json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(data,dict) or type(data.get('schema_version')) is not int or data['schema_version'] != 1 or not isinstance(data.get('cases'),list) or not data['cases']:
            raise ValueError('expected schema_version 1 with nonempty cases list')
        ids=set()
        for item in data['cases']:
            if not isinstance(item,dict):raise ValueError('case must be an object')
            ident=item.get('id')
            if not isinstance(ident,str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',ident) or ident in ids:raise ValueError('invalid/duplicate case id')
            ids.add(ident)
            if not isinstance(item.get('prompt'),str) or not item['prompt'].strip():raise ValueError(f'{ident}: missing prompt')
            if item.get('process_owner') not in ('superpowers','project','none'):raise ValueError(f'{ident}: unknown process owner')
            files=item.get('repository_files')
            if not isinstance(files,dict):raise ValueError(f'{ident}: repository_files must be a mapping')
            for name,value in files.items():
                if not isinstance(name,str) or not name or Path(name).is_absolute() or '..' in Path(name).parts or '\\' in name or ':' in name or name=='.' or not isinstance(value,str):
                    raise ValueError(f'{ident}: unsafe fixture path or invalid content')
            for field in ('expected_behavior','forbidden_behavior'):
                values=item.get(field)
                if not isinstance(values,list) or not values or any(not isinstance(v,str) or not v.strip() for v in values):raise ValueError(f'{ident}: {field} must be nonempty strings')
    except (OSError,ValueError) as exc:fail(f'{path.relative_to(ROOT)}: {exc}',errors)


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
    contract = load_skill_contract(ROOT, errors)
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

    validate_catalog(errors)
    if contract:
        validate_routing(set(names), errors, ROOT / contract["routing_dataset"])
    validate_cases(errors)
    validate_hygiene(errors)
    validate_plugin(ROOT, errors)

    entrypoint_links = {
        ROOT / "README.md": [contract["pattern_catalog"] if contract else "resources/docs/patterns/catalog.md", contract["routing_dataset"] if contract else "resources/evaluations/skill-routing/v2.jsonl"],
        ROOT / "resources" / "docs" / "patterns" / "README.md": [Path(contract["pattern_catalog"]).name] if contract else ["catalog.md"],
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

    required_ci = [ROOT / ".github" / "workflows" / "validate.yml"]
    for workflow in required_ci:
        if not workflow.is_file():
            fail(f"Missing CI workflow: {workflow.relative_to(ROOT)}", errors)

    if errors:
        print("Template validation FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1
    pattern_count=len(re.findall(r"^## [a-z0-9-]+: ", (ROOT/contract["pattern_catalog"]).read_text(),re.MULTILINE))
    print(f"Template validation OK: {len(skill_files)} skills, {pattern_count} patterns, routing {Path(contract['routing_dataset']).stem}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
