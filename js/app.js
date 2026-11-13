/**
 * MONSTER ENERGY STORE - CORE APPLICATION SCRIPT
 * Lightweight Vanilla JS: Toast, Lightbox, Smart Login, Secret Hotkey & Mock Checkout Flow
 */

// 0. Site root resolver: suy ra thư mục gốc từ vị trí js/app.js,
//    để điều hướng đúng dù trang đang ở root, pages/ hay admin/,
//    cả file:// lẫn GitHub Pages (kể cả project site /user/repo/).
const SITE_ROOT = (() => {
  try {
    const s = (document.currentScript && document.currentScript.src)
      || ((document.querySelector('script[src*="js/app.js"]') || {}).src) || '';
    const i = s.lastIndexOf('js/app.js');
    if (i > 0) return s.slice(0, i);
  } catch (err) { /* bỏ qua, dùng fallback */ }
  return './';
})();

// Điều hướng theo đường dẫn tính từ site root (VD: go('pages/cart.html'))
function go(path) {
  window.location.href = SITE_ROOT + path;
}

// 1. Toast Notification
function showToast(message, type = 'success') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;

  const iconClass = type === 'success' 
    ? 'fas fa-check-circle' 
    : (type === 'warning' ? 'fas fa-exclamation-triangle' : 'fas fa-info-circle');

  toast.innerHTML = `
    <i class="${iconClass} toast-icon"></i>
    <span class="toast-msg">${message}</span>
  `;

  container.appendChild(toast);

  // Auto remove after 3.2 seconds
  setTimeout(() => {
    toast.style.animation = 'toastOut 0.3s ease forwards';
    setTimeout(() => {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
    }, 300);
  }, 3200);
}

// 2. Single-image Lightbox Modal
function openLightbox(imgSrc, title) {
  let modal = document.getElementById('image-lightbox');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'image-lightbox';
    modal.className = 'image-lightbox';
    modal.onclick = (e) => { 
      if (e.target === modal || e.target.classList.contains('lightbox-close')) {
        closeLightbox(); 
      }
    };
    modal.innerHTML = `
      <div class="lightbox-content">
        <button class="lightbox-close" title="Đóng" onclick="closeLightbox()">&times;</button>
        <img id="lightbox-img" src="" alt="Lon nước phóng to" />
        <p id="lightbox-caption" class="lightbox-caption"></p>
      </div>
    `;
    document.body.appendChild(modal);
  }
  const imgEl = document.getElementById('lightbox-img');
  const capEl = document.getElementById('lightbox-caption');
  if (imgEl) imgEl.src = imgSrc;
  if (capEl) capEl.innerText = title || '';
  modal.classList.add('active');
}

function closeLightbox() {
  const modal = document.getElementById('image-lightbox');
  if (modal) modal.classList.remove('active');
}

// 3. Smart Login - Whitelist Quản Trị Viên (UX Camouflage)
function handleLogin(e) {
  if (e && e.preventDefault) e.preventDefault();
  const userEl = document.getElementById('login-username');
  const inputVal = (userEl ? userEl.value : '').trim();
  const rawName = inputVal || 'Khách Hàng VIP';
  const username = inputVal.toLowerCase();
  const ADMIN_USERS = ['admin', 'admin@monsterenergy.com'];

  try {
    localStorage.setItem('monster_user', rawName);
  } catch (err) { /* file:// riêng tư có thể chặn storage: bỏ qua */ }

  if (ADMIN_USERS.includes(username)) {
    showToast('Xác thực Quản trị viên thành công! Đang chuyển hướng...', 'success');
    setTimeout(() => { go('admin/index.html'); }, 900);
  } else {
    showToast('Đăng nhập thành công! Chào mừng ' + rawName + ' quay lại mua sắm.', 'success');
    setTimeout(() => { go('index.html'); }, 900);
  }
}

// 3b. Lấy tên tài khoản đã lưu (dùng chung header + trang account)
function getLoggedUser() {
  try {
    return (localStorage.getItem('monster_user') || '').trim();
  } catch (err) { return ''; }
}

// 3c. Đăng xuất: xóa tên đã lưu, về trang chủ
function logout() {
  try {
    localStorage.removeItem('monster_user');
  } catch (err) { /* bỏ qua */ }
  showToast('Đã đăng xuất khỏi tài khoản!', 'info');
  setTimeout(() => { go('index.html'); }, 900);
}

// 3d. Điền thông tin lên trang account.html (chưa đăng nhập thì về login)
function initAccountPage() {
  const displayName = getLoggedUser();
  if (!displayName) {
    showToast('Bạn chưa đăng nhập! Đang chuyển tới trang đăng nhập...', 'warning');
    setTimeout(() => { go('pages/login.html'); }, 900);
    return;
  }
  const nameEl = document.getElementById('account-display-name');
  const avatarEl = document.getElementById('account-avatar');
  if (nameEl) nameEl.innerText = displayName;
  if (avatarEl) avatarEl.innerText = displayName.charAt(0).toUpperCase();
}

// 3e. Header tài khoản: chưa login -> về login.html; đã login -> account.html + hiện tên
function initAccountHeader() {
  const displayName = getLoggedUser();
  const accountLink = document.getElementById('header-account-link');
  if (!displayName) {
    if (accountLink) accountLink.href = SITE_ROOT + 'pages/login.html';
    return;
  }
  if (accountLink) accountLink.href = SITE_ROOT + 'pages/account.html';
  const accountEl = document.getElementById('header-account-value');
  if (accountEl) {
    accountEl.innerText = displayName.length > 18 ? displayName.slice(0, 18) + '…' : displayName;
    accountEl.title = displayName;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  initAccountHeader();
});

// 4. Secret Admin Hotkey: Ctrl + Shift + A (hoặc Cmd + Shift + A trên macOS)
document.addEventListener('keydown', (e) => {
  // Guard: Không kích hoạt khi đang gõ phím trong form/input/textarea/select
  if (/^(INPUT|TEXTAREA|SELECT)$/i.test(e.target.tagName) || e.target.isContentEditable) return;

  // Khớp phím vật lý KeyA (bất kể kiểu gõ tiếng Việt Telex/VNI)
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.code === 'KeyA') {
    e.preventDefault();
    showToast('Kích hoạt cổng Quản trị viên (Secret Hotkey)...', 'info');
    setTimeout(() => { go('admin/index.html'); }, 900);
  }
});

// 5. Checkout Logic - Validate & Pass Data via URLSearchParams
function processCheckout() {
  const nameEl = document.getElementById('checkout-name') || document.getElementById('order-fullname');
  const phoneEl = document.getElementById('checkout-phone') || document.getElementById('order-phone');
  const addrEl = document.getElementById('checkout-address') || document.getElementById('order-address');
  const notesEl = document.getElementById('checkout-notes') || document.getElementById('order-notes');

  const name = (nameEl ? nameEl.value : '').trim();
  let phone = (phoneEl ? phoneEl.value : '').trim();
  const address = (addrEl ? addrEl.value : '').trim();
  const notes = (notesEl ? notesEl.value : '').trim();

  // Validate Họ và tên (tối thiểu 2 ký tự)
  if (name.length < 2) {
    showToast('Vui lòng nhập họ và tên người nhận hợp lệ (tối thiểu 2 ký tự)!', 'warning');
    if (nameEl) nameEl.focus();
    return;
  }

  // Normalize & Validate Số điện thoại chuẩn Việt Nam: 10 chữ số bắt đầu bằng 0 (hỗ trợ dấu chấm, khoảng trắng, gạch nối)
  const cleanPhone = phone.replace(/[\s.-]/g, '');
  const phoneRegex = /^0\d{9}$/;
  if (!phoneRegex.test(cleanPhone)) {
    showToast('Số điện thoại không hợp lệ! Vui lòng nhập đúng 10 chữ số bắt đầu bằng 0 (VD: 0912.888.999 hoặc 0912345678).', 'warning');
    if (phoneEl) phoneEl.focus();
    return;
  }

  // Validate Địa chỉ giao hàng (tối thiểu 10 ký tự)
  if (address.length < 10) {
    showToast('Địa chỉ giao hàng quá ngắn! Vui lòng nhập địa chỉ cụ thể (tối thiểu 10 ký tự).', 'warning');
    if (addrEl) addrEl.focus();
    return;
  }

  // Lấy phương thức thanh toán được chọn
  const methodRadio = document.querySelector('input[name="payment_method"]:checked');
  if (!methodRadio) {
    showToast('Vui lòng chọn 1 phương thức thanh toán!', 'warning');
    return;
  }
  const method = methodRadio.value;

  // Lấy tổng tiền động từ giao diện giỏ hàng
  const totalEl = document.querySelector('.summary-line.total span:last-child');
  const amount = totalEl ? totalEl.textContent.trim() : '216.000đ';

  // Sinh mã đơn hàng động duy nhất
  const orderId = 'ME-' + Date.now().toString().slice(-4);

  // Đóng gói params qua URLSearchParams
  const params = new URLSearchParams({
    order: orderId,
    name: name,
    phone: cleanPhone,
    address: address,
    notes: notes,
    method: method,
    amount: amount,
    items: '7'
  });

  showToast('Thông tin hợp lệ! Đang khởi tạo đơn hàng ' + orderId + '...', 'info');

  setTimeout(() => {
    if (method === 'cod') {
      window.location.href = SITE_ROOT + 'pages/order-success.html?' + params.toString();
    } else {
      window.location.href = SITE_ROOT + 'pages/payment-gateway.html?' + params.toString();
    }
  }, 900);
}

// 6. Countdown Timer & Payment Gateway Controller (Dành cho payment-gateway.html)
function initPaymentGateway() {
  const params = new URLSearchParams(window.location.search);
  const orderId = params.get('order') || ('ME-' + Date.now().toString().slice(-4));
  const amount = params.get('amount') || '216.000đ';
  const method = params.get('method') || 'vietqr';

  const orderEl = document.getElementById('gateway-order-id');
  const amountEl = document.getElementById('gateway-amount');
  const memoEl = document.getElementById('gateway-memo');
  const methodTitle = document.getElementById('gateway-method-title');

  if (orderEl) orderEl.innerText = orderId;
  if (amountEl) amountEl.innerText = amount;
  if (memoEl) memoEl.innerText = orderId;

  if (methodTitle) {
    if (method === 'momo') {
      methodTitle.innerText = 'CỔNG THANH TOÁN VÍ ĐIỆN TỬ MOMO / VNPAY';
    } else if (method === 'card') {
      methodTitle.innerText = 'CỔNG THANH TOÁN THẺ QUỐC TẾ VISA / MASTER';
    } else {
      methodTitle.innerText = 'CỔNG THANH TOÁN CHUYỂN KHOẢN VIETQR (NAPAS247)';
    }
  }

  // Đồng hồ đếm ngược 15:00
  let timeLeft = 15 * 60;
  const timerEl = document.getElementById('countdown-timer');
  const confirmBtn = document.getElementById('btn-confirm-payment');

  const countdown = setInterval(() => {
    timeLeft--;
    const mins = Math.floor(timeLeft / 60);
    const secs = timeLeft % 60;
    if (timerEl) {
      timerEl.innerText = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }

    if (timeLeft <= 0) {
      clearInterval(countdown);
      if (timerEl) {
        timerEl.innerText = '00:00 (Hết hạn)';
        timerEl.style.color = '#EF4444';
      }
      if (confirmBtn) {
        confirmBtn.disabled = true;
        confirmBtn.style.opacity = '0.5';
        confirmBtn.style.cursor = 'not-allowed';
      }
      showToast('Giao dịch đã hết hạn! Vui lòng quay lại giỏ hàng để tạo đơn mới.', 'warning');
    }
  }, 1000);
}

// 7. Xác nhận chuyển khoản (payment-gateway sang order-success)
function confirmMockPayment() {
  const params = new URLSearchParams(window.location.search);
  const orderId = params.get('order') || 'ME-8809';
  const payAmount = params.get('amount') || '216.000đ';

  showToast('Xác nhận đã nhận ' + payAmount + ' thành công cho đơn hàng ' + orderId + '! Đang hoàn tất...', 'success');
  setTimeout(() => {
    window.location.href = SITE_ROOT + 'pages/order-success.html?' + params.toString();
  }, 900);
}

// 8. Populate Order Success Data (Dành cho order-success.html)
function initOrderSuccess() {
  const params = new URLSearchParams(window.location.search);
  const orderId = params.get('order') || ('ME-' + Date.now().toString().slice(-4));
  const name = params.get('name') || 'Trần Minh Thuận';
  const phone = params.get('phone') || '0912345678';
  const address = params.get('address') || '123 Lê Lợi, Phường Bến Nghé, Quận 1, TP.HCM';
  const method = params.get('method') || 'vietqr';
  const amount = params.get('amount') || '216.000đ';

  const orderEl = document.getElementById('success-order-id');
  const nameEl = document.getElementById('success-name');
  const phoneEl = document.getElementById('success-phone');
  const addrEl = document.getElementById('success-address');
  const amountEl = document.getElementById('success-amount');
  const methodBadge = document.getElementById('success-method-badge');
  const timeEl = document.getElementById('success-time');

  if (orderEl) orderEl.innerText = '#' + orderId;
  if (nameEl) nameEl.innerText = name;
  if (phoneEl) phoneEl.innerText = phone;
  if (addrEl) addrEl.innerText = address;
  if (amountEl) amountEl.innerText = amount;
  if (timeEl) {
    const now = new Date();
    timeEl.innerText = now.toLocaleDateString('vi-VN') + ' ' + now.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' });
  }

  if (methodBadge) {
    if (method === 'cod') {
      methodBadge.className = 'badge-status warning';
      methodBadge.innerHTML = '<i class="fas fa-hand-holding-dollar"></i> THANH TOÁN KHI NHẬN HÀNG (COD)';
    } else if (method === 'momo') {
      methodBadge.className = 'badge-status info';
      methodBadge.innerHTML = '<i class="fas fa-wallet"></i> ĐÃ THANH TOÁN QUA VÍ MOMO';
    } else if (method === 'card') {
      methodBadge.className = 'badge-status info';
      methodBadge.innerHTML = '<i class="fas fa-credit-card"></i> ĐÃ THANH TOÁN THẺ QUỐC TẾ';
    } else {
      methodBadge.className = 'badge-status success';
      methodBadge.innerHTML = '<i class="fas fa-qrcode"></i> ĐÃ THANH TOÁN (VIETQR NAPAS247)';
    }
  }
}

// ==========================================================================
// 9. Admin Interactive Modals (Dark Neon Glassmorphism)
// ==========================================================================
function openAdminModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

function closeAdminModal(modalId) {
  if (modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove('active');
  } else {
    document.querySelectorAll('.admin-modal-overlay.active').forEach(m => m.classList.remove('active'));
  }
  const remaining = document.querySelectorAll('.admin-modal-overlay.active');
  if (remaining.length === 0) {
    document.body.style.overflow = '';
  }
}

// Global modal overlay click and ESC key listeners
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeAdminModal();
  }
});

document.addEventListener('click', (e) => {
  if (e.target && e.target.classList && e.target.classList.contains('admin-modal-overlay')) {
    closeAdminModal();
  }
});

// Variable to track active table row being edited
let currentEditingRow = null;

