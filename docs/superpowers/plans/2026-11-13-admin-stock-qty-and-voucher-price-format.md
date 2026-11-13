# Kế Hoạch Triển Khai: Hiển Thị Tồn Kho Admin, Format Tiền VNĐ Voucher & Nút In Hóa Đơn Toast

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 
1. Hiển thị dòng phụ nhỏ số lượng tồn kho dưới badge `CÒN HÀNG` trong bảng kho của `admin/inventory.html` và `admin/index.html` (Monster cố định 1.250 lon, các lon khác ngẫu nhiên thực tế).
2. Tích hợp định dạng tiền tệ VNĐ thời gian thực cho các ô nhập tiền trong cấu hình Voucher & Vận chuyển của `admin/settings.html` và đồng bộ thẻ Live Preview coupon trong `js/app.js`.
3. Cập nhật nút "IN HÓA ĐƠN ĐIỆN TỬ" trong `pages/order-success.html` chuyển từ `window.print()` sang gọi thông báo `showToast(...)`.

**Architecture:** Pure Static HTML5 / CSS3 / Vanilla JS. Giữ nguyên kiến trúc tĩnh, không phụ thuộc thư viện ngoài.

**Tech Stack:** HTML5, CSS3, Vanilla JavaScript, Python test suites.

## Global Constraints

- Không tự động chạy `git push`. Toàn bộ commit thực hiện cục bộ.
- 100% Pure Static Architecture: Không làm thay đổi layout hay gãy vỡ giao diện.
- Test Suite Integrity: Duy trì 100% PASS cho tất cả các test suites hiện có.

---

### Task 1: Viết Script Kiểm Thử TDD `scripts/verify_admin_stock_qty_and_voucher_price_format.py`

**Files:**
- Create: `scripts/verify_admin_stock_qty_and_voucher_price_format.py`

- [x] **Step 1: Viết script `scripts/verify_admin_stock_qty_and_voucher_price_format.py`**
  - Kiểm tra 10 sản phẩm trong `admin/inventory.html` và `admin/index.html` có thẻ `<small>` hiển thị `Tồn: ... lon`.
  - Kiểm tra 4 sản phẩm Monster có đúng `Tồn: 1.250 lon`.
  - Kiểm tra các input tiền tệ trong `admin/settings.html` có class `price-format-input`.
  - Kiểm tra nút "IN HÓA ĐƠN ĐIỆN TỬ" trong `pages/order-success.html` gọi `showToast` và không gọi `window.print()`.
- [x] **Step 2: Chạy kiểm thử để xác nhận trạng thái thất bại ban đầu (Red Phase)**
  Run: `python scripts/verify_admin_stock_qty_and_voucher_price_format.py`
  Expected: FAIL.
- [x] **Step 3: Commit cục bộ script test**

---

### Task 2: Chuyển Đổi Nút "IN HÓA ĐƠN ĐIỆN TỬ" Sang Thông Báo Toast (`pages/order-success.html`)

**Files:**
- Modify: `pages/order-success.html:222-224`

- [x] **Step 1: Cập nhật nút in hóa đơn trong `pages/order-success.html` sang `showToast(...)`**
- [x] **Step 2: Commit cục bộ**

---

### Task 3: Triển Khai Định Dạng Tiền Tệ VNĐ Trong Cài Đặt Voucher & Vận Chuyển (`admin/settings.html` & `js/app.js`)

**Files:**
- Modify: `admin/settings.html`
- Modify: `js/app.js`

- [x] **Step 1: Bổ sung class `price-format-input` cho các ô nhập tiền tệ trong `admin/settings.html`**
  - `#voucher-min-spend`, `#voucher-max-discount`, `#ship-min-free`, `#ship-standard-fee`.
- [x] **Step 2: Cập nhật `initPriceFormatting()` và `updateVoucherLivePreview()` trong `js/app.js`**
  - Thêm các ID voucher/shipping vào danh sách `initPriceFormatting`.
  - Tự động chuẩn hóa format tiền tệ VNĐ (có dấu chấm và đuôi `đ`) khi hiển thị trên thẻ Live Preview coupon.
- [x] **Step 3: Commit cục bộ**

---

### Task 4: Triển Khai Hiển Thị Nhỏ Số Lượng Tồn Kho Trong `admin/inventory.html` & `admin/index.html`

**Files:**
- Modify: `admin/inventory.html`
- Modify: `admin/index.html`
- Test: `scripts/verify_admin_stock_qty_and_voucher_price_format.py`

- [x] **Step 1: Cập nhật 10 hàng sản phẩm trong `admin/inventory.html`**
  - Thêm dòng `<small style="color: var(--text-muted); display: block; margin-top: 4px; font-size: 0.78rem;"><i class="fas fa-box"></i> Tồn: ... lon</small>` vào cột Trạng thái.
  - Monster = 1.250 lon; Redbull = 680, 450, 520 lon; Sting = 890, 740, 610 lon.
- [x] **Step 2: Cập nhật 10 hàng sản phẩm trong `admin/index.html` tương tự**
- [x] **Step 3: Chạy script `scripts/verify_admin_stock_qty_and_voucher_price_format.py` (Green Phase)**
  Run: `python scripts/verify_admin_stock_qty_and_voucher_price_format.py`
  Expected: PASS 100%.
- [x] **Step 4: Commit cục bộ**

---

### Task 5: Kiểm Thử Toàn Diện Hệ Thống & Nghiệm Thu Hồi Quy

**Files:**
- Test: `verify_implementation.py`
- Test: `scripts/verify_price_formatting.py`
- Test: `scripts/verify_admin_kpi_brand_wording.py`
- Test: `scripts/verify_footer_sync.py`
- Test: `scripts/verify_sidebar_filter_sync.py`
- Test: `scripts/verify_clean_brand_pills_and_kicker.py`
- Test: `scripts/verify_no_product_specs.py`
- Test: `scripts/verify_admin_stock_qty_and_voucher_price_format.py`

- [x] **Step 1: Chạy tất cả test suites đảm bảo không hồi quy**
- [x] **Step 2: Cập nhật tài liệu và báo cáo kết quả**
