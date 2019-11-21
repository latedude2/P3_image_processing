import cv2
import numpy as np
import PIL
import treys
from treys import Evaluator
from treys import Card

#Face card detection constants
blue = low_blue, up_blue = ([100, 165, 105], [132, 255, 255])
yellow = low_yellow, up_yellow = ([22, 164, 120], [32, 255, 245])

# HSV margins for the color detection
red_lowpart = low_low_red, up_low_red = [(0, 183, 122), (9, 255, 255)]
red_uppart = low_up_red, up_up_red = [(170, 183, 122), (180, 255, 255)]
black = low_black, up_black = [(0, 0, 0), (180, 255, 56)]

def main():
    video_capture = cv2.VideoCapture(0)

    first_gaussian = backgroundSubtractSetup(video_capture)

    #Main loop
    while True:
        ret, frame = video_capture.read()

        cards = ""

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gaussian_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

        #Background subtraction to only have cards
        difference = backgroundSubtract(gaussian_frame, first_gaussian)

        # Seperate cards into seperate images

        # For each card:
        # analyseCard(cardFrame, greyCardFrame)



        # For debbuging:
        #'''
        cv2.imshow("Frame", frame)
        cv2.imshow("difference", difference)
        #cv2.imshow("Contour", DetermineSuit(gaussian_frame))
        #'''

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

def analyseCard(frame, gray_frame):

    card = ""
    # Rotate cards

    # Get corner image

    # Seperate into suit and number

    # suitImage =
    # numberImage =

    # Detect if red/Black
    isRed = checkRed(frame, gray_frame)

    gaussianCard = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    '''
    cardSuit = DetermineSuit(gaussianCard, isRed)

    '''

    # Template match letter

    # Detect if face card

    # if not faceCard:
    # Count blobs

    return card

def evaluateCards(board, hand):
    board = [
        Card.new('Ah'),
        Card.new('Kd'),
        Card.new('Jc')
    ]
    hand = [
        Card.new('Qs'),
        Card.new('Qh')
    ]
    Card.print_pretty_cards(board + hand)

    evaluator = Evaluator()
    score = evaluator.evaluate(board, hand)
    handType = evaluator.get_rank_class(score)

    print("Player 1 hand rank = %d (%s)\n" % (score, evaluator.class_to_string(handType)))

def backgroundSubtractSetup(video_capture):
    retFirst, first_frame = video_capture.read()
    first_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
    first_gaussian = cv2.GaussianBlur(first_gray, (5, 5), 0)
    return first_gaussian

def backgroundSubtract(gaussian_frame, first_gaussian):
    difference = cv2.absdiff(first_gaussian, gaussian_frame)
    _, difference = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)
    return difference

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

    # this function scans through the image and finds the defined colour
    # all this line needed because of HSV (need to consider each part separately)
    if ((colour[0] > low[0] and colour[0] < up[0]) or (colour[1] > low[1] and colour[1] < up[1]) or (colour[2] > low[2] and colour[2] < up[2])):
        print("it's a red card")
        return True
    else:
        # do the same with yellow colour
        low = np.array(low_up_red, dtype="uint8")
        up = np.array(up_up_red, dtype="uint8")

        if ((colour[0] > low[0] and colour[0] < up[0]) or (colour[1] > low[1] and colour[1] < up[1]) or (colour[2] > low[2] and colour[2] < up[2])):
            print("it's a red card")
            return True
        else:
            low = np.array(low_black, dtype="uint8")
            up = np.array(up_black, dtype="uint8")

            # all() takes all the elements in an array
            if (all(colour > low) and all(colour < up)):
                print("it's a black card")
                return False
            else:
                # if non of those colours are found it means that it's not a face card
                print("Color detection failed")

def find_face_card(image):
    # make lower and upper colour value to identify blue
    low = np.array(low_blue, dtype="uint8")
    up = np.array(up_blue, dtype="uint8")

    # this function scans through the image and finds the defined colour
    # .any() returns a boolean True if the colour is found and False if not
    if (cv2.inRange(image, low, up).any()):
        print("it's a face card because blue")
    else:
        # do the same with yellow colour
        low = np.array(low_yellow, dtype="uint8")
        up = np.array(up_yellow, dtype="uint8")

        if (cv2.inRange(image, low, up).any()):
            print("it's a face card because yellow")
        else:
            # if non of those colours are found it means that it's not a face card
            print("not a face card")


# takes a binary image with a single BLOB and checks which suit the BLOB matches
def DetermineSuit(blur, isRed):
    # Get dimensions of the image
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
    contours, hierarchy = cv2.findContours(blur, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

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
    lowMarg = lowest * 1.2  # setting a margin for when a point is considered close, from the shortest distance
    threshold = .3  # threshold for how big a percentage of the total saved points should be close for it to be one suit or the other

    lowPos = []  # for saving the array positions for the distances that are close enough to the center to be counted

    # Collecting the array positions of the points closer to the center
    for i in range(len(lengths)):
        if (lengths[i] <= lowMarg):
            lowPos.append(i)

    print(len(lowPos))
    print(len(points))

    # Differentiating here will also include color to complete the split of the 4 suits
    # Checking if more points than the threshold percentage are considered close to the center
    if (len(lowPos) > len(points) * threshold):  # Spade and diamond give many close points, since the closest is similar to all other points
        print("spade or diamond")
    elif (len(lowPos) < len(points) * threshold):  # heart and club give few close points, since the closest is an outlier from the other points
        print("heart or club")

    # drawing the contour on the image
    cv2.drawContours(outImg, contours, -1, 255, 1)

    # drawing lines to the close points
    for i in range(len(lowPos)):
        cv2.line(outImg,center, points[lowPos[i]], 100, 1)

    # drawing a clearer line to the cosest point
    cv2.line(outImg, center, points[lengths.index(lowest)], 200, 2)

    return outImg


def templateMatch(original, template):
    image1 = original.shape  # gives information about size and channels of the images (3 for b g r). Optional.
    image2 = template.shape

    if original.shape == template.shape:  # checks if the size and amount of channels in the images match. Optional.
        difference = cv2.subtract(original, template)  # Calculates the pixel difference between original and template images
        # subtracts black pixels as in these pictures they can be either black and white

        b, g, r = cv2.split(difference)  # split an image into three different intensity arrays for each color channel (b g r)

        # print(cv2.countNonZero(b)) #the difference in blue channel

        cv2.imshow("subtracted images", difference)

        # countNonZero - counts the empty spots in the array of pixels (determines white pixels)
        # less white pixels means pictures are more likely to be equal
        if cv2.countNonZero(b) <= 100 and cv2.countNonZero(g) <= 100 and cv2.countNonZero(r) <= 100:
            return True

        else:
            return False

    print("Error: wrong image given to template match")


if __name__ == "__main__" :
    main()