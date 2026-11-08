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

print("=== VERIFY ORDERS TOPBAR SINGLE LINE & ACCOUNT BREADCRUMB ===")

# 1. Check pages/orders.html top-links
orders_content = open("pages/orders.html", encoding="utf-8").read()
top_links_match = re.search(r'<div class="top-links">(.*?)</div>', orders_content, re.DOTALL)
check("orders.html has top-links", top_links_match is not None, "Found .top-links container")

if top_links_match:
    links_block = top_links_match.group(1)
    check("orders.html has Tiếp Tục Mua Sắm", 'Tiếp Tục Mua Sắm' in links_block and '../index.html' in links_block)
    check("orders.html has Giao 2H Hoả Tốc", 'Giao 2H Hoả Tốc' in links_block and '../index.html#features' in links_block)
    check("orders.html has Lịch Sử Đặt Hàng", 'Lịch Sử Đặt Hàng' in links_block and 'orders.html' in links_block)
    check("orders.html has Tài Khoản", 'Tài Khoản' in links_block and 'account.html' in links_block)
    check("orders.html has Đăng Nhập", 'Đăng Nhập' in links_block and 'login.html' in links_block)
    check("orders.html top-links has no redundant cart link", 'cart.html' not in links_block, "Cart link removed from top-links to fit 1 line")

# 2. Check orders.html retains 'Giỏ Hàng (7 lon)' for verify_cart_sync compatibility
check("orders.html retains Giỏ Hàng (7 lon)", 'Giỏ Hàng (7 lon)' in orders_content, "Retains 'Giỏ Hàng (7 lon)' in header action button")

# 3. Check pages/account.html breadcrumb and removal of brand nav
account_content = open("pages/account.html", encoding="utf-8").read()
check("account.html removes nav-bar", '<nav class="nav-bar">' not in account_content and 'handleNavBrandClick' not in account_content)
check("account.html has breadcrumb", '<div class="breadcrumb">' in account_content)
check("account.html breadcrumb structure", 'Trang chủ' in account_content and 'Thành viên' in account_content)

# 4. Check css/style.css top-bar single line styling on desktop
css_content = open("css/style.css", encoding="utf-8").read()
desktop_topbar = False
for m in re.finditer(r"@media\s*\(\s*min-width:\s*992px\s*\)\s*\{", css_content):
    snippet = css_content[m.end():m.end()+2000]
    m_container = re.search(r"\.top-bar\s+\.container\s*\{([^}]*)\}", snippet)
    has_container_nowrap = m_container is not None and re.search(r"flex-wrap\s*:\s*nowrap", m_container.group(1)) is not None
    m_links = re.search(r"\.top-links\s*\{([^}]*)\}", snippet)
    has_links_nowrap = m_links is not None and "white-space" in m_links.group(1) and "nowrap" in m_links.group(1) and re.search(r"gap\s*:\s*14px", m_links.group(1)) is not None
    if has_container_nowrap and has_links_nowrap:
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
