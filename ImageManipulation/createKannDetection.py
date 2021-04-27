import os
import sys
import cv2
import numpy as np
import copy

# There may be some issue when creating the detection files
# I am thinking about using the classes and puttin x,y,width,height in y.kan

# V1 -> will try without "truth", only with the x,y,w,h and see if it works.
# also, will try to see if I can use multiple parameters in the same file
HEADLINE = "#no:\t"
HEADLINE_Y = "#no:\tleftCol\ttopRow\trightCol\tbottomRow\n"
HEIGHT = 120
WIDTH = 160
NRS_HEIGHT = 800  # non-resized height
NRS_WIDTH =  1360  # non-resized width
X_TRAIN_FILE = "../kann_test/mnist_test/kann-data/x-detectionv1.knd"
Y_TRAIN_FILE = "../kann_test/mnist_test/kann-data/y-detectionv1.knd"
TEST_FILE = "../kann_test/mnist_test/kann-data/detectionv1-test.knd"
VALIDATION_FILE = "../kann_test/mnist_test/kann-data/detectionv1-validation.knd"  
# the validation dataset will consist of images also used for training(meaning some of the
# images that are in X_TRAIN_FILE are also here)
MAX_IMAGES = 300
MAX_IMAGES_TEST = 200

# classes = ["40", "21", "04"]
# classes_test = ["40", "21", "04"]  # checked with debug and hardcoded the exact order

def write_headline_to_output(opened_file_pics, opened_file_label = None):
    opened_file_pics.write(HEADLINE)
    for i in range(HEIGHT):
        for j in range(WIDTH):
                opened_file_pics.write(str(i) + ":" + str(j) + "\t")
    opened_file_pics.write("\n")

    if opened_file_label:
        opened_file_label.write(HEADLINE_Y)

    
def write_headline(opened_file):
    opened_file.write(HEADLINE)
    for i in range(HEIGHT):
        for j in range(WIDTH):
                opened_file.write(str(i) + ":" + str(j) + "\t")
    opened_file.write("\n")


def create_ground_truth_dict(filename):
    f = open(filename, "r")
    _dlist = []
    _list = []
    _dict = {}
    for lines in f.readlines():
        name, leftCol, topRow, rightCol, bottomRow, _id= lines.split(";")
        # Change the points relative to the dimensions of the image

        Rx = WIDTH/NRS_WIDTH
        Ry = HEIGHT/NRS_HEIGHT

        leftCol = str(int(Rx * int(leftCol)))
        topRow = str(int(Ry * int(topRow)))
        rightCol = str(int(Rx * int(rightCol)))
        bottomRow = str(int(Ry * int(bottomRow)))

        _list.append(leftCol)
        _list.append(topRow)
        _list.append(rightCol)
        _list.append(bottomRow)
        _id = _id[0:len(_id) - 1]  # _id came splitted with a \n
        _list.append(_id)
        _dlist.append(_list)
        if name in _dict:
            cplist = _dict[name]
            cplist.append(copy.deepcopy(_list))
            _dict[name] = cplist
        else:
            _dict[name] = copy.deepcopy(_dlist)
        _list.clear()
        _dlist.clear()

    return _dict


if(sys.argv[1] == "train"):
    fileName_train = "/home/awfulwaffle/Downloads/FullIJCNN2013/FullIJCNN2013"
    fileName_gt = "/home/awfulwaffle/Downloads/FullIJCNN2013/FullIJCNN2013/gt.txt"

    gt_dict = create_ground_truth_dict(fileName_gt)

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
        validation_ready = True  # setting this variable means that it will write to the VALIDATION_FILE
        for file in files:
            x = file.split(".")[1]
            if file.split(".")[1] != "ppm":
                continue
            if files_index == MAX_IMAGES:
                break
            if file not in gt_dict:
                continue
            if index_validation > (class_index + 1)* MAX_IMAGES / 10:  # ??
                validation_ready = False
            
            filename = os.path.join(subdir, file)
            im = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            im = cv2.resize(im, (WIDTH, HEIGHT))
            im = np.reshape(im, WIDTH * HEIGHT )
            indexClass = str(index) + ":" + "\t"  # "index:\t" 
            # index += 1
            f_train_x.write(indexClass)
            # f_train_y.write(indexClass)
            
            if validation_ready:
                indexClass = str(index_validation) + ":" + "\t"  # "index:\t" 
                # index_validation += 1
                f_validation.write(indexClass)

            for pixel in im:
                # f_train_x.write(str(pixel/255) + "\t")
                f_train_x.write(str(f'{pixel/255.0:.9f}') + "\t")
                if validation_ready:
                    f_validation.write(str(pixel/255) + "\t")
            f_train_x.write("\n")

            # Here we write the coordinates to the y file
            roi_list = gt_dict[file]
            for _list in roi_list:
                f_train_y.write(str(index) + ":" + "\t" + _list[0] + "\t" + _list[1] + "\t" +
                _list[2] + "\t" + _list[3] + "\n")
            index += 1
            index_validation += 1
            # f_train_y.write("\n")

            # for c in classes:  # write to labels file
            #     lastClass = str.split(subdir,"\/")[-1][-2:]  # last 2 digits from subdir, which represents the class. Ex: "04"
            #     if lastClass == c:
            #         f_train_y.write("1\t")
            #     else:
            #         f_train_y.write("0\t")

            files_index += 1

            if validation_ready:
                f_validation.write("\n")

            # Rename the file(if it is not already renamed) to make it clear that it was used for training
            # if file.split(".")[-1] != "test":
            #     os.rename(filename, filename + ".test")

        class_index += 1
        # files_index = 0
    f_train_x.close()
    f_train_y.close()
    f_validation.close()
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