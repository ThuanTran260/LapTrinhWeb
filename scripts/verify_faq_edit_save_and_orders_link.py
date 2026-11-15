#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification Script for:
1. "Mua Sắm Ngay" button in pages/orders.html pointing to ../index.html#monster-products.
2. FAQ form in admin/settings.html having fixed default values of FAQ #1 and "Lưu Thay Đổi" button.
3. FAQ edit in js/app.js emitting "Đã chuyển" toast without overwriting form inputs.
4. FAQ save handler emitting success toast.
"""

import os
import sys
import subprocess

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
passed = 0
failed = 0

def check(desc, condition):
    global passed, failed
    if condition:
        passed += 1
        print(f"✅ PASS: [{desc}]")
    else:
        failed += 1
        print(f"❌ FAIL: [{desc}]")

def read_file(rel_path):
    p = os.path.join(workspace, rel_path)
    if not os.path.exists(p):
        return None
    with open(p, 'r', encoding='utf-8') as f:
        return f.read()

print("=" * 80)
print("KIỂM TRA TỰ ĐỘNG: ĐIỀU HƯỚNG MUA SẮM NGAY & CỐ ĐỊNH FAQ #1 + NÚT LƯU")
print("=" * 80)

# 1. Check pages/orders.html
orders_html = read_file('pages/orders.html')
check("pages/orders.html tồn tại", orders_html is not None)
if orders_html:
    check("pages/orders.html: nút Mua Sắm Ngay trỏ ../index.html#monster-products",
          'href="../index.html#monster-products"' in orders_html and 'Mua Sắm Ngay' in orders_html)
    check("pages/orders.html: không còn href='cart.html' gắn với Mua Sắm Ngay",
          'href="cart.html" class="btn-add-cart"' not in orders_html)

# 2. Check admin/settings.html
settings_html = read_file('admin/settings.html')
check("admin/settings.html tồn tại", settings_html is not None)
if settings_html:
    check("admin/settings.html: form FAQ có sẵn câu hỏi Câu 1",
          'Các dòng nước tăng lực tại Energy Boost gồm những thương hiệu nào?' in settings_html)
    check("admin/settings.html: form FAQ có thứ tự mặc định là 1",
          'id="faq-new-order"' in settings_html and 'value="1"' in settings_html)
    check("admin/settings.html: form FAQ có câu trả lời Câu 1",
          'Energy Boost chuyên phân phối chính hãng hai dòng thương hiệu hàng đầu' in settings_html)
    check("admin/settings.html: có nút 'Lưu Thay Đổi' gọi handleAdminSaveFaq",
          'handleAdminSaveFaq()' in settings_html and 'Lưu Thay Đổi' in settings_html and 'fa-save' in settings_html)

# 3. Check js/app.js & Node.js runtime logic
app_js = read_file('js/app.js')
check("js/app.js tồn tại", app_js is not None)
if app_js:
    check("js/app.js: có hàm handleAdminSaveFaq",
          'function handleAdminSaveFaq' in app_js)

node_test_code = """
const fs = require('fs');
const js = fs.readFileSync('js/app.js', 'utf8');

const elements = {};
function mockElement(id, initialVal = '', type = 'text') {
  elements[id] = {
    id: id,
    type: type,
    value: initialVal,
    textContent: initialVal,
    innerHTML: '',
    classList: { add: () => {}, remove: () => {}, contains: () => false },
    dataset: {},
    listeners: {},
    children: [],
    appendChild: function(c) { this.children.push(c); c.parentElement = this; },
    addEventListener: function(event, handler) { this.listeners[event] = handler; },
    trigger: function(event) { if (this.listeners[event]) this.listeners[event].call(this); },
    selectionStart: initialVal.length,
    selectionEnd: initialVal.length,
    setSelectionRange: function(s, e) { this.selectionStart = s; this.selectionEnd = e; },
    closest: function() { return this; },
    remove: function() {},
    focus: function() {},
    scrollIntoView: function() {},
    querySelectorAll: function() { return []; }
  };
  return elements[id];
}

let lastToastMsg = '';
global.window = { addEventListener: () => {} };
global.document = {
  body: { appendChild: () => {} },
  getElementById: (id) => elements[id] || null,
  createElement: () => mockElement('dummy'),
  querySelectorAll: () => [],
  querySelector: () => null,
  addEventListener: () => {},
  readyState: 'complete'
};
global.showToast = function(msg) { lastToastMsg = msg; };

mockElement('faq-new-question', 'Câu hỏi 1 gốc');
mockElement('faq-new-order', '1');
mockElement('faq-new-answer', 'Câu trả lời 1 gốc');

eval(js);
global.showToast = function(msg) { lastToastMsg = msg; };

// Test 1: handleAdminEditFaq does not change form inputs, emits "Đã chuyển"
handleAdminEditFaq('2', null);
const editDidNotChangeQuestion = (elements['faq-new-question'].value === 'Câu hỏi 1 gốc');
const editDidNotChangeOrder = (elements['faq-new-order'].value === '1');
const editEmittedToast = lastToastMsg.includes('Đã chuyển');

// Test 2: handleAdminSaveFaq emits success toast
lastToastMsg = '';
handleAdminSaveFaq();
const saveEmittedToast = lastToastMsg.includes('Đã lưu thay đổi');

console.log(JSON.stringify({ editDidNotChangeQuestion, editDidNotChangeOrder, editEmittedToast, saveEmittedToast }));
"""

try:
    node_res = subprocess.run(["node", "-e", node_test_code], capture_output=True, text=True, check=True)
    import json
    results = json.loads(node_res.stdout.strip())
    check("Node.js runtime: handleAdminEditFaq không thay đổi câu hỏi trên form", results.get("editDidNotChangeQuestion", False))
    check("Node.js runtime: handleAdminEditFaq không thay đổi thứ tự trên form", results.get("editDidNotChangeOrder", False))
    check("Node.js runtime: handleAdminEditFaq kích hoạt thông báo 'Đã chuyển'", results.get("editEmittedToast", False))
    check("Node.js runtime: handleAdminSaveFaq kích hoạt thông báo 'Đã lưu thay đổi'", results.get("saveEmittedToast", False))
except Exception as e:
    check("Node.js runtime execution pass: " + str(e), False)

print("\n" + "=" * 80)
print(f"KẾT QUẢ TỔNG QUÁT: {passed}/{passed + failed} TIÊU CHÍ ĐẠT")
print("=" * 80)

sys.exit(0 if failed == 0 else 1)
