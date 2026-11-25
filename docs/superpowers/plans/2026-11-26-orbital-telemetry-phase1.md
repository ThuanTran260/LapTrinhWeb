# ENERGY BOOST STORE — Orbital Telemetry 2026 Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` + `dispatching-parallel-agents` + `verification-before-completion`. Execute on branch `feat/orbital-telemetry-redesign` separated from `main` (`1db60d9`). Never execute `git push`.

**Goal:** Deliver Phase 1 of the full **Orbital Telemetry 2026** AI-modern redesign across `index.html`, 5× `pages/product-detail*.html`, and `pages/search-results.html` with **GSAP 3.14 Free Suite** + **OGL WebGL2 GLSL Shaders** while preserving 100% e-commerce functionality and 1:1 native OS scroll.

**Architecture:** Clean modular CSS (`orbital-tokens.css` + `orbital-storefront.css`), dual-engine GLSL WebGL2 + Canvas2D fallback (`js/orbital-webgl.js`), GSAP 3.14 ScrollTrigger/SplitText/Flip choreography & `OrbitalCart` telemetry (`js/orbital-motion.js`), and a strict `data-orbital` coexistence guard in `js/app.js`.

**Tech Stack:** Pure Static HTML5 · CSS3 Custom Properties & Liquid-Glass Approximations · GSAP 3.14.2 (`ScrollTrigger`, `SplitText`, `Flip`, `Observer`) · OGL 1.0.11 WebGL2 ESM + Inline WebGL2/Canvas2D Fallback · Google Fonts Vietnamese (`Unbounded`, `Space Grotesk`, `Be Vietnam Pro`, `JetBrains Mono`) · Vanilla JS.

---

## Global Constraints

1. Work exclusively on branch `feat/orbital-telemetry-redesign` branched from `main` (`1db60d9`). Never `git push`, `git reset --hard`, or `git clean -f`.
2. Enforce `scroll-behavior: auto !important; overflow-x: clip;` on `html[data-orbital="true"]`. Never use Lenis or `ScrollSmoother`. `5 × 120px` wheel ticks MUST equal `600px ± 5px`.
3. Zero em-dashes (`—`) inside generated HTML/UI copy.
4. Zero `console.error`, zero `pageerror`, zero failed image loads (`naturalWidth > 0`), `scrollWidth <= innerWidth` across `1440px`, `1280px`, and `390px`.
5. Support `prefers-reduced-motion: reduce`, `dpr <= 1.75`, off-screen `IntersectionObserver` pausing, and offline/`file://` resilience.

---

## File Map & Wave Execution Graph

- **Wave 0 (Done):** Branch `feat/orbital-telemetry-redesign`, Spec + Plan persisted under `docs/superpowers/`.
- **Wave 1 (Parallel Subagents — Zero Overlapping Files):**
  - Task 1 (`Orbital CSS Systems Architect`): `css/orbital-tokens.css`, `css/orbital-storefront.css`
  - Task 2 (`OGL WebGL2 Shader Engineer`): `js/orbital-webgl.js`
  - Task 3 (`GSAP Motion & App Bridge Engineer`): `js/orbital-motion.js`, surgical `js/app.js` updates
- **Wave 2 (Parallel Subagents AFTER Wave 1):**
  - Task 4 (`Flagship Storefront HTML Architect`): `index.html`
  - Task 5 (`Product Chamber & Search Hub Engineer`): `pages/product-detail.html`, `pages/product-detail-redbull.html`, `pages/product-detail-redbull-thai.html`, `pages/product-detail-redbull-lonvua.html`, `pages/product-detail-sting.html`, `pages/search-results.html`
- **Wave 3 (QA, Live Browser Verification & Local Commit):**
  - Task 6 (`Phase 1 QA & Chromium Verifier`): `scripts/verify_orbital_phase1.py` (static + headless Chromium checks) + `node --check`
  - Task 7 (`Browser Visual Inspector`): Live interactive visual audit & screenshots at `1440px`, `1280px`, `390px`
  - Task 8 (Coordinator): Fix any defects uncovered in Wave 3, re-run verification until 100% green, and commit cleanly to `feat/orbital-telemetry-redesign`.

---

## Locked Interfaces Across Wave 1 & Wave 2

- HTML Root: `<html lang="vi" data-orbital="true" data-spectral="monster|redbull|sting">`
- Nav & Command Palette IDs/Classes: `.orb-nav-shell`, `.orb-nav-bar`, `#orb-cmd-trigger`, `.orb-cart-pill`, `.orb-cart-count`, `.orb-cart-total`, `#header-account-link`, `#header-account-value`, `#orb-mobile-toggle`, `#orb-mobile-drawer`, `#orb-cmd-palette`, `#orb-cmd-input`, `#orb-cmd-list`, `#orb-cmd-close`, `#toast-container`.
- Hero & Sections: `#orbital-launchpad`, `#orbital-space-canvas`, `.orb-hero-title`, `.orb-orbit-stage`, `.orb-orbit-node`, `.orb-target-reticle`, `#orb-telemetry-card`, `#orbital-spectral-drift`, `.orb-drift-track`, `.orb-drift-panel`, `#orb-drift-index`, `.orb-drift-bar-fill`, `#flash-sale`, `#orb-countdown-h/m/s`, `#observatory-vault`, `.orb-filter-dock`, `#orb-vault-search`, `#orb-vault-sort`, `#orb-vault-count`, `.orb-vault-grid`, `.orb-bento-card`, `#payload-telemetry`, `.orb-footer`.
- Product Detail IDs: `#orbital-detail-canvas`, `#main-product-image`, `#orb-detail-title`, `#orb-detail-code`, `#orb-detail-price`, `#orb-detail-old-price`, `#orb-detail-savings`, `#orb-qty-dec`, `#orb-qty-inc`, `#orb-qty-input`, `#orb-detail-add-cart`, `.orb-pack-btn`, `.orb-thumb-btn`.
- Search Hub IDs: `#search-results-grid`, `#search-query-text`, `#search-count-number`, `#search-breadcrumb-query`, `#search-filter-keyword`, `input[name="search-brand"]`, `input[name="search-price"]`, `#orb-search-sort`.
- Global Window Objects: `window.OrbitalWebGL`, `window.OrbitalCart`, `window.OrbitalMotion`.
