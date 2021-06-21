import cv2 

# Exports the flower photo in a format acceptable for the neural network.
filename = "/home/awfulwaffle/repos/TrafficSignClassifier/ImageManipulation/images-yolov4/test/00803.jpg"

img = cv2.imread(filename)
img = cv2.resize(img, (480,480))
img = cv2.normalize(img, img, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

open("images_to_test/yolo_working_480","wb").write(img)