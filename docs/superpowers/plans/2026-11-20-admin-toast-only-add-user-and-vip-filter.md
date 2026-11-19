# Toast-Only Add User & Toast-Only Top 5 VIP Filter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert `saveAddUser`, `initCustomUsersTable`, and `toggleTop5VipFilter` (plus customer filter handlers) in `js/app.js` to strict toast-only simulation that never inserts custom rows into `#customers-table`, never persists `admin_custom_users` in `localStorage` (and cleans stale entries on load), and never hides any rows when clicking `Lọc 5 Người VIP Nhất`.

**Architecture:** Three strictly disjoint parallel slices: Slice 1 updates `js/app.js` (`saveAddUser`, `initCustomUsersTable`, `filterCustomersTableRows`, `toggleTop5VipFilter`, `applyAdminCustomerFilter`, `resetAdminCustomerFilter`); Slice 2 updates `scripts/verify_unconstrained_add_user.py`; Slice 3 updates `scripts/verify_admin_customers_and_vip_filter.py` with Node.js `vm` runtime checks verifying non-mutating DOM and `localStorage` behavior.

**Tech Stack:** Static HTML5, Vanilla JavaScript (ES6), Python 3 Standard Library, Node.js (`v24+`).

## Global Constraints
- Pure static HTML/CSS/JS; no external dependencies.
- `saveAddUser(e)` (`js/app.js`): must ONLY show toast (`'Đã tạo tài khoản thành viên "' + fullname + '" thành công (không ràng buộc)!'`), close `'modal-add-user'`, and reset `#form-add-user`. Zero DOM row insertions into `#customers-table` and zero `localStorage.setItem` writes.
- `initCustomUsersTable()` (`js/app.js`): remains defined (called at DOMContentLoaded), removes any stale `'admin_custom_users'` key from `localStorage` (`localStorage.removeItem('admin_custom_users')`), and never appends rows to `#customers-table`.
- `toggleTop5VipFilter(btn)` & `applyAdminCustomerFilter()` & `resetAdminCustomerFilter()` (`js/app.js`): NEVER set `row.style.display = 'none'` or hide any row in `#customers-table`; always preserve all 6 rows visible while displaying toast feedback.
- Strictly local git commits only; NEVER run `git push`.
- Maintain 100% PASS across `verify_implementation.py` and all 36 `scripts/verify_*.py` scripts.

---

### Task 1: Make `saveAddUser`, `initCustomUsersTable`, and Customer Filters Toast-Only (`js/app.js`)

**Files:**
- Modify: `js/app.js:2311-2374,2447-2524,2596-2634`

- [ ] **Step 1: Update `filterCustomersTableRows`, `toggleTop5VipFilter`, `applyAdminCustomerFilter`, and `resetAdminCustomerFilter` (`js/app.js:2311-2374`)**

```javascript
let isTop5VipFilterActive = false;

function filterCustomersTableRows() {
  const rows = document.querySelectorAll('#customers-table tbody tr');
  if (!rows || !rows.length) return;
  rows.forEach((row) => {
    row.style.display = '';
  });
}

function toggleTop5VipFilter(btn) {
  isTop5VipFilterActive = !isTop5VipFilterActive;
  const targetBtn = btn || document.getElementById('btn-filter-top5-vip');
  if (targetBtn && targetBtn.classList) {
    targetBtn.classList.toggle('active', isTop5VipFilterActive);
  }
  filterCustomersTableRows();
  showToast(
    isTop5VipFilterActive
      ? 'Đang lọc hiển thị 5 người VIP chi tiêu cao nhất!'
      : 'Đang hiển thị toàn bộ danh sách khách hàng.',
    isTop5VipFilterActive ? 'success' : 'info'
  );
}

function applyAdminCustomerFilter() {
  const tierEl = document.getElementById('filter-customer-tier');
  const tier = tierEl ? tierEl.options[tierEl.selectedIndex].text : 'Tất cả';
  const fromEl = document.getElementById('stat-customer-from');
  const toEl = document.getElementById('stat-customer-to');
  const from = fromEl ? fromEl.value : '2026-01-01';
  const to = toEl ? toEl.value : '2026-10-17';

  filterCustomersTableRows();
  showToast('Đã thống kê khách hàng (' + from + ' đến ' + to + ') - Phân loại: ' + tier, 'success');
}

function resetAdminCustomerFilter() {
  isTop5VipFilterActive = false;
  const top5Btn = document.getElementById('btn-filter-top5-vip');
  if (top5Btn && top5Btn.classList) top5Btn.classList.remove('active');
  const tierEl = document.getElementById('filter-customer-tier');
  if (tierEl) tierEl.value = 'all';
  const kwEl = document.getElementById('filter-customer-keyword');
  if (kwEl) kwEl.value = '';
  filterCustomersTableRows();
  showToast('Đã đặt lại bộ lọc khách hàng', 'info');
}
```

