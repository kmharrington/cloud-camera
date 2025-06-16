import os
import sys
import time
import subprocess 
import datetime as dt
import gphoto2 as gp
from camera import CloudCamera, logger

speeds_to_test_night = [
    '30', '20','10','5','1',
]
speeds_to_test_day = [
    '1/125','1/500','1/1000','1/2000',
]
camera = CloudCamera()
camera.set_image_format('Medium Fine JPEG')

wait_time = 30

if not os.path.exists('tmp'):
	os.makedirs('tmp')

def shutter_test(speeds):
    logger.info("Beginning Shutter Speed Testing")
    ori_speed = camera.get_shutterspeed()
    logger.info(f"We were originally set to {ori_speed}")
    for speed in speeds:
        logger.info(f"Try speed {speed}")
        camera.set_shutterspeed(speed)
        target = os.path.join('tmp', f"{dt.datetime.now().isoformat()}" )
        target = target.split(".")[0]
        x = speed.replace("/", "d").replace(".", "p")
        target = f"{target}_s_{x}"
    
        camera.take_photo(target)
        time.sleep(2)
    camera.set_shutterspeed(ori_speed)
   
     
       
while True:

    now = dt.datetime.now().astimezone(dt.timezone.utc)
    if now.hour > 1 and now.hour < 10:
        shutter_test(speeds_to_test_night)
    else:
        shutter_test(speeds_to_test_day)

    time.sleep(wait_time*60)

