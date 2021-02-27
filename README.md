# Traffic Sign Classifier
A traffic sign classifier on the MIMXRT1020 EVK. 

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
- I have compiled it with `g++ main.cpp -L/usr/local/lib -lopencv_core -lopencv_imgproc -lopencv_dnn -lopencv_highgui -lopencv_features2d -lopencv_imgcodecs -lopencv_cnn_3dobj`
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
