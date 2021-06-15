import tensorflow as tf
import cv2
import numpy as np

WIDTH = 320
HEIGHT = 320

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

# Load TFLite model and allocate tensors.
# interpreter = tf.lite.Interpreter(model_path="/home/awfulwaffle/repos/TrafficSignClassifier/tflite/lite-model_ssd_mobilenet_v1_1_metadata_2.tflite")
# interpreter = tf.lite.Interpreter(model_path="models/centernet_512x512.tflite")  # centernet_512x512 works correctly
interpreter = tf.lite.Interpreter(
    model_path="models/exported_ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8_v2.tflite")  # centernet_512x512 works correctly

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
image = cv2.imread("F:/repos/TensorFlow/workspace/training_demo/res/images/train/00001.jpg")
image = cv2.resize(image, (WIDTH, HEIGHT))
input_data = np.array(np.expand_dims(image, axis=0), dtype=np.uint8)
interpreter.set_tensor(input_details[0]['index'], input_data)


interpreter.invoke()

# The function `get_tensor()` returns a copy of the tensor data.
# Use `tensor()` in order to get a pointer to the tensor.
output_boxes = interpreter.get_tensor(output_details[0]["index"])
output_classes = interpreter.get_tensor(output_details[1]["index"])
output_scores = interpreter.get_tensor(output_details[2]["index"])
output_num = interpreter.get_tensor(output_details[3]["index"])
o_4 = interpreter.get_tensor(output_details[4]["index"])
o_5 = interpreter.get_tensor(output_details[5]["index"])
o_6 = interpreter.get_tensor(output_details[6]["index"])

# output_data = interpreter.get_output_details()[2]["index"]
# print(interpreter.get_tensor_details())
print("Detection anchor indices: ", output_boxes)
print("Boxes: ", output_classes)
print("Classes: ", output_scores)
print("Multiclass scores: ", output_num)
print("Scores: ", o_4)
print("Num detections: ", o_5)
print("Raw boxes: ", o_6)

idx = 0
for box in output_classes[0]:
    # print(box[1])
    # I am not sure if the multiplication with HEIGHT and WIDTH are correct or if they should be inversed

    # Order should be the one from here https://tfhub.dev/tensorflow/efficientdet/d3/1
    ymin = round(box[0] * HEIGHT)
    xmin = round(box[1] * WIDTH)
    ymax = round(box[2] * HEIGHT)
    xmax = round(box[3] * WIDTH)
    print(ymin, xmin, ymax, xmax)
    image = cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255, 0, 0))  # box is ymin, xmin, ymax, xmax
    idx += 1
    if idx == 10:
        break
    # https://stackoverflow.com/questions/48915003/get-the-bounding-box-coordinates-in-the-tensorflow-object-detection-api-tutorial
cv2.imshow("img", image)
cv2.waitKey(0)
