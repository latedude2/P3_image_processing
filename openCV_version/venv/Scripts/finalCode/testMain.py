#This file is for testing if web cam setup is not available
import cv2
import numpy as np
from ImageSplit import *
from CardEvaluation import *
from BackgroundSubtraction import *
from DetectRed import *
from DetectFaceCard import *
from TemplateMatch import *
from SuitAnalysis import *
from CardRotation import *

def main():
    frame = cv2.imread("../Images/testImage10.jpg")

    cv2.imshow("Camera footage", frame)
    cards = ""

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gaussian_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

    # Separate cards into separate images
    images = splitIntoCardImages(frame)
    detectedCards = []  #Array of detected card strings
    #for each card looking object
    for i in range(len(images)):
        if(images[i].shape[0] > 100):
            #print("Card " + str(i))
            cv2.imshow("Card" + str(i), images[i])
            detectedCard = analyseCard(images[i])
            if(detectedCard != "Error"):
                detectedCards.append(detectedCard)


    cardString = ""
    for i in range(len(detectedCards)):
        cardString += " "
        cardString += detectedCards[i]
    print(cardString)
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


def analyseCard(frame):

    try:
        ## convert to hsv
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        ## mask of green (36,25,25) ~ (86, 255,255)
        mask = cv2.inRange(hsv, (36, 25, 25), (70, 255, 255))

        ## slice the green
        imask = mask > 0
        green = np.zeros_like(frame, np.uint8)
        green[imask] = frame[imask]

        thresh_frame = cv2.threshold(green, 0, 255, cv2.THRESH_BINARY)

        card = ""

        # Rotate cards
        rotated = cardRotation(frame)
        return afterRotation(rotated, "first")
    except: #If an error is thrown, we try a different rotation algorithm
        try:
            rotated = altRotate(frame)
            return afterRotation(rotated, "alternative")

        except:
            return "Error"

def afterRotation(rotated, stringAdd):
    cv2.imshow("Rotated image " + stringAdd, rotated)

    rotatedCardImage = cardCropped(rotated)
    cv2.imshow("Cropped image " +  stringAdd, rotatedCardImage)

    TM = np.float32([[1, 0, 0], [0, 1, - rotatedCardImage.shape[0] / 6 * 4.8]])
    corner = cv2.warpAffine(rotatedCardImage, TM,
                            (int(rotatedCardImage.shape[1] / 3.9), int(rotatedCardImage.shape[0] / 5.8)))

    cv2.imshow("Corner image " +  stringAdd, corner)
    gray_corner = cv2.cvtColor(corner, cv2.COLOR_BGR2GRAY)

    isRed = checkRed(corner, gray_corner)

    suitImage, numberImage = splitCornerToSuitAndNumber(corner)

    cv2.imshow("Suit image " + stringAdd, suitImage)
    cv2.imshow("Number image " + stringAdd, numberImage)

    suitImage, numberImage = prepareImageForTemplateMatching(suitImage, numberImage)

    border = 5
    suitImage = cv2.copyMakeBorder(suitImage, border, border, border, border, cv2.BORDER_CONSTANT,
                                   value=[0, 0, 0])
    # cv2.imshow("Suit image", suitImage)
    # cv2.imshow("Number image", numberImage)

    suitImage = cv2.cvtColor(suitImage, cv2.COLOR_BGR2GRAY)
    blurredSuit = cv2.GaussianBlur(suitImage, (5, 5), 0)
    cardSuit = determineSuit(blurredSuit, isRed)

    cardNumber = determineNumber(numberImage)

    # Detect if face card

    # if not faceCard:
    # Count blobs

    return cardNumber + cardSuit

if __name__ == "__main__" :
    main()