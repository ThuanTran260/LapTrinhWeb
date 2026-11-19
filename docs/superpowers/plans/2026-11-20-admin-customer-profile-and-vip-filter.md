# Admin Customer Profile Page, "Khách Hàng" Rename, & Top 5 VIP Filter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the `#modal-customer-detail` popup with a standalone `admin/customer-detail.html` page for Nguyễn Văn An (showing his profile, `12.400.000đ` cumulative spending, and a multi-order payment history table with Page-1-only pagination whose other page buttons show a toast without switching pages), rename `"Khách Hàng VIP"` to `"Khách Hàng"` across Admin, rename the `Đơn Hàng Mua (Chi Tiết)` column to `Đơn Gần Đây` with a `Chi Tiết` link to `customer-detail.html`, rename `Thống Kê Top 5 VIP` to `Thống Kê`, add a `"Lọc 5 Người VIP Nhất"` filter on `admin/customers.html`, and point every customer name across `admin/orders.html`, `admin/customers.html`, and `admin/index.html` to `customer-detail.html`.

**Architecture:** Three independent TDD tasks: Task 1 creates `admin/customer-detail.html` plus `handleCustomerHistoryPage` / `openCustomerDetailModal` routing in `js/app.js`; Task 2 renames `"Khách Hàng VIP"` to `"Khách Hàng"` in the sidebar of all 12 existing `admin/*.html` pages, removes `#modal-customer-detail` from `admin/orders.html` and `admin/index.html`, links all customer names there to `customer-detail.html`, and updates `scripts/verify_admin_order_links.py`; Task 3 updates `admin/customers.html` (headings, `Thống Kê` button, `Lọc 5 Người VIP Nhất` control, `Đơn Gần Đây` column + `Chi Tiết` buttons, 6th customer row `#6 Hoàng Đức Long`, removal of `#modal-customer-detail`), updates `toggleTop5VipFilter` / `applyAdminCustomerFilter` / `resetAdminCustomerFilter` / `saveAddUser` / `initCustomUsersTable` in `js/app.js`, and runs the full regression suite.

**Tech Stack:** Static HTML5, CSS3, Vanilla JavaScript (ES6), Python 3 Standard Library, Node.js (`v24+` for runtime unit tests).

## Global Constraints
- Pure static HTML/CSS/JS storefront and admin UI mockup; do not introduce build tools or external Python dependencies.
- Standalone file requirement: customer profile & payment history MUST live in a dedicated page `admin/customer-detail.html` (`href="customer-detail.html"`), NEVER in a popup modal (`#modal-customer-detail` must be removed from `admin/customers.html`, `admin/orders.html`, and `admin/index.html`).
- `admin/customer-detail.html`: displays Nguyễn Văn An's profile (`12.400.000đ` total spent, `15 Đơn`), multiple orders on Page 1 of `#customer-history-tbody`, and pagination buttons (`1`, `2`, `3`, `Sau`) where ONLY Page 1 is coded and clicking Page `2`/`3`/`Sau` only triggers a toast notification without changing page or modifying Page 1 rows.
- Sidebar link label across all `admin/*.html` pages (including `admin/customer-detail.html`): `Khách Hàng` (never `Khách Hàng VIP`).
- `admin/customers.html`:
  - Page title & H1 use `Khách Hàng` (`Quản Lý Khách Hàng` / `QUẢN LÝ <span>KHÁCH HÀNG</span>`), while keeping `TOP 5 KHÁCH HÀNG` in `#customers-section` heading for rubric checks (`verify_admin_ui_mockup.py` & `verify_rubric_coverage.py`).
  - Filter bar button `Thống Kê Top 5 VIP` renamed to `Thống Kê`.
  - Add Top 5 VIP filter button (`id="btn-filter-top5-vip"`, `onclick="toggleTop5VipFilter(this)"`, label `Lọc 5 Người VIP Nhất`) filtering `#customers-table` between all 6 customers (`#1`–`#6`) and Top 5 VIP (`#1`–`#5`).
  - Column header `Đơn Hàng Mua (Chi Tiết)` renamed to `Đơn Gần Đây`.
  - Keep `#EB-XXXX` order links (`openOrderDetailModal`) for rubric compliance AND add a clickable `Chi Tiết` button (`href="customer-detail.html"`) in every row's `Đơn Gần Đây` cell; wrap every customer name in `<a href="customer-detail.html">`.
- `admin/orders.html` & `admin/index.html`: every customer name in the orders table links directly to `customer-detail.html` (Nguyễn Văn An).
- Strictly local git commits only; NEVER run `git push`.
- Maintain 100% PASS across `verify_implementation.py`, `verify_admin_ui_mockup.py`, `verify_rubric_coverage.py`, `verify_unconstrained_add_user.py`, `verify_footer_sync.py`, `verify_admin_order_links.py`, and all `scripts/verify_*.py` suites.

---

### Task 1: Create Standalone `admin/customer-detail.html` & Paginated Toast Handler (`js/app.js`)

**Files:**
- Create: `scripts/verify_admin_customer_detail_page.py`
- Create: `admin/customer-detail.html`
- Modify: `js/app.js:1066-1141` (replace `#modal-customer-detail` popup logic in `openCustomerDetailModal` with direct navigation to `customer-detail.html` and add `handleCustomerHistoryPage(page)`)

