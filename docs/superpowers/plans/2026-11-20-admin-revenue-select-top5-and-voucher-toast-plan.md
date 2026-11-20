# Admin Revenue Filter/Pagination, Select Chevron Alignment, Top-5 Buyer Copy & Unconstrained Voucher Toast Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a Quarter/Year filter bar and table pagination footer to `admin/revenue.html`, align `<select>` dropdown chevron arrows symmetrically across all Admin pages, update the Top-5 filter button copy in `admin/customers.html` to `Lọc 5 Người Mua Nhiều Nhất`, and remove validation constraints while making `#modal-add-voucher` strictly toast-only.

**Architecture:** All interactive controls follow the repository's static toast-only simulation model (`js/app.js` updates visual indicators/labels/active pagination states and emits `showToast(...)` without mutating mock charts, table rows, or voucher arrays). Select chevron alignment replaces browser-dependent native padding with Baseline Widely Available `color-scheme: dark`, `appearance: none`, an SVG `background-image`, and symmetrical right padding (`36px` / `38px` / `32px`). All 5 tasks touch completely disjoint file sets so they can execute cleanly in parallel.

**Tech Stack:** Static HTML5, Vanilla CSS3 (`css/style.css`), Vanilla JavaScript (`js/app.js`), Python 3 + Node.js (`vm`) verification scripts.

## Global Constraints

- Never mutate `MOCK_VOUCHERS_LIST`, `activeVoucherCode`, voucher chip DOM, or `#voucher-toggle-active` in `saveAddVoucher(e)`; add `novalidate` on `#form-add-voucher` and remove `required`, `min="1"`, and `<span class="req">*</span>` inside it.
- Keep all 3 KPI cards, 6 CSS bar chart rows, and 6 monthly detail rows (`04/2026`–`09/2026`) in `admin/revenue.html` visually and structurally intact when filtering or paginating.
- Preserve `#btn-filter-top5-vip` ID and section heading `TOP 5 KHÁCH HÀNG CHI TIÊU CAO NHẤT (SẮP XẾP GIẢM DẦN)` in `admin/customers.html` for rubric scripts (`verify_admin_ui_mockup.py`, `verify_rubric_coverage.py`).
- Preserve compact `<select>` height/font sizing in `admin/index.html` (`#dash-order-status`, `#dash-inv-brand`) while preventing text/chevron collision via `.admin-filter-select--compact`.
- Never execute `git push`; keep all commits strictly local.
- Never place raw double-curly braces (`{ {` joined) in Markdown docs (Jekyll/Liquid safety).

---

### Task 1: Add Top Quarter/Year Filter Bar & Bottom Pagination to `admin/revenue.html`

**Files:**
- Modify: `admin/revenue.html:52-75`, `admin/revenue.html:194-198`
- Verify against: `scripts/verify_admin_revenue_controls.py` (created in Task 5)

**Interfaces:**
- Produces DOM hooks consumed by Task 4 (`js/app.js`):
  - `#revenue-period-subtitle` (topbar `<p>`)
  - `#revenue-filter-bar` with `#filter-revenue-quarter` (`value` in `6m|q1|q2|q3|q4|year`), `#filter-revenue-year` (`2026|2025|2024`), `applyAdminRevenueFilter()`, `resetAdminRevenueFilter()`
  - `#revenue-pagination-summary`, `#revenue-pagination` with `.page-btn[data-page]` (`prev|1|2|3|next`) calling `handleRevenuePage(page, this)`

- [ ] **Step 1: Add `#revenue-period-subtitle` ID and insert `#revenue-filter-bar` between `.admin-topbar` and `.kpi-grid` in `admin/revenue.html`**

Update line 57 and lines 71-74 in `admin/revenue.html` cleanly using exact replacement targets:

```html
          <p id="revenue-period-subtitle" style="font-size: 0.85rem; color: var(--text-muted);">Số liệu tổng hợp báo cáo - 6 tháng gần nhất năm 2026</p>
```

And directly after `</div> <!-- end .admin-topbar -->` above `<!-- KPI Stat Cards -->`:

