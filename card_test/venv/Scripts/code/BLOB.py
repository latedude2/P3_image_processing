from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import sys  # We need this in order to change the max recursion
import random


def main():
    # Python normally only allows a function to call itself 10^4 times, which is not enough for larger BLOBs
    sys.setrecursionlimit(10 ** 9)  # Changing the max recursion to 10^6
    imgName = "Images/nine.JPG"  # Defining the name, since we are currently using it twice
    img = Image.open(imgName)
    counter = Counter()  # Creating an object from the Counter class (which can be found further down)

    binaryImg = binary(img)  # Converting to a binary image, based on some given benchmarks for RGB values
    medianImg = medianFilter(binaryImg)
    blobImg = detectBlobs(medianImg, counter)  # Applying the BLOB detection, which converts "burned" pixels to pink and counts big BLOBs

    img = Image.open (imgName)  # Opening the original image again, cause we have accidentally changed it along the way
    detectColor(counter, img, blobImg, 3)  # Detecting the color of a given BLOB

    blobImg.show()
    del img, binaryImg, medianImg, blobImg  # Deleting the temporary image files to save memory, since we have already shown the output



def detectBlobs(img, counter):  # This function goes through finding each BLOB and counting them
    pixels = list(img.getdata())  # Creates a 1D list of RGB values for each pixel in the image
    width, height = img.size  # Setting the values for width and height based on the dimensions of the image
    pos = 0  # The position, of the current pixel, in the list
    generateColors(counter.colorList)  # Creates a list of 100 colors as (r, g, b) tuples, so we can give each BLOB a color
    baseColor = (255, 0, 0)  # The color initially given to BLOBs, before we know if they are big enough
    whiteColor = (255, 255, 255)  # Defined here so we can use the fire to search for other colors as well

    for R, G, B in pixels:  # A for loop where we can work with the values of R, G & B, for the length of the pixels list

        # Since we have the pixels in a 1D list, we need some values to keep track of our actual x and y positions in the image
        # Because when "burning" pixels, we would like to track not only pixels to the left and right from our current position
        # But also below and above, which would otherwise be hard in a 1D list
        burnWidth = counter.widthCount  # Setting the burning position to the current x position in the image
        burnHeight = counter.heightCount  # Setting the burning position to the current y position in the image

        if (R == 255):  # Since it is a binary image, we can test if it is white using only R
            # Starting a fire from our current position, making all the pixels red, so we know they have been counted
            grassFire8(pos, pixels, width, height, counter, burnWidth, burnHeight, whiteColor, baseColor)

            if (counter.pixelCount > 350):  # Checking if the BLOB we just burned is big enough to be counted
                counter.blobCount += 1  # Counting the bigger BLOBs
                # Calling the fire again, this time changing red pixels to a color from our list, so they can be handled individually later
                grassFire8(pos, pixels, width, height, counter, burnWidth, burnHeight, baseColor, counter.colorList[counter.blobCount])
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
def grassFire8(pos, pixels, width, height, counter, burnWidth, burnHeight, detectColor, burnColor):  # The 8 indicates an eight point conection
    counter.pixelCount += 1  # Adding 1 to the counter for how many pixels the current BLOB persists of
    # Changing the color of the pixel we are "burning" to one of the random colors we have generated
    pixels[pos] = burnColor  # We change the color so that we don't end up counting it twice

    # Checking that the x position of the pixel to the right of the currently burning one is within the image width
    if (burnWidth + 1 < width):
        # Checking that the pixel to the right of the currently burning one is white
        if (pixels[pos + 1] == detectColor):
            # "Setting fire" to the white pixel to the right of the currently burning one
            grassFire8(pos + 1, pixels, width, height, counter, burnWidth + 1, burnHeight, detectColor, burnColor)

    # Checking that the x and y positions of the pixel below to the right of the currently burning one is within the image width
    if (burnWidth + 1 < width and burnHeight + 1 < height):
        # Checking that the pixel below to the right of the currently burning one is white
        if (pixels[pos + 1 + width] == detectColor):
            # "Setting fire" to the white pixel below to the right of the currently burning one
            grassFire8(pos + 1 + width, pixels, width, height, counter, burnWidth + 1, burnHeight + 1, detectColor, burnColor)

    # Checking that the y position of the pixel below the currently burning one is within the image height
    if (burnHeight + 1 < height):
        # Checking that the pixel below the currently burning one is white
        if (pixels[pos + width] == detectColor):
            # "Setting fire" to the white pixel below the currently burning one
            grassFire8(pos + width, pixels, width, height, counter, burnWidth, burnHeight + 1, detectColor, burnColor)

    # Checking that the x and y positions of the pixel below to the left the currently burning one is within the image height
    if (burnHeight + 1 < height and burnWidth - 1 >= 0):
        # Checking that the pixel below to the left the currently burning one is white
        if (pixels[pos + width - 1] == detectColor):
            # "Setting fire" to the white pixel below to the left the currently burning one
            grassFire8(pos + width - 1, pixels, width, height, counter, burnWidth - 1, burnHeight + 1, detectColor, burnColor)

    # Checking that the x position of the pixel to the left of the currently burning one is'nt less than 0
    if (burnWidth - 1 >= 0):
        # Checking that the pixel to the left of the currently burning one is white
        if (pixels[pos - 1] == detectColor):
            # "Setting fire" to the white pixel to the left of the currently burning one
            grassFire8(pos - 1, pixels, width, height, counter, burnWidth - 1, burnHeight, detectColor, burnColor)

    # Checking that the x and y positions of the pixel above to the left of the currently burning one is'nt less than 0
    if (burnWidth - 1 >= 0 and burnHeight - 1 >= 0):
        # Checking that the pixel above to the left of the currently burning one is white
        if (pixels[pos - 1 - width] == detectColor):
            # "Setting fire" to the white pixel above to the left of the currently burning one
            grassFire8(pos - 1 - width, pixels, width, height, counter, burnWidth - 1, burnHeight - 1, detectColor, burnColor)

    # Checking that the y position of the pixel above the currently burning one is'nt less than 0
    if (burnHeight - 1 >= 0):
        # Checking that the pixel above currently burning one is white
        if (pixels[pos - width] == detectColor):
            # "Setting fire" to the white pixel above currently burning one
            grassFire8(pos - width, pixels, width, height, counter, burnWidth, burnHeight - 1, detectColor, burnColor)

    # Checking that the x and y positions of the pixel above to the right the currently burning one is'nt less than 0
    if (burnHeight - 1 >= 0 and burnWidth + 1 < width):
        # Checking that the pixel above to the right currently burning one is white
        if (pixels[pos - width + 1] == detectColor):
            # "Setting fire" to the white pixel above to the right currently burning one
            grassFire8(pos - width + 1, pixels, width, height, counter, burnWidth + 1, burnHeight - 1, detectColor, burnColor)

    return pixels  # Returning the now changed values of the list, where some of the pixels have changed color



