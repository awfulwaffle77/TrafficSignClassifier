Please refer to this [reddit
post](https://www.reddit.com/r/linuxquestions/comments/mw0a3f/need_help_with_linking_c_libraries/)
that I have made for steps of getting it to work.

I got it running: `gcc -o test -I/usr/local/include -L/usr/local/lib
testModel.c -ltensorflowlite_c`

I have used a model that classifies flowers from
[here](https://www.tensorflow.org/hub/tutorials/tf2_image_retraining)
and have successfully had it load a model from memory and predict
classes in file `testModel.c`.

`exportPhoto.py` exports photo as raw format.
