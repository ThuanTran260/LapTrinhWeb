# Adaptive Kinetic Glass UI & Interactive Motion Design

**Date:** 2026-11-23  
**Project:** ENERGY BOOST STORE (28 static HTML pages: `index.html`, 13 `pages/*.html`, 14 `admin/*.html`)  
**Approach Selected:** Adaptive Kinetic Glass (Dual-Mode: `kinetic` Showcase + `precision` Glass)

## 1. Architecture & Non-Breaking Module Isolation

To enhance visual depth and interactive physics across all 28 HTML pages without modifying any existing layout selector, text string, or test invariant in `css/style.css`:

1. **`css/kinetic-glass.css`** (new stylesheet):
   - Linked immediately after `css/style.css` on all 28 HTML files so overrides win naturally in CSS cascade.
   - Preserves `overflow-x: clip` on `html`/`body` (Sticky Header Constraint) and keeps 8px Table Scrollbars intact.
   - Uses dedicated injected `<span>` layers (`.kg-border-glow`, `.kg-glare-layer`) instead of overwriting `::before`/`::after` on cards that already define pseudo-elements (e.g. `.kpi-card::before`).
2. **`js/motion-engine.js`** (new motion module):
   - Dynamically loaded from `js/app.js` using the existing `SITE_ROOT` resolver so every depth (`root`, `pages/`, `admin/`) works offline (`file://`) and on GitHub Pages.
   - Detects page context and sets `document.documentElement.dataset.uiMode` to `"kinetic"` or `"precision"`.

## 2. Dual-Mode Experience Matrix

| Feature / Effect | `kinetic` Mode (`index.html`, `pages/product-detail*.html`) | `precision` Mode (`admin/*.html`, `cart`, `orders`, `account`, `login`, `payment-gateway`, `search-results`) |
| :--- | :--- | :--- |
| Double-Bezel Surfaces & Top Highlight | Yes | Yes |
| Raycast Border Spotlight (`--mx`, `--my`) | Yes (brand-colored per can/section) | Yes (emerald / cyan / gold subtle glow) |
| 3D Tilt & Metallic Specular Glare | Yes (`.product-card-stitch`, Hero 3D stage) | Off (keeps tables/forms rock-steady) |
| Magnetic Button-in-Button & Sheen Sweep | Yes | Tactile sheen & micro-press only |
| Adaptive Energy Cursor Halo & Click Ripple | Yes (desktop fine-pointer only) | Off |
| Hero Carbonation Canvas + WCAG Toggle | Yes (on Hero pages) | Off |
| Ambient Brand Aura Shift on Scroll | Yes (Monster → Redbull → Sting) | Static subtle dark carbon aura |
| Layered Parallax & Velocity Micro-Tilt | Yes (Hero, Combo cans, product grids) | Off |
| KPI Count-Up Animation | N/A | Yes (restores exact Vietnamese `đ` formatting) |
| Volt Scroll Progress Bar & View Transitions | Yes (native CSS + fallback) | Yes (native CSS + fallback) |

## 3. Shared Interface Contract (`css/kinetic-glass.css` ↔ `js/motion-engine.js`)

- Root attributes & classes:
  - `html[data-ui-mode="kinetic" | "precision"]`
  - `html.kg-pointer-fine`, `html.kg-reduced-motion`
- Global injected DOM:
  - `#volt-scroll-progress` (`aria-hidden="true"`, first child of `body`)
  - `#kg-ambient-aura` (`aria-hidden="true"`, driven by `--kg-aura-color`)
  - `#kg-film-grain` (`aria-hidden="true"`)
  - `#kg-cursor-halo` (`aria-hidden="true"`, `.kg-cursor-label` inner text, translated via `--cx`, `--cy`)
- Hero-specific injected DOM:
  - `<canvas id="kg-hero-canvas" aria-hidden="true"></canvas>`
  - `<button type="button" id="volt-canvas-toggle" class="volt-canvas-toggle">` toggling visible text between `"Tắt hiệu ứng nền"` and `"Bật hiệu ứng nền"` (no `aria-pressed`)
- Card-level injected DOM & CSS variables:
  - `.kg-spotlight` targets receive `<span class="kg-border-glow" aria-hidden="true"></span>` and variables `--mx`, `--my`, `--brand-rgb`, plus `.is-hovered`.
  - `.product-card-stitch` receives `<span class="kg-glare-layer" aria-hidden="true"></span>` and `--rx`, `--ry`, `--gx`, `--gy`, plus `.kg-tilt-active`.
  - Magnetic buttons receive `--mag-x`, `--mag-y`.
  - Parallax elements receive `--parallax-y`; `.kg-velocity-grid` receives `--kg-skew`.
  - Fallback reveal elements use `.kg-scroll-reveal`, `.kg-reveal-pending`, `.kg-reveal-visible`.

## 4. Modern Web Guidance & Performance Guardrails

- **Compositor-Only Motion:** Animate exclusively `transform` and `opacity`. Remove `backdrop-filter` from scrolling product cards to prevent GPU fill-rate drops, reserving `backdrop-filter` for sticky `.header`, modals, and floating badges.
- **Reduced Motion (`prefers-reduced-motion`):** Spatial motion opts in inside `@media (prefers-reduced-motion: no-preference)`; `@media (prefers-reduced-motion: reduce)` preserves full visibility (`opacity: 1; transform: none`) and color/border contrast feedback without `0.01ms` hacks.
- **Native CSS Scroll-Driven Animations + Feature Detection:**
  - Progress bar gated by `@supports (animation-timeline: scroll())` with `animation-timeline` placed after `animation`.
  - Scroll entry reveals gated by `@supports ((animation-timeline: view()) and (animation-range: entry))`.
  - JS fallbacks run only when `CSS.supports(...)` returns false and reduced motion is off.
- **Cross-Document View Transitions:** `@view-transition { navigation: auto; }` inside `@media (prefers-reduced-motion: no-preference)`.
- **Offline Compatibility:** 100% functional via `file://` with progressive Lenis smooth scroll enhancement only over `http:`/`https:` desktop fine pointers.
