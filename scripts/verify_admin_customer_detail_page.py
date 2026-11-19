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
