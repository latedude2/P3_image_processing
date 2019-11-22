import cv2
import glob


original = cv2.imread('../Images/Templates/K.png')


all_templates = []
card_name = []


for i in glob.iglob("../Images/Templates/*"):
    image = cv2.imread(i)
    card_name.append(i)
    all_templates.append(image)


for template, card_name in zip(all_templates, card_name): #zip allows to work with more than 1 array

    image1 = original.shape #gives information about size and channels of the images (3 for b g r). Optional.
    image2 = template.shape

    print(image1)
    print(image2)

    if original.shape == template.shape: #checks if the size and amount of channels in the images match. Optional.
        print("same size and channels")

        difference = cv2.subtract(original, template) #Calculates the pixel difference between original and template images
        #subtracts black pixels as in these pictures they can be either black and white

        b, g, r = cv2.split(difference) #split an image into three different intensity arrays for each color channel (b g r)

        print(cv2.countNonZero(b)) #the difference in blue channel

        #cv2.imshow("subtracted images", difference)

        #countNonZero - counts the empty spots in the array of pixels (determines white pixels)
        #less white pixels means pictures are more likely to be equal
        if cv2.countNonZero(b) <= 700: #only needs info from one channel
            print("equal")
            print("Matching card " + card_name)
            break


        else:
            print("not equal")



cv2.imshow("Original", original)
cv2.imshow("Template", template)
cv2.waitKey(0)
cv2.destroyAllWindows()