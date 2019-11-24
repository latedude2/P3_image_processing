import cv2
import numpy as np
# HSV margins for the color detection
red_lowpart = low_low_red, up_low_red = [(0, 40, 122), (25, 255, 255)]
red_uppart = low_up_red, up_up_red = [(170, 40, 122), (180, 255, 255)]
black = low_black, up_black = [(0, 0, 0), (180, 255, 56)]

def checkRed(original, greyImage):
    # original - coloured image of the suit
    # greyImage - greyScale image of the suit
    (thresh, threshold) = cv2.threshold(greyImage, 127, 255, cv2.THRESH_BINARY)
    # reduce noise
    median = cv2.medianBlur(threshold, 5)

    # making an object to hold parameters of the blob detection
    params = cv2.SimpleBlobDetector_Params()

    # define parameters for the blob detector
    params.filterByArea = True # allows using area paramater

    # these parameters are dependant on image size
    params.minArea = 150 # min and max areas of pixels for 1 blob
    params.maxArea = 10000

    params.filterByCircularity = False # to not care about circularity (more circular = bigger angles)
    params.filterByColor = False # to not care about the color
    params.filterByConvexity = False # to not care about convexity (idk actually how to explain it)
    params.filterByInertia = False # doesn't care how much like a circle it is (difference in radiusw)

    detector = cv2.SimpleBlobDetector_create(params) #making the detector by the parameters set before
    keypoints = detector.detect(median) #detecting the blobs

    x = int(keypoints[0].pt[0]) #keypoints[which blob].pt[x(0) or y(1)]
    y = int(keypoints[0].pt[1])
    #print(x)
    #print(y)

    hsv_image = cv2.cvtColor(original, cv2.COLOR_BGR2HSV) #convert the original image to HSV to check for the colours
    colour = hsv_image[y, x]
    #print(colour)

    return checkColour(colour)

    #Debugging - shows where the blobs are
    '''
    im_with_keypoints = cv2.drawKeypoints(median, keypoints, np.array([]), (0, 0, 255),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow("keypoints", im_with_keypoints)
    '''


def checkColour(colour):
    # make lower and upper colour value to identify red
    low = np.array(low_low_red, dtype="uint8")
    up = np.array(up_low_red, dtype="uint8")

    #print(colour)

    # this function scans through the image and finds the defined colour
    # all this line needed because of HSV (need to consider each part separately)
    if ((colour[0] > low[0] and colour[0] < up[0]) and ((colour[1] > low[1] and colour[1] < up[1]) or (colour[2] > low[2] and colour[2] < up[2]))):
        #print("it's a red card")
        return True
    else:
        # do the same with yellow colour
        low = np.array(low_up_red, dtype="uint8")
        up = np.array(up_up_red, dtype="uint8")

        if ((colour[0] > low[0] and colour[0] < up[0]) and ((colour[1] > low[1] and colour[1] < up[1]) or (colour[2] > low[2] and colour[2] < up[2]))):
            #print("it's a red card")
            return True
        else:
            low = np.array(low_black, dtype="uint8")
            up = np.array(up_black, dtype="uint8")

            # all() takes all the elements in an array
            if (all(colour > low) and all(colour < up)):
                #print("it's a black card")
                return False
            else:
                # if non of those colours are found it means that it's not a face card
                #print("Color detection failed, assuming car")
                return False