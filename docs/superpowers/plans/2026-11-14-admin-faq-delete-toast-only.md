# Kế Hoạch Triển Khai: Nút Xóa FAQ Chỉ Hiện Thông Báo (DOM Giữ Nguyên)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tinh chỉnh nút xóa câu hỏi FAQ trong `admin/settings.html` (`handleAdminDeleteFaq` trong `js/app.js`) để khi bấm chỉ hiển thị thông báo toast mà không xóa phần tử khỏi DOM, đồng bộ chuẩn quy tắc của toàn dự án.

**Architecture:** Pure Static HTML5 / Vanilla JS. Giữ nguyên kiến trúc tĩnh, không phụ thuộc thư viện ngoài.

**Tech Stack:** HTML5, CSS3, Vanilla JavaScript, Python test suites.

## Global Constraints

- Không tự động chạy `git push`. Toàn bộ commit thực hiện cục bộ.
- 100% Pure Static Architecture: Không làm thay đổi layout hay gãy vỡ giao diện.
- Test Suite Integrity: Duy trì 100% PASS cho tất cả các test suites hiện có.

---

### Task 1: Cập Nhật Script Kiểm Thử `scripts/verify_admin_features_update.py` (Red Phase)

**Files:**
- Modify: `scripts/verify_admin_features_update.py:302-305`

- [ ] **Step 1: Cập nhật kiểm tra Node.js runtime của `handleAdminDeleteFaq`**
  - Xác nhận rằng sau khi gọi `handleAdminDeleteFaq`, độ dài danh sách `faqList.children.length` không đổi (DOM giữ nguyên) và có phát ra thông báo Toast tương ứng.
- [ ] **Step 2: Chạy kiểm thử để xác nhận trạng thái thất bại ban đầu (Red Phase)**
  Run: `python scripts/verify_admin_features_update.py`
  Expected: FAIL vì hiện tại hàm vẫn đang xóa phần tử khỏi DOM.
- [ ] **Step 3: Commit cục bộ script test**
  `git add scripts/verify_admin_features_update.py`
  `git commit -m "test(admin): update faq delete verification to assert dom preservation and toast emission"`

---

### Task 2: Cập Nhật Hàm `handleAdminDeleteFaq` Trong `js/app.js` (Green Phase)

**Files:**
- Modify: `js/app.js:3348-3356`
- Test: `scripts/verify_admin_features_update.py`

- [ ] **Step 1: Bỏ lệnh `item.remove()` trong hàm `handleAdminDeleteFaq`**
  - Giữ nguyên DOM, chỉ gọi `showToast('Đã xóa câu hỏi FAQ #' + cleanId + ' khỏi danh sách hiển thị!', 'info')`.
- [ ] **Step 2: Chạy script `scripts/verify_admin_features_update.py` (Green Phase)**
  Run: `python scripts/verify_admin_features_update.py`
  Expected: PASS 51/51.
- [ ] **Step 3: Commit cục bộ**
  `git add js/app.js`
  `git commit -m "fix(admin): make faq delete button toast-only preserving dom structure"`

---

### Task 3: Kiểm Thử Toàn Diện Hệ Thống & Nghiệm Thu Hồi Quy

**Files:**
- Test: `scripts/verify_admin_features_update.py`
- Test: `verify_implementation.py`
- Test: `scripts/verify_price_formatting.py`
- Test: `scripts/verify_clean_brand_pills_and_kicker.py`
- Test: `scripts/verify_footer_sync.py`
- Test: `scripts/verify_sidebar_filter_sync.py`
- Test: `scripts/verify_admin_kpi_brand_wording.py`
- Test: `scripts/verify_no_product_specs.py`

- [ ] **Step 1: Chạy tất cả test suites đảm bảo không hồi quy**
- [ ] **Step 2: Cập nhật tài liệu và báo cáo kết quả**
