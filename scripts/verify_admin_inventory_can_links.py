#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression verification for clickable can/title edit links in admin inventory tables."""

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

TARGET_EDIT_HREF = "edit-monster.html"
EXPECTED_INVENTORY_ROWS = 10
EXPECTED_INVENTORY_COLS = 8
EXPECTED_ORDER_ROWS = 6

ANCHOR_RE = re.compile(r"<a\b([^>]*)>([\s\S]*?)</a>", re.IGNORECASE)
BUTTON_RE = re.compile(r"<button\b([^>]*)>([\s\S]*?)</button>", re.IGNORECASE)
ROW_RE = re.compile(r"<tr\b[^>]*>([\s\S]*?)</tr>", re.IGNORECASE)
CELL_RE = re.compile(r"<td\b[^>]*>([\s\S]*?)</td>", re.IGNORECASE)
IMG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
STRONG_RE = re.compile(r"<strong\b[^>]*>[\s\S]*?</strong>", re.IGNORECASE)


def extract_section_html(html: str, section_id: str) -> str | None:
    """Return inner HTML for a <section id="..."> block, or None if not found."""
    pattern = re.compile(
        rf'<section\b[^>]*\bid=["\']{re.escape(section_id)}["\'][^>]*>([\s\S]*?)</section>',
        re.IGNORECASE,
    )
    match = pattern.search(html)
    return match.group(1) if match else None


def extract_cart_table_tbody(container_html: str) -> str | None:
    """Return inner HTML of <tbody> inside the first <table class="...cart-table...">."""
    pattern = re.compile(
        r'<table\b[^>]*\bclass=["\'][^"\']*\bcart-table\b[^"\']*["\'][^>]*>'
        r"[\s\S]*?<tbody\b[^>]*>([\s\S]*?)</tbody>[\s\S]*?</table>",
        re.IGNORECASE,
    )
    match = pattern.search(container_html)
    return match.group(1) if match else None


def extract_rows(tbody_html: str) -> list[list[str]]:
    """Parse <tr> rows and their <td> cell inner HTML fragments from a <tbody>."""
    return [CELL_RE.findall(row_html) for row_html in ROW_RE.findall(tbody_html)]


def has_attr(attrs: str, name: str, value: str) -> bool:
    """Check whether an attribute string contains name="value" (or single-quoted)."""
    return bool(
        re.search(
            rf'\b{re.escape(name)}\s*=\s*["\']{re.escape(value)}["\']',
            attrs,
            re.IGNORECASE,
        )
    )


def has_class(attrs: str, class_name: str) -> bool:
    """Check whether an attribute string's class list contains class_name."""
    return bool(
        re.search(
            rf'\bclass\s*=\s*["\'][^"\']*\b{re.escape(class_name)}\b[^"\']*["\']',
            attrs,
            re.IGNORECASE,
        )
    )


def has_anchor_wrapping(cell_html: str, href: str, inner_pattern: re.Pattern[str]) -> bool:
    """Return True if cell_html has an <a href="..."> whose body matches inner_pattern."""
    for attrs, body in ANCHOR_RE.findall(cell_html):
        if has_attr(attrs, "href", href) and inner_pattern.search(body):
            return True
    return False


