import os
import pandas as pd
from sklearn.model_selection import train_test_split
import shutil


def DatasetSplit(data_dir, output_dir, imgname,labelname,makecsv):
    # 获取所有文件名
    image_dir = os.path.join(data_dir, f'{imgname}')
    label_dir = os.path.join(data_dir, f'{labelname}')
    image_files = sorted(os.listdir(image_dir))
    label_files = sorted(os.listdir(label_dir))

    # 划分数据集
    train_image_files, val_image_files, train_label_files, val_label_files = train_test_split(
        image_files, label_files, test_size=0.2, random_state=42
    )

    # 创建输出文件夹
    os.makedirs(os.path.join(output_dir, 'train', f'{imgname}'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'train', f'{labelname}'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'test', f'{imgname}'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'test', f'{labelname}'), exist_ok=True)

    # 复制NIfTI文件到输出文件夹 for Train
    train_data = []
    for idx, (image_file, label_file) in enumerate(zip(train_image_files, train_label_files)):
        image_path_src = os.path.join(image_dir, image_file)
        label_path_src = os.path.join(label_dir, label_file)

        image_basename = os.path.basename(image_file)
        label_basename = os.path.basename(label_file)

        image_path_dst = os.path.join(output_dir, 'train', f'{imgname}', image_basename)
        label_path_dst = os.path.join(output_dir, 'train', f'{labelname}', label_basename)

        shutil.copy(image_path_src, image_path_dst)
        shutil.copy(label_path_src, label_path_dst)

        train_data.append([image_path_dst, label_path_dst])

    # 复制NIfTI文件到输出文件夹 for Validation
    val_data = []
    for idx, (image_file, label_file) in enumerate(zip(val_image_files, val_label_files)):
        image_path_src = os.path.join(image_dir, image_file)
        label_path_src = os.path.join(label_dir, label_file)

        image_basename = os.path.basename(image_file)
        label_basename = os.path.basename(label_file)

        image_path_dst = os.path.join(output_dir, 'test', f'{imgname}', image_basename)
        label_path_dst = os.path.join(output_dir, 'test', f'{labelname}', label_basename)

        shutil.copy(image_path_src, image_path_dst)
        shutil.copy(label_path_src, label_path_dst)

        val_data.append([image_path_dst, label_path_dst])

    if(makecsv):
        # 创建CSV文件 for Train
        train_csv_data = pd.DataFrame(train_data, columns=['data', 'label'])
        train_csv_data.to_csv(os.path.join(output_dir, 'train', 'traindata.csv'), index=False)
        # 创建CSV文件 for Validation
        val_csv_data = pd.DataFrame(val_data, columns=['data', 'label'])
        val_csv_data.to_csv(os.path.join(output_dir, 'val', 'validata.csv'), index=False)

    print("数据集划分完成！")

# 设置路径
data_dir = r'D:\tempdataset\TTADataset\CHASE_RITE_HRF_RETINA_2'
output_dir = r'D:\tempdataset\TTADataset\CHASE_RITE_HRF_RETINA_3'
imgfolder = 'images'
lablefolder = 'masks'
DatasetSplit(data_dir,output_dir,imgfolder,lablefolder,False)
