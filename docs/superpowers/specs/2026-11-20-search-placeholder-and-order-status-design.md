# Design Spec: Search Placeholder Refinement & Account Order Status Unification

**Date:** 2026-11-20  
**Status:** Approved  
**Author:** AI Assistant  

---

## 1. Problem Statement & User Intent
1. **Storefront search bar whitespace balance:** Shortening the search placeholder to `"Tìm kiếm Monster, Redbull..."` (30 chars) prevented clipping on narrow screens, but left noticeable empty space inside `.search-box` (`max-width: 480px`) on desktop. The user wants **Approach 1**: fill that space cleanly with `"Tìm kiếm Monster, Redbull, Sting..."` (36 chars — dropping `"Energy"` from the original 43-char string) while keeping the existing CSS `min-width: 0; text-overflow: ellipsis;` safeguard in `css/style.css` and keeping the static `#search-dropdown-menu` typing behavior completely unchanged.
2. **Account order status unification (`HOÀN THÀNH`):** On `pages/account.html`, order `#EB-2026` displays `<i class="fas fa-truck-fast"></i> ĐÃ GIAO HỎA TỐC 2H` (while already marked `(Đã trả COD)`), whereas order `#EB-2025` displays `<i class="fas fa-check-circle"></i> HOÀN THÀNH`. The static pre-JS fallback in `pages/order-detail.html` for `#EB-2026` also displays `ĐÃ GIAO HỎA TỐC 2H`. The user wants both `#EB-2026` and `#EB-2025` on the Account page (and the static `#EB-2026` fallback in `pages/order-detail.html`) unified to `<i class="fas fa-check-circle"></i> HOÀN THÀNH`, while preserving `pages/orders.html` (`ĐANG GIAO (2H)` / `Đang Giao (1)` filter pill) and `MOCK_ORDER_DATABASE` in `js/app.js`.

---

## 2. Architecture & Proposed Changes

### 2.1 Search Placeholder Unification (11 Storefront HTML Pages)
Update `<input type="text" class="search-input" ...>` `placeholder` to `"Tìm kiếm Monster, Redbull, Sting..."` across all 11 storefront pages, preserving all existing attributes (`type`, `class`, `autocomplete`, `onfocus`, `onclick`):
- `index.html:54`
- `pages/account.html:49`
- `pages/cart.html:48`
- `pages/order-detail.html:94`
- `pages/orders.html:49`
- `pages/search-results.html:54`
- `pages/product-detail.html:44`
- `pages/product-detail-redbull.html:44`
- `pages/product-detail-sting.html:45`
- `pages/product-detail-redbull-lonvua.html:43`
- `pages/product-detail-redbull-thai.html:43`

CSS (`css/style.css:283-295`) keeps `min-width: 0; text-overflow: ellipsis;` on `.search-input` and `text-overflow: ellipsis;` on `.search-input::placeholder`. `js/app.js` and all `#search-dropdown-menu` lists remain untouched.

### 2.2 Order Status Unification (`HOÀN THÀNH`)
1. `pages/account.html:222`: Change `#EB-2026` status badge from:
   ```html
   <span class="badge-status success" style="font-size: 0.75rem;"><i class="fas fa-truck-fast"></i> ĐÃ GIAO HỎA TỐC 2H</span>
   ```
   to:
   ```html
   <span class="badge-status success" style="font-size: 0.75rem;"><i class="fas fa-check-circle"></i> HOÀN THÀNH</span>
   ```
   matching `#EB-2025` at `pages/account.html:250`.
2. `pages/order-detail.html:242`: Change static fallback badge `#order-detail-status` for `#EB-2026` from:
   ```html
   <span id="order-detail-status" class="badge-status success"><i class="fas fa-truck-fast"></i> ĐÃ GIAO HỎA TỐC 2H</span>
   ```
   to:
   ```html
   <span id="order-detail-status" class="badge-status success"><i class="fas fa-check-circle"></i> HOÀN THÀNH</span>
   ```
3. `pages/orders.html` and `js/app.js` (`MOCK_ORDER_DATABASE`) remain unchanged so the `Đang Giao (1)` filter tab and `verify_orders_shipping_reorder_and_sting_eb2025.py` stay intact.

---

## 3. Verification Strategy
1. Update `scripts/verify_search_placeholder_polish.py` so `EXPECTED_PLACEHOLDER = "Tìm kiếm Monster, Redbull, Sting..."`, remove `"Tìm kiếm Monster, Redbull, Sting..."` from `DISALLOWED_PLACEHOLDERS`, and add `"Tìm kiếm Monster, Redbull..."` (30-char placeholder) to `DISALLOWED_PLACEHOLDERS`.
2. Add `scripts/verify_account_order_status_sync.py` to assert:
   - In `pages/account.html`, both `#EB-2026` and `#EB-2025` cards display `<span class="badge-status success" style="font-size: 0.75rem;"><i class="fas fa-check-circle"></i> HOÀN THÀNH</span>`.
   - `pages/account.html` and `pages/order-detail.html` contain zero occurrences of `"ĐÃ GIAO HỎA TỐC 2H"`.
   - `pages/order-detail.html` `#order-detail-status` fallback shows `<i class="fas fa-check-circle"></i> HOÀN THÀNH`.
   - `pages/orders.html` preserves `ĐANG GIAO (2H)` and `Đang Giao` filter tab.
3. Run `verify_search_placeholder_polish.py`, `verify_account_order_status_sync.py`, `verify_implementation.py`, and all `scripts/verify_*.py` scripts to confirm 100% PASS.
4. Commit locally without `git push`.
