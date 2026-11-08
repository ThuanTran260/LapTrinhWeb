# Header Top Sync and Account Breadcrumb Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Synchronize the orders page (`pages/orders.html`) top-bar links with dashboard while retaining shopping navigation, and replace the redundant brand category navigation bar in the account page (`pages/account.html`) with a standard breadcrumb (`Trang chủ / Thành viên`).

**Architecture:** Pure static HTML5/CSS3 updates. Update `pages/orders.html` `.top-links` container to include the full set of 6 links according to Option 1; update `pages/account.html` by stripping the irrelevant `<nav class="nav-bar">` and prepending `<div class="breadcrumb">` inside `<main class="container account-page-section">`. Add automated regression test suite `scripts/verify_header_top_and_account_breadcrumb.py`.

**Tech Stack:** Pure Static HTML5, Vanilla JavaScript, CSS3, Python 3 (verification scripts).

## Global Constraints

- 100% Pure Static Website (no node servers, no backend API, no database).
- MUST retain `"Giỏ Hàng (7 lon)"` in `pages/orders.html` for compatibility with `scripts/verify_cart_sync.py`.
- STRICT RULE 1: Never run `git push` automatically.
- Planning Gate: Do not edit application source code before user proceeds.

---

### Task 1: Synchronize Top Bar Links in `pages/orders.html` (Option 1)

**Files:**
- Modify: `pages/orders.html:20-27`
- Test: `scripts/verify_header_top_and_account_breadcrumb.py`

**Interfaces:**
- Consumes: Existing CSS classes `.top-bar`, `.top-links`, FontAwesome icon classes (`fa-arrow-left`, `fa-truck-fast`, `fa-clock-rotate-left`, `fa-shopping-cart`, `fa-user-circle`, `fa-sign-in-alt`).
- Produces: Synced `.top-links` with 6 interactive anchor elements.

- [ ] **Step 1: Write verification test for orders top-bar and account breadcrumb**

Create `scripts/verify_header_top_and_account_breadcrumb.py` with failing assertions for the new links and breadcrumb.

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

print("=== VERIFY HEADER TOP SYNC & ACCOUNT BREADCRUMB ===")

# 1. Check pages/orders.html top-links
orders_content = open("pages/orders.html", encoding="utf-8").read()
top_links_match = re.search(r'<div class="top-links">(.*?)</div>', orders_content, re.DOTALL)
check("orders.html has top-links", top_links_match is not None, "Found .top-links container")

if top_links_match:
    links_block = top_links_match.group(1)
    check("orders.html has Tiếp Tục Mua Sắm", 'Tiếp Tục Mua Sắm' in links_block and '../index.html' in links_block)
    check("orders.html has Giao 2H Hoả Tốc", 'Giao 2H Hoả Tốc' in links_block and '../index.html#features' in links_block)
    check("orders.html has Lịch Sử Đặt Hàng", 'Lịch Sử Đặt Hàng' in links_block and 'orders.html' in links_block)
    check("orders.html has Giỏ Hàng (7 lon)", 'Giỏ Hàng (7 lon)' in links_block and 'cart.html' in links_block)
    check("orders.html has Tài Khoản", 'Tài Khoản' in links_block and 'account.html' in links_block)
    check("orders.html has Đăng Nhập", 'Đăng Nhập' in links_block and 'login.html' in links_block)

# 2. Check pages/account.html breadcrumb and removal of brand nav
account_content = open("pages/account.html", encoding="utf-8").read()
check("account.html removes nav-bar", '<nav class="nav-bar">' not in account_content and 'handleNavBrandClick' not in account_content)
check("account.html has breadcrumb", '<div class="breadcrumb">' in account_content)
check("account.html breadcrumb structure", 'Trang chủ' in account_content and 'Thành viên' in account_content)

failed = [c for c in checks if not c[1]]
print(f"\nResult: {len(checks) - len(failed)}/{len(checks)} passed.")
if failed:
    print(f"FAILED {len(failed)} checks.")
    sys.exit(1)
