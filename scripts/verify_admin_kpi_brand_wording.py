#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kiểm thử tinh chỉnh câu chữ thẻ KPI thương hiệu trong trang Admin Dashboard
và phụ đề phân loại kho sang tiếng Việt thuần nhất và dấu bullet '•'.
"""

import sys
from pathlib import Path

def test_admin_kpi_brand_wording():
    root = Path(__file__).resolve().parent.parent
    admin_index_path = root / "admin" / "index.html"
    admin_inventory_path = root / "admin" / "inventory.html"

    assert admin_index_path.exists(), f"Không tìm thấy file: {admin_index_path}"
    assert admin_inventory_path.exists(), f"Không tìm thấy file: {admin_inventory_path}"

    admin_index_content = admin_index_path.read_text(encoding="utf-8")
    admin_inventory_content = admin_inventory_path.read_text(encoding="utf-8")

    failures = []

    # 1. Kiểm tra thẻ KPI số 3 trong admin/index.html
    if "<h3>3 Thương Hiệu</h3>" not in admin_index_content:
        failures.append("admin/index.html: Không tìm thấy '<h3>3 Thương Hiệu</h3>'")
    if "<p>Monster • Redbull • Sting</p>" not in admin_index_content:
        failures.append("admin/index.html: Không tìm thấy '<p>Monster • Redbull • Sting</p>'")

    # 2. Đảm bảo loại bỏ hoàn toàn các chuỗi cũ trong admin/index.html
    if "3 Brand" in admin_index_content:
        failures.append("admin/index.html: Vẫn còn tồn tại chuỗi cũ '3 Brand'")
    if "Monster, Redbull & Sting" in admin_index_content:
        failures.append("admin/index.html: Vẫn còn tồn tại chuỗi cũ 'Monster, Redbull & Sting'")

    # 3. Kiểm tra nhãn phụ tại dòng 276 admin/index.html
    if "3 Thương hiệu: Monster • Redbull • Sting" not in admin_index_content:
        failures.append("admin/index.html: Không tìm thấy nhãn phụ '3 Thương hiệu: Monster • Redbull • Sting'")

    # 4. Kiểm tra phụ đề tại dòng 57 admin/inventory.html
    if "3 Thương hiệu chính thức (Monster • Redbull • Sting)" not in admin_inventory_content:
        failures.append("admin/inventory.html: Không tìm thấy '3 Thương hiệu chính thức (Monster • Redbull • Sting)'")
    if "Monster, Redbull & Sting" in admin_inventory_content:
        failures.append("admin/inventory.html: Vẫn còn tồn tại chuỗi cũ 'Monster, Redbull & Sting'")

    if failures:
        print("[FAIL] Phát hiện lỗi kiểm thử câu chữ thẻ KPI admin:")
        for f in failures:
            print(f"  - {f}")
        return False

    print("[PASS] Tất cả các tiêu chí câu chữ thẻ KPI và phụ đề thương hiệu Admin đều đạt chuẩn 100%!")
    return True

if __name__ == "__main__":
    success = test_admin_kpi_brand_wording()
    sys.exit(0 if success else 1)
