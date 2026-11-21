import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent


def extract_div_block(html: str, class_or_id_pattern: str) -> str:
    match = re.search(rf"<div\b[^>]*{class_or_id_pattern}[^>]*>", html)
    if not match:
        return ""
    depth = 1
    pos = match.end()
    for tag in re.finditer(r"<(/?)div\b[^>]*>", html[pos:]):
        depth += -1 if tag.group(1) else 1
        if depth == 0:
            return html[match.start() : pos + tag.end()]
    return ""


def verify_login_html(html: str) -> list[str]:
    failures: list[str] = []

    # 1. Opening <body> must not carry login-body-wrapper, and page must not contain <nav class="nav-bar">
    body_match = re.search(r"<body\b([^>]*)>", html)
    if not body_match:
        failures.append("pages/login.html: missing opening <body> tag")
    elif "login-body-wrapper" in body_match.group(1):
        failures.append("pages/login.html: opening <body> must NOT carry 'login-body-wrapper'")

    if re.search(r'<nav\b[^>]*class="[^"]*\bnav-bar\b[^"]*"', html):
        failures.append("pages/login.html: page must NOT contain <nav class='nav-bar'>")

    # 2. Top bar with ENERGY10 coupon badge & 4 links
    top_bar = extract_div_block(html, r'class="[^"]*\btop-bar\b[^"]*"')
    if not top_bar:
        failures.append("pages/login.html: missing .top-bar block")
    else:
        if "ENERGY10" not in top_bar:
            failures.append("pages/login.html: .top-bar missing ENERGY10 coupon badge")
        if 'class="coupon-badge"' not in top_bar:
            failures.append("pages/login.html: .top-bar missing .coupon-badge element")
        for expected_link in ("../index.html#features", "orders.html", "account.html", "login.html"):
            if f'href="{expected_link}"' not in top_bar:
                failures.append(f"pages/login.html: .top-bar missing link '{expected_link}'")

    # 3. Header: Logo, search box (5 items), and 3 header actions
    header_match = re.search(r'<header\b[^>]*class="[^"]*\bheader\b[^"]*"[^>]*>([\s\S]*?)</header>', html)
    if not header_match:
        failures.append("pages/login.html: missing <header class='header'>")
    else:
        header_html = header_match.group(0)

        logo_match = re.search(
            r'<a\b[^>]*(?:href="\.\./index\.html"[^>]*class="[^"]*\blogo\b[^"]*"|class="[^"]*\blogo\b[^"]*"[^>]*href="\.\./index\.html")[^>]*>([\s\S]*?)</a>',
            header_html,
        )
        if not logo_match:
            failures.append("pages/login.html: header missing ../index.html .logo link")
        else:
            logo_text = re.sub(r"<[^>]+>", "", logo_match.group(1))
            if "ENERGYBOOST" not in re.sub(r"\s+", "", logo_text):
                failures.append("pages/login.html: header .logo missing 'ENERGYBOOST' text")

        search_box = extract_div_block(header_html, r'class="[^"]*\bsearch-box\b[^"]*"')
        if not search_box:
            failures.append("pages/login.html: missing .search-box inside header")
        else:
            if "openSearchDropdown()" not in search_box:
                failures.append("pages/login.html: .search-box missing openSearchDropdown() trigger")
            if "openAdvancedSearchModal()" not in search_box:
                failures.append("pages/login.html: .search-box missing openAdvancedSearchModal() trigger")

            dropdown = extract_div_block(search_box, r'id="search-dropdown-menu"')
            if not dropdown:
                failures.append("pages/login.html: missing #search-dropdown-menu")
            else:
                static_list = extract_div_block(dropdown, r'class="[^"]*\bsearch-static-list\b[^"]*"')
                if not static_list:
                    failures.append("pages/login.html: missing .search-static-list in #search-dropdown-menu")
                else:
                    items = re.findall(
                        r'<a\b[^>]*class="[^"]*\bsearch-static-item\b[^"]*"[^>]*>[\s\S]*?</a>',
                        static_list,
                    )
                    if len(items) != 5:
                        failures.append(
                            f"pages/login.html: expected 5 .search-static-item links, found {len(items)}"
                        )
                    else:
                        for idx, item in enumerate(items, start=1):
                            srcs = re.findall(r'\bsrc="([^"]+)"', item)
                            if not srcs or any(not src.startswith("../assets/images/") for src in srcs):
                                failures.append(
                                    f"pages/login.html: search item #{idx} image src must use '../assets/images/...', got {srcs}"
                                )

                        item4 = items[3]
                        if "Monster Energy Ultra White 355ml" not in item4:
                            failures.append(
                                "pages/login.html: search item #4 missing 'Monster Energy Ultra White 355ml'"
                            )

                        item5 = items[4]
                        if "Sting Vàng Sleek 330ml" not in item5:
                            failures.append(
                                "pages/login.html: search item #5 missing 'Sting Vàng Sleek 330ml'"
                            )
                        if "../assets/images/sting/sting-gold.webp" not in item5:
                            failures.append(
                                "pages/login.html: search item #5 missing '../assets/images/sting/sting-gold.webp'"
                            )
                        if 'href="product-detail-sting.html"' not in item5:
                            failures.append(
                                "pages/login.html: search item #5 must link to 'product-detail-sting.html'"
                            )

        header_actions = extract_div_block(header_html, r'class="[^"]*\bheader-actions\b[^"]*"')
        if not header_actions:
            failures.append("pages/login.html: missing .header-actions inside header")
        else:
            action_links = re.findall(
                r'<a\b[^>]*class="[^"]*\baction-btn\b[^"]*"[^>]*>[\s\S]*?</a>',
                header_actions,
            )
            if len(action_links) != 3:
                failures.append(
                    f"pages/login.html: expected 3 .action-btn links in .header-actions, found {len(action_links)}"
                )
            if 'href="orders.html"' not in header_actions:
                failures.append("pages/login.html: .header-actions missing orders.html link")
            if not re.search(
                r'<a\b[^>]*href="account\.html"[^>]*id="header-account-link"|<a\b[^>]*id="header-account-link"[^>]*href="account\.html"',
                header_actions,
            ):
                failures.append("pages/login.html: .header-actions missing #header-account-link to account.html")
            if 'id="header-account-value"' not in header_actions:
                failures.append("pages/login.html: .header-actions missing #header-account-value")
            if 'href="cart.html"' not in header_actions:
                failures.append("pages/login.html: .header-actions missing cart.html link")
            if not re.search(r'<span[^>]*class="[^"]*\baction-badge\b[^"]*"[^>]*>\s*7\s*</span>', header_actions):
                failures.append("pages/login.html: .header-actions cart link missing .action-badge with '7'")
            if "216.000đ" not in header_actions:
                failures.append("pages/login.html: .header-actions cart link missing '216.000đ'")

    # 4. <main class="login-page-main"> wrapping .breadcrumb and .login-card
    main_match = re.search(
        r'<main\b[^>]*class="[^"]*\blogin-page-main\b[^"]*"[^>]*>([\s\S]*?)</main>',
        html,
    )
    if not main_match:
        failures.append("pages/login.html: missing <main class='login-page-main'>")
    else:
        main_html = main_match.group(1)

        breadcrumb = extract_div_block(main_html, r'class="[^"]*\bbreadcrumb\b[^"]*"')
        if not breadcrumb:
            failures.append("pages/login.html: missing <div class='breadcrumb'> inside <main class='login-page-main'>")
        else:
            if "Trang chủ" not in breadcrumb:
                failures.append("pages/login.html: .breadcrumb missing 'Trang chủ'")
            if 'id="auth-breadcrumb-current"' not in breadcrumb:
                failures.append("pages/login.html: .breadcrumb missing #auth-breadcrumb-current")

        login_card = extract_div_block(main_html, r'class="[^"]*\blogin-card\b[^"]*"')
        if not login_card:
            failures.append("pages/login.html: missing .login-card inside <main class='login-page-main'>")
        else:
            for preserved in (
                'id="tab-login-btn"',
                'id="tab-register-btn"',
                'id="form-login"',
                'id="form-register"',
                'class="back-home-link"',
            ):
                if preserved not in login_card:
                    failures.append(f"pages/login.html: .login-card missing preserved '{preserved}'")

    # 5. Canonical 4-column <footer class="footer">
    footer_match = re.search(r'<footer\b[^>]*class="[^"]*\bfooter\b[^"]*"[^>]*>([\s\S]*?)</footer>', html)
    if not footer_match:
        failures.append("pages/login.html: missing <footer class='footer'>")
    else:
        footer_html = footer_match.group(0)
        if not extract_div_block(footer_html, r'class="[^"]*\bfooter-grid\b[^"]*"'):
            failures.append("pages/login.html: <footer> missing .footer-grid")
        for heading in ("CÁC DÒNG SẢN PHẨM", "HỆ THỐNG TRANG", "NHẬN VOUCHER ƯU ĐÃI"):
            if heading not in footer_html:
                failures.append(f"pages/login.html: <footer> missing '{heading}'")
        if not extract_div_block(footer_html, r'class="[^"]*\bfooter-bottom\b[^"]*"'):
            failures.append("pages/login.html: <footer> missing .footer-bottom")
        if "showToast('Đã đăng ký nhận tin Energy Boost thành công!'" not in footer_html:
            failures.append("pages/login.html: <footer> newsletter missing expected showToast call")

    # 6. #modal-adv-search exists before #toast-container
    adv_modal = extract_div_block(html, r'id="modal-adv-search"')
    if not adv_modal:
        failures.append("pages/login.html: missing #modal-adv-search modal")
    else:
        if "closeAdvancedSearchModal()" not in adv_modal:
            failures.append("pages/login.html: #modal-adv-search missing closeAdvancedSearchModal()")
        if "handleAdvancedSearch(event)" not in adv_modal:
            failures.append("pages/login.html: #modal-adv-search missing handleAdvancedSearch(event)")

    toast_pos = html.find('id="toast-container"')
    adv_pos = html.find('id="modal-adv-search"')
    if toast_pos == -1:
        failures.append("pages/login.html: missing #toast-container")
    elif adv_pos != -1 and adv_pos >= toast_pos:
        failures.append("pages/login.html: #modal-adv-search must appear before #toast-container")

    return failures


