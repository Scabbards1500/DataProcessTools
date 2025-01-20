import os
import json
from PIL import Image, ImageDraw
import numpy as np


def convert_json_to_mask(json_folder, output_folder):
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    for json_file in os.listdir(json_folder):
        if not json_file.endswith('.json'):
            continue

        json_path = os.path.join(json_folder, json_file)

        # 加载 JSON 文件
        with open(json_path, 'r') as file:
            data = json.load(file)

        image_width = data['imageWidth']
        image_height = data['imageHeight']

        # 创建空白的 mask 图像
        mask = Image.new("L", (image_width, image_height), 0)
        draw = ImageDraw.Draw(mask)

        # 绘制每个 shape 的多边形
        for shape in data['shapes']:
            points = [tuple(point) for point in shape['points']]  # 将 points 转换为 (x, y) 元组列表
            draw.polygon(points, outline=255, fill=255)  # 绘制多边形

        # 保存 mask
        output_path = os.path.join(output_folder, os.path.splitext(json_file)[0] + '_mask.png')
        mask.save(output_path)
        print(f"Mask saved to {output_path}")


# 调用函数
json_folder = r"D:\tempdataset\tooth_seg_new"  # 替换为你的 JSON 文件夹路径
output_folder = r"D:\tempdataset\tooth_seg_new_full"  # 替换为输出路径
convert_json_to_mask(json_folder, output_folder)
