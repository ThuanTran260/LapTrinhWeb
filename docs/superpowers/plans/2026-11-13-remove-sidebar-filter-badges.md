# Kế Hoạch Triển Khai: Lược Bỏ Nhãn Đếm Số Lon Và Khoảng Giá Phụ Khỏi Sidebar Bộ Lọc

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Lược bỏ toàn bộ các thẻ `.filter-option-count` (số lon đếm và khoảng giá phụ) khỏi sidebar bộ lọc tại `index.html` và `pages/search-results.html`, đồng bộ kịch bản kiểm thử `scripts/verify_sidebar_filter_sync.py`.

**Architecture:** Pure Static HTML5 / CSS3 / Vanilla JS. Chỉnh sửa trực tiếp mã nguồn HTML tĩnh, duy trì sự tương thích 100% với form submit bộ lọc `handleSearchResultsFilter` và `applyDashboardSidebarFilter`.

**Tech Stack:** HTML5, CSS3, Vanilla JavaScript, Python test suites.

## Global Constraints

- Không tự động chạy `git push`. Toàn bộ commit thực hiện cục bộ.
- 100% Pure Static Architecture: Không làm thay đổi layout hay gãy vỡ giao diện.
- Giữ nguyên toàn bộ cấu trúc radio inputs: `name`, `value`, `checked`.
- Test Suite Integrity: Duy trì 100% PASS cho tất cả các test suites hiện có.

---

### Task 1: Cập Nhật Script Kiểm Thử TDD `scripts/verify_sidebar_filter_sync.py`

**Files:**
- Modify: `scripts/verify_sidebar_filter_sync.py`

**Interfaces:**
- Consumes: Cấu trúc file `index.html` và `pages/search-results.html`.
- Produces: Test script tự động kiểm tra việc không còn bất kỳ thẻ `filter-option-count` nào và nhãn radio sạch.

- [ ] **Step 1: Cập nhật `scripts/verify_sidebar_filter_sync.py`**
  Điều chỉnh:
  1. Kiểm tra 4 thương hiệu radio có nhãn chuẩn sạch và không có `filter-option-count`.
  2. Kiểm tra 4 khoảng giá radio có nhãn chuẩn sạch và không có `filter-option-count`.
  3. Kiểm tra cả `search-results.html` lẫn `index.html` đều có 0 thẻ `.filter-option-count`.
- [ ] **Step 2: Chạy kiểm thử để xác nhận trạng thái thất bại ban đầu (Red Phase)**
  Run: `python scripts/verify_sidebar_filter_sync.py`
  Expected: FAIL vì hiện tại cả 2 trang vẫn còn các thẻ `filter-option-count`.
- [ ] **Step 3: Commit cục bộ script test**
  `git add scripts/verify_sidebar_filter_sync.py`
  `git commit -m "test(sidebar): update verify_sidebar_filter_sync for clean options without counts"`

---

### Task 2: Lược Bỏ Các Thẻ `filter-option-count` Trong `index.html`

**Files:**
- Modify: `index.html:544-594`
- Test: `scripts/verify_sidebar_filter_sync.py`

**Interfaces:**
- Consumes: Cấu trúc HTML sidebar filter trong `index.html`.
- Produces: Các lựa chọn radio thương hiệu và khoảng giá không còn thẻ `filter-option-count`.

- [ ] **Step 1: Xóa 4 thẻ `filter-option-count` trong nhóm Phân loại thương hiệu của `index.html`**
- [ ] **Step 2: Xóa 3 thẻ `filter-option-count` trong nhóm Khoảng giá của `index.html`**
- [ ] **Step 3: Commit cục bộ**
  `git add index.html`
  `git commit -m "fix(sidebar): remove hardcoded counts and price sublabels from index.html sidebar"`

---

### Task 3: Lược Bỏ Các Thẻ `filter-option-count` Trong `pages/search-results.html`

**Files:**
- Modify: `pages/search-results.html:326-376`
- Test: `scripts/verify_sidebar_filter_sync.py`

**Interfaces:**
- Consumes: Cấu trúc HTML sidebar filter trong `pages/search-results.html`.
- Produces: Các lựa chọn radio thương hiệu và khoảng giá không còn thẻ `filter-option-count`.

- [ ] **Step 1: Xóa 4 thẻ `filter-option-count` trong nhóm Phân loại thương hiệu của `search-results.html`**
- [ ] **Step 2: Xóa 3 thẻ `filter-option-count` trong nhóm Khoảng giá của `search-results.html`**
- [ ] **Step 3: Chạy script `scripts/verify_sidebar_filter_sync.py` (Green Phase)**
  Run: `python scripts/verify_sidebar_filter_sync.py`
  Expected: PASS 100%.
- [ ] **Step 4: Commit cục bộ**
  `git add pages/search-results.html`
  `git commit -m "fix(sidebar): remove hardcoded counts and price sublabels from search-results.html sidebar"`

---

### Task 4: Kiểm Thử Toàn Diện Hệ Thống & Nghiệm Thu Hồi Quy

**Files:**
- Test: `verify_implementation.py`
- Test: `scripts/verify_ui_fixes_and_combo_removal.py`
- Test: `scripts/verify_footer_sync.py`
- Test: `scripts/verify_no_product_specs.py`
- Test: `scripts/verify_clean_brand_pills_and_kicker.py`
- Test: `scripts/verify_sidebar_filter_sync.py`

- [ ] **Step 1: Chạy `verify_implementation.py` (66/66 PASS)**
- [ ] **Step 2: Chạy `scripts/verify_ui_fixes_and_combo_removal.py` (8/8 PASS)**
- [ ] **Step 3: Chạy `scripts/verify_footer_sync.py` (144/144 PASS)**
- [ ] **Step 4: Chạy `scripts/verify_no_product_specs.py` (8/8 PASS)**
- [ ] **Step 5: Chạy `scripts/verify_clean_brand_pills_and_kicker.py` (9/9 PASS)**
- [ ] **Step 6: Chạy `scripts/verify_sidebar_filter_sync.py` (PASS 100%)**
- [ ] **Step 7: Cập nhật tài liệu và báo cáo kết quả**
