# Thiết Kế: Tinh Chỉnh Câu Chữ Thẻ KPI Thương Hiệu Admin Dashboard

**Ngày:** 13/11/2026  
**Trạng thái:** Approved by User  
**Tác giả:** Antigravity  

---

## 1. Bối cảnh & Lý do thay đổi

- **Hiện trạng:**
  - Thẻ KPI số 3 trên Admin Dashboard (`admin/index.html:100-101`) đang hiển thị:
    - Tiêu đề: `3 Brand`
    - Dòng mô tả: `Monster, Redbull & Sting`
- **Vấn đề:**
  - Tiêu đề dùng từ tiếng Anh `Brand` trong khi 3 thẻ KPI còn lại đều thuần Việt (*Doanh thu tháng*, *Số lon đã bán ra*, *35 Đơn Hàng*).
  - Ký tự `&` trong câu tiếng Việt tạo cảm giác gượng gạo, chắp vá văn bản.
- **Quyết định (Hướng 1):**
  - Chuyển đổi sang phong cách tối giản, cao cấp với dấu bullet `•` ngăn cách:
    - Tiêu đề chính (`h3`): **`3 Thương Hiệu`**
    - Dòng mô tả (`p`): **`Monster • Redbull • Sting`**
  - Đồng thời chuẩn hóa dấu `&` tại 2 vị trí tiêu đề phụ liên quan trong admin (`admin/index.html:276` và `admin/inventory.html:57`) để đảm bảo sự nhất quán toàn diện.

---

## 2. Chi Tiết Thay Đổi

### 2.1. Thẻ KPI số 3 trong `admin/index.html` (lines 98-103)
```html
<div class="kpi-card">
  <div class="kpi-icon cyan"><i class="fas fa-warehouse"></i></div>
  <div class="kpi-info">
    <h3>3 Thương Hiệu</h3>
    <p>Monster • Redbull • Sting</p>
  </div>
</div>
```

### 2.2. Nhãn tóm tắt phụ trong `admin/index.html` (line 276)
- Cũ: `3 Thương hiệu: Monster, Redbull & Sting`
- Mới: `3 Thương hiệu: Monster • Redbull • Sting`

### 2.3. Nhãn tóm tắt phụ trong `admin/inventory.html` (line 57)
- Cũ: `3 Thương hiệu chính thức (Monster, Redbull & Sting) - Sẵn sàng xuất kho`
- Mới: `3 Thương hiệu chính thức (Monster • Redbull • Sting) - Sẵn sàng xuất kho`

---

## 3. Tiêu Chí Nghiệm Thu & Kiểm Thử

1. Thẻ KPI cyan trong `admin/index.html` có chính xác `<h3>3 Thương Hiệu</h3>` và `<p>Monster • Redbull • Sting</p>`.
2. Không còn chuỗi `3 Brand` hoặc `Monster, Redbull & Sting` trong `admin/index.html` và `admin/inventory.html`.
3. Toàn bộ các bộ test hiện hữu đều PASS 100%:
   - `python scripts/verify_admin_kpi_brand_wording.py` PASS.
   - `python verify_implementation.py` PASS (66/66).
   - `python scripts/verify_ui_fixes_and_combo_removal.py` PASS (8/8).
   - `python scripts/verify_footer_sync.py` PASS (144/144).
   - `python scripts/verify_no_product_specs.py` PASS (8/8).
   - `python scripts/verify_clean_brand_pills_and_kicker.py` PASS (9/9).
   - `python scripts/verify_sidebar_filter_sync.py` PASS (31/31).
