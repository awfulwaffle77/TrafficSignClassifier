#include <stdio.h>
#include <tensorflow/lite/c/c_api.h>

struct filedata
{
  void *data;
  size_t size;
};

// Get information from RAW Image 
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
  struct filedata m = getData("converted_model.tflite");
  // TfLiteModel *model = TfLiteModelCreateFromFile("converted_model.tflite");
  TfLiteModel* model = TfLiteModelCreate(m.data, m.size);
  // TfLiteModelCreate
  TfLiteInterpreter *interpreter = TfLiteInterpreterCreate(model, NULL);

  struct filedata i = getData("flower1");
  TfLiteInterpreterAllocateTensors(interpreter);
  TfLiteTensor *input_tensor =
      TfLiteInterpreterGetInputTensor(interpreter, 0);
  TfLiteTensorCopyFromBuffer(input_tensor, i.data,
                             i.size); // size is already times sizeof(float)

  TfLiteInterpreterInvoke(interpreter);

  struct filedata o;
  o.data = (float*)malloc(sizeof(float) * 5);  // cause model predicts 5 classes
  o.size = 5;
  const TfLiteTensor *output_tensor =
  TfLiteInterpreterGetOutputTensor(interpreter, 0);
  TfLiteTensorCopyToBuffer(output_tensor, o.data,
                           o.size * sizeof(float));

  float f;
  for(int i = 0; i < 5; i++){
    memcpy(&f, o.data + i * 4, 4);
    printf("%f ", f);
  }

  return 0;
}
