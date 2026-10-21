# Task 1 Brief: Xóa Quick Tags Trong Dropdown Tìm Kiếm Storefront

## Mục tiêu
Loại bỏ hoàn toàn hàng quick tag `#MonsterOriginal #RedbullThai #StingDau...` trong dropdown tìm kiếm Header trên 4 trang storefront:
- `index.html`
- `pages/product-detail.html`
- `pages/product-detail-redbull.html`
- `pages/product-detail-sting.html`

## Yêu cầu chi tiết
1. Trong 4 file trên, tìm khối:
   ```html
   <div class="search-quick-tags">
     ...các thẻ <a> có class="search-quick-tag"...
   </div>
   ```
   và xóa bỏ hoàn toàn khối `div` này.
2. Giữ nguyên:
   - `<div class="search-dropdown-header">...</div>`
   - `<div class="search-static-list">...</div>`
3. Kiểm tra xác nhận:
   - Chạy `git grep "search-quick-tags" "*.html"` để xác nhận không còn tồn tại trong bất kỳ file HTML nào.
   - Chạy `python verify_implementation.py` đảm bảo toàn bộ 66/66 test cases PASS 100%.
4. Commit cục bộ:
   `git add index.html pages/product-detail*.html`
   `git commit -m "feat(search): remove search quick tags from storefront dropdowns"`
   (TUYỆT ĐỐI KHÔNG CHẠY GIT PUSH - RULE 1).
5. Ghi báo cáo kết quả vào:
   `d:\LapTrinhWeb\.superpowers\sdd\2026-10-20-search-refinements-and-admin-brand\task-1-report.md`
