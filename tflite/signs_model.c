#include <stdio.h>
#include <string.h>
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
  struct filedata m = getData("models/centernet_512x512.tflite");
  TfLiteModel *model = TfLiteModelCreate(m.data, m.size);
  TfLiteInterpreter *interpreter = TfLiteInterpreterCreate(model, NULL);

  // Please, for the love of God, throw some exceptions when reading files
  struct filedata i = getData("images_to_test/centernet512x512"); // here there can be any flower images, resized to 224,224 and normalized in [0,1]
  TfLiteInterpreterAllocateTensors(interpreter);
  TfLiteTensor *input_tensor = TfLiteInterpreterGetInputTensor(interpreter, 0);
  TfLiteTensorCopyFromBuffer(input_tensor, i.data,
                             i.size); // size is already times sizeof(float)

  TfLiteInterpreterInvoke(interpreter);

  struct filedata o;
  o.data = (float *)malloc(sizeof(float) * 1);
  o.size = 10; // seems like it is VERY important to have the exact number of predictions

  // it seems that here we can specify the tensor index from the output dictionary
  const TfLiteTensor *output_tensor =
      TfLiteInterpreterGetOutputTensor(interpreter, 2);
  TfLiteTensorCopyToBuffer(output_tensor, o.data,
                           o.size * sizeof(float));
  int tensor_count = TfLiteInterpreterGetOutputTensorCount(interpreter);
  printf("Tensor count: %d\n", tensor_count);

  // as the documentation shows, on the current model(centernet 512x512), the 4th output tensor is number of occurences
  struct filedata o_num_detections;
  o_num_detections.data = (float *)malloc(sizeof(float) * 1);
  o_num_detections.size = 1;
  const TfLiteTensor *output_tensor_num_detections =
      TfLiteInterpreterGetOutputTensor(interpreter, tensor_count - 1);

  TfLiteTensorCopyToBuffer(output_tensor_num_detections, o_num_detections.data,
                           o_num_detections.size * sizeof(float));

  float number_of_detections;
  memcpy(&number_of_detections, o_num_detections.data, 4);
  printf("Number of detections: %f ", number_of_detections);
  fflush(stdout);

  struct filedata o_boxes;
  // o_boxes.data = (float**)malloc(sizeof(float*) * (int)number_of_detections);
  float ***box_coords = (float ***)malloc(sizeof(float **) * 1);
  o_boxes.size = 1 * 100 * 4;

  box_coords[0] = (float **)malloc(sizeof(float *) * 100);
  for (int i = 0; i < 100; i++)
  {
    box_coords[0][i] = (float *)calloc(sizeof(float), 4); // box has 4 coordinates
  }
  o_boxes.data = box_coords;

  const TfLiteTensor *output_tensor_boxes =
      TfLiteInterpreterGetOutputTensor(interpreter, 0);
  TfLiteTensorCopyToBuffer(output_tensor_boxes, o_boxes.data,
                           o_boxes.size * sizeof(float));

  float coords;
  box_coords = (float ***)&o_boxes.data;
  for (int i = 0; i < o_boxes.size; i++)
  {
    // box_coords[0][0][0] is some kind of value ??
    memcpy(&coords, box_coords[0][i], 4); // float size * 4 coords
    for (int j = 0; j < 4; j++)
    {
      printf("%f ", coords);
    }

    if (i == 5)
    {
      break;
    }
  }

  return 0;
}
