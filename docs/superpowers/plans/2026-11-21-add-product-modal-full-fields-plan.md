# Add Product Modal Full Fields Sync Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade `#modal-add-product` ("Thêm Sản Phẩm Mới") in both `admin/inventory.html` and `admin/index.html` to include all 12 detailed product fields matching the standalone edit pages (`admin/edit-*.html`), wire `#add-prod-oldprice` currency formatting/reset in `js/app.js`, and add automated verification.

**Architecture:** Both `admin/inventory.html` and `admin/index.html` share the `#modal-add-product` overlay markup. Keeping `#add-prod-name`, `#add-product-images`, `#add-prod-brand` (`<select>` with the 3 canonical brands for Rubric 2.3), `#add-prod-origin`, `#add-prod-price`, `#add-prod-volume`, and `#add-prod-status` IDs intact preserves full compatibility with existing scripts while adding `#add-prod-oldprice`, `#add-prod-flavor`, `#add-prod-ingredients`, `#add-prod-usage`, `#add-prod-storage`, and `#add-prod-stock`, updating `Trạng Thái Kho` options to `Còn hàng` / `Sắp hết hàng` / `Tạm hết hàng`, and standardizing the cancel button label to `Hủy Bỏ`.

**Tech Stack:** Static HTML5, Vanilla CSS3, Vanilla JS, Python 3 + Node.js verification scripts.

## Global Constraints

- Preserve `#add-prod-file`, `#add-prod-file-2`, `#add-prod-file-3`, `#add-prod-preview`, `previewAddProductImage`, `addProductImageField()`, and the `<select id="add-prod-brand">` 3-brand options (`Monster Energy`, `Redbull Thái Lan`, `Sting PepsiCo`) so `scripts/verify_admin_ui_mockup.py` and `scripts/verify_rubric_coverage.py` remain 100% passing.
- Do NOT add any `preview-add-prod-price` element (prohibited by `scripts/verify_price_formatting.py`).
- Keep `admin/inventory.html` and `admin/index.html` `#modal-add-product` markup identical.
- Never run `git push`; keep all commits local on `main`.

---

### Task 1: Upgrade `#modal-add-product` in `admin/inventory.html` and `admin/index.html`

**Files:**
- Modify: `admin/inventory.html:510-580`
- Modify: `admin/index.html:686-756`

- [ ] **Step 1:** In both `admin/inventory.html` and `admin/index.html`, update `#modal-add-product` `.admin-form-grid` and `.admin-modal-footer` so it contains all 12 fields in order alongside the preserved `#add-product-images` block:
  1. `Tên Sản Phẩm Đầy Đủ <span class="req">*</span>` — `<input type="text" id="add-prod-name" class="admin-form-input" placeholder="VD: Monster Ultra Sunrise 500ml" required />` (`full-width`)
  2. Preserved `Hình ảnh sản phẩm` block (`#add-product-images` with `#add-prod-file`, `#add-prod-preview`, `#add-prod-file-2`, `#add-prod-file-3`, and `+ Thêm ảnh` button calling `addProductImageField()`) (`full-width`)
  3. `Thương Hiệu <span class="req">*</span>` — `<select id="add-prod-brand" class="admin-form-select" required>` with `Monster Energy` (`selected`), `Redbull Thái Lan`, `Sting PepsiCo`
  4. `Sản Xuất Tại <span class="req">*</span>` — `<input type="text" id="add-prod-origin" class="admin-form-input" placeholder="VD: Malaysia (Ủy quyền Monster Energy Company)" required />`
  5. `Giá Bán Lẻ Hiện Tại <span class="req">*</span>` — `<input type="text" id="add-prod-price" class="admin-form-input price-format-input" placeholder="VD: 48.000đ" required />`
  6. `Giá Niêm Yết Cũ` — `<input type="text" id="add-prod-oldprice" class="admin-form-input price-format-input" placeholder="VD: 55.000đ" />`
  7. `Thể Tích / Quy Cách <span class="req">*</span>` — `<input type="text" id="add-prod-volume" class="admin-form-input" placeholder="VD: 355ml (Lon nhôm cao cấp)" required />`
  8. `Hương Vị Đặc Trưng <span class="req">*</span>` — `<input type="text" id="add-prod-flavor" class="admin-form-input" placeholder="VD: Vị cam chanh nhiệt đới sảng khoái, không đường" required />`
  9. `Thành Phần <span class="req">*</span>` — `<textarea id="add-prod-ingredients" class="admin-form-textarea" rows="3" placeholder="VD: Nước bão hòa CO2, Taurine, Caffeine, Vitamin B3, B6, B2, B12..." required></textarea>` (`full-width`)
  10. `Hướng Dẫn Sử Dụng <span class="req">*</span>` — `<textarea id="add-prod-usage" class="admin-form-textarea" rows="2" placeholder="VD: Lắc nhẹ trước khi uống, dùng ngay sau khi mở nắp. Ngon hơn khi uống lạnh." required></textarea>` (`full-width`)
  11. `Bảo Quản <span class="req">*</span>` — `<textarea id="add-prod-storage" class="admin-form-textarea" rows="2" placeholder="VD: Để nơi khô ráo, thoáng mát, tránh ánh sáng trực tiếp hoặc nơi có nhiệt độ cao." required></textarea>` (`full-width`)
  12. `Trạng Thái Kho` — `<select id="add-prod-status" class="admin-form-select">` with `Còn hàng` (`selected`), `Sắp hết hàng`, `Tạm hết hàng`
  13. `Số Lượng Tồn Kho Thực Tế` — `<input type="number" id="add-prod-stock" class="admin-form-input" placeholder="VD: 1250" min="0" />`
  14. Footer: `<button type="button" class="btn-modal-cancel" onclick="closeAdminModal('modal-add-product')">Hủy Bỏ</button>` and `<button type="submit" class="btn-modal-save"><i class="fas fa-plus"></i> Thêm Vào Kho</button>`
