#!/usr/bin/env python3 
 
import glob
from pathlib import Path

from PIL import Image

RAW_PHOTOS_PATH="/home/pi/photos/raw"
TO_SCREEN_PHOTOS_PATH="/home/pi/photos/to_screen"

# Resize image to match screen hight
def resize(pil_img):
    # we need 1448×1072
    resize_height = 1072
    img_width, img_height = pil_img.size

    hpercent = (resize_height/float(img_height))
    wsize = int((float(img_width)*float(hpercent)))
    n_img = pil_img.resize((wsize,resize_height), Image.Resampling.LANCZOS)
    return n_img

# Crop image sides to match screen width
def crop(pil_img):
    # we need 1448×1072
    crop_width = 1448
    crop_height = 1072
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

# Converting image, this results in better on-screen
# quality than doing any kinds of grayscale
def convert(pil_img):
        return pil_img.convert(mode='P', colors=16)


images = glob.glob(RAW_PHOTOS_PATH + "/*.jpg")
for image in images:
    print("Converting {} ...".format(image))
    filename = Path(image).stem
    with open(image, 'rb') as file:
        img = Image.open(file)
        im = convert(crop(resize(img)))
        im.save(TO_SCREEN_PHOTOS_PATH + "/{}.bmp".format(filename))