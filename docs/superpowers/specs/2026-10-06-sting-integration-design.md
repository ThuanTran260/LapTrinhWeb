# Design Spec: Tích Hợp Thương Hiệu Sting Vào Hệ Thống Energy Boost Store

- **Tác giả:** Antigravity Pairing Assistant
- **Ngày:** 2026-10-06
- **Trạng thái:** Chờ phê duyệt (Pending Approval)
- **Nhánh Git:** `feat/energy-boost-rebrand`

---

## 1. Tổng Quan & Bối Cảnh (Context & Goals)
Thư mục `assets/images/sting/` đã có sẵn 3 ảnh lon nước tăng lực Sting:
1. `nuoc-tang-luc-sting-dau-sleek-lon-330ml_202509291421449068.webp` (Sting Dâu Đỏ Sleek 330ml)
2. `nuoc-ngot-lon-sting-gold-sleek-330ml_202509291559402687.webp` (Sting Vàng Nhân Sâm Sleek 330ml)
3. `nuoc-tang-luc-sting-sleek-huong-viet-quat-lon-320ml_202505211557567348.webp` (Sting Xanh Blue Việt Quất Sleek 320ml)

**Mục tiêu thiết kế:**
- Chuyển đổi toàn bộ ảnh sang định dạng WebP có alpha matte trong suốt (RGBA), hòa nhập với giao diện dark mode nền đen `#141820`.
- Thêm **Sting** làm thương hiệu thứ 3 trên thanh Menu chính (`index.html`) cạnh Monster và Redbull.
- Tạo Section danh mục sản phẩm Sting trên Trang chủ với 3 card sản phẩm phong cách Dark Neon Glow (`#FF0055`, `#FFD700`, `#00D2FF`).
- Tạo trang chi tiết sản phẩm chuẩn `pages/product-detail-sting.html` (Sting Dâu Đỏ); cả 3 lon Sting đều điều hướng về trang này.
- Đồng bộ hóa 3 sản phẩm Sting vào hệ thống Quản trị Admin (`admin/inventory.html`, `admin/index.html`) và `PRODUCT_DATA_REGISTRY` trong `js/app.js`.
- Đảm bảo 100% 66/66 test cases của `verify_implementation.py` tiếp tục PASS.

---

## 2. Kiến Trúc Xử Lý Hình Ảnh (Asset Pipeline)
- **Xử lý nền trắng**:
  Sử dụng script Python flood-fill alpha matte bóc tách phông nền trắng `(255, 255, 255)` xung quanh thân lon nước.
- **Tên file chuẩn hóa**:
  - `assets/images/sting/sting-dau.webp` (Dâu Đỏ Sleek 330ml, RGBA trong suốt).
  - `assets/images/sting/sting-gold.webp` (Vàng Nhân Sâm Sleek 330ml, RGBA trong suốt).
  - `assets/images/sting/sting-vietquat.webp` (Xanh Blue Việt Quất Sleek 320ml, RGBA trong suốt).
  - Giữ lại các file gốc làm fallback tương thích.

---

## 3. Giao Diện Người Dùng Storefront (`index.html`)

### 3.1. Navigation Bar
Bổ sung tab thương hiệu thứ 3:
```html
<ul class="nav-menu">
  <li><a href="#monster-products" class="nav-link active"><i class="fas fa-bolt" style="color: var(--primary);"></i> Monster</a></li>
  <li><a href="#redbull-products" class="nav-link"><i class="fas fa-fire" style="color: var(--secondary);"></i> Redbull</a></li>
  <li><a href="#sting-products" class="nav-link"><i class="fas fa-bolt" style="color: #FF0055;"></i> Sting</a></li>
</ul>
```

