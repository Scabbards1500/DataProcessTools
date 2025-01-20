import os
import shutil


def merge_datasets(dataset_paths, output_path):
    image_counter = 1  # 用于重命名文件
    folder_names = ["images", "masks"]

    # 确保输出路径存在
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for folder in folder_names:
        if not os.path.exists(os.path.join(output_path, folder)):
            os.makedirs(os.path.join(output_path, folder))

    # 遍历数据集
    while True:
        datasets_finished = 0
        for i, dataset in enumerate(dataset_paths):
            image_folder = os.path.join(dataset, 'images')
            mask_folder = os.path.join(dataset, 'masks')

            image_files = sorted(os.listdir(image_folder))
            mask_files = sorted(os.listdir(mask_folder))

            if image_counter > len(image_files):
                datasets_finished += 1
                continue

            # 获取当前的图片和mask文件
            image_file = image_files[image_counter - 1]
            mask_file = mask_files[image_counter - 1]

            # 重命名并复制文件到合成数据集
            new_image_name = f"image_{image_counter:06d}.png"
            new_mask_name = f"mask_{image_counter:06d}.png"

            shutil.copy(os.path.join(image_folder, image_file), os.path.join(output_path, 'images', new_image_name))
            shutil.copy(os.path.join(mask_folder, mask_file), os.path.join(output_path, 'masks', new_mask_name))

            print(f"Copied {image_file} and {mask_file} as {new_image_name} and {new_mask_name}")
            image_counter += 1

        if datasets_finished == len(dataset_paths):
            break


dataset_paths = [r'D:\tempdataset\TTADataset\CHASE\train', r'D:\tempdataset\TTADataset\RITE\train', r'D:\tempdataset\TTADataset\HRF\train', r'D:\tempdataset\TTADataset\HRF\train']
output_path = r'D:\tempdataset\TTADataset\CRHR\train'

merge_datasets(dataset_paths, output_path)
