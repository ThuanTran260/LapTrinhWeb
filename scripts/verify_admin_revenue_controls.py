import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent


def extract_css_blocks(css_text: str, selector: str) -> list[str]:
    pattern = rf"(?:^|\n)\s*{re.escape(selector)}\s*\{{([^}}]*)\}}"
    return re.findall(pattern, css_text)


def extract_media_blocks(css_text: str, query_fragment: str) -> list[str]:
    blocks: list[str] = []
    for match in re.finditer(rf"@media[^{{]*{re.escape(query_fragment)}[^{{]*\{{", css_text):
        depth = 0
        start = match.end()
        for idx in range(match.end() - 1, len(css_text)):
            ch = css_text[idx]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    blocks.append(css_text[start:idx])
                    break
    return blocks


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


def verify_revenue_html(rev_html: str) -> list[str]:
    failures: list[str] = []

    if (
        'id="revenue-period-subtitle"' not in rev_html
        or "Số liệu tổng hợp báo cáo - 6 tháng gần nhất năm 2026" not in rev_html
    ):
        failures.append(
            "admin/revenue.html: missing #revenue-period-subtitle with default 2026 6-month subtitle"
        )

    filter_bar_match = re.search(
        r'<div[^>]*id="revenue-filter-bar"[^>]*>([\s\S]*?)</div>\s*<!-- KPI Stat Cards -->',
        rev_html,
    )
    if not filter_bar_match:
        failures.append("admin/revenue.html: missing #revenue-filter-bar above KPI Stat Cards")
    else:
        filter_bar = filter_bar_match.group(0)
        if 'onclick="applyAdminRevenueFilter()"' not in filter_bar:
            failures.append("admin/revenue.html: #revenue-filter-bar missing applyAdminRevenueFilter() button")
        if 'onclick="resetAdminRevenueFilter()"' not in filter_bar:
            failures.append("admin/revenue.html: #revenue-filter-bar missing resetAdminRevenueFilter() button")

        quarter_match = re.search(
            r'<select[^>]*id="filter-revenue-quarter"[^>]*>([\s\S]*?)</select>',
            filter_bar,
        )
        if not quarter_match:
            failures.append("admin/revenue.html: missing #filter-revenue-quarter select")
        else:
            if "admin-filter-select" not in quarter_match.group(0):
                failures.append("admin/revenue.html: #filter-revenue-quarter missing .admin-filter-select class")
            quarter_values = re.findall(r'<option\s+value="([^"]+)"', quarter_match.group(1))
            expected_quarters = ["6m", "q1", "q2", "q3", "q4", "year"]
            if quarter_values != expected_quarters:
                failures.append(
                    f"admin/revenue.html: #filter-revenue-quarter options {quarter_values} != {expected_quarters}"
                )
            if not re.search(r'<option\s+value="6m"\s+selected>', quarter_match.group(1)):
                failures.append("admin/revenue.html: #filter-revenue-quarter '6m' option should be selected by default")

        year_match = re.search(
            r'<select[^>]*id="filter-revenue-year"[^>]*>([\s\S]*?)</select>',
            filter_bar,
        )
        if not year_match:
            failures.append("admin/revenue.html: missing #filter-revenue-year select")
        else:
            if "admin-filter-select" not in year_match.group(0):
                failures.append("admin/revenue.html: #filter-revenue-year missing .admin-filter-select class")
            year_values = re.findall(r'<option\s+value="([^"]+)"', year_match.group(1))
            expected_years = ["2026", "2025", "2024"]
            if year_values != expected_years:
                failures.append(
                    f"admin/revenue.html: #filter-revenue-year options {year_values} != {expected_years}"
                )
            if not re.search(r'<option\s+value="2026"\s+selected>', year_match.group(1)):
                failures.append("admin/revenue.html: #filter-revenue-year '2026' option should be selected by default")

        if not re.search(r'<input[^>]*type="date"[^>]*id="filter-revenue-date-from"[^>]*value="2026-04-01"', filter_bar):
            failures.append("admin/revenue.html: missing date input #filter-revenue-date-from (value='2026-04-01')")
        if not re.search(r'<input[^>]*type="date"[^>]*id="filter-revenue-date-to"[^>]*value="2026-09-30"', filter_bar):
            failures.append("admin/revenue.html: missing date input #filter-revenue-date-to (value='2026-09-30')")

    kpi_cards = re.findall(r'<div class="kpi-card">', rev_html)
    if len(kpi_cards) != 3:
        failures.append(f"admin/revenue.html: expected 3 .kpi-card blocks intact, found {len(kpi_cards)}")

    months = ["04/2026", "05/2026", "06/2026", "07/2026", "08/2026", "09/2026"]
    chart_match = re.search(
        r'DOANH THU 6 THÁNG GẦN NHẤT[\s\S]*?</section>',
        rev_html,
    )
    if not chart_match:
        failures.append("admin/revenue.html: missing 'DOANH THU 6 THÁNG GẦN NHẤT' bar chart section")
    else:
        for month in months:
            if f"<span>{month}</span>" not in chart_match.group(0):
                failures.append(f"admin/revenue.html: bar chart missing month '{month}'")

    tbody_match = re.search(r'CHI TIẾT TỪNG THÁNG[\s\S]*?<tbody>([\s\S]*?)</tbody>', rev_html)
    if not tbody_match:
        failures.append("admin/revenue.html: missing 'CHI TIẾT TỪNG THÁNG' table tbody")
    else:
        rows = re.findall(r'<tr>[\s\S]*?</tr>', tbody_match.group(1))
        if len(rows) != 6:
            failures.append(f"admin/revenue.html: expected 6 monthly detail rows intact, found {len(rows)}")
        for month in months:
            if f"<strong>{month}</strong>" not in tbody_match.group(1):
                failures.append(f"admin/revenue.html: monthly detail table missing row '{month}'")

    footer_match = re.search(
        r'<div class="revenue-pagination-footer">([\s\S]*?)</div>\s*</section>',
        rev_html,
    )
    if not footer_match:
        failures.append("admin/revenue.html: missing .revenue-pagination-footer")
    else:
        footer_html = footer_match.group(0)
        if 'id="revenue-pagination-summary"' not in footer_html:
            failures.append("admin/revenue.html: missing #revenue-pagination-summary")
        if "Đang hiển thị Trang 1/3" not in footer_html:
            failures.append("admin/revenue.html: #revenue-pagination-summary missing initial 'Đang hiển thị Trang 1/3'")

        pag_match = re.search(
            r'<div id="revenue-pagination"[^>]*>([\s\S]*?)</div>',
            footer_html,
        )
        if not pag_match:
            failures.append("admin/revenue.html: missing #revenue-pagination container")
        else:
            pag_html = pag_match.group(1)
            btns = re.findall(r'<button[^>]*class="[^"]*page-btn[^"]*"[^>]*>', pag_html)
            pages = re.findall(r'data-page="([^"]+)"', pag_html)
            if len(btns) != 5 or pages != ["prev", "1", "2", "3", "next"]:
                failures.append(
                    f"admin/revenue.html: #revenue-pagination buttons mismatch (count={len(btns)}, data-page={pages})"
                )
            for expected_call in (
                "handleRevenuePage('prev', this)",
                "handleRevenuePage(1, this)",
                "handleRevenuePage(2, this)",
                "handleRevenuePage(3, this)",
                "handleRevenuePage('next', this)",
            ):
                if expected_call not in pag_html:
                    failures.append(f"admin/revenue.html: #revenue-pagination missing onclick {expected_call}")

            prev_btn = re.search(r'<button[^>]*data-page="prev"[^>]*>', pag_html)
            if not prev_btn or "disabled" not in prev_btn.group(0):
                failures.append("admin/revenue.html: prev button must start disabled on page 1")

            page1_btn = re.search(r'<button[^>]*data-page="1"[^>]*>', pag_html)
            if (
                not page1_btn
                or "active" not in page1_btn.group(0)
                or 'aria-current="page"' not in page1_btn.group(0)
            ):
                failures.append("admin/revenue.html: page 1 button must start active with aria-current='page'")

    return failures


