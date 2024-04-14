import cv2
import numpy as np

# 读取原始图像和标签掩码
original_image = cv2.imread(r"D:\tempdataset\tooth.v4i.coco-segmentation\train\01aee56.jpg")
label_mask = cv2.imread(r"D:\tempdataset\tooth.v4i.coco-segmentation\result\01aee56_OUT.png", cv2.IMREAD_GRAYSCALE)

# # 在原始图像上找到标签掩码的轮廓
# contours, _ = cv2.findContours(label_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
# # 在原始图像上绘制轮廓
# image = cv2.drawContours(original_image, contours, -1, (0, 255, 0), 2)



# 将标签掩码转换为BGR格式以便与原始图像进行混合
label_mask_bgr = cv2.cvtColor(label_mask, cv2.COLOR_GRAY2BGR)
# 设置混合参数（这里设置为半透明，您可以根据需要调整alpha值）
alpha = 0.3
# 将标签掩码半透明地叠加到原始图像上
result = cv2.addWeighted(original_image, 1 - alpha, label_mask_bgr, alpha, 0)

# cv2.imwrite(r"D:\tempdataset\tooth.v4i.coco-segmentation\surroundingtest\test.png",image)
cv2.imwrite(r"D:\tempdataset\tooth.v4i.coco-segmentation\surroundingtest\test2.png",result)