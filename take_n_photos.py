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
npix = int( (60/wait_time)*24*5 )

if not os.path.exists('tmp'):
	os.makedirs('tmp')

for i in range(npix):
    print('Capturing image')
    target = os.path.join('tmp', f"{dt.datetime.now().isoformat()}" )
    target = target.split(".")[0]
    camera.take_photo(target)

    time.sleep(wait_time*60)
