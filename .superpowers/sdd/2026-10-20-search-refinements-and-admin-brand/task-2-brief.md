# Task 2 Brief: Triển Khai Dropdown Gợi Ý Tìm Kiếm Trong Modal Tìm Kiếm Nâng Cao

## Mục tiêu
Tạo dropdown gợi ý Dark Neon thời gian thực trong Modal Tìm Kiếm Nâng Cao (`#modal-adv-search` trên `index.html`). Khi người dùng gõ từ khóa (ví dụ "ultra"), danh sách các lon phù hợp sẽ hiện ra ngay dưới ô input kèm ảnh thumbnail, tên lon, thương hiệu và giá. Click vào sản phẩm sẽ tự điền tên lon và đồng bộ select thương hiệu / khoảng giá.

## Các file cần sửa
1. `css/style.css`
2. `js/app.js`
3. `index.html`

## Yêu cầu chi tiết

### 1. `css/style.css`
Thêm các class Dark Neon Glassmorphism:
```css
/* Advanced Search Suggestions Dropdown */
.adv-search-input-wrapper {
  position: relative;
}
.adv-search-suggestions {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  background: rgba(14, 16, 23, 0.98);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(0, 230, 118, 0.3);
  border-radius: var(--radius-sm);
  max-height: 240px;
  overflow-y: auto;
  z-index: 1000;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
  display: none;
}
.adv-search-suggestions.active {
  display: block;
}
.adv-suggestion-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  cursor: pointer;
  transition: background 0.15s ease;
}
.adv-suggestion-item:last-child {
  border-bottom: none;
}
.adv-suggestion-item:hover {
  background: rgba(0, 230, 118, 0.12);
}
.adv-suggestion-left {
  display: flex;
  align-items: center;
  gap: 10px;
}
.adv-suggestion-thumb {
  width: 26px;
  height: 34px;
  object-fit: contain;
}
.adv-suggestion-name {
  font-size: 0.82rem;
  font-weight: 600;
  color: #FFF;
  margin: 0;
}
.adv-suggestion-brand {
  font-size: 0.72rem;
  color: var(--text-dim);
}
.adv-suggestion-price {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--primary);
  white-space: nowrap;
}
```

### 2. `js/app.js`
1. Khai báo danh mục sản phẩm tĩnh 10 sản phẩm:
```javascript
const STATIC_PRODUCTS_CATALOG = [
  { id: 'mn-1', name: 'Monster Energy Original 355ml', brand: 'Monster Energy', brandKey: 'monster', price: '45.000đ', priceKey: '20to50', image: 'assets/images/monster/original.webp' },
  { id: 'mn-2', name: 'Monster Zero Ultra White 500ml', brand: 'Monster Energy', brandKey: 'monster', price: '48.000đ', priceKey: '20to50', image: 'assets/images/monster/ultra-white.webp' },
  { id: 'mn-3', name: 'Monster Ultra Paradise 500ml', brand: 'Monster Energy', brandKey: 'monster', price: '48.000đ', priceKey: '20to50', image: 'assets/images/monster/ultra-paradise.webp' },
  { id: 'mn-4', name: 'Monster Ultra Punk Punch 500ml', brand: 'Monster Energy', brandKey: 'monster', price: '50.000đ', priceKey: '20to50', image: 'assets/images/monster/ultra-punk-punch.webp' },
  { id: 'rb-1', name: 'Nước Tăng Lực Redbull Original 250ml', brand: 'Redbull Thái Lan', brandKey: 'redbull', price: '18.000đ', priceKey: 'under20', image: 'assets/images/redbull/redbull-original.webp' },
  { id: 'rb-2', name: 'Nước Tăng Lực Redbull Thái Lan 250ml', brand: 'Redbull Thái Lan', brandKey: 'redbull', price: '18.000đ', priceKey: 'under20', image: 'assets/images/redbull/redbull-thai.webp' },
  { id: 'rb-3', name: 'Nước Tăng Lực Redbull Nắp Bật 250ml', brand: 'Redbull Thái Lan', brandKey: 'redbull', price: '20.000đ', priceKey: '20to50', image: 'assets/images/redbull/redbull-lon-vua.webp' },
  { id: 'st-1', name: 'Nước Tăng Lực Sting Dâu Tây Đỏ 330ml', brand: 'Sting PepsiCo', brandKey: 'sting', price: '12.000đ', priceKey: 'under20', image: 'assets/images/sting/sting-dau.webp' },
  { id: 'st-2', name: 'Nước Tăng Lực Sting Vàng Sleek 330ml', brand: 'Sting PepsiCo', brandKey: 'sting', price: '12.000đ', priceKey: 'under20', image: 'assets/images/sting/sting-gold.webp' },
  { id: 'st-3', name: 'Nước Tăng Lực Sting Blue Sleek 320ml', brand: 'Sting PepsiCo', brandKey: 'sting', price: '13.000đ', priceKey: 'under20', image: 'assets/images/sting/sting-vietquat.webp' }
];
```

