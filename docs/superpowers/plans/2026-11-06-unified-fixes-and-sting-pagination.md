# Kế Hoạch Triển Khai: Căn Giữa Phân Trang Sting, Loại Bỏ Đánh Giá Hệ Thống & Đồng Bộ Chỉnh Sửa Dashboard

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Khắc phục lỗi bố cục đưa thanh phân trang Sting xuống bên dưới căn giữa trang (Phương án 1), loại bỏ dòng thông tin không cần thiết `<div><strong>Đánh giá hệ thống:</strong> 5.0 ⭐ (Top 1 Doanh số)</div>` trên các trang chỉnh sửa sản phẩm admin, và đồng bộ toàn bộ nút "Chỉnh Sửa" của Redbull & Sting tại bảng Dashboard (`admin/index.html`) trỏ thẳng về `edit-monster.html`.

**Architecture:** Pure Static HTML5 / CSS3 / Vanilla JavaScript. 
- `index.html`: Bổ sung thẻ đóng `</div>` cho `.products-grid` ở section Sting để `.pagination-strip` ra khỏi grid, hiển thị độc lập căn giữa trang, cập nhật nút `3` mang class `.active`.
- `admin/edit-*.html`: Xóa bỏ dòng `<div><strong>Đánh giá hệ thống:</strong> ...</div>` khỏi thẻ tóm tắt sản phẩm bên trái trên cả 5 trang chỉnh sửa.
- `admin/index.html`: Cập nhật 6 nút Chỉnh sửa của Redbull và Sting trong bảng kho Dashboard trỏ về `edit-monster.html`.
- Giữ nguyên `admin/inventory.html` để duy trì 100% PASS cho bộ test chuyên biệt `scripts/verify_order_detail_pages.py`.

**Tech Stack:** HTML5, CSS3, Python test suites.

## Global Constraints

- 100% Pure Static Architecture: Không làm vỡ layout, hoạt động trơn tru trên mọi độ phân giải.
- Test Suite Integrity: Giữ vững 8/8 PASS trong `scripts/verify_order_detail_pages.py`, 66/66 PASS trong `verify_implementation.py`, và 10/10 PASS trong `scripts/verify_admin_ui_mockup.py`.
- STRICT RULE 1: Tuyệt đối không tự động chạy `git push`. Toàn bộ commit thực hiện cục bộ.

---

### Task 1: Bố Trí Căn Giữa Thanh Phân Trang Sting Xuống Bên Dưới (`index.html`)

**Files:**
- Modify: `index.html:760-776`

- [ ] **Step 1: Bổ sung thẻ `</div>` đóng cho `<div class="products-grid">` ngay sau thẻ đóng của lon Sting thứ 3**
- [ ] **Step 2: Đưa `<div class="pagination-strip">` ra ngoài lưới `.products-grid`, nằm trực tiếp trong `.container`**
- [ ] **Step 3: Cập nhật nút số `3` mang class `.active` (bỏ class `.active` khỏi nút `1`) vì đang duyệt ở khu vực Sting (Thương hiệu 3)**
- [ ] **Step 4: Kiểm tra trực quan layout đảm bảo thanh phân trang căn giữa cân đối bên dưới 3 lon Sting và trên phần Combo 24 lon**

---

### Task 2: Loại Bỏ Dòng "Đánh Giá Hệ Thống" Khỏi Các Trang Chỉnh Sửa Sản Phẩm

**Files:**
- Modify: `admin/edit-monster.html:91`
- Modify: `admin/edit-redbull-original.html:91`
- Modify: `admin/edit-redbull-thai.html:92`
- Modify: `admin/edit-redbull-lonvua.html:92`
- Modify: `admin/edit-sting.html:91`

- [ ] **Step 1: Xóa dòng `<div><strong>Đánh giá hệ thống:</strong> 5.0 ⭐ (Top 1 Doanh số)</div>` trong `admin/edit-monster.html`**
- [ ] **Step 2: Xóa dòng "Đánh giá hệ thống" tương tự trong 4 trang còn lại (`edit-redbull-original.html`, `edit-redbull-thai.html`, `edit-redbull-lonvua.html`, `edit-sting.html`)**
- [ ] **Step 3: Kiểm tra cấu trúc thẻ tóm tắt sản phẩm bên trái hiển thị gọn gàng với SKU, Thương hiệu, Tồn kho, Đã bán**

---

### Task 3: Đồng Bộ Nút Chỉnh Sửa Trong Bảng Kho Dashboard (`admin/index.html`) Về `edit-monster.html`

**Files:**
- Modify: `admin/index.html:360-440` (Bảng `#inventory-section` trong Dashboard)

- [ ] **Step 1: Đổi thuộc tính `href` của 3 sản phẩm Redbull (Original, Thái Lan, Nắp Bật) thành `edit-monster.html`**
- [ ] **Step 2: Đổi thuộc tính `href` của 3 sản phẩm Sting (Dâu Đỏ, Vàng Sleek, Blue Việt Quất) thành `edit-monster.html`**
- [ ] **Step 3: Xác minh cả 10 lon nước trong bảng kho Dashboard đều trỏ thống nhất về `edit-monster.html`**

---

### Task 4: Kiểm Thử Toàn Diện Hệ Thống & Nghiệm Thu

**Files:**
- Test: `scripts/verify_order_detail_pages.py`
- Test: `verify_implementation.py`
- Test: `scripts/verify_admin_ui_mockup.py`

- [ ] **Step 1: Chạy `python scripts/verify_order_detail_pages.py` -> Đảm bảo 8/8 PASS**
- [ ] **Step 2: Chạy `python verify_implementation.py` -> Đảm bảo 66/66 PASS**
- [ ] **Step 3: Chạy `python scripts/verify_admin_ui_mockup.py` -> Đảm bảo 10/10 PASS**
- [ ] **Step 4: Cập nhật walkthrough artifact và báo cáo nghiệm thu cho người dùng**