def verify_inventory_table(rel_path: str, section_id: str | None) -> list[str]:
    """Verify the 10-row inventory table in a given admin HTML file."""
    failures: list[str] = []
    file_path = ROOT / rel_path
    if not file_path.exists():
        return [f"{rel_path}: file not found"]

    html = file_path.read_text(encoding="utf-8")
    scope_label = f"{rel_path} (#{section_id})" if section_id else f"{rel_path} (.cart-table)"

    container = extract_section_html(html, section_id) if section_id else html
    if container is None:
        return [f"{scope_label}: section #{section_id} not found"]

    tbody_html = extract_cart_table_tbody(container)
    if tbody_html is None:
        return [f"{scope_label}: <table class=\"cart-table\"> <tbody> not found"]

    rows = extract_rows(tbody_html)
    if len(rows) != EXPECTED_INVENTORY_ROWS:
        failures.append(
            f"{scope_label}: expected {EXPECTED_INVENTORY_ROWS} <tr> rows, found {len(rows)}"
        )

    for idx, cells in enumerate(rows, start=1):
        row_label = f"{scope_label} row {idx}"
        if len(cells) != EXPECTED_INVENTORY_COLS:
            failures.append(
                f"{row_label}: expected {EXPECTED_INVENTORY_COLS} <td> columns, found {len(cells)}"
            )
            continue

        if not has_anchor_wrapping(cells[0], TARGET_EDIT_HREF, IMG_RE):
            failures.append(
                f'{row_label} col 1: missing <a href="{TARGET_EDIT_HREF}"> wrapping <img>'
            )

        if not has_anchor_wrapping(cells[1], TARGET_EDIT_HREF, STRONG_RE):
            failures.append(
                f'{row_label} col 2: missing <a href="{TARGET_EDIT_HREF}"> wrapping <strong>...</strong>'
            )
        col2_lower = cells[1].lower()
        if "<small" in col2_lower:
            failures.append(
                f"{row_label} col 2: unexpected <small> subtitle inside product name cell"
            )
        if "<br" in col2_lower:
            failures.append(
                f"{row_label} col 2: unexpected <br> line break inside product name cell"
            )

        action_cell = cells[-1]
        if "btn-view-detail" in action_cell:
            failures.append(f"{row_label} col 8: unexpected btn-view-detail in Thao Tác cell")
        if "fa-edit" in action_cell:
            failures.append(f"{row_label} col 8: unexpected fa-edit icon in Thao Tác cell")
        if re.search(rf'\bhref\s*=\s*["\']{re.escape(TARGET_EDIT_HREF)}["\']', action_cell):
            failures.append(
                f'{row_label} col 8: unexpected href="{TARGET_EDIT_HREF}" in Thao Tác cell'
            )

        del_buttons = [
            (attrs, body)
            for attrs, body in BUTTON_RE.findall(action_cell)
            if has_class(attrs, "cart-del-btn")
        ]
        if len(del_buttons) != 1:
            failures.append(
                f'{row_label} col 8: expected 1 <button class="cart-del-btn">, found {len(del_buttons)}'
            )
        else:
            btn_attrs, btn_body = del_buttons[0]
            if "fa-trash" not in btn_body:
                failures.append(f"{row_label} col 8: delete button missing fa-trash icon")
            if "handleAdminDeleteProduct(" not in btn_attrs:
                failures.append(
                    f"{row_label} col 8: delete button missing handleAdminDeleteProduct( handler"
                )

    return failures


def verify_orders_section(rel_path: str) -> list[str]:
    """Verify #orders-section retains all 6 order Chi Tiết detail links."""
    failures: list[str] = []
    file_path = ROOT / rel_path
    if not file_path.exists():
        return [f"{rel_path}: file not found"]

    html = file_path.read_text(encoding="utf-8")
    orders_section = extract_section_html(html, "orders-section")
    if orders_section is None:
        return [f"{rel_path}: section #orders-section not found"]

    tbody_html = extract_cart_table_tbody(orders_section)
    if tbody_html is None:
        return [f"{rel_path} (#orders-section): <table class=\"cart-table\"> <tbody> not found"]

    rows = extract_rows(tbody_html)
    if len(rows) != EXPECTED_ORDER_ROWS:
        failures.append(
            f"{rel_path} (#orders-section): expected {EXPECTED_ORDER_ROWS} order rows, found {len(rows)}"
        )

    detail_link_count = 0
    for idx, cells in enumerate(rows, start=1):
        if not cells:
            failures.append(f"{rel_path} (#orders-section) row {idx}: empty row")
            continue
        row_detail_links = [
            (attrs, body)
            for attrs, body in ANCHOR_RE.findall(cells[-1])
            if has_attr(attrs, "href", "order-detail.html")
            and has_class(attrs, "btn-view-detail")
            and "Chi Tiết" in body
        ]
        if len(row_detail_links) != 1:
            failures.append(
                f"{rel_path} (#orders-section) row {idx}: expected 1 btn-view-detail Chi Tiết link to order-detail.html, found {len(row_detail_links)}"
            )
        detail_link_count += len(row_detail_links)

    if detail_link_count != EXPECTED_ORDER_ROWS:
        failures.append(
            f"{rel_path} (#orders-section): expected {EXPECTED_ORDER_ROWS} order Chi Tiết links total, found {detail_link_count}"
        )

    return failures


def main() -> int:
    failures: list[str] = []
    targets = [
        ("admin/index.html", "inventory-section"),
        ("admin/inventory.html", None),
    ]
    for rel_path, section_id in targets:
        failures.extend(verify_inventory_table(rel_path, section_id))

    failures.extend(verify_orders_section("admin/index.html"))

    if failures:
        print(f"FAIL ({len(failures)} check(s) failed):")
        for item in failures:
            print(f"  - {item}")
        return 1

    print(
        "PASS: admin/index.html (#inventory-section) and admin/inventory.html (cart-table) "
        "all 10 rows link col 1 <img> and col 2 <strong> to edit-monster.html with clean "
        "delete-only Thao Tác, and #orders-section retains all 6 order Chi Tiết links."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
