/**
 * MYKINGDOM TOY STORE - MAIN APP LOGIC
 */

// Global State
let cart = JSON.parse(localStorage.getItem('mykingdom_cart')) || [];
let wishlist = JSON.parse(localStorage.getItem('mykingdom_wishlist')) || [];
let currentCategory = 'Tất cả';
let currentAgeGroup = 'Tất cả';
let currentBrand = 'Tất cả';
let currentSort = 'default';
let searchQuery = '';
let activeDiscount = 0; // % giảm giá từ mã coupon

// DOM Elements
document.addEventListener('DOMContentLoaded', () => {
  initHeroSlider();
  initFlashSaleCountdown();
  renderFilters();
  renderProducts();
  renderFlashSaleProducts();
  updateCartUI();
  updateWishlistUI();
  setupEventListeners();
});

/* ==========================================================================
   1. HERO SLIDER LOGIC
   ========================================================================== */
function initHeroSlider() {
  const slides = document.querySelectorAll('.hero-slide');
  const dots = document.querySelectorAll('.dot');
  let currentSlide = 0;

  if (!slides.length) return;

  function showSlide(index) {
    slides.forEach((slide, i) => {
      slide.classList.toggle('active', i === index);
    });
    dots.forEach((dot, i) => {
      dot.classList.toggle('active', i === index);
    });
    currentSlide = index;
  }

  dots.forEach((dot, i) => {
    dot.addEventListener('click', () => showSlide(i));
  });

  // Auto slide every 5 seconds
  setInterval(() => {
    let nextIndex = (currentSlide + 1) % slides.length;
    showSlide(nextIndex);
  }, 5000);
}

/* ==========================================================================
   2. FLASH SALE COUNTDOWN TIMER
   ========================================================================== */
function initFlashSaleCountdown() {
  const hoursEl = document.getElementById('flash-hours');
  const minsEl = document.getElementById('flash-mins');
  const secsEl = document.getElementById('flash-secs');

  if (!hoursEl) return;

  // Đếm ngược 8 tiếng giả định
  let totalSeconds = 8 * 3600 + 45 * 60 + 30;

  function updateTimer() {
    if (totalSeconds <= 0) {
      totalSeconds = 8 * 3600; // Reset
    }
    totalSeconds--;

    const h = Math.floor(totalSeconds / 3600);
    const m = Math.floor((totalSeconds % 3600) / 60);
    const s = totalSeconds % 60;

    hoursEl.textContent = String(h).padStart(2, '0');
    minsEl.textContent = String(m).padStart(2, '0');
    secsEl.textContent = String(s).padStart(2, '0');
  }

  updateTimer();
  setInterval(updateTimer, 1000);
}

/* ==========================================================================
   3. RENDER FILTERS & TOOLBAR
   ========================================================================== */
function renderFilters() {
  const categoryPillsContainer = document.getElementById('category-pills');
  const agePillsContainer = document.getElementById('age-pills');
  const brandSelect = document.getElementById('brand-select');

  // Category Pills
  if (categoryPillsContainer) {
    categoryPillsContainer.innerHTML = CATEGORIES.map(cat => `
      <button class="filter-pill ${cat === currentCategory ? 'active' : ''}" onclick="filterCategory('${cat}')">
        ${cat}
      </button>
    `).join('');
  }

  // Age Pills
  if (agePillsContainer) {
    agePillsContainer.innerHTML = AGE_GROUPS.map(age => `
      <button class="filter-pill ${age === currentAgeGroup ? 'active' : ''}" onclick="filterAge('${age}')">
        ${age}
      </button>
    `).join('');
  }

  // Brand Select
  if (brandSelect) {
    brandSelect.innerHTML = BRANDS.map(b => `<option value="${b}">${b}</option>`).join('');
  }
}

function filterCategory(cat) {
  currentCategory = cat;
  renderFilters();
  renderProducts();
}

