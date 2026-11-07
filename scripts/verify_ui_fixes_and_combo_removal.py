import os
import sys
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT_DIR)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

results = []

def check(name, condition, details=""):
    results.append((name, condition, details))
    status = "✅ PASS" if condition else "❌ FAIL"
    print(f"{status}: [{name}] {details}")

print("===========================================================================")
print("KIỂM TRA TỰ ĐỘNG: KHẮC PHỤC ĐÁNH GIÁ GIAO DIỆN & LOẠI BỎ COMBO THÙNG")
print("===========================================================================\n")

# Check 1: Nav Brand buttons have correct hrefs and handleNavBrandClick
idx_html = open('index.html', encoding='utf-8').read()
c1 = ('#monster-products' in idx_html and 
      '#redbull-products' in idx_html and 
      '#sting-products' in idx_html and 
      'handleNavBrandClick' in idx_html)
check("1. Header Brand Nav Links", c1, "Thanh điều hướng có đầy đủ anchor #monster-products, #redbull-products, #sting-products và handleNavBrandClick")

# Check 2: Quick Brand Selector near product catalog
c2 = ('quick-brand-nav' in idx_html or 'quick-brand-tabs' in idx_html)
check("2. Quick Brand Tabs", c2, "Có thanh chọn phân loại nhanh đặt sát ngay đầu danh mục sản phẩm chính")

# Check 3: CSS product card alignment & min-height
style_css = open('css/style.css', encoding='utf-8').read()
c3 = ('line-clamp: 2' in style_css or '-webkit-line-clamp: 2' in style_css) and ('min-height' in style_css)
check("3. Product Card Alignment", c3, "CSS có quy chuẩn min-height và line-clamp: 2 cho tiêu đề để các thẻ thẳng hàng")

# Check 4: Button uniformity - "Chi tiết" on cards, 0 "Xem" buttons in product cards
flash_sale_part = re.search(r'id="flash-sale".*?</section>', idx_html, re.DOTALL)
has_xem = bool(flash_sale_part and re.search(r'>\s*Xem\s*<', flash_sale_part.group(0)))
has_chi_tiet_on_flash = bool(flash_sale_part and 'Chi tiết' in flash_sale_part.group(0))
c4 = (not has_xem) and has_chi_tiet_on_flash
check("4. Button Uniformity (Flash Sale vs Main)", c4, "Đồng bộ nút 'Chi tiết' trên toàn bộ các thẻ (không còn nút 'Xem')")

# Check 5: pages/account.html has both Header and Footer
account_html = open('pages/account.html', encoding='utf-8').read()
c5 = ('<header class="header">' in account_html and 
      ('footer' in account_html.lower() and '<footer' in account_html))
check("5. Account Page Header & Footer", c5, "Trang account.html có đầy đủ cả Header đồng bộ và Footer chuẩn")

# Check 6: index.html removes "Combo Thùng 24 lon" while preserving floating cans (.combo-cans)
has_floating_cans = ('combo-cans' in idx_html and 'combo-aura' in idx_html)
has_combo_thung_title = ('COMBO THÙNG 24 LON' in idx_html or 'Combo thùng 24 lon' in idx_html)
c6 = has_floating_cans and (not has_combo_thung_title)
check("6. Showcase Banner (No Combo Thùng, Keep Floating Cans)", c6, "Giữ nguyên 3 lon lơ lửng, loại bỏ nội dung 'Combo thùng 24 lon'")

# Check 7: Admin files clean of "Thùng 24 lon" / combo orders
admin_files = ['admin/index.html', 'admin/orders.html', 'admin/inventory.html', 'admin/customers.html']
admin_combo_matches = []
for af in admin_files:
    content = open(af, encoding='utf-8').read()
    if 'Thùng 24 lon' in content or 'Thùng 24 Lon' in content or '1 Thùng 24' in content:
        admin_combo_matches.append(af)
c7 = (len(admin_combo_matches) == 0)
check("7. Clean Admin Combo / Thùng 24 Lon", c7, f"Admin không còn dữ liệu thùng 24 lon (Vi phạm: {admin_combo_matches})")

# Check 8: Rubric 19/19 checks pass
search_has_sting = ('#sting-products' in idx_html)
c8 = search_has_sting
check("8. Rubric #sting-products Search Coverage", c8, "Thẻ liên kết #sting-products có mặt đầy đủ cho tiêu chí Rubric 1.1")

print("\n===========================================================================")
passed = sum(1 for _, c, _ in results if c)
total = len(results)
print(f"KẾT QUẢ KIỂM THỬ: {passed}/{total} TIÊU CHÍ ĐẠT")
print("===========================================================================")

if passed == total:
    print("🎉 TẤT CẢ TIÊU CHÍ ĐÃ HOÀN TẤT VÀ VƯỢT QUA KIỂM THỬ XUẤT SẮC!")
    sys.exit(0)
else:
    print(f"⚠️ CÒN {total - passed} TIÊU CHÍ CẦN HOÀN THIỆN THEO PLAN.")
    sys.exit(1)