```html
      <!-- Revenue Quarter & Year Filter Bar -->
      <div class="admin-filter-bar" id="revenue-filter-bar" style="margin-bottom: 24px;">
        <div class="admin-filter-groups">
          <div class="admin-filter-group">
            <label class="admin-filter-label" for="filter-revenue-quarter"><i class="fas fa-calendar-check" style="color: var(--primary);"></i> Kỳ / Quý:</label>
            <select id="filter-revenue-quarter" class="admin-filter-select">
              <option value="6m" selected>6 tháng gần nhất (04–09/2026)</option>
              <option value="q1">Quý 1 (Tháng 01 – 03)</option>
              <option value="q2">Quý 2 (Tháng 04 – 06)</option>
              <option value="q3">Quý 3 (Tháng 07 – 09)</option>
              <option value="q4">Quý 4 (Tháng 10 – 12)</option>
              <option value="year">Cả năm (12 tháng)</option>
            </select>
          </div>

          <div class="admin-filter-group">
            <label class="admin-filter-label" for="filter-revenue-year"><i class="fas fa-calendar-alt" style="color: var(--accent-cyan);"></i> Năm:</label>
            <select id="filter-revenue-year" class="admin-filter-select">
              <option value="2026" selected>Năm 2026</option>
              <option value="2025">Năm 2025</option>
              <option value="2024">Năm 2024</option>
            </select>
          </div>
        </div>

        <div class="admin-filter-actions">
          <button type="button" class="btn-filter-apply" onclick="applyAdminRevenueFilter()">
            <i class="fas fa-chart-line"></i> Áp Dụng
          </button>
          <button type="button" class="btn-filter-reset" onclick="resetAdminRevenueFilter()">
            <i class="fas fa-rotate-left"></i> Đặt Lại
          </button>
        </div>
      </div>
```

- [ ] **Step 2: Add `.revenue-pagination-footer` after `</table>` inside `CHI TIẾT TỪNG THÁNG` (`admin/revenue.html:195-197`)**

```html
        <div class="revenue-pagination-footer">
          <p id="revenue-pagination-summary" class="revenue-pagination-summary">Đang hiển thị Trang 1/3 — 6 tháng gần nhất (04/2026–09/2026)</p>
          <div id="revenue-pagination" class="pagination-strip" role="navigation" aria-label="Phân trang chi tiết doanh thu">
            <button type="button" class="page-btn disabled" data-page="prev" aria-label="Trang trước" disabled onclick="handleRevenuePage('prev', this)"><i class="fas fa-chevron-left"></i></button>
            <button type="button" class="page-btn active" data-page="1" aria-current="page" onclick="handleRevenuePage(1, this)">1</button>
            <button type="button" class="page-btn" data-page="2" onclick="handleRevenuePage(2, this)">2</button>
            <button type="button" class="page-btn" data-page="3" onclick="handleRevenuePage(3, this)">3</button>
            <button type="button" class="page-btn" data-page="next" aria-label="Trang sau" onclick="handleRevenuePage('next', this)"><i class="fas fa-chevron-right"></i></button>
          </div>
        </div>
```

- [ ] **Step 3: Verify existing tests on `admin/revenue.html` still pass**

Run:
`python verify_implementation.py; python scripts/verify_order_detail_pages.py; python scripts/verify_footer_sync.py; python scripts/verify_admin_sidebar_and_orders_customer_links.py`
Expected: all exit 0.

- [ ] **Step 4: Commit Task 1**

```bash
git add admin/revenue.html
git commit -m "feat(admin): add quarter/year filter bar and table pagination to revenue report"
```

---

### Task 2: Align Select Chevron Arrows Symmetrically & Add Revenue Pagination Styles (`css/style.css` & `admin/index.html`)

**Files:**
- Modify: `css/style.css:1904-1916`, `css/style.css:4629-4634`, `css/style.css:4748-4763`, `css/style.css:5620-5636`
- Modify: `admin/index.html:125`, `admin/index.html:285`

**Interfaces:**
- Produces CSS rules for `.admin-filter-select`, `.admin-filter-select.admin-filter-select--compact`, `.admin-form-select`, and `.revenue-pagination-footer` / `.revenue-pagination-summary`.

- [ ] **Step 1: Add custom dark-themed SVG chevron & symmetrical padding to `.admin-form-select` (`css/style.css:1904-1916`)**

