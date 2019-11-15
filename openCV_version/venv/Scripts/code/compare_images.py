import cv2
import numpy as np

original = cv2.imread('Images/Templates/K.png')
template = cv2.imread('Images/Templates/A.png')

image1 = original.shape #gives information about size and channels of the images (3 for b g r)
image2 = template.shape

print(image1)
print(image2)

if original.shape == template.shape: #gives info if the channels and size matches
    print("same size and channels")

    difference = cv2.subtract(original, template) #subtracting template pixels from original image's pixels

    b, g, r = cv2.split(difference) #separate the b g r channels

    #print(cv2.countNonZero(b)) the difference in blue channel

    cv2.imshow("difference", difference)


    #self-defined  countnonzero bgr treshold values. Should be adjusted after more testing
    if cv2.countNonZero(b) <= 100 and cv2.countNonZero(g) <= 100 and cv2.countNonZero(r) <= 100:
        print("equal")

    else:
        print("not equal")


cv2.imshow("Original", original)
cv2.imshow("Template", template)
cv2.waitKey(0)
cv2.destroyAllWindows()