# Nâng Cấp Giao Diện Cài Đặt Voucher & Vé Coupon Neon (Settings UI Upgrade) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Nâng cấp khu vực cấu hình Voucher trong `admin/settings.html` từ một ô nhập text thô sơ thành hệ thống cài đặt chuyên nghiệp gồm Thẻ vé Coupon Neon trực quan (Ticket Preview Card) và Form cấu hình tách biệt các trường (Mã code, Loại giảm, Mức giảm, Đơn tối thiểu, Hạn dùng, Công tắc On/Off).

**Architecture:** Frontend thuần Vanilla HTML5/CSS3/ES6 đồng bộ hoàn hảo với hệ thống Dark Neon (`#0B0C10`, `#141720`, `#00E676`). Áp dụng hiệu ứng răng cưa vé coupon bằng CSS radial gradient / pseudo-elements, cùng bộ lắng nghe sự kiện `input` / `change` trong JavaScript để thẻ xem trước tự động cập nhật thời gian thực (Live Preview) khi quản trị viên chỉnh sửa form.

**Tech Stack:** HTML5, CSS3 (Glassmorphism, Neon Glow, Ticket Notches, Custom Toggle Switch), Vanilla JavaScript ES6, Font Awesome 6.4.0.

## Global Constraints

- **Quy tắc Pure UI Simulation:** Hoạt động ở mức giao diện mô phỏng tĩnh, phản hồi tức thì qua Toast Dark Neon, không làm biến đổi hoặc xáo trộn các trang bán hàng.
- **Tuân thủ quy tắc Git an toàn (RULE 1):** Tuyệt đối KHÔNG thực hiện `git push`. Toàn bộ thay đổi thực hiện và commit cục bộ trên nhánh hiện tại (`proceed`).
- **Không gây hồi quy (Zero Regression):** Bảo toàn 66/66 test checks trong `verify_implementation.py` và 10/10 test checks trong `scripts/verify_admin_ui_mockup.py`.

---

### Task 1: Bổ Sung CSS Thẻ Vé Coupon Neon & Toggle Switch (`css/style.css`)

**Files:**
- Modify: `css/style.css`

**Interfaces:**
- Consumes: Hệ thống biến màu Dark Neon `--primary` (`#00E676`), `--secondary` (`#00E5FF`), `--bg-card` (`#141720`).
- Produces: Các class `.voucher-ticket-card`, `.ticket-stub`, `.ticket-body`, `.ticket-badge`, `.ticket-code-pill`, `.custom-toggle-switch`, `.toggle-slider`.

- [x] **Step 1: Viết CSS cho Thẻ vé Coupon Neon (Voucher Ticket Card)**
- [x] **Step 2: Thêm đoạn CSS trên vào cuối file `css/style.css`**
- [x] **Step 3: Kiểm tra cú pháp CSS và các bài test hiện có**
- [x] **Step 4: Commit cục bộ**

---

### Task 2: Nâng Cấp Form Cấu Hình & Thẻ Vé Trong `admin/settings.html`

**Files:**
- Modify: `admin/settings.html:99-122`

**Interfaces:**
- Consumes: Cấu trúc section `VOUCHER & VẬN CHUYỂN`.
- Produces:
  - Khung xem trước thẻ vé `#voucher-ticket-card`.
  - Form với các trường riêng biệt: Mã code (`#voucher-code`), Loại giảm (`#voucher-type`), Mức giảm (`#voucher-amount`), Đơn tối thiểu (`#voucher-min-spend`), Hạn dùng (`#voucher-expiry`), và Công tắc kích hoạt (`#voucher-toggle-active`).
  - Khung cấu hình Chính sách vận chuyển 2H với Đơn miễn phí ship (`#ship-min-free`) và Phí ship tiêu chuẩn (`#ship-fee`).

- [x] **Step 1: Viết cấu trúc HTML nâng cấp cho section Voucher & Vận chuyển**

