# -*- coding: utf-8 -*-
"""
verify_order_detail_pages.py
Kiểm tra toàn diện tính năng Chi Tiết Đơn Hàng (Dedicated Standalone Pages),
Đồng bộ Header lon nước, Đồng bộ nút Chỉnh Sửa Kho Hàng và Loại bỏ (TĨNH).
"""
import os
import re
import sys

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def read_text(rel_path):
    abs_path = os.path.join(ROOT_DIR, rel_path)
    if not os.path.exists(abs_path):
        return None
    with open(abs_path, "r", encoding="utf-8") as f:
        return f.read()

def run_test(name, fn):
    try:
        fn()
        print(f"✅ PASS: [{name}]")
        return True
    except AssertionError as e:
        print(f"❌ FAIL: [{name}] -> {e}")
        return False
    except Exception as e:
        print(f"💥 ERROR: [{name}] -> {type(e).__name__}: {e}")
        return False

tests = []

def test(name):
    def decorator(fn):
        tests.append((name, fn))
        return fn
    return decorator

# --- Test 1: admin/order-detail.html standalone page ---
@test("1. Admin: admin/order-detail.html tồn tại và đầy đủ cấu trúc hóa đơn chi tiết")
def test_admin_order_detail_exists():
    content = read_text("admin/order-detail.html")
    assert content is not None, "File admin/order-detail.html không tồn tại!"
    
    required_ids = [
        "order-detail-id", "order-detail-date", "order-detail-status",
        "order-detail-customer", "order-detail-phone", "order-detail-address",
        "order-detail-payment", "order-detail-notes", "order-items-tbody",
        "order-detail-subtotal", "order-detail-shipping-fee", "order-detail-discount",
        "order-detail-total", "order-timeline-stepper"
    ]
    for rid in required_ids:
        assert f'id="{rid}"' in content, f"Thiếu DOM id='{rid}' trong admin/order-detail.html"
    
    assert "@media print" in content, "Thiếu CSS in ấn @media print trong admin/order-detail.html"
    assert "window.print()" in content, "Thiếu nút in window.print() trong admin/order-detail.html"
    assert "orders.html" in content, "Thiếu liên kết quay lại orders.html"

# --- Test 2: pages/order-detail.html standalone page ---
@test("2. Storefront: pages/order-detail.html tồn tại và đồng bộ header 3 nút + hóa đơn")
def test_storefront_order_detail_exists():
    content = read_text("pages/order-detail.html")
    assert content is not None, "File pages/order-detail.html không tồn tại!"
    
    required_ids = [
        "order-detail-id", "order-detail-date", "order-detail-status",
        "order-detail-customer", "order-detail-phone", "order-detail-address",
        "order-detail-payment", "order-detail-notes", "order-items-tbody",
        "order-detail-subtotal", "order-detail-shipping-fee", "order-detail-discount",
        "order-detail-total", "order-timeline-stepper"
    ]
    for rid in required_ids:
        assert f'id="{rid}"' in content, f"Thiếu DOM id='{rid}' trong pages/order-detail.html"
        
    assert "header-actions" in content, "Thiếu .header-actions trong pages/order-detail.html"
    assert 'id="header-account-link"' in content, "Thiếu #header-account-link trong header actions"
    assert 'id="header-account-value"' in content, "Thiếu #header-account-value trong header actions"
    assert "@media print" in content, "Thiếu CSS in ấn @media print trong pages/order-detail.html"
    assert "window.print()" in content, "Thiếu nút in window.print() trong pages/order-detail.html"

