# Order Success Header Sync & Dashboard Collapsible Nav Drawer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Synchronize `pages/order-success.html`'s top bar, search box (with 5-item dropdown + `#modal-adv-search`), and 3 header action buttons with `index.html` / `pages/account.html`, and upgrade `index.html`'s `<nav class="nav-bar">` with a `Trang chủ` scroll-to-top link plus a collapsible `Nhãn hàng` toggle that slides `Monster`, `Redbull`, and `Sting` out to the right.

**Architecture:** `pages/order-success.html` adopts the canonical subpage storefront header layout (`../` relative paths, no `.nav-bar` since it uses `.breadcrumb`, matching `pages/account.html` and `pages/orders.html`). In `index.html`, `<ul class="nav-menu">` houses `#nav-home-btn` alongside `.nav-brand-group` (`button#nav-brand-toggle` + `.nav-brand-drawer#nav-brand-drawer`) so CSS `max-width`/`transform: translateX` transitions slide the 3 brand anchors out to the right while preserving their exact `handleNavBrandClick(event, this, '...-products')` contracts. All 4 tasks edit disjoint files.

**Tech Stack:** Static HTML5, Vanilla CSS3, Vanilla JS, Python 3 + Node.js (`vm`) verification scripts.

## Global Constraints

- Keep `pages/order-success.html` `<main>` (`Đóng thùng chống sốc 7 lon`, `CHI TIẾT ĐƠN HÀNG (7 LON)`, In hóa đơn điện tử toast) and `<footer>` untouched.
- In `pages/order-success.html`, `.search-static-list` must contain 5 `.search-static-item` links using `../assets/images/...` paths, including `Monster Energy Ultra White 355ml` (Item 4) and `Sting Vàng Sleek 330ml` (`../assets/images/sting/sting-gold.webp` linking to `product-detail-sting.html` at Item 5).
- Preserve `<ul class="nav-menu">...</ul>` wrapper and exact `handleNavBrandClick(event, this, 'monster-products' | 'redbull-products' | 'sting-products')` attributes inside `index.html` so `verify_implementation.py`, `verify_header_footer_pagination.py`, and `verify_ui_fixes_and_combo_removal.py` stay 100% green.
- Never execute `git push`; keep all commits local.

---

### Task 1: Sync Header, Top Bar & Advanced Search Modal in `pages/order-success.html`

**Files:**
- Modify: `pages/order-success.html:15-56`, `pages/order-success.html:300-303`

- [ ] **Step 1: Replace legacy top-bar and simplified header (`pages/order-success.html:15-55`) with canonical subpage top-bar & header**

Replace lines 15-55 of `pages/order-success.html` with the synchronized `.top-bar` (`ENERGY10`, 4 `.top-links`), Logo **ENERGYBOOST**, `.search-box` (`#search-dropdown-menu` with 5 hot products incl. `Monster Energy Ultra White 355ml` and `Sting Vàng Sleek 330ml`), and 3-button `.header-actions` (`orders.html`, `account.html` with `#header-account-link` / `#header-account-value`, `cart.html` with badge `7` and `216.000đ`).

- [ ] **Step 2: Insert `#modal-adv-search` before `<div id="toast-container">` (`pages/order-success.html:301`)**

Add the canonical `#modal-adv-search` modal block (matching `pages/account.html:354-409`) directly above `<div id="toast-container" class="toast-container"></div>`.

- [ ] **Step 3: Run existing checks covering `pages/order-success.html` & search dropdowns**

Run:
`python verify_implementation.py; python scripts/verify_cart_sync.py; python scripts/verify_admin_features_update.py; python scripts/verify_footer_sync.py; python scripts/verify_search_dropdown_hover_stability.py`
Expected: all exit 0.

---

### Task 2: Update `index.html` `.nav-bar` & Add Right-Sliding Drawer CSS in `css/style.css`

**Files:**
- Modify: `index.html:184-194`
- Modify: `css/style.css:403-456`

- [ ] **Step 1: Update `<ul class="nav-menu">` in `index.html:184-194`**

```html
    <!-- Navigation Bar -->
    <nav class="nav-bar">
      <div class="container nav-container">
        <ul class="nav-menu">
          <li>
            <a href="#top" id="nav-home-btn" class="nav-link nav-home-link" onclick="return scrollToDashboardTop(event, this);">
              <i class="fas fa-home" style="color: var(--primary);"></i> Trang chủ
            </a>
          </li>
          <li class="nav-brand-group">
            <button type="button" id="nav-brand-toggle" class="nav-link nav-brand-toggle-btn" aria-expanded="false" aria-controls="nav-brand-drawer" onclick="toggleBrandDrawer(this)">
              <i class="fas fa-tags" style="color: var(--secondary);"></i> Nhãn hàng
              <i class="fas fa-chevron-right nav-brand-chevron" aria-hidden="true"></i>
            </button>
            <div id="nav-brand-drawer" class="nav-brand-drawer" aria-hidden="true">
              <a href="#monster-products" class="nav-link nav-brand-item active" onclick="handleNavBrandClick(event, this, 'monster-products')"><i class="fas fa-bolt" style="color: var(--primary);"></i> Monster</a>
              <a href="#redbull-products" class="nav-link nav-brand-item" onclick="handleNavBrandClick(event, this, 'redbull-products')"><i class="fas fa-fire" style="color: var(--secondary);"></i> Redbull</a>
              <a href="#sting-products" class="nav-link nav-brand-item" onclick="handleNavBrandClick(event, this, 'sting-products')"><i class="fas fa-bolt" style="color: #FF0055;"></i> Sting</a>
            </div>
          </li>
        </ul>
      </div>
    </nav>
```

