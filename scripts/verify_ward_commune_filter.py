#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification Script: Ward & Commune Order Location Filter & Post-Merger Addresses
Xác minh tính năng: Chuyển đổi bộ lọc quận/huyện thành phường/xã phù hợp thực tế sau sáp nhập tại TP.HCM.
- #filter-order-location trong admin/orders.html với các tuỳ chọn phường/xã.
- applyAdminOrderFilter() hiển thị toast thông báo phường/xã được chọn mà KHÔNG ẩn hàng trong bảng.
- Đơn hàng #EB-8805 và #EB-8806 cập nhật địa chỉ phản ánh Phường Võ Thị Sáu (Quận 3).
"""

import os
import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def read_file(rel_path):
    path = os.path.join(ROOT, rel_path)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

tests = []
def test(name):
    def decorator(fn):
        tests.append((name, fn))
        return fn
    return decorator

@test("1. admin/orders.html: #filter-order-location tồn tại với tuỳ chọn mặc định 'Tất cả phường/xã (TP.HCM)'")
def test_filter_select_default():
    content = read_file("admin/orders.html")
    assert content is not None, "admin/orders.html không tồn tại!"
    assert 'id="filter-order-location"' in content, "Thiếu id='filter-order-location' trong admin/orders.html"
    
    # Kiểm tra tuỳ chọn mặc định
    default_opt_pattern = r'<option\s+value="all">\s*Tất cả phường/xã \(TP\.HCM\)\s*</option>'
    assert re.search(default_opt_pattern, content), "Thiếu tuỳ chọn mặc định 'Tất cả phường/xã (TP.HCM)' với value='all'"

@test("2. admin/orders.html: #filter-order-location chứa đầy đủ các tuỳ chọn phường/xã sau sáp nhập")
def test_filter_select_wards():
    content = read_file("admin/orders.html")
    assert content is not None, "admin/orders.html không tồn tại!"
    
    select_match = re.search(r'<select[^>]*id="filter-order-location"[^>]*>([\s\S]*?)</select>', content)
    assert select_match, "Không tìm thấy thẻ <select id='filter-order-location'> trong admin/orders.html"
    select_body = select_match.group(1)
    
    expected_wards = [
        "Phường Bến Nghé",
        "Phường Tân Định",
        "Phường Phạm Ngũ Lão",
        "Phường Võ Thị Sáu",
        "Phường Đa Kao",
        "Xã Bình Hưng"
    ]
    for ward in expected_wards:
        assert ward in select_body, f"Thiếu phường/xã '{ward}' trong dropdown #filter-order-location"

@test("3. js/app.js: applyAdminOrderFilter() lấy text phường/xã đã chọn và hiển thị toast, KHÔNG ẩn hàng")
def test_apply_filter_logic():
    content = read_file("js/app.js")
    assert content is not None, "js/app.js không tồn tại!"
    
    assert "function applyAdminOrderFilter" in content, "Thiếu hàm applyAdminOrderFilter trong js/app.js"
    
    # Tìm thân hàm applyAdminOrderFilter
    fn_match = re.search(r'function\s+applyAdminOrderFilter\s*\(\)\s*\{([\s\S]*?)\n\}', content)
    assert fn_match, "Không phân tích được thân hàm applyAdminOrderFilter"
    fn_body = fn_match.group(1)
    
    # Kiểm tra việc lấy element filter-order-location và lấy text của option
    assert "filter-order-location" in fn_body, "applyAdminOrderFilter không tham chiếu tới filter-order-location"
    assert "options[" in fn_body and ".text" in fn_body, "applyAdminOrderFilter không lấy text của option được chọn"
    
    # Kiểm tra toast thông báo
    assert "showToast" in fn_body, "applyAdminOrderFilter thiếu gọi showToast"
    assert "Khu vực:" in fn_body, "Toast thông báo trong applyAdminOrderFilter thiếu thông tin 'Khu vực:'"
    
    # Kiểm tra KHÔNG ẩn/xóa hàng trong bảng (giữ nguyên toàn bộ hàng theo yêu cầu người dùng)
    assert "style.display = 'none'" not in fn_body, "applyAdminOrderFilter không được ẩn hàng (style.display = 'none')"
    assert "display = 'none'" not in fn_body, "applyAdminOrderFilter không được ẩn hàng (display = 'none')"
    assert ".remove()" not in fn_body, "applyAdminOrderFilter không được xoá hàng (.remove())"

@test("4. js/app.js: MOCK_ORDER_DATABASE cập nhật đơn #EB-8805 và #EB-8806 phản ánh P. Võ Thị Sáu")
def test_order_database_addresses():
    content = read_file("js/app.js")
    assert content is not None, "js/app.js không tồn tại!"
    
    # Kiểm tra EB-8805
    eb8805_match = re.search(r"['\"]EB-8805['\"]\s*:\s*\{([\s\S]*?)\n\s*\},", content)
    assert eb8805_match, "Không tìm thấy cấu hình đơn hàng 'EB-8805' trong MOCK_ORDER_DATABASE"
    eb8805_body = eb8805_match.group(1)
    assert "P. Võ Thị Sáu" in eb8805_body, "Địa chỉ đơn EB-8805 thiếu 'P. Võ Thị Sáu'"
    assert "89 Cách Mạng Tháng 8, P. Võ Thị Sáu, Quận 3, TP.HCM" in eb8805_body, "Địa chỉ đơn EB-8805 không đúng định dạng chuẩn"

    # Kiểm tra EB-8806
    eb8806_match = re.search(r"['\"]EB-8806['\"]\s*:\s*\{([\s\S]*?)\n\s*\},", content)
    assert eb8806_match, "Không tìm thấy cấu hình đơn hàng 'EB-8806' trong MOCK_ORDER_DATABASE"
    eb8806_body = eb8806_match.group(1)
    assert "P. Võ Thị Sáu" in eb8806_body, "Địa chỉ đơn EB-8806 thiếu 'P. Võ Thị Sáu'"
    assert "15 Võ Văn Tần, P. Võ Thị Sáu, Quận 3, TP.HCM" in eb8806_body, "Địa chỉ đơn EB-8806 không đúng định dạng chuẩn"

@test("5. admin/order-detail.html & admin/orders.html: Địa chỉ hiển thị khớp dữ liệu phường/xã sau sáp nhập")
def test_displayed_addresses():
    # Kiểm tra admin/orders.html và admin/order-detail.html
    orders_html = read_file("admin/orders.html")
    assert orders_html is not None, "admin/orders.html không tồn tại!"
    order_detail_html = read_file("admin/order-detail.html")
    assert order_detail_html is not None, "admin/order-detail.html không tồn tại!"
    
    # Không còn địa chỉ cũ P. 6, Quận 3 trong cả 2 file
    assert "P. 6, Quận 3" not in orders_html, "admin/orders.html còn chứa địa chỉ cũ 'P. 6, Quận 3'"
    assert "P. 6, Quận 3" not in order_detail_html, "admin/order-detail.html còn chứa địa chỉ cũ 'P. 6, Quận 3'"
    
    # order-detail.html có trường #order-detail-address để bind địa chỉ từ MOCK_ORDER_DATABASE
    assert 'id="order-detail-address"' in order_detail_html, "admin/order-detail.html thiếu element #order-detail-address"

def main():
    print("=" * 75)
    print("XÁC MINH: BỘ LỌC PHƯỜNG/XÃ & ĐỊA CHỈ ĐƠN HÀNG SAU SÁP NHẬP")
    print("=" * 75)
    passed = 0
    total = len(tests)
    for name, fn in tests:
        try:
            fn()
            print(f"✅ PASS: [{name}]")
            passed += 1
        except AssertionError as e:
            print(f"❌ FAIL: [{name}] -> {e}")
        except Exception as e:
            print(f"💥 ERROR: [{name}] -> {type(e).__name__}: {e}")

    print("=" * 75)
    print(f"KẾT QUẢ: {passed}/{total} TIÊU CHÍ ĐẠT")
    print("=" * 75)
    if passed == total:
        print("🎉 TẤT CẢ TIÊU CHÍ BỘ LỌC PHƯỜNG/XÃ VÀ ĐỊA CHỈ SAU SÁP NHẬP ĐỀU ĐẠT!")
        return 0
    else:
        print("❌ CÓ TIÊU CHÍ CHƯA ĐẠT, VUI LÒNG KIỂM TRA LẠI!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
