# Adaptive Kinetic Glass Implementation Plan

> **For agentic workers:** Parallel execution across disjoint file owners followed by full regression QA and live browser visual verification.

**Goal:** Deliver the Adaptive Kinetic Glass aesthetic and 60fps interactive mouse/scroll choreography across all 28 pages of ENERGY BOOST STORE while keeping `css/style.css` untouched and 100% of existing tests green.

**Architecture:** Isolated additive layer (`css/kinetic-glass.css` + `js/motion-engine.js`) loaded cleanly via one `<link>` tag per HTML file and a dynamic `SITE_ROOT` loader in `js/app.js`.

**Tech Stack:** Native CSS (`animation-timeline: scroll()`, `view()`, `@view-transition`, CSS mask border spotlights, `preserve-3d`), Vanilla JS (`requestAnimationFrame`, `IntersectionObserver`, 2D Canvas), progressive optional Lenis smooth scroll.

## File Ownership Map

- **Subagent 1 (CSS Visual Architect):** Create `css/kinetic-glass.css`
- **Subagent 2 (Motion Engine Engineer):** Create `js/motion-engine.js` and append loader to `js/app.js`
- **Subagent 3 (HTML Integration Engineer):** Add `kinetic-glass.css` `<link>` to all 28 HTML files (`index.html`, 13 `pages/*.html`, 14 `admin/*.html`)
- **Subagent 4 (QA & Test Engineer):** Create `scripts/verify_kinetic_glass_ui.py` and run all 48 verification scripts + JS syntax validation
- **Subagent 5 (Browser Visual Verifier):** Live visual, hover, scroll, mobile, and Admin Portal verification via `browser` subagent
