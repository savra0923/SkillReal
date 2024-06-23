import os
import argparse
import random
import csv
import matplotlib.pyplot as plt
import matplotlib.patches as patches

DEFAULT_NUM_ROIS = 50
DEFAULT_IMAGE_WIDTH = 1000
DEFAULT_IMAGE_HEIGHT = 1000
DEFAULT_MIN_SIZE = 10
DEFAULT_MAX_SIZE = 100

def squares_overlap(square1, square2):
    """
    Check if two squares overlap.
    
    Parameters:
    square1 (tuple): A tuple (x1, y1, x2, y2) where (x1, y1) are the coordinates of the
                     top-left corner and (x2, y2) are the coordinates of the bottom-right
                     corner of the first square.
    square2 (tuple): A tuple (x1, y1, x2, y2) for the second square with similar coordinates
                     representing the top-left and bottom-right corners.
    
    Returns:
    bool: True if the squares overlap, False otherwise.
    
    This function checks if two given squares, represented by their top-left and bottom-right
    corners, overlap with each other. It returns True if there is any overlap and False if
    there is none.
    """
    x1, y1, x2, y2 = square1
    x3, y3, x4, y4 = square2
    
    # Check if one rectangle is to the left of the other
    if x2 < x3 or x4 < x1:
        return False
    
    # Check if one rectangle is above the other
    if y2 < y3 or y4 < y1:
        return False
    
    # If we get here, the rectangles overlap
    return True

def generate_and_test_rois(N, image_size=(1000, 1000), min_size=10, max_size=100):
    """
    Generate random ROIs and test if they overlap.
    
    Parameters:
    N (int): The number of ROIs to generate.
    image_size (tuple): The size of the image as (image_width, image_height), 
                        used as the limit size for ROIs generation. Default is (1000, 1000).
    min_size (int): The minimum size of an ROI. Default is 10.
    max_size (int): The maximum size of an ROI. Default is 100.
    
    Returns:
    tuple: A tuple containing:
           - rois (list of tuples): A list of generated ROIs, each represented as 
             a tuple (x, y, x2, y2) where (x, y) are the coordinates of the top-left 
             corner and (x2, y2) are the coordinates of the bottom-right corner.
           - overlapping_rois (set of int): A set of indices corresponding to the 
             ROIs that overlap.
    
    This function generates N random ROIs within the specified image size and 
    tests whether they overlap. ROIs that overlap with any other ROI are identified 
    and their indices are stored in a set.
    """
    rois = []
    for _ in range(N):
        size = random.randint(min_size, max_size)
        x = random.randint(0, image_size[0] - size)
        y = random.randint(0, image_size[1] - size)
        rois.append((x, y, x + size, y + size))
    
    overlapping_rois = set()
    for i in range(N):
        for j in range(i+1, N):
            if squares_overlap(rois[i], rois[j]):
                overlapping_rois.add(i)
                overlapping_rois.add(j)
    
    return rois, overlapping_rois

