# Walkthrough — Đồng bộ Top Bar Đơn Hàng & Breadcrumb Tài Khoản

**Ngày:** 2026-11-08
**Bối cảnh:** Kế hoạch "Đồng bộ Top Bar Đơn Hàng & Breadcrumb Tài Khoản" (Phương án 1 — đồng bộ nhóm điều hướng trên, không đụng banner chính).
Kế hoạch được thực hiện trong 3 task trên nhánh cục bộ `main`, không push.

**Mục tiêu:**
- `pages/orders.html`: đồng bộ thanh top-bar 3 links → 6 links, khớp với nhóm điều hướng trang dashboard (`index.html`).
- `pages/account.html`: thay thanh điều hướng danh mục thương hiệu (nav-bar: Monster / Redbull / Sting) bằng breadcrumb thành viên (`Trang chủ / Thành viên`).
- Kiểm thử mới `scripts/verify_header_top_and_account_breadcrumb.py` + hồi quy toàn bộ 15 test suites đạt PASS 100%.

## 27. Thay đổi trước/sau (Before/After)

### 27.1. `pages/orders.html` — top-bar 3 links → 6 links

**Trước (3 links):**

| # | Nhãn | href |
|---|------|------|
| 1 | Tiếp Tục Mua Sắm | `../index.html` |
| 2 | Giỏ Hàng (7 lon) | `cart.html` |
| 3 | Tài Khoản | `account.html` |

**Sau (6 links — khớp dashboard):**

| # | Nhãn | href |
|---|------|------|
| 1 | Tiếp Tục Mua Sắm | `../index.html` |
| 2 | **Giao 2H Hoả Tốc** *(mới)* | `../index.html#features` |
| 3 | **Lịch Sử Đặt Hàng** *(mới)* | `orders.html` |
| 4 | Giỏ Hàng (7 lon) | `cart.html` |
| 5 | Tài Khoản | `account.html` |
| 6 | **Đăng Nhập** *(mới)* | `login.html` |

**Diff (commit `55cbf6f`):**
```diff
       <div class="top-links">
         <a href="../index.html"><i class="fas fa-arrow-left"></i> Tiếp Tục Mua Sắm</a>
+        <a href="../index.html#features"><i class="fas fa-truck-fast"></i> Giao 2H Hoả Tốc</a>
+        <a href="orders.html"><i class="fas fa-clock-rotate-left"></i> Lịch Sử Đặt Hàng</a>
         <a href="cart.html"><i class="fas fa-shopping-cart"></i> Giỏ Hàng (7 lon)</a>
         <a href="account.html"><i class="fas fa-user-circle"></i> Tài Khoản</a>
+        <a href="login.html"><i class="fas fa-sign-in-alt"></i> Đăng Nhập</a>
       </div>
```

### 27.2. `pages/account.html` — nav-bar danh mục → breadcrumb thành viên

**Trước:** một `<nav class="nav-bar">` với 3 hạng mục thương hiệu dùng `javascript:void(0)` + `handleNavBrandClick(event, this)`:
- Monster (`fa-bolt`, `var(--primary)`)
- Redbull (`fa-fire`, `var(--secondary)`)
- Sting (`fa-bolt`, `#FF0055`)

**Sau:** nav-bar bị loại bỏ hoàn toàn, thay bằng breadcrumb trong `main`:

```html
<main class="container account-page-section" style="padding-top: 24px; padding-bottom: 40px;">
  <div class="breadcrumb">
    <a href="../index.html">Trang chủ</a>
    <span>/</span>
    <span>Thành viên</span>
  </div>
```

**Diff tóm tắt (commit `fc4b197`):** −12 dòng nav-bar, +6 dòng breadcrumb; `padding-top` của `account-page-section` đổi 32px → 24px (breadcrumb chiếm không gian thay cho nav-bar).

### 27.3. File thay đổi & commits

| Commit | Nội dung | File |
|--------|----------|------|
| `55cbf6f` | `feat(orders): synchronize top-bar navigation with dashboard catalog` | `pages/orders.html`, `scripts/verify_header_top_and_account_breadcrumb.py` (mới) |
| `fc4b197` | `feat(account): replace brand category navbar with member breadcrumb` | `pages/account.html` |
| *(docs commit)* | `docs: document header top sync and account breadcrumb specs and plans` | `walkthrough.md`, `docs/superpowers/plans/2026-11-08-header-top-sync-and-account-breadcrumb.md`, `docs/superpowers/specs/2026-11-08-header-top-sync-and-account-breadcrumb-design.md` |

