# Script to create PASCAL_VOC type annotations and .jpg images from .ppm
# ! Must be run from PASCAL_VOC folder


# Latest update: I have written this exactly to the folder from where I am training
import os
import copy
import cv2
import shutil
from pascal_voc_writer import Writer

__TEST = False
NRS_HEIGHT = 800  # non-resized height
NRS_WIDTH = 1360  # non-resized width
CV2_RESIZE_WIDTH = 320
CV2_RESIZE_HEIGHT = 320

# input_folder = "/home/awfulwaffle/Downloads/FullIJCNN2013/FullIJCNN2013/"
input_folder = "F:/repos/TensorFlow/workspace/training_demo/res/images/test"
labels_dir = "F:/repos/TensorFlow/workspace/training_demo/res/images/test"
images_dir = "F:/repos/TensorFlow/workspace/training_demo/res/images/test"
# ground truth file
gt_file = "F:/repos/FullIJCNN2013/gt.txt"

with open(gt_file) as gt:
    gt_content = gt.readlines()

_extension = "jpg"
train_percent = 70
val_percent = 100 - train_percent

#  content is the content of gt.txt


def create_ground_truth_dict(filename):
    f = open(filename, "r")
    _dlist = []
    _list = []
    _dict = {}
    for lines in f.readlines():
        filename, xMin, yMin, xMax, yMax, _class = lines.split(";")
        # Change the points relative to the dimensions of the image
        filename = filename.split(".")[0] + ".jpg"

        # https://stackoverflow.com/questions/45724955/find-new-coordinates-of-a-point-after-image-resize
        Rx = CV2_RESIZE_WIDTH/NRS_WIDTH
        Ry = CV2_RESIZE_HEIGHT/NRS_HEIGHT

        xMin = round(Rx * int(xMin))
        yMin = round(Ry * int(yMin))
        xMax = round(Rx * int(xMax))
        yMax = round(Ry * int(yMax))

        # To verify if bounding boxes are displayed correctly. UPDATE: it is correct
        if __TEST:
            filename_to_open = os.path.join(
                input_folder, filename.split(".")[0] + "." + _extension)
            img = cv2.imread(filename_to_open)
            img = cv2.resize(img, (CV2_RESIZE_WIDTH, CV2_RESIZE_HEIGHT))
            img = cv2.rectangle(img, (xMin, yMin), (xMax, yMax), (255, 0, 0))
            cv2.imshow("img", img)
            cv2.waitKey(0)

        _class = _class[0:len(_class) - 1]  # _id came splitted with a \n
        _list.append(_class)

        _list.append(xMin)
        _list.append(yMin)
        _list.append(xMax)
        _list.append(yMax)

        _dlist.append(_list)

        if filename in _dict:
            cplist = _dict[filename]
            cplist.append(copy.deepcopy(_list))
            _dict[filename] = cplist
        else:
            _dict[filename] = copy.deepcopy(_dlist)
        _list.clear()
        _dlist.clear()

    return _dict


def clear_dir(dirname):
    for root, dirs, files in os.walk(dirname):
        for file in files:
            os.remove(os.path.join(root, file))


gt_dict = create_ground_truth_dict(gt_file)

# Write the file labels
# first, remove all the files there, because content is appended

# clear_dir(labels_dir)
print(os.getcwd())
for key in gt_dict:
    filename = os.path.join(labels_dir, key.split(".")[0])
    filename += ".xml"
    _list = gt_dict[key]
    toWrite = ""
    writer = Writer(os.path.join(images_dir, key),
                    CV2_RESIZE_WIDTH, CV2_RESIZE_HEIGHT)
    for i in range(len(_list)):
        _sublist = _list[i]
        # toWrite += _sublist[0] + " " + str(_sublist[1]) + " " + str(_sublist[2]) + " " + str(_sublist[3]) + " " + str(_sublist[4])
        writer.addObject(_sublist[0], _sublist[1],
                         _sublist[2], _sublist[3], _sublist[4])
    writer.save(filename)

exit(0)
# =================== ENDING HERE ONLY FOR PASCAL VOC LABELS ========================================
# all images have extension _extenstion, so we get their names
all_files = os.listdir(input_folder)
ext_files = []  # extension files

for file in all_files:
    x = file.split(".")[-1]
    if file.split(".")[-1] == _extension:
        ext_files.append(file)

ext_files.sort()
clear_dir(images_dir)
# print(ext_files)
print("Copying files..")

for ext_file in ext_files:

    full_input_path = os.path.join(input_folder, ext_file)
    save_path = os.path.join(images_dir, ext_file)

    if os.path.isfile(save_path):  # if it exists in images dir
        continue

    shutil.copyfile(full_input_path, save_path)
    img = cv2.imread(save_path, cv2.IMREAD_COLOR)
    dim = (CV2_RESIZE_WIDTH, CV2_RESIZE_HEIGHT)
    resized = cv2.resize(img, dim)
    cv2.imwrite(save_path, resized)

print("Done")