**Interfaces:**
- Produces: `admin/customer-detail.html` (standalone Nguyễn Văn An profile + Page 1 payment history + pagination).
- Produces: `handleCustomerHistoryPage(page, btn)` in `js/app.js` (toast-only pagination handler keeping Page 1 intact) and `openCustomerDetailModal(customerKey)` navigating to `customer-detail.html`.

- [ ] **Step 1: Write `scripts/verify_admin_customer_detail_page.py`**

```python
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    failures = []

    detail_path = ROOT / "admin" / "customer-detail.html"
    app_js = (ROOT / "js" / "app.js").read_text(encoding="utf-8")

    if not detail_path.exists():
        failures.append("admin/customer-detail.html: file does not exist")
    else:
        html = detail_path.read_text(encoding="utf-8")
        if "Nguyễn Văn An" not in html:
            failures.append("admin/customer-detail.html: missing 'Nguyễn Văn An'")
        if "12.400.000đ" not in html:
            failures.append("admin/customer-detail.html: missing '12.400.000đ' cumulative spend")
        if "modal-customer-detail" in html:
            failures.append("admin/customer-detail.html: must NOT contain popup modal-customer-detail")
        if '<i class="fas fa-users"></i> Khách Hàng</a>' not in html:
            failures.append("admin/customer-detail.html: sidebar missing 'Khách Hàng' link")
        if "Khách Hàng VIP" in html:
            failures.append("admin/customer-detail.html: must NOT contain 'Khách Hàng VIP'")

        tbody_match = re.search(r'<tbody id="customer-history-tbody">([\s\S]*?)</tbody>', html)
        if not tbody_match:
            failures.append("admin/customer-detail.html: missing tbody#customer-history-tbody")
        else:
            row_count = len(re.findall(r"<tr\b", tbody_match.group(1)))
            if row_count < 4:
                failures.append(f"admin/customer-detail.html: expected >= 4 Page-1 order rows, got {row_count}")

        for token in ("handleCustomerHistoryPage(2", "handleCustomerHistoryPage(3", "handleCustomerHistoryPage('next'"):
            if token not in html:
                failures.append(f"admin/customer-detail.html: missing pagination trigger {token}")

        for footer_token in ("CÁC DÒNG SẢN PHẨM", "HỆ THỐNG TRANG", "NHẬN VOUCHER ƯU ĐÃI", "footer-bottom"):
            if footer_token not in html:
                failures.append(f"admin/customer-detail.html: footer missing '{footer_token}'")

    if "function handleCustomerHistoryPage(" not in app_js:
        failures.append("js/app.js: missing handleCustomerHistoryPage function")
    if "customer-detail.html" not in app_js:
        failures.append("js/app.js: missing navigation to 'customer-detail.html'")

    node_test = r"""
const fs = require('fs');
const vm = require('vm');
const path = require('path');

const appCode = fs.readFileSync(path.join(process.cwd(), 'js', 'app.js'), 'utf8');
const toasts = [];
const page1Btn = { classList: { contains: (c) => c === 'active', add: () => {}, remove: () => {} } };
const page2Btn = { classList: { contains: () => false, add: () => { throw new Error('Page 2 must not become active'); }, remove: () => {} } };
const tbody = { innerHTML: '<tr><td>#EB-8801</td></tr>' };

const sandbox = {
  console,
  URLSearchParams,
  window: { location: { pathname: '/admin/customer-detail.html', search: '', href: '' }, addEventListener: () => {} },
  document: {
    readyState: 'loading',
    addEventListener: () => {},
    getElementById: (id) => (id === 'customer-history-tbody' ? tbody : null),
    querySelector: () => null,
    querySelectorAll: (sel) => (sel.includes('.page-btn') ? [page1Btn, page2Btn] : []),
    body: { style: {}, appendChild: () => {} },
  },
  localStorage: { getItem: () => '[]', setItem: () => {} },
};

vm.createContext(sandbox);
vm.runInContext(appCode, sandbox);
sandbox.showToast = (msg, type) => toasts.push({ msg, type });

const originalHtml = tbody.innerHTML;
sandbox.handleCustomerHistoryPage(2, page2Btn);
if (toasts.length !== 1 || !toasts[0].msg.includes('Trang 2')) {
  throw new Error('Expected toast mentioning Trang 2, got ' + JSON.stringify(toasts));
}
if (tbody.innerHTML !== originalHtml) {
  throw new Error('Page 1 table mutated when clicking Page 2!');
}
if (sandbox.window.location.href !== '') {
  throw new Error('location.href changed on pagination click!');
}

sandbox.openCustomerDetailModal('tuan');
if (sandbox.window.location.href !== 'customer-detail.html') {
  throw new Error("Expected openCustomerDetailModal('tuan') to route to 'customer-detail.html', got " + sandbox.window.location.href);
}
console.log('NODE_CUSTOMER_DETAIL_PASS');
"""
    proc = subprocess.run(["node", "-e", node_test], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0 or "NODE_CUSTOMER_DETAIL_PASS" not in proc.stdout:
        failures.append(f"Node runtime check failed: {(proc.stderr or proc.stdout).strip()}")

    if failures:
        print(f"FAIL ({len(failures)} checks failed):")
        for item in failures:
            print(f"  - {item}")
        return 1

    print("ALL CHECKS PASSED: Standalone admin/customer-detail.html & toast-only pagination verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run script to verify RED failure**

Run: `python scripts/verify_admin_customer_detail_page.py`
Expected: Exit code `1` failing because `admin/customer-detail.html` and `handleCustomerHistoryPage` do not exist yet.

- [ ] **Step 3: Create `admin/customer-detail.html`**

Create `admin/customer-detail.html` with:
- `<title>Hồ Sơ Khách Hàng - Nguyễn Văn An | ENERGY BOOST ADMIN</title>`
- Admin sidebar (matching `admin/order-detail.html:67-97`, with `customers.html` active and label `Khách Hàng` instead of `Khách Hàng VIP`).
- Topbar with breadcrumb (`Admin / Khách Hàng / Hồ sơ Nguyễn Văn An`), `H1`: `HỒ SƠ <span>KHÁCH HÀNG</span>`, action buttons (`Quay Lại Danh Sách Khách Hàng` → `customers.html`, `Quản Lý Đơn Hàng` → `orders.html`), and admin user pill.
- Profile card (`.admin-section-box`) reusing `.vip-profile-header`, `.vip-avatar` (`NA`), `#vip-detail-name` (`Nguyễn Văn An`), `.vip-badge-diamond` (`HẠNG KIM CƯƠNG`), `.vip-stats-grid` (`2.450` điểm tích lũy, `12.400.000đ` tổng chi tiêu, `15 Đơn` hoàn tất), and `.vip-info-list` (`an_nguyen`, `0912.345.678`, `an.nguyen@gmail.com`, `45 Lê Duẩn, P. Bến Nghé, Quận 1, TP.HCM`, `20/02/2024`, `Miễn phí ship hỏa tốc + Chiết khấu 10%`).
- Payment & Order History card (`.admin-section-box`) with heading `LỊCH SỬ THANH TOÁN & MUA HÀNG`, subtitle badge `Trang 1 / 3 • 6/15 đơn hàng gần nhất • Tổng tích lũy: 12.400.000đ`, and `.cart-table` containing `<tbody id="customer-history-tbody">` with 6 Page-1 order rows of Nguyễn Văn An (no `"Thùng"` wording, using `"Lon"`):
  1. `#EB-8801` | `02/10/2026 - 14:30` | `2x Monster Original 355ml, 2x Redbull Original 250ml` | `VietQR` | `126.000đ` | `ĐÃ GIAO (THÀNH CÔNG)` | `order-detail.html?id=EB-8801`
  2. `#EB-8802` | `01/10/2026 - 10:15` | `4x Monster Zero Ultra White, 3x Redbull Thái Lan` | `Chuyển khoản` | `246.000đ` | `ĐÃ XÁC NHẬN` | `order-detail.html?id=EB-8802`
  3. `#EB-8798` | `25/09/2026 - 16:40` | `48 Lon Monster Energy Original 355ml` | `VietQR` | `1.920.000đ` | `ĐÃ GIAO (THÀNH CÔNG)` | `order-detail.html?id=EB-8801`
  4. `#EB-8795` | `18/09/2026 - 09:20` | `24 Lon Monster Ultra Paradise + 12 Lon Redbull` | `Ví MoMo` | `1.180.000đ` | `ĐÃ GIAO (THÀNH CÔNG)` | `order-detail.html?id=EB-8801`
  5. `#EB-8790` | `10/09/2026 - 19:05` | `48 Lon Sting Dâu & Vàng + 10 Lon Monster` | `COD` | `960.000đ` | `ĐÃ GIAO (THÀNH CÔNG)` | `order-detail.html?id=EB-8801`
  6. `#EB-8784` | `02/09/2026 - 11:30` | `24 Lon Monster Mango Loco + 12 Lon Redbull Thái` | `VietQR` | `1.140.000đ` | `ĐÃ GIAO (THÀNH CÔNG)` | `order-detail.html?id=EB-8801`
