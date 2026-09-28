# 0001. Overflow-x Clip and Dual Scrollbar Architecture

- **Status**: Accepted
- **Date**: 2026-09-28
- **Deciders**: Engineering Team, UI/UX Review

## Context

On Windows desktop platforms, chromium and webkit browsers render prominent 17px light gray/white horizontal scrollbars whenever content exceeds container boundaries. In our Monster Energy dark neon storefront, two areas were adversely affected:
1. The primary navigation bar (`.nav-menu`) on medium/compact viewports.
2. The product detail thumbnail gallery (`.detail-thumbnails`).

These gray Windows scrollbars significantly degraded the visual aesthetic of the dark storefront. However, standard solutions like setting `overflow-x: hidden` on `html` or `body` introduce a critical layout regression: establishing a scroll container / formatting context at the root level breaks `position: sticky; top: 0;` on `.header`.

Furthermore, data tables in `cart.html` (`.cart-table-wrapper`) and `admin.html` (`.admin-section-box`) must retain functional horizontal scrollbars on smaller viewports to ensure accessibility of order and inventory data without breaking the page width.

## Decision

We decided to implement a dual scrollbar and viewport containment strategy:

1. **Protect Sticky Header via `overflow-x: clip`**:
   Apply `overflow-x: clip;` to both `html` and `body`, backed by a progressive enhancement fallback:
   ```css
   html, body {
     overflow-x: clip;
   }
   @supports not (overflow: clip) {
     html, body {
       overflow-x: hidden;
     }
   }
   ```
   Unlike `overflow: hidden`, `overflow: clip` suppresses horizontal page spilling without creating a new scroll container, preserving the sticky positioning of `.header` across all modern browsers.

2. **Invisible Scroll for Navigation and Thumbnails**:
   Apply multi-engine scrollbar hiding exclusively to `.nav-menu` and `.detail-thumbnails`:
   - `scrollbar-width: none;` (Firefox)
   - `-ms-overflow-style: none;` (IE / Legacy Edge)
   - `-webkit-overflow-scrolling: touch;` (iOS WebKit momentum scrolling)
   - `scroll-behavior: smooth;`
   - `::-webkit-scrollbar { display: none; width: 0; height: 0; }` (Chrome, Safari, Edge)

3. **Visual Scroll Affordance (Gradient Fade Mask)**:
   Add a subtle right-edge gradient fade overlay on `.nav-bar::after` on viewports `<= 1200px` (`linear-gradient(90deg, transparent, #0E1017 95%)`) with `pointer-events: none` and `z-index: 2`. This signals to mobile and tablet users that additional navigation items exist beyond the fold without rendering an unsightly physical scrollbar.

4. **Modern Dark Neon Scrollbar for Data Tables & Global Root**:
   Retain visible, themed scrollbars for document scrolling and wide tables (`.cart-table-wrapper`, `.admin-section-box`):
   - WebKit scrollbars: 8px thickness, `#0B0C10` track, `#2D3344` rounded thumb, `var(--primary)` (`#00E676`) neon green on hover.
   - Firefox scrollbars: `scrollbar-color: #2D3344 #0B0C10; scrollbar-width: thin;`.

5. **Compact Nav Optimization (1024px - 1200px)**:
   Add a responsive breakpoint `@media (max-width: 1200px) and (min-width: 769px)` adjusting `.nav-menu { gap: 5px; }` and `.nav-link { padding: 6px 9px; font-size: 0.82rem; }`, combined with shortened labels ("Punch & Shots", "Giỏ Hàng (5)"). This ensures standard desktop users without horizontal scroll wheels can view all menu items without horizontal scrolling.

6. **Accessibility & Active Indicators**:
   - Tab keyboard navigation is supported via `.nav-link:focus-visible { outline: 2px solid var(--primary); outline-offset: -2px; }`.
   - Active neon green indicator is preserved via `.nav-link.active { color: var(--primary); border-bottom: 2px solid var(--primary); }`.

## Considered Options

- **Option A: Global `::-webkit-scrollbar { display: none; }`**
  - *Rejected*: Hiding scrollbars globally makes wide tables in cart and admin dashboard unusable for mouse users who cannot touch-swipe or horizontally tilt their scroll wheel.
- **Option B: Unconditional `overflow-x: hidden` on `body`**
  - *Rejected*: Breaks `.header { position: sticky; top: 0; }` because `overflow-x: hidden` forces the root or body to act as an overflow scroll container.
- **Option C: Collapsing Desktop Navigation into a Hamburger Drawer**
  - *Rejected*: Direct visibility of brand product lines (Original, Ultra, Punch & Shots) is core to user conversion and brand engagement.

## Consequences

- **Positive**:
  - The unsightly Windows gray scrollbar is completely eliminated from navigation and thumbnails.
  - Sticky header remains 100% functional and pinned at top on all browsers.
  - Desktop viewports between 1024px and 1200px comfortably display all navigation items.
  - Mobile swipe remains smooth with gradient fade affordance.
  - Cart and Admin tables retain accessible 8px dark neon scrollbars.
  - Accessible tab key navigation is fully supported.
- **Negative / Constraints**:
  - Any newly introduced horizontal scrolling element must deliberately declare whether it belongs to the Invisible Scroll class or the Table Scrollbar class.
