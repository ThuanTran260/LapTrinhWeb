import os
import re
import sys
import subprocess

# Ensure execution from project root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT_DIR)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

checks = []

def check(name, condition, details=""):
    checks.append((name, condition, details))
    mark = "PASS" if condition else "FAIL"
    print(f"[{mark}] {name} - {details}")

print("=== VERIFY ADVANCED SEARCH SIDEBAR & SEARCH RESULTS PAGE ===")

# 1. Check index.html 2-column catalog layout & sidebar
idx_content = open("index.html", encoding="utf-8").read()
check("index.html layout", "catalog-dashboard-layout" in idx_content, "index.html has .catalog-dashboard-layout")
check("index.html sidebar", "dashboard-filter-sidebar" in idx_content, "index.html has .dashboard-filter-sidebar")
check("index.html sidebar form", 'id="sidebar-filter-form"' in idx_content, "index.html has #sidebar-filter-form")
check("index.html keyword input", 'id="sidebar-filter-keyword"' in idx_content, "index.html has keyword input in sidebar")
check("index.html brand radio", 'name="sidebar-brand"' in idx_content, "index.html has brand radios in sidebar")
check("index.html price radio", 'name="sidebar-price"' in idx_content, "index.html has price radios in sidebar")
check("index.html filter reset button", 'onclick="resetDashboardFilter()"' in idx_content, "index.html has reset button")
check("index.html search page link", 'onclick="openSearchResultsFromDashboard()"' in idx_content, "index.html has shortcut to dedicated search page")
check("index.html keeps modal-adv-search", 'id="modal-adv-search"' in idx_content, "index.html preserves #modal-adv-search for Rubric 1.4")

# 2. Check pages/cart.html header synchronization & title placement
cart_content = open("pages/cart.html", encoding="utf-8").read()
check("cart.html search box", 'class="search-box"' in cart_content, "cart.html has search-box")
check("cart.html search input", 'class="search-input"' in cart_content, "cart.html has search-input")
check("cart.html adv search modal", 'id="modal-adv-search"' in cart_content, "cart.html has #modal-adv-search")
check("cart.html orders action", 'href="orders.html"' in cart_content and "Đơn hàng" in cart_content, "cart.html has orders action button")
check("cart.html account action", 'id="header-account-link"' in cart_content, "cart.html has account action button")
check("cart.html cart badge", 'class="action-badge">7<' in cart_content or '<span class="action-badge">7</span>' in cart_content, "cart.html has cart badge 7")
check("cart.html cart price", "216.000đ" in cart_content, "cart.html has price 216.000đ")
check("cart.html heading moved", 'class="cart-page-title"' in cart_content and "GIỎ HÀNG CỦA BẠN (7 LON - 216.000đ)" in cart_content, "cart title is in page body")

# 3. Check pages/search-results.html
check("search-results.html exists", os.path.exists("pages/search-results.html"), "pages/search-results.html exists")
search_content = open("pages/search-results.html", encoding="utf-8").read()
check("search-results layout", "catalog-dashboard-layout" in search_content, "search-results has .catalog-dashboard-layout")
check("search-results grid", 'id="search-results-grid"' in search_content, "search-results has #search-results-grid")
check("search-results sidebar", "sidebar-filter-card" in search_content, "search-results has .sidebar-filter-card")
check("search-results pagination", "pagination-strip" in search_content and "page-btn" in search_content, "search-results has pagination strip")
check("search-results toast container", 'id="toast-container"' in search_content, "search-results has #toast-container")

# 4. Check css/style.css
css_content = open("css/style.css", encoding="utf-8").read()
check("css layout grid", ".catalog-dashboard-layout" in css_content, "style.css defines .catalog-dashboard-layout")
check("css sidebar card", ".sidebar-filter-card" in css_content, "style.css defines .sidebar-filter-card")
check("css sticky 90px", "top: 90px;" in css_content, "style.css defines top: 90px for desktop sticky")
check("css responsive static", "position: static;" in css_content and "top: auto;" in css_content, "style.css sets position static on mobile/tablet <= 1024px")

# 5. Check js/app.js search logic with node
node_script = """
const fs = require('fs');
const code = fs.readFileSync('js/app.js', 'utf8');
const vm = require('vm');
const sandbox = { 
  window: { 
    location: { pathname: '/pages/search-results.html', href: 'http://localhost/pages/search-results.html' },
    addEventListener: () => {}
  },
  document: { 
    currentScript: { src: 'http://localhost/js/app.js' },
    querySelector: () => null,
    querySelectorAll: () => [],
    getElementById: () => null,
    addEventListener: () => {}
  },
  console: console
};
vm.createContext(sandbox);
vm.runInContext(code, sandbox);

const testBoost = sandbox.filterProducts('/boost', 'all', 'all');
if (testBoost.length !== 10) throw new Error('Expected 10 for /boost, got ' + testBoost.length);

const testMonster = sandbox.filterProducts('Monster', 'all', 'all');
if (testMonster.length !== 4) throw new Error('Expected 4 for Monster, got ' + testMonster.length);

const testRedbull = sandbox.filterProducts('Redbull', 'all', 'all');
if (testRedbull.length !== 3) throw new Error('Expected 3 for Redbull, got ' + testRedbull.length);

const testSting = sandbox.filterProducts('Sting', 'all', 'all');
if (testSting.length !== 3) throw new Error('Expected 3 for Sting, got ' + testSting.length);

const testPriceUnder20 = sandbox.filterProducts('', 'all', 'under20');
if (testPriceUnder20.length !== 5) throw new Error('Expected 5 for under20, got ' + testPriceUnder20.length);

console.log('NODE_SEARCH_OK');
"""

try:
    res = subprocess.run(["node", "-e", node_script], capture_output=True, text=True, check=True)
    check("js search unit tests", "NODE_SEARCH_OK" in res.stdout, "filterProducts handles /boost, brands, price successfully")
except Exception as err:
    check("js search unit tests", False, f"Failed node unit tests: {err}")

failed = [c for c in checks if not c[1]]
print(f"\nResult: {len(checks) - len(failed)}/{len(checks)} passed.")
if failed:
    print(f"FAILED {len(failed)} checks.")
    sys.exit(1)
else:
    print("ALL SEARCH CHECKS PASSED PERFECTLY!")
    sys.exit(0)
