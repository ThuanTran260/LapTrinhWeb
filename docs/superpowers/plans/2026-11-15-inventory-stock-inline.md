# Kế Hoạch Triển Khai: Đưa Số Lượng Tồn Kho Ra Cạnh Badge Trạng Thái

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Chuyển đổi cách hiển thị số lượng tồn kho trong cột trạng thái của bảng kho (`admin/inventory.html` & `admin/index.html`) từ dạng xuống dòng chữ xám mờ sang dạng cùng hàng ngang (inline flex), chữ màu trắng sáng rõ nét kế bên badge "CÒN HÀNG".

**Architecture:** Pure Static HTML5 / CSS3. Giữ nguyên kiến trúc tĩnh, không phụ thuộc thư viện ngoài.

**Tech Stack:** HTML5, CSS3, Python test suites.

## Global Constraints

- Không tự động chạy `git push`. Toàn bộ commit thực hiện cục bộ.
- 100% Pure Static Architecture: Không làm thay đổi layout hay gãy vỡ giao diện bảng.
- Test Suite Integrity: Duy trì 100% PASS cho tất cả các test suites hiện có.

---

### Task 1: Cập Nhật Bảng Kho Trong `admin/inventory.html`

**Files:**
- Modify: `admin/inventory.html` (10 hàng sản phẩm)

- [x] **Step 1: Cập nhật cấu trúc ô trạng thái cho 10 sản phẩm sang `inline-flex`**
  ```html
  <div style="display: inline-flex; align-items: center; gap: 8px; white-space: nowrap;">
    <span class="badge-status success">CÒN HÀNG</span>
    <span style="color: #FFF; font-size: 0.85rem; font-weight: 700;">
      <i class="fas fa-box" style="color: var(--primary); margin-right: 4px;"></i>Tồn: {SO_LUONG} lon
    </span>
  </div>
  ```
- [x] **Step 2: Kiểm tra trực quan bằng `git diff`**

---

### Task 2: Cập Nhật Bảng Kho Trong `admin/index.html`

**Files:**
- Modify: `admin/index.html` (10 hàng sản phẩm)

- [x] **Step 1: Cập nhật cấu trúc ô trạng thái cho 10 sản phẩm sang `inline-flex` tương tự**
- [x] **Step 2: Kiểm tra trực quan bằng `git diff`**

---

### Task 3: Cập Nhật Script Kiểm Thử `scripts/verify_admin_features_update.py`

**Files:**
- Modify: `scripts/verify_admin_features_update.py`

- [x] **Step 1: Cập nhật hàm `verify_stock_qty` trong `scripts/verify_admin_features_update.py`**
  - Xác nhận cấu trúc thẻ `inline-flex` và màu sắc mới `#FFF`.
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
  `git commit -m "feat(admin): display stock quantity inline next to in-stock badge with bright white text"`
