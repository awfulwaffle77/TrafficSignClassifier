import tensorflow as tf 

savepath = "F:/repos/TensorFlow/workspace/training_demo/exported-models/exported_mobilenet320x320_v2/saved_model"
converter = tf.lite.TFLiteConverter.from_saved_model(savepath)
converter.target_spec.supported_ops = [
  tf.lite.OpsSet.TFLITE_BUILTINS, # enable TensorFlow Lite ops.
  tf.lite.OpsSet.SELECT_TF_OPS # enable TensorFlow ops.
]

# converter = tf.compat.v1.lite.TFLiteConverter.from_saved_model(savepath)
tflite_model = converter.convert()
open("models/exported_ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8_v2.tflite", "wb").write(tflite_model)