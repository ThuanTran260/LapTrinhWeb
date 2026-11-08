# Đặc Tả Kỹ Thuật (Design Spec): Đồng Bộ Top Bar Đơn Hàng & Chuẩn Hóa Breadcrumb Tài Khoản

> **Ngày tạo:** 08/11/2026  
> **Trạng thái:** Đã được người dùng phê duyệt (Approved)  
> **Phạm vi:** `pages/orders.html`, `pages/account.html`

---

## 1. Bối Cảnh & Mục Tiêu

### Vấn đề 1: Lệch thanh Top Bar giữa Dashboard và Trang Đơn Hàng
- Tại Dashboard (`index.html`), thanh Top Bar bên phải gồm: `Giao 2H Hoả Tốc` ➜ `Lịch Sử Đặt Hàng` ➜ `Tài Khoản` ➜ `Đăng Nhập`.
- Tại trang Lịch Sử Đơn Hàng (`pages/orders.html`), cụm Top Bar hiện chỉ có: `Tiếp Tục Mua Sắm` ➜ `Giỏ Hàng (7 lon)` ➜ `Tài Khoản`, thiếu `Giao Hoả Tốc` và `Lịch Sử Đặt Hàng`.
- **Mục tiêu:** Đồng bộ thanh Top Bar trang Đơn Hàng theo Phương án 1 (giữ `Tiếp Tục Mua Sắm` và `Giỏ Hàng (7 lon)`, bổ sung tuần tự theo Dashboard).

### Vấn đề 2: Tồn tại thanh phân loại thương hiệu trên trang Tài Khoản Thành Viên
- Tại `pages/account.html`, phía trên thẻ thông tin tài khoản đang tồn tại thẻ `<nav class="nav-bar">` chứa 3 tab thương hiệu: `Monster`, `Redbull`, `Sting`. Đây là thành phần của trang mua sắm sản phẩm, không phù hợp với trang thông tin cá nhân/hồ sơ thành viên.
- Trang Giỏ hàng (`pages/cart.html`) và Kết quả tìm kiếm (`pages/search-results.html`) đều sử dụng cấu trúc Breadcrumb (`Trang chủ / Giỏ hàng` hoặc `Trang chủ / Tìm kiếm...`).
- **Mục tiêu:** Loại bỏ hoàn toàn thanh `nav-bar` phân loại nước tăng lực khỏi `pages/account.html`, thay thế bằng thanh Breadcrumb chuẩn: `Trang chủ / Thành viên`.

---

## 2. Đặc Tả Kỹ Thuật Chi Tiết

### 2.1. Cập Nhật `pages/orders.html` (Top Bar Synchronization - Option 1)

Thay thế cụm `.top-links` trong `pages/orders.html`:
```html
<div class="top-links">
  <a href="../index.html"><i class="fas fa-arrow-left"></i> Tiếp Tục Mua Sắm</a>
  <a href="../index.html#features"><i class="fas fa-truck-fast"></i> Giao 2H Hoả Tốc</a>
  <a href="orders.html"><i class="fas fa-clock-rotate-left"></i> Lịch Sử Đặt Hàng</a>
  <a href="cart.html"><i class="fas fa-shopping-cart"></i> Giỏ Hàng (7 lon)</a>
  <a href="account.html"><i class="fas fa-user-circle"></i> Tài Khoản</a>
  <a href="login.html"><i class="fas fa-sign-in-alt"></i> Đăng Nhập</a>
</div>
```

**Ràng buộc kiểm thử:**
- Phải giữ nguyên văn bản `"Giỏ Hàng (7 lon)"` để đảm bảo tương thích 100% với `scripts/verify_cart_sync.py`.
- Các liên kết trỏ đúng đường dẫn tương đối từ thư mục `pages/`.

### 2.2. Cập Nhật `pages/account.html` (Remove Brand Nav & Add Breadcrumb)

1. **Loại bỏ khối navigation:**
   Xóa bỏ toàn bộ:
   ```html
   <!-- Navigation Bar -->
   <nav class="nav-bar">
     <div class="container nav-container">
       <ul class="nav-menu">
         <li><a href="javascript:void(0)" class="nav-link active" onclick="handleNavBrandClick(event, this)"><i class="fas fa-bolt" style="color: var(--primary);"></i> Monster</a></li>
         <li><a href="javascript:void(0)" class="nav-link" onclick="handleNavBrandClick(event, this)"><i class="fas fa-fire" style="color: var(--secondary);"></i> Redbull</a></li>
         <li><a href="javascript:void(0)" class="nav-link" onclick="handleNavBrandClick(event, this)"><i class="fas fa-bolt" style="color: #FF0055;"></i> Sting</a></li>
       </ul>
     </div>
   </nav>
   ```

2. **Thêm Breadcrumb vào đầu thẻ `<main>`:**
   ```html
   <main class="container account-page-section" style="padding-top: 24px; padding-bottom: 40px;">
     <div class="breadcrumb">
       <a href="../index.html">Trang chủ</a>
       <span>/</span>
       <span>Thành viên</span>
     </div>

     <div class="login-card" style="max-width: 680px; text-align: left; margin: 0 auto;">
       ...
     </div>
   </main>
   ```

---

## 3. Tiêu Chí Nghiệm Thu (Acceptance Criteria)

1. `pages/orders.html`:
   - `.top-links` có đúng 6 liên kết với đầy đủ icon và text chuẩn.
   - Giữ nguyên nút `Tiếp Tục Mua Sắm` và `Giỏ Hàng (7 lon)`.
   - Có thêm `Giao 2H Hoả Tốc`, `Lịch Sử Đặt Hàng`, `Đăng Nhập`.
2. `pages/account.html`:
   - Không còn thẻ `<nav class="nav-bar">` chứa các tab `Monster`, `Redbull`, `Sting`.
   - Xuất hiện thanh điều hướng `.breadcrumb` với cấu trúc `Trang chủ / Thành viên`.
   - Header và Footer vẫn đầy đủ để giữ điểm chuẩn rubric.
3. Toàn bộ 14 bộ kiểm thử hồi quy + 1 bộ kiểm thử mới đều đạt PASS 100%.
