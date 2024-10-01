import os
import sys
import time
import subprocess 
import datetime as dt
import gphoto2 as gp

def kill_monitor():
    out = subprocess.run(["ps", "aux"], capture_output=True)
    lines = str(out.stdout).split("\\n")
    monitor = []
    for line in lines:
        if "gvfs-gphoto2-volume-monitor" in line:
            monitor.append(line)
        if "gvfsd-gphoto2" in line:
            monitor.append(line)
    if len(monitor) == 0:
        print("found no monitor task")
        return
    for m in monitor:
        print(f"Killing: {m}")
        proc_num = m.split()[1]
        subprocess.run(["kill", "-9", proc_num])

camera = gp.Camera()


try:
	camera.init()
except gp.GPhoto2Error as e:
    if e.code != -53:
        print("I do not recognize this error")
        print(e)
        sys.exit()
    kill_monitor()
    time.sleep(2)
    camera.init()

cfg = camera.get_config()
cfg.get_child_by_name('imageformat').set_value('RAW')
camera.set_config(cfg)
