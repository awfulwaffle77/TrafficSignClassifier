import tensorflow as tf 

savepath = "models/ssdmobilenet_github/ssdmobilenet_github/saved_model"
converter = tf.lite.TFLiteConverter.from_saved_model(savepath)
converter.target_spec.supported_ops = [
  tf.lite.OpsSet.TFLITE_BUILTINS, # enable TensorFlow Lite ops.
  tf.lite.OpsSet.SELECT_TF_OPS # enable TensorFlow ops.
]

# converter = tf.compat.v1.lite.TFLiteConverter.from_saved_model(savepath)
tflite_model = converter.convert()
open("models/ssdmobilenet_github.tflite", "wb").write(tflite_model)
# open("custom_model.tflite", "wb").write(tflite_model)