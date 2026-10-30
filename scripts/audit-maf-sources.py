#!/usr/bin/env python3
"""Audit official MAF sources and emit a Markdown report; never edits guidance."""
from __future__ import annotations

import argparse
import json
import re
import urllib.error
import urllib.request
from datetime import date
import socket
import ssl
from maf_knowledge import load_coverage, release_key, audit_fingerprint
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "resources" / "docs" / "capabilities" / "maf-dotnet-1.24.md"
SOURCES = [
    "https://learn.microsoft.com/en-us/agent-framework/agents/",
    "https://learn.microsoft.com/en-us/agent-framework/workflows/",
    "https://learn.microsoft.com/en-us/agent-framework/hosting/",
    "https://learn.microsoft.com/en-us/agent-framework/hosting/self-hosting/",
    "https://learn.microsoft.com/en-us/agent-framework/agents/background-responses",
    "https://learn.microsoft.com/en-us/agent-framework/agents/skills",
    "https://learn.microsoft.com/en-us/agent-framework/concepts/harness",
    "https://github.com/microsoft/agent-framework/releases",
]
EXPECTED_SIGNALS = {
    "https://learn.microsoft.com/en-us/agent-framework/hosting/": [
        "Foundry Hosted Agents", "generally available", "self-hosting", "protocol",
    ],
    "https://learn.microsoft.com/en-us/agent-framework/hosting/self-hosting/": [
        ".NET hosting packages are prerelease", "authentication", "authorization",
    ],
    "https://learn.microsoft.com/en-us/agent-framework/agents/background-responses": [
        "only agents that use the OpenAI Responses API", "continuation token",
    ],
    "https://learn.microsoft.com/en-us/agent-framework/agents/": [
        "Agent Hooks", "FIDES", "Agent Skills", "Harness Agent",
    ],
}
USER_AGENT = "maf-dotnet-guidance-source-audit/4.0"


def request(url: str) -> tuple[int, str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.status, response.geturl(), response.read().decode("utf-8", errors="replace")


def latest_dotnet_release() -> tuple[str, str]:
    req = urllib.request.Request(
        "https://api.github.com/repos/microsoft/agent-framework/releases?per_page=100",
        headers={"Accept": "application/vnd.github+json", "User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        releases = json.load(response)
    for release in releases:
        tag = str(release.get("tag_name", ""))
        if re.fullmatch(r"dotnet-\d+\.\d+\.\d+", tag) and not release.get("draft"):
            return tag, str(release.get("html_url", ""))
    raise RuntimeError("No published dotnet-* release found in first 100 releases")


def build_audit(coverage: dict, source_checks: list[dict], latest_release: str | None, release_error: str | None) -> dict:
    findings=[]
    assessed=coverage['last_assessed_release']['release']
    if latest_release and release_key(latest_release) > release_key(assessed):
        findings.append({'kind':'new_release','source':'github-dotnet-releases','detail':latest_release})
    if release_error:
        findings.append({'kind':'request_failure','source':'github-dotnet-releases','detail':release_error})
    for check in source_checks:
        source=check['source']
        if check.get('failure'):
            findings.append({'kind':'request_failure','source':source,'detail':check['failure']}); continue
        if check.get('final_url',source).rstrip('/') != source.rstrip('/'):
            findings.append({'kind':'redirect','source':source,'detail':check['final_url']})
        for signal in check.get('missing_signals',[]):
            findings.append({'kind':'content_signal','source':source,'detail':signal})
    findings=[json.loads(x) for x in sorted({json.dumps(f,sort_keys=True) for f in findings})]
    return {'schema_version':1,'audit_date':date.today().isoformat(),'full_verification':coverage['full_verification'],
            'last_assessed_release':coverage['last_assessed_release'],'latest_release':latest_release,
            'source_checks':source_checks,'findings':findings,'needs_review':bool(findings),
            'fingerprint':audit_fingerprint(findings,assessed)}


def render_report(audit: dict) -> str:
    lines=['# Scheduled MAF source audit','',f"<!-- maf-source-audit:{audit['fingerprint']} -->",'',
           f"- Audit date: {audit['audit_date']}",f"- Full verification: `{audit['full_verification']['release']}`",
           f"- Last release assessed for deltas: `{audit['last_assessed_release']['release']}`",
           f"- Latest published .NET release: `{audit['latest_release'] or 'unknown'}`",
           f"- Maintainer review required: **{'yes' if audit['needs_review'] else 'no'}**",'',
           'This automated audit is evidence only. Content signals and reachable links do not prove semantic correctness.',
           'Assessed releases do not advance full or per-area verification. Inspect coverage.json and dated evidence.','',
           '## Findings','']
    lines.extend(f"- {f['kind']}: {f['source']} — {f['detail']}" for f in audit['findings'])
    if not audit['findings']: lines.append('No new actionable findings.')
    lines.extend(['','## Source checks',''])
    for row in audit['source_checks']:
        lines.append(f"- {row['source']}: {row.get('status',row.get('failure','unknown'))}; {row.get('diagnostic',row.get('final_url',''))}")
    lines.extend(['','Review official .NET releases/tags and relevant published packages before updating owning references, patterns and fixtures. Do not infer APIs from phrase checks.'])
    return '\n'.join(lines)+'\n'


def failure_category(exc: Exception) -> str:
    reason=getattr(exc,'reason',exc)
    if isinstance(exc,urllib.error.HTTPError): return f'http-{exc.code}'
    if isinstance(reason,ssl.SSLError): return 'tls'
    if isinstance(reason,socket.gaierror): return 'dns'
    if isinstance(reason,(TimeoutError,socket.timeout)): return 'timeout'
    return 'unavailable'


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--json-output',type=Path)
    args=parser.parse_args()
    try: coverage=load_coverage(ROOT/'resources/docs/capabilities/coverage.json')
    except ValueError as exc:
        print(exc); return 2
    checks=[]
    for source in SOURCES:
        try:
            status,final_url,body=request(source)
            checks.append({'source':source,'status':status,'final_url':final_url,
                'missing_signals':[s for s in EXPECTED_SIGNALS.get(source,[]) if s.casefold() not in body.casefold()]})
        except (urllib.error.URLError,TimeoutError) as exc:
            checks.append({'source':source,'failure':failure_category(exc),'diagnostic':str(exc)})
    latest=None; error=None
    try: latest,_=latest_dotnet_release()
    except (urllib.error.URLError,TimeoutError,RuntimeError) as exc: error=failure_category(exc)
    result=build_audit(coverage,checks,latest,error)
    args.output.write_text(render_report(result),encoding='utf-8')
    if args.json_output: args.json_output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(f'Wrote audit report to {args.output}')
    return 1 if error or any(c.get('failure') for c in checks) else 0


if __name__ == '__main__':
    raise SystemExit(main())
