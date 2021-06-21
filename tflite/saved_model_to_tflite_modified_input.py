import tensorflow as tf 

savepath = "models/darknet.tf"

model = tf.saved_model.load(savepath)
concrete_func = model.signatures[
  tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY]
print("===================================================")
print(concrete_func.inputs[0])
print(concrete_func.outputs[0])
print("===================================================")
concrete_func.inputs[0].set_shape((None, 640, 640, 3))
# concrete_func.outputs[0].set_shape((None, 5, 8))  # will not work for outputs
print("===================================================")
print(concrete_func.inputs[0])
print(concrete_func.outputs[0])
print("===================================================")
converter = tf.lite.TFLiteConverter.from_concrete_functions([concrete_func])

converter.target_spec.supported_ops = [
  tf.lite.OpsSet.TFLITE_BUILTINS, # enable TensorFlow Lite ops.
  tf.lite.OpsSet.SELECT_TF_OPS # enable TensorFlow ops.
]

tflite_model = converter.convert()
open("models/exported_darknet.tflite", "wb").write(tflite_model)

interpreter = tf.lite.Interpreter(model_content=tflite_model)
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Test the model on random input data.
input_shape = input_details[0]['shape']
output_shape = output_details[0]['shape']
print(input_shape)
print(output_shape)