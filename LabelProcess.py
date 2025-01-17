import cv2
import os
from PIL import Image

#这个是灰度标签之类的转化的


def labelprocess(input_folder, output_folder):

    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        discrete_to_binary(input_path, output_folder)
        # binary_to_discrete(input_path,output_folder)
        # binary_to_gray(input_path,output_folder)

# 离散label转化为二值标签
def discrete_to_binary(inputpath,outputpath):
    # 读取图像
    image = cv2.imread(inputpath)
    # 将图像转换为灰度图像（如果需要）
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 将灰度图像转换为二值掩码图像
    binary_mask = gray_image > 30
    base_name = os.path.basename(inputpath).split('.')[0]
    output_filename = os.path.join(outputpath, f"{base_name}.png")
    # 将二值掩码保存为图像文件
    cv2.imwrite(output_filename, (binary_mask * 255))

# 二值标签转化成离散标签
def binary_to_discrete(inputpath,outputpath):
    binary_image = Image.open(inputpath)
    gray_image = binary_image.convert("L")
    base_name = os.path.basename(inputpath).split('.')[0]
    output_filename = os.path.join(outputpath, f"{base_name}.png")
    gray_image.save(output_filename)


def binary_to_gray(inputpath,outputpath):
    # 打开二值标签图像
    binary_label = Image.open(inputpath)

    # 创建一个新的图像，尺寸与二值标签相同
    gray_label = Image.new('L', binary_label.size)

    # 将二值标签中的像素值（通常是0和1）映射到灰度级别（0-255）
    for x in range(binary_label.width):
        for y in range(binary_label.height):
            # 获取当前像素值
            pixel_value = binary_label.getpixel((x, y))
            # 将0映射为黑色，1映射为白色
            gray_value = 0 if pixel_value == 0 else 255
            # 在灰度图像中设置像素值
            gray_label.putpixel((x, y), gray_value)

    base_name = os.path.basename(inputpath).split('.')[0]
    output_filename = os.path.join(outputpath, f"{base_name}.png")
    # 保存灰度标签图像
    gray_label.save(output_filename)




# 图像文件夹路径
image_path = r"D:\tempdataset\NUCLEI\masks512"
output_path = r"D:\tempdataset\NUCLEI\masks5122"
labelprocess(image_path, output_path)