def verify_css_and_dashboard_selects(css_text: str, index_html: str) -> list[str]:
    failures: list[str] = []

    form_select_blocks = extract_css_blocks(css_text, ".admin-form-select")
    if not any("appearance: none" in b for b in form_select_blocks):
        failures.append("css/style.css: missing standalone .admin-form-select rule with appearance: none")
    else:
        block = next(b for b in form_select_blocks if "appearance: none" in b)
        for token in (
            "color-scheme: dark;",
            "appearance: none;",
            "-webkit-appearance: none;",
            "background-image: url(\"data:image/svg+xml,",
            "padding: 10px 38px 10px 14px;",
            "background-position: right 14px center;",
        ):
            if token not in block:
                failures.append(f"css/style.css: .admin-form-select missing '{token}'")

    filter_select_blocks = extract_css_blocks(css_text, ".admin-filter-select")
    if not any("appearance: none" in b for b in filter_select_blocks):
        failures.append("css/style.css: missing standalone .admin-filter-select rule with appearance: none")
    else:
        block = next(b for b in filter_select_blocks if "appearance: none" in b)
        for token in (
            "color-scheme: dark;",
            "appearance: none;",
            "-webkit-appearance: none;",
            "background-image: url(\"data:image/svg+xml,",
            "padding: 7px 36px 7px 14px;",
            "background-position: right 12px center;",
        ):
            if token not in block:
                failures.append(f"css/style.css: .admin-filter-select missing '{token}'")

    compact_blocks = extract_css_blocks(css_text, ".admin-filter-select.admin-filter-select--compact")
    if not compact_blocks:
        compact_blocks = extract_css_blocks(css_text, ".admin-filter-select--compact")
    if not compact_blocks:
        failures.append("css/style.css: missing .admin-filter-select--compact rule")
    else:
        block = compact_blocks[0]
        for token in (
            "padding: 5px 32px 5px 12px;",
            "background-position: right 10px center;",
            "font-size: 0.8rem;",
        ):
            if token not in block:
                failures.append(f"css/style.css: .admin-filter-select--compact missing '{token}'")

    if not extract_css_blocks(css_text, ".revenue-pagination-footer"):
        failures.append("css/style.css: missing .revenue-pagination-footer rule")
    if not extract_css_blocks(css_text, ".revenue-pagination-summary"):
        failures.append("css/style.css: missing .revenue-pagination-summary rule")

    mobile_blocks = extract_media_blocks(css_text, "640px")
    if not any(".revenue-pagination-footer" in b and "justify-content: center" in b for b in mobile_blocks):
        failures.append(
            "css/style.css: missing .revenue-pagination-footer centered responsive rule inside @media (max-width: 640px)"
        )

    for select_id in ("dash-order-status", "dash-inv-brand"):
        select_match = re.search(rf'<select[^>]*id="{select_id}"[^>]*>', index_html)
        if not select_match:
            failures.append(f"admin/index.html: missing #{select_id} select")
            continue
        tag = select_match.group(0)
        if "admin-filter-select" not in tag or "admin-filter-select--compact" not in tag:
            failures.append(
                f"admin/index.html: #{select_id} must apply both 'admin-filter-select' and 'admin-filter-select--compact'"
            )
        if "padding: 5px 10px" in tag:
            failures.append(
                f"admin/index.html: #{select_id} must NOT have inline 'padding: 5px 10px' overriding chevron spacing"
            )

    return failures


