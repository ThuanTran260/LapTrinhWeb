# Login & Registration Header + Footer Sync Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Synchronize the `.top-bar`, sticky `<header class="header">` (logo, 5-item search dropdown + `#modal-adv-search`, and 3 header action buttons), `.breadcrumb`, and 4-column `<footer class="footer">` on `pages/login.html` (covering both **Đăng nhập** and **Đăng ký** modes) with the rest of the storefront (`pages/account.html` / `pages/order-success.html`).

**Architecture:** `pages/login.html` adopts the storefront subpage header & footer layout (`../` relative paths, `.breadcrumb` per `verify_header_top_and_account_breadcrumb.py`), moves off `<body class="login-body-wrapper">` onto `<body>` + `<main class="login-page-main">` so full-width sticky header and 4-column footer stack cleanly, adds `#auth-breadcrumb-current` inside `.breadcrumb`, and dynamically syncs breadcrumb text inside `js/app.js`'s `switchAuthTab(mode)`. All 3 tasks edit disjoint files.

**Tech Stack:** Static HTML5, Vanilla CSS3, Vanilla JS, Python 3 + Node.js verification scripts.

## Global Constraints

- Preserve all existing auth elements inside `.login-card` (`#tab-login-btn`, `#tab-register-btn`, `#auth-card-title`, `#auth-card-desc`, `#form-login`, `#form-register`, all `#register-*` / `#login-*` inputs, `.back-home-link`) so `verify_rubric_coverage.py` and existing auth flows stay 100% intact.
- Keep `#search-dropdown-menu` consistent with the 5 canonical items (`../assets/images/...`, Item 4 `Monster Energy Ultra White 355ml`, Item 5 `Sting Vàng Sleek 330ml` -> `../assets/images/sting/sting-gold.webp` linking to `product-detail-sting.html`).
- Keep `<footer class="footer">` aligned with the 4-column canonical subpage footer (`ENERGYBOOST` info, `CÁC DÒNG SẢN PHẨM`, `HỆ THỐNG TRANG`, `NHẬN VOUCHER ƯU ĐÃI`, `.footer-bottom`).
- Never run `git push`; keep all commits local.

---

### Task 1: Add Synced Top Bar, Sticky Header, Breadcrumb, 4-Column Footer & `#modal-adv-search` to `pages/login.html`

**Files:**
- Modify: `pages/login.html:12-126`

- [ ] **Step 1: Replace `<body class="login-body-wrapper">` with `<body>` and insert the canonical subpage `.top-bar` (`ENERGY10`, 4 `.top-links`) + `<header class="header">` (Logo `ENERGYBOOST`, `.search-box` with 5-item `#search-dropdown-menu`, 3 `.header-actions` links: `orders.html`, `account.html` `#header-account-link`/`#header-account-value`, `cart.html` badge `7` / `216.000đ`) matching `pages/account.html` & `pages/order-success.html`.**
- [ ] **Step 2: Wrap `.login-card` inside `<main class="login-page-main"><div class="container">` with `<div class="breadcrumb"><a href="../index.html">Trang chủ</a><span>/</span><span id="auth-breadcrumb-current">Đăng nhập</span></div>` and centered `.login-card` (`margin: 0 auto;`).**
- [ ] **Step 3: Insert canonical 4-column `<footer class="footer">` (`pages/account.html:290-351`) after `</main>` and `#modal-adv-search` (`pages/account.html:354-409`) directly above `<div id="toast-container" class="toast-container"></div>`.**
- [ ] **Step 4: Run `python verify_implementation.py; python scripts/verify_rubric_coverage.py`.**

---

### Task 2: Add `.login-page-main` Layout CSS & Dynamic Auth Breadcrumb Switching

**Files:**
- Modify: `css/style.css:1414-1435`
- Modify: `js/app.js:2174-2198`

- [ ] **Step 1: In `css/style.css` right alongside `.login-body-wrapper`, add `.login-page-main` (`min-height: calc(100vh - 125px); padding: 24px 0 56px; background: radial-gradient(circle at center, #181B26 0%, #08090C 100%);`) while preserving `.login-body-wrapper` for compatibility.**
- [ ] **Step 2: In `js/app.js` (`switchAuthTab(mode)`), also update `#auth-breadcrumb-current` (`'Đăng ký'` when `mode === 'register'`, `'Đăng nhập'` otherwise) so toggling between Đăng nhập and Đăng ký keeps the page breadcrumb in sync.**
- [ ] **Step 3: Run `node --check js/app.js`.**

---

### Task 3: Add Automated Verification (`scripts/verify_login_header_sync.py`)

**Files:**
- Create: `scripts/verify_login_header_sync.py`

- [ ] **Step 1: Verify `pages/login.html` contains `.top-bar` (`ENERGY10`, 4 `.top-links`), `<header class="header">` (Logo, 5 `.search-static-item` links using `../assets/images/...` incl. Ultra White & Sting Vàng Sleek, 3 `.header-actions`), `<main class="login-page-main">`, `<div class="breadcrumb">` with `#auth-breadcrumb-current`, canonical 4-column `<footer class="footer">` (`CÁC DÒNG SẢN PHẨM`, `HỆ THỐNG TRANG`, `NHẬN VOUCHER ƯU ĐÃI`, `.footer-bottom`), `#modal-adv-search`, and all existing auth tabs/forms without `body.login-body-wrapper`.**
- [ ] **Step 2: Verify `css/style.css` defines `.login-page-main` and `js/app.js` updates `#auth-breadcrumb-current` in `switchAuthTab`.**
- [ ] **Step 3: Add Node.js runtime test invoking `switchAuthTab('register')` and `switchAuthTab('login')` cleanly.**
- [ ] **Step 4: Run `python scripts/verify_login_header_sync.py` and full verification suite (`FAILED=0`).**