// Product Data Registry for Admin Modals and Standalone Pages
const PRODUCT_DATA_REGISTRY = {
  'monster-original': {
    id: 'monster-original',
    name: 'Monster Energy Original 355ml',
    brand: 'Monster Energy (Hà Lan / Hoa Kỳ)',
    origin: 'Malaysia (Ủy quyền Monster Energy Company)',
    flavor: 'Vị nguyên bản đậm đà, sảng khoái với Taurine & Nhân sâm',
    price: '45.000đ',
    oldPrice: '55.000đ',
    volume: '355ml (Lon nhôm cao cấp)',
    ingredients: 'Nước bão hòa CO2, Sucroza, chiết xuất đường nho, chiết xuất nhân sâm, L-Carnitine, Taurine (400mg/100ml), Caffeine (30mg/100ml), Inositol, Vitamin B3, B6, B2, B12, Maltodextrin, chất điều chỉnh độ acid...',
    usage: 'Lắc nhẹ trước khi uống, dùng ngay sau khi mở nắp. Ngon hơn khi uống lạnh.',
    storage: 'Để nơi khô ráo, thoáng mát, tránh ánh sáng trực tiếp hoặc nơi có nhiệt độ cao.',
    status: 'Còn hàng',
    editPage: 'edit-monster.html'
  },
  'redbull-original': {
    id: 'redbull-original',
    name: 'Nước Tăng Lực Redbull Original 250ml',
    brand: 'Redbull (Thái Lan / Việt Nam)',
    origin: 'Thái Lan (Nhượng quyền T.C. Pharmaceutical)',
    price: '18.000đ',
    oldPrice: '22.000đ',
    volume: '250ml',
    ingredients: 'Nước, đường mía, chất tạo ngọt, Taurine, Caffeine (50mg), Inositol, Cholin Bitartrate, Kẽm, Vitamin B3, B5, B6, B12...',
    usage: 'Lắc nhẹ trước khi uống, dùng ngay sau khi mở nắp. Ngon hơn khi uống lạnh.',
    storage: 'Để nơi khô ráo, thoáng mát, tránh ánh sáng trực tiếp hoặc nơi có nhiệt độ cao.',
    status: 'Còn hàng',
    editPage: 'edit-redbull-original.html'
  },
  'redbull-thai': {
    id: 'redbull-thai',
    name: 'Nước Tăng Lực Redbull Thái Lan Nhập Khẩu 250ml',
    brand: 'Redbull Krating Daeng (T.C. Pharmaceutical)',
    origin: '100% Nhập Khẩu Nguyên Lon từ Vương Quốc Thái Lan',
    price: '18.000đ',
    oldPrice: '22.000đ',
    volume: '250ml',
    ingredients: 'Nước khoáng thiên nhiên, Sucrose nguyên chất, Taurine hàm lượng cao 1000mg, Caffeine 50mg, Inositol, Vitamin B3, B6, B12...',
    usage: 'Uống trực tiếp khi cần tập trung cao độ, thi đấu thể thao hoặc thức khuya. Ướp đá lạnh tuyệt hảo.',
    storage: 'Bảo quản nhiệt độ phòng hoặc ngăn mát tủ lạnh (4°C - 8°C). Tránh ánh nắng gắt.',
    status: 'Còn hàng',
    editPage: 'edit-redbull-thai.html'
  },
  'redbull-nap-bat': {
    id: 'redbull-nap-bat',
    name: 'Nước Tăng Lực Redbull Nắp Bật 250ml',
    brand: 'Redbull Energy Drink (Sleek Edition)',
    origin: 'Thái Lan (Công nghệ Sleek Can quốc tế)',
    price: '20.000đ',
    oldPrice: '25.000đ',
    volume: '250ml',
    ingredients: 'Nước bão hòa CO2 nhẹ, Đường tinh luyện, Taurine 800mg, Caffeine 80mg, Nhân sâm tự nhiên, Kẽm sinh học, Vitamin B-Complex...',
    usage: 'Bật nắp lon thưởng thức ngay, thích hợp cho người lái xe đường dài, game thủ và tập gym.',
    storage: 'Nơi khô ráo, thoáng mát, tránh va đập mạnh hoặc phơi nắng lâu.',
    status: 'Còn hàng',
    editPage: 'edit-redbull-lonvua.html'
  },
  'sting-dau': {
    id: 'sting-dau',
    name: 'Nước Tăng Lực Sting Dâu Tây Đỏ Sleek 330ml',
    brand: 'Sting (Suntory PepsiCo)',
    origin: 'Việt Nam',
    price: '12.000đ',
    oldPrice: '15.000đ',
    volume: '330ml',
    ingredients: 'Nước bão hòa CO2, đường mía, chất điều chỉnh độ acid, nhân sâm, Taurine, Caffeine, Inositol, Vitamin B3, B6, B12, phẩm màu tổng hợp...',
    usage: 'Dùng trực tiếp, ngon hơn khi uống lạnh. Lắc nhẹ trước khi mở nắp.',
    storage: 'Để nơi khô ráo, thoáng mát, tránh ánh nắng trực tiếp hoặc nơi có nhiệt độ cao.',
    status: 'Còn hàng',
    editPage: 'inventory.html'
  },
  'sting-gold': {
    id: 'sting-gold',
    name: 'Nước Tăng Lực Sting Vàng Nhân Sâm Sleek 330ml',
    brand: 'Sting (Suntory PepsiCo)',
    origin: 'Việt Nam',
    price: '12.000đ',
    oldPrice: '15.000đ',
    volume: '330ml',
    ingredients: 'Nước bão hòa CO2, đường mía, chiết xuất nhân sâm tự nhiên, Taurine, Caffeine, Inositol, Vitamin B3, B6, B12...',
    usage: 'Dùng trực tiếp, ngon hơn khi uống lạnh. Lắc nhẹ trước khi mở nắp.',
    storage: 'Để nơi khô ráo, thoáng mát, tránh ánh nắng trực tiếp hoặc nơi có nhiệt độ cao.',
    status: 'Còn hàng',
    editPage: 'inventory.html'
  },
  'sting-blue': {
    id: 'sting-blue',
    name: 'Nước Tăng Lực Sting Blue Sleek Hương Việt Quất 320ml',
    brand: 'Sting (Suntory PepsiCo)',
    origin: 'Việt Nam',
    price: '13.000đ',
    oldPrice: '16.000đ',
    volume: '320ml',
    ingredients: 'Nước bão hòa CO2, đường mía, hương việt quất tự nhiên và tổng hợp, Taurine, Caffeine, Inositol, Vitamin B3, B6, B12...',
    usage: 'Dùng trực tiếp, ngon hơn khi uống lạnh. Lắc nhẹ trước khi mở nắp.',
    storage: 'Để nơi khô ráo, thoáng mát, tránh ánh nắng trực tiếp hoặc nơi có nhiệt độ cao.',
    status: 'Còn hàng',
    editPage: 'inventory.html'
  }
};

// 9a. Product Edit Modal Logic (Đồng bộ từng lon riêng biệt)
function openProductEditModal(productId, triggerBtn) {
  const pid = String(productId || '').toLowerCase();
  if (pid.startsWith('monster')) {
    window.location.href = 'edit-monster.html';
    return;
  }
  if (pid === 'redbull-thai') {
    window.location.href = 'edit-redbull-thai.html';
    return;
  }
  if (pid === 'redbull-lon-vua' || pid === 'redbull-nap-bat') {
    window.location.href = 'edit-redbull-lonvua.html';
    return;
  }
  if (pid.includes('redbull')) {
    window.location.href = 'edit-redbull-original.html';
    return;
  }
  if (pid.includes('sting')) {
    window.location.href = 'edit-sting.html';
    return;
  }
  const modal = document.getElementById('modal-edit-product');
  if (!modal) return;

  const btn = triggerBtn || (window.event && window.event.target ? window.event.target.closest('button') : null);
  currentEditingRow = btn ? btn.closest('tr') : null;

  const prodKey = productId || 'monster-original';
  const data = PRODUCT_DATA_REGISTRY[prodKey] || PRODUCT_DATA_REGISTRY['monster-original'];

  const nameEl = document.getElementById('edit-prod-name');
  const brandEl = document.getElementById('edit-prod-brand');
  const brandSelect = document.getElementById('edit-prod-brand-select');
  const imgPreview = document.getElementById('edit-prod-img-preview');
  const originEl = document.getElementById('edit-prod-origin');
  const flavorEl = document.getElementById('edit-prod-flavor');
  const priceEl = document.getElementById('edit-prod-price');
  const oldPriceEl = document.getElementById('edit-prod-oldprice');
  const volumeEl = document.getElementById('edit-prod-volume');
  const ingredientsEl = document.getElementById('edit-prod-ingredients');
  const usageEl = document.getElementById('edit-prod-usage');
  const storageEl = document.getElementById('edit-prod-storage');
  const statusEl = document.getElementById('edit-prod-status');
  const standaloneBtn = document.getElementById('modal-standalone-btn');

  if (nameEl) nameEl.value = data.name;
  if (brandEl) brandEl.value = data.brand;
  if (originEl) originEl.value = data.origin;
  if (flavorEl) flavorEl.value = data.flavor || 'Vị nguyên bản đậm đà, sảng khoái với Taurine & Nhân sâm';
  if (priceEl) {
    priceEl.value = data.price;
    setupPriceInput(priceEl);
    updatePricePreview(priceEl);
  }
  if (oldPriceEl) {
    oldPriceEl.value = data.oldPrice;
    setupPriceInput(oldPriceEl);
    updatePricePreview(oldPriceEl);
  }
  if (volumeEl) volumeEl.value = data.volume;
  if (ingredientsEl) ingredientsEl.value = data.ingredients;
  if (usageEl) usageEl.value = data.usage;
  if (storageEl) storageEl.value = data.storage;
  if (statusEl) statusEl.value = data.status;

  if (imgPreview) {
    if (currentEditingRow && currentEditingRow.cells[0]) {
      const rowImg = currentEditingRow.cells[0].querySelector('img');
      if (rowImg) imgPreview.src = rowImg.src;
    } else if (data.image) {
      imgPreview.src = data.image;
    }
  }

  if (brandSelect) {
    const brandValueToMatch = currentEditingRow && currentEditingRow.cells[2] ? currentEditingRow.cells[2].textContent.trim() : data.brand;
    let matched = false;
    Array.from(brandSelect.options).forEach(opt => {
      if (opt.value === brandValueToMatch || brandValueToMatch.includes(opt.value)) {
        brandSelect.value = opt.value;
        matched = true;
      }
    });
    if (!matched && brandSelect.options.length > 0) {
      brandSelect.selectedIndex = 0;
    }
  }

  if (standaloneBtn) {
    if (data.editPage && data.editPage !== 'inventory.html') {
      standaloneBtn.style.display = 'inline-flex';
      standaloneBtn.onclick = () => { window.location.href = data.editPage; };
    } else {
      standaloneBtn.style.display = 'none';
    }
  }

  openAdminModal('modal-edit-product');
}

function saveProductEdit(e) {
  if (e && e.preventDefault) e.preventDefault();
  const nameEl = document.getElementById('edit-prod-name');
  const name = nameEl ? nameEl.value : 'Sản phẩm';

  showToast('Đã lưu thay đổi thông tin sản phẩm "' + name + '" thành công!', 'success');
  closeAdminModal('modal-edit-product');
}

// 9b. Add Product Modal Logic
function addProductImageField() {
  showToast('Đã thêm ảnh sản phẩm thành công!', 'success');
}

function resetAddProductImages() {
  const list = document.getElementById('add-product-images');
  if (!list) return;
  Array.from(list.children).slice(3).forEach(row => row.remove());
  list.querySelectorAll('.product-image-preview').forEach(img => {
    img.hidden = true;
    img.removeAttribute('src');
  });
}

function openAddProductModal() {
  const form = document.getElementById('form-add-product');
  if (form) form.reset();
  resetAddProductImages();
  const addPriceEl = document.getElementById('add-prod-price');
  if (addPriceEl) {
    setupPriceInput(addPriceEl);
    updatePricePreview(addPriceEl);
  }
  openAdminModal('modal-add-product');
}

function saveAddProduct(e) {
  if (e && e.preventDefault) e.preventDefault();
  const nameEl = document.getElementById('add-prod-name');
  const name = (nameEl && nameEl.value) ? nameEl.value : 'Nước Tăng Lực Mới';

  showToast('Đã thêm sản phẩm "' + name + '" vào kho hàng thành công!', 'success');
  closeAdminModal('modal-add-product');
  const form = document.getElementById('form-add-product');
  if (form) {
    form.reset();
    resetAddProductImages();
    const addPrice = document.getElementById('add-prod-price');
    if (addPrice) updatePricePreview(addPrice);
  }
}

// ==========================================================================
// ADMIN INVENTORY: CURRENCY FORMATTING & REAL-TIME PREVIEW SYSTEM
// ==========================================================================
function formatCurrencyVND(val) {
  if (val === undefined || val === null || val === '') return '';
  const clean = String(val).replace(/\D/g, '');
  if (!clean) return '';
  const num = parseInt(clean, 10);
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.') + 'đ';
}

function parseCurrencyVND(val) {
  if (!val) return 0;
  const clean = String(val).replace(/\D/g, '');
  return clean ? parseInt(clean, 10) : 0;
}

function numberToVietnameseWords(n) {
  if (n === undefined || n === null || n === '') return '';
  if (typeof n === 'string') {
    const clean = n.replace(/\D/g, '');
    if (!clean) return '';
    n = parseInt(clean, 10);
  }
  if (n === 0) return 'Không đồng';
  if (isNaN(n)) return '';

  const units = ['', 'nghìn', 'triệu', 'tỷ', 'nghìn tỷ', 'triệu tỷ'];
  const digits = ['không', 'một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín'];

  function readGroupThree(num, showZeroHundred) {
    let h = Math.floor(num / 100);
    let t = Math.floor((num % 100) / 10);
    let u = num % 10;
    let res = [];

    if (h > 0 || showZeroHundred) {
      res.push(digits[h] + ' trăm');
    }

    if (t > 1) {
      res.push(digits[t] + ' mươi');
      if (u === 1) res.push('mốt');
      else if (u === 4) res.push('tư');
      else if (u === 5) res.push('lăm');
      else if (u > 0) res.push(digits[u]);
    } else if (t === 1) {
      res.push('mười');
      if (u === 5) res.push('lăm');
      else if (u > 0) res.push(digits[u]);
    } else if (t === 0 && (h > 0 || showZeroHundred) && u > 0) {
      res.push('lẻ ' + digits[u]);
    } else if (t === 0 && h === 0 && !showZeroHundred && u > 0) {
      res.push(digits[u]);
    }

    return res.join(' ');
  }

  let numStr = Math.floor(Math.abs(n)).toString();
  let groups = [];
  while (numStr.length > 0) {
    groups.push(parseInt(numStr.slice(-3), 10));
    numStr = numStr.slice(0, -3);
  }

  let parts = [];
  for (let i = groups.length - 1; i >= 0; i--) {
    let grp = groups[i];
    if (grp > 0) {
      let isFirstGroup = (i === groups.length - 1);
      let grpText = readGroupThree(grp, !isFirstGroup);
      if (grpText) {
        let unit = units[i];
        parts.push(grpText + (unit ? ' ' + unit : ''));
      }
    }
  }

  let result = parts.join(' ').trim();
  if (!result) return 'Không đồng';
  return result.charAt(0).toUpperCase() + result.slice(1) + ' đồng';
}

function updatePricePreview(inputEl) {
  if (!inputEl) return;
  const parent = inputEl.closest('.admin-form-group') || inputEl.parentElement;
  if (parent) {
    const previewEl = parent.querySelector('.price-preview-tag');
    if (previewEl) {
      previewEl.remove();
    }
  }

  syncStandaloneCardPrice();
}

function syncStandaloneCardPrice() {
  const cardPriceEl = document.getElementById('standalone-card-price-display');
  if (!cardPriceEl) return;
  const priceInput = document.getElementById('standalone-edit-price') || document.querySelector('.admin-standalone-edit-page input.price-format-input:not([id*="old"])');
  const oldPriceInput = document.getElementById('standalone-edit-oldprice') || document.querySelector('.admin-standalone-edit-page input.price-format-input[id*="old"]');
  
  if (priceInput) {
    const curVal = priceInput.value.trim() || '0đ';
    const oldVal = oldPriceInput ? oldPriceInput.value.trim() : '';
    if (oldVal) {
      cardPriceEl.innerHTML = `${curVal} <small style="font-size: 0.85rem; color: var(--text-dim); text-decoration: line-through;">${oldVal}</small>`;
    } else {
      cardPriceEl.innerHTML = curVal;
    }
  }
}

function restoreCursorPosition(input, formatted, digitsBeforeCursor) {
  if (!input || typeof input.setSelectionRange !== 'function') return;
  if (!formatted) {
    input.setSelectionRange(0, 0);
    return;
  }
  if (!digitsBeforeCursor || digitsBeforeCursor <= 0) {
    input.setSelectionRange(0, 0);
    return;
  }
  let seen = 0;
  let targetPos = formatted.length;
  for (let i = 0; i < formatted.length; i++) {
    if (/\d/.test(formatted[i])) {
      seen++;
      if (seen === digitsBeforeCursor) {
        targetPos = i + 1;
        break;
      }
    }
  }
  if (targetPos > formatted.length - 1 && formatted.endsWith('đ')) {
    targetPos = formatted.length - 1;
  }
  input.setSelectionRange(targetPos, targetPos);
}

function setupPriceInput(input) {
  if (!input || input.dataset.priceBound) return;
  input.dataset.priceBound = 'true';
  if (input.type === 'number') {
    input.type = 'text';
  }
  input.classList.add('price-format-input');

  input.addEventListener('keydown', function(e) {
    if (e.key === 'Backspace') {
      const start = this.selectionStart;
      const end = this.selectionEnd;
      if (start === end && start > 0) {
        const charBefore = this.value[start - 1];
        if (charBefore === 'đ' || charBefore === '.') {
          e.preventDefault();
          let prevDigitIdx = -1;
          for (let i = start - 1; i >= 0; i--) {
            if (/\d/.test(this.value[i])) {
              prevDigitIdx = i;
              break;
            }
          }
          if (prevDigitIdx !== -1) {
            const val = this.value;
            const digitsBefore = val.slice(0, prevDigitIdx).replace(/\D/g, '').length;
            const rawWithout = val.slice(0, prevDigitIdx) + val.slice(prevDigitIdx + 1);
            const clean = rawWithout.replace(/\D/g, '');
            const formatted = clean ? formatCurrencyVND(clean) : '';
            this.value = formatted;
            restoreCursorPosition(this, formatted, digitsBefore);
            updatePricePreview(this);
          } else {
            this.value = '';
            updatePricePreview(this);
          }
        }
      }
    } else if (e.key === 'Delete') {
      const start = this.selectionStart;
      const end = this.selectionEnd;
      if (start === end && start < this.value.length) {
        const charAfter = this.value[start];
        if (charAfter === '.' || charAfter === 'đ') {
          e.preventDefault();
          if (charAfter === '.') {
            let nextDigitIdx = -1;
            for (let i = start + 1; i < this.value.length; i++) {
              if (/\d/.test(this.value[i])) {
                nextDigitIdx = i;
                break;
              }
            }
            if (nextDigitIdx !== -1) {
              const val = this.value;
              const digitsBefore = val.slice(0, start).replace(/\D/g, '').length;
              const rawWithout = val.slice(0, nextDigitIdx) + val.slice(nextDigitIdx + 1);
              const clean = rawWithout.replace(/\D/g, '');
              const formatted = clean ? formatCurrencyVND(clean) : '';
              this.value = formatted;
              restoreCursorPosition(this, formatted, digitsBefore);
              updatePricePreview(this);
            }
          }
        }
      }
    }
  });

  input.addEventListener('input', function() {
    const rawDigits = this.value.replace(/\D/g, '');
    const cursor = this.selectionStart || 0;
    const digitsBeforeCursor = this.value.slice(0, cursor).replace(/\D/g, '').length;

    if (!rawDigits) {
      this.value = '';
      updatePricePreview(this);
      return;
    }

    const formatted = formatCurrencyVND(rawDigits);
    this.value = formatted;
    restoreCursorPosition(this, formatted, digitsBeforeCursor);
    updatePricePreview(this);
  });

  input.addEventListener('focus', function() {
    if (this.value.endsWith('đ')) {
      setTimeout(() => {
        if (this.selectionStart === this.value.length) {
          const p = Math.max(0, this.value.length - 1);
          if (typeof this.setSelectionRange === 'function') {
            this.setSelectionRange(p, p);
          }
        }
      }, 0);
    }
    updatePricePreview(this);
  });

  input.addEventListener('blur', function() {
    const clean = this.value.replace(/\D/g, '');
    if (clean) {
      this.value = formatCurrencyVND(clean);
    }
    updatePricePreview(this);
  });

  updatePricePreview(input);
}

