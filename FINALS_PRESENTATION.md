## What I did

1. Augumented + organized the dataset to be compatible with YOLOv5
2. Model conversion from PyTorch to Tensorflow to be used with
TFLite
3. Posibility to be ran in a C program
4. Make the model be read from memory(+ contribution to TFLite repo?)
5. Make it run on MXRT1020 without a camera(image from memory)
6. Make the camera get images on the MXRT1020
7. Full run on MXRT1020 with camera


## Things to consider

Due to running out of time, try to test multiple models and draw graphs
with each one of the state-of-the-art models instead of trying to get it
working on MXRT.

## 25.05.2021

Steps 1 to 3. Make a full run on Linux.
First, test YOLO to see how it runs