After the `.admin-form-input, .admin-form-select, .admin-form-textarea` rule at `css/style.css:1916`, insert:

```css
.admin-form-select {
  color-scheme: dark;
  appearance: none;
  -webkit-appearance: none;
  cursor: pointer;
  padding: 10px 38px 10px 14px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12' fill='none'%3E%3Cpath d='M2.5 4.25L6 7.75L9.5 4.25' stroke='%23E2E8F0' stroke-width='1.7' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 14px center;
  background-size: 12px 12px;
}
```

- [ ] **Step 2: Add symmetrical chevron styling to `.admin-filter-select` & `.admin-filter-select--compact` (`css/style.css:4748-4762`) and pagination footer styles (`css/style.css:4629-4634`, mobile `<= 640px` at `~5630`)**

Right after `.admin-filter-select:focus, .admin-filter-input:focus` (around `css/style.css:4762`):

```css
.admin-filter-select {
  color-scheme: dark;
  appearance: none;
  -webkit-appearance: none;
  cursor: pointer;
  padding: 7px 36px 7px 14px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12' fill='none'%3E%3Cpath d='M2.5 4.25L6 7.75L9.5 4.25' stroke='%23E2E8F0' stroke-width='1.7' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 12px 12px;
}
.admin-filter-select.admin-filter-select--compact {
  padding: 5px 32px 5px 12px;
  background-position: right 10px center;
  font-size: 0.8rem;
}
```

And right after `.page-btn.disabled` (around `css/style.css:4633`), add:

```css
.revenue-pagination-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}
.revenue-pagination-footer .pagination-strip {
  margin: 0;
}
.revenue-pagination-summary {
  font-size: 0.84rem;
  color: var(--text-muted);
  margin: 0;
}
```

And inside `@media (max-width: 640px)` (around `css/style.css:5635`), add:

```css
  .revenue-pagination-footer {
    justify-content: center;
    text-align: center;
  }
```

- [ ] **Step 3: Apply `.admin-filter-select--compact` on Dashboard compact selects (`admin/index.html:125` and `admin/index.html:285`)**

Replace `class="admin-filter-select" style="padding: 5px 10px; font-size: 0.8rem;"` on `#dash-order-status` (`L125`) and `#dash-inv-brand` (`L285`) with `class="admin-filter-select admin-filter-select--compact"` so inline padding no longer squashes the custom right chevron onto option labels.

- [ ] **Step 4: Run CSS & dashboard checks**

Run:
`python verify_implementation.py; python scripts/verify_admin_inventory_can_links.py; python scripts/verify_admin_features_update.py`
Expected: all exit 0.

- [ ] **Step 5: Commit Task 2**

```bash
git add css/style.css admin/index.html
git commit -m "style(admin): center select dropdown chevrons symmetrically and style revenue pagination footer"
```

---

### Task 3: Rename Top-5 Button Copy in `admin/customers.html` & Remove Constraints in `admin/settings.html` Add Voucher Form

**Files:**
- Modify: `admin/customers.html:110-112`
- Modify: `admin/settings.html:546-590`

- [ ] **Step 1: Update Top-5 button wording (`admin/customers.html:110-112`)**

Keep `id="btn-filter-top5-vip"` and `onclick="toggleTop5VipFilter(this)"` unchanged; change button label text only:

```html
            <button type="button" id="btn-filter-top5-vip" class="filter-pill" onclick="toggleTop5VipFilter(this)">
              <i class="fas fa-crown" style="color: var(--accent-gold);"></i> Lọc 5 Người Mua Nhiều Nhất
            </button>
```

Keep `<h2 class="admin-section-title">...TOP 5 KHÁCH HÀNG CHI TIÊU CAO NHẤT (SẮP XẾP GIẢM DẦN)</h2>` untouched.

- [ ] **Step 2: Remove all validation limits & required constraints in `#form-add-voucher` (`admin/settings.html:546-589`)**

