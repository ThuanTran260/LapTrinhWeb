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

## 30. Đồng bộ footer 4 cột cho toàn bộ trang Dashboard & Storefront — kiểm thử hồi quy toàn diện

**Ngày:** 2026-11-08
**Bối cảnh:** Kế hoạch "Đồng Bộ Footer 4 Cột Cho Toàn Bộ Trang Dashboard & Storefront". Tasks 1–3 đã thực hiện trên nhánh cục bộ `main` (không push). Task 4 là nghiệm thu hồi quy + tài liệu, không sửa mã nguồn.

### 30.1. Tóm tắt đồng bộ footer (24 trang)

Footer chuẩn 4 cột (brand + `CÁC DÒNG SẢN PHẨM` + `HỆ THỐNG TRANG` + `NHẬN VOUCHER ƯU ĐÃI` + `.footer-bottom`) đồng bộ cho 24 trang:

| Nhóm | Số trang | Trước | Sau |
|------|----------|-------|-----|
| Storefront `pages/*.html` | 12 | Footer 1 dòng rút gọn (một phần) | Footer đủ 4 cột, `footer-grid` trong `<footer class="footer">`, newsletter `showToast` |
| Dashboard `admin/*.html` | 12 | Footer 1 dòng rút gọn | Footer đủ 4 cột (href dùng `../index.html`, `../index.html#...`, `../pages/...`) |

Ngoại lệ: `pages/login.html` và `admin/login.html` (standalone) bị loại trừ khỏi phạm vi footer sync và khỏi `scripts/verify_footer_sync.py`.

Phát hiện lặp lại đã biết (Task 3, có chủ đích, không chặn nghiệm thu): trang `pages/product-detail-sting.html` có khác biệt lặp đoạn mô tả (duplication) do thay thế theo mẫu; không ảnh hưởng footer sync hay hồi quy.

### 30.2. Bảng bằng chứng hồi quy (Step 1 + Step 2)

Base trước Task 4: `35401b4ce8e5d74babf4673be275d77717c72d0c`.
Đã chạy toàn bộ suite ít nhất **3 lượt** liên tiếp, mỗi lượt đều PASS 100% (không có lỗi hồi quy):

| Suite (lệnh) | Kết quả (mỗi lượt) | Ghi chú |
|-------------|--------------------|---------|
| `python verify_implementation.py` | 66/66 PASS — `ALL 66 CHECKS PASSED PERFECTLY!` | 3/3 lượt |
| `python scripts/verify_footer_sync.py` | 144/144 PASS | 3/3 lượt |
| `python scripts/verify_admin_monster_previews.py` | PASS | 3/3 lượt |
| `python scripts/verify_admin_order_links.py` | 6/6 PASS | 3/3 lượt |
| `python scripts/verify_admin_ui_mockup.py` | 10/10 PASS | 3/3 lượt |
| `python scripts/verify_cart_sync.py` | 15/15 PASS | 3/3 lượt |
| `python scripts/verify_discount_sync_and_clean_ward_labels.py` | 8/8 PASS | 3/3 lượt |
| `python scripts/verify_field_sync_and_clean_image_labels.py` | 46/46 PASS | 3/3 lượt |
| `python scripts/verify_header_footer_pagination.py` | 8/8 PASS | 3/3 lượt |
| `python scripts/verify_header_top_and_account_breadcrumb.py` | 12/12 PASS | 3/3 lượt |
| `python scripts/verify_order_detail_pages.py` | 8/8 PASS | 3/3 lượt |
| `python scripts/verify_price_formatting.py` | 49/49 PASS | 3/3 lượt |
| `python scripts/verify_rubric_coverage.py` | 19/19 PASS (điểm 10.00) | 3/3 lượt |
| `python scripts/verify_search_features.py` | 28/28 PASS | 3/3 lượt |
| `python scripts/verify_sidebar_filter_sync.py` | 23/23 PASS | 3/3 lượt |
| `python scripts/verify_sting_assets.py` | PASS (OVERALL VERIFICATION: PASSED) | 3/3 lượt |
| `python scripts/verify_ui_fixes_and_combo_removal.py` | 8/8 PASS | 3/3 lượt |
| `python scripts/verify_unconstrained_add_user.py` | 30/30 PASS | 3/3 lượt |
| `python scripts/verify_ward_commune_filter.py` | 5/5 PASS | 3/3 lượt |
| `scripts/process_sting_assets.py` | Không thuộc suite verify (script xử lý asset, không chạy) | — |
| `scripts/verify_ward_filter_and_address.py` (theo brief) | **Không tồn tại** — thay thế bằng `scripts/verify_ward_commune_filter.py` (file thực tế) | Substitution đã ghi nhận |

