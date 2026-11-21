import re
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent


def extract_customers_table(html: str) -> str:
    match = re.search(
        r'<table\b[^>]*id="customers-table"[^>]*>.*?</table>',
        html,
        flags=re.DOTALL,
    )
    return match.group(0) if match else ""


def main() -> int:
    failures = []

    customers_html = (ROOT / "admin" / "customers.html").read_text(encoding="utf-8")
    app_js = (ROOT / "js" / "app.js").read_text(encoding="utf-8")

    # (a) Static checks on admin/customers.html
    for forbidden in ("modal-edit-user", "openEditUserModal", "saveEditUser"):
        if forbidden in customers_html:
            failures.append(f"admin/customers.html: forbidden reference '{forbidden}' still present")

    table_html = extract_customers_table(customers_html)
    if not table_html:
        failures.append("admin/customers.html: missing <table id=\"customers-table\">")
    else:
        edit_btn_matches = re.findall(
            r"<button\b[^>]*>.*?</button>",
            table_html,
            flags=re.DOTALL,
        )
        sua_buttons = [btn for btn in edit_btn_matches if re.search(r"\bSửa\b", btn)]
        if sua_buttons:
            failures.append(
                f"admin/customers.html: found {len(sua_buttons)} forbidden 'Sửa' button(s) in #customers-table"
            )

        toggle_count = len(re.findall(r'onclick="toggleLockUser\(', table_html))
        lock_count = len(re.findall(r'class="btn-action-lock"', table_html))
        unlock_count = len(re.findall(r'class="btn-action-unlock"', table_html))

        if toggle_count != 6:
            failures.append(
                f"admin/customers.html: expected 6 toggleLockUser buttons in #customers-table, found {toggle_count}"
            )
        if lock_count != 5:
            failures.append(
                f"admin/customers.html: expected 5 .btn-action-lock buttons in #customers-table, found {lock_count}"
            )
        if unlock_count != 1:
            failures.append(
                f"admin/customers.html: expected 1 .btn-action-unlock button in #customers-table, found {unlock_count}"
            )

    if 'id="modal-add-user"' not in customers_html:
        failures.append("admin/customers.html: missing #modal-add-user")

    # (b) Static checks on js/app.js
    for forbidden in ("openEditUserModal", "saveEditUser", "currentEditingUserRow", "modal-edit-user"):
        if forbidden in app_js:
            failures.append(f"js/app.js: forbidden reference '{forbidden}' still present")

    if "function toggleLockUser(" not in app_js:
        failures.append("js/app.js: missing function toggleLockUser")
    if "CUSTOMER_DATA_REGISTRY" not in app_js:
        failures.append("js/app.js: missing CUSTOMER_DATA_REGISTRY")

    # (c) Node.js VM runtime smoke test for toggleLockUser
    node_test = r"""
const fs = require('fs');
const vm = require('vm');
const path = require('path');

const appCode = fs.readFileSync(path.join(process.cwd(), 'js', 'app.js'), 'utf8');
const toasts = [];

const sandbox = {
  console,
  URLSearchParams,
  window: { location: { pathname: '/admin/customers.html', search: '' }, addEventListener: () => {} },
  document: {
    readyState: 'loading',
    addEventListener: () => {},
    getElementById: () => null,
    querySelector: () => null,
    querySelectorAll: () => [],
    body: { style: {}, appendChild: () => {} },
  },
  localStorage: {
    getItem: () => null,
    setItem: () => {},
    removeItem: () => {},
  },
};

vm.createContext(sandbox);
vm.runInContext(appCode, sandbox);
sandbox.showToast = (msg, type) => toasts.push({ msg, type });

if (typeof sandbox.toggleLockUser !== 'function') {
  throw new Error('toggleLockUser is not defined as a function');
}

const lockBtn = { classList: { contains: (cls) => cls === 'btn-action-lock' } };
const unlockBtn = { classList: { contains: (cls) => cls === 'btn-action-unlock' } };

sandbox.toggleLockUser(lockBtn, 'Trần Thị Bích');
sandbox.toggleLockUser(unlockBtn, 'Vũ Thảo My');

if (toasts.length !== 2) {
  throw new Error(`Expected 2 toasts, got ${toasts.length}: ${JSON.stringify(toasts)}`);
}
if (toasts[0].type !== 'info' || !toasts[0].msg.includes('khoá') || !toasts[0].msg.includes('Trần Thị Bích')) {
  throw new Error(`Unexpected lock toast: ${JSON.stringify(toasts[0])}`);
}
if (toasts[1].type !== 'success' || !toasts[1].msg.includes('mở khoá') || !toasts[1].msg.includes('Vũ Thảo My')) {
  throw new Error(`Unexpected unlock toast: ${JSON.stringify(toasts[1])}`);
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

    print(
        "ALL CHECKS PASSED: edit-user removal and toggleLockUser preservation verified (static + Node runtime)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
