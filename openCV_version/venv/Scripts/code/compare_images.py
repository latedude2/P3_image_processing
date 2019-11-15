import cv2
import numpy as np

original = cv2.imread('Images/Nine.jpg')
template = cv2.imread('Images/Jack.jpg')

image1 = original.shape
image2 = template.shape

print(image1)
print(image2)

if original.shape == template.shape:
    print("same size and channels")
    difference = cv2.subtract(original, template)
    b, g, r = cv2.split(difference) #separate the r b g channels

    print(cv2.countNonZero(b))

    cv2.imshow("difference", difference)



    if cv2.countNonZero(b) <= 100 and cv2.countNonZero(g) <= 100 and cv2.countNonZero(r) <= 100:
        print("equal")

    else:
        print("not equal")


cv2.imshow("Original", original)
cv2.imshow("Template", template)
cv2.waitKey(0)
cv2.destroyAllWindows()