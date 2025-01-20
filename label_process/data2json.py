import os
import numpy as np
import nibabel as nib
import json

def convert_nii_to_json(data_dir, output_json_path):
    # 读取数据和标签
    data_files = sorted(os.listdir(os.path.join(data_dir, 'data')))
    label_files = sorted(os.listdir(os.path.join(data_dir, 'label')))

    dataset = {"training": [], "validation": []}

    for data_file, label_file in zip(data_files, label_files):
        data_path = os.path.join(data_dir, 'data', data_file)
        label_path = os.path.join(data_dir, 'label', label_file)

        # 将数据和标签添加到数据集
        example = {"image": data_path, "label": label_path}

        # 将数据集分为"training"和"validation"
        if np.random.rand() < 0.8:  # 80% for training
            dataset["training"].append(example)
        else:
            dataset["validation"].append(example)

    # 将数据集保存为JSON文件
    with open(output_json_path, 'w') as json_file:
        json.dump(dataset, json_file, indent=2)

if __name__ == "__main__":
    data_directory = r"D:\tempdataset\INSTANCE2022"
    output_json_path = r"D:\python\UNETR\BTCV\dataset\output.json"
    convert_nii_to_json(data_directory, output_json_path)
