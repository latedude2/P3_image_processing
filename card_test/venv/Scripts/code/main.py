from PIL import Image, ImageDraw
from PIL import ImageFilter
import numpy as np


def gaussian_kernel(size, sigma):
    size = int(size) // 2
    x, y = np.mgrid[-size:size + 1, -size:size + 1]
    normal = 1 / (2.0 * np.pi * sigma ** 2)
    g = np.exp(-((x ** 2 + y ** 2) / (2.0 * sigma ** 2))) * normal
    return g

def bw(img):
    image = img.convert('L')
    return image


def main():
    filename = 'ace2.JPG'
    kernelSize = 5
    img = Image.open('Images/ace2.JPG')
    size = width,height = img.size

        #This applies the calculated gaussian blur to the image using the ImageFilter
        #The kernel is translated into a 1D array for the function
    #kernel = np.hstack(gaussian_kernel(kernelSize,1))
    #print (kernel)
    #image2 = bw(img).filter(ImageFilter.Kernel((kernelSize,kernelSize),kernel))

    #pixels = list()
    #img.load()
    #for x in range (1,height-1):
     #   for y in range (1,width-1):
      #      sum = 0.0
       #     for ky in range (-1,1):
        #        for kx in range (-1,1):

#                    pos = (y + ky),(x + kx)
 #                   val = bw(img).getpixel(pos)
  #                  sum += gaussian_kernel(kernelSize,1)[ky+1][kx+1] * val
   #         pixels.append(sum)

    #print (pixels)
    #array = np.array(pixels, dtype=np.uint8)
    #print (array)
    #img2 = Image.fromarray(array.reshape(126,126),"L")

    kernel = gaussian_kernel(kernelSize,1)
    offset = len(kernel) // 2
    input_pixels = img.load()
    img2 = Image.new("RGB",img.size)
    draw = ImageDraw.Draw(img2)

    for x in range(offset, img.width - offset):
        for y in range(offset, img.height - offset):
            acc = [0, 0, 0]
            for a in range(len(kernel)):
                for b in range(len(kernel)):
                    xn = x + a - offset
                    yn = y + b - offset
                    pixel = input_pixels[xn, yn]
                    acc[0] += pixel[0] * kernel[a][b]
                    acc[1] += pixel[1] * kernel[a][b]
                    acc[2] += pixel[2] * kernel[a][b]

            draw.point((x, y), (int(acc[0]), int(acc[1]), int(acc[2])))

    input_pixels = bw(img).load()
    img3 = Image.new("L", img.size)
    draw = ImageDraw.Draw(img3)

    for x in range(offset, img.width - offset):
        for y in range(offset, img.height - offset):
            acc = 0
            for a in range(len(kernel)):
                for b in range(len(kernel)):
                    xn = x + a - offset
                    yn = y + b - offset
                    pixel = input_pixels[xn, yn]
                    acc += pixel * kernel[a][b]


            draw.point((x, y), (int(acc)))

    img3.save("modified_grey_" + filename)
    img2.save("modified_" + filename)
    bw(img).save("grey_" + filename)
    del img, img2, img3



if __name__ == '__main__':
    main()



