import re
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent


def check_html(failures: list[str]) -> None:
    targets = [
        ("admin/customers.html", "filter-customer-keyword", "customers"),
        ("admin/orders.html", "filter-order-keyword", "orders"),
        ("admin/inventory.html", "filter-inv-keyword", "products"),
        ("admin/index.html", "dash-order-keyword", "orders"),
        ("admin/index.html", "dash-inv-keyword", "products"),
    ]
    for rel_path, input_id, expected_mode in targets:
        html = (ROOT / rel_path).read_text(encoding="utf-8")
        inp_match = re.search(rf'<input\b[^>]*id="{re.escape(input_id)}"[^>]*>', html)
        if not inp_match:
            failures.append(f"{rel_path}: missing #{input_id}")
            continue
        tag = inp_match.group(0)
        if f'data-admin-dropdown="{expected_mode}"' not in tag:
            failures.append(f"{rel_path}: #{input_id} missing data-admin-dropdown=\"{expected_mode}\"")
        if 'autocomplete="off"' not in tag:
            failures.append(f"{rel_path}: #{input_id} missing autocomplete=\"off\"")
        for evt in ("onfocus=", "onclick=", "oninput="):
            if evt not in tag or "openAdminSearchDropdown(this)" not in tag:
                failures.append(f"{rel_path}: #{input_id} missing {evt}openAdminSearchDropdown(this)")
        dropdown_id = f"{input_id}-dropdown"
        if f'id="{dropdown_id}"' not in html or "admin-search-dropdown" not in html:
            failures.append(f"{rel_path}: missing #{dropdown_id}.admin-search-dropdown")
    for rel_path in ("admin/customers.html", "admin/orders.html", "admin/inventory.html", "admin/index.html"):
        html = (ROOT / rel_path).read_text(encoding="utf-8")
        if "../css/style.css?v=20261121-search-portal" not in html:
            failures.append(f"{rel_path}: missing updated style.css cache buster")
        if "../js/app.js?v=20261121-search-portal" not in html:
            failures.append(f"{rel_path}: missing updated app.js cache buster")


def check_css(failures: list[str]) -> None:
    css = (ROOT / "css" / "style.css").read_text(encoding="utf-8")
    if css.count("{") != css.count("}"):
        failures.append(f"css/style.css: unbalanced braces ({{={css.count('{')}, }}={css.count('}')})")
    for selector in (
        ".admin-search-dropdown",
        ".admin-search-dropdown.is-fixed",
        ".admin-search-dropdown.align-right",
        ".admin-dropdown-item",
        ".admin-dropdown-avatar",
        ".admin-dropdown-empty",
    ):
        if selector not in css:
            failures.append(f"css/style.css: missing selector '{selector}'")


