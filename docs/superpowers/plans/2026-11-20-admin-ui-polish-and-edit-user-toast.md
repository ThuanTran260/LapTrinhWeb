# Admin UI Polish & Toast-Only Edit User Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Polish the Admin dashboard quick-filter search inputs (`admin/index.html`, `css/style.css`), simplify stock status dropdown options to `CÒN HÀNG` / `Còn hàng` (`admin/inventory.html`, 5 `admin/edit-*.html` files), and fix `openEditUserModal` / make `saveEditUser` toast-only without mutating the table UI or VIP rank badges (`js/app.js`).

**Architecture:** Three independent TDD tasks: Task 1 updates CSS `.admin-filter-search` rules and both dashboard quick-filter inputs in `admin/index.html`; Task 2 updates the stock status `<option>` text in `admin/inventory.html` and the 5 `admin/edit-*.html` pages; Task 3 fixes status/tier pre-fill in `openEditUserModal` and turns `saveEditUser` into a pure toast-and-close handler verified via Node.js runtime tests.

**Tech Stack:** Static HTML5, CSS3, Vanilla JavaScript (ES6), Python 3 Standard Library, Node.js (`v24+` for runtime unit tests).

## Global Constraints
- Pure static HTML/CSS/JS storefront and admin UI mockup; do not introduce build tools or external Python dependencies.
- Dashboard `#dash-order-keyword` (`admin/index.html:135`): exact placeholder `"Tìm mã đơn, khách..."`; remove inline `width: 170px;` on both `#dash-order-keyword` and `#dash-inv-keyword`; add `admin-filter-search--compact` class on both `.admin-filter-search` wrappers.
- `css/style.css`: `.admin-filter-search input` must include `min-width: 0;` and `text-overflow: ellipsis;`; `.admin-filter-search input::placeholder` must include `text-overflow: ellipsis;`; `.admin-filter-search--compact input` sets `width: 195px;` on desktop and `width: 100%;` inside `@media (max-width: 640px)`.
- `admin/inventory.html:98`: exact option `<option value="instock" selected>CÒN HÀNG</option>`; keep line 57 subtitle `- Sẵn sàng xuất kho` unchanged.
- All 5 `admin/edit-*.html` pages (`edit-monster.html`, `edit-redbull-lonvua.html`, `edit-redbull-original.html`, `edit-redbull-thai.html`, `edit-sting.html`): exact option `<option value="Còn hàng" selected>Còn hàng</option>`.
- `js/app.js`: `openEditUserModal` must read status from `currentEditingUserRow.cells[5]` (never `cells[0]`), preserve `smallEmail` extraction, and pre-fill `#edit-user-tier`; `saveEditUser` must ONLY show a success toast and close `modal-edit-user` without mutating any table cell, badge, button, or `localStorage`.
- Strictly local git commits only; NEVER run `git push`.
- Maintain 100% PASS across `verify_implementation.py`, `verify_admin_ui_mockup.py`, `verify_unconstrained_add_user.py`, and all `scripts/verify_*.py` suites.

---

### Task 1: Dashboard Quick-Filter Search Polish (`admin/index.html` & `css/style.css`)

