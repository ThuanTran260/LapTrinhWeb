#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification script:
1. Verify .badge-discount contrast enhancements in css/style.css:
   - color: #000;
   - font-weight: 900;
   - box-shadow: 0 0 10px rgba(0, 255, 102, 0.4);
   - No color: #FFF;
2. Verify top-bar announcement banner consistency across product detail pages:
   - index.html (reference baseline)
   - pages/product-detail-sting.html
   - pages/product-detail-redbull-thai.html
   - pages/product-detail-redbull-lonvua.html
   - pages/product-detail.html
   - pages/product-detail-redbull.html
"""

import sys
import re
from pathlib import Path

passed = 0
failed = 0

def check(condition, message):
    global passed, failed
    if condition:
        print(f"✅ PASS: [{message}]")
        passed += 1
    else:
        print(f"❌ FAIL: [{message}]")
        failed += 1

def main():
    root = Path(__file__).resolve().parent.parent

    print("=" * 80)
    print("KIỂM TRA TỰ ĐỘNG: ĐỒNG BỘ TOPBAR ENERGY10 VÀ TƯƠNG PHẢN BADGE GIẢM GIÁ")
    print("=" * 80)

    # 1. Check css/style.css .badge-discount
    css_path = root / "css" / "style.css"
    check(css_path.is_file(), "css/style.css tồn tại")
    if css_path.is_file():
        css_content = css_path.read_text(encoding="utf-8")
        
        # Extract .badge-discount rule block
        match = re.search(r'\.badge-discount\s*\{([^}]+)\}', css_content)
        check(match is not None, "Tìm thấy class .badge-discount trong css/style.css")
        
        if match:
            rule_body = match.group(1)
            # Check color: #000
            check(re.search(r'color\s*:\s*#000\b', rule_body) is not None, ".badge-discount có thuộc tính color: #000")
            check(re.search(r'color\s*:\s*#FFF\b', rule_body, re.IGNORECASE) is None, ".badge-discount không còn dùng color: #FFF")
            # Check font-weight: 900
            check(re.search(r'font-weight\s*:\s*900\b', rule_body) is not None, ".badge-discount có font-weight: 900")
            # Check box-shadow
            check("box-shadow: 0 0 10px rgba(0, 255, 102, 0.4);" in rule_body or
                  re.search(r'box-shadow\s*:\s*0\s+0\s+10px\s+rgba\(\s*0\s*,\s*255\s*,\s*102\s*,\s*0\.4\s*\)', rule_body) is not None,
                  ".badge-discount có hiệu ứng neon glow box-shadow")
            # Check background
            check("background: var(--secondary);" in rule_body, ".badge-discount giữ nền var(--secondary)")

    # 2. Check top-bar announcement in index.html as baseline
    index_path = root / "index.html"
    check(index_path.is_file(), "index.html tồn tại")
    if index_path.is_file():
        index_content = index_path.read_text(encoding="utf-8")
        check('class="coupon-badge"' in index_content and "ENERGY10" in index_content,
              "index.html có coupon-badge ENERGY10 trong top-bar")

    # 3. Check product detail pages
    detail_pages = [
        "pages/product-detail-sting.html",
        "pages/product-detail-redbull-thai.html",
        "pages/product-detail-redbull-lonvua.html",
        "pages/product-detail.html",
        "pages/product-detail-redbull.html",
    ]

    expected_snippet = 'ENERGY BOOST: Nhập mã <span class="coupon-badge" onclick="showToast(\'Đã chép mã giảm giá ENERGY10!\', \'info\')">ENERGY10</span> giảm ngay 10% cho đơn hàng đầu tiên!'
    old_delivery_snippet = "ĐƠN HÀNG HỎA TỐC"

    for page_rel in detail_pages:
        page_path = root / page_rel
        check(page_path.is_file(), f"{page_rel} tồn tại")
        if not page_path.is_file():
            continue

        content = page_path.read_text(encoding="utf-8")
        top_bar_match = re.search(r'<div class="top-bar">[\s\S]*?</div>\s*</div>', content)
        check(top_bar_match is not None, f"{page_rel}: tìm thấy khối .top-bar")

        if top_bar_match:
            top_bar_content = top_bar_match.group(0)
            check("fas fa-bolt" in top_bar_content, f"{page_rel}: top-bar chứa icon fa-bolt")
            check("coupon-badge" in top_bar_content, f"{page_rel}: top-bar chứa class coupon-badge")
            check("ENERGY10" in top_bar_content, f"{page_rel}: top-bar chứa mã ENERGY10")
            check(expected_snippet in top_bar_content, f"{page_rel}: nội dung announcement-text khớp hoàn toàn với index.html")
            check(old_delivery_snippet not in top_bar_content, f"{page_rel}: top-bar không còn chứa văn bản giao hỏa tốc cũ")

    print("=" * 80)
    print(f"KẾT QUẢ: {passed} PASS / {failed} FAIL (Tổng số: {passed + failed})")
    print("=" * 80)

    if failed > 0:
        sys.exit(1)
    print("🎉 TẤT CẢ KIỂM THỬ XÁC MINH TOPBAR VÀ DISCOUNT BADGE ĐẠT YÊU CẦU 100%!")
    sys.exit(0)

if __name__ == "__main__":
    main()
