imagerater
=======================

This project offers a simple python library to read and display images from a folder.
These images can then be rated in the command line with an integer input between
specified minimum and maximum values.
The library then flattens and normalizes the picture
and saves it together with the integer rating in a npy file.
This library supports image rating and the results can be used to train neural networks.

Install
=======================

pip install imagerater

Execute
=======================

The general form goes like this:
python imagerater.py -f <filelocation> -i <minimum> -x <maximum> -q <question>

This will start the program and read images from the filelocation.
Please consider that all images have to be of the same size as the first image.
If an image has a different size than the first image,
this image cannot be appended to the matrix and will be skipped.

-i 1 defines the minimum value of the rating scale
-x 5 defines the maximum value of the rating scale

You can now rate the images between 1 and 5.

-q defines the question that appears as the command line input prompt.

Please specify all values so that the program works properly.

A sample command could look like this:
python imagerater.py -i 1 -x 5 -f '../images/images_www.zalando.de_cropping/cropped/*.jpg' -q "Rate shoe: "
