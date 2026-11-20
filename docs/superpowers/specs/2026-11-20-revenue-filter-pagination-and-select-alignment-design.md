# Design Spec: Revenue Quarter/Year Filter & Pagination, Balanced Select Arrows, and Top-5 Buyer Button Wording

**Date:** 2026-11-20  
**Status:** Approved  
**Author:** AI Assistant  

---

## 1. Problem Statement & User Intent
Three coordinated Admin UX improvements are requested:
1. **Revenue reporting controls (`admin/revenue.html`, `css/style.css`, `js/app.js`):**
   - Add a `.admin-filter-bar` at the top (between `.admin-topbar` and `.kpi-grid`) with **two primary time controls** — **Kỳ / Quý** (`6 tháng gần nhất`, `Quý 1`–`Quý 4`, `Cả năm`) and **Năm** (`2026`, `2025`, `2024`) — plus `Áp Dụng` and `Đặt Lại` actions (**Approach 1**).
   - Add a `.pagination-strip` footer (`<` `1` `2` `3` `>`) with a compact period/page summary at the bottom of the `CHI TIẾT TỪNG THÁNG` section.
   - Follow **toast-only static simulation**: keep the 3 KPI cards, 6-month CSS bar chart, and 6-month table (`04/2026`–`09/2026`) untouched while updating active/disabled button states, `#revenue-period-subtitle`, `#revenue-pagination-summary`, and displaying descriptive `showToast(...)` feedback.
2. **Symmetrical `<select>` dropdown arrow alignment (`css/style.css`, `admin/index.html`):**
   - Native `<select>` styling on `.admin-filter-select` currently uses `padding: 7px 12px` without `appearance: none`, causing the left text padding (`~15px`) and right browser chevron margin (`~5px`) to appear noticeably off-balance.
   - Normalize `.admin-filter-select` and `.admin-form-select` with Baseline Widely Available CSS (`color-scheme: dark`, `appearance: none`, SVG chevron `background-image`, and balanced right padding/background-position) plus `.admin-filter-select--compact` for `#dash-order-status` and `#dash-inv-brand` in `admin/index.html`.
3. **Update Top-5 VIP button copy (`admin/customers.html`, `js/app.js`, `scripts/verify_admin_customers_and_vip_filter.py`):**
   - Change button label `Lọc 5 Người VIP Nhất` to `Lọc 5 Người Mua Nhiều Nhất` and update its activation toast in `toggleTop5VipFilter` to `'Đang lọc hiển thị 5 người mua nhiều nhất!'`, while preserving `#btn-filter-top5-vip` and section heading `TOP 5 KHÁCH HÀNG CHI TIÊU CAO NHẤT (SẮP XẾP GIẢM DẦN)` for rubric checks.

---

## 2. Architecture & Proposed Changes

### 2.1 Revenue Period Filter Bar & Bottom Pagination (`admin/revenue.html`)
- **Topbar subtitle (`admin/revenue.html:57`):**
  - Add `id="revenue-period-subtitle"` to `<p style="font-size: 0.85rem; color: var(--text-muted);">Số liệu tổng hợp báo cáo - 6 tháng gần nhất năm 2026</p>`.
- **Top Filter Bar (`#revenue-filter-bar`, inserted above `<!-- KPI Stat Cards -->` with `style="margin-bottom: 24px;"`):**
  - **Control 1 (`#filter-revenue-quarter`):**
    - Label: `<label class="admin-filter-label" for="filter-revenue-quarter"><i class="fas fa-calendar-check" style="color: var(--primary);"></i> Kỳ / Quý:</label>`
    - `<select id="filter-revenue-quarter" class="admin-filter-select">` with values:
      - `6m` (`selected`): `6 tháng gần nhất (04–09/2026)`
      - `q1`: `Quý 1 (Tháng 01 – 03)`
      - `q2`: `Quý 2 (Tháng 04 – 06)`
      - `q3`: `Quý 3 (Tháng 07 – 09)`
      - `q4`: `Quý 4 (Tháng 10 – 12)`
      - `year`: `Cả năm (12 tháng)`
  - **Control 2 (`#filter-revenue-year`):**
    - Label: `<label class="admin-filter-label" for="filter-revenue-year"><i class="fas fa-calendar-alt" style="color: var(--accent-cyan);"></i> Năm:</label>`
    - `<select id="filter-revenue-year" class="admin-filter-select">` with values `2026` (`selected`, `Năm 2026`), `2025` (`Năm 2025`), `2024` (`Năm 2024`).
  - **Actions (`.admin-filter-actions`):**
    - `<button type="button" class="btn-filter-apply" onclick="applyAdminRevenueFilter()"><i class="fas fa-chart-line"></i> Áp Dụng</button>`
    - `<button type="button" class="btn-filter-reset" onclick="resetAdminRevenueFilter()"><i class="fas fa-rotate-left"></i> Đặt Lại</button>`
