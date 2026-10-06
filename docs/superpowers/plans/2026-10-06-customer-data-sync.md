# Customer Data Synchronization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Đồng bộ hóa động toàn diện dữ liệu của 6 khách hàng VIP demo (Phạm Minh Tuấn, Nguyễn Văn An, Trần Thị Bích, Lê Hoàng Nam, Vũ Thảo My, Hoàng Đức Long) trên toàn bộ hệ thống quản trị (Kho khách hàng, Dashboard chính, Quản lý đơn hàng, và Modal hồ sơ VIP).

**Architecture:** Mở rộng cơ chế Registry trong `js/app.js` với `CUSTOMER_DATA_REGISTRY` đóng vai trò Single Source of Truth cho dữ liệu khách hàng. Gắn định danh ID rõ ràng vào các thành phần của modal `#modal-customer-detail`, bổ sung CSS class cho các cấp bậc thành viên (Kim Cương, Vàng, Bạc). Cập nhật hành vi click tên khách hàng ở các bảng đơn hàng để mở hồ sơ VIP tương ứng.

**Tech Stack:** HTML5, CSS3 (Dark Neon Glassmorphism), Vanilla JavaScript, FontAwesome 6.4.0.

## Global Constraints
- Tuyệt đối KHÔNG chạy lệnh `git push` (RULE 1).
- Giữ nguyên toàn bộ 66/66 kiểm thử tự động `python verify_implementation.py` PASS 100%.
- Giữ nguyên cấu trúc giao diện Dark Neon, không làm biến dạng layout hay bảng dữ liệu.
- Số điện thoại của 6 khách hàng phải khớp với mask và đơn hàng demo:
  + Tuấn: `0977 888 999` (mask: `0977***999`, đơn: `0977.888.999`)
  + An: `0912 345 678` (mask: `0912***678`, đơn: `0912.345.678`)
  + Bích: `0988 765 432` (mask: `0988***432`, đơn: `0988.765.432`)
  + Nam: `0903 111 222` (mask: `0903***222`, đơn: `0903.111.222`)
  + My: `0934 555 666` (mask: `0934***666`, đơn: `0934.555.666`)
  + Long: `0938 222 111` (mask: `0938***111`, đơn: `0938.222.111`)

---

### Task 1: Bổ Sung CSS Cho Huy Hiệu VIP Vàng & Bạc (`css/style.css`)

**Files:**
- Modify: `css/style.css:1835-1845`

**Interfaces:**
- Thêm `.vip-badge-gold` và `.vip-badge-silver` kế thừa chuẩn phong cách Dark Neon của `.vip-badge-diamond`.

- [x] **Step 1: Thêm CSS rule cho `.vip-badge-gold` (accent vàng neon `var(--accent-gold)`) và `.vip-badge-silver` (ánh bạc `#94A3B8`)**
- [x] **Step 2: Kiểm tra test suite không bị ảnh hưởng**

---

### Task 2: Định Nghĩa `CUSTOMER_DATA_REGISTRY` & Logic Modal Động (`js/app.js`)

**Files:**
- Modify: `js/app.js:630-640`

**Interfaces:**
- Produces: `CUSTOMER_DATA_REGISTRY` với 6 bản ghi (`tuan`, `an`, `bich`, `nam`, `my`, `long`).
- Produces: Hàm `openCustomerDetailModal(customerKey)` cập nhật toàn bộ ID trong modal (`vip-modal-avatar`, `vip-modal-name`, `vip-modal-badge`, `vip-modal-points`, `vip-modal-spent`, `vip-modal-orders`, `vip-modal-phone`, `vip-modal-email`, `vip-modal-address`, `vip-modal-latest-order`, `vip-modal-joindate`, `vip-modal-privilege`, `vip-modal-gift-btn`).

- [x] **Step 1: Viết `CUSTOMER_DATA_REGISTRY` chứa đủ 6 khách hàng với đầy đủ thông tin chuẩn xác**
- [x] **Step 2: Viết lại hàm `openCustomerDetailModal(customerKey)` để cập nhật động các trường vào DOM**

---

### Task 3: Chuẩn Hóa Cấu Trúc DOM Modal & Nút Gọi Tại `admin/customers.html`

**Files:**
- Modify: `admin/customers.html:90-235`

**Interfaces:**
- Cập nhật 6 nút icon mắt (`👁`) trong bảng VIP gọi `openCustomerDetailModal('tuan')`, `('an')`, `('bich')`, `('nam')`, `('my')`, `('long')`.
- Gắn các thuộc tính ID tương ứng vào cấu trúc HTML của `#modal-customer-detail`.

- [x] **Step 1: Cập nhật 6 nút xem chi tiết khách hàng trong bảng với key tương ứng**
- [x] **Step 2: Bổ sung các ID vào các thẻ hiển thị trong `#modal-customer-detail`**

---

### Task 4: Đồng Bộ Hóa Bảng Đơn Hàng & Modal Trên Dashboard (`admin/index.html`)

**Files:**
- Modify: `admin/index.html:130-205,560-615`

**Interfaces:**
- Biến tên khách hàng trong bảng đơn hàng thành nút/link gọi `openCustomerDetailModal(key)`.
- Bổ sung đơn hàng thứ 6 `#EB-8806` cho Hoàng Đức Long (2x Sting Dâu Tây Đỏ - 24.000đ, ĐÃ THANH TOÁN).
- Gắn các thuộc tính ID vào `#modal-customer-detail` trong `admin/index.html`.

- [x] **Step 1: Cập nhật cột Khách hàng trong bảng đơn hàng thành nút mở modal VIP**
- [x] **Step 2: Thêm đơn hàng thứ 6 cho Hoàng Đức Long**
- [x] **Step 3: Bổ sung các ID vào modal `#modal-customer-detail` trên Dashboard**

---

### Task 5: Đồng Bộ Hóa Trang Quản Lý Đơn Hàng (`admin/orders.html`)

**Files:**
- Modify: `admin/orders.html:90-180,240-250`

**Interfaces:**
- Thêm đơn hàng thứ 6 `#EB-8806` cho Hoàng Đức Long.
- Biến tên khách hàng trong bảng đơn thành nút mở modal VIP.
- Bổ sung cấu trúc `#modal-customer-detail` vào cuối trang `admin/orders.html` để có thể xem hồ sơ VIP trực tiếp từ trang đơn hàng.

- [x] **Step 1: Cập nhật bảng đơn hàng với đơn thứ 6 và link mở modal VIP**
- [x] **Step 2: Nhúng modal `#modal-customer-detail` vào `admin/orders.html`**

---

### Task 6: Kiểm Thử Toàn Diện & Git Commit Cục Bộ

**Files:**
- Test: `verify_implementation.py`

- [x] **Step 1: Chạy `python verify_implementation.py` đảm bảo 66/66 test cases PASS**
- [x] **Step 2: Kiểm tra `git status` và `git diff`**
- [x] **Step 3: Commit cục bộ trên nhánh `feat/energy-boost-rebrand`**
