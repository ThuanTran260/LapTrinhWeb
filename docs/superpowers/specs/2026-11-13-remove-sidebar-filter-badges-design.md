# Thiết Kế: Lược Bỏ Nhãn Đếm Số Lon Và Khoảng Giá Phụ Khỏi Sidebar Bộ Lọc

**Ngày:** 13/11/2026  
**Trạng thái:** Approved by User  
**Tác giả:** Antigravity  

---

## 1. Bối cảnh & Lý do thay đổi

- **Hiện trạng:**
  - Sidebar bộ lọc tìm kiếm tại trang chủ (`index.html`) và trang kết quả tìm kiếm (`pages/search-results.html`) đang gắn các thẻ `.filter-option-count` phía bên phải mỗi lựa chọn radio:
    - Nhóm Thương hiệu: `10 lon`, `4 lon`, `3 lon`, `3 lon`.
    - Nhóm Khoảng giá: `12k - 18k`, `20k - 50k`, `Lon lẻ & Lốc`.
- **Vấn đề:**
  - Các giá trị này là dữ liệu tĩnh hardcode, không tự động cập nhật khi Admin thêm bớt sản phẩm trong kho.
  - Cụm từ "Lon lẻ & Lốc" là tàn dư từ các phiên bản cũ trước khi loại bỏ combo thùng.
  - Modal Tìm kiếm nâng cao (`modal-adv-search`) hiện chỉ hiển thị nhãn radio/select thuần túy, việc sidebar có các nhãn phụ gây thiếu nhất quán giữa 2 công cụ tìm kiếm trên cùng hệ thống.
- **Quyết định:**
  - Lược bỏ hoàn toàn toàn bộ các thẻ `<span class="filter-option-count">...</span>` khỏi cả 2 nhóm "Phân loại thương hiệu" và "Khoảng giá" trên cả `index.html` và `pages/search-results.html`.
  - Cập nhật test script `scripts/verify_sidebar_filter_sync.py` để bảo đảm tính đồng nhất giữa 2 trang sau khi loại bỏ.

---

## 2. Chi Tiết Thay Đổi

### 2.1. Trang chủ `index.html` (lines 544-594)
- Xóa 4 thẻ `filter-option-count` ở nhóm Thương hiệu: `10 lon`, `4 lon`, `3 lon`, `3 lon`.
- Xóa 3 thẻ `filter-option-count` ở nhóm Khoảng giá: `12k - 18k`, `20k - 50k`, `Lon lẻ & Lốc`.

### 2.2. Trang tìm kiếm `pages/search-results.html` (lines 326-376)
- Xóa 4 thẻ `filter-option-count` ở nhóm Thương hiệu: `10 lon`, `4 lon`, `3 lon`, `3 lon`.
- Xóa 3 thẻ `filter-option-count` ở nhóm Khoảng giá: `12k - 18k`, `20k - 50k`, `Lon lẻ & Lốc`.

### 2.3. Script kiểm thử `scripts/verify_sidebar_filter_sync.py`
- Cập nhật các danh sách kỳ vọng:
  - `expected_brands`: chỉ kiểm tra `val` và `label` thuần túy, kiểm tra không còn thẻ `filter-option-count` trên cả 2 trang.
  - `expected_prices`: chỉ kiểm tra `val` và `label` thuần túy, kiểm tra không còn thẻ `filter-option-count` trên cả 2 trang.

---

## 3. Tiêu Chí Nghiệm Thu & Kiểm Thử

1. Cả `index.html` và `pages/search-results.html` đều không còn chứa bất kỳ thẻ `<span class="filter-option-count">` nào.
2. Các input radio và nhãn thương hiệu (`Tất cả thương hiệu`, `Monster Energy`, `Redbull Thái Lan`, `Sting PepsiCo`) và khoảng giá (`Tất cả khoảng giá`, `Dưới 20.000đ`, `20.000đ - 50.000đ`, `Trên 50.000đ`) vẫn hoạt động chính xác khi submit form lọc.
3. Toàn bộ các bộ test hiện hữu đều PASS 100%:
   - `python scripts/verify_sidebar_filter_sync.py` PASS.
   - `python verify_implementation.py` PASS.
   - `python scripts/verify_ui_fixes_and_combo_removal.py` PASS.
   - `python scripts/verify_footer_sync.py` PASS.
   - `python scripts/verify_no_product_specs.py` PASS.
   - `python scripts/verify_clean_brand_pills_and_kicker.py` PASS.
