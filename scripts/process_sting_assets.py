import os
from PIL import Image, ImageDraw

def process_sting_images():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "images", "sting"))
    
    image_tasks = [
        {
            "input": "nuoc-tang-luc-sting-dau-sleek-lon-330ml_202509291421449068.webp",
            "output": "sting-dau.webp",
            "label": "Sting Dau (Red)"
        },
        {
            "input": "nuoc-ngot-lon-sting-gold-sleek-330ml_202509291559402687.webp",
            "output": "sting-gold.webp",
            "label": "Sting Vang (Gold)"
        },
        {
            "input": "nuoc-tang-luc-sting-sleek-huong-viet-quat-lon-320ml_202505211557567348.webp",
            "output": "sting-vietquat.webp",
            "label": "Sting Viet Quat (Blue)"
        }
    ]
    
    results = []

    for task in image_tasks:
        in_path = os.path.join(base_dir, task["input"])
        out_path = os.path.join(base_dir, task["output"])
        
        print(f"Processing {task['label']}...")
        print(f"  Source: {in_path}")
        im = Image.open(in_path).convert("RGBA")
        w, h = im.size
        
        # Seed flood-fill from all 4 corners to remove exterior white background
        corners = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
        for pt in corners:
            if im.getpixel(pt)[3] != 0:
                ImageDraw.floodfill(im, pt, (0, 0, 0, 0), thresh=30)
                
        # Save as transparent WebP with quality 95 to meet ~30KB-80KB target
        im.save(out_path, format="WEBP", quality=95)
        print(f"  Saved to: {out_path}")
        
        # Verify the saved file
        saved_im = Image.open(out_path)
        file_size_bytes = os.path.getsize(out_path)
        file_size_kb = file_size_bytes / 1024
        corner_alphas = [saved_im.getpixel(pt)[3] for pt in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]]
        
        verification = {
            "name": task["output"],
            "label": task["label"],
            "path": out_path,
            "exists": os.path.exists(out_path),
            "format": saved_im.format,
            "mode": saved_im.mode,
            "dimensions": f"{saved_im.size[0]}x{saved_im.size[1]}",
            "corner_alphas": corner_alphas,
            "all_corners_transparent": all(a == 0 for a in corner_alphas),
            "size_bytes": file_size_bytes,
            "size_kb": f"{file_size_kb:.2f} KB",
            "size_in_range": 30 <= file_size_kb <= 80
        }
        results.append(verification)
        print(f"  Mode: {verification['mode']}")
        print(f"  Corner alphas: {verification['corner_alphas']}")
        print(f"  File size: {verification['size_kb']} ({verification['size_bytes']} bytes)")
        print(f"  Verification passed: {verification['exists'] and verification['mode'] == 'RGBA' and verification['all_corners_transparent'] and verification['size_in_range']}")
        print("-" * 50)
        
    return results

if __name__ == "__main__":
    process_sting_images()
