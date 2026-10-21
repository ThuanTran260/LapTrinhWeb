# Kế Hoạch Triển Khai: Tinh Chỉnh Tìm Kiếm & Chuẩn Hóa Thương Hiệu Admin

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Xóa các quick tag trong search dropdown, bổ sung dropdown gợi ý tìm kiếm tức thời trong modal Tìm Kiếm Nâng Cao và chuẩn hóa thẻ thống kê 3 Brand trong trang Quản trị Admin.

**Architecture:** Sử dụng kiến trúc 100% Website Tĩnh (Vanilla HTML5, CSS3 Dark Neon Glassmorphism, JavaScript thuần chạy offline client-side). Gợi ý tìm kiếm nâng cao dựa trên mảng catalog sản phẩm tĩnh `STATIC_PRODUCTS_CATALOG` lọc theo thời gian thực khi người dùng gõ phím.

**Tech Stack:** HTML5, CSS3 (Dark Neon Theme), JavaScript (ES6 Client-side), Python (kiểm thử tự động).

## Global Constraints

- **100% Website Tĩnh**: Không sử dụng backend server hoặc cơ sở dữ liệu running; mở và chạy trực tiếp từ `index.html` trên trình duyệt Google Chrome.
- **Bảo toàn dữ liệu demo**: Không làm mất dữ liệu sản phẩm, đơn hàng, khách hàng mẫu.
- **RULE 1**: Tuyệt đối KHÔNG thực hiện `git push` lên remote repository. Chỉ commit local trên nhánh `feat/static-rubric-features`.
- **Hồi quy kiểm thử**: Duy trì 100% (66/66 checks) trong `verify_implementation.py`.

---

### Task 1: Xóa Quick Tags Trong Dropdown Tìm Kiếm Storefront

**Files:**
- Modify: `index.html` (khối `.search-quick-tags`)
- Modify: `pages/product-detail.html` (khối `.search-quick-tags`)
- Modify: `pages/product-detail-redbull.html` (khối `.search-quick-tags`)
- Modify: `pages/product-detail-sting.html` (khối `.search-quick-tags`)

**Interfaces:**
- Loại bỏ toàn bộ phần tử `<div class="search-quick-tags">...</div>` trong `.search-results-dropdown`.
- Giữ nguyên khối `<div class="search-dropdown-header">` và `<div class="search-static-list">`.

- [ ] **Step 1: Xóa khối `.search-quick-tags` trong `index.html`**
  - Xóa đoạn mã:
    ```html
    <div class="search-quick-tags">
      <a href="pages/product-detail.html" class="search-quick-tag">#MonsterOriginal</a>
      <a href="pages/product-detail-redbull.html" class="search-quick-tag">#RedbullThai</a>
      <a href="pages/product-detail-sting.html" class="search-quick-tag">#StingDau</a>
      <a href="pages/product-detail.html" class="search-quick-tag">#UltraWhite</a>
      <a href="#combo-section" class="search-quick-tag" onclick="closeSearchDropdown()">#Combo24Lon</a>
    </div>
    ```

- [ ] **Step 2: Xóa khối `.search-quick-tags` trong 3 trang chi tiết**
  - `pages/product-detail.html`: Xóa khối `.search-quick-tags`
  - `pages/product-detail-redbull.html`: Xóa khối `.search-quick-tags`
  - `pages/product-detail-sting.html`: Xóa khối `.search-quick-tags`

- [ ] **Step 3: Kiểm tra grep xác nhận không còn `.search-quick-tags` trong HTML**
  - Run: `git grep "search-quick-tags" "*.html"`
  - Expected: Không có kết quả nào trả về từ các file HTML.

- [ ] **Step 4: Chạy kiểm thử hồi quy**
  - Run: `python verify_implementation.py`
  - Expected: PASS 66/66 checks.

- [ ] **Step 5: Commit thay đổi Task 1**
  - Run:
    ```bash
    git add index.html pages/product-detail*.html
    git commit -m "feat(search): remove search quick tags from storefront dropdowns"
    ```

---

### Task 2: Triển Khai Dropdown Gợi Ý Tìm Kiếm Trong Modal Tìm Kiếm Nâng Cao

**Files:**
- Modify: `css/style.css` (bổ sung CSS `.adv-search-suggestions`, `.adv-suggestion-item`, `.adv-suggestion-thumb`...)
- Modify: `js/app.js` (bổ sung mảng `STATIC_PRODUCTS_CATALOG`, hàm `handleAdvKeywordInput`, `selectAdvSearchSuggestion`, `openAdvSuggestions`, `closeAdvSuggestions`)
- Modify: `index.html` (thêm container relative và dropdown `#adv-search-suggestions`)

