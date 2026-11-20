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


def verify_index_nav_html(index_html: str) -> list[str]:
    failures: list[str] = []

    nav_match = re.search(r'<ul\b[^>]*class="[^"]*\bnav-menu\b[^"]*"[^>]*>([\s\S]*?)</ul>', index_html)
    if not nav_match:
        failures.append("index.html: missing <ul class='nav-menu'> wrapper")
        return failures

    nav_html = nav_match.group(0)

    home_match = re.search(r'<a\b[^>]*id="nav-home-btn"[^>]*>([\s\S]*?)</a>', nav_html)
    if not home_match:
        failures.append("index.html: missing #nav-home-btn inside .nav-menu")
    else:
        if "scrollToDashboardTop(event, this)" not in home_match.group(0):
            failures.append("index.html: #nav-home-btn must call scrollToDashboardTop(event, this)")
        if "Trang chủ" not in home_match.group(1):
            failures.append("index.html: #nav-home-btn missing 'Trang chủ' label")

    toggle_match = re.search(r'<button\b[^>]*id="nav-brand-toggle"[^>]*>([\s\S]*?)</button>', nav_html)
    if not toggle_match:
        failures.append("index.html: missing #nav-brand-toggle button inside .nav-menu")
    else:
        toggle_tag = toggle_match.group(0)
        if "toggleBrandDrawer(this)" not in toggle_tag:
            failures.append("index.html: #nav-brand-toggle must call toggleBrandDrawer(this)")
        if 'aria-expanded="false"' not in toggle_tag:
            failures.append("index.html: #nav-brand-toggle must default to aria-expanded='false'")
        if 'aria-controls="nav-brand-drawer"' not in toggle_tag:
            failures.append("index.html: #nav-brand-toggle must include aria-controls='nav-brand-drawer'")

    drawer_match = re.search(r'<div\b[^>]*id="nav-brand-drawer"[^>]*>([\s\S]*?)</div>', nav_html)
    if not drawer_match:
        failures.append("index.html: missing #nav-brand-drawer container inside .nav-menu")
    else:
        drawer_html = drawer_match.group(0)
        if 'aria-hidden="true"' not in drawer_html:
            failures.append("index.html: #nav-brand-drawer must start with aria-hidden='true'")
        if "nav-brand-drawer" not in drawer_html:
            failures.append("index.html: #nav-brand-drawer missing .nav-brand-drawer class")

        expected_brands = [
            ("monster-products", "Monster"),
            ("redbull-products", "Redbull"),
            ("sting-products", "Sting"),
        ]
        brand_anchors = re.findall(r"<a\b[^>]*>[\s\S]*?</a>", drawer_html)
        if len(brand_anchors) != 3:
            failures.append(
                f"index.html: #nav-brand-drawer expected 3 brand anchors, found {len(brand_anchors)}"
            )
        for target_id, label in expected_brands:
            anchor_pattern = rf'<a\b[^>]*href="#{re.escape(target_id)}"[^>]*>[\s\S]*?{re.escape(label)}[\s\S]*?</a>'
            anchor_match = re.search(anchor_pattern, drawer_html)
            if not anchor_match:
                failures.append(
                    f"index.html: #nav-brand-drawer missing brand anchor '{label}' linking to '#{target_id}'"
                )
            else:
                anchor_tag = anchor_match.group(0)
                if f"handleNavBrandClick(event, this, '{target_id}')" not in anchor_tag:
                    failures.append(
                        f"index.html: brand anchor '{label}' missing onclick handleNavBrandClick(event, this, '{target_id}')"
                    )
                if "nav-link" not in anchor_tag:
                    failures.append(f"index.html: brand anchor '{label}' missing .nav-link class")

    return failures