def verify_js_static(app_js: str) -> list[str]:
    failures: list[str] = []
    for fn_name in ("applyAdminRevenueFilter", "resetAdminRevenueFilter", "handleRevenuePage"):
        if not extract_function(app_js, fn_name):
            failures.append(f"js/app.js: missing function {fn_name}")
        if f"window.{fn_name} = {fn_name}" not in app_js:
            failures.append(f"js/app.js: missing window.{fn_name} export")
    return failures


def main() -> int:
    failures: list[str] = []

    rev_html = (ROOT / "admin" / "revenue.html").read_text(encoding="utf-8")
    css_text = (ROOT / "css" / "style.css").read_text(encoding="utf-8")
    index_html = (ROOT / "admin" / "index.html").read_text(encoding="utf-8")
    app_js = (ROOT / "js" / "app.js").read_text(encoding="utf-8")

    failures.extend(verify_revenue_html(rev_html))
    failures.extend(verify_css_and_dashboard_selects(css_text, index_html))
    failures.extend(verify_js_static(app_js))

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
      return Math.max(0, opts.findIndex((o) => o.value === val));
    },
  };
}

function makePageButton(pageVal, initialClasses, initialDisabled, initialAriaCurrent) {
  const classes = new Set(initialClasses);
  const attrs = { 'data-page': String(pageVal) };
  if (initialAriaCurrent) attrs['aria-current'] = initialAriaCurrent;
  return {
    disabled: !!initialDisabled,
    classList: {
      toggle: (c, force) => {
        if (force === undefined) {
          if (classes.has(c)) classes.delete(c);
          else classes.add(c);
        } else if (force) {
          classes.add(c);
        } else {
          classes.delete(c);
        }
      },
      add: (c) => classes.add(c),
      remove: (c) => classes.delete(c),
      contains: (c) => classes.has(c),
    },
    getAttribute: (name) => (Object.prototype.hasOwnProperty.call(attrs, name) ? attrs[name] : null),
    setAttribute: (name, value) => { attrs[name] = String(value); },
    removeAttribute: (name) => { delete attrs[name]; },
    _classes: classes,
    _attrs: attrs,
  };
}