```css
/* ==========================================================================
   VOUCHER TICKET NEON PREVIEW & ADVANCED SETTINGS UI
   ========================================================================== */
.voucher-ticket-card {
  display: flex;
  background: linear-gradient(135deg, rgba(20, 23, 32, 0.95), rgba(11, 12, 16, 0.95));
  border: 1px solid rgba(0, 230, 118, 0.35);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(0, 230, 118, 0.12);
  border-radius: 14px;
  overflow: hidden;
  margin-bottom: 24px;
  position: relative;
  transition: all 0.3s ease;
}
.voucher-ticket-card:hover {
  border-color: var(--primary);
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.6), 0 0 25px rgba(0, 230, 118, 0.2);
}
.ticket-stub {
  flex: 0 0 160px;
  background: rgba(0, 230, 118, 0.08);
  border-right: 2px dashed rgba(0, 230, 118, 0.35);
  padding: 20px 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  position: relative;
}
/* Vé khuyết tròn (Notches) */
.ticket-stub::before,
.ticket-stub::after {
  content: '';
  position: absolute;
  width: 18px;
  height: 18px;
  background: #0B0C10;
  border-radius: 50%;
  right: -10px;
}
.ticket-stub::before { top: -9px; }
.ticket-stub::after { bottom: -9px; }

.ticket-stub-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: rgba(0, 230, 118, 0.15);
  border: 1px solid var(--primary);
  color: var(--primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
  margin-bottom: 8px;
}
.ticket-stub-title {
  font-family: var(--font-heading);
  font-size: 0.85rem;
  letter-spacing: 0.5px;
  color: #FFF;
  text-transform: uppercase;
}
.ticket-code-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  margin-top: 8px;
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid var(--primary);
  border-radius: 20px;
  color: var(--primary);
  font-family: monospace;
  font-size: 0.88rem;
  font-weight: 700;
  letter-spacing: 1px;
}

.ticket-body {
  flex: 1;
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.ticket-body-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}
.ticket-discount-value {
  font-family: var(--font-heading);
  font-size: 1.7rem;
  color: var(--primary);
  text-shadow: 0 0 12px rgba(0, 230, 118, 0.4);
  line-height: 1.1;
}
.ticket-discount-desc {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-top: 4px;
}
.ticket-body-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 14px;
  padding-top: 10px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  font-size: 0.8rem;
  color: var(--text-dim);
}

/* Custom Toggle Switch */
.custom-toggle-container {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  user-select: none;
}
.custom-toggle-switch {
  position: relative;
  width: 48px;
  height: 24px;
}
.custom-toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}
.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: #2D3344;
  transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}
.toggle-slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 3px;
  bottom: 3px;
  background-color: #FFF;
  transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 50%;
}
.custom-toggle-switch input:checked + .toggle-slider {
  background-color: var(--primary);
  box-shadow: 0 0 10px rgba(0, 230, 118, 0.4);
}
.custom-toggle-switch input:checked + .toggle-slider:before {
  transform: translateX(24px);
  background-color: #000;
}
```

- [ ] **Step 2: Thêm đoạn CSS trên vào cuối file `css/style.css`**
- [ ] **Step 3: Kiểm tra cú pháp CSS và các bài test hiện có**

Run: `python verify_implementation.py`
Expected: 66/66 PASS

- [ ] **Step 4: Commit cục bộ**

```bash
git add css/style.css
git commit -m "feat(css): add styles for neon voucher ticket preview and custom toggle switch"
```

---

### Task 2: Nâng Cấp Form Cấu Hình & Thẻ Vé Trong `admin/settings.html`

**Files:**
- Modify: `admin/settings.html:99-122`

**Interfaces:**
- Consumes: Cấu trúc section `VOUCHER & VẬN CHUYỂN`.
- Produces:
  - Khung xem trước thẻ vé `#voucher-ticket-card`.
  - Form với các trường riêng biệt: Mã code (`#voucher-code`), Loại giảm (`#voucher-type`), Mức giảm (`#voucher-amount`), Đơn tối thiểu (`#voucher-min-spend`), Hạn dùng (`#voucher-expiry`), và Công tắc kích hoạt (`#voucher-toggle-active`).
  - Khung cấu hình Chính sách vận chuyển 2H với Đơn miễn phí ship (`#ship-min-free`) và Phí ship tiêu chuẩn (`#ship-fee`).

- [ ] **Step 1: Viết cấu trúc HTML nâng cấp cho section Voucher & Vận chuyển**

Thay thế toàn bộ `<section class="admin-section-box" style="max-width: 680px;">` thứ 2 trong `admin/settings.html`:

