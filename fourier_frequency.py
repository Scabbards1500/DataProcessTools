import numpy as np
import cv2
from matplotlib import pyplot as plt

# 读取图像并转换为浮点型
img = cv2.imread(r"D:\tempdataset\TTADataset\CHASE_RITE_HRF_RETINA\all\images\28_rtrain.png", 0)
img_float32 = np.float32(img)

# 傅里叶变换
dft = cv2.dft(img_float32, flags=cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)

# 计算频谱的幅度（用于可视化）
magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]) + 1)

# 图像尺寸
rows, cols = img.shape
crow, ccol = int(rows / 2), int(cols / 2)  # 中心位置
mask_range = 20


# 高通滤波
mask_h = np.ones((rows, cols, 2), np.uint8)
mask_h[crow - mask_range:crow + mask_range, ccol - mask_range:ccol + mask_range] = 0

# 高通滤波频域
magnitude_spectrum_high = magnitude_spectrum * mask_h[:, :, 0]

# 对频域应用高通滤波，并进行逆傅里叶变换
fshift_h = dft_shift * mask_h
f_ishift_h = np.fft.ifftshift(fshift_h)
img_back_h = cv2.idft(f_ishift_h)
img_back_h = cv2.magnitude(img_back_h[:, :, 0], img_back_h[:, :, 1])

# 低通滤波
mask_l = np.zeros((rows, cols, 2), np.uint8)
mask_l[crow - mask_range:crow + mask_range, ccol - mask_range:ccol + mask_range] = 1

# 低通滤波频域
magnitude_spectrum_low = magnitude_spectrum * mask_l[:, :, 0]

# 对频域应用低通滤波，并进行逆傅里叶变换
fshift_l = dft_shift * mask_l
f_ishift_l = np.fft.ifftshift(fshift_l)
img_back_l = cv2.idft(f_ishift_l)
img_back_l = cv2.magnitude(img_back_l[:, :, 0], img_back_l[:, :, 1])

# 绘制结果：第一排是频域，第二排是空间域
plt.figure(figsize=(12, 8))

# 第一排：频域图像
plt.subplot(2, 3, 1)
plt.imshow(magnitude_spectrum, cmap='gray')
plt.ylabel('Frequency Domain', fontsize=18)
plt.xticks([])  # 去除x轴刻度数字
plt.yticks([])

plt.subplot(2, 3, 2)
plt.imshow(magnitude_spectrum_high, cmap='gray')
plt.axis('off')  # 移除坐标轴

plt.subplot(2, 3, 3)
plt.imshow(magnitude_spectrum_low, cmap='gray')
plt.axis('off')  # 移除坐标轴

# 第二排：空间域滤波结果
plt.subplot(2, 3, 4)
plt.imshow(img, cmap='gray')
plt.ylabel('Spatial Domain', fontsize=18)
plt.xlabel('All frequncy', fontsize=18)
plt.xticks([])  # 去除x轴刻度数字
plt.yticks([])

plt.subplot(2, 3, 5)
plt.imshow(img_back_h, cmap='gray')
plt.xlabel('high frequncy', fontsize=18)
plt.xticks([])  # 去除x轴刻度数字
plt.yticks([])

plt.subplot(2, 3, 6)
plt.imshow(img_back_l, cmap='gray')
plt.xlabel('low frequncy', fontsize=18)
plt.xticks([])  # 去除x轴刻度数字
plt.yticks([])

# 自动调整子图间的间距
plt.tight_layout()
plt.savefig(r"D:\python\DataProcessTools\output\high_low_pass_filter.png")
plt.show()
