# Đặc Tả Kỹ Thuật (Design Spec): Tinh Chỉnh Tìm Kiếm & Chuẩn Hóa Thương Hiệu Admin

> **Ngày tạo:** 2026-10-20  
> **Trạng thái:** Đã được người dùng phê duyệt (Approved)  
> **Nguyên tắc cốt lõi:** **100% Website Tĩnh (Không running backend/CSDL)**. Chấm trực tiếp từ `index.html` trên trình duyệt Google Chrome. Không làm mất dữ liệu demo.

---

## 1. Bối Cảnh & Mục Tiêu

Hệ thống Energy Boost hiện có 3 thương hiệu chính thức: **Monster Energy**, **Redbull** và **Sting**. Sau khi hoàn thành các tính năng theo Rubric SGU, người dùng yêu cầu 3 điểm tinh chỉnh giao diện:
1. **Xóa Quick Tags** (`#MonsterOriginal`, `#RedbullThai`...) trong dropdown tìm kiếm trên Header của trang chủ và các trang chi tiết, giúp thanh tìm kiếm tinh gọn và tập trung thẳng vào danh sách sản phẩm.
2. **Hiển thị Gợi Ý Tìm Kiếm (Live Suggestions Dropdown)** trong Modal Tìm Kiếm Nâng Cao (`#modal-adv-search`): Khi người dùng gõ từ khóa (ví dụ: `"ultra"`), dropdown gợi ý xuất hiện ngay dưới ô nhập với danh sách các sản phẩm khớp tên, kèm thumbnail ảnh, tên lon và giá bán. Click vào sản phẩm sẽ tự động điền từ khóa và đồng bộ bộ lọc.
3. **Chuẩn hóa thẻ thống kê Brand trong Admin**:
   - Thẻ KPI Brand: Cập nhật từ `2 Brand` thành `3 Brand`, dòng chữ bên dưới đổi từ `Monster Energy & Redbull` thành `Thương hiệu` (không liệt kê tên thương hiệu).
   - Phụ đề trang Admin: Cập nhật từ 2 thành 3 thương hiệu.

---

## 2. Chi Tiết Kiến Trúc & Thiết Kế

### 2.1. Storefront: Xóa Quick Tags Trong Search Dropdown
* **Các file áp dụng:**
  * `index.html`
  * `pages/product-detail.html`
  * `pages/product-detail-redbull.html`
  * `pages/product-detail-sting.html`
* **Nội dung thay đổi:**
  * Xóa bỏ hoàn toàn khối `<div class="search-quick-tags">...</div>`.
  * Giữ nguyên tiêu đề `<div class="search-dropdown-header">...</div>` và danh sách sản phẩm mẫu `.search-static-list`.

### 2.2. Modal Tìm Kiếm Nâng Cao: Dropdown Gợi Ý Động Tĩnh
* **Vị trí hiển thị:** Trong `#modal-adv-search` trên `index.html`.
* **Cấu trúc HTML:**
  * Bọc trường `#adv-search-keyword` trong thẻ có `position: relative`.
  * Thêm thẻ dropdown `#adv-search-suggestions` ngay dưới input.
* **Danh mục sản phẩm tĩnh (`STATIC_PRODUCTS_CATALOG` trong `js/app.js`):**
  * Monster Original (355ml - 45.000đ - Monster Energy - `assets/images/monster/original.webp`)
  * Monster Zero Ultra White (500ml - 48.000đ - Monster Energy - `assets/images/monster/ultra-white.webp`)
  * Monster Ultra Paradise (500ml - 48.000đ - Monster Energy - `assets/images/monster/ultra-paradise.webp`)
  * Monster Ultra Punk Punch (500ml - 50.000đ - Monster Energy - `assets/images/monster/ultra-punk-punch.webp`)
  * Redbull Original (250ml - 18.000đ - Redbull Thái Lan - `assets/images/redbull/redbull-original.webp`)
  * Redbull Thái Lan (250ml - 18.000đ - Redbull Thái Lan - `assets/images/redbull/redbull-thai.webp`)
  * Redbull Nắp Bật (250ml - 20.000đ - Redbull Thái Lan - `assets/images/redbull/redbull-lon-vua.webp`)
  * Sting Dâu Tây Đỏ (330ml - 12.000đ - Sting PepsiCo - `assets/images/sting/sting-dau.webp`)
  * Sting Vàng Sleek (330ml - 12.000đ - Sting PepsiCo - `assets/images/sting/sting-gold.webp`)
  * Sting Blue Sleek (320ml - 13.000đ - Sting PepsiCo - `assets/images/sting/sting-vietquat.webp`)
* **Logic điều khiển (`js/app.js`):**
  * `handleAdvKeywordInput(value)`:
    * Khi gõ chữ: chuẩn hóa chuỗi (bỏ dấu tiếng Việt, lowercase). Lọc danh sách khớp với tên sản phẩm hoặc thương hiệu.
    * Render kết quả HTML vào `#adv-search-suggestions`.
    * Nếu không khớp sản phẩm nào: hiển thị thông báo "Không tìm thấy sản phẩm gợi ý phù hợp".
  * `selectAdvSearchSuggestion(productIndex)`:
    * Điền tên sản phẩm vào ô `#adv-search-keyword`.
    * Cập nhật `<select id="adv-search-brand">` về đúng thương hiệu tương ứng (`monster`, `redbull`, `sting`).
    * Cập nhật `<select id="adv-search-price">` về đúng khoảng giá tương ứng.
    * Cập nhật dòng preview mẫu trong modal.
    * Đóng dropdown gợi ý.
  * Hỗ trợ đóng dropdown gợi ý khi click ra ngoài hoặc nhấn phím `ESC`.

### 2.3. Admin: Chuẩn Hóa Thẻ KPI Brand & Tiêu Đề
* **Các file áp dụng:**
  * `admin/index.html` (Dashboard)
  * `admin/inventory.html` (Quản lý kho)
* **Nội dung thay đổi:**
  * **Thẻ KPI Brand:**
    * Số lượng: `<h3>3 Brand</h3>`
    * Dòng chữ dưới: `<p>Thương hiệu</p>` (loại bỏ liệt kê tên thương hiệu `Monster Energy & Redbull`).
  * **Phụ đề Admin:**
    * `admin/index.html`: Cập nhật thành: `Cập nhật dữ liệu thời gian thực - 3 Thương hiệu chính thức`
    * `admin/inventory.html`: Cập nhật thành: `3 Thương hiệu chính thức (Monster, Redbull & Sting) - Sẵn sàng xuất kho`

---

## 3. Tiêu Chí Nghiệm Thu (Acceptance Criteria)

1. Dropdown tìm kiếm trên Header của 4 trang (`index.html`, `pages/product-detail*.html`) không còn xuất hiện các tag `#MonsterOriginal #RedbullThai...`.
2. Khi mở modal Tìm Kiếm Nâng Cao trên `index.html` và gõ từ khóa (ví dụ `"ultra"`), dropdown gợi ý hiển thị đúng các lon Ultra; click vào 1 lon sẽ tự điền tên lon và đồng bộ select thương hiệu / khoảng giá.
3. Trong `admin/index.html` và `admin/inventory.html`, thẻ KPI hiển thị `3 Brand` và bên dưới là `Thương hiệu`.
4. Toàn bộ 66/66 test cases trong `python verify_implementation.py` và 45/45 test rubric tiếp tục PASS 100%.
5. Tuân thủ **RULE 1**: Không thực hiện `git push`.
