Please refer to this [reddit
post](https://www.reddit.com/r/linuxquestions/comments/mw0a3f/need_help_with_linking_c_libraries/)
that I have made for steps of getting it to work.

I got it running: `gcc -o test -I/usr/local/include -L/usr/local/lib
testModel.c -ltensorflowlite_c`
