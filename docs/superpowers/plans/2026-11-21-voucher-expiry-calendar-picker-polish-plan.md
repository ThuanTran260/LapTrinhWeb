# Voucher Expiry Interactive Calendar Picker (dd/mm/yyyy) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the "Ngày Hết Hạn" fields (`#voucher-expiry` and `#add-voucher-expiry`) in `admin/settings.html` display `dd/mm/yyyy` (`31/12/2026`) while providing a crisp, directly clickable native dark calendar popup (matching `admin/revenue.html` with `Clear` and `Today` actions and full two-way sync).

**Architecture:** Place the native `<input type="date" class="date-native-picker">` directly over the right-side 40px calendar icon area (`opacity: 0; pointer-events: auto; cursor: pointer; z-index: 3`) above the visual `.date-picker-btn` icon (`color: #E2E8F0; pointer-events: none; z-index: 1`), so clicking the calendar icon hits the native `<input type="date">` directly in all browsers and invokes `openNativeDatePicker()` (`showPicker()`). Two-way JS sync (`syncDatePickerToDisplay` + `syncDisplayToDatePicker`) handles picking a date, clicking native `Clear`, and manually typing `dd/mm/yyyy`.

**Tech Stack:** Static HTML5, Vanilla CSS3, Vanilla JS, Python 3 + Node.js verification scripts.

## Global Constraints

- Preserve `#voucher-expiry` and `#add-voucher-expiry` as `type="text"` with `value="31/12/2026"` and `placeholder="dd/mm/yyyy"`, and preserve zero `required`, `min=`, or `max=` constraints inside `#form-add-voucher` (required by `scripts/verify_admin_add_voucher_toast_only.py`).
- Preserve native `<input type="date">` `color-scheme: dark` calendar popup with `Clear` and `Today` support.
- Never run `git push`; keep all commits local on `main`.

---

### Task 1: Upgrade Date Picker Overlay & Crisp Calendar Icon in `admin/settings.html` and `css/style.css`

**Files:**
- Modify: `css/style.css:2026-2063`
- Modify: `admin/settings.html:188-194` and `admin/settings.html:584-590`

- [ ] **Step 1:** In `css/style.css` (`lines 2026-2063`), update `.date-native-picker` to `pointer-events: auto; cursor: pointer; z-index: 3;`, update `.date-picker-btn` to `color: #E2E8F0; pointer-events: none; z-index: 1;`, and highlight `.date-picker-btn` when `.date-ddmmyyyy-wrapper:hover .date-picker-btn` or `.date-native-picker:focus-visible + .date-picker-btn` is active.
- [ ] **Step 2:** In `admin/settings.html`, update both `#voucher-expiry-picker` (`lines 189-193`) and `#add-voucher-expiry-picker` (`lines 585-589`) so:
  - `#voucher-expiry` calls `oninput="updateVoucherLivePreview(); syncDisplayToDatePicker(this, 'voucher-expiry-picker')"` and `onchange="updateVoucherLivePreview(); syncDisplayToDatePicker(this, 'voucher-expiry-picker')"`
  - `#add-voucher-expiry` calls `oninput="syncDisplayToDatePicker(this, 'add-voucher-expiry-picker')"` and `onchange="syncDisplayToDatePicker(this, 'add-voucher-expiry-picker')"`
  - Each `<input type="date" ... class="date-native-picker">` removes `tabindex="-1"` and binds `onclick="openNativeDatePicker('<pickerId>', '<textId>')"` and `onchange="syncDatePickerToDisplay('<textId>', this)"`, while the visual `<span class="date-picker-btn" aria-hidden="true"><i class="fas fa-calendar-alt"></i></span>` sits underneath.
- [ ] **Step 3:** Verify balanced HTML/CSS braces (`css/style.css` `{` == `}`) and commit locally with message `style(admin): make native calendar picker directly clickable on voucher expiry`.

---

### Task 2: Support Native `Clear`, Empty-Field Default, and Two-Way Sync in `js/app.js`

**Files:**
- Modify: `js/app.js:2845-2856`, `js/app.js:2943-2972`, and `js/app.js:3358-3363`

- [ ] **Step 1:** In `js/app.js` `updateVoucherLivePreview()` (`lines 2845-2856`), when `expiryEl` exists and `expiryEl.value.trim()` is empty (`''`), set `previewExpiry.textContent = '31/12/2026'` (or keep fallback clean) while continuing to format both `dd/mm/yyyy` and `yyyy-mm-dd`.
- [ ] **Step 2:** In `openNativeDatePicker(pickerId, textId)` (`lines 2943-2959`), sync valid `dd/mm/yyyy` from `textEl` into `pickerEl.value`, or default `pickerEl.value = '2026-12-31'` when `textEl` is empty and `!pickerEl.value`, then open via `pickerEl.showPicker()` (with `.focus()`/`.click()` fallback).
- [ ] **Step 3:** In `syncDatePickerToDisplay(textId, pickerEl)` (`lines 2961-2971`), if `!pickerEl.value`, set `textEl.value = ''` (supporting the native calendar `Clear` button!) and call `updateVoucherLivePreview()` when `textId === 'voucher-expiry'`; otherwise format `yyyy-mm-dd` -> `dd/mm/yyyy` into `textEl.value` and update live preview.
- [ ] **Step 4:** Add `syncDisplayToDatePicker(textEl, pickerId)` right after `syncDatePickerToDisplay` to keep the hidden `<input type="date">` synced whenever a valid `dd/mm/yyyy` date is typed (or cleared to `''`), and export `window.syncDisplayToDatePicker = syncDisplayToDatePicker` at the bottom of `js/app.js`.
- [ ] **Step 5:** Run `node --check js/app.js` and commit locally with message `fix(admin): support native clear and two-way sync on voucher date picker`.

---

### Task 3: Update `scripts/verify_admin_add_voucher_toast_only.py` and Run Full Settings Suite

**Files:**
- Modify: `scripts/verify_admin_add_voucher_toast_only.py`

- [ ] **Step 1:** Update `scripts/verify_admin_add_voucher_toast_only.py` to verify:
  - `css/style.css` defines `.date-native-picker` with `pointer-events: auto` and `.date-picker-btn`
  - `admin/settings.html` binds `openNativeDatePicker` on `#voucher-expiry-picker` & `#add-voucher-expiry-picker` and `syncDisplayToDatePicker` on `#voucher-expiry` & `#add-voucher-expiry`
  - Node.js VM runtime tests verify: (a) `openNativeDatePicker` when `textEl` is empty sets `pickerEl.value = '2026-12-31'` and calls `showPicker()`, (b) `syncDatePickerToDisplay` formats `'2027-01-05'` -> `'05/01/2027'`, (c) `syncDatePickerToDisplay` with `''` (`Clear` button) clears `textEl.value = ''`, and (d) `syncDisplayToDatePicker` syncs `'04/01/2026'` -> `'2026-01-04'`.
- [ ] **Step 2:** Run `node --check js/app.js`, `python scripts/verify_admin_add_voucher_toast_only.py`, `python scripts/verify_admin_features_update.py`, `python scripts/verify_admin_tier_privileges.py`, `python scripts/verify_order_detail_pages.py`, and `python scripts/verify_pages_deploy_ready.py` and verify all exit 0.
- [ ] **Step 3:** Commit locally with message `test(admin): verify two-way voucher date picker sync and clear behavior`.
