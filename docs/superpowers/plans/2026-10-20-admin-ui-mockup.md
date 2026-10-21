# Giao Diện Quản Trị Admin Tĩnh (SGU Rubric UI Mockup) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Hoàn thiện 100% các tiêu chí giao diện quản trị viên (Admin UI Mockup / Prototype) theo biên bản chấm thi môn Lập trình Web SGU: Đăng nhập/Đăng xuất URL riêng, Quản lý User (Thêm, Sửa, Khoá/Mở), Quản lý Sản phẩm (Upload ảnh có Preview, Sửa nạp đúng ảnh và phân loại, Xóa an toàn kiểm tra xuất bán), và Quản lý Đơn hàng (Cập nhật trạng thái một chiều, Lọc đơn hàng mô phỏng bằng thông báo, Thống kê Top 5 khách hàng chi tiêu cao nhất có danh sách đơn hàng kèm link xem chi tiết).

**Architecture:** 100% Frontend Tĩnh (HTML5, Vanilla CSS3, Vanilla JavaScript ES6) chạy trực tiếp trên trình duyệt Google Chrome thông qua giao thức `file://` hoặc Static Web Server. Tất cả các tính năng nghiệp vụ nâng cao (lọc dữ liệu, lưu trữ cơ sở dữ liệu) chỉ dừng lại ở mức mô phỏng giao diện tương tác (UI simulation), phản hồi nhanh qua hệ thống Toast Dark Neon và Modal Glassmorphism, không xóa hỏng dữ liệu gốc.

**Tech Stack:** HTML5, CSS3 (Dark Neon Theme `#0B0C10`, `#141720`, `#00E676`), Font Awesome 6.4.0, Vanilla JavaScript ES6 (FileReader API cho Image Preview, DOM Manipulation), Python 3 (cho verification script).

## Global Constraints

- **Chỉ dừng ở mức giao diện (UI Simulation Only):** Không triển khai backend hoặc cơ sở dữ liệu thực; các bộ lọc (lọc đơn hàng, lọc khách hàng) chỉ hiển thị thông báo Toast mô phỏng chi tiết, không làm ẩn mất dòng dữ liệu mẫu.
- **Tuân thủ quy tắc Git an toàn (RULE 1):** Tuyệt đối KHÔNG thực hiện lệnh `git push` hoặc bất kỳ hành động đẩy mã lên remote repository. Chỉ thực hiện commit cục bộ (Local Git Commit).
- **Tính toàn vẹn của mã nguồn:** Giữ nguyên cấu trúc CSS và các trang khách hàng hiện có (`index.html`, `pages/*`), chỉ mở rộng và hoàn thiện trong phạm vi `admin/`, `js/app.js` và `css/style.css`.

---

### Task 1: Tạo Bộ Kiểm Thử Tự Động Giao Diện Admin (`scripts/verify_admin_ui_mockup.py`)

**Files:**
- Create: `scripts/verify_admin_ui_mockup.py`

**Interfaces:**
- Consumes: Cấu trúc file và nội dung HTML/JS trong repository `admin/` và `js/app.js`.
- Produces: Mã thoát `exit(0)` nếu tất cả 10 tiêu chuẩn giao diện Admin đều thỏa mãn, ngược lại trả về `exit(1)` kèm chi tiết lỗi.

- [ ] **Step 1: Viết test script kiểm tra toàn bộ 10 tiêu chí giao diện Admin**

