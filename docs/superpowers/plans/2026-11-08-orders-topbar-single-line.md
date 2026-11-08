# Orders Top Bar Single Line Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the orders page (`pages/orders.html`) top bar so that the announcement text and top navigation links render on the exact same single line without wrapping, identical to the dashboard (`index.html`).

**Architecture:** Remove redundant `Giỏ Hàng (7 lon)` from `.top-links` in `pages/orders.html` (retaining `title="Giỏ Hàng (7 lon)"` in header cart action button to preserve test parity), streamline desktop top-bar CSS with `flex-wrap: nowrap;` and optimized link gap (`14px`), and verify across all 15 test suites.

**Tech Stack:** Pure Static HTML5, CSS3 Flexbox, Python 3 (verification scripts).

## Global Constraints

- 100% Pure Static Website (no backend, no build tools).
- MUST retain `"Giỏ Hàng (7 lon)"` in `pages/orders.html` for compatibility with `scripts/verify_cart_sync.py`.
- STRICT RULE 1: Never run `git push` automatically.
- Planning Gate: Do not edit application source code before user proceeds.

---

### Task 1: Streamline `pages/orders.html` Top Bar Links & Cart Title

**Files:**
- Modify: `pages/orders.html:20-40`
- Test: `scripts/verify_header_top_and_account_breadcrumb.py`

**Interfaces:**
- Consumes: FontAwesome icons, `.top-bar`, `.top-links`, `.action-btn`.
- Produces: 5-link `.top-links` (`Tiếp Tục Mua Sắm`, `Giao 2H Hoả Tốc`, `Lịch Sử Đặt Hàng`, `Tài Khoản`, `Đăng Nhập`) and header cart action button with `title="Giỏ Hàng (7 lon)"`.

- [ ] **Step 1: Update verification test `scripts/verify_header_top_and_account_breadcrumb.py`**

Update the test to assert that `.top-links` contains the 5 streamlined links, does not have redundant cart link in `.top-links`, has `title="Giỏ Hàng (7 lon)"` on the main header cart button, and CSS specifies desktop single-line alignment.

```python
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

checks = []

def check(name, condition, details=""):
    checks.append((name, condition, details))
    mark = "PASS" if condition else "FAIL"
    print(f"[{mark}] {name} - {details}")

print("=== VERIFY ORDERS TOPBAR SINGLE LINE & ACCOUNT BREADCRUMB ===")

# 1. Check pages/orders.html top-links
orders_content = open("pages/orders.html", encoding="utf-8").read()
top_links_match = re.search(r'<div class="top-links">(.*?)</div>', orders_content, re.DOTALL)
check("orders.html has top-links", top_links_match is not None, "Found .top-links container")

if top_links_match:
    links_block = top_links_match.group(1)
    check("orders.html has Tiếp Tục Mua Sắm", 'Tiếp Tục Mua Sắm' in links_block and '../index.html' in links_block)
    check("orders.html has Giao 2H Hoả Tốc", 'Giao 2H Hoả Tốc' in links_block and '../index.html#features' in links_block)
    check("orders.html has Lịch Sử Đặt Hàng", 'Lịch Sử Đặt Hàng' in links_block and 'orders.html' in links_block)
    check("orders.html has Tài Khoản", 'Tài Khoản' in links_block and 'account.html' in links_block)
    check("orders.html has Đăng Nhập", 'Đăng Nhập' in links_block and 'login.html' in links_block)
    check("orders.html top-links has no redundant cart link", 'cart.html' not in links_block, "Cart link removed from top-links to fit 1 line")

# 2. Check orders.html retains 'Giỏ Hàng (7 lon)' for verify_cart_sync compatibility
check("orders.html retains Giỏ Hàng (7 lon)", 'Giỏ Hàng (7 lon)' in orders_content, "Retains 'Giỏ Hàng (7 lon)' in header action button")

# 3. Check pages/account.html breadcrumb and removal of brand nav
account_content = open("pages/account.html", encoding="utf-8").read()
check("account.html removes nav-bar", '<nav class="nav-bar">' not in account_content and 'handleNavBrandClick' not in account_content)
check("account.html has breadcrumb", '<div class="breadcrumb">' in account_content)
check("account.html breadcrumb structure", 'Trang chủ' in account_content and 'Thành viên' in account_content)

# 4. Check css/style.css top-bar single line styling on desktop
css_content = open("css/style.css", encoding="utf-8").read()
check("style.css has top-bar nowrap on desktop", 'top-bar' in css_content and 'nowrap' in css_content)

failed = [c for c in checks if not c[1]]
print(f"\nResult: {len(checks) - len(failed)}/{len(checks)} passed.")
if failed:
    print(f"FAILED {len(failed)} checks.")
    sys.exit(1)
else:
    print("ALL CHECKS PASSED!")
    sys.exit(0)
```

