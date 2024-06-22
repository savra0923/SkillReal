import cv2
import os
import csv
import numpy as np

def find_differences(img1, img2, threshold=30):
    # Ensure both images have the same dimensions
    if img1.shape != img2.shape:
        raise ValueError("Images must have the same dimensions")

    # Find the absolute differences between the pictures
    diff = cv2.absdiff(img1, img2)

    # Create a mask for differences that exceed the threshold
    significant_diff_mask = diff > threshold

    # Apply the mask to the original difference image
    thresholded_diff = np.zeros_like(diff)
    thresholded_diff[significant_diff_mask] = diff[significant_diff_mask]

    return thresholded_diff

def analyze_changes(thresholded_diff):
    # Use connected components analysis to identify distinct changes
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(thresholded_diff, connectivity=8)

    # Filter out small changes (noise)
    min_area = 50  
    significant_changes = [stat for stat in stats[1:] if stat[4] > min_area]  # Exclude background

    num_changes = len(significant_changes)
    changes_info = [{"change_id": i, "pixels": change[4]} for i, change in enumerate(significant_changes, 1)]
    return num_changes, changes_info

def save_changes_to_csv(changes_info, csv_path):
    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ['change_id', 'pixels']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for change in changes_info:
            writer.writerow(change)

def process_test_case(folder_path, results_folder, threshold):
    # Get list of image files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if len(image_files) != 2:
        print(f"Error: Folder {folder_path} should contain exactly 2 images.")
        return

    # Read the images
    img1_path = os.path.join(folder_path, image_files[0])
    img2_path = os.path.join(folder_path, image_files[1])
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)

    # Find differences
    diff_image = find_differences(img1, img2, threshold)

    # Analyze changes
    num_changes, changes_info = analyze_changes(diff_image)

    # Save the thresholded difference image in the results folder
    test_case_name = os.path.basename(folder_path)
    diff_image_path = os.path.join(results_folder, f"{test_case_name}_diff.png")
    cv2.imwrite(diff_image_path, diff_image)

    # Save changes info to CSV
    csv_path = os.path.join(results_folder, f"{test_case_name}_changes.csv")
    save_changes_to_csv(changes_info, csv_path)

    print(f"Results for test case: {test_case_name}")
    print(f"Thresholded difference image saved as: {diff_image_path}")
    print(f"Number of significant changes: {num_changes}")
    print(f"Number of specific pixals changed for each siginificant change is located in: {csv_path}\n")

def main():
    root_folder = "test_cases"
    threshold = 50

    results_folder = os.path.join(root_folder, "results")
    
    # Create the results folder if it doesn't exist
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    # Iterate through all subdirectories in the root folder
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path) and folder_name != "results":
            process_test_case(folder_path, results_folder, threshold)

if __name__ == "__main__":
    main()