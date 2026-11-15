# Thiết Kế: Tách Tồn Kho Thành Cột Riêng Biệt Trong Bảng Kho Admin

**Ngày:** 15/11/2026  
**Trạng thái:** Chờ User duyệt & Proceed  
**Tác giả:** Antigravity  

---

## 1. Bối cảnh & Mục tiêu

Người dùng yêu cầu:
> "tôi nghĩ tồn kho nên đưa lên làm 1 cột riêng kế bên trạng thái /brainstorming"
> "khuyen nghi di" (chọn Phương án 1)

**Hiện trạng:**
Bảng kho sản phẩm tại `admin/inventory.html` và `admin/index.html` hiện có 7 cột:
`Ảnh | Tên Sản Phẩm | Thương Hiệu / Dòng | Thể Tích | Giá Bán | Trạng Thái | Thao Tác`
Trong đó ô `Trạng Thái` đang gộp cả badge `CÒN HÀNG` và số lượng tồn kho trên cùng 1 ô.

**Mục tiêu:**
Tách số lượng tồn kho thành **1 cột độc lập** đứng ngay trước cột Trạng Thái (Bố cục chuẩn 8 cột theo ERP / eCommerce Admin):
1. `Ảnh`
2. `Tên Sản Phẩm`
3. `Thương Hiệu / Dòng`
4. `Thể Tích`
5. `Giá Bán`
6. **`Tồn Kho`** (Cột mới tách riêng)
7. **`Trạng Thái`** (Chỉ hiển thị badge trạng thái)
8. `Thao Tác`

Áp dụng đồng bộ cho toàn bộ 10 sản phẩm tại:
1. `admin/inventory.html` (Quản lý kho sản phẩm)
2. `admin/index.html` (Bảng kho nhanh Dashboard tổng quan)

---

## 2. Chi Tiết Kỹ Thuật

### 2.1. Cấu trúc Tiêu đề bảng (`<thead>`)
```html
<thead>
  <tr>
    <th>Ảnh</th>
    <th>Tên Sản Phẩm</th>
    <th>Thương Hiệu / Dòng</th>
    <th>Thể Tích</th>
    <th>Giá Bán</th>
    <th>Tồn Kho</th>
    <th>Trạng Thái</th>
    <th>Thao Tác</th>
  </tr>
</thead>
```

### 2.2. Cấu trúc các ô dữ liệu (`<tbody>`) cho 2 cột mới

- **Ô Tồn Kho (`<td>`):**
  ```html
  <td>
    <span style="color: #FFF; font-weight: 700; font-size: 0.92rem; white-space: nowrap;">
      <i class="fas fa-box" style="color: var(--primary); margin-right: 6px;"></i>{SO_LUONG} <small style="color: var(--text-muted); font-size: 0.8rem; font-weight: 500;">lon</small>
    </span>
  </td>
  ```

- **Ô Trạng Thái (`<td>`):**
  ```html
  <td>
    <span class="badge-status success">CÒN HÀNG</span>
  </td>
  ```

### 2.3. Dữ liệu chuẩn của 10 sản phẩm

| STT | Tên Sản Phẩm | Thương Hiệu | Giá Bán | Tồn Kho | Trạng Thái |
| :---: | :--- | :--- | :---: | :---: | :---: |
| 1 | Monster Energy Original 355ml | Monster Energy | 45.000đ | **1.250 lon** | `CÒN HÀNG` |
| 2 | Monster Zero Ultra White 500ml | Monster Energy | 48.000đ | **1.250 lon** | `CÒN HÀNG` |
| 3 | Monster Ultra Paradise 500ml | Monster Energy | 48.000đ | **1.250 lon** | `CÒN HÀNG` |
| 4 | Monster Ultra Punk Punch 500ml | Monster Energy | 50.000đ | **1.250 lon** | `CÒN HÀNG` |
| 5 | Nước Tăng Lực Redbull Original 250ml | Redbull Thái Lan | 18.000đ | **680 lon** | `CÒN HÀNG` |
| 6 | Nước Tăng Lực Redbull Thái Chai Thủy Tinh 150ml | Redbull Thái Lan | 18.000đ | **450 lon** | `CÒN HÀNG` |
| 7 | Nước Tăng Lực Redbull Lon Nắp Bật 250ml | Redbull Thái Lan | 20.000đ | **520 lon** | `CÒN HÀNG` |
| 8 | Sting Dâu Tây Đỏ Sleek 330ml | Sting PepsiCo | 12.000đ | **890 lon** | `CÒN HÀNG` |
| 9 | Sting Vàng Sleek 330ml | Sting PepsiCo | 12.000đ | **740 lon** | `CÒN HÀNG` |
| 10 | Sting Blue Sleek 330ml | Sting PepsiCo | 13.000đ | **610 lon** | `CÒN HÀNG` |

---

## 3. Tiêu Chí Nghiệm Thu & Kiểm Thử

1. `admin/inventory.html` có đủ 8 cột trong `<thead>`, chứa cột `<th>Tồn Kho</th>` đứng ngay trước `<th>Trạng Thái</th>`.
2. Toàn bộ 10 hàng trong `admin/inventory.html` có 2 thẻ `<td>` riêng cho Tồn Kho và Trạng Thái.
3. `admin/index.html` đồng bộ hoàn toàn cấu trúc 8 cột và 10 hàng tương tự.
4. Cập nhật `scripts/verify_admin_features_update.py` kiểm tra cột riêng `<th>Tồn Kho</th>`, ô số lượng có icon `fas fa-box`, và ô trạng thái có `badge-status success`.
5. 100% test suites trong repository đều PASS không hồi quy.
