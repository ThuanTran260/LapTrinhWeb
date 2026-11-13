# Kế Hoạch Triển Khai: Loại Bỏ Khối Thông Số Hardcode (product-specs) Khỏi Thẻ Sản Phẩm

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Loại bỏ hoàn toàn khối thông số hardcode `.product-specs` (chứa các icon và text `Sẵn hàng`, `0 Đường`, dung tích...) khỏi tất cả 14 thẻ sản phẩm trên `index.html`, thẻ mẫu trong `pages/search-results.html` và template render trong `js/app.js`, đảm bảo giao diện thẻ gọn gàng và đồng bộ 100% với dữ liệu quản trị Admin.

**Architecture:** Pure Static HTML5 / CSS3 / Vanilla JS. Xóa bỏ thẻ `<div class="product-specs">...</div>` khỏi mã nguồn HTML và template JS. CSS `.product-card-stitch` với `.product-bottom { margin-top: auto; }` sẽ tự động kéo giá tiền và nút giỏ hàng xuống sát đáy card, duy trì sự thẳng hàng tuyệt đối.

**Tech Stack:** HTML5, CSS3, Vanilla JavaScript, Python test suites.

## Global Constraints

- Không tự động chạy `git push`. Toàn bộ commit thực hiện cục bộ.
- 100% Pure Static Architecture: Không làm thay đổi layout hay gãy vỡ giao diện.
- Giữ nguyên toàn bộ 14 nút `btn-add-stitch`, liên kết điều hướng ảnh và tiêu đề đến trang chi tiết sản phẩm.
- Test Suite Integrity: Duy trì 100% PASS cho `verify_implementation.py`, `scripts/verify_ui_fixes_and_combo_removal.py` và `scripts/verify_footer_sync.py`.

---

### Task 1: Viết Script Kiểm Thử TDD `scripts/verify_no_product_specs.py`

**Files:**
- Create: `scripts/verify_no_product_specs.py`

- [ ] **Step 1: Viết test script `scripts/verify_no_product_specs.py`**
- [ ] **Step 2: Chạy kiểm thử để xác nhận trạng thái thất bại ban đầu (Red Phase)**
- [ ] **Step 3: Commit cục bộ script test**

---

### Task 2: Loại Bỏ Khối `.product-specs` Khỏi 14 Thẻ Sản Phẩm Trong `index.html`

**Files:**
- Modify: `index.html:328-424,670-940`
- Test: `scripts/verify_no_product_specs.py`

- [ ] **Step 1: Xóa khối `.product-specs` khỏi 4 thẻ sản phẩm Flash Sale**
- [ ] **Step 2: Xóa khối `.product-specs` khỏi 4 thẻ thương hiệu Monster Energy**
- [ ] **Step 3: Xóa khối `.product-specs` khỏi 3 thẻ thương hiệu Redbull Thái Lan**
- [ ] **Step 4: Xóa khối `.product-specs` khỏi 3 thẻ thương hiệu Sting PepsiCo**
- [ ] **Step 5: Kiểm tra xác minh `index.html` không còn bất kỳ thẻ `product-specs` nào**
- [ ] **Step 6: Commit cục bộ**

---

### Task 3: Loại Bỏ Khối `.product-specs` Khỏi `pages/search-results.html` và `js/app.js`

**Files:**
- Modify: `pages/search-results.html:409-412`
- Modify: `js/app.js:2034-2037`
- Test: `scripts/verify_no_product_specs.py`

- [ ] **Step 1: Xóa khối `.product-specs` trong `pages/search-results.html`**
- [ ] **Step 2: Xóa khối `.product-specs` trong template HTML của `js/app.js`**
- [ ] **Step 3: Chạy script kiểm thử `scripts/verify_no_product_specs.py` (Green Phase)**
- [ ] **Step 4: Commit cục bộ**

---

### Task 4: Kiểm Thử Toàn Diện Hệ Thống & Nghiệm Thu Hồi Quy

**Files:**
- Test: `verify_implementation.py`
- Test: `scripts/verify_ui_fixes_and_combo_removal.py`
- Test: `scripts/verify_footer_sync.py`
- Test: `scripts/verify_header_footer_pagination.py`
- Test: `scripts/verify_no_product_specs.py`

- [ ] **Step 1: Chạy `verify_implementation.py` đảm bảo 66/66 checks PASS**
- [ ] **Step 2: Chạy `scripts/verify_ui_fixes_and_combo_removal.py` đảm bảo 8/8 checks PASS**
- [ ] **Step 3: Chạy `scripts/verify_footer_sync.py` đảm bảo 144/144 checks PASS**
- [ ] **Step 4: Chạy `scripts/verify_no_product_specs.py` đảm bảo PASS 100%**
- [ ] **Step 5: Kiểm tra trực quan giao diện thẻ sản phẩm trên trình duyệt**
- [ ] **Step 6: Cập nhật tài liệu và báo cáo kết quả**
