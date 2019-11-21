import cv2

original = cv2.imread('../Images/Templates/K.png')
template = cv2.imread('../Images/Templates/K.png')

image1 = original.shape #gives information about size and channels of the images (3 for b g r). Optional.
image2 = template.shape

if original.shape == template.shape: #checks if the size and amount of channels in the images match. Optional.
    print("same size and channels")

    difference = cv2.subtract(original, template) #Calculates the pixel difference between original and template images
    #subtracts black pixels as in these pictures they can be either black and white

    b, g, r = cv2.split(difference) #split an image into three different intensity arrays for each color channel (b g r)

   # print(cv2.countNonZero(b)) #the difference in blue channel

    cv2.imshow("subtracted images", difference)

    #countNonZero - counts the empty spots in the array of pixels (determines white pixels)
    #less white pixels means pictures are more likely to be equal
    if cv2.countNonZero(b) <= 100 and cv2.countNonZero(g) <= 100 and cv2.countNonZero(r) <= 100:
        print("equal")

    else:
        print("not equal")


cv2.imshow("Original", original)
cv2.imshow("Template", template)
cv2.waitKey(0)
cv2.destroyAllWindows()