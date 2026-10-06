# Sting Brand Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tích hợp thương hiệu Sting (3 lon nước: Dâu Đỏ, Vàng Nhân Sâm, Xanh Blue Việt Quất) vào giao diện Dark Neon của Energy Boost Store, bao gồm tách nền ảnh trong suốt, thêm menu & section trang chủ, tạo trang chi tiết sản phẩm chuẩn, và đồng bộ dữ liệu với Admin.

**Architecture:** Xử lý asset hình ảnh RGBA WebP không viền trắng từ `assets/images/sting/`. Mở rộng `index.html` với Menu thương hiệu thứ 3 và Section sản phẩm `#sting-products`. Xây dựng trang chi tiết `pages/product-detail-sting.html`. Đồng bộ `PRODUCT_DATA_REGISTRY` trong `js/app.js` và bảng tồn kho tại `admin/inventory.html` & `admin/index.html`.

**Tech Stack:** Pure HTML5, CSS3 (Dark Neon Glassmorphism, CSS Custom Properties), Vanilla JavaScript (ES6+), Python PIL (Image Matte Extraction).

## Global Constraints

- Tuân thủ quy định Git Rule 1: Tuyệt đối không chạy `git push`, chỉ commit cục bộ trên nhánh `feat/energy-boost-rebrand`.
- Giữ vững toàn bộ 66/66 test cases của `verify_implementation.py` (bao gồm nav menu không có các pill cấm, footer giữ link giỏ hàng và punch shots).
- Nền ảnh lon nước Sting phải là WebP trong suốt RGBA, hiển thị mượt mà trên nền đen `#141820` không còn viền trắng.
- Tất cả đường dẫn liên kết giữa Storefront và Admin phải chuẩn xác theo hệ thống tương đối (`SITE_ROOT`, `pages/`, `admin/`).

---

### Task 1: Asset Pipeline - Tách Nền Trong Suốt Cho 3 Lon Sting

**Files:**
- Create/Modify: `assets/images/sting/sting-dau.webp`
- Create/Modify: `assets/images/sting/sting-gold.webp`
- Create/Modify: `assets/images/sting/sting-vietquat.webp`

- [ ] **Step 1: Viết script Python tách nền flood-fill alpha matte cho 3 file trong `assets/images/sting/`**
- [ ] **Step 2: Chạy script và kiểm tra kích thước, kênh RGBA, các góc trong suốt (Alpha = 0)**
- [ ] **Step 3: Kiểm tra dung lượng file nhẹ (~40-70KB) và commit hình ảnh mới**

---

### Task 2: Storefront UI - Cập Nhật Menu & Section Danh Mục Sting Trên `index.html`

**Files:**
- Modify: `index.html`

- [ ] **Step 1: Thêm nút Sting vào `<ul class="nav-menu">`**
  ```html
  <li><a href="#sting-products" class="nav-link"><i class="fas fa-bolt" style="color: #FF0055;"></i> Sting</a></li>
  ```
- [ ] **Step 2: Tạo Section `#sting-products` ngay sau Section `#redbull-products`**
  Gồm tiêu đề thương hiệu Suntory PepsiCo và 3 thẻ sản phẩm (`Sting Dâu Đỏ 330ml`, `Sting Vàng 330ml`, `Sting Xanh Blue 320ml`) với hiệu ứng Neon glow riêng biệt.
- [ ] **Step 3: Gắn liên kết click ảnh/tiêu đề/nút chi tiết trỏ về `pages/product-detail-sting.html` và nút thêm giỏ hàng có Toast**
- [ ] **Step 4: Chạy `python verify_implementation.py` để xác nhận kiểm thử vẫn PASS 100%**

---

### Task 3: Product Detail - Xây Dựng Trang Chi Tiết `pages/product-detail-sting.html`

**Files:**
- Create: `pages/product-detail-sting.html`

- [ ] **Step 1: Khởi tạo trang chi tiết Sting Dâu Đỏ Sleek 330ml chuẩn giao diện Dark Neon**
- [ ] **Step 2: Đặt 1 ảnh lon đại diện trong suốt duy nhất dưới lon nước chính**
- [ ] **Step 3: Cập nhật thông số kỹ thuật (330ml, Suntory PepsiCo, Nhân sâm & Vitamin B, 12.000đ)**
- [ ] **Step 4: Thiết lập mục sản phẩm liên quan gồm Sting Vàng, Sting Blue, Monster Original và Redbull Original**

---

### Task 4: Admin Sync - Đồng Bộ Dữ Liệu Quản Trị & Data Registry

**Files:**
- Modify: `js/app.js`
- Modify: `admin/inventory.html`
- Modify: `admin/index.html`

- [ ] **Step 1: Bổ sung 3 sản phẩm Sting vào `PRODUCT_DATA_REGISTRY` trong `js/app.js`**
  (`sting-dau`, `sting-gold`, `sting-blue` với đầy đủ tên, giá, thương hiệu, nguồn gốc, thành phần).
- [ ] **Step 2: Thêm 3 dòng sản phẩm Sting vào bảng Quản lý kho trong `admin/inventory.html`**
- [ ] **Step 3: Thêm 3 dòng sản phẩm Sting vào bảng Quản lý kho trong `admin/index.html`**
- [ ] **Step 4: Kiểm tra mở Modal chỉnh sửa nhanh sản phẩm Sting hoạt động chính xác**

---

### Task 5: Verification & Local Git Commit

- [ ] **Step 1: Chạy `python verify_implementation.py` đảm bảo 66/66 checks PASS**
- [ ] **Step 2: Kiểm tra thủ công giao diện trang chủ, trang chi tiết Sting, và trang quản trị Admin**
- [ ] **Step 3: Git add và git commit cục bộ trên nhánh `feat/energy-boost-rebrand`**
