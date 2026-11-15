# Thiết Kế: Điều Hướng Nút "Mua Sắm Ngay" Trên Trang Lịch Sử Đơn Hàng

**Ngày:** 15/11/2026  
**Trạng thái:** Approved by User  
**Tác giả:** Antigravity  

---

## 1. Bối cảnh & Lý do thay đổi

- **Hiện trạng:**
  - Trên trang lịch sử đơn hàng (`pages/orders.html:288`), nút **"Mua Sắm Ngay"** (`.btn-add-cart`) đang trỏ đến `cart.html` (`href="cart.html"`).
- **Vấn đề:**
  - Khách hàng đang xem lịch sử đơn hàng hoặc vừa hoàn tất đơn, khi bấm vào nút kêu gọi hành động (CTA) "Mua Sắm Ngay" lại bị chuyển hướng vào trang Giỏ Hàng (`cart.html`) thay vì vào menu/danh mục sản phẩm để mua sắm tiếp. Điều này tạo trải nghiệm rời rạc và không trực quan.
- **Quyết định (Phương án 1):**
  - Chuyển hướng liên kết của nút **"Mua Sắm Ngay"** thành:
    `href="../index.html#monster-products"`
  - Khi khách hàng nhấn nút, trình duyệt sẽ chuyển về trang chủ và cuộn mượt đến ngay vị trí Menu thực đơn sản phẩm (khu vực Monster Energy cùng thanh chuyển đổi nhanh sang Redbull & Sting).
  - Nút bên trái (`Quay lại cửa hàng`) giữ nguyên `href="../index.html"`, tạo nên cặp nút bổ trợ hoàn hảo: một nút về đầu trang chủ, một nút đi thẳng vào menu thực đơn để mua sắm tiếp.

---

## 2. Chi Tiết Kỹ Thuật

### 2.1. File Cần Chỉnh Sửa
- **File:** `pages/orders.html` (dòng 286-290)
- **Trước thay đổi:**
  ```html
  <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--border-color); flex-wrap: wrap; gap: 12px;">
    <a href="../index.html" class="btn-view-detail"><i class="fas fa-arrow-left"></i> Quay lại cửa hàng</a>
    <a href="cart.html" class="btn-add-cart" style="text-decoration: none;"><i class="fas fa-shopping-basket"></i> Mua Sắm Ngay</a>
  </div>
  ```
- **Sau thay đổi:**
  ```html
  <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--border-color); flex-wrap: wrap; gap: 12px;">
    <a href="../index.html" class="btn-view-detail"><i class="fas fa-arrow-left"></i> Quay lại cửa hàng</a>
    <a href="../index.html#monster-products" class="btn-add-cart" style="text-decoration: none;"><i class="fas fa-shopping-basket"></i> Mua Sắm Ngay</a>
  </div>
  ```

---

## 3. Tiêu Chí Nghiệm Thu & Kiểm Thử

1. Thẻ `<a>` chứa text `Mua Sắm Ngay` trong `pages/orders.html` có chính xác thuộc tính `href="../index.html#monster-products"`.
2. Không còn thẻ `<a>` nào trong `pages/orders.html` trỏ đến `cart.html` với nội dung `Mua Sắm Ngay`.
3. Toàn bộ các bộ kiểm thử hệ thống hiện có đều PASS 100%:
   - `python scripts/verify_orders_shop_now_link.py` (PASS 100%).
   - `python verify_implementation.py` (PASS 66/66).
   - `python scripts/verify_admin_features_update.py` (PASS 51/51).
   - `python scripts/verify_footer_sync.py` (PASS 144/144).
   - `python scripts/verify_sidebar_filter_sync.py` (PASS 31/31).
