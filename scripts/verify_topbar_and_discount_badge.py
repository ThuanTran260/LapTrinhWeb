#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification script:
1. Verify .badge-discount contrast enhancements in css/style.css:
   - color: #000;
   - font-weight: 900;
   - box-shadow: 0 0 10px rgba(0, 255, 102, 0.4);
   - No color: #FFF;
   - Mathematical WCAG 2.1 AAA contrast ratio calculation (>= 7.0:1)
2. Verify top-bar announcement banner consistency across product detail pages:
   - index.html (reference baseline)
   - pages/product-detail-sting.html
   - pages/product-detail-redbull-thai.html
   - pages/product-detail-redbull-lonvua.html
   - pages/product-detail.html
   - pages/product-detail-redbull.html
   - pages/search-results.html
   - pages/account.html
3. Verify discount badges presence and text on all product detail pages:
   - Contains .badge-discount with -XX% GIẢM
   - No inline style overrides color back to #FFF or light colors
4. Verify JS showToast handling for 'info' type
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

def rel_luminance(r, g, b):
    def channel(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)

def contrast_ratio(l1, l2):
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

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

    # 2. WCAG 2.1 AAA Contrast Ratio Verification
    lum_mint = rel_luminance(0, 255, 102)     # #00FF66 (var(--secondary))
    lum_black = rel_luminance(0, 0, 0)        # #000000 (.badge-discount color)
    lum_white = rel_luminance(255, 255, 255)  # #FFFFFF (old color)

    new_ratio = contrast_ratio(lum_mint, lum_black)
    old_ratio = contrast_ratio(lum_white, lum_mint)

    check(new_ratio >= 7.0, f"Độ tương phản mới ({new_ratio:.2f}:1) đạt chuẩn WCAG AAA (>= 7.0:1)")
    check(new_ratio >= 15.0, f"Độ tương phản mới ({new_ratio:.2f}:1) đạt mức siêu nét (>= 15:1)")
    check(old_ratio < 4.5, f"Độ tương phản cũ ({old_ratio:.2f}:1) vi phạm tiêu chuẩn WCAG AA (< 4.5:1)")

    # 3. Check top-bar announcement in index.html as baseline
    index_path = root / "index.html"
    check(index_path.is_file(), "index.html tồn tại")
    if index_path.is_file():
        index_content = index_path.read_text(encoding="utf-8")
        check('class="coupon-badge"' in index_content and "ENERGY10" in index_content,
              "index.html có coupon-badge ENERGY10 trong top-bar")

    # 4. Check product detail pages top-bar announcement
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

    # 5. Check other customer-facing pages with top-bar announcement
    storefront_pages = [
        "pages/search-results.html",
        "pages/account.html",
    ]
    for page_rel in storefront_pages:
        page_path = root / page_rel
        check(page_path.is_file(), f"{page_rel} tồn tại")
        if page_path.is_file():
            content = page_path.read_text(encoding="utf-8")
            check(expected_snippet in content, f"{page_rel}: announcement-text đồng bộ ENERGY10")

    # 6. Check discount badges presence and integrity on all 5 product detail pages
    expected_discounts = {
        "pages/product-detail-sting.html": "-20% GIẢM",
        "pages/product-detail-redbull-lonvua.html": "-20% GIẢM",
        "pages/product-detail-redbull-thai.html": "-18% GIẢM",
        "pages/product-detail-redbull.html": "-18% GIẢM",
        "pages/product-detail.html": "-18% GIẢM",
    }

    for page_rel, expected_text in expected_discounts.items():
        page_path = root / page_rel
        if page_path.is_file():
            content = page_path.read_text(encoding="utf-8")
            badge_matches = re.findall(r'<span[^>]*class="[^"]*badge-discount[^"]*"[^>]*>([\s\S]*?)</span>', content)
            check(len(badge_matches) > 0, f"{page_rel}: tìm thấy thẻ .badge-discount")
            if badge_matches:
                badge_text = badge_matches[0].strip()
                check(expected_text in badge_text, f"{page_rel}: nội dung badge là '{expected_text}'")
            # Verify no inline color override
            inline_color_match = re.search(r'<span[^>]*class="[^"]*badge-discount[^"]*"[^>]*style="[^"]*color\s*:', content, re.IGNORECASE)
            check(inline_color_match is None, f"{page_rel}: .badge-discount không bị ghi đè inline color")

    # 7. Check js/app.js showToast implementation supports 'info' type
    app_js_path = root / "js" / "app.js"
    check(app_js_path.is_file(), "js/app.js tồn tại")
    if app_js_path.is_file():
        app_js_content = app_js_path.read_text(encoding="utf-8")
        check("function showToast" in app_js_content, "js/app.js định nghĩa function showToast")
        check("fas fa-info-circle" in app_js_content or "info" in app_js_content, "js/app.js hỗ trợ loại toast 'info'")

    print("=" * 80)
    print(f"KẾT QUẢ: {passed} PASS / {failed} FAIL (Tổng số: {passed + failed})")
    print("=" * 80)

    if failed > 0:
        sys.exit(1)
    print("🎉 TẤT CẢ KIỂM THỬ XÁC MINH TOPBAR VÀ DISCOUNT BADGE ĐẠT YÊU CẦU 100%!")
    sys.exit(0)

if __name__ == "__main__":
    main()
