from source import sunapi_control


Camera1 = sunapi_control.CameraControl('10.31.81.11', 'admin', 'why1not#')

# Camera1.relative_control(80, 30, 20)
# Camera1.continuous_control(focus='Stop')
# Camera1.stop_control()
# Camera1.attributes_information()
# Camera1.area_zoom(1000, 100, 1000, 100)
Camera1.movement_control(movespeed=6, direction='Left')
# Camera1.requesting_cameras_position_information()
# Camera1.moving_to_preset_position(presetname='Preset2')
# Camera1.zoom_out()
# Camera1.aux_control('WiperOn')
# Camera1.attributes_information()
# Camera1.swing_control(0, 'Stop')
# Camera1.applications()
# Camera1.absolute_control(zoom=9)