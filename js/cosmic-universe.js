/**
 * ENERGY BOOST STORE - COSMIC UNIVERSE INTRO ENGINE (#cosmic-universe-intro)
 * Unified single-rAF 3-layer starfield, shooting stars, live energy tether,
 * 6-can 3D orbital ellipse physics, hologram inspector, brand filter, and WCAG controls.
 *
 * Strictly zero-dependency, zero scroll-hijacking, zero per-frame DOM layout reads,
 * and 100% compatible with file:// and GitHub Pages.
 */
(function (window, document) {
  'use strict';

  if (typeof window === 'undefined' || typeof document === 'undefined') {
    return;
  }

  const STORAGE_KEY_PAUSED = 'eb_cosmic_paused';
  const LABEL_ACTIVE = 'Tắt chuyển động vũ trụ';
  const LABEL_PAUSED = 'Bật chuyển động vũ trụ';
  const STAR_COUNT = 140;
  const WARP_DURATION_MS = 180;

  const RING_CONFIG = {
    1: { rxFactor: 0.24, ry: 75, speed: 0.20 },
    2: { rxFactor: 0.36, ry: 112, speed: 0.16 },
    3: { rxFactor: 0.47, ry: 148, speed: 0.13 }
  };

  const BRAND_FALLBACKS = {
    monster: {
      brandLabel: 'Monster Energy',
      sectionTarget: 'monster-products',
      rgb: '57, 255, 20',
      core: '#DCFFD2',
      halo: '#39FF14',
      deep: '#0A4D00'
    },
    redbull: {
      brandLabel: 'Redbull Thái Lan',
      sectionTarget: 'redbull-products',
      rgb: '255, 215, 0',
      core: '#FFF7CC',
      halo: '#FFD700',
      deep: '#664400'
    },
    sting: {
      brandLabel: 'Sting PepsiCo',
      sectionTarget: 'sting-products',
      rgb: '255, 0, 85',
      core: '#FFD6E5',
      halo: '#FF0055',
      deep: '#5C001F'
    }
  };

  const state = {
    initialized: false,
    section: null,
    stage: null,
    canvas: null,
    ctx: null,
    warpFlash: null,
    holoCard: null,
    holoImg: null,
    holoBrand: null,
    holoTitle: null,
    holoPrice: null,
    holoDetailLink: null,
    holoShelfBtn: null,
    motionToggle: null,
    filterButtons: [],
    cans: [],
    canMap: new Map(),
    selectedCan: null,
    activeFilter: 'all',
    stars: [],
    shootingStars: [],
    nextMeteorIn: 2.4,
    pointerFine: false,
    reducedMotion: false,
    isPaused: false,
    inViewport: true,
    isWarping: false,
    warpTimer: 0,
    rafId: 0,
    lastFrameTime: 0,
    animTime: 0,
    pulseTime: 0.28,
    speedMultiplier: 1,
    hoveredEls: new Set(),
    focusedEls: new Set(),
    lastTouchTap: { canId: null, wasSelected: false, time: 0 },
    targetParallaxX: 0,
    targetParallaxY: 0,
    currentParallaxX: 0,
    currentParallaxY: 0,
    currentRgb: [57, 255, 20],
    targetRgb: [57, 255, 20],
    geo: {
      canvasWidth: 1200,
      canvasHeight: 680,
      stageWidth: 800,
      stageHeight: 460,
      stageOffsetX: 0,
      stageOffsetY: 0,
      dpr: 1,
      viewportWidth: 1280,
      isDesktop: true
    },
    cleanups: [],
    observers: [],
    timers: new Set()
  };

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
      /* ignore restricted storage contexts (private browsing / file://) */
    }
  }

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

  function setTrackedTimer(fn, ms) {
    const id = window.setTimeout(function () {
      state.timers.delete(id);
      fn();
    }, ms);
    state.timers.add(id);
    return id;
  }

  function clearTrackedTimer(id) {
    if (!id) return;
    window.clearTimeout(id);
    state.timers.delete(id);
  }

  function detectReducedMotion() {
    if (typeof window.matchMedia !== 'function') return false;
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function detectPointerFine() {
    if (typeof window.matchMedia !== 'function') return true;
    return window.matchMedia('(pointer: fine)').matches;
  }

  function hexToRgbStr(hex) {
    if (!hex) return '';
    const cleaned = String(hex).trim().replace('#', '');
    if (cleaned.length === 3) {
      const r = parseInt(cleaned[0] + cleaned[0], 16);
      const g = parseInt(cleaned[1] + cleaned[1], 16);
      const b = parseInt(cleaned[2] + cleaned[2], 16);
      if (Number.isFinite(r) && Number.isFinite(g) && Number.isFinite(b)) {
        return r + ', ' + g + ', ' + b;
      }
    } else if (cleaned.length === 6) {
      const r = parseInt(cleaned.slice(0, 2), 16);
      const g = parseInt(cleaned.slice(2, 4), 16);
      const b = parseInt(cleaned.slice(4, 6), 16);
      if (Number.isFinite(r) && Number.isFinite(g) && Number.isFinite(b)) {
        return r + ', ' + g + ', ' + b;
      }
    }
    return '';
  }

  function parseRgbTuple(rgbStr) {
    const parts = String(rgbStr || '57, 255, 20').split(',');
    return [
      Math.max(0, Math.min(255, parseInt(parts[0], 10) || 0)),
      Math.max(0, Math.min(255, parseInt(parts[1], 10) || 0)),
      Math.max(0, Math.min(255, parseInt(parts[2], 10) || 0))
    ];
  }

  function parseCanData(el, index) {
    const brand = String(el.dataset.brand || 'monster').trim().toLowerCase();
    const fallback = BRAND_FALLBACKS[brand] || BRAND_FALLBACKS.monster;
    const imgChild = el.querySelector('img');

    const id = el.dataset.id || el.dataset.canId || el.id || ('cosmic-can-' + (index + 1));
    const ringRaw = parseInt(el.dataset.ring || '1', 10);
    const ring = (ringRaw === 1 || ringRaw === 2 || ringRaw === 3) ? ringRaw : 1;
    const angleDeg = parseFloat(el.dataset.angle || String(index * 60));
    const safeDeg = Number.isFinite(angleDeg) ? angleDeg : index * 60;
    const initialAngle = (safeDeg * Math.PI) / 180;

    const haloHex = el.dataset.haloHex || el.dataset.halo || el.dataset.canHalo || fallback.halo;
    const coreHex = el.dataset.coreHex || el.dataset.core || el.dataset.canCore || fallback.core;
    const deepHex = el.dataset.deepHex || el.dataset.deep || el.dataset.canDeep || fallback.deep;
    const rgb = el.dataset.rgb || el.dataset.canRgb || hexToRgbStr(haloHex) || fallback.rgb;

    const title = el.dataset.title || el.dataset.name || (imgChild ? imgChild.getAttribute('alt') : '') || '';
    const price = el.dataset.price || '';
    const img = el.dataset.img || (imgChild ? imgChild.getAttribute('src') : '') || '';
    const href = el.dataset.href || el.getAttribute('href') || 'pages/product-detail.html';
    const sectionTarget = el.dataset.sectionTarget || el.dataset.shelf || fallback.sectionTarget;
    const brandLabel = el.dataset.brandLabel || fallback.brandLabel;

    el.style.setProperty('--can-rgb', rgb);
    el.style.setProperty('--can-core', coreHex);
    el.style.setProperty('--can-halo', haloHex);
    el.style.setProperty('--can-deep', deepHex);

    return {
      el: el,
      id: id,
      ring: ring,
      initialAngle: initialAngle,
      angle: initialAngle,
      brand: brand,
      brandLabel: brandLabel,
      title: title,
      price: price,
      img: img,
      href: href,
      sectionTarget: sectionTarget,
      rgb: rgb,
      rgbTuple: parseRgbTuple(rgb),
      coreHex: coreHex,
      haloHex: haloHex,
      deepHex: deepHex,
      x: 0,
      y: 0,
      isDimmed: false,
      lastIsFront: null
    };
  }

  function generateStars() {
    const stars = [];
    for (let i = 0; i < STAR_COUNT; i++) {
      const bucket = i % 10;
      let depth = 0.3;
      let radius = 0.7;
      let baseAlpha = 0.35;

      if (bucket >= 7) {
        depth = 1.0;
        radius = 1.15 + Math.random() * 0.7;
        baseAlpha = 0.52 + Math.random() * 0.38;
      } else if (bucket >= 4) {
        depth = 0.65;
        radius = 0.85 + Math.random() * 0.5;
        baseAlpha = 0.34 + Math.random() * 0.34;
      } else {
        depth = 0.3;
        radius = 0.55 + Math.random() * 0.42;
        baseAlpha = 0.22 + Math.random() * 0.30;
      }

      const tintRoll = Math.random();
      let tintType = 'white';
      if (tintRoll > 0.91) {
        tintType = 'accent';
      } else if (tintRoll > 0.68) {
        tintType = 'blue';
      }

      stars.push({
        nx: -0.03 + Math.random() * 1.06,
        ny: -0.03 + Math.random() * 1.06,
        depth: depth,
        radius: radius,
        baseAlpha: baseAlpha,
        twinklePhase: Math.random() * Math.PI * 2,
        twinkleSpeed: 0.8 + Math.random() * 1.9,
        tintType: tintType,
        hasSparkle: depth === 1.0 && Math.random() > 0.78
      });
    }
    state.stars = stars;
  }

  function spawnShootingStar() {
    const w = state.geo.canvasWidth || 1200;
    const h = state.geo.canvasHeight || 680;
    const dir = Math.random() > 0.45 ? 1 : -1;
    const slope = (24 + Math.random() * 15) * (Math.PI / 180);
    const speed = 760 + Math.random() * 260;

    state.shootingStars.push({
      x: w * (0.12 + Math.random() * 0.76),
      y: h * (0.04 + Math.random() * 0.32),
      vx: dir * Math.cos(slope) * speed,
      vy: Math.sin(slope) * speed,
      tailLength: 85 + Math.random() * 45,
      elapsed: 0,
      duration: 0.75
    });
  }

  function measureGeometry() {
    if (!state.section) return;

    const sectionRect = state.section.getBoundingClientRect();
    const canvasRect = state.canvas ? state.canvas.getBoundingClientRect() : sectionRect;
    const stageRect = state.stage ? state.stage.getBoundingClientRect() : sectionRect;
    const viewportWidth = window.innerWidth ||
      (document.documentElement ? document.documentElement.clientWidth : 0) ||
      sectionRect.width ||
      1280;

    const refLeft = canvasRect.width > 0 ? canvasRect.left : sectionRect.left;
    const refTop = canvasRect.height > 0 ? canvasRect.top : sectionRect.top;

    const canvasWidth = Math.max(1, Math.round(canvasRect.width || sectionRect.width || viewportWidth));
    const canvasHeight = Math.max(1, Math.round(canvasRect.height || sectionRect.height || 640));
    const dpr = Math.min(window.devicePixelRatio || 1, 2);

    const stageWidth = stageRect.width > 0 ? stageRect.width : canvasWidth;
    const stageHeight = stageRect.height > 0 ? stageRect.height : Math.min(canvasHeight * 0.68, 480);
    const stageOffsetX = stageRect.width > 0 ? (stageRect.left - refLeft) : 0;
    const stageOffsetY = stageRect.height > 0 ? (stageRect.top - refTop) : ((canvasHeight - stageHeight) * 0.5);

    state.geo.canvasWidth = canvasWidth;
    state.geo.canvasHeight = canvasHeight;
    state.geo.stageWidth = stageWidth;
    state.geo.stageHeight = stageHeight;
    state.geo.stageOffsetX = stageOffsetX;
    state.geo.stageOffsetY = stageOffsetY;
    state.geo.dpr = dpr;
    state.geo.viewportWidth = viewportWidth;
    state.geo.isDesktop = viewportWidth >= 768;

    if (state.canvas) {
      const backingW = Math.round(canvasWidth * dpr);
      const backingH = Math.round(canvasHeight * dpr);
      if (state.canvas.width !== backingW || state.canvas.height !== backingH) {
        state.canvas.width = backingW;
        state.canvas.height = backingH;
      }
    }
  }

  function projectOrbits() {
    const isDesktop = state.geo.isDesktop;
    const stageWidth = state.geo.stageWidth;

    for (let i = 0; i < state.cans.length; i++) {
      const can = state.cans[i];
      const el = can.el;

      if (!isDesktop) {
        can.x = 0;
        can.y = 0;
        el.style.setProperty('--orbit-x', '0px');
        el.style.setProperty('--orbit-y', '0px');
        el.style.setProperty('--orbit-scale', '1');
        el.style.setProperty('--orbit-opacity', '1');
        el.style.setProperty('--orbit-bright', '1');
        el.style.setProperty('--orbit-z', '1');
        if (can.lastIsFront !== false) {
          el.classList.remove('is-front');
          can.lastIsFront = false;
        }
        continue;
      }

      const cfg = RING_CONFIG[can.ring] || RING_CONFIG[1];
      const rx = Math.max(120, stageWidth * cfg.rxFactor);
      const ry = cfg.ry;
      const sinA = Math.sin(can.angle);
      const cosA = Math.cos(can.angle);

      const x = cosA * rx;
      const y = sinA * ry;
      const depthNorm = (sinA + 1) * 0.5;
      const scale = 0.78 + depthNorm * 0.32;
      const opacity = 0.64 + depthNorm * 0.36;
      const bright = 0.72 + depthNorm * 0.38;
      const isFront = sinA >= 0;
      const z = isFront
        ? Math.round(22 + depthNorm * 8)
        : Math.round(6 + depthNorm * 8);

      can.x = x;
      can.y = y;

      el.style.setProperty('--orbit-x', x.toFixed(2) + 'px');
      el.style.setProperty('--orbit-y', y.toFixed(2) + 'px');
      el.style.setProperty('--orbit-scale', scale.toFixed(4));
      el.style.setProperty('--orbit-opacity', opacity.toFixed(3));
      el.style.setProperty('--orbit-bright', bright.toFixed(3));
      el.style.setProperty('--orbit-z', String(z));

      if (can.lastIsFront !== isFront) {
        el.classList.toggle('is-front', isFront);
        can.lastIsFront = isFront;
      }
    }
  }

  function drawStarfield(ctx, isAnimated) {
    const w = state.geo.canvasWidth;
    const h = state.geo.canvasHeight;
    const ar = Math.round(state.currentRgb[0]);
    const ag = Math.round(state.currentRgb[1]);
    const ab = Math.round(state.currentRgb[2]);

    const accentR = Math.round(ar * 0.6 + 255 * 0.4);
    const accentG = Math.round(ag * 0.6 + 255 * 0.4);
    const accentB = Math.round(ab * 0.6 + 255 * 0.4);

    for (let i = 0; i < state.stars.length; i++) {
      const s = state.stars[i];
      const px = s.nx * w - state.currentParallaxX * 36 * s.depth;
      const py = s.ny * h - state.currentParallaxY * 36 * s.depth;

      const twinkle = isAnimated
        ? (0.55 + 0.45 * Math.sin(s.twinklePhase + state.animTime * s.twinkleSpeed))
        : 0.85;
      const alpha = Math.max(0.08, Math.min(1, s.baseAlpha * twinkle));

      let colorPrefix = 'rgba(255, 255, 255, ';
      if (s.tintType === 'blue') {
        colorPrefix = 'rgba(190, 231, 255, ';
      } else if (s.tintType === 'accent') {
        colorPrefix = 'rgba(' + accentR + ', ' + accentG + ', ' + accentB + ', ';
      }

      ctx.fillStyle = colorPrefix + alpha.toFixed(3) + ')';
      ctx.beginPath();
      ctx.arc(px, py, s.radius, 0, Math.PI * 2);
      ctx.fill();

      if (s.hasSparkle && alpha > 0.42) {
        const arm = s.radius * 2.4;
        ctx.strokeStyle = colorPrefix + (alpha * 0.45).toFixed(3) + ')';
        ctx.lineWidth = 0.75;
        ctx.beginPath();
        ctx.moveTo(px - arm, py);
        ctx.lineTo(px + arm, py);
        ctx.moveTo(px, py - arm);
        ctx.lineTo(px, py + arm);
        ctx.stroke();
      }
    }
  }

  function drawShootingStars(ctx) {
    if (!state.shootingStars.length) return;

    ctx.save();
    ctx.lineCap = 'round';

    for (let i = state.shootingStars.length - 1; i >= 0; i--) {
      const m = state.shootingStars[i];
      const progress = m.elapsed / m.duration;
      if (progress >= 1) {
        state.shootingStars.splice(i, 1);
        continue;
      }

      const fade = progress < 0.16
        ? (progress / 0.16)
        : Math.pow(Math.max(0, 1 - (progress - 0.16) / 0.84), 1.4);

      const speed = Math.hypot(m.vx, m.vy) || 1;
      const ux = m.vx / speed;
      const uy = m.vy / speed;

      const hx = m.x + m.vx * m.elapsed;
      const hy = m.y + m.vy * m.elapsed;
      const tx = hx - ux * m.tailLength;
      const ty = hy - uy * m.tailLength;

      const grad = ctx.createLinearGradient(tx, ty, hx, hy);
      grad.addColorStop(0, 'rgba(255, 255, 255, 0)');
      grad.addColorStop(0.65, 'rgba(190, 231, 255, ' + (0.48 * fade).toFixed(3) + ')');
      grad.addColorStop(1, 'rgba(255, 255, 255, ' + (0.92 * fade).toFixed(3) + ')');

      ctx.strokeStyle = grad;
      ctx.lineWidth = 1.25;
      ctx.beginPath();
      ctx.moveTo(tx, ty);
      ctx.lineTo(hx, hy);
      ctx.stroke();

      ctx.fillStyle = 'rgba(255, 255, 255, ' + (0.95 * fade).toFixed(3) + ')';
      ctx.beginPath();
      ctx.arc(hx, hy, 1.5, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.restore();
  }

  function drawEnergyTether(ctx) {
    const can = state.selectedCan;
    if (!can || !state.geo.isDesktop || state.geo.stageWidth < 480) return;

    const cx = state.geo.stageOffsetX + state.geo.stageWidth * 0.5;
    const cy = state.geo.stageOffsetY + state.geo.stageHeight * 0.5;
    const tx = cx + can.x;
    const ty = cy + can.y;
    const dx = tx - cx;
    const dy = ty - cy;

    if (dx * dx + dy * dy < 4) return;

    const r = Math.round(state.currentRgb[0]);
    const g = Math.round(state.currentRgb[1]);
    const b = Math.round(state.currentRgb[2]);
    const dimAlpha = can.isDimmed ? 0.35 : 1;

    ctx.save();
    ctx.lineCap = 'round';

    // Layer 1: Outer bloom stroke
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(tx, ty);
    ctx.strokeStyle = 'rgba(' + r + ', ' + g + ', ' + b + ', ' + (0.18 * dimAlpha).toFixed(3) + ')';
    ctx.lineWidth = 6;
    ctx.stroke();

    // Layer 2: Sharp plasma core stroke with subtle accent tint
    const pr = Math.round(255 * 0.82 + r * 0.18);
    const pg = Math.round(255 * 0.82 + g * 0.18);
    const pb = Math.round(255 * 0.82 + b * 0.18);
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(tx, ty);
    ctx.strokeStyle = 'rgba(' + pr + ', ' + pg + ', ' + pb + ', ' + (0.85 * dimAlpha).toFixed(3) + ')';
    ctx.lineWidth = 1.4;
    ctx.stroke();

    // Layer 3: 3 animated photon pulses travelling from core (cx, cy) to can (tx, ty)
    for (let p = 0; p < 3; p++) {
      const u = ((state.pulseTime * 0.55 + p / 3) % 1 + 1) % 1;
      const px = cx + dx * u;
      const py = cy + dy * u;
      const edgeFade = Math.sin(u * Math.PI) * dimAlpha;
      if (edgeFade <= 0.02) continue;

      ctx.fillStyle = 'rgba(' + r + ', ' + g + ', ' + b + ', ' + (0.45 * edgeFade).toFixed(3) + ')';
      ctx.beginPath();
      ctx.arc(px, py, 4.4, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = 'rgba(255, 255, 255, ' + (0.95 * edgeFade).toFixed(3) + ')';
      ctx.beginPath();
      ctx.arc(px, py, 1.85, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.restore();
  }

  function renderStaticFrame() {
    projectOrbits();

    if (!state.ctx) return;
    const ctx = state.ctx;
    const dpr = state.geo.dpr;

    state.currentRgb[0] = state.targetRgb[0];
    state.currentRgb[1] = state.targetRgb[1];
    state.currentRgb[2] = state.targetRgb[2];

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, state.geo.canvasWidth, state.geo.canvasHeight);
    drawStarfield(ctx, false);
    drawEnergyTether(ctx);
  }

  function shouldAnimate() {
    return Boolean(
      state.initialized &&
      !state.isPaused &&
      state.inViewport &&
      !document.hidden
    );
  }

  function stopLoop() {
    if (state.rafId) {
      window.cancelAnimationFrame(state.rafId);
      state.rafId = 0;
    }
    state.lastFrameTime = 0;
  }

  function tick(now) {
    state.rafId = 0;
    if (!shouldAnimate()) return;

    if (!state.lastFrameTime) {
      state.lastFrameTime = now;
    }
    const rawDt = (now - state.lastFrameTime) / 1000;
    const dt = Math.min(0.05, Math.max(0, rawDt));
    state.lastFrameTime = now;

    state.animTime += dt;
    state.pulseTime += dt;

    // Frame-rate independent lerp for active accent color and pointer parallax
    const colorLerp = 1 - Math.pow(1 - 0.1, dt * 60);
    for (let c = 0; c < 3; c++) {
      state.currentRgb[c] += (state.targetRgb[c] - state.currentRgb[c]) * colorLerp;
    }

    const parallaxLerp = 1 - Math.pow(1 - 0.1, dt * 60);
    state.currentParallaxX += (state.targetParallaxX - state.currentParallaxX) * parallaxLerp;
    state.currentParallaxY += (state.targetParallaxY - state.currentParallaxY) * parallaxLerp;

    // Shooting star scheduler (~3.5 - 6.5 seconds)
    state.nextMeteorIn -= dt;
    if (state.nextMeteorIn <= 0) {
      if (state.shootingStars.length < 2) {
        spawnShootingStar();
      }
      state.nextMeteorIn = 3.5 + Math.random() * 3.0;
    }

    for (let i = 0; i < state.shootingStars.length; i++) {
      state.shootingStars[i].elapsed += dt;
    }

    // Smooth hover/focus damping and 3D orbital integration on desktop (>= 768px)
    if (state.geo.isDesktop) {
      const targetMult = (state.hoveredEls.size > 0 || state.focusedEls.size > 0) ? 0 : 1;
      const dampLerp = 1 - Math.pow(1 - 0.12, dt * 60);
      state.speedMultiplier += (targetMult - state.speedMultiplier) * dampLerp;
      if (Math.abs(targetMult - state.speedMultiplier) < 0.001) {
        state.speedMultiplier = targetMult;
      }

      if (state.speedMultiplier > 0.0005) {
        for (let i = 0; i < state.cans.length; i++) {
          const can = state.cans[i];
          const cfg = RING_CONFIG[can.ring] || RING_CONFIG[1];
          can.angle += dt * cfg.speed * state.speedMultiplier;
        }
      }
    }

    projectOrbits();

    if (state.ctx) {
      const ctx = state.ctx;
      const dpr = state.geo.dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, state.geo.canvasWidth, state.geo.canvasHeight);
      drawStarfield(ctx, true);
      drawShootingStars(ctx);
      drawEnergyTether(ctx);
    }

    if (shouldAnimate()) {
      state.rafId = window.requestAnimationFrame(tick);
    }
  }

  function syncMotionToggleUi() {
    const paused = state.isPaused;
    if (state.section) {
      state.section.classList.toggle('is-paused', paused);
      state.section.classList.toggle('is-motion-paused', paused);
      state.section.dataset.cosmicPaused = paused ? 'true' : 'false';
    }

    const btn = state.motionToggle;
    if (!btn) return;

    const text = paused ? LABEL_PAUSED : LABEL_ACTIVE;
    const span = btn.querySelector('.cosmic-motion-label, span');
    if (span) {
      span.textContent = text;
    } else if (btn.children.length > 0) {
      let textNode = null;
      for (let i = 0; i < btn.childNodes.length; i++) {
        if (btn.childNodes[i].nodeType === 3 && btn.childNodes[i].nodeValue.trim().length > 0) {
          textNode = btn.childNodes[i];
          break;
        }
      }
      if (textNode) {
        textNode.nodeValue = ' ' + text;
      } else {
        btn.appendChild(document.createTextNode(' ' + text));
      }
    } else {
      btn.textContent = text;
    }
    btn.classList.toggle('is-paused', paused);
  }

  function syncLoopState() {
    syncMotionToggleUi();

    if (shouldAnimate()) {
      if (!state.rafId) {
        state.lastFrameTime = 0;
        state.rafId = window.requestAnimationFrame(tick);
      }
    } else {
      stopLoop();
      state.shootingStars = [];
      if (!document.hidden && state.initialized) {
        renderStaticFrame();
      }
    }
  }

  function selectCan(canId) {
    if (!state.section || !state.cans.length) return false;

    const targetId = String(canId || '');
    const can = state.canMap.get(targetId);
    if (!can) return false;

    state.selectedCan = can;

    for (let i = 0; i < state.cans.length; i++) {
      const item = state.cans[i];
      item.el.classList.toggle('is-selected', item.id === can.id);
    }

    state.section.style.setProperty('--cosmic-rgb', can.rgb);
    state.section.style.setProperty('--cosmic-core-hex', can.coreHex);
    state.section.style.setProperty('--cosmic-halo-hex', can.haloHex);
    state.section.style.setProperty('--cosmic-deep-hex', can.deepHex);

    state.targetRgb[0] = can.rgbTuple[0];
    state.targetRgb[1] = can.rgbTuple[1];
    state.targetRgb[2] = can.rgbTuple[2];

    if (state.holoImg) {
      if (can.img) state.holoImg.setAttribute('src', can.img);
      state.holoImg.setAttribute('alt', can.title);
    }
    if (state.holoBrand) {
      state.holoBrand.textContent = can.brandLabel;
    }
    if (state.holoTitle) {
      state.holoTitle.textContent = can.title;
    }
    if (state.holoPrice) {
      state.holoPrice.textContent = can.price;
    }
    if (state.holoDetailLink && can.href) {
      state.holoDetailLink.setAttribute('href', can.href);
    }
    if (state.holoShelfBtn) {
      state.holoShelfBtn.dataset.sectionTarget = can.sectionTarget;
      state.holoShelfBtn.setAttribute('data-section-target', can.sectionTarget);
    }

    if (!shouldAnimate()) {
      renderStaticFrame();
    }

    return can.id;
  }

  function setFilter(filterVal) {
    if (!state.section) return 'all';

    const nextFilter = String(filterVal || 'all').trim().toLowerCase() || 'all';
    state.activeFilter = nextFilter;
    state.section.dataset.activeSystem = nextFilter;

    for (let i = 0; i < state.filterButtons.length; i++) {
      const btn = state.filterButtons[i];
      const btnVal = String(btn.dataset.filter || btn.dataset.brand || btn.dataset.system || 'all').toLowerCase();
      const isMatch = btnVal === nextFilter;
      btn.classList.toggle('is-active', isMatch);
    }

    let firstMatch = null;
    for (let i = 0; i < state.cans.length; i++) {
      const can = state.cans[i];
      const matches = nextFilter === 'all' || can.brand === nextFilter;
      can.isDimmed = !matches;
      can.el.classList.toggle('is-dimmed', !matches);
      if (matches && !firstMatch) {
        firstMatch = can;
      }
    }

    if (firstMatch && (!state.selectedCan || (nextFilter !== 'all' && state.selectedCan.brand !== nextFilter))) {
      selectCan(firstMatch.id);
    } else if (!shouldAnimate()) {
      renderStaticFrame();
    }

    return nextFilter;
  }

  function toggleMotion(forceRunning) {
    if (typeof forceRunning === 'boolean') {
      state.isPaused = !forceRunning;
    } else {
      state.isPaused = !state.isPaused;
    }

    safeWriteStorage(STORAGE_KEY_PAUSED, state.isPaused ? '1' : '0');
    syncLoopState();
    return !state.isPaused;
  }

  function navigateWithWarp(href) {
    if (!href || state.isWarping) return;

    if (state.reducedMotion || !state.warpFlash) {
      window.location.href = href;
      return;
    }

    state.isWarping = true;
    state.warpFlash.classList.add('is-warping');

    clearTrackedTimer(state.warpTimer);
    state.warpTimer = setTrackedTimer(function () {
      state.warpTimer = 0;
      if (state.warpFlash) {
        state.warpFlash.classList.remove('is-warping');
      }
      state.isWarping = false;
      window.location.href = href;
    }, WARP_DURATION_MS);
  }

  function isPrimaryPlainClick(e) {
    if (!e) return true;
    if (typeof e.button === 'number' && e.button !== 0) return false;
    return !(e.metaKey || e.ctrlKey || e.shiftKey || e.altKey);
  }

  function handleCanClick(can, e) {
    if (!isPrimaryPlainClick(e)) return;

    const isDesktop = (window.innerWidth || state.geo.viewportWidth) >= 768;
    if (isDesktop) {
      if (e && typeof e.preventDefault === 'function') e.preventDefault();
      if (state.selectedCan !== can) {
        selectCan(can.id);
      }
      navigateWithWarp(can.href);
      return;
    }

    // Mobile (< 768px): first tap selects and updates Hologram Card; second tap navigates
    if (e && typeof e.preventDefault === 'function') e.preventDefault();

    const now = Date.now();
    const recentTouch = state.lastTouchTap.canId === can.id && (now - state.lastTouchTap.time) < 700;
    const alreadySelected = recentTouch
      ? state.lastTouchTap.wasSelected
      : (state.selectedCan === can && can.el.classList.contains('is-selected'));

    state.lastTouchTap.canId = null;

    if (!alreadySelected) {
      selectCan(can.id);
      return;
    }

    navigateWithWarp(can.href);
  }

  function bindEvents() {
    // Pointer parallax & 460px volumetric torch inside #cosmic-universe-intro
    trackListener(state.section, 'pointermove', function (e) {
      if (e && e.pointerType === 'touch') return;
      if (!state.pointerFine && e && e.pointerType && e.pointerType !== 'mouse' && e.pointerType !== 'pen') return;

      const rect = state.section.getBoundingClientRect();
      if (rect.width <= 0 || rect.height <= 0) return;

      const rx = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
      const ry = Math.max(0, Math.min(1, (e.clientY - rect.top) / rect.height));

      state.targetParallaxX = rx - 0.5;
      state.targetParallaxY = ry - 0.5;
      state.section.style.setProperty('--torch-x', (rx * 100).toFixed(2) + '%');
      state.section.style.setProperty('--torch-y', (ry * 100).toFixed(2) + '%');
    }, { passive: true });

    trackListener(state.section, 'pointerleave', function () {
      state.targetParallaxX = 0;
      state.targetParallaxY = 0;
      state.hoveredEls.clear();
    }, { passive: true });

    // Planet can interactions (hover/focus select + smooth damping + click/warp)
    for (let i = 0; i < state.cans.length; i++) {
      (function (can) {
        const el = can.el;

        trackListener(el, 'pointerdown', function (e) {
          if (e && e.pointerType === 'touch') {
            state.lastTouchTap = {
              canId: can.id,
              wasSelected: state.selectedCan === can && el.classList.contains('is-selected'),
              time: Date.now()
            };
          }
        }, { passive: true });

        trackListener(el, 'pointerenter', function (e) {
          if (e && e.pointerType === 'touch') return;
          state.hoveredEls.add(el);
          selectCan(can.id);
        }, { passive: true });

        trackListener(el, 'pointerleave', function () {
          state.hoveredEls.delete(el);
        }, { passive: true });

        trackListener(el, 'focus', function () {
          state.focusedEls.add(el);
          selectCan(can.id);
        });

        trackListener(el, 'blur', function () {
          state.focusedEls.delete(el);
        });

        trackListener(el, 'click', function (e) {
          handleCanClick(can, e);
        });

        if (el.tagName !== 'BUTTON' && el.tagName !== 'A') {
          trackListener(el, 'keydown', function (e) {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              handleCanClick(can, e);
            }
          });
        }
      })(state.cans[i]);
    }

    // Hover/focus damping on Hologram Inspector Card
    if (state.holoCard) {
      trackListener(state.holoCard, 'pointerenter', function (e) {
        if (e && e.pointerType === 'touch') return;
        state.hoveredEls.add(state.holoCard);
      }, { passive: true });

      trackListener(state.holoCard, 'pointerleave', function () {
        state.hoveredEls.delete(state.holoCard);
      }, { passive: true });

      trackListener(state.holoCard, 'focusin', function () {
        state.focusedEls.add(state.holoCard);
      });

      trackListener(state.holoCard, 'focusout', function (e) {
        if (!e.relatedTarget || !state.holoCard.contains(e.relatedTarget)) {
          state.focusedEls.delete(state.holoCard);
        }
      });
    }

    // Hologram Detail Link: 180ms warp flash then navigate
    if (state.holoDetailLink) {
      trackListener(state.holoDetailLink, 'click', function (e) {
        if (!isPrimaryPlainClick(e)) return;
        const href = state.holoDetailLink.getAttribute('href') || (state.selectedCan ? state.selectedCan.href : '');
        if (!href) return;
        e.preventDefault();
        navigateWithWarp(href);
      });
    }

    // Hologram Shelf Button: scroll smoothly to brand section
    if (state.holoShelfBtn) {
      trackListener(state.holoShelfBtn, 'click', function (e) {
        const targetId = state.holoShelfBtn.dataset.sectionTarget ||
          state.holoShelfBtn.getAttribute('data-section-target') ||
          (state.selectedCan ? state.selectedCan.sectionTarget : '');
        if (!targetId) return;

        if (typeof window.handleNavBrandClick === 'function') {
          window.handleNavBrandClick(e, state.holoShelfBtn, targetId);
          return;
        }

        if (e && typeof e.preventDefault === 'function') e.preventDefault();
        const targetEl = document.getElementById(targetId);
        if (targetEl && typeof targetEl.scrollIntoView === 'function') {
          targetEl.scrollIntoView({
            behavior: state.reducedMotion ? 'auto' : 'smooth',
            block: 'start'
          });
        }
      });
    }

    // Dock Brand Filter Buttons
    for (let i = 0; i < state.filterButtons.length; i++) {
      (function (btn) {
        trackListener(btn, 'click', function () {
          const val = btn.dataset.filter || btn.dataset.brand || btn.dataset.system || 'all';
          setFilter(val);
        });
      })(state.filterButtons[i]);
    }

    // WCAG Motion Toggle Button (switches visible text label only)
    if (state.motionToggle) {
      trackListener(state.motionToggle, 'click', function () {
        toggleMotion();
      });
    }

    // Window blur / pointercancel safety cleanup for hover & focus states
    trackListener(window, 'blur', function () {
      state.hoveredEls.clear();
      state.focusedEls.clear();
    });

    // Clear warp overlay if user navigates back via bfcache
    trackListener(window, 'pageshow', function () {
      state.isWarping = false;
      clearTrackedTimer(state.warpTimer);
      state.warpTimer = 0;
      if (state.warpFlash) {
        state.warpFlash.classList.remove('is-warping');
      }
    });

    // Tab visibility auto-sleep
    trackListener(document, 'visibilitychange', function () {
      syncLoopState();
    });

    // ResizeObserver on .cosmic-universe-section and .cosmic-solar-stage (cached geometry)
    function handleResizeUpdate() {
      measureGeometry();
      if (shouldAnimate()) {
        projectOrbits();
      } else {
        renderStaticFrame();
      }
    }

    if (typeof window.ResizeObserver === 'function') {
      const ro = trackObserver(new window.ResizeObserver(handleResizeUpdate));
      ro.observe(state.section);
      if (state.stage && state.stage !== state.section) {
        ro.observe(state.stage);
      }
    }
    trackListener(window, 'resize', handleResizeUpdate, { passive: true });

    // Viewport auto-sleep via IntersectionObserver
    if (typeof window.IntersectionObserver === 'function') {
      const io = trackObserver(new window.IntersectionObserver(function (entries) {
        if (!entries || !entries.length) return;
        let visible = false;
        for (let i = 0; i < entries.length; i++) {
          if (entries[i].isIntersecting) {
            visible = true;
            break;
          }
        }
        if (state.inViewport !== visible) {
          state.inViewport = visible;
          syncLoopState();
        }
      }, { threshold: 0.01 }));
      io.observe(state.section);
    }

    // Live prefers-reduced-motion media query listener
    if (typeof window.matchMedia === 'function') {
      const mqReduced = window.matchMedia('(prefers-reduced-motion: reduce)');
      const onReducedChange = function (e) {
        state.reducedMotion = Boolean(e && e.matches);
        if (state.reducedMotion) {
          state.isPaused = true;
        }
        syncLoopState();
      };
      if (typeof mqReduced.addEventListener === 'function') {
        trackListener(mqReduced, 'change', onReducedChange);
      } else if (typeof mqReduced.addListener === 'function') {
        mqReduced.addListener(onReducedChange);
        state.cleanups.push(function () {
          mqReduced.removeListener(onReducedChange);
        });
      }

      const mqFine = window.matchMedia('(pointer: fine)');
      const onFineChange = function (e) {
        state.pointerFine = Boolean(e && e.matches);
      };
      if (typeof mqFine.addEventListener === 'function') {
        trackListener(mqFine, 'change', onFineChange);
      } else if (typeof mqFine.addListener === 'function') {
        mqFine.addListener(onFineChange);
        state.cleanups.push(function () {
          mqFine.removeListener(onFineChange);
        });
      }
    }
  }

  function init() {
    if (window.__ENERGY_COSMIC_INIT__) {
      return window.EnergyCosmicUniverse;
    }

    const section = document.getElementById('cosmic-universe-intro') ||
      document.querySelector('.cosmic-universe-section');
    if (!section) {
      return window.EnergyCosmicUniverse;
    }

    window.__ENERGY_COSMIC_INIT__ = true;
    state.section = section;
    state.stage = section.querySelector('.cosmic-solar-stage');
    state.canvas = document.getElementById('cosmic-space-canvas');
    state.ctx = (state.canvas && typeof state.canvas.getContext === 'function')
      ? state.canvas.getContext('2d')
      : null;
    state.warpFlash = document.getElementById('cosmic-warp-flash');
    state.holoCard = document.getElementById('cosmic-holo-card');
    state.holoImg = document.getElementById('cosmic-holo-img');
    state.holoBrand = document.getElementById('cosmic-holo-brand');
    state.holoTitle = document.getElementById('cosmic-holo-title');
    state.holoPrice = document.getElementById('cosmic-holo-price');
    state.holoDetailLink = document.getElementById('cosmic-holo-detail-link');
    state.holoShelfBtn = document.getElementById('cosmic-holo-shelf-btn');
    state.motionToggle = document.getElementById('cosmic-motion-toggle');
    state.filterButtons = Array.prototype.slice.call(section.querySelectorAll('.cosmic-filter-btn'));

    state.pointerFine = detectPointerFine();
    state.reducedMotion = detectReducedMotion();
    const storedPaused = safeReadStorage(STORAGE_KEY_PAUSED) === '1';
    state.isPaused = state.reducedMotion || storedPaused;
    state.inViewport = true;
    state.speedMultiplier = 1;
    state.hoveredEls.clear();
    state.focusedEls.clear();
    state.shootingStars = [];
    state.nextMeteorIn = 1.8 + Math.random() * 2.2;
    state.targetParallaxX = 0;
    state.targetParallaxY = 0;
    state.currentParallaxX = 0;
    state.currentParallaxY = 0;

    state.section.style.setProperty('--torch-x', '50%');
    state.section.style.setProperty('--torch-y', '45%');

    const canNodes = section.querySelectorAll('.cosmic-planet-can');
    state.cans = [];
    state.canMap.clear();
    let initialCan = null;

    for (let i = 0; i < canNodes.length; i++) {
      const can = parseCanData(canNodes[i], i);
      state.cans.push(can);
      state.canMap.set(can.id, can);
      if (!initialCan && canNodes[i].classList.contains('is-selected')) {
        initialCan = can;
      }
    }
    if (!initialCan && state.cans.length > 0) {
      initialCan = state.cans[0];
    }

    const activeFilterBtn = section.querySelector('.cosmic-filter-btn.is-active');
    const initialFilter = activeFilterBtn
      ? String(activeFilterBtn.dataset.filter || activeFilterBtn.dataset.brand || 'all').toLowerCase()
      : String(section.dataset.activeSystem || 'all').toLowerCase();

    generateStars();
    measureGeometry();

    if (initialCan) {
      state.currentRgb[0] = initialCan.rgbTuple[0];
      state.currentRgb[1] = initialCan.rgbTuple[1];
      state.currentRgb[2] = initialCan.rgbTuple[2];
      selectCan(initialCan.id);
    }

    setFilter(initialFilter);
    projectOrbits();
    bindEvents();
    state.initialized = true;
    syncLoopState();

    return window.EnergyCosmicUniverse;
  }

  function destroy() {
    stopLoop();

    for (let i = state.cleanups.length - 1; i >= 0; i--) {
      try {
        state.cleanups[i]();
      } catch (err) {
        /* ignore cleanup errors */
      }
    }
    state.cleanups = [];

    for (let i = 0; i < state.observers.length; i++) {
      try {
        state.observers[i].disconnect();
      } catch (err) {
        /* ignore observer disconnect errors */
      }
    }
    state.observers = [];

    state.timers.forEach(function (id) {
      window.clearTimeout(id);
    });
    state.timers.clear();

    if (state.warpFlash) {
      state.warpFlash.classList.remove('is-warping');
    }

    if (state.ctx && state.geo.canvasWidth > 0 && state.geo.canvasHeight > 0) {
      state.ctx.setTransform(state.geo.dpr, 0, 0, state.geo.dpr, 0, 0);
      state.ctx.clearRect(0, 0, state.geo.canvasWidth, state.geo.canvasHeight);
    }

    state.hoveredEls.clear();
    state.focusedEls.clear();
    state.cans = [];
    state.canMap.clear();
    state.selectedCan = null;
    state.stars = [];
    state.shootingStars = [];
    state.filterButtons = [];
    state.section = null;
    state.stage = null;
    state.canvas = null;
    state.ctx = null;
    state.warpFlash = null;
    state.holoCard = null;
    state.holoImg = null;
    state.holoBrand = null;
    state.holoTitle = null;
    state.holoPrice = null;
    state.holoDetailLink = null;
    state.holoShelfBtn = null;
    state.motionToggle = null;
    state.isWarping = false;
    state.warpTimer = 0;
    state.initialized = false;
    window.__ENERGY_COSMIC_INIT__ = false;
  }

  window.EnergyCosmicUniverse = {
    init: init,
    selectCan: selectCan,
    setFilter: setFilter,
    toggleMotion: toggleMotion,
    destroy: destroy
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})(window, document);
