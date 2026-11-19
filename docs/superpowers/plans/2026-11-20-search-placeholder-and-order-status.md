# Search Placeholder Refinement & Account Order Status Unification Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update all 11 storefront search placeholders to `"Tìm kiếm Monster, Redbull, Sting..."` (Approach 1, preserving CSS ellipsis safeguards and static dropdown behavior) and unify `#EB-2026` status to `"HOÀN THÀNH"` in `pages/account.html` and `pages/order-detail.html` static fallback.

**Architecture:** Split into two independent TDD tasks: Task 1 updates `scripts/verify_search_placeholder_polish.py` first (RED), updates the 11 storefront HTML placeholders to `"Tìm kiếm Monster, Redbull, Sting..."` (GREEN), and commits; Task 2 adds `scripts/verify_account_order_status_sync.py` first (RED), updates `#EB-2026` badge markup in `pages/account.html` and `pages/order-detail.html` (GREEN), verifies the entire test suite, and commits.

**Tech Stack:** Static HTML5, CSS3, Python 3 Standard Library (`re`, `sys`, `pathlib`).

## Global Constraints
- Pure static HTML/CSS/JS storefront; do not introduce build tools or external Python dependencies.
- Exact storefront search placeholder across all 11 storefront HTML files: `"Tìm kiếm Monster, Redbull, Sting..."`.
- Keep existing `min-width: 0; text-overflow: ellipsis;` CSS safeguard in `css/style.css` and do not modify `js/app.js` or `#search-dropdown-menu` items.
- Preserve existing `class="search-input"`, `autocomplete`, `onfocus`, and `onclick` attributes on every search input.
- Do not modify `pages/login.html`, `pages/payment-gateway.html`, `pages/order-success.html`, `pages/orders.html`, or `admin/*.html`.
- Exact order status badge on `#EB-2026` and `#EB-2025` in `pages/account.html`: `<span class="badge-status success" style="font-size: 0.75rem;"><i class="fas fa-check-circle"></i> HOÀN THÀNH</span>`.
- Exact static fallback badge `#order-detail-status` in `pages/order-detail.html`: `<span id="order-detail-status" class="badge-status success"><i class="fas fa-check-circle"></i> HOÀN THÀNH</span>`.
- Strictly local git commits only; NEVER run `git push`.
- Maintain 100% PASS across `verify_implementation.py` and all `scripts/verify_*.py` suites.

---

### Task 1: Refine Storefront Search Placeholder to `"Tìm kiếm Monster, Redbull, Sting..."`

**Files:**
- Modify: `scripts/verify_search_placeholder_polish.py:9,25-31`
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
- Produces: Updated `scripts/verify_search_placeholder_polish.py` asserting `"Tìm kiếm Monster, Redbull, Sting..."` and CSS safeguards (`exit 0`).

- [ ] **Step 1: Update `scripts/verify_search_placeholder_polish.py` for the 36-char placeholder**

Update lines 9 and 25–31 of `scripts/verify_search_placeholder_polish.py`:
```python
EXPECTED_PLACEHOLDER = "Tìm kiếm Monster, Redbull, Sting..."
```
and:
```python
DISALLOWED_PLACEHOLDERS = [
    "Tìm kiếm Monster Energy, Redbull, Sting...",
    "Tìm kiếm vị yêu thích",
    "Tìm kiếm Monster, Redbull...",
    "Tìm kiếm Redbull, Monster, Sting...",
    "Tìm kiếm Sting, Monster, Redbull...",
]
```

- [ ] **Step 2: Run the verification script to verify it fails (RED)**

Run: `python scripts/verify_search_placeholder_polish.py`
Expected: Exit code `1` with HTML placeholder failures across all 11 storefront HTML files (expected `'Tìm kiếm Monster, Redbull, Sting...'`, got `'Tìm kiếm Monster, Redbull...'`), while CSS checks pass.

- [ ] **Step 3: Update `placeholder` on all 11 storefront HTML files**

Change `placeholder="Tìm kiếm Monster, Redbull..."` to `placeholder="Tìm kiếm Monster, Redbull, Sting..."` (preserving all other attributes on each `<input>` line) in:
1. `index.html:54`
2. `pages/account.html:49`
3. `pages/cart.html:48`
4. `pages/order-detail.html:94`
5. `pages/orders.html:49`
6. `pages/search-results.html:54`
7. `pages/product-detail.html:44`
8. `pages/product-detail-redbull.html:44`
9. `pages/product-detail-sting.html:45`
10. `pages/product-detail-redbull-lonvua.html:43`
11. `pages/product-detail-redbull-thai.html:43`

- [ ] **Step 4: Run verification scripts (GREEN)**

Run: `python scripts/verify_search_placeholder_polish.py`
Expected: `ALL 14 CHECKS PASSED: CSS safeguard + 11 storefront placeholders verified.` (exit code `0`).

Run: `python scripts/verify_search_features.py` and `python scripts/verify_search_dropdown_hover_stability.py`
Expected: Exit code `0` for both.

- [ ] **Step 5: Commit Task 1 locally**

