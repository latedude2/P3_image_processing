from imutils import perspective
from imutils import contours
import cv2
import numpy as np
import statistics
import math
import imutils


def cardOnSide():
#Testing function

    source = "../Images/testImage10.jpg"

    img = cv2.imread(source)
    rotated = cardRotation(img)
    cropped = cardCropped(rotated)

    #cv2.imshow('Rotated', rotated)
    #cv2.imshow('Cropped', cropped)

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return
    cv2.waitKey(0)
    cv2.destroyAllWindows


# Finds the angle of the card using Hough traslation algorithm.
def cardRotation(img):
    angles = []  # List of the angles of the lines
    threshold = 5  # Threshold to know which lines are closed to eachothers
    tempThresholdAngles = []  # List to temporary hold threshholded angles
    thresholdAngles = []  # List of threshhold angles

    h, w = img.shape[:2]  # Width and Hight of the image
    x = h / 2  # X coordinates of the center of the image
    y = w / 2  # Y coordinates of the center of the image

    # making the pictire gray, applying a blur and thresholding it before finding the edges
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img, (3, 3), cv2.BORDER_DEFAULT)
    retval, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)

    #cv2.imshow("Thresh", thresh)

    edge = cv2.Canny(thresh, retval, retval)

    #cv2.imshow("Canny", edge)

    # finding hough line transformation lines
    lines = cv2.HoughLines(edge, 1, np.pi / 180, 120, 30, 20)

    # Fiding the angle of lines and adding them to the angles array
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        angle = np.rad2deg(np.arctan2(y2 - y1, x2 - x1))
        angles.append(angle)

    # sorting the array of angles
    angles.sort()

    # finding the highest angle. The angle doesnt matter as long as it is a high angle we turn it according
    # to the horizontal line of the picture, because we correct the rotation later on in the cropping.
    avAng = angles[-1]

    # Creating a rotation matrix
    Matrix = cv2.getRotationMatrix2D((x, y), avAng, 1.0)

    # rotating the picture
    rotated = cv2.warpAffine(img, Matrix, (w * 2, h * 2))

    return rotated

