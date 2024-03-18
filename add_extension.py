import os


def add_png_extension(folder_path):
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 构建文件的完整路径
        file_path = os.path.join(folder_path, filename)

        # 检查是否是文件
        if os.path.isfile(file_path):
            # 如果文件名没有 .png 后缀，则添加后缀
            new_filename = filename + '.png'
            new_file_path = os.path.join(folder_path, new_filename)

            # 重命名文件
            os.rename(file_path, new_file_path)
            print(f"Renamed '{filename}' to '{new_filename}'")


# 指定文件夹路径
folder_path = r'C:\Users\scaaa\Downloads\Compressed\tooth.v4i.coco-segmentation\labels'

# 添加 .png 后缀
add_png_extension(folder_path)
