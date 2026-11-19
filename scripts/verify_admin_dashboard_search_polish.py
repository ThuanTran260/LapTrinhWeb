import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    failures = []

    css_text = (ROOT / "css" / "style.css").read_text(encoding="utf-8")
    index_html = (ROOT / "admin" / "index.html").read_text(encoding="utf-8")

    search_block = re.search(r"\.admin-filter-search input\s*\{([^}]*)\}", css_text)
    if not search_block:
        failures.append("css/style.css: missing .admin-filter-search input rule")
    else:
        body = search_block.group(1)
        if "min-width: 0;" not in body:
            failures.append("css/style.css: .admin-filter-search input missing 'min-width: 0;'")
        if "text-overflow: ellipsis;" not in body:
            failures.append("css/style.css: .admin-filter-search input missing 'text-overflow: ellipsis;'")

    ph_block = re.search(r"\.admin-filter-search input::placeholder\s*\{([^}]*)\}", css_text)
    if not ph_block or "text-overflow: ellipsis;" not in ph_block.group(1):
        failures.append("css/style.css: .admin-filter-search input::placeholder missing 'text-overflow: ellipsis;'")

    compact_block = re.search(r"\.admin-filter-search--compact input\s*\{([^}]*)\}", css_text)
    if not compact_block or "width: 195px;" not in compact_block.group(1):
        failures.append("css/style.css: .admin-filter-search--compact input missing 'width: 195px;'")

    mobile_section = re.search(r"@media\s*\(max-width:\s*640px\)\s*\{([\s\S]*)$", css_text)
    if not mobile_section or not re.search(
        r"\.admin-filter-search--compact input\s*\{[^}]*width:\s*100%;",
        mobile_section.group(1),
    ):
        failures.append("css/style.css: @media (max-width: 640px) missing .admin-filter-search--compact input { width: 100%; }")

    if "Tìm mã đơn hoặc khách..." in index_html:
        failures.append("admin/index.html: still contains old placeholder 'Tìm mã đơn hoặc khách...'")
    if "width: 170px;" in index_html:
        failures.append("admin/index.html: still contains inline 'width: 170px;' on quick filter inputs")

    if index_html.count("admin-filter-search--compact") != 2:
        failures.append(
            f"admin/index.html: expected 2 'admin-filter-search--compact' wrappers, found {index_html.count('admin-filter-search--compact')}"
        )

    order_input = re.search(r'<input\b[^>]*id="dash-order-keyword"[^>]*>', index_html)
    if not order_input or 'placeholder="Tìm mã đơn, khách..."' not in order_input.group(0):
        failures.append("admin/index.html: #dash-order-keyword missing placeholder=\"Tìm mã đơn, khách...\"")

    inv_input = re.search(r'<input\b[^>]*id="dash-inv-keyword"[^>]*>', index_html)
    if not inv_input or 'placeholder="Tìm tên sản phẩm..."' not in inv_input.group(0):
        failures.append("admin/index.html: #dash-inv-keyword missing placeholder=\"Tìm tên sản phẩm...\"")

    if failures:
        print(f"FAIL ({len(failures)} checks failed):")
        for item in failures:
            print(f"  - {item}")
        return 1

    print("ALL 10 CHECKS PASSED: Admin dashboard compact search CSS + HTML verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
