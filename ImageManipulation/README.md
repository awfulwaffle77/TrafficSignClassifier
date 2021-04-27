# Purpose

This folder stores the python scripts needed to manipulate images.

## PPM to JPG

Due to the fact that the GTSRB dataset comes as `.ppm`, we need a script to transform them to `.jpg`

## Create Kann Files

Creates the `x` and `y` files. `x` contains the images. Every image is on a line, where an item on
a column represents the pixel value. 

## Issues

- The network does not correctly classify the images. Try to scramble the train data as
to not be one after another in the train file. 

## Modifications

- I have modified the int 255 to float 255.0. I do not know if it makes a difference yet.

## TODO

- As this project will require lots of testing, write a script to
write the output and the parameters used to a file

- See if the written image has the same values in both .py and .c
