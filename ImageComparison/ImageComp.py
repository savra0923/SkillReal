import cv2
import os
import argparse
import csv
import numpy as np

DEFAULT_ROOT = 'test_cases'
DEFAULT_THRESHOLD = 50

def find_differences(img1, img2, threshold=30):
    """
    Find and highlight significant differences between two images.

    Parameters:
    img1 (numpy.ndarray): The first input image.
    img2 (numpy.ndarray): The second input image.
    threshold (int, optional): The minimum difference threshold to consider a change significant. Default is 30.

    Returns:
    numpy.ndarray: An image highlighting the significant differences.

    Raises:
    ValueError: If the input images do not have the same dimensions.

    This function compares two images of the same dimensions and calculates the absolute difference between them.
    Differences that exceed the specified threshold are highlighted, while smaller differences are ignored.
    """
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
    """
    Analyze the thresholded difference image to identify and quantify significant changes.

    Parameters:
    thresholded_diff (numpy.ndarray): An image highlighting the significant differences between two input images.

    Returns:
    tuple: A tuple containing:
        - num_changes (int): The number of significant changes detected.
        - changes_info (list of dict): A list of dictionaries, each containing:
            - 'change_id' (int): The identifier of the change.
            - 'pixels' (int): The number of pixels involved in the change.

    This function uses connected components analysis to identify distinct changes in the thresholded difference image.
    Changes smaller than a predefined minimum area are considered noise and ignored.
    """
    # Use connected components analysis to identify distinct changes
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(thresholded_diff, connectivity=8)

    # Filter out small changes (noise)
    min_area = 50  
    significant_changes = [stat for stat in stats[1:] if stat[4] > min_area]  # Exclude background

    num_changes = len(significant_changes)
    changes_info = [{"change_id": i, "pixels": change[4]} for i, change in enumerate(significant_changes, 1)]
    return num_changes, changes_info

def save_changes_to_csv(changes_info, csv_path):
    """
    Save the significant changes information to a CSV file.

    Parameters:
    changes_info (list of dict): A list of dictionaries containing information about the significant changes.
    csv_path (str): The path to the CSV file where the changes information will be saved.

    Returns:
    None

    This function writes the information about significant changes, including the change ID and the number of pixels involved,
    to a CSV file specified by the user.
    """
    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ['change_id', 'pixels']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for change in changes_info:
            writer.writerow(change)

def process_test_case(folder_path, results_folder, threshold):
    """
    Process a test case folder to find and analyze differences between two images.

    Parameters:
    folder_path (str): The path to the folder containing the two images to compare.
    results_folder (str): The path to the folder where results will be saved.
    threshold (int): The minimum difference threshold to consider a change significant.

    Returns:
    None

    This function reads two images from the specified folder, finds significant differences between them,
    analyzes these differences, saves the thresholded difference image and the changes information to the results folder,
    and prints a summary of the results.
    """
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
    """
    Main function for the Image Comparison Tool.

    This function parses command-line arguments, sets up the environment, and processes all test case folders
    in the specified root folder to find and analyze differences between pairs of images.

    Command-line Arguments:
    -r, --root (str, optional): Root folder containing test case subfolders. Each subfolder should contain exactly two images to compare. Default is "test_cases".
    -t, --threshold (int, optional): Threshold for significant differences (0-255). Higher values detect only more significant changes. Default is 50.

    Example Usage:
    python ImageComp.py --root path/to/test_cases --threshold 30
    python ImageComp.py -r path/to/test_cases -t 30

    This function creates a results folder if it does not exist, iterates through all subdirectories in the root folder,
    and processes each test case to find and analyze differences between the images.
    """
    parser = argparse.ArgumentParser(
        description='Image Comparison Tool: Analyzes differences between pairs of images in test case folders.',
        epilog='Example usage: python ImageComp.py --root path/to/test_cases --threshold 30 \npython ImageComp.py -r path/to/test_cases -t 30'
    )
    parser.add_argument(
        '-r',
        '--root', 
        type=str, 
        default=DEFAULT_ROOT, 
        help='Root folder containing test case subfolders. Each subfolder should contain exactly two images to compare. Default: "test_cases"'
    )
    parser.add_argument(
        '-t',
        '--threshold', 
        type=int, 
        default=DEFAULT_THRESHOLD, 
        help='Threshold for significant differences (0-255). Higher values detect only more significant changes. Default: 50'
    )
    args = parser.parse_args()

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    root_folder = args.root
    threshold = args.threshold

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