def visualize_rois(rois, overlapping_rois, image_size):
    """
    Visualizes Regions of Interest (ROIs) on an image.

    Parameters:
    rois (list of tuples): A list of tuples where each tuple represents an ROI
                           in the format (x, y, x2, y2) with:
                           - x, y: Coordinates of the top-left corner.
                           - x2, y2: Coordinates of the bottom-right corner.
    overlapping_rois (set of int): A set of indices corresponding to the ROIs
                                   that are overlapping.
    image_size (tuple): A tuple representing the size of the image in the format
                        (width, height).

    Returns:
    None

    This function plots the specified ROIs on a matplotlib figure, with red
    rectangles for overlapping ROIs and blue rectangles for non-overlapping ROIs.
    The ROIs are labeled with their index numbers. The y-axis is inverted to
    match typical image coordinate systems.
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0, image_size[0])
    ax.set_ylim(0, image_size[1])
    ax.set_aspect('equal')
    
    for i, roi in enumerate(rois):
        x, y, x2, y2 = roi
        width = x2 - x
        height = y2 - y
        color = 'red' if i in overlapping_rois else 'blue'
        rect = patches.Rectangle((x, y), width, height, linewidth=1, edgecolor=color, facecolor='none')
        ax.add_patch(rect)
        ax.text(x, y, str(i+1), fontsize=8, color='black')
    
    plt.title(f'Visualization of {len(rois)} ROIs\n'
              f'Red: Overlapping ({len(overlapping_rois)}), '
              f'Blue: Non-overlapping ({len(rois) - len(overlapping_rois)})')
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    plt.gca().invert_yaxis()  # Invert y-axis to match image coordinates
    plt.show()

def run_single_test(num_rois, image_width, image_height, min_size, max_size):
    print(f"Running single test with parameters: num_rois={num_rois}, "
          f"image_width={image_width}, image_height={image_height}, min_size={min_size}, max_size={max_size}")
    rois, overlapping_rois = generate_and_test_rois(num_rois, (image_width, image_height), min_size, max_size)
    print(f"Generated {num_rois} ROIs")
    print(f"Number of overlapping ROIs: {len(overlapping_rois)}")
    print(f"Number of non-overlapping ROIs: {num_rois - len(overlapping_rois)}")
    visualize_rois(rois, overlapping_rois, (image_width, image_height))

def run_multiple_tests(csv_file):
    """
    Run the main test case multiple times as specified in a configuration file.

    Parameters:
    test_cases_folder (str): The path to the folder containing the test cases configuration file.

    Returns:
    None

    This function reads the number of iterations to run from a configuration file named "config.txt"
    located in the specified folder, and runs the main function for each iteration.
    """
    
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for i, row in enumerate(reader):
            try:
                num_rois, image_width, image_height, min_size, max_size = map(int, row)
                print(f"Running test case {i+1} with parameters: num_rois={num_rois}, "
                      f"image_width={image_width}, image_height={image_height}, min_size={min_size}, max_size={max_size}")
                rois, overlapping_rois = generate_and_test_rois(num_rois, (image_width, image_height), min_size, max_size)
                print(f"Generated {num_rois} ROIs")
                print(f"Number of overlapping ROIs: {len(overlapping_rois)}")
                print(f"Number of non-overlapping ROIs: {num_rois - len(overlapping_rois)}")
                visualize_rois(rois, overlapping_rois, (image_width, image_height))
            except ValueError:
                print(f"Invalid parameters in line {i+1}: {row}. Skipping this test case.")


def main():
    """
    Overlapping ROIs Tool: Generate and visualize ROIs, color the overlapping ROIs a different color.
    
    This function parses command-line arguments to generate a specified number of ROIs within a given
    image size, and visualizes these ROIs, highlighting those that overlap.
    
    Command-line Arguments:
    -n, --num_rois (int, optional): Number of ROIs to generate. Default is 50.
    -iw, --image_width (int, optional): Width of the image. Default is 1000.
    -ih, --image_height (int, optional): Height of the image. Default is 1000.
    -m, --min_size (int, optional): Minimum size of ROI. Default is 10.
    -M, --max_size (int, optional): Maximum size of ROI. Default is 100.
    
    Example Usage:
    python Overlap.py --num_rois 50 --image_width 1000 --image_height 1000 --min_size 10 --max_size 100
    python Overlap.py -n 50 -iw 1000 -ih 1000 -m 10 -M 100
    
    This function changes the current working directory to the script's location, generates ROIs,
    determines which ones overlap, prints the number of generated, overlapping, and non-overlapping
    ROIs, and visualizes them.
    
    Returns:
    None
    """
    parser = argparse.ArgumentParser(
        description='Overlapping ROIs Tool: Generate and visualize ROIs, color the overlapping ROIs a different color.',
        epilog='Example usage for single test: python Overlap.py -n 50 -iw 1000 -ih 1000 -m 10 -M 100\n'
               'Example usage for multiple tests from CSV file: python Overlap.py --csv_file test_cases.csv'
    )
    parser.add_argument('-n', '--num_rois', type=int, default=DEFAULT_NUM_ROIS, help='Number of ROIs to generate.')
    parser.add_argument('-iw', '--image_width', type=int, default=DEFAULT_IMAGE_WIDTH, help='Width of the image.')
    parser.add_argument('-ih', '--image_height', type=int, default=DEFAULT_IMAGE_HEIGHT, help='Height of the image.')
    parser.add_argument('-m', '--min_size', type=int, default=DEFAULT_MIN_SIZE, help='Minimum size of ROI.')
    parser.add_argument('-M', '--max_size', type=int, default=DEFAULT_MAX_SIZE, help='Maximum size of ROI.')
    parser.add_argument('-c', '--csv_file', type=str, help='CSV file containing test cases.')
    args = parser.parse_args()

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if args.csv_file is not None:
        run_multiple_tests(args.csv_file)
    elif args.num_rois is not None and args.image_width is not None and args.image_height is not None \
            and args.min_size is not None and args.max_size is not None:
        run_single_test(args.num_rois, args.image_width, args.image_height, args.min_size, args.max_size)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()