## 28. Bằng chứng kiểm thử & cam kết an toàn

### 28.1. Hồi quy 15 test suites (Step 1 — đã chạy trước khi viết tài liệu)

Lệnh chạy (PowerShell, đúng như brief):
```powershell
python -c "
import subprocess
scripts = [
    'scripts/verify_header_top_and_account_breadcrumb.py',
    'scripts/verify_sidebar_filter_sync.py',
    'scripts/verify_discount_sync_and_clean_ward_labels.py',
    'scripts/verify_ward_commune_filter.py',
    'scripts/verify_search_features.py',
    'scripts/verify_ui_fixes_and_combo_removal.py',
    'scripts/verify_rubric_coverage.py',
    'scripts/verify_price_formatting.py',
    'scripts/verify_admin_order_links.py',
    'scripts/verify_order_detail_pages.py',
    'scripts/verify_field_sync_and_clean_image_labels.py',
    'scripts/verify_cart_sync.py',
    'verify_implementation.py',
    'scripts/verify_admin_monster_previews.py',
    'scripts/verify_unconstrained_add_user.py'
]
for s in scripts:
    res = subprocess.run(['python', s], capture_output=True, text=True, encoding='utf-8')
    assert res.returncode == 0, f'FAILED: {s}\n{res.stdout}\n{res.stderr}'
    print(f'[OK] {s}')
print('ALL 15 SUITES PASSED (100%)!')
"
```

**Output đầy đủ:**
```
[OK] scripts/verify_header_top_and_account_breadcrumb.py
[OK] scripts/verify_sidebar_filter_sync.py
[OK] scripts/verify_discount_sync_and_clean_ward_labels.py
[OK] scripts/verify_ward_commune_filter.py
[OK] scripts/verify_search_features.py
[OK] scripts/verify_ui_fixes_and_combo_removal.py
[OK] scripts/verify_rubric_coverage.py
[OK] scripts/verify_price_formatting.py
[OK] scripts/verify_admin_order_links.py
[OK] scripts/verify_order_detail_pages.py
[OK] scripts/verify_field_sync_and_clean_image_labels.py
[OK] scripts/verify_cart_sync.py
[OK] verify_implementation.py
[OK] scripts/verify_admin_monster_previews.py
[OK] scripts/verify_unconstrained_add_user.py
ALL 15 SUITES PASSED (100%)!
```

**Kết quả: ALL 15 SUITES PASSED (100%)!**

### 28.2. Output tập trung — kiểm thử mới 10/10

```
=== VERIFY HEADER TOP SYNC & ACCOUNT BREADCRUMB ===
[PASS] orders.html has top-links - Found .top-links container
[PASS] orders.html has Tiếp Tục Mua Sắm -
[PASS] orders.html has Giao 2H Hoả Tốc -
[PASS] orders.html has Lịch Sử Đặt Hàng -
[PASS] orders.html has Giỏ Hàng (7 lon) -
[PASS] orders.html has Tài Khoản -
[PASS] orders.html has Đăng Nhập -
[PASS] account.html removes nav-bar -
[PASS] account.html has breadcrumb -
[PASS] account.html breadcrumb structure -

Result: 10/10 passed.
ALL CHECKS PASSED!
```

### 28.3. Output tập trung — đồng bộ giỏ hàng 15/15 (tương thích)

```
=== VERIFY CART DATA SYNCHRONIZATION (7 LON & 216.000đ) ===
[PASS] cart.html header quantity - Header should say 7 LON
[PASS] cart.html header price - Header should say 216.000đ, not 210.600đ
[PASS] cart.html summary quantity - Summary should say 7 lon
[PASS] cart.html summary total - Total should be 216.000đ
[PASS] index.html header badge - Cart badge in header should be 7
[PASS] index.html header price - Cart price in header should be 216.000đ
[PASS] index.html view cart button removed - Dashboard should not have redundant view cart button
[PASS] product-detail.html badge - Cart badge should be 7
[PASS] product-detail-redbull.html badge - Cart badge should be 7
[PASS] product-detail-redbull-lonvua.html badge - Cart badge should be 7
[PASS] product-detail-redbull-thai.html badge - Cart badge should be 7
[PASS] product-detail-sting.html badge - Cart badge should be 7
[PASS] orders.html cart link - Orders page cart link should say 7 lon
[PASS] order-success.html package step - Packaging step should say 7 lon
[PASS] order-success.html card title - Order summary should say 7 LON

Result: 15/15 passed.
ALL CHECKS PASSED!
```

