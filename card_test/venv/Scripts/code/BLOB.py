from PIL import Image, ImageDraw
import numpy as np

def main():
    img = Image.open('Images/ace2.JPG')
    size = width, height = img.size
    img2 = binary(img)
    counter = Counter(img2)
    img3 = detectBlobs(img2,counter)

    img3.show()
    del img, img2, img3

def detectBlobs(img, counter):
    size = width, height = img.size
    pos = 0

    for R, G, B in counter.pixels:
        if (R == 255):
            grassFire(pos, counter.pixels, width, height, counter)
            if (counter.pixelCount > 400):
                counter.blobCount += 1
            counter.pixelCount = 0
        pos += 1
    img.putdata(counter.pixels)
    print(counter.blobCount)
    return img


def grassFire(pos, pixels, width, height, counter):
    counter.pixelCount += 1
    counter.pixels[pos] = (200, 10, 150)

    if (pos + 1 < width and counter.pixels[pos + 1] == (255, 255, 255)):
        grassFire(pos + 1, counter.pixels, width, height, counter)
    if (pos + width < height and counter.pixels[pos + width] == (255, 255, 255)):
        grassFire(pos + width, counter.pixels, width, height, counter)
    if (pos - 1 > 0 and counter.pixels[pos - 1] == (255, 255, 255)):
        grassFire(pos - 1, counter.pixels, width, height, counter)
    if (pos - width > 0 and counter.pixels[pos - width] == (255, 255, 255)):
        grassFire(pos - width, counter.pixels, width, height, counter)



def randomColor():
    return tuple(np.random.randint(256, size=3))


def binary(img):
    pixels = list(img.getdata())  # making a list from image data (pixel values in r,g,b)

    newPixels = []  # new list made for storing the color values as tuple
    for R, G, B in pixels:  # goes through RGB values in the pixels list
        if (R > 120 and G < 100 and B < 100):
            color = 255  # making it white
        else:
            color = 0  # making it black
        value = (color, color, color)  # making a tuple
        newPixels.append(value)  # adding a tuple to the list

    img.putdata(newPixels)  # putting pixel data to the image
    return img

class Counter:
    pixelCount = 0
    blobCount = 0
    pixels = list(img.getdata())


if __name__ == '__main__':
    main()