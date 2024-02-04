import cv2
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from scipy import signal

def make_mexican_hat_kernel(points=21, a=4):
    a = float(a)
    weights = signal.ricker(points, a)
    center_to_side_length = int(np.floor(points / 2))
    weights = weights[center_to_side_length:]

    def get_pixel_distance_from_center(image):
        center = np.array([(image.shape[0]) / 2, (image.shape[1]) / 2])
        distances = np.linalg.norm(np.indices(image.shape) - center[:, None, None] + 0.5, axis=0)
        return distances

    kernel = np.zeros((points, points))
    distances = get_pixel_distance_from_center(kernel)

    sum = 0
    height, width = kernel.shape
    for y in range(height):
        for x in range(width):
            dist = int(np.round(distances[y, x]))
            if dist > center_to_side_length:
                weight = 0
            else:
                weight = weights[dist]

            kernel[y, x] = weight
            sum = sum + weight

    sum2 = 0
    num_pixels = height * width
    per_pixel_weight_offset = sum / num_pixels
    for y in range(height):
        for x in range(width):
            kernel[y, x] = kernel[y, x] - per_pixel_weight_offset
            sum2 = sum2 + kernel[y, x]

    assert sum2 < 0.1, "this should be close to zero"

    return kernel

def process_image(image_path, output_folder):
    orig_img = cv2.imread(image_path)
    img_name = os.path.basename(image_path)

    hsv = cv2.cvtColor(orig_img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    img = v

    img = cv2.medianBlur(img, 3)

    kernel = make_mexican_hat_kernel(points=5, a=4)
    for _ in range(3):
        img = cv2.filter2D(img, -1, kernel)

    _, img = cv2.threshold(img, 30, 255, cv2.THRESH_BINARY_INV)

    params = cv2.SimpleBlobDetector_Params()

    params.minThreshold = 10
    params.maxThreshold = 200
    params.thresholdStep = 5
    params.minRepeatability = 2
    params.minDistBetweenBlobs = 0.1

    params.filterByArea = True
    params.minArea = 2 ## may need to tweak to get right results
    params.maxArea = 200

    # Filter by circularity
    params.filterByCircularity = True
    params.minCircularity = 0.6
    params.maxCircularity = 1

    detector = cv2.SimpleBlobDetector_create(params)

    keypoints = detector.detect(img)

    n_cells_blob = len(keypoints)

    blob_img = cv2.drawKeypoints(orig_img, keypoints, np.array([]), (0, 0, 255),
                                 cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    output_img_path = os.path.join(output_folder, img_name)
    cv2.imwrite(output_img_path, blob_img)

    return img_name, n_cells_blob

# Folder containing input images
input_folder = "C:/Users/wylde/Desktop/Folsomia candida/Data/egg count images/cropped"
# Folder to save output images with blobs detected
output_folder = "C:/Users/wylde/Desktop/Folsomia candida/Data/egg count images/blobs detected"
# CSV file to save results
csv_file = "C:/Users/wylde/Desktop/Folsomia candida/Data/egg count images/results.csv"

os.makedirs(output_folder, exist_ok=True)

image_results = []

for root, dirs, files in os.walk(input_folder):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image_path = os.path.join(root, file)
            img_name, n_cells_blob = process_image(image_path, output_folder)
            image_results.append((img_name, n_cells_blob))

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Image Name", "Eggs Detected"])
    writer.writerows(image_results)

print("Processing complete.")
