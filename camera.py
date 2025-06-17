import os
import sys
import time
import logging
import subprocess 
import datetime as dt
import gphoto2 as gp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()

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
        logger.info("found no monitor task")
        for line in lines:
            if 'gphoto2' in line:
                logger.info(line)
        return
    for m in monitor:
        logger.info(f"Killing: {m}")
        proc_num = m.split()[1]
        subprocess.run(["kill", "-9", proc_num])

def get_file_from_now(shutter_speed=None, basedir='tmp'):
        """get file from the current time. creates 5 digit ctime 
        folders for the files as well 
        """
        now = str(int(time.time()))
        dir = now[:5]

        target = os.path.join(basedir, dir )
        if not os.path.exists(target):
            os.mkdir(target)
        target = os.path.join(target, now)

        if shutter_speed is not None:
            x = shutter_speed.replace("/", "d").replace(".", "p")
            target = f"{target}_s_{x}"

        return target

FORMATS = [
    'RAW', 
    'Small Fine JPEG',
    'Medium Fine JPEG',
    'Large Fine JPEG',
]

SHUTTER_SPEEDS = [x.strip() for x in """
    30,25,20,15,13,10.3,8,6.3,5,4,3.2,2.5,2,1.6,1.3,1,0.8,0.6,0.5,0.4,0.3,1/4,
    1/5,1/6,1/8,1/10,1/13,1/15,1/20,1/25,1/30,1/40,1/50,1/60,1/80,1/100,1/125,
    1/160,1/200,1/250,1/320,1/400,1/500,1/640,1/800,1/1000,1/1250,1/1600,1/2000,
    1/2500,1/3200,1/4000
""".split(',')]
    
class CloudCamera:
    def __init__(self):
        self.configs = None
        self.camera = None
        
        self.connect()
        if self.camera is None:
            logger.error("Failed to connect to camera")
            
    def connect(self):
        self.camera = gp.Camera()
        
        try:
            self.camera.init()
        except gp.GPhoto2Error as e:
            if e.code != -53:
                logger.error("I do not recognize this error")
                logger.error(e)
                self.camera = None
                return None
            kill_monitor()
            time.sleep(2)
            self.camera.init()
        return self.camera

    def get_configs(self):
        """ Recurse through the camera configuration to build an info dump in a dictionary
        """
        cfg = self.camera.get_config()
        if self.configs is None:
            self.configs = {}

        def recurse_cfgs(child, parent):
            try:
                cs = [c for c in child.get_choices()]
            except:
                cs = []
            name = child.get_name()
            parent[name] = {}
            
            if len(cs) > 0:
                parent[name]['choices'] = cs
            try:        
                parent[name]['value'] = child.get_value()
            except:
                pass
            for grandchild in child.get_children():
                recurse_cfgs( grandchild, parent[name])
                
        recurse_cfgs(cfg, self.configs)
        return self.configs

    def get_shutterspeed(self):
        cfg = self.camera.get_config()
        return cfg.get_child_by_name('shutterspeed').get_value()
    
    def set_shutterspeed(self, speed):
        """30,25,20,15,13,10.3,8,6.3,5,4,3.2,2.5,2,1.6,1.3,1,0.8,0.6,0.5,0.4,0.3,1/4,1/5,
        1/6,1/8,1/10,1/13,1/15,1/20,1/25,1/30,1/40,1/50,1/60,1/80,1/100,1/125,1/160,1/200,
        1/250,1/320,1/400,1/500,1/640,1/800,1/1000,1/1250,1/1600,1/2000,1/2500,1/3200,1/4000
        """
        cfg = self.camera.get_config()
        x = cfg.get_child_by_name('shutterspeed')
        x.set_value(speed)
        self.camera.set_config(cfg)
        
    def set_image_format(self, fmt):
        """TODO: pull choices from self.configs
        """
        assert fmt in FORMATS

        cfg = self.camera.get_config()
        x = cfg.get_child_by_name('imageformat')
        x.set_value(fmt)
        self.camera.set_config(cfg)

    def take_photo(self, path):
        try:
            file_path = self.camera.capture(gp.GP_CAPTURE_IMAGE)
            ext = file_path.name.split('.')[-1] 
            assert "." not in path, "path should not include extension"
            path += f".{ext}"
            camera_file = self.camera.file_get(
                file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL
            )
            camera_file.save(path) 
        except Exception as e:
            self.camera.exit()
            time.sleep(1)
            self.connect()
            logger.error(e)

if __name__ == "__main__":
    camera = CloudCamera()