- [ ] **Step 2: Add `.nav-brand-group`, `.nav-brand-toggle-btn`, `.nav-brand-chevron`, and `.nav-brand-drawer` slide transitions after `.nav-link:focus-visible` (`css/style.css:454`)**

```css
.nav-menu {
  align-items: center;
}

.nav-brand-group {
  display: flex;
  align-items: center;
  gap: 6px;
}

.nav-brand-toggle-btn {
  background: transparent;
  border: none;
  font-family: inherit;
}

.nav-brand-toggle-btn.is-open {
  color: #FFF;
  background: rgba(0, 230, 118, 0.12);
}

.nav-brand-chevron {
  font-size: 0.72rem;
  transition: transform 0.28s cubic-bezier(0.22, 1, 0.36, 1), color 0.2s ease;
}

.nav-brand-toggle-btn.is-open .nav-brand-chevron {
  transform: rotate(180deg);
  color: var(--primary);
}

.nav-brand-drawer {
  display: flex;
  align-items: center;
  gap: 8px;
  max-width: 0;
  opacity: 0;
  overflow: hidden;
  pointer-events: none;
  transform: translateX(-14px);
  transition:
    max-width 0.34s cubic-bezier(0.22, 1, 0.36, 1),
    opacity 0.24s ease,
    transform 0.34s cubic-bezier(0.22, 1, 0.36, 1);
}

.nav-brand-drawer.is-open {
  max-width: 460px;
  opacity: 1;
  pointer-events: auto;
  transform: translateX(0);
}
```

- [ ] **Step 3: Run navbar CSS & HTML regression checks**

Run:
`python verify_implementation.py; python scripts/verify_header_footer_pagination.py; python scripts/verify_ui_fixes_and_combo_removal.py`
Expected: all exit 0.

---

### Task 3: Add `scrollToDashboardTop`, `toggleBrandDrawer`, and Clean Selector Scoping in `js/app.js`

**Files:**
- Modify: `js/app.js:3235-3366`

- [ ] **Step 1: Scope `changeDashboardPage` and `handleNavBrandClick` active selectors to `.nav-menu .nav-link[href*="-products"]`**

Update lines `3236` and `3292` so `Trang chủ` and `Nhãn hàng` toggle buttons are never mistakenly highlighted when switching pagination pages or clicking brand pills, and clear `#nav-home-btn` `.active` when a brand is activated.

- [ ] **Step 2: Implement `scrollToDashboardTop(e, link)` and `toggleBrandDrawer(btn)` cleanly**

```javascript
function scrollToDashboardTop(e, link) {
  if (e) {
    if (typeof e.preventDefault === 'function') e.preventDefault();
    if (typeof e.stopPropagation === 'function') e.stopPropagation();
  }
  if (typeof window !== 'undefined' && typeof window.scrollTo === 'function') {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
  if (typeof document !== 'undefined') {
    document.querySelectorAll('.nav-menu .nav-link[href*="-products"]').forEach(item => {
      item.classList.remove('active');
    });
    const homeBtn = link || document.getElementById('nav-home-btn');
    if (homeBtn && homeBtn.classList) homeBtn.classList.add('active');
  }
  return false;
}

function toggleBrandDrawer(btn) {
  const toggleBtn = btn || document.getElementById('nav-brand-toggle');
  const drawer = document.getElementById('nav-brand-drawer');
  if (!drawer) return false;
  const isOpen = drawer.classList.toggle('is-open');
  drawer.setAttribute('aria-hidden', isOpen ? 'false' : 'true');
  if (toggleBtn && toggleBtn.classList) {
    toggleBtn.classList.toggle('is-open', isOpen);
    toggleBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  }
  return isOpen;
}
```

- [ ] **Step 3: Narrow delegated click handler (`js/app.js:3359`) to `.nav-menu .nav-link[href*="-products"], .quick-brand-nav .quick-brand-btn` and export `window.scrollToDashboardTop` + `window.toggleBrandDrawer`**

- [ ] **Step 4: Syntax-check & run existing JS navbar checks**

Run:
`node --check js/app.js; python scripts/verify_header_footer_pagination.py`
Expected: both exit 0.

---

### Task 4: Create Automated Verification Scripts for `order-success.html` Header & Collapsible Nav Drawer

**Files:**
- Create: `scripts/verify_order_success_header_sync.py`
- Create: `scripts/verify_dashboard_nav_drawer.py`

- [ ] **Step 1: Write `scripts/verify_order_success_header_sync.py`** verifying `.top-bar` (`ENERGY10`), `.search-box`, 5 `.search-static-item` links (`Monster Energy Ultra White 355ml`, `sting-gold.webp`), 3 `.header-actions` (`orders.html`, `account.html`, `cart.html` badge `7`), `#modal-adv-search`, and preserved `7 LON` order summary + toast print button.

- [ ] **Step 2: Write `scripts/verify_dashboard_nav_drawer.py`** verifying `index.html` `#nav-home-btn`, `#nav-brand-toggle`, `#nav-brand-drawer` containing all 3 brand anchors (`Monster`, `Redbull`, `Sting`), `css/style.css` slide transitions (`max-width: 0`, `translateX(-14px)`, `.nav-brand-drawer.is-open`), and Node.js `vm` runtime tests exercising `toggleBrandDrawer()`, `scrollToDashboardTop()`, `handleNavBrandClick()`, and `changeDashboardPage()` active-class scoping.

- [ ] **Step 3: Run full suite**

Run:
`python scripts/verify_order_success_header_sync.py; python scripts/verify_dashboard_nav_drawer.py; python verify_implementation.py`
Expected: all exit 0.
