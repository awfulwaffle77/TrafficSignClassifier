import tensorflow as tf 

savepath = "F:/repos/TensorFlow/workspace/training_demo/exported-models/exported_mobilenet320x320_v2/saved_model"

model = tf.saved_model.load(savepath)
concrete_func = model.signatures[
  tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY]
concrete_func.inputs[0].set_shape([None, 320, 320, 3])
converter = tf.lite.TFLiteConverter.from_concrete_functions([concrete_func])

converter.target_spec.supported_ops = [
  tf.lite.OpsSet.TFLITE_BUILTINS, # enable TensorFlow Lite ops.
  tf.lite.OpsSet.SELECT_TF_OPS # enable TensorFlow ops.
]

tflite_model = converter.convert()
open("models/exported_ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8_v2.tflite", "wb").write(tflite_model)
