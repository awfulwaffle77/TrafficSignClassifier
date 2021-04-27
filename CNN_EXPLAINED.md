[Main reference for
CNN](https://cs231n.github.io/convolutional-networks/)
Very good quotes on
[machinelearningmastery](https://machinelearningmastery.com/) to add in
documentation.
[Easier alternative for CNN development](https://www.researchgate.net/publication/308895193_Designing_Deep_Learning_Neural_Networks_using_Caffe)
[C++ Faster R-CNN
implementation](https://github.com/D-X-Y/caffe-faster-rcnn/tree/dev)

## Papers 

[Defense for two-stage object
detector](https://arxiv.org/pdf/1711.07264.pdf#table.7)
[EfficientNet](https://arxiv.org/pdf/1905.11946.pdf), currently
state-of-the-art in nets as it seems.
[Faster R-CNN paper](https://arxiv.org/pdf/1506.01497.pdf)


## Convolution
[Reference](https://machinelearningmastery.com/convolutional-layers-for-deep-learning-neural-networks/)

Convolution is a linear operation that involves the multiplication 
of a set of weights with the input, much like a traditional neural 
network. Given that the technique was designed for two-dimensional 
input, the multiplication is performed between an array of input 
data and a two-dimensional array of weights, called a filter or a kernel. 

The output from multiplying the filter with the input array one time is
a single value. As the filter is applied multiple times to the input
array, the result is a two-dimensional array of output values that
represent a filtering of the input. As such, the two-dimensional output
array from this operation is called a “feature map“.

Consider that the filters that operate directly on the raw pixel values
will learn to extract low-level features, such as lines.
The filters that operate on the output of the first line layers may
extract features that are combinations of lower-level features, such as
features that comprise multiple lines to express shapes.
This process continues until very deep layers are extracting faces,
animals, houses, and so on.

## Pooling
[Reference](https://machinelearningmastery.com/pooling-layers-for-convolutional-neural-networks/)

A limitation of the feature map output of convolutional layers is that
they record the precise position of features in the input. This means
that small movements in the position of the feature in the input image
will result in a different feature map. This can happen with
re-cropping, rotation, shifting, and other minor changes to the input
image.

A common approach to addressing this problem from signal processing is
called down sampling. This is where a lower resolution version of an
input signal is created that still contains the large or important
structural elements, without the fine detail that may not be as useful
to the task.

## Fully connected layers
[Reference](https://stats.stackexchange.com/questions/182102/what-do-the-fully-connected-layers-do-in-cnns)

*Dense and fully connected are two names for the same thing.*

The Kann Library's dense layers function as
[Keras'](https://www.tutorialspoint.com/keras/keras_dense_layer.htm).
This affects the output size. Please check the [colab
link](https://colab.research.google.com/drive/1khIoCbNl8awBK1dtXb-P2WsMQujA0zeR)

We can divide the whole network (for classification) into two parts:

Feature extraction: In the conventional classification algorithms,
like SVMs, we used to extract features from the data to make the
classification work. The convolutional layers are serving the same
purpose of feature extraction. CNNs capture better representation of
data and hence we don’t need to do feature engineering.

Classification: After feature extraction we need to classify the
data into various classes, this can be done using a fully connected (FC)
neural network. In place of fully connected layers, we can also use a
conventional classifier like SVM. But we generally end up adding FC
layers to make the model end-to-end trainable.

Briefly, fully connected layers add up info and output a 1D array
of classes with prediciton precentages.

## Batch size considerations
[Reference](https://medium.com/deep-learning-experiments/effect-of-batch-size-on-neural-net-training-c5ae8516e57)

Smaller batch sizes tend to give better results, as there is less
generalization. Bigger batch sizes allow paralelization.

## Object detection/recognition
[EfficientNet for ConvNets(Image
classification(?))](https://arxiv.org/pdf/1905.11946.pdf)
[Detection vs.
Recognition with source code](https://learnopencv.com/selective-search-for-object-detection-cpp-python/)
[Edge
boxes](https://www.microsoft.com/en-us/research/wp-content/uploads/2014/09/ZitnickDollarECCV14edgeBoxes.pdf)
[Selective
search](https://www.pyimagesearch.com/2020/06/29/opencv-selective-search-for-object-detection/)
[Mask RCNN](https://arxiv.org/pdf/1703.06870.pdf) -- apparently this is
the state of the art in object detection + recognition.
[Mask RCNN easily
explained](https://alittlepain833.medium.com/simple-understanding-of-mask-rcnn-134b5b330e95)
[Possibly useful Mask RCNN C++ repo](https://github.com/mintaka33/mask_rcnn_cpp)
[Mask RCNN
in-depth](https://engineering.matterport.com/splash-of-color-instance-segmentation-with-mask-r-cnn-and-tensorflow-7c761e238b46)
[Keras Mask
RCNN](https://machinelearningmastery.com/how-to-train-an-object-detection-model-with-keras/)

According to [Mask RCNN
in-dept](https://engineering.matterport.com/splash-of-color-instance-segmentation-with-mask-r-cnn-and-tensorflow-7c761e238b46),
Faster RCNN should be faster than Mask RCNN due to the latter's
overhead.

## Faster R-CNN

[RPN in Faster
R-CNN](https://www.quora.com/How-does-the-region-proposal-network-RPN-in-Faster-R-CNN-work?share=1)
(second answer)
[RPN in Faster R-CNN
explained](https://datascience.stackexchange.com/questions/27277/faster-rcnn-how-anchor-work-with-slider-in-rpn-layer/27282#27282)(scroll
down)

## VGGNet
[Reference paper for
epilepsy](https://www.researchgate.net/publication/323502161_Towards_Brain_Big_Data_Classification_Epileptic_EEG_Identification_with_a_Lightweight_VGGNet_on_Global_MIC)
[Reference from
Quora](https://www.quora.com/What-is-the-VGG-neural-network)


