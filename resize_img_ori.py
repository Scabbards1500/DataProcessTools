from PIL import Image
import os



def batch_resize_images(input_folder, output_folder, target_size=(512, 512), crop=False):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        try:
            # 打开图像文件
            with Image.open(input_path) as img:
                # 如果crop为True，则进行裁剪
                if crop:
                    width, height = img.size
                    # 计算裁剪后的左上角坐标
                    left = (width - target_size[0]) / 2
                    top = (height - target_size[1]) / 2
                    right = (width + target_size[0]) / 2
                    bottom = (height + target_size[1]) / 2
                    # 裁剪图像
                    cropped_img = img.crop((left, top, right, bottom))
                    # 重新调整大小
                    resized_img = cropped_img.resize(target_size)
                else:
                    # 缩放图像
                    resized_img = img.resize(target_size).convert('RGB')
                # 保存图像
                resized_img.save(output_path)
                print(f"成功处理并保存: {output_path}")
        except Exception as e:
            print(f"处理文件 {input_path} 时出错: {e}")


# 输入文件夹路径和输出文件夹路径
input_folder_path = r"D:\tempdataset\NUCLEI\masks_ori"
output_folder_path = r"D:\tempdataset\NUCLEI\masks512"

# 批量缩放图片
batch_resize_images(input_folder_path, output_folder_path,crop=False)