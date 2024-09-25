import os
import time
import datetime as dt
import gphoto2 as gp

camera = gp.Camera()
camera.init()

cfg = camera.get_config()
cfg.get_child_by_name('imageformat').set_value('RAW')
camera.set_config(cfg)

wait_time=10
npix = int( (60/wait_time)*24*5 )

if not os.path.exists('tmp'):
	os.makedirs('tmp')

for i in range(npix):
	print('Capturing image')
	file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
	ext = file_path.name.split('.')[-1]

	target = os.path.join('tmp', f"{dt.datetime.now().isoformat()}.{ext}" )
	camera_file = camera.file_get(
		file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL
	)
	camera_file.save(target)

	time.sleep(wait_time*60)