```html
      <!-- Voucher & Shipping Settings (Nâng Cấp Hướng 1: Thẻ Vé Neon Coupon Live Preview) -->
      <section class="admin-section-box" style="max-width: 740px;">
        <div class="admin-section-header">
          <h2 class="admin-section-title"><i class="fas fa-ticket" style="color: var(--secondary);"></i> VOUCHER KHUYẾN MÃI & VẬN CHUYỂN</h2>
          <div class="custom-toggle-container">
            <span id="voucher-status-label" style="font-size: 0.8rem; font-weight: 700; color: var(--primary);">ĐANG BẬT</span>
            <label class="custom-toggle-switch">
              <input type="checkbox" id="voucher-toggle-active" checked onchange="handleVoucherStatusToggle(this)" />
              <span class="toggle-slider"></span>
            </label>
          </div>
        </div>

        <!-- Thẻ Vé Coupon Neon Trực Quan (Live Preview) -->
        <div id="voucher-ticket-preview" class="voucher-ticket-card">
          <div class="ticket-stub">
            <div class="ticket-stub-icon"><i class="fas fa-bolt"></i></div>
            <div class="ticket-stub-title">ENERGY BOOST</div>
            <div class="ticket-code-pill" id="preview-ticket-code"><i class="fas fa-copy"></i> MONSTER10</div>
          </div>
          <div class="ticket-body">
            <div class="ticket-body-top">
              <div>
                <div class="ticket-discount-value" id="preview-ticket-discount">GIẢM 10%</div>
                <div class="ticket-discount-desc" id="preview-ticket-desc">Áp dụng cho đơn hàng từ 200.000đ (Tối đa 50k)</div>
              </div>
              <span class="badge-status success" id="preview-ticket-badge"><i class="fas fa-circle-check"></i> ĐANG ÁP DỤNG</span>
            </div>
            <div class="ticket-body-bottom">
              <span><i class="fas fa-calendar-alt" style="color: var(--accent-cyan); margin-right: 4px;"></i> Hạn sử dụng: <strong id="preview-ticket-expiry" style="color: #FFF;">31/12/2026</strong></span>
              <span><i class="fas fa-users" style="color: var(--accent-gold); margin-right: 4px;"></i> Áp dụng: Tất cả khách hàng</span>
            </div>
          </div>
        </div>

        <!-- Form Cấu Hình Chi Tiết Tách Biệt Từng Trường -->
        <form onsubmit="handleSaveVoucherSettings(event)">
          <div style="font-size: 0.88rem; font-weight: 700; color: var(--primary); text-transform: uppercase; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
            <i class="fas fa-sliders"></i> Chi Tiết Mã Giảm Giá Mặc Định
          </div>

          <div class="admin-form-grid" style="margin-bottom: 20px;">
            <div class="admin-form-group">
              <label class="admin-form-label" for="voucher-code"><i class="fas fa-barcode"></i> Mã Code Khuyến Mãi <span class="req">*</span></label>
              <input type="text" id="voucher-code" class="admin-form-input" value="MONSTER10" oninput="updateVoucherLivePreview()" required />
            </div>

            <div class="admin-form-group">
              <label class="admin-form-label" for="voucher-type"><i class="fas fa-percent"></i> Loại Giảm Giá <span class="req">*</span></label>
              <select id="voucher-type" class="admin-form-select" onchange="updateVoucherLivePreview()">
                <option value="percent" selected>Giảm theo phần trăm (%)</option>
                <option value="fixed">Giảm số tiền cố định (VNĐ)</option>
              </select>
            </div>

            <div class="admin-form-group">
              <label class="admin-form-label" for="voucher-amount"><i class="fas fa-tags"></i> Mức Giảm <span class="req">*</span></label>
              <input type="text" id="voucher-amount" class="admin-form-input" value="10%" oninput="updateVoucherLivePreview()" required />
            </div>

            <div class="admin-form-group">
              <label class="admin-form-label" for="voucher-min-spend"><i class="fas fa-coins"></i> Đơn Tối Thiểu</label>
              <input type="text" id="voucher-min-spend" class="admin-form-input" value="200.000đ" oninput="updateVoucherLivePreview()" />
            </div>

            <div class="admin-form-group">
              <label class="admin-form-label" for="voucher-max-discount"><i class="fas fa-shield-alt"></i> Giảm Tối Đa</label>
              <input type="text" id="voucher-max-discount" class="admin-form-input" value="50.000đ" oninput="updateVoucherLivePreview()" />
            </div>

            <div class="admin-form-group">
              <label class="admin-form-label" for="voucher-expiry"><i class="fas fa-clock"></i> Ngày Hết Hạn</label>
              <input type="date" id="voucher-expiry" class="admin-form-input" value="2026-12-31" onchange="updateVoucherLivePreview()" />
            </div>
          </div>

          <div style="font-size: 0.88rem; font-weight: 700; color: var(--secondary); text-transform: uppercase; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
            <i class="fas fa-truck-fast"></i> Chính Sách Vận Chuyển Hỏa Tốc 2H
          </div>

          <div class="admin-form-grid" style="margin-bottom: 16px;">
            <div class="admin-form-group">
              <label class="admin-form-label" for="ship-min-free"><i class="fas fa-gift"></i> Miễn Phí Vận Chuyển Từ</label>
              <input type="text" id="ship-min-free" class="admin-form-input" value="200.000đ" />
            </div>

            <div class="admin-form-group">
              <label class="admin-form-label" for="ship-standard-fee"><i class="fas fa-money-bill-wave"></i> Phí Giao Tiêu Chuẩn</label>
              <input type="text" id="ship-standard-fee" class="admin-form-input" value="25.000đ" />
            </div>
          </div>

          <button type="submit" class="btn-add-cart" style="padding: 12px 28px; font-weight: 700;">
            <i class="fas fa-save"></i> Lưu Cấu Hình Voucher & Vận Chuyển
          </button>
        </form>
      </section>
```