- **Bottom Pagination (`#revenue-pagination`, inserted directly after `</table>` in `CHI TIẾT TỪNG THÁNG`):**
  - Container `<div class="revenue-pagination-footer">`:
    - `<p id="revenue-pagination-summary" class="revenue-pagination-summary">Đang hiển thị Trang 1/3 — 6 tháng gần nhất (04/2026–09/2026)</p>`
    - `<div id="revenue-pagination" class="pagination-strip" role="navigation" aria-label="Phân trang chi tiết doanh thu">` containing buttons:
      - `<button type="button" class="page-btn disabled" data-page="prev" aria-label="Trang trước" disabled onclick="handleRevenuePage('prev', this)"><i class="fas fa-chevron-left"></i></button>`
      - `<button type="button" class="page-btn active" data-page="1" aria-current="page" onclick="handleRevenuePage(1, this)">1</button>`
      - `<button type="button" class="page-btn" data-page="2" onclick="handleRevenuePage(2, this)">2</button>`
      - `<button type="button" class="page-btn" data-page="3" onclick="handleRevenuePage(3, this)">3</button>` *(only the active button carries `aria-current="page"`; inactive buttons omit `aria-current`)*
      - `<button type="button" class="page-btn" data-page="next" aria-label="Trang sau" onclick="handleRevenuePage('next', this)"><i class="fas fa-chevron-right"></i></button>`

### 2.2 Symmetrical Select Chevron Alignment & Pagination Footer Styles (`css/style.css` & `admin/index.html`)
- **`css/style.css` — Custom Cross-Browser Select Arrow (`appearance: none` + `color-scheme: dark`):**
  - Keep `.admin-filter-select, .admin-filter-input` shared surface/border/focus rules cleanly intact.
  - Add dedicated rules for `.admin-filter-select` and `.admin-form-select`:
    - `color-scheme: dark;`
    - `appearance: none; -webkit-appearance: none; cursor: pointer;`
    - `background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12' fill='none'%3E%3Cpath d='M2.5 4.25L6 7.75L9.5 4.25' stroke='%23E2E8F0' stroke-width='1.7' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");`
    - `background-repeat: no-repeat;`
  - For `.admin-filter-select`: `padding: 7px 36px 7px 14px; background-position: right 12px center; background-size: 12px 12px;` (14px left text padding balances 12px right border-to-chevron spacing with a clean 12px gap before text).
  - For `.admin-filter-select.admin-filter-select--compact`: `padding: 5px 32px 5px 12px; background-position: right 10px center; font-size: 0.8rem;`
  - For `.admin-form-select`: `padding: 10px 38px 10px 14px; background-position: right 14px center; background-size: 12px 12px;`
- **`admin/index.html` (`L125` & `L285`):**
  - Replace inline `style="padding: 5px 10px; font-size: 0.8rem;"` on `#dash-order-status` and `#dash-inv-brand` with `class="admin-filter-select admin-filter-select--compact"` so the custom chevron never overlaps option labels.
- **`css/style.css` — Revenue Pagination Footer:**
  - Add `.revenue-pagination-footer` (`display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; margin-top: 20px; padding-top: 16px; border-top: 1px solid rgba(255, 255, 255, 0.06);`) and `.revenue-pagination-footer .pagination-strip { margin: 0; }` plus `.revenue-pagination-summary` (`font-size: 0.84rem; color: var(--text-muted); margin: 0;`), stacking centered cleanly at `<= 640px`.

