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


def verify_style_css(style_css: str) -> list[str]:
    failures: list[str] = []

    native_picker_match = re.search(r"\.date-native-picker\s*\{([^}]*)\}", style_css)
    if not native_picker_match:
        failures.append("css/style.css: missing .date-native-picker rule")
    elif not re.search(r"pointer-events\s*:\s*auto", native_picker_match.group(1)):
        failures.append("css/style.css: .date-native-picker must set pointer-events: auto")

    if not re.search(r"\.date-picker-btn\s*\{[^}]*\}", style_css):
        failures.append("css/style.css: missing .date-picker-btn rule")

    return failures


def verify_settings_html(settings_html: str) -> list[str]:
    failures: list[str] = []

    form_match = re.search(
        r'<form[^>]*id="form-add-voucher"[^>]*>[\s\S]*?</form>',
        settings_html,
    )
    if not form_match:
        failures.append("admin/settings.html: missing <form id=\"form-add-voucher\"> block")
        return failures

    form_html = form_match.group(0)
    form_open_tag = re.match(r"<form[^>]*>", form_html)
    if not form_open_tag or "novalidate" not in form_open_tag.group(0):
        failures.append("admin/settings.html: #form-add-voucher must declare novalidate")
    if not form_open_tag or 'onsubmit="saveAddVoucher(event)"' not in form_open_tag.group(0):
        failures.append("admin/settings.html: #form-add-voucher missing onsubmit=\"saveAddVoucher(event)\"")

    if re.search(r"\brequired\b", form_html):
        failures.append("admin/settings.html: #form-add-voucher must have ZERO 'required' attributes")

    if '<span class="req">*</span>' in form_html or 'class="req"' in form_html:
        failures.append("admin/settings.html: #form-add-voucher must have ZERO '<span class=\"req\">*</span>' markers")

    limit_match = re.search(r'<input[^>]*id="add-voucher-limit"[^>]*>', form_html)
    if not limit_match:
        failures.append("admin/settings.html: missing #add-voucher-limit input inside #form-add-voucher")
    else:
        limit_tag = limit_match.group(0)
        if 'type="text"' not in limit_tag:
            failures.append("admin/settings.html: #add-voucher-limit must use unconstrained type=\"text\"")
        if "min=" in limit_tag or "max=" in limit_tag:
            failures.append("admin/settings.html: #add-voucher-limit must NOT have min= or max= constraints")

    for field_id in (
        "add-voucher-code",
        "add-voucher-type",
        "add-voucher-amount",
        "add-voucher-min-spend",
        "add-voucher-max-discount",
        "add-voucher-expiry",
        "add-voucher-limit",
        "add-voucher-target",
    ):
        if f'id="{field_id}"' not in form_html:
            failures.append(f"admin/settings.html: #form-add-voucher missing #{field_id}")

    for expiry_id in ("voucher-expiry", "add-voucher-expiry"):
        picker_id = f"{expiry_id}-picker"
        exp_match = re.search(rf'<input[^>]*id="{expiry_id}"[^>]*>', settings_html)
        if not exp_match:
            failures.append(f"admin/settings.html: missing #{expiry_id}")
        else:
            exp_tag = exp_match.group(0)
            if 'type="text"' not in exp_tag or 'value="31/12/2026"' not in exp_tag or 'placeholder="dd/mm/yyyy"' not in exp_tag:
                failures.append(f"admin/settings.html: #{expiry_id} must use dd/mm/yyyy format (type=\"text\", value=\"31/12/2026\", placeholder=\"dd/mm/yyyy\")")
            if f"syncDisplayToDatePicker(this, '{picker_id}')" not in exp_tag:
                failures.append(f"admin/settings.html: #{expiry_id} must bind syncDisplayToDatePicker(this, '{picker_id}')")
        picker_match = re.search(rf'<input[^>]*id="{picker_id}"[^>]*>', settings_html)
        if not picker_match or f"openNativeDatePicker('{picker_id}', '{expiry_id}')" not in picker_match.group(0):
            failures.append(f"admin/settings.html: missing date picker trigger #{picker_id} binding openNativeDatePicker('{picker_id}', '{expiry_id}')")
        elif f"syncDatePickerToDisplay('{expiry_id}', this)" not in picker_match.group(0):
            failures.append(f"admin/settings.html: #{picker_id} missing syncDatePickerToDisplay('{expiry_id}', this)")

    return failures


