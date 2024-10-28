import os
import sys
import time
import subprocess 
import numpy as np
import datetime as dt
import gphoto2 as gp
import ephem
from camera import CloudCamera, logger


site = ephem.Observer()
site.lat = "-87.979537"
site.long = "41.716144"
site.elev = 225 #meters, about


camera = CloudCamera()
camera.set_image_format('Medium Fine JPEG')
wait_time = 15



while True:
    site.date  = ephem.Date(dt.datetime.now())
    sun = ephem.Sun(site)
    sun_el = np.degrees(sun.alt)

    if sun_el < 0:
        #nighttime
        speed = '10'
    else:
        #daytime
        speed = '1/500'    
        
    camera.set_shutterspeed(speed)
    target = os.path.join('tmp', f"{dt.datetime.now().isoformat()}" )
    target = target.split(".")[0]
    x = speed.replace("/", "d").replace(".", "p")
    target = f"{target}_s_{x}"
    
    camera.take_photo(target)

    time.sleep(wait_time*60)
""" 

speeds_to_test_night = [
    '30', '20','10','5','1',
]
speeds_to_test_day = [
    '1/125','1/500','1/1000','1/2000',
]

if not os.path.exists('tmp'):
	os.makedirs('tmp')

def shutter_test(speeds):
    logger.info("Beginning Shutter Speed Testing")
    ori_speed = camera.get_shutterspeed()
    logger.info(f"We were originally set to {ori_speed}")
    for speed in speeds:
        logger.info(f"Try speed {speed}")
    camera.set_shutterspeed(ori_speed)
   
   
       
while True:

    now = dt.datetime.now().astimezone(dt.timezone.utc)
    if now.hour > 1 and now.hour < 10:
        shutter_test(speeds_to_test_night)
    else:
        shutter_test(speeds_to_test_day)

"""

