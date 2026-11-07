import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT_DIR)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

edit_monster_path = 'admin/edit-monster.html'
content = open(edit_monster_path, encoding='utf-8').read()

expected_imgs = [
    'assets/images/monster/original.webp',
    'assets/images/monster/original-back-1.webp',
    'assets/images/monster/original-back-2.webp',
    'assets/images/monster/original-with-glass.webp'
]

print("===========================================================================")
print("KIỂM TRA BỘ 4 ẢNH PREVIEW CÓ SẴN TRANG QUẢN TRỊ LON MONSTER (ADMIN)")
print("===========================================================================\n")

all_passed = True
for idx, img_rel in enumerate(expected_imgs, 1):
    in_html = f"../{img_rel}" in content or img_rel in content
    on_disk = os.path.exists(img_rel)
    passed = in_html and on_disk
    if not passed:
        all_passed = False
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status}: Hình {idx} ({img_rel}) - Trong HTML: {in_html}, Trên ổ đĩa: {on_disk}")

# Check that there are no broken images without src in edit-product-images
import re
images_section = re.search(r'id="edit-product-images".*?</div>\s*</div>', content, re.DOTALL)
if images_section:
    img_tags = re.findall(r'<img[^>]+>', images_section.group(0))
    print(f"\nTổng số thẻ <img> trong khối chỉnh sửa ảnh: {len(img_tags)}")
    for t in img_tags:
        has_src = 'src="' in t and not 'src=""' in t
        print(f"  Thẻ: {t[:80]}... -> Có src hợp lệ: {has_src}")
        if not has_src:
            all_passed = False

if all_passed:
    print("\n🎉 HOÀN THÀNH: CẢ 4 ẢNH PREVIEW CỦA LON MONSTER ĐỀU HIỂN THỊ RÕ RÀNG!")
    sys.exit(0)
else:
    print("\n❌ CÒN LỖI: Vui lòng kiểm tra lại đường dẫn ảnh.")
    sys.exit(1)
