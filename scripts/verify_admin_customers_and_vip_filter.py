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
