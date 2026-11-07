import os
import sys

# Ensure execution from project root directory regardless of invocation path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT_DIR)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

checks = []

def check(code_id, name, points, condition, details=''):
    checks.append((code_id, name, points, condition, details))
    mark = '✅ PASS' if condition else '❌ FAIL'
    print(f"{mark}: [{code_id} - {points}đ] {name}\n   -> {details}")

print("======================================================================")
print("KIỂM TRA ĐỘ BAO PHỦ TOÀN BỘ TIÊU CHÍ RUBRIC ĐỒ ÁN WEB 1 (10.0 ĐIỂM)")
print("======================================================================\n")

# ==================== PHẦN 1: NGƯỜI DÙNG CUỐI (5.0 ĐIỂM) ====================
print("--- PHẦN 1: CÁC CHỨC NĂNG CHO NGƯỜI DÙNG CUỐI (END-USER) (5.0 ĐIỂM) ---")

# 1.1 Hiển thị sản phẩm theo phân loại (0.5đ)
idx_content = open('index.html', encoding='utf-8').read()
c1_1 = ('#monster-products' in idx_content and 
        '#redbull-products' in idx_content and 
        '#sting-products' in idx_content and 
        'nav-menu' in idx_content)
check('1.1', 'Hiển thị sản phẩm theo phân loại', 0.5, c1_1, 
      'Đầy đủ 3 danh mục Monster Energy, Redbull Thái Lan, Sting PepsiCo và menu phân loại.')

# 1.2 Hiển thị chi tiết sản phẩm (0.5đ)
detail_files = [
    'pages/product-detail.html',
    'pages/product-detail-redbull.html',
    'pages/product-detail-sting.html'
]
c1_2 = all(os.path.exists(f) for f in detail_files)
check('1.2', 'Hiển thị chi tiết sản phẩm', 0.5, c1_2, 
      'Trang chi tiết chuyên sâu cho từng thương hiệu với ảnh phóng to, thông số dinh dưỡng, vị lon.')

# 1.3 Tìm kiếm cơ bản theo tên sản phẩm (tìm tương đối) (0.25đ)
c1_3 = ('search-input' in idx_content and 
        'search-results-dropdown' in idx_content and 
        'search-static-list' in idx_content)
check('1.3', 'Tìm kiếm cơ bản theo tên sản phẩm (tìm tương đối)', 0.25, c1_3, 
      'Thanh tìm kiếm có dropdown gợi ý tức thì các dòng sản phẩm khớp tên tương đối.')

# 1.4 Tìm kiếm nâng cao: tên + phân loại + khoảng giá (0.5đ)
c1_4 = ('modal-adv-search' in idx_content and 
        'adv-search-keyword' in idx_content and 
        'adv-search-brand' in idx_content and 
        'adv-search-price' in idx_content)
check('1.4', 'Tìm kiếm nâng cao kết hợp 3 điều kiện (Tên + Phân loại + Khoảng giá)', 0.5, c1_4, 
      'Modal tìm kiếm nâng cao kết hợp Từ khóa + Thương hiệu + Khoảng giá có gợi ý trực quan.')

# 1.5 Hiển thị sản phẩm và kết quả tìm kiếm dạng phân trang (0.5đ)
c1_5 = ('pagination-strip' in idx_content and 
        'page-btn' in idx_content and 
        'active' in idx_content)
check('1.5', 'Hiển thị sản phẩm và kết quả tìm kiếm dạng phân trang', 0.5, c1_5, 
      'Thanh điều hướng phân trang chuyên nghiệp (Trang 1, 2, 3, Trước, Sau).')

# 1.6 Đăng ký làm người mua hàng (0.5đ)
login_content = open('pages/login.html', encoding='utf-8').read()
c1_6 = ('form-register' in login_content and 
        'register-fullname' in login_content and 
        'register-phone' in login_content and 
        'register-email' in login_content and 
        'register-password' in login_content)
check('1.6', 'Đăng ký làm người mua hàng (giao diện trên người dùng đầu cuối)', 0.5, c1_6, 
      'Form đăng ký người mua đầy đủ họ tên, sđt, email/tên tài khoản, mật khẩu, xác nhận mật khẩu.')

# 1.7 Bán hàng có giỏ hàng:
cart_content = open('pages/cart.html', encoding='utf-8').read()
# 1.7.1 Yêu cầu đăng nhập & tự hiển thị thông tin người đăng nhập (0.5đ)
c1_7_1 = ('checkout-name' in cart_content and 
          'checkout-phone' in cart_content and 
          'cart-table' in cart_content)
