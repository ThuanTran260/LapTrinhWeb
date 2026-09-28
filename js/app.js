/**
 * MONSTER ENERGY STORE - LIGHTWEIGHT NOTIFICATIONS
 * Chỉ phục vụ thông báo trạng thái giao diện khi click
 */

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

/**
 * LIGHTBOX - Phóng to duy nhất 1 ảnh sản phẩm khi click
 */
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
