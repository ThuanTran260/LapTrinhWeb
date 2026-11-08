# Kế Hoạch Triển Khai: Đồng Bộ Footer 4 Cột Cho Toàn Bộ Trang Dashboard & Storefront

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Đồng bộ hoàn toàn footer 4 cột nhận diện thương hiệu Energy Boost (chuẩn theo mẫu `index.html`) cho toàn bộ 12 trang khách hàng trong `pages/` và 12 trang quản trị trong `admin/`.

**Architecture:** Kiến trúc Pure Static HTML5 & CSS3. Chuẩn hóa mã nguồn HTML tĩnh với cấu trúc thẻ semantic `<footer class="footer">` chứa `.container`, `.footer-grid` (4 cột) và `.footer-bottom`. Tự động tinh chỉnh đường dẫn tương đối (`../` và `./`) chính xác cho từng cấp thư mục để đảm bảo không gãy liên kết.

**Tech Stack:** Pure HTML5, CSS3 Glassmorphism/Dark Neon, Vanilla JavaScript (Toast feedback), Python test suites.

## Global Constraints

- Tuân thủ nghiêm ngặt RULE `user_global`: Không tự ý viết mã nguồn hoặc chỉnh sửa file cho đến khi người dùng ấn **Proceed** hoặc đồng ý kế hoạch.
- Tuyệt đối không tự động chạy `git push`. Toàn bộ commit thực hiện cục bộ.
- 100% Pure Static: Không sử dụng framework ngoài, giữ trọn vẹn khả năng chạy trực tiếp file HTML trên trình duyệt.
- Tương thích và duy trì 100% PASS cho toàn bộ bộ test hiện hữu (`verify_implementation.py`, `scripts/verify_*.py`).

---

### Task 1: Thiết Lập CSS Bổ Trợ Cho Footer Trong Admin Layout & Viết Script Kiểm Thử Tự Động

**Files:**
- Modify: `css/style.css`
- Create: `scripts/verify_footer_sync.py`

**Interfaces:**
- Consumes: Cấu trúc lớp `.admin-main`, `.footer`, `.footer-grid` hiện có trong `css/style.css`.
- Produces: Quy tắc `.admin-main .footer` tối ưu hiển thị trong cột nội dung admin; script kiểm thử `scripts/verify_footer_sync.py` kiểm tra cấu trúc footer trên toàn bộ 24 trang HTML.

- [ ] **Step 1: Viết script kiểm thử thất bại (Red Test) `scripts/verify_footer_sync.py`**
  Script duyệt qua danh sách 12 trang `pages/*.html` và 12 trang `admin/*.html`, kiểm tra sự tồn tại của `<footer class="footer">`, `.footer-grid`, `CÁC DÒNG SẢN PHẨM`, `HỆ THỐNG TRANG`, `NHẬN VOUCHER ƯU ĐÃI`, `.footer-bottom`, và kiểm tra không còn thẻ footer 1 dòng rút gọn.
- [ ] **Step 2: Chạy script kiểm thử để xác nhận trạng thái FAIL hiện tại (Red Phase)**
  Run: `python scripts/verify_footer_sync.py`
  Expected: FAIL vì các trang `pages/` đang có footer 1 dòng và `admin/` chưa có footer.
- [ ] **Step 3: Bổ sung CSS bổ trợ cho `.admin-main .footer` trong `css/style.css`**
  Thêm đoạn CSS căn chỉnh khung footer trong khu vực admin:
  ```css
  /* Admin Footer Enhancements */
  .admin-main .footer {
    margin-top: 48px;
    background: #07080A;
    border-radius: var(--radius-md);
    border: 1px solid var(--border-color);
    padding: 36px 24px 20px;
  }
  .admin-main .footer .container {
    max-width: 100%;
    padding: 0;
  }
  ```
- [ ] **Step 4: Commit cục bộ phần chuẩn bị CSS và test script**
  `git add css/style.css scripts/verify_footer_sync.py`
  `git commit -m "test(footer): add verify_footer_sync script and admin footer styling"`

---

### Task 2: Đồng Bộ Footer 4 Cột Chuẩn Cho Toàn Bộ 12 Trang Khách Hàng (`pages/*.html`)

**Files:**
- Modify: `pages/account.html`
- Modify: `pages/cart.html`
- Modify: `pages/orders.html`
- Modify: `pages/order-detail.html`
- Modify: `pages/order-success.html`
- Modify: `pages/payment-gateway.html`
- Modify: `pages/product-detail.html`
- Modify: `pages/product-detail-redbull.html`
- Modify: `pages/product-detail-redbull-thai.html`
- Modify: `pages/product-detail-redbull-lonvua.html`
- Modify: `pages/product-detail-sting.html`
- Modify: `pages/search-results.html`
- Test: `scripts/verify_footer_sync.py`

**Interfaces:**
- Consumes: Đoạn mã HTML Footer 4 cột chuẩn từ `index.html`.
- Produces: Đoạn mã Footer chuẩn với đường dẫn relative cấp `pages/`:
  - `../index.html` cho Trang Chủ và Logo
  - `../index.html#monster-products`, `../index.html#redbull-products`, `../index.html#sting-products` cho danh mục
  - `product-detail.html`, `product-detail-redbull.html`, `cart.html`, `orders.html`, `account.html` cho hệ thống trang
  - `onsubmit="event.preventDefault(); showToast('Đã đăng ký nhận tin Energy Boost thành công!', 'success');"` cho form voucher.