const quarterSelect = makeSelect([
  ['6m', '6 tháng gần nhất (04–09/2026)'],
  ['q1', 'Quý 1 (Tháng 01 – 03)'],
  ['q2', 'Quý 2 (Tháng 04 – 06)'],
  ['q3', 'Quý 3 (Tháng 07 – 09)'],
  ['q4', 'Quý 4 (Tháng 10 – 12)'],
  ['year', 'Cả năm (12 tháng)'],
], '6m');

const yearSelect = makeSelect([
  ['2026', 'Năm 2026'],
  ['2025', 'Năm 2025'],
  ['2024', 'Năm 2024'],
], '2026');

const dateFromInput = { value: '2026-04-01' };
const dateToInput = { value: '2026-09-30' };
const subtitleEl = { textContent: 'Số liệu tổng hợp báo cáo - 6 tháng gần nhất năm 2026' };
const summaryEl = { textContent: 'Đang hiển thị Trang 1/3 — 6 tháng gần nhất (04/2026–09/2026)' };

const btnPrev = makePageButton('prev', ['page-btn', 'disabled'], true, null);
const btn1 = makePageButton('1', ['page-btn', 'active'], false, 'page');
const btn2 = makePageButton('2', ['page-btn'], false, null);
const btn3 = makePageButton('3', ['page-btn'], false, null);
const btnNext = makePageButton('next', ['page-btn'], false, null);
const pageButtons = [btnPrev, btn1, btn2, btn3, btnNext];

const paginationStrip = {
  querySelector: (sel) => {
    if (sel === '.page-btn.active[data-page]') {
      return pageButtons.find((b) => b.classList.contains('active') && b.getAttribute('data-page') !== null) || null;
    }
    return null;
  },
  querySelectorAll: (sel) => (sel === '.page-btn[data-page]' ? pageButtons : []),
};

const elements = {
  'filter-revenue-quarter': quarterSelect,
  'filter-revenue-year': yearSelect,
  'filter-revenue-date-from': dateFromInput,
  'filter-revenue-date-to': dateToInput,
  'revenue-period-subtitle': subtitleEl,
  'revenue-pagination-summary': summaryEl,
  'revenue-pagination': paginationStrip,
};

