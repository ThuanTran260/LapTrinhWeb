# Subpage Navigation Drawer Sync & Routing Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Synchronize `<nav class="nav-bar">` across all 6 `pages/*.html` storefront subpages (`product-detail*.html` + `search-results.html`) to match `index.html`'s `Trang chủ` + right-sliding `Nhãn hàng` drawer, fix subpage routing in `scrollToDashboardTop` and `handleNavBrandClick`, and expand verification coverage in `scripts/verify_dashboard_nav_drawer.py`.

**Architecture:** All 6 storefront subpages that include `<nav class="nav-bar">` adopt `#nav-home-btn` (`href="../index.html"`) and `.nav-brand-group` (`button#nav-brand-toggle` + `#nav-brand-drawer` with `href="../index.html#monster-products"`, `../index.html#redbull-products`, `../index.html#sting-products`). `js/app.js` unifies nav active-state syncing and root resolution so clicking `Trang chủ` on a subpage returns to `../index.html` while clicking it on `index.html` smooth-scrolls to top, and delegated/direct brand clicks parse `#<brand>-products` hashes cleanly from relative `../index.html#...` hrefs. All 4 tasks edit disjoint files.

**Tech Stack:** Static HTML5, Vanilla CSS3, Vanilla JS, Python 3 + Node.js (`vm`) verification scripts.

## Global Constraints

- Keep `<ul class="nav-menu">...</ul>` wrapper and `scrollToDashboardTop(event, this)` / `toggleBrandDrawer(this)` / `handleNavBrandClick(event, this, '...-products')` signatures intact so `verify_implementation.py`, `verify_header_footer_pagination.py`, and `verify_ui_fixes_and_combo_removal.py` stay green.
- Preserve per-page `.active` brand state inside `#nav-brand-drawer` for product pages (`Monster` on `pages/product-detail.html`; `Redbull` on `pages/product-detail-redbull.html`, `pages/product-detail-redbull-thai.html`, `pages/product-detail-redbull-lonvua.html`; `Sting` on `pages/product-detail-sting.html`) and leave NO brand highlighted on `pages/search-results.html`.
- Never execute `git push`; keep all commits local.

---

### Task 1: Sync `<nav class="nav-bar">` in `product-detail.html`, `product-detail-redbull.html`, and `product-detail-redbull-thai.html`

**Files:**
- Modify: `pages/product-detail.html:158-166`
- Modify: `pages/product-detail-redbull.html:158-166`
- Modify: `pages/product-detail-redbull-thai.html:86-94`

- [ ] **Step 1: Replace legacy 3-link `.nav-menu` in `pages/product-detail.html:158-166` (keep `Monster` `.active`)**

Replace `<nav class="nav-bar">...</nav>` with:

```html
    <nav class="nav-bar">
      <div class="container nav-container">
        <ul class="nav-menu">
          <li>
            <a href="../index.html" id="nav-home-btn" class="nav-link nav-home-link" onclick="return scrollToDashboardTop(event, this);">
              <i class="fas fa-home" style="color: var(--primary);"></i> Trang chủ
            </a>
          </li>
          <li class="nav-brand-group">
            <button type="button" id="nav-brand-toggle" class="nav-link nav-brand-toggle-btn" aria-expanded="false" aria-controls="nav-brand-drawer" onclick="toggleBrandDrawer(this)">
              <i class="fas fa-tags" style="color: var(--secondary);"></i> Nhãn hàng
              <i class="fas fa-chevron-right nav-brand-chevron" aria-hidden="true"></i>
            </button>
            <div id="nav-brand-drawer" class="nav-brand-drawer" aria-hidden="true">
              <a href="../index.html#monster-products" class="nav-link nav-brand-item active" onclick="handleNavBrandClick(event, this, 'monster-products')"><i class="fas fa-bolt" style="color: var(--primary);"></i> Monster</a>
              <a href="../index.html#redbull-products" class="nav-link nav-brand-item" onclick="handleNavBrandClick(event, this, 'redbull-products')"><i class="fas fa-fire" style="color: var(--secondary);"></i> Redbull</a>
              <a href="../index.html#sting-products" class="nav-link nav-brand-item" onclick="handleNavBrandClick(event, this, 'sting-products')"><i class="fas fa-bolt" style="color: #FF0055;"></i> Sting</a>
            </div>
          </li>
        </ul>
      </div>
    </nav>
```

- [ ] **Step 2: Replace legacy 3-link `.nav-menu` in `pages/product-detail-redbull.html:158-166` (keep `Redbull` `.active`)**
- [ ] **Step 3: Replace legacy 3-link `.nav-menu` in `pages/product-detail-redbull-thai.html:86-94` (keep `Redbull` `.active`)**
- [ ] **Step 4: Run `python verify_implementation.py` to confirm existing checks on `product-detail.html` pass.**

---

