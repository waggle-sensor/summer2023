#import sys
#sys.path.append("/app/source")

import time

import numpy as np

from source import sunapi_control
from source import sunapi_config
#from source import ubnt_edgeswitch

def main():

    def check_integrity(pos_a, ptz_com, pos_b):
        POS_a = np.array(pos_a)
        POS_b = np.array(pos_b)
        Real_command = np.array(ptz_com)
        Computed_command = POS_b-POS_a
        error = np.abs(Real_command-Computed_command)
        error[0] = error[0]%360
        print('error: ', error)
        #assert(np.all(a+c==b))

    number_of_commands = 50
    Camera1 = sunapi_control.CameraControl('10.31.81.17', 'dario', 'Why1Not@')
    Camera1.absolute_control(1, 1, 1)

    pan_modulation = 2
    tilt_modulation = 2
    zoom_modulation = 1.5

    pan_values = np.array([-5,-1,-0.1,0,0.1,1,5])
    pan_values = pan_values*pan_modulation
    tilt_values = np.array([-5,-1,-0.1,0,0.1,1,5])
    tilt_values = tilt_values*tilt_modulation
    zoom_values = np.array([-0.3,-0.1,0,0.1,0.3])
    zoom_values = zoom_values*zoom_modulation
    
    PAN=np.random.choice(pan_values, number_of_commands)
    TILT=np.random.choice(tilt_values, number_of_commands)
    ZOOM=np.random.choice(zoom_values, number_of_commands)
    first_position = Camera1.requesting_cameras_position_information()
    for (pan, tilt, zoom) in zip(PAN, TILT, ZOOM):
        Camera1.relative_control(pan=pan, tilt=tilt, zoom=zoom)
        second_position = Camera1.requesting_cameras_position_information()
        check_integrity(first_position, (pan, tilt, zoom), second_position)
        #time.sleep(1.0)
        Camera1.snap_shot('Image.jpg')
        #time.sleep(1.0)
        first_position = second_position

    Camera1.absolute_control(1, 1, 1)
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

