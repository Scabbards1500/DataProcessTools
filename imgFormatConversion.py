from PIL import Image
import os



def imgformatconversion(input_folder, output_folder):

    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)

        # 这里是处理方式
        # to_bmp(input_path,output_path)
        # to_jpeg(input_path,output_folder)
        to_png(input_path,output_folder)


def to_bmp(input_path, output_path):
    # 打开JPEG图片
    with Image.open(input_path) as img:
        # 将图片保存为BMP格式,也可以是别的模式
        img.save(output_path, "BMP")


def to_jpeg(input_path, output_path):
    image = Image.open(input_path)

    # 构建输出文件名
    base_name = os.path.basename(input_path).split('.')[0]
    output_filename = os.path.join(output_path,f"{base_name}.jpg")
    # 保存为JPEG格式
    image.save(output_filename, 'JPEG')

    print(f"已将 {input_path} 转换为 {output_filename}")


def to_png(input_path, output_path):
    image = Image.open(input_path)

    # 构建输出文件名
    base_name = os.path.basename(input_path).split('.')[0]
    output_filename = os.path.join(output_path,f"{base_name}.png")
    # 保存为JPEG格式
    image.save(output_filename, 'PNG')

    print(f"已将 {input_path} 转换为 {output_filename}")



if __name__ == '__main__':
    input_image_path = r"D:\tempdataset\test\CHASE\test\input"
    output_image_path = r"D:\tempdataset\test\CHASE\test\input2"
    imgformatconversion(input_image_path, output_image_path)