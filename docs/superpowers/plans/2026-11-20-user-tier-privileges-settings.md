# Plan: Quyền Lợi Các Hạng User Trong Cài Đặt Hệ Thống (Toast-Only Sync)

- **Branch:** `main`
- **Request:** Trong `admin/settings.html` (Cài Đặt Hệ Thống), bổ sung phần cấu hình **Quyền Lợi Các Hạng Thành Viên** đồng bộ với các hạng user và người dùng hiện tại (`Hạng Kim Cương`, `Hạng Vàng`, `Hạng Bạc`, `Khách Hàng Chuẩn`), nhưng **mọi thao tác chỉ hiển thị thông báo `showToast`** (không làm biến đổi DOM thẻ hạng, danh sách khách hàng, `CUSTOMER_DATA_REGISTRY`, hay `localStorage`).
- **Execution Mode:** `/subagent-driven-development` với 9 sub-agent (4 implementer song song trên 4 file tách biệt -> 4 reviewer song song -> 1 Final Whole-Branch Reviewer trên model `pro`).

## Global Constraints
1. **Toast-Only Simulation:** Mọi thao tác (`selectUserTierPrivilege`, `handleTierRankSelectNotice`, `handleTierPrivilegesToggle`, `handleSyncTierPrivilegesNow`, `handleSaveTierPrivileges`, `handleResetTierPrivileges`) chỉ được gọi `showToast(...)` để phản hồi; TUYỆT ĐỐI không thay đổi DOM các thẻ hạng trong `#tier-privileges-grid`, không ghi `localStorage`, không sửa `CUSTOMER_DATA_REGISTRY`, không ẩn/sửa dữ liệu khách hàng.
2. **Đồng bộ 100% với user hiện tại trong codebase:**
   - **Kim Cương** (`diamond`, `.vip-badge-diamond`): `Phạm Minh Tuấn`, `Nguyễn Văn An` (2 khách) — `Miễn phí ship hỏa tốc + Chiết khấu 10%` (`10%`, `Từ 12.000.000đ`, `Điểm x2.0`).
   - **Vàng** (`gold`, `.vip-badge-gold`): `Trần Thị Bích`, `Lê Hoàng Nam` (2 khách) — `Chiết khấu 7% toàn bộ đơn hàng` (`7%`, `Từ 7.000.000đ`, `Điểm x1.5`).
   - **Bạc** (`silver`, `.vip-badge-silver`): `Vũ Thảo My`, `Hoàng Đức Long` & tài khoản đang đăng nhập `Thuận Trần` (`860 điểm`) — `Tích điểm đổi quà VIP độc quyền` (`3%`, `Từ 3.000.000đ`, `Điểm x1.2`).
   - **Khách Hàng Chuẩn** (`standard`, `.tier-badge-standard`): `Khách hàng chuẩn / Tài khoản mới` (khớp modal Sửa/Thêm User ở `admin/customers.html`) — `Tích điểm cơ bản & áp dụng Voucher công khai` (`0%`, `Dưới 3.000.000đ`, `Điểm x1.0`).
3. **Preservation:** Không làm gãy section Thông Tin Cửa Hàng, Voucher (`MONSTER10`, `10%`, `GIẢM 10%`, `voucher-min-spend`..`ship-standard-fee`), FAQ (`QUẢN LÝ CÂU HỎI THƯỜNG GẶP (FAQ)`, FAQ #1–#4), Footer 4 cột, hay sidebar navigation.
4. **Modern Web Guidance:** Áp dụng CSS Grid responsive `repeat(auto-fit, minmax(260px, 1fr))` với `min-inline-size: 0` và `gap`, accessible `<label for>`, thuộc tính `name` trên mọi control, `aria-labelledby` trên `<form>`, `type="button"` cho nút phụ, `:focus-visible` rõ nét, không auto-submit trên `<select>`.

## Tasks
- **Task 1 (`css/style.css`):** Bổ sung style responsive cho `#tier-privileges-section`, `.tier-privileges-grid`, `.tier-privilege-card`, `.tier-card-top`, `.tier-rate-pill`, `.tier-badge-standard`, `.tier-sync-users`, `.tier-privilege-summary`, `.tier-card-actions`, `.tier-threshold-note`, `:focus-visible` và `@media (max-width: 600px)`.
- **Task 2 (`admin/settings.html`):** Chèn `<section id="tier-privileges-section" class="admin-section-box" style="max-width: 740px;">` ngay giữa section Voucher & Shipping và section FAQ, chứa 4 thẻ hạng đồng bộ user hiện tại + biểu mẫu `#form-tier-privileges` với đầy đủ `<label for>`, `name`, `.price-format-input` trên `#tier-privilege-threshold`.
- **Task 3 (`js/app.js`):** Bổ sung `USER_TIER_PRIVILEGES_DATA` và 6 hàm xử lý toast-only (`selectUserTierPrivilege`, `handleTierRankSelectNotice`, `handleTierPrivilegesToggle`, `handleSyncTierPrivilegesNow`, `handleSaveTierPrivileges`, `handleResetTierPrivileges`) + gắn lên `window`.
- **Task 4 (`scripts/verify_admin_tier_privileges.py`):** Viết script kiểm thử tự động kiểm tra HTML/CSS/JS tĩnh và thực thi runtime bằng Node `vm` xác nhận dữ liệu đồng bộ và mọi thao tác chỉ phát sinh `showToast` mà không làm thay đổi DOM hay `localStorage`.
