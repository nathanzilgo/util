from PIL import Image
import os


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

    for root, dirs, files in os.walk(input_folder):
        print(f"Compressing images in {root}.")
        for filename in files:
            print(f"Compressing {filename}.")
            if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
                input_path = os.path.join(root, filename)
                output_path = os.path.join(output_folder, os.path.relpath(input_path, input_folder))
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                compress_image(input_path, output_path, quality=quality)


if __name__ == "__main__":
    input_folder = os.path.abspath("")  # Update with your input folder containing images
    output_folder = os.path.abspath("")  # Update with your output folder for compressed images
    quality = 70  # Adjust the quality level as needed (0 to 100)

    compress_images_in_folder(input_folder, output_folder, quality=quality)
    print("Image compression completed.")
