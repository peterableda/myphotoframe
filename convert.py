#!/usr/bin/env python3 
 
import PIL 
from PIL import Image
from PIL import ImageOps
from PIL import GifImagePlugin
from PIL import ImageSequence
import numpy as np
import glob
from pathlib import Path


def resize(pil_img):
    # we need 1448×1072
    resize_height = 1072
    img_width, img_height = pil_img.size

    hpercent = (resize_height/float(img_height))
    wsize = int((float(img_width)*float(hpercent)))
    n_img = pil_img.resize((wsize,resize_height), PIL.Image.ANTIALIAS)
    return n_img

def crop(pil_img):
    # we need 1448×1072
    crop_width = 1448
    crop_height = 1072
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

def convert(pil_img):
    ary = np.array(pil_img)

    # Split the three channels
    r,g,b = np.split(ary,3,axis=2)
    r=r.reshape(-1)
    g=r.reshape(-1)
    b=r.reshape(-1)

    # Standard RGB to grayscale 
    bitmap = 0.299 * r + 0.587 * g + 0.114 * b
    bitmap = np.array(bitmap).reshape([ary.shape[0], ary.shape[1]])
    return Image.fromarray(bitmap.astype(np.uint8))

# grayscale quality is so much better than the convert
def grayscale(pil_img):
    return pil_img.convert(mode='P', colors=16)

def is_grey_scale(pil_img):
    w, h = pil_img.size
    for i in range(0, w, 20): # sampling only every 20th pixel
        for j in range(0, h, 10):
            r, g, b = pil_img.getpixel((i,j))
            if r != g != b: 
                return False
    return True

## From https://gist.github.com/BigglesZX/4016539
## with some tweeks
def analyseGif(pil_img):
    '''
    Pre-process pass over the image to determine the mode (full or additive).
    Necessary as assessing single frames isn't reliable. Need to know the mode 
    before processing all frames.
    '''
    results = {
        'size': pil_img.size,
        'mode': 'full',
    }
    try:
        while True:
            if pil_img.tile:
                tile = pil_img.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != pil_img.size:
                    results['mode'] = 'partial'
                    break
            pil_img.seek(pil_img.tell() + 1)
    except EOFError:
        pass
    return results

## From https://gist.github.com/BigglesZX/4016539
## with some tweeks
def processGif(path):
    '''
    Iterate the GIF, extracting each frame.
    '''

    pil_img = Image.open(path)

    mode = analyseGif(pil_img)['mode']

    p = pil_img.getpalette()
    
    for n in range(0, pil_img.n_frames):
        print("saving ({}) frame {}. {} {}".format(mode, n, pil_img.size, pil_img.tile))

        pil_img.seek(n)
        last_frame = pil_img.convert('RGBA')
        
        '''
        If the GIF uses local colour tables, each frame will have its own palette.
        If not, we need to apply the global palette to the new frame.
        '''
        if not pil_img.getpalette():
            pil_img.putpalette(p)
        
        new_frame = Image.new('RGBA', pil_img.size)
        
        '''
        Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
        If so, we need to construct the new frame by pasting it on top of the preceding frames.
        '''
        if mode == 'partial':
            new_frame.paste(last_frame)
        
        new_frame.paste(pil_img, (0,0), pil_img.convert('RGBA'))
        # new_frame.save('%s-%d.png' % (''.join(os.path.basename(path).split('.')[:-1]), i), 'PNG')
        new_frame.save("/home/pi/Photos/tmp/gif_{}.png".format(n), 'PNG')

        # last_frame = new_frame



# gif = Image.open('/home/pi/Photos/Adelinei&Peter full-338-ANIMATION.gif')
# print(gif.size)
# print(gif.is_animated)
# print(gif.n_frames)

# processGif('/home/pi/Photos/Adelinei&Peter full-338-ANIMATION.gif') 

# # for frame in ImageSequence.Iterator(gif):
# for n in range(0,gif.n_frames):
#     gif.seek(n)
#     # im = ImageOps.grayscale(crop(resize(gif)))
#     gif.save("/home/pi/Photos/tmp/gif_{}.png".format(n))



images = glob.glob("/home/pi/Photos/to_screen/*.jpg")
for image in images:
    print("Converting {} ...".format(image))
    filename = Path(image).stem
    with open(image, 'rb') as file:
        img = Image.open(file)
        im = grayscale(crop(resize(img)))
        im.save("/home/pi/Photos/to_screen_converted/{}.bmp".format(filename))


# img = Image.open('/home/pi/Photos/3ff.jpg')
# im = convert(crop(resize(img)))
# im = grayscale(crop(resize(img)))
# print(im.size)
# # im.save('/home/pi/img_convert/tmp/3ff.bmp')
