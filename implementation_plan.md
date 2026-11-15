# Kế Hoạch Triển Khai: Cố Định Form FAQ #1, Thêm Nút Lưu, Thông Báo "Đã Chuyển" & Điều Hướng Nút Mua Sắm Ngay

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 
1. Chuyển nút "Mua Sắm Ngay" trên `pages/orders.html` trỏ về `../index.html#monster-products`.
2. Cố định dữ liệu Câu #1 trong form FAQ trên `admin/settings.html`, thêm nút "Lưu Thay Đổi", và cấu hình nút Sửa chỉ hiển thị thông báo Toast "Đã chuyển" mà không thay đổi nội dung form.

**Architecture:** Pure Static HTML5 / Vanilla JS. Giữ nguyên kiến trúc tĩnh, không phụ thuộc thư viện ngoài.

**Tech Stack:** HTML5, CSS3, Vanilla JavaScript, Python test suites.

## Global Constraints

- Không tự động chạy `git push`. Toàn bộ commit thực hiện cục bộ.
- 100% Pure Static Architecture: Không làm thay đổi layout hay gãy vỡ giao diện.
- Test Suite Integrity: Duy trì 100% PASS cho tất cả các test suites hiện có.

---

### Task 1: Viết Script Kiểm Thử TDD `scripts/verify_faq_edit_save_and_orders_link.py` (Red Phase)

**Files:**
- Create: `scripts/verify_faq_edit_save_and_orders_link.py`

- [x] **Step 1: Viết script `scripts/verify_faq_edit_save_and_orders_link.py`**
  - Kiểm tra `pages/orders.html` nút Mua Sắm Ngay trỏ `../index.html#monster-products`.
  - Kiểm tra `admin/settings.html` form FAQ hiển thị sẵn nội dung Câu 1 và có nút "Lưu Thay Đổi".
  - Kiểm tra Node.js runtime: `handleAdminEditFaq` không thay đổi nội dung form và hiển thị toast "Đã chuyển".
  - Kiểm tra `handleAdminSaveFaq` hiển thị toast lưu thành công.
- [x] **Step 2: Chạy kiểm thử để xác nhận trạng thái thất bại ban đầu (Red Phase)**
  Run: `python scripts/verify_faq_edit_save_and_orders_link.py`
  Expected: FAIL.
- [x] **Step 3: Commit cục bộ script test**
  `git add scripts/verify_faq_edit_save_and_orders_link.py`
  `git commit -m "test: add verification for faq edit-save flow and orders shop now link"`

---

### Task 2: Cập Nhật Liên Kết Nút "Mua Sắm Ngay" Trong `pages/orders.html`

**Files:**
- Modify: `pages/orders.html:288`

- [x] **Step 1: Cập nhật `href="cart.html"` thành `href="../index.html#monster-products"` tại dòng 288**
- [x] **Step 2: Commit cục bộ**
  `git add pages/orders.html`
  `git commit -m "fix(orders): redirect shop now button to main product catalog section"`

---

### Task 3: Cập Nhật Giao Diện Form FAQ Trong `admin/settings.html`

**Files:**
- Modify: `admin/settings.html:220-246`

- [x] **Step 1: Cố định nội dung Câu #1 vào form và thêm nút "Lưu Thay Đổi"**
  - Input `#faq-new-question`: có sẵn value Câu 1.
  - Input `#faq-new-order`: có sẵn `value="1"`.
  - Textarea `#faq-new-answer`: có sẵn nội dung câu trả lời Câu 1.
  - Thêm nút `<button type="button" class="btn-add-cart" onclick="handleAdminSaveFaq()"><i class="fas fa-save"></i> Lưu Thay Đổi</button>`.
- [x] **Step 2: Commit cục bộ**
  `git add admin/settings.html`
  `git commit -m "feat(admin): set fixed faq #1 default values and add save changes button"`

---

### Task 4: Cập Nhật Xử Lý `handleAdminEditFaq` & Thêm `handleAdminSaveFaq` Trong `js/app.js`

**Files:**
- Modify: `js/app.js`

- [x] **Step 1: Thêm hàm `handleAdminSaveFaq` hiển thị thông báo lưu thành công**
- [x] **Step 2: Cập nhật `handleAdminEditFaq` chỉ hiển thị Toast "Đã chuyển", không ghi đè form**
- [x] **Step 3: Chạy script `scripts/verify_faq_edit_save_and_orders_link.py` (Green Phase)**
  Run: `python scripts/verify_faq_edit_save_and_orders_link.py`
  Expected: PASS 100%.
- [x] **Step 4: Cập nhật script `scripts/verify_admin_features_update.py` tương ứng nếu cần**
- [x] **Step 5: Commit cục bộ**
  `git add js/app.js scripts/verify_admin_features_update.py`
  `git commit -m "fix(admin): update faq edit to show toast only without modifying form, add save handler"`

---

### Task 5: Kiểm Thử Toàn Diện Hệ Thống & Nghiệm Thu Hồi Quy

**Files:**
- Test: `scripts/verify_faq_edit_save_and_orders_link.py`
- Test: `scripts/verify_admin_features_update.py`
- Test: `verify_implementation.py`
- Test: `scripts/verify_price_formatting.py`
- Test: `scripts/verify_clean_brand_pills_and_kicker.py`
- Test: `scripts/verify_footer_sync.py`
- Test: `scripts/verify_sidebar_filter_sync.py`
- Test: `scripts/verify_admin_kpi_brand_wording.py`

- [x] **Step 1: Chạy tất cả test suites đảm bảo không hồi quy (100% PASS)**
- [x] **Step 2: Cập nhật tài liệu và báo cáo kết quả**
