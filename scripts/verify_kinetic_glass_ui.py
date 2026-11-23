# -*- coding: utf-8 -*-
"""
verify_kinetic_glass_ui.py
Regression and architecture checks for the Adaptive Kinetic Glass UI layer:
1. css/kinetic-glass.css: existence, balanced braces, required CSS features,
   dual-mode selectors, and zero overflow: hidden / overflow-x: hidden on html or body.
2. js/motion-engine.js: existence, required APIs/guards, and no aria-pressed on #volt-canvas-toggle.
3. js/app.js: loads js/motion-engine.js dynamically using SITE_ROOT.
4. All 28 HTML files (index.html, 13 pages/*.html, 14 admin/*.html): load kinetic-glass.css
   inside <head> strictly AFTER style.css.
5. css/style.css: untouched (git diff -- css/style.css returns empty output).
"""

import os
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent


def strip_css_comments(css_text: str) -> str:
    return re.sub(r"/\*[\s\S]*?\*/", "", css_text)


def check_css_balanced_braces(css_text: str) -> tuple[bool, str]:
    cleaned = strip_css_comments(css_text)
    depth = 0
    in_quote = None
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
    parts: list[str] = []
    current: list[str] = []
    paren_depth = 0
    bracket_depth = 0
    in_quote = None
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
    in_quote = None
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


def find_html_body_overflow_violations(css_text: str) -> list[str]:
    cleaned = strip_css_comments(css_text)
    violations: list[str] = []

    stack: list[tuple[str, int]] = []
    header_start = 0
    in_quote = None
    escaped = False

    i = 0
    n = len(cleaned)
    while i < n:
        ch = cleaned[i]
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
            header = cleaned[header_start:i].strip()
            stack.append((header, i + 1))
            header_start = i + 1
        elif ch == "}":
            if stack:
                header, body_start = stack.pop()
                body = cleaned[body_start:i]
                # Inspect leaf declaration blocks (those without nested blocks)
                if "{" not in body and header and not header.lstrip().startswith("@"):
                    if selector_targets_root_or_body(header):
                        if re.search(r"\boverflow(?:-x)?\s*:\s*hidden\b", body, re.IGNORECASE):
                            violations.append(f"Rule '{header}' sets overflow/overflow-x: hidden")
            header_start = i + 1
        i += 1

    return violations


