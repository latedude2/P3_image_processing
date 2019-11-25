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
from BlobCounting import *

def main():
    video_capture = cv2.VideoCapture('http://192.168.43.117:4747/mjpegfeed')
    print("Connected to camera")

    foundCards = []

    frameCount = 0
    frameSkip = 10 #how many frames from camera we skip

    #Main loop
    while True:
        ret, frame = video_capture.read()
        frameCount = frameCount + 1
        if(frameCount % frameSkip == 0):
            cv2.imshow("Camera footage", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Separate cards into separate images
            images = splitIntoCardImages(frame)
            detectedCards = []
            cardCount = 0

            #for each card looking object
            for i in range(len(images)):
                if(images[i].shape[0] > 200 and images[i].shape[1] > 150):  #This has to be set based on card size on the screen (in pixels)
                    cardCount = cardCount + 1
                    #print("Card " + str(i))
                    #cv2.imshow("Card" + str(i), images[i])

                    cv2.imshow("Card" + str(i), images[i])
                    detectedCard = analyseCard(images[i])
                    if (detectedCard != "Error"):
                        detectedCards.append(detectedCard)

            for i in range(len(detectedCards)):
                foundCards.append(detectedCards[i])

            #Remove empty cards (" ")
            foundLength = len(foundCards)
            j = 0
            while (j < foundLength):
                if (foundCards[j] == " "):
                    foundCards.pop(j)
                    # as an element is removed
                    # so decrease the length by 1
                    foundLength = foundLength - 1
                    # run loop again to check element
                    # at same index, when item removed
                    # next item will shift to the left
                    continue
                j = j + 1

            while(len(foundCards) > 30): #remove old cards, we only need recently detected cards
                foundCards.pop(1)

            print(findMostCommonCards(cardCount, foundCards))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
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
    #cv2.imshow("Rotated image " + stringAdd, rotated)


    rotatedCardImage = cardCropped(rotated)
    #cv2.imshow("Cropped image " +  stringAdd, rotatedCardImage)

    TM = np.float32([[1, 0, 0], [0, 1, - rotatedCardImage.shape[0] / 6 * 4.8]])
    corner = cv2.warpAffine(rotatedCardImage, TM,
                            (int(rotatedCardImage.shape[1] / 3.5), int(rotatedCardImage.shape[0] / 5.5)))   #Size of corner image

    cv2.imshow("Corner image " +  stringAdd, corner)

    isRed = checkRed(corner)

    suitImage, numberImage = splitCornerToSuitAndNumber(corner, isRed)

    suitImage, numberImage = prepareImageForTemplateMatching(suitImage, numberImage)

    #cv2.imshow("Suit image " + stringAdd, suitImage)
    #cv2.imshow("Number image " + stringAdd, numberImage)

    border = 5
    suitImage = cv2.copyMakeBorder(suitImage, border, border, border, border, cv2.BORDER_CONSTANT,
                                   value=[0, 0, 0])

    suitImage = cv2.cvtColor(suitImage, cv2.COLOR_BGR2GRAY)
    blurredSuit = cv2.GaussianBlur(suitImage, (5, 5), 0)
    cardSuit = determineSuit(blurredSuit, checkRed(corner))

    if(find_face_card(rotated)):
        print("Found face")
        cardNumber = determineNumber(numberImage, True)
    else:
        cardNumber = countBlobs(rotated, isRed)

    if cardNumber == "1":
        cardNumber = "A"

    return cardNumber + cardSuit

def findMostCommonCards(cardCount, foundCards):
    # Create new list for finding most common cards
    tempFoundCards = []
    for i in range(len(foundCards)):
        tempFoundCards.append(foundCards[i])

    tableCards = []
    for k in range(cardCount):
        mostCommonNow = mostFrequent(tempFoundCards)
        tableCards.append(mostCommonNow)
        length = len(tempFoundCards)
        i = 0
        while (i < length):
            if (tempFoundCards[i] == mostCommonNow):
                tempFoundCards.remove(tempFoundCards[i])
                length = length - 1 #because element was removed
                continue #we don't iterate as an element was taken away
            i = i + 1

    tableString = "Final Cards: "
    for i in range(len(tableCards)):
        tableString += " "
        tableString += tableCards[i]

    return tableString

def mostFrequent(List):
    if(len(List) > 0):
        counter = 0
        card = List[0]

        for i in List:
            curr_frequency = List.count(i)
            if (curr_frequency > counter):
                counter = curr_frequency
                card = i

        return card

    return ""


if __name__ == "__main__" :
    main()