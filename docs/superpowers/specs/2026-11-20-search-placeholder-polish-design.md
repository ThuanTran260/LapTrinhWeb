# Design Spec: Polish & Unify Storefront Search Placeholder

**Date:** 2026-11-20  
**Status:** In Review  
**Author:** AI Assistant  

---

## 1. Problem Statement & User Intent
In the storefront header search bar (`.search-box` / `.search-input`), the current placeholder `"Tìm kiếm Monster Energy, Redbull, Sting..."` (43 characters) overflows the available input width when `.search-input-group` shares space with two `.search-btn` buttons (`max-width: 480px`). As a result, the final word `"Sting..."` gets clipped mid-character at the right edge (appearing as `"Stinc"`).

Across the 11 storefront HTML pages, the search input currently also uses 5 inconsistent placeholder strings ranging from 36 to 54 characters.

The user wants a cleaner, more polished placeholder ending naturally with `"..."` and unified across all storefront pages:
- Target placeholder text: `"Tìm kiếm Monster, Redbull..."` (30 characters)
- Scope: All 11 storefront HTML pages (`index.html` and 10 storefront pages under `pages/`)
- Layout safeguard: Defensive CSS ellipsis & flex shrink protection on `.search-input`

---

## 2. Architecture & Proposed Changes

### 2.1 Storefront HTML Placeholder Unification (11 files)
Set `placeholder="Tìm kiếm Monster, Redbull..."` on `<input type="text" class="search-input" ...>` in every storefront page:
1. `index.html` (currently `"Tìm kiếm Monster Energy, Redbull, Sting..."`)
2. `pages/account.html` (currently `"Tìm kiếm Monster Energy, Redbull, Sting..."`)
3. `pages/cart.html` (currently `"Tìm kiếm Monster Energy, Redbull, Sting..."`)
4. `pages/order-detail.html` (currently `"Tìm kiếm Monster Energy, Redbull, Sting..."`)
5. `pages/orders.html` (currently `"Tìm kiếm Monster Energy, Redbull, Sting..."`)
6. `pages/search-results.html` (currently `"Tìm kiếm Monster Energy, Redbull, Sting..."`)
7. `pages/product-detail.html` (currently `"Tìm kiếm Monster, Redbull, Sting..."`)
8. `pages/product-detail-redbull.html` (currently `"Tìm kiếm Redbull, Monster, Sting..."`)
9. `pages/product-detail-sting.html` (currently `"Tìm kiếm Sting, Monster, Redbull..."`)
10. `pages/product-detail-redbull-lonvua.html` (currently `"Tìm kiếm vị yêu thích (Redbull Nắp Bật, Sleek Can...)"`)
11. `pages/product-detail-redbull-thai.html` (currently `"Tìm kiếm vị yêu thích (Redbull Thái Lan, Krating Daeng...)"`)

Existing search handlers (`onfocus`, `onclick`, dropdown menus) and non-storefront pages (`pages/login.html`, `pages/payment-gateway.html`, `pages/order-success.html`, `admin/*.html`) remain untouched because they do not contain `.search-input`.

### 2.2 CSS Ellipsis & Flex Shrink Safeguard (`css/style.css`)
Update `.search-input` and `.search-input::placeholder` around lines 283–292 in `css/style.css`:
- Add `min-width: 0;` and `text-overflow: ellipsis;` to `.search-input` so the flex input can shrink cleanly without pushing `.search-btn` or clipping mid-letter on narrow viewports (`< 360px`).
- Add `text-overflow: ellipsis;` to `.search-input::placeholder` for consistent placeholder truncation in engines that style `::placeholder` independently.

---

## 3. Verification Strategy
1. Add verification script `scripts/verify_search_placeholder_polish.py` checking:
   - All 11 storefront HTML files have `<input ... class="search-input" ... placeholder="Tìm kiếm Monster, Redbull...">`.
   - Zero occurrences of `"Tìm kiếm Monster Energy, Redbull, Sting..."` or `"Tìm kiếm vị yêu thích"` remain in storefront `.search-input` placeholders.
   - `css/style.css` defines `min-width: 0;` and `text-overflow: ellipsis;` on `.search-input` and `text-overflow: ellipsis;` on `.search-input::placeholder`.
2. Run `python scripts/verify_search_placeholder_polish.py` and confirm 100% PASS.
3. Run `python verify_implementation.py` and the full `scripts/verify_*.py` suite to verify zero regressions.
4. Commit locally without `git push`.
