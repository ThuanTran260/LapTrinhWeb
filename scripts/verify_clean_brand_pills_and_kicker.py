# -*- coding: utf-8 -*-
"""
verify_clean_brand_pills_and_kicker.py
Xác minh:
1. Chuẩn hóa nhãn phân loại nhanh theo hãng (bỏ số vị hardcode: 4 vị, 3 vị).
2. Lược bỏ thẻ kicker marketing hardcode "12.400+ KHÁCH HÀNG TIN DÙNG".
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
print("KIỂM TRA TỰ ĐỘNG: CHUẨN HÓA BRAND PILLS VÀ LƯỢC BỎ KICKER 12.400+")
print("=" * 75)

idx_content = read_text("index.html")
check("index.html tồn tại", idx_content is not None)

if idx_content:
    # 1. Check quick brand selector doesn't have "(4 vị)" or "(3 vị)"
    flavor_counts = re.findall(r'\(\s*\d+\s*vị\s*\)', idx_content)
    check("index.html không còn chuỗi (X vị)", len(flavor_counts) == 0, f"Còn {len(flavor_counts)} chuỗi số vị: {flavor_counts}")

    # 2. Check quick brand nav has clean labels
    has_monster_clean = re.search(r'class="quick-brand-btn[^"]*".*?Monster Energy\s*</a>', idx_content, re.DOTALL) is not None
    has_redbull_clean = re.search(r'class="quick-brand-btn[^"]*".*?Redbull Thái Lan\s*</a>', idx_content, re.DOTALL) is not None
    has_sting_clean = re.search(r'class="quick-brand-btn[^"]*".*?Sting PepsiCo\s*</a>', idx_content, re.DOTALL) is not None
    check("quick-brand-nav có nhãn sạch Monster Energy", has_monster_clean)
    check("quick-brand-nav có nhãn sạch Redbull Thái Lan", has_redbull_clean)
    check("quick-brand-nav có nhãn sạch Sting PepsiCo", has_sting_clean)

    # 3. Check quick-brand-nav preserves data-target and handleNavBrandClick
    check("quick-brand-nav giữ nguyên handleNavBrandClick", 'handleNavBrandClick(event, this, \'monster-products\')' in idx_content)

    # 4. Check 12.400+ KHÁCH HÀNG TIN DÙNG is removed
    has_12400 = "12.400+ KHÁCH HÀNG TIN DÙNG" in idx_content or "12.400+" in idx_content
    check("index.html không còn text 12.400+ KHÁCH HÀNG TIN DÙNG", not has_12400)
    has_section_kicker = re.search(r'class="section-kicker"', idx_content) is not None
    check("index.html không còn class section-kicker", not has_section_kicker)

    # 5. Check section-title of testimonials still exists
    has_testimonials_title = "ĐƯỢC TIN DÙNG BỞI GIỚI" in idx_content and "CHUYÊN NGHIỆP" in idx_content
    check("testimonials section-title vẫn được bảo toàn", has_testimonials_title)

print("=" * 75)
print(f"Result: {passed}/{passed + failed} passed")
if failed == 0:
    print("🎉 TẤT CẢ TIÊU CHÍ ĐÃ HOÀN TẤT VÀ VƯỢT QUA KIỂM THỬ XUẤT SẮC!")
    sys.exit(0)
else:
    print(f"⚠️ CÓ {failed} TIÊU CHÍ CHƯA ĐẠT (RED PHASE)!")
    sys.exit(1)
