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

- [ ] **Step 1: Viết script kiểm thử thất bại (Red Test) `scripts/verify_footer_sync.py`**
- [ ] **Step 2: Chạy script kiểm thử để xác nhận trạng thái FAIL hiện tại (Red Phase)**
- [ ] **Step 3: Bổ sung CSS bổ trợ cho `.admin-main .footer` trong `css/style.css`**
- [ ] **Step 4: Commit cục bộ phần chuẩn bị CSS và test script**

---

### Task 2: Đồng Bộ Footer 4 Cột Chuẩn Cho Toàn Bộ 12 Trang Khách Hàng (`pages/*.html`)

**Files:**
- Modify: `pages/account.html`, `pages/cart.html`, `pages/orders.html`, `pages/order-detail.html`, `pages/order-success.html`, `pages/payment-gateway.html`, `pages/product-detail.html`, `pages/product-detail-redbull.html`, `pages/product-detail-redbull-thai.html`, `pages/product-detail-redbull-lonvua.html`, `pages/product-detail-sting.html`, `pages/search-results.html`
- Test: `scripts/verify_footer_sync.py`

- [ ] **Step 1: Cập nhật Footer trong `pages/account.html` và `pages/cart.html`**
- [ ] **Step 2: Cập nhật Footer trong `pages/orders.html`, `pages/order-detail.html`, `pages/order-success.html`, `pages/payment-gateway.html`**
- [ ] **Step 3: Cập nhật Footer trong 5 trang chi tiết sản phẩm (`product-detail*.html`) và `pages/search-results.html`**
- [ ] **Step 4: Chạy kiểm thử xác minh nhóm `pages/`**
- [ ] **Step 5: Commit cục bộ nhóm trang khách hàng**

---

### Task 3: Đồng Bộ Footer 4 Cột Cho Toàn Bộ 12 Trang Quản Trị Admin Dashboard (`admin/*.html`)

**Files:**
- Modify: `admin/index.html`, `admin/orders.html`, `admin/inventory.html`, `admin/revenue.html`, `admin/customers.html`, `admin/settings.html`, `admin/order-detail.html`, `admin/edit-monster.html`, `admin/edit-redbull-lonvua.html`, `admin/edit-redbull-original.html`, `admin/edit-redbull-thai.html`, `admin/edit-sting.html`
- Test: `scripts/verify_footer_sync.py`

- [ ] **Step 1: Bổ sung Footer 4 cột vào 6 trang nghiệp vụ cốt lõi của Admin**
- [ ] **Step 2: Bổ sung Footer 4 cột vào `admin/order-detail.html` và 5 trang biên tập sản phẩm `admin/edit-*.html`**
- [ ] **Step 3: Chạy script kiểm thử `scripts/verify_footer_sync.py`**
- [ ] **Step 4: Commit cục bộ nhóm trang quản trị Admin Dashboard**

---

### Task 4: Kiểm Thử Toàn Diện Hệ Thống & Nghiệm Thu Hồi Quy

**Files:**
- Test: `verify_implementation.py`
- Test: `scripts/verify_header_footer_pagination.py`
- Test: `scripts/verify_ui_fixes_and_combo_removal.py`
- Test: `scripts/verify_footer_sync.py`

- [ ] **Step 1: Chạy toàn bộ test suites hiện có**
- [ ] **Step 2: Chạy toàn bộ script kiểm thử nghiệp vụ trong `scripts/`**
- [ ] **Step 3: Kiểm tra giao diện và kiểm thử liên kết thực tế trên trình duyệt**
- [ ] **Step 4: Cập nhật tài liệu tổng kết và báo cáo người dùng**
