import os
import time
import argparse
from camera import CloudCamera, get_file_from_now

def get_parser(parser=None):
    if parser is None:
        parser = argparse.ArgumentParser()
    parser.add_argument(
        '--n', default=1, type=int, 
        help="Number of photos to take"
    )
    parser.add_argument(
        '--wait', default=10, type=float,
        help="Seconds (>1) to wait between images"
    )
    parser.add_argument(
        '--shutter-speed', default='1/500', type=str,
        help="Shutter Speed to use:"
    )
    return parser

if __name__== "__main__":
    parser = get_parser(parser=None)
    args = parser.parse_args()

    if args.wait < 1:
        raise ValueError("wait time needs to be more than one second")

    camera = CloudCamera()
    camera.set_image_format('Medium Fine JPEG')
    camera.set_shutterspeed(args.shutter_speed)

    wait_time = args.wait

    for i in range(args.n):
        print('Capturing image')
        target = get_file_from_now(args.shutter_speed)
        camera.take_photo(target)
        time.sleep(wait_time)