- [x] **Step 2: Thực hiện thay thế nội dung trong `admin/settings.html`**
- [x] **Step 3: Chạy script kiểm thử để đảm bảo cấu trúc HTML hoạt động tốt**

Run: `python scripts/verify_admin_ui_mockup.py; python verify_implementation.py`
Expected: 10/10 PASS và 66/66 PASS.

- [x] **Step 4: Commit cục bộ**

```bash
git add admin/settings.html
git commit -m "feat(settings): upgrade voucher settings section with ticket preview and structured fields"
```

---

### Task 3: Viết Logic Tương Tác Live Preview & Xử Lý Form (`js/app.js`)

**Files:**
- Modify: `js/app.js`

**Interfaces:**
- Consumes: Các trường input trong form cài đặt voucher.
- Produces:
  - `updateVoucherLivePreview()`: Đồng bộ nội dung form lên thẻ vé coupon (`#preview-ticket-code`, `#preview-ticket-discount`, `#preview-ticket-desc`, `#preview-ticket-expiry`).
  - `handleVoucherStatusToggle(toggle)`: Đổi trạng thái badge thẻ vé giữa "ĐANG ÁP DỤNG" và "TẠM TẮT".
  - `handleSaveVoucherSettings(e)`: Ngăn chặn reload trang, hiển thị Toast Dark Neon xác nhận lưu cấu hình thành công.

- [x] **Step 1: Viết mã hàm trong `js/app.js`**

```javascript
// ==========================================================================
// 20. VOUCHER SETTINGS LIVE PREVIEW & CONTROLLER
// ==========================================================================
function updateVoucherLivePreview() {
  const codeEl = document.getElementById('voucher-code');
  const amountEl = document.getElementById('voucher-amount');
  const typeEl = document.getElementById('voucher-type');
  const minSpendEl = document.getElementById('voucher-min-spend');
  const maxDiscEl = document.getElementById('voucher-max-discount');
  const expiryEl = document.getElementById('voucher-expiry');

  const previewCode = document.getElementById('preview-ticket-code');
  const previewDiscount = document.getElementById('preview-ticket-discount');
  const previewDesc = document.getElementById('preview-ticket-desc');
  const previewExpiry = document.getElementById('preview-ticket-expiry');

  const code = (codeEl && codeEl.value) ? codeEl.value.trim().toUpperCase() : 'MONSTER10';
  const amount = (amountEl && amountEl.value) ? amountEl.value.trim() : '10%';
  const type = typeEl ? typeEl.value : 'percent';
  const minSpend = (minSpendEl && minSpendEl.value) ? minSpendEl.value.trim() : '200.000đ';
  const maxDisc = (maxDiscEl && maxDiscEl.value) ? maxDiscEl.value.trim() : '50.000đ';
  
  if (previewCode) {
    previewCode.innerHTML = `<i class="fas fa-copy"></i> ${code}`;
  }
  if (previewDiscount) {
    previewDiscount.textContent = type === 'percent' ? `GIẢM ${amount}` : `GIẢM ${amount} Đ`;
  }
  if (previewDesc) {
    previewDesc.textContent = `Áp dụng cho đơn hàng từ ${minSpend} (Tối đa ${maxDisc})`;
  }
  if (previewExpiry && expiryEl && expiryEl.value) {
    const parts = expiryEl.value.split('-');
    if (parts.length === 3) {
      previewExpiry.textContent = `${parts[2]}/${parts[1]}/${parts[0]}`;
    }
  }
}

function handleVoucherStatusToggle(toggle) {
  const isChecked = toggle ? toggle.checked : true;
  const label = document.getElementById('voucher-status-label');
  const badge = document.getElementById('preview-ticket-badge');
  const card = document.getElementById('voucher-ticket-preview');

  if (label) {
    label.textContent = isChecked ? 'ĐANG BẬT' : 'ĐÃ TẮT';
    label.style.color = isChecked ? 'var(--primary)' : 'var(--text-muted)';
  }
  if (badge) {
    badge.className = isChecked ? 'badge-status success' : 'badge-status danger';
    badge.innerHTML = isChecked ? '<i class="fas fa-circle-check"></i> ĐANG ÁP DỤNG' : '<i class="fas fa-circle-xmark"></i> TẠM NGƯNG';
  }
  if (card) {
    card.style.opacity = isChecked ? '1' : '0.55';
    card.style.filter = isChecked ? 'none' : 'grayscale(0.7)';
  }
  showToast(isChecked ? 'Đã kích hoạt chương trình Voucher trên toàn hệ thống!' : 'Đã tạm ngưng áp dụng Voucher trên website.', isChecked ? 'success' : 'warning');
}

function handleSaveVoucherSettings(e) {
  if (e && e.preventDefault) e.preventDefault();
  const codeEl = document.getElementById('voucher-code');
  const code = (codeEl && codeEl.value) ? codeEl.value.trim().toUpperCase() : 'MONSTER10';

  showToast(`Đã lưu thành công cấu hình Voucher "${code}" & chính sách vận chuyển!`, 'success');
}
```

