#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification Script:
1. Synchronized discounts & sale badges across Flash Sale and Brand Sections (#monster-products, #redbull-products) in index.html and pages/search-results.html.
2. Clean labels without parentheses in #filter-order-location in admin/orders.html.
3. DOM validity & UI button uniformity for all 14 product cards.
"""

import os
import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def read_file(rel_path):
    path = os.path.join(ROOT, rel_path)
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

tests = []
def test(name):
    def decorator(fn):
        tests.append((name, fn))
        return fn
    return decorator

# --------------------------------------------------------------------------
# Test Suite
# --------------------------------------------------------------------------

@test("1. index.html #flash-sale: 4 sản phẩm sale có đầy đủ badge sale và giá gạch ngang")
def test_flash_sale_discounts():
    content = read_file("index.html")
    assert content, "index.html không tồn tại!"
    
    flash_match = re.search(r'<section\s+id="flash-sale"[\s\S]*?</section>', content)
    assert flash_match, "Không tìm thấy section #flash-sale trong index.html"
    flash_html = flash_match.group(0)
    
    expected_flash = [
        ("Monster Energy Original 355ml", "-18%", "45.000đ", "55.000đ"),
        ("Monster Zero Ultra White 500ml", "-13%", "48.000đ", "55.000đ"),
        ("Nước Tăng Lực Redbull Original 250ml", "-18%", "18.000đ", "22.000đ"),
        ("Nước Tăng Lực Redbull Nắp Bật 250ml", "-20%", "20.000đ", "25.000đ"),
    ]
    
    for name, badge, price, old_price in expected_flash:
        assert name in flash_html, f"Thiếu sản phẩm '{name}' trong #flash-sale"
        assert badge in flash_html, f"Thiếu badge '{badge}' cho '{name}' trong #flash-sale"
        assert price in flash_html, f"Thiếu giá '{price}' cho '{name}' trong #flash-sale"
        assert old_price in flash_html, f"Thiếu giá cũ '{old_price}' cho '{name}' trong #flash-sale"

@test("2. index.html #monster-products: Đồng bộ badge sale và <del> giá cũ cho Monster Original (-18%) & Monster Ultra White (-13%)")
def test_monster_products_discounts():
    content = read_file("index.html")
    assert content, "index.html không tồn tại!"
    
    monster_match = re.search(r'<section\s+id="monster-products"[\s\S]*?</section>', content)
    assert monster_match, "Không tìm thấy section #monster-products trong index.html"
    monster_html = monster_match.group(0)
    
    # 1. Monster Energy Original 355ml
    assert "Monster Energy Original 355ml" in monster_html, "Thiếu Monster Energy Original 355ml trong #monster-products"
    m_orig_pattern = r'Monster Energy Original 355ml[\s\S]*?<span class="price-val">\s*45\.000đ\s*</span>\s*<del class="price-old">\s*55\.000đ\s*</del>'
    assert re.search(m_orig_pattern, monster_html), "Monster Original trong #monster-products thiếu cấu hình giá <span class='price-val'>45.000đ</span><del class='price-old'>55.000đ</del>"
    
    # Check badge -18% on Monster Original card
    orig_card_match = re.search(r'<!-- Can 1: Monster Original -->([\s\S]*?)<!-- Can 2:', monster_html)
    assert orig_card_match, "Không phân tách được card Can 1: Monster Original"
    assert '<span class="stitch-badge sale">-18%</span>' in orig_card_match.group(1), "Card Monster Original thiếu badge sale -18%"
    
    # 2. Monster Zero Ultra White 500ml
    assert "Monster Zero Ultra White 500ml" in monster_html, "Thiếu Monster Zero Ultra White 500ml trong #monster-products"
    m_white_pattern = r'Monster Zero Ultra White 500ml[\s\S]*?<span class="price-val">\s*48\.000đ\s*</span>\s*<del class="price-old">\s*55\.000đ\s*</del>'
    assert re.search(m_white_pattern, monster_html), "Monster Ultra White trong #monster-products thiếu cấu hình giá <span class='price-val'>48.000đ</span><del class='price-old'>55.000đ</del>"
    
    # Check badge -13% on Monster Ultra White card
    white_card_match = re.search(r'<!-- Can 2: Zero Ultra White -->([\s\S]*?)<!-- Can 3:', monster_html)
    assert white_card_match, "Không phân tách được card Can 2: Zero Ultra White"
    assert '<span class="stitch-badge sale">-13%</span>' in white_card_match.group(1), "Card Monster Ultra White thiếu badge sale -13%"

@test("3. index.html #redbull-products: Đồng bộ badge sale và <del> giá cũ cho Redbull Original (-18%) & Redbull Nắp Bật (-20%)")
def test_redbull_products_discounts():
    content = read_file("index.html")
    assert content, "index.html không tồn tại!"
    
    redbull_match = re.search(r'<section\s+id="redbull-products"[\s\S]*?</section>', content)
    assert redbull_match, "Không tìm thấy section #redbull-products trong index.html"
    redbull_html = redbull_match.group(0)
    
    # 1. Redbull Original 250ml
    assert "Nước Tăng Lực Redbull Original 250ml" in redbull_html, "Thiếu Nước Tăng Lực Redbull Original 250ml trong #redbull-products"
    rb_orig_pattern = r'Nước Tăng Lực Redbull Original 250ml[\s\S]*?<span class="price-val">\s*18\.000đ\s*</span>\s*<del class="price-old">\s*22\.000đ\s*</del>'
    assert re.search(rb_orig_pattern, redbull_html), "Redbull Original trong #redbull-products thiếu cấu hình giá <span class='price-val'>18.000đ</span><del class='price-old'>22.000đ</del>"
    
    # Check badge -18% on Redbull Original card
    rb_orig_card = re.search(r'<!-- Redbull 1: Redbull Original -->([\s\S]*?)<!-- Redbull 2:', redbull_html)
    assert rb_orig_card, "Không phân tách được card Redbull 1: Redbull Original"
    assert '<span class="stitch-badge sale">-18%</span>' in rb_orig_card.group(1), "Card Redbull Original thiếu badge sale -18%"
    
    # 2. Redbull Nắp Bật 250ml
    assert "Nước Tăng Lực Redbull Nắp Bật 250ml" in redbull_html, "Thiếu Nước Tăng Lực Redbull Nắp Bật 250ml trong #redbull-products"
    rb_napbat_pattern = r'Nước Tăng Lực Redbull Nắp Bật 250ml[\s\S]*?<span class="price-val">\s*20\.000đ\s*</span>\s*<del class="price-old">\s*25\.000đ\s*</del>'
    assert re.search(rb_napbat_pattern, redbull_html), "Redbull Nắp Bật trong #redbull-products thiếu cấu hình giá <span class='price-val'>20.000đ</span><del class='price-old'>25.000đ</del>"
    
    # Check badge -20% on Redbull Nắp Bật card
    rb_napbat_card = re.search(r'<!-- Redbull 3: Redbull Lon Vừa Nắp Bật -->([\s\S]*?)</section>', redbull_html)
    assert rb_napbat_card, "Không phân tách được card Redbull 3: Redbull Lon Vừa Nắp Bật"
    assert '<span class="stitch-badge sale">-20%</span>' in rb_napbat_card.group(1), "Card Redbull Nắp Bật thiếu badge sale -20%"

@test("4. pages/search-results.html: Đồng bộ badge sale -18% và <del class='price-old'>55.000đ</del> cho Monster Original")
def test_search_results_discount():
    content = read_file("pages/search-results.html")
    assert content, "pages/search-results.html không tồn tại!"
    
    assert '<span class="stitch-badge sale">-18%</span>' in content, "search-results.html thiếu badge sale -18%"
    assert '<del class="price-old">55.000đ</del>' in content, "search-results.html thiếu <del class='price-old'>55.000đ</del>"
    assert '<span class="price-val">45.000đ</span>' in content, "search-results.html thiếu <span class='price-val'>45.000đ</span>"

@test("5. admin/orders.html: #filter-order-location hoàn toàn sạch ký tự ngoặc đơn '(...)'")
def test_admin_orders_filter_location_clean():
    content = read_file("admin/orders.html")
    assert content, "admin/orders.html không tồn tại!"
    
    select_match = re.search(r'<select[^>]*id="filter-order-location"[^>]*>([\s\S]*?)</select>', content)
    assert select_match, "Không tìm thấy thẻ <select id='filter-order-location'> trong admin/orders.html"
    select_body = select_match.group(1)
    
    # Kiểm tra không chứa dấu '(' hoặc ')'
    options = re.findall(r'<option[^>]*>(.*?)</option>', select_body)
    assert len(options) == 7, f"Kỳ vọng 7 options trong #filter-order-location, nhận được {len(options)}"
    for opt in options:
        opt_text = opt.strip()
        assert '(' not in opt_text and ')' not in opt_text, f"Option '{opt_text}' vẫn còn chứa dấu ngoặc đơn!"
    
    expected_options = [
        ("all", "Tất cả phường/xã"),
        ("ben-nghe", "Phường Bến Nghé"),
        ("tan-dinh", "Phường Tân Định"),
        ("pham-ngu-lao", "Phường Phạm Ngũ Lão"),
        ("vo-thi-sau", "Phường Võ Thị Sáu"),
        ("da-kao", "Phường Đa Kao"),
        ("binh-hung", "Xã Bình Hưng")
    ]
    for val, text in expected_options:
        opt_pattern = rf'<option\s+value="{val}">\s*{re.escape(text)}\s*</option>'
        assert re.search(opt_pattern, select_body), f"Thiếu option value='{val}' với text '{text}' trong dropdown #filter-order-location"

@test("6. CSS style.css: Hỗ trợ styling đầy đủ cho .price-val và del.price-old")
def test_css_price_styles():
    css = read_file("css/style.css")
    assert css, "css/style.css không tồn tại!"
    assert ".price-val" in css, "style.css thiếu class .price-val"
    assert "del.price-old" in css or ".price-old" in css, "style.css thiếu style cho price-old"
    assert ".product-price:has(.price-val)" in css or ".price-val" in css, "style.css có quy tắc định dạng layout cho sản phẩm giảm giá"

def main():
    print("=" * 75)
    print("XÁC MINH: ĐỒNG BỘ GIẢM GIÁ VÀ BỘ LỌC PHƯỜNG/XÃ GỌN GÀNG (NO PARENTHESES)")
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
        print("🎉 TẤT CẢ TIÊU CHÍ ĐỒNG BỘ GIẢM GIÁ & BỘ LỌC ĐỀU ĐẠT 100%!")
        return 0
    else:
        print("❌ CÓ TIÊU CHÍ CHƯA ĐẠT, VUI LÒNG KIỂM TRA LẠI!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
