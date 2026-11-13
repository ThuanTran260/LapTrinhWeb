# Kế Hoạch Triển Khai: Tinh Chỉnh Câu Chữ Thẻ KPI Thương Hiệu Admin Dashboard

> **Trạng thái:** ĐÃ HOÀN THÀNH TOÀN DIỆN (100% PASS)

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

- [x] **Step 1: Viết script `scripts/verify_admin_kpi_brand_wording.py`**
- [x] **Step 2: Chạy kiểm thử để xác nhận trạng thái thất bại ban đầu (Red Phase)**
- [x] **Step 3: Commit cục bộ script test (`edc1ce1`)**

---

### Task 2: Cập Nhật Câu Chữ Thẻ KPI Và Tiêu Đề Phụ Trong `admin/index.html` & `admin/inventory.html`

**Files:**
- Modify: `admin/index.html:100-101,276`
- Modify: `admin/inventory.html:57`
- Test: `scripts/verify_admin_kpi_brand_wording.py`

- [x] **Step 1: Thay thế thẻ KPI số 3 trong `admin/index.html` thành `<h3>3 Thương Hiệu</h3>` và `<p>Monster • Redbull • Sting</p>`**
- [x] **Step 2: Cập nhật nhãn phụ tại dòng 276 trong `admin/index.html`**
- [x] **Step 3: Cập nhật nhãn phụ tại dòng 57 trong `admin/inventory.html`**
- [x] **Step 4: Chạy script `scripts/verify_admin_kpi_brand_wording.py` (Green Phase - PASS 100%)**
- [x] **Step 5: Commit cục bộ (`d7e1d29`)**

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

- [x] **Step 1: Chạy `verify_implementation.py` (66/66 PASS)**
- [x] **Step 2: Chạy `scripts/verify_ui_fixes_and_combo_removal.py` (8/8 PASS)**
- [x] **Step 3: Chạy `scripts/verify_footer_sync.py` (144/144 PASS)**
- [x] **Step 4: Chạy `scripts/verify_sidebar_filter_sync.py` (31/31 PASS)**
- [x] **Step 5: Chạy `scripts/verify_no_product_specs.py` (8/8 PASS)**
- [x] **Step 6: Chạy `scripts/verify_clean_brand_pills_and_kicker.py` (9/9 PASS)**
- [x] **Step 7: Chạy `scripts/verify_admin_kpi_brand_wording.py` (PASS 100%)**
- [x] **Step 8: Cập nhật tài liệu và báo cáo kết quả**
