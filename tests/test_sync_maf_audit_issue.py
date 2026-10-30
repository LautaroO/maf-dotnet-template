"""Issue synchronization is idempotent and refuses inconsistent reports."""
import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
SCRIPTS=Path(__file__).resolve().parents[1]/'scripts'; sys.path.insert(0,str(SCRIPTS))
def load(name,file):
    spec=importlib.util.spec_from_file_location(name,SCRIPTS/file)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
audit=load('audit_sync_source','audit-maf-sources.py')
sync=load('sync','sync-maf-audit-issue.py')

class IssueTests(unittest.TestCase):
    def setUp(self):
        self.data=audit.build_audit({'full_verification':{'release':'dotnet-1.24.0'},'last_assessed_release':{'release':'dotnet-1.26.0'}},[],'dotnet-1.27.0',None)
    def issue(self,number=7,body='',title='MAF source audit',state='OPEN'):
        return {'number':number,'body':body,'title':title,'state':state}
    def test_clean_does_not_mutate(self):
        clean=audit.build_audit(self.data,[],'dotnet-1.26.0',None)
        self.assertEqual(sync.notification_action(clean,[]),('none',None))
    def test_create_update_and_unchanged(self):
        self.assertEqual(sync.notification_action(self.data,[]),('create',None))
        self.assertEqual(sync.notification_action(self.data,[self.issue()]),('update',7))
        marker=f"<!-- maf-source-audit:{self.data['fingerprint']} -->"
        self.assertEqual(sync.notification_action(self.data,[self.issue(body=marker)]),('none',7))
    def test_exact_title_open_and_deterministic_selection(self):
        issues=[self.issue(1,title='MAF source audit other'),self.issue(2,state='CLOSED'),self.issue(9),self.issue(7)]
        self.assertEqual(sync.notification_action(self.data,issues),('update',7))
        self.assertEqual(sync.notification_action(self.data,issues[:2]),('create',None))
    def test_malformed_input_never_mutates(self):
        for bad in [[],self.data|{'schema_version':True},self.data|{'fingerprint':'wrong'},self.data|{'needs_review':False},self.data|{'findings':[{'kind':'unknown'}]}]:
            with self.subTest(bad=bad),self.assertRaises(ValueError):sync.notification_action(bad,[])
    def test_report_mismatch_is_rejected_before_gh(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'report.md';p.write_text('mismatch')
            def forbidden(args): self.fail('gh called for mismatched report')
            with self.assertRaises(ValueError): sync.sync_issue(self.data,p,forbidden)
    def test_gh_calls_use_file_body_and_never_comment(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'body with spaces.md';p.write_text(audit.render_report(self.data))
            calls=[]
            def gh(args):
                calls.append(args)
                return '[]' if args[:2]==['issue','list'] else 'ok'
            self.assertEqual(sync.sync_issue(self.data,p,gh),'create')
            self.assertEqual(calls[-1],['issue','create','--title','MAF source audit','--body-file',str(p)])
            self.assertFalse(any('comment' in call for call in calls))
    def test_repeated_report_causes_no_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'report.md';p.write_text(audit.render_report(self.data));calls=[]
            def gh(args):
                calls.append(args);return json.dumps([self.issue(body=p.read_text())])
            self.assertEqual(sync.sync_issue(self.data,p,gh),'none')
            self.assertEqual(len(calls),1)
    def test_gh_error_propagates_without_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'report.md';p.write_text(audit.render_report(self.data))
            def gh(args):raise RuntimeError('listing failed')
            with self.assertRaisesRegex(RuntimeError,'listing failed'):sync.sync_issue(self.data,p,gh)
