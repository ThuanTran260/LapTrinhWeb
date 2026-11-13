# Thiết Kế: Nút Xóa Câu Hỏi FAQ Admin Chỉ Hiển Thị Thông Báo (Không Xóa DOM)

**Ngày:** 14/11/2026  
**Trạng thái:** Pending User Approval  
**Tác giả:** Antigravity  

---

## 1. Bối cảnh & Mục tiêu

- **Hiện trạng:**
  - Trong trang Quản lý Cài đặt Admin (`admin/settings.html`), phân vùng **QUẢN LÝ CÂU HỎI THƯỜNG GẶP (FAQ)** có nút xóa (icon thùng rác `fa-trash`) gọi hàm `handleAdminDeleteFaq(btn, id)`.
  - Hàm này hiện đang thực hiện `item.remove()`, tức là thực sự xóa phần tử câu hỏi FAQ khỏi DOM hiển thị.
- **Vấn đề & Yêu cầu của người dùng:**
  - Người dùng yêu cầu: *"khi bấm vô nút xoá chỉ hiện thông báo"*.
  - Điều này đồng bộ tuyệt đối với triết lý thiết kế và quy tắc dự án trong hệ thống Storefront/Admin (tương tự như `handleAdminDeleteProduct` ở dòng 2721 trong `js/app.js`: *"Quy tắc dự án: Khi xóa chỉ cần thông báo chứ không thực sự xóa hay ẩn (DOM giữ nguyên)"*).
- **Mục tiêu:**
  - Tinh chỉnh hàm `handleAdminDeleteFaq(btn, id)` trong `js/app.js` để **chỉ gọi `showToast`** thông báo, tuyệt đối **không gọi `item.remove()`** hoặc ẩn phần tử trong DOM.
  - Cập nhật test suite `scripts/verify_admin_features_update.py` để xác nhận hành vi DOM giữ nguyên sau khi nhấn xóa.

---

## 2. Chi Tiết Kỹ Thuật

### 2.1. Cập nhật `js/app.js` (Hàm `handleAdminDeleteFaq`)
- **Trước thay đổi:**
  ```javascript
  function handleAdminDeleteFaq(btn, id) {
    if (btn) {
      const item = btn.closest('.faq-admin-item');
      if (item) {
        item.remove();
      }
    }
    showToast(`Đã xóa câu hỏi FAQ #${id} thành công!`, 'success');
  }
  ```
- **Sau thay đổi:**
  ```javascript
  function handleAdminDeleteFaq(btn, id) {
    // Quy tắc dự án: Khi xóa chỉ hiển thị thông báo toast chứ không thực sự xóa khỏi DOM
    const cleanId = String(id).replace(/[^0-9]/g, '').trim() || String(id);
    showToast(`Đã xóa câu hỏi FAQ #${cleanId} khỏi danh sách hiển thị!`, 'info');
  }
  ```

### 2.2. Cập nhật test kiểm thử `scripts/verify_admin_features_update.py`
- Thay thế kiểm tra `okFaqDel = (faqList.children.length === 0)` thành:
  ```javascript
  // 6. Test FAQ delete: chỉ hiện thông báo, DOM vẫn giữ nguyên phần tử
  const countBefore = faqList.children.length;
  handleAdminDeleteFaq(item5, '5');
  const countAfter = faqList.children.length;
  const okFaqDel = (countBefore === countAfter && countAfter > 0 && lastToastMessage.includes('FAQ #5'));
  ```

---

## 3. Tiêu Chí Nghiệm Thu & Kiểm Thử

1. Bấm nút xóa trên bất kỳ câu hỏi FAQ nào (FAQ #1, #2, #3, #4 hoặc FAQ mới thêm) đều kích hoạt thông báo Toast:
   `"Đã xóa câu hỏi FAQ #{id} khỏi danh sách hiển thị!"`.
2. Phần tử FAQ vẫn hiển thị nguyên vẹn trên màn hình (DOM không bị xóa hoặc mất đi).
3. 100% test suite đạt PASS:
   - `python scripts/verify_admin_features_update.py` (51/51 PASS).
   - `python verify_implementation.py` (66/66 PASS).
   - `python scripts/verify_footer_sync.py` (144/144 PASS).
   - `python scripts/verify_price_formatting.py` (49/49 PASS).
   - Toàn bộ các script khác trong `scripts/` giữ vững 100% PASS.
