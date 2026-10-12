"""Regression tests for validation against real temporary repository inputs."""
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "validate_template", Path(__file__).resolve().parents[1] / "scripts/validate-template.py"
)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class HygieneTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-q")
        (self.root / ".gitignore").write_text("__pycache__/\n*.pyc\n.env\n")

    def git(self, *args):
        return subprocess.run(
            ["git", "-C", str(self.root), *args], check=True, capture_output=True
        )

    def validate(self):
        errors = []
        with patch.object(validator, "ROOT", self.root):
            validator.validate_hygiene(errors)
        return errors

    def test_ignored_local_caches_and_private_files_do_not_fail_hygiene(self):
        cache = self.root / "scripts/__pycache__"
        cache.mkdir(parents=True)
        (cache / "check.pyc").write_bytes(b"cache")
        (self.root / ".env").write_text("local configuration")
        self.assertEqual(self.validate(), [])

    def test_tracked_ignored_cache_still_fails_hygiene(self):
        cache = self.root / "scripts/__pycache__"
        cache.mkdir(parents=True)
        (cache / "check.pyc").write_bytes(b"cache")
        self.git("add", "-f", "scripts/__pycache__/check.pyc")
        self.assertTrue(any("check.pyc" in error for error in self.validate()))

    def test_untracked_nonignored_artifact_fails_hygiene(self):
        (self.root / "sample.cs").write_text("class Sample {}")
        self.assertTrue(any("sample.cs" in error for error in self.validate()))


class RoutingTests(unittest.TestCase):
    def test_non_object_fixture_reports_validation_error_instead_of_crashing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            routing = root / "routing.jsonl"
            routing.write_text('[]\n')
            errors = []
            with patch.object(validator, "ROOT", root), patch.object(validator, "ROUTING", routing):
                validator.validate_routing({"maf-agents"}, errors)
            self.assertTrue(any("object" in error for error in errors))


class PluginHygieneTests(unittest.TestCase):
    def test_canonical_skills_are_allowed_and_duplicate_copies_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            canonical = root / "skills/maf-agents/SKILL.md"
            canonical.parent.mkdir(parents=True)
            canonical.write_text("developer skill")
            errors = []
            with patch.object(validator, "ROOT", root):
                validator.validate_hygiene(errors)
            self.assertEqual(errors, [])
            copied = root / ".agents/skills/maf-agents/SKILL.md"
            copied.parent.mkdir(parents=True)
            copied.write_text(canonical.read_text())
            errors = []
            with patch.object(validator, "ROOT", root):
                validator.validate_hygiene(errors)
            self.assertTrue(any("SKILL.md" in error for error in errors))

    def test_marketplace_catalog_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "marketplace.json").write_text('{"plugins":[]}')
            errors = []
            with patch.object(validator, "ROOT", root):
                validator.validate_hygiene(errors)
            self.assertTrue(any("Marketplace" in error for error in errors))

    def test_skill_copy_outside_plugin_is_still_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            copied = root / "runtime/skills/unsafe/SKILL.md"
            copied.parent.mkdir(parents=True)
            copied.write_text("unexpected runtime skill")
            errors = []
            with patch.object(validator, "ROOT", root):
                validator.validate_hygiene(errors)
            self.assertTrue(any("runtime/skills/unsafe/SKILL.md" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
