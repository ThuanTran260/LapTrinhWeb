# Kế Hoạch Tinh Giản Thành Web Tĩnh Tối Thiểu (Static Web)

Dựa trên các quyết định đã thống nhất qua quá trình trao đổi (/grill-me), trang web sẽ được tinh giản xuống đúng chuẩn **Web Tĩnh (Static Website)** dành cho bài tập/dự án thuần HTML/CSS:
- Loại bỏ toàn bộ logic JS phức tạp (hệ thống giỏ hàng, mã giảm giá, lưu localStorage, danh sách yêu thích, gợi ý tìm kiếm, bộ lọc động).
- Chuyển toàn bộ thẻ sản phẩm về **mã HTML tĩnh thuần túy** nằm trực tiếp trong file `index.html`.
- Tính năng duy nhất khi click vào ảnh sản phẩm là: **Mở Lightbox phóng to duy nhất 1 bức ảnh đó** ở giữa màn hình với nền mờ và nút Đóng (X).
- JavaScript được giảm xuống mức tối thiểu (~15-20 dòng code để điều khiển Lightbox và chuyển banner).

---

## Các Thay Đổi Sẽ Thực Hiện:

### 1. File HTML: `index.html`
- **Header**:
  - Giữ lại Logo và thanh tìm kiếm tĩnh (form input HTML cơ bản, không có JS autocomplete).
  - Loại bỏ nút mở Giỏ hàng Drawer và badge đếm yêu thích/giỏ hàng.
- **Hero Banner**:
  - Giữ lại giao diện banner đẹp mắt.
- **Section Flash Sale & Sản Phẩm**:
  - Chuyển toàn bộ danh sách sản phẩm (LEGO, Hot Wheels, Barbie, STEM...) thành các thẻ HTML tĩnh có cấu trúc semantic rõ ràng (`<article class="product-card">`).
  - Mỗi ảnh sản phẩm được gắn sự kiện `onclick="openLightbox(this.src, this.alt)"` để khi click sẽ phóng to ảnh.
  - Bỏ nút "Thêm vào giỏ", thay bằng giao diện tĩnh đơn giản.
- **Lightbox Modal đơn giản**:
  - Thay thế Quick View Modal phức tạp trước đây bằng 1 khung Lightbox đơn giản duy nhất:
    ```html
    <div id="image-lightbox" class="lightbox-overlay" onclick="closeLightbox()">
      <div class="lightbox-content" onclick="event.stopPropagation()">
        <button class="lightbox-close" onclick="closeLightbox()">&times;</button>
        <img id="lightbox-img" src="" alt="" />
        <p id="lightbox-caption"></p>
      </div>
    </div>
    ```
- **Xóa bỏ**:
  - Gỡ bỏ toàn bộ phần `cart-drawer`, `cart-overlay`, và `toast-container`.
  - Gỡ bỏ thẻ `<script src="js/products.js"></script>`.

### 2. File JavaScript: `js/app.js` & Xóa `js/products.js`
- Xóa bỏ file `js/products.js`.
- Viết lại file `js/app.js` tối giản chỉ còn khoảng 15-20 dòng:
  - Hàm `openLightbox(src, caption)`: Gán ảnh vào modal và hiển thị.
  - Hàm `closeLightbox()`: Ẩn modal.
  - Chuyển banner hero đơn giản.
  - Không có localStorage, không có state giỏ hàng, không có logic tính tiền hay filter.

### 3. File CSS: `css/style.css`
- Tinh giản bỏ style của Quick View modal và Cart drawer.
- Thêm style nhẹ nhàng, gọn đẹp cho Lightbox phóng to duy nhất 1 ảnh.
- Giữ nguyên giao diện đẹp, rực rỡ phong cách MyKingdom cho toàn bộ trang web.
