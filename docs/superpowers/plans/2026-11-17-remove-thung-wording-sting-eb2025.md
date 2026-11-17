# Remove "Thùng" Wording from Order #EB-2025 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the word "Thùng" and "1x" from order #EB-2025 across `pages/orders.html`, `pages/account.html`, and `js/app.js`, replacing it with "24 Lon Sting Dâu Tây Đỏ 330ml".

**Architecture:** Update HTML strings and toast messages in `orders.html` and `account.html`, update `MOCK_ORDER_DATABASE` in `js/app.js`, update verification assertions in `scripts/verify_orders_shipping_reorder_and_sting_eb2025.py`, and run the regression test suite.

**Tech Stack:** Pure Static HTML5, Vanilla JavaScript, Python 3.

## Global Constraints
- Pure static HTML/CSS/JS frontend.
- Strictly local git commits. Never run `git push`.
- Maintain 100% PASS on all regression test suites.

---

### Task 1: Update Test Script Assertions for "24 Lon"

**Files:**
- Modify: `scripts/verify_orders_shipping_reorder_and_sting_eb2025.py:75-125`

- [x] **Step 1: Update assertions in verification script**
Update assertions to check for `24 Lon Sting Dâu Tây Đỏ` and assert that `"Thùng"` is not present in `#EB-2025`.

- [x] **Step 2: Run script to verify it fails**
Run: `python scripts/verify_orders_shipping_reorder_and_sting_eb2025.py`
Expected: FAIL (because HTML still contains "1x Thùng").

---

### Task 2: Update HTML & JS Files

**Files:**
- Modify: `pages/orders.html:245,255`
- Modify: `pages/account.html:243,255,263`
- Modify: `js/app.js:1385,1388`

- [x] **Step 1: Update `pages/orders.html`**
Change `<strong>1x Thùng 24 Lon Sting Dâu Tây Đỏ 330ml</strong>` to `<strong>24 Lon Sting Dâu Tây Đỏ 330ml</strong>`.
Change toast to `'Đã thêm lại 24 lon Sting Dâu vào giỏ hàng!'`.

- [x] **Step 2: Update `pages/account.html`**
Change `<div>1x Thùng 24 Lon Sting Dâu Tây Đỏ Sleek 330ml</div>` to `<div>24 Lon Sting Dâu Tây Đỏ Sleek 330ml</div>`.
Change toast to `'Đã thêm lại 24 lon Sting Dâu vào giỏ!'`.

- [x] **Step 3: Update `js/app.js`**
Update `name` to `'24 Lon Sting Dâu Tây Đỏ Sleek 330ml'` and `notes` to `'24 lon Sting Dâu Tây Đỏ chính hãng PepsiCo'`.

- [x] **Step 4: Run verification script**
Run: `python scripts/verify_orders_shipping_reorder_and_sting_eb2025.py`
Expected: PASS 100%.

---

### Task 3: Regression Verification & Local Commit

**Files:**
- Test all: Run regression test suites.
- Git: Local commit (no git push).

- [x] **Step 1: Run all test suites**
Run regression test suites and confirm 100% PASS.

- [x] **Step 2: Commit locally**
Commit with message:
`fix(orders): display '24 Lon' instead of '1x Thung' for order EB-2025`
Ensure NO `git push` is run.
