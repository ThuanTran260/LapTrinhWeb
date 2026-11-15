# Thiết Kế: Đưa Số Lượng Tồn Kho Ra Cạnh Badge Trạng Thái (admin/inventory.html & admin/index.html)

**Ngày:** 15/11/2026  
**Trạng thái:** Chờ User duyệt & Proceed  
**Tác giả:** Antigravity  

---

## 1. Bối cảnh & Mục tiêu

Người dùng quan sát cột trạng thái/tồn kho trong bảng quản lý kho hàng và yêu cầu:
> "cột phần tồn kho tôi nghĩ ta nên đưa số ra kế bên phần còn hàng cho rõ số dễ nhìn hơn /brainstorming"

**Hiện trạng:**
Trong ô `<td>` của cột Trạng Thái trên bảng kho ở `admin/inventory.html` và `admin/index.html`:
```html
<td>
  <span class="badge-status success">CÒN HÀNG</span>
  <small style="color: var(--text-muted); display: block; margin-top: 4px; font-size: 0.78rem;">
    <i class="fas fa-box"></i> Tồn: 1.250 lon
  </small>
</td>
```
- Nhược điểm: Chữ `Tồn: ... lon` bị xuống dòng, chữ nhỏ màu xám mờ (`--text-muted`) nên khó nhận diện nhanh số lượng tồn kho và chiếm thêm chiều cao mỗi dòng bảng.

**Mục tiêu:**
Chuyển đổi cách hiển thị sang **Phương án 1 (Flex ngang inline)**:
- Badge `CÒN HÀNG` và số lượng tồn kho nằm cạnh nhau trên cùng một hàng ngang.
- Số lượng tồn kho hiển thị màu trắng sáng (`#FFF`, `font-weight: 700`, `font-size: 0.85rem`), đi kèm icon hộp màu xanh neon (`var(--primary)`).
- Áp dụng đồng bộ cho toàn bộ 10 sản phẩm trên cả 2 bảng kho:
  1. `admin/inventory.html` (Bảng quản lý kho sản phẩm)
  2. `admin/index.html` (Bảng kho sản phẩm nhanh tại Dashboard)

---

## 2. Chi Tiết Kỹ Thuật

### 2.1. Cấu trúc HTML mới cho ô Trạng Thái & Tồn Kho

```html
<td>
  <div style="display: inline-flex; align-items: center; gap: 8px; white-space: nowrap;">
    <span class="badge-status success">CÒN HÀNG</span>
    <span style="color: #FFF; font-size: 0.85rem; font-weight: 700;">
      <i class="fas fa-box" style="color: var(--primary); margin-right: 4px;"></i>Tồn: {SO_LUONG} lon
    </span>
  </div>
</td>
```

### 2.2. Danh sách dữ liệu 10 sản phẩm đồng bộ

| STT | Tên Sản Phẩm | Thương Hiệu | Số lượng tồn kho mới |
| :---: | :--- | :--- | :---: |
| 1 | Monster Energy Original 355ml | Monster Energy | `Tồn: 1.250 lon` |
| 2 | Monster Zero Ultra White 500ml | Monster Energy | `Tồn: 1.250 lon` |
| 3 | Monster Ultra Paradise 500ml | Monster Energy | `Tồn: 1.250 lon` |
| 4 | Monster Ultra Punk Punch 500ml | Monster Energy | `Tồn: 1.250 lon` |
| 5 | Nước Tăng Lực Redbull Original 250ml | Redbull Thái Lan | `Tồn: 680 lon` |
| 6 | Nước Tăng Lực Redbull Thái Chai Thủy Tinh 150ml | Redbull Thái Lan | `Tồn: 450 lon` |
| 7 | Nước Tăng Lực Redbull Lon Nắp Bật 250ml | Redbull Thái Lan | `Tồn: 520 lon` |
| 8 | Sting Dâu Tây Đỏ Sleek 330ml | Sting PepsiCo | `Tồn: 890 lon` |
| 9 | Sting Vàng Sleek 330ml | Sting PepsiCo | `Tồn: 740 lon` |
| 10 | Sting Blue Sleek 330ml | Sting PepsiCo | `Tồn: 610 lon` |

---

## 3. Tiêu Chí Nghiệm Thu & Kiểm Thử

1. Cả 10 sản phẩm trong `admin/inventory.html` đều có cấu trúc inline flex, số lượng tồn kho màu trắng sáng nằm cạnh badge `CÒN HÀNG`.
2. Cả 10 sản phẩm trong `admin/index.html` đồng bộ cấu trúc tương tự.
3. Không làm bể layout bảng trên màn hình desktop và tablet/mobile (sử dụng `white-space: nowrap` và `overflow-x: auto` của bảng).
4. Cập nhật `scripts/verify_admin_features_update.py` kiểm tra cấu trúc inline mới: 100% tiêu chí PASS.
5. Tất cả regression test suites (`verify_implementation.py`, `verify_price_formatting.py`, `verify_footer_sync.py`, `verify_sidebar_filter_sync.py`, `verify_faq_edit_save_and_orders_link.py`) đều PASS 100%.
