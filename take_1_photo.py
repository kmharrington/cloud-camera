import os
import sys
import time
import subprocess 
import datetime as dt
import gphoto2 as gp
from camera import CloudCamera



camera = CloudCamera()
camera.set_image_format('Small Fine JPEG')


if not os.path.exists('tmp'):
	os.makedirs('tmp')

print('Capturing image')
target = os.path.join('tmp', f"{dt.datetime.now().isoformat()}" )
target = target.split(".")[0]
camera.take_photo(target)

print(target)
