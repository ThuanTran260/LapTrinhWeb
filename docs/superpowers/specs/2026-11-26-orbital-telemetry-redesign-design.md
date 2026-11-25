# ENERGY BOOST STORE — Orbital Telemetry 2026 Full-Website Redesign Spec

- **Date:** 2026-11-26
- **Branch:** `feat/orbital-telemetry-redesign` (created from `main` at `1db60d9`)
- **Target Scope:** Full 28-page static HTML/CSS/JS redesign decomposed into 3 independent verifiable milestones:
  - **Phase 1 (Current Milestone — 7 Pages + Core Architecture):** `index.html`, 5× `pages/product-detail*.html`, `pages/search-results.html`, plus `css/orbital-tokens.css`, `css/orbital-storefront.css`, `js/orbital-webgl.js`, `js/orbital-motion.js`, surgical `js/app.js` bridge, and `scripts/verify_orbital_phase1.py`.
  - **Phase 2 (Next Milestone — 7 Transaction & Account Pages):** `cart.html`, `payment-gateway.html`, `order-success.html`, `orders.html`, `order-detail.html`, `account.html`, `login.html` (`Flight Manifest` 3-step stepper + `Airlock Access` login).
  - **Phase 3 (Final Milestone — 14 Admin Pages):** `admin/*.html` redesigned into `css/orbital-admin.css` (`Mission Control Cockpit` — zero WebGL overhead, high tabular density, `tabular-nums`, floating dropdowns outside overflow panels).

---

## 1. Design Direction & Aesthetic Calibration

- **Design Read:** *Spatial Telemetry Observatory meets Craft Beverage Showcase* — Obsidian OLED Void (`#030508`), recessed architectural hairlines (`rgba(255, 255, 255, 0.08)`), genuine product studio photography, honest web liquid-glass surface approximations, and a live spectral accent system that transforms both WebGL shaders and UI tokens across 3 flagship beverage systems:
  - **Monster Sector (`monster`):** `#39FF14` (Plasma Lime) / RGB `57, 255, 20` / Secondary `#00E0B8`
  - **Red Bull Solar (`redbull`):** `#FFB800` (Solar Amber) / RGB `255, 184, 0` / Secondary `#FF570D`
  - **Sting Pulsar (`sting`):** `#FF2A6D` (Crimson Pulsar) / RGB `255, 42, 109` / Secondary `#2EA6FF`
- **Dials:**
  - Storefront (Phase 1–2): `DESIGN_VARIANCE: 9` · `MOTION_INTENSITY: 8` · `VISUAL_DENSITY: 4`
  - Admin Cockpit (Phase 3): `DESIGN_VARIANCE: 3` · `MOTION_INTENSITY: 3` · `VISUAL_DENSITY: 7`
- **Typography (100% Vietnamese Diacritic Coverage):**
  - Display: `'Unbounded', 'Space Grotesk', sans-serif`
  - Heading: `'Space Grotesk', 'Be Vietnam Pro', sans-serif`
  - Body/UI: `'Be Vietnam Pro', system-ui, sans-serif`
  - Telemetry / Prices / Timers: `'JetBrains Mono', monospace` with `font-variant-numeric: tabular-nums`
- **Anti-Slop & Engineering Constraints:**
  - Zero em-dashes (`—`) in user-facing copy.
  - Zero Lenis / `ScrollSmoother`; enforce `scroll-behavior: auto !important; overflow-x: clip` on `html[data-orbital="true"]` for 1:1 native OS compositor scrolling.
  - Animate compositor-only properties (`transform`, `opacity`, individual `translate`/`scale`) without injecting glow nodes into flex containers.
  - Honor `prefers-reduced-motion: reduce`, WCAG AA contrast (`>= 4.5:1`), `dvh` sizing, and `0px` horizontal overflow (`1440px`, `1280px`, `390px`).

---

## 2. Architecture & Libraries (Static HTML + CDN + Offline Resilience)