else:
    print("ALL CHECKS PASSED!")
    sys.exit(0)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python scripts/verify_header_top_and_account_breadcrumb.py`
Expected: FAIL (orders top links missing items, account still has nav-bar and missing breadcrumb).

- [ ] **Step 3: Update `pages/orders.html` top links**

Replace lines 21-25 in `pages/orders.html`:
```html
      <div class="top-links">
        <a href="../index.html"><i class="fas fa-arrow-left"></i> Tiếp Tục Mua Sắm</a>
        <a href="../index.html#features"><i class="fas fa-truck-fast"></i> Giao 2H Hoả Tốc</a>
        <a href="orders.html"><i class="fas fa-clock-rotate-left"></i> Lịch Sử Đặt Hàng</a>
        <a href="cart.html"><i class="fas fa-shopping-cart"></i> Giỏ Hàng (7 lon)</a>
        <a href="account.html"><i class="fas fa-user-circle"></i> Tài Khoản</a>
        <a href="login.html"><i class="fas fa-sign-in-alt"></i> Đăng Nhập</a>
      </div>
```

- [ ] **Step 4: Commit Task 1**

```bash
git add pages/orders.html scripts/verify_header_top_and_account_breadcrumb.py
git commit -m "feat(orders): synchronize top-bar navigation with dashboard catalog"
```

---

### Task 2: Standardize Account Page with Breadcrumb and Remove Brand Nav

**Files:**
- Modify: `pages/account.html:179-195`
- Test: `scripts/verify_header_top_and_account_breadcrumb.py`

**Interfaces:**
- Consumes: Existing CSS classes `.breadcrumb`, `.container`, `.account-page-section`.
- Produces: Streamlined member account page with breadcrumb navigation.

- [ ] **Step 1: Remove `<nav class="nav-bar">` from `pages/account.html`**

Delete lines 179-189:
```html
    <!-- Navigation Bar -->
    <nav class="nav-bar">
      <div class="container nav-container">
        <ul class="nav-menu">
          <li><a href="javascript:void(0)" class="nav-link active" onclick="handleNavBrandClick(event, this)"><i class="fas fa-bolt" style="color: var(--primary);"></i> Monster</a></li>
          <li><a href="javascript:void(0)" class="nav-link" onclick="handleNavBrandClick(event, this)"><i class="fas fa-fire" style="color: var(--secondary);"></i> Redbull</a></li>
          <li><a href="javascript:void(0)" class="nav-link" onclick="handleNavBrandClick(event, this)"><i class="fas fa-bolt" style="color: #FF0055;"></i> Sting</a></li>
        </ul>
      </div>
    </nav>
```

- [ ] **Step 2: Add `.breadcrumb` into `<main class="container account-page-section">`**

Insert right inside `<main>`:
```html
  <main class="container account-page-section" style="padding-top: 24px; padding-bottom: 40px;">
    <div class="breadcrumb">
      <a href="../index.html">Trang chủ</a>
      <span>/</span>
      <span>Thành viên</span>
    </div>
```

- [ ] **Step 3: Run verification script to confirm all checks pass**

Run: `python scripts/verify_header_top_and_account_breadcrumb.py`
Expected: PASS (10/10 checks).

- [ ] **Step 4: Commit Task 2**

```bash
git add pages/account.html
git commit -m "feat(account): replace brand category navbar with member breadcrumb"
```

---

### Task 3: Regression Suite Verification & Documentation

**Files:**
- Test: All 15 test suites
- Update: Walkthrough documentation `walkthrough.md`

- [ ] **Step 1: Run complete 15-suite regression test**

```powershell
python -c "
import subprocess
scripts = [
    'scripts/verify_header_top_and_account_breadcrumb.py',
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
    'scripts/verify_cart_sync.py',
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

Document Sections 27 and 28 with before/after comparisons and verification output.

- [ ] **Step 3: Commit Documentation**

```bash
git add docs/superpowers/plans/ docs/superpowers/specs/
git commit -m "docs: document header top sync and account breadcrumb specs and plans"
```
