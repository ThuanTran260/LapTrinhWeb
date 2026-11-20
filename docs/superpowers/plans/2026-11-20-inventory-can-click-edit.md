# Plan: Bấm Vào Lon Nước Ra Trang Chỉnh Sửa & Bỏ Nút Sửa Ở Cột Thao Tác

- **Branch:** `main`
- **Issue / Request:** Trong bảng `QUẢN LÝ KHO SẢN PHẨM ENERGY BOOST` (`admin/index.html` `#inventory-section` và `admin/inventory.html`), khi bấm vào lon nước (ảnh hoặc tên sản phẩm) chuyển thẳng tới trang chỉnh sửa (`edit-monster.html`), đồng thời bỏ nút chỉnh sửa (`.btn-view-detail` + `fa-edit`) ở cột `Thao Tác` và chỉ giữ lại nút xóa (`.cart-del-btn` + `fa-trash`).

## Global Constraints
1. **Clickable Product Can & Title (10 rows each in `admin/index.html` & `admin/inventory.html`):**
   - Column 1 (`Ảnh`): wrap `<img ... />` in `<a href="edit-monster.html" style="display: inline-block;" title="Chỉnh sửa sản phẩm">...</a>` preserving original `src`, `alt`, inline `style`, and `onerror`.
   - Column 2 (`Tên Sản Phẩm`): wrap `<strong>...</strong>` in `<a href="edit-monster.html" style="color: inherit; text-decoration: none;" title="Chỉnh sửa sản phẩm"><strong>...</strong></a>` preserving any `<br/><small ...>...</small>` subtitle outside `<a>` in `admin/inventory.html`.
2. **Column 8 (`Thao Tác` — Delete Only):**
   - Remove `<a href="edit-monster.html" class="btn-view-detail" ...><i class="fas fa-edit"></i></a>` in all 10 inventory rows.
   - Keep `<button class="cart-del-btn" style="padding: 4px 8px;" onclick="handleAdminDeleteProduct(...)"><i class="fas fa-trash"></i></button>` verbatim.
3. **Preservation:** Do NOT modify `#orders-section` in `admin/index.html`, modals (`#modal-add-product`, `#modal-edit-product`), stock quantities (`1.250 lon`, etc.), badges (`CÒN HÀNG`), header, sidebar, or footer.

## Tasks
- **Task 1 (`admin/index.html` `#inventory-section` lines 323-525):** Chuyển 10 hàng sản phẩm kho thành click ảnh/tên tới `edit-monster.html`, bỏ 10 nút chỉnh sửa ở cột `Thao Tác`, giữ nguyên 10 nút xóa.
- **Task 2 (`admin/inventory.html` lines 136-343):** Áp dụng đồng bộ cho toàn bộ 10 hàng sản phẩm trong bảng kho `admin/inventory.html`.
- **Task 3 (`scripts/verify_admin_inventory_can_links.py`):** Thêm script kiểm thử xác minh cả 2 bảng (`admin/index.html` & `admin/inventory.html`) đều bọc ảnh + tên lon nước bằng link `edit-monster.html`, 0 nút `.btn-view-detail`/`fa-edit` ở cột `Thao Tác`, giữ đủ 10 nút xóa `.cart-del-btn`, và không ảnh hưởng `#orders-section`.
