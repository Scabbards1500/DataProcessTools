from PIL import Image
import os


def resize_images(input_dir, output_dir, scale_factor):
    """
    Resize all images in a directory by a given scale factor.

    Parameters:
        input_dir (str): Path to the input directory containing images.
        output_dir (str): Path to the output directory to save resized images.
        scale_factor (float): Scaling factor (e.g., 0.1 for 1/10 size, 2 for double size).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)

        # Ensure the file is an image
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')):
            print(f"Skipping non-image file: {filename}")
            continue

        try:
            # Open and resize the image
            with Image.open(input_path) as img:
                new_width = int(img.width * scale_factor)
                new_height = int(img.height * scale_factor)
                resized_img = img.resize((new_width, new_height), Image.LANCZOS)

                # Save the resized image
                output_path = os.path.join(output_dir, filename)
                resized_img.save(output_path)
                print(f"Resized and saved: {output_path}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    # Example usage
    input_directory = r"D:\tempdataset\tooth_photo\selected_photo\Train_ori"  # Replace with your input directory
    output_directory = r"D:\tempdataset\tooth_photo\selected_photo\Train"  # Replace with your output directory
    scale = 0.1  # Replace with your desired scale factor (e.g., 0.1 for 1/10 size)

    resize_images(input_directory, output_directory, scale)
    input_directory2 = r"D:\tempdataset\tooth_photo\selected_photo\Val_ori"  # Replace with your input directory
    output_directory2 = r"D:\tempdataset\tooth_photo\selected_photo\Val"  # Replace with your output directory
    resize_images(input_directory2, output_directory2, scale)
