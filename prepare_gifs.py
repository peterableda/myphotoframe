#!/usr/bin/env python3 
 
import PIL 
from PIL import Image
from PIL import ImageOps
from PIL import GifImagePlugin
from PIL import ImageSequence
import numpy as np
from pathlib import Path


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
