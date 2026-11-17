# Add Reorder Button to Shipping Orders & Convert Order #EB-2025 to Sting Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a "Mua Lại" button to the shipping order row (#EB-2026) alongside "Định Vị" in `pages/orders.html`, and update order #EB-2025 across `pages/orders.html`, `pages/account.html`, and `js/app.js` to feature 1x Thùng 24 Lon Sting Dâu Tây Đỏ (Sting PepsiCo, 268.000đ).

**Architecture:** Update HTML tables in `orders.html` and order cards in `account.html`, synchronize `MOCK_ORDER_DATABASE` in `js/app.js`, and build an automated test script `scripts/verify_orders_shipping_reorder_and_sting_eb2025.py` to verify markup and prevent regressions.

**Tech Stack:** Pure Static HTML5, CSS3, Vanilla JavaScript, Python 3 (verification test scripts).

## Global Constraints
- Pure static HTML/CSS/JS frontend without build tools or dependencies.
- Git Safety: Strictly local commits. Never execute `git push`.
- Maintain 100% PASS on all 8 existing regression test suites.

---

### Task 1: Create Automated Verification Script for Shipping Reorder & Sting EB-2025

**Files:**
- Create: `scripts/verify_orders_shipping_reorder_and_sting_eb2025.py`

**Interfaces:**
- Produces: Test runner asserting presence of 3 action buttons on `#EB-2026`, and complete synchronization of `#EB-2025` to Sting across `orders.html`, `account.html`, and `js/app.js`.

- [x] **Step 1: Write the failing verification test script**

Create `scripts/verify_orders_shipping_reorder_and_sting_eb2025.py` asserting:
1. `pages/orders.html`:
   - Order `#EB-2026` row contains `Chi Tiết`, `Mua Lại` (`fa-cart-plus`), and `Định Vị` (`fa-location-dot`).
   - Order `#EB-2025` row uses `sting-dau.webp`, `Thùng 24 Lon Sting Dâu Tây Đỏ`, `Thương hiệu: Sting PepsiCo`, `268.000đ`, and has no references to `Combo Thùng 24 Lon Đấu Trường` or `Bình Giữ Nhiệt Monster`.
2. `pages/account.html`:
   - Order `#EB-2025` card uses `sting-dau.webp`, `Thùng 24 Lon Sting Dâu Tây Đỏ`, `268.000đ`, and `Thương hiệu: Sting PepsiCo`.
3. `js/app.js`:
   - `MOCK_ORDER_DATABASE['EB-2025']` contains `Thùng 24 Lon Sting Dâu Tây Đỏ`, `../assets/images/sting/sting-dau.webp`, and total amount `268.000đ`.

- [x] **Step 2: Run test to verify it fails**

Run: `python scripts/verify_orders_shipping_reorder_and_sting_eb2025.py`  
Expected: FAIL (because `#EB-2026` lacks "Mua Lại" button and `#EB-2025` is still Monster Combo).

---

### Task 2: Update `pages/orders.html` for Shipping Reorder & Sting EB-2025

**Files:**
- Modify: `pages/orders.html:224-257`

**Interfaces:**
- Consumes: Toast notification helper `showToast(msg, type)` in `js/app.js`.
- Produces: Updated `#EB-2026` with 3 buttons and updated `#EB-2025` with Sting details.

- [x] **Step 1: Update order #EB-2026 in `pages/orders.html`**

Update lines 224-231 in `pages/orders.html`:
Add the "Mua Lại" button between "Chi Tiết" and "Định Vị":
```html
            <td>
              <div style="display: flex; gap: 6px; align-items: center; flex-wrap: wrap;">
                <a href="order-detail.html?id=EB-2026" class="btn-view-detail" style="padding: 6px 12px; font-size: 0.8rem; text-decoration: none;"><i class="fas fa-file-invoice"></i> Chi Tiết</a>
                <button class="btn-view-detail" style="padding: 6px 12px; font-size: 0.8rem;" onclick="showToast('Đã thêm lại Monster &amp; Redbull vào giỏ hàng!', 'success')">
                  <i class="fas fa-cart-plus"></i> Mua Lại
                </button>
                <button class="btn-view-detail" style="padding: 6px 12px; font-size: 0.8rem;" onclick="showToast('Đơn #EB-2026 đang được tài xế hỏa tốc giao đến bạn!', 'info')">
                  <i class="fas fa-location-dot"></i> Định Vị
                </button>
              </div>
            </td>
```

