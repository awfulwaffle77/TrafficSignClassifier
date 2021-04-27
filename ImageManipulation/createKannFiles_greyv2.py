import os
import sys
import cv2
import numpy as np

HEADLINE = "#no:truth\t"
HEIGHT = 120
WIDTH = 160
X_TRAIN_FILE = "../kann_test/mnist_test/kann-data/gtsrb-train-x-160-gray.knd"
Y_TRAIN_FILE = "../kann_test/mnist_test/kann-data/gtsrb-train-y-160-gray.knd"
TEST_FILE = "../kann_test/mnist_test/kann-data/gtsrb-test-grayscale-160.knd"
VALIDATION_FILE = "../kann_test/mnist_test/kann-data/gtsrb-validation-gray-160.knd"  
# the validation dataset will consist of images also used for training(meaning some of the
# images that are in X_TRAIN_FILE are also here)
MAX_CLASSES = 3  # Max classes to read from files 
MAX_IMAGES = 300
MAX_IMAGES_TEST = 200

classes = ["40", "21", "04"]
classes_test = ["40", "21", "04"]  # checked with debug and hardcoded the exact order

def write_headline_to_output(opened_file_pics, opened_file_label = None):
    opened_file_pics.write(HEADLINE)
    for i in range(HEIGHT):
        for j in range(WIDTH):
                opened_file_pics.write(str(i) + ":" + str(j) + "\t")
    opened_file_pics.write("\n")

    if opened_file_label:
        opened_file_label.write(HEADLINE)
        for c in classes:
            opened_file_label.write(c + "\t")
        opened_file_label.write("\n")
    
def write_headline(opened_file):
    opened_file.write(HEADLINE)
    for i in range(HEIGHT):
        for j in range(WIDTH):
                opened_file.write(str(i) + ":" + str(j) + "\t")
    opened_file.write("\n")




if(sys.argv[1] == "train"):
    fileName_train = "/home/awfulwaffle/Downloads/GTSRB/Final_Training/Images/"
    f_train_x = open(X_TRAIN_FILE, "w")
    f_train_y = open(Y_TRAIN_FILE, "w")
    f_validation = open(VALIDATION_FILE, "w")

    # WRITING THE FIRST LINE WITH THE HEADLINE

    write_headline_to_output(f_train_x, f_train_y)
    write_headline(f_validation) 
    # GOING THROUGH ALL FILES IN THE DIRECTORY AND WRITING THEM TO FILE

    class_index = 0  
    index = 1  # index/ID of the current image being written
    index_validation = 1
    files_index = 0  # Index in an images directory, used to calculate how many images I have traversed
    for subdir, dirs, files in os.walk(fileName_train):
        if subdir == fileName_train:
            continue
        if class_index >= MAX_CLASSES:
            break
        validation_ready = True  # setting this variable means that it will write to the VALIDATION_FILE
        for file in files:
            if files_index == MAX_IMAGES:
                break
            if index_validation > (class_index + 1)* MAX_IMAGES / 10:
                validation_ready = False
            
            filename = os.path.join(subdir, file)
            im = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            im = cv2.resize(im, (WIDTH, HEIGHT))
            im = np.reshape(im, WIDTH * HEIGHT )
            indexClass = str(index) + ":" + str.split(subdir,"\/")[-1][-2:] + "\t"  # "index:className\t" 
            index += 1
            f_train_x.write(indexClass)
            f_train_y.write(indexClass)
            
            if validation_ready:
                indexClass = str(index_validation) + ":" + str.split(subdir,"\/")[-1][-2:] + "\t"  # "index:className\t" 
                index_validation += 1
                f_validation.write(indexClass)

            for pixel in im:
                # f_train_x.write(str(pixel/255) + "\t")
                f_train_x.write(str(f'{pixel/255.0:.9f}') + "\t")
                if validation_ready:
                    f_validation.write(str(pixel/255) + "\t")

            for c in classes:  # write to labels file
                lastClass = str.split(subdir,"\/")[-1][-2:]  # last 2 digits from subdir, which represents the class. Ex: "04"
                if lastClass == c:
                    f_train_y.write("1\t")
                else:
                    f_train_y.write("0\t")
            files_index += 1

            f_train_x.write("\n")
            f_train_y.write("\n")

            if validation_ready:
                f_validation.write("\n")

            # Rename the file(if it is not already renamed) to make it clear that it was used for testing
            if file.split(".")[-1] != "test":
                os.rename(filename, filename + ".test")

        class_index += 1
        files_index = 0
    f_train_x.close()
    print("Train file(s) written to ", X_TRAIN_FILE, Y_TRAIN_FILE)
    print("Validation file written to ", VALIDATION_FILE)

elif sys.argv[1] == "test":
    # Requires train to be run at least one time
    # fileName_test = "/home/awfulwaffle/Downloads/GTSRB/Final_Training/Images"  # the directory whose images I'm writing to the .kan file
    fileName_test = "/home/awfulwaffle/piphotos"
    f_test = open(TEST_FILE, "w")
    print("Reading from ", fileName_test, "...")

    write_headline_to_output(f_test)

    index = 1
    files_index = 0
    class_index = 0
    for subdir, dirs, files in os.walk(fileName_test):
        # if subdir == fileName_test:
        #     continue
        for file in files:
            if class_index >= MAX_CLASSES:
                break
            if file.split(".")[-1] == "test":  # if the file has been used for training, skip it
                continue
            if files_index == MAX_IMAGES_TEST:
                break
            filename = os.path.join(subdir, file)
            im = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            im = cv2.resize(im, (WIDTH, HEIGHT))
            im = np.reshape(im, WIDTH * HEIGHT)
            indexClass = str(index) + ":" + str.split(subdir,"\/")[-1][-2:] + "\t"  # "index:className\t" 
            index += 1
            f_test.write(indexClass) 
            for pixel in im:
                f_test.write(str(f'{pixel/255.0:.9f}') + "\t")
                # f_test.write(str(pixel/255) + "\t")
            files_index += 1
            f_test.write("\n")
        class_index += 1
        files_index = 0
    f_test.close()
    print("Test file written to ", TEST_FILE)
else:
    print("Script should be run as: ", sys.argv[0], " ", "train/test.")