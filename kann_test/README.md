## Purpose

This directory is being used to store the files used to solve the classify problem with the kann C library.

### Steps

- Learn how it works, how train/test files are structured
- Create your own train/test files and create them
- Create a network and test it

### After flow is ready

I have managed to get a flow ready for working with images acquired
from a web camera. The problem right now is speed.

#### Solving the speed problem

One [article](https://semiengineering.com/speeding-up-neural-networks/)
talks about the memory difference between a net that uses floating
point(like ours do) and one that uses integers. There might be
a problem if numbers vary so much(from 0 to 255, rather than 0 to 1).
