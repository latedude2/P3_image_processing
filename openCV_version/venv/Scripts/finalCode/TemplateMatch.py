import cv2
import imutils
import numpy as np
from ImageSplit import *

def templateMatch(original, template):
#returns how many pixels don't match

    width = int(template.shape[1])
    height = int(template.shape[0])
    dim = (width, height)
    # resize image
    original = cv2.resize(original, dim, interpolation=cv2.INTER_AREA)

    #cv2.imshow("Original", original)
    #cv2.imshow("Template", template)

    if original.shape == template.shape:  # checks if the size and amount of channels in the images match. Optional.
        difference = cv2.subtract(original, template)  # Calculates the pixel difference between original and template images
        # subtracts black pixels as in these pictures they can be either black and white

        b, g, r = cv2.split(difference)  # split an image into three different intensity arrays for each color channel (b g r)

        # print(cv2.countNonZero(b)) #the difference in blue channel

        #cv2.imshow("subtracted images", difference)

        # countNonZero - counts the empty spots in the array of pixels (determines white pixels)
        # less white pixels means pictures are more likely to be equal
        return cv2.countNonZero(b)

    print("Error: wrong image given to template match")


def determineNumber(numberImage, isFaceCard):
#Finds which of the four letters the card is based on amount of pixels that don't match

    templateA = cv2.imread("../Images/Templates/A.png")
    templateK = cv2.imread("../Images/Templates/K.png")
    templateQ = cv2.imread("../Images/Templates/Q.png")
    templateJ = cv2.imread("../Images/Templates/J.png")
    number = "CARD NUMBER NOT FOUND "
    negativeProbability = 999999
    if not isFaceCard:
        if (templateMatch(numberImage, templateA) < negativeProbability):
            negativeProbability  = templateMatch(numberImage, templateA)
            number = "A"
    else:
        if (templateMatch(numberImage, templateK) < negativeProbability):
            negativeProbability = templateMatch(numberImage, templateK)
            number = "K"
        if (templateMatch(numberImage, templateQ) < negativeProbability):
            negativeProbability = templateMatch(numberImage, templateQ)
            number = "Q"
        if (templateMatch(numberImage, templateJ) < negativeProbability):
            negativeProbability = templateMatch(numberImage, templateJ)
            number = "J"

    return number

def prepareImageForTemplateMatching(suitImage, numberImage):
#prepares images for template matching and suit analysis by rotating and cropping them

    images = []
    newImages = []
    #cv2.imshow("Suit image", suitImage)
    #cv2.imshow("Number image", numberImage)

    #rotate nubmer image
    TM = cv2.getRotationMatrix2D((numberImage.shape[0] / 2, numberImage.shape[1] / 2), -90, 1)
    rotated = cv2.warpAffine(numberImage, TM, (numberImage.shape[0] * 2, numberImage.shape[1] * 2))

    images.append(rotated)

    # rotate suit image
    TM = cv2.getRotationMatrix2D((suitImage.shape[0] / 2, suitImage.shape[1] / 2), -90, 1.0)
    rotated = cv2.warpAffine(suitImage, TM, (suitImage.shape[1], suitImage.shape[1]))

    images.append(rotated)

    #Crop both images
    for j in range(len(images)):
        grayScale = cv2.cvtColor(images[j], cv2.COLOR_BGR2GRAY)

        c = cv2.findContours(grayScale.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        c = imutils.grab_contours(c)

        #print("This should be 1: " + str(len(c)))
        for i in range(len(c)):
            perimeter = cv2.arcLength(c[i], True)
            if perimeter > 30 and perimeter < 500:      #These are important to avoid holes in letters (A, Q)
                extLeft = tuple(c[i][c[i][:, :, 0].argmin()][0])
                extRight = tuple(c[i][c[i][:, :, 0].argmax()][0])
                extTop = tuple(c[i][c[i][:, :, 1].argmin()][0])
                extBot = tuple(c[i][c[i][:, :, 1].argmax()][0])

                # Used to flatted the array containing the co-ordinates of the vertices.
                TM = np.float32([[1, 0, -extLeft[0]], [0, 1, -extTop[1]]])
                imgT = cv2.warpAffine(images[j], TM, ((extRight[0] - extLeft[0]), (extBot[1] - extTop[1])))

                #cv2.imshow("Single card pls" + str(i), imgT)
                newImages.append(imgT)
                #cv2.imshow("Image: " + str(j) + " " + str(i) ,imgT)


    #We return the bigger image first
    return findTwoBiggestImages(newImages)

