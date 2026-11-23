# Energy Solar System (`#cosmic-universe-intro`) — Cosmic Space Intro Design Spec

**Date:** 2026-11-23  
**Target File:** `index.html` (isolated additive stage at top of `<main id="main-content">`)  
**Files Added:** `css/cosmic-universe.css`, `js/cosmic-universe.js`, `scripts/verify_cosmic_universe.py`

## 1. Experience & Layout Overview

Placed at the top of `<main id="main-content">` right below the Sticky Header and above `.hero-kinetic-section`, `#cosmic-universe-intro` creates an interactive **Energy Solar System** showcasing 6 flagship cans across all 3 official brands:

1. **Monster Energy Original 355ml** (`45.000đ`) → `pages/product-detail.html` · `#monster-products` (`#DCFFD2` / `#39FF14` / `#0A4D00`)
2. **Monster Zero Ultra White 500ml** (`48.000đ`) → `pages/product-detail.html` · `#monster-products` (`#F0FDFF` / `#00E5FF` / `#004E66`)
3. **Nước Tăng Lực Redbull Original 250ml** (`18.000đ`) → `pages/product-detail-redbull.html` · `#redbull-products` (`#FFF7CC` / `#FFD700` / `#664400`)
4. **Nước Tăng Lực Redbull Thái Lan 250ml** (`18.000đ`) → `pages/product-detail-redbull-thai.html` · `#redbull-products` (`#FFF7CC` / `#FF6B00` / `#662900`)
5. **Nước Tăng Lực Sting Dâu Tây Đỏ 330ml** (`12.000đ`) → `pages/product-detail-sting.html` · `#sting-products` (`#FFD6E5` / `#FF0055` / `#5C001F`)
6. **Nước Tăng Lực Sting Blue Sleek 320ml** (`13.000đ`) → `pages/product-detail-sting.html` · `#sting-products` (`#D9F7FF` / `#00D2FF` / `#004466`)

## 2. 5-Layer Volumetric Lighting System

1. **Layer 1 — Deep Void & Dual-Tone Nebula + Space Torch:** `#030508` to `#070B12` OLED void, primary dynamic nebula driven by `--cosmic-rgb` opposite a fixed cold deep-space blue counter-nebula (`contain: strict; transform: translateZ(0)`), plus a 460px pointer-following `.cosmic-torch-layer`.
2. **Layer 2 — 4-Layer Energy Core:** `.core-hot` plasma white-neon center, `.core-corona` 3-stop breathing radial aura (4.5s gentle cycle, WCAG safe), `.core-accretion` tilted 3D `conic-gradient` sweep ring, and `.core-flare` anamorphic horizontal lens flare.
3. **Layer 3 — 3D Orbital Rings & Live Energy Tether:** Elliptical tilted orbits brighter on the front arc than rear arc; Canvas draws a 2-layer beam (6px bloom + 1.4px plasma core + 3 photon pulses) from core to the selected can.
4. **Layer 4 — Per-Can Optics:** `.planet-rim-halo` backlit separation halo, Z-depth attenuation (`sin(angle)` scales size, brightness, opacity, and z-index behind/in front of `.cosmic-energy-core`), and `.planet-plasma-ring` hover glow.
5. **Layer 5 — 3-Stop Color Calibration & WCAG AA Hologram Inspector Card:** `#cosmic-holo-card` (`rgba(6, 9, 14, 0.82)`) with core-facing directional top-left highlight, crisp readable Vietnamese labels, direct `Xem Chi Tiết ↗` link, and `Tới Kệ Hãng ↓` smooth scroll button.

## 3. Physics, Performance & Accessibility Invariants

- **Zero Wheel-Hijacking:** Never attaches `wheel` listeners or loads Lenis; native 1:1 OS compositor scroll remains completely intact.
- **Single Unified `rAF` Loop:** Combines 3-layer mouse-parallax starfield (~140 stars), occasional shooting stars, live energy tether, and 6-can 3D orbital projection with smooth hover/focus damping. Auto-sleeps on `document.hidden` and offscreen `IntersectionObserver`.
- **Mobile (`< 768px`):** Collapses into compact Energy Core + horizontal `scroll-snap` 6-can strip + Hologram Card + Dock with `>= 44px` touch targets and zero horizontal overflow.
- **WCAG 2.2.2 & Reduced Motion:** `#cosmic-motion-toggle` toggles visible text `"Tắt chuyển động vũ trụ"` / `"Bật chuyển động vũ trụ"` without `aria-pressed`; `@media (prefers-reduced-motion: reduce)` freezes motion into a balanced static constellation.
- **Test Compatibility:** Preserves `css/style.css` (`0` edits), respects `verify_no_product_specs.py`, `verify_price_formatting.py`, and `verify_sting_images_aspect_ratio.py`.
