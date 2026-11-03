# Dedicated Pages & UI Polish Implementation Plan: Order Details, Standalone Edit, Text Cleanup & Header Sync

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 
1. Chuyển đổi toàn bộ tính năng "Xem chi tiết đơn hàng" từ Popup Modal sang 2 trang HTML độc lập (`admin/order-detail.html` cho Quản trị viên và `pages/order-detail.html` cho Khách hàng), đọc mã đơn hàng động qua URL param `?id=...`.
2. Xóa triệt để chữ `(TĨNH)` khỏi tiêu đề Quản lý kho và các tiêu đề bảng trên toàn bộ Dashboard, Inventory, Orders, Revenue.
3. Đồng bộ hóa hành vi "Chỉnh sửa sản phẩm" tại Kho Hàng (`admin/inventory.html`): Chuyển từ mở popup modal sang điều hướng trực tiếp vào các trang chỉnh sửa chuyên biệt (`edit-monster.html`, `edit-redbull-*.html`, `edit-sting.html`) đồng nhất 100% với Dashboard `admin/index.html`.
4. Đồng bộ hóa Header & Topbar trên tất cả các trang chi tiết sản phẩm (`pages/product-detail*.html`): Khôi phục nút **Tài khoản** (`#header-account-link`), hiển thị đầy đủ cả 3 nút (Đơn hàng, Tài khoản, Giỏ hàng) và đồng bộ giao diện trang Sting với Monster/Redbull.
5. Bảo toàn 100% kết quả kiểm thử hiện có (`verify_implementation.py` 66/66 PASS, `verify_admin_ui_mockup.py` 10/10 PASS).

**Architecture:** 
Xây dựng 2 trang HTML chi tiết đơn hàng riêng biệt. Đồng bộ các liên kết chỉnh sửa trong `admin/inventory.html` trỏ thẳng sang `edit-*.html`. Xóa các hậu tố `(TĨNH)` trên UI. Đồng bộ cấu trúc `.header-actions` chuẩn 3 nút (Đơn hàng, Tài khoản, Giỏ hàng) trên 5 trang chi tiết sản phẩm. Cập nhật `js/app.js` chứa mock data và helper điều hướng.

**Tech Stack:** HTML5 Semantic, CSS3 Custom Properties (Dark Neon), Vanilla JavaScript (DOM & URLSearchParams), Python 3 Standard Library Test Suites.

## Global Constraints

- 100% Pure Static Website: Không dùng backend server hay CSDL, tương thích hoàn toàn khi host trên GitHub Pages (`thuantran260.github.io/LapTrinhWeb/`).
- Header Uniformity: Mọi trang chi tiết sản phẩm (`product-detail*.html`) phải có cùng một cụm `.header-actions` 3 nút đồng bộ với `index.html`.
- Parity & Consistency: Hành vi click Chỉnh Sửa ở `inventory.html` phải hoàn toàn đồng nhất với `index.html` (đưa ra `edit-monster.html`, `edit-redbull-*.html`, `edit-sting.html`).
- Test Suite Integrity: Giữ vững 66/66 PASS trong `verify_implementation.py` và 10/10 PASS trong `scripts/verify_admin_ui_mockup.py`.
- STRICT RULE 1: Tuyệt đối không tự động chạy `git push`.

---

### Task 1: Đồng Bộ Hóa Header & Khôi Phục Nút Tài Khoản Trên Các Trang Chi Tiết Sản Phẩm

**Files:**
- Modify: `pages/product-detail.html:105-125`
- Modify: `pages/product-detail-redbull.html:105-125`
- Modify: `pages/product-detail-redbull-thai.html:100-120`
- Modify: `pages/product-detail-redbull-lonvua.html:100-120`
- Modify: `pages/product-detail-sting.html:18-35, 105-125`

**Interfaces:**
- Produces: Cụm `.header-actions` chuẩn mực gồm đủ 3 nút:
  1. **Đơn hàng** (`orders.html` kèm icon `fa-receipt`)
  2. **Tài khoản** (`account.html` với `id="header-account-link"` và `id="header-account-value"` để `initAccountHeader()` tự động hiển thị tên người dùng đã đăng nhập)
  3. **Giỏ hàng** (`cart.html` kèm badge số lượng và giá tiền)
  Đồng thời chuẩn hóa Top-bar của trang Sting đồng bộ với Monster và Redbull.

