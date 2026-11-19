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

const tierSelect = {
  value: 'diamond',
  options: [
    { value: 'all', text: 'Tất cả cấp bậc (6 khách)' },
    { value: 'diamond', text: 'Kim Cương' },
  ],
  selectedIndex: 1,
};
const kwInput = { value: 'Phạm' };
const fromInput = { value: '2026-01-01' };
const toInput = { value: '2026-10-17' };

let formResetCalls = 0;
const formAddUser = { reset: () => { formResetCalls += 1; } };
const modalAddUserClasses = new Set(['admin-modal-overlay', 'active']);
const modalAddUser = {
  classList: {
    remove: (c) => modalAddUserClasses.delete(c),
    add: (c) => modalAddUserClasses.add(c),
    contains: (c) => modalAddUserClasses.has(c),
  },
};

let tbodyInsertBeforeCalls = 0;
let tbodyAppendChildCalls = 0;
const tbody = {
  firstChild: null,
  insertBefore: () => { tbodyInsertBeforeCalls += 1; },
  appendChild: () => { tbodyAppendChildCalls += 1; },
  querySelector: () => null,
};
const customersTable = {
  querySelector: (sel) => (sel === 'tbody' ? tbody : null),
};

const localStorageSetCalls = [];
const localStorageRemoveCalls = [];

const sandbox = {
  console,
  URLSearchParams,
  window: { location: { pathname: '/admin/customers.html', search: '' }, addEventListener: () => {} },
  document: {
    readyState: 'loading',
    addEventListener: () => {},
    createElement: (tag) => ({
      tagName: String(tag).toUpperCase(),
      setAttribute: () => {},
      style: {},
      innerHTML: '',
    }),
    getElementById: (id) => ({
      'btn-filter-top5-vip': top5Btn,
      'filter-customer-tier': tierSelect,
      'filter-customer-keyword': kwInput,
      'stat-customer-from': fromInput,
      'stat-customer-to': toInput,
      'customers-table': customersTable,
      'form-add-user': formAddUser,
      'modal-add-user': modalAddUser,
      'add-user-fullname': { value: 'Nguyễn An Test' },
      'add-user-username': { value: 'nguyenantest' },
      'add-user-email': { value: 'test@energyboost.vn' },
      'add-user-phone': { value: '0909123456' },
      'add-user-role': { value: 'user' },
      'add-user-status': { value: 'active' },
      'add-user-password': { value: '123456' },
    }[id] || null),
    querySelector: (sel) => (sel === '.cart-table' ? customersTable : (sel === '#customers-table tbody' ? tbody : null)),
    querySelectorAll: (sel) => (sel.includes('#customers-table tbody tr') ? rows : []),
    body: { style: {}, appendChild: () => {} },
  },
  localStorage: {
    getItem: (k) => (k === 'admin_custom_users' ? JSON.stringify([{ id: 'u_1', fullname: 'Old User' }]) : '[]'),
    setItem: (k, v) => { localStorageSetCalls.push({ k, v }); },
    removeItem: (k) => { localStorageRemoveCalls.push(k); },
  },
};

vm.createContext(sandbox);
vm.runInContext(appCode, sandbox);
sandbox.showToast = (msg, type) => toasts.push({ msg, type });
const closedModals = [];
const origCloseAdminModal = sandbox.closeAdminModal;
sandbox.closeAdminModal = (modalId) => {
  closedModals.push(modalId);
  if (typeof origCloseAdminModal === 'function') {
    return origCloseAdminModal(modalId);
  }
};

function assertAllRowsVisible(context) {
  for (let i = 0; i < 6; i++) {
    if (rows[i].style.display === 'none' || rows[i].style.display !== '') {
      throw new Error(`${context}: expected row #${i + 1} display === '' (got ${JSON.stringify(rows[i].style.display)})`);
    }
  }
}

// 1. toggleTop5VipFilter toggles 'active', emits toast with '5 người VIP', keeps ALL 6 rows visible
toasts.length = 0;
sandbox.toggleTop5VipFilter(top5Btn);
if (!btnClasses.has('active')) throw new Error('Expected active class on #btn-filter-top5-vip');
if (!toasts.some((t) => typeof t.msg === 'string' && t.msg.includes('5 người VIP'))) {
  throw new Error('Expected toggleTop5VipFilter to call showToast with "5 người VIP"');
}
assertAllRowsVisible('toggleTop5VipFilter');

// 2. applyAdminCustomerFilter and resetAdminCustomerFilter keep ALL 6 rows visible and emit toasts
toasts.length = 0;
sandbox.applyAdminCustomerFilter();
if (toasts.length === 0) throw new Error('Expected applyAdminCustomerFilter to call showToast');
assertAllRowsVisible('applyAdminCustomerFilter');

toasts.length = 0;
sandbox.resetAdminCustomerFilter();
if (btnClasses.has('active')) throw new Error('Expected resetAdminCustomerFilter to clear active class');
if (toasts.length === 0) throw new Error('Expected resetAdminCustomerFilter to call showToast');
assertAllRowsVisible('resetAdminCustomerFilter');

// 3. saveAddUser emits toast with 'Nguyễn An Test', closes modal, resets form, 0 DOM inserts, 0 localStorage.setItem
toasts.length = 0;
closedModals.length = 0;
formResetCalls = 0;
tbodyInsertBeforeCalls = 0;
tbodyAppendChildCalls = 0;
localStorageSetCalls.length = 0;

sandbox.saveAddUser({ preventDefault: () => {} });
if (!toasts.some((t) => typeof t.msg === 'string' && t.msg.includes('Nguyễn An Test'))) {
  throw new Error('Expected saveAddUser to call showToast with "Nguyễn An Test"');
}
if (!closedModals.includes('modal-add-user')) {
  throw new Error('Expected saveAddUser to call closeAdminModal("modal-add-user")');
}
if (formResetCalls !== 1) {
  throw new Error(`Expected form.reset() to be called once, got ${formResetCalls}`);
}
if (tbodyInsertBeforeCalls !== 0 || tbodyAppendChildCalls !== 0) {
  throw new Error(`Expected 0 tbody insertBefore/appendChild calls, got insertBefore=${tbodyInsertBeforeCalls}, appendChild=${tbodyAppendChildCalls}`);
}
if (localStorageSetCalls.length !== 0) {
  throw new Error(`Expected 0 localStorage.setItem calls, got ${localStorageSetCalls.length}`);
}

// 4. initCustomUsersTable removes 'admin_custom_users' and adds 0 rows
tbodyInsertBeforeCalls = 0;
tbodyAppendChildCalls = 0;
localStorageRemoveCalls.length = 0;

sandbox.initCustomUsersTable();
if (!localStorageRemoveCalls.includes('admin_custom_users')) {
  throw new Error('Expected initCustomUsersTable to call localStorage.removeItem("admin_custom_users")');
}
if (tbodyInsertBeforeCalls !== 0 || tbodyAppendChildCalls !== 0) {
  throw new Error(`Expected initCustomUsersTable to add 0 rows, got insertBefore=${tbodyInsertBeforeCalls}, appendChild=${tbodyAppendChildCalls}`);
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
