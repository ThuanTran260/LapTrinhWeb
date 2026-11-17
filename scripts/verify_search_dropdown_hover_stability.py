#!/usr/bin/env python3
"""
verify_search_dropdown_hover_stability.py

Kiểm thử xác minh:
1. CSS (.search-static-item:hover) không làm dịch chuyển padding-left (CLS = 0).
2. CSS (.search-item-info h5) có white-space: nowrap; overflow: hidden; text-overflow: ellipsis.
3. CSS (.search-item-left & .search-item-info) có flex: 1 và min-width: 0.
4. Toàn bộ các trang storefront không còn tồn tại chuỗi '(Zero)' gây vỡ dòng trong tiêu đề Item 4.
5. Tiêu đề Item 4 đồng bộ 100% thành 'Monster Energy Ultra White 355ml' trên tất cả các trang.
"""

import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def test_css_hover_stability():
    css_path = os.path.join(REPO_ROOT, "css", "style.css")
    with open(css_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Kiểm tra .search-static-item:hover không có padding-left
    hover_match = re.search(r'\.search-static-item:hover\s*\{([^}]+)\}', content)
    assert hover_match, "Không tìm thấy .search-static-item:hover trong css/style.css"
    hover_body = hover_match.group(1)
    assert "padding-left" not in hover_body, f"LỖI: .search-static-item:hover vẫn còn padding-left: {hover_body}"
    assert "background:" in hover_body, "LỖI: .search-static-item:hover thiếu thuộc tính background highlight"
    print("PASS: .search-static-item:hover không có padding-left (ngăn ngừa CLS và giật layout).")

    # 2. Kiểm tra .search-item-left có flex: 1; min-width: 0
    left_match = re.search(r'\.search-item-left\s*\{([^}]+)\}', content)
    assert left_match, "Không tìm thấy .search-item-left trong css/style.css"
    left_body = left_match.group(1)
    assert "flex: 1" in left_body, "LỖI: .search-item-left thiếu flex: 1"
    assert "min-width: 0" in left_body, "LỖI: .search-item-left thiếu min-width: 0"
    print("PASS: .search-item-left có flex: 1 và min-width: 0.")

    # 3. Kiểm tra .search-item-info có flex: 1; min-width: 0
    info_match = re.search(r'\.search-item-info\s*\{([^}]+)\}', content)
    assert info_match, "Không tìm thấy .search-item-info trong css/style.css"
    info_body = info_match.group(1)
    assert "flex: 1" in info_body, "LỖI: .search-item-info thiếu flex: 1"
    assert "min-width: 0" in info_body, "LỖI: .search-item-info thiếu min-width: 0"
    print("PASS: .search-item-info có flex: 1 và min-width: 0.")

    # 4. Kiểm tra .search-item-info h5 có white-space: nowrap và ellipsis
    h5_match = re.search(r'\.search-item-info\s+h5\s*\{([^}]+)\}', content)
    assert h5_match, "Không tìm thấy .search-item-info h5 trong css/style.css"
    h5_body = h5_match.group(1)
    assert "white-space: nowrap" in h5_body, "LỖI: .search-item-info h5 thiếu white-space: nowrap"
    assert "overflow: hidden" in h5_body, "LỖI: .search-item-info h5 thiếu overflow: hidden"
    assert "text-overflow: ellipsis" in h5_body, "LỖI: .search-item-info h5 thiếu text-overflow: ellipsis"
    print("PASS: .search-item-info h5 có white-space: nowrap; overflow: hidden; text-overflow: ellipsis.")

def test_html_item4_consistency():
    html_files = [
        "index.html",
        "pages/account.html",
        "pages/cart.html",
        "pages/order-detail.html",
        "pages/orders.html",
        "pages/product-detail.html",
        "pages/product-detail-redbull.html",
        "pages/product-detail-sting.html",
        "pages/search-results.html",
    ]

    total_item4_found = 0
    for rel_path in html_files:
        full_path = os.path.join(REPO_ROOT, rel_path)
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Kiểm tra không còn chuỗi (Zero) trong tiêu đề h5 của Item 4
        assert "Monster Energy Ultra White 355ml (Zero)" not in content, (
            f"LỖI: Tệp {rel_path} vẫn còn chứa 'Monster Energy Ultra White 355ml (Zero)'!"
        )

        # Đếm số lượng 'Monster Energy Ultra White 355ml' trong search dropdown
        count = content.count("<h5>Monster Energy Ultra White 355ml</h5>")
        assert count > 0, f"LỖI: Tệp {rel_path} không tìm thấy tiêu đề 'Monster Energy Ultra White 355ml'!"
        total_item4_found += count
        print(f"PASS: {rel_path} đã chuẩn hóa ({count} dropdown(s)).")

    # index.html (2: header + mobile), search-results.html (2: header + mobile), 7 trang khác x 1 = 11 occurrences
    assert total_item4_found >= 11, f"LỖI: Tổng số mục dropdown tìm thấy ({total_item4_found}) ít hơn dự kiến (11)!"
    print(f"PASS: Đã xác thực thành công {total_item4_found} vị trí dropdown trên tất cả {len(html_files)} tệp HTML.")

if __name__ == "__main__":
    try:
        print("=== BẮT ĐẦU KIỂM THỬ XÁC MINH SỬA LỖI SEARCH DROPDOWN HOVER ===")
        test_css_hover_stability()
        test_html_item4_consistency()
        print("=== TẤT CẢ KIỂM THỬ ĐÃ PASS 100%! ===")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[FAIL] {e}")
        sys.exit(1)
