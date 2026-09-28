# Monster Energy Store UI Context

Domain terminology, layout constraints, and styling definitions governing navigation, scrolling behaviors, and interface aesthetics across the Monster Energy static storefront.

## Language

**Invisible Scroll**:
A container configuration enabling smooth touch or mouse-wheel horizontal panning while completely suppressing visible scrollbar tracks and thumb indicators across all browser engines.
_Avoid_: Hidden scroll, hidden overflow, no-scroll, scroll-suppression

**Compact Nav**:
A responsive navigation layout state active on desktop viewports between 1024px and 1200px that reduces link padding, item gap, and font size so all navigation links remain fully visible without horizontal scrolling.
_Avoid_: Mini menu, condensed bar, collapsed nav, desktop drawer

**Sticky Header Constraint**:
The architectural layout rule requiring the global header to remain pinned to the top of the viewport during vertical page scrolling, demanding `overflow-x: clip` rather than `overflow-x: hidden` on ancestor elements to prevent scroll-container interference.
_Avoid_: Fixed header, floating menu, frozen bar, pin header

**Table Scrollbar**:
A purposefully preserved, 8px slim Dark Neon scrollbar configured on wide tabular data containers (`.cart-table-wrapper`, `.admin-section-box`) to guarantee accessibility and data exploration on constrained screens.
_Avoid_: Default scrollbar, raw scroll, unstyled table, native scrollbar

**Dark Neon Theme**:
The brand design system utilizing stealth black surfaces (`#0B0C10`, `#141720`), subtle slate borders (`#2D3344`), and glowing Monster Energy neon green accents (`#00E676`).
_Avoid_: Dark mode, black theme, green palette, neon style