Update lines 546, 554-568, and 588 inside `#modal-add-voucher`:
- `<form id="form-add-voucher" onsubmit="saveAddVoucher(event)" novalidate>`
- `<label class="admin-form-label" for="add-voucher-code"><i class="fas fa-barcode"></i> Mã Code Voucher</label>` + `<input type="text" id="add-voucher-code" class="admin-form-input" placeholder="VD: SUMMER20, VIPBOOST" style="text-transform: uppercase;" />` (no `required`, no `<span class="req">*</span>`)
- `<label class="admin-form-label" for="add-voucher-type"><i class="fas fa-percent"></i> Loại Giảm Giá</label>` (no `<span class="req">*</span>`)
- `<label class="admin-form-label" for="add-voucher-amount"><i class="fas fa-tags"></i> Mức Giảm</label>` + `<input type="text" id="add-voucher-amount" class="admin-form-input" placeholder="VD: 15% hoặc 30.000đ" />` (no `required`, no `<span class="req">*</span>`)
- `<input type="text" id="add-voucher-limit" class="admin-form-input" placeholder="VD: 500" value="500" />` (changed from `type="number"` with `min="1"` to unconstrained `type="text"` without `min`)

- [ ] **Step 3: Run existing HTML verification scripts**

Run:
`python scripts/verify_order_detail_pages.py; python scripts/verify_admin_ui_mockup.py; python scripts/verify_rubric_coverage.py`
Expected: all exit 0.

- [ ] **Step 4: Commit Task 3**

```bash
git add admin/customers.html admin/settings.html
git commit -m "feat(admin): rename top-5 filter button copy and remove add-voucher form constraints"
```

---

### Task 4: Implement Revenue Handlers, Top-5 Buyer Toast & Toast-Only `saveAddVoucher` in `js/app.js`

**Files:**
- Modify: `js/app.js:2321-2334` (`toggleTop5VipFilter`), `js/app.js:2385` (insert revenue handlers), `js/app.js:2869-2929` (`saveAddVoucher`), `js/app.js:3253` (`window` exports)

- [ ] **Step 1: Update `toggleTop5VipFilter` active toast (`js/app.js:2328-2333`)**

```javascript
  showToast(
    isTop5VipFilterActive
      ? 'Đang lọc hiển thị 5 người mua nhiều nhất!'
      : 'Đang hiển thị toàn bộ danh sách khách hàng.',
    isTop5VipFilterActive ? 'success' : 'info'
  );
```

- [ ] **Step 2: Add `applyAdminRevenueFilter`, `resetAdminRevenueFilter`, and `handleRevenuePage` right after `resetDashboardFilter` (`js/app.js:2385`)**

