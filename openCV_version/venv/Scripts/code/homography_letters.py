import numpy as np
import cv2
import matplotlib.pyplot as plt


#im1 = cv2.imread('face3.png')
#im1 = cv2.imread('j2.png',0)
#im1 = cv2.imread('k.png')
im1 = cv2.imread('kingface.jpg')



#im2 = cv2.imread('background_with_cards.png')
#im2 = cv2.imread('all_cards.jpg')
im2 = cv2.imread('king2.png')

img1=cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
img2=cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

orb = cv2.ORB_create()

kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)

matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)

matches = matcher.match(des1,des2, None)
matches = sorted(matches, key = lambda x:x.distance)

points1 = np.zeros((len(matches), 2), dtype=np.float32)
points2 = np.zeros((len(matches), 2), dtype=np.float32)

for i, match in enumerate(matches):
    points1[i, :] = kp1[match.queryIdx].pt
    points2[i, :] = kp2[match.trainIdx].pt

img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:10],None)
plt.imshow(img3)
plt.show()

