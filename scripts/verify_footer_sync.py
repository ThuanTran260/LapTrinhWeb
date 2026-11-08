# -*- coding: utf-8 -*-
"""
verify_footer_sync.py
Xac minh dong bo Footer 4 cot tren toan bo 24 trang Dashboard & Storefront.

Phạm vi (24 file, không bao gồm trang đăng nhập standalone):
- 12 trang khách hàng `pages/*.html`
- 12 trang quản trị `admin/*.html`

Mỗi file được kiểm tra 6 tiêu chí (tổng 144 checks):
1. `<footer class="footer">` tồn tại
2. `.footer-grid` nằm BÊN TRONG khối `<footer class="footer">...</footer>`
3. Ba tiêu đề `CÁC DÒNG SẢN PHẨM`, `HỆ THỐNG TRANG`, `NHẬN VOUCHER ƯU ĐÃI` nằm trong footer
4. `.footer-bottom` nằm trong footer
5. Form voucher có newsletter `showToast('Đã đăng ký nhận tin Energy Boost thành công!'`
6. Không còn footer 1 dòng rút gọn (`container footer-bottom` không có `.footer-grid`)
"""

import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

PAGES_FILES = [
    "pages/account.html",
    "pages/cart.html",
    "pages/orders.html",
    "pages/order-detail.html",
    "pages/order-success.html",
    "pages/payment-gateway.html",
    "pages/product-detail.html",
    "pages/product-detail-redbull.html",
    "pages/product-detail-redbull-thai.html",
    "pages/product-detail-redbull-lonvua.html",
    "pages/product-detail-sting.html",
    "pages/search-results.html",
]

ADMIN_FILES = [
    "admin/index.html",
    "admin/orders.html",
    "admin/inventory.html",
    "admin/revenue.html",
    "admin/customers.html",
    "admin/settings.html",
    "admin/order-detail.html",
    "admin/edit-monster.html",
    "admin/edit-redbull-lonvua.html",
    "admin/edit-redbull-original.html",
    "admin/edit-redbull-thai.html",
    "admin/edit-sting.html",
]

ALL_FILES = PAGES_FILES + ADMIN_FILES

HEADING_PRODUCTS = "CÁC DÒNG SẢN PHẨM"
HEADING_SYSTEM = "HỆ THỐNG TRANG"
HEADING_VOUCHER = "NHẬN VOUCHER ƯU ĐÃI"
NEWSLETTER_TOAST = "showToast('Đã đăng ký nhận tin Energy Boost thành công!'"


def read_text(rel_path):
    abs_path = os.path.join(ROOT_DIR, rel_path)
    if not os.path.exists(abs_path):
        return None
    with open(abs_path, "r", encoding="utf-8") as f:
        return f.read()


def extract_footer_block(content):
    """Trích xuất khối <footer class="footer">...</footer> đầu tiên (nếu có)."""
    if content is None:
        return None
    match = re.search(r'<footer class="footer">.*?</footer>', content, re.DOTALL)
    if match:
        return match.group(0)
    return None


def check(name, condition, reason=""):
    """Hàm kiểm tra chung: in kết quả và trả True/False."""
    if condition:
        print(f"✅ PASS: [{name}]")
        return True
    else:
        if reason:
            print(f"❌ FAIL: [{name}] -> {reason}")
        else:
            print(f"❌ FAIL: [{name}]")
        return False


