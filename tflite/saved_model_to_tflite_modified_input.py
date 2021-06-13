import tensorflow as tf 

savepath = "models/centernet_512x512"

model = tf.saved_model.load(savepath)
concrete_func = model.signatures[
  tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY]
concrete_func.inputs[0].set_shape([None, 512, 512, 3])
converter = tf.lite.TFLiteConverter.from_concrete_functions([concrete_func])

converter.target_spec.supported_ops = [
  tf.lite.OpsSet.TFLITE_BUILTINS, # enable TensorFlow Lite ops.
  tf.lite.OpsSet.SELECT_TF_OPS # enable TensorFlow ops.
]

tflite_model = converter.convert()
open("models/centernet_512x512.tflite", "wb").write(tflite_model)
