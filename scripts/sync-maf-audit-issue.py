#!/usr/bin/env python3
"""Synchronize actionable audit findings; invoked only in the authorized CI job."""
from __future__ import annotations
import argparse
import importlib.util
import json
import subprocess
from datetime import date
from pathlib import Path
from typing import Callable
from maf_knowledge import audit_fingerprint, release_key

_spec=importlib.util.spec_from_file_location('maf_audit_report',Path(__file__).with_name('audit-maf-sources.py'))
_report=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_report)
TITLE='MAF source audit'


def validate_audit(audit: object) -> None:
    if not isinstance(audit,dict) or type(audit.get('schema_version')) is not int or audit['schema_version'] != 1:
        raise ValueError('audit: expected schema_version 1 object')
    try:
        date.fromisoformat(audit['audit_date'])
        release_key(audit['full_verification']['release'])
        assessed=audit['last_assessed_release']['release']; release_key(assessed)
        if audit['latest_release'] is not None: release_key(audit['latest_release'])
        findings=audit['findings']
        if not isinstance(findings,list): raise ValueError('findings must be a list')
        for f in findings:
            if not isinstance(f,dict) or set(f) != {'kind','source','detail'} or f['kind'] not in {'new_release','request_failure','redirect','content_signal'} or any(not isinstance(v,str) or not v for v in f.values()):
                raise ValueError('invalid finding')
        if type(audit['needs_review']) is not bool or audit['needs_review'] != bool(findings): raise ValueError('inconsistent needs_review')
        if audit['fingerprint'] != audit_fingerprint(findings,assessed): raise ValueError('invalid fingerprint')
        if not isinstance(audit['source_checks'],list): raise ValueError('invalid source checks')
        for row in audit['source_checks']:
            if not isinstance(row,dict) or not isinstance(row.get('source'),str): raise ValueError('invalid source row')
    except (KeyError,TypeError,ValueError) as exc:
        raise ValueError(f'invalid audit: {exc}') from exc


def notification_action(audit: dict, issues: list[dict]) -> tuple[str,int | None]:
    validate_audit(audit)
    if not audit['needs_review']: return 'none',None
    matches=[i for i in issues if i.get('title')==TITLE and i.get('state')=='OPEN' and type(i.get('number')) is int]
    if not matches: return 'create',None
    issue=min(matches,key=lambda i:i['number'])
    marker=f"<!-- maf-source-audit:{audit['fingerprint']} -->"
    return ('none' if marker in (issue.get('body') or '') else 'update'),issue['number']


def sync_issue(audit: dict, report_path: Path, run_gh: Callable[[list[str]],str]) -> str:
    validate_audit(audit)
    if report_path.read_text(encoding='utf-8') != _report.render_report(audit):
        raise ValueError('Markdown report does not match audit JSON')
    if not audit['needs_review']: return 'none'
    issues=json.loads(run_gh(['issue','list','--state','open','--search',f'{TITLE} in:title','--limit','1000','--json','number,title,body,state']))
    if not isinstance(issues,list) or any(not isinstance(i,dict) for i in issues): raise ValueError('invalid gh issue list')
    action,number=notification_action(audit,issues)
    if action=='create':run_gh(['issue','create','--title',TITLE,'--body-file',str(report_path)])
    elif action=='update':run_gh(['issue','edit',str(number),'--body-file',str(report_path)])
    return action


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument('--audit-json',required=True,type=Path)
    parser.add_argument('--report',required=True,type=Path)
    args=parser.parse_args()
    def gh(argv):return subprocess.run(['gh',*argv],check=True,capture_output=True,text=True).stdout
    try: action=sync_issue(json.loads(args.audit_json.read_text()),args.report,gh)
    except (ValueError,OSError,subprocess.CalledProcessError) as exc:
        print(f'Audit issue sync failed: {exc}'); return 1
    print(f'Audit issue sync: {action}'); return 0


if __name__=='__main__':raise SystemExit(main())
