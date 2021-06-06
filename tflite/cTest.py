import tensorflow as tf
import tensorflow_hub as hub

detector = hub.Module("https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1")
detector_output = detector(image_tensor, as_dict=True)
class_names = detector_output["detection_class_names"]


# model = hub.KerasLayer("https://tfhub.dev/google/nnlm-en-dim128/2")
# embeddings = model(["The rain in Spain.", "falls",
#                     "mainly", "In the plain!"])

# pretrained_model = tf.keras.applications.MobileNet()

# savepath = "./test_model.mdl"
# tf.saved_model.save(pretrained_model, savepath)
# converter = tf.lite.TFLiteConverter.from_saved_model(savepath)
# tflite_model = converter.convert()
# open("converted_model.tflite", "wb").write(tflite_model)
# # print(embeddings.shape)  #(4,128)