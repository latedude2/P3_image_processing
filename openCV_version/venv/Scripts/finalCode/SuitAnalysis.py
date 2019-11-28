import cv2
import numpy as np

# takes a binary image with a single BLOB and checks which suit the BLOB matches
def determineSuit(blur, isRed):
    # Get dimensions of the image
    Matrix = cv2.getRotationMatrix2D((0, 0), 0, 5.0)
    blur = cv2.warpAffine(blur, Matrix, (blur.shape[1] * 5, blur.shape[0] * 5))

    memes, blur = cv2.threshold(blur, 70, 255, cv2.THRESH_BINARY_INV)

    #cv2.imshow("Scaled suit", blur)

    width = blur.shape[1]
    height = blur.shape[0]

    # can be changed depending on what is nescessary for a clear image
    '''
    blurmed = cv2.medianBlur(img, 9)
    blur = cv2.blur(blurmed, (3,3))
    '''

    # thresholding to discern which pixels are white, when finding the center of mass for the white pixels
    ret, thresh = cv2.threshold(blur, 200, 200, 200)

    # Finding the points where the shape outline changes direction, by making an outline of vectors
    contours, hierarchy = cv2.findContours(blur, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # saving the positions of the white pixels fom the thresholding
    M = cv2.moments(thresh)

    # finding the coordinates for the center of mass for the white pixels
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    center = (cx, cy)

    # new image for displaying the contour and lines to close points
    outImg = np.zeros_like(blur)
    lengths = []  # array for the distances between the center and each point in the contour
    points = []  # array for coordinates for each point in the contour

    # contours is a tripple array containing a list of vectors, 2d arrays.
    for i in range(len(contours[0])):
        # finding the x and y for each point between the different vectors
        # meaning that we only get lengths for where the figure is changing from a straight line
        x = contours[0][i][0][0]
        y = contours[0][i][0][1]

        # only taking the points in the first quarter of the shape, by comparing to the center coordinates
        if(x <= cx and y <= cy):
            # saving the points coordinate
            pointToAppend = (x,y)
            points.append(pointToAppend)

            # saving the distance from the center to this point
            dist = np.sqrt((x-cx)**2 + (y-cy)**2)
            lengths.append(dist)


    lowest = min(lengths)  # finding the distance to the saved point closest to the center
    average = sum(lengths)/len(lengths)  # finding the average distance from the saved points to the center

    # the numbers used here can be changed to calibrate for better results during technical test, since they were found by trial and error
    lowMarg = lowest * 1.1  # setting a margin for when a point is considered close, from the shortest distance
    threshold = .3  # threshold for how big a percentage of the total saved points should be close for it to be one suit or the other

    lowPos = []  # for saving the array positions for the distances that are close enough to the center to be counted

    # Collecting the array positions of the points closer to the center
    for i in range(len(lengths)):
        if (lengths[i] <= lowMarg):
            lowPos.append(i)

    #print(len(lowPos))
    #print(len(points))

    # Differentiating here will also include color to complete the split of the 4 suits
    # Checking if more points than the threshold percentage are considered close to the center
    if (len(lowPos) >= len(points) * threshold):  # Spade and diamond give many close points, since the closest is similar to all other points
        #print("spade or diamond")
        if(isRed):
            return "D"
        else:
            return "S"
    elif (len(lowPos) < len(points) * threshold):  # heart and club give few close points, since the closest is an outlier from the other points
        #print("heart or club")
        if (isRed):
            return "H"
        else:
            return "C"

    '''
    #debugging
    # drawing the contour on the image
    cv2.drawContours(outImg, contours, -1, 255, 1)

    # drawing lines to the close points
    for i in range(len(lowPos)):
        cv2.line(outImg,center, points[lowPos[i]], 100, 1)

    # drawing a clearer line to the cosest point
    cv2.line(outImg, center, points[lengths.index(lowest)], 200, 2)

    return outImg
    
    '''