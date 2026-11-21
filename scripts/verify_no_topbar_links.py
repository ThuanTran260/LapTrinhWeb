#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify .top-links removal across all 14 storefront HTML pages and css/style.css."""

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

FORBIDDEN_TOPBAR_LABELS = (
    "Tiếp Tục Mua Sắm",
    "Giao 2H Hoả Tốc",
    "Quay Lại Cửa Hàng",
    "Quay Lại Giỏ Hàng",
    "Hỗ Trợ 24/7",
)


def extract_div_block(html: str, class_or_id_pattern: str) -> str:
    """Return the balanced <div ...>...</div> block matching class_or_id_pattern."""
    match = re.search(rf"<div\b[^>]*{class_or_id_pattern}[^>]*>", html)
    if not match:
        return ""
    depth = 1
    pos = match.end()
    for tag in re.finditer(r"<(/?)div\b[^>]*>", html[pos:]):
        depth += -1 if tag.group(1) else 1
        if depth == 0:
            return html[match.start() : pos + tag.end()]
    return ""


def get_storefront_pages() -> list[Path]:
    """Return index.html and all 13 pages/*.html storefront pages."""
    pages = [ROOT / "index.html"]
    pages.extend(sorted((ROOT / "pages").glob("*.html")))
    return pages


def verify_page(path: Path) -> list[str]:
    """Verify a single storefront HTML page retains .top-bar/.announcement-text and has no .top-links."""
    rel = path.relative_to(ROOT).as_posix()
    failures: list[str] = []
    if not path.is_file():
        return [f"{rel}: missing file"]

    html = path.read_text(encoding="utf-8")

    top_bar = extract_div_block(html, r'class="[^"]*\btop-bar\b[^"]*"')
    if not top_bar:
        failures.append(f"{rel}: missing .top-bar block")
    else:
        if not re.search(r'class="[^"]*\bannouncement-text\b[^"]*"', top_bar):
            failures.append(f"{rel}: .top-bar missing .announcement-text")
        if re.search(r'class="[^"]*\btop-links\b[^"]*"', top_bar):
            failures.append(f"{rel}: .top-bar must NOT contain .top-links")
        for label in FORBIDDEN_TOPBAR_LABELS:
            if label in top_bar:
                failures.append(f"{rel}: .top-bar must NOT contain link label '{label}'")

    if re.search(r'class="[^"]*\btop-links\b[^"]*"', html):
        failures.append(f"{rel}: page must NOT contain class='top-links'")

    return failures


def verify_css(css_path: Path) -> list[str]:
    """Verify css/style.css contains no .top-links rules while retaining .top-bar and .announcement-text."""
    failures: list[str] = []
    if not css_path.is_file():
        return ["css/style.css: missing file"]

    css = css_path.read_text(encoding="utf-8")
    if re.search(r"\.top-links\b", css):
        failures.append("css/style.css: must NOT contain .top-links rules")
    if not re.search(r"\.top-bar\s*\{", css):
        failures.append("css/style.css: missing .top-bar rule")
    if not re.search(r"\.announcement-text\s*\{", css):
        failures.append("css/style.css: missing .announcement-text rule")
    return failures


def main() -> int:
    pages = get_storefront_pages()
    if len(pages) != 14:
        print(f"FAIL: expected 14 storefront pages (index.html + 13 pages/*.html), found {len(pages)}")
        return 1

    failures: list[str] = []
    for page in pages:
        failures.extend(verify_page(page))
    failures.extend(verify_css(ROOT / "css" / "style.css"))

    if failures:
        print(f"FAIL ({len(failures)} checks failed):")
        for item in failures:
            print(f"  - {item}")
        return 1

    print(
        f"ALL CHECKS PASSED: {len(pages)} storefront pages retain .top-bar/.announcement-text with zero .top-links, and css/style.css retains .top-bar/.announcement-text without .top-links."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
