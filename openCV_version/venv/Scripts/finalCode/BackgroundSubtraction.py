import cv2

def backgroundSubtractSetup(video_capture):
    retFirst, first_frame = video_capture.read()
    first_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
    first_gaussian = cv2.GaussianBlur(first_gray, (5, 5), 0)
    return first_gaussian

def backgroundSubtract(gaussian_frame, first_gaussian):
    difference = cv2.absdiff(first_gaussian, gaussian_frame)
    _, difference = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY_INV)
    return difference