import os
import sys
import re

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

workspace = r"e:\luyentaphe\portfolio\Web ban hang"
style_css_path = os.path.join(workspace, "css", "style.css")
index_html_path = os.path.join(workspace, "index.html")
product_detail_path = os.path.join(workspace, "product-detail.html")
adr_path = os.path.join(workspace, "docs", "adr", "0001-overflow-clip-and-scrollbar-system.md")
context_path = os.path.join(workspace, "CONTEXT.md")

errors = []
successes = []

def check(condition, desc):
    if condition:
        successes.append(f"[PASS] {desc}")
    else:
        errors.append(f"[FAIL] {desc}")

# 1. Check style.css
with open(style_css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

# a) Sticky Header protection
check("overflow-x: clip;" in css_content, "style.css contains 'overflow-x: clip;'")
check("@supports not (overflow: clip)" in css_content, "style.css contains fallback '@supports not (overflow: clip)'")
check("overflow-x: hidden;" in css_content, "style.css contains fallback 'overflow-x: hidden;'")
check("position: sticky;" in css_content and "top: 0;" in css_content, "style.css contains sticky header rules")

# b) Invisible scroll in .nav-menu & .detail-thumbnails
check(".nav-menu" in css_content and "scrollbar-width: none;" in css_content, "style.css has 'scrollbar-width: none;' for nav-menu")
check("-ms-overflow-style: none;" in css_content, "style.css has '-ms-overflow-style: none;'")
check("-webkit-overflow-scrolling: touch;" in css_content, "style.css has '-webkit-overflow-scrolling: touch;'")
check(".nav-menu::-webkit-scrollbar" in css_content and "display: none;" in css_content, "style.css has .nav-menu::-webkit-scrollbar { display: none; }")
check(".detail-thumbnails::-webkit-scrollbar" in css_content, "style.css has .detail-thumbnails::-webkit-scrollbar")

# c) Dark Neon Scrollbar
check("::-webkit-scrollbar" in css_content and "width: 8px;" in css_content and "height: 8px;" in css_content, "style.css has 8px ::-webkit-scrollbar")
check("::-webkit-scrollbar-thumb" in css_content and "#2D3344" in css_content, "style.css has #2D3344 scrollbar thumb")
check("::-webkit-scrollbar-thumb:hover" in css_content and "var(--primary)" in css_content, "style.css has neon green scrollbar hover")
check("scrollbar-color: #2D3344 #0B0C10;" in css_content, "style.css has Firefox scrollbar-color")
check(".cart-table-wrapper" in css_content and "overflow-x: auto;" in css_content, "style.css preserves overflow-x: auto for cart table")
check(".admin-section-box" in css_content and "overflow-x: auto;" in css_content, "style.css preserves overflow-x: auto for admin tables")

# d) Compact Nav & Desktop padding optimization
check("padding: 8px 11px;" in css_content, "style.css has optimized desktop nav-link padding (8px 11px) preventing container clipping")
check("@media (max-width: 1200px) and (min-width: 769px)" in css_content, "style.css has compact nav media query")
check("font-size: 0.82rem;" in css_content, "style.css has font-size: 0.82rem in compact nav")
check("padding: 6px 9px;" in css_content, "style.css has padding: 6px 9px in compact nav")
check("gap: 5px;" in css_content, "style.css has gap: 5px in compact nav")

# e) Gradient Fade Mask
check(".nav-bar::after" in css_content, "style.css has .nav-bar::after")
check("linear-gradient" in css_content and "rgba(14, 16, 23" in css_content, "style.css has gradient fade mask overlay")
check("@media (max-width: 1200px)" in css_content, "style.css activates gradient fade mask on <= 1200px")

# f) Accessibility: focus-visible
check(".nav-link:focus-visible" in css_content and "outline: 2px solid var(--primary);" in css_content, "style.css has focus-visible accessibility ring")

# g) Active Neon Indicator
check(".nav-link.active" in css_content and "border-bottom: 2px solid var(--primary);" in css_content, "style.css preserves active neon green underline")

# 2. Check index.html
with open(index_html_path, "r", encoding="utf-8") as f:
    index_content = f.read()

check("Monster Punch & Shots" not in index_content, "index.html replaced 'Monster Punch & Shots'")
check("Punch & Shots</a>" in index_content, "index.html has shortened 'Punch & Shots'")
check("Giỏ Hàng Tĩnh (5 lon)" not in index_content, "index.html replaced 'Giỏ Hàng Tĩnh (5 lon)'")
check("Giỏ Hàng (5)</a>" in index_content, "index.html has shortened 'Giỏ Hàng (5)'")

# 3. Check product-detail.html
with open(product_detail_path, "r", encoding="utf-8") as f:
    detail_content = f.read()

check("Giỏ Hàng Tĩnh (5 lon)" not in detail_content, "product-detail.html replaced 'Giỏ Hàng Tĩnh (5 lon)'")
check("Giỏ Hàng (5)</a>" in detail_content, "product-detail.html has shortened 'Giỏ Hàng (5)'")

# 4. Check docs/adr/0001-overflow-clip-and-scrollbar-system.md
check(os.path.exists(adr_path), "ADR 0001 file exists")
if os.path.exists(adr_path):
    with open(adr_path, "r", encoding="utf-8") as f:
        adr_content = f.read()
    check("Context" in adr_content, "ADR contains Context section")
    check("Decision" in adr_content, "ADR contains Decision section")
    check("Considered Options" in adr_content or "Alternatives" in adr_content, "ADR contains Alternatives section")
    check("Consequences" in adr_content, "ADR contains Consequences section")

# 5. Check CONTEXT.md
check(os.path.exists(context_path), "CONTEXT.md file exists")
if os.path.exists(context_path):
    with open(context_path, "r", encoding="utf-8") as f:
        ctx_content = f.read()
    check("Invisible Scroll" in ctx_content, "CONTEXT.md defines 'Invisible Scroll'")
    check("Compact Nav" in ctx_content, "CONTEXT.md defines 'Compact Nav'")
    check("Sticky Header Constraint" in ctx_content, "CONTEXT.md defines 'Sticky Header Constraint'")
    check("Table Scrollbar" in ctx_content, "CONTEXT.md defines 'Table Scrollbar'")
    check("Dark Neon Theme" in ctx_content, "CONTEXT.md defines 'Dark Neon Theme'")

print("\n--- TEST RESULTS ---")
for s in successes:
    print(s)
for e in errors:
    print(e)

if errors:
    print(f"\n{len(errors)} checks FAILED!")
    sys.exit(1)
else:
    print(f"\nALL {len(successes)} CHECKS PASSED PERFECTLY!")
    sys.exit(0)
