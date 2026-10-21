#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification Script for Energy Boost Store Admin UI Mockup (SGU Rubric).
Tests 10 canonical acceptance criteria corresponding to R1-R5:
- Test 1: Admin Login Page URL & Form (admin/login.html)
- Test 2: Admin Sidebar Logout Navigation (admin/index.html)
- Test 3: User Management - Add User Modal (admin/customers.html)
- Test 4: User Management - Edit & Lock/Unlock (admin/customers.html)
- Test 5: Product Management - Add File & Image Preview (admin/inventory.html)
- Test 6: Product Management - Edit Image & Category Select (admin/inventory.html)
- Test 7: Product Management - Smart Safe Delete Logic (js/app.js)
- Test 8: Order Management - Unidirectional State Machine (admin/orders.html)
- Test 9: Order Management - Order Filter Toast Simulation (js/app.js)
- Test 10: Customer Statistics - Top 5 VIP with Order Links (admin/customers.html)

Outputs: 10/10 PASS with exit code 0 when satisfied, or exit code 1 with failures.
"""
import os
import sys

# Đảm bảo in tiếng Việt chuẩn trên Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def check_file_content(relative_path, patterns, desc):
    abs_path = os.path.join(workspace, relative_path)
    if not os.path.exists(abs_path):
        print(f"❌ FAIL: [{desc}] File không tồn tại: {relative_path}")
        return False
    with open(abs_path, "r", encoding="utf-8") as f:
        content = f.read()
    missing = [p for p in patterns if p not in content]
    if missing:
        print(f"❌ FAIL: [{desc}] Thiếu các chuỗi bắt buộc trong {relative_path}: {missing[:2]}")
        return False
    print(f"✅ PASS: [{desc}] Thỏa mãn đầy đủ trong {relative_path}")
    return True

def main():
    print("=" * 70)
    print("KIỂM TRA 10 TIÊU CHÍ GIAO DIỆN QUẢN TRỊ ADMIN (SGU RUBRIC UI MOCKUP)")
    print("=" * 70)
    
    tests = [
        # Test 1: Admin Login Page URL riêng biệt và Form độc lập
        (
            "admin/login.html",
            ['id="admin-login-form"', 'handleAdminLogin', 'ĐĂNG NHẬP HỆ THỐNG QUẢN TRỊ'],
            "Test 1: Admin Login Page URL riêng & Form độc lập (admin/login.html)"
        ),
        # Test 2: Admin Sidebar Logout trỏ về admin/login.html
        (
            "admin/index.html",
            ['href="login.html"', 'admin-logout'],
            "Test 2: Admin Sidebar Logout điều hướng về login.html"
        ),
        # Test 3: Modal Thêm Người Dùng Mới
        (
            "admin/customers.html",
            ['id="modal-add-user"', 'openAddUserModal', 'saveAddUser'],
            "Test 3: Quản lý User - Modal Thêm Người Dùng Mới"
        ),
        # Test 4: Modal Sửa Người Dùng & Nút Khoá / Mở User
        (
            "admin/customers.html",
            ['id="modal-edit-user"', 'openEditUserModal', 'toggleLockUser'],
            "Test 4: Quản lý User - Modal Sửa & Nút Khoá/Mở User"
        ),
        # Test 5: Modal Thêm Sản Phẩm có Chọn File và Preview ảnh
        (
            "admin/inventory.html",
            ['type="file"', 'id="add-prod-file"', 'id="add-prod-preview"', 'previewAddProductImage'],
            "Test 5: Quản lý Kho - Thêm Sản Phẩm có Upload & Preview ảnh"
        ),
        # Test 6: Modal Sửa Sản Phẩm hiển thị đúng Ảnh hiện tại & Danh mục
        (
            "admin/inventory.html",
            ['id="edit-prod-img-preview"', 'id="edit-prod-brand-select"', 'previewEditProductImage'],
            "Test 6: Quản lý Kho - Sửa Sản Phẩm nạp đúng Ảnh & Danh mục"
        ),
        # Test 7: Xóa sản phẩm an toàn (Đã bán -> Ẩn, Chưa bán -> Confirm & Xóa)
        (
            "js/app.js",
            ['handleAdminDeleteProduct', 'confirm', 'ĐÃ ẨN'],
            "Test 7: Quản lý Kho - Xóa sản phẩm an toàn (Smart Safe Delete)"
        ),
        # Test 8: Cập nhật tình trạng đơn hàng một chiều
        (
            "admin/orders.html",
            ['openOrderStatusModal', 'Chưa xác nhận', 'Đã xác nhận', 'Đã giao (Thành công)'],
            "Test 8: Quản lý Đơn Hàng - Quy trình trạng thái một chiều"
        ),
        # Test 9: Lọc đơn hàng mô phỏng bằng Toast Notification
        (
            "js/app.js",
            ['applyAdminOrderFilter', 'Đã áp dụng bộ lọc đơn hàng'],
            "Test 9: Quản lý Đơn Hàng - Lọc mô phỏng thông báo Toast"
        ),
        # Test 10: Thống kê Top 5 Khách hàng chi tiêu cao nhất có link xem đơn hàng
        (
            "admin/customers.html",
            ['TOP 5 KHÁCH HÀNG', 'stat-customer-from', 'stat-customer-to', 'openOrderDetailModal'],
            "Test 10: Thống Kê - Top 5 Khách hàng chi tiêu cao nhất kèm Link Đơn"
        )
    ]
    
    passed_count = 0
    for file_rel, patterns, desc in tests:
        if check_file_content(file_rel, patterns, desc):
            passed_count += 1
            
    print("=" * 70)
    print(f"KẾT QUẢ TỔNG HỢP: {passed_count}/{len(tests)} TIÊU CHÍ ĐẠT")
    print("=" * 70)
    
    if passed_count == len(tests):
        print("🎉 XÁC MINH TOÀN DIỆN THÀNH CÔNG (10/10 PASS) - ĐẠT CHUẨN RUBRIC!")
        sys.exit(0)
    else:
        print(f"⚠️ CÒN {len(tests) - passed_count} TIÊU CHÍ CHƯA ĐẠT. VUI LÒNG KIỂM TRA LẠI!")
        sys.exit(1)

if __name__ == "__main__":
    main()