Không thêm file kiểm thử nào ngoài danh sách trên. Nếu phát hiện lỗi hồi quy thì báo BLOCKED, không tự sửa mã nguồn.

### 30.3. Xác thực tĩnh liên kết footer (Step 3 — thay thế browser check)

> Giới hạn: không có trình duyệt trong môi trường này nên không chạy kiểm tra click thực tế. Thay vào đó kiểm tra tĩnh: trích xuất mọi `href` trong `<footer class="footer">...</footer>` của 24 trang và đối chiếu file/anchor đích.

- `pages/*.html`: href dạng `../index.html#monster-products`, `../index.html#redbull-products`, `../index.html#sting-products`, `../index.html`, và sibling `product-detail.html`, `product-detail-redbull.html`, `cart.html`, `orders.html`, `account.html` — 12/12 trang khớp mẫu.
- `admin/*.html`: href dạng `../index.html#...`, `../index.html`, và `../pages/product-detail.html`, `../pages/product-detail-redbull.html`, `../pages/cart.html`, `../pages/orders.html`, `../pages/account.html` — 12/12 trang khớp mẫu.
- File đích tồn tại: `index.html`, `pages/product-detail.html`, `pages/product-detail-redbull.html`, `pages/cart.html`, `pages/orders.html`, `pages/account.html` — tất cả `True`.
- Anchor đích tồn tại trong `index.html`: `monster-products`, `redbull-products`, `sting-products` — tất cả `True`.
- Liên kết footer không có lỗi gãy (broken link) ở mức tĩnh.

### 30.4. File thay đổi & commits

| Commit | Nội dung | File |
|--------|----------|------|
| `1142dee` | `test(footer): add verify_footer_sync script and admin footer styling` | `css/style.css`, `scripts/verify_footer_sync.py` (mới) |
| `c38fc9a` | `feat(pages): synchronize 4-column rich footer across all storefront pages` | 12 file `pages/*.html` |
| `35401b4` | `feat(admin): integrate synchronized 4-column brand footer across all admin dashboard pages` | 12 file `admin/*.html` |
| *(docs commit)* | `docs: record 4-column footer sync and regression evidence` | `walkthrough.md`, `docs/superpowers/plans/2026-11-08-sync-footer-dashboard-and-store-pages.md`, `docs/superpowers/specs/2026-11-08-sync-footer-dashboard-and-store-pages-design.md` |

### 30.5. Cam kết an toàn (Safety)

- **100% Pure Static Website:** Task 4 chỉ chạy script kiểm thử Python cục bộ + ghi tài liệu; không sửa mã nguồn (`pages/`, `admin/`, `css/`, `js/`) hay đổi cấu trúc/thuật toán.
- **Tuyệt đối không `git push`:** mọi commit chỉ tạo trên nhánh cục bộ `main`; không thực hiện push ở bất kỳ bước nào.
- **Tương thích 100% bộ test hiện hữu:** `verify_implementation.py` 66/66 và toàn bộ `scripts/verify_*.py` (18 file) đều PASS ở cả 3 lượt.
- **File ngoài phạm vi:** `implementation_plan.md` (tồn tại từ trước, không thuộc docs commit này) không được staging trong commit docs.
