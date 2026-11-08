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

print("=== VERIFY HEADER TOP SYNC & ACCOUNT BREADCRUMB ===")

# 1. Check pages/orders.html top-links
orders_content = open("pages/orders.html", encoding="utf-8").read()
top_links_match = re.search(r'<div class="top-links">(.*?)</div>', orders_content, re.DOTALL)
check("orders.html has top-links", top_links_match is not None, "Found .top-links container")

if top_links_match:
    links_block = top_links_match.group(1)
    check("orders.html has Tiếp Tục Mua Sắm", 'Tiếp Tục Mua Sắm' in links_block and '../index.html' in links_block)
    check("orders.html has Giao 2H Hoả Tốc", 'Giao 2H Hoả Tốc' in links_block and '../index.html#features' in links_block)
    check("orders.html has Lịch Sử Đặt Hàng", 'Lịch Sử Đặt Hàng' in links_block and 'orders.html' in links_block)
    check("orders.html has Giỏ Hàng (7 lon)", 'Giỏ Hàng (7 lon)' in links_block and 'cart.html' in links_block)
    check("orders.html has Tài Khoản", 'Tài Khoản' in links_block and 'account.html' in links_block)
    check("orders.html has Đăng Nhập", 'Đăng Nhập' in links_block and 'login.html' in links_block)

# 2. Check pages/account.html breadcrumb and removal of brand nav
account_content = open("pages/account.html", encoding="utf-8").read()
check("account.html removes nav-bar", '<nav class="nav-bar">' not in account_content and 'handleNavBrandClick' not in account_content)
check("account.html has breadcrumb", '<div class="breadcrumb">' in account_content)
check("account.html breadcrumb structure", 'Trang chủ' in account_content and 'Thành viên' in account_content)

failed = [c for c in checks if not c[1]]
print(f"\nResult: {len(checks) - len(failed)}/{len(checks)} passed.")
if failed:
    print(f"FAILED {len(failed)} checks.")
    sys.exit(1)
else:
    print("ALL CHECKS PASSED!")
    sys.exit(0)
