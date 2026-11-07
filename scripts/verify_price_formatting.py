#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification Script for Admin Inventory Price Formatting & Real-time Preview Feature.
Tests:
1. CSS style definitions for currency formatting and live preview components.
2. HTML structure in admin/inventory.html, admin/index.html, and admin/edit-*.html.
3. JavaScript logic in js/app.js for formatting, parsing, Vietnamese number words,
   cursor restoration, and DOM initialization.
4. Functional verification via Node.js execution.
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
errors = []
successes = []

def check(condition, desc):
    if condition:
        successes.append(f"✅ PASS: [{desc}]")
        print(f"✅ PASS: [{desc}]")
    else:
        errors.append(f"❌ FAIL: [{desc}]")
        print(f"❌ FAIL: [{desc}]")

def read_file(rel_path):
    abs_path = os.path.join(workspace, rel_path)
    if not os.path.exists(abs_path):
        return None
    with open(abs_path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    print("=" * 75)
    print("XÁC MINH TÍNH NĂNG FORMAT GIÁ TIỀN & XEM TRƯỚC TRONG KHO SẢN PHẨM ADMIN")
    print("=" * 75)

    # 1. Check CSS style definitions
    css = read_file('css/style.css')
    check(css is not None, "style.css tồn tại")
    if css:
        check('.price-preview-tag' in css, "style.css có class .price-preview-tag")
        check('.price-format-input' in css, "style.css có class .price-format-input")
        check('.price-preview-val' in css, "style.css có class .price-preview-val")
        check('.price-preview-words' in css, "style.css có class .price-preview-words")

    # 2. Check admin/inventory.html
    inv = read_file('admin/inventory.html')
    check(inv is not None, "admin/inventory.html tồn tại")
    if inv:
        check('id="edit-prod-price"' in inv and 'price-format-input' in inv, 
              "admin/inventory.html: edit-prod-price có class price-format-input")
        check('id="preview-edit-prod-price"' not in inv, 
              "admin/inventory.html: ĐÃ XÓA preview tag id=preview-edit-prod-price")
        check('id="preview-edit-prod-oldprice"' not in inv, 
              "admin/inventory.html: ĐÃ XÓA preview tag id=preview-edit-prod-oldprice")
        check('id="preview-add-prod-price"' not in inv, 
              "admin/inventory.html: ĐÃ XÓA preview tag id=preview-add-prod-price")

    # 3. Check admin/index.html
    adm_idx = read_file('admin/index.html')
    check(adm_idx is not None, "admin/index.html tồn tại")
    if adm_idx:
        check('id="preview-edit-prod-price"' not in adm_idx, 
              "admin/index.html: modal edit ĐÃ XÓA preview tag preview-edit-prod-price")
        check('id="preview-edit-prod-oldprice"' not in adm_idx, 
              "admin/index.html: modal edit ĐÃ XÓA preview tag preview-edit-prod-oldprice")
        check('id="preview-add-prod-price"' not in adm_idx, 
              "admin/index.html: modal add ĐÃ XÓA preview tag preview-add-prod-price")

    # 4. Check standalone edit pages
    edit_pages = [
        ('admin/edit-monster.html', '45.000đ', '55.000đ'),
        ('admin/edit-redbull-lonvua.html', '20.000đ', '25.000đ'),
        ('admin/edit-redbull-original.html', '18.000đ', '22.000đ'),
        ('admin/edit-redbull-thai.html', '18.000đ', '22.000đ'),
        ('admin/edit-sting.html', '12.000đ', '15.000đ')
    ]
    for page_path, price, oldprice in edit_pages:
        content = read_file(page_path)
        check(content is not None, f"{page_path} tồn tại")
        if content:
            check('id="standalone-edit-price"' in content, 
                  f"{page_path}: có input id=standalone-edit-price")
            check('id="preview-standalone-edit-price"' not in content, 
                  f"{page_path}: ĐÃ XÓA preview tag preview-standalone-edit-price")
            check('id="preview-standalone-edit-oldprice"' not in content, 
                  f"{page_path}: ĐÃ XÓA preview tag preview-standalone-edit-oldprice")
            check('id="standalone-card-price-display"' in content, 
                  f"{page_path}: có thẻ hiển thị giá card id=standalone-card-price-display")

    # 5. Check js/app.js structure
    app_js = read_file('js/app.js')
    check(app_js is not None, "js/app.js tồn tại")
    if app_js:
        check('function formatCurrencyVND' in app_js, "js/app.js có hàm formatCurrencyVND")
        check('function parseCurrencyVND' in app_js, "js/app.js có hàm parseCurrencyVND")
        check('function numberToVietnameseWords' in app_js, "js/app.js có hàm numberToVietnameseWords")
        check('function updatePricePreview' in app_js, "js/app.js có hàm updatePricePreview")
        check('function syncStandaloneCardPrice' in app_js, "js/app.js có hàm syncStandaloneCardPrice")
        check('function restoreCursorPosition' in app_js, "js/app.js có hàm restoreCursorPosition")
        check('function setupPriceInput' in app_js, "js/app.js có hàm setupPriceInput")
        check('function initPriceFormatting' in app_js, "js/app.js có hàm initPriceFormatting")

    # 6. Functional tests with Node.js
    node_test = """
    const fs = require('fs');
    const path = require('path');
    const vm = require('vm');
    const code = fs.readFileSync(path.join(__dirname, 'js', 'app.js'), 'utf-8');

    const sandbox = {
      window: { addEventListener: () => {} },
      document: {
        readyState: 'complete',
        addEventListener: () => {},
        querySelectorAll: () => [],
        querySelector: () => null,
        getElementById: () => null
      },
      console: console,
      parseInt: parseInt,
      Math: Math,
      Number: Number,
      String: String
    };
    vm.createContext(sandbox);
    vm.runInContext(code, sandbox);

    const { formatCurrencyVND, numberToVietnameseWords, parseCurrencyVND } = sandbox;

    // Test cases
    const tests = [
      { num: 45000, formatted: '45.000đ', words: 'Bốn mươi lăm nghìn đồng' },
      { num: 18000, formatted: '18.000đ', words: 'Mười tám nghìn đồng' },
      { num: 20000, formatted: '20.000đ', words: 'Hai mươi nghìn đồng' },
      { num: 12000, formatted: '12.000đ', words: 'Mười hai nghìn đồng' },
      { num: 450000, formatted: '450.000đ', words: 'Bốn trăm năm mươi nghìn đồng' },
      { num: 1250000, formatted: '1.250.000đ', words: 'Một triệu hai trăm năm mươi nghìn đồng' },
      { num: 0, formatted: '0đ', words: 'Không đồng' }
    ];

    let failed = false;
    for (const t of tests) {
      const f = formatCurrencyVND(t.num);
      const w = numberToVietnameseWords(t.num);
      if (f !== t.formatted) {
        console.error('Format mismatch for', t.num, 'expected:', t.formatted, 'got:', f);
        failed = true;
      }
      if (w !== t.words) {
        console.error('Words mismatch for', t.num, 'expected:', t.words, 'got:', w);
        failed = true;
      }
    }

    if (parseCurrencyVND('45.000đ') !== 45000) {
      console.error('parseCurrencyVND failed');
      failed = true;
    }

    // Additional robustness checks: string tolerance
    if (numberToVietnameseWords('45.000đ') !== 'Bốn mươi lăm nghìn đồng') {
      console.error('numberToVietnameseWords with formatted string failed');
      failed = true;
    }
    if (numberToVietnameseWords('12000') !== 'Mười hai nghìn đồng') {
      console.error('numberToVietnameseWords with raw string failed');
      failed = true;
    }
    if (formatCurrencyVND('45.000đ') !== '45.000đ') {
      console.error('formatCurrencyVND with string failed');
      failed = true;
    }

    if (failed) process.exit(1);
    console.log('NODE_SUCCESS');
    """
    proc = subprocess.run(['node', '-e', node_test], cwd=workspace, capture_output=True, text=True)
    check(proc.returncode == 0 and 'NODE_SUCCESS' in proc.stdout, 
          "Node.js functional execution: formatCurrencyVND & numberToVietnameseWords pass 100%")

    print("=" * 75)
    print(f"KẾT QUẢ: {len(successes)}/{len(successes) + len(errors)} TIÊU CHÍ ĐẠT")
    print("=" * 75)

    if errors:
        sys.exit(1)
    else:
        print("🎉 TẤT CẢ KIỂM THỬ ĐỊNH DẠNG GIÁ TIỀN & XEM TRƯỚC ĐỀU THÀNH CÔNG RỰC RỠ!")
        sys.exit(0)

if __name__ == '__main__':
    main()
