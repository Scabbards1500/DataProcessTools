import torch
import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt

import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

# 图像转tensor！
# 读取图像
image = Image.open(r"D:\tempdataset\TTADataset\CHASE\test\images512\Image_01L.jpg")  # 替换为你的图像文件路径
# 定义转换
transform = transforms.ToTensor()
# 将图像转换为张量
tensor = transform(image)









# tensor转图像！
# 定义转换
transform = transforms.ToPILImage()
# 将张量转换为图像
image = transform(tensor)
# 显示图像
plt.imshow(image)
plt.axis('off')  # 不显示坐标轴
plt.show()


