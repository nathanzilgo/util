import os
import shutil
import argparse
from tqdm import tqdm
from PIL import Image


def compress_image(input_path, output_path, quality=85):
    """
    Compresses an image located at input_path and saves it to output_path with specified quality.
    """
    try:
        img = Image.open(input_path)
        img.save(output_path, quality=quality)
    except Exception as e:
        print(f"Error compressing image {input_path}: {e}")


def compress_images_in_folder(input_folder, output_folder, quality=85):
    """
    Compresses all images in input_folder and saves them to output_folder with specified quality.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(input_folder):
        raise ValueError(f"Input folder {input_folder} does not exist.")

    for root, _, files in tqdm(
        os.walk(input_folder),
        total=len(os.listdir(input_folder)),
        desc="Compressing images recursively",
    ):

        print(f"Compressing images in {root}.")
        for filename in files:
            print(f"Compressing {filename}.")
            input_path = os.path.join(root, filename)
            output_path = os.path.join(
                output_folder, os.path.relpath(input_path, input_folder)
            )
            if (
                filename.endswith(".jpg")
                or filename.endswith(".jpeg")
                or filename.endswith(".png")
            ):
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                compress_image(input_path, output_path, quality=quality)
            else:
                print(f"{filename} is not an image file. Skipping...")
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                shutil.copy2(input_path, output_path)

    print("Image compression completed.")


def folder_size(folder):
    """
    Calculates the total size of all files in a folder recursively.
    """
    total_size = 0
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
    return total_size


def folder_size_difference(folder1, folder2):
    """
    Compares the sizes of two folders and prints the difference in megabytes.
    """
    size1 = folder_size(folder1)
    size2 = folder_size(folder2)
    difference_mb = abs(size1 - size2) / (1024 * 1024)  # Convert bytes to megabytes
    print(f"Difference in size between {folder1} and {folder2}: {difference_mb:.2f} MB")


def main():
    parser = argparse.ArgumentParser(
        description="Compresses all images in a folder and saves them to another folder with specified quality."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="Path to the input folder containing images",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="Path to the output folder for compressed images",
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=int,
        default=85,
        help="Quality level of the compressed images (0-100)",
    )

    args = parser.parse_args()

    compress_images_in_folder(args.input, args.output, args.quality)
    folder_size_difference(args.input, args.output)


if __name__ == "__main__":
    main()
