import cv2
import glob #library that look for a list of files on the filesystem with names matching a pattern - template images


original_resized = cv2.imread('../Images/corner1.png') #captured image, got from the camera
original = cv2.resize(original_resized,(75, 110))

all_templates = [] #array to store template images
card_name = ["A", "J", "K", "Q"]


for i in glob.glob("../Images/Templates/*"): #Return a list of path names in the templates folder
    template_img = cv2.imread(i)
    all_templates.append(template_img)

for template, card_name in zip(all_templates, card_name):  #zip allows to work with more than 1 array/list at a time

    image1 = original.shape  #gives information about size and channels of the images (3 for b g r). Optional.
    image2 = template.shape

    print(image1)
    print(image2)

    if original.shape == template.shape: #checks if the size and amount of channels in the images match. Might not be needed
        print("same size and channels")

        difference = cv2.subtract(original, template) #Calculates the pixel difference between original and template images
        #subtracts black pixels as in these pictures they can be either black and white

        b, g, r = cv2.split(difference) #split an image into three different intensity arrays for each color channel (b g r)

        print(cv2.countNonZero(b)) #the difference in blue channel

        #countNonZero - counts the empty spots in the array of pixels (determines white pixels)
        #less white pixels means pictures are more likely to be equal

        whitePixelThreshold = 2000;

        if cv2.countNonZero(b) <= whitePixelThreshold: #only needs info from one channel, the images are binary
            print("equal")
            print("Matching card " + card_name)
            card = card_name
            break

        else:
            print("not equal")


#do something with detected images
if card == "A":
    print("Ace")

elif card == "J":
    print("Jack")

elif card == "K":
    print("King")

else:
    print("Queen")



cv2.imshow("Original", original)
cv2.imshow("Template", template)
cv2.imshow("Subtracted image", difference)
cv2.waitKey(0)
cv2.destroyAllWindows()