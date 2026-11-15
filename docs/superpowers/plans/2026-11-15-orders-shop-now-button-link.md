# Kế Hoạch Triển Khai: Cập Nhật Liên Kết Nút "Mua Sắm Ngay" Trên Trang Lịch Sử Đơn Hàng

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Chuyển đổi thuộc tính `href` của nút **"Mua Sắm Ngay"** trong `pages/orders.html` từ `cart.html` sang `../index.html#monster-products` theo Phương án 1 đã thống nhất.

**Architecture:** Pure Static HTML5 / Vanilla JS. Giữ nguyên kiến trúc tĩnh, không phụ thuộc thư viện ngoài.

**Tech Stack:** HTML5, CSS3, Python test suites.

## Global Constraints

- Không tự động chạy `git push`. Toàn bộ commit thực hiện cục bộ.
- 100% Pure Static Architecture: Không làm thay đổi layout hay gãy vỡ giao diện.
- Test Suite Integrity: Duy trì 100% PASS cho tất cả các test suites hiện có.

---

### Task 1: Viết Script Kiểm Thử TDD `scripts/verify_orders_shop_now_link.py` (Red Phase)

**Files:**
- Create: `scripts/verify_orders_shop_now_link.py`

- [ ] **Step 1: Viết script `scripts/verify_orders_shop_now_link.py`**
  - Kiểm tra `pages/orders.html` chứa `<a href="../index.html#monster-products" ... Mua Sắm Ngay</a>`.
  - Kiểm tra `pages/orders.html` không còn `href="cart.html"` cho nút `Mua Sắm Ngay`.
- [ ] **Step 2: Chạy kiểm thử để xác nhận trạng thái thất bại ban đầu (Red Phase)**
  Run: `python scripts/verify_orders_shop_now_link.py`
  Expected: FAIL vì hiện tại vẫn là `href="cart.html"`.
- [ ] **Step 3: Commit cục bộ script test**
  `git add scripts/verify_orders_shop_now_link.py`
  `git commit -m "test(orders): add verification for shop now button linking to main product menu"`

---

### Task 2: Cập Nhật Liên Kết Nút "Mua Sắm Ngay" Trong `pages/orders.html` (Green Phase)

**Files:**
- Modify: `pages/orders.html:288`
- Test: `scripts/verify_orders_shop_now_link.py`

- [ ] **Step 1: Cập nhật `href="cart.html"` thành `href="../index.html#monster-products"` tại dòng 288**
- [ ] **Step 2: Chạy script `scripts/verify_orders_shop_now_link.py` (Green Phase)**
  Run: `python scripts/verify_orders_shop_now_link.py`
  Expected: PASS 100%.
- [ ] **Step 3: Commit cục bộ**
  `git add pages/orders.html`
  `git commit -m "fix(orders): redirect shop now button to main product catalog section"`

---

### Task 3: Kiểm Thử Toàn Diện Hệ Thống & Nghiệm Thu Hồi Quy

**Files:**
- Test: `scripts/verify_orders_shop_now_link.py`
- Test: `verify_implementation.py`
- Test: `scripts/verify_admin_features_update.py`
- Test: `scripts/verify_price_formatting.py`
- Test: `scripts/verify_clean_brand_pills_and_kicker.py`
- Test: `scripts/verify_footer_sync.py`
- Test: `scripts/verify_sidebar_filter_sync.py`
- Test: `scripts/verify_admin_kpi_brand_wording.py`

- [ ] **Step 1: Chạy tất cả test suites đảm bảo không hồi quy**
- [ ] **Step 2: Cập nhật tài liệu và báo cáo kết quả**