# cropping the picture based on the edges
def cardCropped(rotated):

    contourX = []  # list of x coordinates of the contours
    contourY = []  # list of y coordinates of the contours

    #cv2.imshow("Crop thresh", thresh)

    ## convert to hsv
    hsv = cv2.cvtColor(rotated, cv2.COLOR_BGR2HSV)
    #This code seems to break finding of suit and number.
    ## mask of green (36,25,25) ~ (86, 255,255)
    mask = cv2.inRange(hsv, (36, 25, 25), (70, 255, 255))

    ## slice the green, we don't want the background be kept in the image, but it should not exist in contour finding
    imask = mask > 0
    green = np.zeros_like(rotated, np.uint8)
    green[imask] = rotated[imask]
    rotatedNoGreen = rotated - green

    gray = cv2.cvtColor(rotatedNoGreen, cv2.COLOR_BGR2GRAY)

    memes, threshImg = cv2.threshold(gray, 5, 255, cv2.THRESH_BINARY)

    # finding the countours based on the edges
    c, hierchy = cv2.findContours(threshImg, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(len(c)):
        perimeter = cv2.arcLength(c[i], True)
        if perimeter > 500:
            extLeft = tuple(c[i][c[i][:, :, 0].argmin()][0])
            extRight = tuple(c[i][c[i][:, :, 0].argmax()][0])
            extTop = tuple(c[i][c[i][:, :, 1].argmin()][0])
            extBot = tuple(c[i][c[i][:, :, 1].argmax()][0])

            # Used to flatted the array containing the co-ordinates of the vertices.

            TM = np.float32([[1, 0, -extLeft[0]], [0, 1, -extTop[1]]])
            imgT = cv2.warpAffine(rotated, TM, ((extRight[0] - extLeft[0]), (extBot[1] - extTop[1])))


            return imgT

    #This part of code should not be reached
    print("Card rotation: This part of code should not be reached")

    for cnt in contours:
        perimeter = cv2.arcLength(cnt, True)
        if perimeter > 500:
            # Get an approximation of the contours
            approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
            # making the array into a one dimentional array
            # ([x1,y1],[x2,y2]) into (x1,y1,x2,y2)
            n = approx.ravel()
            i = 0

            # looping through the list to find the x and y
            for j in n:
                if (i % 2 == 0):
                    contourX.append(n[i])  # adding x
                    contourY.append(n[i + 1])  # adding y
                i = i + 1

    # sorting the contour coodinationsfrom lowest to highest
    contourX.sort()
    contourY.sort()

    # making a matrix to move the pictures based on the lowest x and y
    TM = np.float32([[1, 0, -contourX[0]], [0, 1, -contourY[0]]])
    # cropping the image
    cropped = cv2.warpAffine(rotated, TM, ((contourX[-1] - contourX[0]), (contourY[-1] - contourY[0])))

    # finding the width and hight of the image
    hightCropped, widthCropped = cropped.shape[:2]
    xr = hightCropped / 2  # x coordinates of the center of the image
    yr = widthCropped / 2  # y coordinates of the center of the image

    # making sure if the piture is rotated vertically to rotate it horizontally

    if hightCropped < widthCropped:
        croppedRotated = cropped
    elif hightCropped > widthCropped:
        croppedRotated = None
        M = cv2.getRotationMatrix2D((xr, yr), 90, 1.0)  # rotating 90 degrees if the picture is vertical
        croppedRotated = cv2.warpAffine(cropped, M,
                                        (widthCropped, hightCropped))  # switching the w and h after rotation

    return croppedRotated

def altRotate(img):
#Alternative rotation method

    # read the image
    original = img

    ## convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    ## mask of green (36,25,25) ~ (86, 255,255)
    mask = cv2.inRange(hsv, (36, 25, 25), (70, 255, 255))

    ## slice the green
    imask = mask > 0
    green = np.zeros_like(img, np.uint8)
    green[imask] = img[imask]

    memes, threshImg = cv2.threshold(green, 0, 255, cv2.THRESH_BINARY_INV)

    greyScale = cv2.cvtColor(threshImg, cv2.COLOR_BGR2GRAY)

    greyScale = cv2.GaussianBlur(greyScale, (9, 9), 0)

    c = cv2.findContours(greyScale.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    c = imutils.grab_contours(c)

    cv2.drawContours(greyScale, c, -1, 127, 3)

    angle = 0

    for i in range(len(c)):
        perimeter = cv2.arcLength(c[i], True)
        if perimeter > 200:
            extLeft = tuple(c[i][c[i][:, :, 0].argmin()][0])
            extRight = tuple(c[i][c[i][:, :, 0].argmax()][0])
            extTop = tuple(c[i][c[i][:, :, 1].argmin()][0])
            extBot = tuple(c[i][c[i][:, :, 1].argmax()][0])

            finalWidth = 0
            finalLength = 0

            if extLeft[1] > img.shape[0] / 2:
                #print("Rotated right")
                try:
                    if not math.isnan(math.tan(extTop[0] / extLeft[1]) / math.pi * -180):
                        angle = math.tan(extTop[0] / extLeft[1]) / math.pi * -180
                    #print(angle)

                except:
                    print("math fail")

            else:
                #print("Rotated left")
                try:
                    if not math.isnan(math.tan(extLeft[1] / extTop[0]) / math.pi * 180):
                        angle = math.tan(extLeft[1] / extTop[0]) / math.pi * 180
                    #print(angle)
                    finalHeight = math.sqrt((extTop[0] - extLeft[0]) ** 2 + (extTop[1] - extLeft[1]) ** 2)
                    finalWidth = math.sqrt((extTop[0] - extRight[0]) ** 2 + (extTop[1] - extRight[1]) ** 2)
                    #print(finalHeight)
                except:
                    print("math fail")

            #cv2.imshow("Before rotate", original)
            if extLeft[0] - extTop[0] < 70 and extLeft[0] - extTop[0] > -70:
                angle = 0
            #rotated = imutils.rotate_bound(original, angle)

            #Matrix = cv2.getRotationMatrix2D((original.shape[1] / 2, original.shape[0] / 2), -angle - 90, 1.0)
            #rotated = cv2.warpAffine(original, Matrix, (original.shape[1], original.shape[0]))
            #angle = 0 #WE USE THIS IF ROTATION DOES NOT WORK

            #Move to center
            TM = np.float32([[1, 0, original.shape[1] * 0.5], [0, 1, original.shape[0] * 0.5]])
            rotated = cv2.warpAffine(original, TM, (original.shape[1] * 2, original.shape[0] * 2))

            #cv2.imshow("After move", rotated)

            # Creating a rotation matrix
            Matrix = cv2.getRotationMatrix2D((original.shape[1], original.shape[0]), -angle - 90, 1.0)
            rotated = cv2.warpAffine(rotated, Matrix, (rotated.shape[1], rotated.shape[0]))




            #cv2.imshow("After rotate", rotated)

    return rotated


if __name__ == '__main__':
    cardOnSide()