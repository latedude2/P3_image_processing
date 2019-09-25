import PIL
from PIL import Image
from PIL import ImageFilter
import matplotlib.pyplot as plt
import numpy as Numpy
from scipy import ndimage

def main():
    img = openImage("Images/kingspades.jpg")

    ###-------------------------------------------------------------###
    #img = autoGrey(img)
    img = manualGrey(img)

    img = gaussianBlur(img)

    showImage(img)
    del img



def pil_image_to_numpy_array(pil_image):
    return np.asarray(pil_image)

def autoGrey(img):
    #automatic greyscaling
    greyImage = img.convert('L')
    return greyImage

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

def gaussianBlur(img):
    # adding gaussian blur
    blurredImage = img.filter(ImageFilter.GaussianBlur(radius=5))
    return blurredImage

def gradientCalculation(img):
    ### mask for gradient calculation
    Kx = Numpy.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], Numpy.float32)
    Ky = Numpy.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], Numpy.float32)

    ### convolution
    Ix = ndimage.convolve(img, Kx, mode='constant')
    Iy = ndimage.convolve(img, Ky, mode='constant')

    G = Numpy.hypot(Ix, Iy)
    #G = G / G.max() * 255
    #theta = Numpy.arctan2(Iy, Ix)

    ###experimenting here
    """
    newImage = Image.new(blurredImage.mode, blurredImage.size)

    #gradientIntensity = gradientCalculation(blurredImage)
    # Get x-gradient in "sx"
    sx = ndimage.sobel(blurredImage, axis=0, mode='constant')
    # Get y-gradient in "sy"
    sy = ndimage.sobel(blurredImage, axis=1, mode='constant')
    # Get square root of sum of squares
    sobel = Numpy.hypot(sx, sy)

    # Hopefully see some edges
    plt.imshow(sobel, cmap=plt.cm.gray)
    plt.show()

    #newImage.show()
    """

    return G

def openImage(location):
    img = Image.open(location)
    return img

def showImage(img):
    img.show()

if __name__ == "__main__":
    main()


