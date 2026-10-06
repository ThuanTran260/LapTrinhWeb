import os
from PIL import Image

targets = [
    r"d:\LapTrinhWeb\assets\images\sting\sting-dau.webp",
    r"d:\LapTrinhWeb\assets\images\sting\sting-gold.webp",
    r"d:\LapTrinhWeb\assets\images\sting\sting-vietquat.webp"
]

print("=== FINAL VERIFICATION OF STING ASSETS ===")
all_passed = True
for path in targets:
    fname = os.path.basename(path)
    exists = os.path.exists(path)
    if not exists:
        print(f"{fname}: NOT FOUND")
        all_passed = False
        continue
    
    im = Image.open(path)
    w, h = im.size
    mode = im.mode
    size_bytes = os.path.getsize(path)
    size_kib = size_bytes / 1024
    
    corners = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
    corner_pixels = [im.getpixel(pt) for pt in corners]
    corner_alphas = [p[3] for p in corner_pixels]
    
    cond_mode = (mode == "RGBA")
    cond_corners = all(a == 0 for a in corner_alphas)
    cond_size = (30 <= size_kib <= 80)
    passed = cond_mode and cond_corners and cond_size
    if not passed:
        all_passed = False
        
    print(f"File: {fname}")
    print(f"  Dimensions: {w}x{h}")
    print(f"  Mode: {mode} [PASS: {cond_mode}]")
    print(f"  Corner alphas (TL, TR, BL, BR): {corner_alphas} [PASS: {cond_corners}]")
    print(f"  File size: {size_bytes} bytes ({size_kib:.2f} KB) [PASS: {cond_size}]")
    print(f"  Result: {'PASS' if passed else 'FAIL'}")
    print("---")

print(f"OVERALL VERIFICATION: {'PASSED' if all_passed else 'FAILED'}")
