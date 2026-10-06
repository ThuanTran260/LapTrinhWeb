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
  const rawName = (userEl ? userEl.value : '').trim();
  const username = rawName.toLowerCase();
  const ADMIN_USERS = ['admin', 'admin@monsterenergy.com'];

  try {
    localStorage.setItem('monster_user', rawName);
  } catch (err) { /* file:// riêng tư có thể chặn storage: bỏ qua */ }

  if (ADMIN_USERS.includes(username)) {
    showToast('Xác thực Quản trị viên thành công! Đang chuyển hướng...', 'success');
    setTimeout(() => { go('admin/index.html'); }, 900);
  } else {
    showToast('Đăng nhập thành công! Chào mừng quý khách quay lại mua sắm.', 'success');
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
  const amount = params.get('amount') || '210.600đ';
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

  showToast('Xác nhận đã nhận 210.600đ thành công cho đơn hàng ' + orderId + '! Đang hoàn tất...', 'success');
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
  const amount = params.get('amount') || '210.600đ';

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
    brand: 'Monster Energy (Hà Lan)',
    origin: 'Malaysia',
    price: '45.000đ',
    oldPrice: '55.000đ',
    volume: '355ml',
    ingredients: 'Nước bão hòa CO2, Sucroza, chiết xuất đường nho, chiết xuất nhân sâm,...',
    usage: 'Lắc nhẹ trước khi uống, dùng ngay sau khi mở nắp. Ngon hơn khi uống lạnh.',
    storage: 'Để nơi khô ráo, thoáng mát, tránh ánh sáng trực tiếp hoặc nơi có nhiệt độ cao.',
    status: 'Còn hàng',
    editPage: 'inventory.html'
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
  const modal = document.getElementById('modal-edit-product');
  if (!modal) return;

  const btn = triggerBtn || (window.event && window.event.target ? window.event.target.closest('button') : null);
  currentEditingRow = btn ? btn.closest('tr') : null;

  const prodKey = productId || 'monster-original';
  const data = PRODUCT_DATA_REGISTRY[prodKey] || PRODUCT_DATA_REGISTRY['monster-original'];

  const nameEl = document.getElementById('edit-prod-name');
  const brandEl = document.getElementById('edit-prod-brand');
  const originEl = document.getElementById('edit-prod-origin');
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
  if (priceEl) priceEl.value = data.price;
  if (oldPriceEl) oldPriceEl.value = data.oldPrice;
  if (volumeEl) volumeEl.value = data.volume;
  if (ingredientsEl) ingredientsEl.value = data.ingredients;
  if (usageEl) usageEl.value = data.usage;
  if (storageEl) storageEl.value = data.storage;
  if (statusEl) statusEl.value = data.status;

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
  const brandEl = document.getElementById('edit-prod-brand');
  const priceEl = document.getElementById('edit-prod-price');
  const volumeEl = document.getElementById('edit-prod-volume');
  const statusEl = document.getElementById('edit-prod-status');

  const name = nameEl ? nameEl.value : 'Sản phẩm';

  // Live update the table row in DOM
  if (currentEditingRow) {
    const cells = currentEditingRow.cells;
    if (cells && cells.length >= 6) {
      if (cells[1]) {
        const strong = cells[1].querySelector('strong');
        if (strong) strong.textContent = name;
        else cells[1].innerHTML = '<strong>' + name + '</strong>';
      }
      if (cells[2] && brandEl) cells[2].textContent = brandEl.value;
      if (cells[3] && volumeEl) cells[3].textContent = volumeEl.value;
      if (cells[4] && priceEl) cells[4].textContent = priceEl.value;
      if (cells[5] && statusEl) {
        const isAvail = statusEl.value === 'Còn hàng';
        const badgeClass = isAvail ? 'success' : (statusEl.value.includes('Sắp') ? 'warning' : 'danger');
        cells[5].innerHTML = '<span class="badge-status ' + badgeClass + '">' + statusEl.value.toUpperCase() + '</span>';
      }
    }
  }

  showToast('Đã lưu thay đổi thông tin sản phẩm "' + name + '" thành công!', 'success');
  closeAdminModal('modal-edit-product');
}

// 9b. Add Product Modal Logic
function openAddProductModal() {
  const form = document.getElementById('form-add-product');
  if (form) form.reset();
  openAdminModal('modal-add-product');
}

function saveAddProduct(e) {
  if (e && e.preventDefault) e.preventDefault();
  const nameEl = document.getElementById('add-prod-name');
  const brandEl = document.getElementById('add-prod-brand');
  const priceEl = document.getElementById('add-prod-price');
  const volumeEl = document.getElementById('add-prod-volume');
  const statusEl = document.getElementById('add-prod-status');

  const name = (nameEl && nameEl.value) ? nameEl.value : 'Nước Tăng Lực Mới';
  const brand = (brandEl && brandEl.value) ? brandEl.value : 'Monster Energy';
  const price = (priceEl && priceEl.value) ? priceEl.value : '48.000đ';
  const volume = (volumeEl && volumeEl.value) ? volumeEl.value : '355ml';
  const status = (statusEl && statusEl.value) ? statusEl.value : 'Còn hàng';

  // Live append to table in DOM
  const tbody = document.querySelector('#inventory-section table.cart-table tbody') || document.querySelector('table.cart-table tbody');
  if (tbody) {
    const isAvail = status === 'Còn hàng';
    const badgeClass = isAvail ? 'success' : 'warning';
    const newTr = document.createElement('tr');
    newTr.innerHTML = `
      <td><img src="../assets/images/monster/original.webp" alt="${name}" style="width: 36px; height: 46px; object-fit: contain;" /></td>
      <td><strong>${name}</strong></td>
      <td>${brand}</td>
      <td>${volume}</td>
      <td>${price}</td>
      <td><span class="badge-status ${badgeClass}">${status.toUpperCase()}</span></td>
      <td>
        <button class="btn-view-detail" style="padding: 4px 8px; font-size: 0.8rem; display: inline-flex;" onclick="openProductEditModal('custom', this)" title="Chỉnh sửa sản phẩm"><i class="fas fa-edit"></i></button>
        <button class="cart-del-btn" style="padding: 4px 8px;" onclick="this.closest('tr').remove(); showToast('Đã xóa sản phẩm khỏi danh sách!', 'info')" title="Xóa"><i class="fas fa-trash"></i></button>
      </td>
    `;
    tbody.prepend(newTr);
  }

  showToast('Đã thêm sản phẩm "' + name + '" vào kho hàng thành công!', 'success');
  closeAdminModal('modal-add-product');
}

// 9c. Customer VIP Detail Modal Logic
function openCustomerDetailModal(customerName) {
  // Dù bấm Tuấn hay An hay Bích,... đều mở chi tiết hồ sơ VIP của Phạm Minh Tuấn
  openAdminModal('modal-customer-detail');
}

// 9d. Order Detail Modal Logic
function openOrderDetailModal(orderId) {
  // Mở popup chi tiết đơn hàng mẫu #EB-8801
  openAdminModal('modal-order-detail');
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


