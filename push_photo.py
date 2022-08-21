from IT8951 import constants
from IT8951.display import AutoEPDDisplay
from PIL import Image


def get_display():
    print('Initializing EPD...')

    display = AutoEPDDisplay(vcom=-2.28, spi_hz=24000000)

    print('VCOM set to', display.epd.get_vcom())
    return display

def push(img_path, display):
    print('Displaying "{}"...'.format(img_path))

    # clearing image to white
    display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))

    img = Image.open(img_path)

    dims = (display.width, display.height)

    # img.thumbnail(dims)
    paste_coords = [dims[i] - img.size[i] for i in (0,1)]  # align image with bottom of display
    display.frame_buf.paste(img, paste_coords)

    display.draw_full(constants.DisplayModes.GC16)

def print_system_info(display):
    epd = display.epd

    print('System info:')
    print('  display size: {}x{}'.format(epd.width, epd.height))
    print('  img buffer address: {:X}'.format(epd.img_buf_address))
    print('  firmware version: {}'.format(epd.firmware_version))
    print('  LUT version: {}'.format(epd.lut_version))
    print()

def clear_display(display):
    print('Clearing display...')
    display.clear()

import os
import glob
import time
import itertools

# path = "/home/pi/img_convert/tmp/3ff.bmp"
# os.system("sudo /home/pi/photo-frame/epd {}".format(path))

disp = get_display()
print_system_info(disp)

images = glob.glob("/home/pi/Photos/to_screen_converted/*.bmp")
for image in itertools.cycle(images):
    print("Showing {} ...".format(image))
    push(image, disp)
    time.sleep(60) 
