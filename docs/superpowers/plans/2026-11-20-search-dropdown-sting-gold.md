# Plan: Đổi 1 Lon Sting Đỏ Trùng Trong Dropdown Tìm Kiếm Thành Sting Vàng

- **Branch:** `main`
- **Issue:** Các dropdown gợi ý tìm kiếm (`SẢN PHẨM TÌM KIẾM PHỔ BIẾN — 5 sản phẩm hot`) ở `index.html` (Header & Sidebar `BỘ LỌC TÌM KIẾM`), `pages/search-results.html` (Header & Sidebar), và `pages/account.html` (Header) hiện có 2 mục `Sting Dâu Tây Đỏ` (`sting-dau.webp`) tại Item 3 và Item 5.
- **Fix:** Đổi Item 5 trong cả 5 vị trí trên sang `Nước Tăng Lực Sting Vàng Sleek 330ml` (`sting-gold.webp`, `12.000đ`, `Sting PepsiCo`, link `product-detail-sting.html`), giữ nguyên Item 3 là `Sting Dâu Tây Đỏ 330ml`.

## Global Constraints
1. **Canonical Product Metadata (khớp `index.html` & `STATIC_PRODUCTS_CATALOG`):**
   - Title: `Nước Tăng Lực Sting Vàng Sleek 330ml`
   - Image: `assets/images/sting/sting-gold.webp` (ở `index.html`) / `../assets/images/sting/sting-gold.webp` (ở `pages/*.html`)
   - Alt: `Sting Vàng Sleek`
   - Brand badge: `<span class="brand-badge sting">Sting PepsiCo</span>`
   - Price: `12.000đ`
   - Link & click handler: giữ nguyên `pages/product-detail-sting.html` (`index.html`) / `product-detail-sting.html` (`pages/*.html`) và `onclick="closeSearchDropdown()"` (Header) hoặc `onclick="closeSidebarSearchDropdown()"` (Sidebar).
2. **Scope Strictness:** Không sửa các dropdown ở `cart.html`, `orders.html`, `order-detail.html`, `product-detail*.html` (nơi chỉ có 1 Sting Đỏ và không bị trùng). Không sửa logic filter/search khác hay làm gãy `verify_implementation.py`, `verify_footer_sync.py`, `verify_search_placeholder_polish.py`.

## Tasks
- **Task 1 (`index.html`):** Cập nhật Item 5 trong `#search-dropdown-menu` và `#sidebar-search-dropdown-menu` thành `Nước Tăng Lực Sting Vàng Sleek 330ml` (`assets/images/sting/sting-gold.webp`).
- **Task 2 (`pages/search-results.html`, `pages/account.html`):** Cập nhật Item 5 trong Header & Sidebar dropdown của `pages/search-results.html` và Header dropdown của `pages/account.html` thành `Nước Tăng Lực Sting Vàng Sleek 330ml` (`../assets/images/sting/sting-gold.webp`).
- **Task 3 (`scripts/verify_sidebar_filter_sync.py`, `scripts/verify_search_dropdown_sting_gold.py`):** Cập nhật check #3 trong `verify_sidebar_filter_sync.py` kiểm tra rõ cả `Sting Dâu` và `Sting Vàng Sleek 330ml`, và tạo `scripts/verify_search_dropdown_sting_gold.py` kiểm tra toàn bộ `.search-static-list` không còn trùng `sting-dau.webp` và 5 dropdown mục tiêu hiển thị đúng `sting-gold.webp`.
