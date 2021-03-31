import sys
import os
import random

fileName_x = sys.argv[1]
fileName_y = sys.argv[2]
if fileName_x is None:
    print("Give filename x as first argument.")
    exit(-1)
if fileName_y is None:
    print("Give filename y as second argument.")
    exit(-1)


f_x = open(fileName_x, "r")
f_y = open(fileName_y, "r")


## Reading the file, writing the same header, shuffling the lines and reordering indexes

Lines_x = f_x.readlines()
Lines_y = f_y.readlines()

f_x.close()
f_y.close()

f_x = open(fileName_x, "w")
f_y = open(fileName_y, "w")

headline_x = Lines_x[0]
headline_y = Lines_y[0]

Lines_x = Lines_x[1:len(Lines_x)]
Lines_y = Lines_y[1:len(Lines_y)]

shuffled = list(zip(Lines_x,Lines_y))
random.shuffle(shuffled)

Lines_x, Lines_y = zip(*shuffled)

f_x.write(headline_x)
f_y.write(headline_y)
count = 1
# for line in Lines_x:
#     line = line[line.find(":"):]  # strip the line of first character (that would be the index)
#     line = str(count) + line  # add new index
#     f_x.write(line)
#     count += 1

for i in range(len(Lines_y)):  # Lines_x and Lines_y have the same length
    linex = Lines_x[i]
    linex = linex[linex.find(":"):]  # strip the line of first character (that would be the index)
    linex  = str(count) + linex  # add new index
    f_x.write(linex)

    liney = Lines_y[i]
    liney = liney[liney.find(":"):]  # strip the line of first character (that would be the index)
    liney = str(count) + liney  # add new index
    f_y.write(liney)

    count += 1

# TODO: vezi cu liniile alea de labeluri

print("Lines shuffled.")