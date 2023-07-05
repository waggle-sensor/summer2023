from source import sunapi_control
from source import sunapi_config

Camera1 = sunapi_control.CameraControl('10.31.81.11', 'admin', '')
Camera2 = sunapi_config.CameraConfiguration('10.31.81.11', 'admin', '')

# Camera1.relative_control(pan=80)
# Camera1.continuous_control(normalized_speed=True, pan=0)
# Camera1.stop_control()
# Camera1.attributes_information()
# Camera1.area_zoom(1000, 100, 1000, 100)
# Camera1.movement_control(movespeed=6, direction='Left')
# Camera1.requesting_cameras_position_information()
# Camera1.moving_to_preset_position(preset=1)
# Camera1.zoom_out()
# Camera1.aux_control('WiperOn')
# Camera1.attributes_information()
# Camera1.absolute_control(zoom=9)
# Camera1.swing_control(channel=0, mode='PanTilt')
# Camera1.group_control(channel=0, group=1, mode='Start')
# Camera1.tour_control(channel=0, tour=1, mode='Stop')
# Camera1.trace_control(channel=0, trace=1, mode='Stop')
# Camera1.applications()


# Camera2.swing_setup(action='set', channel=0, mode='PanTilt', from_preset=1,
#                     to_preset=2, speed=1, dwell_time=1)

# Camera2.group_setup(action='add', channel=0, group=1, preset_sequence=1,
#                     preset=2, speed=60, dwell_time=2) * error 604

# Camera2.group_setup(action='view', channel=0)