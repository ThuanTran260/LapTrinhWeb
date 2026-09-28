# Kế Hoạch Nâng Cấp Toàn Diện Website Monster Energy Store (Chuẩn 10/10 - Chốt Số Liệu)

Kế hoạch này giải quyết triệt để 100% các khiếm khuyết được chỉ ra và chốt chuẩn số liệu tài chính theo Master ID2:
1. **P0 - Đổi tên file về `kebab-case`**: Loại bỏ hoàn toàn dấu cách và lỗi typo (`orignal`), đảm bảo tương thích 100% với môi trường Linux / GitHub Pages phân biệt chữ hoa-thường.
2. **Master Data Sheet (Bảng dữ liệu chuẩn 8 sản phẩm)**: Thống nhất tuyệt đối tên gọi, giá bán (Ultra White chuẩn 48.000đ), giá cũ, % giảm, rating, tồn kho trên cả 4 trang (`index.html`, `product-detail.html`, `cart.html`, `admin.html`).
3. **P0 - Sửa triệt để 4 card `Related Products`** trong `product-detail.html:216-271`.
4. **P1 - Chuẩn hóa khái niệm Thumbnail trong `product-detail.html`**: Thumbnails phản ánh các góc nhìn / chi tiết của lon Original (không lấy vị khác làm thumbnail).
5. **P1 - Đồng bộ chuẩn xác công thức tài chính `cart.html`**:
   - `Original 45.000đ x 2 = 90.000đ`
   - `Ultra White 48.000đ x 3 = 144.000đ`
   - Tạm tính (5 lon): `90.000đ + 144.000đ = 234.000đ`
   - Voucher `MONSTER10 (10%)`: `-23.400đ`
   - Tổng thanh toán: **`210.600đ`**
   - Header badge trên mọi trang: **`5`** lon | Giá hiển thị: **`210.600đ`**.
6. **P1 - Rà soát dọn sạch text vị cũ** (Juice, Java, Rehab, Mango Loco...) ở Navigation, Search placeholder, Footer, Meta tags, và Orders table trong `admin.html`.
7. **Thêm fallback an toàn**: Thuộc tính `onerror`, `loading="lazy"`.
8. **Automated Verification Script**: Script tự động quét toàn repo đảm bảo **0 file nào còn sót `.jpg` cũ**, 0 link ảnh vỡ, và khớp 100% số liệu.

---

## 1. Bảng Chuẩn Hóa Tên File Ảnh (`kebab-case`)

Thực hiện lệnh đổi tên 8 file trong thư mục `assets/images/monster/`:

| STT | Tên File Cũ Hiện Tại | Tên File Mới Chuẩn Hóa (`kebab-case`) | Trạng Thái / Ghi Chú |
|:---:|:---|:---|:---|
| 1 | `orignal.webp` | **`original.webp`** | Sửa lỗi chính tả thiếu `i` |
| 2 | `Ultra white.webp` | **`ultra-white.webp`** | Bỏ chữ hoa, bỏ dấu cách |
| 3 | `paradise.webp` | **`ultra-paradise.webp`** | Thêm tiền tố dòng Ultra |
| 4 | `watermelon.webp` | **`ultra-watermelon.webp`** | Thêm tiền tố dòng Ultra |
| 5 | `sunrise.webp` | **`ultra-sunrise.webp`** | Thêm tiền tố dòng Ultra |
| 6 | `blue hawaii.webp` | **`ultra-blue-hawaiian.webp`** | Bỏ dấu cách, tên chuẩn hãng |
| 7 | `Ultra punk punch.webp` | **`ultra-punk-punch.webp`** | Bỏ chữ hoa, bỏ dấu cách |
| 8 | `original strawberry shot.webp` | **`strawberry-shot.webp`** | Rút gọn, bỏ dấu cách |
| - | `monster_banner.jpg` | **`monster_banner.jpg`** | Giữ nguyên vì file tồn tại, sắc nét |

---

## 2. Master Data Sheet - Bảng Dữ Liệu Sản Phẩm Chuẩn (Single Source of Truth)

Tất cả các trang web (`index`, `product-detail`, `cart`, `admin`) bắt buộc dùng chung bộ dữ liệu chuẩn này:

