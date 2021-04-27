# Traffic Sign Classifier
A traffic sign classifier on the MIMXRT1020 EVK. 

## Things to document on
- Devicetree
- Arm IP Bus (Reference Manua page 33)

## TODO

~So far, I have managed to train a nerual network and make it
identify some of the images, altough moving really slow. I
need to have the captured image as an array of chars and feed it
to the neural network from memory to have first full flow of work.
So, to do:
- Make the image acquisition use the array from the memory and feed it
to the neural network
- Note the current execution time and accuracy in a file so we can 
make a graph(also please write a script that automatically saves
all of the data we need here: layers, exec time, size, accuracy,
initial parameters 
After that:
- Create a neural network of smaller size to make it identify images faster~

- Object detection with Sliding Window or Selective Search or sth
- Creating a Faster R-CNN to classify images
- Possibility to import parameters from a .hdf5 file trained in python
- Graphs with differnt methods to see the time differences

## What I chose
- Due to the fact that, at the moment, I have not found out how to use fs on Zephyr, I will try to
fiddle with the [sod embedded library](https://sod.pixlab.io/intro.html) due to the fact that
it accept reading images from memory. I will change its `load_weights_upto`(line 4036 in `sod.c`)
so that it can also read a model from memory.
- I have tried to use pipes to simulate a `FILE*`, because I cannot use files, but it did not work.
~~- Apparently, there ways to open a buffer as a `FILE*`. See here: [fmemopen](https://www.gnu.org/software/libc/manual/html_node/String-Streams.html). 
Great read on that [here](https://bytes.com/topic/c/answers/507924-how-convert-char-file)~~
- I have chosen to use Kann C Library

## Working with the Raspberry Pi

After getting the C program with Kann library to work (altough not great at all), I have to acquire images in the same 
format as given test data from the video camera. I should test if this works in Python and then go to write that in C.

Steps:
- Connect to the rpi (done)
- Do the wiring as tutorials show (done)
- Try with a quick script (python would be great) (done)
- Port that to C and test it (c++ tho, done)
- Check if you can create the array in memory (already created)
- Actually modify the C program to classify the array from memory
- Make image grayscale? for better performance

### Kann C Library

The example uses two files, x and y. `x` contains the images and `y` contains the labels. Files are gzipped(hence the .gz extension).
After ungzipping(with `ungzip`), you can see the format of such file. Loading the files in the code work with either .gz file or not gzipped.


## Zephyr

### The files problem
I saw that Zephyr accepts [open() and read()](https://docs.zephyrproject.org/latest/guides/portability/posix.html) so I tried to fiddle with them.

### Finding GPIO Ports
In the file `x` I have found the line `gpio1:gpio@401b8000`, that led me to the [Reference Manual](#) page 34, where I have found that there is a NIC Port
GPIO1 starting at that adress.

### For the Zephyr to C Code communication
I understand the GPIO ports for `device_get_binding` are named `GPIO_x` where `x` is a number from 1 to 5. 
The number of the PIN of the LED that is in the blinky example is 5, corresponding to `GPIO1_IO05` in the [Reference Manual](#) page 273, which has the PAD `GPIO_AB_B0_05`.
Searching for this PAD in the Schematics, it corresponds to USER_LED.
The pin number which has to be used in the C Zephyr code(defined as `PIN` in the [blinky example](#)) is `n` from `GPIOx_IOn`, where `x` is a number from 1 to 5.

- Schematics -> contains PADs.
- The [.xsl](#) -> contains PAD and ALT5(GPIO ports)
- The reference manual -> contains contains PAD and ALT5(GPIO ports)

## Issues
Please read each issue throughoutly.
Also, please delelte `CMakeCache.txt` after every failed build attempt.

### Getting the OpenCV cnn_3dobj module
- To use the [C CNN object classifier](https://docs.opencv.org/3.4/df/d38/tutorial_feature_classification.html)I had installed the OpenCV 
with apt get
- I have followed the instructions to install [caffe](https://github.com/Wangyida/caffe/tree/cnn_triplet) for Ubuntu (here)[http://caffe.berkeleyvision.org/install_apt.html].
The new package name was `caffe` instead of `caffe-cpu/caffe-cuda`
- Compiling the [cnn_3dobj module](https://github.com/opencv/opencv_contrib/tree/master/modules/cnn_3dobj) was a pain, but I finally got it going by installing the dependencies
with apt and finally getting the OpenCV modules(including this one) in `/usr/local/lib` with the command:
`cmake -DBUILD_opencv_cnn_3dobj=ON -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_TBB=ON -D WITH_V4L=ON -D WITH_QT=OFF -D WITH_OPENGL=ON -D WITH_VTK=ON -D OPENCV_EXTRA_MODULES_PATH=../opencv_contrib-master/modules ../opencv-master/`. As the cnn_3dobj module was disabled for me(for some reason), I managed to get it installed with `-DBUILD_opencv_3dobj=ON` and following the steps
shown in [the cnn_3dobj module github page](https://github.com/opencv/opencv_contrib/tree/master/modules/cnn_3dobj)
- Before getting this installed, there were several linking issues at compile time.
- By installing OpenCV with apt, the modules were installed to `/usr/include/opencv4/opencv2`. There were several issues with this, so I created a directory in `/usr/include/` with the 
name `opencv2` which was the symlink(`ln -s`) of `opencv4/opencv2` so it fixed some compiling issues. Also, I had to manually add `cnn_3dobj.hpp` to `/usr/include/opencv4/opencv2` to not 
get compiling errors. The command used to get the binary was `g++ main.cpp -lopencv_core -lopencv_imgproc -lopencv_dnn -lopencv_highgui -lopencv_features2d 
- lopencv_imgcodecs -L/usr/local/lib -lopencv_cnn_3dobj`, where the `OpenCV core, imgproc, dnn etc. libs are in `/usr/include/opencv4/opencv2`(which also has `/usr/include/opencv2` 
linked) and the .so library of cnn_3dobj module(named `libopencv_cnn_3dobj.so`
- I have compiled it with `g++ main.cpp --L/usr/local/lib L/usr/local/lib -lopencv_core -lopencv_imgproc -lopencv_dnn -lopencv_highgui -lopencv_features2d -lopencv_imgcodecs -lopencv_cnn_3dobj`
- After getting it compiled, there was still and issue of the .so files not getting recognized, so I followed 
this [link](https://stackoverflow.com/questions/12335848/opencv-program-compile-error-libopencv-core-so-2-4-cannot-open-shared-object-f)
- The Segmentation Fault errors are due to wrong paths in the .cpp. Some files exist, other don't, such as the `images_all` directory which has to be created.

###  Getting Zephyr on the board
- The OpenSDA J-Link probe is an **onboard** chip and an external debugger is **not** needed
- The reset button is SW5, next to the Micro USB port
- **WSL did not support `west flash` at the time of writing, as JLinkExe was throwing the `Connecting to J-Link failed` error even after adding the `99-jlink.rules` ruleset to `/etc/udev/rules.d`**
- Be sure to add the [firmware](https://www.segger.com/downloads/jlink/OpenSDA_MIMXRT1020-EVK) to be able to see the board in `/dev` (by holding SW5 while powering up the board)
- Testing with the GUI Putty did not work for me, so I did from CLI with the following command: `sudo putty /dev/ttyACM0 -serial -sercfg 115200,8,n,1`. 
The connection should show some numbers when nothing is flashed on it
- Be sure to download [J-Link](https://www.segger.com/downloads/jlink/#J-LinkSoftwareAndDocumentationPack) **and read the README included**
- Only after Dual Booting Linux was I able to get it working by following the steps on [Zephyr website](https://docs.zephyrproject.org/latest/boards/arm/mimxrt1020_evk/doc/index.html).
- I have also installed `libusb-1.0-0-dev`, but I do not believe it is needed

### Making use of a filesystem
