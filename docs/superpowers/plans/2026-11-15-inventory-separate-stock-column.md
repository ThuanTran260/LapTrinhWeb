# Kế Hoạch Triển Khai: Tách Tồn Kho Thành Cột Riêng Biệt Trong Bảng Kho Admin

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tách số lượng tồn kho thành một cột riêng (`<th>Tồn Kho</th>`) nằm ngay trước cột Trạng Thái (`<th>Trạng Thái</th>`) trong bảng kho của `admin/inventory.html` và `admin/index.html`.

**Architecture:** Pure Static HTML5 / CSS3. Giữ nguyên kiến trúc tĩnh, không phụ thuộc thư viện ngoài.

**Tech Stack:** HTML5, CSS3, Python test suites.

## Global Constraints

- Không tự động chạy `git push`. Toàn bộ commit thực hiện cục bộ.
- 100% Pure Static Architecture: Không làm thay đổi layout hay gãy vỡ giao diện bảng.
- Test Suite Integrity: Duy trì 100% PASS cho tất cả các test suites hiện có.

---

### Task 1: Cập Nhật Bảng Kho Trong `admin/inventory.html`

**Files:**
- Modify: `admin/inventory.html` (`<thead>` & 10 hàng sản phẩm)

- [x] **Step 1: Thêm cột `<th>Tồn Kho</th>` vào `<thead>` trước `<th>Trạng Thái</th>`**
- [x] **Step 2: Tách ô dữ liệu thành 2 thẻ `<td>` riêng cho 10 sản phẩm**
  - Cột Tồn Kho: `<span style="color: #FFF; font-weight: 700; font-size: 0.92rem; white-space: nowrap;"><i class="fas fa-box" style="color: var(--primary); margin-right: 6px;"></i>{QTY} <small style="color: var(--text-muted); font-size: 0.8rem; font-weight: 500;">lon</small></span>`
  - Cột Trạng Thái: `<span class="badge-status success">CÒN HÀNG</span>`
- [x] **Step 3: Kiểm tra trực quan bằng `git diff`**

---

### Task 2: Cập Nhật Bảng Kho Trong `admin/index.html`

**Files:**
- Modify: `admin/index.html` (`<thead>` & 10 hàng sản phẩm)

- [x] **Step 1: Thêm cột `<th>Tồn Kho</th>` vào `<thead>` trước `<th>Trạng Thái</th>`**
- [x] **Step 2: Tách ô dữ liệu thành 2 thẻ `<td>` riêng cho 10 sản phẩm tương tự**
- [x] **Step 3: Kiểm tra trực quan bằng `git diff`**

---

### Task 3: Cập Nhật Script Kiểm Thử `scripts/verify_admin_features_update.py`

**Files:**
- Modify: `scripts/verify_admin_features_update.py`

- [x] **Step 1: Cập nhật hàm `verify_stock_qty` trong `scripts/verify_admin_features_update.py`**
  - Xác nhận bảng có cột `<th>Tồn Kho</th>` và `<th>Trạng Thái</th>`.
  - Xác nhận ô số lượng có icon `fas fa-box` và đơn vị `<small ...>lon</small>`.
  - Giữ nguyên các assert về số lượng tồn kho từng sản phẩm (Monster 1.250 lon, Redbull 680, 450, 520 lon, Sting 890, 740, 610 lon).
- [x] **Step 2: Chạy kiểm thử xác nhận đạt 51/51 PASS**
  Run: `python scripts/verify_admin_features_update.py`
  Expected: PASS 51/51.

---

### Task 4: Chạy Toàn Bộ Test Suites Hồi Quy & Thực Hiện Code Review

**Files:**
- Test: `scripts/verify_admin_features_update.py`
- Test: `scripts/verify_faq_edit_save_and_orders_link.py`
- Test: `verify_implementation.py`
- Test: `scripts/verify_price_formatting.py`
- Test: `scripts/verify_footer_sync.py`
- Test: `scripts/verify_sidebar_filter_sync.py`
- Test: `scripts/verify_admin_kpi_brand_wording.py`

- [ ] **Step 1: Chạy tất cả test suites đảm bảo không hồi quy (100% PASS)**
- [ ] **Step 2: Chạy `/code-review` kiểm tra 2 trục Standards & Spec**
- [ ] **Step 3: Commit cục bộ**
  `git add admin/inventory.html admin/index.html scripts/verify_admin_features_update.py docs/superpowers/ implementation_plan.md`
  `git commit -m "feat(admin): make inventory stock a separate dedicated column next to status"`
