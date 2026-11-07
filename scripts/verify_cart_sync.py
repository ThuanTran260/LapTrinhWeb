import os
import re
import sys

# Ensure execution from project root directory regardless of invocation path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT_DIR)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

checks = []

def check(name, condition, details=""):
    checks.append((name, condition, details))
    mark = "PASS" if condition else "FAIL"
    print(f"[{mark}] {name} - {details}")

print("=== VERIFY CART DATA SYNCHRONIZATION (7 LON & 216.000đ) ===")

# 1. Check pages/cart.html
cart_content = open("pages/cart.html", encoding="utf-8").read()
check("cart.html header quantity", "GIỎ HÀNG CỦA BẠN (7 LON" in cart_content, "Header should say 7 LON")
check("cart.html header price", "216.000đ)" in cart_content and "210.600đ" not in cart_content, "Header should say 216.000đ, not 210.600đ")
check("cart.html summary quantity", "Tạm tính (7 lon):" in cart_content, "Summary should say 7 lon")
check("cart.html summary total", "216.000đ" in cart_content, "Total should be 216.000đ")

# 2. Check index.html
index_content = open("index.html", encoding="utf-8").read()
check("index.html header badge", '<span class="action-badge">7</span>' in index_content, "Cart badge in header should be 7")
check("index.html header price", "216.000đ" in index_content, "Cart price in header should be 216.000đ")
check("index.html view cart button", "Xem Giỏ Hàng (7 lon)" in index_content, "View cart button should say 7 lon")

# 3. Check product-detail pages
detail_pages = [
    "pages/product-detail.html",
    "pages/product-detail-redbull.html",
    "pages/product-detail-redbull-lonvua.html",
    "pages/product-detail-redbull-thai.html",
    "pages/product-detail-sting.html"
]
for p in detail_pages:
    content = open(p, encoding="utf-8").read()
    has_badge_7 = ('<span class="action-badge">7</span>' in content or '<span class="badge" id="cart-count">7</span>' in content)
    check(f"{os.path.basename(p)} badge", has_badge_7, "Cart badge should be 7")

# 4. Check pages/orders.html
orders_content = open("pages/orders.html", encoding="utf-8").read()
check("orders.html cart link", "Giỏ Hàng (7 lon)" in orders_content, "Orders page cart link should say 7 lon")

# 5. Check pages/order-success.html
success_content = open("pages/order-success.html", encoding="utf-8").read()
check("order-success.html package step", "Đóng thùng chống sốc 7 lon" in success_content, "Packaging step should say 7 lon")
check("order-success.html card title", "CHI TIẾT ĐƠN HÀNG (7 LON)" in success_content, "Order summary should say 7 LON")

failed = [c for c in checks if not c[1]]
print(f"\nResult: {len(checks) - len(failed)}/{len(checks)} passed.")
if failed:
    print(f"FAILED {len(failed)} checks.")
    sys.exit(1)
else:
    print("ALL CHECKS PASSED!")
    sys.exit(0)