const toasts = [];
const sandbox = {
  console,
  URLSearchParams,
  window: { location: { pathname: '/admin/revenue.html', search: '' }, addEventListener: () => {} },
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
    setItem: () => {},
  },
};

vm.createContext(sandbox);
vm.runInContext(appCode, sandbox);
sandbox.showToast = (msg, type) => toasts.push({ msg, type });

// 1. applyAdminRevenueFilter updates #revenue-period-subtitle with date range and emits success toast (no mock/static wording)
toasts.length = 0;
quarterSelect.value = 'q3';
yearSelect.value = '2025';
dateFromInput.value = '2025-07-01';
dateToInput.value = '2025-09-30';
sandbox.applyAdminRevenueFilter();

if (!subtitleEl.textContent.includes('Quý 3 (Tháng 07 – 09)') || !subtitleEl.textContent.includes('Năm 2025') || !subtitleEl.textContent.includes('2025-07-01') || subtitleEl.textContent.includes('Mô phỏng tĩnh')) {
  throw new Error(`Unexpected subtitle after applyAdminRevenueFilter: ${subtitleEl.textContent}`);
}
if (toasts.length !== 1 || toasts[0].type !== 'success' || !toasts[0].msg.includes('Quý 3 (Tháng 07 – 09)') || !toasts[0].msg.includes('2025-07-01') || toasts[0].msg.includes('Mô phỏng tĩnh')) {
  throw new Error(`Unexpected toast after applyAdminRevenueFilter: ${JSON.stringify(toasts)}`);
}

// 2. resetAdminRevenueFilter resets selects & dates to 6m/2026 (2026-04-01..2026-09-30), restores subtitle, and emits info toast
toasts.length = 0;
sandbox.resetAdminRevenueFilter();

if (quarterSelect.value !== '6m' || yearSelect.value !== '2026' || dateFromInput.value !== '2026-04-01' || dateToInput.value !== '2026-09-30') {
  throw new Error(`Expected reset filter to 6m/2026 (2026-04-01..2026-09-30), got ${quarterSelect.value}/${yearSelect.value} ${dateFromInput.value}..${dateToInput.value}`);
}
if (subtitleEl.textContent !== 'Số liệu tổng hợp báo cáo - 6 tháng gần nhất năm 2026') {
  throw new Error(`Unexpected subtitle after resetAdminRevenueFilter: ${subtitleEl.textContent}`);
}
if (toasts.length !== 1 || toasts[0].type !== 'info') {
  throw new Error(`Unexpected toast after resetAdminRevenueFilter: ${JSON.stringify(toasts)}`);
}

function assertPageState(expectedPage) {
  const numericBtns = { 1: btn1, 2: btn2, 3: btn3 };
  for (const [pStr, btn] of Object.entries(numericBtns)) {
    const p = Number(pStr);
    const shouldBeActive = p === expectedPage;
    if (btn.classList.contains('active') !== shouldBeActive) {
      throw new Error(`Page ${p} active=${btn.classList.contains('active')}, expected ${shouldBeActive}`);
    }
    const aria = btn.getAttribute('aria-current');
    if (shouldBeActive && aria !== 'page') {
      throw new Error(`Expected aria-current='page' on page ${p}, got ${aria}`);
    }
    if (!shouldBeActive && aria !== null) {
      throw new Error(`Expected aria-current removed on page ${p}, got ${aria}`);
    }
  }

  const expectPrevDisabled = expectedPage <= 1;
  if (btnPrev.disabled !== expectPrevDisabled || btnPrev.classList.contains('disabled') !== expectPrevDisabled) {
    throw new Error(`On page ${expectedPage}, prev disabled mismatch: disabled=${btnPrev.disabled}, class=${btnPrev.classList.contains('disabled')}`);
  }
  const expectNextDisabled = expectedPage >= 3;
  if (btnNext.disabled !== expectNextDisabled || btnNext.classList.contains('disabled') !== expectNextDisabled) {
    throw new Error(`On page ${expectedPage}, next disabled mismatch: disabled=${btnNext.disabled}, class=${btnNext.classList.contains('disabled')}`);
  }
}

