import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

SIDEBAR_FILES = [
    "admin/index.html",
    "admin/orders.html",
    "admin/inventory.html",
    "admin/revenue.html",
    "admin/customers.html",
    "admin/settings.html",
    "admin/order-detail.html",
    "admin/edit-monster.html",
    "admin/edit-redbull-lonvua.html",
    "admin/edit-redbull-original.html",
    "admin/edit-redbull-thai.html",
    "admin/edit-sting.html",
]


def main() -> int:
    failures = []

    for rel_path in SIDEBAR_FILES:
        text = (ROOT / rel_path).read_text(encoding="utf-8")
        if '<i class="fas fa-users"></i> Khách Hàng VIP</a>' in text:
            failures.append(f"{rel_path}: sidebar still says 'Khách Hàng VIP'")
        if '<i class="fas fa-users"></i> Khách Hàng</a>' not in text:
            failures.append(f"{rel_path}: sidebar missing 'Khách Hàng' link")

    for page_rel in ("admin/orders.html", "admin/index.html"):
        text = (ROOT / page_rel).read_text(encoding="utf-8")
        if 'id="modal-customer-detail"' in text:
            failures.append(f"{page_rel}: still contains popup #modal-customer-detail")
        if "openCustomerDetailModal(" in text:
            failures.append(f"{page_rel}: still calls openCustomerDetailModal popup trigger")
        links = re.findall(r'<a\s+href="customer-detail\.html"[^>]*>', text)
        if len(links) < 6:
            failures.append(f"{page_rel}: expected >= 6 links to customer-detail.html, found {len(links)}")

    if failures:
        print(f"FAIL ({len(failures)} checks failed):")
        for item in failures:
            print(f"  - {item}")
        return 1

    print("ALL CHECKS PASSED: Admin sidebars say 'Khách Hàng' and orders/dashboard link to customer-detail.html.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
