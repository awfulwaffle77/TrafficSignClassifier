import os
import cv2
import numpy as np

HEADLINE = "#no:truth\t"
HEIGHT = 28
WIDTH = 28
X_TRAIN_FILE = "./gtsrb-train-grey-x.kan"
Y_TRAIN_FILE = "./gtsrb-train-grey-y.kan"
MAX_CLASSES = 3  # Max classes to read from files 
MAX_IMAGES = 300

classes = ["40", "21", "04"]

folderName = "/home/awfulwaffle/Downloads/GTSRB/Final_Training/Images/"
f_train_x = open(X_TRAIN_FILE, "w")
f_train_y = open(Y_TRAIN_FILE, "w")

# WRITING THE FIRST LINE WITH THE HEADLINE

f_train_x.write(HEADLINE)
# print(HEADLINE)
for i in range(HEIGHT):
    for j in range(WIDTH):
        f_train_x.write(str(i) + ":" + str(j) + "\t")
f_train_x.write("\n")

f_train_y.write(HEADLINE)
for c in classes:
    f_train_y.write(c + "\t")
f_train_y.write("\n")

# GOING THROUGH ALL FILES IN THE DIRECTORY AND WRITING THEM TO FILE

class_index = -1  # First file is null for some reason, so we ignore it starting from a lower index
index = 1
files_index = 0
for subdir, dirs, files in os.walk(folderName):
    if class_index >= MAX_CLASSES:
        break
    for file in files:
        if files_index == MAX_IMAGES:
            break
        filename = os.path.join(subdir, file)
        im = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        im = cv2.resize(im, (WIDTH, HEIGHT))
        im = np.reshape(im, WIDTH * HEIGHT)
        indexClass = str(index) + ":" + str.split(subdir,"\/")[-1][-2:] + "\t"  # "index:className\t" 
        index += 1
        f_train_x.write(indexClass)
        f_train_y.write(indexClass)
        for pixel in im:
            f_train_x.write(str(f'{pixel/255:.2f}') + "\t")
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