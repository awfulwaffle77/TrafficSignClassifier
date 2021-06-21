#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <tensorflow/lite/c/c_api.h>

struct filedata
{
  void *data;
  size_t size;
};

// Get information from RAW Image or .tflite model, as both are float32 in range [0,1]
struct filedata getData(char *filename)
{
  int idx = 0;

  FILE *fin = fopen(filename, "rb");

  fseek(fin, 0, SEEK_END);
  int sz = ftell(fin);
  fseek(fin, 0, SEEK_SET);

  float *data = (float *)malloc(sizeof(float) * sz);
  float f;

  for (int i = 0; i < sz / 4; i++)
  { // size is number of floats * 4(floats size)
    fread(&f, 4, 1, fin);
    data[idx++] = f;
  }

  struct filedata ret;
  ret.data = data;
  ret.size = sz;

  return ret;
}

int main()
{

  // TfLiteModel *model = TfLiteModelCreateFromFile("models/centernet_512x512.tflite");
  struct filedata m = getData("models/yolov5_working.tflite");
  TfLiteModel *model = TfLiteModelCreate(m.data, m.size);
  TfLiteInterpreter *interpreter = TfLiteInterpreterCreate(model, NULL);

  // Please, for the love of God, throw some exceptions when reading files
  struct filedata i = getData("images_to_test/yolo_working_480"); // here there can be any flower images, resized to 224,224 and normalized in [0,1]
  TfLiteInterpreterAllocateTensors(interpreter);
  TfLiteTensor *input_tensor = TfLiteInterpreterGetInputTensor(interpreter, 0);
  TfLiteTensorCopyFromBuffer(input_tensor, i.data,
                             i.size); // size is already times sizeof(float)

  TfLiteInterpreterInvoke(interpreter);

  // struct filedata o;
  // o.data = (float *)malloc(sizeof(float) * 1);
  // o.size = 10; // seems like it is VERY important to have the exact number of predictions

  // // it seems that here we can specify the tensor index from the output dictionary
  // const TfLiteTensor *output_tensor =
  //     TfLiteInterpreterGetOutputTensor(interpreter, 0);
  // TfLiteTensorCopyToBuffer(output_tensor, o.data,
  //                          o.size * sizeof(float));
  int tensor_count = TfLiteInterpreterGetOutputTensorCount(interpreter);
  printf("Tensor count: %d\n", tensor_count);

  // as the documentation shows, on the current model(centernet 512x512), the 4th output tensor is number of occurences
  // struct filedata o_num_detections;
  // o_num_detections.data = (float *)malloc(sizeof(float) * 1);
  // o_num_detections.size = 1;
  // const TfLiteTensor *output_tensor_num_detections =
  //     TfLiteInterpreterGetOutputTensor(interpreter, tensor_count - 1);

  // TfLiteTensorCopyToBuffer(output_tensor_num_detections, o_num_detections.data,
  //                          o_num_detections.size * sizeof(float));

  // float number_of_detections;
  // memcpy(&number_of_detections, o_num_detections.data, 4);
  // printf("Number of detections: %f ", number_of_detections);
  // fflush(stdout);

  // For YOLOv5 model
  //
  int number_of_detections = 14175;
  struct filedata o_boxes;

  float **box_coords = malloc(sizeof(float *) * number_of_detections);

  for (int i = 0; i < number_of_detections; i++)
  {
    box_coords[i] = calloc((9 + 1), sizeof(float)); // box has 9 coordinates, added 1 to be sure
  }

  o_boxes.data = (void *)box_coords;
  o_boxes.size = (number_of_detections * 9);

  const TfLiteTensor *output_tensor_boxes =
      TfLiteInterpreterGetOutputTensor(interpreter, 0);
  TfLiteTensorCopyToBuffer(output_tensor_boxes, o_boxes.data,
                           o_boxes.size * sizeof(float));

  box_coords = (float **)&o_boxes.data;  // not entirely sure why we need & there

  for (int i = 0; i < number_of_detections; i++)
  {
    for (int j = 0; j < 9; j++)
    {
      printf("%f ", box_coords[0][j + i * 9]);  // we know we have 9 coordinates, and every line is 9 floats away
      fflush(stdout);
    }
    printf("\n");
  }

  return 0;
}
