# Remove "Chi Tiết" Button from Customers Table Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the 6 `Chi Tiết` buttons from the `Đơn Gần Đây` column in `admin/customers.html` while keeping all `#EB-XXXX` order links and all 6 customer name links pointing to `customer-detail.html`, and update `scripts/verify_admin_customers_and_vip_filter.py` accordingly.

**Architecture:** Two strictly disjoint slices executed in parallel: Task 1 removes the 6 `<div style="margin-top: 6px;"><a href="customer-detail.html" class="btn-view-detail" ...>Chi Tiết</a></div>` blocks in `admin/customers.html`; Task 2 updates `scripts/verify_admin_customers_and_vip_filter.py:51-53` to assert `0` `Chi Tiết` buttons in `#customers-table tbody`.

**Tech Stack:** Static HTML5, Python 3 Standard Library.

## Global Constraints
- Pure static HTML/CSS/JS; no external dependencies.
- Keep all 6 `#EB-XXXX` order links (`openOrderDetailModal`) and all 6 customer name links (`<a href="customer-detail.html"><strong>...</strong></a>`) intact in `admin/customers.html`.
- Remove ONLY the 6 `<div style="margin-top: 6px;"><a href="customer-detail.html" class="btn-view-detail" ...><i class="fas fa-receipt"></i> Chi Tiết</a></div>` lines inside `#customers-table tbody`.
- Strictly local git commits only; NEVER run `git push`.
- Maintain 100% PASS across `verify_implementation.py` and all 36 `scripts/verify_*.py` scripts.

---

### Task 1: Remove `Chi Tiết` Buttons from `admin/customers.html`

**Files:**
- Modify: `admin/customers.html:143,161,178,195,212,229`

- [ ] **Step 1: Remove the 6 `Chi Tiết` button lines inside `Đơn Gần Đây`**

Delete `<div style="margin-top: 6px;"><a href="customer-detail.html" class="btn-view-detail" style="padding: 3px 10px; font-size: 0.76rem; text-decoration: none;" title="Xem lịch sử thanh toán của Nguyễn Văn An"><i class="fas fa-receipt"></i> Chi Tiết</a></div>` on all 6 customer rows (`#1`–`#6`).

---

### Task 2: Update `scripts/verify_admin_customers_and_vip_filter.py`

**Files:**
- Modify: `scripts/verify_admin_customers_and_vip_filter.py:51-53`

- [ ] **Step 1: Assert `0` `Chi Tiết` buttons in `#customers-table tbody`**

Replace lines 51–53:
```python
        detail_btns = re.findall(r'<a href="customer-detail\.html" class="btn-view-detail"[^>]*>[\s\S]*?Chi Tiết</a>', tbody)
        if len(detail_btns) != 6:
            failures.append(f"admin/customers.html: expected 6 'Chi Tiết' links to customer-detail.html, found {len(detail_btns)}")
```
with:
```python
        detail_btns = re.findall(r'<a href="customer-detail\.html" class="btn-view-detail"[^>]*>[\s\S]*?Chi Tiết</a>', tbody)
        if len(detail_btns) != 0:
            failures.append(f"admin/customers.html: expected 0 'Chi Tiết' buttons in #customers-table, found {len(detail_btns)}")
```
