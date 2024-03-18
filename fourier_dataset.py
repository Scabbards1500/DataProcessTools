import torch
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import torchvision.transforms as transforms



import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

import torch
import numpy as np
import cv2

# 读取图像
# 图像转tensor！
# 读取图像

fre_m_all = []
# 遍历一个数据集获取基本风格

def fourier(tensor):
    # 进行傅里叶变换
    fre = torch.fft.fftn(tensor, dim=(-2, -1))  # 在图像的最后两个维度上执行傅里叶变换
    fre_m = torch.abs(fre)   # 幅度谱，求模得到
    fre_p = torch.angle(fre) # 相位谱，求相角得到
    return fre_m, fre_p

def gain_fourier(input_folder):
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        with Image.open(input_path) as img:
            transform = transforms.ToTensor()
            tensor = transform(img)
            fre_m, fre_p = fourier(tensor)
            fre_m_all.append(fre_m)

    fre_m_all_tensor = torch.stack(fre_m_all)
    mean_fre_m = torch.mean(fre_m_all_tensor, dim=0)

    return mean_fre_m


def change_fourier(input_folder,output_folder,fre_m_all):
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        with Image.open(input_path) as img:
            transform = transforms.ToTensor()
            tensor = transform(img)
            _, fre_p = fourier(tensor)
            fre_img = fre_m_all * torch.exp(1j * fre_p)
            img = torch.abs(torch.fft.ifftn(fre_img, dim=(-2, -1)))
            transform = transforms.ToPILImage()
            output_img = transform(img)
            output_path = os.path.join(output_folder, filename)
            output_img.save(output_path)


input_folder1 = r"D:\tempdataset\TTADataset\RITE\train\images512"

input_folder2 = r"D:\tempdataset\TTADataset\HRF\test\images512"
output_folder = r"D:\tempdataset\TTADataset\HRF\test\images_ftrans"

# 获取平均傅里叶幅度
mean_fre_m = gain_fourier(input_folder1)

# 处理图像并保存到输出文件夹
change_fourier(input_folder2, output_folder, mean_fre_m)




