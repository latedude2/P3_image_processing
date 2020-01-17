import cv2
import numpy as np
# HSV margins for the color detection
red_lowpart = low_low_red, up_low_red = [(0, 135, 100), (25, 255, 255)]
red_uppart = low_up_red, up_up_red = [(170, 135, 100), (180, 255, 255)]
black = low_black, up_black = [(0, 0, 0), (180, 255, 56)]

def checkRed(original):
    # Returns true if image has red BLOBs

    median = cv2.medianBlur(original, 5)

    # making an object to hold parameters of the blob detection
    params = cv2.SimpleBlobDetector_Params()

    # define parameters for the blob detector
    params.filterByArea = True  # allows using area paramater

    # these parameters are dependant on image size
    params.minArea = 150  # min and max areas of pixels for 1 blob
    params.maxArea = 10000

    params.filterByColor = True  # care about the color
    params.filterByCircularity = False  # to not care about circularity (more circular = bigger angles)
    params.filterByConvexity = False  # to not care about convexity
    params.filterByInertia = False  # doesn't care how much like a circle it is (difference in radiusw)

    ## convert to hsv
    hsv = cv2.cvtColor(median, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, (0, 135, 100), (20, 255, 255))
    mask = mask | cv2.inRange(hsv, (170, 135, 100), (180, 255, 255))

    ## slice the red
    imask = mask > 0
    red = np.zeros_like(original, np.uint8)
    red[imask] = original[imask]

    usedThresh, threshImg = cv2.threshold(red, 0, 255, cv2.THRESH_BINARY)
    params.blobColor = 255

    detector = cv2.SimpleBlobDetector_create(params)  # making the detector by the parameters set before
    keypoints = detector.detect(threshImg)  # detecting the blobs

    blobCount = len(keypoints)

    if(blobCount > 0):
        return True
    else:
        return False
