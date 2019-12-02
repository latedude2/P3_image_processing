import cv2
import imutils
import numpy as np
from ImageSplit import *


def templateMatch(original, template):
# returns how many pixels don't match

    width = int(template.shape[1])
    height = int(template.shape[0])
    dim = (width, height)
    # resize image
    original = cv2.resize(original, dim, interpolation=cv2.INTER_AREA)

    cv2.imshow("Original", original)
    # cv2.imshow("Template", template)

    if original.shape == template.shape:  # checks if the size and amount of channels in the images match. Optional.
        difference = cv2.subtract(original, template)  # Calculates the pixel difference between original and template images
        # subtracts black pixels as in these pictures they can be either black and white

        b, g, r = cv2.split(difference)  # split an image into three different intensity arrays for each color channel (b g r)

        # print(cv2.countNonZero(b)) #the difference in blue channel

        cv2.imshow("subtracted images", difference)

        # countNonZero - counts the empty spots in the array of pixels (determines white pixels)
        # less white pixels means pictures are more likely to be equal
        return cv2.countNonZero(b)

    print("Error: wrong image given to template match")


def determineNumber(numberImage, isFaceCard):
    # Finds which of the four letters the card is based on amount of pixels that don't match

    widthTopLeft = int(numberImage.shape[0] / 3)
    heightTopLeft = int(numberImage.shape[1] / 3)
    topLeftPart = numberImage[0:heightTopLeft, 0:widthTopLeft]

    cv2.imshow("TOP LEFT PART", topLeftPart)

    templateK = cv2.imread("../Images/Templates/K.png")
    templateQ = cv2.imread("../Images/Templates/Q.png")
    templateJ = cv2.imread("../Images/Templates/J.png")
    number = "CARD NUMBER NOT FOUND "

    negativeProbabilityking = templateMatch(numberImage, templateK)

    if cv2.inRange(topLeftPart, (200, 200, 200), (255, 255, 255)).any():
        print("it's probably not a fckn jack")
        negativeProbabilityjack = templateMatch(numberImage, templateJ)
    else:
        negativeProbabilityjack = 40
        #negativeProbabilityjack = templateMatch(numberImage, templateJ)

    negativeProbabilityqueen = templateMatch(numberImage, templateQ)

    print("KING NEGATIVE")
    print(negativeProbabilityking)
    print("QUEEN NEGATIVE")
    print(negativeProbabilityqueen)
    print("JACK NEGATIVE")
    print(negativeProbabilityjack)

    if (negativeProbabilityking < negativeProbabilityqueen and negativeProbabilityking < negativeProbabilityjack):
        number = "K"
    elif(negativeProbabilityqueen < negativeProbabilityjack):
        number = "Q"
    else:
        number = "J"

    return number

def determineNumberasd(numberImage, isFaceCard):
    card = ""

    original_resized = numberImage  # captured image, got from the camera
    original = cv2.resize(original_resized, (75, 110))

    all_templates = []  # array to store template images
    card_name = ["A", "J", "K", "Q"]

    for i in glob.glob("../Images/Templates/*"):  # Return a list of path names in the templates folder
        template_img = cv2.imread(i)
        all_templates.append(template_img)

    for template, card_name in zip(all_templates, card_name):  # zip allows to work with more than 1 array/list at a time

        image1 = original.shape  # gives information about size and channels of the images (3 for b g r). Optional.
        image2 = template.shape

        print(image1)
        print(image2)

        if original.shape == template.shape:  # checks if the size and amount of channels in the images match. Might not be needed
            print("same size and channels")

            difference = cv2.subtract(original,
                                      template)  # Calculates the pixel difference between original and template images
            # subtracts black pixels as in these pictures they can be either black and white

            b, g, r = cv2.split(
                difference)  # split an image into three different intensity arrays for each color channel (b g r)

            print(cv2.countNonZero(b))  # the difference in blue channel

            # countNonZero - counts the empty spots in the array of pixels (determines white pixels)
            # less white pixels means pictures are more likely to be equal

            whitePixelThreshold = 200000

            if cv2.countNonZero(b) <= whitePixelThreshold:  # only needs info from one channel, the images are binary
                print("equal")
                print("Matching card " + card_name)
                card = card_name
                break

            else:
                print("not equal")

    # do something with detected images
    if card == "A":
        print("Ace")

    elif card == "J":
        print("Jack")

    elif card == "K":
        print("King")

    else:
        print("Queen")


    cv2.imshow("Original", original)
    cv2.imshow("Template", template)
    cv2.imshow("Subtracted image", difference)
    return card

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
        #print("find max contour")
        # find the biggest area
        c = max(c, key=cv2.contourArea)

        extLeft = tuple(c[c[:, :, 0].argmin()][0])
        extRight = tuple(c[c[:, :, 0].argmax()][0])
        extTop = tuple(c[c[:, :, 1].argmin()][0])
        extBot = tuple(c[c[:, :, 1].argmax()][0])

        # Used to flatted the array containing the co-ordinates of the vertices.
        TM = np.float32([[1, 0, -extLeft[0]], [0, 1, -extTop[1]]])
        imgT = cv2.warpAffine(images[j], TM, ((extRight[0] - extLeft[0]), (extBot[1] - extTop[1])))

        #cv2.imshow("Single card pls" + str(j), imgT)
        newImages.append(imgT)
        #cv2.imshow("Image: " + str(j) + " " + str(i) ,imgT)

    #We return the bigger image first
    return findTwoBiggestImages(newImages)

