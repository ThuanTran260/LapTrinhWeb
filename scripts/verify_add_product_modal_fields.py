#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification Script for Full Add-Product Modal Fields & Price Formatting.
Checks:
1. Both admin/inventory.html and admin/index.html #modal-add-product blocks contain
   all 12 exact labels, all 3 stock status options, all 14 required IDs, and 'Hủy Bỏ'.
2. Both #modal-add-product blocks match structurally and exclude 'preview-add-prod-price'.
3. js/app.js registers '#add-prod-oldprice' in initPriceFormatting() and handles
   both 'add-prod-price' and 'add-prod-oldprice' in openAddProductModal() / saveAddProduct().
4. Node.js VM runtime smoke test executing openAddProductModal() and saveAddProduct(event).
"""
import os
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_LABELS = [
    "Tên Sản Phẩm Đầy Đủ",
    "Thương Hiệu",
    "Sản Xuất Tại",
    "Giá Bán Lẻ Hiện Tại",
    "Giá Niêm Yết Cũ",
    "Thể Tích / Quy Cách",
    "Hương Vị Đặc Trưng",
    "Thành Phần",
    "Hướng Dẫn Sử Dụng",
    "Bảo Quản",
    "Trạng Thái Kho",
    "Số Lượng Tồn Kho Thực Tế",
]

REQUIRED_STOCK_OPTIONS = [
    "Còn hàng",
    "Sắp hết hàng",
    "Tạm hết hàng",
]

REQUIRED_IDS = [
    "add-prod-name",
    "add-prod-file",
    "add-prod-preview",
    "add-prod-brand",
    "add-prod-origin",
    "add-prod-price",
    "add-prod-oldprice",
    "add-prod-volume",
    "add-prod-flavor",
    "add-prod-ingredients",
    "add-prod-usage",
    "add-prod-storage",
    "add-prod-status",
    "add-prod-stock",
]

PROHIBITED_TOKEN = "preview-add-prod-price"


def extract_div_block(html: str, class_or_id_pattern: str) -> str:
    match = re.search(rf"<div\b[^>]*{class_or_id_pattern}[^>]*>", html)
    if not match:
        return ""
    depth = 1
    pos = match.end()
    for tag in re.finditer(r"<(/?)div\b[^>]*>", html[pos:]):
        depth += -1 if tag.group(1) else 1
        if depth == 0:
            return html[match.start() : pos + tag.end()]
    return ""


def extract_js_function(js_code: str, func_name: str) -> str:
    match = re.search(rf"function\s+{re.escape(func_name)}\s*\([^)]*\)\s*\{{", js_code)
    if not match:
        return ""
    depth = 1
    pos = match.end()
    while pos < len(js_code) and depth > 0:
        ch = js_code[pos]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        pos += 1
    return js_code[match.start() : pos] if depth == 0 else ""


def check_modal_html(rel_path: str, html: str, failures: list[str]) -> str:
    modal_block = extract_div_block(html, r'id="modal-add-product"')
    if not modal_block:
        failures.append(f"{rel_path}: missing #modal-add-product block")
        return ""

    for label in REQUIRED_LABELS:
        if label not in modal_block:
            failures.append(f"{rel_path}: #modal-add-product missing label '{label}'")

    status_match = re.search(
        r'<select\b[^>]*id="add-prod-status"[^>]*>([\s\S]*?)</select>', modal_block
    )
    if not status_match:
        failures.append(f"{rel_path}: #modal-add-product missing <select id='add-prod-status'>")
    else:
        status_html = status_match.group(1)
        for option in REQUIRED_STOCK_OPTIONS:
            if not re.search(
                rf'<option\b[^>]*value="{re.escape(option)}"[^>]*>\s*{re.escape(option)}\s*</option>',
                status_html,
            ):
                failures.append(
                    f"{rel_path}: #add-prod-status missing stock option '{option}'"
                )

    for elem_id in REQUIRED_IDS:
        if not re.search(rf'\bid="{re.escape(elem_id)}"', modal_block):
            failures.append(f"{rel_path}: #modal-add-product missing id='{elem_id}'")

    if "Hủy Bỏ" not in modal_block:
        failures.append(f"{rel_path}: #modal-add-product missing 'Hủy Bỏ' button text")

    if PROHIBITED_TOKEN in html:
        failures.append(f"{rel_path}: prohibited token '{PROHIBITED_TOKEN}' must not exist")

    return modal_block


def check_js_wiring(js_code: str, failures: list[str]) -> None:
    init_fn = extract_js_function(js_code, "initPriceFormatting")
    if not init_fn:
        failures.append("js/app.js: missing initPriceFormatting()")
    else:
        if "'#add-prod-price'" not in init_fn and '"#add-prod-price"' not in init_fn:
            failures.append("js/app.js: initPriceFormatting() missing '#add-prod-price'")
        if "'#add-prod-oldprice'" not in init_fn and '"#add-prod-oldprice"' not in init_fn:
            failures.append("js/app.js: initPriceFormatting() missing '#add-prod-oldprice'")

    open_fn = extract_js_function(js_code, "openAddProductModal")
    save_fn = extract_js_function(js_code, "saveAddProduct")
    refresh_fn = extract_js_function(js_code, "refreshAddProductPriceInputs")

    if not open_fn:
        failures.append("js/app.js: missing openAddProductModal()")
    if not save_fn:
        failures.append("js/app.js: missing saveAddProduct(e)")

    add_price_handled_in_open = (
        ("add-prod-price" in open_fn and "add-prod-oldprice" in open_fn)
        or (
            "refreshAddProductPriceInputs(true)" in open_fn
            and "add-prod-price" in refresh_fn
            and "add-prod-oldprice" in refresh_fn
        )
    )
    if not add_price_handled_in_open:
        failures.append(
            "js/app.js: openAddProductModal() must handle both add-prod-price and add-prod-oldprice"
        )

    add_price_handled_in_save = (
        ("add-prod-price" in save_fn and "add-prod-oldprice" in save_fn)
        or (
            "refreshAddProductPriceInputs(false)" in save_fn
            and "add-prod-price" in refresh_fn
            and "add-prod-oldprice" in refresh_fn
        )
    )
    if not add_price_handled_in_save:
        failures.append(
            "js/app.js: saveAddProduct() must handle both add-prod-price and add-prod-oldprice"
        )


def run_node_vm_smoke_test(failures: list[str]) -> None:
    node_script = r"""
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const code = fs.readFileSync(path.join(process.cwd(), 'js', 'app.js'), 'utf-8');

