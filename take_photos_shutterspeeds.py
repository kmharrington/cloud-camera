import os
import time
import argparse
from camera import CloudCamera, get_file_from_now
from numpy import linspace
import fractions

shutterspeeds =[30,25,20,15,13,10.3,8,6.3,5,4,3.2,2.5,2,1.6,1.3,1,0.8,0.6,0.5,0.4,0.3,1/4,1/5,1/6,1/8,1/10,1/13,1/15,1/20,1/25,1/30,1/40,1/50,1/60,1/80,1/100,1/125,1/160,1/200,1/250,1/320,1/400,1/500,1/640,1/800,1/1000,1/1250,1/1600,1/2000,1/2500,1/3200,1/4000]


shutterspeeds_strs=['30','25','20','15','13','10.3','8','6.3','5','4','3.2','2.5','2','1.6','1.3','1','0.8','0.6','0.5','0.4','0.3','1/4','1/5','1/6','1/8','1/10','1/13','1/15','1/20','1/25','1/30','1/40','1/50','1/60','1/80','1/100','1/125','1/160','1/200','1/250','1/320','1/400','1/500','1/640','1/800','1/1000','1/1250','1/1600','1/2000','1/2500','1/3200','1/4000']


def get_parser(parser=None):
    if parser is None:
        parser = argparse.ArgumentParser()
    parser.add_argument(
        '--longest-time', default = 10, type = str,
        help = "longest shutter speed time"
    )
    parser.add_argument(
        '--shortest-time', default = 1/4000, type = str,
        help = "shortest shutter speed time"
    )
    parser.add_argument(
        '--steps', default = 10, type = int,
        help = "steps in between longest and shortest shutter speed times"    
    )
    return parser

def closest_shutter_speed(speed):
    diff_list = [abs(speed - i) for i in shutterspeeds]
    mindex = diff_list.index(min(diff_list))
    #print(f"for speed {speed} found shutterspeed {shutterspeeds_strs[mindex]}")
    return shutterspeeds_strs[mindex]


if __name__=="__main__":                                                      
    parser = get_parser(parser=None)
    args = parser.parse_args()

    camera = CloudCamera()                                                    
    camera.set_image_format('Medium Fine JPEG')

    shutter_range_floats = linspace(eval(args.shortest_time), eval(args.longest_time),args.steps)

    shutter_range =[closest_shutter_speed(floatspeed) for floatspeed in shutter_range_floats]

    #shutter_range = set(shutter_range) #set() shuffles the list which is annoying
    final_shutter_range= []
    for i in shutter_range:
        if i not in final_shutter_range:
            final_shutter_range.append(i)
    #print(f"{len(final_shutter_range)}")     
    if len(final_shutter_range) != int(args.steps):
        print("")
        print(f"not enough shutterspeed options. you asked for {args.steps} steps, but the shutterspeed settings can only offer {len(final_shutter_range)}.")
       
    for speed in final_shutter_range:
        speed = str(speed)
        print(f"taking a photo with shutter speed {speed}")
        target=get_file_from_now(speed)
        camera.set_shutterspeed(speed)
        camera.take_photo(target)
        time.sleep(1)

