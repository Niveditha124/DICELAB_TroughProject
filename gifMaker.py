import os
import re
from PIL import Image

# Define a function to extract the numeric part from the filename
def extract_numeric_part(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else -1

def create_gif(png_folder, output_gif, duration=100):
    images = []

    # Get a list of all PNG files in the folder
    png_files = [f for f in os.listdir(png_folder) if f.endswith('.png')]
    
    # Sort the files to maintain the order of frames
    # png_files.sort()
    sorted_filenames = sorted(png_files, key=extract_numeric_part)
    print(sorted_filenames)
    input()

    for png_file in sorted_filenames:
        img_path = os.path.join(png_folder, png_file)
        img = Image.open(img_path)
        images.append(img)

    # Save the images as a GIF
    images[0].save(output_gif, save_all=True, append_images=images[1:], optimize=False, duration=duration, loop=0)

if __name__ == "__main__":
    # Replace these paths with your PNG folder path and the desired output GIF path
    png_folder_path = "my_folder_2023_12_26_16_37_54\images/flowprofile"
    output_gif_path = "my_folder_2023_12_26_16_37_54/videos/flowprofile - CodeArrayWorks.gif"

    create_gif(png_folder_path, output_gif_path)