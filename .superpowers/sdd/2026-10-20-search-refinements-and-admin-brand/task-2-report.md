# Báo Cáo Triển Khai Task 2: Dropdown Gợi Ý Tìm Kiếm Trong Modal Tìm Kiếm Nâng Cao

## 1. Thông Tin Chung
- **Task**: Task 2 - Triển Khai Dropdown Gợi Ý Tìm Kiếm Trong Modal Tìm Kiếm Nâng Cao
- **Trạng thái**: DONE (Hoàn thành 100%)
- **Nhánh Git**: `feat/static-rubric-features`
- **Commit Hash**: `4a111a2`
- **Commit Message**: `feat(search): add live suggestion dropdown to advanced search modal`
- **Quy tắc an toàn**: TUYỆT ĐỐI TUÂN THỦ RULE 1 (KHÔNG thực hiện `git push`).

---

## 2. Các Thay Đổi Chi Tiết

### 2.1. `css/style.css`
Đã bổ sung bộ class Dark Neon Glassmorphism phục vụ dropdown gợi ý:
- `.adv-search-input-wrapper`: Khối định vị `position: relative`.
- `.adv-search-suggestions`: Dropdown glassmorphism (`rgba(14, 16, 23, 0.98)`, `backdrop-filter: blur(16px)`, border neon green mờ `rgba(0, 230, 118, 0.3)`, max-height 240px, overflow-y auto, box-shadow nổi bật).
- `.adv-search-suggestions.active`: Kích hoạt hiển thị dropdown `display: block`.
- `.adv-suggestion-item`: Flex container hiển thị item với hover effect neon green nhẹ nhàng (`rgba(0, 230, 118, 0.12)`).
- `.adv-suggestion-left`, `.adv-suggestion-thumb`, `.adv-suggestion-name`, `.adv-suggestion-brand`, `.adv-suggestion-price`: Bố cục ảnh thumbnail 26x34px, tên lon màu sáng, thương hiệu dimmed và giá tiền màu xanh neon.

### 2.2. `js/app.js`
- **`STATIC_PRODUCTS_CATALOG`**: Khai báo danh mục sản phẩm tĩnh 10 lon nước tăng lực (Monster Original, Ultra White, Ultra Paradise, Ultra Punk Punch, Redbull Original, Redbull Thái, Redbull Nắp Bật, Sting Dâu Tây, Sting Vàng Sleek, Sting Blue Sleek) kèm đầy đủ metadata (`brandKey`, `priceKey`, `price`, `image`).
- **`handleAdvKeywordInput(val)`**: Xử lý lọc thời gian thực khi người dùng gõ phím hoặc focus vào ô input:
  - Khi ô input trống: hiển thị 3 sản phẩm tiêu biểu (Monster Original, Redbull Original, Sting Dâu).
  - Khi có từ khóa: tìm kiếm theo tên hoặc thương hiệu không phân biệt hoa/thường và hỗ trợ tiếng Việt không dấu.
  - Tự động hiển thị fallback thông báo khi không tìm thấy kết quả.
  - Bổ sung `SITE_ROOT` hỗ trợ đường dẫn ảnh chính xác.
- **`openAdvSuggestions()`**: Hỗ trợ mở gợi ý dựa trên từ khóa hiện có.
- **`selectAdvSearchSuggestion(idx)`**: Khi click vào lon gợi ý:
  - Tự động điền tên lon vào `#adv-search-keyword`.
  - Tự động đồng bộ select thương hiệu `#adv-search-brand` (`prod.brandKey`).
  - Tự động đồng bộ select khoảng giá `#adv-search-price` (`prod.priceKey`).
  - Cập nhật dòng preview mẫu `#adv-search-preview`.
  - Đóng dropdown qua `closeAdvSuggestions()`.
- **`closeAdvSuggestions()`**: Đóng dropdown gợi ý.
- **Sự kiện đóng dropdown**:
  - Tích hợp vào global click listener: đóng `#adv-search-suggestions` khi click ngoài `.adv-search-input-wrapper`.
  - Tích hợp vào Escape keydown listener: đóng cả modal và dropdown.
  - Tự động đóng dropdown khi `closeAdvancedSearchModal()` được gọi.

### 2.3. `index.html`
- Trong `#modal-adv-search`, bọc ô input `#adv-search-keyword` bên trong `.adv-search-input-wrapper`.
- Bổ sung dropdown container `<div id="adv-search-suggestions" class="adv-search-suggestions"></div>`.
- Gắn các thuộc tính tương tác: `oninput="handleAdvKeywordInput(this.value)"`, `onfocus="handleAdvKeywordInput(this.value)"`, `autocomplete="off"`.
- Gắn `id="adv-search-preview"` vào khối preview mẫu để JS đồng bộ hiển thị sản phẩm vừa chọn.

---

## 3. Kết Quả Kiểm Thử

### 3.1. Hồi quy hệ thống (`verify_implementation.py`)
- Chạy kiểm thử: `python verify_implementation.py`
- Kết quả: **ALL 66 CHECKS PASSED PERFECTLY!** (100% pass)

### 3.2. Tiêu chí chức năng Task 2
- Kiểm tra sự tồn tại của toàn bộ CSS classes trong `css/style.css`: PASS.
- Kiểm tra các hàm JS (`STATIC_PRODUCTS_CATALOG`, `handleAdvKeywordInput`, `selectAdvSearchSuggestion`, `closeAdvSuggestions`, click outside, escape): PASS.
- Kiểm tra cấu trúc HTML trong `index.html`: PASS.
