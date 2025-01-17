import os
import glob
import scipy.io
import numpy as np
from skimage import io
import cv2

patch_width = 256
patch_height = 256

dataset_dir = r"D:\tempdataset\kumar"
img_dir = r"D:\tempdataset\kumar\images"
label_dir = r"D:\tempdataset\kumar\Labels"
prepared_dataset_dir = r"D:\tempdataset\kumar\kumar_p"

image_list = glob.glob(os.path.join(dataset_dir, img_dir) + "/*.tif")

def img_as_ubyte(image):
    """
    Convert the image to uint8. If the image is already in [0, 255] range, just cast it.
    If the image is in [0, 1] range, scale it to [0, 255] and then cast.
    """
    if image.max() <= 1.0:
        return (image * 255).astype(np.uint8)
    return image.astype(np.uint8)

for img_path in image_list:
    image = io.imread(img_path)

    # Load the corresponding label
    label_path = glob.glob(os.path.join(dataset_dir, label_dir, os.path.splitext(os.path.basename(img_path))[0]) + "*")[0]
    label = scipy.io.loadmat(label_path)
    label = label['inst_map']
    label = label.reshape(label.shape[0], label.shape[1], 1)

    # Convert image to uint8 if necessary
    image = img_as_ubyte(image)

    # Convert label to binary mask and then scale it to 0 and 255
    temp_mask = (label[:, :, 0] > 0).astype(np.uint8) * 255

    # Save the processed image and mask
    io.imsave(os.path.join(prepared_dataset_dir, "images",
                           os.path.splitext(os.path.basename(img_path))[0] + ".tif"),
              image)

    cv2.imwrite(os.path.join(prepared_dataset_dir, "masks",
                             os.path.splitext(os.path.basename(img_path))[0] + ".png"), temp_mask)
