import os
import sys
import time
import subprocess 
import datetime as dt
import gphoto2 as gp
from camera import CloudCamera



camera = CloudCamera()
camera.set_image_format('RAW')

wait_time = 10

if not os.path.exists('tmp'):
	os.makedirs('tmp')

while True:
    try:
        print('Capturing image')
        target = os.path.join('tmp', f"{dt.datetime.now().isoformat()}" )
        target = target.split(".")[0]
        camera.take_photo(target)
    except:
        print("failed to capture image")
        camera.exit()
        camera = CloudCamera()

    time.sleep(wait_time*60)
