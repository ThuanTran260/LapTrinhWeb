#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification script for Sting product images aspect ratio normalization.
Asserts that all 3 Sting WebP images:
1. Exist on disk.
2. Have RGBA color mode with transparent alpha channel.
3. Have tight portrait framing with aspect ratio (width / height) between 0.38 and 0.43 (width < 350, height > 700).
4. Content vertically fills >90% of the canvas with natural tight lateral margins (<= 30px).
"""

import sys
import os
from pathlib import Path
from PIL import Image

def verify_sting_images_aspect_ratio():
    root = Path(__file__).resolve().parent.parent
    sting_dir = root / "assets" / "images" / "sting"

    targets = [
        "sting-dau.webp",
        "sting-gold.webp",
        "sting-vietquat.webp"
    ]

    passes = []
    failures = []

    def check(condition, desc):
        if condition:
            passes.append(desc)
            print(f"  [PASS] {desc}")
        else:
            failures.append(desc)
            print(f"  [FAIL] {desc}")

    print("=== VERIFYING STING WEBP IMAGES ASPECT RATIO ===")

    for filename in targets:
        file_path = sting_dir / filename
        rel_path = file_path.relative_to(root)
        print(f"\nChecking: {rel_path}")

        # 1. Existence
        if not file_path.exists():
            failures.append(f"{filename} does not exist at {rel_path}")
            print(f"  [FAIL] File does not exist")
            continue
        passes.append(f"{filename} exists")

        # Open image
        im = Image.open(file_path)
        w, h = im.size
        mode = im.mode
        aspect_ratio = w / h

        print(f"  Dimensions: {w}x{h}, Mode: {mode}, Aspect Ratio: {aspect_ratio:.4f}")

        # 2. Image Mode
        check(mode == "RGBA", f"{filename}: Mode is 'RGBA' (got '{mode}')")

        # 3. Portrait dimensions and aspect ratio bounds
        check(w < 350, f"{filename}: Width is < 350px (got {w}px)")
        check(290 <= w <= 330, f"{filename}: Width is within [290, 330] (got {w}px)")
        check(h > 700, f"{filename}: Height is > 700px (got {h}px)")
        check(0.38 <= aspect_ratio <= 0.43, f"{filename}: Aspect ratio {aspect_ratio:.4f} is within [0.38, 0.43]")

        # 4. Corner & perimeter transparency
        if mode == "RGBA":
            corners = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
            corner_alphas = [im.getpixel(pt)[3] for pt in corners]
            check(all(a == 0 for a in corner_alphas), f"{filename}: All 4 corners are transparent (alphas: {corner_alphas})")

            # Check that outer edges have 0 non-transparent pixels (no clipped graphics)
            top_edge_alphas = sum(1 for x in range(w) if im.getpixel((x, 0))[3] > 0)
            bottom_edge_alphas = sum(1 for x in range(w) if im.getpixel((x, h - 1))[3] > 0)
            left_edge_alphas = sum(1 for y in range(h) if im.getpixel((0, y))[3] > 0)
            right_edge_alphas = sum(1 for y in range(h) if im.getpixel((w - 1, y))[3] > 0)
            edge_clipped = top_edge_alphas + bottom_edge_alphas + left_edge_alphas + right_edge_alphas
            check(edge_clipped == 0, f"{filename}: Canvas perimeter is fully transparent with 0 clipped pixels")
        else:
            check(False, f"{filename}: Cannot check transparency because mode is not 'RGBA'")

        # 5. Non-transparent content bounding box check
        bbox = im.getbbox()
        if bbox is None:
            check(False, f"{filename}: Image is entirely transparent")
        else:
            left, top, right, bottom = bbox
            content_w = right - left
            content_h = bottom - top
            left_margin = left
            right_margin = w - right
            vertical_coverage = content_h / h

            print(f"  BBox: {bbox} (content {content_w}x{content_h}), margins L={left_margin}px R={right_margin}px, vertical coverage={vertical_coverage*100:.1f}%")

            check(vertical_coverage >= 0.90, f"{filename}: Content fills >= 90% vertically ({vertical_coverage*100:.1f}%)")
            check(left_margin <= 30 and right_margin <= 30, f"{filename}: Lateral margins are tight <= 30px (L={left_margin}, R={right_margin})")

    # 6. Integration checks: Sting images referenced in Storefront & Orders
    print("\n--- Checking Storefront & Orders references to Sting assets ---")
    orders_path = root / "pages" / "orders.html"
    account_path = root / "pages" / "account.html"
    index_path = root / "index.html"
    app_js_path = root / "js" / "app.js"

    if orders_path.exists():
        orders_content = orders_path.read_text(encoding="utf-8")
        check("assets/images/sting/sting-dau.webp" in orders_content, "orders.html references sting-dau.webp")
    else:
        check(False, "orders.html exists")

    if account_path.exists():
        account_content = account_path.read_text(encoding="utf-8")
        check("assets/images/sting/sting-dau.webp" in account_content, "account.html references sting-dau.webp")
    else:
        check(False, "account.html exists")

    if app_js_path.exists():
        app_js_content = app_js_path.read_text(encoding="utf-8")
        for fn in targets:
            check(f"assets/images/sting/{fn}" in app_js_content, f"js/app.js references {fn}")
    else:
        check(False, "js/app.js exists")

    if index_path.exists():
        index_content = index_path.read_text(encoding="utf-8")
        for fn in targets:
            check(f"assets/images/sting/{fn}" in index_content, f"index.html references {fn}")
    else:
        check(False, "index.html exists")

    print("\n" + "=" * 60)
    print(f"Result: {len(passes)} passed, {len(failures)} failed.")
    print("=" * 60)

    if failures:
        print("\nSUMMARY OF FAILURES:")
        for f in failures:
            print(f"  - {f}")
        return False

    print("\nALL STING IMAGES ASPECT RATIO CHECKS PASSED!")
    return True

if __name__ == "__main__":
    success = verify_sting_images_aspect_ratio()
    sys.exit(0 if success else 1)
