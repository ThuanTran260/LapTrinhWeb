# Kế Hoạch Triển Khai: Giữ Nguyên Mã Giảm Giá 10% Khi Bấm Chip Voucher (Static UI Mockup)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Điều chỉnh cơ chế click của cụm chip Voucher trên trang `admin/settings.html`: Cho phép các nút chip (`MONSTER10`, `ENERGY20`, `FREESHIP`) vẫn nhận click và đổi viền xanh active kèm toast thông báo, nhưng dữ liệu vé xem trước và form cấu hình bên dưới hoàn toàn giữ nguyên tĩnh ở `MONSTER10` và `10%` theo đúng tiêu chí chấm đồ án tĩnh của SGU.

**Architecture:** Pure Static HTML/CSS/JavaScript (vanilla JS). Cập nhật hàm `switchVoucherPreview(code)` trong `js/app.js` để chỉ chuyển đổi trạng thái hiển thị của chip `.voucher-chip.active` và thông báo toast, tách biệt hoàn toàn không ghi đè giá trị của `#voucher-code`, `#voucher-amount` hay `#preview-ticket-discount`.

**Tech Stack:** HTML5, CSS3 (Dark Neon Theme Tokens), Vanilla JavaScript (DOM APIs), Python 3 test suites.

## Global Constraints

- 100% Pure Static Website: Không dùng backend server, không chạy code tính toán hoặc ghi đè động làm sai lệch giao diện tĩnh đã định sẵn.
- Visual Feedback: Khi người dùng click vào bất kỳ chip nào (`MONSTER10`, `ENERGY20`, `FREESHIP`), nút phải phản hồi click ngay lập tức (chuyển class `.active` có viền xanh neon sáng và hiện toast).
- Static Rubric Integrity: Thẻ vé xem trước `#preview-ticket-discount` luôn giữ `GIẢM 10%`, form input `#voucher-amount` luôn giữ `10%`, form input `#voucher-code` luôn giữ `MONSTER10`.
- Test Suite Integrity: Giữ vững 66/66 PASS trong `verify_implementation.py` và 10/10 PASS trong `scripts/verify_admin_ui_mockup.py`.
- STRICT RULE 1: Tuyệt đối không tự động chạy `git push`. Toàn bộ commit thực hiện cục bộ.

---

### Task 1: Cập Nhật Hàm switchVoucherPreview Trong js/app.js Giữ Cố Định 10%

**Files:**
- Modify: `js/app.js:1905-1935`
- Test: `scripts/verify_order_detail_pages.py`

**Interfaces:**
- `switchVoucherPreview(code)`: Nhận mã `code` (string), cập nhật `activeVoucherCode = code`, gọi `renderVoucherChips()`, hiển thị Toast `Đang xem cấu hình Voucher "${code}"`, nhưng KHÔNG ghi đè `#voucher-code`, `#voucher-amount`, `#voucher-type` hay gọi `updateVoucherLivePreview()`.
- Form inputs `#voucher-code`, `#voucher-amount` và thẻ vé `#preview-ticket-discount` luôn giữ nguyên giá trị mặc định tĩnh (`MONSTER10`, `10%`, `GIẢM 10%`).

- [ ] **Step 1: Viết test case xác minh hành vi tĩnh của switchVoucherPreview trong file test**
- [ ] **Step 2: Cập nhật hàm `switchVoucherPreview(code)` trong `js/app.js`**
- [ ] **Step 3: Cập nhật hàm `saveAddVoucher(e)` trong `js/app.js` đảm bảo sau khi thêm mới cũng không ghi đè form chính**
- [ ] **Step 4: Chạy kiểm thử tự động xác minh không còn hành vi ghi đè động**
- [ ] **Step 5: Tạo commit cục bộ an toàn**

---

### Task 2: Kiểm Thử Toàn Diện Hệ Thống & Nghiệm Thu Rubric

**Files:**
- Test: `scripts/verify_order_detail_pages.py`
- Test: `verify_implementation.py`
- Test: `scripts/verify_admin_ui_mockup.py`

- [ ] **Step 1: Chạy `python scripts/verify_order_detail_pages.py` -> Đảm bảo 100% PASS**
- [ ] **Step 2: Chạy `python verify_implementation.py` -> Đảm bảo 66/66 checks PASS**
- [ ] **Step 3: Chạy `python scripts/verify_admin_ui_mockup.py` -> Đảm bảo 10/10 checks PASS**
- [ ] **Step 4: Cập nhật walkthrough artifact và báo cáo nghiệm thu**