- Pagination strip (`.pagination-strip`):
  ```html
  <div class="pagination-strip" aria-label="Phân trang lịch sử mua hàng">
    <button type="button" class="page-btn disabled" aria-label="Trang trước" disabled><i class="fas fa-chevron-left"></i></button>
    <button type="button" class="page-btn active" onclick="handleCustomerHistoryPage(1, this)">1</button>
    <button type="button" class="page-btn" onclick="handleCustomerHistoryPage(2, this)">2</button>
    <button type="button" class="page-btn" onclick="handleCustomerHistoryPage(3, this)">3</button>
    <button type="button" class="page-btn" aria-label="Trang sau" onclick="handleCustomerHistoryPage('next', this)"><i class="fas fa-chevron-right"></i></button>
  </div>
  ```
- Standard 4-column Admin footer (identical to `admin/order-detail.html:330-389`), `<div id="toast-container" class="toast-container"></div>`, and `<script src="../js/app.js"></script>`.

- [ ] **Step 4: Update `openCustomerDetailModal` and add `handleCustomerHistoryPage` in `js/app.js`**

In `js/app.js:1066-1141`, replace the modal DOM population with standalone page routing + add `handleCustomerHistoryPage`:
```javascript
function openCustomerDetailModal(customerKey) {
  window.location.href = 'customer-detail.html';
}

function handleCustomerHistoryPage(page, btn) {
  const label = page === 'next' ? 'tiếp theo (Trang 2)' : 'Trang ' + page;
  if (String(page) === '1') {
    showToast('Đang hiển thị Trang 1/3 lịch sử thanh toán của Nguyễn Văn An (Tổng tích lũy 15 đơn: 12.400.000đ).', 'info');
    return;
  }
  showToast('Đã chọn ' + label + ' — Mô phỏng tĩnh chỉ hiển thị chi tiết Trang 1 (15 đơn / 12.400.000đ), không chuyển trang.', 'info');
}
```