function initPriceFormatting() {
  if (typeof document === 'undefined') return;
  const selectors = [
    '.price-format-input',
    '#edit-prod-price',
    '#edit-prod-oldprice',
    '#add-prod-price',
    '#standalone-edit-price',
    '#standalone-edit-oldprice'
  ];
  document.querySelectorAll(selectors.join(', ')).forEach(setupPriceInput);

  const standaloneForm = document.querySelector('.admin-standalone-edit-page form');
  if (standaloneForm) {
    const inputs = standaloneForm.querySelectorAll('input.admin-form-input');
    inputs.forEach(inp => {
      const parent = inp.closest('.admin-form-group');
      if (parent) {
        const label = parent.querySelector('.admin-form-label');
        if (label && /giá/i.test(label.textContent)) {
          setupPriceInput(inp);
        }
      }
    });
  }

  document.querySelectorAll('form').forEach(form => {
    if (form.dataset.priceResetBound) return;
    form.dataset.priceResetBound = 'true';
    form.addEventListener('reset', function() {
      setTimeout(() => {
        form.querySelectorAll('.price-format-input').forEach(inp => {
          updatePricePreview(inp);
        });
      }, 0);
    });
  });
}


// 9c. Customer VIP Detail Modal Logic & Registry
const CUSTOMER_DATA_REGISTRY = {
  'tuan': {
    name: 'Phạm Minh Tuấn',
    initials: 'PT',
    phone: '0977 888 999',
    email: 'minhtuan.pham@gmail.com',
    tier: 'HẠNG KIM CƯƠNG',
    tierClass: 'vip-badge-diamond',
    tierIcon: 'fa-gem',
    points: '3.120',
    spent: '15.200.000đ',
    ordersCount: '18 Đơn',
    address: '88 Nguyễn Huệ, P. Bến Nghé, Quận 1, TP.HCM',
    latestOrder: '#EB-8804 (1 Thùng 24 Lon Mix - 918.000đ)',
    joinDate: '15/01/2024',
    privileges: 'Miễn phí ship hỏa tốc + Chiết khấu 10%'
  },
  'an': {
    name: 'Nguyễn Văn An',
    initials: 'NA',
    phone: '0912 345 678',
    email: 'vanan.nguyen@gmail.com',
    tier: 'HẠNG KIM CƯƠNG',
    tierClass: 'vip-badge-diamond',
    tierIcon: 'fa-gem',
    points: '2.450',
    spent: '12.400.000đ',
    ordersCount: '15 Đơn',
    address: '45 Lê Duẩn, P. Bến Nghé, Quận 1, TP.HCM',
    latestOrder: '#EB-8801 (2x Monster, 2x Redbull - 126.000đ)',
    joinDate: '20/02/2024',
    privileges: 'Miễn phí ship hỏa tốc + Chiết khấu 10%'
  },
  'bich': {
    name: 'Trần Thị Bích',
    initials: 'TB',
    phone: '0988 765 432',
    email: 'bich.tran@gmail.com',
    tier: 'HẠNG VÀNG',
    tierClass: 'vip-badge-gold',
    tierIcon: 'fa-crown',
    points: '1.980',
    spent: '9.600.000đ',
    ordersCount: '11 Đơn',
    address: '120 Hai Bà Trưng, P. Đa Kao, Quận 1, TP.HCM',
    latestOrder: '#EB-8802 (4x Ultra White, 3x Redbull - 246.000đ)',
    joinDate: '10/04/2024',
    privileges: 'Chiết khấu 7% toàn bộ đơn hàng'
  },
  'nam': {
    name: 'Lê Hoàng Nam',
    initials: 'LN',
    phone: '0903 111 222',
    email: 'nam.lehoang@gmail.com',
    tier: 'HẠNG VÀNG',
    tierClass: 'vip-badge-gold',
    tierIcon: 'fa-crown',
    points: '1.540',
    spent: '7.800.000đ',
    ordersCount: '9 Đơn',
    address: '25 Lý Tự Trọng, P. Bến Nghé, Quận 1, TP.HCM',
    latestOrder: '#EB-8803 (2x Redbull Nắp Bật - 40.000đ)',
    joinDate: '05/06/2024',
    privileges: 'Chiết khấu 7% toàn bộ đơn hàng'
  },
  'my': {
    name: 'Vũ Thảo My',
    initials: 'VM',
    phone: '0934 555 666',
    email: 'thaomy.vu@gmail.com',
    tier: 'HẠNG BẠC',
    tierClass: 'vip-badge-silver',
    tierIcon: 'fa-medal',
    points: '1.120',
    spent: '5.400.000đ',
    ordersCount: '6 Đơn',
    address: '15 Nam Kỳ Khởi Nghĩa, Quận 1, TP.HCM',
    latestOrder: '#EB-8805 (3x Ultra Paradise, 3x Redbull - 198.000đ)',
    joinDate: '12/08/2024',
    privileges: 'Tích điểm đổi quà VIP độc quyền'
  },
  'long': {
    name: 'Hoàng Đức Long',
    initials: 'HL',
    phone: '0938 222 111',
    email: 'duclong.hoang@gmail.com',
    tier: 'HẠNG BẠC',
    tierClass: 'vip-badge-silver',
    tierIcon: 'fa-medal',
    points: '860',
    spent: '4.100.000đ',
    ordersCount: '5 Đơn',
    address: '77 Điện Biên Phủ, P. Đa Kao, Quận 1, TP.HCM',
    latestOrder: '#EB-8806 (2x Sting Dâu Tây Đỏ - 24.000đ)',
    joinDate: '28/08/2024',
    privileges: 'Tích điểm đổi quà VIP độc quyền'
  }
};