**Interfaces:**
- Produces in `js/app.js`:
  - `STATIC_PRODUCTS_CATALOG`: mảng 10 object `{ id, name, brand, brandKey, price, priceKey, priceNum, image }`.
  - `handleAdvKeywordInput(inputEl)`: nhận input element, lọc theo `value` và render vào `#adv-search-suggestions`.
  - `selectAdvSearchSuggestion(index)`: điền tên lon, set giá trị select brand, set select price, update preview mẫu, đóng dropdown.
  - `closeAdvSuggestions()`: ẩn dropdown `#adv-search-suggestions`.

- [ ] **Step 1: Bổ sung CSS cho Dropdown Gợi Ý Nâng Cao trong `css/style.css`**
  - Thêm các class:
    ```css
    /* Advanced Search Suggestions Dropdown */
    .adv-search-input-wrapper {
      position: relative;
    }
    .adv-search-suggestions {
      position: absolute;
      top: calc(100% + 4px);
      left: 0;
      right: 0;
      background: rgba(14, 16, 23, 0.98);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(0, 230, 118, 0.3);
      border-radius: var(--radius-sm);
      max-height: 240px;
      overflow-y: auto;
      z-index: 1000;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
      display: none;
    }
    .adv-search-suggestions.active {
      display: block;
    }
    .adv-suggestion-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 12px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      cursor: pointer;
      transition: background 0.15s ease;
    }
    .adv-suggestion-item:last-child {
      border-bottom: none;
    }
    .adv-suggestion-item:hover {
      background: rgba(0, 230, 118, 0.12);
    }
    .adv-suggestion-left {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .adv-suggestion-thumb {
      width: 26px;
      height: 34px;
      object-fit: contain;
    }
    .adv-suggestion-name {
      font-size: 0.82rem;
      font-weight: 600;
      color: #FFF;
      margin: 0;
    }
    .adv-suggestion-brand {
      font-size: 0.72rem;
      color: var(--text-dim);
    }
    .adv-suggestion-price {
      font-size: 0.8rem;
      font-weight: 700;
      color: var(--primary);
      white-space: nowrap;
    }
    ```

- [ ] **Step 2: Bổ sung logic JavaScript trong `js/app.js`**
  - Khởi tạo danh mục `STATIC_PRODUCTS_CATALOG`:
    ```javascript
    const STATIC_PRODUCTS_CATALOG = [
      { id: 'mn-1', name: 'Monster Energy Original 355ml', brand: 'Monster Energy', brandKey: 'monster', price: '45.000đ', priceKey: '20to50', image: 'assets/images/monster/original.webp' },
      { id: 'mn-2', name: 'Monster Zero Ultra White 500ml', brand: 'Monster Energy', brandKey: 'monster', price: '48.000đ', priceKey: '20to50', image: 'assets/images/monster/ultra-white.webp' },
      { id: 'mn-3', name: 'Monster Ultra Paradise 500ml', brand: 'Monster Energy', brandKey: 'monster', price: '48.000đ', priceKey: '20to50', image: 'assets/images/monster/ultra-paradise.webp' },
      { id: 'mn-4', name: 'Monster Ultra Punk Punch 500ml', brand: 'Monster Energy', brandKey: 'monster', price: '50.000đ', priceKey: '20to50', image: 'assets/images/monster/ultra-punk-punch.webp' },
      { id: 'rb-1', name: 'Nước Tăng Lực Redbull Original 250ml', brand: 'Redbull Thái Lan', brandKey: 'redbull', price: '18.000đ', priceKey: 'under20', image: 'assets/images/redbull/redbull-original.webp' },
      { id: 'rb-2', name: 'Nước Tăng Lực Redbull Thái Lan 250ml', brand: 'Redbull Thái Lan', brandKey: 'redbull', price: '18.000đ', priceKey: 'under20', image: 'assets/images/redbull/redbull-thai.webp' },
      { id: 'rb-3', name: 'Nước Tăng Lực Redbull Nắp Bật 250ml', brand: 'Redbull Thái Lan', brandKey: 'redbull', price: '20.000đ', priceKey: '20to50', image: 'assets/images/redbull/redbull-lon-vua.webp' },
      { id: 'st-1', name: 'Nước Tăng Lực Sting Dâu Tây Đỏ 330ml', brand: 'Sting PepsiCo', brandKey: 'sting', price: '12.000đ', priceKey: 'under20', image: 'assets/images/sting/sting-dau.webp' },
      { id: 'st-2', name: 'Nước Tăng Lực Sting Vàng Sleek 330ml', brand: 'Sting PepsiCo', brandKey: 'sting', price: '12.000đ', priceKey: 'under20', image: 'assets/images/sting/sting-gold.webp' },
      { id: 'st-3', name: 'Nước Tăng Lực Sting Blue Sleek 320ml', brand: 'Sting PepsiCo', brandKey: 'sting', price: '13.000đ', priceKey: 'under20', image: 'assets/images/sting/sting-vietquat.webp' }
    ];
    ```
  - Viết các hàm:
    * `handleAdvKeywordInput(val)`: Lọc theo chuỗi `val` và render vào `#adv-search-suggestions`.
    * `selectAdvSearchSuggestion(idx)`: Điền tên lon, set giá trị cho `#adv-search-brand` và `#adv-search-price`, cập nhật preview `#adv-search-preview` và đóng dropdown.
    * `closeAdvSuggestions()`: Đóng dropdown.
    * Gắn sự kiện click outside và Escape để đóng `#adv-search-suggestions`.

