## OCS Agent for Cloud Camera

import time
import numpy as np
import datetime as dt
import ephem
import txaio
from os import environ

from ocs import ocs_agent, site_config
from ocs.ocs_twisted import TimeoutLock

from camera import (
    CloudCamera, 
    get_file_from_now,
    SHUTTER_SPEEDS,
)

def valid_el(el):
    return -90<el<90
def valid_shutter(s):
    return s in SHUTTER_SPEEDS

class CloudCameraAgent:
    """Cloud Camera Agent for controlling the cloud camera

    Parameters:
        agent (OCSAgent): OCSAgent object from :func:`ocs.ocs_agent.init_site_agent`.

    Attributes:
        agent (OCSAgent): OCSAgent object from :func:`ocs.ocs_agent.init_site_agent`.
        log (txaio.tx.Logger): Logger object used to log events within the
            Agent.
        lock (TimeoutLock): TimeoutLock object used to prevent simultaneous
            commands being sent to hardware.
        camera (CloudCamera): connection to the camera
        site (ephem site): used to set the site of the camera
        _running (bool): Internal tracking of whether the Agent should be
            taking photos or not. This is used to exit the Process loop by changing it to False via the count.stop() command. 
    """

    def __init__(self, agent, save_dir):
        self.agent = agent
        self.log = agent.log
        self.lock = TimeoutLock(default_timeout=5)
        self.camera = None
        self.site = None
        self.save_dir = save_dir
        self._running = False
    
    def setup_site(self):
        ### perhaps one day we want these to be parameters
        site = ephem.Observer()
        site.long = "-67.787925"
        site.lat = "-22.95999167"
        site.elev = 5188 #meters, about
        self.site=site
    
    def setup_camera(self):
        if self.camera is not None:
            raise ValueError("I already have a camera")
        camera = CloudCamera()
        camera.set_image_format('Medium Fine JPEG')
        self.camera = camera
    
    @ocs_agent.param('wait_time', default=600., type=float, check=lambda x: x>5)
    @ocs_agent.param('night_sun_el', default=-10, type=float, check=valid_el)
    @ocs_agent.param(
        'night_shutter', default='5', type=str, check=valid_shutter
    )
    @ocs_agent.param('dusk_sun_el', default=0, type=float, check=valid_el)
    @ocs_agent.param(
        'dusk_shutter', default='0.5', type=str, check=valid_shutter
    )
    @ocs_agent.param(
        'day_shutter', default='1/1000', type=str, check=valid_shutter
    )
    def take_photos_off_sun(self, session, params):
        """take_photos_off_sun()

        **Process** - take photos with the camera where the shutter speed is
        set by the current elevation of the sun

        """
        with self.lock.acquire_timeout(job='photos-off-sun') as acquired:
            if not acquired:
                self.log.warn(f"Could not start Process because "
                            f"{self.lock.job} is already running")
                return False, "Could not acquire lock"
            
            if self.site is None:
                self.setup_site()
            if self.camera is None:
                self.setup_camera()

            self._running=True
            self.log.info("Starting to take photos")

            # Main process loop
            while self._running:
                self.site.date  = ephem.Date(dt.datetime.now())
                sun = ephem.Sun(self.site)
                sun_el = np.degrees(sun.alt)
                
                if sun_el < params['night_sun_el']: #nighttime
                    speed= params['night_shutter']
                elif sun_el < params['dusk_sun_el']: #dusk
                    speed = params['dusk_shutter']
                else: #daytime
                    speed = params['day_shutter']

                self.camera.set_shutterspeed(speed)
                target = get_file_from_now(
                    shutter_speed=speed, 
                    base_dir=self.save_dir
                )
                
                self.log.info(self.site.date, sun_el, speed, target)
                self.camera.take_photo(target)

                session.data = {"sun_el": sun_el,
                                "timestamp": time.time()}
                time.sleep(params['wait_time'])

        return True, 'Acquisition exited cleanly.'

    def _stop_taking_photos(self, session, params):
        """Stop taking photos."""
        if self._running:
            self._running= False
            return True, 'requested to stop taking photos.'
        else:
            return False, 'camera is not currently taking photos'

def add_agent_args(parser_in=None):
    if parser_in is None:
        from argparse import ArgumentParser as A
        parser_in = A()
    pgroup = parser_in.add_argument_group('Agent Options')
    pgroup.add_argument('--save-dir', type=str, default='tmp',
                        help="Directory to save photos in.")
    return parser_in

def main(args=None):
    # For logging
    txaio.use_twisted()
    txaio.make_logger()

    # Start logging
    txaio.start_logging(level=environ.get("LOGLEVEL", "info"))
    
    parser = add_agent_args()
    args = site_config.parse_args(
        agent_class='CloudCameraAgent', 
        parser=parser, args=args
    )
    agent, runner = ocs_agent.init_site_agent(args)
    camera = CloudCameraAgent(agent, args.save_dir)
    agent.register_process(
        'take_photos_off_sun',
        camera.take_photos_off_sun,
        camera._stop_taking_photos,
    )
    
    runner.run(agent, auto_reconnect=True)

if __name__ == '__main__':
    main()