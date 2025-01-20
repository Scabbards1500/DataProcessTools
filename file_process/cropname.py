import os


import os

def truncate_filenames(folder_path, new_folder_path, max_length):
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 构建文件的完整路径
        file_path = os.path.join(folder_path, filename)

        # 检查是否是文件
        if os.path.isfile(file_path):
            # 获取文件名和扩展名
            name, extension = os.path.splitext(filename)

            # 如果文件名长度超过指定长度，则进行裁剪
            if len(name) > max_length:
                truncated_name = name[:max_length] + extension

                # 构建新的文件路径
                new_file_path = os.path.join(new_folder_path, truncated_name)

                # 检查新文件路径是否已经存在
                if os.path.exists(new_file_path):
                    print(f"File '{new_file_path}' already exists. Skipping...")
                else:
                    # 重命名文件
                    os.rename(file_path, new_file_path)
                    print(f"Renamed '{filename}' to '{truncated_name}'")
            else:
                print(f"File '{filename}' does not need truncation.")



# 指定文件夹路径和最大文件名长度
max_length = 7

# 裁剪文件名
truncate_filenames(r"D:\tempdataset\tooth_aug.v2i.coco\image", r"D:\tempdataset\tooth_aug.v2i.coco\image2",max_length)
