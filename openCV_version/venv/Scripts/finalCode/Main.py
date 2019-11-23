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
    '''
    rotatedCardImage = cv2.imread("../Images/testImage10.jpg")

    TM = np.float32([[1, 0, 0], [0, 1, - rotatedCardImage.shape[0] / 6 * 4.8]])
    corner = cv2.warpAffine(rotatedCardImage, TM,
                            (int(rotatedCardImage.shape[1] / 3.9), int(rotatedCardImage.shape[0] / 5.8)))

    cv2.imshow("Corner image", corner)


    hsvcorner = cv2.cvtColor(corner, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([85, 50, 40])
    upper_blue = np.array([135, 255, 255])

    mask = cv2.inRange(hsvcorner, lower_blue, upper_blue)

    corner[mask > 0] = (255, 255, 255)

    cv2.imshow('Corner no blue', corner)


    gray_corner = cv2.cvtColor(corner, cv2.COLOR_BGR2GRAY)

    isRed = checkRed(corner, gray_corner)

    suitImage, numberImage = splitCornerToSuitAndNumber(corner)

    suitImage, numberImage = prepareImageForTemplateMatching(suitImage, numberImage)

    border = 5
    suitImage = cv2.copyMakeBorder(suitImage, border, border, border, border, cv2.BORDER_CONSTANT, value = [0,0,0])
    cv2.imshow("Suit image", suitImage)
    cv2.imshow("Number image", numberImage)

    suitImage = cv2.cvtColor(suitImage, cv2.COLOR_BGR2GRAY)

    blurredSuit = cv2.GaussianBlur(suitImage, (5, 5), 0)

    cardSuit = determineSuit(blurredSuit, isRed)

    cardNumber = determineNumber(numberImage)

    print("Card suit " + cardSuit + " Card number: " + cardNumber)
    print(cardNumber)

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return
    '''
    video_capture = cv2.VideoCapture('http://192.168.43.117:4747/mjpegfeed')

    print("Connected to camera")

    first_gaussian = backgroundSubtractSetup(video_capture)

    #Main loop
    while True:
        ret, frame = video_capture.read()

        cv2.imshow("Camera footage", frame)
        cards = ""

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gaussian_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

        #Background subtraction to only have cards
        #difference = backgroundSubtract(first_gaussian, gaussian_frame)

        # Separate cards into separate images
        images = splitIntoCardImages(frame)
        detectedCards = []
        #for each card looking object
        for i in range(len(images)):

            if(images[i].shape[0] > 100):
                #print("Card " + str(i))
                #cv2.imshow("Card" + str(i), images[i])
                try:
                    detectedCard = analyseCard(images[i])
                    if(detectedCard != "Error"):
                        detectedCards.append(detectedCard)
                except:
                    if (False):
                        print("False")

        cardString = ""
        for i in range(len(detectedCards)):
            cardString += " "
            cardString += detectedCards[i]
        print(cardString)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


def analyseCard(frame):

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
    rotated = altRotate(frame)
    #cv2.imshow("Rotated image", rotated)

    rotatedCardImage = cardCropped(rotated)
    #cv2.imshow("Cropped image", rotatedCardImage)

    TM = np.float32([[1, 0, 0], [0, 1, - rotatedCardImage.shape[0] / 6 * 4.8]])
    corner = cv2.warpAffine(rotatedCardImage, TM,
                            (int(rotatedCardImage.shape[1] / 3.9), int(rotatedCardImage.shape[0] / 5.8)))

    #cv2.imshow("Corner image", corner)
    gray_corner = cv2.cvtColor(corner, cv2.COLOR_BGR2GRAY)

    isRed = checkRed(corner, gray_corner)

    suitImage, numberImage = splitCornerToSuitAndNumber(corner)

    suitImage, numberImage = prepareImageForTemplateMatching(suitImage, numberImage)

    border = 5
    suitImage = cv2.copyMakeBorder(suitImage, border, border, border, border, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    #cv2.imshow("Suit image", suitImage)
    #cv2.imshow("Number image", numberImage)

    suitImage = cv2.cvtColor(suitImage, cv2.COLOR_BGR2GRAY)
    blurredSuit = cv2.GaussianBlur(suitImage, (5, 5), 0)
    cardSuit = determineSuit(blurredSuit, isRed)

    cardNumber = determineNumber(numberImage)

    #print(cardSuit)
    #print(cardNumber)

    # Detect if face card

    # if not faceCard:
    # Count blobs

    return cardNumber + cardSuit

if __name__ == "__main__" :
    main()

'''
#BROKEN AF
def rotate(img, original):

    grayScale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    grayScale = cv2.GaussianBlur(grayScale, (9, 9), 0)

    c = cv2.findContours(grayScale.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    c = imutils.grab_contours(c)
    angle = 0


    for i in range(len(c)):
        perimeter = cv2.arcLength(c[i], True)
        if perimeter > 200:
            extLeft = tuple(c[i][c[i][:, :, 0].argmin()][0])
            extRight = tuple(c[i][c[i][:, :, 0].argmax()][0])
            extTop = tuple(c[i][c[i][:, :, 1].argmin()][0])
            extBot = tuple(c[i][c[i][:, :, 1].argmax()][0])

            if extLeft[1] > img.shape[0]/2:
                print("Rotated right")
                try:
                    #if not math.isnan(math.tan(extTop[0] / extLeft[1] ) / math.pi * -180):
                    angle = math.tan(extTop[0] / extLeft[1] ) / math.pi * -180
                    print(angle)

                except:
                    print("math fail")

            else:
                print("Rotated left")
                try:
                    #if not  math.isnan(math.tan(extLeft[1]/ extTop[0]) / math.pi * 180):
                    angle = math.tan(extLeft[1]/ extTop[0]) / math.pi * 180
                    print(angle)
                except:
                    print("math fail")
            cv2.imshow("Before rotate", original)
            if extLeft[0] - extTop[0] < 10 and extLeft[0] - extTop[0] > -10:
                angle = 0
            rotated = imutils.rotate_bound(original, angle)
            # TM = np.float32([[1, 0, -extLeft[0]], [0, 1, -extTop[1]]])
            # Matrix = cv2.getRotationMatrix2D((original.shape[1]/2, original.shape[0]/2), -angle, 1.0)
            # rotated = cv2.warpAffine(original, Matrix, (original.shape[1], original.shape[0]))
            cv2.imshow("After rotate", rotated)
            return rotated

'''


