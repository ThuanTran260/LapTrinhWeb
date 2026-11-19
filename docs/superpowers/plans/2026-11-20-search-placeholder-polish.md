# Search Placeholder Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Unify and shorten the storefront search input placeholder to `"Tìm kiếm Monster, Redbull..."` across all 11 storefront HTML pages and add defensive CSS ellipsis/flex-shrink rules in `css/style.css` so the placeholder never clips mid-character.

**Architecture:** Add a dedicated Python verification script first (TDD) covering both CSS rules and all 11 HTML files, apply the `.search-input` / `.search-input::placeholder` rules in `css/style.css`, then update the `placeholder` attribute in all 11 storefront HTML files and verify zero regressions across the full verification suite.

**Tech Stack:** Static HTML5, CSS3, Python 3 Standard Library (`re`, `sys`, `pathlib`).

## Global Constraints
- Pure static HTML/CSS/JS storefront; do not introduce build tools or external Python dependencies.
- Exact placeholder string on all 11 storefront HTML pages: `"Tìm kiếm Monster, Redbull..."`.
- Preserve existing `class="search-input"`, `autocomplete`, `onfocus`, and `onclick` attributes on every file.
- Do not modify `pages/login.html`, `pages/payment-gateway.html`, `pages/order-success.html`, or `admin/*.html`.
- Strictly local git commits only; NEVER run `git push`.
- Maintain 100% PASS across `verify_implementation.py` and all `scripts/verify_*.py` suites.

---

### Task 1: Add Verification Script & Defensive CSS Rules

**Files:**
- Create: `scripts/verify_search_placeholder_polish.py`
- Modify: `css/style.css:283-292`

**Interfaces:**
- Produces: `scripts/verify_search_placeholder_polish.py` (exit `0` when CSS and all 11 HTML files pass; exit `1` otherwise).

- [ ] **Step 1: Write the verification script (`scripts/verify_search_placeholder_polish.py`)**

