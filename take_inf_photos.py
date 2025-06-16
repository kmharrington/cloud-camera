import os
import sys
import time
import subprocess 
import datetime as dt
import gphoto2 as gp
from camera import CloudCamera, get_file_from_now


camera = CloudCamera()
camera.set_image_format('Medium Fine JPEG')

wait_time = 60
speed = '1/500'

if not os.path.exists('tmp'):
	os.makedirs('tmp')

while True:
    print('Capturing image')
    
    target = get_file_from_now(speed)
    print(speed, target)
    camera.take_photo(target)

    time.sleep(wait_time)