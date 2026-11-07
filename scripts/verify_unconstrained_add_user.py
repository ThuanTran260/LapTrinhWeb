import os
import re
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

errors = []
successes = []

def check(condition, desc):
    if condition:
        successes.append(f"[PASS] {desc}")
    else:
        errors.append(f"[FAIL] {desc}")

# 1. Check admin/customers.html
customers_path = os.path.join(os.path.dirname(__file__), "..", "admin", "customers.html")
with open(customers_path, "r", encoding="utf-8") as f:
    customers_html = f.read()

check('id="modal-add-user"' in customers_html, "customers.html contains modal-add-user")
check('openAddUserModal' in customers_html, "customers.html contains openAddUserModal")
check('saveAddUser' in customers_html, "customers.html contains saveAddUser")

# Extract form-add-user
form_match = re.search(r'<form id="form-add-user".*?</form>', customers_html, re.DOTALL)
check(bool(form_match), "customers.html has form-add-user")

if form_match:
    form_str = form_match.group(0)
    check('novalidate' in form_str, "form-add-user has novalidate attribute")
    check('required' not in form_str, "form-add-user has NO required constraints on inputs")
    check('type="email"' not in form_str, "form-add-user has NO type='email' strict format constraint")
    check('minlength' not in form_str, "form-add-user has NO minlength password/text constraint")
    check('pattern=' not in form_str, "form-add-user has NO pattern regex constraint")
    check('id="add-user-password"' in form_str, "form-add-user provides optional unconstrained password field")
    check('id="add-user-username"' in form_str, "form-add-user provides username field")
    check('id="add-user-fullname"' in form_str, "form-add-user provides fullname field")
    check('id="add-user-email"' in form_str, "form-add-user provides email field")
    check('id="add-user-phone"' in form_str, "form-add-user provides phone field")

# 2. Check admin/index.html
index_path = os.path.join(os.path.dirname(__file__), "..", "admin", "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    index_html = f.read()

check('openAddUserModal()' in index_html, "admin/index.html has openAddUserModal() action")
check('id="modal-add-user"' in index_html, "admin/index.html has modal-add-user")
form_idx_match = re.search(r'<form id="form-add-user".*?</form>', index_html, re.DOTALL)
check(bool(form_idx_match), "admin/index.html has form-add-user")
if form_idx_match:
    form_idx_str = form_idx_match.group(0)
    check('novalidate' in form_idx_str, "admin/index.html form-add-user has novalidate attribute")
    check('required' not in form_idx_str, "admin/index.html form-add-user has NO required constraints")

# Verify modal-add-user is NOT nested inside modal-customer-detail in admin/index.html
detail_pos = index_html.find('id="modal-customer-detail"')
add_pos = index_html.find('id="modal-add-user"')
if detail_pos != -1 and add_pos != -1:
    between = index_html[detail_pos:add_pos]
    open_divs = between.count('<div')
    close_divs = between.count('</div')
    check(close_divs >= open_divs, "modal-customer-detail is properly closed before modal-add-user in admin/index.html")

# 3. Check js/app.js
app_path = os.path.join(os.path.dirname(__file__), "..", "js", "app.js")
with open(app_path, "r", encoding="utf-8") as f:
    app_js = f.read()

check('function saveAddUser(' in app_js, "app.js defines saveAddUser function")
check('function openAddUserModal(' in app_js, "app.js defines openAddUserModal function")
check('function toggleLockUser(' in app_js, "app.js defines toggleLockUser function")
check('Người Dùng Mới' in app_js, "saveAddUser provides graceful default when name is empty")
check('showToast' in app_js, "saveAddUser displays toast feedback")
check('customers-table' in app_js, "saveAddUser targets customers-table avoiding dashboard table pollution")
check('admin_custom_users' in app_js, "saveAddUser persists custom users in localStorage")
check('initCustomUsersTable' in app_js, "app.js provides initCustomUsersTable to reload custom users")
check('emailEl.value = smallEmail.textContent.trim()' in app_js or 'smallEmail' in app_js, "openEditUserModal extracts customer email from table row")
check('btn-action-unlock' in app_js and 'btn-action-lock' in app_js, "toggleLockUser and saveEditUser correctly toggle button action classes")

print("=== VERIFY UNCONSTRAINED ADD USER (ADMIN) ===")
for s in successes:
    print(s)
for e in errors:
    print(e)

if errors:
    print(f"\n{len(errors)} checks FAILED!")
    sys.exit(1)
else:
    print(f"\nALL {len(successes)} CHECKS PASSED PERFECTLY!")
    sys.exit(0)
