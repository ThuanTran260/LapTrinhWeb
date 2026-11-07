# Kế Hoạch Triển Khai: Nút Xóa Giỏ Hàng Tương Tác Chuẩn & Toast Tự Nhiên

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Khôi phục trạng thái tương tác tự nhiên cho 3 nút Xóa trong giỏ hàng (`pages/cart.html`): bấm được bình thường (cursor: pointer, icon đỏ sắc nét, hover scale mượt mà, bỏ dấu cấm not-allowed), không thực hiện xóa hàng khỏi DOM (giữ nguyên dữ liệu giỏ hàng tĩnh), và đổi thông báo Toast sang câu ngắn gọn, tự nhiên theo từng lon nước mà không chứa các từ ngữ kỹ thuật rườm rà.

**Architecture:** Pure Static HTML5 / CSS3 / Vanilla JavaScript. 
- `pages/cart.html`: Gỡ bỏ `cursor: not-allowed; opacity: 0.45; filter: grayscale(1);` và `aria-disabled="true"`. Cập nhật `title="Xóa sản phẩm khỏi giỏ hàng"` và `onclick` gọi `showToast` tự nhiên cho từng lon nước.
- `css/style.css`: Đảm bảo `.cart-del-btn` có `cursor: pointer; border: none;` chuẩn mực.

**Tech Stack:** HTML5, CSS3, Python test suites.

## Global Constraints

- 100% Pure Static Architecture: Không làm vỡ layout, hoạt động trơn tru trên mọi độ phân giải.
- Test Suite Integrity: Giữ vững 8/8 PASS trong `scripts/verify_order_detail_pages.py`, 66/66 PASS trong `verify_implementation.py`, và 10/10 PASS trong `scripts/verify_admin_ui_mockup.py`.
- STRICT RULE 1: Tuyệt đối không tự động chạy `git push`. Toàn bộ commit thực hiện cục bộ.

---

### Task 1: Khôi Phục Tương Tác Nút Xóa & Cập Nhật Toast Tự Nhiên Trong `pages/cart.html`

**Files:**
- Modify: `pages/cart.html:103-164`
- Modify: `css/style.css:1148-1156`

- [ ] **Step 1: Cập nhật CSS `.cart-del-btn` trong `css/style.css` bổ sung `cursor: pointer; border: none;`**
- [ ] **Step 2: Cập nhật 3 nút xóa trong `pages/cart.html`:**
  - Gỡ bỏ inline style vô hiệu hóa và `aria-disabled="true"`
  - Lon 1: `title="Xóa sản phẩm khỏi giỏ hàng" onclick="showToast('Đã xóa Monster Energy Original khỏi giỏ hàng!', 'info')"`
  - Lon 2: `title="Xóa sản phẩm khỏi giỏ hàng" onclick="showToast('Đã xóa Redbull Original 250ml khỏi giỏ hàng!', 'info')"`
  - Lon 3: `title="Xóa sản phẩm khỏi giỏ hàng" onclick="showToast('Đã xóa Monster Zero Ultra White khỏi giỏ hàng!', 'info')"`
- [ ] **Step 3: Chạy 3 test suites: `verify_order_detail_pages.py` (8/8), `verify_implementation.py` (66/66), `verify_admin_ui_mockup.py` (10/10)**
- [ ] **Step 4: Thực hiện commit cục bộ an toàn (`feat(cart): enable interactive delete buttons with natural toast`)**

---

### Task 2: Nghiệm Thu Toàn Diện & Cập Nhật Báo Cáo

**Files:**
- Modify: `C:\Users\Admin\.gemini\antigravity\brain\36478f47-6ab1-476a-a2ac-6f3cf0a64610\walkthrough.md`

- [ ] **Step 1: Cập nhật Walkthrough Artifact**
- [ ] **Step 2: Báo cáo kết quả chi tiết cho người dùng**
