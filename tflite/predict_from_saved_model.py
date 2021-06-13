import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np

image = cv2.imread("/home/awfulwaffle/Downloads/FullIJCNN2013/FullIJCNN2013/00814.ppm")
image = cv2.resize(image, (512,512))
image_extended = np.array(np.expand_dims(image, axis=0), dtype=np.uint8)

detector = hub.load("https://tfhub.dev/tensorflow/centernet/resnet50v1_fpn_512x512/1")

# detector = tf.saved_model.load("models/ssdmobilenet_github/ssdmobilenet_github/saved_model/")
# detector.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
# detector_output = detector.predict(image_extended)

class_ids = detector_output["detection_classes"]
print(detector_output["num_detections"])
print(detector_output["detection_boxes"])
print(detector_output["detection_classes"])
print(detector_output["detection_scores"])

idx = 0
for box in detector_output["detection_boxes"][0]: 
    box = box.numpy().tolist()  # convert Tf.tensor to list
    print(box)
    ymin = round(box[1] * 512)
    xmin = round(box[0] * 512)
    ymax = round(box[3] * 512)
    xmax = round(box[2] * 512)
    image = cv2.rectangle(image, (ymin, xmin), (ymax, xmax), (255,0,0))  # box is ymin, xmin, ymax, xmax
    idx += 1
    if idx == 5:
        break
    # https://stackoverflow.com/questions/48915003/get-the-bounding-box-coordinates-in-the-tensorflow-object-detection-api-tutorial
cv2.imshow("img", image)
cv2.waitKey(0)

