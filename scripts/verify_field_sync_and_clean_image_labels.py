#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification Script:
1. Clean image labels: Strictly 'Hình 1', 'Hình 2', 'Hình 3', 'Hình 4' in edit-monster.html
   and 'Hình 1', 'Hình 2', 'Hình 3' in other edit pages (no extra text / suffixes).
2. Synchronization between Admin edit page, Product Detail page, and Admin modals:
   - Brand: Monster Energy (Hà Lan / Hoa Kỳ)
   - Origin / Made In: Malaysia (Ủy quyền Monster Energy Company)
   - Flavor: Vị nguyên bản đậm đà, sảng khoái với Taurine & Nhân sâm
   - Ingredients: Full text matching admin
   - Volume: 355ml (Lon nhôm cao cấp)
   - Usage & Storage instructions
   - Storage label: Bảo Quản
   - Edit links pointing to edit-monster.html
"""

import os
import sys
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT_DIR)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

passed_tests = 0
failed_tests = 0

def check(description, condition, details=""):
    global passed_tests, failed_tests
    if condition:
        print(f"✅ PASS: [{description}]")
        passed_tests += 1
    else:
        print(f"❌ FAIL: [{description}] - {details}")
        failed_tests += 1

print("===========================================================================")
print("KIỂM TRA ĐỒNG BỘ THÔNG TIN SẢN PHẨM & CHỈ GIỮ LẠI CHỮ HÌNH 1, 2, 3, 4")
print("===========================================================================\n")

# 1. Check admin/edit-monster.html image labels
edit_monster_path = 'admin/edit-monster.html'
check("admin/edit-monster.html exists", os.path.exists(edit_monster_path))
monster_content = open(edit_monster_path, encoding='utf-8').read()

# Verify strictly Hình 1, Hình 2, Hình 3, Hình 4
check(
    "edit-monster.html: Hình 1 label strictly 'Hình 1'",
    '<label class="admin-form-label" for="edit-prod-file">Hình 1</label>' in monster_content
)
check(
    "edit-monster.html: Hình 2 label strictly 'Hình 2'",
    '<label class="admin-form-label" for="edit-prod-file-2">Hình 2</label>' in monster_content
)
check(
    "edit-monster.html: Hình 3 label strictly 'Hình 3'",
    '<label class="admin-form-label" for="edit-prod-file-3">Hình 3</label>' in monster_content
)
check(
    "edit-monster.html: Hình 4 label strictly 'Hình 4'",
    '<label class="admin-form-label" for="edit-prod-file-4">Hình 4</label>' in monster_content
)

# Verify no extra suffixes like (Mặt trước), (Mặt sau 1), etc. inside edit-product-images
img_list_match = re.search(r'id="edit-product-images".*?</div>\s*</div>', monster_content, re.DOTALL)
if img_list_match:
    labels_in_section = re.findall(r'<label[^>]*>(.*?)</label>', img_list_match.group(0))
    clean_labels = all(l.strip() in ['Hình 1', 'Hình 2', 'Hình 3', 'Hình 4'] for l in labels_in_section)
    check("edit-monster.html: No suffixes in image labels", clean_labels, f"Found labels: {labels_in_section}")
else:
    check("edit-monster.html: Found edit-product-images section", False)

check(
    "edit-monster.html: Không còn chữ '(Mặt trước)' trong nhãn ảnh",
    'Hình 1 (Mặt trước)' not in monster_content and 'HÌNH 1 (MẶT TRƯỚC)' not in monster_content
)
check(
    "edit-monster.html: Không còn chữ '(Mặt sau 1)' trong nhãn ảnh",
    'Hình 2 (Mặt sau 1)' not in monster_content
)
check(
    "edit-monster.html: Không còn chữ '(Mặt sau 2)' trong nhãn ảnh",
    'Hình 3 (Mặt sau 2)' not in monster_content
)
check(
    "edit-monster.html: Không còn chữ '(Ly nước đá)' trong nhãn ảnh",
    'Hình 4 (Ly nước đá)' not in monster_content
)

# 2. Check other edit files (Redbull, Sting) for clean image labels
other_edit_files = [
    'admin/edit-redbull-original.html',
    'admin/edit-redbull-lonvua.html',
    'admin/edit-redbull-thai.html',
    'admin/edit-sting.html'
]
for fpath in other_edit_files:
    if os.path.exists(fpath):
        fcontent = open(fpath, encoding='utf-8').read()
        f_list_match = re.search(r'id="edit-product-images".*?</div>\s*</div>', fcontent, re.DOTALL)
        if f_list_match:
            flabels = re.findall(r'<label[^>]*>(.*?)</label>', f_list_match.group(0))
            fclean = all(l.strip() in ['Hình 1', 'Hình 2', 'Hình 3'] for l in flabels)
            check(f"{fpath}: Image labels strictly Hình 1, 2, 3", fclean, f"Labels: {flabels}")

# 3. Check admin/edit-monster.html synchronized field labels & values
check(
    "edit-monster.html: Nhãn 'Sản Xuất Tại *' thay cho 'Nguồn Gốc / Xuất Xứ *'",
    'Sản Xuất Tại <span class="req">*</span>' in monster_content and 'Nguồn Gốc / Xuất Xứ' not in monster_content
)
check(
    "edit-monster.html: Giá trị Sản Xuất Tại là 'Malaysia (Ủy quyền Monster Energy Company)'",
    'value="Malaysia (Ủy quyền Monster Energy Company)"' in monster_content
)
check(
    "edit-monster.html: Nhãn 'Thành Phần *' chuẩn hóa thay cho 'Thành Phần Chi Tiết *'",
    'Thành Phần <span class="req">*</span>' in monster_content and 'Thành Phần Chi Tiết' not in monster_content
)
check(
    "edit-monster.html: Nhãn 'Bảo Quản *' thay cho 'Hướng Dẫn Bảo Quản *'",
    'Bảo Quản <span class="req">*</span>' in monster_content and 'Hướng Dẫn Bảo Quản' not in monster_content
)
check(
    "edit-monster.html: Giá trị Thương Hiệu là 'Monster Energy (Hà Lan / Hoa Kỳ)'",
    'value="Monster Energy (Hà Lan / Hoa Kỳ)"' in monster_content
)
check(
    "edit-monster.html: Card tóm tắt bên trái có Thương hiệu 'Monster Energy (Hà Lan / Hoa Kỳ)'",
    'Monster Energy (Hà Lan / Hoa Kỳ)' in monster_content and '<strong>Thương hiệu:</strong> Monster Energy (Hà Lan / Hoa Kỳ)' in monster_content
)
check(
    "edit-monster.html: Title thuộc tính input chọn hình 1-4 chuẩn hóa",
    all(f'title="Chọn hình {i}"' in monster_content for i in range(1, 5))
)

# 4. Check pages/product-detail.html synchronization
product_detail_path = 'pages/product-detail.html'
check("pages/product-detail.html exists", os.path.exists(product_detail_path))
detail_content = open(product_detail_path, encoding='utf-8').read()

check(
    "product-detail.html: Row Thương hiệu 'Monster Energy (Hà Lan / Hoa Kỳ)'",
    'Monster Energy (Hà Lan / Hoa Kỳ)' in detail_content
)
check(
    "product-detail.html: Row Sản xuất tại 'Malaysia (Ủy quyền Monster Energy Company)'",
    'Malaysia (Ủy quyền Monster Energy Company)' in detail_content
)
check(
    "product-detail.html: Row Hương vị có mặt và màu neon #00FF66",
    'Hương vị' in detail_content and '#00FF66' in detail_content and 'Vị nguyên bản đậm đà, sảng khoái với Taurine & Nhân sâm' in detail_content
)
full_ingredients = 'Nước bão hòa CO2, Sucroza, chiết xuất đường nho, chiết xuất nhân sâm, L-Carnitine, Taurine (400mg/100ml), Caffeine (30mg/100ml), Inositol, Vitamin B3, B6, B2, B12, Maltodextrin, chất điều chỉnh độ acid...'
check(
    "product-detail.html: Row Thành phần hiển thị đầy đủ không bị ngắt quãng",
    full_ingredients in detail_content
)
check(
    "product-detail.html: Row Thể tích '355ml (Lon nhôm cao cấp)'",
    '355ml (Lon nhôm cao cấp)' in detail_content
)
check(
    "product-detail.html: Row Hướng dẫn sử dụng",
    'Lắc nhẹ trước khi uống, dùng ngay sau khi mở nắp. Ngon hơn khi uống lạnh.' in detail_content
)
check(
    "product-detail.html: Row Bảo quản",
    'Để nơi khô ráo, thoáng mát, tránh ánh sáng trực tiếp hoặc nơi có nhiệt độ cao.' in detail_content
)

# 5. Check admin/index.html & admin/inventory.html modal-edit-product
for admin_file in ['admin/index.html', 'admin/inventory.html']:
    acontent = open(admin_file, encoding='utf-8').read()
    check(
        f"{admin_file}: modal có nhãn 'Sản Xuất Tại *'",
        'Sản Xuất Tại <span class="req">*</span>' in acontent
    )
    check(
        f"{admin_file}: modal có trường 'Hương Vị Đặc Trưng'",
        'Hương Vị Đặc Trưng' in acontent and 'edit-prod-flavor' in acontent
    )
    check(
        f"{admin_file}: modal có nhãn 'Bảo Quản'",
        '<label class="admin-form-label">Bảo Quản</label>' in acontent
    )
    check(
        f"{admin_file}: link bảng trỏ về edit-monster.html",
        'href="edit-monster.html"' in acontent
    )
    check(
        f"{admin_file}: modal hiển thị chính xác '2 Quy cách đóng gói'",
        '2 Quy cách đóng gói' in acontent
    )

# 6. Check js/app.js synchronization
app_js_path = 'js/app.js'
check("js/app.js exists", os.path.exists(app_js_path))
js_content = open(app_js_path, encoding='utf-8').read()

check(
    "js/app.js: PRODUCT_DATA_REGISTRY monster-original brand updated",
    "'Monster Energy (Hà Lan / Hoa Kỳ)'" in js_content
)
check(
    "js/app.js: PRODUCT_DATA_REGISTRY monster-original origin updated",
    "'Malaysia (Ủy quyền Monster Energy Company)'" in js_content
)
check(
    "js/app.js: PRODUCT_DATA_REGISTRY monster-original flavor added",
    "'Vị nguyên bản đậm đà, sảng khoái với Taurine & Nhân sâm'" in js_content
)
check(
    "js/app.js: PRODUCT_DATA_REGISTRY monster-original volume updated",
    "'355ml (Lon nhôm cao cấp)'" in js_content
)
check(
    "js/app.js: PRODUCT_DATA_REGISTRY monster-original ingredients full text",
    full_ingredients in js_content
)
check(
    "js/app.js: openProductEditModal populates edit-prod-flavor",
    "edit-prod-flavor" in js_content
)

print(f"\n===========================================================================")
print(f"KẾT QUẢ KIỂM THỬ: {passed_tests}/{passed_tests + failed_tests} TIÊU CHÍ ĐẠT")
print("===========================================================================")

if failed_tests == 0:
    print("🎉 TẤT CẢ TIÊU CHÍ ĐỀU VƯỢT QUA 100%!")
    sys.exit(0)
else:
    print(f"❌ CÒN {failed_tests} LỖI CẦN KHẮC PHỤC.")
    sys.exit(1)
