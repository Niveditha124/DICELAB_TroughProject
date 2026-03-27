import os
import re
import time
from PIL import Image

def extract_numeric_part(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else -1


def create_gif(png_folder, output_gif, duration=100):
    images = []
    png_files = [f for f in os.listdir(png_folder) if f.endswith('.png')]
    sorted_filenames = sorted(png_files, key=extract_numeric_part)

    for png_file in sorted_filenames:
        img_path = os.path.join(png_folder, png_file)
        img = Image.open(img_path)
        images.append(img)

    images[0].save(
        output_gif,
        save_all=True,
        append_images=images[1:],
        optimize=False,
        duration=duration,
        loop=0
    )
    print(f"GIF created: {output_gif}")

if __name__ == "__main__":
    # Replace these paths with your PNG folder path and the desired output GIF path
    folder_name = 'my_folder_' + time.strftime("%Y_%m_%d_%H_%M_%S")
    
    # Define image and video folders
    png_flowprofile = folder_name + "/images/flowprofile"
    png_ucprofile = folder_name + "/images/ucprofile"
    png_kfrprofile = folder_name + "/images/kfrprofile"
    png_iacbchanges = folder_name + "/images/iacbchanges"
    png_flowprofilecontour = folder_name + "/images/flowprofilecontour"
    png_pressureprofile = folder_name + "/images/pressureprofile"


def create_combined_gif(folder1, folder2, folder3, output_gif, duration=100):

    files1 = sorted([f for f in os.listdir(folder1) if f.endswith('.png')], key=extract_numeric_part)
    files2 = sorted([f for f in os.listdir(folder2) if f.endswith('.png')], key=extract_numeric_part)
    files3 = sorted([f for f in os.listdir(folder3) if f.endswith('.png')], key=extract_numeric_part)

    images = []

    for f1, f2, f3 in zip(files1, files2, files3):

        img1 = Image.open(os.path.join(folder1, f1))
        img2 = Image.open(os.path.join(folder2, f2))
        img3 = Image.open(os.path.join(folder3, f3))

        # Ensure same height
        height = max(img1.height, img2.height, img3.height)

        total_width = img1.width + img2.width + img3.width

        combined = Image.new("RGB", (total_width, height))

        x_offset = 0
        for img in [img1, img2, img3]:
            combined.paste(img, (x_offset, 0))
            x_offset += img.width

        images.append(combined)

    images[0].save(
        output_gif,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0
    )

    print(f"Combined GIF created: {output_gif}")
