import tensorflow as tf 

savepath = "models/centernet_512x512"
converter = tf.lite.TFLiteConverter.from_saved_model(savepath)
converter.target_spec.supported_ops = [
  tf.lite.OpsSet.TFLITE_BUILTINS, # enable TensorFlow Lite ops.
  tf.lite.OpsSet.SELECT_TF_OPS # enable TensorFlow ops.
]

# converter = tf.compat.v1.lite.TFLiteConverter.from_saved_model(savepath)
tflite_model = converter.convert()
open("models/centernet_512x512.tflite", "wb").write(tflite_model)
# open("custom_model.tflite", "wb").write(tflite_model)