function filterAge(age) {
  currentAgeGroup = age;
  renderFilters();
  renderProducts();
}

/* ==========================================================================
   4. RENDER PRODUCTS GRID & FLASH SALE
   ========================================================================== */
function getFilteredProducts() {
  return PRODUCTS_DATA.filter(p => {
    const matchCat = currentCategory === 'Tất cả' || p.category === currentCategory;
    const matchAge = currentAgeGroup === 'Tất cả' || p.ageGroup === currentAgeGroup;
    const matchBrand = currentBrand === 'Tất cả' || p.brand === currentBrand;
    const matchSearch = p.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
                        p.brand.toLowerCase().includes(searchQuery.toLowerCase()) ||
                        p.category.toLowerCase().includes(searchQuery.toLowerCase());
    return matchCat && matchAge && matchBrand && matchSearch;
  }).sort((a, b) => {
    if (currentSort === 'price-low') return a.price - b.price;
    if (currentSort === 'price-high') return b.price - a.price;
    if (currentSort === 'rating') return b.rating - a.rating;
    if (currentSort === 'discount') return b.discountPercent - a.discountPercent;
    return 0;
  });
}

function renderProducts() {
  const grid = document.getElementById('main-products-grid');
  if (!grid) return;

  const filtered = getFilteredProducts();

  if (filtered.length === 0) {
    grid.innerHTML = `
      <div class="no-results">
        <i class="fas fa-ghost"></i>
        <h3>Không tìm thấy sản phẩm nào!</h3>
        <p>Vui lòng thử thay đổi từ khóa tìm kiếm hoặc bỏ chọn các bộ lọc.</p>
      </div>
    `;
    return;
  }

  grid.innerHTML = filtered.map(p => createProductCardHTML(p)).join('');
}

function renderFlashSaleProducts() {
  const flashGrid = document.getElementById('flash-products-grid');
  if (!flashGrid) return;

  const flashItems = PRODUCTS_DATA.filter(p => p.isFlashSale).slice(0, 4);

  flashGrid.innerHTML = flashItems.map(p => createProductCardHTML(p, true)).join('');
}

function createProductCardHTML(p, isFlash = false) {
  const isWishlisted = wishlist.includes(p.id);

  return `
    <div class="product-card">
      <span class="product-badge badge-${p.badgeType}">${p.badge}</span>
      <button class="wishlist-toggle-btn ${isWishlisted ? 'active' : ''}" onclick="toggleWishlist('${p.id}')">
        <i class="${isWishlisted ? 'fas' : 'far'} fa-heart"></i>
      </button>

      <div class="product-img-wrapper">
        <img src="${p.image}" alt="${p.name}" class="product-img" loading="lazy" />
        <div class="quick-view-overlay">
          <button class="btn-quick-view" onclick="openQuickView('${p.id}')">
            <i class="fas fa-eye"></i> Xem nhanh
          </button>
        </div>
      </div>

      <div class="product-details">
        <div class="product-meta">
          <span class="product-brand">${p.brand}</span>
          <span class="product-age"><i class="fas fa-child"></i> ${p.ageGroup}</span>
        </div>

        <h3 class="product-title" title="${p.name}">${p.name}</h3>

        <div class="rating-box">
          <i class="fas fa-star"></i>
          <span>${p.rating}</span>
          <span class="reviews-count">(${p.reviewsCount})</span>
        </div>

        <div class="price-wrapper">
          <span class="current-price">${formatCurrency(p.price)}</span>
          <span class="original-price">${formatCurrency(p.originalPrice)}</span>
        </div>

        ${isFlash ? `
          <div class="stock-progress">
            <div class="stock-bar" style="width: ${(p.stockLeft / p.totalStock) * 100}%"></div>
            <span class="stock-text">Đã bán ${p.totalStock - p.stockLeft}/${p.totalStock}</span>
          </div>
        ` : ''}

        <button class="btn-add-cart" onclick="addToCart('${p.id}')">
          <i class="fas fa-cart-plus"></i> Thêm vào giỏ
        </button>
      </div>
    </div>
  `;
}

