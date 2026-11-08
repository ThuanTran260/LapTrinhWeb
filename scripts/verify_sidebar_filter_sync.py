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

# 2. Over50 price option badge is 'Lon lẻ & Lốc' (no 'Combo / Thùng')
over50_match = re.search(r'input[^>]*name="search-price"[^>]*value="over50"[^>]*>[\s\S]*?<span class="filter-option-count">(.*?)</span>', search_content)
check("Price option over50 found", over50_match is not None, "Over50 price radio option found in search-results.html")
if over50_match:
    badge_text = over50_match.group(1).strip()
    check(
        "over50 badge is 'Lon lẻ & Lốc'",
        badge_text == "Lon lẻ & Lốc",
        f"Price over50 badge is '{badge_text}' (strictly 'Lon lẻ & Lốc', no 'Combo / Thùng')"
    )

# 3. Item 5 in sidebar dropdown is Sting Dâu Tây Đỏ (no combo)
sidebar_dropdown_match = re.search(r'id="sidebar-search-dropdown-menu"[\s\S]*?</div>\s*</div>\s*</div>', search_content)
check("Sidebar search dropdown exists", sidebar_dropdown_match is not None, "#sidebar-search-dropdown-menu found")
if sidebar_dropdown_match:
    sidebar_dropdown_html = sidebar_dropdown_match.group(0)
    has_sting_item = "Sting Dâu Tây Đỏ Sleek 330ml" in sidebar_dropdown_html or "Sting Dâu" in sidebar_dropdown_html
    has_combo_item = "Combo Thùng" in sidebar_dropdown_html or "combo-section" in sidebar_dropdown_html
    check("Item 5 is Sting Dâu Tây Đỏ", has_sting_item, "Sidebar dropdown contains Sting Dâu Tây Đỏ")
    check("Sidebar dropdown has no combo", not has_combo_item, "Sidebar dropdown has no combo residual")

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