// 3. Pagination state machine across 1 -> 2 -> 3 -> prev -> next + boundary clamping
assertPageState(1);

// Boundary check: clicking prev on page 1 stays on page 1 with prev disabled
toasts.length = 0;
sandbox.handleRevenuePage('prev', btnPrev);
assertPageState(1);
if (!summaryEl.textContent.includes('Trang 1/3')) {
  throw new Error(`Unexpected summary on page 1 clamp: ${summaryEl.textContent}`);
}

// Transition 1 -> 2
toasts.length = 0;
sandbox.handleRevenuePage(2, btn2);
assertPageState(2);
if (summaryEl.textContent !== 'Đang hiển thị Trang 2/3' || summaryEl.textContent.includes('Mô phỏng tĩnh')) {
  throw new Error(`Unexpected summary on page 2: ${summaryEl.textContent}`);
}
if (toasts.length !== 1 || toasts[0].type !== 'info' || !toasts[0].msg.includes('Trang 2/3') || toasts[0].msg.includes('Mô phỏng tĩnh')) {
  throw new Error(`Unexpected toast on page 2: ${JSON.stringify(toasts)}`);
}

// Transition 2 -> 3
toasts.length = 0;
sandbox.handleRevenuePage(3, btn3);
assertPageState(3);
if (summaryEl.textContent !== 'Đang hiển thị Trang 3/3' || summaryEl.textContent.includes('Mô phỏng tĩnh')) {
  throw new Error(`Unexpected summary on page 3: ${summaryEl.textContent}`);
}
if (toasts.length !== 1 || toasts[0].type !== 'info' || !toasts[0].msg.includes('Trang 3/3') || toasts[0].msg.includes('Mô phỏng tĩnh')) {
  throw new Error(`Unexpected toast on page 3: ${JSON.stringify(toasts)}`);
}

// Boundary check: clicking next on page 3 stays on page 3 with next disabled
toasts.length = 0;
sandbox.handleRevenuePage('next', btnNext);
assertPageState(3);

// Transition 3 -> prev (page 2)
toasts.length = 0;
sandbox.handleRevenuePage('prev', btnPrev);
assertPageState(2);
if (!summaryEl.textContent.includes('Trang 2/3')) {
  throw new Error(`Unexpected summary after prev to page 2: ${summaryEl.textContent}`);
}

// Transition 2 -> next (page 3) with updated quarter filter label
quarterSelect.value = 'q4';
toasts.length = 0;
sandbox.handleRevenuePage('next', btnNext);
assertPageState(3);
if (!summaryEl.textContent.includes('Trang 3/3')) {
  throw new Error(`Unexpected summary after next to page 3: ${summaryEl.textContent}`);
}
if (toasts.length !== 1 || !toasts[0].msg.includes('Trang 3/3') || !toasts[0].msg.includes('Quý 4 (Tháng 10 – 12)')) {
  throw new Error(`Unexpected toast after next to page 3: ${JSON.stringify(toasts)}`);
}

// Transition back to page 1 via direct click
toasts.length = 0;
sandbox.handleRevenuePage(1, btn1);
assertPageState(1);
if (summaryEl.textContent !== 'Đang hiển thị Trang 1/3 — 6 tháng gần nhất (04/2026–09/2026)') {
  throw new Error(`Unexpected default page 1 summary: ${summaryEl.textContent}`);
}

console.log('NODE_REVENUE_CONTROLS_PASS');
"""

    proc = subprocess.run(
        ["node", "-e", node_test],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if proc.returncode != 0 or "NODE_REVENUE_CONTROLS_PASS" not in proc.stdout:
        failures.append(
            f"Node.js runtime test failed (exit {proc.returncode}): {(proc.stderr or proc.stdout).strip()}"
        )

    if failures:
        print(f"FAIL ({len(failures)} checks failed):")
        for item in failures:
            print(f"  - {item}")
        return 1

    print(
        "ALL CHECKS PASSED: admin/revenue.html filter/pagination, select chevron CSS alignment, and Node runtime verified."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
