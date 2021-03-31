import os
import sys
import cv2
import numpy as np

HEADLINE = "#no:truth\t"
HEIGHT = 28
WIDTH = 28
X_TRAIN_FILE = "./gtsrb-train-x-128.knd"
Y_TRAIN_FILE = "./gtsrb-train-y-128.knd"
TEST_FILE = "./gtsrb-test-128.knd"
MAX_CLASSES = 3  # Max classes to read from files 
MAX_IMAGES = 300

classes = ["40", "21", "04"]
classes_test = ["40", "21", "04"]  # checked with debug and hardcoded the exact order

def write_headline_to_output(opened_file_pics, opened_file_label = None):
    opened_file_pics.write(HEADLINE)
    for i in range(HEIGHT):
        for j in range(WIDTH):
            for k in range(3):
                opened_file_pics.write(str(i) + ":" + str(j) + ":" + str(k) + "\t")
    opened_file_pics.write("\n")

    if opened_file_label:
        opened_file_label.write(HEADLINE)
        for c in classes:
            opened_file_label.write(c + "\t")
        opened_file_label.write("\n")


if(sys.argv[1] == "train"):
    fileName_train = "/home/awfulwaffle/Downloads/GTSRB/Final_Training/Images/"
    f_train_x = open(X_TRAIN_FILE, "w")
    f_train_y = open(Y_TRAIN_FILE, "w")

    # WRITING THE FIRST LINE WITH THE HEADLINE

    write_headline_to_output(f_train_x, f_train_y)
    
    # GOING THROUGH ALL FILES IN THE DIRECTORY AND WRITING THEM TO FILE

    class_index = -1  # First file is null for some reason, so we ignore it starting from a lower index
    index = 1  # index/ID of the current image being written
    files_index = 0  # Index in a images directory, used to calculate how many images I have traversed
    for subdir, dirs, files in os.walk(fileName_train):
        if class_index >= MAX_CLASSES:
            break
        for file in files:
            if files_index == MAX_IMAGES:
                break
            filename = os.path.join(subdir, file)
            im = cv2.imread(filename)
            im = cv2.resize(im, (WIDTH, HEIGHT))
            im = np.reshape(im, WIDTH * HEIGHT * 3)
            indexClass = str(index) + ":" + str.split(subdir,"\/")[-1][-2:] + "\t"  # "index:className\t" 
            index += 1
            f_train_x.write(indexClass)
            f_train_y.write(indexClass)
            for pixel in im:
                f_train_x.write(str(pixel) + "\t")
            for c in classes:
                lastClass = str.split(subdir,"\/")[-1][-2:]  # last 2 digits from subdir, which represents the class. Ex: "04"
                if lastClass == c:
                    f_train_y.write("1\t")
                else:
                    f_train_y.write("0\t")
            files_index += 1
            f_train_x.write("\n")
            f_train_y.write("\n")
        class_index += 1
        files_index = 0
    f_train_x.close()
    print("Train file(s) written.")

elif sys.argv[1] == "test":
    fileName_test = "/home/awfulwaffle/Downloads/GTSRB/Final_Test/selected2"
    f_test = open(TEST_FILE, "w")

    write_headline_to_output(f_test)

    index = 1
    files_index = 0
    for subdir, dirs, files in os.walk(fileName_test):
        for file in files:
            if files_index == MAX_IMAGES:
                break
            filename = os.path.join(subdir, file)
            im = cv2.imread(filename)
            im = cv2.resize(im, (WIDTH, HEIGHT))
            im = np.reshape(im, WIDTH * HEIGHT * 3)
            indexClass = str(index) + ":" + str(classes_test[index-1]) + "\t"  # "index:className\t" 
            index += 1
            f_test.write(indexClass) 
            for pixel in im:
                f_test.write(str(pixel) + "\t")
            files_index += 1
            f_test.write("\n")
        files_index = 0
    f_test.close()
    print("Test file written.")
else:
    print("Script should be run as: ", sys.argv[0], " ", "train/test.")