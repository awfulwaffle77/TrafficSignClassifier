Bazel libtensorflowlite_c.so has been made with the command
`bazel build -c opt //tensorflow/lite/c:tensorflowlite_c` from directory
tensorflow/tensorflow/lite.

Please refer to this [reddit
post](https://www.reddit.com/r/linuxquestions/comments/mw0a3f/need_help_with_linking_c_libraries/)
that I have made for steps of getting it to work.

I got it running: `gcc -o test -I/usr/local/include -L/usr/local/lib
testModel.c -ltensorflowlite_c`

## Folders

- `lib`: stores libtensorflow shard object libraries compiled for x86_64 on
  Ubuntu20

## Limitations

NXP MIMXRT1020-EVK has only 256Mbit of SDRAM, which means 8MB.

I have to create a C binary that is at max 8 MB. Due to this 
limitation, I need to pick a smaller model or to quantize this one.
On the [tensorflow lite ops_select
page](https://www.tensorflow.org/lite/guide/ops_select#c),
under perfomance, there is shown how much of a difference in size there
is between only built-in ops and built-in + TF ops. This must
also be taken into consideration.

## How to use models in TFLite C Library (please reformat)

You can see the output of a model in Python as such
```
interpreter = tf.lite.Interpreter(model_path="path/to/model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
```
printing `output_details` shows the output tensors. There, you can
see the property `dtype': <class 'numpy.float32'>`. This dictates
the data type you need to use in C. The property `shape`(ex. `'shape':
array([ 1, 10,  4], dtype=int32)` dictates how many variables you need
to have in your array. For example, if I have this np.float32 and the
shape is [1, 10], the code in C looks like this: 
```
struct filedata o;
  o.data = (float *)malloc(sizeof(float) * 1); 
  o.size = 10;                                

  // it seems that here we can specify the tensor index from the output dictionary
  const TfLiteTensor *output_tensor =
      TfLiteInterpreterGetOutputTensor(interpreter, 2);
  TfLiteTensorCopyToBuffer(output_tensor, o.data,
                           o.size * sizeof(float));
  int x = TfLiteInterpreterGetOutputTensorCount(interpreter);

  float _f;
  for (int i = 0; i < 10; i++)
  {
    memcpy(&_f, o.data + i * 4, 4);
    printf("%f ", _f);
    fflush(stdout);
  }
```


## Models used

- [lite-model_ssd_mobilenet_v1_1_metadata_2.tflite](https://tfhub.dev/tensorflow/lite-model/ssd_mobilenet_v1/1/metadata/2); 
this always outputs 10 classes, 10 scores etc. as stated on [this
page](https://www.tensorflow.org/lite/examples/object_detection/overview#output_signature),
note #2

I have used a model that classifies flowers from
[here](https://www.tensorflow.org/hub/tutorials/tf2_image_retraining)
and have successfully had it load a model from memory and predict
classes in file `testModel.c`.

`exportPhoto.py` exports photo as raw format after *resizing and normalizing*. Very important.

`TfLiteInterpreterGetOutputTensor(interpreter, 0);` might choose which part of the dictionary is reffered.

## Flex Delegates build for TFLite C lib

The model used needed Flex Delegates compiled in the library. This was
made possible with
[this repo](https://github.com/PINTO0309/TensorflowLite-flexdelegate),
because I did not understand how to add dependencies from the docs of
the [official
guide](https://www.tensorflow.org/lite/guide/ops_select#c). At the time
of writing, it is still building. Might want to check this 
[stackoverflow
answer](https://stackoverflow.com/questions/58623937/how-to-build-tensorflow-lite-with-select-tensorflow-ops-for-x86-64-systems)
too.

I have added the dep `//tensorflow/lite/delegates/flex:delegate",` in
the `tensorflow/tensorflow/lite/c/BUILD` file and then compiled with
`sudo bazel build -c opt --config=monolithic
--define=tflite_convert_with_select_tf_ops=true
--define=with_select_tf_ops=true
//tensorflow/lite/c:libtensorflowlite_c.so`. The resulting .so
is found in `tensorflow/bazel-bin..`

*Needs to be tested.*

(?)Please check [this stackoverflow
question](https://stackoverflow.com/questions/65650859/converting-pretrained-model-from-tfhub-to-tflite)

You can use 
```
interpreter = tf.lite.Interpreter(model_path="path/to/model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
```
but this will not show their names exactly, only something like
`TFLite_Detection_PostProcess`. To see a more detailed output, I have found [here](https://www.programmersought.com/article/284366009/)
how to get it.

From directory `~/repos/tensorflow/tensorflow/python/tools`, with the command `python3 saved_model_cli.py show --dir
/home/awfulwaffle/repos/TrafficSignClassifier/tflite/saved_model_ssdmobilenet320x320
--all` for ssdmobilenetv2_320x320, the output looks like this: 
```
ignature_def['serving_default']:
  The given SavedModel SignatureDef contains the following input(s):
    inputs['input_tensor'] tensor_info:
        dtype: DT_UINT8
        shape: (1, -1, -1, 3)
        name: serving_default_input_tensor:0
  The given SavedModel SignatureDef contains the following output(s):
    outputs['detection_anchor_indices'] tensor_info:
        dtype: DT_FLOAT
        shape: (1, 100)
        name: StatefulPartitionedCall:0
    outputs['detection_boxes'] tensor_info:
        dtype: DT_FLOAT
        shape: (1, 100, 4)
        name: StatefulPartitionedCall:1
    outputs['detection_classes'] tensor_info:
        dtype: DT_FLOAT
        shape: (1, 100)
        name: StatefulPartitionedCall:2
    outputs['detection_multiclass_scores'] tensor_info:
        dtype: DT_FLOAT
        shape: (1, 100, 44)
        name: StatefulPartitionedCall:3
    outputs['detection_scores'] tensor_info:
        dtype: DT_FLOAT
        shape: (1, 100)
        name: StatefulPartitionedCall:4
    outputs['num_detections'] tensor_info:
        dtype: DT_FLOAT
        shape: (1)
        name: StatefulPartitionedCall:5
    outputs['raw_detection_boxes'] tensor_info:
        dtype: DT_FLOAT
        shape: (1, 12804, 4)
        name: StatefulPartitionedCall:6
    outputs['raw_detection_scores'] tensor_info:
        dtype: DT_FLOAT
        shape: (1, 12804, 44)
        name: StatefulPartitionedCall:7
  Method name is: tensorflow/serving/predict

Defined Functions:
  Function Name: '__call__'
    Option #1
      Callable with:
        Argument #1
          input_tensor: TensorSpec(shape=(1, None, None, 3), dtype=tf.uint8, name='input_tensor')
```

The output for the model that classifies 5 types of flowers(and
therefore has 5 classes) is:
```
The given SavedModel SignatureDef contains the following output(s):
    outputs['predictions'] tensor_info:
        dtype: DT_FLOAT
        shape: (-1, 1000)
        name: StatefulPartitionedCall:0
  Method name is: tensorflow/serving/predict
```