def check_node_runtime(failures: list[str]) -> None:
    node_code = r"""
const fs = require('fs');
const assert = require('assert');
const vm = require('vm');
const path = require('path');

const appCode = fs.readFileSync(path.join(process.cwd(), 'js', 'app.js'), 'utf8');
const dashboardHtml = fs.readFileSync(path.join(process.cwd(), 'admin', 'index.html'), 'utf8');
const dashboardMenuIds = ['dash-order-keyword-dropdown', 'dash-inv-keyword-dropdown'];
const menuParents = new Map();
const tagStack = [];
const voidTags = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr']);
for (const [, closing, tagName, attrs] of dashboardHtml.replace(/<!--[\s\S]*?-->/g, '').matchAll(/<(\/?)([a-z][\w:-]*)\b([^>]*)>/gi)) {
  const tag = tagName.toLowerCase();
  if (closing) {
    const index = tagStack.lastIndexOf(tag);
    if (index >= 0) tagStack.length = index;
    continue;
  }
  const id = (attrs.match(/\bid="([^"]+)"/) || [])[1];
  if (dashboardMenuIds.includes(id)) {
    assert(!menuParents.has(id), `Duplicate dashboard menu #${id}`);
    menuParents.set(id, tagStack[tagStack.length - 1]);
  }
  if (!voidTags.has(tag) && !attrs.trimEnd().endsWith('/')) tagStack.push(tag);
}
for (const id of dashboardMenuIds) {
  assert.strictEqual(menuParents.get(id), 'body', `#${id} must start outside blurred dashboard panels`);
  assert(dashboardHtml.includes(`aria-controls="${id}"`), `Missing input/menu link for #${id}`);
}
for (const asset of ['../css/style.css', '../js/app.js']) {
  assert(dashboardHtml.includes(`${asset}?v=20261121-search-portal-dashboard"`), `Dashboard must refresh ${asset}`);
}
const toasts = [];
const documentListeners = {};
const windowListeners = {};

function makeClassList(initial = []) {
  const set = new Set(initial);
  return {
    add: (...classes) => classes.forEach((c) => set.add(c)),
    remove: (...classes) => classes.forEach((c) => set.delete(c)),
    toggle: (c, force) => (force === undefined ? (set.has(c) ? set.delete(c) : set.add(c)) : (force ? set.add(c) : set.delete(c))),
    contains: (c) => set.has(c),
    list: () => Array.from(set),
  };
}

function makeSearchGroup(inputId, mode) {
  const input = {
    id: inputId,
    value: '',
    getAttribute: (attr) => (attr === 'data-admin-dropdown' ? mode : null),
  };
  const dropdown = {
    id: `${inputId}-dropdown`,
    innerHTML: '',
    style: {},
    classList: makeClassList(['search-results-dropdown', 'admin-search-dropdown']),
  };
  const wrapper = {
    querySelector: (sel) => (sel.includes('input') ? input : (sel.includes('.admin-search-dropdown') && dropdown.parentElement === wrapper ? dropdown : null)),
    getBoundingClientRect: () => ({ left: 100, right: 300, top: 180, bottom: 220 }),
    closest: () => null,
  };
  dropdown.parentElement = wrapper;
  input.closest = (sel) => (sel === '.admin-filter-search' ? wrapper : null);
  return { input, dropdown, wrapper };
}

const custBox = makeSearchGroup('filter-customer-keyword', 'customers');
const orderBox = makeSearchGroup('filter-order-keyword', 'orders');
const prodBox = makeSearchGroup('filter-inv-keyword', 'products');
const dashboardOrderBox = makeSearchGroup('dash-order-keyword', 'orders');
const dashboardProductBox = makeSearchGroup('dash-inv-keyword', 'products');
const allDropdowns = [custBox.dropdown, orderBox.dropdown, prodBox.dropdown, dashboardOrderBox.dropdown, dashboardProductBox.dropdown];

const sandbox = {
  console,
  URLSearchParams,
  window: {
    innerWidth: 1280,
    innerHeight: 800,
    location: { pathname: '/admin/customers.html', search: '' },
    addEventListener: (type, handler) => { windowListeners[type] = handler; },
  },
  document: {
    readyState: 'loading',
    addEventListener: (type, handler) => { (documentListeners[type] ||= []).push(handler); },
    getElementById: (id) => allDropdowns.find((d) => d.id === id) || null,
    querySelector: () => null,
    querySelectorAll: (sel) => {
      if (sel === '.admin-search-dropdown.is-open') {
        return allDropdowns.filter((d) => d.classList.contains('is-open'));
      }
      return [];
    },
    body: { style: {}, appendChild: (child) => { child.parentElement = sandbox.document.body; } },
  },
  localStorage: { getItem: () => null, setItem: () => {}, removeItem: () => {} },
};
dashboardOrderBox.dropdown.parentElement = sandbox.document.body;
dashboardProductBox.dropdown.parentElement = sandbox.document.body;

vm.createContext(sandbox);
vm.runInContext(appCode, sandbox);
sandbox.showToast = (msg, type) => toasts.push({ msg, type });

// 1. Customers dropdown opens with 6 customers and uses fixed viewport positioning to avoid overflow clipping
sandbox.openAdminSearchDropdown(custBox.input);
if (!custBox.dropdown.classList.contains('is-open')) {
  throw new Error('Customers dropdown did not open');
}
if (!custBox.dropdown.classList.contains('is-fixed') || custBox.dropdown.style.top !== '226px' || custBox.dropdown.style.left !== '100px') {
  throw new Error(`Customers dropdown fixed positioning invalid: top=${custBox.dropdown.style.top}, left=${custBox.dropdown.style.left}`);
}
if (custBox.dropdown.parentElement !== sandbox.document.body) {
  throw new Error('Dropdown must escape blurred/scrollable sections by mounting in document.body');
}
for (const name of ['Phạm Minh Tuấn', 'Nguyễn Văn An', 'Trần Thị Bích', 'Lê Hoàng Nam', 'Vũ Thảo My', 'Hoàng Đức Long']) {
  if (!custBox.dropdown.innerHTML.includes(name)) {
    throw new Error(`Customers dropdown missing '${name}'`);
  }
}
if (!custBox.dropdown.innerHTML.includes('6 khách hàng')) {
  throw new Error('Customers dropdown missing count 6 khách hàng');
}

// 2. Filtering customers by accent-stripped query 'tuan' and non-matching 'ko'
custBox.input.value = 'tuan';
sandbox.openAdminSearchDropdown(custBox.input);
if (!custBox.dropdown.innerHTML.includes('Phạm Minh Tuấn') || custBox.dropdown.innerHTML.includes('Nguyễn Văn An')) {
  throw new Error('Customers filter "tuan" did not narrow to Phạm Minh Tuấn');
}
custBox.input.value = 'ko';
sandbox.openAdminSearchDropdown(custBox.input);
if (!custBox.dropdown.innerHTML.includes('Không tìm thấy kết quả phù hợp')) {
  throw new Error('Customers filter "ko" should show empty state');
}

// 3. Orders dropdown opens with customer + order code and closes previous dropdown
sandbox.openAdminSearchDropdown(orderBox.input);
if (custBox.dropdown.classList.contains('is-open')) {
  throw new Error('Opening orders dropdown should close previously open customers dropdown');
}
if (!orderBox.dropdown.classList.contains('is-open') || !orderBox.dropdown.innerHTML.includes('#EB-8801')) {
  throw new Error('Orders dropdown missing #EB-8801');
}
orderBox.input.value = 'eb-8801';
sandbox.openAdminSearchDropdown(orderBox.input);
if (!orderBox.dropdown.innerHTML.includes('Nguyễn Văn An') || orderBox.dropdown.innerHTML.includes('Phạm Minh Tuấn')) {
  throw new Error('Orders filter "eb-8801" did not narrow to Nguyễn Văn An');
}

// 4. Inventory drinks dropdown opens with all 10 drinks and filters 'sting' to 3 drinks
sandbox.openAdminSearchDropdown(prodBox.input);
if (!prodBox.dropdown.classList.contains('is-open') || !prodBox.dropdown.innerHTML.includes('10 sản phẩm')) {
  throw new Error('Inventory dropdown should show 10 sản phẩm');
}
for (const drink of ['Monster Energy Original 355ml', 'Redbull Original 250ml', 'Sting Dâu Tây Đỏ 330ml']) {
  if (!prodBox.dropdown.innerHTML.includes(drink)) {
    throw new Error(`Inventory dropdown missing '${drink}'`);
  }
}
prodBox.input.value = 'sting';
sandbox.openAdminSearchDropdown(prodBox.input);
if (!prodBox.dropdown.innerHTML.includes('3 sản phẩm') || prodBox.dropdown.innerHTML.includes('Monster Energy Original')) {
  throw new Error('Inventory filter "sting" should narrow to 3 sản phẩm');
}

// 5. Selecting a suggestion sets input value, closes dropdown, emits toast
sandbox.selectAdminSearchSuggestion(prodBox.input, prodBox.dropdown, 'Sting Dâu Tây Đỏ 330ml');
if (prodBox.input.value !== 'Sting Dâu Tây Đỏ 330ml' || prodBox.dropdown.classList.contains('is-open')) {
  throw new Error('selectAdminSearchSuggestion did not fill input and close dropdown');
}
if (!toasts.length || !toasts[toasts.length - 1].msg.includes('Sting Dâu Tây Đỏ 330ml')) {
  throw new Error('selectAdminSearchSuggestion did not show toast');
}

// 6. closeAllAdminSearchDropdowns closes any open dropdown
sandbox.openAdminSearchDropdown(custBox.input);
sandbox.closeAllAdminSearchDropdowns();
if (allDropdowns.some((d) => d.classList.contains('is-open'))) {
  throw new Error('closeAllAdminSearchDropdowns left a dropdown open');
}

// 7. Portal menus still reopen and route delegated suggestion clicks to their input.
custBox.input.value = '';
sandbox.openAdminSearchDropdown(custBox.input);
const clickHandler = documentListeners.click[documentListeners.click.length - 1];
const pickBtn = {
  closest: (selector) => selector === '.admin-search-dropdown' ? custBox.dropdown : null,
  getAttribute: () => 'Nguyễn Văn An',
};
clickHandler({ target: { closest: () => pickBtn } });
if (custBox.input.value !== 'Nguyễn Văn An' || custBox.dropdown.classList.contains('is-open')) {
  throw new Error('Selecting a portaled suggestion did not fill the original input and close');
}
sandbox.openAdminSearchDropdown(custBox.input);
clickHandler({ target: { closest: (selector) => selector === '.admin-filter-search, .admin-search-dropdown' ? custBox.dropdown : null } });
if (!custBox.dropdown.classList.contains('is-open')) {
  throw new Error('Clicking the portal header or list should keep the dropdown open');
}
clickHandler({ target: { closest: () => null } });
if (custBox.dropdown.classList.contains('is-open')) {
  throw new Error('Clicking outside should close a portaled dropdown');
}
sandbox.openAdminSearchDropdown(custBox.input);
documentListeners.keydown[documentListeners.keydown.length - 1]({ key: 'Escape' });
if (custBox.dropdown.classList.contains('is-open')) throw new Error('Escape should close a portaled dropdown');

// 8. Reposition through the stored anchor after scrolling; flip and constrain to the viewport.
sandbox.openAdminSearchDropdown(orderBox.input);
orderBox.wrapper.getBoundingClientRect = () => ({ left: 1100, right: 1270, top: 700, bottom: 740 });
windowListeners.scroll();
if (orderBox.dropdown.style.left !== '928px' || orderBox.dropdown.style.top !== 'auto' || orderBox.dropdown.style.bottom !== '106px') {
  throw new Error('Portal did not stay anchored or flip above near viewport edges');
}
if (orderBox.dropdown.style.maxHeight !== '682px') throw new Error('Upward menu height is not constrained');
orderBox.wrapper.getBoundingClientRect = () => ({ left: 100, right: 300, top: 400, bottom: 440 });
windowListeners.resize();
if (orderBox.dropdown.style.top !== '446px' || orderBox.dropdown.style.bottom !== '' || orderBox.dropdown.style.maxHeight !== '342px') {
  throw new Error('Downward menu height or stale upward position is invalid');
}
sandbox.window.innerWidth = 240;
windowListeners.resize();
if (orderBox.dropdown.style.width !== '216px' || orderBox.dropdown.style.left !== '12px') {
  throw new Error('Dropdown should fit even viewports narrower than 284px');
}
orderBox.wrapper.getBoundingClientRect = () => ({ left: 100, right: 300, top: -80, bottom: -40 });
windowListeners.scroll();
if (orderBox.dropdown.classList.contains('is-open')) throw new Error('Offscreen anchor should close its dropdown');

// 9. Both dashboard fields work with menus that are already outside their wrappers in HTML.
sandbox.window.innerWidth = 1860;
for (const box of [dashboardOrderBox, dashboardProductBox]) {
  box.wrapper.getBoundingClientRect = () => ({ left: 325, right: 520, top: 125, bottom: 165 });
  sandbox.openAdminSearchDropdown(box.input);
  assert(box.dropdown.classList.contains('is-open'), `Dashboard menu #${box.dropdown.id} did not open`);
  assert.strictEqual(box.dropdown.style.left, '325px', 'Dashboard menu drifted horizontally');
  assert.strictEqual(box.dropdown.style.top, '171px', 'Dashboard menu drifted vertically');
  assert.strictEqual(allDropdowns.filter((d) => d.classList.contains('is-open')).length, 1);
  box.input.value = box === dashboardOrderBox ? '8801' : 'sting';
  sandbox.openAdminSearchDropdown(box.input);
  assert(box.dropdown.innerHTML.includes(box === dashboardOrderBox ? 'Nguyễn Văn An' : '3 sản phẩm'));
  const dashboardPick = {
    closest: (selector) => selector === '.admin-search-dropdown' ? box.dropdown : null,
    getAttribute: () => box === dashboardOrderBox ? 'Nguyễn Văn An' : 'Sting Dâu Tây Đỏ 330ml',
  };
  clickHandler({ target: { closest: () => dashboardPick } });
  assert.strictEqual(box.input.value, dashboardPick.getAttribute());
  assert(!box.dropdown.classList.contains('is-open'));
  sandbox.openAdminSearchDropdown(box.input);
  assert(box.dropdown.classList.contains('is-open'), 'Dashboard menu should reopen after selection');
}

console.log('NODE_ADMIN_DROPDOWN_PASS');
"""
    proc = subprocess.run(
        ["node", "-e", node_code],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if proc.returncode != 0 or "NODE_ADMIN_DROPDOWN_PASS" not in proc.stdout:
        failures.append(f"Node VM runtime check failed: {(proc.stderr or proc.stdout).strip()}")


def main() -> int:
    failures: list[str] = []
    check_html(failures)
    check_css(failures)
    check_node_runtime(failures)
    if failures:
        print(f"FAIL ({len(failures)} checks failed):")
        for item in failures:
            print(f"  - {item}")
        return 1
    print("ALL CHECKS PASSED: Admin search dropdowns (customers, orders, inventory drinks) verified statically & in Node VM.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