- [ ] **Step 3: Cập nhật HTML Modal Tìm Kiếm Nâng Cao trong `index.html`**
  - Bọc input `#adv-search-keyword` trong `.adv-search-input-wrapper`:
    ```html
    <div class="admin-form-group full-width" style="margin-bottom: 14px;">
      <label class="admin-form-label"><i class="fas fa-search" style="color: var(--primary);"></i> Tên sản phẩm / Từ khóa</label>
      <div class="adv-search-input-wrapper">
        <input type="text" id="adv-search-keyword" class="admin-form-input" placeholder="VD: Original, Ultra, Dâu tây, Chai vàng..." value="Original" oninput="handleAdvKeywordInput(this.value)" onfocus="handleAdvKeywordInput(this.value)" autocomplete="off" />
        <div id="adv-search-suggestions" class="adv-search-suggestions"></div>
      </div>
    </div>
    ```

- [ ] **Step 4: Chạy kiểm thử hồi quy**
  - Run: `python verify_implementation.py`
  - Expected: PASS 66/66 checks.

- [ ] **Step 5: Commit thay đổi Task 2**
  - Run:
    ```bash
    git add css/style.css js/app.js index.html
    git commit -m "feat(search): add live suggestion dropdown to advanced search modal"
    ```

---

### Task 3: Chuẩn Hóa Thẻ KPI Brand & Tiêu Đề Trong Admin

**Files:**
- Modify: `admin/index.html` (Thẻ KPI Brand & Tiêu đề phụ)
- Modify: `admin/inventory.html` (Thẻ KPI Brand & Tiêu đề phụ)

**Interfaces:**
- Cập nhật số đếm từ `2 Brand` thành `3 Brand`.
- Cập nhật dòng chữ mô tả dưới số thành `<p>Thương hiệu</p>`.
- Cập nhật phụ đề thành `3 Thương hiệu chính thức`.

- [ ] **Step 1: Cập nhật `admin/index.html`**
  - Sửa phụ đề topbar:
    ```html
    <p style="font-size: 0.85rem; color: var(--text-muted);">Cập nhật dữ liệu thời gian thực - 3 Thương hiệu chính thức</p>
    ```
  - Sửa thẻ KPI Brand:
    ```html
    <div class="kpi-card">
      <div class="kpi-icon cyan"><i class="fas fa-warehouse"></i></div>
      <div class="kpi-info">
        <h3>3 Brand</h3>
        <p>Thương hiệu</p>
      </div>
    </div>
    ```

- [ ] **Step 2: Cập nhật `admin/inventory.html`**
  - Sửa phụ đề topbar:
    ```html
    <p style="font-size: 0.85rem; color: var(--text-muted);">3 Thương hiệu lớn (Monster, Redbull & Sting) - Sẵn sàng xuất kho</p>
    ```

- [ ] **Step 3: Kiểm tra grep xác nhận không còn `Monster Energy & Redbull` trong thẻ KPI**
  - Run: `git grep "Monster Energy & Redbull" admin/`
  - Expected: Không còn kết quả nào trong thẻ KPI.

- [ ] **Step 4: Chạy kiểm thử hồi quy**
  - Run: `python verify_implementation.py`
  - Expected: PASS 66/66 checks.

- [ ] **Step 5: Commit thay đổi Task 3**
  - Run:
    ```bash
    git add admin/index.html admin/inventory.html
    git commit -m "fix(admin): standardize brand KPI card to 3 brands with clean label"
    ```

---

### Task 4: Kiểm Thử Toàn Diện & Nghiệm Thu

**Files:**
- Test script: `scratch/verify_search_refinements.py`

- [ ] **Step 1: Viết test script kiểm tra toàn bộ 3 yêu cầu mới**
  - Kiểm tra không còn `.search-quick-tags` trong 4 file storefront HTML.
  - Kiểm tra tồn tại `.adv-search-suggestions` và hàm `handleAdvKeywordInput`, `selectAdvSearchSuggestion`.
  - Kiểm tra `<h3>3 Brand</h3>` và `<p>Thương hiệu</p>` trong `admin/index.html`.

- [ ] **Step 2: Chạy test script**
  - Run: `python scratch/verify_search_refinements.py`
  - Expected: 100% assertions PASS.

- [ ] **Step 3: Chạy lại `verify_implementation.py`**
  - Run: `python verify_implementation.py`
  - Expected: PASS 66/66 checks.

- [ ] **Step 4: Dọn dẹp scratch file và kiểm tra git status**
  - Run: `git status`
  - Expected: Working tree clean, không có file thừa.
