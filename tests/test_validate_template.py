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
    def test_v2_preserves_historical_scenarios_and_behavior(self):
        import json
        root=Path(__file__).resolve().parents[1]
        def records(name):return {r['id']:r for r in map(json.loads,(root/f'resources/evaluations/skill-routing/{name}.jsonl').read_text().splitlines())}
        old,new=records('v1'),records('v2')
        self.assertTrue(old.keys() <= new.keys())
        for ident,record in old.items():
            with self.subTest(id=ident):
                self.assertTrue(set(record.get('assertions',[])) <= set(new[ident].get('assertions',[])))
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
            with patch.object(validator,'ROOT',root),patch.object(validator,'CATALOG',p):validator.validate_catalog(errors)
            return errors
    def test_pattern_count_is_not_fixed_and_code_is_optional(self):
        for n in [1,18]:
            with self.subTest(n=n):self.assertEqual(self.run_catalog(self.catalog(n)),[])
    def test_duplicate_ids_and_missing_decision_sections_fail(self):
        self.assertTrue(self.run_catalog(self.catalog(2,duplicate=True)))
        for section in ['Alternatives','Acceptance examples']:
            self.assertTrue(self.run_catalog(self.catalog(missing=section)))
    def run_matrix(self,source='[Source](https://example.com)',release='dotnet-1.24.0',date='2027-01-15'):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);p=root/'matrix.md'
            p.write_text('Matrix version: 1\nLast verified MAF release: `dotnet-1.24.0`\nVerification date: 2026-10-12\n\n| Feature | .NET availability | Maturity | Required package/boundary | Provider or hosting restrictions | Official source | Verified release | Verified date |\n|---|---|---|---|---|---|---|---|\n'+f'| Example | Available | Stable | Core | Conditional | {source} | {release} | {date} |\n')
            errors=[]
            with patch.object(validator,'ROOT',root),patch.object(validator,'MATRIX',p):validator.validate_matrix(errors)
            return errors
    def test_valid_future_year_and_small_matrix_are_accepted(self):self.assertEqual(self.run_matrix(),[])
    def test_invalid_calendar_tag_and_absent_source_fail(self):
        for kwargs in [{'date':'2026-02-30'},{'release':'bad'},{'source':'none'}]:
            with self.subTest(kwargs=kwargs):self.assertTrue(self.run_matrix(**kwargs))

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

class MatrixCoverageConsistencyTests(unittest.TestCase):
    def test_missing_covered_feature_or_promoted_row_is_rejected(self):
        import json,shutil
        source=Path(__file__).resolve().parents[1]
        for mode in ['missing','promoted']:
            with self.subTest(mode=mode),tempfile.TemporaryDirectory() as directory:
                root=Path(directory);(root/'plugin.json').write_text('{}')
                shutil.copytree(source/'resources/docs/capabilities',root/'resources/docs/capabilities')
                coverage=root/'resources/docs/capabilities/coverage.json';data=json.loads(coverage.read_text())
                for area in data['areas']:
                    if area['id']=='streaming':area['feature']='Streaming'
                coverage.write_text(json.dumps(data))
                p=root/'resources/docs/capabilities/maf-dotnet-1.24.md';lines=p.read_text().splitlines()
                lines=[line for line in lines if not (mode=='missing' and line.startswith('| Streaming |'))]
                if mode=='promoted':lines=[line.replace('dotnet-1.24.0 | 2026-10-12','dotnet-1.26.0 | 2026-10-24') if line.startswith('| Streaming |') else line for line in lines]
                p.write_text('\n'.join(lines)+'\n');errors=[]
                with patch.object(validator,'ROOT',root),patch.object(validator,'MATRIX',p):validator.validate_matrix(errors)
                self.assertTrue(errors)
    def test_global_header_promotion_cannot_hide_unreviewed_areas(self):
        import json,shutil
        source=Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'plugin.json').write_text('{}')
            shutil.copytree(source/'resources/docs/capabilities',root/'resources/docs/capabilities')
            coverage=root/'resources/docs/capabilities/coverage.json';data=json.loads(coverage.read_text())
            data['full_verification'].update(release='dotnet-1.26.0',date='2026-10-24');coverage.write_text(json.dumps(data))
            p=root/'resources/docs/capabilities/maf-dotnet-1.24.md';s=p.read_text().replace('Last verified MAF release: `dotnet-1.24.0`. Verification date: 2026-10-12.','Last verified MAF release: `dotnet-1.26.0`. Verification date: 2026-10-24.');p.write_text(s)
            errors=[]
            with patch.object(validator,'ROOT',root),patch.object(validator,'MATRIX',p):validator.validate_matrix(errors)
            self.assertTrue(errors)
