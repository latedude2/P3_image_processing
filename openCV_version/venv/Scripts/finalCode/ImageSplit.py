import cv2
import imutils
import numpy as np
from DetectRed import *

from openCV_version.venv.Scripts.finalCode.DetectRed import checkRed


def splitIntoCardImages(img):
    images = []

    ## convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    ## mask of green (36,25,25) ~ (86, 255,255)
    mask = cv2.inRange(hsv, (36, 25, 25), (70, 255, 255))

    ## slice the green
    imask = mask > 0
    green = np.zeros_like(img, np.uint8)
    green[imask] = img[imask]

    memes, threshImg = cv2.threshold(green, 0, 255, cv2.THRESH_BINARY_INV)

    grayScale = cv2.cvtColor(threshImg, cv2.COLOR_BGR2GRAY)

    grayScale = cv2.GaussianBlur(grayScale, (9, 9), 0)

    c = cv2.findContours(grayScale.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    c = imutils.grab_contours(c)

    for i in range(len(c)):
        perimeter = cv2.arcLength(c[i], True)
        if perimeter > 500:
            extLeft = tuple(c[i][c[i][:, :, 0].argmin()][0])
            extRight = tuple(c[i][c[i][:, :, 0].argmax()][0])
            extTop = tuple(c[i][c[i][:, :, 1].argmin()][0])
            extBot = tuple(c[i][c[i][:, :, 1].argmax()][0])

            # Used to flatted the array containing the co-ordinates of the vertices.

            TM = np.float32([[1, 0, -extLeft[0]], [0, 1, -extTop[1]]])
            imgT = cv2.warpAffine(img, TM, ((extRight[0] - extLeft[0]), (extBot[1] - extTop[1])))
            if imgT.shape[0] > 200:
                images.append(imgT)
            #cv2.imshow("Single card pls" + str(i), imgT)

    return images

#returns 2 thresholded images suit, number of the card
#has to be given colored image of the corner with the suit blob on the left and number blob on right side of image
def splitCornerToSuitAndNumber(img):
    images = []
    ## convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if checkRed(img, grey):
        minSaturation = 100
        maxSaturation = 255
        mask1 = cv2.inRange(hsv, (170, minSaturation, 25), (180, maxSaturation, 255))
        mask2 = cv2.inRange(hsv, (0, minSaturation, 25), (19, maxSaturation, 255))
        mask = mask1 | mask2

        ## slice the green
        imask = mask > 0
        red = np.zeros_like(img, np.uint8)
        red[imask] = img[imask]

        memes, threshImg = cv2.threshold(red, 0, 255, cv2.THRESH_BINARY_INV)
        threshImg = cv2.bitwise_not(threshImg)

    else:
        memes, threshImg = cv2.threshold(grey, 70, 255, cv2.THRESH_BINARY_INV)
        threshImg = cv2.cvtColor(threshImg, cv2.COLOR_GRAY2BGR)

    #cv2.imshow("Corner threshold", threshImg)

    grayScale = cv2.cvtColor(threshImg, cv2.COLOR_BGR2GRAY)

    c = cv2.findContours(grayScale.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    c = imutils.grab_contours(c)
    #print(len(c))
    for i in range(len(c)):
        perimeter = cv2.arcLength(c[i], True)
        if perimeter > 30 and perimeter < 500:
            extLeft = tuple(c[i][c[i][:, :, 0].argmin()][0])
            extRight = tuple(c[i][c[i][:, :, 0].argmax()][0])
            extTop = tuple(c[i][c[i][:, :, 1].argmin()][0])
            extBot = tuple(c[i][c[i][:, :, 1].argmax()][0])

            # Used to flatted the array containing the co-ordinates of the vertices.
            TM = np.float32([[1, 0, -extLeft[0]], [0, 1, -extTop[1]]])
            imgT = cv2.warpAffine(threshImg, TM, ((extRight[0] - extLeft[0]) + 2, (extBot[1] - extTop[1]) + 2))

            #cv2.imshow("Single card pls" + str(i), imgT)
            images.append(imgT)

    return findTwoBiggestImages(images)


def findTwoBiggestImages(images):
    #if(len(images) < 2):
        #print("Contours failed")

    biggestImage1 = images[0]

    bigImageIndex = 0
    for i in range(len(images)):
        if(images[i].shape[0] * images[i].shape[1] > biggestImage1.shape[0] * biggestImage1.shape[1]):
            biggestImage1 = images[i]
            bigImageIndex = i

    #print(len(images))
    images.remove(biggestImage1)
    #print(len(images))

    biggestImage2 = images[0]
    for i in range(len(images)):
        if (images[i].shape[0] * images[i].shape[1] > biggestImage2.shape[0] * biggestImage2.shape[1]):
            biggestImage2 = images[i]

    return biggestImage2, biggestImage1