- [x] **Step 2: Thêm các hàm trên vào `js/app.js`**
- [x] **Step 3: Kiểm tra cú pháp JavaScript**

Run: `node -c js/app.js`
Expected: 0 errors

- [x] **Step 4: Commit cục bộ**

```bash
git add js/app.js
git commit -m "feat(settings): implement live preview controller and toast handlers for voucher settings"
```

---

### Task 4: Kiểm Thử Toàn Diện & Nghiệm Thu

**Files:**
- Test: `scripts/verify_admin_ui_mockup.py`
- Test: `verify_implementation.py`

- [x] **Step 1: Chạy kiểm thử tự động 10 tiêu chí rubric**

Run: `python scripts/verify_admin_ui_mockup.py`
Expected: 10/10 PASS

- [x] **Step 2: Chạy kiểm thử toàn bộ hệ thống**

Run: `python verify_implementation.py`
Expected: 66/66 PASS

- [x] **Step 3: Kiểm tra Git status đảm bảo sạch sẽ**

Run: `git status -s`
Expected: Clean working tree

- [x] **Step 4: Commit tổng kết**

```bash
git commit --allow-empty -m "docs: complete voucher settings UI upgrade with live neon coupon preview"
```

---

## Verification Plan

### Automated Tests
1. `python scripts/verify_admin_ui_mockup.py` ➔ Xác nhận 10/10 PASS.
2. `python verify_implementation.py` ➔ Xác nhận 66/66 PASS.
3. `node -c js/app.js` ➔ Xác nhận không lỗi cú pháp.

### Manual Verification
1. Mở [`admin/settings.html`](file:///d:/LapTrinhWeb/admin/settings.html) trên Google Chrome.
2. Cuộn xuống phần **VOUCHER KHUYẾN MÃI & VẬN CHUYỂN**:
   - Kiểm tra **Thẻ Vé Neon Coupon Live Preview**: Thấy cuống vé bên trái có icon sấm sét phát sáng, mã `MONSTER10` có viền bo tròn, 2 vết khuyết tròn (notches) ở viền cắt răng cưa, bên phải hiển thị `GIẢM 10%` to rõ và badge `ĐANG ÁP DỤNG`.
   - Thử gõ thay đổi mã code thành `ENERGY2026` ➔ Xem mã trên thẻ vé cập nhật ngay lập tức.
   - Thử đổi mức giảm thành `15%` ➔ Dòng chữ lớn trên vé cập nhật thành `GIẢM 15%`.
   - Gạt công tắc Toggle Switch sang Tắt ➔ Thẻ vé chuyển mờ xám grayscale, badge đổi thành `TẠM NGƯNG` và bắn Toast màu vàng cảnh báo.
   - Gạt bật lại ➔ Thẻ vé bừng sáng neon xanh trở lại.
   - Bấm nút **Lưu Cấu Hình Voucher & Vận Chuyển** ➔ Bắn Toast thông báo Dark Neon xác nhận thành công.
