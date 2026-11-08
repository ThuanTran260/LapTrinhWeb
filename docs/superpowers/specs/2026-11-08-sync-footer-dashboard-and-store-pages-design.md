# Thiết Kế: Đồng Bộ Footer 4 Cột Toàn Diện Cho Dashboard và Các Trang Khách Hàng

**Ngày lập:** 08/11/2026  
**Trạng thái:** Chờ phê duyệt (Pending Approval)  
**Phạm vi áp dụng:**
1. Toàn bộ các trang Khách hàng (`pages/*.html`): `account.html`, `cart.html`, `orders.html`, `order-detail.html`, `order-success.html`, `payment-gateway.html`, `product-detail.html`, `product-detail-redbull.html`, `product-detail-redbull-thai.html`, `product-detail-redbull-lonvua.html`, `product-detail-sting.html`, `search-results.html`.
2. Toàn bộ các trang Quản trị Admin Dashboard (`admin/*.html`): `index.html`, `orders.html`, `inventory.html`, `revenue.html`, `customers.html`, `settings.html`, `order-detail.html`, `edit-monster.html`, `edit-redbull-lonvua.html`, `edit-redbull-original.html`, `edit-redbull-thai.html`, `edit-sting.html`.

---

## 1. Mục Tiêu & Yêu Cầu Thiết Kế

- **Đồng bộ nhận diện thương hiệu:** Thay thế các footer rút gọn 1 dòng ở các trang phụ và bổ sung footer hoàn chỉnh cho các trang admin dashboard theo đúng mẫu thiết kế 4 cột chuẩn của trang chủ `index.html` (như hình mẫu người dùng cung cấp).
- **Cấu trúc 4 cột chuẩn:**
  - **Cột 1 (Thương hiệu & Liên hệ):** Logo ENERGYBOOST phát sáng neon, câu giới thiệu định vị thương hiệu, địa chỉ showroom tại 88 Nguyễn Huệ, Hotline 1900 6868.
  - **Cột 2 (Các dòng sản phẩm):** 7 dòng sản phẩm chủ lực (Monster Original 355ml, Monster Zero Ultra White, Monster Ultra Punk Punch, Punch & Shots, Redbull Original 250ml, Redbull Thái Lan Nắp Bật, Sting Dâu Tây Đỏ 330ml).
  - **Cột 3 (Hệ thống trang):** 6 liên kết điều hướng cốt lõi (Trang Chủ, Monster Original Detail, Redbull Thái Detail, Giỏ Hàng Mẫu, Lịch Sử Đặt Hàng, Tài Khoản Thành Viên).
  - **Cột 4 (Voucher ưu đãi & Newsletter):** Lời kêu gọi đăng ký nhận mã giảm giá 15% cho thùng nước tăng lực đầu tiên kèm ô nhập email và nút gửi neon có feedback Toast thông báo thành công.
  - **Footer Bottom:** Dòng thông tin bản quyền `© 2026 ENERGY BOOST STORE. Built with Pure Static HTML5 & CSS3. All Rights Reserved.` cùng 4 biểu tượng phương thức thanh toán chuẩn quốc tế (Visa, Mastercard, Wallet, Lightning Neon).
- **Phân giải đường dẫn tương đối (Path Resolution):**
  - Trong `pages/*.html`: Các link tới trang chủ trỏ `../index.html`, các link tới trang nội bộ `pages/` trỏ trực tiếp `./<page>.html`, link neo sản phẩm trỏ `../index.html#<brand>-products`.
  - Trong `admin/*.html`: Đặt bên trong `<main class="admin-main">`, các link tới trang chủ trỏ `../index.html`, các link tới trang khách hàng trỏ `../pages/<page>.html`, link neo sản phẩm trỏ `../index.html#<brand>-products`.
- **CSS Tinh Chỉnh Cho Admin Dashboard:**
  - Bổ sung quy tắc CSS cho `.admin-main .footer`: Khối viền bo tròn bo góc `var(--radius-md)`, viền mảnh `1px solid var(--border-color)`, nền mờ `#07080A`, độ rộng tràn tự nhiên trong content layout mà không gây tràn ngang (zero horizontal overflow).

---

## 2. Danh Sách Tệp Tác Động

### 2.1. File Kiểu Dáng (CSS)
- `css/style.css`: Thêm quy tắc định kiểu bổ trợ cho `.admin-main .footer` để hiển thị hài hòa trong cấu trúc lưới admin.

### 2.2. Nhóm Trang Khách Hàng (`pages/*.html`) - 12 tệp
1. `pages/account.html`
2. `pages/cart.html`
3. `pages/orders.html`
4. `pages/order-detail.html`
5. `pages/order-success.html`
6. `pages/payment-gateway.html`
7. `pages/product-detail.html`
8. `pages/product-detail-redbull.html`
9. `pages/product-detail-redbull-thai.html`
10. `pages/product-detail-redbull-lonvua.html`
11. `pages/product-detail-sting.html`
12. `pages/search-results.html`

*(Lưu ý: `pages/login.html` và `admin/login.html` là màn hình form đăng nhập đứng độc lập căn giữa màn hình `login-body-wrapper`, giữ nguyên kiến trúc để không làm vỡ trải nghiệm login).*

### 2.3. Nhóm Trang Quản Trị Admin Dashboard (`admin/*.html`) - 11 tệp
1. `admin/index.html` (Tổng quan Dashboard)
2. `admin/orders.html` (Quản lý Đơn hàng)
3. `admin/inventory.html` (Quản lý Kho)
4. `admin/revenue.html` (Báo cáo Doanh thu)
5. `admin/customers.html` (Khách hàng VIP)
6. `admin/settings.html` (Cài đặt Hệ thống)
7. `admin/order-detail.html` (Chi tiết Đơn hàng Admin)
8. `admin/edit-monster.html`
9. `admin/edit-redbull-lonvua.html`
10. `admin/edit-redbull-original.html`
11. `admin/edit-redbull-thai.html`
12. `admin/edit-sting.html`

---

## 3. Tiêu Chí Nghiệm Thu (Acceptance Criteria)

1. Mọi trang trong danh sách trên đều chứa thẻ `<footer class="footer">` với cấu trúc 4 cột `.footer-grid` và thanh bản quyền `.footer-bottom`.
2. Không còn thẻ footer 1 dòng đơn giản trong bất kỳ trang nào của `pages/*.html`.
3. Toàn bộ liên kết trong footer (đặc biệt là cột Các Dòng Sản Phẩm và Hệ Thống Trang) đều hoạt động chính xác khi click từ cả trang con lẫn trang admin.
4. Form đăng ký voucher ưu đãi hoạt động và hiển thị toast thông báo chuẩn Vanilla JS.
5. Kiểm thử hệ thống: Toàn bộ 66 tests trong `verify_implementation.py` và các kịch bản kiểm thử trong `scripts/` đều PASS 100%.
6. Viết script kiểm thử mới `scripts/verify_footer_sync.py` để tự động duyệt qua tất cả các file HTML và xác nhận tính toàn vẹn của Footer 4 cột.
