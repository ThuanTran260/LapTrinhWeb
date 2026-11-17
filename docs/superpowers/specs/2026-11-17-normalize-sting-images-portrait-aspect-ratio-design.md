# Design Spec: Normalize Sting Product Images to Portrait Aspect Ratio

**Date:** 2026-11-17  
**Status:** Approved by User (Option 1)  
**Author:** AI Assistant  

---

## 1. Problem Statement

### 1.1 Inconsistent Visual Scale of Sting Can Images
In `pages/orders.html` (row `#EB-2025`) and throughout the store (`pages/account.html`, `index.html` catalog cards, search suggestions dropdown, admin inventory table), the Sting can appears significantly smaller and thinner than Monster and Redbull cans when placed in identical thumbnail containers.

### 1.2 Root Cause Analysis
- **Monster & Redbull Images:**
  - `assets/images/monster/original.webp`: Canvas 250 x 625px (aspect ratio ~0.400, tight portrait crop).
  - `assets/images/redbull/redbull-lon-vua.webp`: Canvas 285 x 768px (aspect ratio ~0.371, tight portrait crop).
  - `assets/images/redbull/redbull-original.webp`: Canvas 310 x 791px (aspect ratio ~0.392, tight portrait crop).
- **Sting Images:**
  - `assets/images/sting/sting-dau.webp`: Canvas **1024 x 768px** (landscape 4:3, aspect ratio 1.333).
  - The actual can bbox is `(374, 35, 650, 747)`, meaning the can is only 276px wide, flanked by **374px of transparent empty padding on both left and right** (>70% of canvas width is empty space).
  - When rendered in CSS containers with `width: 32px; height: 42px; object-fit: contain;`, the browser fits the 1024px width into 32px, collapsing the image height to only 24px and rendering the can at an undersized **~22px high by ~8.6px wide** (compared to 42px high for Monster and Redbull).
  - The same issue affects `sting-gold.webp` and `sting-vietquat.webp` (both are 1024x768 with identical empty side margins).

---

## 2. Proposed Architecture & Solution (Option 1)

### 2.1 Crop & Normalize Sting Images to Portrait Framing
Normalize the 3 Sting images using Python PIL with lossless WebP compression (`lossless=True`), trimming the excess horizontal margins while preserving a natural ~15px transparent padding:

1. **`assets/images/sting/sting-dau.webp`**:
   - Original: `(1024, 768)`, bbox: `(374, 35, 650, 747)`
   - Crop box: `(359, 20, 665, 762)` (width: 306, height: 742)
   - New aspect ratio: **0.412** (matches Monster 0.400 and Redbull 0.371)

2. **`assets/images/sting/sting-gold.webp`**:
   - Original: `(1024, 768)`, bbox: `(373, 30, 648, 745)`
   - Crop box: `(358, 15, 663, 760)` (width: 305, height: 745)
   - New aspect ratio: **0.409**

3. **`assets/images/sting/sting-vietquat.webp`**:
   - Original: `(1024, 768)`, bbox: `(360, 8, 651, 760)`
   - Crop box: `(345, 0, 666, 768)` (width: 321, height: 768)
   - New aspect ratio: **0.418**

### 2.2 Resulting Visual Geometry
In any container with fixed dimensions (e.g. `width: 32px; height: 42px; object-fit: contain;` in `pages/orders.html`):
- Rendered height: **42px** (100% full container height, identical to Monster & Redbull).
- Rendered width: **~17.3px** (proportional to genuine 330ml sleek can dimensions).
- Effective visual area increases from 189 sq px to **727 sq px (~3.8x increase)**, completely eliminating the undersized "que tăm" appearance.

---

## 3. Scope of Impact

- `assets/images/sting/sting-dau.webp`: Normalized portrait crop.
- `assets/images/sting/sting-gold.webp`: Normalized portrait crop.
- `assets/images/sting/sting-vietquat.webp`: Normalized portrait crop.
- Storefront & Admin pages automatically benefit without code hacks:
  - `pages/orders.html`: Order `#EB-2025` thumbnail matches `#EB-2026` and `#EB-2024` height.
  - `pages/account.html`: Order `#EB-2025` card thumbnail matches other items.
  - `pages/product-detail-sting.html`: Hero image and thumbnails display cleanly centered.
  - `index.html`: Catalog cards and search dropdown thumbnails.
  - `admin/inventory.html` & `admin/index.html`: Table row thumbnails.

---

## 4. Verification & Testing Strategy

1. **Automated Verification Script (`scripts/verify_sting_images_aspect_ratio.py`):**
   - Assert all 3 Sting WebP files exist on disk.
   - Assert all 3 have portrait aspect ratio between `0.35` and `0.45` (width < height, height > 700px, width between 290px and 330px).
   - Assert transparency / alpha channel is fully preserved (`mode == 'RGBA'`).
   - Assert that in `pages/orders.html`, `pages/account.html`, and `js/app.js`, Sting images are correctly referenced.
2. **Regression Testing:**
   - Run all 10 existing test suites to confirm 100% PASS across the entire project.
3. **Local Commit:**
   - Commit changes locally without `git push`.