- [ ] **Step 2: Update `saveAddUser` and `initCustomUsersTable` (`js/app.js:2447-2524,2596-2634`)**

```javascript
function saveAddUser(e) {
  if (e && e.preventDefault) e.preventDefault();

  const fullnameInput = document.getElementById('add-user-fullname');
  const fullname = (fullnameInput && fullnameInput.value.trim()) || 'Người Dùng Mới';

  showToast('Đã tạo tài khoản thành viên "' + fullname + '" thành công (không ràng buộc)!', 'success');
  closeAdminModal('modal-add-user');
  const form = document.getElementById('form-add-user');
  if (form) form.reset();
}
```
and:
```javascript
function initCustomUsersTable() {
  if (typeof window === 'undefined' || typeof document === 'undefined') return;
  try {
    if (typeof localStorage !== 'undefined' && typeof localStorage.removeItem === 'function') {
      localStorage.removeItem('admin_custom_users');
    }
  } catch (err) {}
  document.querySelectorAll('#customers-table tbody tr[data-custom-user-id]').forEach((row) => {
    if (row && typeof row.remove === 'function') row.remove();
  });
}
```

- [ ] **Step 3: Verify syntax (`node --check js/app.js`)**

---

### Task 2: Update `scripts/verify_unconstrained_add_user.py` for Toast-Only Add User

**Files:**
- Modify: `scripts/verify_unconstrained_add_user.py:74-84`

- [ ] **Step 1: Update checks 79–81 in `scripts/verify_unconstrained_add_user.py`**

Replace lines 79–81:
```python
check('customers-table' in app_js, "saveAddUser targets customers-table avoiding dashboard table pollution")
check('admin_custom_users' in app_js, "saveAddUser persists custom users in localStorage")
check('initCustomUsersTable' in app_js, "app.js provides initCustomUsersTable to reload custom users")
```
with:
```python
check('modal-add-user' in app_js, "saveAddUser closes modal-add-user after toast feedback")
check('localStorage.removeItem(\'admin_custom_users\')' in app_js or "removeItem('admin_custom_users')" in app_js, "initCustomUsersTable clears stale admin_custom_users without appending rows")
check('function initCustomUsersTable(' in app_js, "app.js provides initCustomUsersTable cleanup hook")
```

---

### Task 3: Update `scripts/verify_admin_customers_and_vip_filter.py` for Toast-Only Runtime Verification

**Files:**
- Modify: `scripts/verify_admin_customers_and_vip_filter.py:61-150`

- [ ] **Step 1: Update Node `vm` runtime test in `scripts/verify_admin_customers_and_vip_filter.py`**

Verify in Node `vm`:
1. `toggleTop5VipFilter(top5Btn)` toggles `'active'`, calls `showToast`, and keeps ALL 6 rows (`rows[0..5].style.display === ''`, zero rows set to `'none'`).
2. `applyAdminCustomerFilter()` and `resetAdminCustomerFilter()` also keep ALL 6 rows visible and emit toasts.
3. `saveAddUser` emits success toast, closes `'modal-add-user'`, resets `#form-add-user`, performs `0` `tbody.insertBefore` / `appendChild` calls, and performs `0` `localStorage.setItem` writes.
4. `initCustomUsersTable` calls `localStorage.removeItem('admin_custom_users')` and adds `0` rows.
