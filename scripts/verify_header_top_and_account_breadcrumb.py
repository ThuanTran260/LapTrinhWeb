import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

checks = []

def check(name, condition, details=""):
    checks.append((name, condition, details))
    mark = "PASS" if condition else "FAIL"
    print(f"[{mark}] {name} - {details}")

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

print("=== VERIFY ORDERS TOPBAR SINGLE LINE & ACCOUNT BREADCRUMB ===")

# 1. Check pages/orders.html .top-bar has .announcement-text and NO .top-links
orders_content = open("pages/orders.html", encoding="utf-8").read()
top_bar_block = extract_div_block(orders_content, r'class="[^"]*\btop-bar\b[^"]*"')
check("orders.html has .top-bar", bool(top_bar_block), "Found .top-bar container")
check(
    "orders.html .top-bar has .announcement-text",
    bool(re.search(r'class="[^"]*\bannouncement-text\b[^"]*"', top_bar_block)),
    "Found .announcement-text inside .top-bar",
)
check(
    "orders.html has no .top-links",
    re.search(r'class="[^"]*\btop-links\b[^"]*"', orders_content) is None,
    "Confirmed .top-links is absent",
)
check(
    "orders.html .top-bar has no Tiếp Tục Mua Sắm",
    "Tiếp Tục Mua Sắm" not in top_bar_block,
    "Removed 'Tiếp Tục Mua Sắm' from .top-bar",
)
check(
    "orders.html .top-bar has no Giao 2H Hoả Tốc",
    "Giao 2H Hoả Tốc" not in top_bar_block,
    "Removed 'Giao 2H Hoả Tốc' from .top-bar",
)

# 2. Check orders.html retains 'Giỏ Hàng (7 lon)' for verify_cart_sync compatibility
check("orders.html retains Giỏ Hàng (7 lon)", 'Giỏ Hàng (7 lon)' in orders_content, "Retains 'Giỏ Hàng (7 lon)' in header action button")

# 3. Check pages/account.html breadcrumb and nav-bar with Trang chu + Nhan hang drawer
account_content = open("pages/account.html", encoding="utf-8").read()
check("account.html has nav-bar with Trang chủ & Nhãn hàng", '<nav class="nav-bar">' in account_content and 'id="nav-home-btn"' in account_content and 'id="nav-brand-drawer"' in account_content and 'handleNavBrandClick' in account_content)
check("account.html has breadcrumb", '<div class="breadcrumb">' in account_content)
check("account.html breadcrumb structure", 'Trang chủ' in account_content and 'Thành viên' in account_content)

# 4. Check css/style.css top-bar single line styling on desktop
css_content = open("css/style.css", encoding="utf-8").read()
desktop_topbar = False
for m in re.finditer(r"@media\s*\(\s*min-width:\s*992px\s*\)\s*\{", css_content):
    snippet = css_content[m.end():m.end()+2000]
    m_container = re.search(r"\.top-bar\s+\.container\s*\{([^}]*)\}", snippet)
    has_container_nowrap = m_container is not None and re.search(r"flex-wrap\s*:\s*nowrap", m_container.group(1)) is not None
    if has_container_nowrap:
        desktop_topbar = True
        break
check("style.css has top-bar nowrap on desktop", desktop_topbar)

failed = [c for c in checks if not c[1]]
print(f"\nResult: {len(checks) - len(failed)}/{len(checks)} passed.")
if failed:
    print(f"FAILED {len(failed)} checks.")
    sys.exit(1)
else:
    print("ALL CHECKS PASSED!")
    sys.exit(0)
