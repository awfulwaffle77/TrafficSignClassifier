import cv2 

filename = "flower_photos/roses/24781114_bc83aa811e_n.jpg"

img = cv2.imread(filename)

open("flower1","wb").write(img)