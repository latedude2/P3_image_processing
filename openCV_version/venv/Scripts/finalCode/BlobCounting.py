import cv2
import numpy as np

def countBlobs(original, isRed):
# returns the amount of red or black blobs in the image
# original - colored image of the card
# isRed - Is the card that is being analysed red

    median = cv2.medianBlur(original, 5)

    # making an object to hold parameters of the blob detection
    params = cv2.SimpleBlobDetector_Params()

    # define parameters for the blob detector
    params.filterByArea = True  # allows using area parameter

    # these parameters are dependant on image size
    params.minArea = 1000  # min and max areas of pixels for 1 blob
    params.maxArea = 100000

    params.filterByColor = True  # care about the color
    params.filterByCircularity = False  # to not care about circularity (more circular = bigger angles)
    params.filterByConvexity = False  # to not care about convexity
    params.filterByInertia = False  # doesn't care how much like a circle it is (difference in radius)

    if isRed:
        ## convert to hsv
        hsv = cv2.cvtColor(median, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, (0, 150, 25), (20, 255, 255))
        mask = mask | cv2.inRange(hsv, (170, 150, 25), (180, 255, 255))

        ## slice the red
        imask = mask > 0
        red = np.zeros_like(original, np.uint8)
        red[imask] = original[imask]

        usedThresh, threshImg = cv2.threshold(red, 0, 255, cv2.THRESH_BINARY)

        params.blobColor = 255

        detector = cv2.SimpleBlobDetector_create(params)  # making the detector by the parameters set before
        keypoints = detector.detect(threshImg)  # detecting the blobs

        blobCount = len(keypoints)

    else:

        usedThresh, threshImg = cv2.threshold(original, 100, 255, cv2.THRESH_BINARY_INV)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

        closedImg = cv2.morphologyEx(threshImg, cv2.MORPH_CLOSE, kernel)

        params.blobColor = 255

        detector = cv2.SimpleBlobDetector_create(params)  # making the detector by the parameters set before
        keypoints = detector.detect(closedImg)  # detecting the blobs
        blobCount = len(keypoints)

    if(blobCount == 10):
        return "T"

    return str(blobCount)