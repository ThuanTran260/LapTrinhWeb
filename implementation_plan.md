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

- [ ] **Step 1: Cập nhật `scripts/verify_sidebar_filter_sync.py`**
- [ ] **Step 2: Chạy kiểm thử để xác nhận trạng thái thất bại ban đầu (Red Phase)**
- [ ] **Step 3: Commit cục bộ script test**

---

### Task 2: Lược Bỏ Các Thẻ `filter-option-count` Trong `index.html`

**Files:**
- Modify: `index.html:544-594`
- Test: `scripts/verify_sidebar_filter_sync.py`

- [ ] **Step 1: Xóa 4 thẻ `filter-option-count` trong nhóm Phân loại thương hiệu của `index.html`**
- [ ] **Step 2: Xóa 3 thẻ `filter-option-count` trong nhóm Khoảng giá của `index.html`**
- [ ] **Step 3: Commit cục bộ**

---

### Task 3: Lược Bỏ Các Thẻ `filter-option-count` Trong `pages/search-results.html`

**Files:**
- Modify: `pages/search-results.html:326-376`
- Test: `scripts/verify_sidebar_filter_sync.py`

- [ ] **Step 1: Xóa 4 thẻ `filter-option-count` trong nhóm Phân loại thương hiệu của `search-results.html`**
- [ ] **Step 2: Xóa 3 thẻ `filter-option-count` trong nhóm Khoảng giá của `search-results.html`**
- [ ] **Step 3: Chạy script `scripts/verify_sidebar_filter_sync.py` (Green Phase)**
- [ ] **Step 4: Commit cục bộ**

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
