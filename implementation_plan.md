# Kế Hoạch Triển Khai: Hiển Thị Tồn Kho Admin, Format Tiền VNĐ Voucher, Nút In Hóa Đơn Toast, Loại Bỏ Đánh Giá Chuyên Nghiệp & Quản Lý FAQ

> **Trạng thái:** ĐÃ HOÀN THÀNH TOÀN DIỆN (100% PASS)

**Goal:** 
1. Hiển thị dòng phụ nhỏ số lượng tồn kho dưới badge `CÒN HÀNG` trong bảng kho của `admin/inventory.html` và `admin/index.html` (Monster cố định 1.250 lon, Redbull 680/450/520 lon, Sting 890/740/610 lon).
2. Tích hợp định dạng tiền tệ VNĐ thời gian thực cho các ô nhập tiền trong cấu hình Voucher & Vận chuyển của `admin/settings.html` và đồng bộ thẻ Live Preview coupon trong `js/app.js`.
3. Cập nhật nút "IN HÓA ĐƠN ĐIỆN TỬ" trong `pages/order-success.html` chuyển từ `window.print()` sang gọi thông báo `showToast(...)`.
4. Loại bỏ phần Đánh giá chuyên nghiệp (`.testimonials-head`, `.review-grid`) trên storefront `index.html` và giữ lại thanh cam kết `.trust-strip`.
5. Bổ sung phân vùng Quản Lý Câu Hỏi Thường Gặp (FAQ) trong `admin/settings.html` gồm form thêm mới và danh sách 4 câu hỏi chuẩn có badge thứ tự và nút sửa/xóa.

**Architecture:** Pure Static HTML5 / CSS3 / Vanilla JS. Giữ nguyên kiến trúc tĩnh, không phụ thuộc thư viện ngoài.

**Tech Stack:** HTML5, CSS3, Vanilla JavaScript, Python test suites.

## Global Constraints

- Không tự động chạy `git push`. Toàn bộ commit thực hiện cục bộ.
- 100% Pure Static Architecture: Không làm thay đổi layout hay gãy vỡ giao diện.
- Test Suite Integrity: Duy trì 100% PASS cho tất cả các test suites hiện có.

---

### Task 1: Viết Script Kiểm Thử TDD `scripts/verify_admin_features_update.py`

**Files:**
- Create: `scripts/verify_admin_features_update.py`

- [x] **Step 1: Viết script `scripts/verify_admin_features_update.py`**
  - Kiểm tra 10 sản phẩm trong `admin/inventory.html` và `admin/index.html` có thẻ `<small>` hiển thị `Tồn: ... lon`.
  - Kiểm tra 4 sản phẩm Monster có đúng `Tồn: 1.250 lon`.
  - Kiểm tra các input tiền tệ trong `admin/settings.html` có class `price-format-input`.
  - Kiểm tra nút "IN HÓA ĐƠN ĐIỆN TỬ" trong `pages/order-success.html` gọi `showToast` và không gọi `window.print()`.
  - Kiểm tra loại bỏ phần review chuyên nghiệp và giữ trust-strip.
  - Kiểm tra phân vùng quản lý FAQ trong `admin/settings.html`.
- [x] **Step 2: Chạy kiểm thử để xác nhận trạng thái thất bại ban đầu (Red Phase - 13/45 PASS)**
- [x] **Step 3: Hoàn thiện tính năng chuyển sang Green Phase (45/45 PASS)**

---

### Task 2: Hiển Thị Số Lượng Tồn Kho Trong `admin/inventory.html` & `admin/index.html`

**Files:**
- Modify: `admin/inventory.html`
- Modify: `admin/index.html`

- [x] **Step 1: Cập nhật 10 hàng sản phẩm trong `admin/inventory.html`**
  - Thêm dòng `<small style="color: var(--text-muted); display: block; margin-top: 4px; font-size: 0.78rem;"><i class="fas fa-box"></i> Tồn: ... lon</small>` vào cột Trạng thái.
  - Monster = 1.250 lon; Redbull = 680, 450, 520 lon; Sting = 890, 740, 610 lon.
- [x] **Step 2: Cập nhật 10 hàng sản phẩm trong `admin/index.html` tương tự**