### Task 2: Sync `<nav class="nav-bar">` in `product-detail-redbull-lonvua.html`, `product-detail-sting.html`, and `search-results.html`

**Files:**
- Modify: `pages/product-detail-redbull-lonvua.html:86-94`
- Modify: `pages/product-detail-sting.html:159-167`
- Modify: `pages/search-results.html:177-185`

- [ ] **Step 1: Replace legacy 3-link `.nav-menu` in `pages/product-detail-redbull-lonvua.html:86-94` (keep `Redbull` `.active`)**
- [ ] **Step 2: Replace legacy 3-link `.nav-menu` in `pages/product-detail-sting.html:159-167` (keep `Sting` `.active`)**
- [ ] **Step 3: Replace legacy 3-link `.nav-menu` in `pages/search-results.html:177-185` (with NO brand `.active` since search results are multi-brand)**
- [ ] **Step 4: Run `python scripts/verify_ui_fixes_and_combo_removal.py; python scripts/verify_search_features.py` to confirm green status.**

---

### Task 3: Fix Subpage Routing & Consolidate Nav Helpers in `js/app.js` + Compact Nav Gap in `css/style.css`

**Files:**
- Modify: `js/app.js:3235-3335`
- Modify: `css/style.css:3801-3809`

- [ ] **Step 1: Extract `resolveNavRoot()` and `syncDashboardNavActiveState(activeTargetId, homeActive)` in `js/app.js`**

- `resolveNavRoot()` returns `window.SITE_ROOT` if set, otherwise `SITE_ROOT` (when resolved beyond `'./'`), otherwise `'../'`.
- `syncDashboardNavActiveState(activeTargetId, homeActive)` unifies `.nav-menu .nav-link[href*="-products"], .quick-brand-nav .quick-brand-btn` and `#nav-home-btn` `.active` class toggling across `changeDashboardPage`, `handleNavBrandClick`, and `scrollToDashboardTop`.

- [ ] **Step 2: Fix `handleNavBrandClick` hash parsing (`href.indexOf('#')`) and `scrollToDashboardTop` subpage navigation in `js/app.js`**

- In `handleNavBrandClick`, when `targetId` is omitted and `href` contains `'#'` (such as `'#monster-products'` OR `'../index.html#monster-products'`), extract `href.slice(hashIdx + 1)` cleanly so `window.location.href` redirects to `resolveNavRoot() + 'index.html#' + targetId`.
- In `scrollToDashboardTop`, check `document.getElementById('monster-products')`; if present (dashboard), smooth-scroll to top and call `syncDashboardNavActiveState(null, true)`; if absent (subpage), navigate to `resolveNavRoot() + 'index.html'`.

- [ ] **Step 3: Add `.nav-brand-group, .nav-brand-drawer { gap: 5px; }` inside `@media (max-width: 1200px) and (min-width: 769px)` (`css/style.css:3801-3809`)**
- [ ] **Step 4: Run `node --check js/app.js; python scripts/verify_header_footer_pagination.py`**

---

### Task 4: Expand `scripts/verify_dashboard_nav_drawer.py` to Cover All 6 Subpages & Subpage Runtime Routing

**Files:**
- Modify: `scripts/verify_dashboard_nav_drawer.py`

- [ ] **Step 1: Generalize `verify_index_nav_html` -> `verify_nav_drawer_html(html, filename, expected_home_href, expected_brand_prefix, expected_active_brand)` and check `index.html` plus all 6 `pages/*.html` subpages:**
  - `index.html` (`#top`, `#`, active `monster-products`)
  - `pages/product-detail.html` (`../index.html`, `../index.html#`, active `monster-products`)
  - `pages/product-detail-redbull.html` (`../index.html`, `../index.html#`, active `redbull-products`)
  - `pages/product-detail-redbull-thai.html` (`../index.html`, `../index.html#`, active `redbull-products`)
  - `pages/product-detail-redbull-lonvua.html` (`../index.html`, `../index.html#`, active `redbull-products`)
  - `pages/product-detail-sting.html` (`../index.html`, `../index.html#`, active `sting-products`)
  - `pages/search-results.html` (`../index.html`, `../index.html#`, active `None`)
- [ ] **Step 2: Add Compact Nav CSS check (`.nav-brand-group` / `.nav-brand-drawer` inside `max-width: 1200px` media query)**
- [ ] **Step 3: Add Node.js subpage runtime checks inside `verify_dashboard_nav_drawer.py` (when `#monster-products` is missing):**
  - `scrollToDashboardTop(e, homeBtn)` navigates `window.location.href` to `'../index.html'`.
  - `handleNavBrandClick(e, redbullSubLink)` with `href="../index.html#redbull-products"` and no explicit `targetId` navigates `window.location.href` to `'../index.html#redbull-products'` cleanly.
- [ ] **Step 4: Run `python scripts/verify_dashboard_nav_drawer.py` and full verification suite.**
