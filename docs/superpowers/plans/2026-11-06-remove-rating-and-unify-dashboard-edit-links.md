# Kế Hoạch Triển Khai: Loại Bỏ Đánh Giá Hệ Thống & Đồng Bộ Nút Chỉnh Sửa Dashboard Về Edit Monster

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Loại bỏ dòng thông tin không cần thiết `<div><strong>Đánh giá hệ thống:</strong> 5.0 ⭐ (Top 1 Doanh số)</div>` trên các trang chỉnh sửa sản phẩm admin, đồng thời đồng bộ các nút "Chỉnh Sửa" của dòng sản phẩm Redbull và Sting tại bảng Quản Lý Kho trên Dashboard (`admin/index.html`) trỏ thẳng về `edit-monster.html` tương tự các lon Monster ở trên.

**Architecture:** Pure Static HTML5 / Vanilla JavaScript. 
- Sửa đổi trực tiếp mã nguồn HTML tĩnh: loại bỏ dòng đánh giá ở thẻ xem trước bên trái của các trang `admin/edit-*.html`.
- Trong `admin/index.html`: cập nhật thuộc tính `href` của 6 nút chỉnh sửa Redbull và Sting trong bảng `#inventory-section` từ các link riêng lẻ thành `edit-monster.html`.
- Giữ nguyên `admin/inventory.html` để duy trì trọn vẹn 100% PASS cho bộ test chuyên biệt `scripts/verify_order_detail_pages.py` (Test 5: Parity brand edit links).

**Tech Stack:** HTML5, CSS3, Python test suites.

## Global Constraints

- 100% Pure Static Architecture: Không làm thay đổi layout hay gãy vỡ giao diện.
- Test Suite Integrity: Giữ vững 8/8 PASS trong `scripts/verify_order_detail_pages.py`, 66/66 PASS trong `verify_implementation.py`, và 10/10 PASS trong `scripts/verify_admin_ui_mockup.py`.
- STRICT RULE 1: Tuyệt đối không tự động chạy `git push`. Toàn bộ commit thực hiện cục bộ.

---

### Task 1: Loại Bỏ Dòng "Đánh Giá Hệ Thống" Khỏi Các Trang Chỉnh Sửa Sản Phẩm

**Files:**
- Modify: `admin/edit-monster.html:91`
- Modify: `admin/edit-redbull-original.html:91`
- Modify: `admin/edit-redbull-thai.html:92`
- Modify: `admin/edit-redbull-lonvua.html:92`
- Modify: `admin/edit-sting.html:91`

- [ ] **Step 1: Xóa dòng `<div><strong>Đánh giá hệ thống:</strong> 5.0 ⭐ (Top 1 Doanh số)</div>` trong `admin/edit-monster.html`**
- [ ] **Step 2: Xóa dòng "Đánh giá hệ thống" tương tự trong 4 trang còn lại (`edit-redbull-original.html`, `edit-redbull-thai.html`, `edit-redbull-lonvua.html`, `edit-sting.html`) để đảm bảo tính đồng bộ sạch đẹp trên toàn hệ thống**
- [ ] **Step 3: Kiểm tra cấu trúc thẻ tóm tắt sản phẩm vẫn cân đối, hiển thị SKU, Thương hiệu, Tồn kho hiện tại, Đã bán tháng này**
- [ ] **Step 4: Commit cục bộ an toàn (`chore(admin): remove unnecessary system rating from product edit pages`)**

---

### Task 2: Đồng Bộ Nút Chỉnh Sửa Trong Bảng Kho Dashboard (`admin/index.html`) Về `edit-monster.html`

**Files:**
- Modify: `admin/index.html:360-440` (Bảng `#inventory-section` trong Dashboard)

- [ ] **Step 1: Cập nhật nút Chỉnh sửa của 3 sản phẩm Redbull:**
  - Redbull Original 250ml: đổi `href="edit-redbull-original.html"` thành `href="edit-monster.html"`
  - Redbull Thái Lan 250ml: đổi `href="edit-redbull-thai.html"` thành `href="edit-monster.html"`
  - Redbull Nắp Bật 250ml: đổi `href="edit-redbull-lonvua.html"` thành `href="edit-monster.html"`
- [ ] **Step 2: Cập nhật nút Chỉnh sửa của 3 sản phẩm Sting:**
  - Sting Dâu Tây Đỏ 330ml: đổi `href="edit-sting.html"` thành `href="edit-monster.html"`
  - Sting Vàng Sleek 330ml: đổi `href="edit-sting.html"` thành `href="edit-monster.html"`
  - Sting Blue Sleek 320ml: đổi `href="edit-sting.html"` thành `href="edit-monster.html"`
- [ ] **Step 3: Xác minh cả 10 lon nước trong bảng kho Dashboard đều trỏ đồng nhất về `edit-monster.html`**
- [ ] **Step 4: Commit cục bộ an toàn (`feat(dashboard): point all inventory edit buttons to edit-monster.html`)**

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
