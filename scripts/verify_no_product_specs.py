# -*- coding: utf-8 -*-
"""
verify_no_product_specs.py
Xác minh loại bỏ triệt để khối .product-specs (hardcode icon/text Sẵn hàng, 0 Đường, v.v.)
trên toàn bộ giao diện bán hàng storefront.
"""
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def read_text(rel_path):
    abs_path = os.path.join(ROOT_DIR, rel_path)
    if not os.path.exists(abs_path):
        return None
    with open(abs_path, "r", encoding="utf-8") as f:
        return f.read()

passed = 0
failed = 0

def check(description, condition, details=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"✅ PASS: [{description}]")
    else:
        failed += 1
        print(f"❌ FAIL: [{description}] -> {details}")

print("=" * 75)
print("KIỂM TRA TỰ ĐỘNG: LOẠI BỎ KHỐI PRODUCT-SPECS TRÊN STOREFRONT")
print("=" * 75)

# 1. Check index.html
idx_content = read_text("index.html")
check("index.html tồn tại", idx_content is not None)
if idx_content:
    specs_in_idx = re.findall(r'class="[^"]*product-specs[^"]*"', idx_content)
    check("index.html không còn class product-specs", len(specs_in_idx) == 0, f"Còn {len(specs_in_idx)} thẻ product-specs")
    
    # Đảm bảo 14 thẻ sản phẩm vẫn nguyên vẹn nút btn-add-stitch
    btn_add_matches = re.findall(r'class="btn-add-stitch"', idx_content)
    check("index.html bảo toàn đủ 14 nút btn-add-stitch", len(btn_add_matches) == 14, f"Có {len(btn_add_matches)} nút")
    
    # Đảm bảo 14 thẻ vẫn có điều hướng click ảnh
    img_nav_matches = re.findall(r'class="product-img-wrapper"\s+onclick="window\.location\.href=', idx_content)
    check("index.html bảo toàn đủ 14 liên kết điều hướng ảnh", len(img_nav_matches) == 14, f"Có {len(img_nav_matches)} liên kết")

# 2. Check pages/search-results.html
search_content = read_text("pages/search-results.html")
check("pages/search-results.html tồn tại", search_content is not None)
if search_content:
    specs_in_search = re.findall(r'class="[^"]*product-specs[^"]*"', search_content)
    check("pages/search-results.html không còn class product-specs", len(specs_in_search) == 0, f"Còn {len(specs_in_search)} thẻ product-specs")

# 3. Check js/app.js
app_content = read_text("js/app.js")
check("js/app.js tồn tại", app_content is not None)
if app_content:
    specs_in_app = re.findall(r'product-specs', app_content)
    check("js/app.js không còn chuỗi product-specs", len(specs_in_app) == 0, f"Còn {len(specs_in_app)} lần xuất hiện trong app.js")

print("=" * 75)
print(f"Result: {passed}/{passed + failed} passed")
if failed == 0:
    print("🎉 TOÀN BỘ PRODUCT-SPECS ĐÃ ĐƯỢC DỌN SẠCH THÀNH CÔNG!")
    sys.exit(0)
else:
    print(f"⚠️ CÓ {failed} TIÊU CHÍ CHƯA ĐẠT (RED PHASE)!")
    sys.exit(1)