def verify_file(rel_path):
    """Chạy 6 checks cho một file; trả về (passed, failed)."""
    content = read_text(rel_path)
    passed = 0
    failed = 0

    if content is None:
        for label in (
            "<footer class=\"footer\"> present",
            ".footer-grid inside <footer class=\"footer\">",
            "3 headings inside footer",
            ".footer-bottom inside footer",
            "newsletter showToast voucher inside footer",
            "no 1-line footer (container footer-bottom without grid)",
        ):
            ok = check(f"{rel_path}: {label}", False, f"File {rel_path} không tồn tại!")
            if ok:
                passed += 1
            else:
                failed += 1
        return passed, failed

    footer_block = extract_footer_block(content)

    # 1. <footer class="footer"> present
    cond1 = '<footer class="footer">' in content
    ok = check(
        f"{rel_path}: <footer class=\"footer\"> present",
        cond1,
        f"Không tìm thấy thẻ <footer class=\"footer\"> trong {rel_path} (footer có thể đang thiếu hoặc 1 dòng rút gọn).",
    )
    passed += 1 if ok else 0
    failed += 0 if ok else 1

    # 2. .footer-grid inside footer block
    cond2 = footer_block is not None and "footer-grid" in footer_block
    ok = check(
        f"{rel_path}: .footer-grid inside <footer class=\"footer\">",
        cond2,
        f"Không tìm thấy .footer-grid nằm BÊN TRONG <footer class=\"footer\">...</footer> trong {rel_path}.",
    )
    passed += 1 if ok else 0
    failed += 0 if ok else 1

    # 3. 3 headings inside footer
    headings = [HEADING_PRODUCTS, HEADING_SYSTEM, HEADING_VOUCHER]
    if footer_block is None:
        cond3 = False
        reason3 = "Không có khối <footer> để chứa 3 tiêu đề."
    else:
        missing = [h for h in headings if h not in footer_block]
        cond3 = len(missing) == 0
        reason3 = f"Thiếu tiêu đề trong footer: {', '.join(missing)}" if missing else ""
    ok = check(
        f"{rel_path}: 3 headings (CÁC DÒNG SẢN PHẨM / HỆ THỐNG TRANG / NHẬN VOUCHER ƯU ĐÃI) inside footer",
        cond3,
        reason3,
    )
    passed += 1 if ok else 0
    failed += 0 if ok else 1

    # 4. .footer-bottom inside footer
    cond4 = footer_block is not None and "footer-bottom" in footer_block
    ok = check(
        f"{rel_path}: .footer-bottom inside footer",
        cond4,
        f"Không tìm thấy .footer-bottom nằm BÊN TRONG <footer class=\"footer\">...</footer> trong {rel_path}.",
    )
    passed += 1 if ok else 0
    failed += 0 if ok else 1

    # 5. Newsletter showToast voucher inside footer
    if footer_block is None:
        cond5 = False
        reason5 = "Không có khối <footer> để chứa form voucher."
    else:
        missing5 = []
        if "newsletter-form" not in footer_block:
            missing5.append("newsletter-form")
        if NEWSLETTER_TOAST not in footer_block:
            missing5.append(NEWSLETTER_TOAST)
        cond5 = len(missing5) == 0
        reason5 = f"Thiếu trong footer: {', '.join(missing5)}" if missing5 else ""
    ok = check(
        f"{rel_path}: newsletter showToast voucher inside footer",
        cond5,
        reason5,
    )
    passed += 1 if ok else 0
    failed += 0 if ok else 1

    # 6. No 1-line footer
    if footer_block is None:
        cond6 = False
        reason6 = "Không có khối <footer> nên không thể khẳng định đã bỏ footer 1 dòng."
    else:
        has_one_line = "container footer-bottom" in footer_block
        has_grid = "footer-grid" in footer_block
        cond6 = (not has_one_line) and has_grid
        if has_one_line and not has_grid:
            reason6 = "Footer vẫn là dạng 1 dòng: <div class=\"container footer-bottom\"> mà không có .footer-grid bên trong."
        elif has_one_line:
            reason6 = "Footer còn chứa marker 1 dòng <div class=\"container footer-bottom\">."
        elif not has_grid:
            reason6 = "Footer thiếu .footer-grid (có thể là footer rút gọn)."
        else:
            reason6 = ""
    ok = check(
        f"{rel_path}: no 1-line footer (container footer-bottom without grid)",
        cond6,
        reason6,
    )
    passed += 1 if ok else 0
    failed += 0 if ok else 1

    return passed, failed


def main():
    print("=" * 75)
    print("KIỂM TRA TỰ ĐỘNG: ĐỒNG BỘ FOOTER 4 CỘT — 24 TRANG (12 pages + 12 admin)")
    print("=" * 75)
    total_passed = 0
    total_failed = 0
    files_total = len(ALL_FILES)
    print(f"Phạm vi: {files_total} file (pages/login.html và admin/login.html bị loại trừ)")
    for rel_path in ALL_FILES:
        p, f = verify_file(rel_path)
        total_passed += p
        total_failed += f
    total = total_passed + total_failed
    print("=" * 75)
    print(f"Result: {total_passed}/{total} passed")
    print(f"KẾT QUẢ: {total_passed}/{total} TIÊU CHÍ ĐẠT")
    print("=" * 75)
    if total_failed == 0:
        print("🎉 TẤT CẢ FOOTER ĐÃ ĐỒNG BỘ 4 CỘT!")
        return 0
    else:
        print(f"⚠️ CÒN {total_failed} TIÊU CHÍ CHƯA ĐẠT, VUI LÒNG KIỂM TRA LẠI!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