def verify_login_css(css: str) -> list[str]:
    failures: list[str] = []
    if not re.search(r"\.login-page-main\s*\{[^}]+\}", css):
        failures.append("css/style.css: missing .login-page-main rule definition")
    return failures


def verify_switch_auth_tab_runtime() -> list[str]:
    node_script = r"""
const fs = require('fs');
const vm = require('vm');
const assert = require('assert');

function makeClassList(initial = []) {
  const set = new Set(initial);
  return {
    add: (...cls) => cls.forEach((c) => set.add(c)),
    remove: (...cls) => cls.forEach((c) => set.delete(c)),
    contains: (c) => set.has(c),
    toggle: (c, force) => {
      if (force === undefined) {
        if (set.has(c)) { set.delete(c); return false; }
        set.add(c); return true;
      }
      if (force) { set.add(c); return true; }
      set.delete(c); return false;
    }
  };
}

function makeElement(id, initialClasses = [], initialDisplay = 'block', initialText = '') {
  return {
    id,
    classList: makeClassList(initialClasses),
    style: { display: initialDisplay },
    innerHTML: '',
    innerText: initialText,
    textContent: initialText
  };
}

const elements = {
  'tab-login-btn': makeElement('tab-login-btn', ['auth-tab-btn', 'active']),
  'tab-register-btn': makeElement('tab-register-btn', ['auth-tab-btn']),
  'form-login': makeElement('form-login', [], 'block'),
  'form-register': makeElement('form-register', [], 'none'),
  'auth-card-title': makeElement('auth-card-title'),
  'auth-card-desc': makeElement('auth-card-desc'),
  'auth-breadcrumb-current': makeElement('auth-breadcrumb-current', [], 'inline', 'Đăng nhập')
};

const sandbox = {
  console,
  setTimeout,
  clearTimeout,
  localStorage: {
    getItem: () => null,
    setItem: () => {},
    removeItem: () => {}
  },
  window: {
    addEventListener: () => {},
    location: { hash: '', href: '' }
  },
  document: {
    currentScript: { src: '' },
    querySelector: () => null,
    querySelectorAll: () => [],
    addEventListener: () => {},
    getElementById: (id) => elements[id] || null
  }
};

const code = fs.readFileSync('js/app.js', 'utf8');
vm.runInNewContext(code, sandbox, { filename: 'js/app.js' });

assert.strictEqual(typeof sandbox.switchAuthTab, 'function', 'switchAuthTab must be defined in js/app.js');

sandbox.switchAuthTab('register');
assert.strictEqual(elements['tab-login-btn'].classList.contains('active'), false, 'register: tab-login-btn active removed');
assert.strictEqual(elements['tab-register-btn'].classList.contains('active'), true, 'register: tab-register-btn active added');
assert.strictEqual(elements['form-login'].style.display, 'none', 'register: form-login hidden');
assert.strictEqual(elements['form-register'].style.display, 'block', 'register: form-register shown');
assert.ok(elements['auth-card-title'].innerHTML.includes('ĐĂNG KÝ'), 'register: auth-card-title updated');
assert.ok(elements['auth-card-desc'].innerText.includes('Đăng ký tài khoản'), 'register: auth-card-desc updated');
assert.strictEqual(elements['auth-breadcrumb-current'].textContent, 'Đăng ký', 'register: auth-breadcrumb-current updated');

sandbox.switchAuthTab('login');
assert.strictEqual(elements['tab-login-btn'].classList.contains('active'), true, 'login: tab-login-btn active added');
assert.strictEqual(elements['tab-register-btn'].classList.contains('active'), false, 'login: tab-register-btn active removed');
assert.strictEqual(elements['form-login'].style.display, 'block', 'login: form-login shown');
assert.strictEqual(elements['form-register'].style.display, 'none', 'login: form-register hidden');
assert.ok(elements['auth-card-title'].innerHTML.includes('ĐĂNG NHẬP'), 'login: auth-card-title restored');
assert.ok(elements['auth-card-desc'].innerText.includes('Đăng nhập tài khoản'), 'login: auth-card-desc restored');
assert.strictEqual(elements['auth-breadcrumb-current'].textContent, 'Đăng nhập', 'login: auth-breadcrumb-current restored');

console.log('NODE VM OK: switchAuthTab(register) -> switchAuthTab(login) toggled all 7 DOM elements cleanly.');
"""
    proc = subprocess.run(
        ["node", "-e", node_script],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout).strip()
        return [f"js/app.js runtime switchAuthTab check failed: {err}"]
    print(proc.stdout.strip())
    return []


def main() -> int:
    login_path = ROOT / "pages" / "login.html"
    css_path = ROOT / "css" / "style.css"
    app_js_path = ROOT / "js" / "app.js"

    for required in (login_path, css_path, app_js_path):
        if not required.is_file():
            print(f"FAIL: missing file {required}")
            return 1

    failures: list[str] = []
    failures.extend(verify_login_html(login_path.read_text(encoding="utf-8")))
    failures.extend(verify_login_css(css_path.read_text(encoding="utf-8")))
    failures.extend(verify_switch_auth_tab_runtime())

    if failures:
        print(f"FAIL ({len(failures)} checks failed):")
        for item in failures:
            print(f"  - {item}")
        return 1

    print(
        "ALL CHECKS PASSED: pages/login.html header/search/actions/breadcrumb/footer/#modal-adv-search, css/style.css .login-page-main, and js/app.js switchAuthTab runtime verified."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
