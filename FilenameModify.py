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

import os

import os

def batch_add_string_in_filenames(folder_path, string_to_add):
    """
    批量给文件夹中所有文件名加上指定的字符串。

    参数:
    folder_path (str): 文件夹路径。
    string_to_add (str): 要添加到文件名中的字符串。
    """
    # 获取文件夹中的所有文件
    files = os.listdir(folder_path)

    # 遍历文件列表
    for filename in files:
        # 分割文件名和扩展名
        name, ext = os.path.splitext(filename)
        # 构造新文件名, 在文件名和扩展名之间添加指定字符串
        new_filename = f'{name}{string_to_add}{ext}'
        # 构造旧文件的完整路径
        old_filepath = os.path.join(folder_path, filename)
        # 构造新文件的完整路径
        new_filepath = os.path.join(folder_path, new_filename)
        # 重命名文件
        os.rename(old_filepath, new_filepath)

        print(f'{old_filepath} 重命名为 {new_filepath}')







folder_path = r'D:\tempdataset\TTADataset\Retina\train\mask5122'

# #move string
# string_to_remove = '.jpg'
# batch_remove_string_in_filenames(folder_path, string_to_remove)

#add string
string_to_add = "_rtrain"
batch_add_string_in_filenames(folder_path,string_to_add)