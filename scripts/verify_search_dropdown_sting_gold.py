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
    ("index.html", 2),
    ("pages/search-results.html", 2),
    ("pages/account.html", 1),
]
total_target_dropdowns = 0

for rel_file, expected_count in target_files:
    file_path = os.path.join(ROOT_DIR, rel_file)
    exists = os.path.isfile(file_path)
    check(f"File exists: {rel_file}", exists, f"{rel_file} present")
    if not exists:
        continue

    content = open(file_path, encoding="utf-8").read()
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

        dau_count = block.count("sting-dau.webp")
        check(
            f"{label} has sting-dau.webp count == 1",
            dau_count == 1,
            f"sting-dau.webp count = {dau_count}",
        )

        gold_count = block.count("sting-gold.webp")
        check(
            f"{label} has sting-gold.webp count == 1",
            gold_count == 1,
            f"sting-gold.webp count = {gold_count}",
        )

        gold_items = [item for item in items if "sting-gold.webp" in item]
        paired_ok = (
            len(gold_items) == 1
            and "Nước Tăng Lực Sting Vàng Sleek 330ml" in gold_items[0]
            and "12.000đ" in gold_items[0]
            and re.search(r'href="[^"]*product-detail-sting\.html"', gold_items[0]) is not None
        )
        check(
            f"{label} pairs sting-gold.webp with Sting Vàng Sleek 330ml, 12.000đ, product-detail-sting.html",
            paired_ok,
            "All Sting Gold attributes match inside the same item",
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
    content = open(abs_path, encoding="utf-8").read()
    blocks = extract_search_static_lists(content)
    for idx, block in enumerate(blocks, 1):
        other_dropdown_count += 1
        dau_count = block.count("sting-dau.webp")
        check(
            f"{rel_file} dropdown #{idx} has no duplicate sting-dau.webp (count < 2)",
            dau_count < 2,
            f"sting-dau.webp count = {dau_count}",
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
