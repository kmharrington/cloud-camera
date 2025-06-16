import time
import numpy as np
import datetime as dt
import ephem
from camera import CloudCamera, get_file_from_now

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

