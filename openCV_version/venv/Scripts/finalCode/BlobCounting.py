import cv2
import numpy as np

def countBlobs(original, isRed):
    blobCount = 0

    median = cv2.medianBlur(original, 5)

    # making an object to hold parameters of the blob detection
    params = cv2.SimpleBlobDetector_Params()

    # define parameters for the blob detector
    params.filterByArea = True  # allows using area paramater

    # these parameters are dependant on image size
    params.minArea = 500  # min and max areas of pixels for 1 blob
    params.maxArea = 10000

    params.filterByColor = True  # care about the color
    params.filterByCircularity = False  # to not care about circularity (more circular = bigger angles)
    params.filterByConvexity = False  # to not care about convexity
    params.filterByInertia = False  # doesn't care how much like a circle it is (difference in radiusw)

    if isRed:
        ## convert to hsv
        hsv = cv2.cvtColor(median, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, (0, 100, 25), (20, 255, 255))
        mask = mask | cv2.inRange(hsv, (170, 100, 25), (180, 255, 255))

        ## slice the red
        imask = mask > 0
        red = np.zeros_like(original, np.uint8)
        red[imask] = original[imask]

        memes, threshImg = cv2.threshold(red, 0, 255, cv2.THRESH_BINARY)

        grayScale = cv2.cvtColor(threshImg, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("Red color: ",threshImg)
        params.blobColor = 255

        detector = cv2.SimpleBlobDetector_create(params)  # making the detector by the parameters set before
        keypoints = detector.detect(threshImg)  # detecting the blobs

        im_with_keypoints = cv2.drawKeypoints(threshImg, keypoints, np.array([]), (0, 0, 255),
                                              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        cv2.imshow("Detected red  Blobs: ", im_with_keypoints)

        blobCount = len(keypoints)

    else:
        memes, threshImg = cv2.threshold(original, 100, 255, cv2.THRESH_BINARY_INV)

        grayScale = cv2.cvtColor(threshImg, cv2.COLOR_BGR2GRAY)
        params.blobColor = 255

        detector = cv2.SimpleBlobDetector_create(params)  # making the detector by the parameters set before
        keypoints = detector.detect(threshImg)  # detecting the blobs

        im_with_keypoints = cv2.drawKeypoints(threshImg, keypoints, np.array([]), (0, 0, 255),
                                              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        cv2.imshow("Detected black Blobs: ", im_with_keypoints)

        blobCount = len(keypoints)

    print(blobCount)

    return str(blobCount)