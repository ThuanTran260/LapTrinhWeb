# -*- coding: utf-8 -*-
"""
verify_cosmic_universe.py
Regression and integration checks for the Cosmic Universe Intro (#cosmic-universe-intro):
1. css/cosmic-universe.css: existence, balanced braces, 5 volumetric lighting layers,
   mobile < 768px horizontal scroll-snap rules, @media (prefers-reduced-motion: reduce),
   and zero overflow: hidden / overflow-x: hidden on html or body.
2. js/cosmic-universe.js: existence, exposes EnergyCosmicUniverse, contains
   IntersectionObserver, document.hidden, prefers-reduced-motion, cosmic-motion-toggle,
   zero aria-pressed / ariaPressed in non-comment code, zero wheel event listeners,
   and zero Lenis / lenis.min.js.
3. index.html: links css/cosmic-universe.css AFTER css/kinetic-glass.css in <head>,
   loads js/cosmic-universe.js, contains <section id="cosmic-universe-intro",
   #cosmic-space-canvas, #cosmic-holo-card, #cosmic-motion-toggle (without aria-pressed),
   and all 6 .cosmic-planet-can items with valid assets/images/ and pages/ targets.
4. css/style.css: untouched (git diff -- css/style.css is empty).
"""

import os
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

VOID_HTML_ELEMENTS = frozenset({
    "area", "base", "br", "col", "embed", "hr", "img",
    "input", "link", "meta", "param", "source", "track", "wbr",
})


def strip_css_comments(css_text: str) -> str:
    """Remove CSS /* ... */ comments while preserving quoted string literals."""
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
    """Verify CSS braces and quotes are balanced both structurally and in raw text."""
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
                return False, f"unexpected closing '}}' at cleaned offset {idx}"

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
    """Split CSS selector lists on delimiter outside (), [], and quotes."""
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
    """Return the rightmost compound selector after combinators."""
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
    """Return True if any selector in selector_header directly targets html or body."""
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
    """Parse comment-stripped CSS into (header, body, is_leaf) tuples."""
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
    """Return violations where html or body sets overflow: hidden or overflow-x: hidden."""
    cleaned = strip_css_comments(css_text)
    violations: list[str] = []
    for header, body, is_leaf in extract_css_blocks(cleaned):
        if is_leaf and header and not header.lstrip().startswith("@"):
            if selector_targets_root_or_body(header):
                if re.search(r"\boverflow(?:-x)?\s*:\s*hidden\b", body, re.IGNORECASE):
                    violations.append(f"Rule '{header}' sets overflow/overflow-x: hidden")
    return violations