**Files:**
- Create: `scripts/verify_admin_dashboard_search_and_stock_label.py` (initially checking Task 1 dashboard search criteria; Task 2 adds stock label assertions or Task 1 includes the full script? Let's keep Task 1 focused on its own script `scripts/verify_admin_dashboard_search_polish.py` so Task 1 goes RED -> GREEN cleanly on its own commit, and Task 2 adds `scripts/verify_admin_stock_label_polish.py` — even cleaner per-task gate!).
- Modify: `css/style.css:4794-4797,5615-5618`
- Modify: `admin/index.html:133-136,293-296`

**Interfaces:**
- Produces: `scripts/verify_admin_dashboard_search_polish.py` (exit `0` when CSS and `admin/index.html` pass; exit `1` otherwise).

- [ ] **Step 1: Write `scripts/verify_admin_dashboard_search_polish.py`**

```python
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    failures = []

    css_text = (ROOT / "css" / "style.css").read_text(encoding="utf-8")
    index_html = (ROOT / "admin" / "index.html").read_text(encoding="utf-8")

    search_block = re.search(r"\.admin-filter-search input\s*\{([^}]*)\}", css_text)
    if not search_block:
        failures.append("css/style.css: missing .admin-filter-search input rule")
    else:
        body = search_block.group(1)
        if "min-width: 0;" not in body:
            failures.append("css/style.css: .admin-filter-search input missing 'min-width: 0;'")
        if "text-overflow: ellipsis;" not in body:
            failures.append("css/style.css: .admin-filter-search input missing 'text-overflow: ellipsis;'")

    ph_block = re.search(r"\.admin-filter-search input::placeholder\s*\{([^}]*)\}", css_text)
    if not ph_block or "text-overflow: ellipsis;" not in ph_block.group(1):
        failures.append("css/style.css: .admin-filter-search input::placeholder missing 'text-overflow: ellipsis;'")

    compact_block = re.search(r"\.admin-filter-search--compact input\s*\{([^}]*)\}", css_text)
    if not compact_block or "width: 195px;" not in compact_block.group(1):
        failures.append("css/style.css: .admin-filter-search--compact input missing 'width: 195px;'")

    mobile_section = re.search(r"@media\s*\(max-width:\s*640px\)\s*\{([\s\S]*)$", css_text)
    if not mobile_section or not re.search(
        r"\.admin-filter-search--compact input\s*\{[^}]*width:\s*100%;",
        mobile_section.group(1),
    ):
        failures.append("css/style.css: @media (max-width: 640px) missing .admin-filter-search--compact input { width: 100%; }")

    if "Tìm mã đơn hoặc khách..." in index_html:
        failures.append("admin/index.html: still contains old placeholder 'Tìm mã đơn hoặc khách...'")
    if "width: 170px;" in index_html:
        failures.append("admin/index.html: still contains inline 'width: 170px;' on quick filter inputs")

    if index_html.count("admin-filter-search--compact") != 2:
        failures.append(
            f"admin/index.html: expected 2 'admin-filter-search--compact' wrappers, found {index_html.count('admin-filter-search--compact')}"
        )

    order_input = re.search(r'<input\b[^>]*id="dash-order-keyword"[^>]*>', index_html)
    if not order_input or 'placeholder="Tìm mã đơn, khách..."' not in order_input.group(0):
        failures.append("admin/index.html: #dash-order-keyword missing placeholder=\"Tìm mã đơn, khách...\"")

    inv_input = re.search(r'<input\b[^>]*id="dash-inv-keyword"[^>]*>', index_html)
    if not inv_input or 'placeholder="Tìm tên sản phẩm..."' not in inv_input.group(0):
        failures.append("admin/index.html: #dash-inv-keyword missing placeholder=\"Tìm tên sản phẩm...\"")

    if failures:
        print(f"FAIL ({len(failures)} checks failed):")
        for item in failures:
            print(f"  - {item}")
        return 1

    print("ALL 10 CHECKS PASSED: Admin dashboard compact search CSS + HTML verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run script to verify RED failure**

Run: `python scripts/verify_admin_dashboard_search_polish.py`
Expected: Exit code `1` with failures for missing CSS rules, `width: 170px;`, missing `admin-filter-search--compact`, and old placeholder.

- [ ] **Step 3: Update `css/style.css` and `admin/index.html`**

1. In `css/style.css` lines 4794–4797, change:
```css
.admin-filter-search input {
  padding-left: 30px;
  width: 200px;
}
```
to:
```css
.admin-filter-search input {
  padding-left: 30px;
  width: 200px;
  min-width: 0;
  text-overflow: ellipsis;
}
.admin-filter-search input::placeholder {
  text-overflow: ellipsis;
}
.admin-filter-search--compact input {
  width: 195px;
}
```

2. In `css/style.css` inside `@media (max-width: 640px)` right after line 5617 (`.admin-filter-group > :is(input, select) { width: 100%; }`), add:
```css
  .admin-filter-search--compact input {
    width: 100%;
  }
```

3. In `admin/index.html` lines 133–136, update:
```html
              <div class="admin-filter-search admin-filter-search--compact">
                <button type="button" class="admin-search-btn" aria-label="Tìm kiếm" title="Tìm kiếm"><i class="fas fa-search" aria-hidden="true"></i></button>
                <input type="text" id="dash-order-keyword" class="admin-filter-input" placeholder="Tìm mã đơn, khách..." style="padding: 5px 10px 5px 28px; font-size: 0.8rem;" />
              </div>
```

4. In `admin/index.html` lines 293–296, update:
```html
              <div class="admin-filter-search admin-filter-search--compact">
                <button type="button" class="admin-search-btn" aria-label="Tìm kiếm" title="Tìm kiếm"><i class="fas fa-search" aria-hidden="true"></i></button>
                <input type="text" id="dash-inv-keyword" class="admin-filter-input" placeholder="Tìm tên sản phẩm..." style="padding: 5px 10px 5px 28px; font-size: 0.8rem;" />
              </div>
```

- [ ] **Step 4: Run verification script (GREEN)**

Run: `python scripts/verify_admin_dashboard_search_polish.py`
Expected: `ALL 10 CHECKS PASSED` (exit `0`).

- [ ] **Step 5: Commit Task 1 locally**

```bash
git add scripts/verify_admin_dashboard_search_polish.py css/style.css admin/index.html
git commit -m "fix(admin): widen dashboard compact search inputs and prevent placeholder clipping"
```

---

### Task 2: Simplify Stock Status Dropdown Labels to `CÒN HÀNG` / `Còn hàng`

**Files:**
- Create: `scripts/verify_admin_stock_label_polish.py`
- Modify: `admin/inventory.html:98`
- Modify: `admin/edit-monster.html:189`
- Modify: `admin/edit-redbull-lonvua.html:185`
- Modify: `admin/edit-redbull-original.html:184`
- Modify: `admin/edit-redbull-thai.html:185`
- Modify: `admin/edit-sting.html:184`

**Interfaces:**
- Produces: `scripts/verify_admin_stock_label_polish.py` (exit `0` when all 6 admin HTML files pass; exit `1` otherwise).

- [ ] **Step 1: Write `scripts/verify_admin_stock_label_polish.py`**

```python
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

EDIT_PAGES = [
    "admin/edit-monster.html",
    "admin/edit-redbull-lonvua.html",
    "admin/edit-redbull-original.html",
    "admin/edit-redbull-thai.html",
    "admin/edit-sting.html",
]


def main() -> int:
    failures = []

    inv_html = (ROOT / "admin" / "inventory.html").read_text(encoding="utf-8")
    if "CÒN HÀNG (Sẵn sàng xuất)" in inv_html:
        failures.append("admin/inventory.html: still contains 'CÒN HÀNG (Sẵn sàng xuất)'")
    if '<option value="instock" selected>CÒN HÀNG</option>' not in inv_html:
        failures.append("admin/inventory.html: missing '<option value=\"instock\" selected>CÒN HÀNG</option>'")
    if "- Sẵn sàng xuất kho</p>" not in inv_html:
        failures.append("admin/inventory.html: page subtitle '- Sẵn sàng xuất kho' was unexpectedly modified")

    for rel_path in EDIT_PAGES:
        content = (ROOT / rel_path).read_text(encoding="utf-8")
        if "Còn hàng (Sẵn sàng xuất kho)" in content:
            failures.append(f"{rel_path}: still contains 'Còn hàng (Sẵn sàng xuất kho)'")
        if '<option value="Còn hàng" selected>Còn hàng</option>' not in content:
            failures.append(f"{rel_path}: missing '<option value=\"Còn hàng\" selected>Còn hàng</option>'")

    if failures:
        print(f"FAIL ({len(failures)} checks failed):")
        for item in failures:
            print(f"  - {item}")
        return 1

    print("ALL 7 CHECKS PASSED: Stock status options simplified to 'CÒN HÀNG' / 'Còn hàng'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run script to verify RED failure**

Run: `python scripts/verify_admin_stock_label_polish.py`
Expected: Exit code `1` failing on `admin/inventory.html` and all 5 `admin/edit-*.html` pages.

- [ ] **Step 3: Update stock status `<option>` text across the 6 admin HTML files**

1. `admin/inventory.html:98`:
   `<option value="instock" selected>CÒN HÀNG (Sẵn sàng xuất)</option>` → `<option value="instock" selected>CÒN HÀNG</option>`
2. `admin/edit-monster.html:189`, `admin/edit-redbull-lonvua.html:185`, `admin/edit-redbull-original.html:184`, `admin/edit-redbull-thai.html:185`, `admin/edit-sting.html:184`:
   `<option value="Còn hàng" selected>Còn hàng (Sẵn sàng xuất kho)</option>` → `<option value="Còn hàng" selected>Còn hàng</option>`

- [ ] **Step 4: Run verification script (GREEN)**

Run: `python scripts/verify_admin_stock_label_polish.py`
Expected: `ALL 7 CHECKS PASSED` (exit `0`).

- [ ] **Step 5: Commit Task 2 locally**

```bash
git add scripts/verify_admin_stock_label_polish.py admin/inventory.html admin/edit-monster.html admin/edit-redbull-lonvua.html admin/edit-redbull-original.html admin/edit-redbull-thai.html admin/edit-sting.html
git commit -m "fix(admin): simplify stock status dropdown options to 'CÒN HÀNG' and 'Còn hàng'"
```

---

### Task 3: Fix `openEditUserModal` Column Lookup & Make `saveEditUser` Toast-Only (`js/app.js`)

**Files:**
- Create: `scripts/verify_admin_edit_user_toast_only.py`
- Modify: `js/app.js:2544-2622`

**Interfaces:**
- Produces: `scripts/verify_admin_edit_user_toast_only.py` (static + Node.js runtime verification; exit `0` when all pass).

- [ ] **Step 1: Write `scripts/verify_admin_edit_user_toast_only.py`**

```python
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent


def extract_function(source: str, name: str) -> str:
    match = re.search(rf"function\s+{re.escape(name)}\s*\([^)]*\)\s*\{{", source)
    if not match:
        return ""
    start = match.start()
    depth = 0
    for idx in range(match.end() - 1, len(source)):
        ch = source[idx]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return source[start : idx + 1]
    return ""


def main() -> int:
    failures = []
    app_js = (ROOT / "js" / "app.js").read_text(encoding="utf-8")

    open_fn = extract_function(app_js, "openEditUserModal")
    save_fn = extract_function(app_js, "saveEditUser")

    if not open_fn or not save_fn:
        failures.append("js/app.js: missing openEditUserModal or saveEditUser")
    else:
        if "cells[5]" not in open_fn:
            failures.append("js/app.js: openEditUserModal must read status badge from cells[5]")
        if "smallEmail" not in open_fn:
            failures.append("js/app.js: openEditUserModal must preserve smallEmail extraction")
        if "edit-user-tier" not in open_fn:
            failures.append("js/app.js: openEditUserModal must pre-fill #edit-user-tier")

        for forbidden in ("textContent =", "innerHTML =", "className =", "localStorage.setItem"):
            if forbidden in save_fn:
                failures.append(f"js/app.js: saveEditUser must be toast-only, found DOM/storage mutation '{forbidden}'")
        if "showToast(" not in save_fn or "closeAdminModal('modal-edit-user')" not in save_fn:
            failures.append("js/app.js: saveEditUser must call showToast(...) and closeAdminModal('modal-edit-user')")

    node_test = r"""
const fs = require('fs');
const vm = require('vm');
const path = require('path');

const appCode = fs.readFileSync(path.join(process.cwd(), 'js', 'app.js'), 'utf8');

function makeSelect(options, initialValue) {
  const opts = options.map(([value, text]) => ({ value, text }));
  let val = initialValue;
  return {
    options: opts,
    get value() { return val; },
    set value(v) { val = v; },
    get selectedIndex() {
      return Math.max(0, opts.findIndex(o => o.value === val));
    }
  };
}

const fullnameEl = { value: '' };
const phoneEl = { value: '' };
const emailEl = { value: '' };
const tierEl = makeSelect([
  ['diamond', 'Hạng Kim Cương'],
  ['gold', 'Hạng Vàng'],
  ['silver', 'Hạng Bạc'],
  ['standard', 'Khách Hàng Chuẩn'],
], 'diamond');
const statusEl = makeSelect([
  ['active', 'Đang hoạt động'],
  ['locked', 'Đã khoá'],
], 'active');

const elements = {
  'edit-user-fullname': fullnameEl,
  'edit-user-phone': phoneEl,
  'edit-user-email': emailEl,
  'edit-user-tier': tierEl,
  'edit-user-status': statusEl,
};

const toasts = [];
const closedModals = [];
const openedModals = [];
let localStorageWrites = 0;

function makeRow({ rankText, rankClass, rankStyle, userName, userSub, phone, email, statusText, statusClass, lockClass, lockHtml }) {
  const rankBadge = { textContent: rankText, className: rankClass, style: rankStyle };
  const statusBadge = { textContent: statusText, className: statusClass };
  const strongEl = { textContent: userName };
  const smallEmail = { textContent: email };
  const lockBtn = { className: lockClass, innerHTML: lockHtml, title: 'Khoá' };

  const row = {
    getAttribute: () => null,
    cells: [
      { querySelector: (sel) => (sel === '.badge-status' ? rankBadge : null) },
      { textContent: `${userName}\n${userSub}`, querySelector: (sel) => (sel === 'strong' ? strongEl : null) },
      {
        childNodes: [{ textContent: phone }],
        innerHTML: `${phone}<br><small>${email}</small>`,
        querySelector: (sel) => (sel === 'small' ? smallEmail : null),
      },
      {},
      {},
      { querySelector: (sel) => (sel === '.badge-status' ? statusBadge : null) },
      { querySelector: () => lockBtn },
    ],
    querySelector: (sel) => {
      if (sel === 'strong') return strongEl;
      if (sel === '.badge-status') return rankBadge; // Intentionally mirrors row.querySelector trap!
      if (sel.includes('btn-action')) return lockBtn;
      return null;
    },
    _rankBadge: rankBadge,
    _statusBadge: statusBadge,
    _strongEl: strongEl,
    _lockBtn: lockBtn,
  };
  return row;
}

const rowBich = makeRow({
  rankText: '#3 VIP',
  rankClass: 'badge-status',
  rankStyle: 'color: #CD7F32; border: 1px solid #CD7F32;',
  userName: 'Trần Thị Bích',
  userSub: 'bich_tran (VÀNG)',
  phone: '0988.765.432',
  email: 'bich.tran@gmail.com',
  statusText: 'ĐANG HOẠT ĐỘNG',
  statusClass: 'badge-status success',
  lockClass: 'btn-action-lock',
  lockHtml: '<i class="fas fa-lock"></i> Khoá',
});

const rowMy = makeRow({
  rankText: '#5 VIP',
  rankClass: 'badge-status info',
  rankStyle: '',
  userName: 'Vũ Thảo My',
  userSub: 'my_vu (BẠC)',
  phone: '0934.555.666',
  email: 'my.vu@gmail.com',
  statusText: 'ĐÃ KHOÁ',
  statusClass: 'badge-status locked danger',
  lockClass: 'btn-action-unlock',
  lockHtml: '<i class="fas fa-lock-open"></i> Mở',
});

const sandbox = {
  console,
  URLSearchParams,
  window: { location: { pathname: '/admin/customers.html', search: '' }, addEventListener: () => {} },
  document: {
    readyState: 'loading',
    addEventListener: () => {},
    getElementById: (id) => elements[id] || null,
    querySelector: () => null,
    querySelectorAll: () => [],
    body: { style: {}, appendChild: () => {} },
  },
  localStorage: {
    getItem: () => '[]',
    setItem: () => { localStorageWrites += 1; },
  },
};

vm.createContext(sandbox);
vm.runInContext(appCode, sandbox);
sandbox.showToast = (msg, type) => toasts.push({ msg, type });
sandbox.openAdminModal = (id) => openedModals.push(id);
sandbox.closeAdminModal = (id) => closedModals.push(id);

// Test 1: Opening rowMy (#5 VIP, ĐÃ KHOÁ) must pre-fill status='locked' and tier='silver'
sandbox.openEditUserModal('my', { closest: () => rowMy });
if (statusEl.value !== 'locked') {
  throw new Error(`Expected #5 VIP statusEl.value='locked', got '${statusEl.value}'`);
}
if (tierEl.value !== 'silver') {
  throw new Error(`Expected #5 VIP tierEl.value='silver', got '${tierEl.value}'`);
}

// Test 2: Opening rowBich (#3 VIP, ĐANG HOẠT ĐỘNG, VÀNG) then changing tier & status and saving
sandbox.openEditUserModal('bich', { closest: () => rowBich });
if (tierEl.value !== 'gold' || statusEl.value !== 'active') {
  throw new Error(`Expected #3 VIP tier='gold', status='active', got tier='${tierEl.value}', status='${statusEl.value}'`);
}

fullnameEl.value = 'Trần Thị Bích (Updated)';
tierEl.value = 'standard';
statusEl.value = 'locked';
let prevented = false;
sandbox.saveEditUser({ preventDefault: () => { prevented = true; } });

if (!prevented) throw new Error('saveEditUser did not call preventDefault()');
if (toasts.length !== 1 || toasts[0].type !== 'success') {
  throw new Error(`Expected 1 success toast, got ${JSON.stringify(toasts)}`);
}
if (!closedModals.includes('modal-edit-user')) {
  throw new Error('Expected closeAdminModal("modal-edit-user")');
}
if (rowBich._rankBadge.textContent !== '#3 VIP' || rowBich._rankBadge.className !== 'badge-status') {
  throw new Error(`Rank badge mutated! text='${rowBich._rankBadge.textContent}', class='${rowBich._rankBadge.className}'`);
}
if (rowBich._statusBadge.textContent !== 'ĐANG HOẠT ĐỘNG' || rowBich._statusBadge.className !== 'badge-status success') {
  throw new Error(`Status badge mutated! text='${rowBich._statusBadge.textContent}', class='${rowBich._statusBadge.className}'`);
}
if (rowBich._strongEl.textContent !== 'Trần Thị Bích') {
  throw new Error(`User name mutated in DOM: '${rowBich._strongEl.textContent}'`);
}
if (rowBich._lockBtn.className !== 'btn-action-lock') {
  throw new Error(`Lock button mutated: '${rowBich._lockBtn.className}'`);
}
if (localStorageWrites !== 0) {
  throw new Error(`Expected 0 localStorage writes, got ${localStorageWrites}`);
}
console.log('NODE_RUNTIME_PASS');
"""

    proc = subprocess.run(
        ["node", "-e", node_test],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if proc.returncode != 0 or "NODE_RUNTIME_PASS" not in proc.stdout:
        failures.append(
            f"Node.js runtime test failed (exit {proc.returncode}): {(proc.stderr or proc.stdout).strip()}"
        )

    if failures:
        print(f"FAIL ({len(failures)} checks failed):")
        for item in failures:
            print(f"  - {item}")
        return 1

    print("ALL CHECKS PASSED: openEditUserModal pre-fill + toast-only saveEditUser verified (static + Node runtime).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run script to verify RED failure**

Run: `python scripts/verify_admin_edit_user_toast_only.py`
Expected: Exit code `1` failing both static checks (missing `cells[5]`, `#edit-user-tier` pre-fill, forbidden DOM/storage mutations in `saveEditUser`) and Node runtime test (rank badge overwritten / statusEl wrong).

- [ ] **Step 3: Update `openEditUserModal` and `saveEditUser` in `js/app.js` (lines 2544–2622)**

Replace lines 2544–2622 of `js/app.js` with:
```javascript
function openEditUserModal(customerKey, btn) {
  currentEditingUserRow = btn ? btn.closest('tr') : null;
  const nameEl = document.getElementById('edit-user-fullname');
  const phoneEl = document.getElementById('edit-user-phone');
  const emailEl = document.getElementById('edit-user-email');
  const tierEl = document.getElementById('edit-user-tier');
  const statusEl = document.getElementById('edit-user-status');

  const resolveTierValue = (text) => {
    const upper = (text || '').toUpperCase();
    if (upper.includes('KIM CƯƠNG')) return 'diamond';
    if (upper.includes('VÀNG')) return 'gold';
    if (upper.includes('BẠC')) return 'silver';
    return 'standard';
  };

  if (currentEditingUserRow) {
    const strong = currentEditingUserRow.querySelector('strong');
    if (nameEl && strong) nameEl.value = strong.textContent.trim();
    if (phoneEl && currentEditingUserRow.cells[2]) {
      const pText = currentEditingUserRow.cells[2].childNodes[0] ? currentEditingUserRow.cells[2].childNodes[0].textContent.trim() : '';
      phoneEl.value = pText;
    }
    const smallEmail = currentEditingUserRow.cells[2] ? currentEditingUserRow.cells[2].querySelector('small') : null;
    if (emailEl && smallEmail) {
      emailEl.value = smallEmail.textContent.trim();
    }
    if (tierEl) {
      const infoText = currentEditingUserRow.cells[1] ? currentEditingUserRow.cells[1].textContent : '';
      tierEl.value = resolveTierValue(infoText);
    }
    const statusCell = currentEditingUserRow.cells[5];
    const statusBadge = statusCell ? statusCell.querySelector('.badge-status') : null;
    if (statusBadge && statusEl) {
      statusEl.value = statusBadge.textContent.includes('KHOÁ') ? 'locked' : 'active';
    }
  } else if (typeof CUSTOMER_DATA_REGISTRY !== 'undefined' && CUSTOMER_DATA_REGISTRY[customerKey]) {
    const data = CUSTOMER_DATA_REGISTRY[customerKey];
    if (nameEl) nameEl.value = data.name;
    if (phoneEl) phoneEl.value = data.phone;
    if (emailEl) emailEl.value = data.email;
    if (tierEl) tierEl.value = resolveTierValue(data.tier);
    if (statusEl) statusEl.value = 'active';
  }
  openAdminModal('modal-edit-user');
}

function saveEditUser(e) {
  if (e && e.preventDefault) e.preventDefault();
  const nameEl = document.getElementById('edit-user-fullname');
  const name = nameEl ? nameEl.value.trim() || 'Người dùng' : 'Người dùng';
  const tierEl = document.getElementById('edit-user-tier');
  const statusEl = document.getElementById('edit-user-status');
  const tierText = tierEl && tierEl.selectedIndex >= 0 ? tierEl.options[tierEl.selectedIndex].text : '';
  const statusText = statusEl && statusEl.selectedIndex >= 0 ? statusEl.options[statusEl.selectedIndex].text : '';
  const details = [tierText, statusText].filter(Boolean).join(' • ');

  showToast(
    'Đã lưu thay đổi thông tin người dùng "' + name + '"' + (details ? ' (' + details + ')' : '') + ' thành công!',
    'success'
  );
  closeAdminModal('modal-edit-user');
}
```

- [ ] **Step 4: Run targeted & full regression test suites (GREEN)**

Run:
- `node --check js/app.js` (Expected: exit `0`)
- `python scripts/verify_admin_edit_user_toast_only.py` (Expected: `ALL CHECKS PASSED`, exit `0`)
- `python scripts/verify_unconstrained_add_user.py` (Expected: `ALL 30 CHECKS PASSED PERFECTLY!`, exit `0`)
- `python scripts/verify_admin_ui_mockup.py` (Expected: `10/10 TIÊU CHÍ ĐẠT`, exit `0`)
- `python verify_implementation.py` (Expected: `ALL 66 CHECKS PASSED PERFECTLY!`, exit `0`)
- All `scripts/verify_*.py` scripts (Expected: `0` failures)

- [ ] **Step 5: Commit Task 3 locally**

```bash
git add scripts/verify_admin_edit_user_toast_only.py js/app.js
git commit -m "fix(admin): make saveEditUser toast-only and read status/tier safely in openEditUserModal"
```
