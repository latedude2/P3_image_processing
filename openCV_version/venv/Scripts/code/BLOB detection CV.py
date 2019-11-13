#standard imports for openCv
import cv2
import numpy as np;

#read the image
im = cv2.imread("Images/ace.JPG", cv2.IMREAD_GRAYSCALE)

cv2.imshow('sample image', im)

cv2.waitKey(0) # waits until a key is pressed
cv2.destroyAllWindows() # destroys the window showing image
