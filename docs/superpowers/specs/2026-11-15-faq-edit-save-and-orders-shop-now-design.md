# Thiết Kế: Cố Định Form FAQ #1, Thêm Nút Lưu, Thông Báo "Đã Chuyển" & Điều Hướng Nút Mua Sắm Ngay

**Ngày:** 15/11/2026  
**Trạng thái:** Approved by User  
**Tác giả:** Antigravity  

---

## 1. Bối cảnh & Mục tiêu

Người dùng yêu cầu thực hiện 2 nhóm thay đổi:

1. **Điều hướng nút "Mua Sắm Ngay" trên trang Lịch sử đơn hàng (`pages/orders.html`):**
   - Đổi `href="cart.html"` thành `href="../index.html#monster-products"`.
   - Khi bấm, trình duyệt chuyển về trang chủ và cuộn mượt ngay đến danh mục Menu thực đơn sản phẩm Monster Energy / Redbull / Sting.

2. **Tinh chỉnh giao diện và hành vi Quản lý FAQ trong Admin (`admin/settings.html` & `js/app.js`):**
   - **Form phía trên cố định nội dung Câu #1:**
     - Câu hỏi: `Các dòng nước tăng lực tại Energy Boost gồm những thương hiệu nào?`
     - Thứ tự: `1`
     - Câu trả lời: `Energy Boost chuyên phân phối chính hãng hai dòng thương hiệu hàng đầu: Monster Energy (Original 355ml, Ultra White, Ultra Paradise, Punk Punch) và Redbull Thái Lan (Original 250ml, Lon Nắp Bật 250ml).`
   - **Bổ sung nút "Lưu Thay Đổi":**
     - Nút màu xanh neon `<i class="fas fa-save"></i> Lưu Thay Đổi`.
     - Khi bấm kích hoạt thông báo Toast: `"Đã lưu thay đổi câu hỏi FAQ thành công!"`.
   - **Nút "Chỉnh sửa" ở danh sách FAQ bên dưới:**
     - Khi bấm nút sửa (icon bút `fa-edit`): **Không làm thay đổi** nội dung ở form trên (form trên luôn cố định câu 1).
     - Chỉ hiển thị thông báo Toast: **`"Đã chuyển"`** (hoặc `"Đã chuyển đến câu hỏi FAQ #[id]!"`).

---

## 2. Chi Tiết Kỹ Thuật

### 2.1. Nút "Mua Sắm Ngay" trong `pages/orders.html` (dòng 288)
```html
<a href="../index.html#monster-products" class="btn-add-cart" style="text-decoration: none;">
  <i class="fas fa-shopping-basket"></i> Mua Sắm Ngay
</a>
```

### 2.2. Khối Form FAQ trong `admin/settings.html` (dòng 220-246)
- Tiêu đề khối: `<i class="fas fa-sliders"></i> Cấu Hình & Chỉnh Sửa Câu Hỏi FAQ #1`
- Trường Câu hỏi:
  `value="Các dòng nước tăng lực tại Energy Boost gồm những thương hiệu nào?"`
- Trường Thứ tự:
  `value="1"`
- Trường Câu trả lời:
  `Energy Boost chuyên phân phối chính hãng hai dòng thương hiệu hàng đầu: Monster Energy (Original 355ml, Ultra White, Ultra Paradise, Punk Punch) và Redbull Thái Lan (Original 250ml, Lon Nắp Bật 250ml).`
- Các nút hành động:
  - Nút chính: `<button type="button" class="btn-add-cart" onclick="handleAdminSaveFaq()"><i class="fas fa-save"></i> Lưu Thay Đổi</button>`
  - Nút phụ: `<button type="submit" class="btn-view-detail"><i class="fas fa-plus"></i> Thêm Mới</button>`

### 2.3. Cập nhật trong `js/app.js`
- Thêm hàm `handleAdminSaveFaq()`:
  ```javascript
  function handleAdminSaveFaq() {
    showToast('Đã lưu thay đổi câu hỏi FAQ thành công!', 'success');
  }
  ```
- Cập nhật hàm `handleAdminEditFaq(id, btn)`:
  - Không ghi đè hoặc thay đổi giá trị của `#faq-new-question`, `#faq-new-order`, `#faq-new-answer`.
  - Chỉ kích hoạt thông báo Toast: `showToast('Đã chuyển', 'info')`.

---

## 3. Tiêu Chí Nghiệm Thu & Kiểm Thử

1. `pages/orders.html` có thẻ `<a>` chứa `Mua Sắm Ngay` trỏ đến `../index.html#monster-products`.
2. `admin/settings.html` có form FAQ hiển thị sẵn câu hỏi và câu trả lời của Câu #1.
3. Form FAQ có nút `<button ... onclick="handleAdminSaveFaq()"><i class="fas fa-save"></i> Lưu Thay Đổi</button>`.
4. Bấm nút Sửa trên bất kỳ FAQ nào không thay đổi nội dung ở form trên, và hiển thị thông báo Toast `"Đã chuyển"`.
5. 100% test suites trong hệ thống đều PASS:
   - `python scripts/verify_faq_edit_save_and_orders_link.py` (PASS 100%).
   - `python scripts/verify_admin_features_update.py` (PASS 51/51).
   - `python verify_implementation.py` (PASS 66/66).
   - `python scripts/verify_price_formatting.py` (PASS 49/49).
   - `python scripts/verify_footer_sync.py` (PASS 144/144).
   - `python scripts/verify_sidebar_filter_sync.py` (PASS 31/31).
