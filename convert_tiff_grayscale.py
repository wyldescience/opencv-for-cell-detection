import os
from PIL import Image

# Specify the input folder containing TIFF files
input_folder = "C:/Users/wylde/Desktop/CSBdeep_model/TIF/train_image_tif"

# Specify the output folder for grayscale images
output_folder = "C:/Users/wylde/Desktop/CSBdeep_model/TIF/train_image_grayscale"

# Ensure the output folder exists or create it if necessary
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".tiff") or filename.endswith(".tif"):
        # Construct the full path to the input image
        input_image_path = os.path.join(input_folder, filename)

        # Open the TIFF image
        tiff_image = Image.open(input_image_path)

        # Convert the TIFF image to grayscale
        grayscale_image = tiff_image.convert("L")

        # Construct the full path to the output grayscale image
        output_image_path = os.path.join(output_folder, os.path.splitext(filename)[0] + "_grayscale.tif")

        # Save the grayscale image to the output folder
        grayscale_image.save(output_image_path)

        # Close the images
        tiff_image.close()
        grayscale_image.close()
