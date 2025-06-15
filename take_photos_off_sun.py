import os
import time
import numpy as np
import datetime as dt
import gphoto2 as gp
import ephem
from camera import CloudCamera, logger

def get_file_from_now(shutter_speed, basedir='tmp'):
    """get file from the current time. creates 5 digit ctime 
    folders for the files as well 
    """
    now = int(time.time())
    dir = str(now)[:5]

    target = os.path.join(basedir, dir )
    if not os.path.exists(target):
        os.mkdir(target)
    target = os.path.join(target, now)

    x = shutter_speed.replace("/", "d").replace(".", "p")
    target = f"{target}_s_{x}"

    return target

site = ephem.Observer()
site.long = "-67.787925"
site.lat = "-22.95999167"
site.elev = 5188 #meters, about

camera = CloudCamera()
camera.set_image_format('Medium Fine JPEG')
wait_time = 15

while True:
    site.date  = ephem.Date(dt.datetime.now())
    sun = ephem.Sun(site)
    sun_el = np.degrees(sun.alt)
    
    if sun_el < -10:
        #nighttime
        speed= '10'
    elif sun_el < 0:
        #dusk
        speed = '1'
    else:
        #daytime
        speed = '1/500'  

    camera.set_shutterspeed(speed)
    target = get_file_from_now(speed)
    
    print(site.date, sun_el, speed, target)        
    camera.take_photo(target)

    time.sleep(wait_time*60)

