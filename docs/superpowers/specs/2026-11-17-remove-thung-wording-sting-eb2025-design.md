# Design Spec: Update Order #EB-2025 Wording to "24 Lon" (Remove "Thùng")

**Date:** 2026-11-17  
**Status:** In Review  
**Author:** AI Assistant  

---

## 1. Problem Statement & User Intent
In the previous update, order `#EB-2025` was changed to:
`1x Thùng 24 Lon Sting Dâu Tây Đỏ 330ml` (in `pages/orders.html`) and `1x Thùng 24 Lon Sting Dâu Tây Đỏ Sleek 330ml` (in `pages/account.html` and `js/app.js`).

The user requested:
> "1x Thùng  
> không cần ghi thùng chỉ cần là 24 lon"

The user wants to remove the word "Thùng" and the prefix "1x", simplifying the product display text to simply **"24 Lon"**:
- From: `1x Thùng 24 Lon Sting Dâu Tây Đỏ 330ml`
- To: `24 Lon Sting Dâu Tây Đỏ 330ml`

---

## 2. Proposed Scope of Changes

### 2.1 Orders Table (`pages/orders.html`)
- Title: `<strong>24 Lon Sting Dâu Tây Đỏ 330ml</strong>`
- Reorder toast: `showToast('Đã thêm lại 24 lon Sting Dâu vào giỏ hàng!', 'success')`

### 2.2 Account Dashboard (`pages/account.html`)
- Card title: `<div>24 Lon Sting Dâu Tây Đỏ Sleek 330ml</div>`
- Card comment: `<!-- Order Card 2: 24 Lon Sting Dâu -->`
- Reorder toast: `showToast('Đã thêm lại 24 lon Sting Dâu vào giỏ!', 'success')`

### 2.3 Mock Database (`js/app.js`)
- `MOCK_ORDER_DATABASE['EB-2025']`:
  - Item name: `'24 Lon Sting Dâu Tây Đỏ Sleek 330ml'`
  - Order notes: `'24 lon Sting Dâu Tây Đỏ chính hãng PepsiCo'`

### 2.4 Test Suite Updates
- Update `scripts/verify_orders_shipping_reorder_and_sting_eb2025.py`:
  - Assert that `#EB-2025` title is `'24 Lon Sting Dâu Tây Đỏ 330ml'`.
  - Assert that `#EB-2025` does NOT contain `"Thùng"`.
  - Assert that reorder toast says `'Đã thêm lại 24 lon Sting Dâu vào giỏ hàng!'`.
  - Assert that `account.html` and `js/app.js` are updated accordingly.

---

## 3. Verification Strategy
1. Run `python scripts/verify_orders_shipping_reorder_and_sting_eb2025.py` to confirm 100% PASS with new wording.
2. Run all other 11 regression test suites to guarantee zero regression.
3. Commit locally without `git push`.
