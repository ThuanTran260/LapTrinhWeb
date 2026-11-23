/**
 * ENERGY BOOST STORE - ADAPTIVE KINETIC GLASS MOTION ENGINE
 * Dual-Mode Architecture:
 *   - 'kinetic'   (Storefront Home & Product Detail): 60fps 3D Tilt, Glare, Magnetic CTAs,
 *                 Carbonation Canvas, Energy Cursor Halo, Brand Aura & Scroll Choreography
 *   - 'precision' (Admin Portal & Checkout/Utility Pages): Raycast Border Spotlights,
 *                 Scroll Progress, View Reveals & Exact KPI Count-Up
 *
 * Strictly zero-dependency, compositor-only (transform/opacity), WCAG reduced-motion safe,
 * and 100% compatible with both file:// offline browsing and GitHub Pages.
 */
(function (window, document) {
  'use strict';

  if (typeof window === 'undefined' || typeof document === 'undefined') {
    return;
  }

  const STORAGE_KEY_CANVAS_PAUSED = 'eb_canvas_paused';

  const BRAND_COLOR_MAP = {
    '#39ff14': '57, 255, 20',
    '#00e676': '57, 255, 20',
    'monster': '57, 255, 20',
    'green': '57, 255, 20',
    '#00e5ff': '0, 229, 255',
    '#00d2ff': '0, 229, 255',
    'cyan': '0, 229, 255',
    'ultra': '0, 229, 255',
    '#00ff66': '0, 255, 102',
    'mint': '0, 255, 102',
    '#ffd700': '255, 215, 0',
    'redbull': '255, 215, 0',
    'gold': '255, 215, 0',
    '#ff6b00': '255, 107, 0',
    'orange': '255, 107, 0',
    '#ff0055': '255, 0, 85',
    'sting': '255, 0, 85',
    '#ff1493': '255, 20, 147',
    'pink': '255, 20, 147'
  };

  const KPI_CYCLE_RGB = [
    '57, 255, 20',
    '0, 229, 255',
    '255, 215, 0',
    '255, 0, 85'
  ];

  const SPOTLIGHT_SELECTOR = [
    '.product-card-stitch',
    '.kpi-card',
    '.admin-section-box',
    '.feature-strip-item',
    '.trust-item',
    '.flash-sale-section',
    '.combo-banner',
    '.sidebar-filter-card',
    '.login-card',
    '.cart-summary-card',
    '.cart-summary-box',
    '.account-card',
    '.detail-info-card',
    '.order-card',
    '.admin-topbar'
  ].join(', ');

  const REVEAL_SELECTOR = [
    '.flash-sale-section',
    '.main-products-section',
    '.combo-banner',
    '.trust-item',
    '.faq-item',
    '.product-card-stitch',
    '.kpi-card',
    '.admin-section-box'
  ].join(', ');

  const SECTION_AURA_COLORS = [
    { selector: '.hero-kinetic-section', color: 'rgba(57, 255, 20, 0.16)' },
    { selector: '#flash-sale', color: 'rgba(0, 229, 255, 0.15)' },
    { selector: '#monster-products', color: 'rgba(57, 255, 20, 0.16)' },
    { selector: '#redbull-products', color: 'rgba(255, 215, 0, 0.16)' },
    { selector: '#sting-products', color: 'rgba(255, 0, 85, 0.16)' },
    { selector: '.combo-section', color: 'rgba(57, 255, 20, 0.16)' }
  ];

  const state = {
    mode: 'precision',
    pointerFine: false,
    reducedMotion: false,
    cleanups: [],
    observers: [],
    rafs: new Set(),
    timers: new Set(),
    injectedNodes: [],
    patchedPositions: [],
    heroCanvas: null
  };

  function trackListener(target, type, handler, options) {
    if (!target || typeof target.addEventListener !== 'function') return;
    target.addEventListener(type, handler, options);
    state.cleanups.push(function () {
      target.removeEventListener(type, handler, options);
    });
  }

  function trackObserver(observer) {
    if (observer) state.observers.push(observer);
    return observer;
  }

  function requestTrackedFrame(fn) {
    const id = window.requestAnimationFrame(function (ts) {
      state.rafs.delete(id);
      fn(ts);
    });
    state.rafs.add(id);
    return id;
  }

  function cancelTrackedFrame(id) {
    if (!id) return;
    window.cancelAnimationFrame(id);
    state.rafs.delete(id);
  }

  function setTrackedTimeout(fn, ms) {
    const id = window.setTimeout(function () {
      state.timers.delete(id);
      fn();
    }, ms);
    state.timers.add(id);
    return id;
  }

  function clearTrackedTimeout(id) {
    if (!id) return;
    window.clearTimeout(id);
    state.timers.delete(id);
  }

  function trackInjectedNode(el) {
    if (el) state.injectedNodes.push(el);
    return el;
  }

  function hasDirectChildWithClass(parent, className) {
    if (!parent || !parent.children) return false;
    for (let i = 0; i < parent.children.length; i++) {
      if (parent.children[i].classList && parent.children[i].classList.contains(className)) {
        return true;
      }
    }
    return false;
  }

  function safeReadStorage(key) {
    try {
      return window.localStorage ? window.localStorage.getItem(key) : null;
    } catch (err) {
      return null;
    }
  }

  function safeWriteStorage(key, value) {
    try {
      if (window.localStorage) {
        window.localStorage.setItem(key, value);
      }
    } catch (err) {
      /* ignore storage access errors in restricted/file contexts */
    }
  }

  function parseCssSupports(query, fallbackValue) {
    try {
      if (typeof window.CSS !== 'undefined' && typeof window.CSS.supports === 'function') {
        return arguments.length === 2
          ? window.CSS.supports(query, fallbackValue)
          : window.CSS.supports(query);
      }
    } catch (err) {
      return false;
    }
    return false;
  }

  function resolveBrandRgbFromHint(hintText) {
    if (!hintText) return '';
    const normalized = String(hintText).toLowerCase();

    const keys = Object.keys(BRAND_COLOR_MAP);
    for (let i = 0; i < keys.length; i++) {
      if (normalized.indexOf(keys[i]) !== -1) {
        return BRAND_COLOR_MAP[keys[i]];
      }
    }

    const rgbMatch = normalized.match(/rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})/);
    if (rgbMatch) {
      return rgbMatch[1] + ', ' + rgbMatch[2] + ', ' + rgbMatch[3];
    }

    return '';
  }

  function parseRgbTuple(rgbStr) {
    const parts = String(rgbStr || '57, 255, 20').split(',');
    return [
      parseInt(parts[0], 10) || 0,
      parseInt(parts[1], 10) || 0,
      parseInt(parts[2], 10) || 0
    ];
  }

  /**
   * 1. Context Mode & Capability Detection
   */
  function detectMode() {
    const rawPath = (window.location && window.location.pathname) ? window.location.pathname : '';
    const path = rawPath.toLowerCase().replace(/\\/g, '/');

    const isAdmin = path.indexOf('/admin/') !== -1 || /\/admin$/.test(path);
    const isPrecisionUtility = /(?:^|\/)(cart|orders|order-detail|order-success|payment-gateway|account|login|search-results)(?:\.html)?$/.test(path);

    let mode = 'precision';
    if (!isAdmin && !isPrecisionUtility) {
      const isHome = path === '' ||
        path === '/' ||
        path.endsWith('/index.html') ||
        (path.endsWith('/') && path.indexOf('/pages/') === -1);
      const isProductDetail = path.indexOf('/pages/product-detail') !== -1;
      const hasKineticDom = Boolean(
        document.querySelector &&
        document.querySelector('.hero-kinetic-section, .detail-grid, .product-detail-section, .detail-page-section')
      );

      if (isHome || isProductDetail || hasKineticDom) {
        mode = 'kinetic';
      }
    }

    const pointerFine = typeof window.matchMedia === 'function'
      ? window.matchMedia('(pointer: fine)').matches
      : false;
    const reducedMotion = typeof window.matchMedia === 'function'
      ? window.matchMedia('(prefers-reduced-motion: reduce)').matches
      : false;

    const root = document.documentElement;
    if (root) {
      root.dataset.uiMode = mode;
      if (root.classList) {
        root.classList.toggle('kg-pointer-fine', pointerFine);
        root.classList.toggle('kg-reduced-motion', reducedMotion);
      }
    }

    state.mode = mode;
    state.pointerFine = pointerFine;
    state.reducedMotion = reducedMotion;

    return { mode: mode, pointerFine: pointerFine, reducedMotion: reducedMotion };
  }

  /**
   * 2. Inject Global Adaptive Kinetic Glass Shell Elements
   */
  function injectShellElements(mode, pointerFine, reducedMotion) {
    const body = document.body;
    if (!body) return;

    if (!document.getElementById('volt-scroll-progress')) {
      const progress = document.createElement('div');
      progress.id = 'volt-scroll-progress';
      progress.className = 'volt-scroll-progress';
      progress.setAttribute('aria-hidden', 'true');
      body.insertBefore(progress, body.firstChild);
      trackInjectedNode(progress);
    }

    if (!document.getElementById('kg-ambient-aura')) {
      const aura = document.createElement('div');
      aura.id = 'kg-ambient-aura';
      aura.className = 'kg-ambient-aura';
      aura.setAttribute('aria-hidden', 'true');
      body.appendChild(aura);
      trackInjectedNode(aura);
    }

    if (!document.getElementById('kg-film-grain')) {
      const grain = document.createElement('div');
      grain.id = 'kg-film-grain';
      grain.className = 'kg-film-grain';
      grain.setAttribute('aria-hidden', 'true');
      body.appendChild(grain);
      trackInjectedNode(grain);
    }

    if (mode === 'kinetic' && pointerFine && !reducedMotion && !document.getElementById('kg-cursor-halo')) {
      const halo = document.createElement('div');
      halo.id = 'kg-cursor-halo';
      halo.className = 'kg-cursor-halo';
      halo.setAttribute('aria-hidden', 'true');
      const label = document.createElement('span');
      label.className = 'kg-cursor-label';
      halo.appendChild(label);
      body.appendChild(halo);
      trackInjectedNode(halo);
    }
  }

  /**
   * 3. Brand Accents, Spotlight Containers & Specular Glare Layers
   */
  function detectCardBrandRgb(card) {
    if (!card) return '57, 255, 20';

    const glow = card.querySelector('.product-card-micro-glow');
    if (glow) {
      const hint = [
        glow.getAttribute('style') || '',
        glow.style ? glow.style.backgroundColor : '',
        glow.style ? glow.style.background : ''
      ].join(' ');
      const rgb = resolveBrandRgbFromHint(hint);
      if (rgb) return rgb;
    }

    if (card.closest('#redbull-products')) return '255, 215, 0';
    if (card.closest('#sting-products')) return '255, 0, 85';
    if (card.closest('#monster-products')) return '57, 255, 20';

    const titleText = (card.textContent || '').toLowerCase();
    if (titleText.indexOf('redbull') !== -1) return '255, 215, 0';
    if (titleText.indexOf('sting') !== -1) return '255, 0, 85';
    if (titleText.indexOf('ultra') !== -1) return '0, 229, 255';

    return '57, 255, 20';
  }

  function detectContainerBrandRgb(el, kpiIndexRef) {
    if (el.classList.contains('product-card-stitch')) {
      return detectCardBrandRgb(el);
    }

    if (el.classList.contains('kpi-card')) {
      const rgb = KPI_CYCLE_RGB[kpiIndexRef.index % KPI_CYCLE_RGB.length];
      kpiIndexRef.index += 1;
      return rgb;
    }

    if (el.classList.contains('flash-sale-section')) {
      return '255, 107, 0';
    }

    if (el.classList.contains('feature-strip-item')) {
      const iconBox = el.querySelector('.feature-icon-box');
      if (iconBox) {
        if (iconBox.classList.contains('mint')) return '0, 255, 102';
        if (iconBox.classList.contains('cyan')) return '0, 229, 255';
      }
      return '57, 255, 20';
    }

    const path = ((window.location && window.location.pathname) || '').toLowerCase();
    if (path.indexOf('redbull') !== -1) return '255, 215, 0';
    if (path.indexOf('sting') !== -1) return '255, 0, 85';

    return '57, 255, 20';
  }

  function initBrandAccents(mode, rootNode) {
    const scope = rootNode && typeof rootNode.querySelectorAll === 'function' ? rootNode : document;
    const targets = scope.querySelectorAll(SPOTLIGHT_SELECTOR);
    const kpiIndexRef = { index: 0 };

    for (let i = 0; i < targets.length; i++) {
      const el = targets[i];
      el.classList.add('kg-spotlight');

      if (typeof window.getComputedStyle === 'function') {
        const pos = window.getComputedStyle(el).position;
        if (pos === 'static') {
          el.style.position = 'relative';
          state.patchedPositions.push(el);
        }
      }

      if (!hasDirectChildWithClass(el, 'kg-border-glow')) {
        const borderGlow = document.createElement('span');
        borderGlow.className = 'kg-border-glow';
        borderGlow.setAttribute('aria-hidden', 'true');
        el.appendChild(borderGlow);
        trackInjectedNode(borderGlow);
      }

      if (el.classList.contains('product-card-stitch')) {
        const brandRgb = detectCardBrandRgb(el);
        el.style.setProperty('--brand-rgb', brandRgb);

        if (!hasDirectChildWithClass(el, 'kg-glare-layer')) {
          const glare = document.createElement('span');
          glare.className = 'kg-glare-layer';
          glare.setAttribute('aria-hidden', 'true');
          el.appendChild(glare);
          trackInjectedNode(glare);
        }
      } else if (!el.style.getPropertyValue('--brand-rgb')) {
        const containerRgb = detectContainerBrandRgb(el, kpiIndexRef);
        el.style.setProperty('--brand-rgb', containerRgb);
      }
    }

    const searchGrid = document.getElementById('search-results-grid');
    if (searchGrid && typeof window.MutationObserver === 'function' && !searchGrid.dataset.kgObserved) {
      searchGrid.dataset.kgObserved = '1';
      const gridObserver = trackObserver(new window.MutationObserver(function () {
        initBrandAccents(mode, searchGrid);
        const dynamicCards = searchGrid.querySelectorAll('.product-card-stitch');
        for (let j = 0; j < dynamicCards.length; j++) {
          dynamicCards[j].classList.add('kg-scroll-reveal', 'kg-reveal-visible');
          dynamicCards[j].classList.remove('kg-reveal-pending');
        }
      }));
      gridObserver.observe(searchGrid, { childList: true });
    }
  }

  /**
   * 4. Raycast Border Spotlight (Single rAF-throttled passive pointermove)
   */
  function initRaycastSpotlight() {
    let pendingEvent = null;
    let rafId = 0;
    let activeHovered = null;
    const proximityActive = new Set();
    const PROXIMITY_RADIUS = 240;

    function clearHovered() {
      if (activeHovered) {
        activeHovered.classList.remove('is-hovered');
        activeHovered = null;
      }
    }

    function flushRaycast() {
      rafId = 0;
      if (!pendingEvent) return;

      const x = pendingEvent.x;
      const y = pendingEvent.y;
      const target = pendingEvent.target;

      const hoveredCard = target && typeof target.closest === 'function'
        ? target.closest('.kg-spotlight')
        : null;

      if (hoveredCard !== activeHovered) {
        if (activeHovered) activeHovered.classList.remove('is-hovered');
        if (hoveredCard) hoveredCard.classList.add('is-hovered');
        activeHovered = hoveredCard;
      }

      const cards = document.querySelectorAll('.kg-spotlight');
      const updates = [];

      // Batch DOM geometry reads before style writes to avoid layout thrashing
      for (let i = 0; i < cards.length; i++) {
        const card = cards[i];
        const rect = card.getBoundingClientRect();
        if (rect.width === 0 && rect.height === 0) continue;

        const dx = Math.max(rect.left - x, 0, x - rect.right);
        const dy = Math.max(rect.top - y, 0, y - rect.bottom);
        const dist = Math.hypot(dx, dy);

        if (card === hoveredCard || dist <= PROXIMITY_RADIUS) {
          updates.push({
            card: card,
            mx: Math.round(x - rect.left),
            my: Math.round(y - rect.top)
          });
        }
      }

      const nextSet = new Set();
      for (let i = 0; i < updates.length; i++) {
        const u = updates[i];
        u.card.style.setProperty('--mx', u.mx + 'px');
        u.card.style.setProperty('--my', u.my + 'px');
        nextSet.add(u.card);
      }

      proximityActive.forEach(function (prevCard) {
        if (!nextSet.has(prevCard)) {
          prevCard.classList.remove('is-hovered');
        }
      });

      proximityActive.clear();
      nextSet.forEach(function (c) {
        proximityActive.add(c);
      });
    }

    trackListener(document, 'pointermove', function (e) {
      pendingEvent = { x: e.clientX, y: e.clientY, target: e.target };
      if (!rafId) {
        rafId = requestTrackedFrame(flushRaycast);
      }
    }, { passive: true });

    trackListener(document, 'pointerout', function (e) {
      if (activeHovered && (!e.relatedTarget || !activeHovered.contains(e.relatedTarget))) {
        const nextCard = e.relatedTarget && typeof e.relatedTarget.closest === 'function'
          ? e.relatedTarget.closest('.kg-spotlight')
          : null;
        if (nextCard !== activeHovered) {
          activeHovered.classList.remove('is-hovered');
          activeHovered = nextCard || null;
          if (activeHovered) activeHovered.classList.add('is-hovered');
        }
      }
    }, { passive: true });

    trackListener(document.documentElement, 'pointerleave', clearHovered, { passive: true });
    trackListener(window, 'blur', clearHovered);

    state.cleanups.push(function () {
      cancelTrackedFrame(rafId);
      clearHovered();
    });
  }

  /**
   * 5. 3D Tilt & Metallic Glare on Product Cards + Interactive Hero Stage
   */
  function init3DTiltAndGlare() {
    let activeCard = null;
    let lastMove = null;
    let cardRafId = 0;

    function resetCard(card) {
      if (!card) return;
      card.style.setProperty('--rx', '0deg');
      card.style.setProperty('--ry', '0deg');
      card.style.setProperty('--gx', '50%');
      card.style.setProperty('--gy', '50%');
      card.classList.remove('kg-tilt-active', 'is-hovered');
    }

    function flushCardTilt() {
      cardRafId = 0;
      if (!lastMove) return;

      const card = lastMove.target && typeof lastMove.target.closest === 'function'
        ? lastMove.target.closest('.product-card-stitch')
        : null;

      if (activeCard && activeCard !== card) {
        resetCard(activeCard);
      }
      activeCard = card;

      if (!card) return;

      const rect = card.getBoundingClientRect();
      if (!rect.width || !rect.height) return;

      const px = Math.max(0, Math.min(1, (lastMove.x - rect.left) / rect.width));
      const py = Math.max(0, Math.min(1, (lastMove.y - rect.top) / rect.height));
      const nx = px - 0.5;
      const ny = py - 0.5;

      const rx = (-ny * 14).toFixed(2) + 'deg'; // ±7deg max
      const ry = (nx * 16).toFixed(2) + 'deg';  // ±8deg max
      const gx = (px * 100).toFixed(1) + '%';
      const gy = (py * 100).toFixed(1) + '%';

      card.style.setProperty('--rx', rx);
      card.style.setProperty('--ry', ry);
      card.style.setProperty('--gx', gx);
      card.style.setProperty('--gy', gy);
      card.classList.add('kg-tilt-active');
    }

    trackListener(document, 'pointermove', function (e) {
      lastMove = { x: e.clientX, y: e.clientY, target: e.target };
      if (!cardRafId) {
        cardRafId = requestTrackedFrame(flushCardTilt);
      }
    }, { passive: true });

    trackListener(document, 'pointerout', function (e) {
      if (activeCard && (!e.relatedTarget || !activeCard.contains(e.relatedTarget))) {
        resetCard(activeCard);
        activeCard = null;
      }
    }, { passive: true });

    trackListener(document.documentElement, 'pointerleave', function () {
      if (activeCard) {
        resetCard(activeCard);
        activeCard = null;
      }
    }, { passive: true });

    // Interactive Hero 3D Stage
    const heroSection = document.querySelector('.hero-kinetic-section');
    if (heroSection) {
      const originalCan = heroSection.querySelector('.can-stage-card.original');
      const ultraCan = heroSection.querySelector('.can-stage-card.ultra');
      const spotlightDisc = heroSection.querySelector('.stage-spotlight-disc');
      let heroMove = null;
      let heroRafId = 0;

      function applyStageDepth(nx, ny) {
        const spotX = (nx * 26).toFixed(1) + 'px';
        const spotY = (ny * 20).toFixed(1) + 'px';

        if (spotlightDisc) {
          spotlightDisc.style.setProperty('--spot-x', spotX);
          spotlightDisc.style.setProperty('--spot-y', spotY);
          if (typeof window.getComputedStyle === 'function' && window.getComputedStyle(spotlightDisc).transform === 'none') {
            spotlightDisc.style.translate = spotX + ' ' + spotY;
          }
        }

        if (originalCan) {
          originalCan.style.translate = (nx * -10).toFixed(1) + 'px ' + (ny * -8).toFixed(1) + 'px';
        }
        if (ultraCan) {
          ultraCan.style.translate = (nx * 14).toFixed(1) + 'px ' + (ny * 10).toFixed(1) + 'px';
        }
      }

      function flushHeroStage() {
        heroRafId = 0;
        if (!heroMove) return;
        const rect = heroSection.getBoundingClientRect();
        if (!rect.width || !rect.height) return;
        const nx = Math.max(-0.5, Math.min(0.5, (heroMove.x - rect.left) / rect.width - 0.5));
        const ny = Math.max(-0.5, Math.min(0.5, (heroMove.y - rect.top) / rect.height - 0.5));
        applyStageDepth(nx, ny);
      }

      trackListener(heroSection, 'pointermove', function (e) {
        heroMove = { x: e.clientX, y: e.clientY };
        if (!heroRafId) {
          heroRafId = requestTrackedFrame(flushHeroStage);
        }
      }, { passive: true });

      trackListener(heroSection, 'pointerleave', function () {
        cancelTrackedFrame(heroRafId);
        heroRafId = 0;
        heroMove = null;
        applyStageDepth(0, 0);
        if (state.heroCanvas) state.heroCanvas.setAccentRgb('57, 255, 20');
      }, { passive: true });

      if (originalCan) {
        trackListener(originalCan, 'pointerenter', function () {
          if (state.heroCanvas) state.heroCanvas.setAccentRgb('57, 255, 20');
        }, { passive: true });
        trackListener(originalCan, 'pointerleave', function () {
          if (state.heroCanvas) state.heroCanvas.setAccentRgb('57, 255, 20');
        }, { passive: true });
      }

      if (ultraCan) {
        trackListener(ultraCan, 'pointerenter', function () {
          if (state.heroCanvas) state.heroCanvas.setAccentRgb('255, 215, 0');
        }, { passive: true });
        trackListener(ultraCan, 'pointerleave', function () {
          if (state.heroCanvas) state.heroCanvas.setAccentRgb('57, 255, 20');
        }, { passive: true });
      }

      state.cleanups.push(function () {
        cancelTrackedFrame(heroRafId);
        if (originalCan) originalCan.style.translate = '';
        if (ultraCan) ultraCan.style.translate = '';
        if (spotlightDisc) spotlightDisc.style.translate = '';
      });
    }

    state.cleanups.push(function () {
      cancelTrackedFrame(cardRafId);
      if (activeCard) resetCard(activeCard);
    });
  }

  /**
   * 6. Magnetic Button-in-Button Pull (±8px max)
   */
  function initMagneticButtons() {
    const MAGNETIC_SELECTOR = '.btn-stitch-primary, .btn-stitch-secondary, .btn-combo-now, .btn-add-stitch';
    let activeBtn = null;
    let magEvent = null;
    let magRafId = 0;

    function resetBtn(btn) {
      if (!btn) return;
      btn.style.setProperty('--mag-x', '0px');
      btn.style.setProperty('--mag-y', '0px');
    }

    function flushMagnetic() {
      magRafId = 0;
      if (!magEvent) return;

      const btn = magEvent.target && typeof magEvent.target.closest === 'function'
        ? magEvent.target.closest(MAGNETIC_SELECTOR)
        : null;

      if (activeBtn && activeBtn !== btn) {
        resetBtn(activeBtn);
      }
      activeBtn = btn;

      if (!btn) return;

      const rect = btn.getBoundingClientRect();
      if (!rect.width || !rect.height) return;

      const relX = Math.max(-1, Math.min(1, (magEvent.x - (rect.left + rect.width / 2)) / (rect.width / 2)));
      const relY = Math.max(-1, Math.min(1, (magEvent.y - (rect.top + rect.height / 2)) / (rect.height / 2)));

      btn.style.setProperty('--mag-x', (relX * 8).toFixed(2) + 'px');
      btn.style.setProperty('--mag-y', (relY * 8).toFixed(2) + 'px');
    }

    trackListener(document, 'pointermove', function (e) {
      magEvent = { x: e.clientX, y: e.clientY, target: e.target };
      if (!magRafId) {
        magRafId = requestTrackedFrame(flushMagnetic);
      }
    }, { passive: true });

    trackListener(document, 'pointerout', function (e) {
      if (activeBtn && (!e.relatedTarget || !activeBtn.contains(e.relatedTarget))) {
        resetBtn(activeBtn);
        activeBtn = null;
      }
    }, { passive: true });

    trackListener(document.documentElement, 'pointerleave', function () {
      if (activeBtn) {
        resetBtn(activeBtn);
        activeBtn = null;
      }
    }, { passive: true });

    state.cleanups.push(function () {
      cancelTrackedFrame(magRafId);
      if (activeBtn) resetBtn(activeBtn);
    });
  }

  /**
   * 7. Adaptive Energy Cursor Halo & Brand Click Ripple
   */
  function initEnergyCursorAndRipple() {
    const halo = document.getElementById('kg-cursor-halo');
    if (!halo) return;

    const labelEl = halo.querySelector('.kg-cursor-label');
    const LERP_FACTOR = 0.16;
    const STOP_THRESHOLD = 0.15;

    let targetX = 0;
    let targetY = 0;
    let currentX = 0;
    let currentY = 0;
    let initialized = false;
    let cursorRafId = 0;
    let activeCursorRgb = '57, 255, 20';
    let lastLabel = '';

    function resolveCursorContext(target) {
      if (!target || typeof target.closest !== 'function') {
        return { label: '', rgb: '57, 255, 20' };
      }

      const addBtn = target.closest('.btn-add-stitch, .btn-add-cart, .btn-detail-add-cart');
      if (addBtn) {
        const card = addBtn.closest('.kg-spotlight');
        const rgb = (card && card.style.getPropertyValue('--brand-rgb').trim()) || '57, 255, 20';
        return { label: 'THÊM GIỎ ⚡', rgb: rgb };
      }

      const ctaBtn = target.closest('.btn-stitch-primary, .btn-stitch-secondary, .btn-combo-now');
      if (ctaBtn) {
        const rgb = ctaBtn.classList.contains('btn-stitch-secondary') ? '255, 215, 0' : '57, 255, 20';
        return { label: 'KHÁM PHÁ ⚡', rgb: rgb };
      }

      const viewEl = target.closest('.product-img-wrapper, .can-stage-card');
      if (viewEl) {
        let rgb = '57, 255, 20';
        if (viewEl.classList.contains('ultra')) {
          rgb = '255, 215, 0';
        } else if (viewEl.classList.contains('original')) {
          rgb = '57, 255, 20';
        } else {
          const card = viewEl.closest('.kg-spotlight');
          if (card && card.style.getPropertyValue('--brand-rgb')) {
            rgb = card.style.getPropertyValue('--brand-rgb').trim();
          }
        }
        return { label: 'XEM LON ↗', rgb: rgb };
      }

      const spotlight = target.closest('.kg-spotlight');
      const fallbackRgb = (spotlight && spotlight.style.getPropertyValue('--brand-rgb').trim()) || '57, 255, 20';
      return { label: '', rgb: fallbackRgb };
    }

    function applyHaloPosition(x, y) {
      halo.style.setProperty('--cx', x.toFixed(2) + 'px');
      halo.style.setProperty('--cy', y.toFixed(2) + 'px');
    }

    function tickCursor() {
      cursorRafId = 0;
      const dx = targetX - currentX;
      const dy = targetY - currentY;

      if (Math.abs(dx) < STOP_THRESHOLD && Math.abs(dy) < STOP_THRESHOLD) {
        currentX = targetX;
        currentY = targetY;
        applyHaloPosition(currentX, currentY);
        return;
      }

      currentX += dx * LERP_FACTOR;
      currentY += dy * LERP_FACTOR;
      applyHaloPosition(currentX, currentY);
      cursorRafId = requestTrackedFrame(tickCursor);
    }

    function hideHalo() {
      halo.classList.remove('is-visible', 'has-label', 'is-active');
      if (labelEl && lastLabel !== '') {
        labelEl.textContent = '';
        lastLabel = '';
      }
      cancelTrackedFrame(cursorRafId);
      cursorRafId = 0;
    }

    trackListener(document, 'pointermove', function (e) {
      if (e.pointerType && e.pointerType !== 'mouse' && e.pointerType !== 'pen') {
        hideHalo();
        return;
      }

      targetX = e.clientX;
      targetY = e.clientY;

      if (!initialized) {
        currentX = targetX;
        currentY = targetY;
        initialized = true;
        applyHaloPosition(currentX, currentY);
      }

      const ctx = resolveCursorContext(e.target);
      activeCursorRgb = ctx.rgb;
      halo.style.setProperty('--cursor-rgb', ctx.rgb);
      halo.classList.add('is-visible');

      const hasText = Boolean(ctx.label);
      halo.classList.toggle('has-label', hasText);
      halo.classList.toggle('is-labeled', hasText);
      halo.classList.toggle('is-active', hasText);

      if (labelEl && ctx.label !== lastLabel) {
        labelEl.textContent = ctx.label;
        lastLabel = ctx.label;
      }

      if (!cursorRafId) {
        cursorRafId = requestTrackedFrame(tickCursor);
      }
    }, { passive: true });

    let scrollResyncTimer = 0;
    function clearCursorLabelDuringScroll() {
      if (lastLabel !== '' && labelEl) {
        labelEl.textContent = '';
        lastLabel = '';
      }
      halo.classList.remove('has-label', 'is-labeled', 'is-active');
    }

    trackListener(window, 'scroll', function () {
      if (!initialized || !halo.classList.contains('is-visible')) return;
      clearCursorLabelDuringScroll();
      clearTrackedTimeout(scrollResyncTimer);
      scrollResyncTimer = setTrackedTimeout(function () {
        if (!initialized || !halo.classList.contains('is-visible')) return;
        if (typeof document.elementFromPoint !== 'function') return;
        const under = document.elementFromPoint(targetX, targetY);
        const ctx = resolveCursorContext(under);
        activeCursorRgb = ctx.rgb;
        halo.style.setProperty('--cursor-rgb', ctx.rgb);
        const hasText = Boolean(ctx.label);
        halo.classList.toggle('has-label', hasText);
        halo.classList.toggle('is-labeled', hasText);
        halo.classList.toggle('is-active', hasText);
        if (labelEl && ctx.label !== lastLabel) {
          labelEl.textContent = ctx.label;
          lastLabel = ctx.label;
        }
      }, 140);
    }, { passive: true });

    state.cleanups.push(function () {
      clearTrackedTimeout(scrollResyncTimer);
    });

    trackListener(document.documentElement, 'pointerleave', hideHalo, { passive: true });
    trackListener(window, 'blur', hideHalo);

    trackListener(document, 'pointerdown', function (e) {
      if (e.button === 2) return;
      if (!document.body) return;

      const ctx = resolveCursorContext(e.target);
      const rippleRgb = ctx.rgb || activeCursorRgb || '57, 255, 20';

      const ripple = document.createElement('span');
      ripple.className = 'kg-click-ripple';
      ripple.setAttribute('aria-hidden', 'true');
      ripple.style.left = e.clientX + 'px';
      ripple.style.top = e.clientY + 'px';
      ripple.style.setProperty('--cursor-rgb', rippleRgb);
      ripple.style.setProperty('--ripple-rgb', rippleRgb);

      let cleaned = false;
      let fallbackTimer = 0;

      function cleanupRipple() {
        if (cleaned) return;
        cleaned = true;
        clearTrackedTimeout(fallbackTimer);
        if (ripple.parentNode) {
          ripple.parentNode.removeChild(ripple);
        }
      }

      ripple.addEventListener('animationend', cleanupRipple, { once: true });
      fallbackTimer = setTrackedTimeout(cleanupRipple, 500);

      document.body.appendChild(ripple);
      trackInjectedNode(ripple);
    }, { passive: true });

    state.cleanups.push(hideHalo);
  }

  /**
   * 8. Hero Carbonation & Volt Sparks 2D Canvas + WCAG Toggle
   */
  function initHeroCarbonationCanvas(reducedMotion) {
    const hero = document.querySelector('.hero-kinetic-section');
    if (!hero) return null;

    let canvas = document.getElementById('kg-hero-canvas');
    if (!canvas) {
      canvas = document.createElement('canvas');
      canvas.id = 'kg-hero-canvas';
      canvas.className = 'kg-hero-canvas';
      canvas.setAttribute('aria-hidden', 'true');
      hero.insertBefore(canvas, hero.firstChild);
      trackInjectedNode(canvas);
    }

    let toggleBtn = document.getElementById('volt-canvas-toggle');
    if (!toggleBtn) {
      toggleBtn = document.createElement('button');
      toggleBtn.type = 'button';
      toggleBtn.id = 'volt-canvas-toggle';
      toggleBtn.className = 'volt-canvas-toggle';
      hero.appendChild(toggleBtn);
      trackInjectedNode(toggleBtn);
    }

    const ctx = canvas.getContext ? canvas.getContext('2d') : null;
    if (!ctx) return null;

    const storedPaused = safeReadStorage(STORAGE_KEY_CANVAS_PAUSED);
    let isUserPaused = storedPaused === '1' || storedPaused === 'true' || Boolean(reducedMotion);
    let heroInViewport = true;
    let rafId = 0;
    let lastTime = 0;
    let width = 0;
    let height = 0;
    let dpr = 1;

    const currentRgb = [57, 255, 20];
    const targetRgb = [57, 255, 20];
    const pointer = { x: 0, y: 0, active: false };
    const particles = [];
    const PARTICLE_COUNT = 65;

    function createParticle(randomY) {
      const w = width || 1200;
      const h = height || 560;
      return {
        x: Math.random() * w,
        y: randomY ? Math.random() * h : h + Math.random() * 40,
        vx: (Math.random() - 0.5) * 0.32,
        vy: 0.38 + Math.random() * 0.85,
        size: 1.1 + Math.random() * 2.5,
        alpha: 0.16 + Math.random() * 0.52,
        phase: Math.random() * Math.PI * 2,
        freq: 0.015 + Math.random() * 0.025,
        isSpark: Math.random() > 0.62,
        cyanMix: Math.random() > 0.72
      };
    }

    function syncButtonLabel() {
      toggleBtn.textContent = isUserPaused ? 'Bật hiệu ứng nền' : 'Tắt hiệu ứng nền';
    }

    function resizeCanvas() {
      const rect = hero.getBoundingClientRect();
      width = Math.max(1, Math.round(rect.width));
      height = Math.max(1, Math.round(rect.height));
      dpr = Math.min(window.devicePixelRatio || 1, 2);

      canvas.width = Math.round(width * dpr);
      canvas.height = Math.round(height * dpr);
      canvas.style.width = width + 'px';
      canvas.style.height = height + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      if (particles.length === 0) {
        for (let i = 0; i < PARTICLE_COUNT; i++) {
          particles.push(createParticle(true));
        }
      }
    }

    function stopLoop() {
      if (rafId) {
        cancelTrackedFrame(rafId);
        rafId = 0;
      }
      lastTime = 0;
    }

    function clearCanvas() {
      ctx.clearRect(0, 0, width, height);
    }

    function shouldAnimate() {
      return !isUserPaused && heroInViewport && !document.hidden;
    }

    function renderFrame(now) {
      rafId = 0;
      if (!shouldAnimate()) return;

      if (!lastTime) lastTime = now;
      const dt = Math.min(2.5, Math.max(0.4, (now - lastTime) / 16.667));
      lastTime = now;

      // Smoothly interpolate active brand accent RGB
      for (let c = 0; c < 3; c++) {
        currentRgb[c] += (targetRgb[c] - currentRgb[c]) * 0.08 * dt;
      }
      const r = Math.round(currentRgb[0]);
      const g = Math.round(currentRgb[1]);
      const b = Math.round(currentRgb[2]);

      ctx.clearRect(0, 0, width, height);

      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];
        p.phase += p.freq * dt;

        // Pointer repulsion with gentle swirl
        if (pointer.active) {
          const dx = p.x - pointer.x;
          const dy = p.y - pointer.y;
          const dist = Math.hypot(dx, dy);
          const radius = 135;
          if (dist > 0.5 && dist < radius) {
            const strength = (1 - dist / radius) * 0.85 * dt;
            const nx = dx / dist;
            const ny = dy / dist;
            p.vx += (nx * 1.15 - ny * 0.65) * strength;
            p.vy -= (ny * 0.6 + nx * 0.45) * strength;
          }
        }

        // Dampen lateral impulse and preserve buoyant upward motion
        p.vx *= 0.96;
        p.vy = Math.max(0.28, Math.min(2.1, p.vy * 0.985 + 0.012 * dt));

        p.x += (p.vx + Math.sin(p.phase) * 0.28) * dt;
        p.y -= p.vy * dt;

        if (p.y < -16 || p.x < -24 || p.x > width + 24) {
          particles[i] = createParticle(false);
          continue;
        }

        const pr = p.cyanMix ? 0 : r;
        const pg = p.cyanMix ? 229 : g;
        const pb = p.cyanMix ? 255 : b;

        if (p.isSpark) {
          ctx.fillStyle = 'rgba(' + pr + ',' + pg + ',' + pb + ',' + p.alpha.toFixed(2) + ')';
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.size * 0.72, 0, Math.PI * 2);
          ctx.fill();
        } else {
          ctx.strokeStyle = 'rgba(' + pr + ',' + pg + ',' + pb + ',' + (p.alpha * 0.88).toFixed(2) + ')';
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
          ctx.stroke();
        }
      }

      rafId = requestTrackedFrame(renderFrame);
    }

    function syncLoopState() {
      syncButtonLabel();
      canvas.style.opacity = isUserPaused ? '0' : '1';
      if (shouldAnimate()) {
        if (!rafId) {
          lastTime = 0;
          rafId = requestTrackedFrame(renderFrame);
        }
      } else {
        stopLoop();
        if (isUserPaused) clearCanvas();
      }
    }

    function toggle(forceRunning) {
      if (typeof forceRunning === 'boolean') {
        isUserPaused = !forceRunning;
      } else {
        isUserPaused = !isUserPaused;
      }
      safeWriteStorage(STORAGE_KEY_CANVAS_PAUSED, isUserPaused ? '1' : '0');
      syncLoopState();
      return !isUserPaused;
    }

    function setAccentRgb(rgbStr) {
      const tuple = parseRgbTuple(rgbStr);
      targetRgb[0] = tuple[0];
      targetRgb[1] = tuple[1];
      targetRgb[2] = tuple[2];
    }

    resizeCanvas();
    syncLoopState();

    trackListener(toggleBtn, 'click', function () {
      toggle();
    });

    trackListener(hero, 'pointermove', function (e) {
      const rect = hero.getBoundingClientRect();
      pointer.x = e.clientX - rect.left;
      pointer.y = e.clientY - rect.top;
      pointer.active = true;
    }, { passive: true });

    trackListener(hero, 'pointerleave', function () {
      pointer.active = false;
    }, { passive: true });

    trackListener(document, 'visibilitychange', syncLoopState);

    if (typeof window.IntersectionObserver === 'function') {
      const visObserver = trackObserver(new window.IntersectionObserver(function (entries) {
        if (!entries || !entries.length) return;
        heroInViewport = entries[0].isIntersecting;
        syncLoopState();
      }, { threshold: 0.01 }));
      visObserver.observe(hero);
    }

    let resizeTimer = 0;
    function scheduleResize() {
      clearTrackedTimeout(resizeTimer);
      resizeTimer = setTrackedTimeout(resizeCanvas, 120);
    }

    if (typeof window.ResizeObserver === 'function') {
      const ro = trackObserver(new window.ResizeObserver(scheduleResize));
      ro.observe(hero);
    } else {
      trackListener(window, 'resize', scheduleResize, { passive: true });
    }

    state.cleanups.push(function () {
      stopLoop();
      clearTrackedTimeout(resizeTimer);
    });

    const controller = {
      toggle: toggle,
      setAccentRgb: setAccentRgb,
      isRunning: function () { return !isUserPaused; }
    };
    state.heroCanvas = controller;
    return controller;
  }

  /**
   * 9. Scroll Choreography (Header Sentinel, Progress Fallback, Reveals, Aura, Parallax & Lenis)
   */
  function initScrollChoreography(mode, pointerFine, reducedMotion) {
    // 9A. Header Scroll State via 1px sentinel
    const header = document.querySelector('.header');
    if (header && document.body && typeof window.IntersectionObserver === 'function') {
      let sentinel = document.getElementById('kg-scroll-sentinel');
      if (!sentinel) {
        sentinel = document.createElement('div');
        sentinel.id = 'kg-scroll-sentinel';
        sentinel.setAttribute('aria-hidden', 'true');
        sentinel.style.cssText = 'position:absolute;top:0;left:0;width:1px;height:1px;pointer-events:none;opacity:0;';
        const progress = document.getElementById('volt-scroll-progress');
        if (progress && progress.nextSibling) {
          document.body.insertBefore(sentinel, progress.nextSibling);
        } else {
          document.body.appendChild(sentinel);
        }
        trackInjectedNode(sentinel);
      }

      const headerObserver = trackObserver(new window.IntersectionObserver(function (entries) {
        if (!entries || !entries.length) return;
        header.classList.toggle('kg-scrolled', !entries[0].isIntersecting);
      }, { threshold: 0 }));
      headerObserver.observe(sentinel);
    }

    // 9B. Scroll Progress Fallback (only when native CSS scroll() timeline is unsupported)
    const progressEl = document.getElementById('volt-scroll-progress');
    const supportsScrollTimeline = parseCssSupports('animation-timeline', 'scroll()');
    if (progressEl && !supportsScrollTimeline && !reducedMotion) {
      let progRafId = 0;

      function updateScrollProgress() {
        progRafId = 0;
        const docEl = document.documentElement;
        const maxScroll = Math.max(1, (docEl ? docEl.scrollHeight : 1) - window.innerHeight);
        const scrollTop = window.scrollY || window.pageYOffset || 0;
        const ratio = Math.max(0, Math.min(1, scrollTop / maxScroll));
        progressEl.style.transform = 'scaleX(' + ratio.toFixed(4) + ')';
      }

      updateScrollProgress();
      trackListener(window, 'scroll', function () {
        if (!progRafId) {
          progRafId = requestTrackedFrame(updateScrollProgress);
        }
      }, { passive: true });
      trackListener(window, 'resize', function () {
        if (!progRafId) {
          progRafId = requestTrackedFrame(updateScrollProgress);
        }
      }, { passive: true });

      state.cleanups.push(function () {
        cancelTrackedFrame(progRafId);
      });
    }

    // 9C. Scroll Reveals + CSS.supports fallback
    const revealTargets = document.querySelectorAll(REVEAL_SELECTOR);
    const supportsViewTimeline = parseCssSupports('(animation-timeline: view()) and (animation-range: entry)');

    for (let i = 0; i < revealTargets.length; i++) {
      revealTargets[i].classList.add('kg-scroll-reveal');
    }

    if (!supportsViewTimeline && !reducedMotion && typeof window.IntersectionObserver === 'function' && revealTargets.length > 0) {
      const vh = window.innerHeight || 900;
      const belowFold = [];

      // Read all bounding rects first before toggling classes
      for (let i = 0; i < revealTargets.length; i++) {
        const el = revealTargets[i];
        const rect = el.getBoundingClientRect();
        if (rect.top < vh * 0.96) {
          el.classList.add('kg-reveal-visible');
        } else {
          belowFold.push(el);
        }
      }

      if (belowFold.length > 0) {
        const revealObserver = trackObserver(new window.IntersectionObserver(function (entries, obs) {
          const toReveal = [];
          for (let i = 0; i < entries.length; i++) {
            const entry = entries[i];
            if (entry.isIntersecting || entry.boundingClientRect.top < 0) {
              toReveal.push(entry.target);
              obs.unobserve(entry.target);
            }
          }

          toReveal.forEach(function (el, idx) {
            const delayMs = Math.min(idx * 55, 275);
            el.style.transitionDelay = delayMs + 'ms';
            el.classList.remove('kg-reveal-pending');
            el.classList.add('kg-reveal-visible');
            setTrackedTimeout(function () {
              el.style.transitionDelay = '';
            }, delayMs + 650);
          });
        }, { threshold: 0.08, rootMargin: '0px 0px -24px 0px' }));

        for (let i = 0; i < belowFold.length; i++) {
          belowFold[i].classList.add('kg-reveal-pending');
          revealObserver.observe(belowFold[i]);
        }
      }
    }

    // 9D. Ambient Brand Aura Shift (kinetic mode)
    if (mode === 'kinetic' && document.documentElement) {
      const path = ((window.location && window.location.pathname) || '').toLowerCase();
      if (path.indexOf('redbull') !== -1) {
        document.documentElement.style.setProperty('--kg-aura-color', 'rgba(255, 215, 0, 0.16)');
      } else if (path.indexOf('sting') !== -1) {
        document.documentElement.style.setProperty('--kg-aura-color', 'rgba(255, 0, 85, 0.16)');
      } else {
        document.documentElement.style.setProperty('--kg-aura-color', 'rgba(57, 255, 20, 0.16)');
      }

      const sectionColorMap = new Map();
      const activeAuraSections = new Set();

      SECTION_AURA_COLORS.forEach(function (item) {
        const sec = document.querySelector(item.selector);
        if (sec) {
          sectionColorMap.set(sec, item.color);
          activeAuraSections.add(sec);
        }
      });

      function updateAmbientAuraByViewport() {
        if (!activeAuraSections.size) return;
        const vh = window.innerHeight || 800;
        const anchorY = vh * 0.42;
        let bestColor = null;
        let bestScore = Infinity;

        activeAuraSections.forEach(function (sec) {
          const rect = sec.getBoundingClientRect();
          if (rect.bottom < 0 || rect.top > vh) return;
          const overlapTop = Math.max(0, rect.top);
          const overlapBottom = Math.min(vh, rect.bottom);
          if (overlapBottom <= overlapTop) return;
          const dist = (anchorY >= rect.top && anchorY <= rect.bottom)
            ? 0
            : Math.min(Math.abs(rect.top - anchorY), Math.abs(rect.bottom - anchorY));
          if (dist < bestScore) {
            bestScore = dist;
            bestColor = sectionColorMap.get(sec);
          }
        });

        if (bestColor) {
          document.documentElement.style.setProperty('--kg-aura-color', bestColor);
        }
      }

      let auraRafId = 0;
      function scheduleAuraUpdate() {
        if (auraRafId || !activeAuraSections.size) return;
        auraRafId = requestTrackedFrame(function () {
          auraRafId = 0;
          updateAmbientAuraByViewport();
        });
      }

      if (typeof window.IntersectionObserver === 'function') {
        activeAuraSections.clear();
        const auraObserver = trackObserver(new window.IntersectionObserver(function (entries) {
          for (let i = 0; i < entries.length; i++) {
            if (entries[i].isIntersecting) {
              activeAuraSections.add(entries[i].target);
            } else {
              activeAuraSections.delete(entries[i].target);
            }
          }
          scheduleAuraUpdate();
        }, { threshold: [0, 0.2, 0.5, 0.8] }));

        sectionColorMap.forEach(function (_color, sec) {
          auraObserver.observe(sec);
        });
      } else {
        updateAmbientAuraByViewport();
      }
      trackListener(window, 'scroll', scheduleAuraUpdate, { passive: true });
      state.cleanups.push(function () {
        cancelTrackedFrame(auraRafId);
      });
    }

    // 9E. Layered Parallax & Velocity Micro-Tilt (kinetic + motion allowed)
    if (mode === 'kinetic' && !reducedMotion) {
      const grids = document.querySelectorAll('.products-grid');
      for (let i = 0; i < grids.length; i++) {
        grids[i].classList.add('kg-velocity-grid');
      }

      const parallaxSpecs = [
        { el: document.querySelector('.combo-can.can-1'), factor: -16 },
        { el: document.querySelector('.combo-can.can-2'), factor: -24 },
        { el: document.querySelector('.combo-can.can-3'), factor: -12 },
        { el: document.querySelector('.can-stage-card.original'), factor: -14 },
        { el: document.querySelector('.can-stage-card.ultra'), factor: -20 }
      ].filter(function (spec) { return Boolean(spec.el); });

      const activeParallaxSpecs = new Set(parallaxSpecs);
      const specByEl = new Map();
      parallaxSpecs.forEach(function (spec) {
        specByEl.set(spec.el, spec);
      });

      if (typeof window.IntersectionObserver === 'function' && parallaxSpecs.length > 0) {
        activeParallaxSpecs.clear();
        const parallaxObserver = trackObserver(new window.IntersectionObserver(function (entries) {
          for (let i = 0; i < entries.length; i++) {
            const spec = specByEl.get(entries[i].target);
            if (!spec) continue;
            if (entries[i].isIntersecting) {
              activeParallaxSpecs.add(spec);
            } else {
              activeParallaxSpecs.delete(spec);
            }
          }
        }, { rootMargin: '200px 0px' }));

        parallaxSpecs.forEach(function (spec) {
          parallaxObserver.observe(spec.el);
        });
      }

      let lastScrollY = window.scrollY || window.pageYOffset || 0;
      let scrollRafId = 0;
      let skewResetTimer = 0;

      function applyScrollKinematics() {
        scrollRafId = 0;
        const currentScrollY = window.scrollY || window.pageYOffset || 0;
        const delta = currentScrollY - lastScrollY;
        lastScrollY = currentScrollY;

        const vh = window.innerHeight || 900;
        const vCenter = vh * 0.5;

        // Batch reads strictly over near-viewport parallax elements before writes
        const writes = [];
        activeParallaxSpecs.forEach(function (spec) {
          const rect = spec.el.getBoundingClientRect();
          if (rect.bottom < -200 || rect.top > vh + 200) return;
          const elCenter = rect.top + rect.height * 0.5;
          const norm = Math.max(-1, Math.min(1, (elCenter - vCenter) / vh));
          writes.push({ el: spec.el, y: (norm * spec.factor).toFixed(2) + 'px' });
        });

        for (let i = 0; i < writes.length; i++) {
          writes[i].el.style.setProperty('--parallax-y', writes[i].y);
        }

        if (grids.length > 0 && Math.abs(delta) > 1.5) {
          const skew = Math.max(-2.2, Math.min(2.2, delta * 0.06)).toFixed(2) + 'deg';
          for (let i = 0; i < grids.length; i++) {
            grids[i].style.setProperty('--kg-skew', skew);
          }

          clearTrackedTimeout(skewResetTimer);
          skewResetTimer = setTrackedTimeout(function () {
            for (let i = 0; i < grids.length; i++) {
              grids[i].style.setProperty('--kg-skew', '0deg');
            }
          }, 120);
        }
      }

      applyScrollKinematics();
      trackListener(window, 'scroll', function () {
        if (!scrollRafId) {
          scrollRafId = requestTrackedFrame(applyScrollKinematics);
        }
      }, { passive: true });

      state.cleanups.push(function () {
        cancelTrackedFrame(scrollRafId);
        clearTrackedTimeout(skewResetTimer);
        for (let i = 0; i < grids.length; i++) {
          grids[i].style.setProperty('--kg-skew', '0deg');
        }
      });
    }
  }

  /**
   * 10. Admin Precision Enhancements (Faithful KPI Count-Up)
   */
  function solveCubicBezierY(t, p1x, p1y, p2x, p2y) {
    // Binary-search parameter u so BezierX(u) == t, then evaluate BezierY(u)
    function sampleX(u) {
      const inv = 1 - u;
      return 3 * inv * inv * u * p1x + 3 * inv * u * u * p2x + u * u * u;
    }
    function sampleY(u) {
      const inv = 1 - u;
      return 3 * inv * inv * u * p1y + 3 * inv * u * u * p2y + u * u * u;
    }

    let low = 0;
    let high = 1;
    let u = t;
    for (let i = 0; i < 8; i++) {
      u = (low + high) * 0.5;
      if (sampleX(u) < t) low = u;
      else high = u;
    }
    return sampleY(u);
  }

  function parseKpiValue(rawText) {
    const original = String(rawText || '');
    const trimmed = original.trim();
    const match = trimmed.match(/^([+-]?\s*)(\d+(?:[.,]\d+)*)(.*)$/);
    if (!match) return null;

    const prefix = match[1];
    const numPart = match[2];
    const suffix = match[3];

    let target = 0;
    let decimals = 0;
    let useViDots = false;

    if (/^\d{1,3}(?:\.\d{3})+$/.test(numPart)) {
      useViDots = true;
      target = parseInt(numPart.replace(/\./g, ''), 10);
    } else if (/^\d{1,3}(?:,\d{3})+$/.test(numPart)) {
      target = parseInt(numPart.replace(/,/g, ''), 10);
    } else if (/^\d+\.\d+$/.test(numPart)) {
      decimals = numPart.split('.')[1].length;
      target = parseFloat(numPart);
    } else if (/^\d+,\d+$/.test(numPart)) {
      decimals = numPart.split(',')[1].length;
      target = parseFloat(numPart.replace(',', '.'));
    } else {
      target = parseFloat(numPart.replace(/[.,]/g, ''));
    }

    if (!Number.isFinite(target) || target <= 0) return null;

    return {
      original: original,
      prefix: prefix,
      suffix: suffix,
      target: target,
      decimals: decimals,
      useViDots: useViDots
    };
  }

  function formatKpiFrame(parsed, progress) {
    if (progress >= 1) return parsed.original;
    const eased = solveCubicBezierY(progress, 0.22, 1, 0.36, 1);
    const val = parsed.target * eased;
    let numStr = '';
    if (parsed.decimals > 0) {
      numStr = val.toFixed(parsed.decimals);
    } else if (parsed.useViDots) {
      numStr = Math.round(val).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    } else {
      numStr = Math.round(val).toString();
    }
    return parsed.prefix + numStr + parsed.suffix;
  }

  function initAdminPrecisionEnhancements(mode, reducedMotion) {
    if (mode !== 'precision' || reducedMotion) return;
    if (typeof window.IntersectionObserver !== 'function') return;

    const kpiNodes = document.querySelectorAll('.kpi-value, .kpi-info h3');
    if (!kpiNodes.length) return;

    const DURATION_MS = 750;
    const activeKpiAnimations = [];

    function animateKpi(el) {
      if (el.dataset.kgKpiAnimated === '1') return;
      const parsed = parseKpiValue(el.textContent);
      if (!parsed) return;

      el.dataset.kgKpiAnimated = '1';
      const startTime = typeof window.performance !== 'undefined' && typeof window.performance.now === 'function'
        ? window.performance.now()
        : Date.now();
      let rafId = 0;

      const record = {
        cancel: function () {
          cancelTrackedFrame(rafId);
          el.textContent = parsed.original;
        }
      };
      activeKpiAnimations.push(record);

      function step(now) {
        const currentNow = typeof now === 'number' ? now : Date.now();
        const elapsed = currentNow - startTime;
        const progress = Math.min(1, Math.max(0, elapsed / DURATION_MS));

        el.textContent = formatKpiFrame(parsed, progress);

        if (progress < 1) {
          rafId = requestTrackedFrame(step);
        } else {
          el.textContent = parsed.original;
          rafId = 0;
        }
      }

      rafId = requestTrackedFrame(step);
    }

    const kpiObserver = trackObserver(new window.IntersectionObserver(function (entries, obs) {
      for (let i = 0; i < entries.length; i++) {
        if (entries[i].isIntersecting) {
          obs.unobserve(entries[i].target);
          animateKpi(entries[i].target);
        }
      }
    }, { threshold: 0.15 }));

    for (let i = 0; i < kpiNodes.length; i++) {
      kpiObserver.observe(kpiNodes[i]);
    }

    state.cleanups.push(function () {
      for (let i = 0; i < activeKpiAnimations.length; i++) {
        activeKpiAnimations[i].cancel();
      }
    });
  }

  /**
   * Public API Lifecycle
   */
  function init() {
    if (window.__ENERGY_MOTION_INIT__) {
      return window.EnergyMotionEngine;
    }
    window.__ENERGY_MOTION_INIT__ = true;

    const context = detectMode();
    injectShellElements(context.mode, context.pointerFine, context.reducedMotion);
    initBrandAccents(context.mode);
    initRaycastSpotlight();

    if (context.mode === 'kinetic' && context.pointerFine && !context.reducedMotion) {
      init3DTiltAndGlare();
      initMagneticButtons();
      initEnergyCursorAndRipple();
    }

    if (context.mode === 'kinetic') {
      initHeroCarbonationCanvas(context.reducedMotion);
    }

    initScrollChoreography(context.mode, context.pointerFine, context.reducedMotion);
    initAdminPrecisionEnhancements(context.mode, context.reducedMotion);

    return window.EnergyMotionEngine;
  }

  function getMode() {
    return state.mode || detectMode().mode;
  }

  function toggleCanvas(forceRunning) {
    if (state.heroCanvas && typeof state.heroCanvas.toggle === 'function') {
      return state.heroCanvas.toggle(forceRunning);
    }
    return false;
  }

  function destroy() {
    for (let i = state.cleanups.length - 1; i >= 0; i--) {
      try {
        state.cleanups[i]();
      } catch (err) {
        /* ignore cleanup errors */
      }
    }
    state.cleanups = [];

    state.rafs.forEach(function (id) {
      window.cancelAnimationFrame(id);
    });
    state.rafs.clear();

    state.timers.forEach(function (id) {
      window.clearTimeout(id);
    });
    state.timers.clear();

    for (let i = 0; i < state.observers.length; i++) {
      try {
        state.observers[i].disconnect();
      } catch (err) {
        /* ignore */
      }
    }
    state.observers = [];

    for (let i = 0; i < state.patchedPositions.length; i++) {
      state.patchedPositions[i].style.position = '';
    }
    state.patchedPositions = [];

    for (let i = 0; i < state.injectedNodes.length; i++) {
      const node = state.injectedNodes[i];
      if (node && node.parentNode) {
        node.parentNode.removeChild(node);
      }
    }
    state.injectedNodes = [];

    const header = document.querySelector('.header');
    if (header) header.classList.remove('kg-scrolled');

    const activeEls = document.querySelectorAll('.kg-spotlight, .kg-scroll-reveal, .kg-velocity-grid');
    for (let i = 0; i < activeEls.length; i++) {
      activeEls[i].classList.remove('is-hovered', 'kg-tilt-active', 'kg-reveal-pending');
    }

    const searchGrid = document.getElementById('search-results-grid');
    if (searchGrid && searchGrid.dataset) {
      delete searchGrid.dataset.kgObserved;
    }

    const kpis = document.querySelectorAll('.kpi-value, .kpi-info h3');
    for (let i = 0; i < kpis.length; i++) {
      if (kpis[i].dataset) {
        delete kpis[i].dataset.kgKpiAnimated;
      }
    }

    state.heroCanvas = null;
    window.__ENERGY_MOTION_INIT__ = false;
  }

  window.EnergyMotionEngine = {
    init: init,
    getMode: getMode,
    toggleCanvas: toggleCanvas,
    destroy: destroy
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})(window, document);