/* ==========================================================================
   5. CART & WISHLIST STATE MANAGEMENT
   ========================================================================== */
function addToCart(productId, qty = 1) {
  const product = PRODUCTS_DATA.find(p => p.id === productId);
  if (!product) return;

  const existingItem = cart.find(item => item.id === productId);
  if (existingItem) {
    existingItem.quantity += qty;
  } else {
    cart.push({ ...product, quantity: qty });
  }

  saveCart();
  updateCartUI();
  triggerBadgeBounce();
  showToast(`Đã thêm <b>${product.name.slice(0, 25)}...</b> vào giỏ hàng!`, 'success');
}

function updateCartQuantity(productId, delta) {
  const item = cart.find(i => i.id === productId);
  if (!item) return;

  item.quantity += delta;
  if (item.quantity <= 0) {
    cart = cart.filter(i => i.id !== productId);
  }

  saveCart();
  updateCartUI();
}

function removeFromCart(productId) {
  cart = cart.filter(i => i.id !== productId);
  saveCart();
  updateCartUI();
  showToast('Đã xóa sản phẩm khỏi giỏ hàng', 'info');
}

function saveCart() {
  localStorage.setItem('mykingdom_cart', JSON.stringify(cart));
}

function updateCartUI() {
  const cartBadge = document.getElementById('cart-badge');
  const cartSubtotalEl = document.getElementById('cart-subtotal');
  const cartDiscountEl = document.getElementById('cart-discount');
  const cartTotalEl = document.getElementById('cart-total');
  const drawerItemsList = document.getElementById('drawer-items-list');

  const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
  const subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  const discountAmount = Math.round(subtotal * (activeDiscount / 100));
  const finalTotal = subtotal - discountAmount;

  if (cartBadge) cartBadge.textContent = totalItems;
  if (cartSubtotalEl) cartSubtotalEl.textContent = formatCurrency(subtotal);
  if (cartDiscountEl) cartDiscountEl.textContent = `-${formatCurrency(discountAmount)}`;
  if (cartTotalEl) cartTotalEl.textContent = formatCurrency(finalTotal);

  if (drawerItemsList) {
    if (cart.length === 0) {
      drawerItemsList.innerHTML = `
        <div style="text-align: center; padding: 40px 10px; color: #888;">
          <i class="fas fa-shopping-basket" style="font-size: 3rem; color: #FF2E63; margin-bottom: 12px;"></i>
          <p>Giỏ hàng của bạn hiện đang trống!</p>
        </div>
      `;
    } else {
      drawerItemsList.innerHTML = cart.map(item => `
        <div class="cart-item">
          <img src="${item.image}" alt="${item.name}" class="cart-item-img" />
          <div class="cart-item-info">
            <h4 class="cart-item-title">${item.name}</h4>
            <div class="cart-item-price">${formatCurrency(item.price)}</div>
            <div class="quantity-picker">
              <button class="qty-btn" onclick="updateCartQuantity('${item.id}', -1)">-</button>
              <input type="text" class="qty-input" value="${item.quantity}" readonly />
              <button class="qty-btn" onclick="updateCartQuantity('${item.id}', 1)">+</button>
            </div>
          </div>
          <button class="cart-item-remove" onclick="removeFromCart('${item.id}')">
            <i class="fas fa-trash-alt"></i>
          </button>
        </div>
      `).join('');
    }
  }
}