- [ ] **Step 2: Update `pages/orders.html`**

Update `.top-links` to 5 links:
```html
      <div class="top-links">
        <a href="../index.html"><i class="fas fa-arrow-left"></i> Tiếp Tục Mua Sắm</a>
        <a href="../index.html#features"><i class="fas fa-truck-fast"></i> Giao 2H Hoả Tốc</a>
        <a href="orders.html"><i class="fas fa-clock-rotate-left"></i> Lịch Sử Đặt Hàng</a>
        <a href="account.html"><i class="fas fa-user-circle"></i> Tài Khoản</a>
        <a href="login.html"><i class="fas fa-sign-in-alt"></i> Đăng Nhập</a>
      </div>
```

Update header Cart action button in `pages/orders.html`:
```html
          <!-- Cart Link -->
          <a href="cart.html" class="action-btn" title="Giỏ Hàng (7 lon)">
            <div class="action-icon-wrapper">
              <i class="fas fa-shopping-cart"></i>
              <span class="action-badge">7</span>
            </div>
            <div class="action-text">
              <span class="action-label">Giỏ hàng</span>
              <span class="action-value" style="color: var(--primary);">216.000đ</span>
            </div>
          </a>
```

- [ ] **Step 3: Commit Task 1**

```bash
git add pages/orders.html scripts/verify_header_top_and_account_breadcrumb.py
git commit -m "fix(orders): streamline top-bar links to 5 items and assign title to cart action"
```

---

### Task 2: CSS Enhancement for Single-Line Desktop Top Bar

**Files:**
- Modify: `css/style.css:120560-120600`
- Test: `scripts/verify_header_top_and_account_breadcrumb.py`

**Interfaces:**
- Consumes: `.top-bar`, `.container`, `.announcement-text`, `.top-links`.
- Produces: Robust desktop single-line rule with `flex-wrap: nowrap` and `gap: 14px`.

- [ ] **Step 1: Add desktop single-line rule in `css/style.css`**

Add rule under `.top-links`:
```css
@media (min-width: 992px) {
  .top-bar .container {
    flex-wrap: nowrap;
  }
  .announcement-text {
    white-space: nowrap;
    flex-shrink: 0;
  }
  .top-links {
    white-space: nowrap;
    gap: 14px;
    flex-shrink: 0;
  }
}
```

- [ ] **Step 2: Run verification script**

Run: `python scripts/verify_header_top_and_account_breadcrumb.py`
Expected: PASS (11/11 checks).

- [ ] **Step 3: Commit Task 2**

```bash
git add css/style.css
git commit -m "style(topbar): ensure desktop top-bar remains on single line without wrapping"
```

---

### Task 3: Complete Regression Testing

**Files:**
- Test: All 15 test suites
- Update: Walkthrough document `walkthrough.md`

- [ ] **Step 1: Run complete 15-suite test regression**

Run:
```powershell
python -c "
import subprocess
scripts = [
    'scripts/verify_header_top_and_account_breadcrumb.py',
    'scripts/verify_cart_sync.py',
    'scripts/verify_sidebar_filter_sync.py',
    'scripts/verify_discount_sync_and_clean_ward_labels.py',
    'scripts/verify_ward_commune_filter.py',
    'scripts/verify_search_features.py',
    'scripts/verify_ui_fixes_and_combo_removal.py',
    'scripts/verify_rubric_coverage.py',
    'scripts/verify_price_formatting.py',
    'scripts/verify_admin_order_links.py',
    'scripts/verify_order_detail_pages.py',
    'scripts/verify_field_sync_and_clean_image_labels.py',
    'verify_implementation.py',
    'scripts/verify_admin_monster_previews.py',
    'scripts/verify_unconstrained_add_user.py'
]
for s in scripts:
    res = subprocess.run(['python', s], capture_output=True, text=True, encoding='utf-8')
    assert res.returncode == 0, f'FAILED: {s}\n{res.stdout}\n{res.stderr}'
    print(f'[OK] {s}')
print('ALL 15 SUITES PASSED (100%)!')
"
```
Expected: PASS (100% across all 15 suites).

- [ ] **Step 2: Update Walkthrough document**

Document Section 29 in `walkthrough.md` with visual verification and commit.

- [ ] **Step 3: Commit Documentation**

```bash
git add walkthrough.md docs/superpowers/plans/
git commit -m "docs: record orders topbar single line fix in walkthrough and plans"
```