def strip_js_comments(js_text: str) -> str:
    """Remove // and /* ... */ JS comments while keeping string/template literals intact."""
    pattern = re.compile(
        r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|`(?:\\.|[^`\\])*`)|//[^\n]*|/\*[\s\S]*?\*/'
    )
    return pattern.sub(lambda m: m.group(1) if m.group(1) else "", js_text)


class CosmicIndexParser(HTMLParser):
    """Collect head CSS links, script srcs, and #cosmic-universe-intro DOM structure."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_head = False
        self.cosmic_depth = 0
        self.head_stylesheets: list[str] = []
        self.script_srcs: list[str] = []

        self.has_cosmic_section = False
        self.cosmic_section_attrs: dict[str, str | None] = {}
        self.has_space_canvas = False
        self.has_holo_card = False
        self.motion_toggle_attrs: dict[str, str | None] | None = None
        self.planet_cans: list[dict[str, str | None]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag_l = tag.lower()
        attr_map = {k.lower(): v for k, v in attrs}

        if tag_l == "head":
            self.in_head = True
        elif tag_l == "link" and self.in_head:
            href = (attr_map.get("href") or "").strip()
            rel = (attr_map.get("rel") or "").lower().split()
            if href and ("stylesheet" in rel or not rel):
                self.head_stylesheets.append(href.split("?", 1)[0])
        elif tag_l == "script":
            src = (attr_map.get("src") or "").strip()
            if src:
                self.script_srcs.append(src.split("?", 1)[0])

        el_id = (attr_map.get("id") or "").strip()
        classes = (attr_map.get("class") or "").split()

        if tag_l == "section" and el_id == "cosmic-universe-intro":
            self.has_cosmic_section = True
            self.cosmic_section_attrs = attr_map
            self.cosmic_depth = 1
            return

        if self.cosmic_depth > 0:
            if el_id == "cosmic-space-canvas" and tag_l == "canvas":
                self.has_space_canvas = True
            if el_id == "cosmic-holo-card":
                self.has_holo_card = True
            if el_id == "cosmic-motion-toggle":
                self.motion_toggle_attrs = attr_map
            if "cosmic-planet-can" in classes:
                self.planet_cans.append(attr_map)

            if tag_l not in VOID_HTML_ELEMENTS:
                self.cosmic_depth += 1

    def handle_endtag(self, tag: str) -> None:
        tag_l = tag.lower()
        if tag_l == "head":
            self.in_head = False
        if self.cosmic_depth > 0 and tag_l not in VOID_HTML_ELEMENTS:
            self.cosmic_depth -= 1


def is_within_dir(target_path: Path, parent_dir: Path) -> bool:
    """Return True if target_path resolves strictly inside parent_dir."""
    try:
        target_path.resolve().relative_to(parent_dir.resolve())
        return True
    except ValueError:
        return False


def main() -> int:
    results: list[tuple[str, bool, str]] = []

    def record(name: str, passed: bool, details: str = "") -> None:
        results.append((name, passed, details))
        tag = "PASS" if passed else "FAIL"
        msg = f"[{tag}] {name}"
        if details:
            msg += f" — {details}"
        print(msg)

    os.chdir(ROOT)

    # ------------------------------------------------------------------
    # 1. css/cosmic-universe.css checks
    # ------------------------------------------------------------------
    cosmic_css_path = ROOT / "css" / "cosmic-universe.css"
    if not cosmic_css_path.is_file():
        record("css/cosmic-universe.css exists", False, "file missing")
        cosmic_css = ""
    else:
        cosmic_css = cosmic_css_path.read_text(encoding="utf-8")
        record("css/cosmic-universe.css exists", len(cosmic_css.strip()) > 0, f"{len(cosmic_css)} chars")

    if cosmic_css:
        balanced, brace_info = check_css_balanced_braces(cosmic_css)
        record("css/cosmic-universe.css balanced braces", balanced, brace_info)

        cleaned_css = strip_css_comments(cosmic_css)
        css_blocks = extract_css_blocks(cleaned_css)
        rule_headers = [
            header for header, _, is_leaf in css_blocks
            if is_leaf and header and not header.lstrip().startswith("@")
        ]

        volumetric_selectors = [
            ".cosmic-nebula-layer",
            ".cosmic-torch-layer",
            ".core-hot",
            ".core-corona",
            ".core-accretion",
            ".core-flare",
            ".cosmic-orbit-ring",
            ".planet-rim-halo",
            ".planet-plasma-ring",
        ]
        missing_selectors = [
            sel for sel in volumetric_selectors
            if not any(
                re.search(rf"{re.escape(sel)}(?=$|[\s.,:#\[>+~()])", hdr)
                for hdr in rule_headers
            )
        ]
        record(
            "css/cosmic-universe.css defines all 5 volumetric lighting layers (9 selectors)",
            len(missing_selectors) == 0,
            "all 9 selectors defined" if not missing_selectors else f"missing: {missing_selectors}",
        )

        mobile_media_bodies: list[str] = []
        reduced_motion_bodies: list[str] = []
        for header, body, _ in css_blocks:
            hdr_l = header.strip().lower()
            if hdr_l.startswith("@media"):
                max_w_match = re.search(r"max-width\s*:\s*(\d+(?:\.\d+)?)\s*px", hdr_l)
                if max_w_match and float(max_w_match.group(1)) < 768.0:
                    mobile_media_bodies.append(body)
                if re.search(r"prefers-reduced-motion\s*:\s*reduce", hdr_l):
                    reduced_motion_bodies.append(body)

        mobile_css = "\n".join(mobile_media_bodies)
        mobile_blocks = extract_css_blocks(mobile_css)
        has_track_snap = any(
            ".cosmic-planet-track" in hdr
            and re.search(r"\boverflow-x\s*:\s*auto\b", body, re.IGNORECASE)
            and re.search(r"\bscroll-snap-type\s*:\s*x\b", body, re.IGNORECASE)
            for hdr, body, is_leaf in mobile_blocks
            if is_leaf
        )
        has_can_snap = any(
            ".cosmic-planet-can" in hdr
            and re.search(r"\bscroll-snap-align\s*:\s*(?:center|start|end)\b", body, re.IGNORECASE)
            for hdr, body, is_leaf in mobile_blocks
            if is_leaf
        )
        record(
            "css/cosmic-universe.css mobile (< 768px) horizontal scroll-snap rules",
            bool(mobile_media_bodies) and has_track_snap and has_can_snap,
            "verified .cosmic-planet-track overflow-x/scroll-snap-type: x & .cosmic-planet-can scroll-snap-align"
            if (mobile_media_bodies and has_track_snap and has_can_snap)
            else f"mobile_blocks={len(mobile_media_bodies)}, track_snap={has_track_snap}, can_snap={has_can_snap}",
        )

        has_reduced_motion = any(
            re.search(r"\b(?:animation|transition|transform)\s*:\s*none\b", body, re.IGNORECASE)
            for body in reduced_motion_bodies
        )
        record(
            "css/cosmic-universe.css @media (prefers-reduced-motion: reduce)",
            has_reduced_motion,
            "prefers-reduced-motion: reduce fallback verified" if has_reduced_motion else "missing or empty reduce block",
        )

        overflow_violations = find_html_body_overflow_violations(cosmic_css)
        record(
            "css/cosmic-universe.css zero overflow:hidden / overflow-x:hidden on html or body",
            len(overflow_violations) == 0,
            "clean (no html/body overflow:hidden)" if not overflow_violations else "; ".join(overflow_violations),
        )

    # ------------------------------------------------------------------
    # 2. js/cosmic-universe.js checks
    # ------------------------------------------------------------------
    cosmic_js_path = ROOT / "js" / "cosmic-universe.js"
    if not cosmic_js_path.is_file():
        record("js/cosmic-universe.js exists", False, "file missing")
        cosmic_js = ""
    else:
        cosmic_js = cosmic_js_path.read_text(encoding="utf-8")
        record("js/cosmic-universe.js exists", len(cosmic_js.strip()) > 0, f"{len(cosmic_js)} chars")

    if cosmic_js:
        cosmic_code = strip_js_comments(cosmic_js)

        exposes_api = bool(re.search(r"\b(?:window\.)?EnergyCosmicUniverse\s*=", cosmic_code))
        required_js_tokens = [
            "EnergyCosmicUniverse",
            "IntersectionObserver",
            "document.hidden",
            "prefers-reduced-motion",
            "cosmic-motion-toggle",
        ]
        missing_js_tokens = [tok for tok in required_js_tokens if tok not in cosmic_code]
        record(
            "js/cosmic-universe.js exposes EnergyCosmicUniverse & required runtime guards",
            exposes_api and len(missing_js_tokens) == 0,
            "EnergyCosmicUniverse + IntersectionObserver + document.hidden + prefers-reduced-motion + cosmic-motion-toggle"
            if (exposes_api and not missing_js_tokens)
            else f"exposes_api={exposes_api}, missing={missing_js_tokens}",
        )

        has_aria_pressed = bool(re.search(r"aria-pressed|ariaPressed", cosmic_code, re.IGNORECASE))
        record(
            "js/cosmic-universe.js zero aria-pressed / ariaPressed in non-comment code",
            not has_aria_pressed,
            "clean (no aria-pressed / ariaPressed)" if not has_aria_pressed else "found unexpected aria-pressed/ariaPressed",
        )

        has_wheel_listener = bool(
            re.search(
                r"""(?:addEventListener|trackListener)\s*\([^)]*['"](?:mouse)?wheel['"]|\bon(?:mouse)?wheel\s*=""",
                cosmic_code,
                re.IGNORECASE,
            )
        )
        record(
            "js/cosmic-universe.js zero wheel event listeners",
            not has_wheel_listener,
            "1:1 native scroll preserved (no wheel listener)" if not has_wheel_listener else "found wheel event listener",
        )

        has_lenis = bool(re.search(r"\bLenis\b|lenis\.min\.js", cosmic_code, re.IGNORECASE))
        record(
            "js/cosmic-universe.js zero Lenis / lenis.min.js",
            not has_lenis,
            "clean (no Lenis dependency)" if not has_lenis else "found Lenis reference",
        )

    # ------------------------------------------------------------------
    # 3. index.html checks
    # ------------------------------------------------------------------
    index_path = ROOT / "index.html"
    if not index_path.is_file():
        record("index.html exists", False, "file missing")
    else:
        index_html = index_path.read_text(encoding="utf-8")
        parser = CosmicIndexParser()
        parser.feed(index_html)
        parser.close()

        # 3a. css/cosmic-universe.css linked in <head> strictly AFTER css/kinetic-glass.css
        kg_indices = [i for i, h in enumerate(parser.head_stylesheets) if h == "css/kinetic-glass.css"]
        cu_indices = [i for i, h in enumerate(parser.head_stylesheets) if h == "css/cosmic-universe.css"]
        css_order_ok = (
            len(kg_indices) == 1
            and len(cu_indices) == 1
            and cu_indices[0] > kg_indices[-1]
        )
        record(
            "index.html links css/cosmic-universe.css AFTER css/kinetic-glass.css",
            css_order_ok,
            f"order verified (kinetic-glass.css@{kg_indices}, cosmic-universe.css@{cu_indices})"
            if css_order_ok
            else f"head stylesheets={parser.head_stylesheets}",
        )

        # 3b. loads js/cosmic-universe.js
        cu_scripts = [s for s in parser.script_srcs if s == "js/cosmic-universe.js"]
        record(
            "index.html loads js/cosmic-universe.js",
            len(cu_scripts) == 1,
            "loaded once (js/cosmic-universe.js)" if len(cu_scripts) == 1 else f"matches={cu_scripts}",
        )

        # 3c. Required Cosmic DOM nodes + #cosmic-motion-toggle without aria-pressed
        toggle_ok = (
            parser.motion_toggle_attrs is not None
            and "aria-pressed" not in parser.motion_toggle_attrs
        )
        dom_ok = (
            parser.has_cosmic_section
            and parser.has_space_canvas
            and parser.has_holo_card
            and toggle_ok
        )
        record(
            "index.html cosmic DOM (#cosmic-universe-intro, canvas, holo-card, motion-toggle without aria-pressed)",
            dom_ok,
            "all 4 DOM elements present and #cosmic-motion-toggle has no aria-pressed"
            if dom_ok
            else (
                f"section={parser.has_cosmic_section}, canvas={parser.has_space_canvas}, "
                f"holo={parser.has_holo_card}, toggle_attrs={parser.motion_toggle_attrs}"
            ),
        )

        # 3d. All 6 .cosmic-planet-can items with valid assets/images/ and pages/ targets
        assets_dir = ROOT / "assets" / "images"
        pages_dir = ROOT / "pages"
        can_errors: list[str] = []
        if len(parser.planet_cans) != 6:
            can_errors.append(f"expected 6 .cosmic-planet-can items, found {len(parser.planet_cans)}")

        for idx, attrs in enumerate(parser.planet_cans, 1):
            can_id = attrs.get("data-id") or f"#{idx}"
            data_img = (attrs.get("data-img") or "").strip()
            data_href = (attrs.get("data-href") or "").strip()

            if not data_img:
                can_errors.append(f"{can_id}: missing data-img")
            else:
                img_path = ROOT / data_img
                if not data_img.startswith("assets/images/") or not is_within_dir(img_path, assets_dir) or not img_path.is_file():
                    can_errors.append(f"{can_id}: invalid or missing image '{data_img}'")

            if not data_href:
                can_errors.append(f"{can_id}: missing data-href")
            else:
                href_clean = data_href.split("#", 1)[0].split("?", 1)[0]
                href_path = ROOT / href_clean
                if not href_clean.startswith("pages/") or not is_within_dir(href_path, pages_dir) or not href_path.is_file():
                    can_errors.append(f"{can_id}: invalid or missing page target '{data_href}'")

        record(
            "index.html all 6 .cosmic-planet-can items have valid assets/images/ & pages/ targets",
            len(can_errors) == 0,
            f"6/6 cans verified ({', '.join(c.get('data-id') or '?' for c in parser.planet_cans)})"
            if not can_errors
            else "; ".join(can_errors),
        )

    # ------------------------------------------------------------------
    # 4. css/style.css untouched (git diff -- css/style.css empty)
    # ------------------------------------------------------------------
    diff_unstaged = subprocess.run(
        ["git", "diff", "--", "css/style.css"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    diff_staged = subprocess.run(
        ["git", "diff", "--cached", "--", "css/style.css"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    style_untouched = (
        diff_unstaged.returncode == 0
        and diff_staged.returncode == 0
        and diff_unstaged.stdout.strip() == ""
        and diff_staged.stdout.strip() == ""
    )
    record(
        "git diff -- css/style.css is empty (0 edits)",
        style_untouched,
        "0 edits to css/style.css" if style_untouched else "css/style.css has uncommitted changes",
    )

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    passed_count = sum(1 for _, ok, _ in results if ok)
    total_count = len(results)
    print(f"\nSUMMARY: {passed_count}/{total_count} checks passed.")
    return 0 if passed_count == total_count else 1


if __name__ == "__main__":
    raise SystemExit(main())
