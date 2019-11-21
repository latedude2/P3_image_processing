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

    cv2.imshow('rotated', rotated)
    cv2.imshow('cropped', cropped)
    cv2.waitKey(0)
    cv2.destroyAllWindows

#Finds the angle of the card using Hough traslation algorithm.
def cardRotation(img):
    angles = []
    threshold = 5
    tempThresholdAngles = []
    thresholdAngles = []

    h, w = img.shape[:2]
    x = h/2
    y = w/2

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    retval, thresh = cv2.threshold(blur,0.66*blur.max(),255,cv2.THRESH_BINARY)
    edge = cv2.Canny(thresh,retval, retval)

    lines = cv2.HoughLines(edge, 1, np.pi/180, int(retval))

    print(lines)
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

    angles.sort()

    for i in range(len(angles)):
        if (abs(angles[i]) == abs(angles[len(angles)-1])):
            tempThresholdAngles.append(angles[i])
            thresholdAngles.append(sum(tempThresholdAngles) / len(tempThresholdAngles))
            tempThresholdAngles.clear()
        elif (abs(angles[i]) - abs(angles[i+1]) <= threshold):
            tempThresholdAngles.append(angles[i])
        else: 
            tempThresholdAngles.append(angles[i])
            thresholdAngles.append(sum(tempThresholdAngles) / len(tempThresholdAngles))
            tempThresholdAngles.clear()

    #find the average angles.
    avAng = thresholdAngles[0]
    Matrix = cv2.getRotationMatrix2D((x,y),avAng,1.0)
    rotated = cv2.warpAffine(img, Matrix, (w + 100, h + 100))

    return rotated

def cardCropped(rotated):
    gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    retval, thresh2 = cv2.threshold(blur,0.66*blur.max(),255,cv2.THRESH_BINARY)
    edge = cv2.Canny(thresh2,retval, retval)


    contours, hierchy= cv2.findContours(edge,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    contourX = []
    contourY = []

    for cnt in contours:
        #Get an approximation
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True) 
        # draws boundary of contours.  
        # Used to flatted the array containing the co-ordinates of the vertices. 
        n = approx.ravel()  
        i = 0

        for j in n : 
            if(i % 2 == 0): 
                contourX.append(n[i])
                contourY.append(n[i + 1])
            i = i + 1

    contourX.sort()
    contourY.sort()

    TM = np.float32([ [1 , 0 , -contourX[0]], [0 , 1 , -contourY[0]] ])
    imgT = cv2.warpAffine(rotated, TM, ((contourX[-1] - contourX[0]),(contourY[-1] - contourY[0])))

    return imgT

if __name__ == '__main__':
    cardOnSide()
