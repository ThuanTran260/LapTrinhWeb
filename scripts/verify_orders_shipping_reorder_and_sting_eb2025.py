#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification script for:
1. Adding "Mua Lại" button to shipping order #EB-2026 in pages/orders.html.
2. Converting order #EB-2025 from Monster Combo to Sting 24-can case across
   pages/orders.html, pages/account.html, and js/app.js.
"""

import sys
import re
from pathlib import Path

def test_orders_shipping_reorder_and_sting_eb2025():
    root = Path(__file__).resolve().parent.parent
    orders_path = root / "pages" / "orders.html"
    account_path = root / "pages" / "account.html"
    app_js_path = root / "js" / "app.js"

    assert orders_path.exists(), f"File not found: {orders_path}"
    assert account_path.exists(), f"File not found: {account_path}"
    assert app_js_path.exists(), f"File not found: {app_js_path}"

    orders_html = orders_path.read_text(encoding="utf-8")
    account_html = account_path.read_text(encoding="utf-8")
    app_js = app_js_path.read_text(encoding="utf-8")

    failures = []
    passes = []

    def check(condition, desc):
        if condition:
            passes.append(desc)
        else:
            failures.append(desc)

    # -------------------------------------------------------------
    # 0. Check physical asset existence
    # -------------------------------------------------------------
    print("--- 0. Checking physical asset existence ---")
    sting_img_path = root / "assets" / "images" / "sting" / "sting-dau.webp"
    check(sting_img_path.exists(), f"Asset exists on disk: {sting_img_path.relative_to(root)}")

    # -------------------------------------------------------------
    # 1. Check pages/orders.html
    # -------------------------------------------------------------
    print("--- 1. Checking pages/orders.html ---")

    # Order #EB-2026 action buttons
    # Need: Chi Tiết, Mua Lại (fas fa-cart-plus), and Định Vị (fas fa-location-dot)
    eb2026_match = re.search(r'#EB-2026[\s\S]*?</tr>', orders_html)
    if not eb2026_match:
        failures.append("orders.html: Order #EB-2026 row not found")
    else:
        eb2026_row = eb2026_match.group(0)
        check("order-detail.html?id=EB-2026" in eb2026_row, "orders.html: #EB-2026 has 'Chi Tiết' link")
        check("fas fa-file-invoice" in eb2026_row, "orders.html: #EB-2026 'Chi Tiết' has fas fa-file-invoice icon")
        check("fas fa-cart-plus" in eb2026_row and "Mua Lại" in eb2026_row, "orders.html: #EB-2026 has 'Mua Lại' button with fas fa-cart-plus")
        check("showToast('Đã thêm lại Monster &amp; Redbull vào giỏ hàng!', 'success')" in eb2026_row or
              "showToast('Đã thêm lại Monster & Redbull vào giỏ hàng!', 'success')" in eb2026_row,
              "orders.html: #EB-2026 'Mua Lại' calls showToast for Monster & Redbull")
        check("fas fa-location-dot" in eb2026_row and "Định Vị" in eb2026_row, "orders.html: #EB-2026 has 'Định Vị' button with fas fa-location-dot")
        
        # Verify button ordering: 'Chi Tiết' -> 'Mua Lại' -> 'Định Vị'
        pos_detail = eb2026_row.find("order-detail.html?id=EB-2026")
        pos_reorder = eb2026_row.find("Mua Lại")
        pos_track = eb2026_row.find("Định Vị")
        check(0 <= pos_detail < pos_reorder < pos_track, "orders.html: #EB-2026 button order is 'Chi Tiết' -> 'Mua Lại' -> 'Định Vị'")

    # Order #EB-2025 in orders.html
    eb2025_match = re.search(r'#EB-2025[\s\S]*?</tr>', orders_html)
    if not eb2025_match:
        failures.append("orders.html: Order #EB-2025 row not found")
    else:
        eb2025_row = eb2025_match.group(0)
        check("../assets/images/sting/sting-dau.webp" in eb2025_row, "orders.html: #EB-2025 uses sting-dau.webp")
        check("24 Lon Sting Dâu Tây Đỏ 330ml" in eb2025_row, "orders.html: #EB-2025 title is '24 Lon Sting Dâu Tây Đỏ 330ml'")
        check("Thương hiệu: Sting PepsiCo" in eb2025_row, "orders.html: #EB-2025 subtitle is 'Thương hiệu: Sting PepsiCo'")
        check("268.000đ" in eb2025_row, "orders.html: #EB-2025 price is '268.000đ'")
        check("fas fa-cart-plus" in eb2025_row and "Mua Lại" in eb2025_row, "orders.html: #EB-2025 has 'Mua Lại' button with fas fa-cart-plus")
        check("showToast('Đã thêm lại 24 lon Sting Dâu vào giỏ hàng!', 'success')" in eb2025_row,
              "orders.html: #EB-2025 reorder toast is 'Đã thêm lại 24 lon Sting Dâu vào giỏ hàng!'")
        check("Thùng" not in eb2025_row and "1x Thùng" not in eb2025_row, "orders.html: #EB-2025 block does not contain 'Thùng' or '1x Thùng'")
        check("Combo Thùng 24 Lon Đấu Trường" not in eb2025_row, "orders.html: #EB-2025 no longer contains old Monster combo name")
        check("Bình Giữ Nhiệt Monster" not in eb2025_row, "orders.html: #EB-2025 no longer contains gift thermos mention")
        check("918.000đ" not in eb2025_row, "orders.html: #EB-2025 no longer contains old 918.000đ price")

    # -------------------------------------------------------------
    # 2. Check pages/account.html
    # -------------------------------------------------------------
    print("--- 2. Checking pages/account.html ---")
    eb2025_acc_match = re.search(r'Mã đơn: #EB-2025[\s\S]*?(?=<!-- Navigation Actions -->|<div class="login-actions")', account_html)
    if not eb2025_acc_match:
        failures.append("account.html: Order card #EB-2025 not found")
    else:
        eb2025_card = eb2025_acc_match.group(0)
        check("../assets/images/sting/sting-dau.webp" in eb2025_card, "account.html: #EB-2025 uses sting-dau.webp")
        check("24 Lon Sting Dâu Tây Đỏ Sleek 330ml" in eb2025_card, "account.html: #EB-2025 title is '24 Lon Sting Dâu Tây Đỏ Sleek 330ml'")
        check("Thương hiệu: Sting PepsiCo" in eb2025_card, "account.html: #EB-2025 subtitle is 'Thương hiệu: Sting PepsiCo'")
        check("268.000đ" in eb2025_card, "account.html: #EB-2025 total price is '268.000đ'")
        check("order-detail.html?id=EB-2025" in eb2025_card, "account.html: #EB-2025 has 'Chi Tiết' link to order-detail.html?id=EB-2025")
        check("showToast('Đã thêm lại 24 lon Sting Dâu vào giỏ!', 'success')" in eb2025_card,
              "account.html: #EB-2025 reorder toast is 'Đã thêm lại 24 lon Sting Dâu vào giỏ!'")
        check("Thùng" not in eb2025_card and "1x Thùng" not in eb2025_card, "account.html: #EB-2025 block does not contain 'Thùng' or '1x Thùng'")
        check("Combo Thùng 24 Lon Đấu Trường" not in eb2025_card, "account.html: #EB-2025 no longer contains old combo name")
        check("Bình Giữ Nhiệt Monster" not in eb2025_card, "account.html: #EB-2025 no longer contains thermos mention")
        check("918.000đ" not in eb2025_card, "account.html: #EB-2025 no longer contains old 918.000đ price")

    # -------------------------------------------------------------
    # 3. Check js/app.js
    # -------------------------------------------------------------
    print("--- 3. Checking js/app.js ---")
    eb2025_db_match = re.search(r"['\"]EB-2025['\"]\s*:\s*\{([\s\S]*?)\n\s*\},?\s*\n\s*['\"]EB-2024['\"]", app_js)
    if not eb2025_db_match:
        failures.append("js/app.js: MOCK_ORDER_DATABASE['EB-2025'] block not found")
    else:
        eb2025_db = eb2025_db_match.group(1)
        check("../assets/images/sting/sting-dau.webp" in eb2025_db, "js/app.js: EB-2025 uses sting-dau.webp image")
        check("24 Lon Sting Dâu Tây Đỏ Sleek 330ml" in eb2025_db, "js/app.js: EB-2025 item name is '24 Lon Sting Dâu Tây Đỏ Sleek 330ml'")
        check("Thương hiệu: Sting PepsiCo" in eb2025_db, "js/app.js: EB-2025 item desc is 'Thương hiệu: Sting PepsiCo'")
        check("'268.000đ'" in eb2025_db or '"268.000đ"' in eb2025_db, "js/app.js: EB-2025 prices are 268.000đ")
        check("totalAmount: '268.000đ'" in eb2025_db or 'totalAmount: "268.000đ"' in eb2025_db, "js/app.js: EB-2025 totalAmount is '268.000đ'")
        check("subtotal: '268.000đ'" in eb2025_db or 'subtotal: "268.000đ"' in eb2025_db, "js/app.js: EB-2025 subtotal is '268.000đ'")
        check("24 lon Sting Dâu Tây Đỏ" in eb2025_db, "js/app.js: EB-2025 notes specify 24 lon Sting Dâu Tây Đỏ")
        check("Thùng" not in eb2025_db and "1x Thùng" not in eb2025_db, "js/app.js: EB-2025 block does not contain 'Thùng' or '1x Thùng'")
        check("Bộ 7 Lon Nước Tăng Lực VIP" not in eb2025_db, "js/app.js: EB-2025 no longer contains old 7 Lon VIP item")
        check("918.000đ" not in eb2025_db, "js/app.js: EB-2025 no longer contains 918.000đ")
        check("Bình Giữ Nhiệt Monster" not in eb2025_db, "js/app.js: EB-2025 no longer contains gift thermos")

    for p in passes:
        print(f"✅ PASS: [{p}]")

    if failures:
        print("\n❌ FAILURES:")
        for f in failures:
            print(f"❌ FAIL: [{f}]")
        print(f"\nResult: {len(passes)} passed, {len(failures)} failed.")
        return False

    print(f"\n============================================================================")
    print(f"Result: {len(passes)}/{len(passes)} passed.")
    print("🎉 ALL ORDERS SHIPPING REORDER AND STING EB-2025 CHECKS PASSED 100%!")
    print(f"============================================================================")
    return True

if __name__ == "__main__":
    success = test_orders_shipping_reorder_and_sting_eb2025()
    sys.exit(0 if success else 1)