### 28.4. Cam kết an toàn (Global Constraints) — đã tuân thủ

- **100% Pure Static Website:** chỉ sửa HTML tĩnh + script kiểm thử Python cục bộ; không có node server, backend API, hay database.
- **Giữ nguyên `"Giỏ Hàng (7 lon)"` trong `pages/orders.html`** để tương thích `scripts/verify_cart_sync.py` — xác nhận bởi check `orders.html has Giỏ Hàng (7 lon)` (PASS) và suite giỏ hàng 15/15 (PASS).
- **Tuyệt đối không `git push`:** mọi commit chỉ tạo trên nhánh cục bộ `main`; không thực hiện push ở bất kỳ bước nào.
- Task 3 chỉ tạo/sửa tài liệu (`walkthrough.md` + docs kế hoạch/đặc tả); không sửa mã nguồn (`pages/`, `scripts/`, `js/`, `css/`).

## 29. Orders top-bar về 1 dòng duy nhất giống dashboard

### 29.1. Vấn đề (Problem)

Sau khi Section 27 đồng bộ `pages/orders.html` lên 6 links (khớp dashboard `index.html`), thanh top-bar trên desktop bị xuống dòng: tổng chiều rộng ước tính ~1265px > 1200px (max-width container), vượt không gian cho phép. Announcement text và top-links không còn nằm trên cùng 1 dòng như dashboard.

Nguyên nhân: link `Giỏ Hàng (7 lon)` trong `.top-links` là thừa — header đã có nút giỏ hàng riêng (`.action-btn`) hiển thị số lượng và giá. Việc loại bỏ 1 link (6 → 5 links) tiết kiệm ~145px chiều rộng, đưa tổng về dưới giới hạn 1200px, đồng thời thêm CSS `flex-wrap: nowrap` cho desktop để đảm bảo không wrap.

### 29.2. Before/After

**Before (6 links + không có nowrap):**

| # | Nhãn | href |
|---|------|------|
| 1 | Tiếp Tục Mua Sắm | `../index.html` |
| 2 | Giao 2H Hoả Tốc | `../index.html#features` |
| 3 | Lịch Sử Đặt Hàng | `orders.html` |
| 4 | Giỏ Hàng (7 lon) | `cart.html` |
| 5 | Tài Khoản | `account.html` |
| 6 | Đăng Nhập | `login.html` |

**After (5 links — khớp 1 dòng giống dashboard):**

| # | Nhãn | href |
|---|------|------|
| 1 | Tiếp Tục Mua Sắm | `../index.html` |
| 2 | Giao 2H Hoả Tốc | `../index.html#features` |
| 3 | Lịch Sử Đặt Hàng | `orders.html` |
| 4 | Tài Khoản | `account.html` |
| 5 | Đăng Nhập | `login.html` |

Header cart action button (`pages/orders.html`, dòng 156) — link thừa bị loại khỏi `.top-links` nhưng chuỗi `"Giỏ Hàng (7 lon)"` được giữ nguyên dưới dạng `title` trên nút giỏ hàng header:

```html
<a href="cart.html" class="action-btn" title="Giỏ Hàng (7 lon)">
```

CSS desktop (`css/style.css`, media query `@media (min-width: 992px)` sau rule `.top-links`):

```css
@media (min-width: 992px) {
  .top-bar .container {
    flex-wrap: nowrap;
  }
  .announcement-text {
    white-space: nowrap;
    flex-shrink: 0;
  }
  .top-links {
    white-space: nowrap;
    gap: 14px;
    flex-shrink: 0;
  }
}
```

### 29.3. Bằng chứng kiểm thử (Verification evidence)

Hồi quy 15 test suites (PowerShell, đúng như brief Task 3):

**Output đầy đủ:**
```
[OK] scripts/verify_header_top_and_account_breadcrumb.py
[OK] scripts/verify_cart_sync.py
[OK] scripts/verify_sidebar_filter_sync.py
[OK] scripts/verify_discount_sync_and_clean_ward_labels.py
[OK] scripts/verify_ward_commune_filter.py
[OK] scripts/verify_search_features.py
[OK] scripts/verify_ui_fixes_and_combo_removal.py
[OK] scripts/verify_rubric_coverage.py
[OK] scripts/verify_price_formatting.py
[OK] scripts/verify_admin_order_links.py
[OK] scripts/verify_order_detail_pages.py
[OK] scripts/verify_field_sync_and_clean_image_labels.py
[OK] verify_implementation.py
[OK] scripts/verify_admin_monster_previews.py
[OK] scripts/verify_unconstrained_add_user.py
ALL 15 SUITES PASSED (100%)!
```

