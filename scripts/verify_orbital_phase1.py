# -*- coding: utf-8 -*-
"""
verify_orbital_phase1.py
Phase 1 QA & Real Chromium Playwright Verifier for ENERGY BOOST STORE.

Stage 1: Static Integrity Audit across Orbital CSS, JS, and all 7 Phase 1 HTML files.
Stage 2: Real Headless Chromium Verification via Node Playwright + Ephemeral Local HTTP Server.

Exits 0 ONLY when every Stage 1 and Stage 2 check passes; exits 1 on any failure.
"""

from __future__ import annotations

import functools
import http.server
import json
import mimetypes
import os
import re
import socketserver
import subprocess
import sys
import tempfile
import threading
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

PHASE1_CSS_FILES = [
    "css/orbital-tokens.css",
    "css/orbital-storefront.css",
]

PHASE1_JS_FILES = [
    "js/orbital-webgl.js",
    "js/orbital-motion.js",
    "js/app.js",
]

PHASE1_HTML_FILES = [
    "index.html",
    "pages/product-detail.html",
    "pages/product-detail-redbull.html",
    "pages/product-detail-redbull-thai.html",
    "pages/product-detail-redbull-lonvua.html",
    "pages/product-detail-sting.html",
    "pages/search-results.html",
]

PHASE2_3_SMOKE_PAGES = [
    "pages/cart.html",
    "admin/index.html",
]

LEGACY_CSS_FILES = (
    "style.css",
    "kinetic-glass.css",
    "cosmic-universe.css",
)


# ---------------------------------------------------------------------------
# Stage 1 Helpers (CSS / JS / HTML Static Analysis)
# ---------------------------------------------------------------------------

def strip_css_comments(css_text: str) -> str:
    out: list[str] = []
    i = 0
    n = len(css_text)
    in_quote: str | None = None
    escaped = False

    while i < n:
        ch = css_text[i]
        if escaped:
            out.append(ch)
            escaped = False
            i += 1
            continue
        if in_quote:
            out.append(ch)
            if ch == "\\":
                escaped = True
            elif ch == in_quote:
                in_quote = None
            i += 1
            continue
        if ch in ("'", '"'):
            in_quote = ch
            out.append(ch)
            i += 1
            continue
        if ch == "/" and i + 1 < n and css_text[i + 1] == "*":
            end = css_text.find("*/", i + 2)
            if end == -1:
                break
            i = end + 2
            continue
        out.append(ch)
        i += 1

    return "".join(out)


def check_css_balanced_braces(css_text: str) -> tuple[bool, str]:
    cleaned = strip_css_comments(css_text)
    depth = 0
    in_quote: str | None = None
    escaped = False

    for idx, ch in enumerate(cleaned):
        if escaped:
            escaped = False
            continue
        if in_quote:
            if ch == "\\":
                escaped = True
            elif ch == in_quote:
                in_quote = None
            continue
        if ch in ("'", '"'):
            in_quote = ch
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth < 0:
                return False, f"unexpected closing '}}' at offset {idx}"

    if in_quote is not None:
        return False, f"unclosed string literal ({in_quote})"
    if depth != 0:
        return False, f"unbalanced braces remaining (depth={depth})"

    raw_open = css_text.count("{")
    raw_close = css_text.count("}")
    if raw_open != raw_close:
        return False, f"raw brace mismatch ('{{'={raw_open}, '}}'={raw_close})"

    return True, f"balanced ({raw_open} pairs)"