```python
# scripts/verify_admin_ui_mockup.py
import os
import sys
import re

def check_file_exists(path):
    if not os.path.exists(path):
        print(f"❌ FAIL: File does not exist: {path}")
        return False
    print(f"✅ PASS: File exists: {path}")
    return True

def check_content(path, patterns, desc):
    if not os.path.exists(path):
        print(f"❌ FAIL: [{desc}] File not found: {path}")
        return False
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    missing = [p for p in patterns if p not in content]
    if missing:
        print(f"❌ FAIL: [{desc}] Missing patterns in {path}: {missing[:3]}")
        return False
    print(f"✅ PASS: [{desc}] All required patterns found in {path}")
    return True

def main():
    print("=" * 60)
    print("KIỂM TRA TIÊU CHÍ GIAO DIỆN QUẢN TRỊ ADMIN (SGU RUBRIC)")
    print("=" * 60)
    
    results = []
    
    # Check 1: admin/login.html exists and has separate form
    results.append(check_file_exists("admin/login.html"))
    results.append(check_content("admin/login.html", [
        'id="admin-login-form"',
        'handleAdminLogin',
        'ĐĂNG NHẬP HỆ THỐNG QUẢN TRỊ'
    ], "Admin Login Page Separate URL"))

    # Check 2: Logout redirects to admin/login.html
    results.append(check_content("admin/index.html", [
        'href="login.html"',
        'admin-logout'
    ], "Admin Index Logout Link"))

    # Check 3: Add User Modal in admin/customers.html
    results.append(check_content("admin/customers.html", [
        'id="modal-add-user"',
        'openAddUserModal',
        'saveAddUser'
    ], "User Management: Add User Modal"))

    # Check 4: Edit User Modal & Lock/Unlock Buttons in admin/customers.html
    results.append(check_content("admin/customers.html", [
        'id="modal-edit-user"',
        'openEditUserModal',
        'toggleLockUser'
    ], "User Management: Edit & Lock/Unlock User"))

    # Check 5: Add Product Modal with File Upload and Preview in admin/inventory.html
    results.append(check_content("admin/inventory.html", [
        'type="file"',
        'id="add-prod-file"',
        'id="add-prod-preview"',
        'previewAddProductImage'
    ], "Add Product: File Input & Image Preview"))

    # Check 6: Edit Product Modal with Image Preview and Category Select
    results.append(check_content("admin/inventory.html", [
        'id="edit-prod-img-preview"',
        'id="edit-prod-brand-select"',
        'previewEditProductImage'
    ], "Edit Product: Display Current Image & Category"))

    # Check 7: Safe Delete Product (Check orders -> Hide vs Confirm & Delete)
    results.append(check_content("js/app.js", [
        'handleAdminDeleteProduct',
        'confirm',
        'ĐÃ ẨN'
    ], "Delete Product: Smart Safe Delete Logic"))

    # Check 8: Order Status Update (Unidirectional state machine)
    results.append(check_content("admin/orders.html", [
        'openOrderStatusModal',
        'Chưa xác nhận',
        'Đã xác nhận',
        'Đã giao (Thành công)'
    ], "Order Management: Standard Statuses & Modal"))
    results.append(check_content("js/app.js", [
        'updateOrderStatusUnidirectional',
        'ORDER_STATUS_ORDER'
    ], "Order Management: Unidirectional State Machine in JS"))

    # Check 9: Order Filter Toast Simulation
    results.append(check_content("js/app.js", [
        'applyAdminOrderFilter',
        'Đã áp dụng bộ lọc đơn hàng'
    ], "Order Filter: Toast Notification Simulation"))

    # Check 10: Top 5 Customer Statistics with Detailed Order Links
    results.append(check_content("admin/customers.html", [
        'TOP 5 KHÁCH HÀNG',
        'stat-customer-from',
        'stat-customer-to',
        'openOrderDetailModal'
    ], "Statistics: Top 5 Customers with Order Detail Links"))

    print("=" * 60)
    passed = sum(1 for r in results if r)
    total = len(results)
    print(f"KẾT QUẢ: {passed}/{total} tiêu chí ĐẠT")
    print("=" * 60)
    sys.exit(0 if passed == total else 1)

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Chạy test để xác nhận kiểm thử ban đầu thất bại (Red Phase)**

Run: `python scripts/verify_admin_ui_mockup.py`
Expected: FAIL (nhiều tiêu chí chưa tồn tại).

- [ ] **Step 3: Commit file test script**

```bash
git add scripts/verify_admin_ui_mockup.py
git commit -m "test: add verification script for admin UI rubric compliance"
```

---

### Task 2: Triển Khai Trang Đăng Nhập & Đăng Xuất Quản Trị Viên Riêng Biệt (`admin/login.html`)

**Files:**
- Create: `admin/login.html`
- Modify: `admin/index.html:39-47`, `admin/inventory.html:35-42`, `admin/orders.html:35-42`, `admin/customers.html:35-42`, `admin/revenue.html:35-42`, `admin/settings.html:35-42`
- Modify: `js/app.js`

**Interfaces:**
- Consumes: CSS Dark Neon từ `../css/style.css`, Toast notification từ `js/app.js`.
- Produces: Trang URL `admin/login.html` với form đăng nhập quản trị viên độc lập; hàm `handleAdminLogin(e)` và hàm `adminLogout()`.

- [ ] **Step 1: Viết mã tạo trang `admin/login.html`**

```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Đăng Nhập Quản Trị | ENERGY BOOST STORE</title>
  <meta name="robots" content="noindex, nofollow" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
  <link rel="stylesheet" href="../css/style.css" />
  <style>
    .admin-login-wrapper {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: radial-gradient(circle at 50% 20%, rgba(0, 230, 118, 0.08) 0%, #0B0C10 70%);
      padding: 20px;
    }
    .admin-login-card {
      background: rgba(20, 23, 32, 0.85);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(0, 230, 118, 0.3);
      box-shadow: 0 12px 35px rgba(0, 0, 0, 0.6), 0 0 20px rgba(0, 230, 118, 0.15);
      border-radius: 16px;
      width: 100%;
      max-width: 440px;
      padding: 36px 32px;
      color: #FFF;
    }
    .admin-login-header {
      text-align: center;
      margin-bottom: 28px;
    }
    .admin-login-header .logo-badge {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 60px;
      height: 60px;
      border-radius: 14px;
      background: rgba(0, 230, 118, 0.15);
      border: 1px solid var(--primary);
      color: var(--primary);
      font-size: 1.8rem;
      margin-bottom: 12px;
    }
    .admin-login-header h1 {
      font-family: var(--font-heading);
      font-size: 1.6rem;
      letter-spacing: 1px;
      margin: 0;
      color: #FFF;
      text-transform: uppercase;
    }
    .admin-login-header p {
      color: var(--text-muted);
      font-size: 0.85rem;
      margin-top: 6px;
    }
  </style>
</head>
<body>

  <div class="admin-login-wrapper">
    <div class="admin-login-card">
      <div class="admin-login-header">
        <div class="logo-badge"><i class="fas fa-shield-halved"></i></div>
        <h1>ĐĂNG NHẬP HỆ THỐNG QUẢN TRỊ</h1>
        <p>Cổng truy cập độc lập dành riêng cho Quản trị viên</p>
      </div>

      <form id="admin-login-form" onsubmit="handleAdminLogin(event)">
        <div class="form-group" style="margin-bottom: 18px;">
          <label class="form-label" for="admin-user"><i class="fas fa-user-shield" style="color: var(--primary);"></i> Tài khoản Quản trị</label>
          <input type="text" id="admin-user" class="form-control" value="admin" placeholder="Nhập tài khoản admin..." required />
        </div>

        <div class="form-group" style="margin-bottom: 22px;">
          <label class="form-label" for="admin-pass"><i class="fas fa-key" style="color: var(--secondary);"></i> Mật khẩu</label>
          <div class="password-wrapper" style="position: relative;">
            <input type="password" id="admin-pass" class="form-control" value="••••••••" placeholder="Nhập mật khẩu..." required />
            <i class="fas fa-eye" id="toggle-admin-pass" onclick="togglePasswordVisibility('admin-pass', 'toggle-admin-pass')" style="position: absolute; right: 14px; top: 50%; transform: translateY(-50%); cursor: pointer; color: var(--text-muted);"></i>
          </div>
        </div>

        <button type="submit" class="btn-primary" style="width: 100%; padding: 13px; font-size: 1rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; display: flex; align-items: center; justify-content: center; gap: 8px;">
          <i class="fas fa-right-to-bracket"></i> Đăng Nhập Quản Trị
        </button>

        <div style="text-align: center; margin-top: 20px;">
          <a href="../index.html" style="color: var(--text-muted); font-size: 0.85rem; text-decoration: none; display: inline-flex; align-items: center; gap: 6px;">
            <i class="fas fa-arrow-left"></i> Quay lại trang mua sắm
          </a>
        </div>
      </form>
    </div>
  </div>

  <div id="toast-container" class="toast-container"></div>
  <script src="../js/app.js"></script>
</body>
</html>
```

- [ ] **Step 2: Viết hàm xử lý đăng nhập & đăng xuất trong `js/app.js`**

```javascript
// Thêm vào js/app.js
function handleAdminLogin(e) {
  if (e && e.preventDefault) e.preventDefault();
  const userEl = document.getElementById('admin-user');
  const user = (userEl ? userEl.value : '').trim();
  
  try {
    localStorage.setItem('admin_logged_in', 'true');
    localStorage.setItem('admin_user_name', user || 'Thuận Trần (Admin)');
  } catch (err) {}

  showToast('Xác thực Quản trị viên cấp cao thành công! Đang chuyển vào Dashboard...', 'success');
  setTimeout(() => {
    window.location.href = 'index.html';
  }, 800);
}

function adminLogout() {
  try {
    localStorage.removeItem('admin_logged_in');
    localStorage.removeItem('admin_user_name');
  } catch (err) {}
  showToast('Đã đăng xuất khỏi tài khoản Quản trị!', 'info');
  setTimeout(() => {
    window.location.href = 'login.html';
  }, 700);
}
```

- [ ] **Step 3: Cập nhật liên kết Đăng xuất tại tất cả các file sidebar trong `admin/*.html`**

Đổi link đăng xuất từ `../pages/login.html` thành:
```html
<a href="login.html" class="admin-menu-link" style="color: #EF4444;" onclick="event.preventDefault(); adminLogout();">
  <i class="fas fa-sign-out-alt"></i> Đăng Xuất
</a>
```

- [ ] **Step 4: Chạy kiểm thử Task 1 & 2**

Run: `python -c "import os; assert os.path.exists('admin/login.html'); print('admin/login.html exists!')"`
Expected: PASS

- [ ] **Step 5: Commit cục bộ**

```bash
git add admin/login.html admin/index.html admin/inventory.html admin/orders.html admin/customers.html admin/revenue.html admin/settings.html js/app.js
git commit -m "feat(admin): add dedicated admin login page and update logout workflow"
```

---

### Task 3: Triển Khai Giao Diện Quản Lý User (Thêm, Sửa, Khoá/Mở) (`admin/customers.html`)

**Files:**
- Modify: `admin/customers.html`
- Modify: `js/app.js`
- Modify: `css/style.css`

**Interfaces:**
- Consumes: Bảng khách hàng và danh sách người dùng trong hệ thống.
- Produces: Nút Thêm User mới, Modal Thêm User (`#modal-add-user`), Modal Sửa User (`#modal-edit-user`), cột Trạng thái với badge trực quan (`ĐANG HOẠT ĐỘNG` / `ĐÃ KHOÁ`) và nút thao tác Khoá / Mở user tức thì trên UI.

- [ ] **Step 1: Bổ sung CSS cho badge trạng thái và nút toggle khoá user trong `css/style.css`**

```css
/* User Lock/Unlock & Management UI */
.badge-status.locked {
  background: rgba(239, 68, 68, 0.18);
  color: #EF4444;
  border: 1px solid rgba(239, 68, 68, 0.4);
}
.btn-action-lock {
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  border: 1px solid rgba(239, 68, 68, 0.4);
  background: rgba(239, 68, 68, 0.1);
  color: #EF4444;
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.2s ease;
}
.btn-action-lock:hover {
  background: rgba(239, 68, 68, 0.25);
  box-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
}
.btn-action-unlock {
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  border: 1px solid rgba(0, 230, 118, 0.4);
  background: rgba(0, 230, 118, 0.1);
  color: var(--primary);
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.2s ease;
}
.btn-action-unlock:hover {
  background: rgba(0, 230, 118, 0.25);
  box-shadow: 0 0 10px rgba(0, 230, 118, 0.3);
}
```

- [ ] **Step 2: Thêm nút "Thêm Người Dùng Mới" và cập nhật các cột của bảng trong `admin/customers.html`**

Thêm nút ở Topbar:
```html
<button class="btn-add-cart" style="padding: 10px 18px;" onclick="openAddUserModal()">
  <i class="fas fa-user-plus"></i> Thêm Người Dùng Mới
</button>
```

Cập nhật các cột của bảng `table.cart-table`:
Thêm cột `Trạng Thái` (ĐANG HOẠT ĐỘNG / ĐÃ KHOÁ) và cập nhật cột `Thao Tác` có đầy đủ 3 nút:
1. `Xem` (`openCustomerDetailModal`)
2. `Sửa` (`openEditUserModal(key)`)
3. `Khoá/Mở` (`toggleLockUser(this, userName)`)

- [ ] **Step 3: Thêm Modal Thêm User (`#modal-add-user`) và Modal Sửa User (`#modal-edit-user`) vào `admin/customers.html`**

```html
<!-- Modal Thêm Người Dùng Mới -->
<div id="modal-add-user" class="admin-modal-overlay">
  <div class="admin-modal-card">
    <div class="admin-modal-header">
      <h3 class="admin-modal-title"><i class="fas fa-user-plus" style="color: var(--primary);"></i> Thêm Tài Khoản Người Dùng</h3>
      <button type="button" class="admin-modal-close" onclick="closeAdminModal('modal-add-user')">&times;</button>
    </div>
    <form id="form-add-user" onsubmit="saveAddUser(event)">
      <div class="admin-modal-body">
        <div class="admin-form-grid">
          <div class="admin-form-group">
            <label class="admin-form-label">Tên Đăng Nhập <span class="req">*</span></label>
            <input type="text" id="add-user-username" class="admin-form-input" placeholder="VD: hoangnam2026" required />
          </div>
          <div class="admin-form-group">
            <label class="admin-form-label">Họ và Tên <span class="req">*</span></label>
            <input type="text" id="add-user-fullname" class="admin-form-input" placeholder="VD: Lê Hoàng Nam" required />
          </div>
          <div class="admin-form-group">
            <label class="admin-form-label">Email <span class="req">*</span></label>
            <input type="email" id="add-user-email" class="admin-form-input" placeholder="nam.lehoang@gmail.com" required />
          </div>
          <div class="admin-form-group">
            <label class="admin-form-label">Số Điện Thoại <span class="req">*</span></label>
            <input type="text" id="add-user-phone" class="admin-form-input" placeholder="0903 111 222" required />
          </div>
          <div class="admin-form-group">
            <label class="admin-form-label">Vai Trò / Phân Quyền</label>
            <select id="add-user-role" class="admin-form-select">
              <option value="user" selected>Khách hàng thành viên</option>
              <option value="vip">Khách hàng VIP</option>
              <option value="admin">Quản trị viên phụ tá</option>
            </select>
          </div>
          <div class="admin-form-group">
            <label class="admin-form-label">Trạng Thái Ban Đầu</label>
            <select id="add-user-status" class="admin-form-select">
              <option value="active" selected>Đang hoạt động</option>
              <option value="locked">Tạm khoá</option>
            </select>
          </div>
        </div>
      </div>
      <div class="admin-modal-footer">
        <button type="button" class="btn-modal-cancel" onclick="closeAdminModal('modal-add-user')">Hủy bỏ</button>
        <button type="submit" class="btn-modal-save"><i class="fas fa-check"></i> Lưu Người Dùng</button>
      </div>
    </form>
  </div>
</div>

<!-- Modal Sửa Người Dùng -->
<div id="modal-edit-user" class="admin-modal-overlay">
  <div class="admin-modal-card">
    <div class="admin-modal-header">
      <h3 class="admin-modal-title"><i class="fas fa-user-edit" style="color: var(--secondary);"></i> Sửa Thông Tin Người Dùng</h3>
      <button type="button" class="admin-modal-close" onclick="closeAdminModal('modal-edit-user')">&times;</button>
    </div>
    <form id="form-edit-user" onsubmit="saveEditUser(event)">
      <div class="admin-modal-body">
        <div class="admin-form-grid">
          <div class="admin-form-group">
            <label class="admin-form-label">Họ và Tên</label>
            <input type="text" id="edit-user-fullname" class="admin-form-input" required />
          </div>
          <div class="admin-form-group">
            <label class="admin-form-label">Số Điện Thoại</label>
            <input type="text" id="edit-user-phone" class="admin-form-input" required />
          </div>
          <div class="admin-form-group full-width">
            <label class="admin-form-label">Email</label>
            <input type="email" id="edit-user-email" class="admin-form-input" required />
          </div>
          <div class="admin-form-group">
            <label class="admin-form-label">Hạng Thành Viên</label>
            <select id="edit-user-tier" class="admin-form-select">
              <option value="KIM CƯƠNG">KIM CƯƠNG</option>
              <option value="VÀNG">VÀNG</option>
              <option value="BẠC">BẠC</option>
            </select>
          </div>
          <div class="admin-form-group">
            <label class="admin-form-label">Trạng Thái</label>
            <select id="edit-user-status" class="admin-form-select">
              <option value="active">Đang hoạt động</option>
              <option value="locked">Đã khoá</option>
            </select>
          </div>
        </div>
      </div>
      <div class="admin-modal-footer">
        <button type="button" class="btn-modal-cancel" onclick="closeAdminModal('modal-edit-user')">Hủy bỏ</button>
        <button type="submit" class="btn-modal-save"><i class="fas fa-save"></i> Cập Nhật Thông Tin</button>
      </div>
    </form>
  </div>
</div>
```

- [ ] **Step 4: Viết các hàm điều khiển User trong `js/app.js`**

Viết các hàm:
- `openAddUserModal()`
- `saveAddUser(e)`: Hiện Toast mô phỏng thêm người dùng mới, prepend dòng mới lên bảng với badge ĐANG HOẠT ĐỘNG.
- `openEditUserModal(customerKey)`: Nạp thông tin mẫu từ `CUSTOMER_DATA_REGISTRY` lên modal sửa.
- `saveEditUser(e)`: Hiện Toast mô phỏng lưu thành công và cập nhật tên trên bảng.
- `toggleLockUser(btn, customerName)`: Chuyển đổi trạng thái dòng người dùng giữa ĐANG HOẠT ĐỘNG và ĐÃ KHOÁ, đổi icon nút khoá/mở và bắn Toast thông báo tương ứng.

- [ ] **Step 5: Chạy kiểm thử tự động xác nhận các tiêu chí User**

Run: `python scripts/verify_admin_ui_mockup.py`
Expected: Các tiêu chí User Management (Check 3 & 4) chuyển sang PASS.

- [ ] **Step 6: Commit cục bộ**

```bash
git add admin/customers.html js/app.js css/style.css
git commit -m "feat(admin): implement user management UI (add, edit, lock/unlock)"
```

---

### Task 4: Triển Khai Upload Ảnh Có Preview & Sửa Sản Phẩm Chuẩn (`admin/inventory.html`)

**Files:**
- Modify: `admin/inventory.html`
- Modify: `js/app.js`

**Interfaces:**
- Consumes: Modal thêm/sửa sản phẩm hiện có.
- Produces:
  - Form Thêm: `<input type="file" id="add-prod-file">` kèm khung preview ảnh bằng `FileReader`.
  - Form Sửa: Hiển thị ảnh hiện tại `#edit-prod-img-preview`, chọn đúng danh mục phân loại `#edit-prod-brand-select`, cho phép đổi ảnh có preview.

- [ ] **Step 1: Cập nhật Modal Thêm Sản Phẩm (`#modal-add-product`) trong `admin/inventory.html`**

Bổ sung trường upload file và vùng hiển thị xem trước ảnh:
```html
<div class="admin-form-group full-width">
  <label class="admin-form-label">Hình Ảnh Sản Phẩm <span class="req">*</span> (Chọn file để xem trước)</label>
  <div style="display: flex; gap: 16px; align-items: center;">
    <input type="file" id="add-prod-file" class="admin-form-input" accept="image/*" onchange="previewAddProductImage(this)" style="flex: 1;" />
    <div id="add-prod-preview-wrapper" style="width: 60px; height: 75px; border: 1px dashed var(--primary); border-radius: 8px; display: flex; align-items: center; justify-content: center; background: rgba(0,0,0,0.3); overflow: hidden;">
      <img id="add-prod-preview" src="../assets/images/monster/original.webp" alt="Xem trước ảnh" style="max-width: 100%; max-height: 100%; object-fit: contain;" />
    </div>
  </div>
</div>
```

- [ ] **Step 2: Cập nhật Modal Sửa Sản Phẩm (`#modal-edit-product`) trong `admin/inventory.html`**

Hiển thị ảnh sản phẩm hiện tại và dropdown phân loại chuẩn:
```html
<div class="admin-form-group full-width" style="display: flex; gap: 16px; align-items: center; background: rgba(255,255,255,0.02); padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06);">
  <img id="edit-prod-img-preview" src="../assets/images/monster/original.webp" alt="Ảnh hiện tại" style="width: 50px; height: 65px; object-fit: contain; border: 1px solid var(--primary); border-radius: 6px; padding: 4px; background: #0B0C10;" />
  <div style="flex: 1;">
    <label class="admin-form-label">Đổi Hình Ảnh (Tùy chọn)</label>
    <input type="file" id="edit-prod-file" class="admin-form-input" accept="image/*" onchange="previewEditProductImage(this)" />
  </div>
</div>

<div class="admin-form-group">
  <label class="admin-form-label">Phân Loại / Thương Hiệu <span class="req">*</span></label>
  <select id="edit-prod-brand-select" class="admin-form-select">
    <option value="Monster Energy">Monster Energy (Cổ điển)</option>
    <option value="Monster Ultra">Monster Ultra (0 Đường)</option>
    <option value="Punch & Shots">Punch & Shots</option>
    <option value="Redbull Thái Lan">Redbull Thái Lan</option>
    <option value="Sting PepsiCo">Sting PepsiCo</option>
  </select>
</div>
```

- [ ] **Step 3: Viết logic đọc file preview ảnh và nạp đúng thông tin khi sửa trong `js/app.js`**

```javascript
// Hàm hiển thị xem trước ảnh khi thêm sản phẩm
function previewAddProductImage(input) {
  if (input.files && input.files[0]) {
    const reader = new FileReader();
    reader.onload = function(e) {
      const img = document.getElementById('add-prod-preview');
      if (img) img.src = e.target.result;
    };
    reader.readAsDataURL(input.files[0]);
  }
}

// Hàm hiển thị xem trước ảnh khi sửa sản phẩm
function previewEditProductImage(input) {
  if (input.files && input.files[0]) {
    const reader = new FileReader();
    reader.onload = function(e) {
      const img = document.getElementById('edit-prod-img-preview');
      if (img) img.src = e.target.result;
    };
    reader.readAsDataURL(input.files[0]);
  }
}
```

Cập nhật hàm `openProductEditModal(productId, triggerBtn)`: Đọc ảnh và thông tin từ dòng được click để nạp lên `#edit-prod-img-preview` và `#edit-prod-brand-select`.

- [ ] **Step 4: Chạy kiểm thử tự động xác nhận tiêu chí Thêm/Sửa sản phẩm**

Run: `python scripts/verify_admin_ui_mockup.py`
Expected: Check 5 & Check 6 chuyển sang PASS.

- [ ] **Step 5: Commit cục bộ**

```bash
git add admin/inventory.html js/app.js
git commit -m "feat(admin): add image preview on add/edit product and sync category selector"
```

---

### Task 5: Triển Khai Xóa Sản Phẩm An Toàn (Đã Bán ➔ Ẩn, Chưa Bán ➔ Xác Nhận & Xóa)

**Files:**
- Modify: `admin/inventory.html`
- Modify: `js/app.js`

**Interfaces:**
- Consumes: Nút xóa sản phẩm trong bảng kho hàng.
- Produces: Hàm `handleAdminDeleteProduct(btn, productName, hasOrders)`:
  - Nếu `hasOrders === true`: Hiện Toast thông báo sản phẩm đã bán, cập nhật badge của dòng đó thành `ĐÃ ẨN` (mô phỏng ẩn khỏi storefront).
  - Nếu `hasOrders === false`: Hiển thị `confirm()`, nếu admin đồng ý thì hiện Toast và remove dòng khỏi bảng.

- [ ] **Step 1: Cập nhật các nút xóa trong `admin/inventory.html`**

Đa dạng hóa danh sách: một số sản phẩm đã bán (`hasOrders = true`, ví dụ: Original, Redbull Original), và một số sản phẩm mới nhập kho chưa bán (`hasOrders = false`, ví dụ: Strawberry Shot, Sting Blue Sleek):
```html
<!-- Sản phẩm đã bán -->
<button class="cart-del-btn" style="padding: 4px 8px;" onclick="handleAdminDeleteProduct(this, 'Monster Energy Original 355ml', true)"><i class="fas fa-trash"></i></button>

<!-- Sản phẩm chưa từng bán -->
<button class="cart-del-btn" style="padding: 4px 8px;" onclick="handleAdminDeleteProduct(this, 'Monster Energy Strawberry Shot 500ml', false)"><i class="fas fa-trash"></i></button>
```

- [ ] **Step 2: Viết hàm `handleAdminDeleteProduct` hoàn chỉnh trong `js/app.js`**

```javascript
function handleAdminDeleteProduct(btn, productName, hasOrders) {
  const name = productName || 'Sản phẩm';
  const row = btn ? btn.closest('tr') : null;

  if (hasOrders) {
    // Sản phẩm đã phát sinh đơn hàng -> Chuyển sang chế độ ẨN
    if (row) {
      const statusCell = row.cells[5];
      if (statusCell) {
        statusCell.innerHTML = '<span class="badge-status" style="background: rgba(255,255,255,0.1); color: #888; border: 1px solid #555;">ĐÃ ẨN</span>';
      }
    }
    showToast('Sản phẩm "' + name + '" đã phát sinh đơn hàng xuất bán! Hệ thống đã chuyển sang chế độ ẨN khỏi web để bảo toàn lịch sử hóa đơn.', 'warning');
  } else {
    // Sản phẩm chưa được bán ra -> Hỏi lại và tiến hành xóa
    const confirmed = confirm('Sản phẩm "' + name + '" chưa phát sinh đơn hàng xuất bán nào.\nBạn có chắc chắn muốn TIẾN HÀNH XOÁ hoàn toàn sản phẩm này khỏi hệ thống?');
    if (confirmed) {
      if (row) row.remove();
      showToast('Đã tiến hành xoá hoàn toàn sản phẩm "' + name + '" khỏi hệ thống kho hàng!', 'info');
    }
  }
}
```

- [ ] **Step 3: Chạy kiểm thử tự động xác nhận tiêu chí Xóa an toàn**

Run: `python scripts/verify_admin_ui_mockup.py`
Expected: Check 7 chuyển sang PASS.

- [ ] **Step 4: Commit cục bộ**

```bash
git add admin/inventory.html js/app.js
git commit -m "feat(admin): implement smart safe delete workflow (hide sold vs confirm delete unsold)"
```

---

### Task 6: Triển Khai Quản Lý Đơn Hàng (Quy Trình Một Chiều & Lọc Mô Phỏng Bằng Toast)

**Files:**
- Modify: `admin/orders.html`
- Modify: `js/app.js`

**Interfaces:**
- Consumes: Bảng đơn hàng tại `admin/orders.html`.
- Produces:
  - 4 trạng thái chuẩn: `Chưa xác nhận` ➔ `Đã xác nhận` ➔ `Đã giao (Thành công)` / `Đã giao (Huỷ đơn)`.
  - Modal hoặc hàm cập nhật trạng thái đơn một chiều `updateOrderStatusUnidirectional()`: chỉ cho phép chọn bước tiếp theo, chặn chọn bước lùi.
  - Hàm `applyAdminOrderFilter()`: Lấy thông tin từ form lọc và hiển thị Toast thông báo chi tiết mà KHÔNG làm mất dòng dữ liệu đơn hàng (đúng yêu cầu chỉ dừng ở mức giao diện).

- [ ] **Step 1: Chuẩn hóa 4 trạng thái trong bảng `admin/orders.html`**

Cập nhật các dòng đơn hàng với trạng thái chuẩn:
- `#EB-8803`: `Chưa xác nhận`
- `#EB-8802`: `Đã xác nhận`
- `#EB-8801`: `Đã giao (Thành công)`
- `#EB-8806`: `Đã giao (Huỷ đơn)`

Cột Thao tác bổ sung nút "Cập Nhật Trạng Thái":
```html
<button class="btn-view-detail" style="padding: 4px 10px; font-size: 0.8rem; background: rgba(0, 230, 118, 0.15); color: var(--primary); border-color: rgba(0, 230, 118, 0.3);" onclick="openOrderStatusModal('EB-8803', 'Chưa xác nhận', this)">
  <i class="fas fa-arrow-right-arrow-left"></i> Chuyển Trạng Thái
</button>
```

- [ ] **Step 2: Thêm Modal Cập Nhật Trạng Thái Đơn Hàng Một Chiều (`#modal-order-status`) vào `admin/orders.html`**

```html
<div id="modal-order-status" class="admin-modal-overlay">
  <div class="admin-modal-card" style="max-width: 480px;">
    <div class="admin-modal-header">
      <h3 class="admin-modal-title"><i class="fas fa-arrows-split-up-and-left" style="color: var(--primary);"></i> Cập Nhật Trạng Thái Đơn Hàng</h3>
      <button type="button" class="admin-modal-close" onclick="closeAdminModal('modal-order-status')">&times;</button>
    </div>
    <div class="admin-modal-body">
      <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 12px;">
        Mã đơn: <strong id="status-modal-order-id" style="color: #FFF;">#EB-8803</strong> | Hiện tại: <span id="status-modal-current-badge" class="badge-status info">Chưa xác nhận</span>
      </p>
      <div style="background: rgba(255,255,255,0.03); padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08); margin-bottom: 16px;">
        <small style="color: #ffcc00;"><i class="fas fa-exclamation-triangle"></i> Quy tắc nghiệp vụ một chiều: Trạng thái chỉ được phép cập nhật xuôi, không cho phép cập nhật ngược.</small>
      </div>
      <label class="admin-form-label">Chọn Trạng Thái Kế Tiếp:</label>
      <select id="select-next-status" class="admin-form-select"></select>
    </div>
    <div class="admin-modal-footer">
      <button type="button" class="btn-modal-cancel" onclick="closeAdminModal('modal-order-status')">Hủy bỏ</button>
      <button type="button" class="btn-modal-save" onclick="saveOrderStatus()"><i class="fas fa-check"></i> Xác Nhận Cập Nhật</button>
    </div>
  </div>
</div>
```

- [ ] **Step 3: Viết logic ràng buộc một chiều trong `js/app.js`**

```javascript
const ORDER_STATUS_ORDER = {
  'Chưa xác nhận': ['Đã xác nhận', 'Đã giao (Huỷ đơn)'],
  'Đã xác nhận': ['Đã giao (Thành công)', 'Đã giao (Huỷ đơn)'],
  'Đã giao (Thành công)': [], // Hoàn tất, không được cập nhật ngược
  'Đã giao (Huỷ đơn)': []     // Hoàn tất, không được cập nhật ngược
};

let currentOrderEditingBtn = null;
let currentOrderIdForStatus = '';

function openOrderStatusModal(orderId, currentStatus, btn) {
  currentOrderIdForStatus = orderId;
  currentOrderEditingBtn = btn;
  
  const idEl = document.getElementById('status-modal-order-id');
  const badgeEl = document.getElementById('status-modal-current-badge');
  const selectEl = document.getElementById('select-next-status');
  
  if (idEl) idEl.textContent = '#' + orderId;
  if (badgeEl) badgeEl.textContent = currentStatus;
  
  const allowedNext = ORDER_STATUS_ORDER[currentStatus] || [];
  if (selectEl) {
    selectEl.innerHTML = '';
    if (allowedNext.length === 0) {
      selectEl.innerHTML = '<option value="">(Đơn hàng đã hoàn tất - Không thể cập nhật ngược)</option>';
      selectEl.disabled = true;
    } else {
      selectEl.disabled = false;
      allowedNext.forEach(st => {
        const opt = document.createElement('option');
        opt.value = st;
        opt.textContent = '➔ ' + st;
        selectEl.appendChild(opt);
      });
    }
  }
  openAdminModal('modal-order-status');
}

function saveOrderStatus() {
  const selectEl = document.getElementById('select-next-status');
  if (!selectEl || selectEl.disabled || !selectEl.value) {
    showToast('Không thể cập nhật! Trạng thái đơn hàng chỉ có thể cập nhật xuôi, không cho phép cập nhật ngược.', 'warning');
    closeAdminModal('modal-order-status');
    return;
  }
  const nextStatus = selectEl.value;
  if (currentOrderEditingBtn) {
    const row = currentOrderEditingBtn.closest('tr');
    if (row && row.cells[4]) {
      const isSuccess = nextStatus.includes('Thành công');
      const isCancel = nextStatus.includes('Huỷ');
      const badgeClass = isSuccess ? 'success' : (isCancel ? 'danger' : 'warning');
      row.cells[4].innerHTML = '<span class="badge-status ' + badgeClass + '">' + nextStatus.toUpperCase() + '</span>';
      currentOrderEditingBtn.setAttribute('onclick', `openOrderStatusModal('${currentOrderIdForStatus}', '${nextStatus}', this)`);
    }
  }
  showToast('Đã cập nhật trạng thái đơn hàng #' + currentOrderIdForStatus + ' thành "' + nextStatus + '" (Quy tắc một chiều)!', 'success');
  closeAdminModal('modal-order-status');
}
```

- [ ] **Step 4: Cập nhật hàm lọc đơn hàng mô phỏng thông báo Toast trong `js/app.js`**

Đảm bảo đúng yêu cầu của user:
```javascript
function applyAdminOrderFilter() {
  const statusEl = document.getElementById('filter-order-status');
  const status = statusEl ? statusEl.options[statusEl.selectedIndex].text : 'Tất cả';
  const fromEl = document.getElementById('filter-order-date-from');
  const toEl = document.getElementById('filter-order-date-to');
  const from = fromEl ? fromEl.value : '';
  const to = toEl ? toEl.value : '';
  const locEl = document.getElementById('filter-order-location');
  const loc = locEl ? locEl.options[locEl.selectedIndex].text : 'Tất cả';
  const kwEl = document.getElementById('filter-order-keyword');
  const kw = (kwEl ? kwEl.value : '').trim();

  let msg = 'Đã áp dụng bộ lọc đơn hàng: [' + status + '] | Khu vực: [' + loc + ']';
  if (from && to) msg += ' | Từ: ' + from + ' đến ' + to;
  if (kw) msg += ' | Từ khóa: "' + kw + '"';
  msg += ' (Mô phỏng giao diện)';
  
  showToast(msg, 'success');
}
```

- [ ] **Step 5: Chạy kiểm thử tự động xác nhận tiêu chí Đơn hàng**

Run: `python scripts/verify_admin_ui_mockup.py`
Expected: Check 8 & Check 9 chuyển sang PASS.

- [ ] **Step 6: Commit cục bộ**

```bash
git add admin/orders.html js/app.js
git commit -m "feat(admin): implement unidirectional order workflow and mock filter toast"
```

---

### Task 7: Triển Khai Thống Kê Top 5 Khách Hàng Chi Tiêu Cao Nhất Kèm Link Chi Tiết Đơn (`admin/customers.html`)

**Files:**
- Modify: `admin/customers.html`
- Modify: `js/app.js`

**Interfaces:**
- Consumes: Bảng thống kê và dữ liệu chi tiêu khách hàng.
- Produces: Bảng hiển thị đúng **Top 5 khách hàng có mức chi tiêu cao nhất** sắp xếp giảm dần theo tổng tiền mua; mỗi khách hàng có danh sách từng đơn hàng kèm link bấm xem chi tiết đơn hàng qua modal `#modal-order-detail`.

- [ ] **Step 1: Cập nhật cấu trúc bảng Top 5 trong `admin/customers.html`**

Thay thế bảng 6 khách thành bảng Top 5 chuẩn, thêm cột danh sách các đơn hàng có link mở chi tiết:
```html
<div class="admin-section-header">
  <h2 class="admin-section-title"><i class="fas fa-trophy" style="color: var(--accent-gold);"></i> TOP 5 KHÁCH HÀNG CÓ MỨC CHI TIÊU CAO NHẤT (SẮP XẾP GIẢM DẦN)</h2>
</div>

<table class="cart-table">
  <thead>
    <tr>
      <th style="width: 60px;">Hạng</th>
      <th>Khách Hàng</th>
      <th>Số Điện Thoại</th>
      <th>Danh Sách Đơn Hàng (Bấm xem chi tiết)</th>
      <th>Tổng Tiền Mua</th>
      <th>Thao Tác</th>
    </tr>
  </thead>
  <tbody>
    <!-- Top 1: Phạm Minh Tuấn -->
    <tr>
      <td><span class="badge-status" style="background: rgba(255, 204, 0, 0.2); color: #ffcc00; font-weight: 800;">#1</span></td>
      <td><strong>Phạm Minh Tuấn</strong><br><small style="color: var(--primary);">Hạng Kim Cương</small></td>
      <td>0977 888 999</td>
      <td>
        <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.82rem;">
          <div><a href="javascript:void(0)" onclick="openOrderDetailModal('EB-8804')" style="color: var(--secondary); text-decoration: underline;"><i class="fas fa-file-invoice"></i> #EB-8804</a>: 918.000đ (1 Thùng 24 Lon)</div>
          <div><a href="javascript:void(0)" onclick="openOrderDetailModal('EB-8801')" style="color: var(--secondary); text-decoration: underline;"><i class="fas fa-file-invoice"></i> #EB-8801</a>: 126.000đ (2x Monster, 2x Redbull)</div>
          <small style="color: var(--text-muted);">+ 16 đơn hàng khác trong kỳ</small>
        </div>
      </td>
      <td><strong style="color: var(--primary); font-size: 1.05rem;">15.200.000đ</strong></td>
      <td>
        <button class="btn-view-detail" style="padding: 4px 10px; font-size: 0.8rem;" onclick="openCustomerDetailModal('tuan')"><i class="fas fa-id-card"></i> Hồ Sơ</button>
      </td>
    </tr>

    <!-- Top 2: Nguyễn Văn An -->
    <tr>
      <td><span class="badge-status" style="background: rgba(255, 204, 0, 0.15); color: #e6b800; font-weight: 800;">#2</span></td>
      <td><strong>Nguyễn Văn An</strong><br><small style="color: var(--primary);">Hạng Kim Cương</small></td>
      <td>0912 345 678</td>
      <td>
        <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.82rem;">
          <div><a href="javascript:void(0)" onclick="openOrderDetailModal('EB-8801')" style="color: var(--secondary); text-decoration: underline;"><i class="fas fa-file-invoice"></i> #EB-8801</a>: 126.000đ (2x Monster, 2x Redbull)</div>
          <div><a href="javascript:void(0)" onclick="openOrderDetailModal('EB-8802')" style="color: var(--secondary); text-decoration: underline;"><i class="fas fa-file-invoice"></i> #EB-8802</a>: 246.000đ (4x Ultra White, 3x Redbull)</div>
          <small style="color: var(--text-muted);">+ 13 đơn hàng khác trong kỳ</small>
        </div>
      </td>
      <td><strong style="color: var(--primary); font-size: 1.05rem;">12.400.000đ</strong></td>
      <td>
        <button class="btn-view-detail" style="padding: 4px 10px; font-size: 0.8rem;" onclick="openCustomerDetailModal('an')"><i class="fas fa-id-card"></i> Hồ Sơ</button>
      </td>
    </tr>

    <!-- Top 3: Trần Thị Bích -->
    <tr>
      <td><span class="badge-status" style="background: rgba(255, 204, 0, 0.1); color: #cca300; font-weight: 800;">#3</span></td>
      <td><strong>Trần Thị Bích</strong><br><small style="color: #ffaa00;">Hạng Vàng</small></td>
      <td>0988 765 432</td>
      <td>
        <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.82rem;">
          <div><a href="javascript:void(0)" onclick="openOrderDetailModal('EB-8802')" style="color: var(--secondary); text-decoration: underline;"><i class="fas fa-file-invoice"></i> #EB-8802</a>: 246.000đ (4x Ultra White, 3x Redbull)</div>
          <small style="color: var(--text-muted);">+ 10 đơn hàng khác trong kỳ</small>
        </div>
      </td>
      <td><strong style="color: var(--primary); font-size: 1.05rem;">9.600.000đ</strong></td>
      <td>
        <button class="btn-view-detail" style="padding: 4px 10px; font-size: 0.8rem;" onclick="openCustomerDetailModal('bich')"><i class="fas fa-id-card"></i> Hồ Sơ</button>
      </td>
    </tr>

    <!-- Top 4: Lê Hoàng Nam -->
    <tr>
      <td><span class="badge-status" style="background: rgba(255, 255, 255, 0.1); color: #FFF; font-weight: 800;">#4</span></td>
      <td><strong>Lê Hoàng Nam</strong><br><small style="color: #ffaa00;">Hạng Vàng</small></td>
      <td>0903 111 222</td>
      <td>
        <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.82rem;">
          <div><a href="javascript:void(0)" onclick="openOrderDetailModal('EB-8803')" style="color: var(--secondary); text-decoration: underline;"><i class="fas fa-file-invoice"></i> #EB-8803</a>: 40.000đ (2x Redbull Nắp Bật)</div>
          <small style="color: var(--text-muted);">+ 8 đơn hàng khác trong kỳ</small>
        </div>
      </td>
      <td><strong style="color: var(--primary); font-size: 1.05rem;">7.800.000đ</strong></td>
      <td>
        <button class="btn-view-detail" style="padding: 4px 10px; font-size: 0.8rem;" onclick="openCustomerDetailModal('nam')"><i class="fas fa-id-card"></i> Hồ Sơ</button>
      </td>
    </tr>

    <!-- Top 5: Vũ Thảo My -->
    <tr>
      <td><span class="badge-status" style="background: rgba(255, 255, 255, 0.1); color: #FFF; font-weight: 800;">#5</span></td>
      <td><strong>Vũ Thảo My</strong><br><small style="color: #a0aec0;">Hạng Bạc</small></td>
      <td>0934 555 666</td>
      <td>
        <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.82rem;">
          <div><a href="javascript:void(0)" onclick="openOrderDetailModal('EB-8805')" style="color: var(--secondary); text-decoration: underline;"><i class="fas fa-file-invoice"></i> #EB-8805</a>: 198.000đ (3x Paradise, 3x Redbull)</div>
          <small style="color: var(--text-muted);">+ 5 đơn hàng khác trong kỳ</small>
        </div>
      </td>
      <td><strong style="color: var(--primary); font-size: 1.05rem;">5.400.000đ</strong></td>
      <td>
        <button class="btn-view-detail" style="padding: 4px 10px; font-size: 0.8rem;" onclick="openCustomerDetailModal('my')"><i class="fas fa-id-card"></i> Hồ Sơ</button>
      </td>
    </tr>
  </tbody>
</table>
```

- [ ] **Step 2: Thêm Modal Xem Chi Tiết Đơn Hàng (`#modal-order-detail`) vào `admin/customers.html`**

Bảo đảm khi người dùng bấm vào các link `#EB-8804`, `#EB-8801`, `#EB-8802`... trên bảng thì popup chi tiết hóa đơn mở lên sắc nét ngay lập tức.

- [ ] **Step 3: Cập nhật hàm `applyAdminCustomerFilter` trong `js/app.js`**

```javascript
function applyAdminCustomerFilter() {
  const fromEl = document.getElementById('stat-customer-from');
  const toEl = document.getElementById('stat-customer-to');
  const from = fromEl ? fromEl.value : '2026-01-01';
  const to = toEl ? toEl.value : '2026-10-17';
  const tierEl = document.getElementById('filter-customer-tier');
  const tier = tierEl ? tierEl.options[tierEl.selectedIndex].text : 'Tất cả';

  showToast('Đã thống kê Top 5 khách hàng có mức mua cao nhất (Từ ' + from + ' đến ' + to + ') - Sắp xếp giảm dần theo tổng tiền mua!', 'success');
}
```

- [ ] **Step 4: Chạy kiểm thử tự động xác nhận tiêu chí Thống kê Top 5**

Run: `python scripts/verify_admin_ui_mockup.py`
Expected: Check 10 chuyển sang PASS. Toàn bộ 10/10 checks PASS.

- [ ] **Step 5: Commit cục bộ**

```bash
git add admin/customers.html js/app.js
git commit -m "feat(admin): implement top 5 customers statistics UI with order detail links"
```

---

### Task 8: Tổng Kiểm Tra Chéo Toàn Bộ Tiêu Chí & Hoàn Thiện

**Files:**
- Modify: `docs/superpowers/plans/2026-10-20-admin-ui-mockup.md`
- Test: `scripts/verify_admin_ui_mockup.py`
- Test: `verify_implementation.py`

**Interfaces:**
- Consumes: Toàn bộ website tĩnh.
- Produces: 100% test PASS, 0 broken link ảnh, 0 vi phạm quy tắc Git.

- [ ] **Step 1: Chạy test suite `verify_admin_ui_mockup.py`**

Run: `python scripts/verify_admin_ui_mockup.py`
Expected: 10/10 PASS với exit code 0.

- [ ] **Step 2: Chạy test suite toàn repo `verify_implementation.py`**

Run: `python verify_implementation.py`
Expected: 66/66 PASS (hoặc toàn bộ checks PASS).

- [ ] **Step 3: Kiểm tra Git status đảm bảo không sót file tạm và chỉ commit cục bộ**

Run: `git status -s`
Expected: Clean working tree.

- [ ] **Step 4: Commit tổng kết**

```bash
git commit --allow-empty -m "docs: complete admin UI mockup implementation plan adhering to SGU rubric"
```