function applyCouponCode() {
  const couponInput = document.getElementById('coupon-input');
  if (!couponInput) return;
  const code = couponInput.value.trim().toUpperCase();

  if (code === 'KINGDOM50' || code === 'MYKINGDOM') {
    activeDiscount = 10; // Giảm 10%
    showToast('Áp dụng mã giảm 10% thành công!', 'success');
    updateCartUI();
  } else if (code === 'FREESHIP') {
    showToast('Mã miễn phí vận chuyển đã được kích hoạt!', 'success');
  } else {
    showToast('Mã giảm giá không hợp lệ!', 'info');
  }
}

/* Wishlist Logic */
function toggleWishlist(productId) {
  const index = wishlist.indexOf(productId);
  if (index > -1) {
    wishlist.splice(index, 1);
    showToast('Đã xóa khỏi danh sách yêu thích', 'info');
  } else {
    wishlist.push(productId);
    showToast('Đã thêm vào danh sách yêu thích!', 'success');
  }

  localStorage.setItem('mykingdom_wishlist', JSON.stringify(wishlist));
  updateWishlistUI();
  renderProducts();
  renderFlashSaleProducts();
}

function updateWishlistUI() {
  const wishlistBadge = document.getElementById('wishlist-badge');
  if (wishlistBadge) wishlistBadge.textContent = wishlist.length;
}

function triggerBadgeBounce() {
  const badge = document.getElementById('cart-badge');
  if (badge) {
    badge.classList.add('bounce');
    setTimeout(() => badge.classList.remove('bounce'), 400);
  }
}

/* ==========================================================================
   6. QUICK VIEW MODAL LOGIC
   ========================================================================== */
function openQuickView(productId) {
  const product = PRODUCTS_DATA.find(p => p.id === productId);
  if (!product) return;

  const modalOverlay = document.getElementById('quickview-modal');
  const modalContainer = document.getElementById('modal-body-content');

  if (!modalOverlay || !modalContainer) return;

  modalContainer.innerHTML = `
    <div class="modal-grid">
      <div>
        <img src="${product.image}" alt="${product.name}" class="modal-product-img" />
      </div>
      <div class="modal-product-info">
        <span class="product-badge badge-${product.badgeType}">${product.badge}</span>
        <h2 style="margin-top: 10px;">${product.name}</h2>
        <div class="rating-box" style="margin-bottom: 12px;">
          <i class="fas fa-star"></i> <span>${product.rating}</span>
          <span class="reviews-count">(${product.reviewsCount} đánh giá từ khách hàng)</span>
        </div>
        <div class="price-wrapper" style="margin-bottom: 16px;">
          <span class="current-price" style="font-size: 1.5rem;">${formatCurrency(product.price)}</span>
          <span class="original-price" style="font-size: 1.1rem;">${formatCurrency(product.originalPrice)}</span>
        </div>
        <p class="modal-description">${product.description}</p>
        
        <table class="modal-specs-table">
          <tr><td>Thương hiệu</td><td><b>${product.brand}</b></td></tr>
          <tr><td>Độ tuổi phù hợp</td><td>${product.ageGroup}</td></tr>
          <tr><td>Chất liệu</td><td>${product.specs.material}</td></tr>
          <tr><td>Xuất xứ</td><td>${product.specs.origin}</td></tr>
          <tr><td>Số chi tiết</td><td>${product.specs.pieces} chi tiết</td></tr>
        </table>

        <div style="display: flex; gap: 12px; align-items: center;">
          <div class="quantity-picker" style="height: 42px;">
            <button class="qty-btn" style="width: 36px;" onclick="adjustModalQty(-1)">-</button>
            <input type="text" id="modal-qty-input" class="qty-input" value="1" readonly style="width: 44px;" />
            <button class="qty-btn" style="width: 36px;" onclick="adjustModalQty(1)">+</button>
          </div>
          <button class="btn-add-cart" style="flex: 1; height: 42px;" onclick="addModalItemToCart('${product.id}')">
            <i class="fas fa-shopping-cart"></i> Thêm Vào Giỏ hàng
          </button>
        </div>
      </div>
    </div>
  `;

  modalOverlay.classList.add('active');
}

