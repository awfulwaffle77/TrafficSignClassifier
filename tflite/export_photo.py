import cv2 

# Exports the flower photo in a format acceptable for the neural network.
filename = "/home/awfulwaffle/Downloads/FullIJCNN2013/FullIJCNN2013/00814.ppm"

img = cv2.imread(filename)
img = cv2.resize(img, (512,512))
# img = cv2.normalize(img, img, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

open("images_to_test/centernet512x512","wb").write(img)