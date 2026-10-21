# TEST READY: Energy Boost Store Admin UI Mockup Test Suite

**Author:** Test Writer 1  
**Date:** 2026-10-20  
**Target Platform:** Python 3 Standard Library (`os`, `sys`) on Windows / Cross-platform  
**Specification Reference:** `ORIGINAL_REQUEST.md` and `explorer_survey_3/report.md`  

---

## 1. Overview

The automated verification suite for the **Energy Boost Store Admin UI Mockup (SGU Web Programming Rubric)** is ready. The suite provides deterministic validation of the 10 canonical acceptance criteria across requirements R1 through R5.

### Key Characteristics
- **Zero External Dependencies:** Built entirely with Python Standard Library (`os`, `sys`). No `pytest`, `selenium`, or browser drivers required.
- **Console Encoding Safe:** Configured with `sys.stdout.reconfigure(encoding='utf-8')` for Windows CMD/PowerShell UTF-8 output.
- **Strict Exit Codes:** Returns `sys.exit(0)` when all 10 criteria pass; returns `sys.exit(1)` if any criterion fails.

---

## 2. Test Execution Commands

### Primary Test Suite (Admin UI Mockup)
Run from project root (`d:\LapTrinhWeb`):
```powershell
python scripts/verify_admin_ui_mockup.py
```

### Full Regression Suite (Layout, Sticky Header, Routing)
```powershell
python verify_implementation.py
```

---

## 3. Test Cases Specification (10 Canonical Checks)

| Test ID | Requirement | Target File | Verified Criteria & Tokens |
|:---|:---|:---|:---|
| **Test 1** | **R1 (Admin Login)** | `admin/login.html` | - Separate URL & independent form<br>- Tokens: `id="admin-login-form"`, `handleAdminLogin`, `ĐĂNG NHẬP HỆ THỐNG QUẢN TRỊ` |
| **Test 2** | **R1 (Admin Logout)** | `admin/index.html` | - Sidebar logout redirects to `login.html`<br>- Tokens: `href="login.html"`, `admin-logout` |
| **Test 3** | **R2 (Add User Modal)** | `admin/customers.html` | - Add User modal & form handlers<br>- Tokens: `id="modal-add-user"`, `openAddUserModal`, `saveAddUser` |
| **Test 4** | **R2 (Edit & Lock User)** | `admin/customers.html` | - Edit modal & Lock/Unlock toggle<br>- Tokens: `id="modal-edit-user"`, `openEditUserModal`, `toggleLockUser` |
| **Test 5** | **R3 (Add Product Preview)** | `admin/inventory.html` | - File upload input & image preview element<br>- Tokens: `type="file"`, `id="add-prod-file"`, `id="add-prod-preview"`, `previewAddProductImage` |
| **Test 6** | **R3 (Edit Product Modal)** | `admin/inventory.html` | - Edit image preview & brand category select<br>- Tokens: `id="edit-prod-img-preview"`, `id="edit-prod-brand-select"`, `previewEditProductImage` |
| **Test 7** | **R3 (Smart Safe Delete)** | `js/app.js` | - Safe delete logic: sold items -> hidden badge; unsold items -> confirmation dialog<br>- Tokens: `handleAdminDeleteProduct`, `confirm`, `ĐÃ ẨN` |
| **Test 8** | **R4 (Order State Machine)** | `admin/orders.html` | - Unidirectional status update modal with 4 canonical states (`Chưa xác nhận`, `Đã xác nhận`, `Đã giao (Thành công)`, `Đã giao (Huỷ đơn)`)<br>- Tokens: `openOrderStatusModal`, `Chưa xác nhận`, `Đã xác nhận`, `Đã giao (Thành công)` |
| **Test 9** | **R4 (Order Filter Toast)** | `js/app.js` | - UI-only simulation toast notification preserving table rows<br>- Tokens: `applyAdminOrderFilter`, `Đã áp dụng bộ lọc đơn hàng` |
| **Test 10** | **R5 (Top 5 VIP & Orders)** | `admin/customers.html` | - Top 5 ranking, date filter inputs, and order detail popup trigger links<br>- Tokens: `TOP 5 KHÁCH HÀNG`, `stat-customer-from`, `stat-customer-to`, `openOrderDetailModal` |

---

## 4. Initial Baseline Results (Pre-Implementation)

Executed on commit baseline before implementer modifications:

### `python scripts/verify_admin_ui_mockup.py`
- **Result:** `1/10 TIÊU CHÍ ĐẠT` (Exit code: `1`)
- **Passing (1):**
  - ✅ Test 9: Quản lý Đơn Hàng - Lọc mô phỏng thông báo Toast (`applyAdminOrderFilter`)
- **Failing (9):**
  - ❌ Test 1: Admin Login Page URL riêng & Form độc lập (`admin/login.html` missing)
  - ❌ Test 2: Admin Sidebar Logout điều hướng về `login.html` (currently points to `../pages/login.html`)
  - ❌ Test 3: Quản lý User - Modal Thêm Người Dùng Mới (missing `#modal-add-user`)
  - ❌ Test 4: Quản lý User - Modal Sửa & Nút Khoá/Mở User (missing `#modal-edit-user`, `toggleLockUser`)
  - ❌ Test 5: Quản lý Kho - Thêm Sản Phẩm có Upload & Preview ảnh (missing file input / preview)
  - ❌ Test 6: Quản lý Kho - Sửa Sản Phẩm nạp đúng Ảnh & Danh mục (missing edit preview / brand select)
  - ❌ Test 7: Quản lý Kho - Xóa sản phẩm an toàn (Smart Safe Delete) (missing `confirm`, `ĐÃ ẨN`)
  - ❌ Test 8: Quản lý Đơn Hàng - Quy trình trạng thái một chiều (missing `#modal-order-status`, 4 states)
  - ❌ Test 10: Thống Kê - Top 5 Khách hàng chi tiêu cao nhất kèm Link Đơn (missing `TOP 5 KHÁCH HÀNG`, `openOrderDetailModal`)

### `python verify_implementation.py`
- **Result:** `ALL 66 CHECKS PASSED PERFECTLY!` (Exit code: `0`)
- **Status:** Baseline regression tests are 100% green.

---

## 5. Verification for Completion (TDD Goal)

When implementation is completed:
1. `python scripts/verify_admin_ui_mockup.py` MUST report:
   ```text
   KẾT QUẢ TỔNG HỢP: 10/10 TIÊU CHÍ ĐẠT
   🎉 XÁC MINH TOÀN DIỆN THÀNH CÔNG (10/10 PASS) - ĐẠT CHUẨN RUBRIC!
   ```
   with exit code `0`.
2. `python verify_implementation.py` MUST maintain `ALL 66 CHECKS PASSED PERFECTLY!` with exit code `0`.
