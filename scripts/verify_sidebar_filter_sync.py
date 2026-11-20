import os
import sys
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT_DIR)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

checks = []

def check(name, condition, details=""):
    checks.append((name, condition, details))
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {name} - {details}")

print("=== VERIFY SIDEBAR FILTER SYNC BETWEEN DASHBOARD & SEARCH RESULTS ===")

search_html_path = os.path.join(ROOT_DIR, "pages", "search-results.html")
index_html_path = os.path.join(ROOT_DIR, "index.html")

check("search-results.html exists", os.path.exists(search_html_path), "File pages/search-results.html exists")
check("index.html exists", os.path.exists(index_html_path), "File index.html exists")

search_content = open(search_html_path, encoding="utf-8").read()
index_content = open(index_html_path, encoding="utf-8").read()

# 1. Brand option for Monster is strictly <span>Monster Energy</span> (no (Hà Lan)) in sidebar filter
monster_radio_match = re.search(r'input[^>]*name="search-brand"[^>]*value="monster"[^>]*>[\s\S]*?<span>(.*?)</span>', search_content)
check("Brand option monster found", monster_radio_match is not None, "Monster brand radio input found in search-results.html")
if monster_radio_match:
    brand_text = monster_radio_match.group(1).strip()
    check(
        "Monster brand text is 'Monster Energy'",
        brand_text == "Monster Energy",
        f"Brand option text is '{brand_text}' (strictly 'Monster Energy', no '(Hà Lan)')"
    )

# Also check index.html has identical <span>Monster Energy</span>
idx_monster_radio_match = re.search(r'input[^>]*name="sidebar-brand"[^>]*value="monster"[^>]*>[\s\S]*?<span>(.*?)</span>', index_content)
if idx_monster_radio_match:
    idx_brand_text = idx_monster_radio_match.group(1).strip()
    check(
        "Dashboard brand text matches",
        idx_brand_text == "Monster Energy",
        f"Dashboard brand option is '{idx_brand_text}'"
    )

# 2. Check that neither index.html nor search-results.html has any filter-option-count
idx_counts = re.findall(r'class="filter-option-count"', index_content)
search_counts = re.findall(r'class="filter-option-count"', search_content)
check("index.html has 0 filter-option-count", len(idx_counts) == 0, f"Found {len(idx_counts)} filter-option-count in index.html")
check("search-results.html has 0 filter-option-count", len(search_counts) == 0, f"Found {len(search_counts)} filter-option-count in search-results.html")

# Check all brand options sync with clean labels (no count)
expected_brands = [
    ("all", "Tất cả thương hiệu"),
    ("monster", "Monster Energy"),
    ("redbull", "Redbull Thái Lan"),
    ("sting", "Sting PepsiCo"),
]
for val, label in expected_brands:
    m_search = re.search(rf'name="search-brand"[^>]*value="{val}"[^>]*>[\s\S]*?<span>({re.escape(label)})</span>', search_content)
    check(f"Search brand option {val} matches label '{label}'", m_search is not None)
    m_idx = re.search(rf'name="sidebar-brand"[^>]*value="{val}"[^>]*>[\s\S]*?<span>({re.escape(label)})</span>', index_content)
    check(f"Dashboard brand option {val} matches label '{label}'", m_idx is not None)

# Check all price options sync with clean labels (no sublabel/badge)
expected_prices = [
    ("all", "Tất cả khoảng giá"),
    ("under20", "Dưới 20.000đ"),
    ("20to50", "20.000đ - 50.000đ"),
    ("over50", "Trên 50.000đ"),
]
for val, label in expected_prices:
    m_search = re.search(rf'name="search-price"[^>]*value="{val}"[^>]*>[\s\S]*?<span>({re.escape(label)})</span>', search_content)
    check(f"Search price option {val} matches label '{label}'", m_search is not None)
    m_idx = re.search(rf'name="sidebar-price"[^>]*value="{val}"[^>]*>[\s\S]*?<span>({re.escape(label)})</span>', index_content)
    check(f"Dashboard price option {val} matches label '{label}'", m_idx is not None)

# 3. Sidebar dropdown preserves Sting Dâu Tây Đỏ 330ml (no combo) and Item 5 is Sting Vàng Sleek 330ml
for page_label, page_html in [("search-results", search_content), ("index.html", index_content)]:
    dropdown_match = re.search(
        r'id="sidebar-search-dropdown-menu"[\s\S]*?</div>\s*</div>\s*</div>',
        page_html,
    )
    check(
        f"Sidebar search dropdown exists ({page_label})",
        dropdown_match is not None,
        f"#sidebar-search-dropdown-menu found in {page_label}",
    )
    if dropdown_match:
        dropdown_html = dropdown_match.group(0)
        has_sting_red = "Sting Dâu Tây Đỏ 330ml" in dropdown_html
        has_combo_item = "Combo Thùng" in dropdown_html or "combo-section" in dropdown_html
        check(
            f"Sidebar dropdown preserves Sting Dâu Tây Đỏ 330ml ({page_label})",
            has_sting_red,
            f"Sidebar dropdown in {page_label} contains Sting Dâu Tây Đỏ 330ml",
        )
        check(
            f"Sidebar dropdown has no combo ({page_label})",
            not has_combo_item,
            f"Sidebar dropdown in {page_label} has no combo residual",
        )
        items = re.findall(r'<a\b[^>]*class="search-static-item"[^>]*>[\s\S]*?</a>', dropdown_html)
        item5 = items[4] if len(items) >= 5 else ""
        has_sting_gold_item5 = (
            len(items) == 5
            and "Nước Tăng Lực Sting Vàng Sleek 330ml" in item5
            and "sting-gold.webp" in item5
        )
        check(
            f"Item 5 is Nước Tăng Lực Sting Vàng Sleek 330ml ({page_label})",
            has_sting_gold_item5,
            f"Item 5 in {page_label} sidebar dropdown uses sting-gold.webp and Sting Vàng Sleek 330ml",
        )
        check(
            f"Item 5 calls closeSidebarSearchDropdown in {page_label}",
            'onclick="closeSidebarSearchDropdown()"' in item5,
            f"Dropdown item 5 in {page_label} closes sidebar dropdown correctly",
        )

# 4. Sidebar contains navigation button back to ../index.html
has_home_btn = (
    "window.location.href='../index.html'" in search_content and
    "Về danh mục trang chủ" in search_content
)
check("Sidebar navigation button back to index.html", has_home_btn, "Button with onclick window.location.href='../index.html' and 'Về danh mục trang chủ' exists")

# 5. Redundant 'Thương hiệu nổi bật' block removed from sidebar card
sidebar_card_match = re.search(r'<div class="sidebar-filter-card">([\s\S]*?)</div>\s*</aside>', search_content)
check("Sidebar filter card located", sidebar_card_match is not None, ".sidebar-filter-card found")
if sidebar_card_match:
    card_html = sidebar_card_match.group(1)
    has_redundant_block = "Thương hiệu nổi bật" in card_html
    check(
        "Redundant 'Thương hiệu nổi bật' removed",
        not has_redundant_block,
        "Redundant 'Thương hiệu nổi bật' block successfully removed from sidebar filter card"
    )

failed = [c for c in checks if not c[1]]
print(f"\nResult: {len(checks) - len(failed)}/{len(checks)} passed.")
if failed:
    print(f"FAILED {len(failed)} checks.")
    sys.exit(1)
else:
    print("ALL SIDEBAR FILTER SYNC CHECKS PASSED PERFECTLY!")
    sys.exit(0)
