"""Conservative, heuristic preflight checks for proposed unified diffs.

This is not a sandbox, static analyzer, or proof of safety. It only flags a few
high-risk patterns in added lines so reviewers have actionable reasons to pause.
"""
from __future__ import annotations

import re
from typing import Any

_RISK_PATTERNS: tuple[tuple[str, re.Pattern[str], str], ...] = (
    ("dynamic_execution", re.compile(r"\b(eval|exec)\s*\("), "Dynamic code execution pattern"),
    ("shell_execution", re.compile(r"\b(os\.system|subprocess\.(run|Popen|call|check_output))\s*\("), "Shell or subprocess execution pattern"),
    ("unsafe_deserialization", re.compile(r"\bpickle\.(loads|load)\s*\("), "Unsafe pickle deserialization pattern"),
    ("network_access", re.compile(r"\b(requests\.(get|post|put|delete)|urllib\.request\.urlopen|httpx\.(get|post))\s*\("), "Network request pattern"),
    ("secret_access", re.compile(r"\b(os\.environ|os\.getenv)\b|\b(?:API_KEY|SECRET_KEY|TOKEN)\b"), "Possible environment or secret access"),
)

def inspect_patch(patch: str) -> dict[str, Any]:
    """Return transparent diff-format and added-line heuristic findings."""
    text = patch or ""
    added = [line[1:] for line in text.splitlines() if line.startswith("+") and not line.startswith("+++")]
    has_hunk = any(line.startswith("@@") for line in text.splitlines())
    has_file_header = any(line.startswith(("--- ", "+++ ")) for line in text.splitlines())
    findings: list[dict[str, str]] = []
    for rule_id, pattern, label in _RISK_PATTERNS:
        if any(pattern.search(line) for line in added):
            findings.append({"id": rule_id, "severity": "warning", "message": label + " in added diff lines; inspect the surrounding context."})

    if not text.strip():
        findings.append({"id": "empty_patch", "severity": "info", "message": "No patch was proposed; request more context or inspect the diagnosis."})
    elif not (has_hunk and has_file_header):
        findings.append({"id": "diff_format", "severity": "warning", "message": "Missing basic unified-diff file headers or hunk marker; do not apply it as-is."})
    if len(text) > 20000:
        findings.append({"id": "large_patch", "severity": "warning", "message": "Patch exceeds 20,000 characters; split it into smaller reviewable changes."})

    warnings = sum(item["severity"] == "warning" for item in findings)
    if warnings:
        status = "REVIEW REQUIRED"
    elif not text.strip():
        status = "NO PATCH"
    else:
        status = "NO HEURISTIC FLAGS"
    return {
        "status": status,
        "warning_count": warnings,
        "added_lines_checked": len(added),
        "checks": ["unified-diff shape", "dynamic execution", "shell/subprocess calls", "unsafe pickle loading", "network request patterns", "possible secret access", "patch size"],
        "findings": findings,
        "limitations": "Heuristic preflight only. No code was executed; absence of flags does not establish correctness or safety.",
    }
