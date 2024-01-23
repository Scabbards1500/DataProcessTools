from PIL import Image

def jpeg_to_bmp(input_path, output_path):
    # 打开JPEG图片
    with Image.open(input_path) as img:
        # 将图片保存为BMP格式,也可以是别的模式
        img.save(output_path, "BMP")



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



input_path = "C:\\Users\\scaaa\\Desktop\\green.jpg"
output_path = "C:\\Users\\scaaa\\Desktop\\grass.jpg"
crop_to_fixed_size(input_path, output_path)

#jpeg->bmp
input_image_path = "C:\\Users\\scaaa\\Desktop\\grass.jpg"
output_image_path = "C:\\Users\\scaaa\\Desktop\\grass.bmp"
jpeg_to_bmp(input_image_path, output_image_path)