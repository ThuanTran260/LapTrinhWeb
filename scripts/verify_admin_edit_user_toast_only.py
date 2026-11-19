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
