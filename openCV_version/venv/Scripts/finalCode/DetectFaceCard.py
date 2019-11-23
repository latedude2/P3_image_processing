import numpy as np
import cv2

#Face card detection constants
blue = low_blue, up_blue = ([100, 165, 105], [132, 255, 255])
yellow = low_yellow, up_yellow = ([22, 164, 120], [32, 255, 245])

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