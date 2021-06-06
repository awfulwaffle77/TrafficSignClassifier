import tensorflow as tf
import cv2
import numpy as np


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
interpreter = tf.lite.Interpreter(model_path="flowers_model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Test model on random input data.
input_shape = input_details[0]['shape']
# input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)
# input_data = np.array(cv2.imread("/home/awfulwaffle/repos/TrafficSignClassifier/tflite/flower_tulips"), dtype=np.float32)
image = cv2.imread("/home/awfulwaffle/repos/TrafficSignClassifier/tflite/daisy.png")
image = cv2.resize(image, (224,224))
input_data = np.array(np.expand_dims(image, axis=0), dtype=np.float32)
interpreter.set_tensor(input_details[0]['index'], input_data)

interpreter.invoke()

# The function `get_tensor()` returns a copy of the tensor data.
# Use `tensor()` in order to get a pointer to the tensor.
output_data = interpreter.get_tensor(output_details[0]['index'])
print(output_data)