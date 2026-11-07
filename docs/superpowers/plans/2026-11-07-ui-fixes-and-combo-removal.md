# UI Fixes, Teacher Review Remediations & Combo Removal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Khắc phục triệt để 4 nhận xét đánh giá của giáo viên (phân loại cách xa sản phẩm, lỗi canh chỉnh sản phẩm, nút Flash sale Xem vs Chi tiết, trang tài khoản mất header), đồng thời hoàn thiện điều hướng cuộn mượt theo hãng, loại bỏ "Combo Thùng 24 lon" (giữ visual 3 lon lơ lửng) và dọn sạch dữ liệu combo trong Admin.

**Architecture:** 
- Tiếp tục tuân thủ kiến trúc Pure Static Website 100% (HTML5/CSS3/Vanilla JS, không backend, chạy hoàn hảo trên `file:///` và GitHub Pages).
- Chuẩn hóa CSS Grid và Flexbox cho toàn bộ thẻ sản phẩm để các cột, tiêu đề, thông số và nút chân thẻ thẳng hàng tăm tắp.
- Thống nhất nút xem chi tiết "Chi tiết" (thay vì so le "Xem" vs "Chi tiết").
- Thêm thanh chọn thương hiệu nhanh (Quick Brand Selector) ngay đầu danh mục sản phẩm và hoàn thiện cuộn mượt có offset 110px.
- Chuyển đổi combo banner thành Showcase Banner 100% chính hãng giữ nguyên visual 3 lon nước lơ lửng, dọn sạch dữ liệu combo trong Admin và Search suggestions.

**Tech Stack:** HTML5, CSS3, Vanilla JavaScript (ES6+), FontAwesome 6.4.0, Python 3 (verification test suites).

