#!/usr/bin/env python3
"""Audit official MAF sources and emit a Markdown report; never edits guidance."""
from __future__ import annotations

import argparse
import json
import re
import urllib.error
import urllib.request
from datetime import date
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    matrix_text = MATRIX.read_text(encoding="utf-8")
    baseline_match = re.search(r"Last verified MAF release: `([^`]+)`", matrix_text)
    baseline = baseline_match.group(1) if baseline_match else "unknown"

    rows = []
    failures = []
    for source in SOURCES:
        try:
            status, final_url, body = request(source)
            notes = ["redirected"] if final_url.rstrip("/") != source.rstrip("/") else []
            missing_signals = [signal for signal in EXPECTED_SIGNALS.get(source, []) if signal.casefold() not in body.casefold()]
            if missing_signals:
                notes.append("maturity/content changed: missing " + ", ".join(missing_signals))
            note = "; ".join(notes) if notes else "ok"
            rows.append((source, status, final_url, note))
        except (urllib.error.URLError, TimeoutError) as exc:
            failures.append(f"{source}: {exc}")

    latest = "unknown"
    release_url = ""
    try:
        latest, release_url = latest_dotnet_release()
    except (urllib.error.URLError, TimeoutError, RuntimeError) as exc:
        failures.append(f"GitHub release lookup: {exc}")

    needs_review = latest != baseline or bool(failures) or any(row[3] != "ok" for row in rows)
    lines = [
        "# Scheduled MAF source audit",
        "",
        f"- Audit date: {date.today().isoformat()}",
        f"- Matrix baseline: `{baseline}`",
        f"- Latest published .NET release: [`{latest}`]({release_url})" if release_url else f"- Latest published .NET release: `{latest}`",
        f"- Maintainer review required: **{'yes' if needs_review else 'no'}**",
        "",
        "This automated audit is evidence only. It does not edit the capability matrix or guidance.",
        "",
        "## Source checks",
        "",
        "| Requested source | Status | Final URL | Note |",
        "|---|---:|---|---|",
    ]
    lines.extend(f"| {source} | {status} | {final_url} | {note} |" for source, status, final_url, note in rows)
    if failures:
        lines.extend(["", "## Failures", "", *[f"- {failure}" for failure in failures]])
    lines.extend([
        "",
        "## Maintainer checklist",
        "",
        "- Review release notes and official .NET package/API changes.",
        "- Check maturity changes, especially hosting, declarative features, runtime Agent Skills, Harness, Agent Hooks and FIDES.",
        "- Review redirects before updating official-source links.",
        "- Update guidance, matrix metadata, changelog and routing fixtures manually when evidence warrants it.",
    ])
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote audit report to {args.output}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
