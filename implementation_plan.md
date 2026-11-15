# Kế Hoạch Triển Khai: Nút Thêm Câu Hỏi FAQ Mới Chỉ Hiện Thông Báo

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Chuyển đổi hành vi nút "Thêm Câu Hỏi Mới" trong Quản lý FAQ tại Admin (`admin/settings.html` & `js/app.js`) chỉ hiển thị thông báo Toast thành công, không thay đổi DOM danh sách và giữ nguyên dữ liệu câu #1 trên form.

**Architecture:** Pure Static HTML5 / Vanilla JS. Giữ nguyên kiến trúc tĩnh, không phụ thuộc thư viện ngoài.

**Tech Stack:** HTML5, CSS3, Vanilla JavaScript, Python test suites.

## Global Constraints

- Không tự động chạy `git push`. Toàn bộ commit thực hiện cục bộ.
- 100% Pure Static Architecture: Không làm thay đổi layout hay gãy vỡ giao diện.
- Test Suite Integrity: Duy trì 100% PASS cho tất cả các test suites hiện có.

---

### Task 1: Cập Nhật Script Kiểm Thử TDD `scripts/verify_faq_edit_save_and_orders_link.py` (Red Phase)

**Files:**
- Modify: `scripts/verify_faq_edit_save_and_orders_link.py`

- [x] **Step 1: Bổ sung kiểm thử cho `handleAdminAddFaq` chỉ hiển thị Toast thành công**
  - Kiểm tra `handleAdminAddFaq` kích hoạt thông báo `"Đã thêm câu hỏi thường gặp mới thành công!"`.
  - Kiểm tra `handleAdminAddFaq` không xóa form inputs.
- [x] **Step 2: Chạy kiểm thử để xác nhận trạng thái thất bại (Red Phase)**
  Run: `python scripts/verify_faq_edit_save_and_orders_link.py`
  Expected: FAIL hoặc phát hiện hành vi cũ chưa đáp ứng.

---

### Task 2: Cập Nhật Hàm `handleAdminAddFaq` Trong `js/app.js`

**Files:**
- Modify: `js/app.js`

- [x] **Step 1: Rút gọn `handleAdminAddFaq` chỉ hiển thị thông báo Toast thành công**
  ```javascript
  function handleAdminAddFaq(e) {
    if (e && typeof e.preventDefault === 'function') e.preventDefault();
    showToast('Đã thêm câu hỏi thường gặp mới thành công!', 'success');
    return false;
  }
  ```
- [x] **Step 2: Chạy kiểm thử `scripts/verify_faq_edit_save_and_orders_link.py` (Green Phase)**
  Run: `python scripts/verify_faq_edit_save_and_orders_link.py`
  Expected: PASS 100%.

---

### Task 3: Cập Nhật Script `scripts/verify_admin_features_update.py`

**Files:**
- Modify: `scripts/verify_admin_features_update.py`

- [x] **Step 1: Cập nhật runtime test trong `scripts/verify_admin_features_update.py` để khớp với hành vi mới**
  - Xác nhận `handleAdminAddFaq` kích hoạt toast thông báo và giữ nguyên DOM.
- [x] **Step 2: Chạy kiểm thử `scripts/verify_admin_features_update.py`**
  Run: `python scripts/verify_admin_features_update.py`
  Expected: PASS 51/51.

---

### Task 4: Chạy Toàn Bộ Test Suites Hồi Quy & Thực Hiện Code Review

**Files:**
- Test: `scripts/verify_faq_edit_save_and_orders_link.py`
- Test: `scripts/verify_admin_features_update.py`
- Test: `verify_implementation.py`
- Test: `scripts/verify_price_formatting.py`
- Test: `scripts/verify_footer_sync.py`
- Test: `scripts/verify_sidebar_filter_sync.py`
- Test: `scripts/verify_admin_kpi_brand_wording.py`

- [x] **Step 1: Chạy tất cả test suites đảm bảo không hồi quy (100% PASS)**
- [x] **Step 2: Chạy `/code-review` kiểm tra 2 trục Standards & Spec**
- [x] **Step 3: Commit cục bộ**
  `git add js/app.js scripts/verify_admin_features_update.py scripts/verify_faq_edit_save_and_orders_link.py docs/superpowers/ implementation_plan.md`
  `git commit -m "fix(admin): make faq add button toast-only preserving dom and form state"`