- **GSAP 3.14.2 Free Suite (UMD `<script defer>` via jsDelivr):** `gsap.min.js`, `ScrollTrigger.min.js`, `SplitText.min.js`, `Flip.min.js`, `Observer.min.js` (100% compatible with both GitHub Pages HTTPS and local `file://`).
- **OGL WebGL2 (`js/orbital-webgl.js`):**
  - Loads `https://cdn.jsdelivr.net/npm/ogl@1.0.11/+esm` dynamically to render GLSL volumetric fBM nebula clouds, gravitational eclipse corona, cursor-damped chromatic light dispersion, and twinkling depth stars.
  - Automatic graceful fallback chain: **OGL WebGL2 → Inline zero-dependency Raw WebGL2 fullscreen-triangle shader → Lightweight Canvas2D radial glow + starfield**.
  - Performance discipline: `dpr <= 1.75`, `IntersectionObserver` pauses loop off-screen, `document.visibilitychange` pauses hidden tabs, static 1-frame render on `prefers-reduced-motion: reduce`.

---

## 3. Flagship Storefront Choreography (`index.html` — 6 Distinct Chapters)

1. **Floating Orbital Command Bar + `Ctrl + K` Command Palette:** Single crisp frosted 60px top bar (`Energy Boost OBS-01`, section anchors, `Ctrl+K` Command Palette search modal across all 10 SKUs, Orders, Account, live Telemetry Cart pill synced via `localStorage`, mobile drawer).
2. **Chapter 01 — `#orbital-launchpad` (Hero `100dvh`):** Full-bleed WebGL2 shader canvas + asymmetric left editorial column (`SplitText` line-mask reveal, Vietnamese `Unbounded` headline, primary/secondary CTAs, Spectral System Switcher pills) + right **2.5D Solar Orbit Stage** (6 flagship cans across 3 elliptical rings at collision-free `0.18/0.14/0.11 rad/s` & `60°` phase spacing + Target-Lock HUD + live `#orb-telemetry-card`).
3. **Chapter 02 — `#orbital-spectral-drift` (`GSAP ScrollTrigger` Pinned Horizontal-Pan):** On desktop (`>= 960px`), vertical scroll pins the viewport and scrubs cleanly (`1:1 native scroll`, zero wheel hijacking) across 3 full-viewport brand realms (*Monster Sector*, *Red Bull Solar*, *Sting Pulsar*), morphing shader spectra dynamically and updating the bottom progress rail (`01 / 03` .. `03 / 03`). On `< 960px`, seamlessly switches to native horizontal snap cards.
4. **Chapter 03 — `#flash-sale` (Flash Eclipse):** Live monospace countdown (`HH:MM:SS`) + 4 cursor-reactive deal cards wired to `OrbitalCart.add`.
5. **Chapter 04 — `#observatory-vault` (`GSAP Flip` Asymmetric Bento Vault):** All 10 verified SKUs in a `4-col` asymmetric Bento grid (`2-col` featured studio cards for flagship Monster Original & Redbull Original), preserving `#monster-products`, `#redbull-products`, and `#sting-products` anchors, plus **Orbital Filter Dock** (Brand, Zero Sugar, Sort, Live keyword search) animated with `Flip.from()`.
6. **Chapter 05 — `#payload-telemetry` (Sticky Split Combos, Crew Telemetry & FAQ):** Sticky left brand mission specs + interactive `<details class="orb-faq-item">` FAQ accordion alongside 24-can Payload Combo deals and authentic customer telemetry logs.
7. **Chapter 06 — Deep Space Footer:** Architectural giant watermark, 3-column links & flagship HCMC store details, newsletter subscription form (`showToast`), and payment icons.

---

## 4. Product Detail Inspection Chambers & Search Hub

- **5 Artifact Inspection Chambers (`pages/product-detail*.html`):** `55% / 45%` sticky split stage featuring `#orbital-detail-canvas` OGL plasma halo matching product spectrum, real multi-angle thumbnail switcher + lightbox zoom, dynamic `?sku=` hydration (allowing `mn-2`, `mn-3`, `mn-4`, `st-2`, `st-3` links to load exact SKU photos/prices/spectra cleanly), Pack Selector (`Lon lẻ ×1`, `Lốc 6 -5%`, `Thùng 24 -12%`), live Quantity `-`/`+`, real-time subtotal readout, authentic product spec table, and Related Observatory row.
- **Unified Search Hub (`pages/search-results.html`):** Real multi-criteria filter across all 10 SKUs (keyword without Vietnamese diacritics, brand, price bracket, sort) animated with `GSAP Flip` and synced with URL `URLSearchParams`.
