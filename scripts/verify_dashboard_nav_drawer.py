import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

STOREFRONT_NAV_TARGETS = [
    ("index.html", "#top", "#", "monster-products"),
    ("pages/product-detail.html", "../index.html", "../index.html#", "monster-products"),
    ("pages/product-detail-redbull.html", "../index.html", "../index.html#", "redbull-products"),
    ("pages/product-detail-redbull-thai.html", "../index.html", "../index.html#", "redbull-products"),
    ("pages/product-detail-redbull-lonvua.html", "../index.html", "../index.html#", "redbull-products"),
    ("pages/product-detail-sting.html", "../index.html", "../index.html#", "sting-products"),
    ("pages/search-results.html", "../index.html", "../index.html#", None),
]


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


def _extract_classes(tag: str) -> list[str]:
    class_match = re.search(r'\bclass="([^"]*)"', tag)
    return class_match.group(1).split() if class_match else []


def verify_nav_drawer_html(
    html: str,
    filename: str,
    expected_home_href: str,
    expected_brand_prefix: str,
    expected_active_brand: Optional[str],
) -> list[str]:
    failures: list[str] = []

    nav_match = re.search(r'<ul\b[^>]*class="[^"]*\bnav-menu\b[^"]*"[^>]*>([\s\S]*?)</ul>', html)
    if not nav_match:
        failures.append(f"{filename}: missing <ul class='nav-menu'> wrapper")
        return failures

    nav_html = nav_match.group(0)

    home_match = re.search(r'<a\b[^>]*id="nav-home-btn"[^>]*>([\s\S]*?)</a>', nav_html)
    if not home_match:
        failures.append(f"{filename}: missing #nav-home-btn inside .nav-menu")
    else:
        home_tag = home_match.group(0)
        if f'href="{expected_home_href}"' not in home_tag:
            failures.append(
                f"{filename}: #nav-home-btn must have href='{expected_home_href}'"
            )
        if "scrollToDashboardTop(event, this)" not in home_tag:
            failures.append(f"{filename}: #nav-home-btn must call scrollToDashboardTop(event, this)")
        if "Trang chủ" not in home_match.group(1):
            failures.append(f"{filename}: #nav-home-btn missing 'Trang chủ' label")

    toggle_match = re.search(r'<button\b[^>]*id="nav-brand-toggle"[^>]*>([\s\S]*?)</button>', nav_html)
    if not toggle_match:
        failures.append(f"{filename}: missing #nav-brand-toggle button inside .nav-menu")
    else:
        toggle_tag = toggle_match.group(0)
        if "toggleBrandDrawer(this)" not in toggle_tag:
            failures.append(f"{filename}: #nav-brand-toggle must call toggleBrandDrawer(this)")
        if 'aria-expanded="false"' not in toggle_tag:
            failures.append(f"{filename}: #nav-brand-toggle must default to aria-expanded='false'")
        if 'aria-controls="nav-brand-drawer"' not in toggle_tag:
            failures.append(
                f"{filename}: #nav-brand-toggle must include aria-controls='nav-brand-drawer'"
            )

    drawer_html = extract_div_block(nav_html, r'id="nav-brand-drawer"')
    if not drawer_html:
        failures.append(f"{filename}: missing #nav-brand-drawer container inside .nav-menu")
    else:
        open_tag_match = re.match(r"<div\b[^>]*>", drawer_html)
        drawer_open_tag = open_tag_match.group(0) if open_tag_match else ""
        if 'aria-hidden="true"' not in drawer_open_tag:
            failures.append(f"{filename}: #nav-brand-drawer must start with aria-hidden='true'")
        if "nav-brand-drawer" not in _extract_classes(drawer_open_tag):
            failures.append(f"{filename}: #nav-brand-drawer missing .nav-brand-drawer class")

        expected_brands = [
            ("monster-products", "Monster"),
            ("redbull-products", "Redbull"),
            ("sting-products", "Sting"),
        ]
        brand_anchors = re.findall(r"<a\b[^>]*>[\s\S]*?</a>", drawer_html)
        if len(brand_anchors) != 3:
            failures.append(
                f"{filename}: #nav-brand-drawer expected 3 brand anchors, found {len(brand_anchors)}"
            )

        for target_id, label in expected_brands:
            expected_href = f"{expected_brand_prefix}{target_id}"
            anchor_pattern = rf'<a\b[^>]*href="{re.escape(expected_href)}"[^>]*>[\s\S]*?{re.escape(label)}[\s\S]*?</a>'
            anchor_tag = next(
                (a for a in brand_anchors if re.fullmatch(anchor_pattern, a)),
                "",
            )
            if not anchor_tag:
                failures.append(
                    f"{filename}: #nav-brand-drawer missing brand anchor '{label}' linking to '{expected_href}'"
                )
            else:
                if f"handleNavBrandClick(event, this, '{target_id}')" not in anchor_tag:
                    failures.append(
                        f"{filename}: brand anchor '{label}' missing onclick handleNavBrandClick(event, this, '{target_id}')"
                    )
                classes = _extract_classes(anchor_tag)
                if "nav-link" not in classes:
                    failures.append(f"{filename}: brand anchor '{label}' missing .nav-link class")
                if "nav-brand-item" not in classes:
                    failures.append(f"{filename}: brand anchor '{label}' missing .nav-brand-item class")
                is_active = "active" in classes
                should_be_active = expected_active_brand == target_id
                if should_be_active and not is_active:
                    failures.append(
                        f"{filename}: expected brand anchor '{label}' ({target_id}) to have .active class"
                    )
                elif not should_be_active and is_active:
                    failures.append(
                        f"{filename}: brand anchor '{label}' ({target_id}) must NOT have .active class"
                    )

    active_brand_items = [
        tag
        for tag in re.findall(r"<a\b[^>]*>", nav_html)
        if "nav-brand-item" in _extract_classes(tag) and "active" in _extract_classes(tag)
    ]
    expected_active_count = 1 if expected_active_brand else 0
    if len(active_brand_items) != expected_active_count:
        failures.append(
            f"{filename}: expected {expected_active_count} active .nav-menu .nav-brand-item link(s), found {len(active_brand_items)}"
        )

    return failures


