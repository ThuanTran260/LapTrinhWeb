# Remove Inventory Product Subtitle Notes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove all 10 `<br/><small style="color: var(--text-muted);">...</small>` note subtitles under product names in `admin/inventory.html`, matching the clean single-line layout of `admin/index.html` `#inventory-section`.

**Architecture:** Clean Column 2 (`Tên Sản Phẩm`) across all 10 `<tr>` rows in `admin/inventory.html:138-318` while preserving the clickable `<a href="edit-monster.html"...><strong>...</strong></a>` wrappers, stock counts, and delete-only Action column. Extend `scripts/verify_admin_inventory_can_links.py` to assert zero `<br` or `<small` notes remain inside Column 2 of the inventory tables.

**Tech Stack:** Static HTML5, Python 3 verification scripts.

## Global Constraints

- Preserve all 10 clickable `<a href="edit-monster.html" ...><strong>...</strong></a>` wrappers in Column 2 and `<a href="edit-monster.html" ...><img ... /></a>` wrappers in Column 1.
- Preserve all stock counts (`1.250 lon`, `680 lon`, `450 lon`, `520 lon`, `890 lon`, `740 lon`, `610 lon`) — notice Tồn Kho's `<small ...>lon</small>` sits inside Column 6 and MUST NOT be touched!
- Never execute `git push`; keep all commits local.

---

### Task 1: Remove Column 2 `<br/><small ...>` Subtitles from All 10 Rows in `admin/inventory.html`

**Files:**
- Modify: `admin/inventory.html:138-318` (strictly Column 2 `<td>` on rows 1–10)

- [ ] **Step 1: Strip `<br/><small style="color: var(--text-muted);">...</small>` from lines 138, 158, 178, 198, 218, 238, 258, 278, 298, and 318**

Keep `<a href="edit-monster.html" style="color: inherit; text-decoration: none;" title="Chỉnh sửa sản phẩm"><strong>...</strong></a>` intact inside `<td>...</td>`. Leave `<small style="color: var(--text-muted); font-size: 0.8rem; font-weight: 500;">lon</small>` in Column 6 (`Tồn Kho`) completely untouched.

- [ ] **Step 2: Run existing inventory verification scripts**

Run:
`python scripts/verify_admin_inventory_can_links.py; python scripts/verify_admin_features_update.py; python scripts/verify_order_detail_pages.py`
Expected: all exit 0.

---

### Task 2: Enforce Zero Column-2 Note Subtitles in `scripts/verify_admin_inventory_can_links.py`

**Files:**
- Modify: `scripts/verify_admin_inventory_can_links.py`

- [ ] **Step 1: Add Column 2 cleanliness assertion in `verify_inventory_table()` (`scripts/verify_admin_inventory_can_links.py`)**

Assert that `cells[1]` (Column 2, product name cell) contains neither `<small` nor `<br` in both `admin/index.html` (`#inventory-section`) and `admin/inventory.html` (`cart-table`).

- [ ] **Step 2: Run verification checks**

Run:
`python scripts/verify_admin_inventory_can_links.py; python scripts/verify_admin_features_update.py; python scripts/verify_order_detail_pages.py; python verify_implementation.py`
Expected: all exit 0.
