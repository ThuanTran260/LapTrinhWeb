import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
EXPECTED_PLACEHOLDER = "Tìm kiếm Monster, Redbull, Sting..."

STOREFRONT_FILES = [
    "index.html",
    "pages/account.html",
    "pages/cart.html",
    "pages/order-detail.html",
    "pages/orders.html",
    "pages/search-results.html",
    "pages/product-detail.html",
    "pages/product-detail-redbull.html",
    "pages/product-detail-sting.html",
    "pages/product-detail-redbull-lonvua.html",
    "pages/product-detail-redbull-thai.html",
]

DISALLOWED_PLACEHOLDERS = [
    "Tìm kiếm Monster Energy, Redbull, Sting...",
    "Tìm kiếm vị yêu thích",
    "Tìm kiếm Monster, Redbull...",
    "Tìm kiếm Redbull, Monster, Sting...",
    "Tìm kiếm Sting, Monster, Redbull...",
]


def extract_css_block(css_text: str, selector: str) -> str:
    pattern = re.compile(rf"{re.escape(selector)}\s*\{{([^}}]*)\}}", re.MULTILINE)
    match = pattern.search(css_text)
    return match.group(1) if match else ""


def main() -> int:
    failures = []

    css_path = ROOT / "css" / "style.css"
    css_text = css_path.read_text(encoding="utf-8")

    search_input_block = extract_css_block(css_text, ".search-input")
    placeholder_block = extract_css_block(css_text, ".search-input::placeholder")

    if "min-width: 0;" not in search_input_block:
        failures.append("css/style.css: .search-input missing 'min-width: 0;'")
    if "text-overflow: ellipsis;" not in search_input_block:
        failures.append("css/style.css: .search-input missing 'text-overflow: ellipsis;'")
    if "text-overflow: ellipsis;" not in placeholder_block:
        failures.append("css/style.css: .search-input::placeholder missing 'text-overflow: ellipsis;'")

    input_tag_re = re.compile(r'<input\b[^>]*class="[^"]*\bsearch-input\b[^"]*"[^>]*>', re.IGNORECASE)
    placeholder_re = re.compile(r'placeholder="([^"]*)"')

    for rel_path in STOREFRONT_FILES:
        file_path = ROOT / rel_path
        if not file_path.exists():
            failures.append(f"{rel_path}: file missing")
            continue

        content = file_path.read_text(encoding="utf-8")
        tag_match = input_tag_re.search(content)
        if not tag_match:
            failures.append(f"{rel_path}: missing <input class=\"search-input\">")
            continue

        tag = tag_match.group(0)
        ph_match = placeholder_re.search(tag)
        actual = ph_match.group(1) if ph_match else None
        if actual != EXPECTED_PLACEHOLDER:
            failures.append(
                f"{rel_path}: expected placeholder '{EXPECTED_PLACEHOLDER}', got '{actual}'"
            )

        for old_text in DISALLOWED_PLACEHOLDERS:
            if old_text in tag:
                failures.append(f"{rel_path}: disallowed old placeholder fragment '{old_text}'")

    if failures:
        print(f"FAIL ({len(failures)} checks failed):")
        for item in failures:
            print(f"  - {item}")
        return 1

    print(f"ALL {3 + len(STOREFRONT_FILES)} CHECKS PASSED: CSS safeguard + 11 storefront placeholders verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
