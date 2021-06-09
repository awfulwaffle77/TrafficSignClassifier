import cv2 

# Exports the flower photo in a format acceptable for the neural network.
filename = "/home/awfulwaffle/repos/TrafficSignClassifier/tflite/flower_photos/sunflowers/6953297_8576bf4ea3.jpg"

img = cv2.imread(filename)
img = cv2.resize(img, (224,224))
img = cv2.normalize(img, img, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

open("flower_sunflower","wb").write(img)