# This is a rewrite of the function used for manual grey-scaling
def binary(img):
    pixels = list(img.getdata())  # making a list from image data (pixel values in r,g,b)

    newPixels = []  # new list made for storing the color values as tuples (data points with more than one value: (10, 2))
    for R, G, B in pixels:  # goes through RGB values in the pixels list
        if (R > 120 and G < 100 and B < 100):  # Checking if the RGB values of the current pixel match the thresholds (here looking for red)
            color = 255  # making it red
        elif (R < 40 and G < 35 and B < 30):  # Checking if the RGB values of the current pixel match the thresholds (here looking for black)
            color = 255  # making it white
        else:
            color = 0  # making it black
        value = (color, color, color)  # making a tuple with three identical values
        newPixels.append(value)  # adding the current tuple to the list we have created

    img.putdata(newPixels)  # Constructing a new image from the tuple values in our list
    return img  # Returning the newly constructed image


# A median filter for clearing out noise in the binary image
def medianFilter(img):
    pixels = list(img.getdata()) # making a list from image data (pixel values in r,g,b)
    width, height = img.size  # Setting the values for width and height based on the dimensions of the image
    newImg = img

    newPixels = []  # new list made for storing the color values as tuples (data points with more than one value: (10, 2))
    whiteCounter = 0  # Since it is a binary image, we just need to count if there are more white or black pixels in the vicinity
    listPos = 0  # Current pixel in the image list of pixels
    xPos = 0  # Current x position in the image
    yPos = 0  # current y position in the image
    value = 0  # Used to assigning a color to the new list of pixels

    for R, G, B in pixels:  # looping through the image's RGB-values
        if (xPos >= width):  # Checking if we have reached the edge of the image
            xPos = 0  # resetting our x position when we cross the edge
            yPos += 1  # adding to our y position, since we are now in the next row of pixels

        if (xPos - 1 >= 0 and yPos - 1 >= 0):  # Checking that we aren't looking for a pixel outside the image
            if (pixels[listPos - 1 - width] == (255, 255, 255)):  # Checking if the pixel above to the left is white
                whiteCounter += 1  # counting the white pixel

        if (yPos - 1 >= 0):  # Checking that we aren't looking for a pixel outside the image
            if (pixels[listPos - width] == (255, 255, 255)):  # Checking if the pixel above is white
                whiteCounter += 1  # counting the white pixel

        if (yPos - 1 >= 0 and xPos + 1 < width):  # Checking that we aren't looking for a pixel outside the image
            if (pixels[listPos + 1 - width] == (255, 255, 255)):  # Checking if the pixel above to the right is white
                whiteCounter += 1  # counting the white pixel

        if (xPos - 1 >= 0):  # Checking that we aren't looking for a pixel outside the image
            if (pixels[listPos - 1] == (255, 255, 255)):  # Checking if the pixel to the left is white
                whiteCounter += 1  # counting the white pixel

        # We don't need to check if we are outside the image, since this is just our current pixel
        if (pixels[listPos] == (255, 255, 255)):  # Checking if the current pixel is white
                whiteCounter += 1  # counting the white pixel

        if (xPos + 1 < width):  # Checking that we aren't looking for a pixel outside the image
            if (pixels[listPos + 1] == (255, 255, 255)):  # Checking if the pixel to the right is white
                whiteCounter += 1  # counting the white pixel

        if (yPos + 1 < height and xPos - 1 >= 0):  # Checking that we aren't looking for a pixel outside the image
            if (pixels[listPos - 1 + width] == (255, 255, 255)):  # Checking if the pixel below to the left is white
                whiteCounter += 1  # counting the white pixel

        if (yPos + 1 < height):  # Checking that we aren't looking for a pixel outside the image
            if (pixels[listPos + width] == (255, 255, 255)):  # Checking if the pixel below is white
                whiteCounter += 1  # counting the white pixel

        if (xPos + 1 < width and yPos + 1 < height):  # Checking that we aren't looking for a pixel outside the image
            if (pixels[listPos + 1 + width] == (255, 255, 255)):  # Checking if the pixel below to the right is white
                whiteCounter += 1  # counting the white pixel

        if (whiteCounter >= 5):  # Checking if more than half of the pixels where white
            value = 255
        else:
            value = 0

        color = (value, value, value)
        newPixels.append(color)  # Adding the calculated color to the list of pixels for the new image

        listPos += 1
        xPos += 1
        whiteCounter = 0  # Resetting our counter for the nest pixel

    newImg.putdata(newPixels)  # Constructing a new image from the tuple values in our list
    return newImg  # Returning the newly constructed image


