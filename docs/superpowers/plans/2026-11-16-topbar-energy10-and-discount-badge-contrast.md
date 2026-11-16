# Synchronize Top-Bar ENERGY10 Announcement & Enhance Discount Badge Contrast Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Synchronize the header top-bar announcement banner across product detail pages (especially `product-detail-sting.html`) with `index.html` to promote the `ENERGY10` discount code, and enhance readability of discount badges (`.badge-discount`) with bold black text on an electric mint/neon green background.

**Architecture:** Update `.badge-discount` in `css/style.css` to achieve high contrast (15.6:1 WCAG AAA), synchronize `.announcement-text` across all 5 product detail pages to match `index.html`, and construct an automated verification script `scripts/verify_topbar_and_discount_badge.py` to validate consistency and prevent regressions.

**Tech Stack:** HTML5, CSS3, Vanilla JavaScript, Python 3 (verification test scripts).

## Global Constraints
- Pure static HTML/CSS/JS without bundlers or server runtime.
- Maintain existing visual harmony of the Kinetic Volt design system.
- Strict Git Safety: No automated `git push`. All commits remain strictly local.
- Ensure all 7 existing regression test suites continue to pass 100%.

---

### Task 1: Create Automated Verification Script for Top-Bar & Discount Badge

**Files:**
- Create: `scripts/verify_topbar_and_discount_badge.py`

**Interfaces:**
- Produces: Test runner script reporting pass/fail for `.badge-discount` contrast rules and top-bar announcement text matching `index.html`.

- [ ] **Step 1: Write the failing verification script**

Create `scripts/verify_topbar_and_discount_badge.py` asserting:
1. `css/style.css`: `.badge-discount` contains `color: #000;` (or `black`), `font-weight: 900;`, `box-shadow: 0 0 10px rgba(0, 255, 102, 0.4);`, and does not have `color: #FFF;`.
2. `pages/product-detail-sting.html`: announcement text matches `ENERGY BOOST: Nhập mã <span class="coupon-badge" onclick="showToast('Đã chép mã giảm giá ENERGY10!', 'info')">ENERGY10</span>`.
3. `pages/product-detail-redbull-thai.html`: announcement text contains `coupon-badge` and `ENERGY10`.
4. `pages/product-detail-redbull-lonvua.html`: announcement text contains `coupon-badge` and `ENERGY10`.
5. `pages/product-detail.html` & `pages/product-detail-redbull.html`: announcement text contains `coupon-badge` and `ENERGY10`.

- [ ] **Step 2: Run test to verify it fails**

Run: `python scripts/verify_topbar_and_discount_badge.py`  
Expected: FAIL (because styles still use `#FFF` and sting topbar still uses old hỏa tốc text).

---

### Task 2: Enhance Discount Badge Contrast in `css/style.css`

**Files:**
- Modify: `css/style.css:749-760`

**Interfaces:**
- Consumes: CSS custom variable `var(--secondary)` (#00FF66).
- Produces: Updated `.badge-discount` styling with `color: #000; font-weight: 900; box-shadow: 0 0 10px rgba(0, 255, 102, 0.4);`.

- [ ] **Step 1: Update `.badge-discount` in `css/style.css`**

Replace:
```css
.badge-discount {
  position: absolute;
  top: 12px;
  left: 12px;
  background: var(--secondary);
  color: #FFF;
  font-size: 0.75rem;
  font-weight: 800;
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  z-index: 5;
}
```
With:
```css
.badge-discount {
  position: absolute;
  top: 12px;
  left: 12px;
  background: var(--secondary);
  color: #000;
  font-size: 0.75rem;
  font-weight: 900;
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  z-index: 5;
  box-shadow: 0 0 10px rgba(0, 255, 102, 0.4);
}
```

- [ ] **Step 2: Run verification script to check discount badge assertions**

Run: `python scripts/verify_topbar_and_discount_badge.py`  
Expected: Discount badge assertions PASS; topbar assertions still failing.

---

### Task 3: Synchronize Top-Bar Announcement Across Product Detail Pages

**Files:**
- Modify: `pages/product-detail-sting.html:18-21`
- Modify: `pages/product-detail-redbull-thai.html:18-21`
- Modify: `pages/product-detail-redbull-lonvua.html:18-21`
- Modify: `pages/product-detail.html:17-20`
- Modify: `pages/product-detail-redbull.html:17-20`

**Interfaces:**
- Consumes: Standard top-bar announcement markup from `index.html:21-24`.
- Produces: Cohesive top-bar announcement banner with interactive `coupon-badge` element across all product detail pages.

- [ ] **Step 1: Update `pages/product-detail-sting.html`**

Replace lines 18-21:
```html
      <div class="announcement-text">
        <i class="fas fa-bolt"></i>
        <span>ENERGY BOOST: Nhập mã <span class="coupon-badge" onclick="showToast('Đã chép mã giảm giá ENERGY10!', 'info')">ENERGY10</span> giảm ngay 10% cho đơn hàng đầu tiên!</span>
      </div>
```

- [ ] **Step 2: Update remaining product detail pages**

Update `product-detail-redbull-thai.html`, `product-detail-redbull-lonvua.html`, `product-detail.html`, and `product-detail-redbull.html` to align identically with the standard announcement format.

- [ ] **Step 3: Run verification script to verify all tests pass**

Run: `python scripts/verify_topbar_and_discount_badge.py`  
Expected: All tests in `verify_topbar_and_discount_badge.py` PASS 100%.

---

### Task 4: Run Full Regression Suite, Code Review & Local Commit

**Files:**
- Test all: Run 8 test suites.
- Review: Dual subagent code review (Standards & Spec).
- Git: Local commit.

- [ ] **Step 1: Run entire regression test suite**

Run:
```powershell
python scripts/verify_topbar_and_discount_badge.py
python scripts/verify_admin_features_update.py
python scripts/verify_faq_edit_save_and_orders_link.py
python scripts/verify_implementation.py
python scripts/verify_price_formatting.py
python scripts/verify_footer_sync.py
python scripts/verify_sidebar_filter_sync.py
python scripts/verify_admin_kpi_brand_wording.py
```
Expected: 100% PASS on all suites.

- [ ] **Step 2: Execute dual code review**

Dispatch Standards Reviewer and Spec Reviewer subagents. Resolve any reported issues.

- [ ] **Step 3: Commit locally**

Commit with message:
```bash
git add css/style.css pages/product-detail*.html scripts/verify_topbar_and_discount_badge.py docs/superpowers/
git commit -m "fix(style): improve discount badge contrast and sync product detail topbar energy10 announcement"
```
Ensure NO `git push` is executed.
