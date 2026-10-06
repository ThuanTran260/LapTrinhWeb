# Task 1 Brief: Tạo Trang Chỉnh Sửa Đại Diện Monster (`admin/edit-monster.html`)

**Files:**
- Create: `admin/edit-monster.html`
- Reference: `admin/edit-redbull-original.html`, `pages/product-detail.html`

**Requirements:**
1. Tạo file `admin/edit-monster.html` sử dụng layout 2 cột `.admin-edit-layout` giống hệt `admin/edit-redbull-original.html`.
2. Cột trái:
   - Huy hiệu `SẴN HÀNG XUẤT KHO`
   - Ảnh đại diện lon Monster: `../assets/images/monster/original.webp`
   - Tiêu đề: `Monster Energy Original 355ml`
   - Giá: `45.000đ` (cũ: `55.000đ`)
   - Khối SKU:
     - SKU: `MN-ORIGINAL-355`
     - Thương hiệu: `Monster Energy (Hà Lan)`
     - Tồn kho: `1.250 lon`
     - Đã bán tháng này: `2.150 lon`
     - Đánh giá: `5.0 ⭐ (Top 1 Doanh số)`
   - Nút "Lưu Thay Đổi": `onclick="saveStandaloneEdit(event, 'Monster Energy Original 355ml')"`
3. Cột phải:
   - Tiêu đề: `Thông Số Kỹ Thuật Độc Lập` với icon neon green
   - Badge tag: `DÒNG NGUYÊN BẢN`
   - Các trường form:
     - Tên Sản Phẩm Đầy Đủ: `Monster Energy Original 355ml`
     - Thương Hiệu: `Monster Energy (Hà Lan / Hoa Kỳ)`
     - Nguồn Gốc / Xuất Xứ: `Malaysia (Ủy quyền Monster Energy Company)`
     - Giá Bán Lẻ Hiện Tại: `45.000đ`
     - Giá Niêm Yết Cũ: `55.000đ`
     - Thể Tích / Quy Cách: `355ml (Lon nhôm cao cấp)`
     - Hương Vị Đặc Trưng: `Vị nguyên bản đậm đà, sảng khoái với Taurine & Nhân sâm`
     - Thành Phần Chi Tiết: `Nước bão hòa CO2, Sucroza, chiết xuất đường nho, chiết xuất nhân sâm, L-Carnitine, Taurine (400mg/100ml), Caffeine (30mg/100ml), Inositol, Vitamin B3, B6, B2, B12, Maltodextrin, chất điều chỉnh độ acid...`
     - Hướng Dẫn Sử Dụng: `Lắc nhẹ trước khi uống, dùng ngay sau khi mở nắp. Ngon hơn khi uống lạnh.`
     - Bảo Quản: `Để nơi khô ráo, thoáng mát, tránh ánh sáng trực tiếp hoặc nơi có nhiệt độ cao.`
4. Topbar:
   - Breadcrumb: Admin / Kho hàng / Chỉnh sửa: Monster Energy Original 355ml
   - Nút "Xem Trên Storefront" dẫn tới `../pages/product-detail.html`
   - Nút "Quay Lại Kho" dẫn tới `inventory.html`
5. Tuân thủ RULE 1: Không chạy git push.
