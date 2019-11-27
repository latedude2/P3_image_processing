import numpy as np
import cv2

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

    mask = cv2.inRange(hsv, (16, 150, 100), (30, 255, 255)) #Look for colour only existing in face cards

    ## slice the yellow
    imask = mask > 0
    yellow = np.zeros_like(image, np.uint8)
    yellow[imask] = image[imask]

    memes, threshImg = cv2.threshold(yellow, 0, 255, cv2.THRESH_BINARY)

    cv2.imshow("Yellow color: ",threshImg)
    params.blobColor = 255

    detector = cv2.SimpleBlobDetector_create(params)  # making the detector by the parameters set before
    keypoints = detector.detect(threshImg)  # detecting the blobs

    im_with_keypoints = cv2.drawKeypoints(threshImg, keypoints, np.array([]), (0, 0, 255),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    #cv2.imshow("Detected blue: ", im_with_keypoints)
    blobCount = len(keypoints)

    if(blobCount > 0):
        return True
    else:
        return False