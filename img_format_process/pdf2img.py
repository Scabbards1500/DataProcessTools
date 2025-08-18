from pdf2image import convert_from_path
from pathlib import Path
import json
import cv2

poppler_path = r"D:\DevTools\poppler-24.08.0\Library\bin"


def pdf_to_images_for_rapidlayout(pdf_path, image_output_dir, dpi=150):
    pdf_path = Path(pdf_path)
    image_output_dir = Path(image_output_dir)
    image_output_dir.mkdir(parents=True, exist_ok=True)

    # Convert PDF to images
    images = convert_from_path(pdf_path, dpi=dpi,poppler_path=poppler_path)

    results = []
    for idx, img in enumerate(images):
        img_name = f"page_{idx+1:03d}.jpg"
        img_path = image_output_dir / img_name
        img.save(img_path, "JPEG")

        results.append({
            "page": idx + 1,
            "image_path": str(img_path.resolve())
        })

    # Save JSON
    json_path = image_output_dir / "pages.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    return json_path

# 使用方法
pdf_path = "img_tests.pdf"  # 原始 PDF 路径
output_dir = "rapidlayout_pages"  # 输出图像和 JSON 的文件夹
json_file = pdf_to_images_for_rapidlayout(pdf_path, output_dir)
print(f"图像转换完成，图像路径列表保存在：{json_file}")