- [ ] **Step 5: Run verification script (GREEN) & commit Task 1**

Run:
- `node --check js/app.js`
- `python scripts/verify_admin_customer_detail_page.py`
Expected: Exit `0`.

```bash
git add scripts/verify_admin_customer_detail_page.py admin/customer-detail.html js/app.js
git commit -m "feat(admin): add standalone customer-detail page for Nguyen Van An with toast-only pagination"
```

---

### Task 2: Rename Sidebar `"Khách Hàng VIP"` → `"Khách Hàng"` & Route Order/Dashboard Customer Names to `customer-detail.html`

**Files:**
- Create: `scripts/verify_admin_sidebar_and_orders_customer_links.py`
- Modify: `admin/index.html:35,164-256,768-831`
- Modify: `admin/orders.html:35,144-256,378-441`
- Modify: `admin/inventory.html:35`, `admin/revenue.html:35`, `admin/customers.html:35`, `admin/settings.html:35`, `admin/order-detail.html:85`, `admin/edit-monster.html:35`, `admin/edit-redbull-lonvua.html:36`, `admin/edit-redbull-original.html:35`, `admin/edit-redbull-thai.html:36`, `admin/edit-sting.html:35`

**Interfaces:**
- Consumes: `admin/customer-detail.html` created in Task 1.
- Produces: `scripts/verify_admin_sidebar_and_orders_customer_links.py` (exit `0` when all 12 admin sidebars use `"Khách Hàng"` and `admin/orders.html` + `admin/index.html` route every customer name directly to `customer-detail.html` without `#modal-customer-detail`).

- [ ] **Step 1: Write `scripts/verify_admin_sidebar_and_orders_customer_links.py`**

