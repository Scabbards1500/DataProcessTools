import os
import shutil


def move_files(source_dir, target_dir):
    """
    将 source_dir 下所有子文件夹中的文件移动到 target_dir。

    Args:
        source_dir (str): 源目录路径。
        target_dir (str): 目标目录路径。
    """
    # 检查 source_dir 是否存在
    if not os.path.exists(source_dir):
        print(f"源目录 {source_dir} 不存在。")
        return

    # 如果目标目录不存在，创建它
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"目标目录 {target_dir} 已创建。")

    # 遍历源目录中的所有文件夹和文件
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            # 获取文件的完整路径
            file_path = os.path.join(root, file)
            # 构建目标路径
            target_path = os.path.join(target_dir, file)

            # 检查文件是否已存在于目标目录
            if os.path.exists(target_path):
                print(f"文件 {file} 已存在于目标目录，跳过。")
                continue

            # 移动文件
            shutil.move(file_path, target_dir)
            print(f"文件 {file} 已移动到 {target_dir}。")

    print("所有文件已成功移动。")


# 使用示例
source_directory = r"D:\tempdataset\tooth_new\ori_data\new-1123"  # 替换为实际源目录路径
target_directory = r"D:\tempdataset\tooth_new\ori_data\new_all"  # 替换为实际目标目录路径

move_files(source_directory, target_directory)