### 2.3 Revenue JS Handlers & Top-5 Buyer Copy Update (`js/app.js` & `admin/customers.html`)
- **`js/app.js` — Revenue Filter & Pagination Handlers:**
  - `applyAdminRevenueFilter()`: reads selected option labels from `#filter-revenue-quarter` and `#filter-revenue-year`, updates `#revenue-period-subtitle` to `'Đang chọn kỳ: ' + quarterText + ' • ' + yearText + ' (Hiển thị dữ liệu mẫu 6 tháng 04–09/2026)'`, and calls `showToast('Đã áp dụng bộ lọc doanh thu: ' + quarterText + ' — ' + yearText + ' (Mô phỏng tĩnh, giữ nguyên dữ liệu 6 tháng gần nhất).', 'success')`.
  - `resetAdminRevenueFilter()`: resets `#filter-revenue-quarter` to `'6m'`, `#filter-revenue-year` to `'2026'`, restores `#revenue-period-subtitle` to `'Số liệu tổng hợp báo cáo - 6 tháng gần nhất năm 2026'`, and calls `showToast('Đã đặt lại bộ lọc doanh thu về mặc định (6 tháng gần nhất năm 2026).', 'info')`.
  - `handleRevenuePage(page, btn)`:
    - Reads current active page from `#revenue-pagination .page-btn.active` (`data-page`), computes target page (`prev` -> `current - 1`, `next` -> `current + 1`, else integer clamped to `[1, 3]`). No-ops cleanly if already at boundary.
    - Updates `.active` and `aria-current="page"` on numeric `.page-btn[data-page]`, and toggles `.disabled` + `disabled` property on `prev` (`target === 1`) and `next` (`target === 3`).
    - Updates `#revenue-pagination-summary` to `'Đang hiển thị Trang 1/3 — 6 tháng gần nhất (04/2026–09/2026)'` on page 1 or `'Đang hiển thị Trang ' + target + '/3 — Mô phỏng tĩnh (giữ nguyên 6 tháng 04/2026–09/2026)'` on pages 2–3.
    - Calls `showToast(...)` with `'info'` announcing the simulated page without changing the 6 chart bars or 6 table rows.
  - Attach `window.applyAdminRevenueFilter`, `window.resetAdminRevenueFilter`, and `window.handleRevenuePage`.
- **`admin/customers.html:110-112` & `js/app.js:2328-2333`:**
  - Update `#btn-filter-top5-vip` text from `Lọc 5 Người VIP Nhất` to `Lọc 5 Người Mua Nhiều Nhất`.
  - Update `toggleTop5VipFilter(btn)` active toast in `js/app.js` to `'Đang lọc hiển thị 5 người mua nhiều nhất!'`.

---

## 3. Verification Strategy
1. Update `scripts/verify_admin_customers_and_vip_filter.py` to expect `Lọc 5 Người Mua Nhiều Nhất` and `'5 người mua nhiều nhất'` while preserving all `#btn-filter-top5-vip` and `TOP 5 KHÁCH HÀNG` checks.
2. Add `scripts/verify_admin_revenue_controls.py` verifying:
   - Static HTML structure of `#revenue-filter-bar`, `#filter-revenue-quarter`, `#filter-revenue-year`, `#revenue-pagination`, `#revenue-pagination-summary`, and unchanged 6 chart bars + 6 table rows in `admin/revenue.html`.
   - CSS rules in `css/style.css` (`appearance: none`, `color-scheme: dark`, SVG `background-image`, balanced `padding-right`/`background-position` on `.admin-filter-select`, `.admin-filter-select--compact`, and `.admin-form-select`) and compact class usage in `admin/index.html`.
   - Node.js VM runtime checks covering `applyAdminRevenueFilter`, `resetAdminRevenueFilter`, `handleRevenuePage` (`1 -> 2 -> 3 -> prev -> next` + disabled boundary checks + unchanged DOM table/chart).
3. Run `node --check js/app.js`, `python verify_implementation.py`, and all `scripts/verify_*.py` scripts (`verify_admin_ui_mockup.py`, `verify_rubric_coverage.py`, `verify_order_detail_pages.py`, `verify_pages_deploy_ready.py`, etc.) confirming 0 failures.
4. Commit implementation changes locally without `git push`.
