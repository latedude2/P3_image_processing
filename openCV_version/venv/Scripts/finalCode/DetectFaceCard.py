import numpy as np
import cv2

# defining what means colour blue and yellow with lower and upper borders of them in HSV scale
blue = low_blue, up_blue = ([100, 130, 100], [132, 255, 255])
yellow = low_yellow, up_yellow = ([22, 110, 100], [32, 255, 245])

def orig_find_face_card(image):
    # make lower and upper colour value to identify blue
    low = np.array(low_blue, dtype="uint8")
    up = np.array(up_blue, dtype="uint8")

    # this function scans through the image and finds the defined colour
    # .any() returns a boolean True if the colour is found and False if not
    if (cv2.inRange(image, low, up).any()):
        print("it's a face card because blue")
        return True
    else:
        # do the same with yellow colour
        low = np.array(low_yellow, dtype="uint8")
        up = np.array(up_yellow, dtype="uint8")

        if (cv2.inRange(image, low, up).any()):
            print("it's a face card because yellow")
            return True
        else:
            # if non of those colours are found it means that it's not a face card
            print("not a face card")
            return False

def find_face_card(image):
#Returns true if image has yellow BLOBs

    # making an object to hold parameters of the blob detection
    params = cv2.SimpleBlobDetector_Params()

    # define parameters for the blob detector
    params.filterByArea = True  # allows using area parameter

    # these parameters are dependant on image size
    params.minArea = 100  # min and max areas of pixels for 1 blob
    params.maxArea = 10000

    params.filterByColor = True  # to care about the color
    params.filterByCircularity = False  # to not care about circularity (more circular = bigger angles)
    params.filterByConvexity = False  # to not care about convexity
    params.filterByInertia = False  # doesn't care how much like a circle it is (difference in radiusw)

    ## convert to hsv
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, (16, 150, 100), (30, 255, 255))  # Look for colour only existing in face cards

    ## slice the yellow
    imask = mask > 0
    yellow = np.zeros_like(image, np.uint8)
    yellow[imask] = image[imask]

    usedThresh, threshImg = cv2.threshold(yellow, 0, 255, cv2.THRESH_BINARY)

    cv2.imshow("Yellow color: ", threshImg)
    params.blobColor = 255

    detector = cv2.SimpleBlobDetector_create(params)  # making the detector by the parameters set before
    keypoints = detector.detect(threshImg)  # detecting the blobs

    blobCount = len(keypoints)

    if(blobCount > 0):
        return True
    else:
        return False