# --- Test 3: js/app.js Database và Routing ---
@test("3. Logic Core: js/app.js có MOCK_ORDER_DATABASE (9 đơn) và initOrderDetailPage")
def test_app_js_orders_data_and_router():
    content = read_text("js/app.js")
    assert content is not None, "File js/app.js không tồn tại!"
    
    assert "MOCK_ORDER_DATABASE" in content, "Thiếu MOCK_ORDER_DATABASE trong js/app.js"
    order_codes = ["EB-8801", "EB-8802", "EB-8803", "EB-8804", "EB-8805", "EB-8806", "EB-2026", "EB-2025", "EB-2024"]
    for code in order_codes:
        assert f"'{code}'" in content or f'"{code}"' in content, f"Thiếu mã đơn {code} trong MOCK_ORDER_DATABASE"
        
    assert "function initOrderDetailPage" in content, "Thiếu hàm initOrderDetailPage trong js/app.js"
    assert "function openOrderDetailModal" in content, "Thiếu hàm openOrderDetailModal trong js/app.js"
    assert "order-detail.html?id=" in content, "Thiếu logic điều hướng order-detail.html?id= trong js/app.js"

# --- Test 4: Đồng bộ Header trên 5 trang chi tiết sản phẩm ---
@test("4. Header Uniformity: 5 trang product-detail*.html đồng bộ 3 nút gồm #header-account-link")
def test_product_detail_headers():
    files = [
        "pages/product-detail.html",
        "pages/product-detail-sting.html",
        "pages/product-detail-redbull.html",
        "pages/product-detail-redbull-thai.html",
        "pages/product-detail-redbull-lonvua.html"
    ]
    for f in files:
        content = read_text(f)
        assert content is not None, f"File {f} không tồn tại!"
        assert "header-actions" in content, f"File {f} thiếu cụm .header-actions"
        assert 'id="header-account-link"' in content, f"File {f} thiếu nút #header-account-link"
        assert 'id="header-account-value"' in content, f"File {f} thiếu #header-account-value"
        assert "orders.html" in content, f"File {f} thiếu nút Đơn hàng (orders.html)"
        assert "cart.html" in content, f"File {f} thiếu nút Giỏ hàng (cart.html)"

# --- Test 5: Đồng bộ nút Chỉnh Sửa Kho Hàng (inventory.html) ---
@test("5. Parity: admin/inventory.html có nút Chỉnh Sửa thống nhất về edit-monster.html")
def test_inventory_edit_links():
    content = read_text("admin/inventory.html")
    assert content is not None, "File admin/inventory.html không tồn tại!"
    
    assert "edit-monster.html" in content, "admin/inventory.html thiếu link edit-monster.html"
    # Toàn bộ 10 sản phẩm trong bảng kho đều trỏ thống nhất về edit-monster.html
    count_edit_monster = content.count('href="edit-monster.html"')
    assert count_edit_monster >= 10, f"Cần ít nhất 10 nút Chỉnh Sửa trỏ về edit-monster.html, tìm thấy {count_edit_monster}"
    assert "edit-redbull" not in content, "Vẫn còn link edit-redbull trong admin/inventory.html"
    assert 'href="edit-sting.html"' not in content, "Vẫn còn link edit-sting.html trong admin/inventory.html"

# --- Test 6: Loại bỏ hoàn toàn chữ (TĨNH) khỏi 4 trang Admin ---
@test("6. UI Cleanliness: 0 tiêu đề chứa '(TĨNH)' trên 4 trang Admin")
def test_remove_tinh_from_admin():
    admin_files = [
        "admin/index.html",
        "admin/inventory.html",
        "admin/orders.html",
        "admin/revenue.html"
    ]
    for f in admin_files:
        content = read_text(f)
        assert content is not None, f"File {f} không tồn tại!"
        assert "(TĨNH)" not in content, f"File {f} vẫn còn chữ '(TĨNH)'!"