- [ ] **Step 1: Cập nhật Footer trong `pages/account.html` và `pages/cart.html`**
  Thay thế thẻ footer 1 dòng bằng footer 4 cột đầy đủ với các link tương đối chuẩn xác.
- [ ] **Step 2: Cập nhật Footer trong `pages/orders.html`, `pages/order-detail.html`, `pages/order-success.html`, `pages/payment-gateway.html`**
  Thay thế thẻ footer 1 dòng bằng footer 4 cột đầy đủ.
- [ ] **Step 3: Cập nhật Footer trong 5 trang chi tiết sản phẩm (`product-detail*.html`) và `pages/search-results.html`**
  Thay thế footer rút gọn hoặc footer cũ thành footer 4 cột đồng nhất chuẩn.
- [ ] **Step 4: Chạy kiểm thử xác minh nhóm `pages/`**
  Run: `python scripts/verify_footer_sync.py`
  Expected: Toàn bộ 12 trang thuộc `pages/` đều PASS kiểm tra cấu trúc footer.
- [ ] **Step 5: Commit cục bộ nhóm trang khách hàng**
  `git add pages/`
  `git commit -m "feat(pages): synchronize 4-column rich footer across all storefront pages"`

---

### Task 3: Đồng Bộ Footer 4 Cột Cho Toàn Bộ 12 Trang Quản Trị Admin Dashboard (`admin/*.html`)

**Files:**
- Modify: `admin/index.html`
- Modify: `admin/orders.html`
- Modify: `admin/inventory.html`
- Modify: `admin/revenue.html`
- Modify: `admin/customers.html`
- Modify: `admin/settings.html`
- Modify: `admin/order-detail.html`
- Modify: `admin/edit-monster.html`
- Modify: `admin/edit-redbull-lonvua.html`
- Modify: `admin/edit-redbull-original.html`
- Modify: `admin/edit-redbull-thai.html`
- Modify: `admin/edit-sting.html`
- Test: `scripts/verify_footer_sync.py`

**Interfaces:**
- Consumes: Đoạn mã HTML Footer 4 cột chuẩn từ `index.html`.
- Produces: Đoạn mã Footer chuẩn đặt trước thẻ đóng `</main>` trong layout `admin-main`:
  - `../index.html` cho Logo và Trang Chủ
  - `../index.html#monster-products`, `../index.html#redbull-products`, `../index.html#sting-products` cho các dòng sản phẩm
  - `../pages/product-detail.html`, `../pages/product-detail-redbull.html`, `../pages/cart.html`, `../pages/orders.html`, `../pages/account.html` cho hệ thống trang.

- [ ] **Step 1: Bổ sung Footer 4 cột vào 6 trang nghiệp vụ cốt lõi của Admin**
  Chèn footer vào trước `</main>` trong `admin/index.html`, `admin/orders.html`, `admin/inventory.html`, `admin/revenue.html`, `admin/customers.html`, `admin/settings.html`.
- [ ] **Step 2: Bổ sung Footer 4 cột vào trang chi tiết đơn hàng admin `admin/order-detail.html` và 5 trang biên tập sản phẩm `admin/edit-*.html`**
  Chèn footer vào trước `</main>` trong `admin/order-detail.html`, `admin/edit-monster.html`, `admin/edit-redbull-lonvua.html`, `admin/edit-redbull-original.html`, `admin/edit-redbull-thai.html`, `admin/edit-sting.html`.
- [ ] **Step 3: Chạy script kiểm thử `scripts/verify_footer_sync.py`**
  Run: `python scripts/verify_footer_sync.py`
  Expected: PASS 100% trên toàn bộ 24 trang (12 pages + 12 admin).
- [ ] **Step 4: Commit cục bộ nhóm trang quản trị Admin Dashboard**
  `git add admin/`
  `git commit -m "feat(admin): integrate synchronized 4-column brand footer across all admin dashboard pages"`

---

### Task 4: Kiểm Thử Toàn Diện Hệ Thống & Nghiệm Thu Hồi Quy (Regression Testing)

**Files:**
- Test: `verify_implementation.py`
- Test: `scripts/verify_header_footer_pagination.py`
- Test: `scripts/verify_header_top_and_account_breadcrumb.py`
- Test: `scripts/verify_ui_fixes_and_combo_removal.py`
- Test: `scripts/verify_admin_ui_mockup.py`
- Test: `scripts/verify_order_detail_pages.py`
- Test: `scripts/verify_unconstrained_add_user.py`
- Test: `scripts/verify_ward_filter_and_address.py`
- Test: `scripts/verify_footer_sync.py`

- [ ] **Step 1: Chạy toàn bộ test suites hiện có**
  Run: `python verify_implementation.py`
  Expected: ALL 66 CHECKS PASSED PERFECTLY!
- [ ] **Step 2: Chạy toàn bộ script kiểm thử nghiệp vụ trong `scripts/`**
  Run: `python scripts/verify_header_footer_pagination.py`, `python scripts/verify_footer_sync.py`, v.v.
  Expected: Không có bất kỳ lỗi hồi quy nào.
- [ ] **Step 3: Kiểm tra giao diện và kiểm thử liên kết thực tế trên trình duyệt**
- [ ] **Step 4: Cập nhật tài liệu tổng kết và báo cáo người dùng**