---

### Task 3: Triển Khai Định Dạng Tiền Tệ VNĐ Trong Cài Đặt Voucher & Vận Chuyển (`admin/settings.html` & `js/app.js`)

**Files:**
- Modify: `admin/settings.html`
- Modify: `js/app.js`

- [x] **Step 1: Bổ sung class `price-format-input` cho các ô nhập tiền tệ trong `admin/settings.html`**
  - `#voucher-min-spend`, `#voucher-max-discount`, `#ship-min-free`, `#ship-standard-fee`.
- [x] **Step 2: Cập nhật `initPriceFormatting()` và `updateVoucherLivePreview()` trong `js/app.js`**
  - Thêm các ID voucher/shipping vào danh sách `initPriceFormatting`.
  - Tự động chuẩn hóa format tiền tệ VNĐ (có dấu chấm và đuôi `đ`) khi hiển thị trên thẻ Live Preview coupon `(Tối đa 13.131đ)`.

---

### Task 4: Chuyển Đổi Nút "IN HÓA ĐƠN ĐIỆN TỬ" Sang Thông Báo Toast (`pages/order-success.html`)

**Files:**
- Modify: `pages/order-success.html:222-224`

- [x] **Step 1: Cập nhật nút in hóa đơn trong `pages/order-success.html` sang `showToast(...)`**

---

### Task 5: Loại Bỏ Đánh Giá Chuyên Nghiệp Trên Storefront & Giữ Cam Kết Trust-Strip (`index.html`)

**Files:**
- Modify: `index.html`
- Modify: `scripts/verify_clean_brand_pills_and_kicker.py`

- [x] **Step 1: Xóa bỏ `.testimonials-head` và `.review-grid` trong `index.html`**
- [x] **Step 2: Bảo toàn thanh cam kết `.trust-strip` (100% CHÍNH HÃNG, ĐỔI TRẢ MIỄN PHÍ, KIỂM TRA TRƯỚC KHI NHẬN, HỖ TRỢ 24/7)**
- [x] **Step 3: Cập nhật `scripts/verify_clean_brand_pills_and_kicker.py` không còn assert tiêu đề review (9/9 PASS)**

---

### Task 6: Phân Vùng Quản Lý Câu Hỏi Thường Gặp (FAQ) Trong Admin (`admin/settings.html` & `js/app.js`)

**Files:**
- Modify: `admin/settings.html`
- Modify: `js/app.js`

- [x] **Step 1: Thêm phân vùng `admin-section-box` với tiêu đề `QUẢN LÝ CÂU HỎI THƯỜNG GẶP (FAQ)`**
- [x] **Step 2: Thêm form thêm mới (input câu hỏi, input thứ tự, textarea câu trả lời, nút Thêm Câu Hỏi)**
- [x] **Step 3: Thêm danh sách 4 câu hỏi FAQ chuẩn với badge #1-#4 và các nút thao tác Sửa/Xóa**
- [x] **Step 4: Thêm hàm xử lý `handleAdminAddFaq`, `handleAdminDeleteFaq`, `handleAdminEditFaq` trong `js/app.js`**

---

### Task 7: Kiểm Thử Toàn Diện Hệ Thống & Nghiệm Thu Hồi Quy

**Files:**
- Test: `verify_implementation.py` (66/66 PASS)
- Test: `scripts/verify_admin_features_update.py` (45/45 PASS)
- Test: `scripts/verify_price_formatting.py` (49/49 PASS)
- Test: `scripts/verify_footer_sync.py` (144/144 PASS)
- Test: `scripts/verify_sidebar_filter_sync.py` (31/31 PASS)
- Test: `scripts/verify_clean_brand_pills_and_kicker.py` (9/9 PASS)
- Test: `scripts/verify_admin_kpi_brand_wording.py` (PASS 100%)
- Test: `scripts/verify_no_product_specs.py` (8/8 PASS)
- Test: `scripts/verify_cart_sync.py` (15/15 PASS)
- Test: `scripts/verify_search_features.py` (28/28 PASS)
- Test: `scripts/verify_order_detail_pages.py` (8/8 PASS)
- Test: `scripts/verify_rubric_coverage.py` (19/19 PASS)
