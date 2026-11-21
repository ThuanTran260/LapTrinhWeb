import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent


def verify_settings_html(settings_html: str) -> list[str]:
    """Verify static HTML structure, synced data, and accessibility in admin/settings.html."""
    failures: list[str] = []

    voucher_marker = "VOUCHER KHUYẾN MÃI & VẬN CHUYỂN"
    tier_marker = 'id="tier-privileges-section"'
    faq_marker = "QUẢN LÝ CÂU HỎI THƯỜNG GẶP (FAQ)"

    voucher_idx = settings_html.find(voucher_marker)
    tier_idx = settings_html.find(tier_marker)
    faq_idx = settings_html.find(faq_marker)

    if voucher_idx == -1:
        failures.append(f"admin/settings.html: missing voucher section marker '{voucher_marker}'")
    if tier_idx == -1:
        failures.append("admin/settings.html: missing #tier-privileges-section")
    if faq_idx == -1:
        failures.append(f"admin/settings.html: missing FAQ section marker '{faq_marker}'")
    if voucher_idx != -1 and tier_idx != -1 and faq_idx != -1:
        if not (voucher_idx < tier_idx < faq_idx):
            failures.append(
                "admin/settings.html: #tier-privileges-section must appear between Voucher section and FAQ section"
            )

    section_match = re.search(
        r'<section[^>]*id="tier-privileges-section"[^>]*>([\s\S]*?)</section>',
        settings_html,
    )
    if not section_match:
        failures.append("admin/settings.html: could not parse <section id=\"tier-privileges-section\">...</section>")
        return failures

    section_html = section_match.group(0)

    if "QUYỀN LỢI CÁC HẠNG THÀNH VIÊN" not in section_html:
        failures.append("admin/settings.html: missing heading 'QUYỀN LỢI CÁC HẠNG THÀNH VIÊN'")

    for tier in ("diamond", "gold", "silver", "standard"):
        if f'data-tier="{tier}"' not in section_html:
            failures.append(f"admin/settings.html: missing tier card with data-tier=\"{tier}\"")

    synced_users = [
        "Phạm Minh Tuấn",
        "Nguyễn Văn An",
        "Trần Thị Bích",
        "Lê Hoàng Nam",
        "Vũ Thảo My",
        "Hoàng Đức Long",
        "Thuận Trần",
    ]
    for user_name in synced_users:
        if user_name not in section_html:
            failures.append(f"admin/settings.html: missing synced user '{user_name}' in #tier-privileges-section")

    if 'href="customers.html"' not in section_html:
        failures.append("admin/settings.html: missing link to 'customers.html' in #tier-privileges-section")

    privilege_phrases = [
        "Miễn phí ship hỏa tốc + Chiết khấu 10%",
        "Chiết khấu 7% toàn bộ đơn hàng",
        "Tích điểm đổi quà VIP độc quyền",
        "Tích điểm cơ bản",
    ]
    for phrase in privilege_phrases:
        if phrase not in section_html:
            failures.append(f"admin/settings.html: missing synced privilege phrase '{phrase}'")

    required_ids = [
        "btn-sync-tier-privileges",
        "tier-privileges-toggle",
        "tier-privileges-status-label",
        "form-tier-privileges",
        "tier-privilege-rank",
        "tier-privilege-discount",
        "tier-privilege-threshold",
        "tier-privilege-point-rate",
        "tier-privilege-shipping",
        "tier-privilege-desc",
    ]
    for element_id in required_ids:
        if f'id="{element_id}"' not in section_html:
            failures.append(f"admin/settings.html: missing #{element_id} inside #tier-privileges-section")

    if 'id="tier-privilege-voucher"' in section_html or "Voucher Áp Dụng Riêng" in section_html:
        failures.append("admin/settings.html: #tier-privileges-section must NOT contain #tier-privilege-voucher ('Voucher Áp Dụng Riêng')")

    if not re.search(r'<input[^>]*\bid="shop-name"[^>]*\bvalue="ENERGY BOOST"', settings_html):
        failures.append("admin/settings.html: #shop-name must have value='ENERGY BOOST'")

    form_tag_match = re.search(r'<form[^>]*id="form-tier-privileges"[^>]*>', section_html)
    if not form_tag_match:
        failures.append("admin/settings.html: missing <form id=\"form-tier-privileges\"> tag")
    else:
        form_tag = form_tag_match.group(0)
        if "aria-labelledby=" not in form_tag:
            failures.append("admin/settings.html: #form-tier-privileges missing aria-labelledby attribute")
        if "novalidate" not in form_tag:
            failures.append("admin/settings.html: #form-tier-privileges missing novalidate attribute")

    threshold_match = re.search(r'<input[^>]*id="tier-privilege-threshold"[^>]*>', section_html)
    if not threshold_match or "price-format-input" not in threshold_match.group(0):
        failures.append("admin/settings.html: #tier-privilege-threshold must have class 'price-format-input'")

    for btn_label in ("Lưu Quyền Lợi Hạng", "Khôi Phục Mặc Định"):
        if btn_label not in section_html:
            failures.append(f"admin/settings.html: missing button label '{btn_label}'")

    form_fields = [
        "tier-privilege-rank",
        "tier-privilege-discount",
        "tier-privilege-threshold",
        "tier-privilege-point-rate",
        "tier-privilege-shipping",
        "tier-privilege-desc",
    ]
    for field_id in form_fields:
        if not re.search(rf'<label[^>]*\bfor="{re.escape(field_id)}"[^>]*>', section_html):
            failures.append(f"admin/settings.html: missing accessible <label for=\"{field_id}\">")
        field_tag_match = re.search(
            rf'<(?:input|select|textarea)[^>]*\bid="{re.escape(field_id)}"[^>]*>',
            section_html,
        )
        if not field_tag_match or not re.search(r'\bname="[^"]+"', field_tag_match.group(0)):
            failures.append(f"admin/settings.html: #{field_id} missing name attribute")

    return failures


