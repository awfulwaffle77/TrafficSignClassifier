Please refer to this [reddit
post](https://www.reddit.com/r/linuxquestions/comments/mw0a3f/need_help_with_linking_c_libraries/)
that I have made for steps of getting it to work.

I got it running: `gcc -o test -I/usr/local/include -L/usr/local/lib
testModel.c -ltensorflowlite_c`

I have used a model that classifies flowers from
[here](https://www.tensorflow.org/hub/tutorials/tf2_image_retraining)
and have successfully had it load a model from memory and predict
classes in file `testModel.c`.

`exportPhoto.py` exports photo as raw format after **resizing and normalizing**. Very important.

Please check [this stackoverflow
question](https://stackoverflow.com/questions/65650859/converting-pretrained-model-from-tfhub-to-tflite)

I have found [here](https://www.programmersought.com/article/284366009/)
how the output of the model looks like
With the command `python3 saved_model_cli.py show --dir
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
