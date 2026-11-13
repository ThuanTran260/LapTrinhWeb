# Thiết Kế: Loại Bỏ Khối Thông Số Hardcode (product-specs) Khỏi Thẻ Sản Phẩm

**Ngày:** 13/11/2026  
**Trạng thái:** Approved by User  
**Tác giả:** Antigravity  

---

## 1. Bối cảnh & Lý do thay đổi

- **Hiện trạng:** Các thẻ sản phẩm tại trang chủ (`index.html`), trang tìm kiếm (`pages/search-results.html`) và hàm render động trong `js/app.js` đang hiển thị khối `.product-specs` với các icon và text hardcode:
  - Icon chai/lon + Thể tích: `355ml`, `250ml`, `500ml`, `330ml`...
  - Icon khiên/lá/sấm sét + Nhãn đặc tính: `Sẵn hàng`, `0 Đường`, `0 Calo - 0 Đường`, `Malaysia SX`, `Kẽm & Vitamin`, `Nhập Thái Lan`, `Dáng Vừa Tiện Lợi`, `Nhân Sâm & Vị Dâu`, `Chiết Xuất Nhân Sâm`, `Hương Việt Quất Mới`...
- **Vấn đề:**
  - Trang quản trị Admin (`admin/inventory.html`, `admin/edit-*.html`) hoàn toàn **không có phần cấu hình hay quản lý** cho các nhãn icon đặc tính này. Do đó xảy ra tình trạng "lệch pha" giữa dữ liệu quản trị và giao diện hiển thị.
  - Các thông số thể tích lon đã có sẵn trong tên sản phẩm (VD: *Monster Energy Original 355ml*), làm dòng specs trở nên dư thừa.
- **Quyết định (Phương án 1):** Loại bỏ triệt để toàn bộ khối `<div class="product-specs">...</div>` khỏi tất cả các thẻ sản phẩm. Giữ giao diện thẻ sản phẩm theo phong cách tối giản (Minimalist Neon Glassmorphism):
  `Badge giảm giá` $\rightarrow$ `Ảnh lon nước` $\rightarrow$ `Danh mục thương hiệu` $\rightarrow$ `Tên sản phẩm` $\rightarrow$ `Đường kẻ phân cách & Khối Giá + Nút Thêm Giỏ Hàng`.

---

## 2. Chi Tiết Thay Đổi

### 2.1. Trang chủ `index.html` (14 thẻ sản phẩm)
Loại bỏ thẻ `<div class="product-specs">...</div>` tại:
1. **4 thẻ Flash Sale / Top Best Seller:**
   - Monster Original (lines 328-331)
   - Redbull Original (lines 359-362)
   - Monster Zero Ultra White (lines 390-393)
   - Redbull Nắp Bật (lines 421-424)
2. **10 thẻ Danh mục thương hiệu (Brand Sections):**
   - 4 thẻ Monster Energy: Original (line 670), Ultra White (line 699), Ultra Paradise (line 725), Pipeline Punch (line 750)
   - 3 thẻ Redbull: Original (line 792), Thái Lan (line 818), Nắp Bật (line 846)
   - 3 thẻ Sting: Dâu Tây Đỏ (line 886), Vàng Sleek (line 911), Blue Sleek (line 936)

### 2.2. Trang tìm kiếm `pages/search-results.html`
Loại bỏ `<div class="product-specs">...</div>` tại thẻ sản phẩm mẫu hiển thị tĩnh (line 409-412).

### 2.3. Tệp logic `js/app.js`
Loại bỏ khối HTML `.product-specs` trong template chuỗi tạo card tại hàm `renderMonsterProductCard()` (hoặc các hàm render card tương tự).

### 2.4. Tệp kiểu dáng `css/style.css`
Giữ nguyên hoặc dọn dẹp các class thừa nếu cần, đảm bảo `.product-bottom` vẫn giữ thuộc tính `margin-top: auto;` để đáy thẻ luôn cân bằng và thẳng hàng trên cùng một đường sàn.

---

## 3. Kế Hoạch Kiểm Thử & Tiêu Chí Nghiệm Thu

1. **Kiểm tra trực quan & cấu trúc:**
   - 0 còn bất kỳ thẻ `<div class="product-specs">` nào trong `index.html`, `pages/search-results.html` và `js/app.js`.
   - Các thẻ sản phẩm vẫn duy trì đầy đủ: nút `btn-add-stitch`, liên kết điều hướng click ảnh/tên sản phẩm, nhãn hãng và giá tiền.
2. **Kiểm tra hồi quy:**
   - Chạy toàn bộ 66 kiểm thử trong `verify_implementation.py` $\rightarrow$ Đạt 66/66 PASS.
   - Chạy `scripts/verify_ui_fixes_and_combo_removal.py` $\rightarrow$ Đạt 8/8 PASS.
   - Chạy `scripts/verify_footer_sync.py` $\rightarrow$ Đạt 144/144 PASS.
   - Viết script kiểm thử mới `scripts/verify_no_product_specs.py` để tự động hóa việc xác minh không còn `.product-specs` trên giao diện storefront.
