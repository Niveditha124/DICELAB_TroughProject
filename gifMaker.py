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
    png_height = folder_name + '/images/height'
