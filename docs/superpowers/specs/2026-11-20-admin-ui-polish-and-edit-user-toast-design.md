# Design Spec: Admin Dashboard Search Polish, Stock Status Simplification, and Toast-Only User Edit

**Date:** 2026-11-20  
**Status:** Approved  
**Author:** AI Assistant  

---

## 1. Problem Statement & User Intent
Three UI/UX issues in the Admin section need to be resolved together:
1. **Dashboard order search placeholder clipped (`admin/index.html:135`):** `#dash-order-keyword` uses `placeholder="Tìm mã đơn hoặc khách..."` (25 chars) inside an inline `width: 170px` box (`132px` net text width), clipping mid-word as `"Tìm mã đơn hoặc khá"`. The user selected **Approach 1**: shorten placeholder to `"Tìm mã đơn, khách..."` (20 chars), replace inline `width: 170px` with a unified `.admin-filter-search--compact` (`195px` desktop, `100%` at `<= 640px`) across both `#dash-order-keyword` and `#dash-inv-keyword`, and add `min-width: 0; text-overflow: ellipsis;` on `.admin-filter-search input` & `::placeholder` in `css/style.css`.
2. **Verbose stock status dropdown label (`admin/inventory.html:98` & 5 `admin/edit-*.html`):** `#filter-inv-stock` displays `"CÒN HÀNG (Sẵn sàng xuất)"` and the 5 product edit pages display `"Còn hàng (Sẵn sàng xuất kho)"`. The user wants only `"CÒN HÀNG"` in `admin/inventory.html:98` and `"Còn hàng"` in the 5 `admin/edit-*.html` files (preserving the `admin/inventory.html:57` page subtitle).
3. **Edit User Modal (`saveEditUser` / `openEditUserModal`) corrupting VIP rank badge & mutating UI (`js/app.js:2544-2622`):**
   - Root cause: `openEditUserModal` (`js/app.js:2562`) and `saveEditUser` (`js/app.js:2592`) called `currentEditingUserRow.querySelector('.badge-status')`, which matched `cells[0]` (the **Hạng** column `#1 VIP`..`#5 VIP`!) rather than `cells[5]` (the **Trạng Thái** column `ĐANG HOẠT ĐỘNG` / `ĐÃ KHOÁ`), causing Row 3 (`#3 VIP`) to turn into `"ĐANG HOẠT ĐỘNG"` with altered styling upon saving.
   - User intent: When editing a user's info, tier, or status and clicking Save, **never mutate the table UI or `localStorage`** (keep rank badge `#1 VIP`–`#5 VIP`, colors, status badge, and lock/unlock buttons untouched) and **only show a toast notification** + close `#modal-edit-user`. Also fix `openEditUserModal` so it reads status from `cells[5]` (not `cells[0]`) and pre-fills `#edit-user-tier` accurately when opening the modal.

---

## 2. Architecture & Proposed Changes

### 2.1 Dashboard Quick Filter Search Polish (`admin/index.html` & `css/style.css`)
- `admin/index.html:133-136` (`ĐƠN HÀNG MỚI NHẤT`):
  - Add `admin-filter-search--compact` to the `.admin-filter-search` wrapper.
  - Update `#dash-order-keyword`: set `placeholder="Tìm mã đơn, khách..."` and remove `width: 170px;` from inline `style` (`style="padding: 5px 10px 5px 28px; font-size: 0.8rem;"`).
- `admin/index.html:293-296` (`QUẢN LÝ KHO`):
  - Add `admin-filter-search--compact` to the `.admin-filter-search` wrapper.
  - Update `#dash-inv-keyword`: keep `placeholder="Tìm tên sản phẩm..."` and remove `width: 170px;` from inline `style` (`style="padding: 5px 10px 5px 28px; font-size: 0.8rem;"`).
