To get image as grayscale in Linux, simply use
`v4l2-ctl -c saturation=0` to set camera input saturation to 0.
[Reference](https://stackoverflow.com/questions/21881299/get-grayscale-image-directly-from-webcam-using-opencv)

Camera resolution is default higher, so I tried to lower it.
I tried 128x128 with `v4l2-ctl --set-fmt-video=width=128,height=128,pixelformat=YUYV`,
but it resetted to 160x120(width x height). When running the program with
128x128, it resetted to the default OpenCV values(I suppose), which
were 640x480. The solution was to set the resolution to 160x120 with
`v4l2-ctl --set-fmt-video=width=160,height=120,pixelformat=YUYV`.

Camera uses `YUYV` format, which is equivalent to [YUY2](https://www.fourcc.org/pixel-format/yuv-yuy2/).
It is the same as [YCbCr](https://en.wikipedia.org/wiki/YCbCr)

Given the YUYV input, I need to change it in memory to a grayscale format.
Writing the image to .jpg and then reading it in a `Mat` variable shows
that the content of the old Mat, `saved_img` is differnet from `image`, 
meaning that there is some conversion. These values do not correspond
to the the python script though.

Reading the image in the .c source without GRAYSCALE and reading it
**with** grayscale in the .py file leads to different results.

Reading the image in both places with GRAYSCALE, leads to the same array.

`imencode` returns a vector with size 6230, exactly the size of the
image after it is being saved as a `.jpg`. The image is compressed,
resulting in less than 120x160(=19200)bytes, but the image
viewer app decompresses it(probably) to show it in 120x160.

The question is, does the array resulting from imread result in
an array of 120x160 elements or 6230? 
I suppose that using the function imread returns in memory
the uncompressed array, so I do not need `imencode`.
**Maybe try encode and then decode??**

Encoding and decoding worked(I am 99% sure it does).
What I think it happens: The input from the camera is
YCbCr, I encode it to `.jpg` and then, when it is
decoded, it is transformed in RGB format, same as
when reading with `imread`. 
How I checked: I verified the arrays that result from this
encode-decode shenanigan and they are matching. Also, the
array resulted from `imread` in python, after resizing and reshaping
matches this one from memory. 

*Mission passed?*

Try checking with images sent as byte stream to the video camera.
You get the point? To check on the exact images that we verify
the algorithm, but to simulate it coming from the video camera.