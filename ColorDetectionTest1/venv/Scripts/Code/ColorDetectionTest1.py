import PIL
from PIL import Image
from PIL import ImageFilter
import matplotlib.pyplot as plt
import numpy as Numpy
from scipy import ndimage

def main():
    img = Image.open("Images/kingspades.jpg")

    ###-------------------------------------------------------------###
    #automatic greyscaling
    #img = img.convert('L')

    ""
    ### manual greyscaling
    pixels = list(img.getdata()) #making a list from image data (pixel values in r,g,b)

    grey = [] #new list made for storing the greyscale values as tuple
    for R,G,B in pixels: # goes through RGB values in the pixels list
        color = int(R * 299/1000 + G * 587/1000 + B * 114/1000) #calculating the grey color
        value = (color, color, color) #making a tuple
        grey.append(value) # adding a tuple to the list

    img.putdata(grey) # putting pixel data to the image
    ""

    # adding gaussian blur
    blurredImage = img.filter(ImageFilter.GaussianBlur(radius=5))
    """
    newImage = Image.new(blurredImage.mode, blurredImage.size)

    #gradientIntensity = gradientCalculation(blurredImage)
    ""
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

    blurredImage.show()
    del blurredImage

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

    return G

if __name__ == "__main__":
    main()