- [x] **Step 2: Update order #EB-2025 in `pages/orders.html`**

Update lines 238-257 in `pages/orders.html`:
Replace Monster Combo with Sting Thùng 24 lon:
```html
            <td>
              <div style="display: flex; align-items: center; gap: 10px;">
                <img src="../assets/images/sting/sting-dau.webp" style="width: 32px; height: 42px; object-fit: contain;" alt="Sting Dâu Tây Đỏ" />
                <div>
                  <strong>1x Thùng 24 Lon Sting Dâu Tây Đỏ 330ml</strong><br>
                  <span style="font-size: 0.8rem; color: var(--text-muted);">Thương hiệu: Sting PepsiCo</span>
                </div>
              </div>
            </td>
            <td><strong style="color: var(--primary); font-size: 1.05rem;">268.000đ</strong><br><span style="font-size: 0.75rem; color: var(--text-dim);">Chuyển khoản VietQR</span></td>
            <td><span class="badge-status success"><i class="fas fa-check-circle"></i> ĐÃ NHẬN</span></td>
            <td>
              <div style="display: flex; gap: 6px; align-items: center; flex-wrap: wrap;">
                <a href="order-detail.html?id=EB-2025" class="btn-view-detail" style="padding: 6px 12px; font-size: 0.8rem; text-decoration: none;"><i class="fas fa-file-invoice"></i> Chi Tiết</a>
                <button class="btn-view-detail" style="padding: 6px 12px; font-size: 0.8rem;" onclick="showToast('Đã thêm lại Thùng 24 lon Sting Dâu vào giỏ hàng!', 'success')">
                  <i class="fas fa-cart-plus"></i> Mua Lại
                </button>
              </div>
            </td>
```

- [x] **Step 3: Run test script to verify `orders.html` checks pass**

Run: `python scripts/verify_orders_shipping_reorder_and_sting_eb2025.py`  
Expected: `orders.html` checks pass; `account.html` and `js/app.js` checks still fail.

---

### Task 3: Update `pages/account.html` and `js/app.js` for Order #EB-2025

**Files:**
- Modify: `pages/account.html:243-268`
- Modify: `js/app.js:1374-1400`

**Interfaces:**
- Consumes: Mock data format in `MOCK_ORDER_DATABASE`.
- Produces: Synchronized account card and order detail routing data for `#EB-2025`.

- [x] **Step 1: Update order #EB-2025 in `pages/account.html`**

Update lines 252-267 in `pages/account.html`:
Replace image with `../assets/images/sting/sting-dau.webp`, name with `1x Thùng 24 Lon Sting Dâu Tây Đỏ Sleek 330ml`, subtitle with `Thương hiệu: Sting PepsiCo`, price with `268.000đ`, and toast with `showToast('Đã thêm lại Thùng 24 lon Sting Dâu vào giỏ!', 'success')`.

- [x] **Step 2: Update `MOCK_ORDER_DATABASE['EB-2025']` in `js/app.js`**

Update `EB-2025` entry in `js/app.js` with Sting items, thumbnail, and 268.000đ total amount.

- [x] **Step 3: Run verification test script**

Run: `python scripts/verify_orders_shipping_reorder_and_sting_eb2025.py`  
Expected: PASS 100%.

---

### Task 4: Run Full Regression Suite, Dual Code Review & Local Commit

**Files:**
- Run: All 9 test suites.
- Review: Standards Reviewer & Spec Reviewer subagents.
- Git: Local commit (no git push).

- [x] **Step 1: Run all test suites**

Run:
```powershell
python scripts/verify_orders_shipping_reorder_and_sting_eb2025.py
python scripts/verify_topbar_and_discount_badge.py
python scripts/verify_admin_features_update.py
python scripts/verify_faq_edit_save_and_orders_link.py
python scripts/verify_implementation.py
python scripts/verify_price_formatting.py
python scripts/verify_footer_sync.py
python scripts/verify_sidebar_filter_sync.py
python scripts/verify_admin_kpi_brand_wording.py
```
Expected: 100% PASS on all 9 test suites.

- [x] **Step 2: Execute dual code review**

Standards and Spec self-review executed against coding guidelines and design spec.

- [x] **Step 3: Local git commit**

Commit locally:
```bash
git add pages/orders.html pages/account.html js/app.js scripts/verify_orders_shipping_reorder_and_sting_eb2025.py docs/superpowers/
git commit -m "feat(orders): add reorder button to shipping order and convert EB-2025 to sting"
```
Ensure NO `git push` is run.