function makeClassList(initial = []) {
  const set = new Set(initial);
  return {
    add(cls) { set.add(cls); },
    remove(cls) { set.delete(cls); },
    contains(cls) { return set.has(cls); }
  };
}

function makeInput(id) {
  const listeners = {};
  const el = {
    id,
    type: 'text',
    value: '',
    selectionStart: 0,
    selectionEnd: 0,
    dataset: {},
    classList: makeClassList(['admin-form-input']),
    addEventListener(type, fn) {
      listeners[type] = listeners[type] || [];
      listeners[type].push(fn);
    },
    trigger(type, eventObj = {}) {
      (listeners[type] || []).forEach(fn => fn.call(el, eventObj));
    },
    setSelectionRange(start, end) {
      el.selectionStart = start;
      el.selectionEnd = end;
    },
    closest() { return null; },
    parentElement: null
  };
  return el;
}

const nameInput = makeInput('add-prod-name');
const priceInput = makeInput('add-prod-price');
const oldPriceInput = makeInput('add-prod-oldprice');

const modal = {
  id: 'modal-add-product',
  classList: makeClassList(['admin-modal-overlay'])
};

let resetCount = 0;
const form = {
  id: 'form-add-product',
  reset() {
    resetCount += 1;
    nameInput.value = '';
    priceInput.value = '';
    oldPriceInput.value = '';
  }
};

const previewImgs = [
  { hidden: false, src: 'old.png', removeAttribute(attr) { if (attr === 'src') this.src = ''; } },
  { hidden: false, src: 'old2.png', removeAttribute(attr) { if (attr === 'src') this.src = ''; } },
  { hidden: false, src: 'old3.png', removeAttribute(attr) { if (attr === 'src') this.src = ''; } }
];
const extraRow = { removed: false, remove() { this.removed = true; } };
const imagesList = {
  id: 'add-product-images',
  children: [{}, {}, {}, extraRow],
  querySelectorAll(sel) {
    return sel === '.product-image-preview' ? previewImgs : [];
  }
};

const toasts = [];
const toastContainer = {
  id: 'toast-container',
  appendChild(node) { toasts.push(node); }
};

const elementsById = {
  'modal-add-product': modal,
  'form-add-product': form,
  'add-product-images': imagesList,
  'add-prod-name': nameInput,
  'add-prod-price': priceInput,
  'add-prod-oldprice': oldPriceInput,
  'toast-container': toastContainer
};

const sandbox = {
  window: { addEventListener: () => {} },
  document: {
    readyState: 'complete',
    body: { style: { overflow: '' }, appendChild: () => {} },
    addEventListener: () => {},
    querySelectorAll: (sel) => {
      if (sel === '.admin-modal-overlay.active') {
        return modal.classList.contains('active') ? [modal] : [];
      }
      return [];
    },
    querySelector: () => null,
    getElementById: (id) => elementsById[id] || null,
    createElement: (tag) => ({
      tagName: tag.toUpperCase(),
      className: '',
      innerHTML: '',
      style: {},
      parentNode: null
    })
  },
  console,
  parseInt,
  Math,
  Number,
  String,
  Array,
  Set,
  setTimeout: () => 0
};

