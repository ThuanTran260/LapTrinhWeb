# Task 4 Brief: Kiểm Thử Toàn Diện & Nghiệm Thu

## Mục tiêu
Kiểm thử tự động toàn diện tất cả các thay đổi từ Task 1, 2, 3:
1. Xác nhận không còn `.search-quick-tags` trong 4 file storefront HTML.
2. Xác nhận dropdown gợi ý tìm kiếm nâng cao đã tích hợp đầy đủ trong HTML, CSS và JS.
3. Xác nhận thẻ KPI Brand và tiêu đề Admin hiển thị đúng 3 Brand và nhãn Thương hiệu gọn gàng.
4. Đảm bảo toàn bộ 66/66 checks của `verify_implementation.py` và 45/45 tiêu chí rubric PASS 100%.

## Yêu cầu chi tiết
1. Tạo script kiểm thử tự động `scratch/verify_search_refinements.py` kiểm tra:
   - Không còn class `search-quick-tags` trong `index.html` và 3 trang chi tiết `pages/product-detail*.html`.
   - `index.html` có `#adv-search-suggestions`, `adv-search-input-wrapper`, `oninput="handleAdvKeywordInput(this.value)"`, `#adv-search-preview`.
   - `css/style.css` có `.adv-search-suggestions`, `.adv-suggestion-item`, `.adv-suggestion-price`.
   - `js/app.js` có `STATIC_PRODUCTS_CATALOG`, `handleAdvKeywordInput`, `selectAdvSearchSuggestion`, `closeAdvSuggestions`.
   - `admin/index.html` có `3 Brand`, `<p>Thương hiệu</p>`, không còn `Monster Energy & Redbull`.
   - `admin/inventory.html` có `3 Thương hiệu`.
2. Chạy script: `python scratch/verify_search_refinements.py`.
3. Chạy `python verify_implementation.py` (đảm bảo 66/66 checks PASS).
4. Dọn dẹp thư mục `scratch/` trong workspace nếu có, giữ working tree sạch sẽ.
5. Ghi báo cáo vào:
   `d:\LapTrinhWeb\.superpowers\sdd\2026-10-20-search-refinements-and-admin-brand\task-4-report.md`.
6. Tuyệt đối tuân thủ RULE 1: Không git push.
