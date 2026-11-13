# Thiết Kế: Hiển Thị Tồn Kho Admin, Định Dạng Tiền VNĐ Voucher & Nút In Hóa Đơn Toast

**Ngày:** 13/11/2026  
**Trạng thái:** Approved by User  
**Tác giả:** Antigravity  

---

## 1. Bối cảnh & Mục tiêu

Người dùng yêu cầu thực hiện 3 cải tiến trên hệ thống:

1. **Hiển thị nhỏ số lượng tồn kho:**
   - Trong bảng quản lý kho (`admin/inventory.html` và `admin/index.html`), hiển thị số lượng tồn kho thực tế của từng sản phẩm.
   - 4 dòng sản phẩm **Monster Energy** cố định đúng số liệu hiện tại: **`1.250 lon`**.
   - Các dòng sản phẩm **Redbull** và **Sting** hiển thị các con số ngẫu nhiên thực tế đa dạng (ví dụ: 450 - 890 lon).
   - Vị trí: Hiển thị dòng phụ nhỏ trang nhã bên dưới huy hiệu `CÒN HÀNG` trong cột **Trạng Thái**.

2. **Định dạng tiền tệ VNĐ thời gian thực cho Cài đặt Voucher & Vận chuyển:**
   - Trong trang `admin/settings.html`, khi người dùng nhập số tiền vào ô **Giảm Tối Đa** (hoặc Đơn tối thiểu, Phí vận chuyển), số tiền chưa được tự động format tiền tệ VNĐ (ví dụ nhập `13131` không có dấu chấm và ký hiệu `đ`), khiến thẻ xem trước coupon hiển thị thô `(Tối đa 13131)`.
   - Cần tự động định dạng tiền tệ VNĐ trực tiếp khi gõ phím (`13131` $\rightarrow$ `13.131đ`) và đồng bộ thẻ Live Preview ngay lập tức: `(Tối đa 13.131đ)`.

3. **Nút "IN HÓA ĐƠN ĐIỆN TỬ" chỉ hiển thị thông báo:**
   - Tại trang `pages/order-success.html`, nút `IN HÓA ĐƠN ĐIỆN TỬ` hiện tại đang gọi `window.print()` (mở hộp thoại in trình duyệt).
   - Thay đổi: Chuyển sang hiển thị thông báo toast trang nhã: `showToast('Hóa đơn điện tử đã được tạo và gửi đến email của bạn!', 'success')` mà không mở hộp thoại in trình duyệt.

---

## 2. Chi Tiết Thiết Kế Kỹ Thuật

### 2.1. Phần 1: Số Lượng Tồn Kho Trong Bảng Quản Lý Kho (`admin/inventory.html` & `admin/index.html`)

Trong cột **Trạng Thái** (`<td>...</td>`), bên dưới `<span class="badge-status success">CÒN HÀNG</span>`, bổ sung dòng chữ nhỏ:
```html
<td>
  <span class="badge-status success">CÒN HÀNG</span>
  <small style="color: var(--text-muted); display: block; margin-top: 4px; font-size: 0.78rem;">
    <i class="fas fa-box"></i> Tồn: {qty} lon
  </small>
</td>
```

