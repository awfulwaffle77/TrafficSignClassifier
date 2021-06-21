import tensorflow as tf
import cv2
import numpy as np
import time

WIDTH = 480
HEIGHT = 480

_BLUE = (255,0,0)
_GREEN = (0,255,0)
_RED = (0, 0, 255)
_PURPLE = (255, 0, 255)

_COLORS = [_RED, _GREEN, _BLUE, _PURPLE]

# interpreter = tf.saved_model.load("saved_model_ssdmobilenet320x320")
# interpreter = tf.lite.Interpreter("custom_ssdmobile.tflite")
# print(interpreter.get_input_details())
# print(interpreter.get_output_details())

# itp = tf.saved_model.load("flowers_model.mdl")
# # image = x[1, :, :, :]
# itp.compile()
# image = open("flower_tulips","rb").read()
# scores = itp.predict(itp.predict(image))
# predicted_index = np.argmax(image)
# print(predicted_index)

def classFilter(classdata):
    classes = []  # create a list
    for i in range(classdata.shape[0]):  # loop through all predictions
        classes.append(classdata[i].argmax())  # get the best classification location
    return classes  # return classes (int)


def YOLOdetect(output_data):  # input = interpreter, output is boxes(xyxy), classes, scores
    output_data = output_data[0]  # x(1, 25200, 7) to x(25200, 7)
    boxes = np.squeeze(output_data[..., :4])  # boxes  [25200, 4]
    scores = np.squeeze(output_data[..., 4:5])  # confidences  [25200, 1]
    classes = classFilter(output_data[..., 5:])  # get classes
    # Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    x, y, w, h = boxes[..., 0], boxes[..., 1], boxes[..., 2], boxes[..., 3]  # xywh
    xyxy = [x - w / 2, y - h / 2, x + w / 2, y + h / 2]  # xywh to xyxy   [4, 25200]

    return xyxy, classes, scores  # output is boxes(x,y,x,y), classes(int), scores(float) [predictions length]


# Load TFLite model and allocate tensors.
# interpreter = tf.lite.Interpreter(model_path="/home/awfulwaffle/repos/TrafficSignClassifier/tflite/lite-model_ssd_mobilenet_v1_1_metadata_2.tflite")
# interpreter = tf.lite.Interpreter(model_path="models/centernet_512x512.tflite")  # centernet_512x512 works correctly
interpreter = tf.lite.Interpreter(
    # model_path="models/exported_resnet640.tflite")  # centernet_512x512 works correctly
    model_path="models/yolov5_working.tflite")  # centernet_512x512 works correctly

interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
print("======================================================")
print(input_details)
print("======================================================")
# print(output_details)
for detail in output_details:
    print(detail)
    print(" ")

# Test model on random input data.
input_shape = input_details[0]['shape']
# input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)
# input_data = np.array(cv2.imread("/home/awfulwaffle/repos/TrafficSignClassifier/tflite/flower_tulips"), dtype=np.float32)
image = cv2.imread("/home/awfulwaffle/repos/TrafficSignClassifier/ImageManipulation/images-yolov4/test/00803.jpg")
image = cv2.resize(image, (WIDTH, HEIGHT))
image = cv2.normalize(image, image, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
input_data = np.array(np.expand_dims(image, axis=0), dtype=np.float32)
interpreter.set_tensor(input_details[0]['index'], input_data)

t0 = time.time()
interpreter.invoke()
t1 = time.time()

print("Intereference in: ", t1 - t0)

# The function `get_tensor()` returns a copy of the tensor data.
# Use `tensor()` in order to get a pointer to the tensor.
output_data = interpreter.get_tensor(output_details[0]["index"])

print("Output: ", output_data)
# xyxy, classes, scores = YOLOdetect(output_data)

# https://stackoverflow.com/questions/65824714/process-output-data-from-yolov5-tflite
# idx = 0
# for i in range(len(scores)):
#     if ((scores[i] > 0.1) and (scores[i] <= 1.0)):
#         H = HEIGHT
#         W = WIDTH
#         xmin = int(max(1, (xyxy[0][i] * W)))
#         ymin = int(max(1, (xyxy[1][i] * H)))
#         xmax = int(min(H, (xyxy[2][i] * W)))
#         ymax = int(min(W, (xyxy[3][i] * H)))
#
#         image = cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)
    # https://stackoverflow.com/questions/48915003/get-the-bounding-box-coordinates-in-the-tensorflow-object-detection-api-tutorial
print("Shape: ", output_data[0].shape)
for box in output_data[0]:
    print(box)
    cx = (box[0])
    cy = (box[1])
    w = (box[2])
    h = (box[3])
    
    ymin = int((cy - h/2) * HEIGHT)
    xmin = int((cx - w/2) * WIDTH)
    ymax = int((cy + h/2) * HEIGHT)
    xmax = int((cx + w/2) * WIDTH)


    scores = box[5:9]
    color = _COLORS[np.argmax(scores)]
    if box[4] < 0.9:
        continue
    image = cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color)  # box is ymin, xmin, ymax, xmax

    print(ymin, xmin, ymax, xmax)
cv2.imshow("img", image)
cv2.waitKey(0)