function openCustomerDetailModal(customerKey) {
  let data = (typeof CUSTOMER_DATA_REGISTRY !== 'undefined' && CUSTOMER_DATA_REGISTRY[customerKey]) ? CUSTOMER_DATA_REGISTRY[customerKey] : null;
  if (!data && typeof customerKey === 'string') {
    try {
      const customUsers = JSON.parse(localStorage.getItem('admin_custom_users') || '[]');
      const matched = customUsers.find(u => u.id === customerKey || u.fullname === customerKey || u.username === customerKey);
      if (matched) {
        data = {
          name: matched.fullname,
          tier: (matched.role || 'user').toUpperCase(),
          tierClass: 'vip-badge-silver',
          tierIcon: 'fa-user',
          initials: matched.fullname.split(' ').filter(Boolean).map(w => w[0]).slice(-2).join('').toUpperCase() || 'ND',
          points: '0',
          spent: matched.spent || '0đ',
          ordersCount: matched.orders || '0 Đơn',
          phone: matched.phone || '0938.222.111',
          email: matched.email || 'user@energyboost.vn',
          address: 'Chưa cập nhật địa chỉ',
          latestOrder: 'Chưa có đơn hàng (Thành viên mới)',
          joinDate: matched.createdAt || new Date().toLocaleDateString('vi-VN'),
          privileges: 'Ưu đãi thành viên mới'
        };
      }
    } catch (e) {}
  }
  if (!data) {
    data = (typeof CUSTOMER_DATA_REGISTRY !== 'undefined' && CUSTOMER_DATA_REGISTRY['tuan']) || {};
  }
  
  const elAvatar = document.getElementById('vip-modal-avatar');
  const elName = document.getElementById('vip-modal-name');
  const elBadge = document.getElementById('vip-modal-badge');
  const elPoints = document.getElementById('vip-modal-points');
  const elSpent = document.getElementById('vip-modal-spent');
  const elOrders = document.getElementById('vip-modal-orders');
  const elPhone = document.getElementById('vip-modal-phone');
  const elEmail = document.getElementById('vip-modal-email');
  const elAddress = document.getElementById('vip-modal-address');
  const elLatest = document.getElementById('vip-modal-latest-order');
  const elJoin = document.getElementById('vip-modal-joindate');
  const elPrivilege = document.getElementById('vip-modal-privilege');
  const elBtn = document.getElementById('vip-modal-gift-btn');

  if (elAvatar) elAvatar.textContent = data.initials;
  if (elName) elName.textContent = data.name;
  if (elBadge) {
    elBadge.className = data.tierClass;
    elBadge.innerHTML = `<i class="fas ${data.tierIcon}"></i> ${data.tier}`;
  }
  if (elPoints) elPoints.textContent = data.points;
  if (elSpent) elSpent.textContent = data.spent;
  if (elOrders) elOrders.textContent = data.ordersCount;
  if (elPhone) elPhone.textContent = data.phone;
  if (elEmail) elEmail.textContent = data.email;
  if (elAddress) elAddress.textContent = data.address;
  if (elLatest) {
    const latestText = data.latestOrder || '';
    const match = latestText.match(/^(#EB-\d+)(.*)$/);
    if (match) {
      elLatest.innerHTML = `<a href="order-detail.html" style="color: var(--primary); text-decoration: underline;" title="Xem chi tiết đơn hàng ${match[1]}">${match[1]}</a>${match[2]}`;
    } else {
      elLatest.textContent = latestText;
    }
  }
  if (elJoin) elJoin.textContent = data.joinDate;
  if (elPrivilege) elPrivilege.textContent = data.privileges;
  if (elBtn) {
    elBtn.onclick = function() {
      showToast('Đã gửi voucher tri ân VIP tới ' + data.name + '!', 'success');
      closeAdminModal('modal-customer-detail');
    };
  }

  openAdminModal('modal-customer-detail');
}

// 9d. Mock Order Database & Routing Logic
const MOCK_ORDER_DATABASE = {
  'EB-8801': {
    id: 'EB-8801',
    code: 'EB-8801',
    customerName: 'Nguyễn Văn An',
    phone: '0912 345 678',
    address: '45 Lê Duẩn, P. Bến Nghé, Quận 1, TP.HCM',
    date: '02/10/2026 14:30',
    status: 'ĐÃ GIAO (THÀNH CÔNG)',
    statusClass: 'success',
    paymentMethod: 'VietQR',
    shippingMethod: 'Giao Hỏa Tốc (2H Nội Thành)',
    notes: 'Giao giờ hành chính, gọi trước 15 phút',
    items: [
      {
        name: 'Monster Energy Original 355ml',
        desc: 'Lon Sleek 355ml - Nhập khẩu chính hãng',
        img: '../assets/images/monster/original.webp',
        qty: 2,
        price: '45.000đ',
        total: '90.000đ'
      },
      {
        name: 'Redbull Original 250ml',
        desc: 'Lon lùn 250ml - Kẽm & Vitamin Thái Lan',
        img: '../assets/images/redbull/redbull-original.webp',
        qty: 2,
        price: '18.000đ',
        total: '36.000đ'
      }
    ],
    subtotal: '126.000đ',
    shippingFee: '0đ (Miễn phí)',
    discount: '0đ',
    totalAmount: '126.000đ'
  },
  'EB-8802': {
    id: 'EB-8802',
    code: 'EB-8802',
    customerName: 'Trần Thị Bình',
    phone: '0988 123 456',
    address: '128 Hai Bà Trưng, P. Tân Định, Quận 1, TP.HCM',
    date: '02/10/2026 11:15',
    status: 'ĐÃ XÁC NHẬN',
    statusClass: 'warning',
    paymentMethod: 'COD',
    shippingMethod: 'Giao hàng tiêu chuẩn (Tiết kiệm)',
    notes: 'Gọi trước khi tới giao hàng',
    items: [
      {
        name: 'Monster Energy Ultra White 355ml',
        desc: 'Lon Sleek 355ml - Không đường Zero Calorie',
        img: '../assets/images/monster/ultra-white.webp',
        qty: 4,
        price: '55.000đ',
        total: '220.000đ'
      },
      {
        name: 'Redbull Krating Daeng Thái 250ml',
        desc: 'Lon lùn nắp giật nhập khẩu Thái Lan',
        img: '../assets/images/redbull/redbull-thai.webp',
        qty: 3,
        price: '40.000đ',
        total: '120.000đ'
      }
    ],
    subtotal: '340.000đ',
    shippingFee: '0đ (Miễn phí)',
    discount: '0đ',
    totalAmount: '340.000đ'
  },
  'EB-8803': {
    id: 'EB-8803',
    code: 'EB-8803',
    customerName: 'Lê Hoàng Nam',
    phone: '0903 789 012',
    address: '72 Nguyễn Huệ, P. Bến Nghé, Quận 1, TP.HCM',
    date: '01/10/2026 16:45',
    status: 'CHƯA XÁC NHẬN',
    statusClass: 'info',
    paymentMethod: 'VietQR',
    shippingMethod: 'Giao Hỏa Tốc (2H Nội Thành)',
    notes: 'Để trước cửa phòng trọ nếu đi vắng',
    items: [
      {
        name: 'Bộ 7 Lon Nước Tăng Lực VIP',
        desc: 'Tặng kèm Bình Giữ Nhiệt Monster trị giá 280.000đ',
        img: '../assets/images/monster/original.webp',
        qty: 1,
        price: '918.000đ',
        total: '918.000đ'
      }
    ],
    subtotal: '918.000đ',
    shippingFee: '0đ (Miễn phí)',
    discount: '0đ',
    totalAmount: '918.000đ'
  },
  'EB-8804': {
    id: 'EB-8804',
    code: 'EB-8804',
    customerName: 'Phạm Minh Đức',
    phone: '0977 456 789',
    address: '56 Trần Hưng Đạo, P. Phạm Ngũ Lão, Quận 1, TP.HCM',
    date: '01/10/2026 10:20',
    status: 'ĐÃ GIAO (THÀNH CÔNG)',
    statusClass: 'success',
    paymentMethod: 'VietQR',
    shippingMethod: 'Giao hàng tiêu chuẩn',
    notes: 'Đóng gói kỹ làm quà tặng hội thảo esport',
    items: [
      {
        name: 'Monster Energy Ultra Paradise 355ml',
        desc: 'Hương kiwi chanh thanh mát, không calo',
        img: '../assets/images/monster/ultra-paradise.webp',
        qty: 4,
        price: '55.000đ',
        total: '220.000đ'
      },
      {
        name: 'Sting Dâu Tây Đỏ 330ml',
        desc: 'Lon cao Sleek 330ml năng lượng sảng khoái',
        img: '../assets/images/sting/sting-dau.webp',
        qty: 2,
        price: '10.000đ',
        total: '20.000đ'
      }
    ],
    subtotal: '240.000đ',
    shippingFee: '0đ (Miễn phí)',
    discount: '0đ',
    totalAmount: '240.000đ'
  },
  'EB-8805': {
    id: 'EB-8805',
    code: 'EB-8805',
    customerName: 'Vũ Hải Đăng',
    phone: '0932 654 987',
    address: '89 Cách Mạng Tháng 8, P. Võ Thị Sáu, Quận 3, TP.HCM',
    date: '30/09/2026 15:10',
    status: 'ĐÃ XÁC NHẬN',
    statusClass: 'warning',
    paymentMethod: 'COD',
    shippingMethod: 'Giao hàng hỏa tốc',
    notes: 'Giao nhanh trước 17h chiều',
    items: [
      {
        name: 'Redbull Nắp Bật 250ml',
        desc: 'Lon vàng nắp bật cao cấp tiện lợi',
        img: '../assets/images/redbull/redbull-lon-vua.webp',
        qty: 3,
        price: '40.000đ',
        total: '120.000đ'
      },
      {
        name: 'Sting Vàng Gold Lon 330ml',
        desc: 'Hương vị nhân sâm tăng cường sinh lực',
        img: '../assets/images/sting/sting-gold.webp',
        qty: 2,
        price: '15.000đ',
        total: '30.000đ'
      }
    ],
    subtotal: '150.000đ',
    shippingFee: '0đ (Miễn phí)',
    discount: '0đ',
    totalAmount: '150.000đ'
  },
  'EB-8806': {
    id: 'EB-8806',
    code: 'EB-8806',
    customerName: 'Đỗ Kim Ngân',
    phone: '0918 321 654',
    address: '15 Võ Văn Tần, P. Võ Thị Sáu, Quận 3, TP.HCM',
    date: '29/09/2026 09:00',
    status: 'ĐÃ GIAO (THÀNH CÔNG)',
    statusClass: 'success',
    paymentMethod: 'VietQR',
    shippingMethod: 'Giao hàng tiêu chuẩn',
    notes: 'Đơn hàng VIP ưu tiên xử lý',
    items: [
      {
        name: 'Monster Energy Ultra Punk Punch 355ml',
        desc: 'Vị trái cây nhiệt đới hoang dã năng động',
        img: '../assets/images/monster/ultra-punk-punch.webp',
        qty: 2,
        price: '48.000đ',
        total: '96.000đ'
      }
    ],
    subtotal: '96.000đ',
    shippingFee: '0đ (Miễn phí)',
    discount: '0đ',
    totalAmount: '96.000đ'
  },
  'EB-2026': {
    id: 'EB-2026',
    code: 'EB-2026',
    customerName: 'Thuận Trần',
    phone: '0912.888.999',
    address: '88 Nguyễn Huệ, Bến Nghé, Quận 1, TP.HCM',
    date: '03/10/2026 09:30 AM',
    status: 'ĐANG GIAO (2H)',
    statusClass: 'warning',
    paymentMethod: 'COD khi nhận',
    shippingMethod: 'Giao Hỏa Tốc (2H)',
    notes: 'Giao hỏa tốc 2H, giao tận tay người nhận',
    items: [
      {
        name: 'Monster Energy Original 355ml',
        desc: 'Lon Sleek 355ml - Nhập khẩu chính hãng',
        img: '../assets/images/monster/original.webp',
        qty: 2,
        price: '45.000đ',
        total: '90.000đ'
      },
      {
        name: 'Redbull Original 250ml',
        desc: 'Lon lùn 250ml - Năng lượng bứt phá',
        img: '../assets/images/redbull/redbull-original.webp',
        qty: 2,
        price: '18.000đ',
        total: '36.000đ'
      }
    ],
    subtotal: '126.000đ',
    shippingFee: '0đ (Miễn phí)',
    discount: '0đ',
    totalAmount: '126.000đ'
  },
  'EB-2025': {
    id: 'EB-2025',
    code: 'EB-2025',
    customerName: 'Thuận Trần',
    phone: '0912.888.999',
    address: '88 Nguyễn Huệ, Bến Nghé, Quận 1, TP.HCM',
    date: '28/09/2026 15:45 PM',
    status: 'ĐÃ NHẬN',
    statusClass: 'success',
    paymentMethod: 'Chuyển khoản VietQR',
    shippingMethod: 'Giao hàng tiêu chuẩn',
    notes: 'Kèm bình giữ nhiệt quà tặng sự kiện',
    items: [
      {
        name: 'Bộ 7 Lon Nước Tăng Lực VIP',
        desc: 'Tặng Bình Giữ Nhiệt Monster (Trị giá 280K)',
        img: '../assets/images/monster/original.webp',
        qty: 1,
        price: '918.000đ',
        total: '918.000đ'
      }
    ],
    subtotal: '918.000đ',
    shippingFee: '0đ (Miễn phí)',
    discount: '0đ',
    totalAmount: '918.000đ'
  },
  'EB-2024': {
    id: 'EB-2024',
    code: 'EB-2024',
    customerName: 'Thuận Trần',
    phone: '0912.888.999',
    address: '88 Nguyễn Huệ, Bến Nghé, Quận 1, TP.HCM',
    date: '20/09/2026 11:15 AM',
    status: 'ĐÃ NHẬN',
    statusClass: 'success',
    paymentMethod: 'Ví MoMo',
    shippingMethod: 'Giao hàng tiêu chuẩn',
    notes: 'Khách hàng thành viên thân thiết',
    items: [
      {
        name: 'Redbull Nắp Bật 250ml',
        desc: 'Thương hiệu: Redbull Thái Lan',
        img: '../assets/images/redbull/redbull-lon-vua.webp',
        qty: 3,
        price: '20.000đ',
        total: '60.000đ'
      }
    ],
    subtotal: '60.000đ',
    shippingFee: '0đ (Miễn phí)',
    discount: '0đ',
    totalAmount: '60.000đ'
  }
};

// Index order database with aliases without 'EB-' prefix
Object.keys(MOCK_ORDER_DATABASE).forEach(k => {
  const short = k.replace(/^EB-/, '');
  if (!MOCK_ORDER_DATABASE[short]) {
    MOCK_ORDER_DATABASE[short] = MOCK_ORDER_DATABASE[k];
  }
});
window.MOCK_ORDER_DATABASE = MOCK_ORDER_DATABASE;

// 9d. Order Detail Routing Logic
function openOrderDetailModal(orderId) {
  const code = (orderId || 'EB-8801').replace(/^#/, '');
  window.location.href = 'order-detail.html?id=' + encodeURIComponent(code);
}
window.openOrderDetailModal = openOrderDetailModal;

// 9e. Populate Order Detail Page (Dành cho order-detail.html của Admin & Khách Hàng)
function initOrderDetailPage(role) {
  const params = new URLSearchParams(window.location.search);
  const rawId = params.get('id') || (role === 'admin' ? 'EB-8801' : 'EB-2026');
  const cleanId = (rawId || '').toUpperCase().replace(/^#/, '');
  const orderId = cleanId.startsWith('EB-') ? cleanId : ('EB-' + cleanId);
  const shortId = cleanId.replace(/^EB-/, '');

  const db = (typeof MOCK_ORDER_DATABASE !== 'undefined' && MOCK_ORDER_DATABASE) || window.MOCK_ORDER_DATABASE || {};
  const order = db[cleanId] || db[orderId] || db[shortId] || (role === 'admin' ? db['EB-8801'] : db['EB-2026']) || Object.values(db)[0];

  if (!order) return;

  const displayCode = order.code || order.id || cleanId;
  const customerName = (role !== 'admin' && typeof getLoggedUser === 'function' && getLoggedUser())
    ? getLoggedUser()
    : order.customerName;

  // Title & Breadcrumb
  document.title = (role === 'admin' ? 'Chi Tiết Đơn Hàng #' : 'Chi Tiết Đơn Hàng #') + displayCode + (role === 'admin' ? ' - Energy Boost Admin' : ' - Energy Boost');

  const breadcrumbEl = document.getElementById('order-breadcrumb-id');
  if (breadcrumbEl) breadcrumbEl.textContent = '#' + displayCode;

  // #order-detail-id & #order-detail-code
  const idEl = document.getElementById('order-detail-id');
  if (idEl) idEl.textContent = '#' + displayCode;
  const codeEl = document.getElementById('order-detail-code');
  if (codeEl) codeEl.textContent = '#' + displayCode;

  // #order-detail-date
  const dateEl = document.getElementById('order-detail-date');
  if (dateEl) dateEl.textContent = order.date;

  // #order-detail-status
  const statusEl = document.getElementById('order-detail-status');
  if (statusEl) {
    statusEl.className = 'badge-status ' + (order.statusClass || 'info');
    let icon = '<i class="fas fa-clock"></i> ';
    if (order.statusClass === 'success') icon = '<i class="fas fa-check-circle"></i> ';
    else if (order.statusClass === 'warning') icon = '<i class="fas fa-truck-fast"></i> ';
    else if (order.statusClass === 'danger') icon = '<i class="fas fa-circle-xmark"></i> ';
    statusEl.innerHTML = icon + order.status;
  }

  // #order-detail-customer
  const custEl = document.getElementById('order-detail-customer');
  if (custEl) custEl.textContent = customerName;

  // #order-detail-phone
  const phoneEl = document.getElementById('order-detail-phone');
  if (phoneEl) phoneEl.textContent = order.phone;

  // #order-detail-address
  const addrEl = document.getElementById('order-detail-address');
  if (addrEl) addrEl.textContent = order.address;

  // #order-detail-payment
  const payEl = document.getElementById('order-detail-payment');
  if (payEl) payEl.textContent = order.paymentMethod;

  // #order-detail-shipping
  const shipEl = document.getElementById('order-detail-shipping');
  if (shipEl) shipEl.textContent = order.shippingMethod;

  // #order-detail-notes & #order-detail-note
  const noteEl = document.getElementById('order-detail-notes') || document.getElementById('order-detail-note');
  if (noteEl) {
    noteEl.textContent = order.notes || order.note || 'Giao hàng ướp lạnh, gọi trước khi đến 15 phút';
  }

  // #order-items-tbody
  const tbodyEl = document.getElementById('order-items-tbody');
  if (tbodyEl && Array.isArray(order.items)) {
    const isSubdir = typeof window !== 'undefined' && (window.location.pathname.includes('/pages/') || window.location.pathname.includes('/admin/'));
    const tableEl = tbodyEl.closest('table');
    const has5Cols = tableEl && tableEl.querySelectorAll('thead th').length === 5;
    tbodyEl.innerHTML = order.items.map(item => {
      let imgSrc = item.img || '';
      if (imgSrc && !imgSrc.startsWith('http') && !imgSrc.startsWith('data:')) {
        if (isSubdir) {
          if (!imgSrc.startsWith('../')) imgSrc = '../' + imgSrc;
        } else {
          imgSrc = imgSrc.replace(/^\.\.\//, '');
        }
      }
      if (has5Cols) {
        return `<tr>
        <td>
          <div style="display: flex; align-items: center; gap: 12px;">
            <img src="${imgSrc}" alt="${item.name}" style="width: 36px; height: 46px; object-fit: contain; border-radius: 4px; background: rgba(255, 255, 255, 0.03); padding: 2px;" />
            <strong style="color: #FFF;">${item.name}</strong>
          </div>
        </td>
        <td style="color: var(--text-muted); font-size: 0.88rem;">${item.desc || 'Tiêu chuẩn'}</td>
        <td style="text-align: right; color: var(--text-muted);">${item.price}</td>
        <td style="text-align: center; font-weight: 600;">${item.qty}</td>
        <td style="text-align: right; color: var(--primary); font-weight: 700;">${item.total}</td>
      </tr>`;
      }
      return `<tr>
        <td>
          <div style="display: flex; align-items: center; gap: 12px;">
            <img src="${imgSrc}" alt="${item.name}" style="width: 36px; height: 46px; object-fit: contain; border-radius: 4px; background: rgba(255, 255, 255, 0.03); padding: 2px;" />
            <div>
              <strong style="color: #FFF;">${item.name}</strong><br/>
              <small style="color: var(--text-muted);">${item.desc || ''}</small>
            </div>
          </div>
        </td>
        <td style="text-align: center; font-weight: 600;">${item.qty}</td>
        <td style="text-align: right; color: var(--text-muted);">${item.price}</td>
        <td style="text-align: right; color: var(--primary); font-weight: 700;">${item.total}</td>
      </tr>`;
    }).join('');
  }

  // #order-detail-subtotal
  const subtotalEl = document.getElementById('order-detail-subtotal');
  if (subtotalEl) subtotalEl.textContent = order.subtotal;

  // #order-detail-shipping-fee
  const shippingFeeEl = document.getElementById('order-detail-shipping-fee');
  if (shippingFeeEl) shippingFeeEl.textContent = order.shippingFee;

  // #order-detail-discount
  const discountEl = document.getElementById('order-detail-discount');
  if (discountEl) discountEl.textContent = order.discount;

  // #order-detail-total
  const totalEl = document.getElementById('order-detail-total');
  if (totalEl) totalEl.textContent = order.totalAmount;

  if (typeof updateOrderTimelineFromStatus === 'function') updateOrderTimelineFromStatus();
  if (typeof updateCustomerOrderTimeline === 'function') updateCustomerOrderTimeline();
}
window.initOrderDetailPage = initOrderDetailPage;

// Tự động khởi tạo Order Detail Page nếu tìm thấy ID trên DOM
if (typeof document !== 'undefined') {
  const triggerOrderDetail = () => {
    if (document.getElementById('order-detail-id') || document.getElementById('order-items-tbody')) {
      const isCurrentAdmin = window.location.pathname.includes('/admin/');
      initOrderDetailPage(isCurrentAdmin ? 'admin' : 'customer');
    }
  };
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', triggerOrderDetail);
  } else {
    triggerOrderDetail();
  }
}


// 10. Order History Live Filter Pill Tabs (Vô hiệu hóa ẩn dòng, giữ trạng thái active & thông báo Toast)
function filterOrderList(status, btn) {
  const group = btn ? btn.closest('.order-filter-group') : null;
  if (group) {
    group.querySelectorAll('.filter-pill').forEach(b => {
      b.classList.remove('active');
      b.setAttribute('aria-selected', 'false');
    });
    btn.classList.add('active');
    btn.setAttribute('aria-selected', 'true');
  }

  // Vô hiệu hóa việc ẩn dòng đơn hàng (luôn giữ hiển thị toàn bộ 3 đơn hàng)
  const rows = document.querySelectorAll('#orders-tbody tr');
  rows.forEach(row => {
    row.style.display = '';
  });

  const msg = status === 'all' 
    ? 'Đang hiển thị tất cả 3 đơn hàng' 
    : (status === 'shipping' ? 'Đang lọc 1 đơn hàng giao hỏa tốc (#EB-2026)' : 'Đang lọc 2 đơn hàng đã nhận thành công (#EB-2025, #EB-2024)');
  showToast(msg, 'info');
}

// 11. Standalone Admin Product Edit Form Save
function saveStandaloneEdit(e, productName) {
  if (e && e.preventDefault) e.preventDefault();
  const name = productName || 'Sản phẩm Redbull';
  showToast('Đã lưu thành công các thay đổi cho "' + name + '"!', 'success');
}

// 12. Dynamic Quantity Control Handler (.qty-control)
document.addEventListener('click', function(e) {
  const btn = e.target.closest('.qty-btn');
  if (!btn) return;
  const control = btn.closest('.qty-control');
  if (!control) return;
  const input = control.querySelector('.qty-input');
  if (!input) return;
  let val = parseInt(input.value, 10) || 1;
  const text = btn.textContent.trim();
  if (text === '+') {
    input.value = Math.min(99, val + 1);
  } else if (text === '-') {
    input.value = Math.max(1, val - 1);
  }
});

// ==========================================================================
// 13. STATIC SEARCH DROPDOWN & ADVANCED SEARCH (RUBRIC COMPLIANCE)
// ==========================================================================
const STATIC_PRODUCTS_CATALOG = [
  { id: 'mn-1', name: 'Monster Energy Original 355ml', brand: 'Monster Energy', brandKey: 'monster', price: '45.000đ', priceKey: '20to50', image: 'assets/images/monster/original.webp', detailUrl: 'pages/product-detail.html', tag: 'HÀ LAN', keywords: 'energy boost nước tăng lực hà lan classic đen green truyền thống' },
  { id: 'mn-2', name: 'Monster Zero Ultra White 500ml', brand: 'Monster Energy', brandKey: 'monster', price: '48.000đ', priceKey: '20to50', image: 'assets/images/monster/ultra-white.webp', detailUrl: 'pages/product-detail.html', tag: 'ZERO SUGAR', keywords: 'energy boost nước tăng lực zero sugar không đường trắng ultra white calo thấp' },
  { id: 'mn-3', name: 'Monster Ultra Paradise 500ml', brand: 'Monster Energy', brandKey: 'monster', price: '48.000đ', priceKey: '20to50', image: 'assets/images/monster/ultra-paradise.webp', detailUrl: 'pages/product-detail.html', tag: 'KIWI CHANH', keywords: 'energy boost nước tăng lực kiwi chanh dưa leo xanh lá paradise ultra zero' },
  { id: 'mn-4', name: 'Monster Ultra Punk Punch 500ml', brand: 'Monster Energy', brandKey: 'monster', price: '50.000đ', priceKey: '20to50', image: 'assets/images/monster/ultra-punk-punch.webp', detailUrl: 'pages/product-detail.html', tag: 'FRUIT PUNCH', keywords: 'energy boost nước tăng lực fruit punch hoa quả trái cây nhiệt đới hồng tím punk' },
  { id: 'rb-1', name: 'Nước Tăng Lực Redbull Original 250ml', brand: 'Redbull Thái Lan', brandKey: 'redbull', price: '18.000đ', priceKey: 'under20', image: 'assets/images/redbull/redbull-original.webp', detailUrl: 'pages/product-detail-redbull.html', tag: 'ORIGINAL', keywords: 'energy boost nước tăng lực bò húc bò cụng original vàng truyền thống thái lan' },
  { id: 'rb-2', name: 'Nước Tăng Lực Redbull Thái Lan 250ml', brand: 'Redbull Thái Lan', brandKey: 'redbull', price: '18.000đ', priceKey: 'under20', image: 'assets/images/redbull/redbull-thai.webp', detailUrl: 'pages/product-detail-redbull-thai.html', tag: 'THÁI LAN', keywords: 'energy boost nước tăng lực krating daeng thái lan nhập khẩu đậm đà 250ml' },
  { id: 'rb-3', name: 'Nước Tăng Lực Redbull Nắp Bật 250ml', brand: 'Redbull Thái Lan', brandKey: 'redbull', price: '20.000đ', priceKey: '20to50', image: 'assets/images/redbull/redbull-lon-vua.webp', detailUrl: 'pages/product-detail-redbull-lonvua.html', tag: 'NẮP BẬT', keywords: 'energy boost nước tăng lực sleek can nắp bật tiện lợi cao cấp lon lùn' },
  { id: 'st-1', name: 'Nước Tăng Lực Sting Dâu Tây Đỏ 330ml', brand: 'Sting PepsiCo', brandKey: 'sting', price: '12.000đ', priceKey: 'under20', image: 'assets/images/sting/sting-dau.webp', detailUrl: 'pages/product-detail-sting.html', tag: 'DÂU ĐỎ', keywords: 'energy boost nước tăng lực sting dâu tây đỏ pepsico ga sảng khoái' },
  { id: 'st-2', name: 'Nước Tăng Lực Sting Vàng Sleek 330ml', brand: 'Sting PepsiCo', brandKey: 'sting', price: '12.000đ', priceKey: 'under20', image: 'assets/images/sting/sting-gold.webp', detailUrl: 'pages/product-detail-sting.html', tag: 'NHÂN SÂM', keywords: 'energy boost nước tăng lực sting vàng nhân sâm ginseng sleek pepsico' },
  { id: 'st-3', name: 'Nước Tăng Lực Sting Blue Sleek 320ml', brand: 'Sting PepsiCo', brandKey: 'sting', price: '13.000đ', priceKey: 'under20', image: 'assets/images/sting/sting-vietquat.webp', detailUrl: 'pages/product-detail-sting.html', tag: 'BLUE XANH', keywords: 'energy boost nước tăng lực sting blue việt quất xanh dương sleek mát lạnh' }
];

function openSearchDropdown() {
  const dropdown = document.getElementById('search-dropdown-menu');
  if (dropdown) dropdown.classList.add('is-open');
}

function closeSearchDropdown() {
  const dropdown = document.getElementById('search-dropdown-menu');
  if (dropdown) dropdown.classList.remove('is-open');
}

function toggleSearchDropdown() {
  const dropdown = document.getElementById('search-dropdown-menu');
  if (dropdown) {
    dropdown.classList.toggle('is-open');
  }
}

function openSidebarSearchDropdown() {
  const dropdown = document.getElementById('sidebar-search-dropdown-menu');
  if (dropdown) dropdown.classList.add('is-open');
}

function closeSidebarSearchDropdown() {
  const dropdown = document.getElementById('sidebar-search-dropdown-menu');
  if (dropdown) dropdown.classList.remove('is-open');
}

function toggleSidebarSearchDropdown() {
  const dropdown = document.getElementById('sidebar-search-dropdown-menu');
  if (dropdown) {
    dropdown.classList.toggle('is-open');
  }
}

function openAdvancedSearchModal() {
  const modal = document.getElementById('modal-adv-search');
  if (modal) {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  } else {
    // Nếu trang hiện tại không có modal (như product-detail), điều hướng tới trang kết quả tìm kiếm
    go('pages/search-results.html');
  }
}

function closeAdvancedSearchModal() {
  const modal = document.getElementById('modal-adv-search');
  if (modal) {
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }
  closeAdvSuggestions();
}

function handleAdvancedSearch(e) {
  if (e && e.preventDefault) e.preventDefault();
  closeAdvancedSearchModal();
  const kwEl = document.getElementById('adv-search-keyword');
  const brandEl = document.getElementById('adv-search-brand');
  const priceEl = document.getElementById('adv-search-price');

  const q = kwEl ? kwEl.value.trim() : '';
  const brand = brandEl ? brandEl.value : 'all';
  const price = priceEl ? priceEl.value : 'all';

  const brandLabels = { all: 'Tất cả thương hiệu', monster: 'Monster Energy', redbull: 'Redbull Thái Lan', sting: 'Sting PepsiCo' };
  const priceLabels = { all: 'Tất cả khoảng giá', under20: 'Dưới 20.000đ', '20to50': '20.000đ - 50.000đ', over50: 'Trên 50.000đ' };

  const criteria = [];
  if (q) criteria.push(`Từ khóa: "${q}"`);
  if (brand !== 'all') criteria.push(brandLabels[brand] || brand);
  if (price !== 'all') criteria.push(priceLabels[price] || price);

  const criteriaText = criteria.length > 0 ? criteria.join(' | ') : 'Tất cả sản phẩm';
  showToast(`Đã áp dụng bộ lọc nâng cao: ${criteriaText}`, 'success');
}

// 13b. Global Header Search Navigation (Enter or Search Button Click)
function executeHeaderSearch(query) {
  const q = (query || '').trim();
  const isSearchPage = window.location.pathname.includes('search-results.html') || !!document.getElementById('search-results-grid');
  if (isSearchPage) {
    const params = new URLSearchParams(window.location.search);
    if (q) params.set('q', q);
    else params.delete('q');
    try {
      window.history.pushState({}, '', window.location.pathname + (params.toString() ? '?' + params.toString() : ''));
    } catch (err) {}
    const sidebarKw = document.getElementById('search-filter-keyword');
    if (sidebarKw) sidebarKw.value = q;
    document.querySelectorAll('.search-input').forEach(inp => { if (inp) inp.value = q; });
    renderSearchResults([], q, 1);
    showToast('Đã tìm thấy 1 sản phẩm phù hợp!', 'info');
    return;
  }
  go('pages/search-results.html' + (q ? '?q=' + encodeURIComponent(q) : ''));
}

// 13c. Dashboard Sidebar Filter Submissions
function filterDashboardInPlace(keyword, brand, price) {
  const cleanKw = cleanSearchQuery(keyword);
  const words = cleanKw.split(/\s+/).filter(Boolean);

  const sections = [
    { id: 'monster-products', brandKey: 'monster' },
    { id: 'redbull-products', brandKey: 'redbull' },
    { id: 'sting-products', brandKey: 'sting' }
  ];

  let totalVisible = 0;

  sections.forEach(sec => {
    const secEl = document.getElementById(sec.id);
    if (!secEl) return;

    const brandMatches = (brand === 'all' || brand === sec.brandKey);
    const cards = secEl.querySelectorAll('.product-card');
    let sectionVisibleCount = 0;

    cards.forEach(card => {
      if (!brandMatches) {
        card.style.display = 'none';
        return;
      }

      const priceEl = card.querySelector('.price-current');
      const priceText = priceEl ? priceEl.textContent.replace(/[^\d]/g, '') : '0';
      const priceNum = parseInt(priceText, 10) || 0;

      let priceMatches = true;
      if (price === 'under20') priceMatches = priceNum < 20000;
      else if (price === '20to50') priceMatches = (priceNum >= 20000 && priceNum <= 50000);
      else if (price === 'over50') priceMatches = priceNum > 50000;

      const titleEl = card.querySelector('.product-title');
      const catEl = card.querySelector('.product-cat');
      const cardText = removeVietnameseTones(`${titleEl ? titleEl.textContent : ''} ${catEl ? catEl.textContent : ''} energy boost lon nước tăng lực`.toLowerCase());

      const kwMatches = words.length === 0 || words.every(w => cardText.includes(w));

      if (priceMatches && kwMatches) {
        card.style.display = '';
        sectionVisibleCount++;
        totalVisible++;
      } else {
        card.style.display = 'none';
      }
    });

    if (sectionVisibleCount > 0) {
      secEl.style.display = '';
    } else {
      secEl.style.display = 'none';
    }
  });

  const productsCol = document.querySelector('.dashboard-products-column');
  let emptyState = document.getElementById('dashboard-filter-empty');
  if (totalVisible === 0) {
    if (!emptyState && productsCol) {
      emptyState = document.createElement('div');
      emptyState.id = 'dashboard-filter-empty';
      emptyState.className = 'search-empty-state';
      emptyState.style.cssText = 'text-align: center; padding: 48px 20px; background: var(--bg-card); border: 1px dashed var(--border-color); border-radius: var(--radius-lg); margin-top: 10px;';
      emptyState.innerHTML = `
        <i class="fas fa-box-open" style="font-size: 3rem; color: var(--text-dim); margin-bottom: 16px;"></i>
        <h3 style="color: #FFF; font-size: 1.25rem; margin-bottom: 8px;">Không tìm thấy sản phẩm trên dashboard</h3>
        <p style="color: var(--text-muted); font-size: 0.9rem; max-width: 480px; margin: 0 auto 20px;">
          Không có sản phẩm nào phù hợp với bộ lọc hiện tại. Thử chọn thương hiệu khác hoặc nhấn Đặt lại.
        </p>
        <button type="button" class="btn-filter-apply" style="display: inline-flex; width: auto; padding: 10px 24px; margin: 0 auto;" onclick="resetDashboardFilter()">
          <i class="fas fa-rotate-left"></i> Xem tất cả sản phẩm
        </button>
      `;
      productsCol.appendChild(emptyState);
    } else if (emptyState) {
      emptyState.style.display = '';
    }
    showToast('Không có lon nước nào khớp với tiêu chí lọc!', 'warning');
  } else {
    if (emptyState) emptyState.style.display = 'none';
    showToast(`Đã tìm thấy ${totalVisible} sản phẩm phù hợp trên dashboard!`, 'success');
  }
}

function handleDashboardFilterSubmit(e, shouldNavigate = false) {
  if (e && e.preventDefault) e.preventDefault();
  const kwInput = document.getElementById('sidebar-filter-keyword');
  const keyword = kwInput ? kwInput.value.trim() : '';
  const brandEl = document.querySelector('input[name="sidebar-brand"]:checked');
  const brand = brandEl ? brandEl.value : 'all';
  const priceEl = document.querySelector('input[name="sidebar-price"]:checked');
  const price = priceEl ? priceEl.value : 'all';

  if (shouldNavigate) {
    const params = new URLSearchParams();
    if (keyword) params.set('q', keyword);
    if (brand && brand !== 'all') params.set('brand', brand);
    if (price && price !== 'all') params.set('price', price);

    const queryStr = params.toString();
    go('pages/search-results.html' + (queryStr ? '?' + queryStr : ''));
    return;
  }

  // Tắt tính năng ẩn/lọc sản phẩm trên DOM, giữ nguyên giao diện đầy đủ các lon nước và chỉ hiện thông báo Toast
  ['monster-products', 'redbull-products', 'sting-products'].forEach(id => {
    const secEl = document.getElementById(id);
    if (secEl) {
      secEl.style.display = '';
      secEl.querySelectorAll('.product-card').forEach(card => {
        card.style.display = '';
      });
    }
  });

  const emptyState = document.getElementById('dashboard-filter-empty');
  if (emptyState) emptyState.style.display = 'none';

  const brandLabels = { all: 'Tất cả thương hiệu', monster: 'Monster Energy', redbull: 'Redbull Thái Lan', sting: 'Sting PepsiCo' };
  const priceLabels = { all: 'Tất cả khoảng giá', under20: 'Dưới 20.000đ', '20to50': '20.000đ - 50.000đ', over50: 'Trên 50.000đ' };

  const criteria = [];
  if (keyword) criteria.push(`Từ khóa: "${keyword}"`);
  if (brand !== 'all') criteria.push(brandLabels[brand] || brand);
  if (price !== 'all') criteria.push(priceLabels[price] || price);

  const criteriaText = criteria.length > 0 ? criteria.join(' | ') : 'Tất cả sản phẩm';
  showToast(`Đã áp dụng bộ lọc: ${criteriaText}`, 'success');
}

function openSearchResultsFromDashboard() {
  handleDashboardFilterSubmit(null, true);
}

function resetDashboardFilter() {
  const kwInput = document.getElementById('sidebar-filter-keyword');
  if (kwInput) kwInput.value = '';
  const allBrand = document.querySelector('input[name="sidebar-brand"][value="all"]');
  if (allBrand) allBrand.checked = true;
  const allPrice = document.querySelector('input[name="sidebar-price"][value="all"]');
  if (allPrice) allPrice.checked = true;

  ['monster-products', 'redbull-products', 'sting-products'].forEach(id => {
    const secEl = document.getElementById(id);
    if (secEl) {
      secEl.style.display = '';
      secEl.querySelectorAll('.product-card').forEach(card => {
        card.style.display = '';
      });
    }
  });

  const emptyState = document.getElementById('dashboard-filter-empty');
  if (emptyState) emptyState.style.display = 'none';

  showToast('Đã đặt lại bộ lọc tìm kiếm nâng cao (hiển thị đủ 10 lon)!', 'info');
}

// 13d. Search Results Page Logic
function removeVietnameseTones(str) {
  if (!str) return '';
  str = str.replace(/à|á|ạ|ả|ã|â|ầ|ấ|ậ|ẩ|ẫ|ă|ằ|ắ|ặ|ẳ|ẵ/g, 'a');
  str = str.replace(/è|é|ẹ|ẻ|ẽ|ê|ề|ế|ệ|ể|ễ/g, 'e');
  str = str.replace(/ì|í|ị|ỉ|ĩ/g, 'i');
  str = str.replace(/ò|ó|ọ|ỏ|õ|ô|ồ|ố|ộ|ổ|ỗ|ơ|ờ|ớ|ợ|ở|ỡ/g, 'o');
  str = str.replace(/ù|ú|ụ|ủ|ũ|ư|ừ|ứ|ự|ử|ữ/g, 'u');
  str = str.replace(/ỳ|ý|ỵ|ỷ|ỹ/g, 'y');
  str = str.replace(/đ/g, 'd');
  str = str.replace(/À|Á|Ạ|Ả|Ã|Â|Ầ|Ấ|Ậ|Ẩ|Ẫ|Ă|Ằ|Ắ|Ặ|Ẳ|Ẵ/g, 'A');
  str = str.replace(/È|É|Ẹ|Ẻ|Ẽ|Ê|Ề|Ế|Ệ|Ể|Ễ/g, 'E');
  str = str.replace(/Ì|Í|Ị|Ỉ|Ĩ/g, 'I');
  str = str.replace(/Ò|Ó|Ọ|Ỏ|Õ|Ô|Ồ|Ố|Ộ|Ổ|Ỗ|Ơ|Ờ|Ớ|Ợ|Ở|Ỡ/g, 'O');
  str = str.replace(/Ù|Ú|Ụ|Ủ|Ũ|Ư|Ừ|Ứ|Ự|Ử|Ữ/g, 'U');
  str = str.replace(/Ỳ|Ý|Ỵ|Ỷ|Ỹ/g, 'Y');
  str = str.replace(/Đ/g, 'D');
  return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}

function cleanSearchQuery(str) {
  if (!str) return '';
  return removeVietnameseTones(str.toLowerCase())
    .replace(/^[\s\/\\]+/, '')
    .trim();
}

function filterProducts(keyword, brand, price) {
  const cleanKw = cleanSearchQuery(keyword);
  return STATIC_PRODUCTS_CATALOG.filter(prod => {
    if (brand && brand !== 'all' && prod.brandKey !== brand) {
      return false;
    }
    if (price && price !== 'all' && prod.priceKey !== price) {
      return false;
    }
    if (cleanKw) {
      const normName = removeVietnameseTones(prod.name.toLowerCase());
      const normBrand = removeVietnameseTones(prod.brand.toLowerCase());
      const normTag = removeVietnameseTones((prod.tag || '').toLowerCase());
      const normKwMeta = removeVietnameseTones((prod.keywords || '').toLowerCase());
      const searchable = `${normName} ${normBrand} ${normTag} ${normKwMeta} energy boost`;
      const words = cleanKw.split(/\s+/).filter(Boolean);
      const matchesAll = words.every(w => searchable.includes(w));
      if (!matchesAll) return false;
    }
    return true;
  });
}

let currentSearchProducts = [];
let currentSearchKeyword = '';
let currentSearchPage = 1;
const SEARCH_PAGE_SIZE = 6;

function renderSearchResultsPagination(totalItems, currentPage) {
  const strip = document.querySelector('.dashboard-products-column .pagination-strip') || document.querySelector('.pagination-strip');
  if (!strip) return;

  strip.style.display = 'flex';
  strip.innerHTML = `
    <span class="page-btn" style="opacity: 0.4; cursor: not-allowed;" title="Trang trước"><i class="fas fa-chevron-left"></i></span>
    <a href="javascript:void(0)" class="page-btn active" onclick="changeSearchPage(1); return false;" title="Trang 1 / 1">1</a>
    <span class="page-btn" style="opacity: 0.4; cursor: not-allowed;" title="Trang sau"><i class="fas fa-chevron-right"></i></span>
  `;
}

window.changeSearchPage = function(page) {
  currentSearchPage = 1;
  const container = document.getElementById('search-results-grid');
  if (container) {
    container.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
};

function renderSearchResults(products, keyword, page = 1) {
  const defaultMonster = (typeof STATIC_PRODUCTS_CATALOG !== 'undefined' && STATIC_PRODUCTS_CATALOG.length > 0) ? STATIC_PRODUCTS_CATALOG[0] : {
    id: 'mn-1',
    name: 'Monster Energy Original 355ml',
    brand: 'Monster Energy',
    brandKey: 'monster',
    price: '45.000đ',
    priceKey: '20to50',
    image: 'assets/images/monster/original.webp',
    detailUrl: 'pages/product-detail.html',
    tag: 'HÀ LAN',
    keywords: 'energy boost nước tăng lực monster energy original hà lan nhập khẩu xanh lá'
  };
  currentSearchProducts = [defaultMonster];
  currentSearchKeyword = keyword || '';
  currentSearchPage = 1;

  const container = document.getElementById('search-results-grid');
  const countEl = document.getElementById('search-count-number');
  const queryTextEl = document.getElementById('search-query-text');
  const breadcrumbKw = document.getElementById('search-breadcrumb-query');

  if (countEl) countEl.textContent = '1';
  if (queryTextEl) {
    queryTextEl.textContent = keyword ? `"${keyword}"` : 'Tất cả sản phẩm';
  }
  if (breadcrumbKw) {
    breadcrumbKw.textContent = keyword ? `"${keyword}"` : 'Kết quả tìm kiếm';
  }

  renderSearchResultsPagination(1, 1);

  if (!container) return;

  const isInsidePages = window.location.pathname.includes('/pages/') || window.location.href.includes('/pages/');
  const imgPrefix = isInsidePages ? '../' : '';
  const detailLink = isInsidePages ? defaultMonster.detailUrl.replace('pages/', '') : defaultMonster.detailUrl;
  const imgSrc = imgPrefix + defaultMonster.image;

  container.innerHTML = `
    <div class="product-card product-card-stitch">
      <div class="product-card-micro-glow" style="background: #39FF14;"></div>
      <div class="stitch-badge-group">
        <span class="stitch-badge sale">-18%</span>
      </div>
      <div class="product-img-wrapper" onclick="window.location.href='${detailLink}'" title="Xem ${defaultMonster.name}" role="link" tabindex="0">
        <img src="${imgSrc}" alt="${defaultMonster.name}" class="product-img" loading="lazy" onerror="this.src='${imgPrefix}assets/images/monster/original.webp'" />
      </div>
      <div class="product-info">
        <span class="product-cat">${defaultMonster.brand}</span>
        <a href="${detailLink}" class="product-title-link"><h3 class="product-title">${defaultMonster.name}</h3></a>
        <div class="product-bottom">
          <div class="product-price">
            <span class="price-label">GIÁ CHÍNH HÃNG</span>
            <span class="price-val">${defaultMonster.price}</span>
            <del class="price-old">55.000đ</del>
          </div>
          <div class="btn-card-group">
            <button class="btn-add-stitch" title="Thêm vào giỏ" onclick="event.stopPropagation(); showToast('Đã thêm Monster Original vào giỏ hàng!', 'success')"><i class="fas fa-cart-plus"></i></button>
          </div>
        </div>
      </div>
    </div>
  `;
}

function initSearchResultsPage() {
  if (!document.getElementById('search-results-grid')) return;

  const params = new URLSearchParams(window.location.search);
  const q = params.get('q') || '';
  const brand = params.get('brand') || 'all';
  const price = params.get('price') || 'all';

  const headerInputs = document.querySelectorAll('.search-input');
  headerInputs.forEach(inp => { if (inp) inp.value = q; });

  const sidebarKw = document.getElementById('search-filter-keyword');
  if (sidebarKw) sidebarKw.value = q;

  const brandRadio = document.querySelector(`input[name="search-brand"][value="${brand}"]`);
  if (brandRadio) brandRadio.checked = true;

  const priceRadio = document.querySelector(`input[name="search-price"][value="${price}"]`);
  if (priceRadio) priceRadio.checked = true;

  renderSearchResults([], q, 1);
}

// Tự động khởi tạo trang kết quả tìm kiếm khi DOM đã nạp
if (typeof document !== 'undefined') {
  const autoInitSearch = () => {
    if (document.getElementById('search-results-grid')) {
      initSearchResultsPage();
    }
  };
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', autoInitSearch);
  } else {
    autoInitSearch();
  }
}

function handleSearchResultsFilter(e) {
  if (e && e.preventDefault) e.preventDefault();
  const kwInput = document.getElementById('search-filter-keyword');
  const q = kwInput ? kwInput.value.trim() : '';
  document.querySelectorAll('.search-input').forEach(inp => { if (inp) inp.value = q; });

  const brandEl = document.querySelector('input[name="search-brand"]:checked');
  const brand = brandEl ? brandEl.value : 'all';
  const priceEl = document.querySelector('input[name="search-price"]:checked');
  const price = priceEl ? priceEl.value : 'all';

  const params = new URLSearchParams();
  if (q) params.set('q', q);
  if (brand && brand !== 'all') params.set('brand', brand);
  if (price && price !== 'all') params.set('price', price);

  const newUrl = window.location.pathname + (params.toString() ? '?' + params.toString() : '');
  try {
    window.history.pushState({}, '', newUrl);
  } catch (err) {}

  renderSearchResults([], q, 1);
  showToast('Đã tìm thấy 1 sản phẩm phù hợp!', 'info');
}

function resetSearchPageFilter() {
  const sidebarKw = document.getElementById('search-filter-keyword');
  if (sidebarKw) sidebarKw.value = '';
  document.querySelectorAll('.search-input').forEach(inp => { if (inp) inp.value = ''; });

  const allBrand = document.querySelector('input[name="search-brand"][value="all"]');
  if (allBrand) allBrand.checked = true;
  const allPrice = document.querySelector('input[name="search-price"][value="all"]');
  if (allPrice) allPrice.checked = true;

  try {
    window.history.pushState({}, '', window.location.pathname);
  } catch (err) {}

  renderSearchResults([], '', 1);
  showToast('Đã hiển thị sản phẩm mặc định (1 lon Monster)!', 'info');
}

function renderAdvSuggestions() {
  const container = document.getElementById('adv-search-suggestions');
  if (!container) return;

  const root = typeof SITE_ROOT !== 'undefined' ? SITE_ROOT : '';
  let html = '';
  STATIC_PRODUCTS_CATALOG.forEach((prod, idx) => {
    const imgSrc = root + prod.image;
    html += `
      <div class="adv-suggestion-item" onclick="selectAdvSearchSuggestion(${idx})">
        <div class="adv-suggestion-left">
          <img src="${imgSrc}" alt="${prod.name}" class="adv-suggestion-thumb" />
          <div>
            <div class="adv-suggestion-name">${prod.name}</div>
            <div class="adv-suggestion-brand">${prod.brand}</div>
          </div>
        </div>
        <div class="adv-suggestion-price">${prod.price}</div>
      </div>
    `;
  });
  container.innerHTML = html;
}

function handleAdvKeywordInput(val) {
  openAdvSuggestions();
}

function openAdvSuggestions() {
  const container = document.getElementById('adv-search-suggestions');
  if (!container) return;
  renderAdvSuggestions();
  container.classList.add('active');
}

function selectAdvSearchSuggestion(idx) {
  const prod = STATIC_PRODUCTS_CATALOG[idx];
  if (!prod) return;

  const kwEl = document.getElementById('adv-search-keyword');
  if (kwEl) kwEl.value = prod.name;

  const brandEl = document.getElementById('adv-search-brand');
  if (brandEl) brandEl.value = prod.brandKey;

  const priceEl = document.getElementById('adv-search-price');
  if (priceEl) priceEl.value = prod.priceKey;

  const previewEl = document.getElementById('adv-search-preview');
  if (previewEl) {
    previewEl.innerHTML = `<i class="fas fa-info-circle" style="color: var(--primary);"></i> Kết quả mẫu phù hợp tiêu chí: <strong style="color: #FFF;">${prod.name} (${prod.price})</strong>`;
  }

  closeAdvSuggestions();
}

function closeAdvSuggestions() {
  const container = document.getElementById('adv-search-suggestions');
  if (container) {
    container.classList.remove('active');
  }
}

// Global click outside & Escape listeners for search dropdown and advanced suggestions
document.addEventListener('click', function(e) {
  const searchBox = e.target.closest('.search-box');
  if (!searchBox) {
    closeSearchDropdown();
  }
  const filterInputWrapper = e.target.closest('.filter-input-wrapper');
  if (!filterInputWrapper) {
    closeSidebarSearchDropdown();
  }
  const advWrapper = e.target.closest('.adv-search-input-wrapper');
  if (!advWrapper) {
    closeAdvSuggestions();
  }

});

document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    closeSearchDropdown();
    closeSidebarSearchDropdown();
    closeAdvancedSearchModal();
    closeAdvSuggestions();
  } else if (e.key === 'Enter') {
    const input = e.target.closest('.search-input');
    if (input) {
      e.preventDefault();
      executeHeaderSearch(input.value);
    }
  }
});

// ==========================================================================
// 14. AUTH TABS & REGISTRATION LOGIC (RUBRIC COMPLIANCE)
// ==========================================================================
function switchAuthTab(mode) {
  const loginBtn = document.getElementById('tab-login-btn');
  const registerBtn = document.getElementById('tab-register-btn');
  const formLogin = document.getElementById('form-login');
  const formRegister = document.getElementById('form-register');
  const titleEl = document.getElementById('auth-card-title');
  const descEl = document.getElementById('auth-card-desc');

  if (mode === 'register') {
    if (loginBtn) loginBtn.classList.remove('active');
    if (registerBtn) registerBtn.classList.add('active');
    if (formLogin) formLogin.style.display = 'none';
    if (formRegister) formRegister.style.display = 'block';
    if (titleEl) titleEl.innerHTML = 'ĐĂNG KÝ <span>THÀNH VIÊN VIP</span>';
    if (descEl) descEl.innerText = 'Đăng ký tài khoản người mua hàng để nhận ưu đãi thành viên và tích điểm đổi quà:';
  } else {
    if (loginBtn) loginBtn.classList.add('active');
    if (registerBtn) registerBtn.classList.remove('active');
    if (formLogin) formLogin.style.display = 'block';
    if (formRegister) formRegister.style.display = 'none';
    if (titleEl) titleEl.innerHTML = 'ĐĂNG NHẬP <span>ENERGY BOOST</span>';
    if (descEl) descEl.innerText = 'Đăng nhập tài khoản để nhận ưu đãi thành viên và theo dõi đơn hàng:';
  }
}

function handleRegister(e) {
  if (e && e.preventDefault) e.preventDefault();
  const nameEl = document.getElementById('register-fullname');
  const emailEl = document.getElementById('register-email');
  const passEl = document.getElementById('register-password');
  const confirmEl = document.getElementById('register-confirm-password');

  const fullName = (nameEl && nameEl.value.trim()) || 'Khách Hàng Mới';
  const email = (emailEl && emailEl.value.trim()) || '';
  const pass = passEl ? passEl.value : '';
  const confirm = confirmEl ? confirmEl.value : '';

  try {
    localStorage.setItem('monster_user', fullName);
  } catch (err) { }

  showToast('Đăng ký tài khoản thành công! Chào mừng ' + fullName + ' gia nhập Energy Boost VIP.', 'success');

  setTimeout(() => {
    const loginUserEl = document.getElementById('login-username');
    if (loginUserEl) loginUserEl.value = email || fullName;
    switchAuthTab('login');
  }, 1000);
}

function togglePasswordVisibility(inputId, iconId) {
  const input = document.getElementById(inputId);
  const icon = document.getElementById(iconId);
  if (!input) return;
  if (input.type === 'password') {
    input.type = 'text';
    if (icon) {
      icon.classList.remove('fa-eye');
      icon.classList.add('fa-eye-slash');
    }
  } else {
    input.type = 'password';
    if (icon) {
      icon.classList.remove('fa-eye-slash');
      icon.classList.add('fa-eye');
    }
  }
}

// Check URL hash for direct tab opening (e.g. login.html#register)
window.addEventListener('DOMContentLoaded', () => {
  if (window.location.hash === '#register') {
    switchAuthTab('register');
  }
});

// ==========================================================================
// 15. ADMIN STATIC FILTER & SMART SAFE DELETE (RUBRIC COMPLIANCE)
// ==========================================================================
function applyAdminOrderFilter() {
  const statusEl = document.getElementById('filter-order-status');
  const status = (statusEl && statusEl.selectedIndex >= 0 && statusEl.options[statusEl.selectedIndex]) ? statusEl.options[statusEl.selectedIndex].text : 'Tất cả';
  const fromEl = document.getElementById('filter-order-date-from');
  const toEl = document.getElementById('filter-order-date-to');
  const from = fromEl ? fromEl.value : '';
  const to = toEl ? toEl.value : '';
  const locEl = document.getElementById('filter-order-location');
  const loc = (locEl && locEl.selectedIndex >= 0 && locEl.options[locEl.selectedIndex]) ? locEl.options[locEl.selectedIndex].text : 'Tất cả';
  const kwEl = document.getElementById('filter-order-keyword');
  const kw = (kwEl ? kwEl.value : '').trim();

  let msg = 'Đã áp dụng bộ lọc đơn hàng: [' + status + '] | Khu vực: [' + loc + ']';
  if (from && to) msg += ' | Từ: ' + from + ' đến ' + to;
  if (kw) msg += ' | Từ khóa: "' + kw + '"';
  showToast(msg, 'success');
}

function resetAdminOrderFilter() {
  const statusEl = document.getElementById('filter-order-status');
  if (statusEl) statusEl.value = 'all';
  const locEl = document.getElementById('filter-order-location');
  if (locEl) locEl.value = 'all';
  const fromEl = document.getElementById('filter-order-date-from');
  if (fromEl) fromEl.value = '2026-10-01';
  const toEl = document.getElementById('filter-order-date-to');
  if (toEl) toEl.value = '2026-10-17';
  const kwEl = document.getElementById('filter-order-keyword');
  if (kwEl) kwEl.value = '';
  showToast('Đã đặt lại bộ lọc đơn hàng mặc định', 'info');
}

function applyAdminInventoryFilter() {
  const brandEl = document.getElementById('filter-inv-brand');
  const brand = brandEl ? brandEl.options[brandEl.selectedIndex].text : 'Tất cả';
  const stockEl = document.getElementById('filter-inv-stock');
  const stock = stockEl ? stockEl.options[stockEl.selectedIndex].text : 'Tất cả';
  const kwEl = document.getElementById('filter-inv-keyword');
  const kw = (kwEl ? kwEl.value : '').trim();

  const msg = 'Đã lọc kho hàng: [' + brand + '] | Trạng thái: [' + stock + ']' + (kw ? ' | SKU: "' + kw + '"' : '');
  showToast(msg, 'success');
}

function resetAdminInventoryFilter() {
  const brandEl = document.getElementById('filter-inv-brand');
  if (brandEl) brandEl.value = 'all';
  const stockEl = document.getElementById('filter-inv-stock');
  if (stockEl) stockEl.value = 'all';
  const kwEl = document.getElementById('filter-inv-keyword');
  if (kwEl) kwEl.value = '';
  showToast('Đã đặt lại bộ lọc kho hàng mặc định', 'info');
}

function applyAdminCustomerFilter() {
  const tierEl = document.getElementById('filter-customer-tier');
  const tier = tierEl ? tierEl.options[tierEl.selectedIndex].text : 'Tất cả';
  const fromEl = document.getElementById('stat-customer-from');
  const toEl = document.getElementById('stat-customer-to');
  const from = fromEl ? fromEl.value : '2026-01-01';
  const to = toEl ? toEl.value : '2026-10-17';

  showToast('Đã thống kê Top 5 khách hàng mua cao nhất (' + from + ' đến ' + to + ') - Phân loại: ' + tier, 'success');
}

function resetAdminCustomerFilter() {
  const tierEl = document.getElementById('filter-customer-tier');
  if (tierEl) tierEl.value = 'all';
  const kwEl = document.getElementById('filter-customer-keyword');
  if (kwEl) kwEl.value = '';
  showToast('Đã đặt lại bộ lọc khách hàng VIP', 'info');
}

function applyDashboardFilter(type) {
  if (type === 'orders') {
    const statusEl = document.getElementById('dash-order-status');
    const status = statusEl ? statusEl.options[statusEl.selectedIndex].text : 'Tất cả';
    showToast('Dashboard: Đang lọc đơn hàng [' + status + ']', 'info');
  } else {
    const brandEl = document.getElementById('dash-inv-brand');
    const brand = brandEl ? brandEl.options[brandEl.selectedIndex].text : 'Tất cả';
    showToast('Dashboard: Đang lọc kho hàng [' + brand + ']', 'info');
  }
}

function resetDashboardFilter(type) {
  if (type === 'orders') {
    const statusEl = document.getElementById('dash-order-status');
    if (statusEl) statusEl.value = 'all';
    const kwEl = document.getElementById('dash-order-keyword');
    if (kwEl) kwEl.value = '';
  } else {
    const brandEl = document.getElementById('dash-inv-brand');
    if (brandEl) brandEl.value = 'all';
    const kwEl = document.getElementById('dash-inv-keyword');
    if (kwEl) kwEl.value = '';
  }
  showToast('Đã đặt lại bộ lọc trên Dashboard', 'info');
}

// ==========================================================================
// 16. ADMIN AUTHENTICATION SIMULATION (R1 COMPLIANCE)
// ==========================================================================
function handleAdminLogin(e) {
  if (e && e.preventDefault) e.preventDefault();
  const userEl = document.getElementById('admin-user');
  const user = (userEl ? userEl.value : '').trim();
  const adminName = user || 'Thuận Trần (Admin)';
  
  try {
    localStorage.setItem('admin_logged_in', 'true');
    localStorage.setItem('admin_user_name', adminName);
    localStorage.setItem('monster_user', adminName);
  } catch (err) {}

  showToast('Xác thực Quản trị viên cấp cao thành công! Đang chuyển vào Dashboard...', 'success');
  setTimeout(() => {
    window.location.href = 'index.html';
  }, 800);
}

function adminLogout(e) {
  if (e && e.preventDefault) e.preventDefault();
  try {
    localStorage.removeItem('admin_logged_in');
    localStorage.removeItem('admin_user_name');
  } catch (err) {}
  showToast('Đã đăng xuất khỏi tài khoản Quản trị!', 'info');
  setTimeout(() => {
    window.location.href = 'login.html';
  }, 700);
}

// ==========================================================================
// 17. USER MANAGEMENT UI HANDLERS (R2 COMPLIANCE - ZERO CONSTRAINTS / FAST BOOST)
// ==========================================================================
let currentEditingUserRow = null;

function openAddUserModal() {
  const form = document.getElementById('form-add-user');
  if (form) form.reset();
  openAdminModal('modal-add-user');
}

function saveAddUser(e) {
  if (e && e.preventDefault) e.preventDefault();

  // Bỏ toàn bộ ràng buộc (zero constraints / boost mode):
  // Không ép điền đầy đủ (required), không regex sđt, không ép định dạng email khắt khe, không ép độ dài mật khẩu.
  const fullnameInput = document.getElementById('add-user-fullname');
  const usernameInput = document.getElementById('add-user-username');
  const emailInput = document.getElementById('add-user-email');
  const phoneInput = document.getElementById('add-user-phone');
  const roleInput = document.getElementById('add-user-role');
  const statusInput = document.getElementById('add-user-status');
  const passwordInput = document.getElementById('add-user-password');

  const fullname = (fullnameInput && fullnameInput.value.trim()) || 'Người Dùng Mới';
  const username = (usernameInput && usernameInput.value.trim()) || ('user_' + Math.floor(1000 + Math.random() * 9000));
  const email = (emailInput && emailInput.value.trim()) || (username + '@energyboost.vn');
  const phone = (phoneInput && phoneInput.value.trim()) || '0938.222.111';
  const role = (roleInput && roleInput.value) || 'user';
  const status = (statusInput && statusInput.value) || 'active';
  const password = (passwordInput && passwordInput.value) || '123456';
  const userId = 'u_' + Date.now();
  const createdAt = new Date().toLocaleDateString('vi-VN');

  const userObj = {
    id: userId,
    fullname,
    username,
    email,
    phone,
    role,
    status,
    password,
    spent: '0đ',
    orders: '0 đơn hàng (Mới tạo)',
    createdAt
  };

  // Lưu vào localStorage để dữ liệu lưu trữ bền vững (không bị mất khi F5)
  try {
    const customUsers = JSON.parse(localStorage.getItem('admin_custom_users') || '[]');
    customUsers.unshift(userObj);
    localStorage.setItem('admin_custom_users', JSON.stringify(customUsers));
  } catch (err) {
    console.error('Error saving user to localStorage:', err);
  }

  // Xác định chính xác bảng khách hàng (tránh chèn nhầm vào bảng đơn hàng ở dashboard admin/index.html)
  const custTable = document.getElementById('customers-table') ||
    (window.location.pathname.includes('customers.html') ? document.querySelector('.cart-table') : null);

  if (custTable) {
    const tbody = custTable.querySelector('tbody') || custTable;
    if (tbody) {
      const isLocked = status === 'locked';
      const safeName = fullname.replace(/"/g, '&quot;').replace(/'/g, "\\'");
      const tr = document.createElement('tr');
      tr.setAttribute('data-custom-user-id', userId);
      tr.innerHTML = `
        <td><span class="badge-status" style="background: rgba(0,255,136,0.15); color: var(--primary); border: 1px solid var(--primary); font-weight: 700;">MỚI</span></td>
        <td><strong>${fullname}</strong><br><small style="color: var(--text-muted);">${username} (${role.toUpperCase()})</small></td>
        <td>${phone}<br><small style="color: var(--text-dim);">${email}</small></td>
        <td><span style="color: var(--text-muted);">0 đơn hàng (Mới tạo)</span></td>
        <td><strong style="color: var(--primary); font-size: 1.05rem;">0đ</strong></td>
        <td><span class="badge-status ${isLocked ? 'danger' : 'success'}">${isLocked ? 'ĐÃ KHOÁ' : 'ĐANG HOẠT ĐỘNG'}</span></td>
        <td>
          <button class="btn-view-detail" style="padding: 4px 8px; font-size: 0.8rem;" onclick="openEditUserModal('', this)" title="Sửa"><i class="fas fa-edit"></i> Sửa</button>
          <button class="${isLocked ? 'btn-action-unlock' : 'btn-action-lock'}" onclick="toggleLockUser(this, '${safeName}')" title="${isLocked ? 'Mở khoá' : 'Khoá'}"><i class="fas fa-${isLocked ? 'lock-open' : 'lock'}"></i> ${isLocked ? 'Mở khoá' : 'Khoá'}</button>
        </td>
      `;
      tbody.insertBefore(tr, tbody.firstChild);
    }
  }

  showToast('Đã tạo tài khoản thành viên "' + fullname + '" thành công (không ràng buộc)!', 'success');
  closeAdminModal('modal-add-user');
  const form = document.getElementById('form-add-user');
  if (form) form.reset();
}

function openEditUserModal(customerKey, btn) {
  currentEditingUserRow = btn ? btn.closest('tr') : null;
  const nameEl = document.getElementById('edit-user-fullname');
  const phoneEl = document.getElementById('edit-user-phone');
  const emailEl = document.getElementById('edit-user-email');
  const statusEl = document.getElementById('edit-user-status');

  if (currentEditingUserRow) {
    const strong = currentEditingUserRow.querySelector('strong');
    if (nameEl && strong) nameEl.value = strong.textContent.trim();
    if (phoneEl && currentEditingUserRow.cells[2]) {
      const pText = currentEditingUserRow.cells[2].childNodes[0] ? currentEditingUserRow.cells[2].childNodes[0].textContent.trim() : '';
      phoneEl.value = pText;
    }
    const smallEmail = currentEditingUserRow.cells[2] ? currentEditingUserRow.cells[2].querySelector('small') : null;
    if (emailEl && smallEmail) {
      emailEl.value = smallEmail.textContent.trim();
    }
    const badge = currentEditingUserRow.querySelector('.badge-status');
    if (badge && statusEl) {
      statusEl.value = badge.textContent.includes('KHOÁ') ? 'locked' : 'active';
    }
  } else if (typeof CUSTOMER_DATA_REGISTRY !== 'undefined' && CUSTOMER_DATA_REGISTRY[customerKey]) {
    const data = CUSTOMER_DATA_REGISTRY[customerKey];
    if (nameEl) nameEl.value = data.name;
    if (phoneEl) phoneEl.value = data.phone;
    if (emailEl) emailEl.value = data.email;
  }
  openAdminModal('modal-edit-user');
}

function saveEditUser(e) {
  if (e && e.preventDefault) e.preventDefault();
  const nameEl = document.getElementById('edit-user-fullname');
  const name = nameEl ? nameEl.value.trim() || 'Người dùng' : 'Người dùng';
  const phoneEl = document.getElementById('edit-user-phone');
  const emailEl = document.getElementById('edit-user-email');
  const statusEl = document.getElementById('edit-user-status');

  if (currentEditingUserRow) {
    const oldStrong = currentEditingUserRow.querySelector('strong');
    const oldName = oldStrong ? oldStrong.textContent.trim() : '';
    if (oldStrong && nameEl) oldStrong.textContent = name;
    
    if (phoneEl && currentEditingUserRow.cells[2]) {
      const emailVal = emailEl ? emailEl.value.trim() : '';
      currentEditingUserRow.cells[2].innerHTML = (phoneEl.value.trim() || '') + (emailVal ? '<br><small style="color: var(--text-dim);">' + emailVal + '</small>' : '');
    }
    const badge = currentEditingUserRow.querySelector('.badge-status');
    const lockBtn = currentEditingUserRow.querySelector('.btn-action-lock, .btn-action-unlock');
    if (statusEl && badge) {
      const isLocked = statusEl.value === 'locked';
      badge.className = 'badge-status ' + (isLocked ? 'danger' : 'success');
      badge.textContent = isLocked ? 'ĐÃ KHOÁ' : 'ĐANG HOẠT ĐỘNG';
      if (lockBtn) {
        lockBtn.className = isLocked ? 'btn-action-unlock' : 'btn-action-lock';
        lockBtn.innerHTML = `<i class="fas fa-${isLocked ? 'lock-open' : 'lock'}"></i> ${isLocked ? 'Mở khoá' : 'Khoá'}`;
        lockBtn.title = isLocked ? 'Mở khoá' : 'Khoá';
      }
    }

    // Đồng bộ thay đổi vào localStorage nếu là người dùng tùy chỉnh
    try {
      const customUsers = JSON.parse(localStorage.getItem('admin_custom_users') || '[]');
      const rowId = currentEditingUserRow.getAttribute('data-custom-user-id');
      const matched = customUsers.find(u => (rowId && u.id === rowId) || u.fullname === oldName);
      if (matched) {
        matched.fullname = name;
        if (phoneEl) matched.phone = phoneEl.value.trim();
        if (emailEl) matched.email = emailEl.value.trim();
        if (statusEl) matched.status = statusEl.value;
        localStorage.setItem('admin_custom_users', JSON.stringify(customUsers));
      }
    } catch (err) {}
  }

  showToast('Đã lưu thay đổi thông tin người dùng "' + name + '" thành công!', 'success');
  closeAdminModal('modal-edit-user');
}

function toggleLockUser(btn, customerName) {
  const isLocked = btn && btn.classList.contains('btn-action-unlock');
  const action = isLocked ? 'mở khoá' : 'khoá';
  showToast('Đã ' + action + ' tài khoản "' + customerName + '" thành công!', isLocked ? 'success' : 'info');
}

function initCustomUsersTable() {
  if (typeof window === 'undefined' || typeof document === 'undefined') return;
  const isCustomersPage = window.location && window.location.pathname && window.location.pathname.includes('customers.html');
  const custTable = document.getElementById('customers-table') || (isCustomersPage ? document.querySelector('.cart-table') : null);
  if (!custTable) return;
  const tbody = custTable.querySelector('tbody') || custTable;
  if (!tbody) return;

  // Tránh render trùng lặp nếu hàm được gọi nhiều lần
  if (tbody.querySelector('[data-custom-user-id]')) return;

  try {
    const rawUsers = typeof localStorage !== 'undefined' ? localStorage.getItem('admin_custom_users') : null;
    const customUsers = JSON.parse(rawUsers || '[]');
    // Render custom users in reverse order so newest is at the top
    for (let i = customUsers.length - 1; i >= 0; i--) {
      const u = customUsers[i];
      const isLocked = u.status === 'locked';
      const safeName = (u.fullname || 'Người Dùng Mới').replace(/"/g, '&quot;').replace(/'/g, "\\'");
      const tr = document.createElement('tr');
      tr.setAttribute('data-custom-user-id', u.id || ('u_' + i));
      tr.innerHTML = `
        <td><span class="badge-status" style="background: rgba(0,255,136,0.15); color: var(--primary); border: 1px solid var(--primary); font-weight: 700;">MỚI</span></td>
        <td><strong>${u.fullname || 'Người Dùng Mới'}</strong><br><small style="color: var(--text-muted);">${u.username || 'user'} (${(u.role || 'user').toUpperCase()})</small></td>
        <td>${u.phone || '0938.222.111'}<br><small style="color: var(--text-dim);">${u.email || 'user@energyboost.vn'}</small></td>
        <td><span style="color: var(--text-muted);">${u.orders || '0 đơn hàng (Mới tạo)'}</span></td>
        <td><strong style="color: var(--primary); font-size: 1.05rem;">${u.spent || '0đ'}</strong></td>
        <td><span class="badge-status ${isLocked ? 'danger' : 'success'}">${isLocked ? 'ĐÃ KHOÁ' : 'ĐANG HOẠT ĐỘNG'}</span></td>
        <td>
          <button class="btn-view-detail" style="padding: 4px 8px; font-size: 0.8rem;" onclick="openEditUserModal('', this)" title="Sửa"><i class="fas fa-edit"></i> Sửa</button>
          <button class="${isLocked ? 'btn-action-unlock' : 'btn-action-lock'}" onclick="toggleLockUser(this, '${safeName}')" title="${isLocked ? 'Mở khoá' : 'Khoá'}"><i class="fas fa-${isLocked ? 'lock-open' : 'lock'}"></i> ${isLocked ? 'Mở khoá' : 'Khoá'}</button>
        </td>
      `;
      tbody.insertBefore(tr, tbody.firstChild);
    }
  } catch (err) {
    console.error('Error loading custom users:', err);
  }
}

// ==========================================================================
// 18. FILEREADER IMAGE PREVIEWS & SMART SAFE DELETE (R3 COMPLIANCE)
// ==========================================================================
function previewAddProductImage(e) {
  const input = (e && e.target) ? e.target : e;
  const row = input && input.closest('.product-image-row');
  const img = row ? row.querySelector('.product-image-preview') : document.getElementById('add-prod-preview');
  if (!input || !img) return;
  if (!input.files || !input.files[0]) {
    img.hidden = true;
    img.removeAttribute('src');
    return;
  }
  const file = input.files[0];
  const reader = new FileReader();
  reader.onload = function(evt) {
    if (input.files[0] !== file) return;
    img.src = evt.target.result;
    img.hidden = false;
  };
  reader.readAsDataURL(file);
}

function previewEditProductImage(e) {
  const input = (e && e.target) ? e.target : e;
  if (input && input.closest('.product-image-row')) {
    previewAddProductImage(input);
    return;
  }
  if (input && input.files && input.files[0]) {
    const reader = new FileReader();
    reader.onload = function(evt) {
      const img = document.getElementById('edit-prod-img-preview');
      if (img) img.src = evt.target.result;
    };
    reader.readAsDataURL(input.files[0]);
  }
}

function handleAdminDeleteProduct(btnOrName, productNameOrHasOrders, maybeHasOrders) {
  let name = 'Sản phẩm';
  let hasOrders = false;

  if (typeof btnOrName === 'string') {
    name = btnOrName;
    hasOrders = !!productNameOrHasOrders;
  } else {
    name = productNameOrHasOrders || 'Sản phẩm';
    hasOrders = !!maybeHasOrders;
  }

  // Quy tắc dự án: Khi xóa chỉ cần thông báo chứ không thực sự xóa hay ẩn (DOM giữ nguyên)
  if (hasOrders) {
    showToast('Sản phẩm "' + name + '" đã phát sinh đơn hàng xuất bán! Hệ thống đã chuyển trạng thái sang ĐÃ ẨN để bảo toàn lịch sử giao dịch.', 'warning');
  } else {
    showToast('Đã xóa sản phẩm "' + name + '" khỏi hệ thống kho hàng.', 'info');
  }
}

// ==========================================================================
// 19. UNIDIRECTIONAL ORDER STATE MACHINE (R4 COMPLIANCE)
// ==========================================================================
const ORDER_STATUS_ORDER = {
  'Chưa xác nhận': ['Đã xác nhận', 'Đã giao (Huỷ đơn)'],
  'Đã xác nhận': ['Đã giao (Thành công)', 'Đã giao (Huỷ đơn)'],
  'Đã giao (Thành công)': [],
  'Đã giao (Huỷ đơn)': []
};

let currentOrderEditingBtn = null;
let currentOrderIdForStatus = '';

function openOrderStatusModal(orderId, currentStatus, btn) {
  currentOrderIdForStatus = orderId;
  currentOrderEditingBtn = btn;
  
  const idEl = document.getElementById('status-modal-order-id');
  const badgeEl = document.getElementById('status-modal-current-badge');
  const selectEl = document.getElementById('select-next-status');
  
  if (idEl) idEl.textContent = '#' + orderId;
  if (badgeEl) {
    badgeEl.textContent = currentStatus;
    const isSuccess = currentStatus.includes('Thành công');
    const isCancel = currentStatus.includes('Huỷ');
    const isWarning = currentStatus.includes('xác nhận') && !currentStatus.includes('Chưa');
    badgeEl.className = 'badge-status ' + (isSuccess ? 'success' : (isCancel ? 'danger' : (isWarning ? 'warning' : 'info')));
  }
  
  const allowedNext = ORDER_STATUS_ORDER[currentStatus] || [];
  if (selectEl) {
    selectEl.innerHTML = '';
    if (allowedNext.length === 0) {
      selectEl.innerHTML = '<option value="">(Đơn hàng đã hoàn tất - Không thể cập nhật ngược)</option>';
      selectEl.disabled = true;
    } else {
      selectEl.disabled = false;
      allowedNext.forEach(st => {
        const opt = document.createElement('option');
        opt.value = st;
        opt.textContent = '➔ ' + st;
        selectEl.appendChild(opt);
      });
    }
  }
  openAdminModal('modal-order-status');
}

function saveOrderStatus() {
  const selectEl = document.getElementById('select-next-status');
  if (!selectEl || selectEl.disabled || !selectEl.value) {
    showToast('Không thể cập nhật! Trạng thái đơn hàng chỉ có thể cập nhật xuôi, không cho phép cập nhật ngược.', 'warning');
    closeAdminModal('modal-order-status');
    return;
  }
  const nextStatus = selectEl.value;
  // Quy tắc dự án: Giữ lại giao diện modal và thông báo nhưng tắt tính năng chuyển (trạng thái trong bảng giữ nguyên)
  showToast('Đã cập nhật trạng thái đơn hàng #' + currentOrderIdForStatus + ' thành "' + nextStatus + '"!', 'success');
  closeAdminModal('modal-order-status');
}

// ==========================================================================
// 20. VOUCHER SETTINGS LIVE PREVIEW & MULTI-VOUCHER CONTROLLER
// ==========================================================================

// Mock registry representing multiple campaign vouchers in the system
const MOCK_VOUCHERS_LIST = [
  {
    code: 'MONSTER10',
    type: 'percent',
    amount: '10%',
    minSpend: '200.000đ',
    maxDiscount: '50.000đ',
    expiry: '2026-12-31',
    target: 'all',
    targetText: 'Tất cả khách hàng',
    limit: 1000
  },
  {
    code: 'ENERGY20',
    type: 'fixed',
    amount: '20.000đ',
    minSpend: '150.000đ',
    maxDiscount: '20.000đ',
    expiry: '2026-11-30',
    target: 'new',
    targetText: 'Chỉ khách hàng mới',
    limit: 500
  },
  {
    code: 'FREESHIP',
    type: 'fixed',
    amount: '25.000đ',
    minSpend: '200.000đ',
    maxDiscount: '25.000đ',
    expiry: '2026-12-31',
    target: 'vip',
    targetText: 'Chỉ khách hàng VIP',
    limit: 300
  }
];

let activeVoucherCode = 'MONSTER10';

function getVoucherTag(voucher) {
  if (voucher.code === 'FREESHIP') return 'FREESHIP';
  if (voucher.type === 'percent') {
    const val = voucher.amount.replace(/%/g, '').trim();
    return `${val}%`;
  }
  const num = voucher.amount.replace(/\D/g, '');
  if (num && parseInt(num, 10) >= 1000) {
    return `${Math.round(parseInt(num, 10) / 1000)}K`;
  }
  return voucher.amount;
}

function renderVoucherChips() {
  const container = document.getElementById('voucher-chips-list');
  if (!container) return;

  container.innerHTML = MOCK_VOUCHERS_LIST.map(v => {
    const isActive = v.code === activeVoucherCode;
    const tag = getVoucherTag(v);
    return `<button type="button" class="voucher-chip ${isActive ? 'active' : ''}" onclick="switchVoucherPreview('${v.code}')" title="Xem & cấu hình mã ${v.code}">
      ${v.code} <span class="voucher-chip-tag">${tag}</span>
    </button>`;
  }).join('');
}

function switchVoucherPreview(code) {
  const voucher = MOCK_VOUCHERS_LIST.find(v => v.code === code);
  if (!voucher) return;

  activeVoucherCode = voucher.code;

  renderVoucherChips();

  showToast(`Đang xem cấu hình Voucher "${voucher.code}"`, 'info');
}

function updateVoucherLivePreview() {
  const codeEl = document.getElementById('voucher-code');
  const amountEl = document.getElementById('voucher-amount');
  const typeEl = document.getElementById('voucher-type');
  const minSpendEl = document.getElementById('voucher-min-spend');
  const maxDiscEl = document.getElementById('voucher-max-discount');
  const expiryEl = document.getElementById('voucher-expiry');

  const previewCode = document.getElementById('preview-ticket-code');
  const previewDiscount = document.getElementById('preview-ticket-discount');
  const previewDesc = document.getElementById('preview-ticket-desc');
  const previewExpiry = document.getElementById('preview-ticket-expiry');

  const code = (codeEl && codeEl.value) ? codeEl.value.trim().toUpperCase() : 'MONSTER10';
  const rawAmount = (amountEl && amountEl.value) ? amountEl.value.trim() : '10%';
  const type = typeEl ? typeEl.value : 'percent';
  const minSpend = (minSpendEl && minSpendEl.value) ? minSpendEl.value.trim() : '0đ';
  const maxDisc = (maxDiscEl && maxDiscEl.value) ? maxDiscEl.value.trim() : '';

  if (previewCode) {
    previewCode.innerHTML = `<i class="fas fa-copy"></i> ${code}`;
  }

  if (previewDiscount) {
    if (type === 'percent') {
      const cleanPercent = rawAmount.replace(/%/g, '').trim();
      previewDiscount.textContent = `GIẢM ${cleanPercent}%`;
    } else {
      const cleanFixed = rawAmount.replace(/\s*(đ|Đ|vnđ|VNĐ)$/i, '').trim();
      previewDiscount.textContent = `GIẢM ${cleanFixed}đ`;
    }
  }

  if (previewDesc) {
    const minText = (!minSpend || minSpend === '0' || minSpend === '0đ') ? 'mọi đơn hàng' : `đơn từ ${minSpend}`;
    const maxText = maxDisc ? ` (Tối đa ${maxDisc})` : '';
    previewDesc.textContent = `Áp dụng cho ${minText}${maxText}`;
  }

  if (previewExpiry && expiryEl && expiryEl.value) {
    const parts = expiryEl.value.split('-');
    if (parts.length === 3) {
      previewExpiry.textContent = `${parts[2]}/${parts[1]}/${parts[0]}`;
    }
  }
}

function handleVoucherStatusToggle(toggle) {
  const isChecked = toggle ? toggle.checked : true;
  const label = document.getElementById('voucher-status-label');
  const badge = document.getElementById('preview-ticket-badge');
  const card = document.getElementById('voucher-ticket-preview');

  if (label) {
    label.textContent = isChecked ? 'ĐANG BẬT' : 'ĐÃ TẮT';
    label.style.color = isChecked ? 'var(--primary)' : 'var(--text-muted)';
  }
  if (badge) {
    badge.className = isChecked ? 'badge-status success' : 'badge-status danger';
    badge.innerHTML = isChecked ? '<i class="fas fa-circle-check"></i> ĐANG ÁP DỤNG' : '<i class="fas fa-circle-xmark"></i> TẠM NGƯNG';
  }
  if (card) {
    card.style.opacity = isChecked ? '1' : '0.55';
    card.style.filter = isChecked ? 'none' : 'grayscale(0.7)';
  }
  showToast(isChecked ? 'Đã kích hoạt chương trình Voucher trên toàn hệ thống!' : 'Đã tạm ngưng áp dụng Voucher trên website.', isChecked ? 'success' : 'warning');
}

function handleSaveVoucherSettings(e) {
  if (e && e.preventDefault) e.preventDefault();
  const codeEl = document.getElementById('voucher-code');
  const typeEl = document.getElementById('voucher-type');
  const amountEl = document.getElementById('voucher-amount');
  const minSpendEl = document.getElementById('voucher-min-spend');
  const maxDiscountEl = document.getElementById('voucher-max-discount');
  const expiryEl = document.getElementById('voucher-expiry');

  const code = (codeEl && codeEl.value) ? codeEl.value.trim().toUpperCase() : 'MONSTER10';
  const type = typeEl ? typeEl.value : 'percent';
  const amount = (amountEl && amountEl.value) ? amountEl.value.trim() : '10%';
  const minSpend = (minSpendEl && minSpendEl.value) ? minSpendEl.value.trim() : '200.000đ';
  const maxDiscount = (maxDiscountEl && maxDiscountEl.value) ? maxDiscountEl.value.trim() : '50.000đ';
  const expiry = (expiryEl && expiryEl.value) ? expiryEl.value : '2026-12-31';

  // Update in mock list if matches active voucher
  const existing = MOCK_VOUCHERS_LIST.find(v => v.code === activeVoucherCode || v.code === code);
  if (existing) {
    existing.code = code;
    existing.type = type;
    existing.amount = amount;
    existing.minSpend = minSpend;
    existing.maxDiscount = maxDiscount;
    existing.expiry = expiry;
  }
  activeVoucherCode = code;
  renderVoucherChips();

  showToast(`Đã lưu thành công cấu hình Voucher "${code}" & chính sách vận chuyển!`, 'success');
}

function handleAddVoucherTypeChange(type) {
  const amountInput = document.getElementById('add-voucher-amount');
  if (amountInput) {
    amountInput.placeholder = type === 'percent' ? 'VD: 15% hoặc 20%' : 'VD: 30.000đ hoặc 50.000đ';
  }
}

function copyVoucherCode(code) {
  const codeEl = document.getElementById('voucher-code');
  const codeToCopy = code || (codeEl ? codeEl.value.trim().toUpperCase() : 'MONSTER10');
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(codeToCopy).catch(() => {});
  }
  showToast(`Đã sao chép mã voucher "${codeToCopy}" vào bộ nhớ tạm!`, 'info');
}

function openAddVoucherModal() {
  const form = document.getElementById('form-add-voucher');
  if (form) form.reset();
  const dateInput = document.getElementById('add-voucher-expiry');
  if (dateInput && !dateInput.value) {
    dateInput.value = '2026-12-31';
  }
  openAdminModal('modal-add-voucher');
}

function saveAddVoucher(e) {
  if (e && e.preventDefault) e.preventDefault();
  const codeEl = document.getElementById('add-voucher-code');
  const typeEl = document.getElementById('add-voucher-type');
  const amountEl = document.getElementById('add-voucher-amount');
  const minSpendEl = document.getElementById('add-voucher-min-spend');
  const maxDiscountEl = document.getElementById('add-voucher-max-discount');
  const expiryEl = document.getElementById('add-voucher-expiry');
  const targetEl = document.getElementById('add-voucher-target');
  const limitEl = document.getElementById('add-voucher-limit');

  const code = (codeEl && codeEl.value) ? codeEl.value.trim().toUpperCase() : 'ENERGY20';
  const type = typeEl ? typeEl.value : 'percent';
  const amount = (amountEl && amountEl.value) ? amountEl.value.trim() : '15%';
  const minSpend = (minSpendEl && minSpendEl.value) ? minSpendEl.value.trim() : '150.000đ';
  const maxDiscount = (maxDiscountEl && maxDiscountEl.value) ? maxDiscountEl.value.trim() : '40.000đ';
  const expiry = (expiryEl && expiryEl.value) ? expiryEl.value : '2026-12-31';
  const target = targetEl ? targetEl.value : 'all';
  const limit = (limitEl && limitEl.value) ? parseInt(limitEl.value, 10) : 500;

  const targetMap = {
    all: 'Tất cả khách hàng',
    vip: 'Chỉ khách hàng VIP',
    new: 'Chỉ khách hàng mới'
  };
  const targetText = targetMap[target] || 'Tất cả khách hàng';

  // Add or update in mock multi-voucher registry
  const existingIdx = MOCK_VOUCHERS_LIST.findIndex(v => v.code === code);
  const newVoucher = {
    code,
    type,
    amount,
    minSpend,
    maxDiscount,
    expiry,
    target,
    targetText,
    limit
  };

  if (existingIdx >= 0) {
    MOCK_VOUCHERS_LIST[existingIdx] = newVoucher;
  } else {
    MOCK_VOUCHERS_LIST.unshift(newVoucher);
  }

  activeVoucherCode = code;

  renderVoucherChips();

  // Ensure toggle is active
  const toggle = document.getElementById('voucher-toggle-active');
  if (toggle && !toggle.checked) {
    toggle.checked = true;
    handleVoucherStatusToggle(toggle);
  }

  closeAdminModal('modal-add-voucher');
  showToast(`Đã thêm mã Voucher mới "${code}" thành công! Hệ thống hiện đang quản lý ${MOCK_VOUCHERS_LIST.length} mã voucher chiến dịch.`, 'success');
}

// Auto-initialize components on DOM ready
if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      if (document.getElementById('voucher-chips-list')) {
        renderVoucherChips();
      }
      initPriceFormatting();
      initCustomUsersTable();
    });
  } else {
    if (document.getElementById('voucher-chips-list')) {
      renderVoucherChips();
    }
    initPriceFormatting();
    initCustomUsersTable();
  }
}

