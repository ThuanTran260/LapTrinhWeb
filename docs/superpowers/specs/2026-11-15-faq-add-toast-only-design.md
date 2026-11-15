# Thiết Kế: Nút Thêm Câu Hỏi FAQ Mới Chỉ Hiện Thông Báo (Giữ Nguyên DOM & Form)

**Ngày:** 15/11/2026  
**Trạng thái:** Chờ User phê duyệt kế hoạch  
**Tác giả:** Antigravity  

---

## 1. Bối cảnh & Mục tiêu

Người dùng yêu cầu:
> "phần faq khi bấm nút thêm câu hỏi mới tôi chỉ muốn hiện thông báo thôi"

Hiện tại:
- Nút **"Xóa"** FAQ (`handleAdminDeleteFaq`): Chỉ hiển thị thông báo Toast thành công, giữ nguyên DOM.
- Nút **"Chỉnh sửa"** FAQ (`handleAdminEditFaq`): Chỉ hiển thị thông báo Toast `"Đã chuyển đến câu hỏi FAQ #[id]"`, không can thiệp form trên.
- Nút **"Lưu Thay Đổi"** FAQ (`handleAdminSaveFaq`): Chỉ hiển thị thông báo Toast lưu thành công.
- Tuy nhiên nút **"Thêm Câu Hỏi Mới"** (`handleAdminAddFaq`) trước đó vẫn thực hiện chèn thêm phần tử vào danh sách DOM và xóa trắng form.

**Mục tiêu:**
Đồng bộ hóa 100% tính năng mô phỏng tĩnh của nút **"Thêm Câu Hỏi Mới"**:
- Khi bấm nút `Thêm Câu Hỏi Mới`: Chỉ hiển thị thông báo Toast thành công:
  `"Đã thêm câu hỏi thường gặp mới thành công!"` (type `success`).
- Không chèn thêm phần tử mới vào danh sách FAQ trong DOM (danh sách giữ nguyên 4 câu chuẩn của hệ thống).
- Không xóa trắng nội dung trên form (giữ nguyên dữ liệu câu #1 đang cố định).

---

## 2. Chi Tiết Kỹ Thuật

### 2.1. Cập nhật hàm `handleAdminAddFaq` trong `js/app.js`

```javascript
function handleAdminAddFaq(e) {
  if (e && typeof e.preventDefault === 'function') e.preventDefault();
  showToast('Đã thêm câu hỏi thường gặp mới thành công!', 'success');
  return false;
}
```

### 2.2. Giao diện trong `admin/settings.html`
- Form `#faq-add-form` với sự kiện `onsubmit="handleAdminAddFaq(event)"` giữ nguyên.
- Nút bấm `<button type="submit" class="btn-view-detail"><i class="fas fa-plus"></i> Thêm Câu Hỏi Mới</button>` giữ nguyên, đảm bảo styling nhất quán.

---

## 3. Tiêu Chí Nghiệm Thu & Kiểm Thử

1. Bấm nút "Thêm Câu Hỏi Mới" hiển thị thông báo Toast: `"Đã thêm câu hỏi thường gặp mới thành công!"`.
2. Danh sách `#faq-admin-list` giữ nguyên số lượng phần tử hiện tại (không bị append thẻ div mới).
3. Các trường input `#faq-new-question`, `#faq-new-order`, `#faq-new-answer` giữ nguyên nội dung (không bị wipe sạch về rỗng).
4. Cập nhật test suite và đảm bảo 100% test suites trong repository đều PASS.
