# Design Spec: Synchronize Top-Bar ENERGY10 Announcement & Enhance Discount Badge Legibility

**Date:** 2026-11-16  
**Status:** Approved by User (Option 1)  
**Author:** AI Assistant  

---

## 1. Problem Statement

### 1.1 Inconsistent Header Top-Bar Announcement
On the Sting product detail page (`pages/product-detail-sting.html`), the announcement banner currently displays:
```html
<div class="announcement-text">
  <i class="fas fa-truck-fast" style="color: var(--primary);"></i>
  <span>ĐƠN HÀNG HỎA TỐC: <strong>Cam kết giao lạnh trong 2H</strong> tại TP.HCM & Hà Nội!</span>
</div>
```
Meanwhile, the homepage (`index.html`) features the signature promo code announcement:
```html
<div class="announcement-text">
  <i class="fas fa-bolt"></i>
  <span>ENERGY BOOST: Nhập mã <span class="coupon-badge" onclick="showToast('Đã chép mã giảm giá ENERGY10!', 'info')">ENERGY10</span> giảm ngay 10% cho đơn hàng đầu tiên!</span>
</div>
```
This discrepancy confuses shoppers navigating between the homepage and Sting product details. Furthermore, `pages/product-detail-redbull-thai.html` and `pages/product-detail-redbull-lonvua.html` also carry the old delivery text, while `product-detail.html` and `product-detail-redbull.html` use the `ENERGY10` coupon text. All product detail pages should be synchronized to provide a cohesive customer experience.

### 1.2 Low Contrast on Discount Badges
The `.badge-discount` class in `css/style.css` (lines 749–760) renders promotional badges (e.g., `-18% GIẢM`, `-20% GIẢM`) with white text (`#FFF`) on a neon green background (`var(--secondary)` = `#00FF66`):
```css
.badge-discount {
  position: absolute;
  top: 12px;
  left: 12px;
  background: var(--secondary);
  color: #FFF; /* ❌ Contrast ratio ~1.35:1 */
  font-size: 0.75rem;
  font-weight: 800;
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  z-index: 5;
}
```
This creates a severe accessibility issue where the text is washed out and the discount figures are barely legible against the bright fluorescent background.

---

## 2. Proposed Solution (Option 1 - User Approved)

### 2.1 Top-Bar Header Synchronization
Update `pages/product-detail-sting.html` (and also ensure `pages/product-detail-redbull-thai.html`, `pages/product-detail-redbull-lonvua.html`, `pages/product-detail.html`, `pages/product-detail-redbull.html`) feature the exact uniform announcement banner matching `index.html`:
```html
      <div class="announcement-text">
        <i class="fas fa-bolt"></i>
        <span>ENERGY BOOST: Nhập mã <span class="coupon-badge" onclick="showToast('Đã chép mã giảm giá ENERGY10!', 'info')">ENERGY10</span> giảm ngay 10% cho đơn hàng đầu tiên!</span>
      </div>
```
This ensures:
- Visual consistency across the entire customer-facing storefront.
- Seamless coupon copying functionality via the interactive `.coupon-badge` element.

### 2.2 High-Contrast Neon-Accent Discount Badges
Update `.badge-discount` in `css/style.css` to use deep black typography (`color: #000; font-weight: 900;`) on the electric mint/neon green background (`background: var(--secondary);`), reinforced with a subtle neon glow (`box-shadow: 0 0 10px rgba(0, 255, 102, 0.4);`):
```css
.badge-discount {
  position: absolute;
  top: 12px;
  left: 12px;
  background: var(--secondary);
  color: #000;
  font-size: 0.75rem;
  font-weight: 900;
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  z-index: 5;
  box-shadow: 0 0 10px rgba(0, 255, 102, 0.4);
}
```

#### Contrast Analysis:
- Background: `#00FF66` (Relative luminance ~0.73)
- Text Color: `#000000` (Relative luminance 0.0)
- Contrast Ratio: **15.6:1** (Exceeds WCAG AAA threshold of 7:1)
- Result: Crisp, ultra-sharp numbers that immediately pop out and grab buyer attention while maintaining the cyberpunk Kinetic Volt design aesthetic.

---

## 3. Scope of Modifications

1. `css/style.css`:
   - Update `.badge-discount` styling rule at lines 749–760.
2. `pages/product-detail-sting.html`:
   - Replace announcement text block in `.top-bar .announcement-text` (lines 18–21).
3. `pages/product-detail-redbull-thai.html`:
   - Synchronize announcement text block to match `index.html`.
4. `pages/product-detail-redbull-lonvua.html`:
   - Synchronize announcement text block to match `index.html`.
5. `pages/product-detail.html` & `pages/product-detail-redbull.html`:
   - Ensure announcement text ends with `"giảm ngay 10% cho đơn hàng đầu tiên!"` matching `index.html`.
6. `scripts/verify_topbar_and_discount_badge.py`:
   - Automated test suite verifying contrast rule, styles, and top-bar announcement consistency across all target files.

---

## 4. Verification & Testing Strategy

1. **Automated Verification Script (`verify_topbar_and_discount_badge.py`):**
   - Check `css/style.css`: `.badge-discount` has `color: #000`, `font-weight: 900`, `box-shadow`, `background: var(--secondary)`.
   - Check `pages/product-detail-sting.html`: contains `ENERGY BOOST: Nhập mã`, `coupon-badge`, `ENERGY10`.
   - Check all product detail pages: all contain the unified top-bar announcement.
2. **Regression Testing:**
   - Run all 7 existing regression test suites (`verify_admin_features_update.py`, `verify_faq_edit_save_and_orders_link.py`, `verify_implementation.py`, `verify_price_formatting.py`, `verify_footer_sync.py`, `verify_sidebar_filter_sync.py`, `verify_admin_kpi_brand_wording.py`).
3. **Dual Code Review:**
   - Run parallel Standards Reviewer and Spec Reviewer subagents.
4. **Git Safety:**
   - Commit locally only. No `git push`.
