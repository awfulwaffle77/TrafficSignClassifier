import tensorflow as tf 

savepath = "/home/awfulwaffle/repos/TrafficSignClassifier/ImageManipulation/yolov5/models/customyolov5"
# converter = tf.lite.TFLiteConverter.from_saved_model(savepath)
converter = tf.compat.v1.lite.TFLiteConverter.from_saved_model(savepath)
tflite_model = converter.convert()
open("customyolov5.tflite", "wb").write(tflite_model)