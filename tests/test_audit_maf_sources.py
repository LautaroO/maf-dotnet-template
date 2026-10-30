"""Audit observable reports with controlled sources; never fetch the network."""
import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
SCRIPTS=Path(__file__).resolve().parents[1]/'scripts'
sys.path.insert(0,str(SCRIPTS))
spec=importlib.util.spec_from_file_location('audit',SCRIPTS/'audit-maf-sources.py')
audit=importlib.util.module_from_spec(spec); spec.loader.exec_module(audit)

class AuditTests(unittest.TestCase):
    def setUp(self):
        self.coverage={'full_verification':{'release':'dotnet-1.24.0'},'last_assessed_release':{'release':'dotnet-1.26.0'}}
    def build(self,latest='dotnet-1.26.0',checks=None,error=None):
        return audit.build_audit(self.coverage,checks or [],latest,error)
    def test_reviewed_delta_is_not_new_release(self):
        result=self.build(); self.assertFalse(result['needs_review'])
        self.assertIn('dotnet-1.24.0',audit.render_report(result)); self.assertIn('dotnet-1.26.0',audit.render_report(result))
    def test_new_release_and_lower_release(self):
        self.assertEqual(self.build('dotnet-1.27.0')['findings'][0]['kind'],'new_release')
        self.assertFalse(self.build('dotnet-1.25.0')['needs_review'])
    def test_missing_release_is_failure_not_release_evidence(self):
        result=self.build(None,error='tls')
        self.assertEqual([x['kind'] for x in result['findings']],['request_failure'])
        self.assertIsNone(result['latest_release'])
    def test_fingerprint_is_stable_for_order_duplicates_and_date(self):
        rows=[{'source':'https://one','failure':'timeout','diagnostic':'time 1'}, {'source':'https://two','missing_signals':['hello']}]
        a=self.build(checks=rows); rows[0]['diagnostic']='time 2'
        b=self.build(checks=list(reversed(rows))+rows)
        self.assertEqual(a['fingerprint'],b['fingerprint'])
        self.assertNotEqual(a['fingerprint'],self.build('dotnet-1.27.0',rows)['fingerprint'])
        self.assertNotEqual(a['fingerprint'],self.build(checks=[{'source':'https://two','missing_signals':['bye']}])['fingerprint'])
    def test_redirect_and_content_are_not_semantic_verification(self):
        r=self.build(checks=[{'source':'https://a','final_url':'https://b','missing_signals':['text']}])
        self.assertEqual({x['kind'] for x in r['findings']},{'redirect','content_signal'})
        self.assertIn('evidence only',audit.render_report(r))
    def test_cli_preserves_markdown_and_writes_matching_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            md=Path(tmp)/'audit.md'; js=Path(tmp)/'audit.json'
            with patch.object(audit,'request',return_value=(200,'https://test','')),patch.object(audit,'SOURCES',[]),patch.object(audit,'latest_dotnet_release',return_value=('dotnet-1.26.0','https://release')),patch.object(sys,'argv',['audit','--output',str(md),'--json-output',str(js)]):
                self.assertEqual(audit.main(),0)
            result=json.loads(js.read_text()); self.assertFalse(result['needs_review'])
            self.assertIn(result['fingerprint'],md.read_text())
    def test_request_errors_still_write_usable_reports(self):
        import urllib.error
        with tempfile.TemporaryDirectory() as tmp:
            md=Path(tmp)/'audit.md'; js=Path(tmp)/'audit.json'
            with patch.object(audit,'request',side_effect=urllib.error.URLError('DNS unavailable')),patch.object(audit,'latest_dotnet_release',side_effect=TimeoutError()),patch.object(sys,'argv',['audit','--output',str(md),'--json-output',str(js)]):
                self.assertEqual(audit.main(),1)
            r=json.loads(js.read_text()); self.assertTrue(r['needs_review'])
            self.assertTrue(all(x['kind']=='request_failure' for x in r['findings']))