def verify_drawer_css(css_text: str) -> list[str]:
    failures: list[str] = []

    drawer_blocks = extract_css_blocks(css_text, ".nav-brand-drawer")
    if not drawer_blocks:
        failures.append("css/style.css: missing .nav-brand-drawer rule")
    else:
        block = drawer_blocks[0]
        for token in (
            "max-width: 0;",
            "opacity: 0;",
            "overflow: hidden;",
            "visibility: hidden;",
            "transform: translateX(-14px);",
            "transition:",
        ):
            if token not in block:
                failures.append(f"css/style.css: .nav-brand-drawer missing '{token}'")

    open_blocks = extract_css_blocks(css_text, ".nav-brand-drawer.is-open")
    if not open_blocks:
        failures.append("css/style.css: missing .nav-brand-drawer.is-open rule")
    else:
        block = open_blocks[0]
        for token in (
            "visibility: visible;",
            "max-width: 460px;",
            "opacity: 1;",
            "transform: translateX(0);",
        ):
            if token not in block:
                failures.append(f"css/style.css: .nav-brand-drawer.is-open missing '{token}'")

    if not extract_css_blocks(css_text, ".nav-brand-toggle-btn.is-open .nav-brand-chevron"):
        failures.append("css/style.css: missing .nav-brand-toggle-btn.is-open .nav-brand-chevron rule")

    reduced_blocks = extract_media_blocks(css_text, "prefers-reduced-motion: reduce")
    if not any(".nav-brand-drawer" in b and "transition: none" in b for b in reduced_blocks):
        failures.append(
            "css/style.css: missing @media (prefers-reduced-motion: reduce) rule disabling transitions for .nav-brand-drawer"
        )

    return failures


def verify_js_static(app_js: str) -> list[str]:
    failures: list[str] = []
    for fn_name in (
        "scrollToDashboardTop",
        "toggleBrandDrawer",
        "handleNavBrandClick",
        "changeDashboardPage",
    ):
        if not extract_function(app_js, fn_name):
            failures.append(f"js/app.js: missing function {fn_name}")
        if f"window.{fn_name} = {fn_name}" not in app_js:
            failures.append(f"js/app.js: missing window.{fn_name} export")

    change_fn = extract_function(app_js, "changeDashboardPage")
    if '.nav-menu .nav-link[href*="-products"]' not in change_fn:
        failures.append(
            "js/app.js: changeDashboardPage must scope active class updates to '.nav-menu .nav-link[href*=\"-products\"]'"
        )

    return failures


