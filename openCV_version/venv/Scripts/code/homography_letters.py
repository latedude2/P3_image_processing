import numpy as np
import cv2
import matplotlib.pyplot as plt


#im1 = cv2.imread('Images/face3.png')
#im1 = cv2.imread('Images/j2.png',0)
#im1 = cv2.imread('Images/kingface.jpg')

#im2 = cv2.imread('Images/background_with_cards.png')
#im2 = cv2.imread('Images/all_cards.jpg')
#im2 = cv2.imread('Images/king2.png')

img1 = cv2.imread("Images/kingface_rotated.png", cv2.IMREAD_GRAYSCALE) #gray template image
img2 = cv2.imread("Images/king.jpg", cv2.IMREAD_GRAYSCALE) #gray original iamge

orb = cv2.ORB_create() #initiate ORB object with undefined list of keypoints,

#Finding the keypoints and computing the descriptors with ORB
#Unmapping/Separating key points and descriptors from the orb created keypoint list, so we can work with them separately
keyPoints1, des1 = orb.detectAndCompute(img1,None) #choose which image to work with, None - no input.
keyPoints2, des2 = orb.detectAndCompute(img2,None)

#initiate Brute Force Matcher
matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)


#apply the Matcher to both images  using information descriptors from both images.
#Creates a list that is put into matchingPoints of the matching points between two images
matchingPoints = matcher.match(des1,des2, None)



#sorts out the matchingPoints based on their distance. Returns a sorted list of matchingPoints
matchingPoints = sorted(matchingPoints, key = lambda x:x.distance)

#creating a list/matrix that's filled with zeros and replace the zeros with keypoints that are indexed
#the length of it is as big as the matches, the datatype has to be float 32
#size of the list is matchingPoints x 2
points1 = np.zeros((len(matchingPoints), 2), dtype=np.float32)
points2 = np.zeros((len(matchingPoints), 2), dtype=np.float32)

#fills the empty list with keypoints
for i, match in enumerate(matchingPoints):
    points1[i, :] = keyPoints1[match.queryIdx].pt #gives the index of the descriptor in the list of query descriptors from the query(original) image
    print()
    points2[i, :] = keyPoints2[match.trainIdx].pt #gives the index of the descriptor in the list of training descriptors from the training(template) image
print(points1)


#draws lines on 10 keypoints that match in two images and displays in a 3rd image
img3 = cv2.drawMatches(img1,keyPoints1,img2,keyPoints2,matchingPoints[:10],None)



plt.imshow(img3)
plt.show()

