# Unified Brand Edit Pages & Admin Synchronization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Đồng bộ hóa hoàn toàn thao tác chỉnh sửa sản phẩm trong Admin cho 3 thương hiệu (Monster, Redbull, Sting), mỗi thương hiệu quy về đúng 1 trang chỉnh sửa đại diện độc lập (Monster Original, Redbull Original, Sting Dâu Đỏ), đồng nhất cột Thao Tác (2 nút: Chỉnh sửa và Xóa) trên cả Dashboard và Kho hàng.

**Architecture:** Sử dụng kiến trúc Static HTML5/CSS3 thuần với layout 2 cột Dark Neon đã thiết kế cho trang chỉnh sửa độc lập (`.admin-edit-layout`). Thống nhất hành vi điều hướng: mọi sản phẩm cùng thương hiệu đều trỏ về trang chỉnh sửa đại diện của thương hiệu đó. Thêm chuyển hướng tự động cho các trang biến thể cũ. Đồng bộ bảng dữ liệu trong `admin/inventory.html` và `admin/index.html`.

**Tech Stack:** Pure HTML5, CSS3 (Dark Neon Glassmorphism), Vanilla JavaScript, FontAwesome 6.4.0.

## Global Constraints
- Không chạy lệnh `git push` dưới mọi hình thức (RULE 1).
- Giữ nguyên toàn bộ 66/66 kiểm thử tự động `python verify_implementation.py` PASS 100%.
- Duy trì đồng bộ thông số sản phẩm với `PRODUCT_DATA_REGISTRY` và các trang `pages/product-detail*.html`.
- Cột thao tác trên tất cả 10 sản phẩm (4 Monster, 3 Redbull, 3 Sting) phải đồng nhất tuyệt đối gồm 2 nút: `[Chỉnh Sửa]` và `[Xóa]`.

---

### Task 1: Tạo Trang Chỉnh Sửa Đại Diện Monster (`admin/edit-monster.html`)

**Files:**
- Create: `admin/edit-monster.html`
- Reference: `admin/edit-redbull-original.html`, `pages/product-detail.html`

**Interfaces:**
- Produces: Standalone edit page for Monster Energy brand with layout identical to Image 2.
- Previews: Monster Energy Original 355ml (`assets/images/monster/original.webp`), SKU: `MN-ORIGINAL-355`, Giá: 45.000đ (cũ 55.000đ), Tồn kho: 1.250 lon, Đã bán: 2.150 lon.
- Actions: Nút "Xem Trên Storefront" trỏ tới `../pages/product-detail.html`, "Quay Lại Kho" trỏ tới `inventory.html`, nút "Lưu Thay Đổi" gọi `saveStandaloneEdit(event, 'Monster Energy Original 355ml')`.

- [ ] **Step 1: Tạo file `admin/edit-monster.html` với đầy đủ layout và thông số chuẩn của Monster Original**
- [ ] **Step 2: Kiểm tra liên kết storefront và nút quay lại kho hoạt động chính xác**
- [ ] **Step 3: Kiểm tra form submit kích hoạt thông báo Toast**

---

### Task 2: Tạo Trang Chỉnh Sửa Đại Diện Sting (`admin/edit-sting.html`)

**Files:**
- Create: `admin/edit-sting.html`
- Reference: `admin/edit-redbull-original.html`, `pages/product-detail-sting.html`

**Interfaces:**
- Produces: Standalone edit page for Sting Energy brand with layout identical to Image 2.
- Previews: Nước Tăng Lực Sting Dâu Tây Đỏ 330ml (`assets/images/sting/sting-dau.webp`), SKU: `ST-STRAWBERRY-330`, Giá: 12.000đ (cũ 15.000đ), Tồn kho: 1.800 lon, Đã bán: 3.420 lon.
- Actions: Nút "Xem Trên Storefront" trỏ tới `../pages/product-detail-sting.html`, "Quay Lại Kho" trỏ tới `inventory.html`, nút "Lưu Thay Đổi" gọi `saveStandaloneEdit(event, 'Sting Dâu Tây Đỏ 330ml')`.