def main() -> int:
    failures: list[str] = []

    index_html = (ROOT / "index.html").read_text(encoding="utf-8")
    css_text = (ROOT / "css" / "style.css").read_text(encoding="utf-8")
    app_js = (ROOT / "js" / "app.js").read_text(encoding="utf-8")

    failures.extend(verify_index_nav_html(index_html))
    failures.extend(verify_drawer_css(css_text))
    failures.extend(verify_js_static(app_js))

    node_test = r"""
const fs = require('fs');
const vm = require('vm');
const path = require('path');

const appCode = fs.readFileSync(path.join(process.cwd(), 'js', 'app.js'), 'utf8');

function makeElement({ id = '', href = '', dataTarget = '', textContent = '', initialClasses = [], initialAttrs = {} }) {
  const classes = new Set(initialClasses);
  const attrs = { ...initialAttrs };
  if (href) attrs.href = href;
  if (dataTarget) attrs['data-target'] = dataTarget;
  const scrollIntoViewCalls = [];

  return {
    id,
    textContent,
    classList: {
      add: (c) => classes.add(c),
      remove: (c) => classes.delete(c),
      contains: (c) => classes.has(c),
      toggle: (c, force) => {
        if (force === undefined) {
          if (classes.has(c)) {
            classes.delete(c);
            return false;
          }
          classes.add(c);
          return true;
        }
        if (force) {
          classes.add(c);
          return true;
        }
        classes.delete(c);
        return false;
      },
    },
    getAttribute: (name) => (Object.prototype.hasOwnProperty.call(attrs, name) ? attrs[name] : null),
    setAttribute: (name, value) => { attrs[name] = String(value); },
    removeAttribute: (name) => { delete attrs[name]; },
    getBoundingClientRect: () => ({ top: id === 'redbull-products' ? 900 : id === 'sting-products' ? 1700 : 300 }),
    scrollIntoView: (opts) => { scrollIntoViewCalls.push(opts); },
    _scrollIntoViewCalls: scrollIntoViewCalls,
    _classes: classes,
    _attrs: attrs,
  };
}

const homeBtn = makeElement({
  id: 'nav-home-btn',
  href: '#top',
  textContent: 'Trang chủ',
  initialClasses: ['nav-link', 'nav-home-link'],
});
const brandToggle = makeElement({
  id: 'nav-brand-toggle',
  textContent: 'Nhãn hàng',
  initialClasses: ['nav-link', 'nav-brand-toggle-btn'],
  initialAttrs: { 'aria-expanded': 'false', 'aria-controls': 'nav-brand-drawer' },
});
const brandDrawer = makeElement({
  id: 'nav-brand-drawer',
  initialClasses: ['nav-brand-drawer'],
  initialAttrs: { 'aria-hidden': 'true' },
});

const monsterLink = makeElement({
  href: '#monster-products',
  textContent: 'Monster',
  initialClasses: ['nav-link', 'nav-brand-item', 'active'],
});
const redbullLink = makeElement({
  href: '#redbull-products',
  textContent: 'Redbull',
  initialClasses: ['nav-link', 'nav-brand-item'],
});
const stingLink = makeElement({
  href: '#sting-products',
  textContent: 'Sting',
  initialClasses: ['nav-link', 'nav-brand-item'],
});
const brandNavLinks = [monsterLink, redbullLink, stingLink];

const quickMonster = makeElement({ dataTarget: 'monster-products', textContent: 'Monster', initialClasses: ['quick-brand-btn', 'active'] });
const quickRedbull = makeElement({ dataTarget: 'redbull-products', textContent: 'Redbull', initialClasses: ['quick-brand-btn'] });
const quickSting = makeElement({ dataTarget: 'sting-products', textContent: 'Sting', initialClasses: ['quick-brand-btn'] });
const quickBtns = [quickMonster, quickRedbull, quickSting];

const monsterSection = makeElement({ id: 'monster-products' });
const redbullSection = makeElement({ id: 'redbull-products' });
const stingSection = makeElement({ id: 'sting-products' });

const pageBtn1 = makeElement({ initialClasses: ['page-btn', 'active'], initialAttrs: { 'data-page': '1' } });
const pageBtn2 = makeElement({ initialClasses: ['page-btn'], initialAttrs: { 'data-page': '2' } });
const pageBtn3 = makeElement({ initialClasses: ['page-btn'], initialAttrs: { 'data-page': '3' } });
const pagePrev = makeElement({ id: 'page-btn-prev', initialClasses: ['page-btn', 'disabled'] });
const pageNext = makeElement({ id: 'page-btn-next', initialClasses: ['page-btn'] });

const elementsById = {
  'nav-home-btn': homeBtn,
  'nav-brand-toggle': brandToggle,
  'nav-brand-drawer': brandDrawer,
  'monster-products': monsterSection,
  'redbull-products': redbullSection,
  'sting-products': stingSection,
  'page-btn-prev': pagePrev,
  'page-btn-next': pageNext,
};

const scrollCalls = [];
const sandbox = {
  console,
  URLSearchParams,
  window: {
    location: { pathname: '/index.html', search: '' },
    pageYOffset: 120,
    scrollTo: (opts) => scrollCalls.push(opts),
    addEventListener: () => {},
  },
  document: {
    readyState: 'loading',
    addEventListener: () => {},
    getElementById: (id) => elementsById[id] || null,
    querySelector: () => null,
    querySelectorAll: (selector) => {
      if (selector === '.nav-menu .nav-link[href*="-products"]') return brandNavLinks;
      if (selector === '.nav-menu .nav-link[href*="-products"], .quick-brand-nav .quick-brand-btn') {
        return [...brandNavLinks, ...quickBtns];
      }
      if (selector === '.pagination-strip .page-btn[data-page]') return [pageBtn1, pageBtn2, pageBtn3];
      return [];
    },
    body: { style: {}, appendChild: () => {} },
  },
  localStorage: {
    getItem: () => '[]',
    setItem: () => {},
  },
};

vm.createContext(sandbox);
vm.runInContext(appCode, sandbox);

// 1. toggleBrandDrawer opens and closes with synchronized ARIA + is-open classes
const opened = sandbox.window.toggleBrandDrawer(brandToggle);
if (
  opened !== true ||
  !brandDrawer.classList.contains('is-open') ||
  !brandToggle.classList.contains('is-open') ||
  brandDrawer.getAttribute('aria-hidden') !== 'false' ||
  brandToggle.getAttribute('aria-expanded') !== 'true'
) {
  throw new Error('toggleBrandDrawer did not open drawer with expected classes and ARIA attributes');
}

const closed = sandbox.window.toggleBrandDrawer(brandToggle);
if (
  closed !== false ||
  brandDrawer.classList.contains('is-open') ||
  brandToggle.classList.contains('is-open') ||
  brandDrawer.getAttribute('aria-hidden') !== 'true' ||
  brandToggle.getAttribute('aria-expanded') !== 'false'
) {
  throw new Error('toggleBrandDrawer did not close drawer with expected classes and ARIA attributes');
}

// 2. scrollToDashboardTop resets brand active links, activates #nav-home-btn, scrolls top, preserves toggle
let prevented = false;
let stopped = false;
const mockEvent = {
  preventDefault: () => { prevented = true; },
  stopPropagation: () => { stopped = true; },
};

scrollCalls.length = 0;
const topRet = sandbox.window.scrollToDashboardTop(mockEvent, homeBtn);
if (
  topRet !== false ||
  !prevented ||
  !stopped ||
  scrollCalls.length !== 1 ||
  scrollCalls[0].top !== 0 ||
  scrollCalls[0].behavior !== 'smooth'
) {
  throw new Error(`scrollToDashboardTop scroll/event failure: ret=${topRet}, calls=${JSON.stringify(scrollCalls)}`);
}
if (
  !homeBtn.classList.contains('active') ||
  monsterLink.classList.contains('active') ||
  redbullLink.classList.contains('active') ||
  stingLink.classList.contains('active') ||
  brandToggle.classList.contains('active')
) {
  throw new Error('scrollToDashboardTop did not scope active state to #nav-home-btn and clear brand links');
}

// 3. handleNavBrandClick scrolls to target section, updates pagination, clears #nav-home-btn active
scrollCalls.length = 0;
const brandRet = sandbox.window.handleNavBrandClick(mockEvent, redbullLink, 'redbull-products');
if (
  brandRet !== false ||
  scrollCalls.length !== 1 ||
  scrollCalls[0].top !== 910 ||
  scrollCalls[0].behavior !== 'smooth'
) {
  throw new Error(`handleNavBrandClick scroll failure: ret=${brandRet}, calls=${JSON.stringify(scrollCalls)}`);
}
if (
  sandbox.window.currentDashboardPage !== 2 ||
  !redbullLink.classList.contains('active') ||
  monsterLink.classList.contains('active') ||
  stingLink.classList.contains('active') ||
  !quickRedbull.classList.contains('active') ||
  quickMonster.classList.contains('active') ||
  homeBtn.classList.contains('active')
) {
  throw new Error('handleNavBrandClick failed to sync brand active state or clear #nav-home-btn');
}

// 4. changeDashboardPage scopes .active to .nav-menu .nav-link[href*="-products"] without touching #nav-home-btn or #nav-brand-toggle
brandToggle.classList.add('active');
const page3Ret = sandbox.window.changeDashboardPage(3, mockEvent);
if (page3Ret !== false || sandbox.window.currentDashboardPage !== 3) {
  throw new Error(`changeDashboardPage(3) failed: ret=${page3Ret}, page=${sandbox.window.currentDashboardPage}`);
}
if (
  !stingLink.classList.contains('active') ||
  monsterLink.classList.contains('active') ||
  redbullLink.classList.contains('active') ||
  stingSection._scrollIntoViewCalls.length !== 1 ||
  homeBtn.classList.contains('active') ||
  !brandToggle.classList.contains('active')
) {
  throw new Error('changeDashboardPage(3) failed active-class scoping on .nav-menu .nav-link[href*="-products"]');
}

const page1Ret = sandbox.window.changeDashboardPage(1, mockEvent);
if (
  page1Ret !== false ||
  sandbox.window.currentDashboardPage !== 1 ||
  !monsterLink.classList.contains('active') ||
  redbullLink.classList.contains('active') ||
  stingLink.classList.contains('active') ||
  monsterSection._scrollIntoViewCalls.length !== 1
) {
  throw new Error('changeDashboardPage(1) failed to restore monster-products active state');
}

// Boundary check: out-of-range page should be ignored cleanly
if (sandbox.window.changeDashboardPage(4, mockEvent) !== false || sandbox.window.currentDashboardPage !== 1) {
  throw new Error('changeDashboardPage(4) should reject out-of-range page without mutating state');
}

console.log('NODE_DASHBOARD_NAV_DRAWER_PASS');
"""

    proc = subprocess.run(
        ["node", "-e", node_test],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if proc.returncode != 0 or "NODE_DASHBOARD_NAV_DRAWER_PASS" not in proc.stdout:
        failures.append(
            f"Node.js runtime test failed (exit {proc.returncode}): {(proc.stderr or proc.stdout).strip()}"
        )

    if failures:
        print(f"FAIL ({len(failures)} checks failed):")
        for item in failures:
            print(f"  - {item}")
        return 1

    print(
        "ALL CHECKS PASSED: index.html collapsible brand drawer, CSS slide/reduced-motion rules, and Node.js nav drawer/pagination runtime verified."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