### 3.2. Section Danh Mục Sting (`#sting-products`)
- **Vị trí**: Nằm ngay sau Section Redbull trên `index.html`.
- **Thành phần**:
  - Tiêu đề: `THƯƠNG HIỆU <span>STING (PEPSICO)</span>` + Nút `Xem Chi Tiết Sting`.
  - **Lưới 3 sản phẩm**:
    1. **Sting Dâu Tây Đỏ Sleek 330ml**:
       - Giá: `12.000đ` | Thể tích: `330ml` | Điểm nhấn: `Vị Dâu Tây Đỏ Bùng Nổ`
       - Hiệu ứng Neon: Viền phát sáng đỏ/hồng `#FF0055`, badge `DÂU ĐỎ`.
    2. **Sting Vàng Nhân Sâm Sleek 330ml**:
       - Giá: `12.000đ` | Thể tích: `330ml` | Điểm nhấn: `Chiết Xuất Nhân Sâm`
       - Hiệu ứng Neon: Viền phát sáng vàng gold `#FFD700`, badge `NHÂN SÂM`.
    3. **Sting Xanh Blue Hương Việt Quất 320ml**:
       - Giá: `13.000đ` | Thể tích: `320ml` | Điểm nhấn: `Vị Blue Việt Quất Mới`
       - Hiệu ứng Neon: Viền phát sáng xanh dương `#00D2FF`, badge `BLUE XANH`.
- **Tương tác**:
  - Click vào ảnh / tiêu đề / nút "Chi tiết": Chuyển hướng tới `pages/product-detail-sting.html`.
  - Click nút "+": Thêm giỏ hàng nhanh kèm toast thông báo.

---

## 4. Trang Chi Tiết Khách Hàng (`pages/product-detail-sting.html`)
- Kế thừa bố cục Dark Neon hiện đại của `product-detail-redbull.html`.
- **Hình ảnh**: 1 thumbnail lon Sting Dâu Đỏ duy nhất dưới lon nước chính.
- **Thông tin chi tiết**:
  - Tên: Nước Tăng Lực Sting Dâu Tây Đỏ Sleek 330ml
  - Giá: 12.000đ (Giá cũ: 15.000đ)
  - Thương hiệu: Suntory PepsiCo (Việt Nam)
  - Thể tích: 330ml
  - Mô tả: Nước tăng lực hương dâu tây đỏ kết hợp nhân sâm, taurine, inositol và các vitamin nhóm B mang lại nguồn năng lượng bứt phá tức thì.
- **Sản phẩm liên quan**: Sting Vàng, Sting Việt Quất, Monster Original, Redbull Original.

---

## 5. Quản Trị Admin & Data Registry

### 5.1. Bổ sung `PRODUCT_DATA_REGISTRY` trong `js/app.js`
- Thêm các key:
  - `sting-dau`: Sting Dâu Tây Đỏ 330ml (Suntory PepsiCo, 12.000đ, 330ml, Còn hàng)
  - `sting-gold`: Sting Vàng Nhân Sâm 330ml (Suntory PepsiCo, 12.000đ, 330ml, Còn hàng)
  - `sting-blue`: Sting Xanh Hương Việt Quất 320ml (Suntory PepsiCo, 13.000đ, 320ml, Còn hàng)

### 5.2. Bảng Kho Hàng Admin (`admin/inventory.html` & `admin/index.html`)
- Bổ sung 3 dòng sản phẩm Sting vào bảng quản lý kho với ảnh trong suốt, giá bán, số lượng tồn kho (500 - 900 lon), và nút sửa mở Modal đồng bộ 100%.

---

## 6. Kế Hoạch Kiểm Thử (Verification Plan)
- Chạy `python verify_implementation.py` đảm bảo toàn bộ 66/66 test cases PASS:
  - Khối `nav-menu` không chứa các pill bị cấm.
  - Footer giữ liên kết giỏ hàng và danh mục.
  - Các ràng buộc CSS/JS không bị ảnh hưởng.
- Kiểm tra tính toàn vẹn hiển thị hình ảnh không bị vỡ hoặc viền trắng trên nền đen.