- `css/style.css`:
  - Around line 4794 (`.admin-filter-search input`): add `min-width: 0;` and `text-overflow: ellipsis;`, plus `.admin-filter-search input::placeholder { text-overflow: ellipsis; }`, plus `.admin-filter-search--compact input { width: 195px; }`.
  - Inside `@media (max-width: 640px)` (around line 5617): add `.admin-filter-search--compact input { width: 100%; }`.

### 2.2 Simplify Stock Status Labels (`admin/inventory.html` & 5 `admin/edit-*.html`)
- `admin/inventory.html:98`: change `<option value="instock" selected>CÒN HÀNG (Sẵn sàng xuất)</option>` to `<option value="instock" selected>CÒN HÀNG</option>`. Keep line 57 (`- Sẵn sàng xuất kho`) unchanged.
- Update `<option value="Còn hàng" selected>Còn hàng (Sẵn sàng xuất kho)</option>` to `<option value="Còn hàng" selected>Còn hàng</option>` in:
  - `admin/edit-monster.html:189`
  - `admin/edit-redbull-lonvua.html:185`
  - `admin/edit-redbull-original.html:184`
  - `admin/edit-redbull-thai.html:185`
  - `admin/edit-sting.html:184`

### 2.3 Fix `openEditUserModal` & Make `saveEditUser` Toast-Only (`js/app.js`)
- `openEditUserModal(customerKey, btn)` (`js/app.js:2544-2573`):
  - Read status badge from `currentEditingUserRow.cells[5]` (`currentEditingUserRow.cells[5] ? currentEditingUserRow.cells[5].querySelector('.badge-status') : null`) instead of `currentEditingUserRow.querySelector('.badge-status')` (which hit `cells[0]` VIP rank badge).
  - Pre-fill `#edit-user-tier` from `cells[1]` text (`KIM CƯƠNG` → `'diamond'`, `VÀNG` → `'gold'`, `BẠC` → `'silver'`, else `'standard'`) or from `CUSTOMER_DATA_REGISTRY[customerKey].tier`.
- `saveEditUser(e)` (`js/app.js:2575-2622`):
  - Prevent default form submission (`e.preventDefault()`).
  - Read `#edit-user-fullname`, `#edit-user-tier` selected option text, and `#edit-user-status` selected option text.
  - Display toast: `showToast('Đã lưu thay đổi thông tin người dùng "' + name + '"' + (details ? ' (' + details + ')' : '') + ' thành công!', 'success')`.
  - Close `#modal-edit-user` via `closeAdminModal('modal-edit-user')`.
  - **Zero DOM or `localStorage` mutations** inside `saveEditUser` so rank badges (`#1 VIP`–`#5 VIP`), colors, status badges (`ĐANG HOẠT ĐỘNG` / `ĐÃ KHOÁ`), and lock/unlock buttons remain completely unchanged on screen.

---

## 3. Verification Strategy
1. `scripts/verify_admin_dashboard_search_and_stock_label.py`: verifies Task 1 (`admin/index.html` & `css/style.css`) and Task 2 (`admin/inventory.html` & 5 `admin/edit-*.html`).
2. `scripts/verify_admin_edit_user_toast_only.py`: runs both static checks on `js/app.js` and a Node.js DOM/VM runtime test verifying:
   - `openEditUserModal` reads `#5 VIP` (`Vũ Thảo My`) status from `cells[5]` as `'locked'` and `#3 VIP` (`Trần Thị Bích`) tier as `'gold'` & status `'active'`.
   - Calling `saveEditUser` after changing `#edit-user-fullname`, `#edit-user-tier` (`'standard'`), and `#edit-user-status` (`'locked'`) invokes `showToast(...)` and `closeAdminModal('modal-edit-user')` while preserving `cells[0]` (`#3 VIP` badge text, class, and inline style), `cells[5]` (`ĐANG HOẠT ĐỘNG`), `cells[6]` button, and `localStorage` completely unmodified.
3. Run `verify_implementation.py` and all `scripts/verify_*.py` scripts (including `verify_unconstrained_add_user.py` and `verify_admin_ui_mockup.py`) to guarantee 0 regressions.
4. Commit locally without `git push`.
