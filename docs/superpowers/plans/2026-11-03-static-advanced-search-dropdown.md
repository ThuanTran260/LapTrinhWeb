# Kế Hoạch Triển Khai: Khôi Phục Giao Diện Thả Xuống Danh Sách Lon Nước Tĩnh Cho Tìm Kiếm Nâng Cao

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Khôi phục giao diện menu thả xuống hiển thị danh sách các lon nước mẫu (`#adv-search-suggestions`) khi người dùng click/focus vào ô nhập từ khóa trong modal Tìm Kiếm Nâng Cao (`#modal-adv-search` trên `index.html`), bảo đảm giao diện thuần tĩnh (không chạy code lọc mảng theo ký tự gõ theo rubric).

**Architecture:** Pure Static HTML5 / Vanilla JavaScript. 
- `index.html`: Khôi phục `#adv-search-suggestions` trong `.adv-search-input-wrapper` và gắn `onfocus="openAdvSuggestions()"`, `onclick="openAdvSuggestions()"`, `oninput="openAdvSuggestions()"`.
- `js/app.js`: Cập nhật `openAdvSuggestions()`, `selectAdvSearchSuggestion(idx)`, `closeAdvSuggestions()`, `handleAdvKeywordInput(val)` để luôn render danh sách lon nước mẫu cố định tĩnh từ `STATIC_PRODUCTS_CATALOG` mà không lọc theo chuỗi gõ.

**Tech Stack:** HTML5, CSS3, Vanilla JavaScript, Python 3 test suites.

## Global Constraints

- 100% Pure Static Architecture: Hoạt động trực tiếp trên file:// và GitHub Pages.
- Static Drink Cans List: Danh sách thả xuống luôn hiển thị danh sách lon nước mẫu tĩnh đẹp mắt, không lọc mảng động theo từng ký tự gõ, bảo đảm tiêu chí chấm đồ án tĩnh.
- Test Suite Integrity: Giữ vững 8/8 PASS trong `scripts/verify_order_detail_pages.py`, 66/66 PASS trong `verify_implementation.py`, và 10/10 PASS trong `scripts/verify_admin_ui_mockup.py`.
- STRICT RULE 1: Tuyệt đối không tự động chạy `git push`. Toàn bộ commit thực hiện cục bộ.

---

### Task 1: Khôi Phục Cấu Trúc Dropdown & Sự Kiện Tương Tác Trong `index.html`

**Files:**
- Modify: `index.html` (vùng `.adv-search-input-wrapper` trong `#modal-adv-search`)

- [x] **Step 1: Khôi phục `<div id="adv-search-suggestions" class="adv-search-suggestions"></div>` ngay sau `#adv-search-keyword`**
- [x] **Step 2: Gắn sự kiện `onfocus="openAdvSuggestions()"`, `onclick="openAdvSuggestions()"`, `oninput="openAdvSuggestions()"` vào `#adv-search-keyword`**
- [x] **Step 3: Kiểm tra cấu trúc DOM hợp lệ**

---

### Task 2: Triển Khai Logic Dropdown Tĩnh Đầy Đủ Lon Nước Trong `js/app.js`

**Files:**
- Modify: `js/app.js` (khu vực các hàm `handleAdvKeywordInput`, `openAdvSuggestions`, `selectAdvSearchSuggestion`, `closeAdvSuggestions`)

- [x] **Step 1: Viết hàm `renderAdvSuggestions()` hoặc cập nhật `openAdvSuggestions()` để nạp danh sách lon nước mẫu tĩnh** (đầy đủ các lon đại diện: Monster Original, Monster Ultra White, Redbull Original, Redbull Thái Lan, Sting Dâu Tây, Sting Vàng) có ảnh thumbnail `SITE_ROOT`, tên lon, thương hiệu và giá.
- [x] **Step 2: Đảm bảo khi gõ phím (`handleAdvKeywordInput` / `oninput`), danh sách lon nước mẫu vẫn hiển thị đầy đủ, không lọc mảng theo text** (đáp ứng đúng tiêu chí đồ án tĩnh).
- [x] **Step 3: Cập nhật `selectAdvSearchSuggestion(idx)`: điền tên lon vào input, đồng bộ chọn thương hiệu và khoảng giá, cập nhật thẻ `#adv-search-preview` và đóng dropdown**
- [x] **Step 4: Kiểm tra đóng dropdown khi click outside hoặc bấm Escape**
- [ ] **Step 5: Commit cục bộ an toàn (`feat(search): restore static drink cans dropdown in advanced search`)** (Chờ Parent Agent yêu cầu)

---

### Task 3: Kiểm Thử Toàn Diện Hệ Thống & Nghiệm Thu

**Files:**
- Test: `scripts/verify_order_detail_pages.py`
- Test: `verify_implementation.py`
- Test: `scripts/verify_admin_ui_mockup.py`

- [x] **Step 1: Chạy `python scripts/verify_order_detail_pages.py` -> Đảm bảo 8/8 PASS**
- [x] **Step 2: Chạy `python verify_implementation.py` -> Đảm bảo 66/66 PASS**
- [x] **Step 3: Chạy `python scripts/verify_admin_ui_mockup.py` -> Đảm bảo 10/10 PASS**
- [ ] **Step 4: Cập nhật walkthrough artifact và báo cáo nghiệm thu**
