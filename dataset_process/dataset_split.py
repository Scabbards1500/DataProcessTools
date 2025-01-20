import os
import shutil
import random


def split_dataset(input_dir, output_dir1, output_dir2, split_ratio):
    """
    Split files from input directory into two output directories based on the given ratio.

    Parameters:
        input_dir (str): Path to the input directory containing files to be split.
        output_dir1 (str): Path to the first output directory.
        output_dir2 (str): Path to the second output directory.
        split_ratio (float): Ratio for splitting files into output_dir1 (e.g., 0.8 for 80%).
    """
    if not os.path.exists(output_dir1):
        os.makedirs(output_dir1)
    if not os.path.exists(output_dir2):
        os.makedirs(output_dir2)

    # Get all files from the input directory
    files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    random.shuffle(files)  # Shuffle the files to ensure randomness

    # Calculate split index
    split_index = int(len(files) * split_ratio)

    # Split files
    files_for_dir1 = files[:split_index]
    files_for_dir2 = files[split_index:]

    # Copy files to respective output directories
    for file in files_for_dir1:
        shutil.copy(os.path.join(input_dir, file), os.path.join(output_dir1, file))
    for file in files_for_dir2:
        shutil.copy(os.path.join(input_dir, file), os.path.join(output_dir2, file))

    print(f"Total files: {len(files)}")
    print(f"Files in {output_dir1}: {len(files_for_dir1)}")
    print(f"Files in {output_dir2}: {len(files_for_dir2)}")


if __name__ == "__main__":
    # Example usage
    input_directory = r"D:\tempdataset\tooth_photo\cutted_bound_img"  # Replace with your input folder path
    output_directory1 = r"D:\tempdataset\tooth_photo\cutted_bound\Train"  # Replace with first output folder path
    output_directory2 = r"D:\tempdataset\tooth_photo\cutted_bound\Val"  # Replace with second output folder path
    split_ratio = 0.8  # Replace with your desired split ratio (e.g., 0.8 for 80% training and 20% testing)

    split_dataset(input_directory, output_directory1, output_directory2, split_ratio)
