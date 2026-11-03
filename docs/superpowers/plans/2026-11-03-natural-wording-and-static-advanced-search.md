# Kế Hoạch Triển Khai: Chuyển Tìm Kiếm Nâng Cao Về Tĩnh & Chuẩn Hóa Thông Báo Tự Nhiên

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Chuyển tính năng Tìm Kiếm Nâng Cao (`#modal-adv-search`) về dạng giao diện tĩnh hoàn toàn (không chạy thuật toán lọc mảng khi gõ phím), đồng thời rà soát và loại bỏ sạch sẽ các từ mang tính chất "mô phỏng / demo tĩnh / rubric" trong các thông báo Toast và văn bản UI, thay bằng ngôn từ thực tế chuyên nghiệp.

**Architecture:** Pure Static HTML5 / Vanilla JavaScript. Loại bỏ code event listener gõ phím lọc mảng trong `index.html` và `js/app.js`. Chuẩn hóa văn bản toast và title trong `js/app.js`, `pages/cart.html`, `admin/revenue.html`, `admin/settings.html`.

**Tech Stack:** HTML5, CSS3, Vanilla JavaScript, Python 3 test suites.

## Global Constraints

- 100% Pure Static Architecture: Không chạy code lọc mảng ngầm khi gõ từ khóa tìm kiếm nâng cao.
- Clean Professional Wording: Tuyệt đối không xuất hiện các từ "mô phỏng", "demo tĩnh", "theo rubric" trong các thông báo Toast hiển thị cho người dùng và các nhãn UI.
- Test Suite Integrity: Giữ vững 66/66 PASS trong `verify_implementation.py`, 10/10 PASS trong `scripts/verify_admin_ui_mockup.py`, và 8/8 PASS trong `scripts/verify_order_detail_pages.py`.
- STRICT RULE 1: Tuyệt đối không tự động chạy `git push`. Toàn bộ commit thực hiện cục bộ.

---

### Task 1: Chuyển Tìm Kiếm Nâng Cao Về Giao Diện Tĩnh & Thông Báo Tự Nhiên

**Files:**
- Modify: `index.html:980-1025`
- Modify: `js/app.js:1320-1410`

- [ ] **Step 1: Gỡ bỏ `oninput` và `onfocus` gọi `handleAdvKeywordInput` trong `index.html`**
- [ ] **Step 2: Dọn dẹp gợi ý dropdown động `#adv-search-suggestions` trong `index.html`**
- [ ] **Step 3: Cập nhật hàm `handleAdvancedSearch(e)` trong `js/app.js` hiển thị toast tự nhiên: `"Đã áp dụng bộ lọc nâng cao cho danh mục sản phẩm!"`**
- [ ] **Step 4: Kiểm tra và tạo commit cục bộ an toàn**

---

### Task 2: Chuẩn Hóa Toàn Bộ Thông Báo Toast & Văn Bản UI (Xóa "Mô Phỏng / Demo Tĩnh")

**Files:**
- Modify: `js/app.js` (dòng 617, 1681, 1724, 1768, 1770, 1832)
- Modify: `pages/cart.html` (dòng 6, 104, 132, 160)
- Modify: `admin/revenue.html` (dòng 57, 61)
- Modify: `admin/settings.html` (dòng 57, 77)

- [ ] **Step 1: Cập nhật 6 câu Toast trong `js/app.js` loại bỏ "(Mô phỏng)"**
- [ ] **Step 2: Cập nhật `pages/cart.html` đổi tiêu đề và thông báo nút xóa thành tự nhiên**
- [ ] **Step 3: Cập nhật `admin/revenue.html` và `admin/settings.html` loại bỏ "demo tĩnh"**
- [ ] **Step 4: Tạo commit cục bộ an toàn**

---

### Task 3: Kiểm Thử Toàn Diện Hệ Thống & Nghiệm Thu

**Files:**
- Test: `scripts/verify_order_detail_pages.py`
- Test: `verify_implementation.py`
- Test: `scripts/verify_admin_ui_mockup.py`

- [ ] **Step 1: Chạy `python scripts/verify_order_detail_pages.py` -> Đảm bảo 8/8 PASS**
- [ ] **Step 2: Chạy `python verify_implementation.py` -> Đảm bảo 66/66 PASS**
- [ ] **Step 3: Chạy `python scripts/verify_admin_ui_mockup.py` -> Đảm bảo 10/10 PASS**
- [ ] **Step 4: Cập nhật walkthrough artifact và báo cáo nghiệm thu**
