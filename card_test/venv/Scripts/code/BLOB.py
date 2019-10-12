from PIL import Image, ImageDraw
import numpy as np
import sys  # We need this in order to change the max recursion
import random


def main():
    # Python normally only allows a function to call itself 10^4 times, which is not enough for larger BLOBs
    sys.setrecursionlimit(10 ** 6)  # Changing the max recursion to 10^6
    img = Image.open('Images/ace2.JPG')

    binaryImg = binary(img)  # Converting to a binary image, based on some given benchmarks for RGB values
    blobImg = detectBlobs(binaryImg)  # Applying the BLOB detection, which converts "burned" pixels to pink and counts big BLOBs

    blobImg.show()
    del img, binaryImg, blobImg  # Deleting the temporary image files to save memory, since we have already shown the output



def detectBlobs(img):  # This function goes through finding each BLOB and counting them
    pixels = list(img.getdata())  # Creates a 1D list of RGB values for each pixel in the image
    width, height = img.size  # Setting the values for width and height based on the dimensions of the image
    pos = 0  # The position, of the current pixel, in the list
    counter = Counter()  # Creating an object from the Counter class (which can be found further down)
    generateColors(counter.colorList)  # Creates a list of 100 colors as (r, g, b) tuples, so we can give each BLOB a color

    for R, G, B in pixels:  # A for loop where we can work with the values of R, G & B, for the length of the pixels list

        # Since we have the pixels in a 1D list, we need some values to keep track of our actual x and y positions in the image
        # Because when "burning" pixels, we would like to track not only pixels to the left and right from our current position
        # But also below and above, which would otherwise be hard in a 1D list
        burnWidth = counter.widthCount  # Setting the burning position to the current x position in the image
        burnHeight = counter.heightCount  # Setting the burning position to the current y position in the image

        if (R == 255):  # Since it is a binary image, we can test if it is white using only R
            grassFire(pos, pixels, width, height, counter, burnWidth,
                      burnHeight)  # Starting a fire from our current position

            if (counter.pixelCount > 200):  # Checking if the BLOB we just burned is big enough to be counted
                counter.blobCount += 1  # Counting the BLOB
            counter.pixelCount = 0  # Resetting the pixel counter, so we are ready to count the size of the next BLOB

        counter.widthCount += 1  # Adding 1 to our current x position
        if (counter.widthCount >= width):  # Checking if our current x position is higher than the width
            counter.widthCount = 0  # Resetting our x position, to indicate that we have reset our x in the image
            counter.heightCount += 1  # Adding 1 to our current y position, since we have moved to the next line of pixels

        pos += 1  # Adding 1 to the position, to match the next element in the list that we will be checking

    img.putdata(pixels)  # Reconstructing an image from the now changed values of the pixels list
    print(counter.blobCount)  # Showing the amount of bigger BLOBs that we have found
    return img  # Returning the newly constructed image



# Even though we take a lot of variables, this method has to be on its own, since it will be calling itself
# Some of these could probable be avoided with some type of global variables since they don't change during the recursion
def grassFire(pos, pixels, width, height, counter, burnWidth, burnHeight):
    counter.pixelCount += 1  # Adding 1 to the counter for how many pixels the current BLOB persists of
    # Changing the color of the pixel we are "burning" to one of the random colors we have generated
    pixels[pos] = counter.colorList[counter.blobCount]  # We change the color so that we don't end up counting it twice

    # Checking that the x position of the pixel to the right of the currently burning one is within the image width
    if (burnWidth + 1 < width):
        # Checking that the pixel to the right of the currently burning one is white
        if (pixels[pos + 1] == (255, 255, 255)):
            # "Setting fire" to the white pixel to the right of the currently burning one
            grassFire(pos + 1, pixels, width, height, counter, burnWidth + 1, burnHeight)

    # Checking that the y position of the pixel below the currently burning one is within the image height
    if (burnHeight + 1 < height):
        # Checking that the pixel below the currently burning one is white
        if (pixels[pos + width] == (255, 255, 255)):
            # "Setting fire" to the white pixel below the currently burning one
            grassFire(pos + width, pixels, width, height, counter, burnWidth, burnHeight + 1)

    # Checking that the x position of the pixel to the left of the currently burning one is'nt less than 0
    if (burnWidth - 1 >= 0):
        # Checking that the pixel to the left of the currently burning one is white
        if (pixels[pos - 1] == (255, 255, 255)):
            # "Setting fire" to the white pixel to the left of the currently burning one
            grassFire(pos - 1, pixels, width, height, counter, burnWidth - 1, burnHeight)

    # Checking that the y position of the pixel above the currently burning one is'nt less than 0
    if (burnHeight - 1 >= 0):
        # Checking that the pixel above currently burning one is white
        if (pixels[pos - width] == (255, 255, 255)):
            # "Setting fire" to the white pixel above currently burning one
            grassFire(pos - width, pixels, width, height, counter, burnWidth, burnHeight - 1)

    return pixels  # Returning the now changed values of the list, where some of the pixels have changed color



# This is a rewrite of the function used for manual grey-scaling
def binary(img):
    pixels = list(img.getdata())  # making a list from image data (pixel values in r,g,b)

    newPixels = []  # new list made for storing the color values as tuples (data points with more than one value: (10, 2))
    for R, G, B in pixels:  # goes through RGB values in the pixels list
        if (R > 120 and G < 100 and B < 100):  # Checking if the RGB values of the current pixel match the thresholds (here looking for red)
            color = 255  # making it white
        else:
            color = 0  # making it black
        value = (color, color, color)  # making a tuple with three identical values
        newPixels.append(value)  # adding the current tuple to the list we have created

    img.putdata(newPixels)  # Constructing a new image from the tuple values in our list
    return img  # Returning the newly constructed image


# This class contain a bunch of variables that, in other programs would simply be global variables
# But since Python handles variables weirdly, we instead have them here, so we can change the specific values of an object
class Counter:
    pixelCount = 0  # Is used to track how many pixels each BLOB consists of
    blobCount = 0  # Is used to keep track of how many bigger BLOBs we find
    widthCount = 0  # Is used to keep track of our current x position in the image
    heightCount = 0  # Is used to track our current y position in the image
    colorList = []  # A list for storing colors to give the different BLOBs


def generateColors(colorList):  # Generates a list of 100 colors

    for i in range(100):  # A for loop that run 100 times through values of i from 0 to 99
        # Assigning a random int value between 0 and 255 to each color
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        color = (r, g, b)  # Collecting the three random values in a tuple
        colorList.append(color)  # Adding the tuple/color to our list of colors


if __name__ == '__main__':
    main()
