from PIL import Image
import sys
import re 
import os

# Filename would be the folder where are the .ppm files are
folderName = sys.argv[1]
print(folderName)

for subdir, dirs, files in os.walk(folderName):
    # If directory does not exist
    for file in files:
        filename = os.path.join(subdir, file)
        # If it is already a jpg, skip
        if filename.split('.')[-1] == "jpg":
            continue
        # Due to the fact that the GTSRB has a .csv file in all folders, we check it to not be a csv
        #   so we can convert only .ppm files
        if filename.split('.')[-1] == "csv":
            os.remove(filename)
            continue
        im = Image.open(filename)
        # Should be new path
        newname = filename.split('.')[0] + '.jpg'
        # Remove the ppm file as we do not need it
        im.save(newname)
        im.close()
        os.remove(filename)