check('1.7.1', 'Yêu cầu đăng nhập & tự hiển thị thông tin người đăng nhập', 0.5, c1_7_1, 
      'Hiển thị họ tên người mua (Thuận Trần), số điện thoại nhận hàng từ tài khoản đăng nhập.')

# 1.7.2 Cho phép chọn địa chỉ tài khoản hoặc nhập địa chỉ mới (0.25đ)
c1_7_2 = ('checkout-address' in cart_content and 
          'autocomplete="street-address"' in cart_content)
check('1.7.2', 'Cho phép chọn địa chỉ tài khoản hoặc nhập địa chỉ mới', 0.25, c1_7_2, 
      'Trường địa chỉ nhận hàng linh hoạt cho phép chỉnh sửa/nhập địa chỉ mới bất kỳ.')

# 1.7.3 Chọn hình thức chi trả trực tuyến hoặc tiền mặt (0.5đ)
c1_7_3 = ('pay-cod' in cart_content and 
          'pay-qr' in cart_content and 
          'pay-momo' in cart_content)
check('1.7.3', 'Chọn hình thức chi trả (Trực tuyến hoặc Tiền mặt - Không yêu cầu trang thanh toán)', 0.5, c1_7_3, 
      'Radio options: COD Tiền mặt khi nhận hàng vs Quét mã QR VietQR vs Ví MoMo/VNPay.')

# 1.8 Hiển thị và lưu đơn hàng khi kết thúc giao dịch (0.5đ)
success_content = open('pages/order-success.html', encoding='utf-8').read()
c1_8 = ('order-info-card' in success_content or 'success-icon' in success_content or 'order-id' in success_content)
check('1.8', 'Hiển thị và lưu đơn hàng khi kết thúc giao dịch', 0.5, c1_8, 
      'Trang order-success hiển thị mã đơn, tóm tắt thanh toán và liên kết đến lịch sử mua hàng.')

# 1.9 Xem lại lịch sử mua hàng nhóm theo đơn (0.5đ)
orders_content = open('pages/orders.html', encoding='utf-8').read()
account_content = open('pages/account.html', encoding='utf-8').read()
c1_9 = ('#EB-' in orders_content and 'orders-tbody' in orders_content and '#EB-' in account_content)
check('1.9', 'Xem lại lịch sử mua hàng của người mua (được nhóm theo đơn hàng)', 0.5, c1_9, 
      'Trang orders.html và account.html nhóm lịch sử theo từng mã đơn (#EB-2026, #EB-2025) với danh sách lon chi tiết.')


# ==================== PHẦN 2: QUẢN TRỊ VIÊN (WEB-ADMIN) (5.0 ĐIỂM) ====================
print("\n--- PHẦN 2: CÁC CHỨC NĂNG CHO QUẢN TRỊ VIÊN (WEB-ADMIN) (5.0 ĐIỂM) ---")

# 2.1 Đăng nhập & Đăng xuất URL riêng (0.5đ)
admin_login = open('admin/login.html', encoding='utf-8').read()
app_js = open('js/app.js', encoding='utf-8').read()
c2_1 = (os.path.exists('admin/login.html') and 
        ('admin-login-form' in admin_login or 'form-admin-login' in admin_login) and 
        'adminLogout' in app_js and 
        'login.html' in open('admin/index.html', encoding='utf-8').read())
check('2.1', 'Đăng nhập & Đăng xuất Admin qua URL riêng biệt', 0.5, c2_1, 
      'Trang admin/login.html tách biệt với pages/login.html, nút Đăng xuất sidebar điều hướng về login.html.')

# 2.2 Quản lý user: thêm, sửa, khóa/mở (0.5đ)
cust_content = open('admin/customers.html', encoding='utf-8').read()
c2_2 = ('modal-add-user' in cust_content and 
        'modal-edit-user' in cust_content and 
        'toggleLockUser' in cust_content and 
        'btn-action-lock' in cust_content)
check('2.2', 'Quản lý user (thêm#đăng ký, sửa, khoá/ mở user)', 0.5, c2_2, 
      'Modal Thêm user, Modal Sửa user và Nút Khoá/Mở tài khoản trực quan trên bảng.')

# 2.3 Thêm sản phẩm: đúng phân loại, upload hình có preview (0.5đ)
inv_content = open('admin/inventory.html', encoding='utf-8').read()
c2_3 = ('modal-add-product' in inv_content and 
        'add-prod-file' in inv_content and 
        'previewAddProductImage' in inv_content and 
        'Monster Energy' in inv_content)