def strip_js_comments(js_text: str) -> str:
    # Remove block and line comments while keeping string literals intact
    pattern = re.compile(
        r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|`(?:\\.|[^`\\])*`)|//[^\n]*|/\*[\s\S]*?\*/'
    )
    return pattern.sub(lambda m: m.group(1) if m.group(1) else "", js_text)


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
    # 1. css/kinetic-glass.css checks
    # ------------------------------------------------------------------
    kg_css_path = ROOT / "css" / "kinetic-glass.css"
    if not kg_css_path.is_file():
        record("css/kinetic-glass.css exists", False, "file missing")
        kg_css = ""
    else:
        kg_css = kg_css_path.read_text(encoding="utf-8")
        record("css/kinetic-glass.css exists", len(kg_css.strip()) > 0, f"{len(kg_css)} chars")

    if kg_css:
        balanced, brace_info = check_css_balanced_braces(kg_css)
        record("css/kinetic-glass.css balanced braces", balanced, brace_info)

        required_css_tokens = [
            "@view-transition",
            "@supports (animation-timeline: scroll())",
            "@supports ((animation-timeline: view()) and (animation-range: entry))",
            "@media (prefers-reduced-motion: no-preference)",
            "@media (prefers-reduced-motion: reduce)",
            "#volt-scroll-progress",
            "#volt-canvas-toggle",
            ".kg-border-glow",
            ".kg-glare-layer",
            'data-ui-mode="kinetic"',
            'data-ui-mode="precision"',
        ]
        missing_css_tokens = [tok for tok in required_css_tokens if tok not in kg_css]
        record(
            "css/kinetic-glass.css required rules & tokens",
            len(missing_css_tokens) == 0,
            "all 11 required tokens present" if not missing_css_tokens else f"missing: {missing_css_tokens}",
        )

        overflow_violations = find_html_body_overflow_violations(kg_css)
        record(
            "css/kinetic-glass.css no overflow:hidden / overflow-x:hidden on html or body",
            len(overflow_violations) == 0,
            "clean (preserves overflow-x: clip)" if not overflow_violations else "; ".join(overflow_violations),
        )

    # ------------------------------------------------------------------
    # 2. js/motion-engine.js checks
    # ------------------------------------------------------------------
    motion_js_path = ROOT / "js" / "motion-engine.js"
    if not motion_js_path.is_file():
        record("js/motion-engine.js exists", False, "file missing")
        motion_js = ""
    else:
        motion_js = motion_js_path.read_text(encoding="utf-8")
        record("js/motion-engine.js exists", len(motion_js.strip()) > 0, f"{len(motion_js)} chars")

    if motion_js:
        required_js_tokens = [
            "EnergyMotionEngine",
            "detectMode",
            "volt-canvas-toggle",
            "prefers-reduced-motion",
            "document.hidden",
            "IntersectionObserver",
        ]
        missing_js_tokens = [tok for tok in required_js_tokens if tok not in motion_js]
        record(
            "js/motion-engine.js required symbols & guards",
            len(missing_js_tokens) == 0,
            "all 6 required tokens present" if not missing_js_tokens else f"missing: {missing_js_tokens}",
        )

        motion_code = strip_js_comments(motion_js)
        has_aria_pressed = bool(re.search(r"aria-pressed|ariaPressed", motion_code, re.IGNORECASE))
        record(
            "js/motion-engine.js does NOT attach aria-pressed to volt-canvas-toggle",
            not has_aria_pressed,
            "no aria-pressed in active code" if not has_aria_pressed else "found unexpected aria-pressed",
        )

        has_lenis_hijack = bool(re.search(r"window\.Lenis|lenis\.min\.js", motion_code, re.IGNORECASE))
        record(
            "js/motion-engine.js does NOT load Lenis wheel-hijacking (preserves 1:1 native scroll)",
            not has_lenis_hijack,
            "1:1 native scroll preserved (no Lenis)" if not has_lenis_hijack else "found Lenis wheel-hijack conflicting with scroll-behavior: smooth",
        )

    # ------------------------------------------------------------------
    # 3. js/app.js checks
    # ------------------------------------------------------------------
    app_js_path = ROOT / "js" / "app.js"
    if not app_js_path.is_file():
        record("js/app.js exists", False, "file missing")
    else:
        app_js = app_js_path.read_text(encoding="utf-8")
        app_code = strip_js_comments(app_js)
        has_site_root = bool(re.search(r"\bconst\s+SITE_ROOT\b|\bSITE_ROOT\b", app_code))
        loader_match = re.search(
            r"SITE_ROOT[\s\S]{0,400}js/motion-engine\.js",
            app_code,
        )
        record(
            "js/app.js loads motion-engine.js using SITE_ROOT",
            has_site_root and loader_match is not None,
            "dynamic SITE_ROOT + 'js/motion-engine.js' loader verified"
            if (has_site_root and loader_match)
            else "missing SITE_ROOT-based loader for js/motion-engine.js",
        )

    # ------------------------------------------------------------------
    # 4. All 28 HTML files include kinetic-glass.css AFTER style.css
    # ------------------------------------------------------------------
    index_html = [ROOT / "index.html"]
    pages_html = sorted((ROOT / "pages").glob("*.html"))
    admin_html = sorted((ROOT / "admin").glob("*.html"))
    all_html = index_html + pages_html + admin_html

    expected_counts_ok = len(pages_html) == 13 and len(admin_html) == 14 and len(all_html) == 28
    record(
        "HTML file inventory (1 root + 13 pages + 14 admin = 28)",
        expected_counts_ok,
        f"root={len(index_html)}, pages={len(pages_html)}, admin={len(admin_html)}, total={len(all_html)}",
    )

    link_tag_re = re.compile(r"<link\b[^>]*>", re.IGNORECASE)
    href_re = re.compile(r"""href\s*=\s*["']([^"']+)["']""", re.IGNORECASE)

    html_failures: list[str] = []
    for html_path in all_html:
        rel_path = html_path.relative_to(ROOT).as_posix()
        if not html_path.is_file():
            html_failures.append(f"{rel_path}: file missing")
            continue

        content = html_path.read_text(encoding="utf-8")
        head_match = re.search(r"<head\b[^>]*>([\s\S]*?)</head>", content, re.IGNORECASE)
        if not head_match:
            html_failures.append(f"{rel_path}: missing <head> block")
            continue

        head_html = head_match.group(1)
        expected_prefix = "css/" if rel_path == "index.html" else "../css/"

        style_positions: list[int] = []
        kg_positions: list[int] = []

        for m in link_tag_re.finditer(head_html):
            tag = m.group(0)
            href_m = href_re.search(tag)
            if not href_m:
                continue
            href = href_m.group(1)
            href_no_q = href.split("?", 1)[0]
            if href_no_q == f"{expected_prefix}style.css":
                style_positions.append(m.start())
            elif href_no_q == f"{expected_prefix}kinetic-glass.css":
                kg_positions.append(m.start())

        if not style_positions:
            html_failures.append(f"{rel_path}: missing {expected_prefix}style.css <link> in <head>")
        if not kg_positions:
            html_failures.append(f"{rel_path}: missing {expected_prefix}kinetic-glass.css <link> in <head>")
        elif len(kg_positions) > 1:
            html_failures.append(f"{rel_path}: duplicate kinetic-glass.css <link> ({len(kg_positions)})")
        elif style_positions and kg_positions[0] <= style_positions[-1]:
            html_failures.append(f"{rel_path}: kinetic-glass.css must appear AFTER style.css")

    record(
        "All 28 HTML files include kinetic-glass.css AFTER style.css",
        len(html_failures) == 0,
        "28/28 verified" if not html_failures else "; ".join(html_failures),
    )

    # ------------------------------------------------------------------
    # 5. css/style.css untouched (git diff -- css/style.css empty)
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
