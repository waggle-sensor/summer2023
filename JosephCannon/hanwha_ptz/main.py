#import sys
#sys.path.append("/app/source")

import time
import datetime
import os
import glob
import os.path
import traceback
import subprocess

import argparse

import numpy as np

from source import sunapi_control
from source import sunapi_config
#from source import ubnt_edgeswitch

from waggle.plugin import Plugin

def set_random_position(camera):
    status=1
    while status != 0:
        pan_pos=np.random.randint(0,360)
        tilt_pos=np.random.randint(-20,90)
        zoom_pos=np.random.randint(0,2)
        status=camera.absolute_control(float(pan_pos), float(tilt_pos), float(zoom_pos))
        time.sleep(1)

def grab_image(camera):
    position = camera.requesting_cameras_position_information()
    pos_str = str(position[0])+','+str(position[1])+','+str(position[2])+' '
    # ct stores current time
    ct = str(datetime.datetime.now())
    camera.snap_shot('/imgs/' + pos_str + ct + '.jpg')


def tar_images(output_filename, folder_to_archive):
    try:
        cmd = ['tar', 'cvf', output_filename, folder_to_archive]
        output = subprocess.check_output(cmd).decode("utf-8").strip() 
        print(output)          
    except Exception:
        print(f"E: {traceback.format_exc()}")


def publish_images():
    # run tar -cvf images.tar /imgs
    tar_images('images.tar', '/imgs')
    files = glob.glob('/imgs/*.jpg', recursive=True)
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))

    with Plugin() as plugin:
        ct = str(datetime.datetime.now())
        os.rename('images.tar', ct+'_images.tar')
        plugin.upload_file(ct+'_images.tar')





def main():

    parser = argparse.ArgumentParser("PTZ sampler")
    parser.add_argument("-it", "--iterations", help="An integer with the number of iterations (PTZ rounds) to be run (default=10).", type=int, default=10)
    parser.add_argument("-mv", "--movements", help="An integer with the number of movements in each PTZ round to be run (default=10).", type=int, default=10)
    args = parser.parse_args()



    iterations = args.iterations
    number_of_commands = args.movements

    Camera1 = sunapi_control.CameraControl('10.31.81.17', 'dario', 'Why1Not@')

    status = 1
    while status != 0:
        status=Camera1.absolute_control(1, 1, 1)
        time.sleep(1)

    pan_modulation = 2
    tilt_modulation = 2
    zoom_modulation = 1.5

    pan_values = np.array([-5,-1,-0.1,0,0.1,1,5])
    pan_values = pan_values*pan_modulation
    tilt_values = np.array([-5,-1,-0.1,0,0.1,1,5])
    tilt_values = tilt_values*tilt_modulation
    zoom_values = np.array([-0.2,-0.1,0,0.1,0.2])
    zoom_values = zoom_values*zoom_modulation
    
    for iteration in range(iterations):
        PAN=np.random.choice(pan_values, number_of_commands)
        TILT=np.random.choice(tilt_values, number_of_commands)
        ZOOM=np.random.choice(zoom_values, number_of_commands)
        set_random_position(camera=Camera1)
        grab_image(camera=Camera1)

        for (pan, tilt, zoom) in zip(PAN, TILT, ZOOM):
            Camera1.relative_control(pan=pan, tilt=tilt, zoom=zoom)
            grab_image(camera=Camera1)
            #if np.random.rand() > 0.85:
            #    set_random_position(camera=Camera1)
            #    grab_image(camera=Camera1)


        publish_images()

    status = 1
    while status != 0:
        status=Camera1.absolute_control(1, 1, 1)
        time.sleep(1)

    print('DONE!')

if __name__ == "__main__":
    main()

#Camera1 = sunapi_control.CameraControl('10.31.81.11', 'admin', '')
#Camera2 = sunapi_config.CameraConfiguration('10.31.81.11', 'admin', '')
#Switch1 = ubnt_edgeswitch.SwitchInformation('10.31.81.2', 'ubnt', '')

# Camera1.relative_control(pan=180)
# Camera1.continuous_control(normalized_speed=True, pan=40)
# Camera1.stop_control()
# Camera1.attributes_information()
# Camera1.area_zoom(1000, 100, 1000, 100)
# Camera1.movement_control(movespeed=6, direction='Left')
# Camera1.requesting_cameras_position_information()
# Camera1.moving_to_preset_position(preset=1)
# Camera1.zoom_out()
# Camera1.aux_control('WiperOn')
# Camera1.attributes_information()
# Camera1.absolute_control(tilt=-10)
# Camera1.swing_control(channel=0, mode='PanTilt')
# Camera1.group_control(channel=0, group=1, mode='Start')
# Camera1.tour_control(channel=0, tour=1, mode='Stop')
# Camera1.trace_control(channel=0, trace=1, mode='Stop')
# Camera1.applications()

# Camera2.swing_setup(action='view', channel=0)

# Camera2.swing_setup(action='set', channel=0, mode='PanTilt', from_preset=1,
#                     to_preset=2, speed=60, dwell_time=2)

# # adds to the end of the list up to 128 preset positions
# Camera2.group_setup(action='add', channel=0, group=1, preset=4, speed=50, dwell_time=1)

# # updates the preset in the preset sequence selected. ex. if preset sequence is 3, and
# # preset is 4, update position 3 of the preset sequence to be preset 4
# Camera2.group_setup(action='update', channel=0, group=1, preset_sequence=3, preset=4, speed=50, dwell_time=1)

# Camera2.group_setup(action='remove', channel=0, group=1)

# Camera2.group_setup(action='view', channel=0, group=2)

