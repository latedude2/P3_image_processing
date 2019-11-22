import cv2
import numpy as np
import imutils
import PIL

img = cv2.imread("../Images/testImage2.jpg")

## convert to hsv
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

## mask of green (36,25,25) ~ (86, 255,255)
# mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))
mask = cv2.inRange(hsv, (36, 25, 25), (70, 255,255))

## slice the green
imask = mask>0
green = np.zeros_like(img, np.uint8)
green[imask] = img[imask]

memes, threshImg = cv2.threshold(green, 0, 255, cv2.THRESH_BINARY_INV)


images = []

params = cv2.SimpleBlobDetector_Params()

# Filter by Area.
params.filterByArea = True

# Disable unwanted filter criteria params
params.filterByCircularity = False # to not care about circularity (more circular = bigger angles)
params.filterByColor = False # to not care about the color
params.filterByConvexity = False # to not care about convexity (idk actually how to explain it)
params.filterByInertia = False # doesn't care how much like a circle it is (difference in radiusw)

# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create(params)

# Detect blobs.
keypoints = detector.detect(threshImg)

grayScale = cv2.cvtColor(threshImg, cv2.COLOR_BGR2GRAY)

grayScale = cv2.GaussianBlur(grayScale, (9,9), 0)

c = cv2.findContours(grayScale.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
c= imutils.grab_contours(c)

for i in range(len(c)):
    perimeter = cv2.arcLength(c[i], True)
    if perimeter > 50:
        extLeft = tuple(c[i][c[i][:, :, 0].argmin()][0])
        extRight = tuple(c[i][c[i][:, :, 0].argmax()][0])
        extTop = tuple(c[i][c[i][:, :, 1].argmin()][0])
        extBot = tuple(c[i][c[i][:, :, 1].argmax()][0])


        # draws boundary of contours.
        # Used to flatted the array containing the co-ordinates of the vertices.

        TM = np.float32([[1, 0, -extLeft[0]], [0, 1, -extTop[1]]])
        imgT = cv2.warpAffine(img, TM, ((extRight[0] - extLeft[0]), (extBot[1] - extTop[1])))

        images.append(imgT)
        cv2.imshow("Single card pls" + str(i), imgT)


cv2.drawContours(grayScale, c, -1, 150, 3)


cv2.imshow("Contour", grayScale)


# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(threshImg, keypoints, np.array([]), (0, 0, 255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)



#return images
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()