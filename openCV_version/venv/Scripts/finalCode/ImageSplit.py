import cv2
import imutils
import numpy as np
from DetectRed import *

from DetectRed import checkRed


def splitIntoCardImages(img):
#Splits the image into an array of images that each have 1 card in them

    images = []

    blur = cv2.GaussianBlur(img, (9, 9), 0)

    ## convert to hsv
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    ## mask of green (36,25,25) ~ (86, 255,255)
    mask = cv2.inRange(hsv, (30, 25, 5), (75, 255, 255))

    ## slice the green
    imask = mask > 0
    green = np.zeros_like(img, np.uint8)
    green[imask] = img[imask]

    memes, threshImg = cv2.threshold(green, 0, 255, cv2.THRESH_BINARY_INV)

    grayScale = cv2.cvtColor(threshImg, cv2.COLOR_BGR2GRAY)

    c = cv2.findContours(grayScale.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    c = imutils.grab_contours(c)

    for i in range(len(c)):
        perimeter = cv2.arcLength(c[i], True)
        if perimeter > 500:
            extLeft = tuple(c[i][c[i][:, :, 0].argmin()][0])
            extRight = tuple(c[i][c[i][:, :, 0].argmax()][0])
            extTop = tuple(c[i][c[i][:, :, 1].argmin()][0])
            extBot = tuple(c[i][c[i][:, :, 1].argmax()][0])

            #TM - Transform matrix for moving the card to the top left corner
            TM = np.float32([[1, 0, -extLeft[0]], [0, 1, -extTop[1]]])
            # Crop the card image
            imgT = cv2.warpAffine(img, TM, ((extRight[0] - extLeft[0]), (extBot[1] - extTop[1])))
            if imgT.shape[0] < 400 and imgT.shape[0] > 150:
                images.append(imgT)
            #cv2.imshow("Single card pls" + str(i), imgT)

    return images


def splitCornerToSuitAndNumber(img, isRed):
# returns 2 thresholded images suit, number of the card
# has to be given colored image of the corner with the suit blob on the left and number blob on right side of image

    images = []
    ## convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if isRed:
        minSaturation = 130
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

        #cv2.imshow("Red Thresh",threshImg)

    else:
        memes, threshImg = cv2.threshold(grey, 70, 255, cv2.THRESH_BINARY_INV)
        threshImg = cv2.cvtColor(threshImg, cv2.COLOR_GRAY2BGR)
        #cv2.imshow("Black threshold", threshImg)

    grayScale = cv2.cvtColor(threshImg, cv2.COLOR_BGR2GRAY)

    c = cv2.findContours(grayScale.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    c = imutils.grab_contours(c)


    for i in range(len(c)):
        perimeter = cv2.arcLength(c[i], True)

        if perimeter > 30 and perimeter < 500:
            x, y, w, h = cv2.boundingRect(c[i])
            if h > 10:
                # print(i)
                extLeft = tuple(c[i][c[i][:, :, 0].argmin()][0])
                extRight = tuple(c[i][c[i][:, :, 0].argmax()][0])
                extTop = tuple(c[i][c[i][:, :, 1].argmin()][0])
                extBot = tuple(c[i][c[i][:, :, 1].argmax()][0])

                if(extTop[1] > 2): # we dont want objects that are touching image top - this causes problems with cards like 10 and Queen
                    #print("contourTop: " + str(extTop[1]) + " image top: " + str(img.shape[1]))

                    # Used to flatted the array containing the co-ordinates of the vertices.
                    TM = np.float32([[1, 0, -extLeft[0]], [0, 1, -extTop[1]]])
                    imgT = cv2.warpAffine(threshImg, TM, ((extRight[0] - extLeft[0]) + 2, (extBot[1] - extTop[1]) + 2))

                    #cv2.imshow("Single card pls" + str(i), imgT)
                    images.append(imgT)

    return findTwoBiggestImages(images)

def findTwoBiggestImages(images):
#Returns to biggest images in the list based on area

    #if(len(images) < 2):
        #print("Contours failed")
    #print(len(images))

#find first biggest image - number
    biggestImage1 = images[0]
    for i in range(len(images)):
        if(images[i].shape[0] * images[i].shape[1] > biggestImage1.shape[0] * biggestImage1.shape[1]):
            height = images[i].shape[0]
            width = images[i].shape[1]
            if(width > height):
                if( width / height > 1.3):
                    biggestImage1 = images[i]
            else:
                if (height / width > 1.3):
                    biggestImage1 = images[i]

    images.remove(biggestImage1)
    #print(len(images))

    '''
    #find first biggest image - number
    biggestImage1 = images[0]
    for i in range(len(images)):
        if(images[i].shape[0] * images[i].shape[1] > biggestImage1.shape[0] * biggestImage1.shape[1]):
            biggestImage1 = images[i]
    images.remove(biggestImage1)
    #print(len(images))
    
    '''

    cv2.imshow("Number", biggestImage1)
    # cv2.imwrite("NumberImage.png", biggestImage1)
    # Create new list that does not have images with holes in them(We are trying to avoid blobs with holes in them) - this might need changing

    imagesToCheck = []
    try:
        for i in range(len(images)):
            width = images[i].shape[1]
            heigth = images[i].shape[0]
            image = images[i]
            centerH = int(heigth / 2)
            centerW = int(width / 2)
            image_data = np.asarray(image)
            centerPixel = image_data[centerH, centerW]
            if centerPixel[0] > 0:
                imagesToCheck.append(images[i])
    except:
        if False:
            print("Failed to remove")


    #print(len(imagesToCheck))

    #find second biggest image
    biggestImage2 = imagesToCheck[0]

    for i in range(len(imagesToCheck)):
        if (imagesToCheck[i].shape[0] * imagesToCheck[i].shape[1] > biggestImage2.shape[0] * biggestImage2.shape[1]):
            biggestImage2 = imagesToCheck[i]

    #cv2.imshow("Suit", biggestImage2)

    return biggestImage2, biggestImage1

