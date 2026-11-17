# Design Spec: Add Reorder Button to Shipping Orders & Convert Order #EB-2025 to Sting

**Date:** 2026-11-17  
**Status:** Approved by User (Option 1 & Sting Choice A)  
**Author:** AI Assistant  

---

## 1. Problem Statement & User Intent

### 1.1 Missing Reorder Action on Shipping Order (#EB-2026)
In `pages/orders.html`, order `#EB-2026` (Status: `ĐANG GIAO (2H)`) currently contains only two action buttons in its action column:
- `Chi Tiết` (`<a href="order-detail.html?id=EB-2026">`)
- `Định Vị` (`<button onclick="showToast(...)">`)

Unlike the completed orders below (`#EB-2025` and `#EB-2024`), order `#EB-2026` lacks a "Mua Lại" (Reorder) button. Customers frequently want to reorder or re-add their fast-delivery items (2x Monster + 2x Redbull) without losing the ability to track real-time delivery status.

### 1.2 Outdated Combo Product in Order #EB-2025
Order `#EB-2025` currently displays an old promotional combo:
- Name: `1x Combo Thùng 24 Lon Đấu Trường`
- Subtitle: `🎁 Tặng Bình Giữ Nhiệt Monster (Trị giá 280K)`
- Image: `assets/images/monster/original.webp`
- Price: `918.000đ`

The user requested to change this order into a **Sting** product:
- Product: `1x Thùng 24 Lon Sting Dâu Tây Đỏ 330ml`
- Subtitle (Choice A): `Thương hiệu: Sting PepsiCo` (consistent with the subtitle pattern of `#EB-2024`: `Thương hiệu: Redbull Thái Lan`)
- Image: `assets/images/sting/sting-dau.webp`
- Price: Adjusted to standard retail case price of `268.000đ`
- Reorder toast: `"Đã thêm lại Thùng 24 lon Sting Dâu vào giỏ hàng!"`

---

## 2. Proposed Architecture & UI Specifications

### 2.1 Order #EB-2026 Action Column (Option 1)
In `pages/orders.html`, update the action buttons inside `.btn-view-detail` container:
```html
<div style="display: flex; gap: 6px; align-items: center; flex-wrap: wrap;">
  <a href="order-detail.html?id=EB-2026" class="btn-view-detail" style="padding: 6px 12px; font-size: 0.8rem; text-decoration: none;">
    <i class="fas fa-file-invoice"></i> Chi Tiết
  </a>
  <button class="btn-view-detail" style="padding: 6px 12px; font-size: 0.8rem;" onclick="showToast('Đã thêm lại Monster &amp; Redbull vào giỏ hàng!', 'success')">
    <i class="fas fa-cart-plus"></i> Mua Lại
  </button>
  <button class="btn-view-detail" style="padding: 6px 12px; font-size: 0.8rem;" onclick="showToast('Đơn #EB-2026 đang được tài xế hỏa tốc giao đến bạn!', 'info')">
    <i class="fas fa-location-dot"></i> Định Vị
  </button>
</div>
```

### 2.2 Order #EB-2025 Content Synchronization
Synchronize across three layers:

#### Layer 1: Orders Table (`pages/orders.html`)
- Image: `../assets/images/sting/sting-dau.webp` (alt: `Sting Dâu Tây Đỏ`)
- Title: `1x Thùng 24 Lon Sting Dâu Tây Đỏ 330ml`
- Subtitle: `<span style="font-size: 0.8rem; color: var(--text-muted);">Thương hiệu: Sting PepsiCo</span>`
- Price: `<strong style="color: var(--primary); font-size: 1.05rem;">268.000đ</strong><br><span style="font-size: 0.75rem; color: var(--text-dim);">Chuyển khoản VietQR</span>`
- Toast: `showToast('Đã thêm lại Thùng 24 lon Sting Dâu vào giỏ hàng!', 'success')`

#### Layer 2: Account Dashboard (`pages/account.html`)
- Image: `../assets/images/sting/sting-dau.webp`
- Title: `1x Thùng 24 Lon Sting Dâu Tây Đỏ Sleek 330ml`
- Subtitle: `<div style="font-size: 0.78rem; color: var(--text-muted);">Thương hiệu: Sting PepsiCo</div>`
- Price: `Tổng thanh toán: <strong style="color: var(--primary); font-size: 1.05rem;">268.000đ</strong> (VietQR)`
- Toast: `showToast('Đã thêm lại Thùng 24 lon Sting Dâu vào giỏ!', 'success')`

#### Layer 3: Mock Order Database (`js/app.js`)
Update `MOCK_ORDER_DATABASE['EB-2025']`:
```javascript
  'EB-2025': {
    id: 'EB-2025',
    code: 'EB-2025',
    customerName: 'Thuận Trần',
    phone: '0912.888.999',
    address: '88 Nguyễn Huệ, Bến Nghé, Quận 1, TP.HCM',
    date: '28/09/2026 15:45 PM',
    status: 'ĐÃ NHẬN',
    statusClass: 'success',
    paymentMethod: 'Chuyển khoản VietQR',
    shippingMethod: 'Giao hàng tiêu chuẩn',
    notes: 'Thùng 24 lon Sting Dâu Tây Đỏ chính hãng PepsiCo',
    items: [
      {
        name: 'Thùng 24 Lon Sting Dâu Tây Đỏ Sleek 330ml',
        desc: 'Thương hiệu: Sting PepsiCo',
        img: '../assets/images/sting/sting-dau.webp',
        qty: 1,
        price: '268.000đ',
        total: '268.000đ'
      }
    ],
    subtotal: '268.000đ',
    shippingFee: '0đ (Miễn phí)',
    discount: '0đ',
    totalAmount: '268.000đ'
  },
```

---

## 3. Automated Verification Strategy

Create `scripts/verify_orders_shipping_reorder_and_sting_eb2025.py`:
1. Assert `#EB-2026` in `pages/orders.html` contains all 3 action buttons: `Chi Tiết`, `Mua Lại` (`fas fa-cart-plus`), and `Định Vị` (`fas fa-location-dot`).
2. Assert `#EB-2025` in `pages/orders.html` displays:
   - `sting-dau.webp`
   - `Thùng 24 Lon Sting Dâu Tây Đỏ`
   - `Thương hiệu: Sting PepsiCo`
   - `268.000đ`
   - Does NOT contain `Combo Thùng 24 Lon Đấu Trường` or `Bình Giữ Nhiệt Monster`.
3. Assert `pages/account.html` has synchronized `#EB-2025` with `sting-dau.webp`, `268.000đ`, and `Sting PepsiCo`.
4. Assert `js/app.js` `MOCK_ORDER_DATABASE['EB-2025']` has updated items, image, and total amount to `268.000đ`.
5. Run existing 8 test suites to verify 0 regressions.