- [ ] **Step 2:** Run `python scripts/verify_admin_ui_mockup.py`, `python scripts/verify_price_formatting.py`, and `python scripts/verify_rubric_coverage.py` to confirm zero regressions.
- [ ] **Step 3:** Commit locally with message `feat(admin): add full product detail fields to add-product modal`.

---

### Task 2: Wire `#add-prod-oldprice` Formatting and Reset in `js/app.js`

**Files:**
- Modify: `js/app.js:631-657` and `js/app.js:920-936`

- [ ] **Step 1:** In `js/app.js` `initPriceFormatting()`, add `'#add-prod-oldprice'` right after `'#add-prod-price'` in `selectors`.
- [ ] **Step 2:** In `js/app.js` `openAddProductModal()` and `saveAddProduct(e)`, use a small shared loop over `['add-prod-price', 'add-prod-oldprice']` (or helper) so both price fields are set up on open and have `updatePricePreview` refreshed on open and reset.
- [ ] **Step 3:** Run `node --check js/app.js` and `python scripts/verify_price_formatting.py`.
- [ ] **Step 4:** Commit locally with message `fix(admin): support old price formatting and reset in add-product modal`.

---

### Task 3: Add Automated Verification (`scripts/verify_add_product_modal_fields.py`) and Run Admin Suite

**Files:**
- Create: `scripts/verify_add_product_modal_fields.py`

- [ ] **Step 1:** Create `scripts/verify_add_product_modal_fields.py` to check:
  - Both `admin/inventory.html` and `admin/index.html` `#modal-add-product` blocks contain all 12 exact labels (`Tên Sản Phẩm Đầy Đủ`, `Thương Hiệu`, `Sản Xuất Tại`, `Giá Bán Lẻ Hiện Tại`, `Giá Niêm Yết Cũ`, `Thể Tích / Quy Cách`, `Hương Vị Đặc Trưng`, `Thành Phần`, `Hướng Dẫn Sử Dụng`, `Bảo Quản`, `Trạng Thái Kho`, `Số Lượng Tồn Kho Thực Tế`), all 3 stock status options (`Còn hàng`, `Sắp hết hàng`, `Tạm hết hàng`), all required IDs (`add-prod-name`, `add-prod-file`, `add-prod-preview`, `add-prod-brand`, `add-prod-origin`, `add-prod-price`, `add-prod-oldprice`, `add-prod-volume`, `add-prod-flavor`, `add-prod-ingredients`, `add-prod-usage`, `add-prod-storage`, `add-prod-status`, `add-prod-stock`), and `Hủy Bỏ`.
  - Both modals match structurally and do not include prohibited `preview-add-prod-price`.
  - `js/app.js` registers `#add-prod-oldprice` in `initPriceFormatting()` and handles both `add-prod-price` and `add-prod-oldprice` in `openAddProductModal()` / `saveAddProduct()`.
  - Node.js VM runtime smoke test executing `openAddProductModal()` and `saveAddProduct(event)` cleanly.
- [ ] **Step 2:** Run `python scripts/verify_add_product_modal_fields.py`, `python scripts/verify_admin_ui_mockup.py`, `python scripts/verify_price_formatting.py`, `python scripts/verify_field_sync_and_clean_image_labels.py`, `python scripts/verify_admin_features_update.py`, `python scripts/verify_rubric_coverage.py`, and `python scripts/verify_pages_deploy_ready.py` and verify all exit 0.
- [ ] **Step 3:** Commit locally with message `test(admin): verify full add-product modal fields and price formatting`.
