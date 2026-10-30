"""Check the repository-root plugin using isolated installation fixtures."""
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_template", REPO / "scripts/validate-template.py")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class PluginLayoutTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue((REPO / "plugin.json").is_file(), "Repository-root plugin is not implemented")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "installed"
        self.root.mkdir()
        for directory in ("skills", "resources"):
            shutil.copytree(REPO / directory, self.root / directory)
        for filename in ("plugin.json", "VERSION", "LICENSE"):
            shutil.copy2(REPO / filename, self.root / filename)

    def validate(self):
        errors = []
        validator.validate_plugin(self.root, errors)
        return errors

    def test_standalone_installation_matches_declared_skills_and_resources(self):
        self.assertEqual(self.validate(), [])
        self.assertEqual({p.parent.name for p in (self.root / "skills").glob("*/SKILL.md")}, set(json.loads((self.root/"resources/skill-contract.json").read_text())["skills"]))

    def test_manifest_version_must_match_release_version(self):
        (self.root / "VERSION").write_text("99.0.0")
        self.assertTrue(any("version" in e.lower() for e in self.validate()))

    def test_missing_manifest_is_reported(self):
        (self.root / "plugin.json").unlink()
        self.assertTrue(any("plugin.json" in e for e in self.validate()))

    def test_non_object_manifest_is_reported_without_crashing(self):
        (self.root / "plugin.json").write_text("[]")
        self.assertTrue(any("object" in e for e in self.validate()))

    def test_manifest_directory_is_rejected(self):
        path = self.root / "plugin.json"
        path.unlink()
        path.mkdir()
        self.assertTrue(any("plugin.json" in e for e in self.validate()))

    def test_resource_file_cannot_replace_resource_directory(self):
        path = self.root / "resources"
        shutil.rmtree(path)
        path.write_text("not a resource tree")
        self.assertTrue(any("resources" in e and "directory" in e for e in self.validate()))

    def test_missing_transitive_reference_is_reported(self):
        source = self.root / "skills/maf-implementation/references/agents.md"
        source.write_text(source.read_text() + "\n[Missing](missing.md)\n")
        self.assertTrue(any("missing.md" in e for e in self.validate()))

    def test_reference_escape_is_reported(self):
        source = self.root / "skills/maf-implementation/SKILL.md"
        source.write_text(source.read_text() + "\n[Unsafe](../../../outside.md)\n")
        self.assertTrue(any("escapes" in e for e in self.validate()))

    def test_resource_symlink_is_rejected(self):
        source = self.root / "resources/references/official-sources.md"
        source.unlink()
        source.symlink_to(REPO / "resources/references/official-sources.md")
        self.assertTrue(any("symlink" in e.lower() for e in self.validate()))

    def test_missing_or_extra_skill_is_reported(self):
        shutil.rmtree(self.root / "skills/maf-implementation")
        extra = self.root / "skills/unexpected/SKILL.md"
        extra.parent.mkdir()
        extra.write_text("---\nname: unexpected\ndescription: Unexpected skill.\n---\n")
        errors = self.validate()
        self.assertTrue(any("maf-implementation" in e for e in errors))
        self.assertTrue(any("unexpected" in e for e in errors))

    def test_validation_does_not_modify_the_installed_package(self):
        manifest = self.root / "plugin.json"
        manifest.write_text('{"name":"wrong","version":"0.0.0"}')
        before = {p.relative_to(self.root): p.read_bytes()
                  for p in self.root.rglob("*") if p.is_file()}
        self.assertTrue(self.validate())
        self.assertEqual(before, {p.relative_to(self.root): p.read_bytes()
                                 for p in self.root.rglob("*") if p.is_file()})


if __name__ == "__main__":
    unittest.main()

class SkillContractTests(unittest.TestCase):
    setUp = PluginLayoutTests.setUp
    validate = PluginLayoutTests.validate
    def contract(self):
        return json.loads((self.root/'resources/skill-contract.json').read_text())
    def write_contract(self,data):
        (self.root/'resources/skill-contract.json').write_text(json.dumps(data))
    def test_declared_extension_needs_no_hardcoded_inventory_change(self):
        data=self.contract(); data['skills'].append('maf-example'); self.write_contract(data)
        p=self.root/'skills/maf-example/SKILL.md';p.parent.mkdir();p.write_text('---\nname: maf-example\ndescription: Use when testing declared extension behavior.\n---\n')
        self.assertEqual(self.validate(),[])
    def test_missing_duplicate_and_invalid_contract_are_rejected(self):
        for data in [[],{}, {'schema_version':True},self.contract()|{'skills':['maf-review','maf-review']}]:
            with self.subTest(data=data):
                self.write_contract(data);self.assertTrue(self.validate())
    def test_contract_paths_cannot_escape_or_be_missing(self):
        original=self.contract()
        for value in ['../outside.jsonl','/tmp/external.jsonl','resources/missing.jsonl']:
            self.write_contract(original|{'routing_dataset':value})
            self.assertTrue(self.validate())
    def test_retired_name_cannot_be_active_or_target_unknown(self):
        data=self.contract(); old=next(iter(data['retired_routes']))
        data['skills'].append(old);self.write_contract(data);self.assertTrue(self.validate())
        data=self.contract();data['retired_routes'][old]='unknown';self.write_contract(data);self.assertTrue(self.validate())
