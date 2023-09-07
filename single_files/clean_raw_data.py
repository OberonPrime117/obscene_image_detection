
# import os
# import concurrent.futures
# import cv2
# import numpy as np

# # Define the directory path
# dir_path = 'data'

# # Initialize an empty list to store the file contents
# file_contents = []
# img1 = cv2.imread('image_not_available.jpg')
# # Loop through all the files in the directory and its subdirectories
# for root, dirs, files in os.walk(dir_path):
#     for file in files:
#         img2 = cv2.imread(os.path.join(root, file))
#         try:
#             mse = np.mean((img1 - img2) ** 2)
#             if mse < 10:
#                 print("The images are similar")
#             else:
#                 print("The images are different")
#         except ValueError:
#             pass


import os
import concurrent.futures
import cv2
import numpy as np
from PIL import Image

# Define the directory path
dir_path = 'data'

# Initialize an empty list to store the file contents
file_contents = []
img1 = cv2.imread('image_not_available.jpg')

# Define a function to compare two images
def compare_images(img2, loc):
    try:
        mse = np.mean((img1 - img2) ** 2)
        if mse < 10:
            os.remove(loc)
            print("deleted, score: ", str(mse))
        else:
            print("The images are different")
    except ValueError:
        pass

def remove_mp4(img2):
    imgval = img2[:-4]
    img2_name = imgval.split("_")
    if "mp4" == img2_name[-1] or "gif" == img2_name[-1]:
        os.remove(img2)
        print("deleted mp4")

def corrupted_img(img2):
    try:
        with Image.open(img2) as img:
            img.verify()
    except (IOError, SyntaxError) as e:
        os.remove(img2)
        print("deleted corrupted image")

# 0 - COMPARE IMAGE DELETION ACC TO IMGUR TEMPLATE
# 1 - MP4, GIF DELETION
# 2 - CORRUPTED IMAGE DELETION
flag = 2


# Loop through all the files in the directory and its subdirectories
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    for root, dirs, files in os.walk(dir_path):
        print("Hello")
        for file in files:
            if flag == 0:
                img2 = cv2.imread(os.path.join(root, file))
                loc = os.path.join(root, file)
                executor.submit(compare_images, img2, loc)
            elif flag == 1:
                img2 = os.path.join(root, file)
                executor.submit(remove_mp4, img2)
            elif flag == 2:
                img2 = os.path.join(root, file)
                executor.submit(corrupted_img, img2)
