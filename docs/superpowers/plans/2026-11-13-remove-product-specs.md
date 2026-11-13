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

**Interfaces:**
- Consumes: Cấu trúc tệp `index.html`, `pages/search-results.html`, `js/app.js`.
- Produces: Test script tự động kiểm tra số lượng khối `.product-specs` (yêu cầu = 0).

- [ ] **Step 1: Viết test script `scripts/verify_no_product_specs.py`**
  Script kiểm tra:
  1. `index.html` có 0 thẻ chứa class `product-specs`.
  2. `pages/search-results.html` có 0 thẻ chứa class `product-specs`.
  3. `js/app.js` không còn chuỗi `<div class="product-specs">`.
  4. Vẫn bảo toàn đủ 14 thẻ sản phẩm với `btn-add-stitch` và liên kết điều hướng trong `index.html`.
- [ ] **Step 2: Chạy kiểm thử để xác nhận trạng thái thất bại ban đầu (Red Phase)**
  Run: `python scripts/verify_no_product_specs.py`
  Expected: FAIL vì hiện tại `index.html` có 14 thẻ, `search-results.html` có 1 thẻ, `js/app.js` có 1 thẻ `product-specs`.
- [ ] **Step 3: Commit cục bộ script test**
  `git add scripts/verify_no_product_specs.py`
  `git commit -m "test(specs): add automated verification for product specs removal"`

---

### Task 2: Loại Bỏ Khối `.product-specs` Khỏi 14 Thẻ Sản Phẩm Trong `index.html`

**Files:**
- Modify: `index.html:328-424,670-940`
- Test: `scripts/verify_no_product_specs.py`

**Interfaces:**
- Consumes: 14 thẻ sản phẩm trong `index.html` (4 Flash Sale + 10 Brand sections).
- Produces: 14 thẻ sản phẩm gọn gàng, sạch sẽ, không còn khối `<div class="product-specs">...</div>`.

- [ ] **Step 1: Xóa khối `.product-specs` khỏi 4 thẻ sản phẩm Flash Sale**
  - Monster Original 355ml
  - Redbull Original 250ml
  - Monster Zero Ultra White 500ml
  - Redbull Nắp Bật 250ml
- [ ] **Step 2: Xóa khối `.product-specs` khỏi 4 thẻ thương hiệu Monster Energy**
  - Monster Original 355ml
  - Monster Zero Ultra White
  - Monster Ultra Paradise
  - Monster Pipeline Punch
- [ ] **Step 3: Xóa khối `.product-specs` khỏi 3 thẻ thương hiệu Redbull Thái Lan**
  - Redbull Original 250ml
  - Redbull Thái Lan 250ml
  - Redbull Nắp Bật 250ml
- [ ] **Step 4: Xóa khối `.product-specs` khỏi 3 thẻ thương hiệu Sting PepsiCo**
  - Sting Dâu Tây Đỏ 330ml
  - Sting Vàng Sleek 330ml
  - Sting Blue Sleek 320ml
- [ ] **Step 5: Kiểm tra xác minh `index.html` không còn bất kỳ thẻ `product-specs` nào**
- [ ] **Step 6: Commit cục bộ**
  `git add index.html`
  `git commit -m "fix(storefront): remove hardcoded product-specs from all 14 product cards in index.html"`

---

### Task 3: Loại Bỏ Khối `.product-specs` Khỏi `pages/search-results.html` và `js/app.js`

**Files:**
- Modify: `pages/search-results.html:409-412`
- Modify: `js/app.js:2034-2037`
- Test: `scripts/verify_no_product_specs.py`

**Interfaces:**
- Consumes: Mã nguồn HTML trang tìm kiếm và file script điều khiển.
- Produces: Giao diện thẻ kết quả tìm kiếm và template JS đồng bộ không còn `.product-specs`.

- [ ] **Step 1: Xóa khối `.product-specs` trong `pages/search-results.html`**
- [ ] **Step 2: Xóa khối `.product-specs` trong template HTML của `js/app.js`**
- [ ] **Step 3: Chạy script kiểm thử `scripts/verify_no_product_specs.py` (Green Phase)**
  Run: `python scripts/verify_no_product_specs.py`
  Expected: PASS 100% với 0 thẻ `.product-specs` trên toàn bộ hệ thống.
- [ ] **Step 4: Commit cục bộ**
  `git add pages/search-results.html js/app.js`
  `git commit -m "fix(catalog): remove product-specs from search results page and app.js template"`

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
