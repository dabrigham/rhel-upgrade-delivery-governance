#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


LOCAL_ATTRIBUTES = {"href", "src"}
IGNORED_SCHEMES = {"http", "https", "mailto", "tel", "data"}


@dataclass(frozen=True)
class LinkReference:
    source_file: Path
    tag: str
    attribute: str
    value: str


class LocalLinkParser(HTMLParser):
    def __init__(self, source_file: Path) -> None:
        super().__init__()
        self.source_file = source_file
        self.references: list[LinkReference] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for attribute, value in attrs:
            if attribute in LOCAL_ATTRIBUTES and value:
                self.references.append(LinkReference(self.source_file, tag, attribute, value))


def collect_references(html_path: Path) -> list[LinkReference]:
    parser = LocalLinkParser(html_path)
    parser.feed(html_path.read_text(encoding="utf-8"))
    return parser.references


def is_local_reference(value: str) -> bool:
    parsed = urlparse(value)
    if parsed.scheme in IGNORED_SCHEMES or parsed.netloc:
        return False
    if value.startswith("#"):
        return False
    return True


def resolve_local_reference(reference: LinkReference, web_root: Path) -> tuple[Path | None, str | None]:
    parsed = urlparse(reference.value)
    path_part = unquote(parsed.path)
    if not path_part:
        return None, None

    target = (reference.source_file.parent / path_part).resolve()
    try:
        target.relative_to(web_root)
    except ValueError:
        return target, "points outside web/"
    if not target.exists():
        return target, "missing local file"
    return target, None


def check_web_links(web_root: Path) -> list[str]:
    web_root = web_root.resolve()
    errors: list[str] = []
    html_files = sorted(web_root.rglob("*.html"))
    if not html_files:
        return [f"No HTML files found under {web_root}"]

    for html_path in html_files:
        for reference in collect_references(html_path):
            if not is_local_reference(reference.value):
                continue
            target, error = resolve_local_reference(reference, web_root)
            if error:
                relative_source = html_path.relative_to(web_root)
                target_display = target.relative_to(web_root) if target and error != "points outside web/" else target
                errors.append(
                    f"{relative_source}: {reference.tag}[{reference.attribute}]={reference.value!r} "
                    f"{error}: {target_display}"
                )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Check local links and assets in the static web bundle.")
    parser.add_argument("web_root", nargs="?", default="web", help="Static web root to check.")
    args = parser.parse_args()

    web_root = Path(args.web_root)
    errors = check_web_links(web_root)
    if errors:
        print("Web link check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Web link check passed: {web_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
