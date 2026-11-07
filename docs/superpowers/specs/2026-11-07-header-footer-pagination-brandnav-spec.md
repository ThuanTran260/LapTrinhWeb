# Spec: Thống Nhất Header, Phân Trang 1-2-3, Cuộn Hãng & Căn Lề Chân Thẻ Sản Phẩm

**Ngày:** 07/11/2026  
**Trạng thái:** Approved  

---

## 1. Bối cảnh & Mục tiêu
- **Phân trang:** Khối phân trang `< 1 2 3 >` ở đáy danh mục trang chủ `index.html` đang bị dính cứng ở trang 3, người dùng không chuyển đổi được giữa các trang 1, 2, 3 và nút mũi tên `< >`.
- **Điều hướng hãng:** Người dùng và người đánh giá nhận xét khoảng cách từ thanh điều hướng (navbar) trên cùng đến danh mục sản phẩm khá xa. Cần cho phép khi bấm vào hãng nào (Monster, Redbull, Sting) thì trang cuộn mượt xuống đúng khu vực sản phẩm của hãng đó.
- **Header Lịch sử đơn hàng:** Trang `pages/orders.html` đang dùng header giản lược, chưa đồng bộ với giao diện chuẩn của `cart.html` và `account.html` (thiếu thanh tìm kiếm, cụm tài khoản).
- **Chân thẻ sản phẩm (Footer card):** Khối giá tiền và nút giỏ hàng bị lệch trọng tâm thị giác, hai màu xanh neon đặc cạnh nhau gây chói mắt. Cần canh lề hài hòa theo trục sàn (baseline alignment) và cân bằng thị giác 2 tầng.

---

## 2. Chi tiết Giải pháp Thiết kế

### 2.1. Thống nhất Header trang Lịch sử đơn hàng (`pages/orders.html` & `pages/order-detail.html`)
- Thay thế header hiện tại bằng Header chuẩn đồng bộ với `pages/cart.html` và `pages/account.html`:
  - **Bên trái:** Logo ENERGYBOOST.
  - **Ở giữa:** Thanh tìm kiếm hoàn chỉnh gồm: ô nhập `search-input`, nút tìm kiếm, nút mở modal bộ lọc nâng cao, và popup gợi ý tĩnh 5 lon hot (`#search-dropdown-menu`).
  - **Bên phải:** Cụm 3 nút hành động chuẩn:
    - Nút 1: `Đơn hàng` (Lịch sử) - class `action-btn`, hiển thị nhãn và icon biên nhận chuẩn (không ghi chữ `[ACTIVE]` hay bất kỳ nhãn lạ nào).
    - Nút 2: `Tài khoản` (Thành viên).
    - Nút 3: `Giỏ hàng` (7 lon - 216.000đ).
  - Tích hợp modal tìm kiếm nâng cao (`modal-adv-search`) vào trang `orders.html` để đồng bộ hoàn toàn với toàn bộ hệ thống.

### 2.2. Xử lý Phân trang thông minh (`< 1 2 3 >`) trong `index.html`
- Hàm JavaScript `changeDashboardPage(pageNum, e)` trong `js/app.js`:
  - Quản lý biến trạng thái `currentDashboardPage` (giá trị 1, 2, 3; mặc định 1).
  - **Trang 1:** Active nút 1, vô hiệu hóa nút `<`, cuộn mượt đến `#monster-products`.
  - **Trang 2:** Active nút 2, bật cả 2 nút `<` và `>`, cuộn mượt đến `#redbull-products`.
  - **Trang 3:** Active nút 3, vô hiệu hóa nút `>`, cuộn mượt đến `#sting-products`.
  - Nút `<`: Gọi `changeDashboardPage(currentDashboardPage - 1)`.
  - Nút `>`: Gọi `changeDashboardPage(currentDashboardPage + 1)`.

### 2.3. Cuộn mượt điều hướng thương hiệu (Monster, Redbull, Sting)
- Cập nhật lại hành vi click cho các nút trên navbar:
  - Khi click vào `Monster`: Gắn `active` và cuộn mượt (`scrollIntoView({ behavior: 'smooth' })`) tới `#monster-products`.
  - Khi click vào `Redbull`: Gắn `active` và cuộn mượt tới `#redbull-products`.
  - Khi click vào `Sting`: Gắn `active` và cuộn mượt tới `#sting-products`.
- CSS: Bổ sung `scroll-margin-top: 100px;` cho 3 section `#monster-products`, `#redbull-products`, `#sting-products` để tiêu đề thương hiệu không bị thanh Header cố định (sticky header) che mất khi cuộn tới.
- Ở các trang phụ: Chuyển hướng về `../index.html#<brand>-products`.

### 2.4. Canh lề chân thẻ sản phẩm (Giá & Nút thêm giỏ hàng)
- Bổ sung nhãn phụ phía trên giá tiền:
  ```html
  <div class="product-price">
    <span class="price-label">GIÁ CHÍNH HÃNG</span>
    <span class="price-current">45.000đ</span>
  </div>
  ```
- Tinh chỉnh CSS `.btn-add-stitch`:
  - Kích thước $40 \times 40\text{px}$, bo góc $10\text{px}$.
  - Nền mờ Glassmorphism: `background: rgba(57, 255, 20, 0.12)`, viền `1px solid rgba(57, 255, 20, 0.35)`, icon giỏ hàng màu xanh neon.
  - Hover: Hóa neon sáng rực `background: var(--primary); color: #080A0C; transform: translateY(-2px);`.
- Tinh chỉnh CSS `.product-bottom`:
  - `display: flex; justify-content: space-between; align-items: flex-end; padding-top: 14px; border-top: 1px solid rgba(255, 255, 255, 0.06); min-height: auto;`
  - Đáy giá tiền và đáy nút bấm thẳng hàng hoàn hảo trên cùng một đường sàn.

---

## 3. Kế hoạch Kiểm thử & Xác minh
1. Kiểm tra chuyển đổi phân trang 1 $\leftrightarrow$ 2 $\leftrightarrow$ 3 và hoạt động của 2 nút mũi tên `< >`.
2. Kiểm tra bấm các nút Monster, Redbull, Sting trên navbar cuộn mượt và không bị che khuất tiêu đề.
3. Kiểm tra Header trên `pages/orders.html` hiển thị đầy đủ, tìm kiếm hoạt động, 3 nút hành động chuẩn xác.
4. Kiểm tra giao diện chân thẻ sản phẩm hiển thị hài hòa, cân bằng 2 bên trên desktop và mobile.
5. Chạy toàn bộ 66 kiểm thử hệ thống `verify_implementation.py` và kiểm thử admin đảm bảo pass 100%.
