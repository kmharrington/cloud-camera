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

class CloudCamera:
    def __init__(self):
        self.connect()
        if self.camera is None:
            print("Failed to connect to camera")
    def connect(self):
        self.camera = gp.Camera()

        try:
	        self.camera.init()
        except gp.GPhoto2Error as e:
            if e.code != -53:
                print("I do not recognize this error")
                print(e)
                self.camera = None
                return None
            kill_monitor()
            time.sleep(2)
            self.camera.init()
        return self.camera

    def set_image_format(self, fmt):
        assert fmt in ['RAW', 'Small Fine JPEG']

        cfg = self.camera.get_config()
        cfg.get_child_by_name('imageformat').set_value(fmt)
        self.camera.set_config(cfg)

    def take_photo(self, path):
        file_path = self.camera.capture(gp.GP_CAPTURE_IMAGE)
        ext = file_path.name.split('.')[-1] 
        assert "." not in path, "path should not include extension"
        path += f".ext"
        camera_file = self.camera.file_get(
            file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL
        )
        camera_file.save(path) 
