#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification Script: Admin Order Links Unification
Xác minh tính năng: Khi click vào các đơn hàng ở trang admin, tất cả trỏ về 1 trang duy nhất order-detail.html
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

@test("1. admin/orders.html: Mã đơn #EB-8801 đến #EB-8806 đều có thẻ <a> trỏ về order-detail.html")
def test_orders_html_order_ids():
    content = read_file("admin/orders.html")
    assert content is not None, "admin/orders.html không tồn tại!"
    order_ids = ["#EB-8801", "#EB-8802", "#EB-8803", "#EB-8804", "#EB-8805", "#EB-8806"]
    for oid in order_ids:
        pattern = rf'<a\s+href="order-detail\.html"[^>]*>{oid}</a>'
        assert re.search(pattern, content), f"Thiếu liên kết order-detail.html cho mã đơn {oid} trong admin/orders.html"

@test("2. admin/orders.html: Cột Thao tác có nút Chi Tiết trỏ về order-detail.html và nút Chuyển Trạng Thái")
def test_orders_html_actions():
    content = read_file("admin/orders.html")
    assert content is not None, "admin/orders.html không tồn tại!"
    # Có ít nhất 6 nút Chi Tiết trỏ về order-detail.html trong bảng
    detail_links = re.findall(r'<a\s+href="order-detail\.html"\s+class="btn-view-detail"[^>]*>[\s\S]*?Chi Tiết[\s\S]*?</a>', content)
    assert len(detail_links) >= 6, f"Cần ít nhất 6 nút Chi Tiết trỏ về order-detail.html trong admin/orders.html, tìm thấy {len(detail_links)}"
    # Giữ nguyên nút Chuyển Trạng Thái cho Rubric 2.6.1
    status_buttons = re.findall(r'openOrderStatusModal\(', content)
    assert len(status_buttons) >= 6, f"Cần ít nhất 6 nút Chuyển Trạng Thái trong admin/orders.html, tìm thấy {len(status_buttons)}"

@test("3. admin/index.html: Bảng đơn gần đây #EB-8801 đến #EB-8806 trỏ về order-detail.html")
def test_index_html_order_links():
    content = read_file("admin/index.html")
    assert content is not None, "admin/index.html không tồn tại!"
    order_ids = ["#EB-8801", "#EB-8802", "#EB-8803", "#EB-8804", "#EB-8805", "#EB-8806"]
    for oid in order_ids:
        pattern = rf'<a\s+href="order-detail\.html"[^>]*>{oid}</a>'
        assert re.search(pattern, content), f"Thiếu liên kết order-detail.html cho mã đơn {oid} trong admin/index.html"
    detail_links = re.findall(r'<a\s+href="order-detail\.html"\s+class="btn-view-detail"[^>]*>[\s\S]*?Chi Tiết[\s\S]*?</a>', content)
    assert len(detail_links) >= 6, f"Cần ít nhất 6 nút Chi Tiết trỏ về order-detail.html trong admin/index.html, tìm thấy {len(detail_links)}"

@test("4. admin/order-detail.html: Trang đích duy nhất có nút quay lại orders.html và đầy đủ thông tin hóa đơn")
def test_order_detail_page():
    content = read_file("admin/order-detail.html")
    assert content is not None, "admin/order-detail.html không tồn tại!"
    assert 'href="orders.html"' in content, "admin/order-detail.html thiếu liên kết quay lại orders.html"
    assert 'Quay Lại Danh Sách Đơn Hàng' in content, "admin/order-detail.html thiếu nút Quay Lại Danh Sách Đơn Hàng"
    assert 'window.print()' in content, "admin/order-detail.html thiếu nút In Hóa Đơn"
    required_ids = [
        "order-detail-id", "order-detail-date", "order-detail-status",
        "order-detail-customer", "order-detail-phone", "order-detail-address",
        "order-detail-payment", "order-detail-notes", "order-items-tbody",
        "order-detail-subtotal", "order-detail-shipping-fee", "order-detail-discount",
        "order-detail-total", "order-timeline-stepper"
    ]
    for rid in required_ids:
        assert f'id="{rid}"' in content, f"Thiếu ID '{rid}' trong admin/order-detail.html"

@test("5. Modal chi tiết khách hàng VIP: Đơn hàng gần nhất trỏ về order-detail.html")
def test_vip_modal_order_link():
    files = ["admin/orders.html", "admin/index.html", "admin/customers.html"]
    for f in files:
        content = read_file(f)
        assert content is not None, f"File {f} không tồn tại!"
        assert 'id="vip-modal-latest-order"' in content, f"File {f} thiếu #vip-modal-latest-order"
        assert 'href="order-detail.html"' in content, f"File {f} thiếu liên kết order-detail.html trong modal"

@test("6. Logic Core: js/app.js hỗ trợ nạp dữ liệu và xử lý fallback an toàn cho order-detail.html")
def test_app_js_order_detail_logic():
    content = read_file("js/app.js")
    assert content is not None, "js/app.js không tồn tại!"
    assert "function initOrderDetailPage" in content, "Thiếu hàm initOrderDetailPage trong js/app.js"
    assert "role === 'admin' ? 'EB-8801'" in content, "Thiếu logic mặc định EB-8801 cho admin trong js/app.js"
    assert "openCustomerDetailModal" in content, "Thiếu hàm openCustomerDetailModal trong js/app.js"

def main():
    print("=" * 75)
    print("XÁC MINH: LIÊN KẾT ĐƠN HÀNG ADMIN TRỎ THỐNG NHẤT VỀ ORDER-DETAIL.HTML")
    print("=" * 75)
    passed = 0
    total = len(tests)
    for name, fn in tests:
        try:
            fn()
            print(f"✅ PASS: [{name}]")
            passed += 1
        except Exception as e:
            print(f"❌ FAIL: [{name}] - {e}")

    print("=" * 75)
    print(f"KẾT QUẢ: {passed}/{total} TIÊU CHÍ ĐẠT")
    print("=" * 75)
    if passed == total:
        print("🎉 TẤT CẢ LIÊN KẾT ĐƠN HÀNG ADMIN ĐÃ TRỎ THỐNG NHẤT VỀ 1 TRANG DUY NHẤT!")
        return 0
    return 1

if __name__ == "__main__":
    sys.exit(main())
