import imageprocessing
import sys
from PIL import Image
import pixel

def debug():
    im = Image.open('lena_std.tif')
    rgb_im = im.convert('RGBA')

    pixels = im.load()

    hsv = pixel.rgb_to_hsv(pixels[1,1])
    rgb = pixel.hsv_to_rgb(hsv)

    print(pixels[1,1])
    print(hsv)
    print(rgb)

    return True

if(__name__ == '__main__'):
    debug()
    imageprocessing.main(sys.argv)