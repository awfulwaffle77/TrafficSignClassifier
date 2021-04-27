To implement Faster R-CNN in C with th basic CNN layers provided by
Kann, I have found this [Python FRCNN
repo](https://github.com/kbardool/keras-frcnn/blob/master/train_frcnn.py).
This uses VGG16/ResNet50 as base Network. We can try and implement a
VGG16 network from scratch with Kann.

One important step that is needed is checking if custom loss functions
are easily introduced in Kann and how it is done. There is a custom loss
function needed for RPN.
