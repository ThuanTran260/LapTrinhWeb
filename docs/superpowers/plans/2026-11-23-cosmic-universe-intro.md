# Energy Solar System Implementation Plan

> **For agentic workers:** Parallel execution across disjoint file owners followed by full regression QA (48/48 scripts) and live browser + 1:1 scroll verification.

**Goal:** Add the `#cosmic-universe-intro` 3D orbital space showcase with 5-layer volumetric lighting and direct links to all 6 flagship cans at the top of `index.html`.

**Architecture:** Isolated additive stylesheet (`css/cosmic-universe.css`) and unified single-`rAF` engine (`js/cosmic-universe.js`) integrated cleanly at 3 points in `index.html`, leaving `css/style.css` and the other 27 HTML pages untouched.

## File Ownership Map

- **Subagent 1 (Cosmic Lighting & CSS Architect):** Create `css/cosmic-universe.css`
- **Subagent 2 (Cosmic Physics & Canvas Engineer):** Create `js/cosmic-universe.js`
- **Subagent 3 (Storefront Cosmic Markup Integrator):** Edit `index.html` (CSS link, `#cosmic-universe-intro` markup, deferred JS script)
- **Subagent 4 (Cosmic QA & Regression Engineer):** Create `scripts/verify_cosmic_universe.py` and run all 48 verification scripts
- **Subagent 5 (Browser Visual & Scroll Verifier):** Live desktop/mobile visual audit, interactive links/filters/hover check, and 1:1 scroll benchmark via `browser` subagent
