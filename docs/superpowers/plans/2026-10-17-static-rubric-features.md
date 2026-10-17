# Kế Hoạch Triển Khai: Chuẩn Hóa Theo Tiêu Chí Chấm Điểm Website Tĩnh (SGU)

> **Căn cứ:** Bảng tiêu chí chấm điểm môn *Lập trình web và ứng dụng* (Khoa CNTT - SGU, Giảng viên: Cô Phan Thị Kim Loan).  
> **Nguyên tắc tối thượng:** **100% WEBSITE TĨNH (KHÔNG RUNNING BACKEND/CSDL)**. Chấm bài trực tiếp từ file `index.html` trên trình duyệt Google Chrome. Mọi tương tác (xóa giỏ hàng, xóa sản phẩm, duyệt đơn, đăng ký, tìm kiếm) đều vận hành ở mức giao diện tĩnh an toàn, có thông báo toast/modal phản hồi nhưng **KHÔNG làm mất/xóa hỏng dữ liệu mẫu**.  
> **Nhánh Git:** `feat/static-rubric-features` (tạo từ `feat/energy-boost-rebrand`, tuân thủ nghiêm ngặt **RULE 1**: strictly NO git push).

---

### Task 1: Bổ Sung CSS Cho Các Thành Phần Giao Diện Tĩnh (`css/style.css`)
- [ ] **Step 1:** Thêm CSS `.search-results-dropdown`, `.search-static-item`, `.search-quick-tag`, `.search-dropdown-header`
- [ ] **Step 2:** Thêm CSS modal tìm kiếm nâng cao `.adv-search-modal`
- [ ] **Step 3:** Thêm CSS phân trang tĩnh `.pagination-strip`, `.page-btn`
- [ ] **Step 4:** Thêm CSS tab xác thực `.auth-tabs`, `.auth-tab-btn`, `.auth-switch-text`, `.password-wrapper`
- [ ] **Step 5:** Thêm CSS bộ lọc admin `.admin-filter-bar`, `.admin-filter-group`, `.admin-filter-select`, `.btn-filter-apply`, `.btn-filter-reset`

### Task 2: Triển Khai Search Dropdown, Tìm Kiếm Nâng Cao & Phân Trang (Storefront)
- [ ] **Step 1:** Thêm cấu trúc HTML `#search-dropdown-menu` vào `index.html` và các trang `pages/product-detail*.html`
- [ ] **Step 2:** Thêm nút icon mở tìm kiếm nâng cao và modal `#modal-adv-search` trên `index.html`
- [ ] **Step 3:** Bổ sung cụm phân trang tĩnh `« 1 2 3 »` ở chân các section sản phẩm
- [ ] **Step 4:** Viết hàm điều khiển đóng/mở dropdown và modal tìm kiếm nâng cao trong `js/app.js`

### Task 3: Triển Khai Giao Diện Đăng Ký Tài Khoản (`pages/login.html`)
- [ ] **Step 1:** Thêm cụm Tab ĐĂNG NHẬP / ĐĂNG KÝ vào `.login-card` trên `pages/login.html`
- [ ] **Step 2:** Thêm form đăng ký `#form-register` với 5 trường + checkbox + nút đăng ký
- [ ] **Step 3:** Viết hàm `switchAuthTab()`, `handleRegister()`, `togglePasswordVisibility()` trong `js/app.js`

### Task 4: Triển Khai Bộ Lọc Admin Mẫu Tĩnh & Xóa An Toàn Theo Rubric
- [ ] **Step 1:** Thêm `.admin-filter-bar` vào `admin/orders.html` (Trạng thái, Khoảng ngày, Quận/Huyện)
- [ ] **Step 2:** Thêm `.admin-filter-bar` vào `admin/inventory.html` (Thương hiệu, Tồn kho) và chuẩn hóa cảnh báo xóa an toàn
- [ ] **Step 3:** Thêm `.admin-filter-bar` và khung khoảng ngày thống kê vào `admin/customers.html`
- [ ] **Step 4:** Thêm `.admin-filter-bar` mẫu tĩnh vào `admin/index.html` (Dashboard)

### Task 5: Kiểm Thử Tự Động Toàn Diện & Local Git Commit
- [ ] **Step 1:** Chạy `python verify_implementation.py` (đảm bảo 66/66 checks PASS)
- [ ] **Step 2:** Viết và chạy `scratch/verify_rubric_features.py` kiểm tra toàn bộ tiêu chí SGU
- [ ] **Step 3:** Dọn dẹp scratch file, kiểm tra git status và commit cục bộ trên `feat/static-rubric-features`
