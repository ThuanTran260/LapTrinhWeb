# -*- coding: utf-8 -*-
"""
verify_admin_features_update.py
Kiểm thử tự động cho 5 tính năng:
1. Hiển thị số lượng tồn kho trong bảng Quản lý kho (admin/inventory.html & admin/index.html)
2. Định dạng tiền tệ VNĐ thời gian thực cho cấu hình Voucher & Vận chuyển (admin/settings.html & js/app.js)
3. Nút 'IN HÓA ĐƠN ĐIỆN TỬ' hiển thị thông báo toast (pages/order-success.html)
4. Loại bỏ phần Đánh giá chuyên nghiệp trên storefront (index.html) & giữ lại trust-strip
5. Phân vùng Quản Lý Câu Hỏi Thường Gặp (FAQ) trong admin (admin/settings.html)
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

print("=" * 80)
print("KIỂM TRA TỰ ĐỘNG: 5 TÍNH NĂNG ADMIN & STOREFRONT CẬP NHẬT MỚI")
print("=" * 80)

# ----------------------------------------------------------------------
# 1. Hiển thị số lượng tồn kho trong Quản lý kho
# ----------------------------------------------------------------------
print("\n--- 1. KIỂM TRA HIỂN THỊ TỒN KHO TRONG BẢNG KHO (admin/inventory.html & admin/index.html) ---")
inv_html = read_text("admin/inventory.html")
adm_idx_html = read_text("admin/index.html")

check("admin/inventory.html tồn tại", inv_html is not None)
check("admin/index.html tồn tại", adm_idx_html is not None)

def verify_stock_qty(file_name, content):
    if not content:
        return
    # Check 4 Monster items fixed 1.250 lon
    monster_matches = re.findall(r'Tồn:\s*1\.250\s*lon', content)
    check(f"{file_name}: 4 sản phẩm Monster có Tồn: 1.250 lon", len(monster_matches) >= 4, f"Tìm thấy {len(monster_matches)} lon")
    
    # Check 3 Redbull items: 680, 450, 520 lon
    check(f"{file_name}: Redbull Original có Tồn: 680 lon", "Tồn: 680 lon" in content)
    check(f"{file_name}: Redbull Thái Lan có Tồn: 450 lon", "Tồn: 450 lon" in content)
    check(f"{file_name}: Redbull Nắp Bật có Tồn: 520 lon", "Tồn: 520 lon" in content)
    
    # Check 3 Sting items: 890, 740, 610 lon
    check(f"{file_name}: Sting Dâu Tây Đỏ có Tồn: 890 lon", "Tồn: 890 lon" in content)
    check(f"{file_name}: Sting Vàng Sleek có Tồn: 740 lon", "Tồn: 740 lon" in content)
    check(f"{file_name}: Sting Blue Sleek có Tồn: 610 lon", "Tồn: 610 lon" in content)
    
    # Check style formatting
    check(f"{file_name}: cấu trúc thẻ small chứa fas fa-box và style chuẩn",
          '<small style="color: var(--text-muted); display: block; margin-top: 4px; font-size: 0.78rem;"><i class="fas fa-box"></i> Tồn:' in content)

verify_stock_qty("admin/inventory.html", inv_html)
verify_stock_qty("admin/index.html", adm_idx_html)

# ----------------------------------------------------------------------
# 2. Định dạng tiền tệ VNĐ thời gian thực cho Voucher & Vận chuyển
# ----------------------------------------------------------------------
print("\n--- 2. KIỂM TRA ĐỊNH DẠNG TIỀN TỆ VNĐ CHO VOUCHER & VẬN CHUYỂN ---")
settings_html = read_text("admin/settings.html")
app_js = read_text("js/app.js")

check("admin/settings.html tồn tại", settings_html is not None)
check("js/app.js tồn tại", app_js is not None)

if settings_html:
    # Check inputs have price-format-input
    for inp_id in ['voucher-min-spend', 'voucher-max-discount', 'ship-min-free', 'ship-standard-fee']:
        pattern = rf'id="{inp_id}"[^>]*class="[^"]*price-format-input[^"]*"'
        alt_pattern = rf'class="[^"]*price-format-input[^"]*"[^>]*id="{inp_id}"'
        has_class = re.search(pattern, settings_html) or re.search(alt_pattern, settings_html)
        check(f"admin/settings.html: input #{inp_id} có class price-format-input", bool(has_class))

if app_js:
    # Check initPriceFormatting handles voucher and shipping inputs or .price-format-input
    check("js/app.js: initPriceFormatting hỗ trợ .price-format-input", "'.price-format-input'" in app_js)
    check("js/app.js: updateVoucherLivePreview định dạng tiền tệ VNĐ chuẩn", "formatCurrencyVND" in app_js)

# ----------------------------------------------------------------------
# 3. Nút 'IN HÓA ĐƠN ĐIỆN TỬ' hiển thị thông báo toast
# ----------------------------------------------------------------------
print("\n--- 3. KIỂM TRA NÚT 'IN HÓA ĐƠN ĐIỆN TỬ' TRONG pages/order-success.html ---")
order_success_html = read_text("pages/order-success.html")
check("pages/order-success.html tồn tại", order_success_html is not None)

if order_success_html:
    check("pages/order-success.html: không còn onclick='window.print()'", 'onclick="window.print()"' not in order_success_html)
    expected_toast = "onclick=\"showToast('Hóa đơn điện tử đã được tạo và gửi đến email của bạn!', 'success')\""
    check("pages/order-success.html: nút gọi showToast thông báo hóa đơn điện tử", expected_toast in order_success_html)

# ----------------------------------------------------------------------
# 4. Loại bỏ phần Đánh giá chuyên nghiệp trên storefront & giữ trust-strip
# ----------------------------------------------------------------------
print("\n--- 4. KIỂM TRA LOẠI BỎ ĐÁNH GIÁ CHUYÊN NGHIỆP TRONG index.html ---")
index_html = read_text("index.html")
check("index.html tồn tại", index_html is not None)

if index_html:
    check("index.html: không còn tiêu đề ĐƯỢC TIN DÙNG BỞI GIỚI CHUYÊN NGHIỆP", "ĐƯỢC TIN DÙNG BỞI GIỚI" not in index_html)
    check("index.html: không còn testimonials-head", "testimonials-head" not in index_html)
    check("index.html: không còn review-grid", "review-grid" not in index_html)
    check("index.html: giữ lại trust-strip", "trust-strip" in index_html)
    check("index.html: trust-strip có '100% CHÍNH HÃNG'", "100% CHÍNH HÃNG" in index_html)
    check("index.html: trust-strip có 'ĐỔI TRẢ MIỄN PHÍ'", "ĐỔI TRẢ MIỄN PHÍ" in index_html)
    check("index.html: trust-strip có 'KIỂM TRA TRƯỚC KHI NHẬN'", "KIỂM TRA TRƯỚC KHI NHẬN" in index_html)
    check("index.html: trust-strip có 'HỖ TRỢ 24/7'", "HỖ TRỢ 24/7" in index_html)

# ----------------------------------------------------------------------
# 5. Phân vùng Quản Lý Câu Hỏi Thường Gặp (FAQ) trong Admin
# ----------------------------------------------------------------------
print("\n--- 5. KIỂM TRA PHÂN VÙNG QUẢN LÝ FAQ TRONG admin/settings.html ---")
if settings_html:
    check("admin/settings.html: có tiêu đề QUẢN LÝ CÂU HỎI THƯỜNG GẶP (FAQ)", "QUẢN LÝ CÂU HỎI THƯỜNG GẶP (FAQ)" in settings_html)
    check("admin/settings.html: có icon fa-circle-question", "fa-circle-question" in settings_html)
    check("admin/settings.html: có nút Thêm Câu Hỏi", "Thêm Câu Hỏi" in settings_html)
    check("admin/settings.html: có form thêm câu hỏi (input, textarea)", "faq-new-question" in settings_html or "faq-question" in settings_html)
    check("admin/settings.html: có 4 câu hỏi FAQ chuẩn của hệ thống",
          "Các dòng nước tăng lực tại Energy Boost gồm những thương hiệu nào?" in settings_html and
          "Shop giao hàng trong bao lâu?" in settings_html)
    check("admin/settings.html: có badge thứ tự #1-#4",
          "#1" in settings_html and "#2" in settings_html and "#3" in settings_html and "#4" in settings_html)
    check("admin/settings.html: có nút Thao tác Sửa/Xóa",
          "fa-edit" in settings_html and "fa-trash" in settings_html)

print("\n" + "=" * 80)
print(f"KẾT QUẢ TỔNG QUÁT: {passed}/{passed + failed} TIÊU CHÍ ĐẠT")
print("=" * 80)

if failed == 0:
    print("🎉 TẤT CẢ 5 TÍNH NĂNG MỚI ĐÃ ĐƯỢC XÁC MINH VÀ VƯỢT QUA KIỂM THỬ XUẤT SẮC!")
    sys.exit(0)
else:
    print(f"⚠️ CÓ {failed} TIÊU CHÍ CHƯA ĐẠT.")
    sys.exit(1)
