from pycocotools.coco import COCO
import os
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import cv2

def convert_coco2mask_show(image_id):
    img = coco.imgs[image_id]
    image = np.array(Image.open(os.path.join(img_dir, img['file_name'])))
    cat_ids = coco.getCatIds()
    anns_ids = coco.getAnnIds(imgIds=img['id'], catIds=cat_ids, iscrowd=None)
    name = coco.loadCats(coco.getCatIds())[0]["name"]
    anns = coco.loadAnns(anns_ids)
    coco.showAnns(anns)
    mask = coco.annToMask(anns[0])

    for i in range(len(anns)):
        mask += coco.annToMask(anns[i])
    mask = np.array([mask.tolist()]*3).transpose((1,2,0)).astype("uint8")*255
    # 获取文件名
    file_name = img['file_name']
    # 生成新的文件名
    new_file_name = "{}".format(file_name)
    plt.imsave(os.path.join(save_dir, new_file_name), mask)

if __name__ == '__main__':
    Dataset_dir = r"D:\tempdataset\tooth.v4i.coco\train"
    coco = COCO(os.path.join(Dataset_dir, '_annotations.coco.json'))
    img_dir = Dataset_dir
    save_dir = r"D:\tempdataset\tooth.v4i.coco\mask"
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    image_ids = list(range(300000))
    for id in image_ids:
        convert_coco2mask_show(id)
