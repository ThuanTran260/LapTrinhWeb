# Kế Hoạch Triển Khai: Đồng Bộ Nút Chỉnh Sửa Kho Hàng (`admin/inventory.html`) Về `edit-monster.html`

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Đồng bộ toàn bộ 6 nút "Chỉnh Sửa" của các sản phẩm Redbull và Sting trong bảng kho hàng của trang Kho Nước Tăng Lực (`admin/inventory.html`) sang trỏ về `edit-monster.html`, tạo tính thống nhất tuyệt đối 10/10 lon nước giữa trang Dashboard (`admin/index.html`) và trang Kho hàng (`admin/inventory.html`), đồng thời cập nhật bài test Test 5 đảm bảo 100% PASS.

**Architecture:** Pure Static HTML5 / Vanilla JavaScript. 
- `admin/inventory.html`: Cập nhật thuộc tính `href` của 3 sản phẩm Redbull và 3 sản phẩm Sting từ các trang edit riêng sang `edit-monster.html`.
- `scripts/verify_order_detail_pages.py`: Cập nhật Test 5 (`test_inventory_edit_links`) để kiểm tra toàn bộ các nút Chỉnh sửa trong `admin/inventory.html` đều trỏ thống nhất về `edit-monster.html`.

**Tech Stack:** HTML5, Python test suites.

## Global Constraints

- 100% Pure Static Architecture: Không làm vỡ layout, hoạt động trơn tru trên mọi độ phân giải.
- Test Suite Integrity: Giữ vững 8/8 PASS trong `scripts/verify_order_detail_pages.py`, 66/66 PASS trong `verify_implementation.py`, và 10/10 PASS trong `scripts/verify_admin_ui_mockup.py`.
- STRICT RULE 1: Tuyệt đối không tự động chạy `git push`. Toàn bộ commit thực hiện cục bộ.

---

### Task 1: Đồng Bộ Toàn Bộ Nút Chỉnh Sửa Trong `admin/inventory.html` Về `edit-monster.html`

**Files:**
- Modify: `admin/inventory.html:190-275`
- Modify: `scripts/verify_order_detail_pages.py:120-130`

- [x] **Step 1: Cập nhật 3 nút Chỉnh sửa của Redbull trong `admin/inventory.html` sang `href="edit-monster.html"`**
  - Redbull Original 250ml
  - Redbull Thái Lan 250ml
  - Redbull Nắp Bật 250ml
- [x] **Step 2: Cập nhật 3 nút Chỉnh sửa của Sting trong `admin/inventory.html` sang `href="edit-monster.html"`**
  - Sting Dâu Tây Đỏ 330ml
  - Sting Vàng Sleek 330ml
  - Sting Blue Sleek 320ml
- [x] **Step 3: Cập nhật Test 5 trong `scripts/verify_order_detail_pages.py`**
  - Kiểm tra tiêu đề test và xác minh `admin/inventory.html` có tất cả các nút chỉnh sửa trỏ về `edit-monster.html`.
- [x] **Step 4: Chạy xác minh 3 test suites: `verify_order_detail_pages.py` (8/8), `verify_implementation.py` (66/66), `verify_admin_ui_mockup.py` (10/10)**
- [x] **Step 5: Thực hiện commit cục bộ an toàn (`feat(inventory): point all edit buttons to edit-monster.html`)**

---

### Task 2: Nghiệm Thu Toàn Diện & Cập Nhật Báo Cáo

**Files:**
- Modify: `C:\Users\Admin\.gemini\antigravity\brain\36478f47-6ab1-476a-a2ac-6f3cf0a64610\walkthrough.md`

- [ ] **Step 1: Cập nhật Walkthrough Artifact với tính năng đồng bộ nút Chỉnh sửa kho**
- [ ] **Step 2: Báo cáo kết quả và xác nhận commit an toàn cho người dùng**
