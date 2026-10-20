# Task 3 Brief: Chuẩn Hóa Thẻ KPI Brand & Tiêu Đề Trong Admin

## Mục tiêu
Khắc phục việc thiếu Sting trong bảng điều khiển và số liệu kho admin. Cập nhật thẻ KPI Brand thành `3 Brand` với dòng mô tả đơn giản là `Thương hiệu` (bỏ liệt kê tên `Monster Energy & Redbull`), và cập nhật phụ đề thành 3 thương hiệu chính thức.

## Các file cần sửa
1. `admin/index.html`
2. `admin/inventory.html`

## Yêu cầu chi tiết

### 1. `admin/index.html`
- Sửa phụ đề topbar (khoảng dòng 57):
  Từ:
  `<p style="font-size: 0.85rem; color: var(--text-muted);">Cập nhật dữ liệu thời gian thực - 2 Thương hiệu chính thức (Monster & Redbull)</p>`
  Thành:
  `<p style="font-size: 0.85rem; color: var(--text-muted);">Cập nhật dữ liệu thời gian thực - 3 Thương hiệu chính thức</p>`

- Sửa thẻ KPI Brand (khoảng dòng 93-99):
  Từ:
  ```html
        <div class="kpi-card">
          <div class="kpi-icon cyan"><i class="fas fa-warehouse"></i></div>
          <div class="kpi-info">
            <h3>2 Brand</h3>
            <p>Monster Energy & Redbull</p>
          </div>
        </div>
  ```
  Thành:
  ```html
        <div class="kpi-card">
          <div class="kpi-icon cyan"><i class="fas fa-warehouse"></i></div>
          <div class="kpi-info">
            <h3>3 Brand</h3>
            <p>Thương hiệu</p>
          </div>
        </div>
  ```

### 2. `admin/inventory.html`
- Sửa phụ đề topbar (khoảng dòng 57):
  Từ:
  `<p style="font-size: 0.85rem; color: var(--text-muted);">2 Thương hiệu lớn (Monster Energy & Redbull) - Sẵn sàng xuất kho</p>`
  Thành:
  `<p style="font-size: 0.85rem; color: var(--text-muted);">3 Thương hiệu chính thức (Monster, Redbull & Sting) - Sẵn sàng xuất kho</p>`

### 3. Kiểm tra & Commit
- Chạy `git grep "Monster Energy & Redbull" admin/` để đảm bảo không còn chuỗi này trong các thẻ thống kê.
- Chạy `python verify_implementation.py` (đảm bảo 66/66 test cases PASS).
- Commit:
  `git add admin/index.html admin/inventory.html`
  `git commit -m "fix(admin): standardize brand KPI card to 3 brands with clean label"`
  (TUYỆT ĐỐI KHÔNG CHẠY GIT PUSH - RULE 1).
- Ghi báo cáo vào:
  `d:\LapTrinhWeb\.superpowers\sdd\2026-10-20-search-refinements-and-admin-brand\task-3-report.md`