```bash
git add scripts/verify_search_placeholder_polish.py index.html pages/account.html pages/cart.html pages/order-detail.html pages/orders.html pages/search-results.html pages/product-detail.html pages/product-detail-redbull.html pages/product-detail-sting.html pages/product-detail-redbull-lonvua.html pages/product-detail-redbull-thai.html
git commit -m "fix(ui): refine storefront search placeholder to 'Tìm kiếm Monster, Redbull, Sting...'"
```

---

### Task 2: Unify `#EB-2026` Status to `HOÀN THÀNH` in Account & Order Detail Fallback

**Files:**
- Create: `scripts/verify_account_order_status_sync.py`
- Modify: `pages/account.html:222`
- Modify: `pages/order-detail.html:242`

**Interfaces:**
- Produces: `scripts/verify_account_order_status_sync.py` (exit `0` when `#EB-2026` and `#EB-2025` share `HOÀN THÀNH` status in `pages/account.html` and static `pages/order-detail.html` fallback, while `pages/orders.html` retains `ĐANG GIAO (2H)`).

- [ ] **Step 1: Write `scripts/verify_account_order_status_sync.py`**

```python
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
EXPECTED_ACCOUNT_BADGE = (
    '<span class="badge-status success" style="font-size: 0.75rem;">'
    '<i class="fas fa-check-circle"></i> HOÀN THÀNH</span>'
)
EXPECTED_DETAIL_BADGE = (
    '<span id="order-detail-status" class="badge-status success">'
    '<i class="fas fa-check-circle"></i> HOÀN THÀNH</span>'
)


def main() -> int:
    failures = []

    account_html = (ROOT / "pages" / "account.html").read_text(encoding="utf-8")
    detail_html = (ROOT / "pages" / "order-detail.html").read_text(encoding="utf-8")
    orders_html = (ROOT / "pages" / "orders.html").read_text(encoding="utf-8")

    if "ĐÃ GIAO HỎA TỐC 2H" in account_html:
        failures.append("pages/account.html still contains 'ĐÃ GIAO HỎA TỐC 2H'")
    if "ĐÃ GIAO HỎA TỐC 2H" in detail_html:
        failures.append("pages/order-detail.html still contains 'ĐÃ GIAO HỎA TỐC 2H'")

    card_2026 = re.search(r"Mã đơn: #EB-2026[\s\S]*?Mã đơn: #EB-2025", account_html)
    if not card_2026 or EXPECTED_ACCOUNT_BADGE not in card_2026.group(0):
        failures.append("pages/account.html: #EB-2026 missing unified 'HOÀN THÀNH' badge")

    card_2025 = re.search(r"Mã đơn: #EB-2025[\s\S]*?TIẾP TỤC MUA SẮM", account_html)
    if not card_2025 or EXPECTED_ACCOUNT_BADGE not in card_2025.group(0):
        failures.append("pages/account.html: #EB-2025 missing 'HOÀN THÀNH' badge")

    if EXPECTED_DETAIL_BADGE not in detail_html:
        failures.append("pages/order-detail.html: #order-detail-status missing 'HOÀN THÀNH' fallback badge")

    if "ĐANG GIAO (2H)" not in orders_html or 'filterOrderList(\'shipping\', this)' not in orders_html:
        failures.append("pages/orders.html: shipping order or filter tab unexpectedly altered")

    if failures:
        print(f"FAIL ({len(failures)} checks failed):")
        for item in failures:
            print(f"  - {item}")
        return 1

    print("ALL 6 CHECKS PASSED: #EB-2026 & #EB-2025 unified to 'HOÀN THÀNH' on account & detail fallback.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run the verification script to verify it fails (RED)**

Run: `python scripts/verify_account_order_status_sync.py`
Expected: Exit code `1` with failures reporting `"ĐÃ GIAO HỎA TỐC 2H"` still present in `pages/account.html` and `pages/order-detail.html`.

- [ ] **Step 3: Update `pages/account.html:222` and `pages/order-detail.html:242`**

1. In `pages/account.html:222`, change:
```html
          <span class="badge-status success" style="font-size: 0.75rem;"><i class="fas fa-truck-fast"></i> ĐÃ GIAO HỎA TỐC 2H</span>
```
to:
```html
          <span class="badge-status success" style="font-size: 0.75rem;"><i class="fas fa-check-circle"></i> HOÀN THÀNH</span>
```

2. In `pages/order-detail.html:242`, change:
```html
          <span id="order-detail-status" class="badge-status success"><i class="fas fa-truck-fast"></i> ĐÃ GIAO HỎA TỐC 2H</span>
```
to:
```html
          <span id="order-detail-status" class="badge-status success"><i class="fas fa-check-circle"></i> HOÀN THÀNH</span>
```

- [ ] **Step 4: Run targeted verification & full regression suite (GREEN)**

Run:
- `python scripts/verify_account_order_status_sync.py` (Expected: `ALL 6 CHECKS PASSED`, exit `0`)
- `python verify_implementation.py` (Expected: `ALL 66 CHECKS PASSED PERFECTLY!`, exit `0`)
- All `scripts/verify_*.py` scripts (Expected: `0` failures)

- [ ] **Step 5: Commit Task 2 locally**

```bash
git add scripts/verify_account_order_status_sync.py pages/account.html pages/order-detail.html
git commit -m "fix(orders): unify #EB-2026 status badge to 'HOÀN THÀNH' in account and detail fallback"
```