2. Viết hàm `handleAdvKeywordInput(val)`:
   - Nếu `val` trống: hiển thị 3 sản phẩm tiêu biểu (Monster Original, Redbull Original, Sting Dâu).
   - Nếu `val` có ký tự: lọc sản phẩm không phân biệt hoa/thường, không phân biệt dấu tiếng Việt đơn giản (`toLowerCase()`).
   - Render HTML danh sách `.adv-suggestion-item` vào `#adv-search-suggestions` và thêm class `active`.
   - Mỗi item gọi `onclick="selectAdvSearchSuggestion(${idx})"`.
   - Nếu không có kết quả: hiển thị thông báo "Không tìm thấy sản phẩm gợi ý phù hợp".

3. Viết hàm `selectAdvSearchSuggestion(idx)`:
   - Lấy sản phẩm từ `STATIC_PRODUCTS_CATALOG[idx]`.
   - Điền tên vào `#adv-search-keyword`.
   - Đồng bộ select: `#adv-search-brand` thành `prod.brandKey`, `#adv-search-price` thành `prod.priceKey`.
   - Cập nhật `#adv-search-preview`: `Kết quả mẫu phù hợp tiêu chí: <strong style="color: #FFF;">${prod.name} (${prod.price})</strong>`.
   - Gọi `closeAdvSuggestions()`.

4. Viết hàm `closeAdvSuggestions()`:
   - Gỡ class `active` khỏi `#adv-search-suggestions`.

5. Bổ sung sự kiện đóng:
   - Trong listener `click` toàn cục: nếu `!e.target.closest('.adv-search-input-wrapper')` thì gọi `closeAdvSuggestions()`.
   - Trong listener `keydown` Escape: gọi `closeAdvSuggestions()`.

### 3. `index.html`
- Trong `#modal-adv-search`, tìm `#adv-search-keyword` và bọc trong:
```html
<div class="admin-form-group full-width" style="margin-bottom: 14px;">
  <label class="admin-form-label"><i class="fas fa-search" style="color: var(--primary);"></i> Tên sản phẩm / Từ khóa</label>
  <div class="adv-search-input-wrapper">
    <input type="text" id="adv-search-keyword" class="admin-form-input" placeholder="VD: Original, Ultra, Dâu tây, Chai vàng..." value="Original" oninput="handleAdvKeywordInput(this.value)" onfocus="handleAdvKeywordInput(this.value)" autocomplete="off" />
    <div id="adv-search-suggestions" class="adv-search-suggestions"></div>
  </div>
</div>
```
- Gắn `id="adv-search-preview"` vào khối preview mẫu để JS cập nhật.

### 4. Kiểm tra & Commit
- Chạy `python verify_implementation.py` (đảm bảo 66/66 test cases PASS).
- Commit:
  `git add css/style.css js/app.js index.html`
  `git commit -m "feat(search): add live suggestion dropdown to advanced search modal"`
  (TUYỆT ĐỐI KHÔNG CHẠY GIT PUSH - RULE 1).
- Ghi báo cáo vào:
  `d:\LapTrinhWeb\.superpowers\sdd\2026-10-20-search-refinements-and-admin-brand\task-2-report.md`
