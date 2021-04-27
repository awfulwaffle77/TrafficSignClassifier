import cv2 
import numpy as np

HEIGHT = 120
WIDTH = 160

filename = "/home/awfulwaffle/newpic.jpg"
filename_grey = "/home/awfulwaffle/newpic_grey.jpg"


im = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
img = cv2.imread(filename_grey, cv2.IMREAD_GRAYSCALE)
im = cv2.resize(im, (WIDTH, HEIGHT))
img = cv2.resize(img, (WIDTH, HEIGHT))
im = np.reshape(im, WIDTH * HEIGHT )
img = np.reshape(img, WIDTH * HEIGHT )

for pixel in img:
    print(pixel)