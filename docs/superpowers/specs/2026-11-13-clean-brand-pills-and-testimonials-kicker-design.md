# Thiết Kế: Chuẩn Hóa Nhãn Phân Loại Nhanh Và Lược Bỏ Kicker Đánh Giá Hardcode

**Ngày:** 13/11/2026  
**Trạng thái:** Approved by User  
**Tác giả:** Antigravity  

---

## 1. Bối cảnh & Lý do thay đổi

1. **Thanh phân loại nhanh theo hãng (`quick-brand-nav`):**
   - Đang hiển thị text kèm số vị hardcode: `Monster Energy (4 vị)`, `Redbull Thái Lan (3 vị)`, `Sting PepsiCo (3 vị)`.
   - Việc ghi cứng số vị gây rủi ro sai lệch thông tin khi danh mục sản phẩm thay đổi hoặc khi quản trị viên cập nhật kho hàng trong admin.
   - Thống nhất loại bỏ phần `(4 vị)` và `(3 vị)`, chỉ giữ lại tên thương hiệu chuẩn: `Monster Energy`, `Redbull Thái Lan`, `Sting PepsiCo`.
2. **Khu vực Đánh giá khách hàng (`testimonials-head`):**
   - Đang có thẻ kicker marketing: `<span class="section-kicker"><i class="fas fa-award"></i> 12.400+ KHÁCH HÀNG TIN DÙNG</span>`.
   - Con số 12.400+ là số liệu tĩnh chưa kết nối với dữ liệu bán hàng thực tế từ hệ thống quản trị, làm giảm tính tự nhiên và minh bạch của website.
   - Thống nhất loại bỏ hoàn toàn thẻ kicker này.

---

## 2. Chi Tiết Thay Đổi Trong `index.html`

### 2.1. Chuẩn hóa 3 nút Phân loại nhanh (`quick-brand-nav`)
- Vị trí: dòng 621-630 trong `index.html`.
- Thay đổi:
  - Nút 1: `<i class="fas fa-bolt" style="color: var(--primary);"></i> Monster Energy`
  - Nút 2: `<i class="fas fa-fire" style="color: var(--secondary);"></i> Redbull Thái Lan`
  - Nút 3: `<i class="fas fa-bolt" style="color: #FF0055;"></i> Sting PepsiCo`
- Giữ nguyên toàn bộ cấu trúc neo: `href="#monster-products"`, `data-target="..."`, `onclick="handleNavBrandClick(event, this, '...')"` và hiệu ứng active.

### 2.2. Lược bỏ thẻ Kicker tại `testimonials-head`
- Vị trí: dòng 947 trong `index.html`.
- Xóa bỏ dòng: `<span class="section-kicker"><i class="fas fa-award"></i> 12.400+ KHÁCH HÀNG TIN DÙNG</span>`.
- Tiêu đề khối giữ nguyên: `<h2 class="section-title">ĐƯỢC TIN DÙNG BỞI GIỚI <span>CHUYÊN NGHIỆP</span></h2>`.

---

## 3. Tiêu Chí Nghiệm Thu & Kiểm Thử

1. **`index.html`:**
   - Không còn chuỗi `(4 vị)` hay `(3 vị)`.
   - Không còn chuỗi `12.400+ KHÁCH HÀNG TIN DÙNG` hoặc thẻ `.section-kicker`.
   - Nút phân loại nhanh vẫn hoạt động cuộn mượt khi click.
2. **Kiểm thử hồi quy:**
   - 66/66 checks trong `verify_implementation.py` PASS.
   - 8/8 checks trong `scripts/verify_ui_fixes_and_combo_removal.py` PASS.
   - 144/144 checks trong `scripts/verify_footer_sync.py` PASS.
   - 8/8 checks trong `scripts/verify_no_product_specs.py` PASS.
   - Viết test script `scripts/verify_clean_brand_pills_and_kicker.py` xác minh PASS 100%.