```python
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

SIDEBAR_FILES = [
    "admin/index.html",
    "admin/orders.html",
    "admin/inventory.html",
    "admin/revenue.html",
    "admin/customers.html",
    "admin/settings.html",
    "admin/order-detail.html",
    "admin/edit-monster.html",
    "admin/edit-redbull-lonvua.html",
    "admin/edit-redbull-original.html",
    "admin/edit-redbull-thai.html",
    "admin/edit-sting.html",
]


def main() -> int:
    failures = []

    for rel_path in SIDEBAR_FILES:
        text = (ROOT / rel_path).read_text(encoding="utf-8")
        if '<i class="fas fa-users"></i> Khách Hàng VIP</a>' in text:
            failures.append(f"{rel_path}: sidebar still says 'Khách Hàng VIP'")
        if '<i class="fas fa-users"></i> Khách Hàng</a>' not in text:
            failures.append(f"{rel_path}: sidebar missing 'Khách Hàng' link")

    for page_rel in ("admin/orders.html", "admin/index.html"):
        text = (ROOT / page_rel).read_text(encoding="utf-8")
        if 'id="modal-customer-detail"' in text:
            failures.append(f"{page_rel}: still contains popup #modal-customer-detail")
        if "openCustomerDetailModal(" in text:
            failures.append(f"{page_rel}: still calls openCustomerDetailModal popup trigger")
        links = re.findall(r'<a\s+href="customer-detail\.html"[^>]*>', text)
        if len(links) < 6:
            failures.append(f"{page_rel}: expected >= 6 links to customer-detail.html, found {len(links)}")

    if failures:
        print(f"FAIL ({len(failures)} checks failed):")
        for item in failures:
            print(f"  - {item}")
        return 1

    print("ALL CHECKS PASSED: Admin sidebars say 'Khách Hàng' and orders/dashboard link to customer-detail.html.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run script to verify RED failure**

Run: `python scripts/verify_admin_sidebar_and_orders_customer_links.py`
Expected: Exit code `1`.

- [ ] **Step 3: Update sidebar link text on all 12 `admin/*.html` files**

Replace `<i class="fas fa-users"></i> Khách Hàng VIP</a>` with `<i class="fas fa-users"></i> Khách Hàng</a>` across all 12 files listed in **Files**.

- [ ] **Step 4: Replace customer name buttons & remove `#modal-customer-detail` in `admin/orders.html` and `admin/index.html`**

1. In `admin/orders.html` (lines 144, 166, 188, 210, 232, 254), replace each `<button type="button" class="btn-link" onclick="openCustomerDetailModal('...')" ...>NAME</button>` with:
```html
<a href="customer-detail.html" style="color:#FFF;font-weight:700;text-decoration:none;" title="Xem hồ sơ & lịch sử thanh toán của Nguyễn Văn An">
  NAME
</a>
```
and remove the `<!-- Modal Chi Tiết Khách Hàng VIP (Động) -->` (`id="modal-customer-detail"`) block at lines 378–441.

2. In `admin/index.html` (lines 164, 181, 198, 220, 237, 254), replace each `<button type="button" class="btn-link" onclick="openCustomerDetailModal('...')" ...>NAME</button>` with:
```html
<a href="customer-detail.html" style="color:#FFF;font-weight:700;text-decoration:none;" title="Xem hồ sơ & lịch sử thanh toán của Nguyễn Văn An">
  NAME
</a>
```
and remove the `<!-- Modal Chi Tiết Khách Hàng VIP (Phạm Minh Tuấn) -->` (`id="modal-customer-detail"`) block at lines 768–831.

- [ ] **Step 5: Run verification scripts & commit Task 2 locally**

Run:
- `python scripts/verify_admin_sidebar_and_orders_customer_links.py` (Expected: exit `0`)
- `python scripts/verify_unconstrained_add_user.py` (Expected: exit `0`)
- `python scripts/verify_order_detail_pages.py` (Expected: exit `0`)

```bash
git add scripts/verify_admin_sidebar_and_orders_customer_links.py admin/*.html
git commit -m "feat(admin): rename sidebar to 'Khách Hàng' and link order customer names to customer-detail.html"
```

---

### Task 3: Update `admin/customers.html` (`Đơn Gần Đây`, `Chi Tiết`, `Thống Kê`, Top 5 VIP Filter, All → `customer-detail.html`) & Filter/Add-User JS

**Files:**
- Create: `scripts/verify_admin_customers_and_vip_filter.py`
- Modify: `scripts/verify_admin_order_links.py:79-87`
- Modify: `admin/customers.html:6-7,54-56,109-215,285-350`
- Modify: `js/app.js:2375-2392,2522-2534,2635-2647`

**Interfaces:**
- Consumes: `admin/customer-detail.html` (Task 1) and updated sidebar/orders links (Task 2).
- Produces: `toggleTop5VipFilter(btn)` in `js/app.js` and `scripts/verify_admin_customers_and_vip_filter.py`.

- [ ] **Step 1: Write `scripts/verify_admin_customers_and_vip_filter.py` & update `scripts/verify_admin_order_links.py`**

1. Update `scripts/verify_admin_order_links.py:79-87` (`test_vip_modal_order_link`) to verify `admin/customer-detail.html` and `href="customer-detail.html"` without `#modal-customer-detail`:
```python
@test("5. Hồ sơ khách hàng: Tên khách hàng trỏ về trang riêng customer-detail.html (không dùng popup)")
def test_vip_modal_order_link():
    detail_page = read_file("admin/customer-detail.html")
    assert detail_page is not None, "Thiếu trang riêng admin/customer-detail.html!"
    assert 'href="order-detail.html' in detail_page, "admin/customer-detail.html thiếu liên kết tới order-detail.html"
    files = ["admin/orders.html", "admin/index.html", "admin/customers.html"]
    for f in files:
        content = read_file(f)
        assert content is not None, f"File {f} không tồn tại!"
        assert 'id="modal-customer-detail"' not in content, f"File {f} vẫn còn popup #modal-customer-detail"
        assert 'href="customer-detail.html"' in content, f"File {f} thiếu liên kết customer-detail.html"
```

2. Create `scripts/verify_admin_customers_and_vip_filter.py`:
```python
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    failures = []

    cust_html = (ROOT / "admin" / "customers.html").read_text(encoding="utf-8")
    app_js = (ROOT / "js" / "app.js").read_text(encoding="utf-8")

    if "<title>Quản Lý Khách Hàng | ENERGY BOOST ADMIN</title>" not in cust_html:
        failures.append("admin/customers.html: title not updated to 'Quản Lý Khách Hàng | ENERGY BOOST ADMIN'")
    if "QUẢN LÝ <span>KHÁCH HÀNG</span>" not in cust_html:
        failures.append("admin/customers.html: H1 not updated to 'QUẢN LÝ <span>KHÁCH HÀNG</span>'")
    if '<i class="fas fa-users"></i> Khách Hàng VIP</a>' in cust_html:
        failures.append("admin/customers.html: sidebar still contains 'Khách Hàng VIP'")
    if "TOP 5 KHÁCH HÀNG" not in cust_html:
        failures.append("admin/customers.html: missing 'TOP 5 KHÁCH HÀNG' token for rubric checks")
    if "openOrderDetailModal" not in cust_html:
        failures.append("admin/customers.html: missing 'openOrderDetailModal' token for rubric checks")
    if "<th>Đơn Hàng Mua (Chi Tiết)</th>" in cust_html:
        failures.append("admin/customers.html: column header still says 'Đơn Hàng Mua (Chi Tiết)'")
    if "<th>Đơn Gần Đây</th>" not in cust_html:
        failures.append("admin/customers.html: missing '<th>Đơn Gần Đây</th>' header")
    if "Thống Kê Top 5 VIP" in cust_html:
        failures.append("admin/customers.html: button still says 'Thống Kê Top 5 VIP'")
    if not re.search(r'onclick="applyAdminCustomerFilter\(\)"[^>]*>[\s\S]*?Thống Kê\s*</button>', cust_html):
        failures.append("admin/customers.html: apply button label not updated to 'Thống Kê'")
    if 'id="btn-filter-top5-vip"' not in cust_html or "Lọc 5 Người VIP Nhất" not in cust_html:
        failures.append("admin/customers.html: missing #btn-filter-top5-vip ('Lọc 5 Người VIP Nhất')")
    if 'id="modal-customer-detail"' in cust_html:
        failures.append("admin/customers.html: must NOT contain popup #modal-customer-detail")

    tbody_match = re.search(r'<table class="cart-table" id="customers-table">[\s\S]*?<tbody>([\s\S]*?)</tbody>', cust_html)
    if not tbody_match:
        failures.append("admin/customers.html: missing #customers-table tbody")
    else:
        tbody = tbody_match.group(1)
        for rank in range(1, 7):
            if f'data-vip-rank="{rank}"' not in tbody:
                failures.append(f"admin/customers.html: missing row with data-vip-rank=\"{rank}\"")
        if "Hoàng Đức Long" not in tbody:
            failures.append("admin/customers.html: missing 6th customer 'Hoàng Đức Long'")
        detail_btns = re.findall(r'<a href="customer-detail\.html" class="btn-view-detail"[^>]*>[\s\S]*?Chi Tiết</a>', tbody)
        if len(detail_btns) != 6:
            failures.append(f"admin/customers.html: expected 6 'Chi Tiết' links to customer-detail.html, found {len(detail_btns)}")
        name_links = re.findall(r'<a href="customer-detail\.html"[^>]*><strong>[^<]+</strong></a>', tbody)
        if len(name_links) != 6:
            failures.append(f"admin/customers.html: expected 6 customer name links to customer-detail.html, found {len(name_links)}")

    if "function toggleTop5VipFilter(" not in app_js:
        failures.append("js/app.js: missing toggleTop5VipFilter function")

    node_test = r"""
const fs = require('fs');
const vm = require('vm');
const path = require('path');

const appCode = fs.readFileSync(path.join(process.cwd(), 'js', 'app.js'), 'utf8');
const toasts = [];

function makeCustomerRow(rank, tierText, nameText) {
  return {
    getAttribute: (attr) => (attr === 'data-vip-rank' ? String(rank) : null),
    style: { display: '' },
    textContent: `${nameText} ${tierText}`,
  };
}

const rows = [
  makeCustomerRow(1, 'KIM CƯƠNG', 'Phạm Minh Tuấn'),
  makeCustomerRow(2, 'KIM CƯƠNG', 'Nguyễn Văn An'),
  makeCustomerRow(3, 'VÀNG', 'Trần Thị Bích'),
  makeCustomerRow(4, 'VÀNG', 'Lê Hoàng Nam'),
  makeCustomerRow(5, 'BẠC', 'Vũ Thảo My'),
  makeCustomerRow(6, 'BẠC', 'Hoàng Đức Long'),
];

const btnClasses = new Set(['filter-pill']);
const top5Btn = {
  classList: {
    toggle: (c, force) => (force === undefined ? (btnClasses.has(c) ? btnClasses.delete(c) : btnClasses.add(c)) : (force ? btnClasses.add(c) : btnClasses.delete(c))),
    add: (c) => btnClasses.add(c),
    remove: (c) => btnClasses.delete(c),
    contains: (c) => btnClasses.has(c),
  },
};

const tierSelect = { value: 'all', options: [{ value: 'all', text: 'Tất cả cấp bậc (6 khách)' }], selectedIndex: 0 };
const kwInput = { value: '' };
const fromInput = { value: '2026-01-01' };
const toInput = { value: '2026-10-17' };

const sandbox = {
  console,
  URLSearchParams,
  window: { location: { pathname: '/admin/customers.html', search: '' }, addEventListener: () => {} },
  document: {
    readyState: 'loading',
    addEventListener: () => {},
    getElementById: (id) => ({
      'btn-filter-top5-vip': top5Btn,
      'filter-customer-tier': tierSelect,
      'filter-customer-keyword': kwInput,
      'stat-customer-from': fromInput,
      'stat-customer-to': toInput,
    }[id] || null),
    querySelector: () => null,
    querySelectorAll: (sel) => (sel.includes('#customers-table tbody tr') ? rows : []),
    body: { style: {}, appendChild: () => {} },
  },
  localStorage: { getItem: () => '[]', setItem: () => {} },
};

vm.createContext(sandbox);
vm.runInContext(appCode, sandbox);
sandbox.showToast = (msg, type) => toasts.push({ msg, type });

// Enable Top 5 VIP filter -> rank 6 hidden, ranks 1..5 visible
sandbox.toggleTop5VipFilter(top5Btn);
if (!btnClasses.has('active')) throw new Error('Expected active class on #btn-filter-top5-vip');
if (rows[5].style.display !== 'none') throw new Error('Expected row #6 to be hidden under Top 5 VIP filter');
for (let i = 0; i < 5; i++) {
  if (rows[i].style.display === 'none') throw new Error(`Expected row #${i + 1} to stay visible`);
}

// Reset restores all 6 rows
sandbox.resetAdminCustomerFilter();
if (btnClasses.has('active')) throw new Error('Expected reset to clear active class');
for (let i = 0; i < 6; i++) {
  if (rows[i].style.display !== '') throw new Error(`Expected row #${i + 1} visible after reset`);
}
console.log('NODE_VIP_FILTER_PASS');
"""
    proc = subprocess.run(["node", "-e", node_test], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0 or "NODE_VIP_FILTER_PASS" not in proc.stdout:
        failures.append(f"Node runtime test failed: {(proc.stderr or proc.stdout).strip()}")

    if failures:
        print(f"FAIL ({len(failures)} checks failed):")
        for item in failures:
            print(f"  - {item}")
        return 1

    print("ALL CHECKS PASSED: admin/customers.html & Top 5 VIP filter verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run verification scripts to verify RED failure**

Run:
- `python scripts/verify_admin_customers_and_vip_filter.py`
- `python scripts/verify_admin_order_links.py`
Expected: Both exit `1`.

- [ ] **Step 3: Update `admin/customers.html`**

Apply the exact changes to `admin/customers.html`:
1. Line 6: `<title>Quản Lý Khách Hàng | ENERGY BOOST ADMIN</title>`
2. Lines 54–56: `<h1>QUẢN LÝ <span>KHÁCH HÀNG</span></h1>`
3. Line 110–116:
```html
          <div class="admin-filter-actions">
            <button type="button" id="btn-filter-top5-vip" class="filter-pill" onclick="toggleTop5VipFilter(this)">
              <i class="fas fa-crown" style="color: var(--accent-gold);"></i> Lọc 5 Người VIP Nhất
            </button>
            <button type="button" class="btn-filter-apply" onclick="applyAdminCustomerFilter()">
              <i class="fas fa-chart-line"></i> Thống Kê
            </button>
            <button type="button" class="btn-filter-reset" onclick="resetAdminCustomerFilter()">
              <i class="fas fa-rotate-left"></i> Đặt Lại
            </button>
          </div>
```
4. Line 125: `<th>Đơn Gần Đây</th>`
5. Rows `#1`–`#5` (`data-vip-rank="1"`..`"5"`): wrap each `<strong>Tên</strong>` in `<a href="customer-detail.html" style="color: inherit; text-decoration: none;" title="Xem hồ sơ & lịch sử thanh toán của Nguyễn Văn An"><strong>...</strong></a>`, keep `#EB-XXXX` link(s) (`openOrderDetailModal`) inside `cells[3]` AND add `<div style="margin-top: 6px;"><a href="customer-detail.html" class="btn-view-detail" style="padding: 3px 10px; font-size: 0.76rem; text-decoration: none;" title="Xem lịch sử thanh toán của Nguyễn Văn An"><i class="fas fa-receipt"></i> Chi Tiết</a></div>`.
6. Add row `#6` (`data-vip-rank="6"`) inside `<tbody>` right after `#5 Vũ Thảo My`:
```html
            <!-- #6: Hoàng Đức Long -->
            <tr data-vip-rank="6">
              <td><span class="badge-status" style="background: rgba(148,163,184,0.16); color: #CBD5E1; border: 1px solid #64748B; font-weight: 800;">#6 BẠC</span></td>
              <td><a href="customer-detail.html" style="color: inherit; text-decoration: none;" title="Xem hồ sơ & lịch sử thanh toán của Nguyễn Văn An"><strong>Hoàng Đức Long</strong></a><br><small style="color: var(--text-muted);">long_hoang (BẠC)</small></td>
              <td>0938.222.111<br><small style="color: var(--text-dim);">duclong.hoang@gmail.com</small></td>
              <td>
                <a href="order-detail.html?id=EB-8806" onclick="openOrderDetailModal('EB-8806'); return false;" style="color: var(--primary); font-weight: 700; text-decoration: underline;">#EB-8806</a>: 24.000đ
                <div style="margin-top: 6px;"><a href="customer-detail.html" class="btn-view-detail" style="padding: 3px 10px; font-size: 0.76rem; text-decoration: none;" title="Xem lịch sử thanh toán của Nguyễn Văn An"><i class="fas fa-receipt"></i> Chi Tiết</a></div>
              </td>
              <td><strong style="color: var(--primary); font-size: 1.05rem;">4.100.000đ</strong></td>
              <td><span class="badge-status success">ĐANG HOẠT ĐỘNG</span></td>
              <td>
                <button class="btn-view-detail" style="padding: 4px 8px; font-size: 0.8rem;" onclick="openEditUserModal('long', this)" title="Sửa"><i class="fas fa-edit"></i> Sửa</button>
                <button class="btn-action-lock" onclick="toggleLockUser(this, 'Hoàng Đức Long')" title="Khoá"><i class="fas fa-lock"></i> Khoá</button>
              </td>
            </tr>
```
7. Remove `#modal-customer-detail` (`lines 285-350`) from `admin/customers.html`.

- [ ] **Step 4: Update `js/app.js` customer filter & custom user row templates**

1. Replace `applyAdminCustomerFilter` & `resetAdminCustomerFilter` (`js/app.js:2375-2392`) with:
```javascript
let isTop5VipFilterActive = false;

function filterCustomersTableRows() {
  const rows = document.querySelectorAll('#customers-table tbody tr');
  if (!rows || !rows.length) return;
  const tierEl = document.getElementById('filter-customer-tier');
  const tierVal = tierEl ? tierEl.value : 'all';
  const kwEl = document.getElementById('filter-customer-keyword');
  const kw = kwEl ? kwEl.value.trim().toLowerCase() : '';

  const tierKeywords = {
    diamond: 'kim cương',
    gold: 'vàng',
    silver: 'bạc',
  };

  rows.forEach((row) => {
    const rankAttr = parseInt(row.getAttribute('data-vip-rank') || '99', 10);
    const text = (row.textContent || '').toLowerCase();
    const matchTop5 = !isTop5VipFilterActive || (rankAttr >= 1 && rankAttr <= 5);
    const matchTier = tierVal === 'all' || (tierKeywords[tierVal] && text.includes(tierKeywords[tierVal]));
    const matchKw = !kw || text.includes(kw);
    row.style.display = (matchTop5 && matchTier && matchKw) ? '' : 'none';
  });
}

function toggleTop5VipFilter(btn) {
  isTop5VipFilterActive = !isTop5VipFilterActive;
  const targetBtn = btn || document.getElementById('btn-filter-top5-vip');
  if (targetBtn && targetBtn.classList) {
    targetBtn.classList.toggle('active', isTop5VipFilterActive);
  }
  filterCustomersTableRows();
  showToast(
    isTop5VipFilterActive
      ? 'Đang lọc hiển thị 5 người VIP chi tiêu cao nhất!'
      : 'Đang hiển thị toàn bộ danh sách khách hàng.',
    isTop5VipFilterActive ? 'success' : 'info'
  );
}

function applyAdminCustomerFilter() {
  const tierEl = document.getElementById('filter-customer-tier');
  const tier = tierEl ? tierEl.options[tierEl.selectedIndex].text : 'Tất cả';
  const fromEl = document.getElementById('stat-customer-from');
  const toEl = document.getElementById('stat-customer-to');
  const from = fromEl ? fromEl.value : '2026-01-01';
  const to = toEl ? toEl.value : '2026-10-17';

  filterCustomersTableRows();
  showToast('Đã thống kê khách hàng (' + from + ' đến ' + to + ') - Phân loại: ' + tier, 'success');
}

function resetAdminCustomerFilter() {
  isTop5VipFilterActive = false;
  const top5Btn = document.getElementById('btn-filter-top5-vip');
  if (top5Btn && top5Btn.classList) top5Btn.classList.remove('active');
  const tierEl = document.getElementById('filter-customer-tier');
  if (tierEl) tierEl.value = 'all';
  const kwEl = document.getElementById('filter-customer-keyword');
  if (kwEl) kwEl.value = '';
  filterCustomersTableRows();
  showToast('Đã đặt lại bộ lọc khách hàng', 'info');
}
```
2. Update `saveAddUser` (`js/app.js:2524-2526`):
```javascript
        <td><a href="customer-detail.html" style="color: inherit; text-decoration: none;" title="Xem hồ sơ & lịch sử thanh toán của Nguyễn Văn An"><strong>${fullname}</strong></a><br><small style="color: var(--text-muted);">${username} (${role.toUpperCase()})</small></td>
        <td>${phone}<br><small style="color: var(--text-dim);">${email}</small></td>
        <td><span style="color: var(--text-muted);">0 đơn hàng (Mới tạo)</span><div style="margin-top: 6px;"><a href="customer-detail.html" class="btn-view-detail" style="padding: 3px 10px; font-size: 0.76rem; text-decoration: none;"><i class="fas fa-receipt"></i> Chi Tiết</a></div></td>
```
3. Update `initCustomUsersTable` (`js/app.js:2637-2639`):
```javascript
        <td><a href="customer-detail.html" style="color: inherit; text-decoration: none;" title="Xem hồ sơ & lịch sử thanh toán của Nguyễn Văn An"><strong>${u.fullname || 'Người Dùng Mới'}</strong></a><br><small style="color: var(--text-muted);">${u.username || 'user'} (${(u.role || 'user').toUpperCase()})</small></td>
        <td>${u.phone || '0938.222.111'}<br><small style="color: var(--text-dim);">${u.email || 'user@energyboost.vn'}</small></td>
        <td><span style="color: var(--text-muted);">${u.orders || '0 đơn hàng (Mới tạo)'}</span><div style="margin-top: 6px;"><a href="customer-detail.html" class="btn-view-detail" style="padding: 3px 10px; font-size: 0.76rem; text-decoration: none;"><i class="fas fa-receipt"></i> Chi Tiết</a></div></td>
```

- [ ] **Step 5: Run full regression suite & commit Task 3 locally**

Run:
- `node --check js/app.js`
- `python scripts/verify_admin_customers_and_vip_filter.py`
- `python scripts/verify_admin_customer_detail_page.py`
- `python scripts/verify_admin_sidebar_and_orders_customer_links.py`
- `python scripts/verify_admin_order_links.py`
- `python scripts/verify_admin_ui_mockup.py`
- `python scripts/verify_rubric_coverage.py`
- `python scripts/verify_unconstrained_add_user.py`
- `python scripts/verify_footer_sync.py`
- `python verify_implementation.py`
- All `scripts/verify_*.py` scripts (Expected: 0 failures)

```bash
git add scripts/verify_admin_customers_and_vip_filter.py scripts/verify_admin_order_links.py admin/customers.html js/app.js
git commit -m "feat(admin): rename to 'Khách Hàng', add Top 5 VIP filter, 'Đơn Gần Đây' + 'Chi Tiết' links"
```
