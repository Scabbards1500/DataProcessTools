import cv2
import numpy as np
import matplotlib.pyplot as plt

# 读取彩色图像
image = cv2.imread(r"D:\tempdataset\tooth_new\tooth_seg_new\images\11-front.png")

# 提取每个颜色通道（BGR顺序）
blue_channel = image[:, :, 0]
green_channel = image[:, :, 1]
red_channel = image[:, :, 2]

# 对每个通道应用Canny边缘检测
edges_blue = cv2.Canny(blue_channel, threshold1=100, threshold2=220)
edges_green = cv2.Canny(green_channel, threshold1=90, threshold2=220)
edges_red = cv2.Canny(red_channel, threshold1=180, threshold2=220)

# 可视化每个通道的边缘
plt.figure(figsize=(12, 8))

# 显示蓝色通道边缘
plt.subplot(2, 6, 1)
plt.imshow(edges_blue, cmap='gray')
plt.title('Blue Channel Edges')
plt.axis('off')

# 显示蓝色通道原图
plt.subplot(2, 6, 4)
plt.imshow(blue_channel)
plt.title('Blue Channel')
plt.axis('off')

# 显示绿色通道边缘
plt.subplot(2, 6, 2)
plt.imshow(edges_green, cmap='gray')
plt.title('Green Channel Edges')
plt.axis('off')

# 显示绿色通道原图
plt.subplot(2, 6, 5)
plt.imshow(green_channel)
plt.title('Green Channel')
plt.axis('off')

# 显示红色通道边缘
plt.subplot(2, 6, 3)
plt.imshow(edges_red, cmap='gray')
plt.title('Red Channel Edges')
plt.axis('off')

# 显示红色通道原图
plt.subplot(2, 6, 6)
plt.imshow(red_channel)
plt.title('Red Channel')
plt.axis('off')

# 显示结果
plt.tight_layout()
plt.savefig("RGB_canny.png", dpi=300, bbox_inches='tight')
plt.show()