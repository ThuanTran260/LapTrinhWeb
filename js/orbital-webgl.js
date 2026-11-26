/**
 * ENERGY BOOST STORE — ORBITAL TELEMETRY 2026 WEBGL2 / CANVAS2D ENGINE
 * Dual-mode fullscreen shader engine for Hero Space (#orbital-space-canvas)
 * and Product Detail Halo (#orbital-detail-canvas).
 *
 * Fallback Chain:
 *   1. OGL 1.0.11 WebGL2/WebGL1 ESM (https://cdn.jsdelivr.net/npm/ogl@1.0.11/+esm)
 *   2. Inline zero-dependency Raw WebGL2/WebGL1 fullscreen-triangle GLSL runner
 *   3. Lightweight Canvas2D radial nebula, corona & starfield fallback
 *
 * Strictly offline/file:// safe, zero unhandled rejections, dpr <= 1.75,
 * off-screen IntersectionObserver + visibilitychange RAF pausing,
 * and WCAG prefers-reduced-motion static frame support.
 */
(function (window, document) {
  'use strict';

  if (typeof window === 'undefined' || typeof document === 'undefined') {
    return;
  }

  const OGL_CDN_URL = 'https://cdn.jsdelivr.net/npm/ogl@1.0.11/+esm';
  const OGL_IMPORT_TIMEOUT_MS = 2200;
  const MAX_DPR = 1.75;
  const COLOR_LERP_PER_FRAME = 0.07;
  const MOUSE_LERP_PER_FRAME = 0.075;
  const DEFAULT_WARP_INTENSITY = 0.85;

  // Linearized lush HDR-balanced RGB floats in [0..1] for GLSL
  const SPECTRAL_PALETTES = {
    monster: {
      a: [0.22, 1.00, 0.08],
      b: [0.00, 0.88, 0.72]
    },
    redbull: {
      a: [1.00, 0.72, 0.00],
      b: [1.00, 0.34, 0.05]
    },
    sting: {
      a: [1.00, 0.16, 0.43],
      b: [0.18, 0.65, 1.00]
    }
  };

  // WebGL1 (#version 100) compatible vertex shader matching OGL Triangle(gl) attributes
  const VERTEX_SHADER = [
    'precision highp float;',
    'attribute vec2 position;',
    'attribute vec2 uv;',
    'varying vec2 vUv;',
    'void main() {',
    '  vUv = uv;',
    '  gl_Position = vec4(position, 0.0, 1.0);',
    '}'
  ].join('\n');

  // Shared GLSL noise & starfield helpers for both Hero and Detail shaders
  const GLSL_NOISE_HELPERS = [
    '#ifdef GL_FRAGMENT_PRECISION_HIGH',
    '  precision highp float;',
    '#else',
    '  precision mediump float;',
    '#endif',
    '',
    'varying vec2 vUv;',
    'uniform float uTime;',
    'uniform vec2 uResolution;',
    'uniform float uAspect;',
    'uniform vec2 uMouse;',
    'uniform vec3 uColorA;',
    'uniform vec3 uColorB;',
    'uniform float uWarp;',
    'uniform float uPixelRatio;',
    '',
    'float hash21(vec2 p) {',
    '  p = fract(p * vec2(123.34, 456.21));',
    '  p += dot(p, p + 45.32);',
    '  return fract(p.x * p.y);',
    '}',
    '',
    'float valueNoise(vec2 p) {',
    '  vec2 i = floor(p);',
    '  vec2 f = fract(p);',
    '  vec2 u = f * f * (3.0 - 2.0 * f);',
    '  float a = hash21(i);',
    '  float b = hash21(i + vec2(1.0, 0.0));',
    '  float c = hash21(i + vec2(0.0, 1.0));',
    '  float d = hash21(i + vec2(1.0, 1.0));',
    '  return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);',
    '}',
    '',
    'float fbm(vec2 p) {',
    '  float v = 0.0;',
    '  float amp = 0.5;',
    '  mat2 rot = mat2(0.80, -0.60, 0.60, 0.80);',
    '  for (int i = 0; i < 4; i++) {',
    '    v += amp * valueNoise(p);',
    '    p = rot * p * 2.03 + vec2(17.1, 31.7);',
    '    amp *= 0.5;',
    '  }',
    '  return v;',
    '}',
    '',
    'float starLayer(vec2 coord, float scale, float density, float phaseOffset) {',
    '  vec2 scaled = coord * scale;',
    '  vec2 gv = fract(scaled) - 0.5;',
    '  vec2 id = floor(scaled);',
    '  float rnd = hash21(id);',
    '  if (rnd < density) return 0.0;',
    '  vec2 offset = vec2(hash21(id + 13.7), hash21(id + 71.3)) - 0.5;',
    '  float d = length(gv - offset * 0.66);',
    '  float size = mix(0.020, 0.052, fract(rnd * 37.0));',
    '  float star = smoothstep(size, size * 0.12, d);',
    '  float twinkle = 0.64 + 0.36 * sin(uTime * (0.65 + fract(rnd * 19.0) * 1.15) + rnd * 6.2831 + phaseOffset);',
    '  return star * twinkle * smoothstep(density, 1.0, rnd);',
    '}'
  ].join('\n');

  const HERO_FRAGMENT_SHADER = [
    GLSL_NOISE_HELPERS,
    '',
    'void main() {',
    '  vec2 aspectScale = vec2(uAspect, 1.0);',
    '  vec2 c = uAspect >= 1.15 ? vec2(0.67, 0.50) : vec2(0.50, 0.36);',
    '  vec2 p = (vUv - c) * aspectScale;',
    '  vec2 m = (uMouse - c) * aspectScale;',
    '  float r = length(p);',
    '  float fit = mix(0.68, 1.0, smoothstep(0.45, 1.15, uAspect));',
    '  float ang = atan(p.y, p.x + 1e-5);',
    '',
    '  // Deep OLED void base #030508',
    '  vec3 col = vec3(0.012, 0.020, 0.032);',
    '',
    '  // 4-octave domain-warped fBM nebula clouds drifting at uTime * 0.08',
    '  float t = uTime * 0.08;',
    '  vec2 nebCoord = p * 2.15;',
    '  float n1 = fbm(nebCoord + vec2(t, -t * 0.62));',
    '  float n2 = fbm(nebCoord * 1.45 + vec2(n1 * 1.25 - t * 0.48, n1 * 0.85 + t * 0.36));',
    '  float cloud = smoothstep(0.25, 0.88, n2);',
    '',
    '  // Pointer illumination gently lights nearby nebula filaments',
    '  float ptrDist2 = dot(p - m, p - m);',
    '  float ptrLight = exp(-ptrDist2 * 5.2);',
    '  vec3 nebCol = mix(uColorB, uColorA, smoothstep(0.26, 0.78, n1));',
    '  nebCol = mix(nebCol, mix(uColorA, vec3(1.0), 0.25), ptrLight * 0.38);',
    '',
    '  // Restrain nebula intensity over editorial copy so WCAG AA text stays crisp',
    '  float readZone = uAspect >= 1.15 ? smoothstep(0.04, 0.62, vUv.x) : smoothstep(0.96, 0.42, vUv.y);',
    '  float radialEnv = exp(-r * 1.15);',
    '  float nebGain = (0.14 + 0.10 * radialEnv) * mix(0.56, 1.0, readZone) + ptrLight * 0.11;',
    '  col += nebCol * cloud * nebGain;',
    '',
    '  // Gravitational eclipse corona ring + warm inner core halo + warp ripple',
    '  float ringWave = sin(ang * 3.0 + uTime * 0.65) * 0.0035 + (n1 - 0.5) * 0.012;',
    '  float ringR = 0.235 * fit + ringWave + uWarp * 0.032 * sin(uTime * 9.0 - r * 22.0);',
    '  float dRing = abs(r - ringR);',
    '  float coronaCrisp = exp(-dRing * 92.0) * (0.58 + 0.22 * uWarp);',
    '  float coronaSoft = exp(-dRing * 17.0) * (0.20 + 0.14 * uWarp);',
    '  float outerRing = exp(-abs(r - ringR * 1.38) * 140.0) * (0.14 + 0.07 * sin(ang * 2.0 - uTime * 0.5));',
    '  float innerCore = exp(-r * 6.5) * (0.18 + 0.16 * uWarp);',
    '',
    '  float warpRadius = ringR + (1.0 - clamp(uWarp, 0.0, 1.2)) * 0.36;',
    '  float warpRipple = exp(-abs(r - warpRadius) * 44.0) * uWarp * 0.52;',
    '  float warpTrail = exp(-abs(r - (warpRadius - 0.035)) * 28.0) * uWarp * 0.26;',
    '',
    '  // Multi-depth procedural twinkling starfield occluded behind the eclipse core',
    '  float starOcclude = smoothstep(ringR * 0.38, ringR * 0.94, r);',
    '  vec2 starCoord = (vUv - 0.5) * aspectScale - (uMouse - 0.5) * 0.022;',
    '  float sFar = starLayer(starCoord, 26.0, 0.78, 0.0);',
    '  float sMid = starLayer(starCoord + vec2(4.3, 9.1), 13.5, 0.88, 2.1);',
    '  col += sFar * 0.52 * vec3(0.78, 0.86, 0.98) * starOcclude;',
    '  col += sMid * 0.82 * mix(vec3(0.92, 0.96, 1.0), uColorB, 0.28) * starOcclude;',
    '',
    '  vec3 coronaTint = mix(uColorA, uColorB, 0.42 + 0.42 * sin(ang * 2.0 - uTime * 0.4));',
    '  col += coronaTint * (coronaCrisp + coronaSoft + outerRing);',
    '  col += mix(uColorA, vec3(1.0), 0.36) * innerCore;',
    '  col += uColorA * warpRipple + uColorB * warpTrail;',
    '  col += mix(uColorA, vec3(1.0), 0.25) * ptrLight * 0.065;',
    '',
    '  col = col / (1.0 + max(col - 0.88, 0.0) * 0.45);',
    '  gl_FragColor = vec4(clamp(col, 0.0, 1.0), 1.0);',
    '}'
  ].join('\n');

  const DETAIL_FRAGMENT_SHADER = [
    GLSL_NOISE_HELPERS,
    '',
    'void main() {',
    '  vec2 aspectScale = vec2(uAspect, 1.0);',
    '  vec2 c = vec2(0.5, 0.5);',
    '  vec2 p = (vUv - c) * aspectScale;',
    '  vec2 m = (uMouse - c) * aspectScale;',
    '  float r = length(p);',
    '  float fit = min(uAspect, 1.0);',
    '  float ang = atan(p.y, p.x + 1e-5);',
    '',
    '  // Deep OLED chamber backdrop #030508',
    '  vec3 col = vec3(0.012, 0.020, 0.032);',
    '',
    '  // Subtle perimeter star dust behind the studio chamber',
    '  vec2 starCoord = (vUv - 0.5) * aspectScale - (uMouse - 0.5) * 0.015;',
    '  float sBg = starLayer(starCoord, 18.0, 0.86, 1.4);',
    '  col += sBg * 0.42 * vec3(0.80, 0.88, 0.98) * smoothstep(0.14 * fit, 0.42 * fit, r);',
    '',
    '  // Volumetric plasma mist framing the product can',
    '  float t = uTime * 0.08;',
    '  float n1 = fbm(p * 3.0 + vec2(t, -t * 0.55));',
    '  float n2 = fbm(p * 4.2 + vec2(n1 * 1.1 - t * 0.4, n1 * 0.7 + t * 0.3));',
    '  float mistEnv = exp(-r * 3.1 / max(fit, 0.45));',
    '  col += mix(uColorB, uColorA, n1) * smoothstep(0.22, 0.85, n2) * mistEnv * 0.32;',
    '',
    '  // Concentric orbital telemetry rings around center',
    '  float r1 = 0.22 * fit;',
    '  float r2 = 0.33 * fit + uWarp * 0.025 * sin(uTime * 10.0 - r * 20.0);',
    '  float r3 = 0.42 * fit;',
    '  float ring1 = exp(-abs(r - r1) * 110.0) * 0.26;',
    '  float ring2 = exp(-abs(r - r2) * 85.0) * (0.48 + 0.18 * uWarp) + exp(-abs(r - r2) * 18.0) * 0.16;',
    '  float ring3 = exp(-abs(r - r3) * 130.0) * 0.20 * (0.55 + 0.45 * smoothstep(-0.2, 0.6, sin(ang * 8.0 + uTime * 0.45)));',
    '',
    '  // Cursor-reactive directional rim highlight',
    '  float mLen = length(m);',
    '  vec2 mDir = mLen > 0.001 ? m / mLen : vec2(0.707, 0.707);',
    '  vec2 pDir = r > 0.001 ? p / r : vec2(0.0, 1.0);',
    '  float rimAlign = pow(max(dot(pDir, mDir), 0.0), 4.0) * min(mLen * 3.5, 1.0);',
    '  float rimBand = exp(-abs(r - r2) * 28.0) * rimAlign;',
    '  float ptrGlow = exp(-dot(p - m, p - m) * 7.5);',
    '',
    '  vec3 ringTint = mix(uColorA, uColorB, 0.45 + 0.45 * sin(ang * 2.0 - uTime * 0.5));',
    '  col += ringTint * (ring1 + ring2 + ring3);',
    '  col += mix(uColorA, vec3(1.0), 0.36) * rimBand * 0.42;',
    '  col += mix(uColorB, uColorA, 0.5) * ptrGlow * 0.14;',
    '  col += uColorA * exp(-r * 6.0 / max(fit, 0.45)) * (0.14 + 0.12 * uWarp);',
    '',
    '  float vig = smoothstep(0.88, 0.26, length(vUv - 0.5));',
    '  col = mix(vec3(0.012, 0.020, 0.032), col, 0.35 + 0.65 * vig);',
    '  col = col / (1.0 + max(col - 0.88, 0.0) * 0.45);',
    '  gl_FragColor = vec4(clamp(col, 0.0, 1.0), 1.0);',
    '}'
  ].join('\n');

  let cachedOgl = null;
  let oglLoadPromise = null;

  function clamp(value, min, max) {
    return Math.min(max, Math.max(min, value));
  }

  function lerp(a, b, t) {
    return a + (b - a) * t;
  }

  function normalizeSpectralKey(key) {
    const raw = String(key || '').trim().toLowerCase();
    if (SPECTRAL_PALETTES[raw]) return raw;
    if (raw.indexOf('redbull') !== -1 || raw.indexOf('solar') !== -1) return 'redbull';
    if (raw.indexOf('sting') !== -1 || raw.indexOf('pulsar') !== -1) return 'sting';
    return 'monster';
  }

  function getInitialSpectralKey() {
    const attr = document.documentElement
      ? document.documentElement.getAttribute('data-spectral')
      : '';
    return normalizeSpectralKey(attr || 'monster');
  }

  function detectReducedMotion() {
    try {
      if (typeof window.matchMedia === 'function') {
        return Boolean(window.matchMedia('(prefers-reduced-motion: reduce)').matches);
      }
    } catch (err) {
      /* ignore matchMedia failures */
    }
    return false;
  }

  function getTargetDpr() {
    return Math.min(window.devicePixelRatio || 1, MAX_DPR);
  }

  const initialKey = getInitialSpectralKey();
  const initialPalette = SPECTRAL_PALETTES[initialKey];

  const globalState = {
    spectralKey: initialKey,
    explicitSpectral: false,
    targetColorA: initialPalette.a.slice(),
    targetColorB: initialPalette.b.slice(),
    reducedMotion: detectReducedMotion(),
    hiddenByTab: document.visibilityState === 'hidden',
    instances: new Map(),
    sharedBound: false,
    sharedCleanups: []
  };

  function resolveCanvas(target, fallbackId) {
    if (target && typeof target.getContext === 'function') {
      return target;
    }
    if (typeof target === 'string') {
      return document.querySelector(target);
    }
    if (!target && fallbackId) {
      return document.getElementById(fallbackId);
    }
    return null;
  }

  function measureCanvasBox(canvas) {
    const parent = canvas.parentElement;
    const canvasRect = canvas.getBoundingClientRect();
    const parentRect = parent ? parent.getBoundingClientRect() : null;
    let width = canvasRect.width || (parentRect ? parentRect.width : 0) || window.innerWidth || 1280;
    let height = canvasRect.height || (parentRect ? parentRect.height : 0) || window.innerHeight || 720;

    if (parentRect && parentRect.width > 0 && parentRect.height > 0) {
      let cs = null;
      try {
        cs = window.getComputedStyle ? window.getComputedStyle(canvas) : null;
      } catch (err) {
        cs = null;
      }
      if (!cs || cs.position === 'absolute' || cs.position === 'fixed' || cs.width === '100%') {
        width = parentRect.width;
        height = parentRect.height;
      }
    }

    return {
      width: Math.max(1, Math.round(width)),
      height: Math.max(1, Math.round(height))
    };
  }

  // Keep responsive CSS layout intact when canvas is positioned inset:0; avoid locking stale px width on resize.
  function syncCanvasCssLayout(canvas, width, height) {
    let cs = null;
    try {
      cs = window.getComputedStyle ? window.getComputedStyle(canvas) : null;
    } catch (err) {
      cs = null;
    }
    if (cs && (cs.position === 'absolute' || cs.position === 'fixed')) {
      canvas.style.width = '';
      canvas.style.height = '';
    } else {
      canvas.style.width = width + 'px';
      canvas.style.height = height + 'px';
      canvas.style.maxWidth = '100%';
    }
  }

  // Async ESM loader for OGL with strict timeout & caught rejection guarantee
  function loadOGL() {
    if (cachedOgl) {
      return Promise.resolve(cachedOgl);
    }
    if (oglLoadPromise) {
      return oglLoadPromise;
    }
    if (typeof navigator !== 'undefined' && navigator.onLine === false) {
      return Promise.resolve(null);
    }

    oglLoadPromise = new Promise(function (resolve) {
      let settled = false;
      let timerId = 0;

      function finish(mod) {
        if (settled) return;
        settled = true;
        if (timerId) {
          window.clearTimeout(timerId);
          timerId = 0;
        }
        if (mod && mod.Renderer && mod.Triangle && mod.Program && mod.Mesh) {
          cachedOgl = mod;
          resolve(mod);
        } else {
          resolve(null);
        }
      }

      timerId = window.setTimeout(function () {
        finish(null);
      }, OGL_IMPORT_TIMEOUT_MS);

      try {
        // Use indirect dynamic import so environments without ESM support still parse/fail gracefully
        const importPromise = import(OGL_CDN_URL);
        if (importPromise && typeof importPromise.then === 'function') {
          importPromise.then(
            function (mod) {
              finish(mod);
            },
            function () {
              finish(null);
            }
          );
        } else {
          finish(null);
        }
      } catch (err) {
        finish(null);
      }
    });

    return oglLoadPromise;
  }

  // ---------------------------------------------------------------------------
  // Backend 1: OGL WebGL2 / WebGL1
  // ---------------------------------------------------------------------------
  function createOGLBackend(ogl, instance, vertexSrc, fragmentSrc) {
    const canvas = instance.canvas;
    const dpr = getTargetDpr();
    let renderer;
    let gl;
    let geometry;
    let program;
    let mesh;

    try {
      renderer = new ogl.Renderer({
        canvas: canvas,
        alpha: true,
        antialias: true,
        dpr: dpr,
        powerPreference: 'high-performance'
      });
      gl = renderer && renderer.gl ? renderer.gl : null;
      if (!gl) return null;

      const uniforms = {
        uTime: { value: instance.time },
        uResolution: { value: new Float32Array([instance.width * dpr, instance.height * dpr]) },
        uAspect: { value: instance.aspect },
        uMouse: { value: new Float32Array([instance.mouseX, instance.mouseY]) },
        uColorA: { value: new Float32Array(instance.colorA) },
        uColorB: { value: new Float32Array(instance.colorB) },
        uWarp: { value: instance.currentWarp },
        uPixelRatio: { value: dpr }
      };

      geometry = new ogl.Triangle(gl);
      program = new ogl.Program(gl, {
        vertex: vertexSrc,
        fragment: fragmentSrc,
        uniforms: uniforms,
        depthTest: false,
        depthWrite: false
      });

      // Verify shaders compiled/linked cleanly if OGL exposed program handle
      if (program.program && !gl.getProgramParameter(program.program, gl.LINK_STATUS)) {
        if (typeof geometry.remove === 'function') geometry.remove();
        if (typeof program.remove === 'function') program.remove();
        return null;
      }

      mesh = new ogl.Mesh(gl, { geometry: geometry, program: program });

      const backend = {
        name: 'ogl',
        gl: gl,
        resize: function (width, height, nextDpr) {
          renderer.dpr = nextDpr;
          renderer.setSize(width, height);
          syncCanvasCssLayout(canvas, width, height);
          uniforms.uResolution.value[0] = canvas.width;
          uniforms.uResolution.value[1] = canvas.height;
          uniforms.uAspect.value = width / Math.max(height, 1);
          uniforms.uPixelRatio.value = nextDpr;
        },
        render: function (inst) {
          if (inst.contextLost) return;
          uniforms.uTime.value = inst.time;
          uniforms.uAspect.value = inst.aspect;
          uniforms.uMouse.value[0] = inst.mouseX;
          uniforms.uMouse.value[1] = inst.mouseY;
          uniforms.uColorA.value[0] = inst.colorA[0];
          uniforms.uColorA.value[1] = inst.colorA[1];
          uniforms.uColorA.value[2] = inst.colorA[2];
          uniforms.uColorB.value[0] = inst.colorB[0];
          uniforms.uColorB.value[1] = inst.colorB[1];
          uniforms.uColorB.value[2] = inst.colorB[2];
          uniforms.uWarp.value = inst.currentWarp;
          renderer.render({ scene: mesh });
        },
        destroy: function () {
          try {
            if (geometry && typeof geometry.remove === 'function') geometry.remove();
            if (program && typeof program.remove === 'function') program.remove();
          } catch (err) {
            /* ignore cleanup errors */
          }
        }
      };

      backend.resize(instance.width, instance.height, dpr);
      return backend;
    } catch (err) {
      return null;
    }
  }

  // ---------------------------------------------------------------------------
  // Backend 2: Raw WebGL2 / WebGL1 Fullscreen-Triangle Runner
  // ---------------------------------------------------------------------------
  function compileShader(gl, type, source) {
    const shader = gl.createShader(type);
    if (!shader) return null;
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      gl.deleteShader(shader);
      return null;
    }
    return shader;
  }

  function createRawWebGLBackend(instance, vertexSrc, fragmentSrc) {
    const canvas = instance.canvas;
    const ctxOpts = {
      alpha: true,
      antialias: true,
      powerPreference: 'high-performance',
      preserveDrawingBuffer: false
    };

    let gl = null;
    try {
      gl = canvas.getContext('webgl2', ctxOpts) ||
        canvas.getContext('webgl', ctxOpts) ||
        canvas.getContext('experimental-webgl', ctxOpts);
    } catch (err) {
      gl = null;
    }
    if (!gl) return null;

    const vs = compileShader(gl, gl.VERTEX_SHADER, vertexSrc);
    const fs = compileShader(gl, gl.FRAGMENT_SHADER, fragmentSrc);
    if (!vs || !fs) {
      if (vs) gl.deleteShader(vs);
      if (fs) gl.deleteShader(fs);
      return null;
    }

    const program = gl.createProgram();
    if (!program) {
      gl.deleteShader(vs);
      gl.deleteShader(fs);
      return null;
    }
    gl.attachShader(program, vs);
    gl.attachShader(program, fs);
    gl.linkProgram(program);

    gl.deleteShader(vs);
    gl.deleteShader(fs);

    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
      gl.deleteProgram(program);
      return null;
    }

    // Exact same clip-space fullscreen triangle as OGL Triangle(gl):
    // position [-1,-1], [3,-1], [-1,3] paired with uv = position * 0.5 + 0.5
    const interleaved = new Float32Array([
      -1, -1, 0, 0,
       3, -1, 2, 0,
      -1,  3, 0, 2
    ]);

    const vbo = gl.createBuffer();
    if (!vbo) {
      gl.deleteProgram(program);
      return null;
    }

    gl.bindBuffer(gl.ARRAY_BUFFER, vbo);
    gl.bufferData(gl.ARRAY_BUFFER, interleaved, gl.STATIC_DRAW);

    const aPos = gl.getAttribLocation(program, 'position');
    const aUv = gl.getAttribLocation(program, 'uv');

    const locs = {
      uTime: gl.getUniformLocation(program, 'uTime'),
      uResolution: gl.getUniformLocation(program, 'uResolution'),
      uAspect: gl.getUniformLocation(program, 'uAspect'),
      uMouse: gl.getUniformLocation(program, 'uMouse'),
      uColorA: gl.getUniformLocation(program, 'uColorA'),
      uColorB: gl.getUniformLocation(program, 'uColorB'),
      uWarp: gl.getUniformLocation(program, 'uWarp'),
      uPixelRatio: gl.getUniformLocation(program, 'uPixelRatio')
    };

    gl.disable(gl.DEPTH_TEST);
    gl.disable(gl.CULL_FACE);

    const backend = {
      name: 'webgl',
      gl: gl,
      resize: function (width, height, nextDpr) {
        canvas.width = Math.max(1, Math.round(width * nextDpr));
        canvas.height = Math.max(1, Math.round(height * nextDpr));
        syncCanvasCssLayout(canvas, width, height);
        gl.viewport(0, 0, canvas.width, canvas.height);
      },
      render: function (inst) {
        if (inst.contextLost) return;
        gl.useProgram(program);
        gl.bindBuffer(gl.ARRAY_BUFFER, vbo);
        if (aPos !== -1) {
          gl.enableVertexAttribArray(aPos);
          gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 16, 0);
        }
        if (aUv !== -1) {
          gl.enableVertexAttribArray(aUv);
          gl.vertexAttribPointer(aUv, 2, gl.FLOAT, false, 16, 8);
        }

        if (locs.uTime !== null) gl.uniform1f(locs.uTime, inst.time);
        if (locs.uResolution !== null) gl.uniform2f(locs.uResolution, canvas.width, canvas.height);
        if (locs.uAspect !== null) gl.uniform1f(locs.uAspect, inst.aspect);
        if (locs.uMouse !== null) gl.uniform2f(locs.uMouse, inst.mouseX, inst.mouseY);
        if (locs.uColorA !== null) gl.uniform3f(locs.uColorA, inst.colorA[0], inst.colorA[1], inst.colorA[2]);
        if (locs.uColorB !== null) gl.uniform3f(locs.uColorB, inst.colorB[0], inst.colorB[1], inst.colorB[2]);
        if (locs.uWarp !== null) gl.uniform1f(locs.uWarp, inst.currentWarp);
        if (locs.uPixelRatio !== null) gl.uniform1f(locs.uPixelRatio, inst.dpr);

        gl.drawArrays(gl.TRIANGLES, 0, 3);
      },
      destroy: function () {
        try {
          gl.deleteBuffer(vbo);
          gl.deleteProgram(program);
        } catch (err) {
          /* ignore cleanup errors */
        }
      }
    };

    backend.resize(instance.width, instance.height, instance.dpr);
    return backend;
  }

  // ---------------------------------------------------------------------------
  // Backend 3: Canvas2D Atmospheric Renderer Fallback
  // ---------------------------------------------------------------------------
  function rgbCss(tuple, alpha) {
    const r = Math.round(clamp(tuple[0], 0, 1) * 255);
    const g = Math.round(clamp(tuple[1], 0, 1) * 255);
    const b = Math.round(clamp(tuple[2], 0, 1) * 255);
    return 'rgba(' + r + ', ' + g + ', ' + b + ', ' + alpha.toFixed(3) + ')';
  }

  function createSeededStars(count) {
    const stars = [];
    let seed = 48271;
    function nextRand() {
      seed = (seed * 16807) % 2147483647;
      return (seed - 1) / 2147483646;
    }
    for (let i = 0; i < count; i++) {
      stars.push({
        x: nextRand(),
        y: nextRand(),
        radius: 0.55 + nextRand() * 1.35,
        depth: 0.35 + nextRand() * 0.65,
        phase: nextRand() * Math.PI * 2,
        speed: 0.6 + nextRand() * 1.1,
        tinted: nextRand() > 0.78
      });
    }
    return stars;
  }

  function createCanvas2DBackend(instance) {
    const canvas = instance.canvas;
    let ctx = null;
    try {
      ctx = canvas.getContext('2d');
    } catch (err) {
      ctx = null;
    }
    if (!ctx) return null;

    const isHero = instance.mode === 'hero';
    const stars = createSeededStars(isHero ? 92 : 34);

    const backend = {
      name: 'canvas2d',
      gl: null,
      resize: function (width, height, nextDpr) {
        canvas.width = Math.max(1, Math.round(width * nextDpr));
        canvas.height = Math.max(1, Math.round(height * nextDpr));
        syncCanvasCssLayout(canvas, width, height);
        ctx.setTransform(nextDpr, 0, 0, nextDpr, 0, 0);
      },
      render: function (inst) {
        const w = inst.width;
        const h = inst.height;
        const t = inst.time;
        const aspect = w / Math.max(h, 1);

        ctx.setTransform(inst.dpr, 0, 0, inst.dpr, 0, 0);

        // Deep OLED void base #030508
        ctx.fillStyle = '#030508';
        ctx.fillRect(0, 0, w, h);

        const cx = isHero ? (aspect >= 1.15 ? w * 0.67 : w * 0.50) : w * 0.50;
        // Convert GLSL UV center y (0=bottom, 0.36) to Canvas2D y (0=top, 0.64)
        const cy = isHero ? (aspect >= 1.15 ? h * 0.50 : h * 0.64) : h * 0.50;
        const minDim = Math.min(w, h);
        const baseR = isHero
          ? minDim * (aspect >= 1.15 ? 0.24 : 0.34)
          : minDim * 0.33;

        // Radial nebula clouds
        const driftX = Math.sin(t * 0.28) * minDim * 0.06;
        const driftY = Math.cos(t * 0.22) * minDim * 0.05;

        const nebA = ctx.createRadialGradient(
          cx - baseR * 0.45 + driftX,
          cy - baseR * 0.28 + driftY,
          baseR * 0.08,
          cx - baseR * 0.2 + driftX,
          cy,
          minDim * (isHero ? 0.72 : 0.62)
        );
        nebA.addColorStop(0, rgbCss(inst.colorA, isHero ? 0.20 : 0.24));
        nebA.addColorStop(0.5, rgbCss(inst.colorA, 0.07));
        nebA.addColorStop(1, 'rgba(3, 5, 8, 0)');
        ctx.fillStyle = nebA;
        ctx.fillRect(0, 0, w, h);

        const nebB = ctx.createRadialGradient(
          cx + baseR * 0.5 - driftX * 0.8,
          cy + baseR * 0.35 - driftY * 0.8,
          baseR * 0.06,
          cx + baseR * 0.2,
          cy,
          minDim * (isHero ? 0.68 : 0.56)
        );
        nebB.addColorStop(0, rgbCss(inst.colorB, isHero ? 0.18 : 0.20));
        nebB.addColorStop(0.52, rgbCss(inst.colorB, 0.06));
        nebB.addColorStop(1, 'rgba(3, 5, 8, 0)');
        ctx.fillStyle = nebB;
        ctx.fillRect(0, 0, w, h);

        // Pointer light glow
        const mx = inst.mouseX * w;
        const my = (1 - inst.mouseY) * h;
        const ptrGrad = ctx.createRadialGradient(mx, my, 0, mx, my, minDim * 0.34);
        ptrGrad.addColorStop(0, rgbCss(inst.colorA, 0.12));
        ptrGrad.addColorStop(0.55, rgbCss(inst.colorB, 0.04));
        ptrGrad.addColorStop(1, 'rgba(3, 5, 8, 0)');
        ctx.fillStyle = ptrGrad;
        ctx.fillRect(0, 0, w, h);

        // Twinkling deep-space stars
        const pxShift = (inst.mouseX - 0.5) * 14;
        const pyShift = ((1 - inst.mouseY) - 0.5) * 14;
        for (let i = 0; i < stars.length; i++) {
          const s = stars[i];
          const sx = ((s.x * w - pxShift * s.depth) % w + w) % w;
          const sy = ((s.y * h - pyShift * s.depth) % h + h) % h;
          const distFromCore = Math.hypot(sx - cx, sy - cy);
          if (isHero && distFromCore < baseR * 0.75) continue;
          if (!isHero && distFromCore < baseR * 0.48) continue;

          const twinkle = 0.45 + 0.55 * (0.5 + 0.5 * Math.sin(t * s.speed + s.phase));
          const alpha = (0.30 + s.depth * 0.55) * twinkle;
          ctx.fillStyle = s.tinted
            ? rgbCss(inst.colorB, alpha)
            : 'rgba(226, 238, 255, ' + alpha.toFixed(3) + ')';
          ctx.beginPath();
          ctx.arc(sx, sy, s.radius, 0, Math.PI * 2);
          ctx.fill();
        }

        // Inner warm core glow & orbital corona rings
        const coreGlow = ctx.createRadialGradient(cx, cy, baseR * 0.15, cx, cy, baseR * 1.15);
        coreGlow.addColorStop(0, rgbCss(inst.colorA, 0.14 + inst.currentWarp * 0.12));
        coreGlow.addColorStop(0.58, rgbCss(inst.colorB, 0.07));
        coreGlow.addColorStop(1, 'rgba(3, 5, 8, 0)');
        ctx.fillStyle = coreGlow;
        ctx.beginPath();
        ctx.arc(cx, cy, baseR * 1.15, 0, Math.PI * 2);
        ctx.fill();

        const ringR = baseR * (1 + inst.currentWarp * 0.04);
        ctx.save();
        ctx.lineWidth = isHero ? 1.6 : 1.5;
        ctx.strokeStyle = rgbCss(inst.colorA, 0.48 + inst.currentWarp * 0.25);
        ctx.beginPath();
        ctx.arc(cx, cy, ringR, 0, Math.PI * 2);
        ctx.stroke();

        ctx.lineWidth = 1;
        ctx.strokeStyle = rgbCss(inst.colorB, 0.22);
        ctx.beginPath();
        ctx.arc(cx, cy, ringR * (isHero ? 1.38 : 0.67), 0, Math.PI * 2);
        ctx.stroke();

        if (!isHero) {
          ctx.strokeStyle = rgbCss(inst.colorB, 0.18);
          ctx.beginPath();
          ctx.arc(cx, cy, ringR * 1.27, 0, Math.PI * 2);
          ctx.stroke();
        }

        if (inst.currentWarp > 0.01) {
          const warpR = ringR + (1 - clamp(inst.currentWarp, 0, 1.2)) * minDim * 0.28;
          ctx.lineWidth = 1.8;
          ctx.strokeStyle = rgbCss(inst.colorA, clamp(inst.currentWarp * 0.55, 0, 0.75));
          ctx.beginPath();
          ctx.arc(cx, cy, warpR, 0, Math.PI * 2);
          ctx.stroke();
        }
        ctx.restore();
      },
      destroy: function () {
        try {
          ctx.clearRect(0, 0, canvas.width, canvas.height);
        } catch (err) {
          /* ignore */
        }
      }
    };

    backend.resize(instance.width, instance.height, instance.dpr);
    return backend;
  }

  // ---------------------------------------------------------------------------
  // Instance Lifecycle, Loop Control & Shared Listeners
  // ---------------------------------------------------------------------------
  function stepInstanceState(instance, dt) {
    const frameScale = dt * 60;
    const colorAlpha = 1 - Math.pow(1 - COLOR_LERP_PER_FRAME, frameScale);
    const mouseAlpha = 1 - Math.pow(1 - MOUSE_LERP_PER_FRAME, frameScale);

    for (let i = 0; i < 3; i++) {
      instance.colorA[i] = lerp(instance.colorA[i], globalState.targetColorA[i], colorAlpha);
      instance.colorB[i] = lerp(instance.colorB[i], globalState.targetColorB[i], colorAlpha);
    }

    instance.mouseX = lerp(instance.mouseX, instance.targetMouseX, mouseAlpha);
    instance.mouseY = lerp(instance.mouseY, instance.targetMouseY, mouseAlpha);

    if (instance.targetWarp > 0.001 || instance.currentWarp > 0.001) {
      instance.targetWarp *= Math.pow(0.91, frameScale);
      if (instance.targetWarp < 0.001) instance.targetWarp = 0;
      const warpAlpha = 1 - Math.pow(1 - 0.22, frameScale);
      instance.currentWarp = lerp(instance.currentWarp, instance.targetWarp, warpAlpha);
      if (instance.currentWarp < 0.001 && instance.targetWarp === 0) {
        instance.currentWarp = 0;
      }
    }

    instance.time += dt;
  }

  function renderStaticFrame(instance) {
    if (instance.destroyed || instance.contextLost || !instance.backend) return;
    for (let i = 0; i < 3; i++) {
      instance.colorA[i] = globalState.targetColorA[i];
      instance.colorB[i] = globalState.targetColorB[i];
    }
    instance.currentWarp = 0;
    instance.targetWarp = 0;
    instance.backend.render(instance);
  }

  function stopInstanceLoop(instance) {
    if (instance.rafId) {
      window.cancelAnimationFrame(instance.rafId);
      instance.rafId = 0;
    }
    instance.lastFrameTime = 0;
  }

  function shouldAnimate(instance) {
    return (
      !instance.destroyed &&
      !instance.contextLost &&
      Boolean(instance.backend) &&
      !globalState.reducedMotion &&
      !globalState.hiddenByTab &&
      !instance.pausedByVisibility &&
      !instance.pausedByContentVisibility
    );
  }

  function syncInstanceLoop(instance) {
    if (!shouldAnimate(instance)) {
      stopInstanceLoop(instance);
      if (
        globalState.reducedMotion &&
        !instance.renderedStaticOnce &&
        instance.backend &&
        !instance.pausedByVisibility &&
        !globalState.hiddenByTab
      ) {
        instance.renderedStaticOnce = true;
        renderStaticFrame(instance);
      }
      return;
    }

    if (instance.rafId) return;

    instance.lastFrameTime = 0;
    function tick(now) {
      instance.rafId = 0;
      if (!shouldAnimate(instance)) return;

      const dt = instance.lastFrameTime
        ? clamp((now - instance.lastFrameTime) * 0.001, 0.001, 0.05)
        : 1 / 60;
      instance.lastFrameTime = now;

      stepInstanceState(instance, dt);
      instance.backend.render(instance);

      if (shouldAnimate(instance)) {
        instance.rafId = window.requestAnimationFrame(tick);
      }
    }

    instance.rafId = window.requestAnimationFrame(tick);
  }

  function resizeInstance(instance) {
    if (instance.destroyed || !instance.backend) return;
    const size = measureCanvasBox(instance.canvas);
    const dpr = getTargetDpr();
    if (
      size.width === instance.width &&
      size.height === instance.height &&
      dpr === instance.dpr
    ) {
      return;
    }
    instance.width = size.width;
    instance.height = size.height;
    instance.aspect = size.width / Math.max(size.height, 1);
    instance.dpr = dpr;
    instance.backend.resize(size.width, size.height, dpr);

    if (globalState.reducedMotion) {
      renderStaticFrame(instance);
    }
  }

  function bindSharedListeners() {
    if (globalState.sharedBound) return;
    globalState.sharedBound = true;

    function onVisibilityChange() {
      globalState.hiddenByTab = document.visibilityState === 'hidden';
      globalState.instances.forEach(function (inst) {
        syncInstanceLoop(inst);
      });
    }

    function onPointerMove(e) {
      if (!e || typeof e.clientX !== 'number' || typeof e.clientY !== 'number') return;
      globalState.instances.forEach(function (inst) {
        if (inst.destroyed || inst.pausedByVisibility || globalState.hiddenByTab) return;
        const rect = inst.canvas.getBoundingClientRect();
        if (rect.width <= 0 || rect.height <= 0) return;
        const nx = clamp((e.clientX - rect.left) / rect.width, 0, 1);
        // Invert Y to match WebGL vUv origin at bottom-left
        const ny = clamp(1 - (e.clientY - rect.top) / rect.height, 0, 1);
        inst.targetMouseX = nx;
        inst.targetMouseY = ny;
      });
    }

    function onResize() {
      globalState.instances.forEach(function (inst) {
        resizeInstance(inst);
      });
    }

    document.addEventListener('visibilitychange', onVisibilityChange);
    window.addEventListener('pointermove', onPointerMove, { passive: true });
    window.addEventListener('resize', onResize, { passive: true });

    globalState.sharedCleanups.push(function () {
      document.removeEventListener('visibilitychange', onVisibilityChange);
      window.removeEventListener('pointermove', onPointerMove);
      window.removeEventListener('resize', onResize);
    });

    if (typeof window.matchMedia === 'function') {
      const mqReduced = window.matchMedia('(prefers-reduced-motion: reduce)');
      const onReducedChange = function (ev) {
        globalState.reducedMotion = Boolean(ev && ev.matches);
        globalState.instances.forEach(function (inst) {
          inst.renderedStaticOnce = false;
          syncInstanceLoop(inst);
        });
      };
      if (typeof mqReduced.addEventListener === 'function') {
        mqReduced.addEventListener('change', onReducedChange);
        globalState.sharedCleanups.push(function () {
          mqReduced.removeEventListener('change', onReducedChange);
        });
      } else if (typeof mqReduced.addListener === 'function') {
        mqReduced.addListener(onReducedChange);
        globalState.sharedCleanups.push(function () {
          mqReduced.removeListener(onReducedChange);
        });
      }
    }
  }

  function unbindSharedListenersIfEmpty() {
    if (globalState.instances.size > 0 || !globalState.sharedBound) return;
    for (let i = globalState.sharedCleanups.length - 1; i >= 0; i--) {
      try {
        globalState.sharedCleanups[i]();
      } catch (err) {
        /* ignore cleanup errors */
      }
    }
    globalState.sharedCleanups = [];
    globalState.sharedBound = false;
  }

  function destroyInstance(instance) {
    if (!instance || instance.destroyed) return;
    instance.destroyed = true;
    stopInstanceLoop(instance);

    for (let i = instance.cleanups.length - 1; i >= 0; i--) {
      try {
        instance.cleanups[i]();
      } catch (err) {
        /* ignore cleanup errors */
      }
    }
    instance.cleanups = [];

    if (instance.backend) {
      instance.backend.destroy();
      instance.backend = null;
    }

    if (instance.canvas && instance.canvas.dataset) {
      delete instance.canvas.dataset.orbRenderer;
    }

    globalState.instances.delete(instance.canvas);
    unbindSharedListenersIfEmpty();
  }

  function attachInstanceObservers(instance) {
    const canvas = instance.canvas;

    function onContextLost(e) {
      if (e && typeof e.preventDefault === 'function') {
        e.preventDefault();
      }
      instance.contextLost = true;
      stopInstanceLoop(instance);
    }

    function onContextRestored() {
      instance.contextLost = false;
      instance.renderedStaticOnce = false;
      syncInstanceLoop(instance);
    }

    canvas.addEventListener('webglcontextlost', onContextLost, false);
    canvas.addEventListener('webglcontextrestored', onContextRestored, false);
    instance.cleanups.push(function () {
      canvas.removeEventListener('webglcontextlost', onContextLost, false);
      canvas.removeEventListener('webglcontextrestored', onContextRestored, false);
    });

    function onContentVisibilityChange(e) {
      instance.pausedByContentVisibility = Boolean(e && e.skipped);
      syncInstanceLoop(instance);
    }

    canvas.addEventListener('contentvisibilityautostatechange', onContentVisibilityChange);
    instance.cleanups.push(function () {
      canvas.removeEventListener('contentvisibilityautostatechange', onContentVisibilityChange);
    });

    if (typeof window.IntersectionObserver === 'function') {
      const io = new window.IntersectionObserver(
        function (entries) {
          for (let i = 0; i < entries.length; i++) {
            if (entries[i].target === canvas) {
              instance.pausedByVisibility = !entries[i].isIntersecting;
              syncInstanceLoop(instance);
            }
          }
        },
        { threshold: 0 }
      );
      io.observe(canvas);
      instance.cleanups.push(function () {
        io.disconnect();
      });
    }

    if (typeof window.ResizeObserver === 'function') {
      const ro = new window.ResizeObserver(function () {
        resizeInstance(instance);
      });
      ro.observe(canvas);
      if (canvas.parentElement) {
        ro.observe(canvas.parentElement);
      }
      instance.cleanups.push(function () {
        ro.disconnect();
      });
    }
  }

  function bootBackend(instance, oglModule) {
    if (instance.destroyed) return;

    const vertexSrc = VERTEX_SHADER;
    const fragmentSrc = instance.mode === 'detail'
      ? DETAIL_FRAGMENT_SHADER
      : HERO_FRAGMENT_SHADER;

    let backend = null;
    if (oglModule) {
      backend = createOGLBackend(oglModule, instance, vertexSrc, fragmentSrc);
    }
    if (!backend) {
      backend = createRawWebGLBackend(instance, vertexSrc, fragmentSrc);
    }
    if (!backend) {
      backend = createCanvas2DBackend(instance);
    }
    if (!backend) return;

    instance.backend = backend;
    instance.canvas.dataset.orbRenderer = backend.name;

    if (globalState.reducedMotion) {
      instance.renderedStaticOnce = true;
      renderStaticFrame(instance);
    } else {
      // Paint immediate first frame before next rAF so first paint is never blank
      backend.render(instance);
      syncInstanceLoop(instance);
    }
  }

  function initCanvasMode(canvasArg, mode, brandKeyOpt) {
    const fallbackId = mode === 'detail' ? 'orbital-detail-canvas' : 'orbital-space-canvas';
    const canvas = resolveCanvas(canvasArg, fallbackId);
    if (!canvas) return null;

    if (brandKeyOpt) {
      setSpectralSystem(brandKeyOpt);
    } else if (!globalState.explicitSpectral) {
      const domSpectral = document.documentElement
        ? document.documentElement.getAttribute('data-spectral')
        : '';
      if (domSpectral) {
        const resolvedDom = normalizeSpectralKey(domSpectral);
        const domPalette = SPECTRAL_PALETTES[resolvedDom];
        globalState.spectralKey = resolvedDom;
        globalState.targetColorA = domPalette.a.slice();
        globalState.targetColorB = domPalette.b.slice();
      }
    }

    const existing = globalState.instances.get(canvas);
    if (existing && !existing.destroyed) {
      if (existing.mode === mode) {
        resizeInstance(existing);
        return existing.controller;
      }
      destroyInstance(existing);
    }

    const box = measureCanvasBox(canvas);
    const defaultMouseX = mode === 'hero' && (box.width / Math.max(box.height, 1)) >= 1.15 ? 0.67 : 0.50;
    const defaultMouseY = mode === 'hero' && (box.width / Math.max(box.height, 1)) < 1.15 ? 0.36 : 0.50;

    const instance = {
      canvas: canvas,
      mode: mode,
      destroyed: false,
      contextLost: false,
      pausedByVisibility: false,
      pausedByContentVisibility: false,
      renderedStaticOnce: false,
      rafId: 0,
      lastFrameTime: 0,
      time: 0,
      width: box.width,
      height: box.height,
      aspect: box.width / Math.max(box.height, 1),
      dpr: getTargetDpr(),
      mouseX: defaultMouseX,
      mouseY: defaultMouseY,
      targetMouseX: defaultMouseX,
      targetMouseY: defaultMouseY,
      colorA: globalState.targetColorA.slice(),
      colorB: globalState.targetColorB.slice(),
      currentWarp: 0,
      targetWarp: 0,
      backend: null,
      cleanups: [],
      controller: null
    };

    instance.controller = {
      canvas: canvas,
      mode: mode,
      setSpectralSystem: setSpectralSystem,
      triggerWarp: triggerWarp,
      resize: function () {
        resizeInstance(instance);
      },
      destroy: function () {
        destroyInstance(instance);
      }
    };

    globalState.instances.set(canvas, instance);
    bindSharedListeners();
    attachInstanceObservers(instance);

    loadOGL().then(
      function (oglMod) {
        bootBackend(instance, oglMod);
      },
      function () {
        bootBackend(instance, null);
      }
    );

    return instance.controller;
  }

  // ---------------------------------------------------------------------------
  // Public API
  // ---------------------------------------------------------------------------
  function initHeroSpace(canvas) {
    return initCanvasMode(canvas, 'hero');
  }

  function initDetailHalo(canvas, brandKey) {
    return initCanvasMode(canvas, 'detail', brandKey);
  }

  function setSpectralSystem(brandKey) {
    const resolved = normalizeSpectralKey(brandKey);
    const palette = SPECTRAL_PALETTES[resolved];

    globalState.spectralKey = resolved;
    globalState.explicitSpectral = true;
    globalState.targetColorA = palette.a.slice();
    globalState.targetColorB = palette.b.slice();

    if (document.documentElement) {
      document.documentElement.setAttribute('data-spectral', resolved);
    }

    if (globalState.reducedMotion) {
      globalState.instances.forEach(function (inst) {
        if (!inst.pausedByVisibility && !globalState.hiddenByTab) {
          renderStaticFrame(inst);
        } else {
          inst.renderedStaticOnce = false;
        }
      });
    }

    return resolved;
  }

  function triggerWarp(intensity) {
    const amount = typeof intensity === 'number' && Number.isFinite(intensity)
      ? clamp(intensity, 0, 1.5)
      : DEFAULT_WARP_INTENSITY;

    if (globalState.reducedMotion || amount <= 0) {
      return 0;
    }

    globalState.instances.forEach(function (inst) {
      inst.targetWarp = Math.max(inst.targetWarp, amount);
      syncInstanceLoop(inst);
    });

    return amount;
  }

  function destroy(canvasOpt) {
    if (canvasOpt) {
      const target = resolveCanvas(canvasOpt);
      if (target && globalState.instances.has(target)) {
        destroyInstance(globalState.instances.get(target));
      }
      return;
    }

    const list = Array.from(globalState.instances.values());
    for (let i = 0; i < list.length; i++) {
      destroyInstance(list[i]);
    }
    globalState.instances.clear();
    unbindSharedListenersIfEmpty();
  }

  window.OrbitalWebGL = {
    initHeroSpace: initHeroSpace,
    initDetailHalo: initDetailHalo,
    setSpectralSystem: setSpectralSystem,
    triggerWarp: triggerWarp,
    destroy: destroy
  };

  function autoMount() {
    const heroCanvas = document.getElementById('orbital-space-canvas');
    if (heroCanvas) {
      initHeroSpace(heroCanvas);
    }
    const detailCanvas = document.getElementById('orbital-detail-canvas');
    if (detailCanvas) {
      const spectral = document.documentElement
        ? document.documentElement.getAttribute('data-spectral') || 'monster'
        : 'monster';
      initDetailHalo(detailCanvas, spectral);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', autoMount, { once: true });
  } else {
    autoMount();
  }
})(window, document);