def extract_balanced_media_blocks(css_text: str, query_pattern: str) -> list[str]:
    """Extract full balanced-brace bodies for @media blocks matching query_pattern."""
    blocks: list[str] = []
    for match in re.finditer(query_pattern, css_text):
        start = match.end()
        depth = 1
        idx = start
        while idx < len(css_text) and depth > 0:
            ch = css_text[idx]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            idx += 1
        if depth == 0:
            blocks.append(css_text[start : idx - 1])
    return blocks


def verify_style_css(style_css: str) -> list[str]:
    """Verify required tier privilege CSS selectors, focus-visible, and responsive rules."""
    failures: list[str] = []

    required_selectors = [
        ".tier-privileges-grid",
        ".tier-privilege-card",
        ".tier-card-top",
        ".tier-rate-pill",
        ".tier-badge-standard",
        ".tier-sync-users",
        ".tier-privilege-summary",
        ".tier-card-actions",
        ".tier-privileges-sync-note",
    ]
    for selector in required_selectors:
        if selector not in style_css:
            failures.append(f"css/style.css: missing selector '{selector}'")

    if not re.search(
        r'(?:#tier-privileges-section|\.tier-privileges-sync-note|\.tier-privilege-card)[^\n{]*:focus-visible',
        style_css,
    ):
        failures.append("css/style.css: missing :focus-visible outline rule for tier privileges controls")

    media_blocks = extract_balanced_media_blocks(
        style_css,
        r'@media\s*\(\s*max-width:\s*600px\s*\)\s*\{',
    )
    has_tier_responsive = any(
        ".tier-privileges-grid" in block and ".tier-card-actions" in block
        for block in media_blocks
    )
    if not has_tier_responsive:
        failures.append(
            "css/style.css: missing @media (max-width: 600px) rules for .tier-privileges-grid and .tier-card-actions"
        )

    if style_css.count("{") != style_css.count("}"):
        failures.append(
            f"css/style.css: unbalanced braces ({{={style_css.count('{')}, }}={style_css.count('}')})"
        )

    return failures