// ==========================================================================
// NAVIGATION BRAND BUTTONS & CATALOG PAGINATION
// ==========================================================================
var currentDashboardPage = 1;
if (typeof window !== 'undefined') {
  window.currentDashboardPage = 1;
}

function updatePaginationUI(pageNum) {
  if (typeof document === 'undefined') return;
  const strip = document.getElementById('catalog-pagination') || document.querySelector('.pagination-strip');
  if (!strip) return;

  const buttons = strip.querySelectorAll('.page-btn[data-page]');
  buttons.forEach(btn => {
    const p = parseInt(btn.getAttribute('data-page'), 10);
    if (p === pageNum) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });

  const prevBtn = strip.querySelector('#page-btn-prev') || strip.querySelector('.page-btn-prev') || strip.firstElementChild;
  const nextBtn = strip.querySelector('#page-btn-next') || strip.querySelector('.page-btn-next') || strip.lastElementChild;

  if (prevBtn) {
    if (pageNum <= 1) {
      prevBtn.classList.add('disabled');
      prevBtn.setAttribute('aria-disabled', 'true');
    } else {
      prevBtn.classList.remove('disabled');
      prevBtn.removeAttribute('aria-disabled');
    }
  }

  if (nextBtn) {
    if (pageNum >= 3) {
      nextBtn.classList.add('disabled');
      nextBtn.setAttribute('aria-disabled', 'true');
    } else {
      nextBtn.classList.remove('disabled');
      nextBtn.removeAttribute('aria-disabled');
    }
  }
}

