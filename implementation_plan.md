# Kế Hoạch Triển Khai: Chuẩn Hóa Nhãn Phân Loại Nhanh Và Lược Bỏ Kicker Đánh Giá Hardcode

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Chuẩn hóa nhãn 3 nút phân loại nhanh theo hãng (bỏ số vị hardcode `(4 vị)`, `(3 vị)`) và lược bỏ thẻ kicker marketing `12.400+ KHÁCH HÀNG TIN DÙNG` trong `index.html`.

**Architecture:** Pure Static HTML5 / CSS3 / Vanilla JS. Chỉnh sửa trực tiếp mã nguồn HTML tĩnh, duy trì sự tương thích 100% với các hàm JavaScript điều hướng `handleNavBrandClick`.

**Tech Stack:** HTML5, CSS3, Vanilla JavaScript, Python test suites.

## Global Constraints

- Không tự động chạy `git push`. Toàn bộ commit thực hiện cục bộ.
- 100% Pure Static Architecture: Không làm thay đổi layout hay gãy vỡ giao diện.
- Giữ nguyên toàn bộ cấu trúc neo và điều hướng thương hiệu của các nút phân loại nhanh.
- Test Suite Integrity: Duy trì 100% PASS cho tất cả các test suites hiện có.

---

### Task 1: Viết Script Kiểm Thử TDD `scripts/verify_clean_brand_pills_and_kicker.py`

**Files:**
- Create: `scripts/verify_clean_brand_pills_and_kicker.py`

- [ ] **Step 1: Viết script `scripts/verify_clean_brand_pills_and_kicker.py`**
- [ ] **Step 2: Chạy kiểm thử để xác nhận trạng thái thất bại ban đầu (Red Phase)**
- [ ] **Step 3: Commit cục bộ script test**

---

### Task 2: Chuẩn Hóa 3 Nút Phân Loại Nhanh Trong `index.html`

**Files:**
- Modify: `index.html:621-630`
- Test: `scripts/verify_clean_brand_pills_and_kicker.py`

- [ ] **Step 1: Thay thế `Monster Energy (4 vị)` thành `Monster Energy`**
- [ ] **Step 2: Thay thế `Redbull Thái Lan (3 vị)` thành `Redbull Thái Lan`**
- [ ] **Step 3: Thay thế `Sting PepsiCo (3 vị)` thành `Sting PepsiCo`**
- [ ] **Step 4: Commit cục bộ**

---

### Task 3: Lược Bỏ Thẻ Kicker `12.400+ KHÁCH HÀNG TIN DÙNG` Trong `index.html`

**Files:**
- Modify: `index.html:944-951`
- Test: `scripts/verify_clean_brand_pills_and_kicker.py`

- [ ] **Step 1: Xóa dòng `<span class="section-kicker"><i class="fas fa-award"></i> 12.400+ KHÁCH HÀNG TIN DÙNG</span>`**
- [ ] **Step 2: Chạy script `scripts/verify_clean_brand_pills_and_kicker.py` (Green Phase)**
- [ ] **Step 3: Commit cục bộ**

---

### Task 4: Kiểm Thử Toàn Diện Hệ Thống & Nghiệm Thu Hồi Quy

**Files:**
- Test: `verify_implementation.py`
- Test: `scripts/verify_ui_fixes_and_combo_removal.py`
- Test: `scripts/verify_footer_sync.py`
- Test: `scripts/verify_no_product_specs.py`
- Test: `scripts/verify_clean_brand_pills_and_kicker.py`

- [ ] **Step 1: Chạy `verify_implementation.py` (66/66 PASS)**
- [ ] **Step 2: Chạy `scripts/verify_ui_fixes_and_combo_removal.py` (8/8 PASS)**
- [ ] **Step 3: Chạy `scripts/verify_footer_sync.py` (144/144 PASS)**
- [ ] **Step 4: Chạy `scripts/verify_no_product_specs.py` (8/8 PASS)**
- [ ] **Step 5: Chạy `scripts/verify_clean_brand_pills_and_kicker.py` (PASS 100%)**
- [ ] **Step 6: Cập nhật tài liệu và báo cáo kết quả**
