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

class RoutingMigrationTests(unittest.TestCase):
    def test_active_routes_match_declared_skills(self):
        root=Path(__file__).resolve().parents[1]
        errors=[];contract=validator.load_skill_contract(root,errors)
        validator.validate_routing(set(contract['skills']),errors,root/contract['routing_dataset'])
        self.assertEqual(errors,[])
    def test_conflicting_or_duplicate_routes_are_rejected(self):
        import json
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);p=root/'routing.jsonl'
            p.write_text(json.dumps({'id':'one','prompt':'test','expected_skills':['maf-review','maf-review'],'must_not_route':['maf-review']})+'\n')
            errors=[]
            with patch.object(validator,'ROOT',root):validator.validate_routing({'maf-review'},errors,p)
            self.assertTrue(any('duplicate' in e for e in errors))
            self.assertTrue(any('conflicting' in e for e in errors))

class KnowledgeDocumentTests(unittest.TestCase):
    def catalog(self,count=1,missing=None,duplicate=False):
        headings=['When it fits','Responsibilities and boundaries','Alternatives','Failure behavior','Acceptance examples']
        return '\n'.join('## '+('same' if duplicate else f'case-{i}')+': Example\n'+''.join(f'### {h}\nConcrete example.\n' for h in headings if h != missing) for i in range(count))+'\n'
    def run_catalog(self,text):
        import json
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'resources').mkdir();p=root/'catalog.md';p.write_text(text);(root/'routing.jsonl').write_text('{}')
            (root/'resources/skill-contract.json').write_text(json.dumps({'schema_version':1,'skills':['maf-review'],'retired_routes':{},'routing_dataset':'routing.jsonl','pattern_catalog':'catalog.md'}))
            errors=[]
            with patch.object(validator,'ROOT',root):validator.validate_catalog(errors)
            return errors
    def test_pattern_count_is_not_fixed_and_code_is_optional(self):
        for n in [1,18]:
            with self.subTest(n=n):self.assertEqual(self.run_catalog(self.catalog(n)),[])
    def test_duplicate_ids_and_missing_decision_sections_fail(self):
        self.assertTrue(self.run_catalog(self.catalog(2,duplicate=True)))
        for section in ['Alternatives','Acceptance examples']:
            self.assertTrue(self.run_catalog(self.catalog(missing=section)))
class AssistantCaseTests(unittest.TestCase):
    def setUp(self):
        self.case={'id':'example','prompt':'Design an assistant','repository_files':{},'process_owner':'none','expected_behavior':['Ask a material question'],'forbidden_behavior':['Invent project facts']}
    def run_cases(self,data):
        import json
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);p=root/'cases.json';p.write_text(json.dumps(data));errors=[]
            with patch.object(validator,'ROOT',root):validator.validate_cases(errors,p)
            return errors
    def test_greenfield_empty_repository_is_valid(self):self.assertEqual(self.run_cases({'schema_version':1,'cases':[self.case]}),[])
    def test_duplicate_ids_and_invalid_process_fail(self):
        self.assertTrue(self.run_cases({'schema_version':1,'cases':[self.case,self.case]}))
        self.assertTrue(self.run_cases({'schema_version':1,'cases':[self.case|{'process_owner':'unknown'}]}))
    def test_unsafe_paths_and_malformed_fixtures_fail(self):
        for files in [{'../outside':'x'},{'/tmp/out':'x'},{'C:\\tmp\\out':'x'},{'src/../out':'x'},['not a mapping'],{'safe':None}]:
            with self.subTest(files=files):self.assertTrue(self.run_cases({'schema_version':1,'cases':[self.case|{'repository_files':files}]}))
    def test_absent_behavior_and_bad_schema_fail(self):
        for data in [[],{'schema_version':True,'cases':[self.case]},{'schema_version':1,'cases':[self.case|{'expected_behavior':[]}]}]:
            self.assertTrue(self.run_cases(data))
    def test_every_behavior_case_has_an_active_route(self):
        import json
        root=Path(__file__).resolve().parents[1]
        cases=json.loads((root/'resources/evaluations/skill-routing/architectural-assistant-cases.json').read_text())['cases']
        records={r['id']:r for r in map(json.loads,(root/'resources/evaluations/skill-routing/v2.jsonl').read_text().splitlines())}
        for case in cases:
            self.assertIn(case['id'],records)
            self.assertTrue(set(case['expected_behavior']+['must not: '+v for v in case['forbidden_behavior']]) <= set(records[case['id']].get('assertions',[])))

class ConceptSourceValidationTests(unittest.TestCase):
    def test_source_export_validates_without_release_knowledge_or_audit(self):
        import shutil,subprocess,sys
        source=Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for name in ['skills','resources','docs','scripts','.github']:
                shutil.copytree(source/name,root/name,ignore=shutil.ignore_patterns('__pycache__'))
            for name in ['plugin.json','VERSION','LICENSE','README.md','AGENTS.md','CHANGELOG.md']:
                shutil.copy2(source/name,root/name)
            shutil.rmtree(root/'resources/docs/capabilities',ignore_errors=True)
            for name in ['scripts/maf_knowledge.py','scripts/audit-maf-sources.py','scripts/sync-maf-audit-issue.py','.github/workflows/source-audit.yml']:
                (root/name).unlink(missing_ok=True)
            result=subprocess.run([sys.executable,'-B','scripts/validate-template.py'],cwd=root,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
