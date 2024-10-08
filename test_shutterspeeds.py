import os
import sys
import time
import subprocess 
import datetime as dt
import gphoto2 as gp
from camera import CloudCamera

speeds_to_test = [
    '30','20','10','5','2.5','1','0.5','1/4', '1/8', '1/15', '1/30', '1/60', '1/125'
]
camera = CloudCamera()
camera.set_image_format('Large Fine JPEG')

wait_time = 30

if not os.path.exists('tmp'):
	os.makedirs('tmp')

def shutter_test():
    print("Beginning Shutter Speed Testing")
    ori_speed = camera.get_sutterspeed()
    print(f"We were originally set to {ori_speed}")
    for speed in speeds_to_test:
        print(f"Try speed {speed}")
        camera.set_shutterspeed(speed)
        target = os.path.join('tmp', f"{dt.datetime.now().isoformat()}" )
        target = target.split(".")[0]
        x = speed.replace("/", "d").replace(".", "p")
        target = f"{target}_s_{x}"
    
        camera.take_photo(target)
        time.sleep(5)
    camera.set_shutterspeed(ori_speed)
   
     
"""        
while True:
    print('Capturing image')
    target = os.path.join('tmp', f"{dt.datetime.now().isoformat()}" )
    target = target.split(".")[0]
    camera.take_photo(target)

    now = dt.datetime.now().astimezone(dt.timezone.utc)
    if now.hour > 1 and now.hour < 10:
        shutter_test()
        
    time.sleep(wait_time*60)
"""
