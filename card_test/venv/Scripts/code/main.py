from PIL import Image, ImageDraw
import numpy as np

def main():

    kernelSize = 5 #the size of the kernel, this must always be an uneven value of at least 3
    img = Image.open('Images/eight.JPG')
    size = width,height = img.size

    sobel_kernel1 = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    sobel_kernel2 = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]

    sobel_kernel3 = [[1, 0, -1], [2, 0, -2], [1, 0, -1]]
    sobel_kernel4 = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

    # preparing a blank canvas the image can be drawn on
    img1 = manualGrey(img)

    img2 = applySingleKernel(img1, gaussian_kernel(kernelSize,1))

    img3 = applyDoubleKernel(img2, sobel_kernel1, sobel_kernel2)
    img4 = applyDoubleKernel(img2, sobel_kernel3, sobel_kernel4)

    img5 = combineEdges(img3, img4)

    img5.show()

    del img, img2, img3, img4, img5  # deleting afterwards to save memory space

# calculates the values of each kernel necessary for the blur, based off the gaussian formula (its a really long formula)
def gaussian_kernel(size, sigma):
    size = int(size) // 2
    x, y = np.mgrid[-size:size + 1, -size:size + 1]
    normal = 1 / (2.0 * np.pi * sigma ** 2)
    g = np.exp(-((x ** 2 + y ** 2) / (2.0 * sigma ** 2))) * normal
    # This returns a 2D array, with the values of the kernel
    return g

# this currently just runs the automated conversion to a grey-scale
def bw(img):
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

def applySingleKernel(img, kernel):
    img2 = Image.new("RGB", img.size)
    draw = ImageDraw.Draw(img2)

    # the offset prevents errors from border pixels
    offset = len(kernel) // 2
    # loading the image's pixels
    input_pixels = img.load()

    # cycling through the pixels one by one
    for x in range(offset, img.width - offset):
        for y in range(offset, img.height - offset):
            acc = [0, 0, 0] # setting a base pixel that wil be drawn one by one, depending on its' current value

            # cycling through the surrounding pixels in the kernels range, to apply filter calculations
            for a in range(len(kernel)):
                for b in range(len(kernel)):
                    xn = x + a - offset
                    yn = y + b - offset
                    pixel = input_pixels[xn, yn]

                    # applying the new value for each color to the new pixels
                    acc[0] += pixel[0] * kernel[a][b]
                    acc[1] += pixel[1] * kernel[a][b]
                    acc[2] += pixel[2] * kernel[a][b]

            # applying the newly calculated pixel to the canvas
            draw.point((x, y), (int(acc[0]), int(acc[1]), int(acc[2])))

    return img2

def applyDoubleKernel(img, kernel1, kernel2):
    img2 = Image.new("RGB", img.size)
    draw = ImageDraw.Draw(img2)

    # the offset prevents errors from border pixels
    offset = len(kernel1) // 2
    # loading the image's pixels
    input_pixels = img.load()

    # cycling through the pixels one by one
    for x in range(offset, img.width - offset):
        for y in range(offset, img.height - offset):
            acc = [0, 0, 0] # setting a base pixel that wil be drawn one by one, depending on its' current value

            # cycling through the surrounding pixels in the kernels range, to apply filter calculations
            for a in range(len(kernel1)):
                for b in range(len(kernel1)):
                    xn = x + a - offset
                    yn = y + b - offset
                    pixel = input_pixels[xn, yn]

                    # applying the new value for each color to the new pixels
                    acc[0] += pixel[0] * (kernel1[a][b] + kernel2[a][b])
                    acc[1] += pixel[1] * (kernel1[a][b] + kernel2[a][b])
                    acc[2] += pixel[2] * (kernel1[a][b] + kernel2[a][b])

            # applying the newly calculated pixel to the canvas
            draw.point((x, y), (int(acc[0]), int(acc[1]), int(acc[2])))

    return img2

def combineEdges(img1, img2):
    pixels1 = list(img1.getdata())
    pixels2 = list(img2.getdata())

    img3 = Image.new("RGB", img1.size)
    newPixels = []
    pos = 0
    black = (0, 0, 0)

    for R, G, B in pixels1:
        if (R > 150):
            newPixels.append(pixels1[pos])
        else:
            newPixels.append(black)
        pos += 1

    pos = 0
    for R, G, B in pixels2:
        if (R > 150):
            newPixels[pos] = pixels2[pos]
        pos += 1

    img3.putdata(newPixels)
    return img3

if __name__ == '__main__':
    main()



