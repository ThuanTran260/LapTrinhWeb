# Remove Top-Bar Links Across All Storefront Pages Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the right-side `.top-links` navigation block (e.g., `Tiếp Tục Mua Sắm`, `Giao 2H Hoả Tốc`, `Lịch Sử Đặt Hàng`, `Tài Khoản`, `Đăng Nhập`, `Quay Lại Cửa Hàng`, `Quay Lại Giỏ Hàng`, `Lịch Sử Đơn Hàng`, `Hỗ Trợ 24/7`, `Giỏ Hàng`, `Trang Chủ`) from `.top-bar` on all 14 storefront HTML pages, clean up unused `.top-links` CSS rules, and update/add automated verification scripts.

**Architecture:** Every storefront page (`index.html` + 13 `pages/*.html`) preserves its `.top-bar` container and left-aligned `.announcement-text` banner (`ENERGY10`, `ĐƠN HÀNG HỎA TỐC`, `ĐƠN HÀNG ĐỦ ĐIỀU KIỆN`, or `KẾT NỐI BẢO MẬT`), while dropping `<div class="top-links">...</div>`. Dead `.top-links` CSS rules are removed from `css/style.css` while preserving `.top-bar`, `.top-bar .container`, and `.announcement-text` rules. Affected verification scripts are updated and a dedicated cross-page verification script `scripts/verify_no_topbar_links.py` enforces zero `.top-links` regressions across all 14 storefront pages.

**Tech Stack:** Static HTML5, Vanilla CSS3, Python 3 verification scripts.

## Global Constraints

- Preserve `<div class="top-bar"><div class="container"><div class="announcement-text">...</div></div></div>` on all 14 storefront pages (`index.html` and all 13 `pages/*.html`) with `.announcement-text` remaining left-aligned and its content unchanged (including `ENERGY10` `.coupon-badge` where present).
- Do NOT remove or alter `<header class="header">`, `.header-actions` (`Đơn Hàng`, `Tài Khoản`, `Giỏ Hàng`), `.breadcrumb`, or `<footer class="footer">` links.
- Remove `<div class="top-links">...</div>` and all its child links from all 14 storefront pages; ensure zero `.top-links` elements or `.top-links` CSS rules remain in `index.html`, `pages/*.html`, and `css/style.css`.
- Never run `git push`; keep all commits local on `main`.

---

### Task 1: Remove `.top-links` from `index.html` and Core Storefront Subpages

**Files:**
- Modify: `index.html:25-30`
- Modify: `pages/account.html:20-25`
- Modify: `pages/cart.html:21-26`
- Modify: `pages/login.html:21-26`
- Modify: `pages/order-detail.html:67-72`
- Modify: `pages/order-success.html:22-27`
- Modify: `pages/orders.html:21-27`
- Modify: `pages/payment-gateway.html:22-26`
- Modify: `pages/search-results.html:25-30`

- [ ] **Step 1:** In each of the 9 HTML files listed above, remove the `<div class="top-links">...</div>` block inside `<div class="top-bar"><div class="container">...</div></div>` while keeping `<div class="announcement-text">...</div>` untouched.
- [ ] **Step 2:** Verify with `git grep -n "top-links" -- index.html pages/account.html pages/cart.html pages/login.html pages/order-detail.html pages/order-success.html pages/orders.html pages/payment-gateway.html pages/search-results.html` that zero matches remain, and verify `.announcement-text` + `.top-bar` remain present in all 9 files.
- [ ] **Step 3:** Commit changes locally with message `feat(topbar): remove .top-links from index and core storefront pages`.

---

### Task 2: Remove `.top-links` from Product Detail Pages and Clean Unused CSS

**Files:**
- Modify: `pages/product-detail.html:21-26`
- Modify: `pages/product-detail-redbull.html:21-26`
- Modify: `pages/product-detail-redbull-lonvua.html:22-26`
- Modify: `pages/product-detail-redbull-thai.html:22-26`
- Modify: `pages/product-detail-sting.html:22-27`
- Modify: `css/style.css:178-200` and `css/style.css:3845`

- [ ] **Step 1:** Remove the `<div class="top-links">...</div>` block from all 5 product detail pages while preserving `<div class="announcement-text">...</div>` and `.top-bar`.
- [ ] **Step 2:** In `css/style.css`, remove the unused `.top-links` and `.top-links a:hover` rules (lines 178-185, lines 195-199 inside `@media (min-width: 992px)`, and line 3845 inside `@media (max-width: 640px)`), leaving `.top-bar`, `.top-bar .container`, `.announcement-text`, and `.coupon-badge` intact.
- [ ] **Step 3:** Verify with `git grep -n "top-links" -- index.html pages/ css/` that zero matches remain across all HTML and CSS files, and run `python scripts/verify_topbar_and_discount_badge.py` to confirm announcement banner and discount badge checks still pass.
- [ ] **Step 4:** Commit changes locally with message `refactor(topbar): remove .top-links from product detail pages and css`.

---

### Task 3: Update Affected Verification Scripts and Add `scripts/verify_no_topbar_links.py`

**Files:**
- Modify: `scripts/verify_header_top_and_account_breadcrumb.py:17-53`
- Modify: `scripts/verify_login_header_sync.py:38-50`
- Modify: `scripts/verify_order_success_header_sync.py:27-39`
- Create: `scripts/verify_no_topbar_links.py`

- [ ] **Step 1:** Update `scripts/verify_header_top_and_account_breadcrumb.py` so check #1 verifies `pages/orders.html` has `.top-bar` with `.announcement-text` and NO `.top-links` (nor `Tiếp Tục Mua Sắm`, `Giao 2H Hoả Tốc`), and check #4 verifies `.top-bar .container` has `flex-wrap: nowrap` on desktop without requiring `.top-links` in CSS.
- [ ] **Step 2:** Update `scripts/verify_login_header_sync.py` (lines 38-50) and `scripts/verify_order_success_header_sync.py` (lines 27-39) so `.top-bar` verification checks for `ENERGY10`, `.coupon-badge`, and the absence of `.top-links` instead of requiring `.top-links` hrefs inside `.top-bar`.
- [ ] **Step 3:** Create `scripts/verify_no_topbar_links.py` that inspects `index.html`, all 13 `pages/*.html`, and `css/style.css` to assert: (a) every storefront page retains `.top-bar` and `.announcement-text`, (b) zero storefront pages contain `class="top-links"` or any top-bar link buttons (`Tiếp Tục Mua Sắm`, `Giao 2H Hoả Tốc`, `Quay Lại Cửa Hàng`, `Quay Lại Giỏ Hàng`, `Hỗ Trợ 24/7` inside `.top-bar`), and (c) `css/style.css` contains no `.top-links` rules while retaining `.top-bar` and `.announcement-text`.
- [ ] **Step 4:** Run `python scripts/verify_no_topbar_links.py`, `python scripts/verify_header_top_and_account_breadcrumb.py`, `python scripts/verify_login_header_sync.py`, `python scripts/verify_order_success_header_sync.py`, `python scripts/verify_topbar_and_discount_badge.py`, `python scripts/verify_header_footer_pagination.py`, `python scripts/verify_rubric_coverage.py`, and `python scripts/verify_pages_deploy_ready.py`, confirming all exit 0.
- [ ] **Step 5:** Commit changes locally with message `test(topbar): verify .top-links removal across all storefront pages`.