## Global Constraints
- Không tự ý chạy `git push` lên GitHub / remote repository.
- Giữ vững 100% tiêu chí Pure Static Website, không thêm dependency backend/server.
- Không đưa lại các ràng buộc đăng nhập/đăng ký.
- Chi tiết đơn hàng duy trì là trang HTML riêng biệt ([pages/order-detail.html](file:///e:/luyentaphe/portfolio/Web%20ban%20hang/pages/order-detail.html), [admin/order-detail.html](file:///e:/luyentaphe/portfolio/Web%20ban%20hang/admin/order-detail.html)).
- Mọi bài test tự động (`verify_rubric_coverage.py`, `verify_order_detail_pages.py`, v.v.) phải đạt 100% PASS.

---

### Task 1: Tạo Bộ Kiểm Thử Tự Động Toàn Diện Cho Các Nhận Xét & Dọn Dẹp Combo

**Files:**
- Create: `scripts/verify_ui_fixes_and_combo_removal.py`

- [ ] **Step 1: Viết script test `scripts/verify_ui_fixes_and_combo_removal.py`**
  - Kiểm tra 1: Điều hướng hãng nước trên Header có `onclick="handleNavBrandClick(event, this, '...')"` và link anchor `#brand-products`.
  - Kiểm tra 2: Cụm phân loại nhanh (Quick Brand Selector) xuất hiện ngay sát đầu danh mục sản phẩm chính.
  - Kiểm tra 3: Quy chuẩn canh chỉnh thẻ sản phẩm: `.product-title` có `min-height` cố định và `line-clamp`, `.product-specs` có `min-height`, `.product-bottom` căn đáy đồng đều.
  - Kiểm tra 4: Đồng bộ 100% nút "Chi tiết" trên Flash Sale và Danh mục sản phẩm (không còn nút nào ghi "Xem").
  - Kiểm tra 5: `pages/account.html` có đầy đủ cả Header và Footer chuẩn mực.
  - Kiểm tra 6: Trang chủ `index.html` loại bỏ từ khóa "Combo Thùng 24 lon", giữ lại visual 3 lon nước lơ lửng `.combo-cans`.
  - Kiểm tra 7: Admin (`admin/index.html`, `admin/orders.html`, `admin/inventory.html`, `admin/customers.html`) không còn tồn tại đơn hàng hoặc tùy chọn "Thùng 24 lon" / combo.
  - Kiểm tra 8: `scripts/verify_rubric_coverage.py` đạt 19/19 (10.0/10.0 Điểm).

- [ ] **Step 2: Chạy script để xác nhận trạng thái RED ban đầu**
  - Lệnh: `python scripts/verify_ui_fixes_and_combo_removal.py`
  - Kết quả mong đợi: Script báo các điểm chưa đạt trước khi sửa đổi.

---

### Task 2: Khắc Phục "Phân Loại Cách Xa Phần SP" & Cuộn Hãng Mượt Chuẩn Xác

**Files:**
- Modify: `index.html`
- Modify: `css/style.css`
- Modify: `js/app.js`

- [ ] **Step 1: Bổ sung thanh phân loại nhanh (Quick Brand Selector) ngay đầu `main-catalog-container`**
  - Đặt một dải tab chọn hãng nổi bật ngay phía trên `#monster-products` với 3 tab:
    + `[⚡ Monster Energy (4 vị)]`
    + `[🔥 Redbull Thái Lan (3 vị)]`
    + `[⚡ Sting PepsiCo (3 vị)]`
  - Đảm bảo người dùng nhìn thấy phân loại nằm sát ngay bên cạnh/phía trên phần sản phẩm hiển thị.

- [ ] **Step 2: Cập nhật hàm `handleNavBrandClick` trong `js/app.js` với tính toán offset chính xác**
  - Sử dụng:
    ```javascript
    const yOffset = -110;
    const y = targetEl.getBoundingClientRect().top + window.pageYOffset + yOffset;
    window.scrollTo({ top: y, behavior: 'smooth' });
    ```
  - Đảm bảo khi cuộn xuống, tiêu đề thương hiệu không bị thanh Sticky Header che lấp.

- [ ] **Step 3: Cập nhật thẻ `href` trên Header của `index.html` và các trang con**
  - `href="#monster-products"`
  - `href="#redbull-products"`
  - `href="#sting-products"`
  - Giúp điều hướng anchor chuẩn HTML5 và mượt mà cả khi chạy không cần JS.

---

### Task 3: Khắc Phục "Lỗi Canh Chỉnh SP" & Đồng Bộ Nút "Chi Tiết" (Flash Sale vs Danh Mục)

**Files:**
- Modify: `css/style.css`
- Modify: `index.html`

- [ ] **Step 1: Quy chuẩn CSS cho `.product-card`, `.product-title`, `.product-specs` và `.product-bottom`**
  - Trong `css/style.css`:
    ```css
    .product-title {
      font-family: var(--font-heading);
      font-size: 1.05rem;
      color: #FFF;
      margin-bottom: 8px;
      line-height: 1.35;
      min-height: 44px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    .product-specs {
      min-height: 28px;
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 12px;
    }
    .product-bottom {
      margin-top: auto;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      padding-top: 14px;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
    }
    ```

- [ ] **Step 2: Thống nhất cấu trúc nút bấm trên mọi thẻ sản phẩm trong `index.html`**
  - Cả 4 thẻ Flash Sale và 10 thẻ trong danh mục hãng (Monster, Redbull, Sting) đều sử dụng cặp nút chuẩn:
    ```html
    <div class="btn-card-group">
      <a href="pages/product-detail-*.html" class="btn-view-detail" title="Xem chi tiết lon">
        <i class="fas fa-eye"></i> Chi tiết
      </a>
      <button class="btn-add-stitch" title="Thêm vào giỏ" onclick="event.stopPropagation(); showToast(...)">
        <i class="fas fa-cart-plus"></i>
      </button>
    </div>
    ```
  - Loại bỏ hoàn toàn sự không đồng nhất giữa chữ "Xem" và "Chi tiết".

---

### Task 4: Khắc Phục "Trang Tài Khoản Mất Header" & Bổ Sung Footer Chuẩn

**Files:**
- Modify: `pages/account.html`

- [ ] **Step 1: Đồng bộ hóa toàn diện Header trên `pages/account.html`**
  - Giữ vững thanh Top bar thông báo và Header chính (Logo, Search box gợi ý lon nước tĩnh, 3 nút: Lịch sử đơn hàng, Tài khoản thành viên, Giỏ hàng 7 lon 216.000đ).
  - Đồng bộ thanh `nav-bar` 3 hãng nước: bấm vào sẽ điều hướng về `../index.html#brand-products`.

- [ ] **Step 2: Bổ sung Footer chuẩn mực vào cuối `pages/account.html`**
  - Chèn footer hoàn chỉnh (gồm Giới thiệu thương hiệu, Các dòng sản phẩm, Hệ thống trang, Thông tin liên hệ và bản quyền) giống hệt `index.html` và `orders.html`.

- [ ] **Step 3: Canh chỉnh layout `account-page-section`**
  - Đảm bảo `padding-top: 40px; padding-bottom: 60px;` cân đối, không bị dính vào sticky header hay tràn đáy.

---

### Task 5: Loại Bỏ "Combo Thùng 24 Lon", Giữ Visual 3 Lon Lơ Lửng & Dọn Sạch Combo Admin

**Files:**
- Modify: `index.html`
- Modify: `admin/index.html`
- Modify: `admin/orders.html`
- Modify: `admin/inventory.html`
- Modify: `admin/customers.html`
- Modify: `js/app.js`
- Modify: `pages/search-results.html`

- [ ] **Step 1: Chuyển đổi Banner Combo thành Showcase Banner 100% Chính Hãng trong `index.html`**
  - Giữ nguyên cấu trúc `.combo-cans` (3 lon nước Monster hồng, Monster đen phát sáng aura neon xanh và Redbull).
  - Thay đổi nội dung chữ sang **"BỘ SƯU TẬP NƯỚC TĂNG LỰC ĐỈNH CAO - 100% CHÍNH HÃNG"**.
  - Các chỉ số: `100% Chính Hãng (Nhập khẩu chính ngạch)`, `Giao Lạnh 2H (Ướp lạnh tận tay)`, `Đa Dạng Vị (10 dòng lon độc đáo)`.
  - Nút bấm: `<a href="#monster-products" class="btn btn-primary"><i class="fas fa-fire"></i> KHÁM PHÁ CÁC VỊ NƯỚC NGAY</a>`.

- [ ] **Step 2: Dọn sạch gợi ý Combo trong Ô Tìm Kiếm (`search-static-list`)**
  - Trong `index.html`, `pages/*.html`: Thay mục `Combo Thùng 24 Lon` thành `Sting Dâu Tây Đỏ Sleek 330ml` trỏ về `#sting-products`.
  - Giúp bài kiểm tra `scripts/verify_rubric_coverage.py` đạt điểm 19/19 (10.0/10.0 Điểm).

- [ ] **Step 3: Dọn sạch Combo trong toàn bộ khu vực Admin**
  - Trong `admin/index.html` & `admin/orders.html`: Đổi các dòng đơn hàng demo thành `5 Lon Monster Original + 2 Redbull Thái (216.000đ)` khớp chuẩn giỏ hàng.
  - Trong `admin/inventory.html` & `admin/index.html`: Xóa bỏ tab/nút `3. Thùng 24 lon` và input upload ảnh thùng trong Modal Thêm/Sửa sản phẩm.
  - Trong `admin/customers.html`: Đổi đơn hàng gần nhất của khách VIP thành `Bộ 7 Lon Nước Tăng Lực VIP`.
  - Trong `js/app.js`: Đổi `Combo Thùng 24 Lon Đấu Trường` trong `MOCK_ORDER_DATABASE` thành `Bộ 7 Lon Nước Tăng Lực VIP`.

---

### Task 6: Kiểm Thử Toàn Diện & Xác Nhận Đạt Chuẩn (Verification Gate)

**Files:**
- Test: `scripts/verify_ui_fixes_and_combo_removal.py`
- Test: `scripts/verify_rubric_coverage.py`
- Test: `scripts/verify_order_detail_pages.py`
- Test: `scripts/verify_header_footer_pagination.py`
- Test: `scripts/verify_cart_sync.py`
- Test: `verify_implementation.py`

- [ ] **Step 1: Chạy bộ kiểm thử mới `verify_ui_fixes_and_combo_removal.py`**
  - Xác nhận 8/8 kiểm tra đều PASS 100%.

- [ ] **Step 2: Chạy kiểm thử Rubric Đề Thi**
  - Xác nhận `verify_rubric_coverage.py` đạt trọn vẹn 19/19 Tiêu chí (10.0 / 10.0 Điểm).

- [ ] **Step 3: Chạy tất cả các test suites hồi quy**
  - Đảm bảo 100% các bộ test khác đều PASS xanh.
