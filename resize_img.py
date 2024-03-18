from PIL import Image
import os


def img_resize(input_folder, output_folder, targetsize):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        #resize
        batch_resize_images(input_path,output_folder,targetsize)
        # #crop
        # crop_to_fixed_size(input_path,output_path,targetsize)


def batch_resize_images(input_path, output_path, target_size):
        try:
            # 打开图像文件
            with Image.open(input_path) as img:
                # 缩放图像
                resized_img = img.resize(target_size)
                # 保存缩放后的图像
                resized_img.save(output_path)
                print(f"成功缩放并保存: {output_path}")
        except Exception as e:
            print(f"处理文件 {input_path} 时出错: {e}")

def crop_to_fixed_size(input_path, output_path, target_size=(256, 256)):
    # 打开图像文件
    image = Image.open(input_path)

    # 获取图像的宽度和高度
    width, height = image.size

    # 计算裁剪的左上角和右下角坐标，以确保裁剪后的大小为目标大小
    left = (width - target_size[0]) // 2
    top = (height - target_size[1]) // 2
    right = left + target_size[0]
    bottom = top + target_size[1]

    # 裁剪图像
    cropped_image = image.crop((left, top, right, bottom))

    # 保存裁剪后的图像
    cropped_image.save(output_path)



# 输入文件夹路径和输出文件夹路径
input_folder_path = r"C:\Users\scaaa\Downloads\Compressed\tooth.v4i.coco-segmentation\train"
output_folder_path = r"C:\Users\scaaa\Downloads\Compressed\tooth.v4i.coco-segmentation\train512"

# 批量缩放图片
img_resize(input_folder_path, output_folder_path, (512,512))
# crop_to_fixed_size(r"D:\tempdataset\CHASEDB1\masks512\0\Image_01L_1stHO.png",r"D:\tempdataset\CHASEDB1\masks512\0\Image_01L_1stHO2.png")


