import numpy as np
import cv2
import matplotlib.pyplot as plt

# 读取图片
img = cv2.imread(r"D:\tempdataset\TTADataset\CHASE_RITE_HRF_RETINA\all\images\01_test.png", 0)  # 以灰度模式读取图片

# 进行傅里叶变换
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)  # 将低频移动到图像中心

# 提取振幅和相位
magnitude_spectrum = np.abs(fshift)  # 振幅
phase_spectrum = np.angle(fshift)    # 相位

# 可视化振幅
# plt.subplot(1, 2, 1)
plt.imshow(np.log(1 + magnitude_spectrum), cmap='gray')  # 对数缩放处理
# plt.title('Magnitude Spectrum')
plt.xticks([])  # 去除x轴刻度数字
plt.yticks([])  # 去除y轴刻度数字
plt.savefig(r"D:\python\DataProcessTools\output\Magnitude2.png")

# 可视化相位
# plt.subplot(1, 2, 2)
plt.imshow(phase_spectrum, cmap='gray')
# plt.title('Phase Spectrum')
plt.xticks([])  # 去除x轴刻度数字
plt.yticks([])  # 去除y轴刻度数字
plt.savefig(r"D:\python\DataProcessTools\output\phase2.png")

# 显示结果
plt.show()
