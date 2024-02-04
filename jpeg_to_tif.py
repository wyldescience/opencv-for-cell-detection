

import os
from PIL import Image
import shutil

# Specify the input folder containing JPEG files
input_folder = "C:/Users/wylde/Desktop/CSBdeep_model/Test_images"

# Specify the output folder for TIFF files
output_folder = "C:/Users/wylde/Desktop/CSBdeep_model/TIF/train_image_tif"

# Ensure the output folder exists or create it if necessary
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".tiff") or filename.endswith(".jpeg"):
        # Construct the full path to the input image
        input_image_path = os.path.join(input_folder, filename)

        # Open the JPEG image
        jpeg_image = Image.open(input_image_path)

        # Convert the JPEG image to TIFF format with the .tif extension
        tiff_image = jpeg_image.convert("RGB")

        # Construct the full path to the output TIFF image with the .tif extension
        output_image_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".tif")

        # Save the TIFF image to the output folder with the .tif extension
        tiff_image.save(output_image_path)

        # Close the images
        jpeg_image.close()
        tiff_image.close()

# Optional: Remove the original JPEG files from the input folder if desired
# for filename in os.listdir(input_folder):
#     if filename.endswith(".jpg") or filename.endswith(".jpeg"):
#         os.remove(os.path.join(input_folder, filename))