function adjustModalQty(delta) {
  const qtyInput = document.getElementById('modal-qty-input');
  if (!qtyInput) return;
  let val = parseInt(qtyInput.value) || 1;
  val = Math.max(1, val + delta);
  qtyInput.value = val;
}

function addModalItemToCart(productId) {
  const qtyInput = document.getElementById('modal-qty-input');
  const qty = parseInt(qtyInput ? qtyInput.value : 1) || 1;
  addToCart(productId, qty);
  closeModal();
}

function closeModal() {
  const modalOverlay = document.getElementById('quickview-modal');
  if (modalOverlay) modalOverlay.classList.remove('active');
}

/* ==========================================================================
   7. EVENT LISTENERS & UTILS
   ========================================================================== */
function setupEventListeners() {
  // Drawer Toggles
  const cartTrigger = document.getElementById('cart-drawer-trigger');
  const closeCartBtn = document.getElementById('close-cart-btn');
  const cartOverlay = document.getElementById('cart-overlay');
  const cartDrawer = document.getElementById('cart-drawer');

  if (cartTrigger) {
    cartTrigger.addEventListener('click', () => {
      cartOverlay.classList.add('active');
      cartDrawer.classList.add('active');
    });
  }

  if (closeCartBtn) {
    closeCartBtn.addEventListener('click', closeCartDrawer);
  }
  if (cartOverlay) {
    cartOverlay.addEventListener('click', closeCartDrawer);
  }

  // Search Input
  const searchInput = document.getElementById('search-input');
  const searchDropdown = document.getElementById('search-dropdown');

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value.trim();
      renderProducts();
      updateSearchDropdown(searchQuery, searchDropdown);
    });
  }

  // Brand Select
  const brandSelect = document.getElementById('brand-select');
  if (brandSelect) {
    brandSelect.addEventListener('change', (e) => {
      currentBrand = e.target.value;
      renderProducts();
    });
  }

  // Sort Select
  const sortSelect = document.getElementById('sort-select');
  if (sortSelect) {
    sortSelect.addEventListener('change', (e) => {
      currentSort = e.target.value;
      renderProducts();
    });
  }
}

function updateSearchDropdown(query, dropdownEl) {
  if (!dropdownEl) return;
  if (!query) {
    dropdownEl.classList.remove('active');
    return;
  }

  const matches = PRODUCTS_DATA.filter(p => p.name.toLowerCase().includes(query.toLowerCase())).slice(0, 5);

  if (matches.length === 0) {
    dropdownEl.classList.remove('active');
    return;
  }

  dropdownEl.innerHTML = matches.map(p => `
    <div class="search-item" onclick="openQuickView('${p.id}')">
      <img src="${p.image}" alt="${p.name}" />
      <div class="search-item-info">
        <div class="search-item-title">${p.name}</div>
        <div class="search-item-price">${formatCurrency(p.price)}</div>
      </div>
    </div>
  `).join('');
  dropdownEl.classList.add('active');
}

function closeCartDrawer() {
  document.getElementById('cart-overlay').classList.remove('active');
  document.getElementById('cart-drawer').classList.remove('active');
}

function formatCurrency(amount) {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount);
}

function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <i class="toast-icon fas ${type === 'success' ? 'fa-check-circle' : 'fa-info-circle'}"></i>
    <span class="toast-message">${message}</span>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 3000);
}

function checkoutSimulation() {
  if (cart.length === 0) {
    showToast('Giỏ hàng trống! Vui lòng chọn thêm sản phẩm', 'info');
    return;
  }

  alert('🎉 Cảm ơn bạn đã đặt hàng tại Vương Quốc Đồ Chơi!\n\nĐơn hàng của bạn đã được tiếp nhận và xử lý giao hàng siêu tốc trong 2 giờ.');
  cart = [];
  saveCart();
  updateCartUI();
  closeCartDrawer();
}