```javascript
function applyAdminRevenueFilter() {
  const quarterEl = document.getElementById('filter-revenue-quarter');
  const yearEl = document.getElementById('filter-revenue-year');
  const quarterText = (quarterEl && quarterEl.selectedIndex >= 0 && quarterEl.options[quarterEl.selectedIndex])
    ? quarterEl.options[quarterEl.selectedIndex].text.trim()
    : '6 tháng gần nhất (04–09/2026)';
  const yearText = (yearEl && yearEl.selectedIndex >= 0 && yearEl.options[yearEl.selectedIndex])
    ? yearEl.options[yearEl.selectedIndex].text.trim()
    : 'Năm 2026';

  const subtitleEl = document.getElementById('revenue-period-subtitle');
  if (subtitleEl) {
    subtitleEl.textContent = `Đang chọn kỳ: ${quarterText} • ${yearText} (Hiển thị dữ liệu mẫu 6 tháng 04–09/2026)`;
  }
  showToast(`Đã áp dụng bộ lọc doanh thu: ${quarterText} — ${yearText} (Mô phỏng tĩnh, giữ nguyên dữ liệu 6 tháng gần nhất).`, 'success');
}

function resetAdminRevenueFilter() {
  const quarterEl = document.getElementById('filter-revenue-quarter');
  const yearEl = document.getElementById('filter-revenue-year');
  if (quarterEl) quarterEl.value = '6m';
  if (yearEl) yearEl.value = '2026';

  const subtitleEl = document.getElementById('revenue-period-subtitle');
  if (subtitleEl) {
    subtitleEl.textContent = 'Số liệu tổng hợp báo cáo - 6 tháng gần nhất năm 2026';
  }
  showToast('Đã đặt lại bộ lọc doanh thu về mặc định (6 tháng gần nhất năm 2026).', 'info');
}

function handleRevenuePage(page, btn) {
  const strip = document.getElementById('revenue-pagination');
  const totalPages = 3;
  let currentPage = 1;

  if (strip) {
    const activeBtn = strip.querySelector('.page-btn.active[data-page]');
    const parsedActive = activeBtn ? parseInt(activeBtn.getAttribute('data-page'), 10) : 1;
    if (!Number.isNaN(parsedActive)) currentPage = parsedActive;
  }

  let targetPage = currentPage;
  if (page === 'prev') {
    targetPage = Math.max(1, currentPage - 1);
  } else if (page === 'next') {
    targetPage = Math.min(totalPages, currentPage + 1);
  } else {
    const parsedTarget = parseInt(page, 10);
    if (!Number.isNaN(parsedTarget)) {
      targetPage = Math.min(totalPages, Math.max(1, parsedTarget));
    }
  }

  if (strip) {
    strip.querySelectorAll('.page-btn[data-page]').forEach((item) => {
      const val = item.getAttribute('data-page');
      if (val === 'prev') {
        const isFirst = targetPage <= 1;
        item.classList.toggle('disabled', isFirst);
        item.disabled = isFirst;
      } else if (val === 'next') {
        const isLast = targetPage >= totalPages;
        item.classList.toggle('disabled', isLast);
        item.disabled = isLast;
      } else {
        const isCurrent = parseInt(val, 10) === targetPage;
        item.classList.toggle('active', isCurrent);
        if (isCurrent) {
          item.setAttribute('aria-current', 'page');
        } else {
          item.removeAttribute('aria-current');
        }
      }
    });
  }

  const summaryEl = document.getElementById('revenue-pagination-summary');
  if (summaryEl) {
    summaryEl.textContent = targetPage === 1
      ? 'Đang hiển thị Trang 1/3 — 6 tháng gần nhất (04/2026–09/2026)'
      : `Đang hiển thị Trang ${targetPage}/3 — Mô phỏng tĩnh (giữ nguyên 6 tháng 04/2026–09/2026)`;
  }

  const quarterEl = document.getElementById('filter-revenue-quarter');
  const periodLabel = (quarterEl && quarterEl.selectedIndex >= 0 && quarterEl.options[quarterEl.selectedIndex])
    ? quarterEl.options[quarterEl.selectedIndex].text.trim()
    : '6 tháng gần nhất (04–09/2026)';
  showToast(`Đang xem Trang ${targetPage}/${totalPages} (${periodLabel}) — Mô phỏng tĩnh, giữ nguyên bảng 6 tháng mẫu.`, 'info');
}
```

- [ ] **Step 3: Replace `saveAddVoucher` (`js/app.js:2869-2929`) with pure toast-only implementation and export new helpers (`js/app.js:3253`)**

Replace `saveAddVoucher(e)` with:

```javascript
function saveAddVoucher(e) {
  if (e && e.preventDefault) e.preventDefault();
  const codeEl = document.getElementById('add-voucher-code');
  const rawCode = (codeEl && typeof codeEl.value === 'string') ? codeEl.value.trim() : '';
  const code = rawCode ? rawCode.toUpperCase() : 'VOUCHER MỚI';

  closeAdminModal('modal-add-voucher');
  showToast(`Đã tạo & kích hoạt mã Voucher "${code}" thành công (không ràng buộc)!`, 'success');
  const form = document.getElementById('form-add-voucher');
  if (form) form.reset();
}
```

And inside `if (typeof window !== 'undefined')` around line 3253, add:

```javascript
  window.applyAdminRevenueFilter = applyAdminRevenueFilter;
  window.resetAdminRevenueFilter = resetAdminRevenueFilter;
  window.handleRevenuePage = handleRevenuePage;
  window.saveAddVoucher = saveAddVoucher;
  window.toggleTop5VipFilter = toggleTop5VipFilter;
```

- [ ] **Step 4: Syntax-check `js/app.js` and run existing JS runtime verification scripts**

Run:
`node --check js/app.js; python scripts/verify_order_detail_pages.py; python scripts/verify_admin_features_update.py`
Expected: all exit 0.

- [ ] **Step 5: Commit Task 4**

```bash
git add js/app.js
git commit -m "feat(admin): add revenue filter/pagination handlers, top-5 buyer toast, and toast-only add voucher"
```