function changeDashboardPage(pageNum, e) {
  if (e) {
    if (typeof e.preventDefault === 'function') e.preventDefault();
    if (typeof e.stopPropagation === 'function') e.stopPropagation();
  }
  const targetPage = parseInt(pageNum, 10);
  if (isNaN(targetPage) || targetPage < 1 || targetPage > 3) return false;

  currentDashboardPage = targetPage;
  if (typeof window !== 'undefined') {
    window.currentDashboardPage = targetPage;
  }

  updatePaginationUI(targetPage);

  const brandMap = {
    1: 'monster-products',
    2: 'redbull-products',
    3: 'sting-products'
  };

  const targetId = brandMap[targetPage];
  if (typeof document !== 'undefined') {
    const targetEl = document.getElementById(targetId);
    if (targetEl) {
      targetEl.scrollIntoView({ behavior: 'smooth' });
    }

    // Sync navbar active brand button
    const navLinks = document.querySelectorAll('.nav-menu .nav-link');
    if (navLinks.length >= 3) {
      navLinks.forEach((link, idx) => {
        if (idx === targetPage - 1) {
          link.classList.add('active');
        } else {
          link.classList.remove('active');
        }
      });
    }
  }

  return false;
}

function handleNavBrandClick(e, link, targetId) {
  if (e) {
    if (typeof e.preventDefault === 'function') e.preventDefault();
    if (typeof e.stopPropagation === 'function') e.stopPropagation();
  }
  if (!link) return false;

  if (!targetId) {
    const href = link.getAttribute('href') || link.getAttribute('data-target') || '';
    if (href.startsWith('#') && href.length > 1) {
      targetId = href.substring(1);
    } else if (href && !href.startsWith('#') && !href.startsWith('javascript')) {
      targetId = href;
    } else {
      const text = (link.textContent || '').toLowerCase();
      if (text.includes('monster')) targetId = 'monster-products';
      else if (text.includes('redbull')) targetId = 'redbull-products';
      else if (text.includes('sting')) targetId = 'sting-products';
    }
  }

  if (targetId && typeof document !== 'undefined') {
    const targetEl = document.getElementById(targetId);
    if (targetEl) {
      const yOffset = -110;
      const y = targetEl.getBoundingClientRect().top + window.pageYOffset + yOffset;
      window.scrollTo({ top: y, behavior: 'smooth' });

      // Sync pagination state
      let page = 1;
      if (targetId === 'redbull-products') page = 2;
      else if (targetId === 'sting-products') page = 3;

      currentDashboardPage = page;
      if (typeof window !== 'undefined') {
        window.currentDashboardPage = page;
      }
      updatePaginationUI(page);

      // Highlight active in both header nav and quick brand selector
      const brandKey = targetId.replace('-products', '');
      document.querySelectorAll('.nav-menu .nav-link, .quick-brand-nav .quick-brand-btn').forEach(btn => {
        const btnRef = (btn.getAttribute('href') || '') + ' ' + (btn.getAttribute('data-target') || '') + ' ' + (btn.textContent || '');
        if (btnRef.toLowerCase().includes(brandKey)) {
          btn.classList.add('active');
        } else {
          btn.classList.remove('active');
        }
      });
    } else {
      // Cross-page navigation from subpages
      const root = typeof window !== 'undefined' && window.SITE_ROOT ? window.SITE_ROOT : '../';
      window.location.href = root + 'index.html#' + targetId;
    }
  }

  return false;
}

if (typeof window !== 'undefined') {
  window.changeDashboardPage = changeDashboardPage;
  window.handleNavBrandClick = handleNavBrandClick;
  window.updatePaginationUI = updatePaginationUI;
}

if (typeof document !== 'undefined') {
  document.addEventListener('click', function(e) {
    const navLink = e.target.closest('.nav-menu .nav-link, .quick-brand-nav .quick-brand-btn');
    if (navLink) {
      if (typeof e.preventDefault === 'function') e.preventDefault();
      if (typeof e.stopPropagation === 'function') e.stopPropagation();
      handleNavBrandClick(e, navLink);
    }
  });
}