def verify_css_rules(css_text: str) -> list[str]:
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

    nav_menu_blocks = extract_css_blocks(css_text, ".nav-menu")
    if not nav_menu_blocks or "align-items: center;" not in nav_menu_blocks[0]:
        failures.append("css/style.css: primary .nav-menu rule missing 'align-items: center;'")
    top_level_nav_menu = re.findall(r"(?:^|\n)\.nav-menu\s*\{", css_text)
    if len(top_level_nav_menu) != 1:
        failures.append(f"css/style.css: expected single top-level .nav-menu rule, found {len(top_level_nav_menu)}")

    toggle_btn_blocks = extract_css_blocks(css_text, ".nav-brand-toggle-btn")
    if not toggle_btn_blocks or "line-height: inherit;" not in toggle_btn_blocks[0]:
        failures.append("css/style.css: .nav-brand-toggle-btn missing 'line-height: inherit;'")

    compact_blocks = extract_media_blocks(css_text, "(max-width: 1200px) and (min-width: 769px)")
    if not any(
        re.search(r"\.nav-brand-group\s*,\s*\.nav-brand-drawer\s*\{[^}]*\bgap:\s*5px\s*;", block)
        for block in compact_blocks
    ):
        failures.append(
            "css/style.css: missing .nav-brand-group, .nav-brand-drawer { gap: 5px; } inside @media (max-width: 1200px) and (min-width: 769px)"
        )

    reduced_blocks = extract_media_blocks(css_text, "prefers-reduced-motion: reduce")
    if not any(".nav-brand-drawer" in b and "transition: none" in b for b in reduced_blocks):
        failures.append(
            "css/style.css: missing @media (prefers-reduced-motion: reduce) rule disabling transitions for .nav-brand-drawer"
        )

    return failures


verify_drawer_css = verify_css_rules


