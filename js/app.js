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
  const nameEl = document.getElementById('order-fullname');
  const phoneEl = document.getElementById('order-phone');
  const addrEl = document.getElementById('order-address');
  const notesEl = document.getElementById('order-notes');

  const name = (nameEl ? nameEl.value : '').trim();
  const phone = (phoneEl ? phoneEl.value : '').trim();
  const address = (addrEl ? addrEl.value : '').trim();
  const notes = (notesEl ? notesEl.value : '').trim();

  // Validate Họ và tên (tối thiểu 2 ký tự)
  if (name.length < 2) {
    showToast('Vui lòng nhập họ và tên người nhận hợp lệ (tối thiểu 2 ký tự)!', 'warning');
    if (nameEl) nameEl.focus();
    return;
  }

  // Validate Số điện thoại chuẩn Việt Nam: 10 chữ số bắt đầu bằng 0
  const phoneRegex = /^0\d{9}$/;
  if (!phoneRegex.test(phone)) {
    showToast('Số điện thoại không hợp lệ! Vui lòng nhập đúng 10 chữ số bắt đầu bằng 0 (VD: 0912345678).', 'warning');
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

  // Sinh mã đơn hàng động duy nhất
  const orderId = 'ME-' + Date.now().toString().slice(-4);

  // Đóng gói params qua URLSearchParams
  const params = new URLSearchParams({
    order: orderId,
    name: name,
    phone: phone,
    address: address,
    notes: notes,
    method: method,
    amount: '210.600đ',
    items: '5'
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