def verify_js_static(app_js: str) -> list[str]:
    failures: list[str] = []

    save_fn = extract_function(app_js, "saveAddVoucher")
    if not save_fn:
        failures.append("js/app.js: missing saveAddVoucher function")
        return failures

    for forbidden in (
        "MOCK_VOUCHERS_LIST",
        ".unshift",
        "renderVoucherChips",
        "activeVoucherCode",
        "voucher-toggle-active",
        "localStorage.setItem",
    ):
        if forbidden in save_fn:
            failures.append(f"js/app.js: saveAddVoucher must be toast-only, found '{forbidden}'")

    if "closeAdminModal('modal-add-voucher')" not in save_fn:
        failures.append("js/app.js: saveAddVoucher must call closeAdminModal('modal-add-voucher')")
    if "showToast(" not in save_fn:
        failures.append("js/app.js: saveAddVoucher must call showToast(...)")
    if ".reset()" not in save_fn:
        failures.append("js/app.js: saveAddVoucher must call form.reset()")
    if "window.saveAddVoucher = saveAddVoucher" not in app_js:
        failures.append("js/app.js: missing window.saveAddVoucher export")
    for export_name in ("openNativeDatePicker", "syncDatePickerToDisplay", "syncDisplayToDatePicker"):
        if f"window.{export_name} = {export_name}" not in app_js:
            failures.append(f"js/app.js: missing window.{export_name} export")

    return failures


