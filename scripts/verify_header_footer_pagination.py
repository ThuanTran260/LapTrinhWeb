# -*- coding: utf-8 -*-
"""
verify_header_footer_pagination.py
Xác minh toàn diện 4 hạng mục:
1. Thống nhất Header cho pages/orders.html và pages/order-detail.html
2. Phân trang linh hoạt < 1 2 3 > trong index.html và js/app.js
3. Cuộn mượt khi click thương hiệu (Monster, Redbull, Sting) và scroll-margin-top
4. Căn lề chân thẻ sản phẩm (GIÁ CHÍNH HÃNG, baseline alignment, btn-add-stitch glassmorphism)
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

tests = []

def test(name):
    def decorator(fn):
        tests.append((name, fn))
        return fn
    return decorator

# --- Group 1: Header Uniformity ---
@test("1.1 pages/orders.html có đầy đủ header chuẩn (Logo, Search box, 3 Action Buttons)")
def test_orders_header():
    c = read_text("pages/orders.html")
    assert c is not None, "File pages/orders.html không tồn tại!"
    assert "header-main" in c, "Thiếu .header-main trong orders.html"
    assert "search-box" in c, "Thiếu thanh search-box trong orders.html"
    assert "search-dropdown-menu" in c, "Thiếu #search-dropdown-menu trong orders.html"
    assert "modal-adv-search" in c, "Thiếu modal tìm kiếm nâng cao #modal-adv-search trong orders.html"
    assert "header-actions" in c, "Thiếu .header-actions trong orders.html"
    assert "orders.html" in c, "Thiếu nút orders.html trong header actions"
    assert "account.html" in c, "Thiếu nút account.html trong header actions"
    assert "cart.html" in c, "Thiếu nút cart.html trong header actions"
    assert "header-account-link" in c, "Thiếu #header-account-link trong header actions"
    assert "[ACTIVE]" not in c, "Chữ '[ACTIVE]' không được xuất hiện dưới dạng text hiển thị!"

@test("1.2 pages/order-detail.html có đầy đủ header chuẩn và modal tìm kiếm nâng cao")
def test_order_detail_header():
    c = read_text("pages/order-detail.html")
    assert c is not None, "File pages/order-detail.html không tồn tại!"
    assert "search-box" in c, "Thiếu thanh search-box trong order-detail.html"
    assert "search-dropdown-menu" in c, "Thiếu #search-dropdown-menu trong order-detail.html"
    assert "modal-adv-search" in c, "Thiếu #modal-adv-search trong order-detail.html"
    assert "header-account-link" in c, "Thiếu #header-account-link trong order-detail.html"
    assert "[ACTIVE]" not in c, "Chữ '[ACTIVE]' không được xuất hiện dưới dạng text hiển thị!"

# --- Group 2: Smart Pagination ---
@test("2.1 index.html: Phân trang không còn kẹt ở trang 3, mặc định active trang 1")
def test_index_pagination_markup():
    c = read_text("index.html")
    assert c is not None, "File index.html không tồn tại!"
    assert 'id="catalog-pagination"' in c or 'class="pagination-strip"' in c, "Thiếu markup pagination trong index.html"
    assert 'changeDashboardPage(1, event)' in c, "Nút trang 1 phải gọi changeDashboardPage(1, event)"
    assert 'changeDashboardPage(2, event)' in c, "Nút trang 2 phải gọi changeDashboardPage(2, event)"
    assert 'changeDashboardPage(3, event)' in c, "Nút trang 3 phải gọi changeDashboardPage(3, event)"
    # Trang 1 active, nút < ban đầu disabled
    assert 'data-page="1"' in c, "Nút trang 1 phải có attribute data-page='1'"
    assert 'data-page="2"' in c, "Nút trang 2 phải có attribute data-page='2'"
    assert 'data-page="3"' in c, "Nút trang 3 phải có attribute data-page='3'"
    assert 'page-btn active" data-page="1"' in c or 'data-page="1" class="page-btn active"' in c or 'class="page-btn active" data-page="1"' in c, "Trang 1 phải active mặc định"
    assert 'page-btn page-btn-prev disabled' in c or 'disabled" id="page-btn-prev"' in c, "Nút Prev < phải disabled ban đầu"

@test("2.2 js/app.js: Có hàm changeDashboardPage và updatePaginationUI xử lý logic chuyển trang")
def test_app_js_pagination_logic():
    c = read_text("js/app.js")
    assert c is not None, "File js/app.js không tồn tại!"
    assert "function changeDashboardPage" in c, "Thiếu hàm changeDashboardPage trong js/app.js"
    assert "function updatePaginationUI" in c, "Thiếu hàm updatePaginationUI trong js/app.js"
    assert "window.changeDashboardPage" in c, "changeDashboardPage phải được export ra window"
    assert "currentDashboardPage" in c, "Thiếu biến currentDashboardPage trong js/app.js"
    assert "monster-products" in c and "redbull-products" in c and "sting-products" in c, "Thiếu ánh xạ brand tương ứng với các trang"

# --- Group 3: Brand Navigation & Smooth Scroll ---
@test("3.1 index.html & js/app.js: Navbar Monster, Redbull, Sting kích hoạt cuộn mượt")
def test_brand_navigation_scroll():
    c_index = read_text("index.html")
    c_js = read_text("js/app.js")
    assert "handleNavBrandClick(event, this, 'monster-products')" in c_index, "Nút Monster trên navbar phải gọi handleNavBrandClick với target monster-products"
    assert "handleNavBrandClick(event, this, 'redbull-products')" in c_index, "Nút Redbull trên navbar phải gọi handleNavBrandClick với target redbull-products"
    assert "handleNavBrandClick(event, this, 'sting-products')" in c_index, "Nút Sting trên navbar phải gọi handleNavBrandClick với target sting-products"
    assert "scrollIntoView" in c_js, "Hàm handleNavBrandClick phải gọi scrollIntoView để cuộn trang"
    assert "window.handleNavBrandClick" in c_js, "handleNavBrandClick phải được export ra window"

@test("3.2 css/style.css: Có scroll-margin-top: 100px để không bị sticky header che khuất")
def test_scroll_margin_css():
    c = read_text("css/style.css")
    assert c is not None, "File css/style.css không tồn tại!"
    assert "scroll-margin-top" in c, "Thiếu scroll-margin-top trong css/style.css"
    assert "#monster-products" in c, "Thiếu #monster-products trong css/style.css"
    assert "#redbull-products" in c, "Thiếu #redbull-products trong css/style.css"
    assert "#sting-products" in c, "Thiếu #sting-products trong css/style.css"

# --- Group 4: Card Footer & Alignment ---
@test("4.1 css/style.css: .product-bottom căn lề flex-end, .btn-add-stitch hiệu ứng glassmorphism")
def test_card_footer_css():
    c = read_text("css/style.css")
    assert ".product-bottom" in c, "Thiếu .product-bottom trong css/style.css"
    assert "align-items: flex-end" in c, ".product-bottom phải căn lề align-items: flex-end"
    assert ".price-label" in c, "Thiếu class .price-label trong css/style.css"
    assert ".btn-add-stitch" in c, "Thiếu class .btn-add-stitch trong css/style.css"
    assert "width: 40px" in c and "height: 40px" in c, ".btn-add-stitch phải có kích thước 40x40px"

@test("4.2 index.html: Tất cả thẻ sản phẩm có nhãn phụ GIÁ CHÍNH HÃNG")
def test_product_card_price_label():
    c = read_text("index.html")
    count_label = c.count("GIÁ CHÍNH HÃNG")
    assert count_label >= 14, f"Cần ít nhất 14 nhãn GIÁ CHÍNH HÃNG trong index.html, hiện tại có {count_label}"

def main():
    print("=" * 75)
    print("KIỂM TRA TỰ ĐỘNG: HEADER, PHÂN TRANG, CUỘN HÃNG & CĂN LỀ CHÂN THẺ SẢN PHẨM")
    print("=" * 75)
    passed = 0
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"✅ PASS: [{name}]")
            passed += 1
        except AssertionError as e:
            print(f"❌ FAIL: [{name}] -> {e}")
            failed += 1
        except Exception as e:
            print(f"💥 ERROR: [{name}] -> {type(e).__name__}: {e}")
            failed += 1

    print("=" * 75)
    print(f"KẾT QUẢ: {passed}/{len(tests)} TIÊU CHÍ ĐẠT")
    print("=" * 75)
    if failed == 0:
        print("🎉 TẤT CẢ TIÊU CHÍ ĐÃ HOÀN TẤT VÀ VƯỢT QUA KIỂM THỬ XUẤT SẮC!")
        return 0
    else:
        print(f"⚠️ CÒN {failed} TIÊU CHÍ CHƯA ĐẠT, VUI LÒNG KIỂM TRA LẠI!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