def verify_js_static(app_js: str) -> list[str]:
    failures: list[str] = []

    for fn_name in (
        "resolveNavRoot",
        "syncDashboardNavActiveState",
        "scrollToDashboardTop",
        "toggleBrandDrawer",
        "handleNavBrandClick",
        "changeDashboardPage",
    ):
        if not extract_function(app_js, fn_name):
            failures.append(f"js/app.js: missing function {fn_name}")

    for fn_name in (
        "scrollToDashboardTop",
        "toggleBrandDrawer",
        "handleNavBrandClick",
        "changeDashboardPage",
    ):
        if f"window.{fn_name} = {fn_name}" not in app_js:
            failures.append(f"js/app.js: missing window.{fn_name} export")

    sync_fn = extract_function(app_js, "syncDashboardNavActiveState")
    if sync_fn:
        if '.nav-menu .nav-link[href*="-products"]' not in sync_fn:
            failures.append(
                "js/app.js: syncDashboardNavActiveState must scope active updates to '.nav-menu .nav-link[href*=\"-products\"]'"
            )
        if "getElementById('nav-home-btn')" not in sync_fn or "classList.toggle('active'" not in sync_fn:
            failures.append(
                "js/app.js: syncDashboardNavActiveState must toggle .active on #nav-home-btn"
            )

    change_fn = extract_function(app_js, "changeDashboardPage")
    if change_fn and "syncDashboardNavActiveState(" not in change_fn:
        failures.append("js/app.js: changeDashboardPage must call syncDashboardNavActiveState")

    brand_click_fn = extract_function(app_js, "handleNavBrandClick")
    if brand_click_fn:
        if "syncDashboardNavActiveState(" not in brand_click_fn:
            failures.append("js/app.js: handleNavBrandClick must call syncDashboardNavActiveState")
        if "resolveNavRoot()" not in brand_click_fn:
            failures.append("js/app.js: handleNavBrandClick must use resolveNavRoot() for subpage redirects")

    top_fn = extract_function(app_js, "scrollToDashboardTop")
    if top_fn:
        if "syncDashboardNavActiveState(" not in top_fn:
            failures.append("js/app.js: scrollToDashboardTop must call syncDashboardNavActiveState")
        if "resolveNavRoot()" not in top_fn:
            failures.append("js/app.js: scrollToDashboardTop must use resolveNavRoot() for subpage redirects")

    return failures


def main() -> int:
    failures: list[str] = []

    for rel_path, expected_home_href, expected_brand_prefix, expected_active_brand in STOREFRONT_NAV_TARGETS:
        page_path = ROOT / rel_path
        if not page_path.exists():
            failures.append(f"{rel_path}: missing file")
            continue
        html = page_path.read_text(encoding="utf-8")
        failures.extend(
            verify_nav_drawer_html(
                html,
                rel_path,
                expected_home_href,
                expected_brand_prefix,
                expected_active_brand,
            )
        )

    css_text = (ROOT / "css" / "style.css").read_text(encoding="utf-8")
    app_js = (ROOT / "js" / "app.js").read_text(encoding="utf-8")

    failures.extend(verify_css_rules(css_text))
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
const pagePrev = makeElement({ id: 'page-btn-prev', initialClasses: ['page-btn', 'disabled'], initialAttrs: { 'aria-disabled': 'true' } });
const pageNext = makeElement({ id: 'page-btn-next', initialClasses: ['page-btn'] });
const catalogPagination = {
  id: 'catalog-pagination',
  querySelector: (selector) => {
    if (selector === '#page-btn-prev') return pagePrev;
    if (selector === '#page-btn-next') return pageNext;
    return null;
  },
  querySelectorAll: (selector) => {
    if (selector === '.page-btn[data-page]') return [pageBtn1, pageBtn2, pageBtn3];
    return [];
  },
};

const elementsById = {
  'nav-home-btn': homeBtn,
  'nav-brand-toggle': brandToggle,
  'nav-brand-drawer': brandDrawer,
  'monster-products': monsterSection,
  'redbull-products': redbullSection,
  'sting-products': stingSection,
  'catalog-pagination': catalogPagination,
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
    querySelector: (selector) => {
      if (selector === '.pagination-strip') return catalogPagination;
      return null;
    },
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

// 0. Non-DOM guard: toggleBrandDrawer safely returns false when document is undefined
const origDocument = sandbox.document;
sandbox.document = undefined;
try {
  if (sandbox.window.toggleBrandDrawer(brandToggle) !== false) {
    throw new Error('toggleBrandDrawer must return false safely when document is undefined');
  }
} finally {
  sandbox.document = origDocument;
}

// 1. toggleBrandDrawer opens and closes with synchronized ARIA + is-open classes (both explicit btn and fallback lookup)
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

const closed = sandbox.window.toggleBrandDrawer();
if (
  closed !== false ||
  brandDrawer.classList.contains('is-open') ||
  brandToggle.classList.contains('is-open') ||
  brandDrawer.getAttribute('aria-hidden') !== 'true' ||
  brandToggle.getAttribute('aria-expanded') !== 'false'
) {
  throw new Error('toggleBrandDrawer() without btn argument did not close drawer with expected classes and ARIA attributes');
}

delete elementsById['nav-brand-drawer'];
if (sandbox.window.toggleBrandDrawer(brandToggle) !== false) {
  throw new Error('toggleBrandDrawer should return false when #nav-brand-drawer is missing');
}
elementsById['nav-brand-drawer'] = brandDrawer;

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
  homeBtn.classList.contains('active') ||
  pageBtn1.classList.contains('active') ||
  !pageBtn2.classList.contains('active') ||
  pageBtn3.classList.contains('active') ||
  pagePrev.classList.contains('disabled') ||
  pagePrev.getAttribute('aria-disabled') !== null ||
  pageNext.classList.contains('disabled') ||
  pageNext.getAttribute('aria-disabled') !== null
) {
  throw new Error('handleNavBrandClick failed to sync brand active state, pagination UI, or clear #nav-home-btn');
}

