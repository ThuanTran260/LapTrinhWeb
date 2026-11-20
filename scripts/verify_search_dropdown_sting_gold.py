from pathlib import Path
import glob
import os
import re
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT_DIR)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

checks = []


def check(name, condition, details=""):
    checks.append((name, condition, details))
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {name} - {details}")


def extract_search_static_lists(html):
    """Extract full <div class="...search-static-list...">...</div> blocks using div nesting depth."""
    lists = []
    for match in re.finditer(r'<div\b[^>]*class="[^"]*\bsearch-static-list\b[^"]*"[^>]*>', html):
        depth = 1
        pos = match.end()
        for tag in re.finditer(r'<(/?)div\b[^>]*>', html[pos:]):
            depth += -1 if tag.group(1) else 1
            if depth == 0:
                lists.append(html[match.start():pos + tag.end()])
                break
    return lists


def extract_static_items(list_html):
    """Extract all <a ... class="...search-static-item...">...</a> entries in a list."""
    return re.findall(
        r'<a\b[^>]*class="[^"]*\bsearch-static-item\b[^"]*"[^>]*>[\s\S]*?</a>',
        list_html,
    )


def get_item_srcs(item_html):
    """Return all src attribute values inside an item element."""
    return re.findall(r'\bsrc="([^"]+)"', item_html)


def get_item_href(item_html):
    """Return the href attribute value on the item's opening <a> tag, or None."""
    match = re.search(r'^<a\b[^>]*\bhref="([^"]+)"', item_html)
    return match.group(1) if match else None


print("=== VERIFY STING GOLD IN SEARCH DROPDOWNS ===")

# 1. Verify required Sting image assets exist
for rel_path in [
    os.path.join("assets", "images", "sting", "sting-gold.webp"),
    os.path.join("assets", "images", "sting", "sting-dau.webp"),
]:
    full_path = os.path.join(ROOT_DIR, rel_path)
    check(
        f"Asset exists: {rel_path.replace(os.sep, '/')}",
        os.path.isfile(full_path),
        f"Found {rel_path.replace(os.sep, '/')}",
    )

# 2. Verify all 5 .search-static-list dropdowns across index.html, pages/search-results.html, pages/account.html
target_files = [
    (
        "index.html",
        2,
        "pages/product-detail-sting.html",
        "assets/images/sting/sting-gold.webp",
        "assets/images/sting/sting-dau.webp",
    ),
    (
        "pages/search-results.html",
        2,
        "product-detail-sting.html",
        "../assets/images/sting/sting-gold.webp",
        "../assets/images/sting/sting-dau.webp",
    ),
    (
        "pages/account.html",
        1,
        "product-detail-sting.html",
        "../assets/images/sting/sting-gold.webp",
        "../assets/images/sting/sting-dau.webp",
    ),
]
total_target_dropdowns = 0

for rel_file, expected_count, expected_href, expected_gold_src, expected_dau_src in target_files:
    file_path = Path(ROOT_DIR) / rel_file
    exists = file_path.is_file()
    check(f"File exists: {rel_file}", exists, f"{rel_file} present")
    if not exists:
        continue

    content = file_path.read_text(encoding="utf-8")
    blocks = extract_search_static_lists(content)
    total_target_dropdowns += len(blocks)
    check(
        f"{rel_file} has {expected_count} .search-static-list block(s)",
        len(blocks) == expected_count,
        f"Found {len(blocks)} block(s)",
    )

    for idx, block in enumerate(blocks, 1):
        label = f"{rel_file} dropdown #{idx}"
        items = extract_static_items(block)
        check(
            f"{label} has exactly 5 search-static-item entries",
            len(items) == 5,
            f"Found {len(items)} item(s)",
        )

        exact_dau_items = [item for item in items if expected_dau_src in get_item_srcs(item)]
        any_dau_src_count = sum(
            1 for item in items for src in get_item_srcs(item) if src.endswith("sting-dau.webp")
        )
        check(
            f"{label} has {expected_dau_src} src count == 1",
            len(exact_dau_items) == 1 and any_dau_src_count == 1,
            f"exact src count = {len(exact_dau_items)}, any sting-dau.webp src count = {any_dau_src_count}",
        )

        exact_gold_items = [item for item in items if expected_gold_src in get_item_srcs(item)]
        any_gold_src_count = sum(
            1 for item in items for src in get_item_srcs(item) if src.endswith("sting-gold.webp")
        )
        check(
            f"{label} has {expected_gold_src} src count == 1",
            len(exact_gold_items) == 1 and any_gold_src_count == 1,
            f"exact src count = {len(exact_gold_items)}, any sting-gold.webp src count = {any_gold_src_count}",
        )

        paired_ok = (
            len(exact_gold_items) == 1
            and "Nước Tăng Lực Sting Vàng Sleek 330ml" in exact_gold_items[0]
            and "12.000đ" in exact_gold_items[0]
            and get_item_href(exact_gold_items[0]) == expected_href
        )
        check(
            f"{label} pairs {expected_gold_src} with Sting Vàng Sleek 330ml, 12.000đ, {expected_href}",
            paired_ok,
            f"Matched href='{get_item_href(exact_gold_items[0]) if exact_gold_items else None}' and Sting Gold metadata",
        )

check(
    "Total inspected target dropdowns == 5",
    total_target_dropdowns == 5,
    f"Inspected {total_target_dropdowns} dropdown(s)",
)

# 3. Scan all other pages/*.html files with .search-static-list for duplicate sting-dau.webp
checked_pages = {"pages/search-results.html", "pages/account.html"}
other_html_files = sorted(glob.glob(os.path.join(ROOT_DIR, "pages", "*.html")))
other_dropdown_count = 0

for abs_path in other_html_files:
    rel_file = os.path.relpath(abs_path, ROOT_DIR).replace(os.sep, "/")
    if rel_file in checked_pages:
        continue
    content = Path(abs_path).read_text(encoding="utf-8")
    blocks = extract_search_static_lists(content)
    for idx, block in enumerate(blocks, 1):
        other_dropdown_count += 1
        items = extract_static_items(block)
        dau_srcs = [src for item in items for src in get_item_srcs(item) if src.endswith("sting-dau.webp")]
        exact_prefix_ok = all(src == "../assets/images/sting/sting-dau.webp" for src in dau_srcs)
        check(
            f"{rel_file} dropdown #{idx} has no duplicate sting-dau.webp (src count < 2) and valid prefix",
            len(dau_srcs) < 2 and exact_prefix_ok,
            f"sting-dau.webp src count = {len(dau_srcs)}, srcs = {dau_srcs}",
        )

check(
    "Scanned other pages/*.html files with .search-static-list",
    other_dropdown_count > 0,
    f"Verified {other_dropdown_count} additional dropdown(s) across other pages/*.html",
)

failed = [c for c in checks if not c[1]]
print(f"\nResult: {len(checks) - len(failed)}/{len(checks)} passed.")
if failed:
    print(f"FAILED {len(failed)} checks.")
    sys.exit(1)

print("ALL STING GOLD SEARCH DROPDOWN CHECKS PASSED!")
sys.exit(0)
