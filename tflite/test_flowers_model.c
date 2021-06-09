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
    // fscanf(fin, "%f", &f);
    // data[i++] = f;
    fread(&f, 4, 1, fin);
    data[idx++] = f;
    // fread(&data[idx], 4, 1, fin);  // size is 4 cause we have floats
  }

  struct filedata ret;
  ret.data = data;
  ret.size = sz;

  return ret;
}

int main()
{
  // struct filedata m = getData("flowers_model.tflite");
  TfLiteModel *model = TfLiteModelCreateFromFile("flowers_model.tflite");
  // TfLiteModel* model = TfLiteModelCreate(m.data, m.size);
  // TfLiteModelCreate
  TfLiteInterpreter *interpreter = TfLiteInterpreterCreate(model, NULL);


  // Please, for the love of God, throw some exceptions when reading files
  struct filedata i = getData("flower_sunflower");  // here there can be any flower images, resized to 224,224 and normalized in [0,1]
  TfLiteInterpreterAllocateTensors(interpreter);
  TfLiteTensor *input_tensor = TfLiteInterpreterGetInputTensor(interpreter, 0);
  TfLiteTensorCopyFromBuffer(input_tensor, i.data,
                             i.size); // size is already times sizeof(float)

  TfLiteInterpreterInvoke(interpreter);

  struct filedata o;
  o.data = (float*)malloc(sizeof(float) * 5);  // cause model predicts 5 classes
  o.size = 5;  // seems like it is VERY important to have the exact number of predictions

  // it seems that here we can specify the tensor index from the output dictionary
  const TfLiteTensor *output_tensor =
  TfLiteInterpreterGetOutputTensor(interpreter, 0);  
  TfLiteTensorCopyToBuffer(output_tensor, o.data,
                           o.size * sizeof(float));

  int x = TfLiteInterpreterGetOutputTensorCount(interpreter);
  float f;
  float max = -100;
  int idx = -1;
  for(int i = 0; i < 5; i++){
    memcpy(&f, o.data + i * 4, 4);
    if(f > max){
      max = f;
      idx = i;
    }
    
    printf("%f ", f);
  }
  printf("\nPredicted class is: %d\n", idx);

  // struct filedata m = getData("flowers_model.tflite");
  // // TfLiteModel *model = TfLiteModelCreateFromFile("converted_model.tflite");
  // TfLiteModel *model = TfLiteModelCreate(m.data, m.size);
  // // TfLiteModelCreate
  // TfLiteInterpreter *interpreter = TfLiteInterpreterCreate(model, NULL);

  // // Please, for the love of God, throw some exceptions when reading files
  // struct filedata i = getData("flower1");
  // TfLiteInterpreterAllocateTensors(interpreter);
  // TfLiteTensor *input_tensor = TfLiteInterpreterGetInputTensor(interpreter, 0);
  // TfLiteTensorCopyFromBuffer(input_tensor, i.data,
  //                            i.size); // size is already times sizeof(float)

  // TfLiteInterpreterInvoke(interpreter);

  // struct filedata o;
  // // int detection_anchor_indices = 100;
  // // int detection_boxes = 100 * 4;
  // // int detection_classes = 100;
  // // int detection_multiclass_scores = 100 * 44;
  // // int detection_scores = 100;
  // // int num_detections = 1;
  // // int full_size = detection_anchor_indices + detection_boxes + detection_classes + detection_multiclass_scores + detection_scores + num_detections;
  // // o.data = (float *)malloc(sizeof(float) * (full_size + 1)); // cause model predicts 5 classes
  // // o.size = full_size + 1;
  // o.data = (float*)malloc(sizeof(float) * (5 + 1));
  // o.size = 5 + 1;
  // const TfLiteTensor *output_tensor =
  //     TfLiteInterpreterGetOutputTensor(interpreter, 0);
  // TfLiteTensorCopyToBuffer(output_tensor, o.data,
  //                          o.size);

  // float f;
  // for(int i = 0; i < 5; i++){
  //   memcpy(&f, o.data + i * 4, 4);
  //   printf("%f ", f);
  // }
  // // memcpy(&f, o.data + detection_anchor_indices + 1, 4);
  // // printf("%f", f);

  return 0;
}