**Kết quả: ALL 15 SUITES PASSED (100%)!**

Output tập trung — kiểm thử header/breadcrumb 12/12:

```
=== VERIFY ORDERS TOPBAR SINGLE LINE & ACCOUNT BREADCRUMB ===
[PASS] orders.html has top-links - Found .top-links container
[PASS] orders.html has Tiếp Tục Mua Sắm -
[PASS] orders.html has Giao 2H Hoả Tốc -
[PASS] orders.html has Lịch Sử Đặt Hàng -
[PASS] orders.html has Tài Khoản -
[PASS] orders.html has Đăng Nhập -
[PASS] orders.html top-links has no redundant cart link - Cart link removed from top-links to fit 1 line
[PASS] orders.html retains Giỏ Hàng (7 lon) - Retains 'Giỏ Hàng (7 lon)' in header action button
[PASS] account.html removes nav-bar -
[PASS] account.html has breadcrumb -
[PASS] account.html breadcrumb structure -
[PASS] style.css has top-bar nowrap on desktop -

Result: 12/12 passed.
ALL CHECKS PASSED!
```

Output tập trung — đồng bộ giỏ hàng 15/15 (tương thích):
```
=== VERIFY CART DATA SYNCHRONIZATION (7 LON & 216.000đ) ===
[PASS] cart.html header quantity - Header should say 7 LON
[PASS] cart.html header price - Header should say 216.000đ, not 210.600đ
[PASS] cart.html summary quantity - Summary should say 7 lon
[PASS] cart.html summary total - Total should be 216.000đ
[PASS] index.html header badge - Cart badge in header should be 7
[PASS] index.html header price - Cart price in header should be 216.000đ
[PASS] index.html view cart button removed - Dashboard should not have redundant view cart button
[PASS] product-detail.html badge - Cart badge should be 7
[PASS] product-detail-redbull.html badge - Cart badge should be 7
[PASS] product-detail-redbull-lonvua.html badge - Cart badge should be 7
[PASS] product-detail-redbull-thai.html badge - Cart badge should be 7
[PASS] product-detail-sting.html badge - Cart badge should be 7
[PASS] orders.html cart link - Orders page cart link should say 7 lon
[PASS] order-success.html package step - Packaging step should say 7 lon
[PASS] order-success.html card title - Order summary should say 7 LON

Result: 15/15 passed.
ALL CHECKS PASSED!
```

### 29.4. File thay đổi & commits

| Commit | Nội dung | File |
|--------|----------|------|
| `9d831e0` | `fix(orders): streamline top-bar links to 5 items and assign title to cart action` | `pages/orders.html`, `scripts/verify_header_top_and_account_breadcrumb.py` |
| `292b851` | `test(orders): tighten topbar CSS check to scoped media-query assertion` | `scripts/verify_header_top_and_account_breadcrumb.py` |
| `67d25f4` | `style(topbar): ensure desktop top-bar remains on single line without wrapping` | `css/style.css` |
| *(docs commit)* | `docs: record orders topbar single line fix in walkthrough and plans` | `walkthrough.md`, `docs/superpowers/plans/2026-11-08-orders-topbar-single-line.md` |

### 29.5. Cam kết an toàn (Safety)

- **100% Pure Static Website:** chỉ sửa HTML tĩnh + CSS + script kiểm thử Python cục bộ; không có node server, backend API, hay database.
- **Giữ nguyên `"Giỏ Hàng (7 lon)"` trong `pages/orders.html`** (dòng 156, `title` trên nút giỏ hàng header) để tương thích `scripts/verify_cart_sync.py` — xác nhận bởi check `orders.html retains Giỏ Hàng (7 lon)` (PASS) và suite giỏ hàng 15/15 (PASS).
- **Tuyệt đối không `git push`:** mọi commit chỉ tạo trên nhánh cục bộ `main`; không thực hiện push ở bất kỳ bước nào.
- CSS `flex-wrap: nowrap` chỉ áp dụng trên desktop (`@media (min-width: 992px)`); mobile giữ hành vi wrap/flex hiện tại nên không phá vỡ bố cục nhỏ.