def main() -> int:
    failures: list[str] = []

    style_css = (ROOT / "css" / "style.css").read_text(encoding="utf-8")
    settings_html = (ROOT / "admin" / "settings.html").read_text(encoding="utf-8")
    app_js = (ROOT / "js" / "app.js").read_text(encoding="utf-8")

    failures.extend(verify_style_css(style_css))
    failures.extend(verify_settings_html(settings_html))
    failures.extend(verify_js_static(app_js))

    node_test = r"""
const fs = require('fs');
const vm = require('vm');
const path = require('path');

const appCode = fs.readFileSync(path.join(process.cwd(), 'js', 'app.js'), 'utf8');

let formResetCalls = 0;
const codeEl = { value: '' };
const typeEl = { value: 'percent' };
const amountEl = { value: '' };
const minSpendEl = { value: '' };
const maxDiscountEl = { value: '' };
const expiryEl = { value: '' };
let showPickerCalls = 0;
const voucherExpiryEl = { value: '15/08/2026' };
const voucherExpiryPickerEl = { value: '', showPicker: () => { showPickerCalls += 1; } };
const previewTicketExpiryEl = { textContent: '' };
const addExpiryPickerEl = { value: '' };
const limitEl = { value: '' };
const targetEl = { value: 'all' };

const chipsSentinelHtml = '<button class="voucher-chip active">MONSTER10</button><button class="voucher-chip">ENERGY20</button><button class="voucher-chip">FREESHIP</button>';
const chipsContainer = { innerHTML: chipsSentinelHtml };
const voucherToggleActive = { checked: true };

const formAddVoucher = {
  reset: () => {
    formResetCalls += 1;
    codeEl.value = '';
    amountEl.value = '';
    limitEl.value = '500';
  },
};

const modalAddVoucherClasses = new Set(['admin-modal-overlay', 'active']);
const modalAddVoucher = {
  classList: {
    add: (c) => modalAddVoucherClasses.add(c),
    remove: (c) => modalAddVoucherClasses.delete(c),
    contains: (c) => modalAddVoucherClasses.has(c),
  },
};

const elements = {
  'add-voucher-code': codeEl,
  'add-voucher-type': typeEl,
  'add-voucher-amount': amountEl,
  'add-voucher-min-spend': minSpendEl,
  'add-voucher-max-discount': maxDiscountEl,
  'add-voucher-expiry': expiryEl,
  'add-voucher-expiry-picker': addExpiryPickerEl,
  'voucher-expiry': voucherExpiryEl,
  'voucher-expiry-picker': voucherExpiryPickerEl,
  'preview-ticket-expiry': previewTicketExpiryEl,
  'add-voucher-limit': limitEl,
  'add-voucher-target': targetEl,
  'form-add-voucher': formAddVoucher,
  'modal-add-voucher': modalAddVoucher,
  'voucher-chips-list': chipsContainer,
  'voucher-toggle-active': voucherToggleActive,
};

let localStorageWrites = 0;
const toasts = [];
const closedModals = [];
let renderVoucherChipsCalls = 0;

const sandbox = {
  console,
  URLSearchParams,
  window: { location: { pathname: '/admin/settings.html', search: '' }, addEventListener: () => {} },
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
const origCloseAdminModal = sandbox.closeAdminModal;
sandbox.closeAdminModal = (modalId) => {
  closedModals.push(modalId);
  if (typeof origCloseAdminModal === 'function') {
    return origCloseAdminModal(modalId);
  }
};
const origRenderVoucherChips = sandbox.renderVoucherChips;
sandbox.renderVoucherChips = () => {
  renderVoucherChipsCalls += 1;
  if (typeof origRenderVoucherChips === 'function') {
    return origRenderVoucherChips();
  }
};

function readVoucherState() {
  return vm.runInContext(
    '({ len: MOCK_VOUCHERS_LIST.length, snapshot: JSON.stringify(MOCK_VOUCHERS_LIST), active: activeVoucherCode })',
    sandbox
  );
}

const initialState = readVoucherState();
if (initialState.len !== 3 || initialState.active !== 'MONSTER10') {
  throw new Error(`Unexpected initial voucher state: ${JSON.stringify(initialState)}`);
}

// Case 1: Empty inputs (no required constraint)
codeEl.value = '';
amountEl.value = '';
limitEl.value = '';
toasts.length = 0;
closedModals.length = 0;
formResetCalls = 0;
let prevented1 = false;

sandbox.saveAddVoucher({ preventDefault: () => { prevented1 = true; } });

if (!prevented1) throw new Error('Case 1: saveAddVoucher did not call preventDefault()');
if (!closedModals.includes('modal-add-voucher')) {
  throw new Error('Case 1: expected closeAdminModal("modal-add-voucher")');
}
if (modalAddVoucherClasses.has('active')) {
  throw new Error('Case 1: expected modal-add-voucher active class removed');
}
if (toasts.length !== 1 || toasts[0].type !== 'success' || !toasts[0].msg.includes('VOUCHER MỚI')) {
  throw new Error(`Case 1: unexpected toast output: ${JSON.stringify(toasts)}`);
}
if (formResetCalls !== 1) {
  throw new Error(`Case 1: expected form.reset() once, got ${formResetCalls}`);
}
const afterCase1 = readVoucherState();
if (
  afterCase1.len !== initialState.len ||
  afterCase1.snapshot !== initialState.snapshot ||
  afterCase1.active !== initialState.active
) {
  throw new Error(`Case 1: voucher registry mutated! before=${initialState.snapshot}, after=${afterCase1.snapshot}`);
}
if (renderVoucherChipsCalls !== 0) {
  throw new Error(`Case 1: renderVoucherChips should not be called, got ${renderVoucherChipsCalls}`);
}
if (chipsContainer.innerHTML !== chipsSentinelHtml) {
  throw new Error('Case 1: #voucher-chips-list DOM was mutated');
}
if (voucherToggleActive.checked !== true) {
  throw new Error('Case 1: #voucher-toggle-active.checked was mutated');
}
if (localStorageWrites !== 0) {
  throw new Error(`Case 1: expected 0 localStorage writes, got ${localStorageWrites}`);
}

// Case 2: Arbitrary unconstrained inputs (code='test', limit='Không giới hạn')
modalAddVoucherClasses.add('active');
codeEl.value = 'test';
typeEl.value = 'fixed';
amountEl.value = 'Tùy ý không ràng buộc';
limitEl.value = 'Không giới hạn';
expiryEl.value = '';
toasts.length = 0;
closedModals.length = 0;
formResetCalls = 0;
let prevented2 = false;

sandbox.saveAddVoucher({ preventDefault: () => { prevented2 = true; } });

if (!prevented2) throw new Error('Case 2: saveAddVoucher did not call preventDefault()');
if (!closedModals.includes('modal-add-voucher')) {
  throw new Error('Case 2: expected closeAdminModal("modal-add-voucher")');
}
if (toasts.length !== 1 || toasts[0].type !== 'success' || !toasts[0].msg.includes('TEST')) {
  throw new Error(`Case 2: unexpected toast output: ${JSON.stringify(toasts)}`);
}
if (formResetCalls !== 1) {
  throw new Error(`Case 2: expected form.reset() once, got ${formResetCalls}`);
}
const afterCase2 = readVoucherState();
if (
  afterCase2.len !== initialState.len ||
  afterCase2.snapshot !== initialState.snapshot ||
  afterCase2.active !== initialState.active
) {
  throw new Error('Case 2: voucher registry mutated on arbitrary inputs');
}
if (renderVoucherChipsCalls !== 0) {
  throw new Error(`Case 2: renderVoucherChips should not be called, got ${renderVoucherChipsCalls}`);
}
if (chipsContainer.innerHTML !== chipsSentinelHtml) {
  throw new Error('Case 2: #voucher-chips-list DOM was mutated');
}
if (voucherToggleActive.checked !== true) {
  throw new Error('Case 2: #voucher-toggle-active.checked was mutated');
}
if (localStorageWrites !== 0) {
  throw new Error(`Case 2: expected 0 localStorage writes, got ${localStorageWrites}`);
}

// Case 3: When #voucher-toggle-active starts unchecked (false), saveAddVoucher leaves it false
voucherToggleActive.checked = false;
codeEl.value = 'flash99';
sandbox.saveAddVoucher({ preventDefault: () => {} });
if (voucherToggleActive.checked !== false) {
  throw new Error('Case 3: saveAddVoucher mutated #voucher-toggle-active.checked from false to true');
}

// Case 4: openAddVoucherModal fills dd/mm/yyyy default when expiry is empty
expiryEl.value = '';
sandbox.openAddVoucherModal();
if (expiryEl.value !== '31/12/2026' || addExpiryPickerEl.value !== '2026-12-31') {
  throw new Error(`Case 4: expected openAddVoucherModal defaults 31/12/2026 / 2026-12-31, got ${expiryEl.value} / ${addExpiryPickerEl.value}`);
}

// Case 5: openNativeDatePicker, syncDatePickerToDisplay (date + Clear), and syncDisplayToDatePicker
sandbox.openNativeDatePicker('voucher-expiry-picker', 'voucher-expiry');
if (voucherExpiryPickerEl.value !== '2026-08-15' || showPickerCalls !== 1) {
  throw new Error(`Case 5a: expected picker synced to 2026-08-15 and showPicker called once, got ${voucherExpiryPickerEl.value} / ${showPickerCalls}`);
}
voucherExpiryPickerEl.value = '2027-01-05';
sandbox.syncDatePickerToDisplay('voucher-expiry', voucherExpiryPickerEl);
if (voucherExpiryEl.value !== '05/01/2027' || previewTicketExpiryEl.textContent !== '05/01/2027') {
  throw new Error(`Case 5b: expected display and preview '05/01/2027', got ${voucherExpiryEl.value} / ${previewTicketExpiryEl.textContent}`);
}
voucherExpiryPickerEl.value = '';
sandbox.syncDatePickerToDisplay('voucher-expiry', voucherExpiryPickerEl);
if (voucherExpiryEl.value !== '' || previewTicketExpiryEl.textContent !== '31/12/2026') {
  throw new Error(`Case 5c: expected Clear to reset textEl to '' and preview to '31/12/2026', got '${voucherExpiryEl.value}' / '${previewTicketExpiryEl.textContent}'`);
}
expiryEl.value = '10/10/2026';
addExpiryPickerEl.value = '';
sandbox.syncDatePickerToDisplay('add-voucher-expiry', addExpiryPickerEl);
if (expiryEl.value !== '') {
  throw new Error(`Case 5c-modal: expected Clear to reset add-voucher-expiry to '', got '${expiryEl.value}'`);
}
voucherExpiryEl.value = '';
voucherExpiryPickerEl.value = '';
sandbox.openNativeDatePicker('voucher-expiry-picker', 'voucher-expiry');
if (voucherExpiryPickerEl.value !== '2026-12-31' || showPickerCalls !== 2) {
  throw new Error(`Case 5d: expected empty-field openNativeDatePicker to default picker to '2026-12-31' and call showPicker() twice, got '${voucherExpiryPickerEl.value}' / ${showPickerCalls}`);
}
voucherExpiryEl.value = '04/01/2026';
sandbox.syncDisplayToDatePicker(voucherExpiryEl, 'voucher-expiry-picker');
if (voucherExpiryPickerEl.value !== '2026-01-04') {
  throw new Error(`Case 5e: expected syncDisplayToDatePicker('04/01/2026') -> '2026-01-04', got '${voucherExpiryPickerEl.value}'`);
}
voucherExpiryEl.value = '';
sandbox.syncDisplayToDatePicker(voucherExpiryEl, 'voucher-expiry-picker');
if (voucherExpiryPickerEl.value !== '') {
  throw new Error(`Case 5e-clear: expected syncDisplayToDatePicker('') -> '', got '${voucherExpiryPickerEl.value}'`);
}

console.log('NODE_ADD_VOUCHER_TOAST_ONLY_PASS');
"""

    proc = subprocess.run(
        ["node", "-e", node_test],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if proc.returncode != 0 or "NODE_ADD_VOUCHER_TOAST_ONLY_PASS" not in proc.stdout:
        failures.append(
            f"Node.js runtime test failed (exit {proc.returncode}): {(proc.stderr or proc.stdout).strip()}"
        )

    if failures:
        print(f"FAIL ({len(failures)} checks failed):")
        for item in failures:
            print(f"  - {item}")
        return 1

    print(
        "ALL CHECKS PASSED: #form-add-voucher unconstrained HTML + toast-only saveAddVoucher verified (static + Node runtime)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
