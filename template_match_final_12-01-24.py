#### FINAL SCRIPT USE IN CONJUNCTION WITH FIJI TO COMPLETE & CHECK EGG COUNTS
## Dr Zac Wylde, Postdoctoral Fellow, UNSW 2024, wyldescience@gmail.com
## This script uses opencv template matching to identify and count eggs of Folsomia canida imaged using a dissection scope with limited resolution.
## Additionally, it writes the results to a csv file and pulls details relating to isoline, generation, age and treatment.


import skimage
import numpy as np
import os
import csv
from skimage.draw import circle_perimeter
import glob

def extract_info_from_filename(filename):
    # Extracting Isoline, Generation, Age, and Treatment from the filename
    iso = None
    gen = None
    age = None
    treat = None

    for part in filename.split("_"):
        if part.startswith('I') and part[1:].isdigit():
            iso = int(part[1:])
        elif part.startswith('F') and part[1:].isdigit():
            gen = int(part[1:])
        elif part.startswith('O') or part.startswith('Y'):
            age = part[0]
        elif part.lower() in ['swi', 'con']:
            treat = part.upper()

    return iso, gen, age, treat

def template_matching(image_path, template, csv_writer):
    # import image
    im = skimage.io.imread(image_path)

    # convert to gray and create a smoothed version
    im_gray = skimage.color.rgb2gray(im)
    im_gauss = skimage.filters.gaussian(im_gray, sigma=2)

    # create a simple binary mask to avoid detecting eggs in the background
    mask = (im_gauss > 0.4)

    # compare image and template
    result = skimage.feature.match_template(im_gray, template, pad_input=True)

    # mask the output result
    result_masked = result * mask

    # get local maxima
    coords = skimage.feature.peak_local_max(result_masked, threshold_abs=0.5, threshold_rel=0.1, min_distance=4, exclude_border=True)

    # print the number of matches
    num_matches = len(coords)
    print(f"Number of matches found in {image_path}: {num_matches}")

    # Extract date from the image filename (assuming DD-MM-YY format)
    date_str = os.path.basename(image_path).split("_")[-1].split(".")[0]
    day, month, year = map(int, date_str.split('-'))
    date = f"{year + 2000}-{month:02d}-{day:02d}"  # Assuming year is in 20YY format

    # Extract additional information from the filename
    isoline, generation, age, treatment = extract_info_from_filename(os.path.basename(image_path))

    # Write the result to CSV (without the .tif extension in the filename)
    csv_writer.writerow([
        os.path.splitext(os.path.basename(image_path))[0],
        num_matches,
        date,
        isoline,
        generation,
        age,
        treatment,
        "",  # false_pos
        "",  # false_neg
        ""   # final_count
    ])

    # Create a copy for visualization
    im_vis = np.copy(im)

    # Draw the outlines on the visualization image
    for coord in coords:
        rr, cc = circle_perimeter(coord[0], coord[1], radius=5, shape=im.shape)
        im_vis[rr, cc] = [255, 0, 0]  # Red color for outline

    # Save the result as a new image
    output_path = os.path.join("C:/Users/wylde/Desktop/Folsomia candida/Data/stardist napari/images/Matches/",
                               f"{os.path.splitext(os.path.basename(image_path))[0]}_matches.tif")
    skimage.io.imsave(output_path, im_vis)

    # Show the visualization in Napari
    #viewer = napari.Viewer()
    #viewer.add_image(im_vis)

    # Show the Napari viewer
    #napari.run()

# Path to the template image
template_path = "C:/Users/wylde/Desktop/Folsomia candida/Data/stardist napari/images/Train/I1_F1_O20_SWI_R1_13-09-23.tif"
template = skimage.io.imread(template_path, as_gray=True)[333:341, 456:464]  # Extract a region from the image as a template

# Path to the images folder to process
image_folder = "C:/Users/wylde/Desktop/Folsomia candida/Data/stardist napari/images/Train/"

# Get a list of all image files with .tif extension in the folder
tif_paths = glob.glob(os.path.join(image_folder, "*.tif"))

# Get a list of all image files with .jpg extension in the folder
jpg_paths = glob.glob(os.path.join(image_folder, "*.jpg"))

# Combine the lists
image_paths = tif_paths + jpg_paths

print(image_paths)

# Open the CSV file for writing or append if it already exists
csv_file_path = "C:/Users/wylde/Desktop/Folsomia candida/Data/stardist napari/images/Matches/results.csv"
mode = 'a' if os.path.exists(csv_file_path) else 'w'

fieldnames = ['image', 'match', 'date', 'iso', 'gen', 'age', 'treat', 'false_pos', 'false_neg', 'final_count']

with open(csv_file_path, mode=mode, newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # If the file is newly created, write the header
    if mode == 'w':
        csv_writer.writerow(fieldnames)

    # Perform template matching for each image
    for image_path in image_paths:
        template_matching(image_path, template, csv_writer)