# This class contain a bunch of variables that, in other programs would simply be global variables
# But since Python handles variables weirdly, we instead have them here, so we can change the specific values of an object
class Counter:
    pixelCount = 0  # Is used to track how many pixels each BLOB consists of
    blobCount = 0  # Is used to keep track of how many bigger BLOBs we find
    widthCount = 0  # Is used to keep track of our current x position in the image
    heightCount = 0  # Is used to track our current y position in the image
    colorList = []  # A list for storing colors to give the different BLOBs


def generateColors(colorList):  # Generates a list of 75 colors
    r = 0
    g = 0
    b = 250

    for i in range(75):  # A for loop that run 100 times through values of i from 0 to 99
        # Assigning slowly changing color values for the different BLOBS
        if (i < 25):
            b -= 10
            g += 10
        elif (25 >= i < 50):
            g -= 10
            r += 10
        else:
            r -= 10
            b += 10

        color = (r, g, b)  # Collecting the three  values in a tuple
        colorList.append(color)  # Adding the tuple/color to our list of colors


def detectColor (counter, originalImg, blobImg, blobNum):
    originalPixels = list(originalImg.getdata())  # Creates a 1D list of RGB values for each pixel in the original image
    blobPixels = list(blobImg.getdata())  # Creates a 1D list of RGB values for each pixel in the BLOB image
    pos = 0  # tracking the position in the pixel lists, so we know which pixels to check in the original image
    pixelsToCheck = []  # Saving a list of the position of the pixels we are checking

    # Will be used to find the average color of the BLOB
    redTotal = 0
    greenTotal = 0
    blueTotal = 0
    blobSize = 0

    for R, G, B in blobPixels:
        pos += 1
        if ((R, G, B) == counter.colorList[blobNum]):  # Finding the pixels matching the color of the BLOB we are checking
            pixelsToCheck.append(pos)  # saving the pixel positions
            blobSize += 1  # Counting the BLOB size to calculate average color

    pos = 0  # Resetting position so we can go though the new image, since we have saved the ones we need in a list
    for R, G, B in originalPixels:
        pos += 1
        if (pos in pixelsToCheck):  # Finding the pixels matching our saved positions
            # Adding up the colors of all the pixels in the BLOB
            redTotal += R
            greenTotal += G
            blueTotal += B

    # calculating the average for each color
    averageRed = redTotal/blobSize
    averageGreen = greenTotal/blobSize
    averageBlue = blueTotal/blobSize

    # Checking for red with the same parameters as in the binary function
    if (averageRed > 120 and averageGreen < 100 and averageBlue < 100):
        print("The card is red")
    else:  # Since this area was detected in the binary function, the only other option than red is black
        print("The card is black")


if __name__ == '__main__':
    main()
