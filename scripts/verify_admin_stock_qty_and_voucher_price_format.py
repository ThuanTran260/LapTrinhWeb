# -*- coding: utf-8 -*-
"""
verify_admin_stock_qty_and_voucher_price_format.py
Wrapper redirecting to verify_admin_features_update.py
"""
import subprocess
import sys
import os

if __name__ == "__main__":
    script_path = os.path.join(os.path.dirname(__file__), "verify_admin_features_update.py")
    res = subprocess.run([sys.executable, script_path], check=False)
    sys.exit(res.returncode)