// 4. changeDashboardPage scopes .active to .nav-menu .nav-link[href*="-products"], clears #nav-home-btn, updates pagination UI, without touching #nav-brand-toggle
brandToggle.classList.add('active');
homeBtn.classList.add('active');
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
  !brandToggle.classList.contains('active') ||
  pageBtn1.classList.contains('active') ||
  pageBtn2.classList.contains('active') ||
  !pageBtn3.classList.contains('active') ||
  pagePrev.classList.contains('disabled') ||
  pagePrev.getAttribute('aria-disabled') !== null ||
  !pageNext.classList.contains('disabled') ||
  pageNext.getAttribute('aria-disabled') !== 'true'
) {
  throw new Error('changeDashboardPage(3) failed active-class clearing/scoping or pagination UI transition');
}

const page1Ret = sandbox.window.changeDashboardPage(1, mockEvent);
if (
  page1Ret !== false ||
  sandbox.window.currentDashboardPage !== 1 ||
  !monsterLink.classList.contains('active') ||
  redbullLink.classList.contains('active') ||
  stingLink.classList.contains('active') ||
  monsterSection._scrollIntoViewCalls.length !== 1 ||
  !pageBtn1.classList.contains('active') ||
  pageBtn2.classList.contains('active') ||
  pageBtn3.classList.contains('active') ||
  !pagePrev.classList.contains('disabled') ||
  pagePrev.getAttribute('aria-disabled') !== 'true' ||
  pageNext.classList.contains('disabled') ||
  pageNext.getAttribute('aria-disabled') !== null
) {
  throw new Error('changeDashboardPage(1) failed to restore monster-products active state and pagination UI');
}

// Boundary check: out-of-range page should be ignored cleanly
if (sandbox.window.changeDashboardPage(4, mockEvent) !== false || sandbox.window.currentDashboardPage !== 1) {
  throw new Error('changeDashboardPage(4) should reject out-of-range page without mutating state');
}

// 5. Subpage behavior when dashboard sections (#monster-products, etc.) are absent
delete elementsById['monster-products'];
delete elementsById['redbull-products'];
delete elementsById['sting-products'];

sandbox.window.location.href = 'pages/product-detail-redbull.html';
const subTopRet = sandbox.window.scrollToDashboardTop(mockEvent, homeBtn);
if (subTopRet !== false || sandbox.window.location.href !== '../index.html') {
  throw new Error(
    `Subpage scrollToDashboardTop failed: ret=${subTopRet}, href=${sandbox.window.location.href}`
  );
}

const stingSubLink = makeElement({
  href: '../index.html#sting-products',
  textContent: 'Sting',
  initialClasses: ['nav-link', 'nav-brand-item'],
});
sandbox.window.location.href = 'pages/product-detail-redbull.html';
const subBrandRet = sandbox.window.handleNavBrandClick(mockEvent, stingSubLink);
if (subBrandRet !== false || sandbox.window.location.href !== '../index.html#sting-products') {
  throw new Error(
    `Subpage handleNavBrandClick failed: ret=${subBrandRet}, href=${sandbox.window.location.href}`
  );
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
        "ALL CHECKS PASSED: 7 storefront pages collapsible brand drawer, CSS slide/compact/reduced-motion rules, JS static wiring, and Node.js dashboard/subpage runtime verified."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
