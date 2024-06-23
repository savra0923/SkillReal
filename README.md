# SkillReal
This is answers to the SkillReal home assignment.
This code was writen in python and ran with python 3.12.0.
Please make sure you have the right python compiler.

# Explenations
I was asked to write an explenation for each task. Please refer to 'SkillReal Home Assignment Answers.pdf' for the answers.

# Run the Code
- Navigate to the SkillReal folder.
- run pip install -r requirements.txt
- For question 1, run python ImageComp.py -r path/to/test_cases -t 30.
    - Where -r is the path to the folder with the test cases folders and -t is the threshold for significant differences
    - Each test case is a folder with the 2 images we wish to compare.
- If no parameters were given, default parameters will be used.
- For question 2, python Overlap.py -n 50 -iw 1000 -ih 1000 -m 10 -M 100 or python Overlap.py --csv_file test_cases.csv. Here we can run the code once or multiple times.
    - To run once either give no arguments or change at least 1 of the following:
        - -n Number of ROIs to generate.
        - -iw Width of the image.
        - -ih Height of the image.
        - -m Minimum size of ROI.
        - -M Maximum size of ROI.
    - Parameters that were not changed will use default values.
    - To run multiple times give a path to a test_cases.csv file with all needed parameters. You can use the given test_cases.csv file provided.

# Disclaimer
The image comparison task asked for test case. Except for test case 3, ALL PHOTOS USED ARE NOT MY OWN. I downloaded them from a free stock photo website and changed them a bit.