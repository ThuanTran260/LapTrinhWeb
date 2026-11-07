# Plan: Thống Nhất Header, Phân Trang 1-2-3, Cuộn Hãng & Căn Lề Chân Thẻ Sản Phẩm

**Spec:** `docs/superpowers/specs/2026-11-07-header-footer-pagination-brandnav-spec.md`

## Global Constraints
- Preserve all existing tests in `verify_implementation.py` (66 checks) and `scripts/verify_price_formatting.py` (49 checks).
- Strictly adhere to Git rule: NO `git push` under any circumstances. Local commits only.
- Preserve responsive layout (desktop & mobile).

---

### Task 1: Thống Nhất Header cho `pages/orders.html` & `pages/order-detail.html`
- **Files:** `pages/orders.html`, `pages/order-detail.html`
- **Details:**
  - Thay thế header giản lược bằng header chuẩn hoàn chỉnh giống `pages/cart.html` và `pages/account.html`.
  - Giữ lại top-bar thông báo.
  - Cụm hành động bên phải gồm 3 nút:
    - Nút 1: `Đơn hàng` (Lịch sử) - nhãn chuẩn, icon `fa-receipt`, không có chữ `[ACTIVE]`.
    - Nút 2: `Tài khoản` (Thành viên).
    - Nút 3: `Giỏ hàng` (7 lon / 216.000đ).
  - Tích hợp search box với `#search-dropdown-menu` và modal `#modal-adv-search`.

---

### Task 2: Chuyển Phân Trang Thông Minh `< 1 2 3 >` ở Đáy Danh Mục
- **Files:** `index.html`, `js/app.js`
- **Details:**
  - Thêm hàm `changeDashboardPage(pageNum, e)` vào `js/app.js`.
  - Quản lý trạng thái `currentDashboardPage` (1, 2, 3).
  - Cập nhật HTML pagination trong `index.html`:
    - Nút `<`: `onclick="changeDashboardPage(currentDashboardPage - 1, event)"`.
    - Nút `1`: `onclick="changeDashboardPage(1, event)"`.
    - Nút `2`: `onclick="changeDashboardPage(2, event)"`.
    - Nút `3`: `onclick="changeDashboardPage(3, event)"`.
    - Nút `>`: `onclick="changeDashboardPage(currentDashboardPage + 1, event)"`.
  - Mặc định khởi đầu ở trang 1 (`class="page-btn active"` tại trang 1, nút `<` mờ `opacity: 0.4; pointer-events: none`).
  - Khi chuyển trang: Cập nhật active class, cập nhật trạng thái disabled cho `<` và `>`, và cuộn mượt tới hãng tương ứng (1: Monster, 2: Redbull, 3: Sting).

---

### Task 3: Kích Hoạt Cuộn Mượt Cho Nút Hãng (Monster, Redbull, Sting) Trên Navbar
- **Files:** `index.html`, `pages/*.html`, `js/app.js`, `css/style.css`
- **Details:**
  - Cập nhật `handleNavBrandClick(e, link, targetId)` trong `js/app.js`:
    - Chuyển `active` sang nút vừa bấm.
    - Cuộn mượt (`targetEl.scrollIntoView({ behavior: 'smooth' })`).
  - Cập nhật CSS trong `css/style.css`:
    - Thêm `#monster-products, #redbull-products, #sting-products { scroll-margin-top: 100px; }` để thanh header cố định không che khuất tiêu đề hãng.
  - Các trang phụ (`pages/*.html`): dẫn về `../index.html#monster-products`, v.v.

---

### Task 4: Căn Lề & Tinh Chỉnh Chân Thẻ Sản Phẩm (Giá & Giỏ Hàng)
- **Files:** `css/style.css`, `index.html`, `pages/*.html`
- **Details:**
  - Thêm nhãn phụ `<span class="price-label">GIÁ CHÍNH HÃNG</span>` phía trên `<span class="price-current">...</span>`.
  - Tinh chỉnh CSS:
    - `.product-bottom`: `display: flex; justify-content: space-between; align-items: flex-end; padding-top: 14px; border-top: 1px solid rgba(255, 255, 255, 0.06); min-height: auto; gap: 12px;`.
    - `.price-label`: `font-size: 0.68rem; color: var(--text-dim); font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 2px;`.
    - `.btn-add-stitch`: kích thước $40 \times 40\text{px}$, `border-radius: 10px`, nền `rgba(57, 255, 20, 0.12)`, viền `1px solid rgba(57, 255, 20, 0.35)`, icon màu xanh neon; hover sáng rực nền neon và nảy nhẹ.

---

### Task 5: Xác Minh & Kiểm Thử Toàn Diện
- **Files:** `scripts/verify_header_footer_pagination.py`
- **Details:**
  - Tạo script kiểm thử tự động kiểm tra đủ 4 hạng mục.
  - Chạy `python verify_implementation.py` (đảm bảo 66/66 checks PASS).
  - Chạy `python scripts/verify_price_formatting.py` (đảm bảo 49/49 checks PASS).