| ID | Tên Hiển Thị | Tag Nổi Bật | Giá Bán | Giá Cũ | Giảm | Rating | Tồn Kho | File Ảnh Mới |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---|
| 1 | **Monster Energy Original 500ml** | CỔ ĐIỂN / BESTSELLER | 45.000đ | 55.000đ | -18% | 5.0 (1.850) | 150 lon | `assets/images/monster/original.webp` |
| 2 | **Monster Zero Ultra White 500ml** | 0 ĐƯỜNG - 0 CALO | 48.000đ | 55.000đ | -13% | 4.9 (980) | 95 lon | `assets/images/monster/ultra-white.webp` |
| 3 | **Monster Ultra Paradise 500ml** | KIWI & CHANH XANH | 48.000đ | 58.000đ | -17% | 4.8 (890) | 85 lon | `assets/images/monster/ultra-paradise.webp` |
| 4 | **Monster Ultra Punk Punch 500ml** | PUNK FRUIT PUNCH | 50.000đ | 60.000đ | -17% | 4.9 (1.100) | 70 lon | `assets/images/monster/ultra-punk-punch.webp` |
| 5 | **Monster Ultra Watermelon 500ml** | DƯA HẤU TƯƠI MÁT | 48.000đ | 58.000đ | -17% | 4.8 (750) | 60 lon | `assets/images/monster/ultra-watermelon.webp` |
| 6 | **Monster Ultra Sunrise 500ml** | CAM TƯƠI BÌNH MINH | 48.000đ | 58.000đ | -17% | 4.7 (620) | 50 lon | `assets/images/monster/ultra-sunrise.webp` |
| 7 | **Monster Ultra Blue Hawaiian 500ml** | HOA QUẢ POLYNESIA | 50.000đ | 60.000đ | -17% | 4.9 (810) | 45 lon | `assets/images/monster/ultra-blue-hawaiian.webp` |
| 8 | **Monster Energy Strawberry Shot 500ml** | DÂU TÂY ĐẬM VỊ | 50.000đ | 60.000đ | -17% | 4.8 (530) | 40 lon | `assets/images/monster/strawberry-shot.webp` |

*Quy chuẩn specs chung cho cả 8 lon:* Dung tích 500ml | 160mg Caffeine | Taurine, Inositol, Vitamin B (B3, B6, B12) | Nhập khẩu tiêu chuẩn Hoa Kỳ.

---

## 3. Checklist Thực Hiện Trong Build Mode

### Bước 1: Rename File Ảnh Trên Ổ Đĩa
- Thực thi lệnh đổi tên 8 file trong `assets/images/monster/` theo đúng bảng mục 1.

### Bước 2: Sửa `index.html`
- `76, 80`: Cập nhật badge giỏ hàng `2` -> **`5`**, tổng tiền `216.000đ` -> **`210.600đ`**.
- `55`: Search placeholder đổi thành `Tìm kiếm Original, Ultra White, Paradise, Punk Punch...`.
- `91-96`: Nav menu: Tất Cả Hương Vị, Flash Sale Giờ Vàng, Monster Original, Monster Ultra Series, Monster Punch & Shots.
- `124-139`: Side promo banners trỏ sang `ultra-punk-punch.webp` và `ultra-white.webp`.
- `198-324`: 4 lon Flash Sale:
  - Lon 1: `original.webp` (Monster Energy Original 500ml - 45.000đ)
  - Lon 2: `ultra-white.webp` (Monster Zero Ultra White 500ml - 48.000đ)
  - Lon 3: `ultra-paradise.webp` (Monster Ultra Paradise 500ml - 48.000đ)
  - Lon 4: `ultra-punk-punch.webp` (Monster Ultra Punk Punch 500ml - 50.000đ)
- `340-573`: Main catalog 8 lon khớp thứ tự 1 -> 8 theo Master Data Sheet, gắn `onerror="this.src='assets/images/monster/original.webp'"`, `loading="lazy"`.
- `597-605`: Footer category links cập nhật dọn sạch vị cũ.

