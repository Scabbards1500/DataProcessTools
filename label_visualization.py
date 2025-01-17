import cv2
import os

# 输入和输出文件夹路径
images_folder = r"D:\tempdataset\tooth_new\tooth_seg_new\images"
masks_folder = r"D:\tempdataset\tooth_new\tooth_seg_new\masks"
output_folder = r"D:\tempdataset\tooth_new\tooth_seg_new\output"

# 如果输出文件夹不存在，则创建它
os.makedirs(output_folder, exist_ok=True)

# 遍历 images 文件夹中的所有文件
for image_file in os.listdir(images_folder):
    # 构造图像和对应的标签路径
    image_path = os.path.join(images_folder, image_file)
    mask_path = os.path.join(masks_folder, image_file.replace('.png', '_mask.png'))  # 根据命名规则调整

    # 确保标签文件存在
    if not os.path.exists(mask_path):
        print(f"Mask file for {image_file} not found. Skipping.")
        continue

    # 读取原始图像和标签掩码
    original_image = cv2.imread(image_path)
    label_mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

    # 在原始图像上找到标签掩码的轮廓
    contours, _ = cv2.findContours(label_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 在原始图像上绘制轮廓
    image_with_contours = cv2.drawContours(original_image, contours, -1, (0, 255, 0), 1)

    # 将标签掩码转换为BGR格式以便与原始图像进行混合
    label_mask_bgr = cv2.cvtColor(label_mask, cv2.COLOR_GRAY2BGR)

    # 设置混合参数（这里设置为半透明，您可以根据需要调整 alpha 值）
    alpha = 0.3
    result = cv2.addWeighted(original_image, 1 - alpha, label_mask_bgr, alpha, 0)

    # 保存处理后的图像到输出文件夹
    output_path = os.path.join(output_folder, image_file)
    cv2.imwrite(output_path, result)

    print(f"Processed and saved: {output_path}")
