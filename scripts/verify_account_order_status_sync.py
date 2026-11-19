import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
EXPECTED_ACCOUNT_BADGE = (
    '<span class="badge-status success" style="font-size: 0.75rem;">'
    '<i class="fas fa-check-circle"></i> HOÀN THÀNH</span>'
)
EXPECTED_DETAIL_BADGE = (
    '<span id="order-detail-status" class="badge-status success">'
    '<i class="fas fa-check-circle"></i> HOÀN THÀNH</span>'
)


def main() -> int:
    """Verify #EB-2026 and #EB-2025 share HOÀN THÀNH status on account and order-detail fallback."""
    failures = []

    account_html = (ROOT / "pages" / "account.html").read_text(encoding="utf-8")
    detail_html = (ROOT / "pages" / "order-detail.html").read_text(encoding="utf-8")
    orders_html = (ROOT / "pages" / "orders.html").read_text(encoding="utf-8")

    if "ĐÃ GIAO HỎA TỐC 2H" in account_html:
        failures.append("pages/account.html still contains 'ĐÃ GIAO HỎA TỐC 2H'")
    if "ĐÃ GIAO HỎA TỐC 2H" in detail_html:
        failures.append("pages/order-detail.html still contains 'ĐÃ GIAO HỎA TỐC 2H'")

    card_2026 = re.search(r"Mã đơn: #EB-2026[\s\S]*?Mã đơn: #EB-2025", account_html)
    if not card_2026 or EXPECTED_ACCOUNT_BADGE not in card_2026.group(0):
        failures.append("pages/account.html: #EB-2026 missing unified 'HOÀN THÀNH' badge")

    card_2025 = re.search(r"Mã đơn: #EB-2025[\s\S]*?TIẾP TỤC MUA SẮM", account_html)
    if not card_2025 or EXPECTED_ACCOUNT_BADGE not in card_2025.group(0):
        failures.append("pages/account.html: #EB-2025 missing 'HOÀN THÀNH' badge")

    if EXPECTED_DETAIL_BADGE not in detail_html:
        failures.append("pages/order-detail.html: #order-detail-status missing 'HOÀN THÀNH' fallback badge")

    if "ĐANG GIAO (2H)" not in orders_html or 'filterOrderList(\'shipping\', this)' not in orders_html:
        failures.append("pages/orders.html: shipping order or filter tab unexpectedly altered")

    if failures:
        print(f"FAIL ({len(failures)} checks failed):")
        for item in failures:
            print(f"  - {item}")
        return 1

    print("ALL 6 CHECKS PASSED: #EB-2026 & #EB-2025 unified to 'HOÀN THÀNH' on account & detail fallback.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