vm.createContext(sandbox);
vm.runInContext(code, sandbox);

if (typeof sandbox.openAddProductModal !== 'function') {
  throw new Error('openAddProductModal is not a function');
}
if (typeof sandbox.saveAddProduct !== 'function') {
  throw new Error('saveAddProduct is not a function');
}

sandbox.openAddProductModal();

if (resetCount !== 1) {
  throw new Error('Expected form.reset() on openAddProductModal(), count=' + resetCount);
}
if (!modal.classList.contains('active')) {
  throw new Error('Expected #modal-add-product to have active class after openAddProductModal()');
}
if (!extraRow.removed) {
  throw new Error('Expected extra image row to be removed on openAddProductModal()');
}
if (previewImgs.some(img => !img.hidden || img.src !== '')) {
  throw new Error('Expected preview images to be reset on openAddProductModal()');
}
if (priceInput.dataset.priceBound !== 'true' || oldPriceInput.dataset.priceBound !== 'true') {
  throw new Error('Expected both price inputs to be bound via setupPriceInput');
}

priceInput.value = '48000';
priceInput.selectionStart = 5;
priceInput.trigger('input');
if (priceInput.value !== '48.000đ') {
  throw new Error('Expected add-prod-price formatted as 48.000đ, got: ' + priceInput.value);
}

oldPriceInput.value = '55000';
oldPriceInput.selectionStart = 5;
oldPriceInput.trigger('input');
if (oldPriceInput.value !== '55.000đ') {
  throw new Error('Expected add-prod-oldprice formatted as 55.000đ, got: ' + oldPriceInput.value);
}

nameInput.value = 'Monster Ultra Sunrise 500ml';
let prevented = false;
sandbox.saveAddProduct({ preventDefault: () => { prevented = true; } });

if (!prevented) {
  throw new Error('Expected event.preventDefault() to be called in saveAddProduct');
}
if (modal.classList.contains('active')) {
  throw new Error('Expected #modal-add-product to close after saveAddProduct()');
}
if (resetCount !== 2) {
  throw new Error('Expected form.reset() on saveAddProduct(), count=' + resetCount);
}
if (priceInput.value !== '' || oldPriceInput.value !== '') {
  throw new Error('Expected price inputs cleared after saveAddProduct()');
}
if (toasts.length !== 1 || !toasts[0].innerHTML.includes('Monster Ultra Sunrise 500ml')) {
  throw new Error('Expected success toast containing product name');
}

console.log('NODE_ADD_MODAL_SMOKE_PASS');
"""
    proc = subprocess.run(
        ["node", "-e", node_script],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if proc.returncode != 0 or "NODE_ADD_MODAL_SMOKE_PASS" not in proc.stdout:
        stderr = (proc.stderr or "").strip()
        stdout = (proc.stdout or "").strip()
        failures.append(
            f"Node.js VM smoke test failed (exit={proc.returncode}): {stderr or stdout}"
        )


def main() -> int:
    failures: list[str] = []

    inv_path = ROOT / "admin" / "inventory.html"
    idx_path = ROOT / "admin" / "index.html"
    js_path = ROOT / "js" / "app.js"

    for p in (inv_path, idx_path, js_path):
        if not p.is_file():
            failures.append(f"Missing required file: {p.relative_to(ROOT)}")

    if not failures:
        inv_html = inv_path.read_text(encoding="utf-8")
        idx_html = idx_path.read_text(encoding="utf-8")
        js_code = js_path.read_text(encoding="utf-8")

        inv_modal = check_modal_html("admin/inventory.html", inv_html, failures)
        idx_modal = check_modal_html("admin/index.html", idx_html, failures)

        if inv_modal and idx_modal:
            norm_inv = re.sub(r"\s+", " ", inv_modal).strip()
            norm_idx = re.sub(r"\s+", " ", idx_modal).strip()
            if norm_inv != norm_idx:
                failures.append(
                    "Structural parity mismatch: #modal-add-product differs between admin/inventory.html and admin/index.html"
                )

        check_js_wiring(js_code, failures)
        run_node_vm_smoke_test(failures)

    if failures:
        print(f"FAIL ({len(failures)} checks failed):")
        for item in failures:
            print(f"  - {item}")
        return 1

    print(
        "ALL CHECKS PASSED: #modal-add-product has all 12 fields, 3 stock options, 14 IDs, structural parity across admin/inventory.html & admin/index.html, #add-prod-oldprice wiring in js/app.js, and Node.js VM smoke test passed."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
