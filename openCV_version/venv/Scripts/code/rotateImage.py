from imutils import perspective
from imutils import contours
import cv2
import numpy as np 
import imutils

def cardOnSide():

    source = "../Images\\8_of_clubs.png"

    img = cv2.imread(source)
    rotated = cardRotation(img)
    cropped = cardCropped(rotated)

    cv2.imshow('Rotated', rotated)
    cv2.imshow('Cropped', cropped)
    cv2.waitKey(0)
    cv2.destroyAllWindows

#Finds the angle of the card using Hough traslation algorithm.
def cardRotation(img):
    angles = [] # List of the angles of the lines
    threshold = 5 # Threshold to know which lines are closed to eachothers
    tempThresholdAngles = [] # List to temporary hold threshholded angles
    thresholdAngles = [] # List of threshhold angles

    h, w = img.shape[:2] # Width and Hight of the image
    x = h/2 # X coordinates of the center of the image
    y = w/2 # Y coordinates of the center of the image

    #making the pictire gray, applying a blur and thresholding it before finding the edges
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img,(3,3),cv2.BORDER_DEFAULT)
    retval, thresh = cv2.threshold(blur,0.66*blur.max(),255,cv2.THRESH_BINARY_INV)
    edge = cv2.Canny(thresh,retval, retval)

    #finding hough line transformation lines
    lines = cv2.HoughLines(edge, 1, np.pi/180, 120, 30, 20)

    # Fiding the angle of lines and adding them to the angles array
    for line in lines:
        rho,theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        angle = np.rad2deg(np.arctan2(y2 - y1,x2 - x1))
        angles.append(angle)

    #sorting the array of angles
    angles.sort()

    #finding the highest angle. The angle doesnt matter as long as it is a high angle we turn it according
    #to the horizontal line of the picture, because we correct the rotation later on in the cropping.
    avAng = angles[-1]

    #Creating a rotation matrix
    Matrix = cv2.getRotationMatrix2D((x,y),avAng,1.0)

    #rotating the picture
    rotated = cv2.warpAffine(img, Matrix, (w*2, h*2))


    return rotated

#cropping the picture based on the edges
def cardCropped(rotated):

    contourX = [] #list of x coordinates of the contours
    contourY = [] #list of y coordinates of the contours

    #making the pictire gray, applying a blur and thresholding it before finding the edges
    gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(rotated,(23,23),0)
    retval, thresh = cv2.threshold(blur,0.6*blur.max(),255,cv2.THRESH_BINARY)
    edge = cv2.Canny(thresh,retval, retval)

    #finding the countours based on the edges
    contours, hierchy= cv2.findContours(edge,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        #Get an approximation of the contours
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)   
        # making the array into a one dimentional array 
        # ([x1,y1],[x2,y2]) into (x1,y1,x2,y2) 
        n = approx.ravel()  
        i = 0

        #looping through the list to find the x and y
        for j in n : 
            if(i % 2 == 0): 
                contourX.append(n[i])   #adding x
                contourY.append(n[i + 1])   #adding y
            i = i + 1

    #sorting the contour coodinationsfrom lowest to highest
    contourX.sort()
    contourY.sort()
    
    #making a matrix to move the pictures based on the lowest x and y
    TM = np.float32([ [1 , 0 , -contourX[0]], [0 , 1 , -contourY[0]] ])
    #cropping the image
    cropped = cv2.warpAffine(rotated, TM, ((contourX[-1] - contourX[0]),(contourY[-1] - contourY[0])))

    #finding the width and hight of the image
    hightCropped, widthCropped = cropped.shape[:2]
    xr = hightCropped/2    # x coordinates of the center of the image
    yr = widthCropped/2    # y coordinates of the center of the image

    #making sure if the piture is rotated vertically to rotate it horizontally

    if hightCropped < widthCropped:
        croppedRotated = cropped
    elif hightCropped > widthCropped:
        croppedRotated = None
        M = cv2.getRotationMatrix2D((xr,yr), 90, 1.0) # rotating 90 degrees if the picture is vertical
        croppedRotated = cv2.warpAffine(cropped, M, (widthCropped,hightCropped)) # switching the w and h after rotation

    return croppedRotated


if __name__ == '__main__':
    cardOnSide()