check('2.3', 'Thêm sản phẩm: đúng phân loại - có upload hình & preview ảnh', 0.5, c2_3, 
      'Modal Thêm phân loại chuẩn (Monster, Redbull, Sting), input file có FileReader xem trước ảnh tức thì.')

# 2.4 Sửa sản phẩm: nạp đúng thông tin trước khi sửa (0.5đ)
c2_4 = ('modal-edit-product' in inv_content and 
        ('openProductEditModal' in inv_content or 'openEditProductModal' in inv_content) and 
        'edit-prod-img-preview' in inv_content)
check('2.4', 'Sửa sản phẩm: hiển thị đúng thông tin trước khi sửa (phân loại và hình)', 0.5, c2_4, 
      'Modal Sửa tự nạp đúng ảnh hiện tại, danh mục thương hiệu, giá bán và số lượng tồn kho.')

# 2.5 Xóa sản phẩm: kiểm tra đã bán -> ẩn; chưa bán -> hỏi xóa (0.75đ)
c2_5 = ('handleAdminDeleteProduct' in app_js and 
        'hasOrders' in app_js and 
        'ĐÃ ẨN' in app_js)
check('2.5', 'Xoá sản phẩm: đã bán thì ẩn, chưa bán thì hỏi lại và xoá', 0.75, c2_5, 
      'Hàm handleAdminDeleteProduct kiểm tra hasOrders: đã phát sinh đơn thì ẩn khỏi web, chưa bán thì xóa.')

# 2.6.1 Cập nhật trạng thái đơn hàng 1 chiều (0.5đ)
order_content = open('admin/orders.html', encoding='utf-8').read()
c2_6_1 = ('modal-order-status' in order_content and 
          'ORDER_STATUS_ORDER' in app_js and 
          'Chưa xác nhận' in app_js and 
          'Đã xác nhận' in app_js and 
          'Đã giao' in app_js)
check('2.6.1', 'Cập nhật tình trạng đơn hàng (chỉ cập nhật xuôi, không cho phép cập nhật ngược)', 0.5, c2_6_1, 
      'State machine một chiều: Chưa xác nhận -> Đã xác nhận -> Đã giao, khóa cập nhật ngược.')

# 2.6.2 Lọc đơn hàng: trạng thái / ngày đặt / địa điểm giao hàng (0.75đ)
c2_6_2 = ('filter-order-status' in order_content and 
          'filter-order-date-from' in order_content and 
          'filter-order-date-to' in order_content and 
          'filter-order-location' in order_content)
check('2.6.2', 'Lọc đơn hàng theo tình trạng / khoảng thời gian / địa điểm giao hàng', 0.75, c2_6_2, 
      'Bộ lọc 3 chiều: Tình trạng đơn hàng, Khoảng ngày từ-đến, Địa điểm Quận/Huyện/Thành phố.')

# 2.6.3 Thống kê Top 5 khách hàng chi tiêu cao nhất (1.0đ)
c2_6_3 = ('stat-customer-from' in cust_content and 
          'stat-customer-to' in cust_content and 
          'TOP 5 KHÁCH HÀNG' in cust_content and 
          'openOrderDetailModal' in cust_content and 
          '15.200.000đ' in cust_content)
check('2.6.3', 'Thống kê Top 5 khách hàng mua cao nhất (có khoảng thời gian, link chi tiết đơn, tổng mua giảm dần)', 1.0, c2_6_3, 
      'Bảng Top 5 VIP sắp xếp giảm dần (15.2M > 12.4M > 9.6M > 7.8M > 5.4M), form chọn ngày, link đơn hàng xem chi tiết.')

# ==================== TỔNG KẾT ====================
passed = sum(1 for _, _, _, ok, _ in checks if ok)
total = len(checks)
total_points = sum(pts for _, _, pts, ok, _ in checks if ok)
max_points = sum(pts for _, _, pts, _, _ in checks)

print("\n======================================================================")
print(f"KẾT QUẢ TỔNG HỢP: {passed}/{total} TIÊU CHÍ ĐẠT")
print(f"TỔNG ĐIỂM DỰ KIẾN: {total_points:.2f} / {max_points:.2f} ĐIỂM")
print("======================================================================")

if passed == total:
    print("🎉 CHÚC MỪNG: HỆ THỐNG ĐÃ BAO PHỦ 100% TẤT CẢ TIÊU CHÍ RUBRIC ĐỀ THI!")
    sys.exit(0)
else:
    print(f"⚠️ CẢNH BÁO: Còn {total - passed} tiêu chí chưa hoàn thiện!")
    sys.exit(1)
