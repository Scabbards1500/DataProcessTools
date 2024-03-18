import os


def batch_remove_string_in_filenames(folder_path, string_to_remove):
    """
    批量去除文件夹中所有文件名中的指定字符串并重命名文件。

    参数:
    folder_path (str): 文件夹路径。
    string_to_remove (str): 要从文件名中移除的字符串。
    """
    # 获取文件夹中的所有文件
    files = os.listdir(folder_path)

    # 遍历文件列表
    for filename in files:
        # 如果指定的字符串在文件名中，则进行替换
        if string_to_remove in filename:
            # 构造新文件名，去除指定字符串
            new_filename = filename.replace(string_to_remove, '')
            # 构造旧文件的完整路径
            old_filepath = os.path.join(folder_path, filename)
            # 构造新文件的完整路径
            new_filepath = os.path.join(folder_path, new_filename)
            # 重命名文件
            os.rename(old_filepath, new_filepath)

            print(f'{old_filepath} 重命名为 {new_filepath}')


# 使用示例
folder_path = r'C:\Users\scaaa\Downloads\Compressed\tooth.v4i.coco-segmentation\labels512'
string_to_remove = '.jpg'
batch_remove_string_in_filenames(folder_path, string_to_remove)