### Bước 3: Sửa `product-detail.html`
- `54, 58`: Cập nhật badge giỏ hàng `2` -> **`5`**, tổng tiền `216.000đ` -> **`210.600đ`**.
- `97`: Ảnh chính `original.webp`.
- `99-112`: 4 Thumbnails góc nhìn lon Original (Chính diện, Móng cào xanh, Dinh dưỡng, Nắp lon) đều trỏ `original.webp`.
- `216-271`: 4 Thẻ `Related Products` sửa toàn bộ sang file mới:
  1. `ultra-white.webp` (Monster Zero Ultra White - 48.000đ)
  2. `ultra-paradise.webp` (Monster Ultra Paradise - 48.000đ)
  3. `ultra-watermelon.webp` (Monster Ultra Watermelon - 48.000đ)
  4. `ultra-punk-punch.webp` (Monster Ultra Punk Punch - 50.000đ)

### Bước 4: Sửa `cart.html` (Checklist chi tiết 7 điểm)
- `54, 58`: Badge giỏ hàng `2` -> **`5`**, tổng tiền `216.000đ` -> **`210.600đ`**.
- `81`: Ảnh item 1 `original.webp` + `onerror="this.src='assets/images/monster/original.webp'"`.
- `108-111`: Item 2 đổi ảnh sang `ultra-white.webp`, title `Monster Zero Ultra White 500ml`, cat `Monster Ultra | 0 Đường - 0 Calo`.
- `115`: Đơn giá Item 2 sửa `50.000đ` -> **`48.000đ`**.
- `123`: Thành tiền Item 2 (3 lon x 48k) sửa `150.000đ` -> **`144.000đ`**.
- `144-145`: Tạm tính (5 lon) sửa `240.000đ` -> **`234.000đ`**.
- `149-150`: Giảm giá voucher MONSTER10 (10%) sửa `-24.000đ` -> **`-23.400đ`**.
- `166`: Tổng cộng sửa `216.000đ` -> **`210.600đ`**.
- `169`: Toast checkout sửa `216.000đ` -> **`210.600đ`**.

### Bước 5: Sửa `admin.html`
- **Bảng Quản Lý Kho (8 dòng)**:
  - Cập nhật 8 ảnh `.webp` mới chuẩn kebab-case.
  - Tên lon nước, dòng sản phẩm, giá bán (Ultra White 48.000đ), tồn kho khớp 100% với Master Data Sheet.
- **Bảng Đơn Hàng Mẫu (Orders Table)**:
  - #ME-8801: `2x Monster Original, 1x Ultra Punk Punch`
  - #ME-8802: `4x Ultra White, 2x Ultra Blue Hawaiian`
  - #ME-8803: `1x Strawberry Shot 500ml`
  - #ME-8804: `1 Thùng 24 Lon Monster Original`
  - #ME-8805: `3x Ultra Paradise, 2x Ultra Watermelon`

---

## 4. Automated Verification Plan (Kịch Bản Kiểm Thử Tự Động)

### Kịch bản 1: Quét Toàn Repo Bằng Lệnh Không Còn Tồn Tại File `.jpg` Cũ
Chạy lệnh PowerShell kiểm tra toàn bộ thư mục dự án:
```powershell
Get-ChildItem -Path . -Include *.html, *.css, *.js -Recurse | Select-String -Pattern "monster_original.jpg|monster_zero_ultra.jpg|monster_mango_loco.jpg|monster_pipeline_punch.jpg|monster_ultra_paradise.jpg|monster_ultra_fiesta.jpg|monster_java_mean_bean.jpg|monster_rehab_tea.jpg|orignal.webp|Ultra white.webp|Ultra punk punch.webp"
```
**Yêu cầu:** Kết quả trả về phải rỗng (0 match).

### Kịch bản 2: Kiểm Tra Sự Tồn Tại Của Toàn Bộ File Ảnh Được Trích Dẫn
Dùng script PowerShell phân tích tất cả các thẻ `img[src]` trong 4 file HTML, kiểm tra `Test-Path` trên ổ đĩa.
**Yêu cầu:** 100% file ảnh tồn tại trên đĩa, không có đường link nào bị 404.

### Kịch bản 3: Kiểm Tra Tính Toán Số Liệu `cart.html`
Kiểm tra bằng script: `(2 * 45000) + (3 * 48000) - 23400 = 210600`. Đảm bảo các text `234.000đ`, `-23.400đ`, `210.600đ`, và `210.600đ` trên header khớp nhau hoàn toàn.
