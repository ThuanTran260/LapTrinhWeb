/**
 * ENERGY BOOST STORE - ORBITAL TELEMETRY 2026 MOTION & STOREFRONT ENGINE
 * GSAP 3.14 (ScrollTrigger, SplitText, Flip, Observer) + 2.5D Solar Orbit Stage
 * + OrbitalCart + Ctrl+K Command Palette + Product Detail Inspection Chamber.
 *
 * Strictly 1:1 native compositor scroll, zero wheel-hijacking, compositor-friendly transforms,
 * WCAG reduced-motion safe, and 100% compatible with both file:// and HTTPS hosting.
 */
(function (window, document) {
  'use strict';

  if (typeof window === 'undefined' || typeof document === 'undefined') {
    return;
  }

  // ==========================================================================
  // 0. CANONICAL 10-SKU ORBITAL CATALOG
  // ==========================================================================
  const ORBITAL_CATALOG = [
    {
      id: 'mn-1',
      code: 'OBS-MN01',
      name: 'Monster Energy Original 355ml',
      brand: 'monster',
      brandLabel: 'Monster Energy',
      price: 45000,
      oldPrice: 55000,
      badge: '-18%',
      volume: '355ml',
      origin: 'Hà Lan / Malaysia',
      specs: 'Taurine 400mg/100ml · Caffeine 30mg/100ml · Vitamin B3, B6, B2, B12',
      detailUrl: 'pages/product-detail.html',
      image: 'assets/images/monster/original.webp',
      gallery: [
        'assets/images/monster/original.webp',
        'assets/images/monster/original-back-1.webp',
        'assets/images/monster/original-back-2.webp',
        'assets/images/monster/original-with-glass.webp'
      ],
      tags: ['original', 'monster'],
      keywords: 'energy boost nước tăng lực monster original hà lan truyền thống xanh lá'
    },
    {
      id: 'mn-2',
      code: 'OBS-MN02',
      name: 'Monster Zero Ultra White 500ml',
      brand: 'monster',
      brandLabel: 'Monster Ultra',
      price: 48000,
      oldPrice: 55000,
      badge: '-13%',
      volume: '500ml',
      origin: 'Hà Lan / Malaysia',
      specs: '0g Đường · Zero Calories · Hương cam chanh thanh mát · Vitamin B-Complex',
      detailUrl: 'pages/product-detail.html?sku=mn-2',
      image: 'assets/images/monster/ultra-white.webp',
      gallery: ['assets/images/monster/ultra-white.webp'],
      tags: ['zero-sugar', 'monster'],
      keywords: 'energy boost nước tăng lực monster zero sugar không đường trắng ultra white calo thấp'
    },
    {
      id: 'mn-3',
      code: 'OBS-MN03',
      name: 'Monster Ultra Paradise 500ml',
      brand: 'monster',
      brandLabel: 'Monster Ultra',
      price: 48000,
      oldPrice: null,
      badge: 'ZERO SUGAR',
      volume: '500ml',
      origin: 'Hà Lan / Malaysia',
      specs: '0g Đường · Vị Kiwi, Chanh xanh & Dưa leo · Taurine & Caffeine',
      detailUrl: 'pages/product-detail.html?sku=mn-3',
      image: 'assets/images/monster/ultra-paradise.webp',
      gallery: ['assets/images/monster/ultra-paradise.webp'],
      tags: ['zero-sugar', 'monster'],
      keywords: 'energy boost nước tăng lực monster kiwi chanh dưa leo xanh lá paradise ultra zero sugar'
    },
    {
      id: 'mn-4',
      code: 'OBS-MN04',
      name: 'Monster Ultra Punk Punch 500ml',
      brand: 'monster',
      brandLabel: 'Monster Ultra',
      price: 50000,
      oldPrice: null,
      badge: 'FRUIT PUNCH',
      volume: '500ml',
      origin: 'Hà Lan / Malaysia',
      specs: 'Hương Fruit Punch trái cây nhiệt đới · Taurine, Nhân sâm & Vitamin B',
      detailUrl: 'pages/product-detail.html?sku=mn-4',
      image: 'assets/images/monster/ultra-punk-punch.webp',
      gallery: ['assets/images/monster/ultra-punk-punch.webp'],
      tags: ['monster'],
      keywords: 'energy boost nước tăng lực monster fruit punch hoa quả trái cây nhiệt đới hồng tím punk'
    },
    {
      id: 'rb-1',
      code: 'OBS-RB01',
      name: 'Nước Tăng Lực Redbull Original 250ml',
      brand: 'redbull',
      brandLabel: 'Redbull Thái Lan',
      price: 18000,
      oldPrice: 22000,
      badge: '-18%',
      volume: '250ml',
      origin: 'Thái Lan',
      specs: 'Kẽm & Vitamin B3, B5, B6, B12 · Taurine & Caffeine',
      detailUrl: 'pages/product-detail-redbull.html',
      image: 'assets/images/redbull/redbull-original.webp',
      gallery: ['assets/images/redbull/redbull-original.webp'],
      tags: ['redbull'],
      keywords: 'energy boost nước tăng lực redbull bò húc bò cụng original vàng truyền thống thái lan'
    },
    {
      id: 'rb-2',
      code: 'OBS-RB02',
      name: 'Nước Tăng Lực Redbull Thái Lan Nhập Khẩu 250ml',
      brand: 'redbull',
      brandLabel: 'Redbull Krating Daeng',
      price: 18000,
      oldPrice: 22000,
      badge: '-18%',
      volume: '250ml',
      origin: 'Thái Lan (Nhập khẩu)',
      specs: 'Taurine 1000mg · Caffeine 50mg · Inositol & Vitamin nhóm B',
      detailUrl: 'pages/product-detail-redbull-thai.html',
      image: 'assets/images/redbull/redbull-thai.webp',
      gallery: ['assets/images/redbull/redbull-thai.webp'],
      tags: ['redbull'],
      keywords: 'energy boost nước tăng lực redbull krating daeng thái lan nhập khẩu đậm đà 250ml'
    },
    {
      id: 'rb-3',
      code: 'OBS-RB03',
      name: 'Nước Tăng Lực Redbull Nắp Bật 250ml',
      brand: 'redbull',
      brandLabel: 'Redbull Sleek Edition',
      price: 20000,
      oldPrice: 25000,
      badge: '-20%',
      volume: '250ml',
      origin: 'Thái Lan (Sleek Can)',
      specs: 'Taurine 800mg · Caffeine 80mg · Nhân sâm & Kẽm sinh học',
      detailUrl: 'pages/product-detail-redbull-lonvua.html',
      image: 'assets/images/redbull/redbull-lon-vua.webp',
      gallery: ['assets/images/redbull/redbull-lon-vua.webp'],
      tags: ['redbull'],
      keywords: 'energy boost nước tăng lực redbull sleek can nắp bật tiện lợi cao cấp lon lùn vừa'
    },
    {
      id: 'st-1',
      code: 'OBS-ST01',
      name: 'Nước Tăng Lực Sting Dâu Tây Đỏ Sleek 330ml',
      brand: 'sting',
      brandLabel: 'Sting PepsiCo',
      price: 12000,
      oldPrice: 15000,
      badge: '-20%',
      volume: '330ml',
      origin: 'Việt Nam (Suntory PepsiCo)',
      specs: 'Hương dâu tây đỏ · Hồng sâm, Taurine, Inositol & Vitamin B',
      detailUrl: 'pages/product-detail-sting.html',
      image: 'assets/images/sting/sting-dau.webp',
      gallery: ['assets/images/sting/sting-dau.webp'],
      tags: ['sting'],
      keywords: 'energy boost nước tăng lực sting dâu tây đỏ pepsico ga sảng khoái 330ml'
    },
    {
      id: 'st-2',
      code: 'OBS-ST02',
      name: 'Nước Tăng Lực Sting Vàng Sleek 330ml',
      brand: 'sting',
      brandLabel: 'Sting PepsiCo',
      price: 12000,
      oldPrice: null,
      badge: 'NHÂN SÂM',
      volume: '330ml',
      origin: 'Việt Nam (Suntory PepsiCo)',
      specs: 'Chiết xuất nhân sâm vàng · Taurine & Vitamin nhóm B',
      detailUrl: 'pages/product-detail-sting.html?sku=st-2',
      image: 'assets/images/sting/sting-gold.webp',
      gallery: ['assets/images/sting/sting-gold.webp'],
      tags: ['sting'],
      keywords: 'energy boost nước tăng lực sting vàng nhân sâm ginseng sleek pepsico gold 330ml'
    },
    {
      id: 'st-3',
      code: 'OBS-ST03',
      name: 'Nước Tăng Lực Sting Blue Sleek 320ml',
      brand: 'sting',
      brandLabel: 'Sting PepsiCo',
      price: 13000,
      oldPrice: null,
      badge: 'VIỆT QUẤT',
      volume: '320ml',
      origin: 'Việt Nam (Suntory PepsiCo)',
      specs: 'Hương việt quất xanh mát lạnh · Taurine, Caffeine & Vitamin B',
      detailUrl: 'pages/product-detail-sting.html?sku=st-3',
      image: 'assets/images/sting/sting-vietquat.webp',
      gallery: ['assets/images/sting/sting-vietquat.webp'],
      tags: ['sting'],
      keywords: 'energy boost nước tăng lực sting blue việt quất xanh dương sleek mát lạnh 320ml'
    }
  ];

  const CATALOG_BY_ID = new Map();
  for (let i = 0; i < ORBITAL_CATALOG.length; i++) {
    CATALOG_BY_ID.set(ORBITAL_CATALOG[i].id, ORBITAL_CATALOG[i]);
  }

  const STORAGE_COUNT_KEY = 'orbital_cart_count';
  const STORAGE_TOTAL_KEY = 'orbital_cart_total';
  const DEFAULT_CART = { count: 7, total: 216000 };
  const VALID_SYSTEMS = new Set(['monster', 'redbull', 'sting']);

  // ==========================================================================
  // 1. MODULE STATE & UTILITIES
  // ==========================================================================
  const runtime = {
    initialized: false,
    reducedMotion: false,
    pointerFine: false,
    cleanups: [],
    observers: [],
    intervals: [],
    timers: new Set(),
    gsapCtx: null,
    gsapMatchMedia: null,
    orbit: {
      stage: null,
      reticle: null,
      nodes: [],
      nodeData: [],
      lockedSku: 'mn-1',
      rafId: 0,
      lastTs: 0,
      stageW: 520,
      stageH: 420,
      hovered: false,
      focused: false,
      inViewport: true,
      reticleNeedsCenter: false
    },
    vaultState: {
      brand: 'all',
      tag: 'all',
      sort: 'default',
      query: ''
    },
    cmdState: {
      isOpen: false,
      activeIndex: 0,
      items: [],
      lastFocused: null
    },
    cartPulseTimer: 0,
    memoryCart: { count: DEFAULT_CART.count, total: DEFAULT_CART.total }
  };

  function getSkuById(skuId) {
    if (!skuId) return null;
    return CATALOG_BY_ID.get(String(skuId).trim()) || null;
  }

  function isInsidePages() {
    const p = String((window.location && window.location.pathname) || '');
    const h = String((window.location && window.location.href) || '');
    return p.includes('/pages/') || h.includes('/pages/');
  }

  function resolvePath(rootRelativePath) {
    if (!rootRelativePath) return '#';
    const str = String(rootRelativePath);
    if (/^(https?:|data:|#|\/|\.\.\/)/i.test(str)) {
      return str;
    }
    return isInsidePages() ? ('../' + str) : str;
  }

  function normalizeVietnamese(str) {
    if (!str) return '';
    return String(str)
      .replace(/à|á|ạ|ả|ã|â|ầ|ấ|ậ|ẩ|ẫ|ă|ằ|ắ|ặ|ẳ|ẵ/g, 'a')
      .replace(/è|é|ẹ|ẻ|ẽ|ê|ề|ế|ệ|ể|ễ/g, 'e')
      .replace(/ì|í|ị|ỉ|ĩ/g, 'i')
      .replace(/ò|ó|ọ|ỏ|õ|ô|ồ|ố|ộ|ổ|ỗ|ơ|ờ|ớ|ợ|ở|ỡ/g, 'o')
      .replace(/ù|ú|ụ|ủ|ũ|ư|ừ|ứ|ự|ử|ữ/g, 'u')
      .replace(/ỳ|ý|ỵ|ỷ|ỹ/g, 'y')
      .replace(/đ/g, 'd')
      .replace(/À|Á|Ạ|Ả|Ã|Â|Ầ|Ấ|Ậ|Ẩ|Ẫ|Ă|Ằ|Ắ|Ặ|Ẳ|Ẵ/g, 'A')
      .replace(/È|É|Ẹ|Ẻ|Ẽ|Ê|Ề|Ế|Ệ|Ể|Ễ/g, 'E')
      .replace(/Ì|Í|Ị|Ỉ|Ĩ/g, 'I')
      .replace(/Ò|Ó|Ọ|Ỏ|Õ|Ô|Ồ|Ố|Ộ|Ổ|Ỗ|Ơ|Ờ|Ớ|Ợ|Ở|Ỡ/g, 'O')
      .replace(/Ù|Ú|Ụ|Ủ|Ũ|Ư|Ừ|Ứ|Ự|Ử|Ữ/g, 'U')
      .replace(/Ỳ|Ý|Ỵ|Ỷ|Ỹ/g, 'Y')
      .replace(/Đ/g, 'D')
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase()
      .trim();
  }

  function escapeHtml(str) {
    return String(str || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function addTrackedListener(target, type, handler, options) {
    if (!target || typeof target.addEventListener !== 'function') return;
    target.addEventListener(type, handler, options);
    runtime.cleanups.push(function () {
      target.removeEventListener(type, handler, options);
    });
  }

  function addTrackedTimer(fn, delayMs) {
    const id = window.setTimeout(function () {
      runtime.timers.delete(id);
      fn();
    }, delayMs);
    runtime.timers.add(id);
    return id;
  }

  function clearTrackedTimer(id) {
    if (!id) return;
    window.clearTimeout(id);
    runtime.timers.delete(id);
  }

  function detectReducedMotion() {
    if (typeof window.matchMedia !== 'function') return false;
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function detectPointerFine() {
    if (typeof window.matchMedia !== 'function') return false;
    return window.matchMedia('(pointer: fine)').matches;
  }

  function safeGetStorage(key) {
    try {
      return window.localStorage ? window.localStorage.getItem(key) : null;
    } catch (err) {
      return null;
    }
  }

  function safeSetStorage(key, val) {
    try {
      if (window.localStorage) {
        window.localStorage.setItem(key, String(val));
      }
    } catch (err) {
      /* ignore restricted storage (file:// private mode) */
    }
  }

  function emitToast(message, type) {
    if (typeof window.showToast === 'function') {
      window.showToast(message, type || 'success');
    }
  }

  // ==========================================================================
  // 2. GSAP 3.14 SAFE BOOTSTRAPPER
  // ==========================================================================
  function bootstrapGSAP() {
    const gsap = window.gsap;
    if (!gsap || typeof gsap.registerPlugin !== 'function') {
      return null;
    }

    const plugins = [];
    if (window.ScrollTrigger) plugins.push(window.ScrollTrigger);
    if (window.SplitText) plugins.push(window.SplitText);
    if (window.Flip) plugins.push(window.Flip);
    if (window.Observer) plugins.push(window.Observer);

    if (plugins.length > 0) {
      try {
        gsap.registerPlugin.apply(gsap, plugins);
      } catch (err) {
        /* fallback gracefully if plugin registration fails */
      }
    }

    if (window.ScrollTrigger && typeof window.ScrollTrigger.config === 'function') {
      try {
        window.ScrollTrigger.config({ ignoreMobileResize: true });
      } catch (err) {}
    }

    return gsap;
  }

  // ==========================================================================
  // 3. ORBITAL CART TELEMETRY STORE
  // ==========================================================================
  const OrbitalCart = {
    formatVND: function (n) {
      const num = Math.max(0, Math.round(Number(n) || 0));
      return String(num).replace(/\B(?=(\d{3})+(?!\d))/g, '.') + 'đ';
    },

    getState: function () {
      const rawCount = safeGetStorage(STORAGE_COUNT_KEY);
      const rawTotal = safeGetStorage(STORAGE_TOTAL_KEY);

      let count = runtime.memoryCart.count;
      let total = runtime.memoryCart.total;

      if (rawCount !== null && rawTotal !== null) {
        const parsedCount = parseInt(rawCount, 10);
        const parsedTotal = parseInt(rawTotal, 10);
        if (Number.isFinite(parsedCount) && parsedCount >= 0) count = parsedCount;
        if (Number.isFinite(parsedTotal) && parsedTotal >= 0) total = parsedTotal;
      } else {
        safeSetStorage(STORAGE_COUNT_KEY, count);
        safeSetStorage(STORAGE_TOTAL_KEY, total);
      }

      runtime.memoryCart = { count: count, total: total };
      return { count: count, total: total };
    },

    syncUI: function () {
      const state = this.getState();
      const formatted = this.formatVND(state.total);

      document.querySelectorAll('.orb-cart-count').forEach(function (el) {
        el.textContent = String(state.count);
      });
      document.querySelectorAll('.orb-cart-total').forEach(function (el) {
        el.textContent = formatted;
      });
    },

    add: function (item) {
      const payload = item || {};
      const qty = Math.max(1, Math.round(Number(payload.qty) || 1));
      const numericPrice = typeof payload.price === 'number'
        ? Math.max(0, Math.round(payload.price))
        : (parseInt(String(payload.price || '0').replace(/\D/g, ''), 10) || 0);

      const deltaTotal = payload.totalPrice != null
        ? Math.max(0, Math.round(Number(payload.totalPrice) || 0))
        : (numericPrice * qty);

      const current = this.getState();
      const nextCount = current.count + qty;
      const nextTotal = current.total + deltaTotal;

      runtime.memoryCart = { count: nextCount, total: nextTotal };
      safeSetStorage(STORAGE_COUNT_KEY, nextCount);
      safeSetStorage(STORAGE_TOTAL_KEY, nextTotal);

      this.syncUI();

      const pills = document.querySelectorAll('.orb-cart-pill');
      pills.forEach(function (pill) {
        pill.classList.remove('is-pulsing');
        void pill.offsetWidth;
        pill.classList.add('is-pulsing');
      });
      if (runtime.cartPulseTimer) {
        clearTrackedTimer(runtime.cartPulseTimer);
      }
      runtime.cartPulseTimer = addTrackedTimer(function () {
        document.querySelectorAll('.orb-cart-pill').forEach(function (pill) {
          pill.classList.remove('is-pulsing');
        });
      }, 650);

      const displayName = payload.name || (getSkuById(payload.id) && getSkuById(payload.id).name) || 'Sản phẩm';
      emitToast('Đã nạp ' + qty + ' × ' + displayName + ' vào giỏ hàng!', 'success');
      return { count: nextCount, total: nextTotal };
    },

    reset: function () {
      runtime.memoryCart = { count: DEFAULT_CART.count, total: DEFAULT_CART.total };
      safeSetStorage(STORAGE_COUNT_KEY, DEFAULT_CART.count);
      safeSetStorage(STORAGE_TOTAL_KEY, DEFAULT_CART.total);
      this.syncUI();
      return { count: DEFAULT_CART.count, total: DEFAULT_CART.total };
    }
  };

  // ==========================================================================
  // 4. SPECTRAL SYSTEM SWITCHER
  // ==========================================================================
  function setSystem(brandKey) {
    const key = String(brandKey || '').trim().toLowerCase();
    if (!VALID_SYSTEMS.has(key)) return;

    if (document.documentElement) {
      document.documentElement.setAttribute('data-spectral', key);
    }

    document.querySelectorAll('[data-system]').forEach(function (el) {
      const matches = String(el.dataset.system || '').toLowerCase() === key;
      el.classList.toggle('is-active', matches);
      if (el.hasAttribute('aria-pressed')) {
        el.setAttribute('aria-pressed', matches ? 'true' : 'false');
      }
    });

    if (window.OrbitalWebGL) {
      if (typeof window.OrbitalWebGL.setSpectralSystem === 'function') {
        window.OrbitalWebGL.setSpectralSystem(key);
      } else if (typeof window.OrbitalWebGL.setSpectrum === 'function') {
        window.OrbitalWebGL.setSpectrum(key);
      } else if (typeof window.OrbitalWebGL.setSystem === 'function') {
        window.OrbitalWebGL.setSystem(key);
      } else if (typeof window.OrbitalWebGL.setBrand === 'function') {
        window.OrbitalWebGL.setBrand(key);
      }
    }

    try {
      document.dispatchEvent(new CustomEvent('orbital:spectral-change', { detail: { system: key } }));
    } catch (err) {}
  }

  // ==========================================================================
  // 5. FLOATING NAV + MOBILE DRAWER + CTRL+K COMMAND PALETTE
  // ==========================================================================
  function initFloatingNav() {
    const navShell = document.querySelector('.orb-nav-shell');
    if (navShell) {
      const updateNavScroll = function () {
        const y = window.scrollY || window.pageYOffset || 0;
        navShell.classList.toggle('is-scrolled', y > 24);
      };
      updateNavScroll();
      addTrackedListener(window, 'scroll', updateNavScroll, { passive: true });
    }

    const mobileToggle = document.getElementById('orb-mobile-toggle');
    const mobileDrawer = document.getElementById('orb-mobile-drawer');
    if (mobileToggle && mobileDrawer) {
      const setDrawerOpen = function (open) {
        mobileDrawer.classList.toggle('is-open', open);
        mobileToggle.classList.toggle('is-open', open);
        mobileToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
        mobileDrawer.setAttribute('aria-hidden', open ? 'false' : 'true');
      };

      addTrackedListener(mobileToggle, 'click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        setDrawerOpen(!mobileDrawer.classList.contains('is-open'));
      });

      addTrackedListener(mobileDrawer, 'click', function (e) {
        const link = e.target.closest('a, button[data-system], #orb-cmd-trigger');
        if (link) {
          setDrawerOpen(false);
        }
      });

      addTrackedListener(document, 'click', function (e) {
        if (!mobileDrawer.classList.contains('is-open')) return;
        if (!mobileDrawer.contains(e.target) && !mobileToggle.contains(e.target)) {
          setDrawerOpen(false);
        }
      });

      addTrackedListener(document, 'keydown', function (e) {
        if (e.key === 'Escape' && mobileDrawer.classList.contains('is-open')) {
          const hadFocus = mobileDrawer.contains(document.activeElement);
          setDrawerOpen(false);
          if (hadFocus && typeof mobileToggle.focus === 'function') {
            mobileToggle.focus();
          }
        }
      });
    }
  }

  function renderCommandList(query) {
    const listEl = document.getElementById('orb-cmd-list');
    if (!listEl) return;

    const rawQ = String(query || '').trim();
    const normQ = normalizeVietnamese(rawQ);
    const words = normQ ? normQ.split(/\s+/).filter(Boolean) : [];

    const matched = ORBITAL_CATALOG.filter(function (sku) {
      if (words.length === 0) return true;
      const haystack = normalizeVietnamese(
        [sku.id, sku.code, sku.name, sku.brand, sku.brandLabel, sku.badge, sku.volume, sku.tags.join(' '), sku.keywords].join(' ')
      );
      return words.every(function (w) { return haystack.indexOf(w) !== -1; });
    });

    const itemsHtml = matched.map(function (sku, idx) {
      const activeCls = idx === 0 ? ' is-active' : '';
      return (
        '<a href="' + escapeHtml(resolvePath(sku.detailUrl)) + '" class="orb-cmd-item' + activeCls + '" role="option" data-cmd-idx="' + idx + '" data-sku="' + escapeHtml(sku.id) + '">' +
          '<img src="' + escapeHtml(resolvePath(sku.image)) + '" alt="' + escapeHtml(sku.name) + '" class="orb-cmd-thumb" loading="lazy" />' +
          '<span class="orb-cmd-meta">' +
            '<strong class="orb-cmd-title">' + escapeHtml(sku.name) + '</strong>' +
            '<span class="orb-cmd-sub">' + escapeHtml(sku.brandLabel) + ' · ' + escapeHtml(sku.volume) + (sku.badge ? ' · ' + escapeHtml(sku.badge) : '') + '</span>' +
          '</span>' +
          '<span class="orb-cmd-price">' + escapeHtml(OrbitalCart.formatVND(sku.price)) + '</span>' +
        '</a>'
      );
    }).join('');

    const searchUrl = resolvePath('pages/search-results.html') + (rawQ ? '?q=' + encodeURIComponent(rawQ) : '');
    const jumpLabel = rawQ
      ? ('Xem tất cả kết quả cho "' + escapeHtml(rawQ) + '" trong Trung tâm Tìm kiếm →')
      : ('Mở Trung tâm Tìm kiếm (tất cả ' + ORBITAL_CATALOG.length + ' SKU) →');

    const emptyNotice = matched.length === 0
      ? '<div class="orb-cmd-empty">Không tìm thấy SKU khớp "' + escapeHtml(rawQ) + '".</div>'
      : '';

    const jumpIdx = matched.length;
    const jumpHtml =
      '<a href="' + escapeHtml(searchUrl) + '" class="orb-cmd-item orb-cmd-jump' + (matched.length === 0 ? ' is-active' : '') + '" role="option" data-cmd-idx="' + jumpIdx + '">' +
        '<span class="orb-cmd-meta"><strong class="orb-cmd-title">' + jumpLabel + '</strong></span>' +
      '</a>';

    listEl.innerHTML = emptyNotice + itemsHtml + jumpHtml;
    runtime.cmdState.items = Array.prototype.slice.call(listEl.querySelectorAll('.orb-cmd-item'));
    runtime.cmdState.activeIndex = 0;
  }

  function updateCommandSelection(nextIdx) {
    const items = runtime.cmdState.items || [];
    if (items.length === 0) return;

    const count = items.length;
    const clamped = ((nextIdx % count) + count) % count;
    runtime.cmdState.activeIndex = clamped;

    items.forEach(function (el, idx) {
      const active = idx === clamped;
      el.classList.toggle('is-active', active);
      el.setAttribute('aria-selected', active ? 'true' : 'false');
      if (active && typeof el.scrollIntoView === 'function') {
        el.scrollIntoView({ block: 'nearest' });
      }
    });
  }

  function openCommandPalette() {
    const palette = document.getElementById('orb-cmd-palette');
    if (!palette) return;

    runtime.cmdState.lastFocused = document.activeElement;
    runtime.cmdState.isOpen = true;

    const isNativeDialog = palette.tagName === 'DIALOG' && typeof palette.showModal === 'function';
    if (isNativeDialog) {
      if (!palette.open) {
        try { palette.showModal(); } catch (err) {}
      }
      palette.classList.add('is-open');
    } else {
      palette.classList.add('is-open');
      palette.setAttribute('aria-hidden', 'false');
    }

    const inputEl = document.getElementById('orb-cmd-input');
    renderCommandList(inputEl ? inputEl.value : '');

    if (inputEl && typeof inputEl.focus === 'function') {
      const focusCmdInput = function () {
        inputEl.focus();
        if (inputEl.value && typeof inputEl.select === 'function') {
          inputEl.select();
        }
      };
      if (typeof window.requestAnimationFrame === 'function') {
        window.requestAnimationFrame(focusCmdInput);
      } else {
        focusCmdInput();
      }
    }
  }

  function closeCommandPalette() {
    const palette = document.getElementById('orb-cmd-palette');
    if (!palette) return;

    runtime.cmdState.isOpen = false;
    const isNativeDialog = palette.tagName === 'DIALOG' && typeof palette.close === 'function';

    palette.classList.remove('is-open');
    if (isNativeDialog) {
      if (palette.open) {
        try { palette.close(); } catch (err) {}
      }
    } else {
      palette.setAttribute('aria-hidden', 'true');
      const prev = runtime.cmdState.lastFocused;
      if (prev && typeof prev.focus === 'function') {
        prev.focus();
      }
    }
  }

  function initCommandPalette() {
    const palette = document.getElementById('orb-cmd-palette');
    const inputEl = document.getElementById('orb-cmd-input');
    const closeBtn = document.getElementById('orb-cmd-close');

    addTrackedListener(document, 'click', function (e) {
      const trigger = e.target.closest('#orb-cmd-trigger, [data-cmd-open]');
      if (trigger) {
        e.preventDefault();
        openCommandPalette();
      }
    });

    addTrackedListener(document, 'keydown', function (e) {
      if ((e.ctrlKey || e.metaKey) && !e.shiftKey && !e.altKey && e.key && e.key.toLowerCase() === 'k') {
        if (!palette) return;
        e.preventDefault();
        if (runtime.cmdState.isOpen) {
          closeCommandPalette();
        } else {
          openCommandPalette();
        }
        return;
      }

      if (e.key === 'Escape' && runtime.cmdState.isOpen) {
        closeCommandPalette();
      }
    });

    if (!palette) return;

    if (palette.tagName === 'DIALOG') {
      addTrackedListener(palette, 'cancel', function () {
        runtime.cmdState.isOpen = false;
        palette.classList.remove('is-open');
      });
    }

    addTrackedListener(palette, 'click', function (e) {
      if (e.target === palette) {
        closeCommandPalette();
        return;
      }
      const chipBtn = e.target.closest('.orb-cmd-chip[data-cmd-query]');
      if (chipBtn) {
        const nextQuery = String(chipBtn.getAttribute('data-cmd-query') || '').trim();
        palette.querySelectorAll('.orb-cmd-chip').forEach(function (c) {
          c.classList.toggle('is-active', c === chipBtn);
        });
        if (inputEl) {
          inputEl.value = nextQuery;
          renderCommandList(nextQuery);
          if (typeof inputEl.focus === 'function') inputEl.focus();
        }
        return;
      }
      const itemLink = e.target.closest('.orb-cmd-item');
      if (itemLink) {
        closeCommandPalette();
      }
    });

    if (closeBtn) {
      addTrackedListener(closeBtn, 'click', function () {
        closeCommandPalette();
      });
    }

    if (inputEl) {
      addTrackedListener(inputEl, 'input', function () {
        renderCommandList(inputEl.value);
      });

      addTrackedListener(inputEl, 'keydown', function (e) {
        if (e.key === 'ArrowDown') {
          e.preventDefault();
          e.stopPropagation();
          updateCommandSelection(runtime.cmdState.activeIndex + 1);
        } else if (e.key === 'ArrowUp') {
          e.preventDefault();
          e.stopPropagation();
          updateCommandSelection(runtime.cmdState.activeIndex - 1);
        } else if (e.key === 'Enter') {
          e.preventDefault();
          e.stopPropagation();
          const items = runtime.cmdState.items || [];
          const active = items[runtime.cmdState.activeIndex];
          if (active && active.getAttribute('href')) {
            closeCommandPalette();
            window.location.href = active.getAttribute('href');
          } else {
            const q = inputEl.value.trim();
            closeCommandPalette();
            window.location.href = resolvePath('pages/search-results.html') + (q ? '?q=' + encodeURIComponent(q) : '');
          }
        } else if (e.key === 'Escape') {
          e.preventDefault();
          e.stopPropagation();
          closeCommandPalette();
        }
      });
    }
  }

  function routeBrandHash(brandKey) {
    if (!VALID_SYSTEMS.has(brandKey)) return;
    setSystem(brandKey);
    const vault = document.getElementById('observatory-vault');
    if (vault) {
      filterVault({ brand: brandKey });
      vault.scrollIntoView({ behavior: runtime.reducedMotion ? 'auto' : 'smooth', block: 'start' });
      return;
    }
    const target = document.getElementById(brandKey + '-products');
    if (target) {
      target.scrollIntoView({ behavior: runtime.reducedMotion ? 'auto' : 'smooth', block: 'start' });
    }
  }

  function initSpectralAndHashLinks() {
    addTrackedListener(document, 'click', function (e) {
      const sysBtn = e.target.closest('[data-system]');
      if (sysBtn) {
        const key = String(sysBtn.dataset.system || '').toLowerCase();
        if (VALID_SYSTEMS.has(key)) {
          const flagshipBySystem = { monster: 'mn-1', redbull: 'rb-1', sting: 'st-1' };
          if (document.querySelector('.orb-orbit-stage') && flagshipBySystem[key]) {
            selectOrbitNode(flagshipBySystem[key]);
          } else {
            setSystem(key);
          }
          if (sysBtn.dataset.filterVault === 'true' && document.getElementById('observatory-vault')) {
            filterVault({ brand: key });
          }
        }
      }

      const link = e.target.closest('a[href]');
      if (!link) return;
      const href = link.getAttribute('href') || '';

      const brandHashMatch = href.match(/^#(monster|redbull|sting)-products$/i);
      if (brandHashMatch && document.getElementById('observatory-vault')) {
        e.preventDefault();
        routeBrandHash(brandHashMatch[1].toLowerCase());
        return;
      }

      if (href.startsWith('#') && href.length > 1) {
        const target = document.getElementById(href.slice(1));
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: runtime.reducedMotion ? 'auto' : 'smooth', block: 'start' });
        }
      }
    });

    const initialHash = String((window.location && window.location.hash) || '');
    const initialBrandMatch = initialHash.match(/^#(monster|redbull|sting)-products$/i);
    if (initialBrandMatch && document.getElementById('observatory-vault')) {
      const bKey = initialBrandMatch[1].toLowerCase();
      setSystem(bKey);
      filterVault({ brand: bKey });
    }
  }

  // ==========================================================================
  // 6. CHAPTER 01: HERO SPLITTEXT + 2.5D 6-CAN SOLAR ORBIT STAGE
  // ==========================================================================
  function initHeroReveal(gsap) {
    const heroTitle = document.querySelector('.orb-hero-title');
    if (!heroTitle || !gsap || typeof gsap.matchMedia !== 'function') return;

    const mm = runtime.gsapMatchMedia || gsap.matchMedia();
    runtime.gsapMatchMedia = mm;

    mm.add('(prefers-reduced-motion: no-preference)', function () {
      const SplitText = window.SplitText;
      if (SplitText && typeof SplitText.create === 'function') {
        try {
          const split = SplitText.create('.orb-hero-title', {
            type: 'words'
          });
          const targets = (split && split.words && split.words.length > 0) ? split.words : '.orb-hero-title';
          gsap.from(targets, {
            y: 18,
            opacity: 0,
            duration: 0.46,
            stagger: 0.03,
            ease: 'power3.out',
            clearProps: 'transform,opacity',
            onComplete: function () {
              if (split && typeof split.revert === 'function') {
                split.revert();
              }
            }
          });
          return;
        } catch (err) {
          /* fall through to clean non-SplitText tween */
        }
      }

      gsap.from('.orb-hero-title', {
        y: 18,
        opacity: 0,
        duration: 0.46,
        ease: 'power3.out',
        clearProps: 'transform,opacity'
      });
    });
  }

  const RING_SPEEDS = [0.18, 0.14, 0.11];
  const STAGGERED_PHASES_DEG = [0, 180, 60, 240, 120, 300];

  function detectNeedsCentering(el) {
    if (!el || typeof window.getComputedStyle !== 'function') return false;
    const cs = window.getComputedStyle(el);
    const hasIndividualTranslate = cs.translate && cs.translate !== 'none';
    const hasNegMargin = (parseFloat(cs.marginLeft) || 0) < -4;
    if (hasIndividualTranslate || hasNegMargin) return false;
    const tf = cs.transform || '';
    return tf.indexOf('matrix') !== -1;
  }

  function measureOrbitStage() {
    const orbit = runtime.orbit;
    if (!orbit.stage) return;

    const rect = orbit.stage.getBoundingClientRect();
    orbit.stageW = rect.width > 0 ? rect.width : (orbit.stage.clientWidth || 520);
    orbit.stageH = rect.height > 0 ? rect.height : (orbit.stage.clientHeight || 420);

    for (let i = 0; i < orbit.nodeData.length; i++) {
      const item = orbit.nodeData[i];
      if (typeof window.getComputedStyle === 'function') {
        const cs = window.getComputedStyle(item.el);
        item.isAbsolute = cs.position === 'absolute';
      } else {
        item.isAbsolute = true;
      }
    }
  }

  function positionReticleOverItem(item) {
    const reticle = runtime.orbit.reticle;
    if (!reticle || !item) return;

    if (!item.isAbsolute) {
      reticle.classList.remove('is-active');
      reticle.style.transform = '';
      return;
    }

    reticle.classList.add('is-active');
    const tx = item.x.toFixed(1) + 'px';
    const ty = item.y.toFixed(1) + 'px';
    const sc = (item.depth * 1.06).toFixed(3);
    const centerSuffix = runtime.orbit.reticleNeedsCenter ? ' translate(-50%, -50%)' : '';
    reticle.style.transform = 'translate3d(' + tx + ', ' + ty + ', 0)' + centerSuffix + ' scale(' + sc + ')';
  }

  function renderOrbitFrame() {
    const orbit = runtime.orbit;
    const w = orbit.stageW || 520;
    const h = orbit.stageH || 420;

    const rx1 = Math.max(68, Math.min(w * 0.24, w * 0.5 - 52));
    const rx2 = Math.max(104, Math.min(w * 0.36, w * 0.5 - 48));
    const rx3 = Math.max(136, Math.min(w * 0.44, w * 0.5 - 46));
    const radii = {
      1: { rx: rx1, ry: Math.min(rx1 * 0.86, h * 0.5 - 52) },
      2: { rx: rx2, ry: Math.min(rx2 * 0.82, h * 0.5 - 48) },
      3: { rx: rx3, ry: Math.min(rx3 * 0.78, h * 0.5 - 46) }
    };

    let lockedItem = null;

    for (let i = 0; i < orbit.nodeData.length; i++) {
      const item = orbit.nodeData[i];
      if (!item.isAbsolute) {
        item.el.style.transform = '';
        item.el.style.zIndex = '';
        item.el.style.opacity = '';
        continue;
      }

      const ringGeo = radii[item.ring] || radii[1];
      const sinA = Math.sin(item.angle);
      const cosA = Math.cos(item.angle);

      const x = cosA * ringGeo.rx;
      const y = sinA * ringGeo.ry;
      const depthNorm = (sinA + 1) * 0.5;
      const depth = 0.82 + depthNorm * 0.26;
      const isLocked = item.sku === orbit.lockedSku;
      const z = isLocked ? 38 : Math.round(10 + depthNorm * 20);
      const opacity = isLocked ? 1 : (0.72 + depthNorm * 0.28);

      item.x = x;
      item.y = y;
      item.depth = depth;

      const centerSuffix = item.needsCenter ? ' translate(-50%, -50%)' : '';
      item.el.style.transform = 'translate3d(' + x.toFixed(1) + 'px, ' + y.toFixed(1) + 'px, 0)' + centerSuffix + ' scale(' + depth.toFixed(3) + ')';
      item.el.style.zIndex = String(z);
      item.el.style.opacity = opacity.toFixed(3);

      if (isLocked) {
        lockedItem = item;
      }
    }

    if (lockedItem) {
      positionReticleOverItem(lockedItem);
    }
  }

  function updateTelemetryCard(sku) {
    if (!sku) return;
    const codeEl = document.getElementById('orb-telemetry-code');
    const titleEl = document.getElementById('orb-telemetry-title');
    const priceEl = document.getElementById('orb-telemetry-price');
    const metaEl = document.getElementById('orb-telemetry-meta');
    const linkEl = document.getElementById('orb-telemetry-link');
    const addBtn = document.getElementById('orb-telemetry-add');
    const imgEl = document.getElementById('orb-telemetry-img');

    if (codeEl) codeEl.textContent = sku.code || sku.id.toUpperCase();
    if (titleEl) titleEl.textContent = sku.name;
    if (priceEl) priceEl.textContent = OrbitalCart.formatVND(sku.price);
    if (metaEl) metaEl.textContent = [sku.volume, sku.origin, sku.badge || sku.brandLabel].filter(Boolean).join(' · ');
    if (linkEl) linkEl.setAttribute('href', resolvePath(sku.detailUrl));
    if (addBtn) {
      addBtn.setAttribute('data-sku', sku.id);
      addBtn.setAttribute('aria-label', 'Nạp ' + sku.name + ' vào giỏ hàng');
    }
    if (imgEl) {
      imgEl.src = resolvePath(sku.image);
      imgEl.alt = sku.name;
    }
  }

  function selectOrbitNode(skuId) {
    const orbit = runtime.orbit;
    const sku = getSkuById(skuId) || ORBITAL_CATALOG[0];
    if (!sku) return;

    orbit.lockedSku = sku.id;

    let lockedItem = null;
    for (let i = 0; i < orbit.nodeData.length; i++) {
      const item = orbit.nodeData[i];
      const match = item.sku === sku.id;
      item.el.classList.toggle('is-locked', match);
      if (item.el.hasAttribute('aria-pressed')) {
        item.el.setAttribute('aria-pressed', match ? 'true' : 'false');
      }
      if (match) lockedItem = item;
    }

    setSystem(sku.brand);
    updateTelemetryCard(sku);

    if (lockedItem) {
      positionReticleOverItem(lockedItem);
      renderOrbitFrame();
    }
  }

  function shouldRunOrbitLoop() {
    const orbit = runtime.orbit;
    return !runtime.reducedMotion &&
      !document.hidden &&
      orbit.inViewport &&
      !orbit.hovered &&
      !orbit.focused &&
      orbit.nodeData.length > 0;
  }

  function syncOrbitLoopState() {
    const orbit = runtime.orbit;
    if (shouldRunOrbitLoop() && typeof window.requestAnimationFrame === 'function') {
      if (!orbit.rafId) {
        orbit.lastTs = 0;
        orbit.rafId = window.requestAnimationFrame(stepOrbitLoop);
      }
    } else if (orbit.rafId) {
      if (typeof window.cancelAnimationFrame === 'function') {
        window.cancelAnimationFrame(orbit.rafId);
      }
      orbit.rafId = 0;
      orbit.lastTs = 0;
    }
  }

  function stepOrbitLoop(ts) {
    const orbit = runtime.orbit;
    orbit.rafId = 0;
    if (!shouldRunOrbitLoop() || typeof window.requestAnimationFrame !== 'function') return;

    if (!orbit.lastTs) orbit.lastTs = ts;
    const dt = Math.min(0.05, Math.max(0, (ts - orbit.lastTs) / 1000));
    orbit.lastTs = ts;

    for (let i = 0; i < orbit.nodeData.length; i++) {
      const item = orbit.nodeData[i];
      if (!item.isAbsolute) continue;
      item.angle = (item.angle + item.speed * dt) % (Math.PI * 2);
    }

    renderOrbitFrame();
    orbit.rafId = window.requestAnimationFrame(stepOrbitLoop);
  }

  function initSolarOrbitStage() {
    const stage = document.querySelector('.orb-orbit-stage');
    if (!stage) return;

    const nodes = Array.prototype.slice.call(stage.querySelectorAll('.orb-orbit-node[data-sku]'));
    if (nodes.length === 0) return;

    const orbit = runtime.orbit;
    orbit.stage = stage;
    orbit.reticle = stage.querySelector('.orb-target-reticle');
    orbit.reticleNeedsCenter = orbit.reticle ? detectNeedsCentering(orbit.reticle) : false;
    orbit.nodes = nodes;
    orbit.nodeData = nodes.map(function (el, idx) {
      const ringRaw = parseInt(el.dataset.ring || '', 10);
      const ring = (ringRaw === 1 || ringRaw === 2 || ringRaw === 3) ? ringRaw : (Math.floor(idx / 2) + 1);
      const degRaw = parseFloat(el.dataset.angle || '');
      const deg = Number.isFinite(degRaw) ? degRaw : STAGGERED_PHASES_DEG[idx % STAGGERED_PHASES_DEG.length];
      const sku = el.dataset.sku || ORBITAL_CATALOG[0].id;
      const speed = RING_SPEEDS[(ring - 1) % RING_SPEEDS.length];

      return {
        el: el,
        sku: sku,
        ring: ring,
        speed: speed,
        angle: (deg * Math.PI) / 180,
        x: 0,
        y: 0,
        depth: 1,
        isAbsolute: true,
        needsCenter: detectNeedsCentering(el)
      };
    });

    measureOrbitStage();

    const preLocked = nodes.find(function (n) { return n.classList.contains('is-locked'); }) || nodes[0];
    selectOrbitNode(preLocked.dataset.sku);
    renderOrbitFrame();

    nodes.forEach(function (nodeEl) {
      addTrackedListener(nodeEl, 'click', function () {
        selectOrbitNode(nodeEl.dataset.sku);
      });
      addTrackedListener(nodeEl, 'keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          selectOrbitNode(nodeEl.dataset.sku);
        }
      });
    });

    const addTelemetryBtn = document.getElementById('orb-telemetry-add');
    if (addTelemetryBtn) {
      addTrackedListener(addTelemetryBtn, 'click', function (e) {
        e.preventDefault();
        const sku = getSkuById(addTelemetryBtn.dataset.sku || orbit.lockedSku);
        if (sku) {
          OrbitalCart.add({ id: sku.id, name: sku.name, price: sku.price, qty: 1 });
        }
      });
    }

    addTrackedListener(stage, 'pointerenter', function () {
      orbit.hovered = true;
      syncOrbitLoopState();
    });
    addTrackedListener(stage, 'pointerleave', function () {
      orbit.hovered = false;
      syncOrbitLoopState();
    });
    addTrackedListener(stage, 'focusin', function () {
      orbit.focused = true;
      syncOrbitLoopState();
    });
    addTrackedListener(stage, 'focusout', function (e) {
      if (!e.relatedTarget || !stage.contains(e.relatedTarget)) {
        orbit.focused = false;
        syncOrbitLoopState();
      }
    });

    if (typeof window.IntersectionObserver === 'function') {
      const io = new window.IntersectionObserver(function (entries) {
        for (let i = 0; i < entries.length; i++) {
          orbit.inViewport = entries[i].isIntersecting;
        }
        syncOrbitLoopState();
      }, { threshold: 0.05 });
      io.observe(stage);
      runtime.observers.push(io);
    }

    if (typeof window.ResizeObserver === 'function') {
      const ro = new window.ResizeObserver(function () {
        measureOrbitStage();
        renderOrbitFrame();
      });
      ro.observe(stage);
      runtime.observers.push(ro);
    } else {
      addTrackedListener(window, 'resize', function () {
        measureOrbitStage();
        renderOrbitFrame();
      }, { passive: true });
    }

    addTrackedListener(document, 'visibilitychange', syncOrbitLoopState);
    syncOrbitLoopState();
  }

  // ==========================================================================
  // 7. CHAPTER 02: PINNED HORIZONTAL-PAN (#orbital-spectral-drift)
  // ==========================================================================
  function initSpectralDrift(gsap) {
    const section = document.getElementById('orbital-spectral-drift');
    const track = section ? section.querySelector('.orb-drift-track') : null;
    if (!section || !track || !gsap || !window.ScrollTrigger || typeof gsap.matchMedia !== 'function') {
      return;
    }

    const indexEl = document.getElementById('orb-drift-index');
    const barFill = section.querySelector('.orb-drift-bar-fill');
    const mm = runtime.gsapMatchMedia || gsap.matchMedia();
    runtime.gsapMatchMedia = mm;

    mm.add('(min-width: 960px) and (prefers-reduced-motion: no-preference)', function () {
      let currentBand = '';

      const tween = gsap.to('.orb-drift-track', {
        xPercent: -66.6667,
        ease: 'none',
        scrollTrigger: {
          trigger: '#orbital-spectral-drift',
          pin: true,
          scrub: 0.55,
          anticipatePin: 1,
          invalidateOnRefresh: true,
          end: function () {
            return '+=' + Math.round(window.innerWidth * 1.9);
          },
          onUpdate: function (self) {
            const p = Math.max(0, Math.min(1, self.progress || 0));
            if (barFill) {
              barFill.style.width = (p * 100).toFixed(2) + '%';
            }
            let nextBand = 'monster';
            let label = '01 / 03';
            if (p >= 0.67) {
              nextBand = 'sting';
              label = '03 / 03';
            } else if (p >= 0.33) {
              nextBand = 'redbull';
              label = '02 / 03';
            }
            if (indexEl && indexEl.textContent !== label) {
              indexEl.textContent = label;
            }
            if (nextBand !== currentBand) {
              currentBand = nextBand;
              setSystem(nextBand);
            }
          }
        }
      });

      return function () {
        if (tween && tween.scrollTrigger) tween.scrollTrigger.kill();
        if (tween) tween.kill();
      };
    });

    const refreshTriggers = function () {
      if (window.ScrollTrigger && typeof window.ScrollTrigger.refresh === 'function') {
        window.ScrollTrigger.refresh();
      }
    };
    addTrackedListener(window, 'load', refreshTriggers);
    if (document.fonts && document.fonts.ready && typeof document.fonts.ready.then === 'function') {
      document.fonts.ready.then(refreshTriggers).catch(function () {});
    }
  }

  // ==========================================================================
  // 8. CHAPTER 03: FLASH ECLIPSE LIVE COUNTDOWN
  // ==========================================================================
  function initFlashCountdown() {
    const hEl = document.getElementById('orb-countdown-h');
    const mEl = document.getElementById('orb-countdown-m');
    const sEl = document.getElementById('orb-countdown-s');
    if (!hEl && !mEl && !sEl) return;

    const initH = hEl ? (parseInt(hEl.textContent, 10) || 0) : 8;
    const initM = mEl ? (parseInt(mEl.textContent, 10) || 0) : 45;
    const initS = sEl ? (parseInt(sEl.textContent, 10) || 0) : 30;
    let remaining = Math.max(1, initH * 3600 + initM * 60 + initS);

    const renderClock = function () {
      const hrs = Math.floor(remaining / 3600);
      const mins = Math.floor((remaining % 3600) / 60);
      const secs = remaining % 60;
      if (hEl) hEl.textContent = String(hrs).padStart(2, '0');
      if (mEl) mEl.textContent = String(mins).padStart(2, '0');
      if (sEl) sEl.textContent = String(secs).padStart(2, '0');
    };

    renderClock();

    const intervalId = window.setInterval(function () {
      remaining = remaining > 1 ? (remaining - 1) : (8 * 3600 + 59 * 60 + 59);
      renderClock();
    }, 1000);
    runtime.intervals.push(intervalId);
  }

  // ==========================================================================
  // 9. CHAPTER 04: OBSERVATORY BENTO VAULT (GSAP FLIP FILTERING)
  // ==========================================================================
  function syncVaultFilterControls() {
    const st = runtime.vaultState;

    document.querySelectorAll('#observatory-vault .orb-filter-pill[data-filter-brand]').forEach(function (btn) {
      const active = String(btn.dataset.filterBrand || '') === st.brand;
      btn.classList.toggle('is-active', active);
      if (btn.hasAttribute('aria-pressed')) {
        btn.setAttribute('aria-pressed', active ? 'true' : 'false');
      }
    });

    document.querySelectorAll('#observatory-vault .orb-filter-pill[data-filter-tag]').forEach(function (btn) {
      const active = String(btn.dataset.filterTag || '') === st.tag;
      btn.classList.toggle('is-active', active);
      if (btn.hasAttribute('aria-pressed')) {
        btn.setAttribute('aria-pressed', active ? 'true' : 'false');
      }
    });

    const searchInput = document.getElementById('orb-vault-search');
    if (searchInput && searchInput.value !== st.query) {
      searchInput.value = st.query;
    }

    const sortSelect = document.getElementById('orb-vault-sort');
    if (sortSelect && sortSelect.value !== st.sort) {
      sortSelect.value = st.sort;
    }
  }

  function filterVault(opts) {
    const vault = document.getElementById('observatory-vault');
    if (!vault) return;

    if (opts && typeof opts === 'object') {
      if ('brand' in opts) runtime.vaultState.brand = String(opts.brand || 'all');
      if ('tag' in opts) runtime.vaultState.tag = String(opts.tag || 'all');
      if ('sort' in opts) runtime.vaultState.sort = String(opts.sort || 'default');
      if ('query' in opts) runtime.vaultState.query = String(opts.query || '');
    }

    syncVaultFilterControls();

    const grid = vault.querySelector('.orb-vault-grid');
    const cards = Array.prototype.slice.call(vault.querySelectorAll('.orb-bento-card[data-sku]'));
    if (!grid || cards.length === 0) return;

    const st = runtime.vaultState;
    const normQuery = normalizeVietnamese(st.query);
    const words = normQuery ? normQuery.split(/\s+/).filter(Boolean) : [];

    const canFlip = Boolean(window.Flip && window.gsap && !runtime.reducedMotion);
    let flipState = null;
    if (canFlip) {
      try {
        flipState = window.Flip.getState(cards);
      } catch (err) {
        flipState = null;
      }
    }

    const sortedCards = cards.slice().sort(function (a, b) {
      const aOrder = parseInt(a.dataset.order || '0', 10) || 0;
      const bOrder = parseInt(b.dataset.order || '0', 10) || 0;
      const aPrice = parseInt(a.dataset.price || '0', 10) || 0;
      const bPrice = parseInt(b.dataset.price || '0', 10) || 0;
      if (st.sort === 'price-asc') return (aPrice - bPrice) || (aOrder - bOrder);
      if (st.sort === 'price-desc') return (bPrice - aPrice) || (aOrder - bOrder);
      return aOrder - bOrder;
    });

    let visibleCount = 0;

    sortedCards.forEach(function (card) {
      const skuId = card.dataset.sku || '';
      const brand = String(card.dataset.brand || '').toLowerCase();
      const rawTags = String(card.dataset.tags || '').toLowerCase().split(/[\s,]+/).filter(Boolean);
      const skuMeta = getSkuById(skuId);

      const brandOk = st.brand === 'all' || brand === st.brand;
      const tagOk = st.tag === 'all' || rawTags.indexOf(st.tag) !== -1;

      let queryOk = true;
      if (words.length > 0) {
        const searchText = normalizeVietnamese(
          [
            skuId,
            brand,
            rawTags.join(' '),
            card.textContent || '',
            skuMeta ? skuMeta.keywords : '',
            skuMeta ? skuMeta.brandLabel : ''
          ].join(' ')
        );
        queryOk = words.every(function (w) { return searchText.indexOf(w) !== -1; });
      }

      const visible = brandOk && tagOk && queryOk;
      card.classList.toggle('is-hidden', !visible);
      if (visible) visibleCount++;
      grid.appendChild(card);
    });

    const countEl = document.getElementById('orb-vault-count');
    if (countEl) {
      countEl.textContent = visibleCount + ' / ' + cards.length + ' lon';
    }

    const emptyEl = document.getElementById('orb-vault-empty');
    if (emptyEl) {
      emptyEl.classList.toggle('is-hidden', visibleCount > 0);
      emptyEl.hidden = visibleCount > 0;
    }

    if (flipState) {
      try {
        window.Flip.from(flipState, {
          duration: 0.5,
          ease: 'power3.inOut',
          stagger: 0.02,
          absolute: true,
          simple: true,
          onEnter: function (els) {
            return window.gsap.fromTo(
              els,
              { opacity: 0, scale: 0.94 },
              { opacity: 1, scale: 1, duration: 0.35, ease: 'power2.out', clearProps: 'transform,opacity' }
            );
          },
          onLeave: function (els) {
            return window.gsap.to(els, { opacity: 0, scale: 0.94, duration: 0.25 });
          },
          onComplete: function () {
            if (window.ScrollTrigger && typeof window.ScrollTrigger.refresh === 'function') {
              window.ScrollTrigger.refresh();
            }
          }
        });
      } catch (err) {
        if (window.ScrollTrigger && typeof window.ScrollTrigger.refresh === 'function') {
          window.ScrollTrigger.refresh();
        }
      }
    } else if (window.ScrollTrigger && typeof window.ScrollTrigger.refresh === 'function') {
      window.ScrollTrigger.refresh();
    }
  }

  function initObservatoryVault() {
    const vault = document.getElementById('observatory-vault');
    if (!vault) return;

    vault.querySelectorAll('.orb-filter-pill[data-filter-brand]').forEach(function (pill) {
      addTrackedListener(pill, 'click', function () {
        const brandVal = pill.dataset.filterBrand || 'all';
        if (VALID_SYSTEMS.has(brandVal)) {
          setSystem(brandVal);
        }
        filterVault({ brand: brandVal });
      });
    });

    vault.querySelectorAll('.orb-filter-pill[data-filter-tag]').forEach(function (pill) {
      addTrackedListener(pill, 'click', function () {
        const tagVal = pill.dataset.filterTag || 'all';
        const nextTag = runtime.vaultState.tag === tagVal && tagVal !== 'all' ? 'all' : tagVal;
        filterVault({ tag: nextTag });
      });
    });

    const searchInput = document.getElementById('orb-vault-search');
    let vaultSearchTimer = 0;
    if (searchInput) {
      addTrackedListener(searchInput, 'input', function () {
        if (vaultSearchTimer) clearTrackedTimer(vaultSearchTimer);
        vaultSearchTimer = addTrackedTimer(function () {
          filterVault({ query: searchInput.value });
        }, 140);
      });
    }

    const sortSelect = document.getElementById('orb-vault-sort');
    if (sortSelect) {
      addTrackedListener(sortSelect, 'change', function () {
        filterVault({ sort: sortSelect.value || 'default' });
      });
    }

    vault.querySelectorAll('#orb-vault-reset, [data-vault-reset], #orb-vault-empty button').forEach(function (btn) {
      addTrackedListener(btn, 'click', function () {
        filterVault({ brand: 'all', tag: 'all', sort: 'default', query: '' });
      });
    });

    const countEl = document.getElementById('orb-vault-count');
    const totalCards = vault.querySelectorAll('.orb-bento-card[data-sku]').length;
    if (countEl && totalCards > 0) {
      countEl.textContent = totalCards + ' / ' + totalCards + ' lon';
    }
  }

  function animateSearchCards(container) {
    const grid = container || document.getElementById('search-results-grid');
    if (!grid || !window.gsap || runtime.reducedMotion) return;

    const cards = grid.querySelectorAll('.orb-bento-card');
    if (!cards || cards.length === 0) return;

    window.gsap.fromTo(
      cards,
      { y: 16, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.38, stagger: 0.04, ease: 'power2.out', clearProps: 'transform,opacity' }
    );
  }

  // ==========================================================================
  // 10. DELEGATED POINTER SPECULAR HIGHLIGHT
  // ==========================================================================
  function initPointerSpecular() {
    if (!runtime.pointerFine || runtime.reducedMotion) return;

    const CARD_SELECTOR = '.orb-bento-card, .orb-eclipse-card, .orb-combo-card';
    let pending = null;
    let rafId = 0;

    addTrackedListener(document, 'pointermove', function (e) {
      if (e.pointerType && e.pointerType !== 'mouse' && e.pointerType !== 'pen') return;
      const card = e.target && typeof e.target.closest === 'function' ? e.target.closest(CARD_SELECTOR) : null;
      if (!card) return;

      pending = { card: card, x: e.clientX, y: e.clientY };
      if (!rafId && typeof window.requestAnimationFrame === 'function') {
        rafId = window.requestAnimationFrame(function () {
          rafId = 0;
          if (!pending) return;
          const target = pending.card;
          const cx = pending.x;
          const cy = pending.y;
          pending = null;
          const rect = target.getBoundingClientRect();
          if (rect.width > 0 && rect.height > 0) {
            const mx = Math.max(0, Math.min(100, ((cx - rect.left) / rect.width) * 100));
            const my = Math.max(0, Math.min(100, ((cy - rect.top) / rect.height) * 100));
            target.style.setProperty('--mx', mx.toFixed(1) + '%');
            target.style.setProperty('--my', my.toFixed(1) + '%');
          }
        });
      }
    }, { passive: true });
  }

  // ==========================================================================
  // 11. PRODUCT DETAIL INSPECTION CHAMBER
  // ==========================================================================
  function inferDefaultDetailSkuId() {
    const p = String((window.location && window.location.pathname) || '').toLowerCase();
    if (p.includes('product-detail-redbull-thai')) return 'rb-2';
    if (p.includes('product-detail-redbull-lonvua')) return 'rb-3';
    if (p.includes('product-detail-redbull')) return 'rb-1';
    if (p.includes('product-detail-sting')) return 'st-1';
    return 'mn-1';
  }

  function parseNormalizedDiscount(raw) {
    const val = parseFloat(String(raw || '0'));
    if (!Number.isFinite(val) || val <= 0) return 0;
    return val >= 1 ? (val / 100) : val;
  }

  function initDetailChamber() {
    const addCartBtn = document.getElementById('orb-detail-add-cart');
    if (!addCartBtn) return;

    const mainImg = document.getElementById('main-product-image');
    const titleEl = document.getElementById('orb-detail-title');
    const codeEl = document.getElementById('orb-detail-code');
    const priceEl = document.getElementById('orb-detail-price');
    const oldPriceEl = document.getElementById('orb-detail-old-price');
    const savingsEl = document.getElementById('orb-detail-savings');
    const qtyDecBtn = document.getElementById('orb-qty-dec');
    const qtyIncBtn = document.getElementById('orb-qty-inc');
    const qtyInput = document.getElementById('orb-qty-input');

    const params = new URLSearchParams(window.location.search || '');
    const defaultSkuId = inferDefaultDetailSkuId();
    const requestedSkuId = (params.get('sku') || '').trim();
    const matchedSku = getSkuById(requestedSkuId);
    const activeSku = matchedSku || getSkuById(defaultSkuId) || ORBITAL_CATALOG[0];
    const activeSkuId = activeSku.id;

    // Hydrate dynamically when ?sku= points to another SKU (e.g. mn-2, mn-3, mn-4, st-2, st-3)
    if (matchedSku && matchedSku.id !== defaultSkuId) {
      if (mainImg) {
        mainImg.src = resolvePath(matchedSku.image);
        mainImg.alt = matchedSku.name;
      }
      if (titleEl) titleEl.textContent = matchedSku.name;
      if (codeEl) codeEl.textContent = matchedSku.code || matchedSku.id.toUpperCase();
      document.title = matchedSku.name + ' - Chi Tiết Sản Phẩm | ENERGY BOOST STORE';

      const breadcrumbTail = document.getElementById('orb-breadcrumb-current') ||
        document.querySelector('.breadcrumb span:last-child');
      if (breadcrumbTail) breadcrumbTail.textContent = matchedSku.name;

      const badgeEl = document.getElementById('orb-detail-badge') ||
        document.querySelector('.detail-badge-row .badge-discount');
      if (badgeEl && matchedSku.badge) {
        badgeEl.textContent = matchedSku.badge;
      }

      const volEl = document.getElementById('orb-detail-volume');
      if (volEl) volEl.textContent = matchedSku.volume;
      const originEl = document.getElementById('orb-detail-origin');
      if (originEl) originEl.textContent = matchedSku.origin;
      const specsEl = document.getElementById('orb-detail-specs');
      if (specsEl) specsEl.textContent = matchedSku.specs;

      if (priceEl) {
        priceEl.setAttribute('data-base-price', String(matchedSku.price));
        priceEl.textContent = OrbitalCart.formatVND(matchedSku.price);
      }
      if (oldPriceEl) {
        if (matchedSku.oldPrice) {
          oldPriceEl.setAttribute('data-base-old-price', String(matchedSku.oldPrice));
          oldPriceEl.textContent = OrbitalCart.formatVND(matchedSku.oldPrice);
          oldPriceEl.hidden = false;
          oldPriceEl.style.display = '';
        } else {
          oldPriceEl.setAttribute('data-base-old-price', '0');
          oldPriceEl.textContent = '';
          oldPriceEl.hidden = true;
          oldPriceEl.style.display = 'none';
        }
      }

      setSystem(matchedSku.brand);

      const thumbBtns = Array.prototype.slice.call(document.querySelectorAll('.orb-thumb-btn'));
      if (thumbBtns.length > 0) {
        const gallery = matchedSku.gallery && matchedSku.gallery.length > 0 ? matchedSku.gallery : [matchedSku.image];
        thumbBtns.forEach(function (btn, idx) {
          if (idx < gallery.length) {
            const src = resolvePath(gallery[idx]);
            btn.setAttribute('data-src', src);
            btn.classList.toggle('is-active', idx === 0);
            btn.hidden = false;
            btn.style.display = '';
            const thumbImg = btn.querySelector('img');
            if (thumbImg) {
              thumbImg.src = src;
              thumbImg.alt = matchedSku.name;
            }
          } else {
            btn.hidden = true;
            btn.style.display = 'none';
            btn.classList.remove('is-active');
          }
        });
      }
    } else if (activeSku) {
      setSystem(activeSku.brand);
    }

    const basePriceAttr = priceEl ? parseInt(priceEl.getAttribute('data-base-price') || '', 10) : NaN;
    const basePriceText = priceEl ? parseInt(String(priceEl.textContent || '').replace(/\D/g, ''), 10) : NaN;
    const baseUnitPrice = (Number.isFinite(basePriceAttr) && basePriceAttr > 0)
      ? basePriceAttr
      : ((Number.isFinite(basePriceText) && basePriceText > 0) ? basePriceText : activeSku.price);

    const oldAttr = oldPriceEl ? parseInt(oldPriceEl.getAttribute('data-base-old-price') || '', 10) : NaN;
    const oldText = (oldPriceEl && !oldPriceEl.hidden && oldPriceEl.style.display !== 'none')
      ? parseInt(String(oldPriceEl.textContent || '').replace(/\D/g, ''), 10)
      : NaN;
    const baseOldPrice = Number.isFinite(oldAttr)
      ? oldAttr
      : ((Number.isFinite(oldText) && oldText > 0) ? oldText : (activeSku.oldPrice || 0));

    let activeMult = 1;
    let activeDiscount = 0;
    let activePack = '1';

    const packButtons = Array.prototype.slice.call(document.querySelectorAll('.orb-pack-btn[data-pack]'));
    const initialPackBtn = packButtons.find(function (b) { return b.classList.contains('is-active'); }) || packButtons[0];
    if (initialPackBtn) {
      activePack = String(initialPackBtn.dataset.pack || '1');
      activeMult = parseInt(initialPackBtn.dataset.mult || activePack || '1', 10) || 1;
      activeDiscount = parseNormalizedDiscount(initialPackBtn.dataset.discount);
    }

    function getQty() {
      if (!qtyInput) return 1;
      const val = parseInt(qtyInput.value, 10);
      const clamped = Number.isFinite(val) ? Math.max(1, Math.min(99, val)) : 1;
      if (String(clamped) !== String(qtyInput.value)) {
        qtyInput.value = String(clamped);
      }
      return clamped;
    }

    function computeTotals() {
      const qty = getQty();
      const unitPackPrice = Math.round(baseUnitPrice * activeMult * (1 - activeDiscount));
      const totalAddPrice = unitPackPrice * qty;
      const totalCans = activeMult * qty;
      return {
        qty: qty,
        totalAddPrice: totalAddPrice,
        totalCans: totalCans
      };
    }

    function recalculateDetailPrice() {
      const totals = computeTotals();
      if (priceEl) {
        priceEl.textContent = OrbitalCart.formatVND(totals.totalAddPrice);
      }

      const compareUnit = baseOldPrice > baseUnitPrice ? baseOldPrice : (activeDiscount > 0 ? baseUnitPrice : 0);
      const compareTotal = compareUnit > 0 ? (compareUnit * activeMult * totals.qty) : 0;

      if (compareTotal > totals.totalAddPrice) {
        const saved = compareTotal - totals.totalAddPrice;
        if (oldPriceEl) {
          oldPriceEl.textContent = OrbitalCart.formatVND(compareTotal);
          oldPriceEl.hidden = false;
          oldPriceEl.style.display = '';
        }
        if (savingsEl) {
          savingsEl.textContent = 'Tiết kiệm ' + OrbitalCart.formatVND(saved);
          savingsEl.hidden = false;
          savingsEl.style.display = '';
        }
      } else {
        if (oldPriceEl) {
          oldPriceEl.textContent = '';
          oldPriceEl.hidden = true;
          oldPriceEl.style.display = 'none';
        }
        if (savingsEl) {
          savingsEl.textContent = '';
          savingsEl.hidden = true;
          savingsEl.style.display = 'none';
        }
      }
    }

    packButtons.forEach(function (btn) {
      addTrackedListener(btn, 'click', function () {
        packButtons.forEach(function (b) {
          const isMe = b === btn;
          b.classList.toggle('is-active', isMe);
          if (b.hasAttribute('aria-pressed')) {
            b.setAttribute('aria-pressed', isMe ? 'true' : 'false');
          }
        });
        activePack = String(btn.dataset.pack || '1');
        activeMult = parseInt(btn.dataset.mult || activePack || '1', 10) || 1;
        activeDiscount = parseNormalizedDiscount(btn.dataset.discount);
        recalculateDetailPrice();
      });
    });

    if (qtyDecBtn && qtyInput) {
      addTrackedListener(qtyDecBtn, 'click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        qtyInput.value = String(Math.max(1, getQty() - 1));
        recalculateDetailPrice();
      });
    }

    if (qtyIncBtn && qtyInput) {
      addTrackedListener(qtyIncBtn, 'click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        qtyInput.value = String(Math.min(99, getQty() + 1));
        recalculateDetailPrice();
      });
    }

    if (qtyInput) {
      addTrackedListener(qtyInput, 'input', recalculateDetailPrice);
      addTrackedListener(qtyInput, 'change', recalculateDetailPrice);
    }

    const allThumbs = Array.prototype.slice.call(document.querySelectorAll('.orb-thumb-btn[data-src]'));
    allThumbs.forEach(function (thumbBtn) {
      addTrackedListener(thumbBtn, 'click', function () {
        const nextSrc = thumbBtn.getAttribute('data-src');
        if (!nextSrc || !mainImg) return;
        allThumbs.forEach(function (b) { b.classList.toggle('is-active', b === thumbBtn); });
        mainImg.src = nextSrc;
        if (window.gsap && !runtime.reducedMotion) {
          window.gsap.fromTo(
            mainImg,
            { opacity: 0.45, scale: 0.98 },
            { opacity: 1, scale: 1, duration: 0.25, ease: 'power2.out', clearProps: 'transform,opacity' }
          );
        }
      });
    });

    if (mainImg) {
      mainImg.style.cursor = 'zoom-in';
      addTrackedListener(mainImg, 'click', function () {
        const title = (titleEl && titleEl.textContent) || activeSku.name;
        if (typeof window.openLightbox === 'function') {
          window.openLightbox(mainImg.src, title);
        }
      });
    }

    addTrackedListener(addCartBtn, 'click', function (e) {
      e.preventDefault();
      const totals = computeTotals();
      const activeTitle = (titleEl && titleEl.textContent.trim()) || activeSku.name;
      let packLabel = '';
      if (activeMult === 6) packLabel = ' (Lốc 6 lon)';
      else if (activeMult === 24) packLabel = ' (Thùng 24 lon)';
      else if (activeMult > 1) packLabel = ' (Bộ ' + activeMult + ' lon)';

      OrbitalCart.add({
        id: activeSkuId,
        name: activeTitle + packLabel,
        price: totals.totalAddPrice,
        totalPrice: totals.totalAddPrice,
        qty: totals.totalCans
      });
    });

    recalculateDetailPrice();
  }

  // ==========================================================================
  // 12. DELEGATED DATA-ADD-SKU / COMBO CART WIRING
  // ==========================================================================
  function initDelegatedAddCart() {
    addTrackedListener(document, 'click', function (e) {
      const btn = e.target.closest('[data-add-sku], [data-add-combo]');
      if (!btn) return;
      const inlineOnClick = String(btn.getAttribute('onclick') || '');
      if (inlineOnClick.indexOf('OrbitalCart') !== -1) return;

      e.preventDefault();
      e.stopPropagation();

      if (btn.hasAttribute('data-add-combo')) {
        const comboName = btn.getAttribute('data-combo-name') || btn.getAttribute('data-name') || 'Combo Năng Lượng';
        const comboPrice = parseInt(String(btn.getAttribute('data-price') || '0').replace(/\D/g, ''), 10) || 0;
        const comboQty = parseInt(btn.getAttribute('data-qty') || '1', 10) || 1;
        OrbitalCart.add({
          id: btn.getAttribute('data-add-combo') || 'combo',
          name: comboName,
          price: comboPrice,
          totalPrice: comboPrice,
          qty: comboQty
        });
        return;
      }

      const skuId = btn.getAttribute('data-add-sku');
      const sku = getSkuById(skuId);
      if (sku) {
        OrbitalCart.add({
          id: sku.id,
          name: sku.name,
          price: sku.price,
          qty: 1
        });
      }
    });
  }

  // ==========================================================================
  // 13. LIFECYCLE INIT & TEARDOWN
  // ==========================================================================
  function destroy() {
    if (runtime.orbit.rafId) {
      if (typeof window.cancelAnimationFrame === 'function') {
        window.cancelAnimationFrame(runtime.orbit.rafId);
      }
      runtime.orbit.rafId = 0;
    }

    runtime.intervals.forEach(function (id) {
      window.clearInterval(id);
    });
    runtime.intervals = [];

    runtime.timers.forEach(function (id) {
      window.clearTimeout(id);
    });
    runtime.timers.clear();

    runtime.observers.forEach(function (obs) {
      if (obs && typeof obs.disconnect === 'function') obs.disconnect();
    });
    runtime.observers = [];

    runtime.cleanups.forEach(function (fn) {
      try { fn(); } catch (err) {}
    });
    runtime.cleanups = [];

    if (runtime.gsapMatchMedia && typeof runtime.gsapMatchMedia.revert === 'function') {
      try { runtime.gsapMatchMedia.revert(); } catch (err) {}
      runtime.gsapMatchMedia = null;
    }

    runtime.initialized = false;
  }

  function init() {
    if (runtime.initialized) return;
    runtime.initialized = true;

    runtime.reducedMotion = detectReducedMotion();
    runtime.pointerFine = detectPointerFine();

    const gsap = bootstrapGSAP();

    OrbitalCart.syncUI();
    initFloatingNav();
    initCommandPalette();
    initSpectralAndHashLinks();
    initHeroReveal(gsap);
    initSolarOrbitStage();
    initSpectralDrift(gsap);
    initFlashCountdown();
    initObservatoryVault();
    initPointerSpecular();
    initDetailChamber();
    initDelegatedAddCart();

    if (document.getElementById('search-results-grid')) {
      animateSearchCards();
    }

    if (typeof window.matchMedia === 'function') {
      const motionMq = window.matchMedia('(prefers-reduced-motion: reduce)');
      const onMotionChange = function (evt) {
        runtime.reducedMotion = Boolean(evt.matches);
        syncOrbitLoopState();
      };
      if (typeof motionMq.addEventListener === 'function') {
        addTrackedListener(motionMq, 'change', onMotionChange);
      }
    }
  }

  // Export globals immediately so inline onclick handlers & js/app.js can access them
  window.ORBITAL_CATALOG = ORBITAL_CATALOG;
  window.OrbitalCart = OrbitalCart;
  window.OrbitalMotion = {
    init: init,
    destroy: destroy,
    setSystem: setSystem,
    selectOrbitNode: selectOrbitNode,
    filterVault: filterVault,
    openCommandPalette: openCommandPalette,
    closeCommandPalette: closeCommandPalette,
    animateSearchCards: animateSearchCards,
    initDetailChamber: initDetailChamber,
    getCatalog: function () { return ORBITAL_CATALOG.slice(); },
    getSku: getSkuById
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})(window, document);