def split_top_level(text: str, delimiter: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    paren_depth = 0
    bracket_depth = 0
    in_quote: str | None = None
    escaped = False

    for ch in text:
        if escaped:
            current.append(ch)
            escaped = False
            continue
        if in_quote:
            current.append(ch)
            if ch == "\\":
                escaped = True
            elif ch == in_quote:
                in_quote = None
            continue
        if ch in ("'", '"'):
            in_quote = ch
            current.append(ch)
        elif ch == "(":
            paren_depth += 1
            current.append(ch)
        elif ch == ")":
            paren_depth = max(0, paren_depth - 1)
            current.append(ch)
        elif ch == "[":
            bracket_depth += 1
            current.append(ch)
        elif ch == "]":
            bracket_depth = max(0, bracket_depth - 1)
            current.append(ch)
        elif ch == delimiter and paren_depth == 0 and bracket_depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(ch)

    tail = "".join(current).strip()
    if tail:
        parts.append(tail)
    return parts


def extract_rightmost_compound(selector: str) -> str:
    paren_depth = 0
    bracket_depth = 0
    in_quote: str | None = None
    escaped = False
    last_combinator_idx = -1

    for idx, ch in enumerate(selector):
        if escaped:
            escaped = False
            continue
        if in_quote:
            if ch == "\\":
                escaped = True
            elif ch == in_quote:
                in_quote = None
            continue
        if ch in ("'", '"'):
            in_quote = ch
        elif ch == "(":
            paren_depth += 1
        elif ch == ")":
            paren_depth = max(0, paren_depth - 1)
        elif ch == "[":
            bracket_depth += 1
        elif ch == "]":
            bracket_depth = max(0, bracket_depth - 1)
        elif paren_depth == 0 and bracket_depth == 0 and (ch.isspace() or ch in (">", "+", "~")):
            last_combinator_idx = idx

    return selector[last_combinator_idx + 1 :].strip()


def selector_targets_root_or_body(selector_header: str) -> bool:
    for raw_sel in split_top_level(selector_header, ","):
        if not raw_sel or raw_sel.startswith("@"):
            continue
        compound = extract_rightmost_compound(raw_sel)
        if re.match(r"^(?:html|body)(?=$|[.#\[:])", compound, re.IGNORECASE):
            return True
        for fn_match in re.finditer(r":(?:is|where)\(([^()]*)\)", compound, re.IGNORECASE):
            for arg in split_top_level(fn_match.group(1), ","):
                arg_compound = extract_rightmost_compound(arg)
                if re.match(r"^(?:html|body)(?=$|[.#\[:])", arg_compound, re.IGNORECASE):
                    return True
    return False


def extract_css_blocks(cleaned_css: str) -> list[tuple[str, str, bool]]:
    blocks: list[tuple[str, str, bool]] = []
    stack: list[tuple[str, int]] = []
    header_start = 0
    in_quote: str | None = None
    escaped = False

    i = 0
    n = len(cleaned_css)
    while i < n:
        ch = cleaned_css[i]
        if escaped:
            escaped = False
            i += 1
            continue
        if in_quote:
            if ch == "\\":
                escaped = True
            elif ch == in_quote:
                in_quote = None
            i += 1
            continue
        if ch in ("'", '"'):
            in_quote = ch
        elif ch == ";" and not stack:
            header_start = i + 1
        elif ch == "{":
            header = cleaned_css[header_start:i].strip()
            stack.append((header, i + 1))
            header_start = i + 1
        elif ch == "}":
            if stack:
                header, body_start = stack.pop()
                body = cleaned_css[body_start:i]
                blocks.append((header, body, "{" not in body))
            header_start = i + 1
        i += 1

    return blocks


def find_html_body_overflow_violations(css_text: str) -> list[str]:
    cleaned = strip_css_comments(css_text)
    violations: list[str] = []
    for header, body, is_leaf in extract_css_blocks(cleaned):
        if is_leaf and header and not header.lstrip().startswith("@"):
            if selector_targets_root_or_body(header):
                if re.search(r"\boverflow(?:-x)?\s*:\s*hidden\b", body, re.IGNORECASE):
                    violations.append(f"Rule '{header}' sets overflow/overflow-x: hidden")
    return violations


def strip_js_comments(js_text: str) -> str:
    pattern = re.compile(
        r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|`(?:\\.|[^`\\])*`)|//[^\n]*|/\*[\s\S]*?\*/'
    )
    return pattern.sub(lambda m: m.group(1) if m.group(1) else "", js_text)


class Phase1HTMLAuditParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.html_attrs: dict[str, str | None] | None = None
        self.stylesheets: list[str] = []
        self.scripts: list[str] = []
        self.local_refs: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag_l = tag.lower()
        attr_map = {k.lower(): v for k, v in attrs}

        if tag_l == "html" and self.html_attrs is None:
            self.html_attrs = attr_map

        if tag_l == "link":
            href = (attr_map.get("href") or "").strip()
            rel = (attr_map.get("rel") or "").lower().split()
            if href and ("stylesheet" in rel or not rel):
                self.stylesheets.append(href)
            if href:
                self.local_refs.append(("link[href]", href))

        if tag_l == "script":
            src = (attr_map.get("src") or "").strip()
            if src:
                self.scripts.append(src)
                self.local_refs.append(("script[src]", src))

        for attr_name in ("src", "data-src", "href"):
            val = (attr_map.get(attr_name) or "").strip()
            if val:
                self.local_refs.append((f"{tag_l}[{attr_name}]", val))

        onerror = attr_map.get("onerror") or ""
        for m in re.finditer(r"this\.src\s*=\s*['\"]([^'\"]+)['\"]", onerror):
            self.local_refs.append((f"{tag_l}[onerror]", m.group(1).strip()))


def is_external_or_virtual_ref(ref: str) -> bool:
    lower = ref.lower()
    return (
        not ref
        or ref.startswith("#")
        or lower.startswith(("http://", "https://", "//", "data:", "mailto:", "tel:", "javascript:"))
    )


def run_stage1_audit() -> tuple[int, int]:
    print("=== STAGE 1: STATIC INTEGRITY AUDIT ===")
    passed = 0
    failed = 0

    def record(ok: bool, label: str, detail: str) -> None:
        nonlocal passed, failed
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {label}: {detail}")
        if ok:
            passed += 1
        else:
            failed += 1

    # 1. CSS checks
    combined_clean_css = ""
    for rel_css in PHASE1_CSS_FILES:
        path = ROOT / rel_css
        if not path.is_file():
            record(False, f"CSS exists ({rel_css})", "File missing")
            continue
        text = path.read_text(encoding="utf-8")
        record(True, f"CSS exists ({rel_css})", f"{len(text)} chars")

        bal_ok, bal_msg = check_css_balanced_braces(text)
        record(bal_ok, f"CSS braces ({rel_css})", bal_msg)

        violations = find_html_body_overflow_violations(text)
        record(
            len(violations) == 0,
            f"CSS html/body overflow-hidden check ({rel_css})",
            "0 violations" if not violations else "; ".join(violations),
        )
        combined_clean_css += "\n" + strip_css_comments(text)

    tokens_clean = strip_css_comments((ROOT / "css/orbital-tokens.css").read_text(encoding="utf-8")) if (ROOT / "css/orbital-tokens.css").is_file() else ""
    has_clip = bool(re.search(r"overflow-x\s*:\s*clip\b", tokens_clean, re.IGNORECASE))
    has_scroll_auto = bool(re.search(r"scroll-behavior\s*:\s*auto\s*!important", tokens_clean, re.IGNORECASE))
    record(
        has_clip,
        "CSS 1:1 scroll overflow-x: clip (css/orbital-tokens.css)",
        "present on orbital root/body" if has_clip else "missing overflow-x: clip",
    )
    record(
        has_scroll_auto,
        "CSS 1:1 scroll-behavior: auto !important (css/orbital-tokens.css)",
        "present on html[data-orbital='true']" if has_scroll_auto else "missing scroll-behavior: auto !important",
    )

    # 2. JS checks
    syntax_proc = subprocess.run(
        ["node", "--check", *PHASE1_JS_FILES],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    record(
        syntax_proc.returncode == 0,
        "JS syntax (node --check)",
        f"exit={syntax_proc.returncode} on {', '.join(PHASE1_JS_FILES)}"
        if syntax_proc.returncode == 0
        else (syntax_proc.stderr or syntax_proc.stdout).strip(),
    )

    for rel_js in PHASE1_JS_FILES:
        path = ROOT / rel_js
        if not path.is_file():
            record(False, f"JS exists ({rel_js})", "File missing")
            continue
        raw_js = path.read_text(encoding="utf-8")
        code_js = strip_js_comments(raw_js)

        lenis_hits = len(re.findall(r"\blenis\b", code_js, re.IGNORECASE))
        smoother_hits = len(re.findall(r"\bScrollSmoother\b", code_js, re.IGNORECASE))
        wheel_hits = len(re.findall(r"addEventListener\s*\(\s*['\"]wheel['\"]", code_js, re.IGNORECASE))
        record(
            lenis_hits == 0 and smoother_hits == 0 and wheel_hits == 0,
            f"JS zero-hijack check ({rel_js})",
            f"lenis={lenis_hits}, ScrollSmoother={smoother_hits}, addEventListener('wheel')={wheel_hits}",
        )

    app_js_path = ROOT / "js/app.js"
    app_js_code = strip_js_comments(app_js_path.read_text(encoding="utf-8")) if app_js_path.is_file() else ""
    has_orbital_guard = bool(
        re.search(r"documentElement\.hasAttribute\(\s*['\"]data-orbital['\"]\s*\)\)\s*return\s*;", app_js_code)
    )
    record(
        has_orbital_guard,
        "js/app.js data-orbital loader guard",
        "skips legacy motion-engine.js when html[data-orbital] is present"
        if has_orbital_guard
        else "data-orbital loader guard missing",
    )

    # 3. 7 Phase 1 HTML files
    for rel_html in PHASE1_HTML_FILES:
        path = ROOT / rel_html
        if not path.is_file():
            record(False, f"HTML exists ({rel_html})", "File missing")
            continue

        html_text = path.read_text(encoding="utf-8")
        parser = Phase1HTMLAuditParser()
        parser.feed(html_text)

        html_attrs = parser.html_attrs or {}
        root_ok = (html_attrs.get("lang") == "vi") and (html_attrs.get("data-orbital") == "true")
        record(
            root_ok,
            f"HTML root attr ({rel_html})",
            f"lang={html_attrs.get('lang')!r}, data-orbital={html_attrs.get('data-orbital')!r}, data-spectral={html_attrs.get('data-spectral')!r}",
        )

        legacy_found = []
        for sheet in parser.stylesheets:
            base = sheet.split("?", 1)[0].split("#", 1)[0].rsplit("/", 1)[-1].lower()
            if base in LEGACY_CSS_FILES:
                legacy_found.append(sheet)
        record(
            len(legacy_found) == 0,
            f"HTML no legacy CSS ({rel_html})",
            "0 legacy CSS links" if not legacy_found else f"found: {legacy_found}",
        )

        emdash_count = html_text.count("\u2014")
        record(
            emdash_count == 0,
            f"HTML zero em-dashes ({rel_html})",
            f"count={emdash_count}",
        )

        missing_paths: list[str] = []
        checked_count = 0
        seen_refs: set[tuple[str, str]] = set()
        for kind, ref in parser.local_refs:
            if is_external_or_virtual_ref(ref):
                continue
            clean_ref = ref.split("#", 1)[0].split("?", 1)[0]
            if not clean_ref:
                continue
            key = (kind, clean_ref)
            if key in seen_refs:
                continue
            seen_refs.add(key)
            checked_count += 1
            resolved = (path.parent / unquote(clean_ref)).resolve()
            if not resolved.exists():
                missing_paths.append(f"{kind}={ref}")

        record(
            len(missing_paths) == 0,
            f"HTML local asset/href paths ({rel_html})",
            f"checked={checked_count}, missing=0"
            if not missing_paths
            else f"checked={checked_count}, missing={missing_paths}",
        )

    return passed, failed


# ---------------------------------------------------------------------------
# Stage 2 Helpers (HTTP Server + Dynamic Node Playwright + Chromium Discovery)
# ---------------------------------------------------------------------------

class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".webp": "image/webp",
        ".js": "application/javascript; charset=utf-8",
        ".mjs": "application/javascript; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".html": "text/html; charset=utf-8",
        ".svg": "image/svg+xml",
        ".woff2": "font/woff2",
        ".json": "application/json; charset=utf-8",
    }

    def log_message(self, format: str, *args: object) -> None:
        pass


class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def locate_node_playwright() -> Path:
    candidates: list[Path] = []
    local_app = os.environ.get("LOCALAPPDATA", "")
    app_data = os.environ.get("APPDATA", "")

    if local_app:
        npx_root = Path(local_app) / "npm-cache" / "_npx"
        if npx_root.is_dir():
            for match in sorted(npx_root.glob("*/node_modules/playwright"), reverse=True):
                candidates.append(match)

    if app_data:
        candidates.append(Path(app_data) / "npm" / "node_modules" / "playwright")

    candidates.append(ROOT / "node_modules" / "playwright")

    node_path = os.environ.get("NODE_PATH", "")
    if node_path:
        for entry in node_path.split(os.pathsep):
            if entry:
                candidates.append(Path(entry) / "playwright")

    for cand in candidates:
        if (cand / "package.json").is_file():
            return cand

    raise FileNotFoundError(
        "Could not locate Node 'playwright' module under %LOCALAPPDATA%\\npm-cache\\_npx or global node_modules."
    )


def locate_chromium_executable() -> Path:
    local_app = os.environ.get("LOCALAPPDATA", "")
    candidates: list[Path] = []

    if local_app:
        ms_pw = Path(local_app) / "ms-playwright"
        if ms_pw.is_dir():
            for exe in sorted(ms_pw.glob("chromium-*/chrome-win64/chrome.exe"), reverse=True):
                candidates.append(exe)
            for exe in sorted(ms_pw.glob("chromium-*/chrome-win/chrome.exe"), reverse=True):
                candidates.append(exe)

    candidates.extend([
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    ])

    for cand in candidates:
        if cand.is_file():
            return cand

    raise FileNotFoundError(
        "Could not locate Chromium executable under %LOCALAPPDATA%\\ms-playwright or Program Files Chrome."
    )


NODE_PLAYWRIGHT_RUNNER = r"""
const fs = require('fs');
const cfgPath = process.argv[2];
const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
const { chromium } = require(cfg.playwrightDir);

const RESULTS = [];
let passCount = 0;
let failCount = 0;

function record(ok, label, detail) {
  const tag = ok ? '[PASS]' : '[FAIL]';
  const line = `${tag} ${label}: ${detail}`;
  console.log(line);
  RESULTS.push({ ok, label, detail });
  if (ok) passCount += 1;
  else failCount += 1;
}

function isLocalUrl(url, baseOrigin) {
  return typeof url === 'string' && url.startsWith(baseOrigin);
}

function attachNetworkAndErrorListeners(page, baseOrigin) {
  const state = {
    consoleErrors: [],
    pageErrors: [],
    localHttpErrors: [],
    localRequestFailed: [],
    externalNotes: [],
  };

  page.on('console', (msg) => {
    if (msg.type() === 'error') {
      const loc = msg.location ? msg.location() : {};
      const where = loc && loc.url ? ` @ ${loc.url}` : '';
      state.consoleErrors.push(`${msg.text()}${where}`);
    }
  });

  page.on('pageerror', (err) => {
    state.pageErrors.push(err && err.stack ? String(err.stack) : String(err));
  });

  page.on('requestfailed', (req) => {
    const url = req.url();
    const errText = (req.failure() && req.failure().errorText) || 'unknown';
    if (isLocalUrl(url, baseOrigin)) {
      state.localRequestFailed.push(`${url} (${errText})`);
    } else {
      state.externalNotes.push(`REQFAIL ${url} (${errText})`);
    }
  });

  page.on('response', (res) => {
    const url = res.url();
    const status = res.status();
    if (status >= 400) {
      if (isLocalUrl(url, baseOrigin)) {
        state.localHttpErrors.push(`${status} ${url}`);
      } else {
        state.externalNotes.push(`HTTP ${status} ${url}`);
      }
    }
  });

  return state;
}

async function waitForPageReady(page, opts = {}) {
  await page.waitForLoadState('load');
  await page.evaluate(async () => {
    if (document.fonts && document.fonts.ready) {
      try { await document.fonts.ready; } catch (_) {}
    }
  });
  if (opts.waitForCanvasSelector) {
    await page.waitForFunction(
      (sel) => {
        const c = document.querySelector(sel);
        return Boolean(c && c.dataset && c.dataset.orbRenderer);
      },
      opts.waitForCanvasSelector,
      { timeout: 4500 }
    ).catch(() => {});
  } else {
    await page.waitForTimeout(250);
  }
}

async function scrollAndVerifyImages(page) {
  // First verify images currently in initial viewport
  const initialBroken = await page.evaluate(() => {
    const vw = window.innerWidth;
    const vh = window.innerHeight;
    const bad = [];
    for (const img of document.querySelectorAll('img')) {
      const st = getComputedStyle(img);
      if (st.display === 'none' || st.visibility === 'hidden' || img.closest('[hidden], .is-hidden')) continue;
      const r = img.getBoundingClientRect();
      if (r.width <= 0 || r.height <= 0) continue;
      if (r.bottom < 0 || r.top > vh || r.right < 0 || r.left > vw) continue;
      if (!img.complete || img.naturalWidth <= 0) {
        bad.push(`${img.getAttribute('src')} (complete=${img.complete}, w=${img.naturalWidth})`);
      }
    }
    return bad;
  });

  // Scroll step-by-step down the page to trigger loading="lazy" images cleanly
  await page.evaluate(async () => {
    const total = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
    const step = Math.max(300, Math.floor(window.innerHeight * 0.75));
    for (let y = 0; y <= total; y += step) {
      window.scrollTo(0, y);
      await new Promise((r) => setTimeout(r, 45));
    }
    window.scrollTo(0, total);
    await new Promise((r) => setTimeout(r, 120));
    // Also explicitly trigger any remaining visible non-hidden lazy imgs if outside ScrollTrigger pin
    const visibleImgs = Array.from(document.querySelectorAll('img')).filter((img) => {
      const st = getComputedStyle(img);
      if (st.display === 'none' || st.visibility === 'hidden' || img.closest('[hidden], .is-hidden')) return false;
      const r = img.getBoundingClientRect();
      return r.width > 0 && r.height > 0;
    });
    await Promise.all(
      visibleImgs.map((img) => {
        if (img.complete && img.naturalWidth > 0) return Promise.resolve();
        return new Promise((resolve) => {
          const timer = setTimeout(resolve, 3500);
          img.addEventListener('load', () => { clearTimeout(timer); resolve(); }, { once: true });
          img.addEventListener('error', () => { clearTimeout(timer); resolve(); }, { once: true });
        });
      })
    );
    window.scrollTo(0, 0);
  });

  await page.waitForTimeout(150);

  const allStats = await page.evaluate(() => {
    const visible = [];
    const broken = [];
    for (const img of document.querySelectorAll('img')) {
      const st = getComputedStyle(img);
      if (st.display === 'none' || st.visibility === 'hidden' || img.closest('[hidden], .is-hidden')) continue;
      const r = img.getBoundingClientRect();
      if (r.width <= 0 || r.height <= 0) continue;
      visible.push(img.getAttribute('src'));
      if (!img.complete || img.naturalWidth <= 0) {
        broken.push(`${img.getAttribute('src')} (complete=${img.complete}, w=${img.naturalWidth})`);
      }
    }
    return { totalVisible: visible.length, broken };
  });

  return { initialBroken, ...allStats };
}

(async () => {
  const browser = await chromium.launch({
    executablePath: cfg.chromeExe,
    headless: true,
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
  });

  try {
    // -----------------------------------------------------------------------
    // 1. ALL 7 PHASE 1 PAGES x 3 VIEWPORTS (1440x900, 1280x720, 390x844)
    // -----------------------------------------------------------------------
    console.log('\n--- TEST 1: 7 PHASE 1 PAGES x 3 VIEWPORTS ---');
    const viewports = [
      { width: 1440, height: 900, label: '1440x900' },
      { width: 1280, height: 720, label: '1280x720' },
      { width: 390, height: 844, label: '390x844' },
    ];

    for (const relPage of cfg.phase1Pages) {
      const url = `${cfg.baseOrigin}/${relPage}`;
      for (const vp of viewports) {
        const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
        const page = await ctx.newPage();
        const net = attachNetworkAndErrorListeners(page, cfg.baseOrigin);
        try {
          await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
          const canvasSel = relPage === 'index.html'
            ? '#orbital-space-canvas'
            : (relPage.includes('product-detail') ? '#orbital-detail-canvas' : null);
          await waitForPageReady(page, { waitForCanvasSelector: canvasSel });

          const overflowInfo = await page.evaluate(() => ({
            scrollWidth: document.documentElement.scrollWidth,
            innerWidth: window.innerWidth,
            clientWidth: document.documentElement.clientWidth,
            overflow: document.documentElement.scrollWidth > window.innerWidth,
          }));
          record(
            !overflowInfo.overflow,
            `Viewport overflow (${relPage} @ ${vp.label})`,
            `scrollWidth=${overflowInfo.scrollWidth} <= innerWidth=${overflowInfo.innerWidth}`
          );

          if (relPage === 'index.html' && vp.label === '390x844') {
            const mobileLayout = await page.evaluate(() => {
              const cw = document.documentElement.clientWidth;
              const toggle = document.getElementById('orb-mobile-toggle');
              const navBar = document.querySelector('.orb-nav-bar');
              const pills = Array.from(document.querySelectorAll('.orb-spectral-switcher .orb-sys-pill'));
              const pillTops = pills.map((p) => Math.round(p.getBoundingClientRect().top));
              const pillSpread = pillTops.length ? (Math.max(...pillTops) - Math.min(...pillTops)) : 0;
              const tRect = toggle ? toggle.getBoundingClientRect() : null;
              const nRect = navBar ? navBar.getBoundingClientRect() : null;
              return {
                clientWidth: cw,
                toggleRight: tRect ? Math.round(tRect.right * 10) / 10 : null,
                navRight: nRect ? Math.round(nRect.right * 10) / 10 : null,
                pillSpread,
              };
            });
            record(
              Boolean(mobileLayout.toggleRight && mobileLayout.toggleRight <= mobileLayout.clientWidth && mobileLayout.navRight <= mobileLayout.clientWidth),
              'Mobile 390x844 header toggle & navbar within clientWidth',
              JSON.stringify(mobileLayout)
            );
            record(
              mobileLayout.pillSpread <= 4,
              'Mobile 390x844 spectral switcher single-row alignment',
              `pillTopSpread=${mobileLayout.pillSpread}px`
            );
            await page.waitForTimeout(700);
            const heroTitleCheck = await page.evaluate(() => {
              const t = document.querySelector('.orb-hero-title');
              if (!t) return null;
              const cs = getComputedStyle(t);
              const r = t.getBoundingClientRect();
              const childrenOpaque = Array.from(t.querySelectorAll('*')).every((el) => parseFloat(getComputedStyle(el).opacity) >= 0.99);
              return { opacity: parseFloat(cs.opacity), childrenOpaque, height: Math.round(r.height), text: t.textContent.trim().replace(/\s+/g, ' ') };
            });
            record(
              Boolean(heroTitleCheck && heroTitleCheck.opacity >= 0.99 && heroTitleCheck.childrenOpaque && heroTitleCheck.height >= 70),
              'Mobile 390x844 hero headline full visibility after SplitText revert',
              JSON.stringify(heroTitleCheck)
            );
          }

          if (vp.label === '1440x900') {
            if (canvasSel) {
              const cInfo = await page.evaluate((sel) => {
                const c = document.querySelector(sel);
                if (!c) return null;
                const r = c.getBoundingClientRect();
                return {
                  attrW: c.width,
                  attrH: c.height,
                  rectW: Math.round(r.width),
                  rectH: Math.round(r.height),
                  renderer: c.dataset ? c.dataset.orbRenderer : '',
                };
              }, canvasSel);
              record(
                Boolean(cInfo && cInfo.attrW > 0 && cInfo.attrH > 0 && cInfo.rectW > 0 && cInfo.rectH > 0 && cInfo.renderer),
                `Canvas surface (${relPage} @ ${vp.label})`,
                JSON.stringify(cInfo)
              );
            }

            const globals = await page.evaluate(() => ({
              gsap: typeof window.gsap,
              ScrollTrigger: typeof window.ScrollTrigger,
              Flip: typeof window.Flip,
              OrbitalWebGL: typeof window.OrbitalWebGL,
              OrbitalMotion: typeof window.OrbitalMotion,
              OrbitalCart: typeof window.OrbitalCart,
            }));
            const globalsOk =
              globals.gsap === 'object' &&
              globals.ScrollTrigger === 'function' &&
              globals.Flip === 'function' &&
              globals.OrbitalWebGL === 'object' &&
              globals.OrbitalMotion === 'object' &&
              globals.OrbitalCart === 'object';
            record(
              globalsOk,
              `Globals loaded (${relPage})`,
              JSON.stringify(globals)
            );

            const imgStats = await scrollAndVerifyImages(page);
            record(
              imgStats.initialBroken.length === 0 && imgStats.broken.length === 0 && imgStats.totalVisible > 0,
              `Visible images (${relPage} @ ${vp.label})`,
              `visible=${imgStats.totalVisible}, broken=${imgStats.broken.length}` +
                (imgStats.broken.length ? ` [${imgStats.broken.join('; ')}]` : '')
            );
          }

          const errOk =
            net.consoleErrors.length === 0 &&
            net.pageErrors.length === 0 &&
            net.localHttpErrors.length === 0 &&
            net.localRequestFailed.length === 0;
          record(
            errOk,
            `Zero runtime/local errors (${relPage} @ ${vp.label})`,
            `console.error=${net.consoleErrors.length}, pageerror=${net.pageErrors.length}, local404=${net.localHttpErrors.length}, localReqFail=${net.localRequestFailed.length}` +
              (errOk ? '' : ` | details=${JSON.stringify(net)}`) +
              (net.externalNotes.length ? ` | externalNotes=${JSON.stringify(net.externalNotes)}` : '')
          );
        } finally {
          await ctx.close();
        }
      }
    }

    // -----------------------------------------------------------------------
    // 1B. TABLET 1024x768 & LAPTOP 1280x720 NAVBAR INTEGRITY CHECK
    // -----------------------------------------------------------------------
    console.log('\n--- TEST 1B: TABLET 1024x768 & 1280x720 NAVBAR CONTAINMENT ---');
    for (const navVp of [{ width: 1024, height: 768, label: '1024x768' }, { width: 1280, height: 720, label: '1280x720' }]) {
      const ctx = await browser.newContext({ viewport: { width: navVp.width, height: navVp.height } });
      const page = await ctx.newPage();
      await page.goto(`${cfg.baseOrigin}/index.html`, { waitUntil: 'domcontentloaded', timeout: 20000 });
      await waitForPageReady(page, { waitForCanvasSelector: '#orbital-space-canvas' });
      const navCheck = await page.evaluate(() => {
        const cw = document.documentElement.clientWidth;
        const navBar = document.querySelector('.orb-nav-bar');
        const brand = document.querySelector('.orb-brand-mark');
        const links = document.querySelector('.orb-nav-links');
        const actions = document.querySelector('.orb-nav-actions');
        const nRect = navBar ? navBar.getBoundingClientRect() : null;
        const bRect = brand ? brand.getBoundingClientRect() : null;
        const lRect = links && getComputedStyle(links).display !== 'none' ? links.getBoundingClientRect() : null;
        const aRect = actions ? actions.getBoundingClientRect() : null;
        const brandActionsOverlap = bRect && aRect ? (bRect.right > aRect.left - 4) : false;
        const linksActionsOverlap = lRect && aRect ? (lRect.right > aRect.left - 4 || lRect.left < bRect.right + 4) : false;
        return {
          clientWidth: cw,
          scrollWidth: document.documentElement.scrollWidth,
          navRight: nRect ? Math.round(nRect.right * 10) / 10 : null,
          brandActionsOverlap,
          linksActionsOverlap,
        };
      });
      record(
        Boolean(
          navCheck.scrollWidth <= navCheck.clientWidth &&
          navCheck.navRight <= navCheck.clientWidth &&
          !navCheck.brandActionsOverlap &&
          !navCheck.linksActionsOverlap
        ),
        `Navbar containment & zero overlap (${navVp.label})`,
        JSON.stringify(navCheck)
      );
      await ctx.close();
    }

    // -----------------------------------------------------------------------
    // 2..7 INTERACTIVE TESTS ON index.html (fresh context 1440x900)
    // -----------------------------------------------------------------------
    console.log('\n--- TEST 2..7: index.html INTERACTIVE & SCROLL SUITE ---');
    {
      const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
      const page = await ctx.newPage();
      const net = attachNetworkAndErrorListeners(page, cfg.baseOrigin);
      await page.goto(`${cfg.baseOrigin}/index.html`, { waitUntil: 'domcontentloaded', timeout: 20000 });
      await waitForPageReady(page, { waitForCanvasSelector: '#orbital-space-canvas' });

      // TEST 2: 1:1 Native Scroll Benchmark
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.waitForTimeout(100);
      await page.mouse.move(720, 450);
      for (let i = 0; i < 5; i += 1) {
        await page.mouse.wheel(0, 120);
        await page.waitForTimeout(50);
      }
      await page.waitForTimeout(250);
      const scrollYAfter = await page.evaluate(() => Math.round(window.scrollY));
      const scrollDeltaOk = Math.abs(scrollYAfter - 600) <= 5;
      record(
        scrollDeltaOk,
        '1:1 Native Scroll Benchmark (5 x 120px wheel)',
        `window.scrollY=${scrollYAfter}px (expected 600 ± 5px)`
      );

      // Reset to top for Hero tests
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.waitForTimeout(150);

      // TEST 3: Shader Canvas & Spectral Switch
      const canvasInfo = await page.evaluate(() => {
        const c = document.getElementById('orbital-space-canvas');
        if (!c) return null;
        const r = c.getBoundingClientRect();
        return {
          attrW: c.width,
          attrH: c.height,
          rectW: Math.round(r.width),
          rectH: Math.round(r.height),
          renderer: c.dataset ? c.dataset.orbRenderer : '',
        };
      });
      const canvasOk = Boolean(
        canvasInfo &&
        canvasInfo.attrW > 0 &&
        canvasInfo.attrH > 0 &&
        canvasInfo.rectW > 0 &&
        canvasInfo.rectH > 0 &&
        canvasInfo.renderer
      );
      record(
        canvasOk,
        'Hero WebGL/Canvas2D Shader Surface',
        JSON.stringify(canvasInfo)
      );

      await page.click('[data-system="redbull"]');
      const spRedbull = await page.evaluate(() => document.documentElement.getAttribute('data-spectral'));
      await page.click('[data-system="sting"]');
      const spSting = await page.evaluate(() => document.documentElement.getAttribute('data-spectral'));
      await page.click('[data-system="monster"]');
      const spMonster = await page.evaluate(() => document.documentElement.getAttribute('data-spectral'));
      record(
        spRedbull === 'redbull' && spSting === 'sting' && spMonster === 'monster',
        'Spectral Switcher transitions',
        `redbull->${spRedbull}, sting->${spSting}, monster->${spMonster}`
      );

      // TEST 4: 2.5D Solar Orbit Node Click
      // Move pointer onto the orbit stage first (triggers pointerenter pause, matching real user interaction)
      await page.locator('.orb-orbit-stage').hover();
      await page.waitForTimeout(120);
      await page.locator('.orb-orbit-node[data-sku="rb-1"]').click();
      await page.waitForTimeout(150);
      const orbitRes = await page.evaluate(() => ({
        code: (document.getElementById('orb-telemetry-code') || {}).textContent?.trim(),
        spectral: document.documentElement.getAttribute('data-spectral'),
      }));
      record(
        orbitRes.code === 'OBS-RB01' && orbitRes.spectral === 'redbull',
        '2.5D Solar Orbit Node Click (rb-1)',
        `code=${orbitRes.code}, data-spectral=${orbitRes.spectral}`
      );

      // TEST 5: Bento Vault GSAP Flip Filtering
      await page.locator('#observatory-vault').scrollIntoViewIfNeeded();
      await page.waitForTimeout(150);

      async function clickVaultFilterAndCount(brand) {
        await page.locator(`#observatory-vault [data-filter-brand="${brand}"]`).click();
        await page.waitForTimeout(650);
        return page.evaluate(() => {
          const visibleCards = Array.from(document.querySelectorAll('#observatory-vault .orb-bento-card:not(.is-hidden)'));
          const renderedCount = visibleCards.filter((el) => {
            const cs = getComputedStyle(el);
            return cs.display !== 'none' && parseFloat(cs.opacity) >= 0.99;
          }).length;
          return {
            notHiddenCount: visibleCards.length,
            fullyVisibleCount: renderedCount,
            badgeText: (document.getElementById('orb-vault-count') || {}).textContent?.trim(),
          };
        });
      }

      const flipMonster = await clickVaultFilterAndCount('monster');
      const flipRedbull = await clickVaultFilterAndCount('redbull');
      const flipSting = await clickVaultFilterAndCount('sting');
      const flipAll = await clickVaultFilterAndCount('all');
      const flipOk =
        flipMonster.notHiddenCount === 4 && flipMonster.fullyVisibleCount === 4 &&
        flipRedbull.notHiddenCount === 3 && flipRedbull.fullyVisibleCount === 3 &&
        flipSting.notHiddenCount === 3 && flipSting.fullyVisibleCount === 3 &&
        flipAll.notHiddenCount === 10 && flipAll.fullyVisibleCount === 10;
      record(
        flipOk,
        'Bento Vault GSAP Flip Filtering',
        `monster=${flipMonster.notHiddenCount}(vis=${flipMonster.fullyVisibleCount}), redbull=${flipRedbull.notHiddenCount}(vis=${flipRedbull.fullyVisibleCount}), sting=${flipSting.notHiddenCount}(vis=${flipSting.fullyVisibleCount}), all=${flipAll.notHiddenCount}(vis=${flipAll.fullyVisibleCount})`
      );

      // TEST 6: Command Palette Ctrl + K
      await page.evaluate(() => {
        if (document.activeElement && typeof document.activeElement.blur === 'function') {
          document.activeElement.blur();
        }
      });
      await page.keyboard.press('Control+k');
      await page.waitForTimeout(150);
      const cmdOpened = await page.evaluate(() => {
        const p = document.getElementById('orb-cmd-palette');
        return Boolean(p && (p.classList.contains('is-open') || p.classList.contains('open')));
      });
      await page.locator('#orb-cmd-input').fill('sting');
      await page.waitForTimeout(100);
      const stingCmdCount = await page.locator('#orb-cmd-list a.orb-cmd-item[data-sku]').count();
      await page.keyboard.press('Escape');
      await page.waitForTimeout(150);
      const cmdClosed = await page.evaluate(() => {
        const p = document.getElementById('orb-cmd-palette');
        return Boolean(p && !p.classList.contains('is-open') && !p.classList.contains('open') && p.getAttribute('aria-hidden') === 'true');
      });
      record(
        cmdOpened && stingCmdCount === 3 && cmdClosed,
        'Command Palette Ctrl+K workflow',
        `opened=${cmdOpened}, stingSkuMatches=${stingCmdCount}, closedOnEsc=${cmdClosed}`
      );

      // TEST 7: Cart Telemetry Add
      const initialCartCount = await page.locator('.orb-cart-count').first().textContent();
      await page.locator('#orb-telemetry-add').click();
      await page.waitForTimeout(150);
      const afterCartState = await page.evaluate(() => ({
        countText: (document.querySelector('.orb-cart-count') || {}).textContent?.trim(),
        toastCount: document.querySelectorAll('#toast-container .toast, .toast').length,
        toastText: (document.querySelector('.toast') || {}).textContent?.trim(),
      }));
      record(
        String(initialCartCount).trim() === '7' &&
        afterCartState.countText === '8' &&
        afterCartState.toastCount >= 1,
        'Cart Telemetry Add (#orb-telemetry-add)',
        `initial=${String(initialCartCount).trim()}, after=${afterCartState.countText}, toasts=${afterCartState.toastCount}, msg=${JSON.stringify(afterCartState.toastText)}`
      );

      record(
        net.consoleErrors.length === 0 && net.pageErrors.length === 0 && net.localHttpErrors.length === 0,
        'Interactive suite zero errors (index.html)',
        `console.error=${net.consoleErrors.length}, pageerror=${net.pageErrors.length}, local404=${net.localHttpErrors.length}`
      );

      await ctx.close();
    }

    // -----------------------------------------------------------------------
    // 8. PRODUCT DETAIL INSPECTION CHAMBER
    // -----------------------------------------------------------------------
    console.log('\n--- TEST 8: PRODUCT DETAIL INSPECTION CHAMBER ---');
    {
      const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
      const page = await ctx.newPage();
      const net = attachNetworkAndErrorListeners(page, cfg.baseOrigin);
      await page.goto(`${cfg.baseOrigin}/pages/product-detail.html`, { waitUntil: 'domcontentloaded', timeout: 20000 });
      await waitForPageReady(page, { waitForCanvasSelector: '#orbital-detail-canvas' });

      const detailCanvas = await page.evaluate(() => {
        const c = document.getElementById('orbital-detail-canvas');
        if (!c) return null;
        const r = c.getBoundingClientRect();
        return {
          attrW: c.width,
          attrH: c.height,
          rectW: Math.round(r.width),
          rectH: Math.round(r.height),
          renderer: c.dataset ? c.dataset.orbRenderer : '',
        };
      });
      const detailCanvasOk = Boolean(
        detailCanvas && detailCanvas.attrW > 0 && detailCanvas.attrH > 0 && detailCanvas.rectW > 0 && detailCanvas.rectH > 0 && detailCanvas.renderer
      );
      record(detailCanvasOk, 'Detail Halo Canvas (#orbital-detail-canvas)', JSON.stringify(detailCanvas));

      const basePrice = (await page.locator('#orb-detail-price').textContent())?.trim();
      await page.locator('.orb-pack-btn[data-pack="6"]').click();
      const pack6Price = (await page.locator('#orb-detail-price').textContent())?.trim();
      await page.locator('#orb-qty-inc').click();
      const qtyVal = await page.locator('#orb-qty-input').inputValue();
      const pack6Qty2Price = (await page.locator('#orb-detail-price').textContent())?.trim();
      record(
        basePrice === '45.000đ' && pack6Price === '256.500đ' && qtyVal === '2' && pack6Qty2Price === '513.000đ',
        'Detail Pack x6 + Qty=2 Pricing',
        `base=${basePrice}, pack6=${pack6Price}, qty=${qtyVal}, pack6*qty2=${pack6Qty2Price}`
      );

      await page.locator('.orb-thumb-btn[data-src*="original-back-1"]').click();
      await page.waitForFunction(() => {
        const img = document.getElementById('main-product-image');
        return Boolean(img && img.src.includes('original-back-1') && img.complete && img.naturalWidth > 0);
      }, null, { timeout: 5000 }).catch(() => {});
      const thumbResult = await page.evaluate(() => {
        const img = document.getElementById('main-product-image');
        return img ? { src: img.src, complete: img.complete, naturalWidth: img.naturalWidth } : null;
      });
      record(
        Boolean(thumbResult && thumbResult.src.includes('original-back-1') && thumbResult.complete && thumbResult.naturalWidth > 0),
        'Detail Thumbnail Switch (original-back-1)',
        JSON.stringify(thumbResult)
      );

      const thumbBounds = await page.evaluate(() => {
        const issues = [];
        const btns = Array.from(document.querySelectorAll('.orb-thumb-btn'));
        for (const btn of btns) {
          if (getComputedStyle(btn).display === 'none' || btn.hidden) continue;
          const img = btn.querySelector('img');
          if (!img) continue;
          const br = btn.getBoundingClientRect();
          const ir = img.getBoundingClientRect();
          if (ir.bottom > br.bottom + 1 || ir.right > br.right + 1 || ir.top < br.top - 1 || ir.left < br.left - 1) {
            issues.push({ imgBottom: Math.round(ir.bottom), btnBottom: Math.round(br.bottom) });
          }
        }
        return { checked: btns.length, issues };
      });
      record(
        thumbBounds.checked >= 4 && thumbBounds.issues.length === 0,
        'Detail Thumbnails Contained Inside 72x72 Frames',
        JSON.stringify(thumbBounds)
      );

      // ?sku=mn-2
      await page.goto(`${cfg.baseOrigin}/pages/product-detail.html?sku=mn-2`, { waitUntil: 'domcontentloaded', timeout: 20000 });
      await waitForPageReady(page, { waitForCanvasSelector: '#orbital-detail-canvas' });
      const sku2Info = await page.evaluate(() => ({
        title: (document.getElementById('orb-detail-title') || {}).textContent?.trim(),
        price: (document.getElementById('orb-detail-price') || {}).textContent?.trim(),
        spectral: document.documentElement.getAttribute('data-spectral'),
      }));
      record(
        Boolean(sku2Info.title && sku2Info.title.includes('Monster Zero Ultra White 500ml') && sku2Info.price === '48.000đ'),
        'Detail SKU Hydration (?sku=mn-2)',
        JSON.stringify(sku2Info)
      );

      record(
        net.consoleErrors.length === 0 && net.pageErrors.length === 0 && net.localHttpErrors.length === 0,
        'Detail suite zero errors',
        `console.error=${net.consoleErrors.length}, pageerror=${net.pageErrors.length}, local404=${net.localHttpErrors.length}`
      );

      await ctx.close();
    }

    // -----------------------------------------------------------------------
    // 9. SEARCH HUB (?q=ultra)
    // -----------------------------------------------------------------------
    console.log('\n--- TEST 9: SEARCH HUB ---');
    {
      const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
      const page = await ctx.newPage();
      const net = attachNetworkAndErrorListeners(page, cfg.baseOrigin);
      await page.goto(`${cfg.baseOrigin}/pages/search-results.html?q=ultra`, { waitUntil: 'domcontentloaded', timeout: 20000 });
      await waitForPageReady(page);
      await page.waitForTimeout(450);

      const searchInfo = await page.evaluate(() => {
        const medias = Array.from(document.querySelectorAll('#search-results-grid .orb-bento-card .orb-card-media'));
        const tops = medias.map((m) => Math.round(m.getBoundingClientRect().top));
        const mediaTopSpread = tops.length ? (Math.max(...tops) - Math.min(...tops)) : 0;
        return {
          countText: (document.getElementById('search-count-number') || {}).textContent?.trim(),
          cardCount: document.querySelectorAll('#search-results-grid .orb-bento-card').length,
          mediaTopSpread,
        };
      });
      record(
        searchInfo.countText === '3' && searchInfo.cardCount === 3,
        'Search Hub (?q=ultra)',
        `#search-count-number=${searchInfo.countText}, .orb-bento-card count=${searchInfo.cardCount}`
      );
      record(
        searchInfo.mediaTopSpread <= 2,
        'Search Hub 3-card baseline alignment (?q=ultra)',
        `mediaTopSpread=${searchInfo.mediaTopSpread}px`
      );
      record(
        net.consoleErrors.length === 0 && net.pageErrors.length === 0 && net.localHttpErrors.length === 0,
        'Search Hub zero errors',
        `console.error=${net.consoleErrors.length}, pageerror=${net.pageErrors.length}, local404=${net.localHttpErrors.length}`
      );
      await ctx.close();
    }

    // -----------------------------------------------------------------------
    // 10. PHASE 2/3 SMOKE CHECK (pages/cart.html & admin/index.html)
    // -----------------------------------------------------------------------
    console.log('\n--- TEST 10: PHASE 2/3 SMOKE CHECK ---');
    for (const relSmoke of cfg.smokePages) {
      const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
      const page = await ctx.newPage();
      const net = attachNetworkAndErrorListeners(page, cfg.baseOrigin);
      await page.goto(`${cfg.baseOrigin}/${relSmoke}`, { waitUntil: 'domcontentloaded', timeout: 20000 });
      await waitForPageReady(page);
      await page.waitForTimeout(300);

      // Untouched Phase 2/3 HTML files do not yet include the Phase 1 inline SVG <link rel="icon">.
      const nonFaviconErrors = net.consoleErrors.filter((msg) => !msg.includes('/favicon.ico'));
      const nonFavicon404 = net.localHttpErrors.filter((msg) => !msg.includes('/favicon.ico'));
      const ok =
        nonFaviconErrors.length === 0 &&
        net.pageErrors.length === 0 &&
        nonFavicon404.length === 0 &&
        net.localRequestFailed.length === 0;
      record(
        ok,
        `Smoke check (${relSmoke})`,
        `nonFaviconErrors=${nonFaviconErrors.length}, pageerror=${net.pageErrors.length}, nonFavicon404=${nonFavicon404.length}` +
          (ok ? '' : ` | details=${JSON.stringify(net)}`)
      );
      await ctx.close();
    }
  } finally {
    await browser.close();
  }

  console.log(`\n=== STAGE 2 SUMMARY: passed=${passCount}, failed=${failCount} ===`);
  if (failCount > 0) {
    process.exitCode = 1;
  }
})();
"""


def run_stage2_chromium() -> int:
    print("\n=== STAGE 2: REAL HEADLESS CHROMIUM VERIFICATION ===")
    playwright_dir = locate_node_playwright()
    chrome_exe = locate_chromium_executable()
    print(f"[INFO] Node playwright: {playwright_dir}")
    print(f"[INFO] Chromium binary: {chrome_exe}")

    handler = functools.partial(QuietHTTPRequestHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    port = server.server_address[1]
    base_origin = f"http://127.0.0.1:{port}"
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"[INFO] Ephemeral HTTP server: {base_origin}", flush=True)
    sys.stdout.flush()

    try:
        with tempfile.TemporaryDirectory(prefix="orbital_qa_") as tmpdir:
            tmp = Path(tmpdir)
            runner_path = tmp / "run_orbital_qa.cjs"
            cfg_path = tmp / "qa_config.json"

            runner_path.write_text(NODE_PLAYWRIGHT_RUNNER, encoding="utf-8")
            cfg_path.write_text(
                json.dumps(
                    {
                        "baseOrigin": base_origin,
                        "playwrightDir": str(playwright_dir),
                        "chromeExe": str(chrome_exe),
                        "phase1Pages": PHASE1_HTML_FILES,
                        "smokePages": PHASE2_3_SMOKE_PAGES,
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )

            proc = subprocess.run(
                ["node", str(runner_path), str(cfg_path)],
                cwd=str(ROOT),
                capture_output=False,
                text=True,
                timeout=180,
            )
            return proc.returncode
    finally:
        server.shutdown()
        server.server_close()


def main() -> int:
    s1_passed, s1_failed = run_stage1_audit()
    print(f"\n=== STAGE 1 SUMMARY: passed={s1_passed}, failed={s1_failed} ===")

    s2_rc = run_stage2_chromium()
    if s1_failed > 0 or s2_rc != 0:
        print(f"\n[FAIL] OVERALL PHASE 1 QA FAILED (stage1_failed={s1_failed}, stage2_exit={s2_rc})")
        return 1

    print("\n[PASS] ALL STAGE 1 AND STAGE 2 CHECKS PASSED!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
