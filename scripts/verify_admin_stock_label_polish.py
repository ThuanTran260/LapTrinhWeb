import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

EDIT_PAGES = [
    "admin/edit-monster.html",
    "admin/edit-redbull-lonvua.html",
    "admin/edit-redbull-original.html",
    "admin/edit-redbull-thai.html",
    "admin/edit-sting.html",
]


def main() -> int:
    failures = []

    inv_html = (ROOT / "admin" / "inventory.html").read_text(encoding="utf-8")
    if "CÒN HÀNG (Sẵn sàng xuất)" in inv_html:
        failures.append("admin/inventory.html: still contains 'CÒN HÀNG (Sẵn sàng xuất)'")
    if '<option value="instock" selected>CÒN HÀNG</option>' not in inv_html:
        failures.append("admin/inventory.html: missing '<option value=\"instock\" selected>CÒN HÀNG</option>'")
    if "- Sẵn sàng xuất kho</p>" not in inv_html:
        failures.append("admin/inventory.html: page subtitle '- Sẵn sàng xuất kho' was unexpectedly modified")

    for rel_path in EDIT_PAGES:
        content = (ROOT / rel_path).read_text(encoding="utf-8")
        if "Còn hàng (Sẵn sàng xuất kho)" in content:
            failures.append(f"{rel_path}: still contains 'Còn hàng (Sẵn sàng xuất kho)'")
        if '<option value="Còn hàng" selected>Còn hàng</option>' not in content:
            failures.append(f"{rel_path}: missing '<option value=\"Còn hàng\" selected>Còn hàng</option>'")

    if failures:
        print(f"FAIL ({len(failures)} checks failed):")
        for item in failures:
            print(f"  - {item}")
        return 1

    print("ALL 7 CHECKS PASSED: Stock status options simplified to 'CÒN HÀNG' / 'Còn hàng'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