```python
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
EXPECTED_PLACEHOLDER = "Tìm kiếm Monster, Redbull..."

STOREFRONT_FILES = [
    "index.html",
    "pages/account.html",
    "pages/cart.html",
    "pages/order-detail.html",
    "pages/orders.html",
    "pages/search-results.html",
    "pages/product-detail.html",
    "pages/product-detail-redbull.html",
    "pages/product-detail-sting.html",
    "pages/product-detail-redbull-lonvua.html",
    "pages/product-detail-redbull-thai.html",
]

DISALLOWED_PLACEHOLDERS = [
    "Tìm kiếm Monster Energy, Redbull, Sting...",
    "Tìm kiếm vị yêu thích",
    "Tìm kiếm Monster, Redbull, Sting...",
    "Tìm kiếm Redbull, Monster, Sting...",
    "Tìm kiếm Sting, Monster, Redbull...",
]


def extract_css_block(css_text: str, selector: str) -> str:
    pattern = re.compile(rf"{re.escape(selector)}\s*\{{([^}}]*)\}}", re.MULTILINE)
    match = pattern.search(css_text)
    return match.group(1) if match else ""


def main() -> int:
    failures = []

    css_path = ROOT / "css" / "style.css"
    css_text = css_path.read_text(encoding="utf-8")

    search_input_block = extract_css_block(css_text, ".search-input")
    placeholder_block = extract_css_block(css_text, ".search-input::placeholder")

    if "min-width: 0;" not in search_input_block:
        failures.append("css/style.css: .search-input missing 'min-width: 0;'")
    if "text-overflow: ellipsis;" not in search_input_block:
        failures.append("css/style.css: .search-input missing 'text-overflow: ellipsis;'")
    if "text-overflow: ellipsis;" not in placeholder_block:
        failures.append("css/style.css: .search-input::placeholder missing 'text-overflow: ellipsis;'")

    input_tag_re = re.compile(r'<input\b[^>]*class="[^"]*\bsearch-input\b[^"]*"[^>]*>', re.IGNORECASE)
    placeholder_re = re.compile(r'placeholder="([^"]*)"')

    for rel_path in STOREFRONT_FILES:
        file_path = ROOT / rel_path
        if not file_path.exists():
            failures.append(f"{rel_path}: file missing")
            continue

        content = file_path.read_text(encoding="utf-8")
        tag_match = input_tag_re.search(content)
        if not tag_match:
            failures.append(f"{rel_path}: missing <input class=\"search-input\">")
            continue

        tag = tag_match.group(0)
        ph_match = placeholder_re.search(tag)
        actual = ph_match.group(1) if ph_match else None
        if actual != EXPECTED_PLACEHOLDER:
            failures.append(
                f"{rel_path}: expected placeholder '{EXPECTED_PLACEHOLDER}', got '{actual}'"
            )

        for old_text in DISALLOWED_PLACEHOLDERS:
            if old_text in tag:
                failures.append(f"{rel_path}: disallowed old placeholder fragment '{old_text}'")

    if failures:
        print(f"FAIL ({len(failures)} checks failed):")
        for item in failures:
            print(f"  - {item}")
        return 1

    print(f"ALL {3 + len(STOREFRONT_FILES)} CHECKS PASSED: CSS safeguard + 11 storefront placeholders verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run the verification script to verify it fails (RED)**

Run: `python scripts/verify_search_placeholder_polish.py`
Expected: Exit code `1` with 14 failures (3 CSS checks + 11 HTML placeholder checks).

- [ ] **Step 3: Add defensive CSS rules in `css/style.css`**

Update `css/style.css` lines 283–292 from:
```css
.search-input {
  flex: 1;
  background: transparent;
  color: #FFF;
  padding: 8px 16px;
  font-size: 0.9rem;
}
.search-input::placeholder {
  color: var(--text-dim);
}
```
to:
```css
.search-input {
  flex: 1;
  min-width: 0;
  background: transparent;
  color: #FFF;
  padding: 8px 16px;
  font-size: 0.9rem;
  text-overflow: ellipsis;
}
.search-input::placeholder {
  color: var(--text-dim);
  text-overflow: ellipsis;
}
```

- [ ] **Step 4: Re-run `python scripts/verify_search_placeholder_polish.py` to confirm CSS checks pass**

Run: `python scripts/verify_search_placeholder_polish.py`
Expected: Exit code `1` with ONLY the 11 HTML file failures remaining (zero `css/style.css` failures).

- [ ] **Step 5: Commit Task 1 locally**

```bash
git add scripts/verify_search_placeholder_polish.py css/style.css
git commit -m "test(search): add placeholder polish check and css ellipsis safeguard"
```

---

### Task 2: Unify Storefront Search Placeholder Across All 11 HTML Files

**Files:**
- Modify: `index.html:54`
- Modify: `pages/account.html:49`
- Modify: `pages/cart.html:48`
- Modify: `pages/order-detail.html:94`
- Modify: `pages/orders.html:49`
- Modify: `pages/search-results.html:54`
- Modify: `pages/product-detail.html:44`
- Modify: `pages/product-detail-redbull.html:44`
- Modify: `pages/product-detail-sting.html:45`
- Modify: `pages/product-detail-redbull-lonvua.html:43`
- Modify: `pages/product-detail-redbull-thai.html:43`

**Interfaces:**
- Consumes: `scripts/verify_search_placeholder_polish.py` created in Task 1.

- [ ] **Step 1: Update `placeholder` in all 11 HTML files to `"Tìm kiếm Monster, Redbull..."`**

Exact replacements (preserving all other attributes on each `<input>` line):
1. `index.html:54`: `placeholder="Tìm kiếm Monster Energy, Redbull, Sting..."` -> `placeholder="Tìm kiếm Monster, Redbull..."`
2. `pages/account.html:49`: `placeholder="Tìm kiếm Monster Energy, Redbull, Sting..."` -> `placeholder="Tìm kiếm Monster, Redbull..."`
3. `pages/cart.html:48`: `placeholder="Tìm kiếm Monster Energy, Redbull, Sting..."` -> `placeholder="Tìm kiếm Monster, Redbull..."`
4. `pages/order-detail.html:94`: `placeholder="Tìm kiếm Monster Energy, Redbull, Sting..."` -> `placeholder="Tìm kiếm Monster, Redbull..."`
5. `pages/orders.html:49`: `placeholder="Tìm kiếm Monster Energy, Redbull, Sting..."` -> `placeholder="Tìm kiếm Monster, Redbull..."`
6. `pages/search-results.html:54`: `placeholder="Tìm kiếm Monster Energy, Redbull, Sting..."` -> `placeholder="Tìm kiếm Monster, Redbull..."`
7. `pages/product-detail.html:44`: `placeholder="Tìm kiếm Monster, Redbull, Sting..."` -> `placeholder="Tìm kiếm Monster, Redbull..."`
8. `pages/product-detail-redbull.html:44`: `placeholder="Tìm kiếm Redbull, Monster, Sting..."` -> `placeholder="Tìm kiếm Monster, Redbull..."`
9. `pages/product-detail-sting.html:45`: `placeholder="Tìm kiếm Sting, Monster, Redbull..."` -> `placeholder="Tìm kiếm Monster, Redbull..."`
10. `pages/product-detail-redbull-lonvua.html:43`: `placeholder="Tìm kiếm vị yêu thích (Redbull Nắp Bật, Sleek Can...)"` -> `placeholder="Tìm kiếm Monster, Redbull..."`
11. `pages/product-detail-redbull-thai.html:43`: `placeholder="Tìm kiếm vị yêu thích (Redbull Thái Lan, Krating Daeng...)"` -> `placeholder="Tìm kiếm Monster, Redbull..."`

- [ ] **Step 2: Run the new verification script (GREEN)**

Run: `python scripts/verify_search_placeholder_polish.py`
Expected: `ALL 14 CHECKS PASSED: CSS safeguard + 11 storefront placeholders verified.` (exit code `0`).

- [ ] **Step 3: Run the full regression suite**

Run:
- `python verify_implementation.py`
- All `scripts/verify_*.py` scripts
Expected: 100% PASS, 0 failures.

- [ ] **Step 4: Commit Task 2 locally**

```bash
git add index.html pages/account.html pages/cart.html pages/order-detail.html pages/orders.html pages/search-results.html pages/product-detail.html pages/product-detail-redbull.html pages/product-detail-sting.html pages/product-detail-redbull-lonvua.html pages/product-detail-redbull-thai.html
git commit -m "fix(ui): unify storefront search placeholder to 'Tìm kiếm Monster, Redbull...'"
```