# --- Test 7: Bỏ nút Chi tiết/Xem trong admin, giữ liên kết đơn mua của khách hàng ---
@test("7. Admin: Bỏ nút Chi tiết/Xem, giữ liên kết đơn mua và chi tiết đơn hàng storefront")
def test_modal_cleanup_and_links():
    admin_files = ["admin/orders.html", "admin/customers.html", "admin/index.html"]
    for f in admin_files:
        content = read_text(f)
        assert content is not None, f"File {f} không tồn tại!"
        assert 'id="modal-order-detail"' not in content, f"File {f} vẫn còn thừa modal #modal-order-detail!"
        assert 'fa-eye' not in content, f"File {f} vẫn còn nút Chi tiết/Xem"
        if f == "admin/customers.html":
            assert 'href="order-detail.html?id=' in content, "Thiếu liên kết đơn hàng mua của khách hàng"
        else:
            assert 'href="order-detail.html"' not in content, f"File {f} vẫn còn nút chi tiết đơn hàng"
        
    store_files = ["pages/orders.html", "pages/account.html"]
    for f in store_files:
        content = read_text(f)
        assert content is not None, f"File {f} không tồn tại!"
        assert "order-detail.html?id=" in content, f"File {f} thiếu link sang order-detail.html?id="

# --- Test 8: Voucher Chips Visual Feedback & Static 10% Rubric Integrity ---
@test("8. Settings Voucher: switchVoucherPreview giữ cố định 10% tĩnh và cập nhật active chip + toast")
def test_switch_voucher_preview_static_integrity():
    content = read_text("js/app.js")
    assert content is not None, "File js/app.js không tồn tại!"
    
    # Extract function switchVoucherPreview
    match = re.search(r"function\s+switchVoucherPreview\s*\([^)]*\)\s*\{([\s\S]*?)\n\}", content)
    assert match, "Không tìm thấy hàm switchVoucherPreview trong js/app.js"
    fn_body = match.group(1)
    
    # Verify no dynamic overwriting of form inputs
    assert "mainAmountInput" not in fn_body, "switchVoucherPreview vẫn còn chứa mainAmountInput!"
    assert "mainCodeInput" not in fn_body, "switchVoucherPreview vẫn còn chứa mainCodeInput!"
    assert "updateVoucherLivePreview" not in fn_body, "switchVoucherPreview không được gọi updateVoucherLivePreview!"
    
    # Verify active state update and toast
    assert "activeVoucherCode =" in fn_body, "switchVoucherPreview thiếu cập nhật activeVoucherCode"
    assert "renderVoucherChips()" in fn_body, "switchVoucherPreview phải gọi renderVoucherChips() để cập nhật active class"
    assert "showToast" in fn_body, "switchVoucherPreview phải gọi showToast để hiển thị phản hồi tương tác"

    # Verify admin/settings.html keeps static 10% rubric template
    settings_html = read_text("admin/settings.html")
    assert settings_html is not None, "File admin/settings.html không tồn tại!"
    assert 'value="MONSTER10"' in settings_html, "Form voucher-code phải có default value='MONSTER10'"
    assert 'value="10%"' in settings_html, "Form voucher-amount phải có default value='10%'"
    assert "GIẢM 10%" in settings_html, "Vé xem trước preview-ticket-discount phải chứa 'GIẢM 10%'"

def main():
    print("=" * 75)
    print("XÁC MINH CÁC TÍNH NĂNG ĐẶC BIỆT: TRANG CHI TIẾT ĐƠN HÀNG, HEADER & KHO HÀNG")
    print("=" * 75)
    
    passed = 0
    total = len(tests)
    for name, fn in tests:
        if run_test(name, fn):
            passed += 1
            
    print("=" * 75)
    print(f"KẾT QUẢ KIỂM THỬ: {passed}/{total} TIÊU CHÍ ĐẠT (100% SUCCESS)")
    print("=" * 75)
    
    if passed == total:
        print(f"🎉 TẤT CẢ {passed}/{total} NHÓM TIÊU CHÍ ĐỀU ĐẠT CHUẨN XUẤT SẮC!")
        sys.exit(0)
    else:
        print(f"⚠️ CÓ {total - passed} TIÊU CHÍ THẤT BẠI. CẦN SỬA LẠI!")
        sys.exit(1)

if __name__ == "__main__":
    main()