**Bảng dữ liệu 10 sản phẩm kho:**
| STT | Tên Sản Phẩm | Thương Hiệu | Số Lượng Tồn | Ghi Chú |
|:---:|:---|:---|:---:|:---|
| 1 | Monster Energy Original 355ml | Monster Energy | **1.250 lon** | Cố định theo yêu cầu |
| 2 | Monster Zero Ultra White 500ml | Monster Energy | **1.250 lon** | Cố định theo yêu cầu |
| 3 | Monster Ultra Paradise 500ml | Monster Energy | **1.250 lon** | Cố định theo yêu cầu |
| 4 | Monster Ultra Punk Punch 500ml | Monster Energy | **1.250 lon** | Cố định theo yêu cầu |
| 5 | Nước Tăng Lực Redbull Original 250ml | Redbull Thái Lan | **680 lon** | Phân bổ đa dạng |
| 6 | Nước Tăng Lực Redbull Thái Lan 250ml | Redbull Thái Lan | **450 lon** | Phân bổ đa dạng |
| 7 | Nước Tăng Lực Redbull Nắp Bật 250ml | Redbull Thái Lan | **520 lon** | Phân bổ đa dạng |
| 8 | Nước Tăng Lực Sting Dâu Tây Đỏ 330ml | Sting (PepsiCo) | **890 lon** | Phân bổ đa dạng |
| 9 | Nước Tăng Lực Sting Vàng Sleek 330ml | Sting (PepsiCo) | **740 lon** | Phân bổ đa dạng |
| 10 | Nước Tăng Lực Sting Blue Sleek 320ml | Sting (PepsiCo) | **610 lon** | Phân bổ đa dạng |

---

### 2.2. Phần 2: Định Dạng VNĐ Trong `admin/settings.html` & `js/app.js`

1. **Trong `admin/settings.html`:**
   Thêm class `price-format-input` cho các trường tiền tệ:
   - `#voucher-min-spend` (Đơn tối thiểu)
   - `#voucher-max-discount` (Giảm tối đa)
   - `#ship-min-free` (Miễn phí vận chuyển từ)
   - `#ship-standard-fee` (Phí giao tiêu chuẩn)

2. **Trong `js/app.js`:**
   - Trong `initPriceFormatting()`: Mở rộng bộ chọn bao gồm các trường:
     `#voucher-min-spend`, `#voucher-max-discount`, `#ship-min-free`, `#ship-standard-fee`.
   - Đảm bảo khi người dùng gõ phím vào `#voucher-max-discount` hoặc `#voucher-min-spend`, sự kiện `input` tự động định dạng số thành chuỗi tiền tệ VNĐ (ví dụ `13131` thành `13.131đ`).
   - Cập nhật hàm `updateVoucherLivePreview()` để đảm bảo khi đọc giá trị `#voucher-max-discount`:
     - Nếu người dùng nhập số thuần, tự động định dạng có đuôi `đ` (ví dụ `13131` hiển thị thành `(Tối đa 13.131đ)`).

---

### 2.3. Phần 3: Nút In Hóa Đơn Điện Tử Trong `pages/order-success.html`

Trong `pages/order-success.html:222-224`:
- Cũ:
  ```html
  <button type="button" onclick="window.print()" class="btn-success-secondary">
    <i class="fas fa-print"></i> IN HÓA ĐƠN ĐIỆN TỬ
  </button>
  ```
- Mới:
  ```html
  <button type="button" onclick="showToast('Hóa đơn điện tử đã được tạo và gửi đến email của bạn!', 'success')" class="btn-success-secondary">
    <i class="fas fa-print"></i> IN HÓA ĐƠN ĐIỆN TỬ
  </button>
  ```

---

## 3. Tiêu Chí Nghiệm Thu & Kiểm Thử

1. Cột Trạng Thái của cả 10 sản phẩm trong `admin/inventory.html` và `admin/index.html` đều có thẻ `<small>` hiển thị `Tồn: ... lon`.
2. Đúng 4 sản phẩm Monster có `Tồn: 1.250 lon`.
3. 6 sản phẩm Redbull và Sting có số lượng tồn đa dạng và không rỗng.
4. Các input tiền tệ trong `admin/settings.html` có class `price-format-input` và được khởi tạo format VNĐ.
5. Hàm `updateVoucherLivePreview()` trong `js/app.js` định dạng giá trị tối đa có đuôi `đ` và dấu chấm ngăn cách hàng nghìn.
6. Nút `IN HÓA ĐƠN ĐIỆN TỬ` trong `pages/order-success.html` gọi `showToast` thay vì `window.print()`.
7. 100% các bộ test hiện có đều PASS (`verify_implementation.py`, `verify_price_formatting.py`, `verify_footer_sync.py`, `verify_sidebar_filter_sync.py`, v.v.).
