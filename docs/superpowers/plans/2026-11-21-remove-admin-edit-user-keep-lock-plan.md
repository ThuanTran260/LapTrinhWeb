# Remove Admin Edit User Modal (Keep Lock/Unlock) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the "Chỉnh Sửa Thông Tin Người Dùng" (`#modal-edit-user`) modal, table `Sửa` buttons, and `openEditUserModal`/`saveEditUser` JS handlers from admin, while preserving the user lock/unlock (`toggleLockUser`) and add-user (`#modal-add-user`) functionality.

**Architecture:** `admin/customers.html` is the sole admin page containing `#modal-edit-user` and row-level `openEditUserModal(...)` buttons. Removing those UI controls from `admin/customers.html` and removing `currentEditingUserRow`, `openEditUserModal`, and `saveEditUser` from `js/app.js` (while keeping `toggleLockUser`, `openAddUserModal`, `saveAddUser`, `initCustomUsersTable`, and `CUSTOMER_DATA_REGISTRY` intact) leaves user management cleanly focused on adding and locking/unlocking accounts. Affected verification scripts are updated and `scripts/verify_admin_user_lock_only.py` enforces both removal of user editing and preservation of user locking.

**Tech Stack:** Static HTML5, Vanilla JS, Python 3 + Node.js verification scripts.

## Global Constraints

- Preserve all 6 `toggleLockUser` buttons (`5` `.btn-action-lock` + `1` `.btn-action-unlock`) in `admin/customers.html` and `toggleLockUser(btn, customerName)` in `js/app.js`.
- Preserve `#modal-add-user`, `openAddUserModal()`, `saveAddUser()`, `initCustomUsersTable()`, and `CUSTOMER_DATA_REGISTRY` (required by `scripts/verify_admin_tier_privileges.py` and `scripts/verify_unconstrained_add_user.py`).
- Preserve all product edit modals/pages (`#modal-edit-product`, `admin/edit-*.html`).
- Never run `git push`; keep all commits local on `main`.

---

### Task 1: Remove `Sửa` Buttons and `#modal-edit-user` from `admin/customers.html`

**Files:**
- Modify: `admin/customers.html:146-231` and `admin/customers.html:360-406`

- [ ] **Step 1:** In `admin/customers.html`, remove all 6 `<button ... onclick="openEditUserModal(...)" ...><i class="fas fa-edit"></i> Sửa</button>` lines from `#customers-table` (rows `#1` through `#6`), leaving every `<button class="btn-action-lock" ...>` and `<button class="btn-action-unlock" ...>` intact.
- [ ] **Step 2:** Remove the entire `<!-- Modal Sửa Thông Tin Người Dùng (R2) -->` `<div id="modal-edit-user" class="admin-modal-overlay">...</div>` block (`lines 360-406`), keeping `#modal-add-user` and `<div id="toast-container">` intact.
- [ ] **Step 3:** Verify with `git grep -n "modal-edit-user\|openEditUserModal\|saveEditUser\|edit-user-" -- admin/customers.html` that 0 matches remain while `toggleLockUser` matches 6 times and `modal-add-user` remains intact.
- [ ] **Step 4:** Commit locally with message `refactor(admin): remove edit-user modal and buttons from customers page`.

---

### Task 2: Remove `openEditUserModal`, `saveEditUser`, and `currentEditingUserRow` from `js/app.js`

**Files:**
- Modify: `js/app.js:2552` and `js/app.js:2572-2635`

- [ ] **Step 1:** In `js/app.js`, remove `let currentEditingUserRow = null;` (line 2552), `function openEditUserModal(customerKey, btn) { ... }`, and `function saveEditUser(e) { ... }` (lines 2572-2634).
- [ ] **Step 2:** Keep `openAddUserModal`, `saveAddUser`, `toggleLockUser`, `initCustomUsersTable`, and `CUSTOMER_DATA_REGISTRY` untouched.
- [ ] **Step 3:** Verify with `git grep -n "EditUser\|edit-user\|currentEditingUserRow" -- js/app.js` that 0 matches remain, and run `node --check js/app.js` and `python scripts/verify_admin_tier_privileges.py`.
- [ ] **Step 4:** Commit locally with message `refactor(admin): remove edit-user JS handlers while keeping toggleLockUser`.

---

### Task 3: Update Verification Scripts and Add `scripts/verify_admin_user_lock_only.py`

**Files:**
- Modify: `scripts/verify_admin_ui_mockup.py:69-74`
- Modify: `scripts/verify_rubric_coverage.py:127-134`
- Modify: `scripts/verify_unconstrained_add_user.py:82-84`
- Delete: `scripts/verify_admin_edit_user_toast_only.py`
- Create: `scripts/verify_admin_user_lock_only.py`

- [ ] **Step 1:** Update `scripts/verify_admin_ui_mockup.py` Test 4 (`lines 69-74`) to verify `['toggleLockUser', 'btn-action-lock', 'btn-action-unlock']` in `admin/customers.html` (`"Test 4: Quản lý User - Nút Khoá/Mở User"`).
- [ ] **Step 2:** Update `scripts/verify_rubric_coverage.py` check `2.2` (`lines 127-134`) so `c2_2` verifies `'modal-add-user'`, `'toggleLockUser'`, `'btn-action-lock'`, and `'btn-action-unlock'` in `admin/customers.html` without requiring `modal-edit-user`.
- [ ] **Step 3:** Update `scripts/verify_unconstrained_add_user.py` line 82 so instead of checking `openEditUserModal` email extraction, it checks `'openEditUserModal' not in app_js and 'modal-edit-user' not in customers_html`.
- [ ] **Step 4:** Remove obsolete `scripts/verify_admin_edit_user_toast_only.py` and create `scripts/verify_admin_user_lock_only.py` that verifies: (a) `admin/customers.html` has zero `#modal-edit-user`, `openEditUserModal`, `saveEditUser`, or `Sửa` edit buttons in `#customers-table` and retains all 6 `toggleLockUser` buttons (`5` `.btn-action-lock`, `1` `.btn-action-unlock`) plus `#modal-add-user`; (b) `js/app.js` has zero `openEditUserModal`, `saveEditUser`, `currentEditingUserRow`, or `modal-edit-user` while retaining `toggleLockUser` and `CUSTOMER_DATA_REGISTRY`; and (c) a Node.js VM runtime smoke test calls `toggleLockUser` for both lock (`.btn-action-lock` -> `'info'` toast) and unlock (`.btn-action-unlock` -> `'success'` toast).
- [ ] **Step 5:** Run `python scripts/verify_admin_user_lock_only.py`, `python scripts/verify_admin_ui_mockup.py`, `python scripts/verify_unconstrained_add_user.py`, `python scripts/verify_admin_customers_and_vip_filter.py`, `python scripts/verify_admin_tier_privileges.py`, `python scripts/verify_rubric_coverage.py`, and `python scripts/verify_pages_deploy_ready.py`, confirming all exit 0.
- [ ] **Step 6:** Commit changes locally with message `test(admin): verify edit-user removal and user lock preservation`.