---

### Task 5: Update VIP Filter Test & Create Verification Scripts for Revenue Controls, Select Alignment & Toast-Only Add Voucher

**Files:**
- Modify: `scripts/verify_admin_customers_and_vip_filter.py:36-37`, `scripts/verify_admin_customers_and_vip_filter.py:195-202`
- Create: `scripts/verify_admin_revenue_controls.py`
- Create: `scripts/verify_admin_add_voucher_toast_only.py`

- [ ] **Step 1: Update `scripts/verify_admin_customers_and_vip_filter.py` assertions for `Lọc 5 Người Mua Nhiều Nhất`**

Update lines 36-37 and 195-201 in `scripts/verify_admin_customers_and_vip_filter.py` to expect `"Lọc 5 Người Mua Nhiều Nhất"` in `admin/customers.html` and `'5 người mua nhiều nhất'` in `toggleTop5VipFilter` toast output (while keeping `#btn-filter-top5-vip` and `TOP 5 KHÁCH HÀNG` checks intact).

- [ ] **Step 2: Create `scripts/verify_admin_revenue_controls.py`**

Verify:
1. `admin/revenue.html`: `#revenue-period-subtitle`, `#revenue-filter-bar`, `#filter-revenue-quarter` (6 options: `6m`, `q1`, `q2`, `q3`, `q4`, `year`), `#filter-revenue-year` (`2026`, `2025`, `2024`), `applyAdminRevenueFilter()`, `resetAdminRevenueFilter()`, `.revenue-pagination-footer`, `#revenue-pagination-summary`, `#revenue-pagination` (`prev`, `1`, `2`, `3`, `next`), plus all 6 bar items (`04/2026`..`09/2026`) and 6 detail rows intact.
2. `css/style.css` & `admin/index.html`: `.admin-filter-select` & `.admin-form-select` declare `appearance: none`, `color-scheme: dark`, `background-image`, symmetrical `padding: 7px 36px 7px 14px` / `background-position: right 12px center` and `padding: 10px 38px 10px 14px` / `background-position: right 14px center`, `.admin-filter-select--compact` exists and is applied to `#dash-order-status` and `#dash-inv-brand` without inline `padding: 5px 10px`.
3. Node.js VM runtime test exercising `applyAdminRevenueFilter()`, `resetAdminRevenueFilter()`, and `handleRevenuePage` across `1 -> 2 -> 3 -> prev -> next` plus boundary disabling (`prev` disabled on page 1, `next` disabled on page 3), verifying `showToast`, `#revenue-period-subtitle`, and `#revenue-pagination-summary` updates.

- [ ] **Step 3: Create `scripts/verify_admin_add_voucher_toast_only.py`**

Verify:
1. `admin/settings.html` `#form-add-voucher` has `novalidate`, zero `required` attributes inside the form block, zero `<span class="req">*</span>` inside the form block, and `#add-voucher-limit` has no `min="` restriction (`type="text"`).
2. `js/app.js` `saveAddVoucher` does not call `MOCK_VOUCHERS_LIST.unshift` or `renderVoucherChips`.
3. Node.js VM runtime test running `saveAddVoucher` both with empty inputs (`code = ''`) and unconstrained arbitrary inputs (`code = 'test'`, `limit = 'Không giới hạn'`), asserting `showToast(...)` fires, `closeAdminModal('modal-add-voucher')` runs, and `MOCK_VOUCHERS_LIST.length`, `activeVoucherCode`, chip DOM, and `#voucher-toggle-active.checked` stay 100% unmodified.

- [ ] **Step 4: Run all new and existing test suites**

Run:
`python scripts/verify_admin_customers_and_vip_filter.py; python scripts/verify_admin_revenue_controls.py; python scripts/verify_admin_add_voucher_toast_only.py; python verify_implementation.py`
Expected: all exit 0.

- [ ] **Step 5: Commit Task 5**

```bash
git add scripts/verify_admin_customers_and_vip_filter.py scripts/verify_admin_revenue_controls.py scripts/verify_admin_add_voucher_toast_only.py
git commit -m "test(admin): verify revenue filter/pagination, select alignment, top-5 wording, and toast-only add voucher"
```
