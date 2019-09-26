from PIL import Image, ImageDraw, ImageFilter
import matplotlib.pyplot as plt
from scipy import ndimage
import numpy as np
import cv2
from numba import vectorize

@vectorize(['float32(float32, float32)'], target='cuda')
def main():
    """filename = 'ace2.JPG'
    kernelSize = 5 #the size of the kernel, this must always be an uneven value of at least 3
    img = Image.open('Images/ace2.JPG')
    size = width,height = img.size
    """
    print("START")
    img = cv2.imread('Images/ace2.JPG')
    print("Reading done")
    img2 = gaussianOpenCVPixels(img, 5)
    print("Gaussian done")
    cv2.imshow('Processed image', img2)
    print("image shown")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """
    # preparing a blank canvas the image can be drawn on
    img = manualGrey(img)

    img2 = gaussian(img, kernelSize)

    img2.show()
    #img.save("grey_" + filename)
    #img2.save("gaussian_grey_" + filename)

    del img2  # deleting afterwards to save memory space
    """


def pil_image_to_numpy_array(pil_image):
    return np.asarray(pil_image)

def gaussianBlur(img):
    # adding gaussian blur
    blurredImage = img.filter(ImageFilter.GaussianBlur(radius=5))
    return blurredImage

# calculates the values of each kernel necessary for the blur, based off the gaussian formula (its a really long formula)
def gaussian_kernel(size, sigma):
    size = int(size) // 2
    x, y = np.mgrid[-size:size + 1, -size:size + 1]
    normal = 1 / (2.0 * np.pi * sigma ** 2)
    g = np.exp(-((x ** 2 + y ** 2) / (2.0 * sigma ** 2))) * normal
    # This returns a 2D array, with the values of the kernel
    return g

# this currently just runs the automated conversion to a grey-scale
def autoGrey(img):
    image = img.convert('L')
    return image

def manualGrey(img):
    ### manual greyscaling
    pixels = list(img.getdata())  # making a list from image data (pixel values in r,g,b)

    grey = []  # new list made for storing the greyscale values as tuple
    for R, G, B in pixels:  # goes through RGB values in the pixels list
        color = int(R * 299 / 1000 + G * 587 / 1000 + B * 114 / 1000)  # calculating the grey color
        value = (color, color, color)  # making a tuple
        grey.append(value)  # adding a tuple to the list

    img.putdata(grey)  # putting pixel data to the image
    return img

#######################################################################################################

def gaussianOpenCVPixels(img, kernelSize):
    kernel = gaussian_kernel(kernelSize, 1)

    # the offset prevents errors from border pixels
    offset = len(kernel) // 2
    # loading the image's pixels
    pixels = width, height = img.shape[0], img.shape[1]

    # cycling through the pixels one by one
    for x in range(offset, width - offset):
        for y in range(offset, height - offset):
            acc = R, G, B = (int(0), int(0), int(0)) # setting a base pixel that wil be drawn one by one, depending on its' current value

            # cycling through the surrounding pixels in the kernels range, to apply filter calculations
            for a in range(len(kernel)):
                for b in range(len(kernel)):
                    xn = x + a - offset
                    yn = y + b - offset
                    pixel = img[xn, yn]

                    # applying the new value for each color to the new pixels
                    R += pixel[0] * kernel[a][b]
                    G += pixel[1] * kernel[a][b]
                    B += pixel[2] * kernel[a][b]

            # applying the newly calculated pixel to the canvas
            img[x, y] = (int(R), int(G), int(B))

    return img

##################################################################################################

def gaussian(img, kernelSize):
    img2 = Image.new("RGB", img.size)
    draw = ImageDraw.Draw(img2)

    kernel = gaussian_kernel(kernelSize, 1)
    # the offset prevents errors from border pixels
    offset = len(kernel) // 2
    # loading the image's pixels
    input_pixels = img.load()

    # cycling through the pixels one by one
    for x in range(offset, img.width - offset):
        for y in range(offset, img.height - offset):
            acc = R, G, B = (0, 0, 0) # setting a base pixel that wil be drawn one by one, depending on its' current value

            # cycling through the surrounding pixels in the kernels range, to apply filter calculations
            for a in range(len(kernel)):
                for b in range(len(kernel)):
                    xn = x + a - offset
                    yn = y + b - offset
                    pixel = input_pixels[xn, yn]

                    # applying the new value for each color to the new pixels
                    R += pixel[0] * kernel[a][b]
                    G += pixel[1] * kernel[a][b]
                    B += pixel[2] * kernel[a][b]

            # applying the newly calculated pixel to the canvas
            draw.point((x, y), (int(R), int(G), int(B)))

    return img2

if __name__ == '__main__':
    main()



