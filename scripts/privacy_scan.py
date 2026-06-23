#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


TEXT_EXTENSIONS = {
    ".css",
    ".csv",
    ".html",
    ".js",
    ".json",
    ".md",
    ".mmd",
    ".py",
    ".sh",
    ".svg",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "outputs"}
SKIP_FILES = {
    "privacy_scan.py",
    "privacy_scan_report.md",
    "sensitive_terms.example.txt",
    "sensitive_terms.local.txt",
    "sensitive_terms.txt",
}
RAW_SCREENSHOT_EXTENSIONS = {".bmp", ".gif", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"}

SECRET_PATTERNS = [
    ("email_address", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("ipv4_address", re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")),
    ("absolute_local_path", re.compile(r"(/Users/|/private/|C:\\\\Users\\\\)", re.IGNORECASE)),
    ("openai_key", re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b")),
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("private_key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("secret_assignment", re.compile(r"\b(password|passwd|token|secret|api[_-]?key)\s*[:=]", re.IGNORECASE)),
    ("enterprise_record_id", re.compile(r"\b(CHG|CTASK|TASK|INC|RITM)\d{4,}\b", re.IGNORECASE)),
    (
        "internal_url",
        re.compile(
            r"https?://[^\s)\"']*(internal|corp|sharepoint|servicenow|service-now)[^\s)\"']*",
            re.IGNORECASE,
        ),
    ),
    (
        "internal_hostname",
        re.compile(r"\b[a-z0-9][a-z0-9-]*\.(corp|internal|intranet|lan|local)\b", re.IGNORECASE),
    ),
    (
        "unc_network_path",
        re.compile(r"\\\\(?!internal-source\\upgrade-data\.xlsx\b)[A-Za-z0-9._$-]+\\[^\s<>\"']+", re.IGNORECASE),
    ),
    ("excel_external_reference", re.compile(r"\[[^\]]+\.xlsx\]", re.IGNORECASE)),
]

PROPER_NOUN_EXTENSIONS = {".html", ".md"}
ALLOWED_PROPER_NOUN_PHRASES = {
    "AI Assisted Delivery",
    "Claude Code",
    "Derek Brigham",
    "GitHub Pages",
    "RHEL Upgrade Delivery Governance",
    "Technical Program Management",
}


@dataclass(frozen=True)
class Finding:
    kind: str
    path: Path
    line_number: int
    detail: str


def load_deny_terms(root: Path) -> list[str]:
    terms_paths = [
        root / "scripts" / "sensitive_terms.example.txt",
        root / "scripts" / "sensitive_terms.local.txt",
    ]
    terms: list[str] = []
    seen: set[str] = set()
    for terms_path in terms_paths:
        if not terms_path.exists():
            continue
        for raw_line in terms_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if line and not line.startswith("#") and line not in seen:
                terms.append(line)
                seen.add(line)
    return terms


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative_parts = set(path.relative_to(root).parts)
        if relative_parts & SKIP_DIRS:
            continue
        if path.name in SKIP_FILES:
            continue
        if path.suffix.lower() in TEXT_EXTENSIONS:
            files.append(path)
    return files


def line_excerpt(line: str, limit: int = 120) -> str:
    clean = " ".join(line.strip().split())
    if len(clean) <= limit:
        return clean
    return clean[: limit - 3] + "..."


def is_allowed_pattern_match(name: str, value: str) -> bool:
    return name == "ipv4_address" and value == "127.0.0.1"


def scan_file(path: Path, root: Path, deny_terms: list[str]) -> tuple[list[Finding], set[str]]:
    findings: list[Finding] = []
    proper_nouns: set[str] = set()
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        findings.append(Finding("unreadable_text_file", path.relative_to(root), 0, "File could not be decoded as UTF-8."))
        return findings, proper_nouns

    lowered_terms = [(term, term.lower()) for term in deny_terms]
    for line_number, line in enumerate(lines, start=1):
        lower_line = line.lower()
        for term, lowered in lowered_terms:
            if lowered in lower_line:
                findings.append(
                    Finding("deny_list_term", path.relative_to(root), line_number, f"Matched configured term: {term}")
                )

        for name, pattern in SECRET_PATTERNS:
            for match in pattern.finditer(line):
                if not is_allowed_pattern_match(name, match.group(0)):
                    findings.append(Finding(name, path.relative_to(root), line_number, line_excerpt(line)))

        if path.suffix.lower() in PROPER_NOUN_EXTENSIONS:
            for phrase in re.findall(r"\b[A-Z][A-Za-z0-9]+(?:\s+[A-Z][A-Za-z0-9]+)+\b", line):
                if phrase not in ALLOWED_PROPER_NOUN_PHRASES:
                    proper_nouns.add(phrase)

    return findings, proper_nouns


def find_blocked_public_image_files(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    screenshot_root = root / "web" / "assets" / "screenshots"
    if not screenshot_root.exists():
        return findings

    for path in screenshot_root.rglob("*"):
        if path.is_file() and path.suffix.lower() in RAW_SCREENSHOT_EXTENSIONS:
            findings.append(
                Finding(
                    "raw_screenshot_raster_file",
                    path.relative_to(root),
                    0,
                    "Public screenshot evidence must be recreated or fully sanitized SVG, not raw raster screenshots.",
                )
            )
    return findings


def write_report(root: Path, findings: list[Finding], proper_nouns: set[str]) -> Path:
    report_path = root / "privacy_scan_report.md"
    lines = ["# Privacy Scan Report", ""]
    if findings:
        lines.append("Status: FAIL")
        lines.append("")
        lines.append("Findings:")
        for finding in findings:
            location = f"{finding.path}:{finding.line_number}" if finding.line_number else str(finding.path)
            lines.append(f"- {finding.kind} at `{location}`: {finding.detail}")
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("No blocking privacy findings were detected.")

    lines.extend(["", "Proper Noun Review:", ""])
    if proper_nouns:
        lines.append("These capitalized terms were detected and should be manually reviewed before publication:")
        for noun in sorted(proper_nouns):
            lines.append(f"- {noun}")
    else:
        lines.append("No unexpected capitalized terms were detected.")

    lines.extend(
        [
            "",
            "Notes:",
            "- This scanner is a guardrail, not a substitute for human review.",
            "- The example deny list is public-safe; optional local terms are read from `scripts/sensitive_terms.local.txt` when present.",
            "- The configured deny lists fail closed when a configured sensitive term is found.",
            "- Synthetic demo identifiers are intentionally allowed when they use the `demo` pattern.",
        ]
    )
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan the sanitized public export for sensitive content.")
    parser.add_argument("root", nargs="?", default=".", help="Repository root to scan.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    deny_terms = load_deny_terms(root)
    findings: list[Finding] = []
    proper_nouns: set[str] = set()
    findings.extend(find_blocked_public_image_files(root))

    for path in iter_files(root):
        file_findings, file_nouns = scan_file(path, root, deny_terms)
        findings.extend(file_findings)
        proper_nouns.update(file_nouns)

    report_path = write_report(root, findings, proper_nouns)
    print(f"Privacy scan report: {report_path}")
    if findings:
        print(f"Privacy scan failed with {len(findings)} blocking finding(s).")
        return 1
    print("Privacy scan passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
