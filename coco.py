import cv2
from pycocotools.coco import COCO
import os
import shutil
import matplotlib.pyplot as plt
import numpy as np

#这个还没有实践过

'''
路径参数
'''
# 原coco数据集的路径
dataDir = "./"
# 用于保存新生成的mask数据的路径
savepath = "coco_mask/"

'''
数据集参数
'''
# coco有80类，这里写要进行二值化的类的名字
# 其他没写的会被当做背景变成黑色
classes_names = ['car']  # 自行修改标签

datasets_list = ['coco']


# 生成保存路径
# if the dir is not exists,make it,else delete it
def mkr(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        os.mkdir(path)
    else:
        os.mkdir(path)


# 生成mask图
def mask_generator(coco, width, height, anns_list):
    mask_pic = np.zeros((height, width))
    # 生成mask - 此处生成的是4通道的mask图,如果使用要改成三通道,可以将下面的注释解除,或者在使用图片时搜相关的程序改为三通道
    for single in anns_list:
        # print(single)  # 输出每一个标注信息
        mask_single = coco.annToMask(single)
        mask_pic += mask_single
    # coco.showAnns(anns_list)
    # 转化为255
    for row in range(height):
        for col in range(width):
            if mask_pic[row][col] > 0:
                mask_pic[row][col] = 255
    # 转为三通道
    imgs = np.zeros(shape=(height, width, 3), dtype=np.float32)
    imgs[:, :, 0] = mask_pic[:, :]
    imgs[:, :, 1] = mask_pic[:, :]
    imgs[:, :, 2] = mask_pic[:, :]
    imgs = imgs.astype(np.uint8)
    return imgs