def verify_js_runtime() -> list[str]:
    """Execute js/app.js in Node vm and verify data sync + strict toast-only invariants."""
    node_test = r"""
const fs = require('fs');
const vm = require('vm');
const path = require('path');

const appCode = fs.readFileSync(path.join(process.cwd(), 'js', 'app.js'), 'utf8');
const toasts = [];
const localStorageSetCalls = [];

function makeCard(tier) {
  return {
    getAttribute: (attr) => (attr === 'data-tier' ? tier : null),
    innerHTML: `<div data-mock-tier="${tier}">initial-${tier}</div>`,
    style: { display: '', opacity: '', borderColor: '' },
  };
}

const cards = [
  makeCard('diamond'),
  makeCard('gold'),
  makeCard('silver'),
  makeCard('standard'),
];

const grid = {
  innerHTML: '<div id="tier-grid-initial">4-cards</div>',
  querySelectorAll: (sel) => (sel.includes('tier-privilege-card') ? cards : []),
};

const statusLabel = {
  textContent: 'ĐANG BẬT',
  style: { color: 'var(--primary)' },
};

const tierToggle = {
  checked: true,
  disabled: false,
};

const rankOptions = [
  { value: 'diamond', text: 'Hạng Kim Cương (Từ 12.000.000đ)' },
  { value: 'gold', text: 'Hạng Vàng (Từ 7.000.000đ)' },
  { value: 'silver', text: 'Hạng Bạc (Từ 3.000.000đ)' },
  { value: 'standard', text: 'Khách Hàng Chuẩn (Mặc định)' },
];

const formInputs = {
  'tier-privilege-rank': {
    value: 'diamond',
    selectedIndex: 0,
    options: rankOptions,
  },
  'tier-privilege-discount': { value: '10%' },
  'tier-privilege-threshold': { value: '12.000.000đ' },
  'tier-privilege-point-rate': {
    value: 'x2.0',
    selectedIndex: 0,
    options: [{ value: 'x2.0', text: 'x2.0' }],
  },
  'tier-privilege-shipping': {
    value: 'Miễn phí ship hỏa tốc 2H',
    selectedIndex: 0,
    options: [{ value: 'Miễn phí ship hỏa tốc 2H', text: 'Miễn phí ship hỏa tốc 2H' }],
  },
  'tier-privilege-desc': { value: 'Miễn phí ship hỏa tốc + Chiết khấu 10%' },
};

const elementsById = {
  'tier-privileges-status-label': statusLabel,
  'tier-privileges-toggle': tierToggle,
  'tier-privileges-grid': grid,
  ...formInputs,
};

const sandbox = {
  console,
  URLSearchParams,
  window: {
    location: { pathname: '/admin/settings.html', search: '' },
    addEventListener: () => {},
  },
  document: {
    readyState: 'loading',
    addEventListener: () => {},
    createElement: (tag) => ({
      tagName: String(tag).toUpperCase(),
      setAttribute: () => {},
      style: {},
      innerHTML: '',
    }),
    getElementById: (id) => elementsById[id] || null,
    querySelector: (sel) => (sel === '#tier-privileges-grid' ? grid : null),
    querySelectorAll: (sel) => (sel.includes('tier-privilege-card') ? cards : []),
    body: { style: {}, appendChild: () => {} },
  },
  localStorage: {
    getItem: () => null,
    setItem: (k, v) => { localStorageSetCalls.push({ k, v }); },
    removeItem: () => {},
  },
};

vm.createContext(sandbox);
vm.runInContext(appCode, sandbox);

const spyShowToast = (message, type) => {
  toasts.push({ message, type });
};
sandbox.showToast = spyShowToast;
if (sandbox.window) {
  sandbox.window.showToast = spyShowToast;
}

const tierData = vm.runInContext('typeof USER_TIER_PRIVILEGES_DATA !== "undefined" ? USER_TIER_PRIVILEGES_DATA : undefined', sandbox);
const customerRegistry = vm.runInContext('typeof CUSTOMER_DATA_REGISTRY !== "undefined" ? CUSTOMER_DATA_REGISTRY : undefined', sandbox);

if (!tierData || typeof tierData !== 'object') {
  throw new Error('USER_TIER_PRIVILEGES_DATA is missing or not an object in js/app.js');
}
if (!customerRegistry || typeof customerRegistry !== 'object') {
  throw new Error('CUSTOMER_DATA_REGISTRY is missing or not an object in js/app.js');
}

for (const key of ['diamond', 'gold', 'silver', 'standard']) {
  if (!tierData[key]) {
    throw new Error(`USER_TIER_PRIVILEGES_DATA missing key '${key}'`);
  }
}

const tierLabelToKey = {
  'HẠNG KIM CƯƠNG': 'diamond',
  'HẠNG VÀNG': 'gold',
  'HẠNG BẠC': 'silver',
};

for (const [custKey, cust] of Object.entries(customerRegistry)) {
  const tierKey = tierLabelToKey[cust.tier];
  if (!tierKey) {
    throw new Error(`Unexpected customer tier '${cust.tier}' for '${custKey}' in CUSTOMER_DATA_REGISTRY`);
  }
  const tierEntry = tierData[tierKey];
  if (tierEntry.privileges !== cust.privileges) {
    throw new Error(
      `Privilege mismatch for '${custKey}' (${tierKey}): expected '${cust.privileges}', got '${tierEntry.privileges}'`
    );
  }
  if (!Array.isArray(tierEntry.users) || !tierEntry.users.includes(cust.name)) {
    throw new Error(`Customer '${cust.name}' missing from USER_TIER_PRIVILEGES_DATA.${tierKey}.users`);
  }
}

if (!Array.isArray(tierData.silver.users) || !tierData.silver.users.includes('Thuận Trần')) {
  throw new Error("Expected 'Thuận Trần' in USER_TIER_PRIVILEGES_DATA.silver.users");
}

const requiredHandlers = [
  'selectUserTierPrivilege',
  'handleTierRankSelectNotice',
  'handleTierPrivilegesToggle',
  'handleSyncTierPrivilegesNow',
  'handleSaveTierPrivileges',
  'handleResetTierPrivileges',
];
for (const fnName of requiredHandlers) {
  if (typeof sandbox[fnName] !== 'function') {
    throw new Error(`Missing global handler '${fnName}' in js/app.js`);
  }
  if (typeof sandbox.window[fnName] !== 'function') {
    throw new Error(`Handler '${fnName}' is not exported on window`);
  }
}

const initialState = {
  statusText: statusLabel.textContent,
  inputs: Object.fromEntries(Object.entries(formInputs).map(([k, el]) => [k, el.value])),
  gridInnerHTML: grid.innerHTML,
  cards: cards.map((c) => ({ innerHTML: c.innerHTML, style: JSON.stringify(c.style) })),
  customerRegistryJson: JSON.stringify(customerRegistry),
};

function assertToastOnlyAndUnchanged(actionLabel) {
  if (toasts.length !== 1) {
    throw new Error(`${actionLabel}: expected exactly 1 showToast call, got ${toasts.length}`);
  }
  const toast = toasts[0];
  if (typeof toast.message !== 'string' || toast.message.trim().length === 0) {
    throw new Error(`${actionLabel}: expected non-empty toast message, got ${JSON.stringify(toast.message)}`);
  }
  if (statusLabel.textContent !== initialState.statusText) {
    throw new Error(`${actionLabel}: #tier-privileges-status-label.textContent was mutated to ${JSON.stringify(statusLabel.textContent)}`);
  }
  for (const [id, expectedVal] of Object.entries(initialState.inputs)) {
    if (formInputs[id].value !== expectedVal) {
      throw new Error(`${actionLabel}: #${id}.value was mutated from ${JSON.stringify(expectedVal)} to ${JSON.stringify(formInputs[id].value)}`);
    }
  }
  if (grid.innerHTML !== initialState.gridInnerHTML) {
    throw new Error(`${actionLabel}: #tier-privileges-grid.innerHTML was mutated`);
  }
  cards.forEach((card, idx) => {
    if (card.innerHTML !== initialState.cards[idx].innerHTML) {
      throw new Error(`${actionLabel}: card #${idx + 1} innerHTML was mutated`);
    }
    if (JSON.stringify(card.style) !== initialState.cards[idx].style) {
      throw new Error(`${actionLabel}: card #${idx + 1} style was mutated`);
    }
  });
  if (localStorageSetCalls.length !== 0) {
    throw new Error(`${actionLabel}: expected 0 localStorage.setItem writes, got ${localStorageSetCalls.length}`);
  }
  if (JSON.stringify(customerRegistry) !== initialState.customerRegistryJson) {
    throw new Error(`${actionLabel}: CUSTOMER_DATA_REGISTRY was mutated`);
  }
}

function runAndVerify(actionLabel, fn) {
  toasts.length = 0;
  localStorageSetCalls.length = 0;
  fn();
  assertToastOnlyAndUnchanged(actionLabel);
}

for (const tierKey of ['diamond', 'gold', 'silver', 'standard']) {
  runAndVerify(`selectUserTierPrivilege('${tierKey}')`, () => {
    sandbox.selectUserTierPrivilege(tierKey);
  });
}

runAndVerify('handleTierRankSelectNotice(rankSelect)', () => {
  sandbox.handleTierRankSelectNotice(formInputs['tier-privilege-rank']);
});

runAndVerify('handleTierRankSelectNotice(goldSelect)', () => {
  sandbox.handleTierRankSelectNotice({
    value: 'gold',
    selectedIndex: 1,
    options: rankOptions,
  });
});

runAndVerify('handleTierPrivilegesToggle({ checked: false })', () => {
  sandbox.handleTierPrivilegesToggle({ checked: false });
});

runAndVerify('handleTierPrivilegesToggle({ checked: true })', () => {
  sandbox.handleTierPrivilegesToggle({ checked: true });
});

runAndVerify('handleSyncTierPrivilegesNow()', () => {
  sandbox.handleSyncTierPrivilegesNow();
});

let preventDefaultCalls = 0;
runAndVerify('handleSaveTierPrivileges(event)', () => {
  sandbox.handleSaveTierPrivileges({ preventDefault: () => { preventDefaultCalls += 1; } });
});
if (preventDefaultCalls !== 1) {
  throw new Error(`Expected handleSaveTierPrivileges to call event.preventDefault() once, got ${preventDefaultCalls}`);
}

runAndVerify('handleResetTierPrivileges()', () => {
  sandbox.handleResetTierPrivileges();
});

console.log('NODE_TIER_PRIVILEGES_PASS');
"""
    proc = subprocess.run(
        ["node", "-e", node_test],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if proc.returncode != 0 or "NODE_TIER_PRIVILEGES_PASS" not in proc.stdout:
        detail = (proc.stderr or proc.stdout).strip()
        return [f"js/app.js Node vm runtime check failed: {detail}"]
    return []


def main() -> int:
    settings_html = (ROOT / "admin" / "settings.html").read_text(encoding="utf-8")
    style_css = (ROOT / "css" / "style.css").read_text(encoding="utf-8")

    failures = []
    failures.extend(verify_settings_html(settings_html))
    failures.extend(verify_style_css(style_css))
    failures.extend(verify_js_runtime())

    if failures:
        print(f"FAIL ({len(failures)} checks failed):")
        for item in failures:
            print(f"  - {item}")
        return 1

    print("ALL CHECKS PASSED: admin/settings.html tier privileges UI, CSS, and toast-only JS verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