- [ ] **Step 1: Cập nhật `.header-actions` trong `pages/product-detail.html` (Monster)**
- [ ] **Step 2: Cập nhật `.header-actions` trong `pages/product-detail-redbull.html` (Redbull Original)**
- [ ] **Step 3: Cập nhật `.header-actions` trong `pages/product-detail-redbull-thai.html` (Redbull Thái)**
- [ ] **Step 4: Cập nhật `.header-actions` trong `pages/product-detail-redbull-lonvua.html` (Redbull Lon Vừa)**
- [ ] **Step 5: Cập nhật `.top-bar` và `.header-actions` trong `pages/product-detail-sting.html` (Sting Dâu Đỏ)**

---

### Task 2: Xóa Bỏ Chữ "(TĨNH)" Trên Các Tiêu Đề Giao Diện Admin

**Files:**
- Modify: `admin/index.html:113, 271`
- Modify: `admin/inventory.html:78`
- Modify: `admin/orders.html:74`
- Modify: `admin/revenue.html:138`

- [ ] **Step 1: Trong `admin/index.html`:**
  - Sửa `QUẢN LÝ KHO SẢN PHẨM ENERGY BOOST (TĨNH)` ➔ `QUẢN LÝ KHO SẢN PHẨM ENERGY BOOST`
  - Sửa `ĐƠN HÀNG MỚI NHẤT (TĨNH)` ➔ `ĐƠN HÀNG MỚI NHẤT`
- [ ] **Step 2: Trong `admin/inventory.html`:**
  - Sửa `QUẢN LÝ KHO SẢN PHẨM ENERGY BOOST (TĨNH)` ➔ `QUẢN LÝ KHO SẢN PHẨM ENERGY BOOST`
- [ ] **Step 3: Trong `admin/orders.html`:**
  - Sửa `DANH SÁCH ĐƠN HÀNG (TĨNH)` ➔ `DANH SÁCH ĐƠN HÀNG`
- [ ] **Step 4: Trong `admin/revenue.html`:**
  - Sửa `CHI TIẾT TỪNG THÁNG (TĨNH)` ➔ `CHI TIẾT TỪNG THÁNG`

---

### Task 3: Đồng Bộ Nút Chỉnh Sửa Sản Phẩm Tại Kho Nước (`admin/inventory.html`) Sang Trang Riêng

**Files:**
- Modify: `admin/inventory.html`
- Modify: `js/app.js`

- [ ] **Step 1: Cập nhật các hàng sản phẩm Monster trong `admin/inventory.html`:**
  Đổi nút chỉnh sửa thành:
  `<a href="edit-monster.html" class="btn-view-detail" style="padding: 4px 8px; font-size: 0.8rem; display: inline-flex;" title="Chỉnh sửa sản phẩm"><i class="fas fa-edit"></i></a>`
- [ ] **Step 2: Cập nhật các hàng sản phẩm Redbull trong `admin/inventory.html`:**
  Đổi nút chỉnh sửa thành link trỏ tới `edit-redbull-original.html`, `edit-redbull-thai.html`, `edit-redbull-lonvua.html`.
- [ ] **Step 3: Cập nhật các hàng sản phẩm Sting trong `admin/inventory.html`:**
  Đổi nút chỉnh sửa thành link trỏ tới `edit-sting.html`.
- [ ] **Step 4: Cập nhật hàm `openProductEditModal(productId, btn)` trong `js/app.js`:**
  Điều hướng sang `edit-monster.html` / `edit-redbull-*.html` / `edit-sting.html` nếu được gọi bằng JS.

---

### Task 4: Bổ Sung Dữ Liệu & Logic Chi Tiết Đơn Hàng Trong `js/app.js`

**Files:**
- Modify: `js/app.js`

