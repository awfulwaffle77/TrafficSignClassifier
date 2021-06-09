import cv2 

# Exports the flower photo in a format acceptable for the neural network.
filename = "/home/awfulwaffle/repos/TrafficSignClassifier/tflite/apple.jpeg"

img = cv2.imread(filename)
img = cv2.resize(img, (300,300))
# img = cv2.normalize(img, img, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

open("apple","wb").write(img)