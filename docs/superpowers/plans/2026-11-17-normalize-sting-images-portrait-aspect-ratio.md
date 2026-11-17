# Normalize Sting Product Images to Portrait Aspect Ratio Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Crop and normalize all Sting product images (`sting-dau.webp`, `sting-gold.webp`, `sting-vietquat.webp`) from 1024x768 landscape to ~306x742 portrait aspect ratio (~0.41) so they render at the exact same visual height and scale as Monster and Redbull across the store.

**Architecture:** Use a lossless PIL Python script to crop transparent side whitespace on the 3 Sting WebP files, verify their physical geometry via an automated test script `scripts/verify_sting_images_aspect_ratio.py`, and run the full regression test suite to ensure zero regressions.

**Tech Stack:** Python 3 (PIL / Pillow), WebP, HTML5, CSS3.

## Global Constraints
- Preserve lossless RGBA alpha transparency on all WebP images.
- Keep aspect ratios between 0.38 and 0.43, matching Monster (0.40) and Redbull (0.37).
- Git Safety: Strictly local commits. Never execute `git push`.
- Maintain 100% PASS on all existing regression test suites.

---

### Task 1: Create Automated Verification Script for Sting Images Aspect Ratio

**Files:**
- Create: `scripts/verify_sting_images_aspect_ratio.py`

**Interfaces:**
- Produces: Test runner verifying image file dimensions, portrait aspect ratios (0.38 - 0.43), and RGBA mode.

- [x] **Step 1: Write the failing verification test script**

Create `scripts/verify_sting_images_aspect_ratio.py` asserting:
1. `assets/images/sting/sting-dau.webp` exists, has mode 'RGBA', height > 700, width < 350, and aspect ratio (width / height) between 0.38 and 0.43.
2. `assets/images/sting/sting-gold.webp` exists, has mode 'RGBA', height > 700, width < 350, and aspect ratio between 0.38 and 0.43.
3. `assets/images/sting/sting-vietquat.webp` exists, has mode 'RGBA', height > 700, width < 350, and aspect ratio between 0.38 and 0.43.

- [x] **Step 2: Run test to verify it fails**

Run: `python scripts/verify_sting_images_aspect_ratio.py`  
Expected: FAIL (because all 3 images are currently 1024x768 landscape with aspect ratio 1.33).

---

### Task 2: Crop and Normalize Sting WebP Images

**Files:**
- Modify: `assets/images/sting/sting-dau.webp`
- Modify: `assets/images/sting/sting-gold.webp`
- Modify: `assets/images/sting/sting-vietquat.webp`

**Interfaces:**
- Consumes: Raw 1024x768 WebP files.
- Produces: Lossless cropped WebP files with tight portrait bounding box.

- [x] **Step 1: Execute image normalization script**

Run Python script using PIL:
- `sting-dau.webp`: crop `(359, 20, 665, 762)` -> save with `lossless=True`.
- `sting-gold.webp`: crop `(358, 15, 663, 760)` -> save with `lossless=True`.
- `sting-vietquat.webp`: crop `(345, 0, 666, 768)` -> save with `lossless=True`.

- [x] **Step 2: Run verification script to check image metrics pass**

Run: `python scripts/verify_sting_images_aspect_ratio.py`  
Expected: PASS (all 3 images satisfy portrait aspect ratio and RGBA assertions).

---

### Task 3: Run Full Regression Suite, Code Review & Local Commit

**Files:**
- Test all: Run all regression test suites.
- Git: Local commit (no git push).

- [x] **Step 1: Run all test suites**

Run:
```powershell
python scripts/verify_sting_images_aspect_ratio.py
python scripts/verify_orders_shipping_reorder_and_sting_eb2025.py
python scripts/verify_topbar_and_discount_badge.py
python scripts/verify_admin_features_update.py
python scripts/verify_faq_edit_save_and_orders_link.py
python scripts/verify_price_formatting.py
python scripts/verify_footer_sync.py
python scripts/verify_sidebar_filter_sync.py
python scripts/verify_admin_kpi_brand_wording.py
python scripts/verify_order_detail_pages.py
```
Expected: 100% PASS on all suites.

- [x] **Step 2: Local git commit**

Commit with message:
```bash
git add assets/images/sting/*.webp scripts/verify_sting_images_aspect_ratio.py docs/superpowers/
git commit -m "fix(images): normalize sting webp images to portrait aspect ratio matching monster and redbull"
```
Ensure NO `git push` is run.
