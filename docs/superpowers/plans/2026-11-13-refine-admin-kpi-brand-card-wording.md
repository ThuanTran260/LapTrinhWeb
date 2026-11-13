# Kế Hoạch Triển Khai: Tinh Chỉnh Câu Chữ Thẻ KPI Thương Hiệu Admin Dashboard

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Thay thế câu chữ thẻ KPI thương hiệu trong `admin/index.html` từ `3 Brand` / `Monster, Redbull & Sting` thành `3 Thương Hiệu` / `Monster • Redbull • Sting` theo Hướng 1 đã được phê duyệt.

**Architecture:** Pure Static HTML5 / CSS3 / Vanilla JS. Chỉnh sửa trực tiếp file HTML tĩnh, không ảnh hưởng layout hoặc logic CSS.

**Tech Stack:** HTML5, CSS3, Vanilla JavaScript, Python test suites.

## Global Constraints

- Không tự động chạy `git push`. Toàn bộ commit thực hiện cục bộ.
- 100% Pure Static Architecture: Không làm thay đổi layout hay gãy vỡ giao diện.
- Test Suite Integrity: Duy trì 100% PASS cho tất cả các test suites hiện có.

---

### Task 1: Viết Script Kiểm Thử TDD `scripts/verify_admin_kpi_brand_wording.py`

**Files:**
- Create: `scripts/verify_admin_kpi_brand_wording.py`

**Interfaces:**
- Consumes: Cấu trúc file `admin/index.html` và `admin/inventory.html`.
- Produces: Test script tự động kiểm tra việc chuẩn hóa câu chữ thuần Việt và dấu bullet `•`.

- [ ] **Step 1: Viết script `scripts/verify_admin_kpi_brand_wording.py`**
  Kiểm tra:
  1. `admin/index.html` chứa `<h3>3 Thương Hiệu</h3>` và `<p>Monster • Redbull • Sting</p>`.
  2. `admin/index.html` không còn chuỗi `3 Brand` hay `Monster, Redbull & Sting`.
  3. `admin/inventory.html` không còn chuỗi `Monster, Redbull & Sting`.
- [ ] **Step 2: Chạy kiểm thử để xác nhận trạng thái thất bại ban đầu (Red Phase)**
  Run: `python scripts/verify_admin_kpi_brand_wording.py`
  Expected: FAIL vì hiện tại vẫn là `3 Brand`.
- [ ] **Step 3: Commit cục bộ script test**
  `git add scripts/verify_admin_kpi_brand_wording.py`
  `git commit -m "test(admin): add verification for admin kpi brand card wording refinement"`

---

### Task 2: Cập Nhật Câu Chữ Thẻ KPI Và Tiêu Đề Phụ Trong `admin/index.html` & `admin/inventory.html`

**Files:**
- Modify: `admin/index.html:100-101,276`
- Modify: `admin/inventory.html:57`
- Test: `scripts/verify_admin_kpi_brand_wording.py`

**Interfaces:**
- Consumes: Thẻ KPI số 3 trong `admin/index.html` và text tóm tắt trong `admin/inventory.html`.
- Produces: Câu chữ thuần Việt thanh lịch với dấu bullet `•` ngăn cách.

- [ ] **Step 1: Thay thế thẻ KPI số 3 trong `admin/index.html` thành `<h3>3 Thương Hiệu</h3>` và `<p>Monster • Redbull • Sting</p>`**
- [ ] **Step 2: Cập nhật nhãn phụ tại dòng 276 trong `admin/index.html`**
- [ ] **Step 3: Cập nhật nhãn phụ tại dòng 57 trong `admin/inventory.html`**
- [ ] **Step 4: Chạy script `scripts/verify_admin_kpi_brand_wording.py` (Green Phase)**
  Run: `python scripts/verify_admin_kpi_brand_wording.py`
  Expected: PASS 100%.
- [ ] **Step 5: Commit cục bộ**
  `git add admin/index.html admin/inventory.html`
  `git commit -m "fix(admin): refine kpi brand card wording to '3 Thương Hiệu' with bullet separator"`

---

### Task 3: Kiểm Thử Toàn Diện Hệ Thống & Nghiệm Thu Hồi Quy

**Files:**
- Test: `verify_implementation.py`
- Test: `scripts/verify_ui_fixes_and_combo_removal.py`
- Test: `scripts/verify_footer_sync.py`
- Test: `scripts/verify_no_product_specs.py`
- Test: `scripts/verify_clean_brand_pills_and_kicker.py`
- Test: `scripts/verify_sidebar_filter_sync.py`
- Test: `scripts/verify_admin_kpi_brand_wording.py`

- [ ] **Step 1: Chạy `verify_implementation.py` (66/66 PASS)**
- [ ] **Step 2: Chạy `scripts/verify_ui_fixes_and_combo_removal.py` (8/8 PASS)**
- [ ] **Step 3: Chạy `scripts/verify_footer_sync.py` (144/144 PASS)**
- [ ] **Step 4: Chạy `scripts/verify_sidebar_filter_sync.py` (31/31 PASS)**
- [ ] **Step 5: Chạy `scripts/verify_admin_kpi_brand_wording.py` (PASS 100%)**
- [ ] **Step 6: Cập nhật tài liệu và báo cáo kết quả**