- [ ] **Step 1: Tạo file `admin/edit-sting.html` với đầy đủ layout và thông số chuẩn của Sting Dâu Tây Đỏ**
- [ ] **Step 2: Kiểm tra liên kết storefront và nút quay lại kho hoạt động chính xác**
- [ ] **Step 3: Kiểm tra form submit kích hoạt thông báo Toast**

---

### Task 3: Chuyển Hướng An Toàn Cho 2 Trang Biến Thể Cũ (`admin/edit-redbull-thai.html` & `admin/edit-redbull-lonvua.html`)

**Files:**
- Modify: `admin/edit-redbull-thai.html:10-15`
- Modify: `admin/edit-redbull-lonvua.html:10-15`

**Interfaces:**
- Thêm mã chuyển hướng tự động bằng JavaScript `<script>window.location.replace('edit-redbull-original.html');</script>` để tránh tạo ra đa trang phân tán cho cùng một thương hiệu.

- [ ] **Step 1: Cập nhật thẻ `<head>` của `admin/edit-redbull-thai.html` với script chuyển hướng sang `edit-redbull-original.html`**
- [ ] **Step 2: Cập nhật thẻ `<head>` của `admin/edit-redbull-lonvua.html` với script chuyển hướng sang `edit-redbull-original.html`**

---

### Task 4: Đồng Bộ Cột Thao Tác Trong Kho Hàng Admin (`admin/inventory.html`)

**Files:**
- Modify: `admin/inventory.html:100-230`

**Interfaces:**
- Thay thế icon bút chì modal cũ bằng link trực tiếp `<a href="..." class="btn-view-detail" title="Chỉnh sửa sản phẩm"><i class="fas fa-edit"></i></a>` trỏ về trang đại diện của từng thương hiệu:
  + Dòng 1-4 (Monster Original, Zero White, Paradise, Punk Punch) -> `edit-monster.html`
  + Dòng 5-7 (Redbull Original, Thái Lan, Nắp Bật) -> `edit-redbull-original.html`
  + Dòng 8-10 (Sting Dâu Đỏ, Vàng Nhân Sâm, Blue Việt Quất) -> `edit-sting.html`
- Xóa bỏ nút icon `fa-file-pen` dư thừa ở 3 dòng Redbull để toàn bộ 10 dòng trong bảng đều chỉ có đúng 2 nút: `[Chỉnh Sửa]` và `[Xóa]`.

- [ ] **Step 1: Cập nhật 4 dòng sản phẩm Monster trỏ tới `edit-monster.html`**
- [ ] **Step 2: Cập nhật 3 dòng sản phẩm Redbull trỏ tới `edit-redbull-original.html` và loại bỏ nút `fa-file-pen`**
- [ ] **Step 3: Cập nhật 3 dòng sản phẩm Sting trỏ tới `edit-sting.html`**

---

### Task 5: Đồng Bộ Bảng Kho Hàng Trên Dashboard Admin (`admin/index.html`)

**Files:**
- Modify: `admin/index.html:220-350`

**Interfaces:**
- Tương tự như `admin/inventory.html`, đồng bộ toàn bộ 10 dòng sản phẩm trên bảng kho của trang Dashboard chính:
  + 4 dòng Monster -> `edit-monster.html`
  + 3 dòng Redbull -> `edit-redbull-original.html` (loại bỏ nút `fa-file-pen` dư thừa)
  + 3 dòng Sting -> `edit-sting.html`

- [ ] **Step 1: Cập nhật 4 dòng sản phẩm Monster trỏ tới `edit-monster.html`**
- [ ] **Step 2: Cập nhật 3 dòng sản phẩm Redbull trỏ tới `edit-redbull-original.html` và loại bỏ nút `fa-file-pen`**
- [ ] **Step 3: Cập nhật 3 dòng sản phẩm Sting trỏ tới `edit-sting.html`**

---

### Task 6: Kiểm Thử Toàn Diện & Git Commit Cục Bộ

**Files:**
- Test: `verify_implementation.py`

- [ ] **Step 1: Chạy `python verify_implementation.py` xác nhận 66/66 test cases PASS**
- [ ] **Step 2: Kiểm tra `git status` và `git diff --stat`**
- [ ] **Step 3: Thực hiện commit cục bộ trên nhánh `feat/energy-boost-rebrand`**
