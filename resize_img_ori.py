from PIL import Image
import os

def batch_resize_images(input_folder, output_folder, target_size=(512, 512)):
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
                # 缩放图像
                resized_img = img.resize(target_size)
                # 保存缩放后的图像
                resized_img.save(output_path)
                print(f"成功缩放并保存: {output_path}")
        except Exception as e:
            print(f"处理文件 {input_path} 时出错: {e}")

# 输入文件夹路径和输出文件夹路径
input_folder_path = r"D:\tempdataset\TTADataset\Retina\test\mask"
output_folder_path = r"D:\tempdataset\TTADataset\Retina\test\mask512"

# 批量缩放图片
batch_resize_images(input_folder_path, output_folder_path)