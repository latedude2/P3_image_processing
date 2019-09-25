from PIL import Image, ImageDraw
from PIL import ImageFilter
import numpy as np

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


def main():
    filename = 'ace2.JPG'
    kernelSize = 5 #the size of the kernel, this must always be an uneven value of at least 3
    img = Image.open('Images/ace2.JPG')
    size = width,height = img.size


    kernel = gaussian_kernel(kernelSize,1)
    # the offset prevents errors from border pixels
    offset = len(kernel) // 2
    # loading the image's pixels
    input_pixels = img.load()
    # preparing a blank canvas the image can be drawn on
    img2 = Image.new("RGB",img.size)
    draw = ImageDraw.Draw(img2)

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

    # the same as above, however since this will be a grey-scale image the mode is "L"
    input_pixels = bw(img).load()
    img3 = Image.new("L", img.size)
    draw = ImageDraw.Draw(img3)

    # cycling through the surrounding pixels in the kernels range, to apply filter calculations
    for x in range(offset, img.width - offset):
        for y in range(offset, img.height - offset):
            acc = 0 # Because each pixel has only one value, acc is no longer an array, just an integer

            # cycling through the surrounding pixels in the kernels range, to apply filter calculations
            for a in range(len(kernel)):
                for b in range(len(kernel)):
                    xn = x + a - offset
                    yn = y + b - offset
                    pixel = input_pixels[xn, yn]
                    acc += pixel * kernel[a][b] # applying our new singular value to be drawn

            # applying the newly calculated pixel to the canvas
            draw.point((x, y), (int(acc)))

    # Saving 3 different images, to compare grey-scale, blurred grey-scale and blurred color
    img3.save("modified_grey_" + filename)
    img2.save("modified_" + filename)
    bw(img).save("grey_" + filename)
    del img, img2, img3 # deleting afterwards to save memory space



if __name__ == '__main__':
    main()