- [ ] **Step 1: Định nghĩa database dữ liệu mẫu đơn hàng phong phú trong `js/app.js`**
- [ ] **Step 2: Viết hàm `initOrderDetailPage(role)` tự động parse URL param `?id=` và điền thông tin lên giao diện**
- [ ] **Step 3: Cập nhật hàm `openOrderDetailModal(orderId)` để điều hướng trực tiếp sang `order-detail.html?id=...`**
- [ ] **Step 4: Kiểm tra cú pháp JavaScript bằng `node -c js/app.js`**

---

### Task 5: Xây Dựng Trang Chi Tiết Đơn Hàng Quản Trị Viên (`admin/order-detail.html`)

**Files:**
- Create: `admin/order-detail.html`

- [ ] **Step 1: Tạo khung HTML semantic với Sidebar Admin, Topbar, Breadcrumb**
- [ ] **Step 2: Xây dựng Section Order Summary Box (Mã đơn, badge trạng thái, ngày đặt)**
- [ ] **Step 3: Xây dựng Card thông tin khách hàng (Họ tên, SĐT, Địa chỉ giao hàng, Ghi chú)**
- [ ] **Step 4: Xây dựng bảng chi tiết sản phẩm (`.order-items-table`) hiển thị lon nước, đơn giá, số lượng, thành tiền**
- [ ] **Step 5: Xây dựng khối tổng thanh toán (`.order-total-row`) và các nút thao tác ("Quay lại danh sách", "In hóa đơn")**

---

### Task 6: Xây Dựng Trang Chi Tiết Đơn Hàng Khách Hàng (`pages/order-detail.html`)

**Files:**
- Create: `pages/order-detail.html`

- [ ] **Step 1: Tạo khung HTML storefront với Topbar, Header, Logo và Breadcrumb**
- [ ] **Step 2: Thiết kế thẻ hóa đơn khách hàng (Haptic Double-Bezel card) với trạng thái giao hàng**
- [ ] **Step 3: Xây dựng bảng chi tiết các lon nước đã đặt kèm hình ảnh sản phẩm thực tế**
- [ ] **Step 4: Thêm khối tổng tiền, ưu đãi giảm giá và phương thức thanh toán (COD / Chuyển khoản)**
- [ ] **Step 5: Bổ sung nút "← Quay lại lịch sử đơn hàng" (`orders.html`) và "Tiếp tục mua sắm" (`../index.html`)**

---

### Task 7: Chuyển Đổi Các Nút/Liên Kết Popup Sang Trang HTML Riêng & Dọn Dẹp Modal

**Files:**
- Modify: `admin/orders.html`
- Modify: `admin/customers.html`
- Modify: `admin/index.html`
- Modify: `pages/orders.html`
- Modify: `pages/account.html`

- [ ] **Step 1: Cập nhật các nút "Chi tiết" trong `admin/orders.html` thành `<a href="order-detail.html?id=...">`**
- [ ] **Step 2: Cập nhật các link mã đơn của Top 5 VIP trong `admin/customers.html` thành `<a href="order-detail.html?id=..." onclick="openOrderDetailModal(...)">`**
- [ ] **Step 3: Cập nhật bảng đơn hàng gần đây trong `admin/index.html` thành link sang `order-detail.html?id=...`**
- [ ] **Step 4: Cập nhật `pages/orders.html` và `pages/account.html` bổ sung nút "Xem Chi Tiết" trỏ sang `order-detail.html?id=...`**
- [ ] **Step 5: Xóa bỏ khối popup modal `#modal-order-detail` thừa khỏi các file admin**

---

### Task 8: Kiểm Thử Hồi Quy Tự Động & Nghiệm Thu Tiêu Chí

**Files:**
- Test: `verify_implementation.py`
- Test: `scripts/verify_admin_ui_mockup.py`
- Test: `scripts/verify_order_detail_pages.py`

- [ ] **Step 1: Viết script kiểm thử tự động `scripts/verify_order_detail_pages.py`**
- [ ] **Step 2: Chạy `python scripts/verify_order_detail_pages.py` -> Đảm bảo PASS 100%**
- [ ] **Step 3: Chạy `python verify_implementation.py` -> Đảm bảo 66/66 checks PASS**
- [ ] **Step 4: Chạy `python scripts/verify_admin_ui_mockup.py` -> Đảm bảo 10/10 checks PASS**
- [ ] **Step 5: Kiểm tra git status và tạo commit cục bộ an toàn**
