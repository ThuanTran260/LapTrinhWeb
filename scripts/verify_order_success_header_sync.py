import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent


def extract_div_block(html: str, class_or_id_pattern: str) -> str:
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


def verify_order_success_header_sync(html: str) -> list[str]:
    failures: list[str] = []

    # 1. Top bar with ENERGY10 coupon badge
    top_bar = extract_div_block(html, r'class="[^"]*\btop-bar\b[^"]*"')
    if not top_bar:
        failures.append("pages/order-success.html: missing .top-bar block")
    else:
        if "ENERGY10" not in top_bar:
            failures.append("pages/order-success.html: .top-bar missing ENERGY10 coupon badge")
        if 'class="coupon-badge"' not in top_bar:
            failures.append("pages/order-success.html: .top-bar missing .coupon-badge element")
        for expected_link in ("orders.html", "account.html", "login.html"):
            if f'href="{expected_link}"' not in top_bar:
                failures.append(f"pages/order-success.html: .top-bar missing link '{expected_link}'")

    # 2. Header search box & static dropdown with 5 items
    header_match = re.search(r'<header\b[^>]*class="[^"]*\bheader\b[^"]*"[^>]*>([\s\S]*?)</header>', html)
    if not header_match:
        failures.append("pages/order-success.html: missing <header class='header'>")
    else:
        header_html = header_match.group(0)

        search_box = extract_div_block(header_html, r'class="[^"]*\bsearch-box\b[^"]*"')
        if not search_box:
            failures.append("pages/order-success.html: missing .search-box inside header")
        else:
            if "openSearchDropdown()" not in search_box:
                failures.append("pages/order-success.html: .search-box missing openSearchDropdown() trigger")
            if "openAdvancedSearchModal()" not in search_box:
                failures.append("pages/order-success.html: .search-box missing openAdvancedSearchModal() trigger")

            dropdown = extract_div_block(search_box, r'id="search-dropdown-menu"')
            if not dropdown:
                failures.append("pages/order-success.html: missing #search-dropdown-menu")
            else:
                static_list = extract_div_block(dropdown, r'class="[^"]*\bsearch-static-list\b[^"]*"')
                if not static_list:
                    failures.append("pages/order-success.html: missing .search-static-list in #search-dropdown-menu")
                else:
                    items = re.findall(
                        r'<a\b[^>]*class="[^"]*\bsearch-static-item\b[^"]*"[^>]*>[\s\S]*?</a>',
                        static_list,
                    )
                    if len(items) != 5:
                        failures.append(
                            f"pages/order-success.html: expected 5 .search-static-item links, found {len(items)}"
                        )
                    else:
                        for idx, item in enumerate(items, start=1):
                            srcs = re.findall(r'\bsrc="([^"]+)"', item)
                            if not srcs or any(not src.startswith("../assets/images/") for src in srcs):
                                failures.append(
                                    f"pages/order-success.html: search item #{idx} image src must use '../assets/images/...', got {srcs}"
                                )

                        item4 = items[3]
                        if "Monster Energy Ultra White 355ml" not in item4:
                            failures.append(
                                "pages/order-success.html: search item #4 missing 'Monster Energy Ultra White 355ml'"
                            )

                        item5 = items[4]
                        if "Sting Vàng Sleek 330ml" not in item5:
                            failures.append(
                                "pages/order-success.html: search item #5 missing 'Sting Vàng Sleek 330ml'"
                            )
                        if "../assets/images/sting/sting-gold.webp" not in item5:
                            failures.append(
                                "pages/order-success.html: search item #5 missing '../assets/images/sting/sting-gold.webp'"
                            )
                        if 'href="product-detail-sting.html"' not in item5:
                            failures.append(
                                "pages/order-success.html: search item #5 must link to 'product-detail-sting.html'"
                            )

        # 3. Header actions (orders.html, account.html #header-account-link, cart.html badge 7)
        header_actions = extract_div_block(header_html, r'class="[^"]*\bheader-actions\b[^"]*"')
        if not header_actions:
            failures.append("pages/order-success.html: missing .header-actions inside header")
        else:
            action_links = re.findall(r'<a\b[^>]*class="[^"]*\baction-btn\b[^"]*"[^>]*>[\s\S]*?</a>', header_actions)
            if len(action_links) != 3:
                failures.append(
                    f"pages/order-success.html: expected 3 .action-btn links in .header-actions, found {len(action_links)}"
                )
            if 'href="orders.html"' not in header_actions:
                failures.append("pages/order-success.html: .header-actions missing orders.html link")
            if not re.search(r'<a\b[^>]*href="account\.html"[^>]*id="header-account-link"|<a\b[^>]*id="header-account-link"[^>]*href="account\.html"', header_actions):
                failures.append("pages/order-success.html: .header-actions missing #header-account-link to account.html")
            if 'href="cart.html"' not in header_actions:
                failures.append("pages/order-success.html: .header-actions missing cart.html link")
            if not re.search(r'<span[^>]*class="[^"]*\baction-badge\b[^"]*"[^>]*>\s*7\s*</span>', header_actions):
                failures.append("pages/order-success.html: .header-actions cart link missing .action-badge with '7'")

    # 4. Advanced Search Modal (#modal-adv-search)
    adv_modal = extract_div_block(html, r'id="modal-adv-search"')
    if not adv_modal:
        failures.append("pages/order-success.html: missing #modal-adv-search modal")
    else:
        if "closeAdvancedSearchModal()" not in adv_modal:
            failures.append("pages/order-success.html: #modal-adv-search missing closeAdvancedSearchModal()")
        if "handleAdvancedSearch(event)" not in adv_modal:
            failures.append("pages/order-success.html: #modal-adv-search missing handleAdvancedSearch(event)")

    # 5. Preserved <main> (7 LON order summary, timeline step, toast print button) & <footer>
    main_match = re.search(r'<main\b[^>]*>([\s\S]*?)</main>', html)
    if not main_match:
        failures.append("pages/order-success.html: missing <main> content")
    else:
        main_html = main_match.group(1)
        if "Đóng thùng chống sốc 7 lon" not in main_html:
            failures.append("pages/order-success.html: <main> missing preserved 'Đóng thùng chống sốc 7 lon'")
        if "CHI TIẾT ĐƠN HÀNG (7 LON)" not in main_html:
            failures.append("pages/order-success.html: <main> missing preserved 'CHI TIẾT ĐƠN HÀNG (7 LON)'")
        if not re.search(
            r'<button\b[^>]*onclick="showToast\([^)]*\)"[^>]*>[\s\S]*?IN HÓA ĐƠN ĐIỆN TỬ[\s\S]*?</button>',
            main_html,
        ):
            failures.append("pages/order-success.html: <main> missing preserved 'IN HÓA ĐƠN ĐIỆN TỬ' toast button")

    if '<footer class="footer">' not in html:
        failures.append("pages/order-success.html: missing preserved <footer class='footer'>")
    if "initOrderSuccess()" not in html:
        failures.append("pages/order-success.html: missing initOrderSuccess() initialization call")

    return failures


def main() -> int:
    target = ROOT / "pages" / "order-success.html"
    if not target.is_file():
        print(f"FAIL: missing file {target}")
        return 1

    html = target.read_text(encoding="utf-8")
    failures = verify_order_success_header_sync(html)

    if failures:
        print(f"FAIL ({len(failures)} checks failed):")
        for item in failures:
            print(f"  - {item}")
        return 1

    print(
        "ALL CHECKS PASSED: pages/order-success.html top-bar, search dropdown (5 items), header actions, #modal-adv-search, and preserved 7 LON order summary verified."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
