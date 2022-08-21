import os
import glob
import time
import itertools

# path = "/home/pi/img_convert/tmp/3ff.bmp"
# os.system("sudo /home/pi/photo-frame/epd {}".format(path))

images = glob.glob("/home/pi/Photos/converted/*.bmp")
for image in itertools.cycle(images):
    print("Showing {} ...".format(image))
    os.system("sudo /home/pi/photo-frame/epd {}".format(image))
    time.sleep(300) # 5 min

