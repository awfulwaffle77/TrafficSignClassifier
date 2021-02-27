import os
import cv2
import numpy as np
from operator import add

PATH_SIGNS_DIR = "/home/awfulwaffle/Downloads/GTSRB/Final_Training/Images"
# PATH_SIGNS_DIR = os.path.join(PATH_IMAGES

directories = os.listdir(PATH_SIGNS_DIR)
for directory in directories:
    files_path = os.path.join(PATH_SIGNS_DIR, directory)
    images_names = os.listdir(files_path)
    base_img = np.zeros((128, 128, 3), dtype=np.float)
    for image in images_names:
        if image[-4:] == ".csv":
            continue
        img = cv2.imread(os.path.join(files_path, image))
        img = cv2.resize(img, (128, 128))
        base_img += img / (len(images_names) - 1)
    # base_img = base_img/(len(images_names) - 1)
    #    base_img = base_img.astype(int)
    cv2.imwrite(os.path.join(PATH_SIGNS_DIR, "means", str(directory) + ".jpg"), np.array(np.round(base_img), np.uint8))
    print("Written ", str(directory + ".jpg"))
