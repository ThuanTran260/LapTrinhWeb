# Task 2 Brief: Tạo Trang Chỉnh Sửa Đại Diện Sting (`admin/edit-sting.html`)

**Files:**
- Create: `admin/edit-sting.html`
- Reference: `admin/edit-redbull-original.html`, `admin/edit-monster.html`, `pages/product-detail-sting.html`

**Requirements:**
1. Tạo file `admin/edit-sting.html` sử dụng layout 2 cột `.admin-edit-layout` Dark Neon Glassmorphism.
2. Cột trái (Product Summary Card):
   - Huy hiệu `SẴN HÀNG XUẤT KHO` (badge-status success)
   - Ảnh đại diện lon Sting: `../assets/images/sting/sting-dau.webp` (fallback: `../assets/images/sting/nuoc-tang-luc-sting-dau-sleek-lon-330ml_202509291421449068.webp`)
   - Tiêu đề: `Nước Tăng Lực Sting Dâu Tây Đỏ 330ml`
   - Giá: `12.000đ` (giá cũ niêm yết: `15.000đ`)
   - Khối SKU:
     - SKU: `ST-STRAWBERRY-330` (accent màu neon dâu `#FF0055`)
     - Thương hiệu: `Sting (Suntory PepsiCo)`
     - Tồn kho: `1.800 lon`
     - Đã bán tháng này: `3.420 lon`
     - Đánh giá: `5.0 ⭐ (Top 1 Doanh số Nước Ngọt Tăng Lực)`
   - Nút "Lưu Thay Đổi": `onclick="saveStandaloneEdit(event, 'Sting Dâu Tây Đỏ 330ml')"`
3. Cột phải (Detail Edit Form):
   - Tiêu đề: `Thông Số Kỹ Thuật Độc Lập` với icon `#FF0055`
   - Badge tag: `DÒNG DÂU TÂY ĐỎ SLEEK`
   - Form Fields:
     - Tên đầy đủ: `Nước Tăng Lực Sting Dâu Tây Đỏ Sleek 330ml`
     - Thương hiệu: `Sting (Suntory PepsiCo)`
     - Nguồn gốc: `Việt Nam (Tập đoàn Suntory PepsiCo)`
     - Giá bán lẻ: `12.000đ`
     - Giá niêm yết cũ: `15.000đ`
     - Thể tích / Quy cách: `330ml (Lon Sleek cao cấp)`
     - Hương vị đặc trưng: `Dâu tây đỏ thơm ngon & Nhân sâm`
     - Thành phần chi tiết: `Nước bão hòa CO2, đường mía, chất điều chỉnh độ acid (330, 331iii), hương dâu tây tự nhiên và tổng hợp, nhân sâm, Taurine (200mg/L), Caffeine (190mg/L), Inositol (30mg/L), Vitamin B3, B6, B12, màu tổng hợp (Allura Red AC 129)...`
     - Hướng dẫn sử dụng: `Dùng trực tiếp, ngon hơn khi uống lạnh. Lắc nhẹ trước khi mở nắp.`
     - Bảo quản: `Bảo quản nơi khô ráo, thoáng mát, tránh ánh nắng trực tiếp hoặc nơi có nhiệt độ cao.`
     - Trạng thái kho & Tồn kho thực tế: `Còn hàng (Sẵn sàng xuất kho)` / `1800`
   - Sự kiện submit: `onsubmit="saveStandaloneEdit(event, 'Sting Dâu Tây Đỏ 330ml')"`
4. Topbar:
   - Breadcrumb: `Admin / Kho hàng / Chỉnh sửa: Sting Dâu Tây Đỏ 330ml`
   - Nút `Xem Trên Storefront`: Liên kết `../pages/product-detail-sting.html`
   - Nút `Quay Lại Kho`: Liên kết `inventory.html`
5. Tuân thủ RULE 1: Tuyệt đối không git push.
