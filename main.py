
import requests
from requests.auth import HTTPDigestAuth

#http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value>&action=<value>[&<parameter>=<value>]
# <Device IP> = Device IP address
# <value>.cgi = CGI name
# msubmenu=<value> = Submenu
# action=<value> = Action
# [&<parameter>=<value>] = Parameter

def camera_command(Device_IP, value_cgi, payload):

    # Function used to send commands to the camera
    # Args:
    #     payload: argument dictionary for camera control
    # Returns:
    #     Returns the response from the device to the command sent

    url = 'http://' + Device_IP + '/stw-cgi/' + value_cgi

    resp = requests.get(url, auth=HTTPDigestAuth('admin', 'why1not@'), params=payload)
    print(resp.status_code)
    print(resp.url)
    return resp

def relative_move(Pan = None, Tilt = None, Zoom = None):

    # http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value1>&action=<value2>[&<parameter(s)>=<value(s)3>]
    # ex.(http://10.31.81.11/stw-cgi/ptzcontrol.cgi?msubmenu=relative&action=control&Pan=90&Tilt=5&Zoom=1)
    # payload = {msubmenu: <value1>, action: <value2>, <parameter(s)>: <value(s)3>}
    # camera_command(<Device IP>, <value>.cgi, payload)

    payload = {'msubmenu': 'relative', 'action': 'control'}
    # Pan = (0, +-180); Tilt = (0, +-110) at 90 degrees camera flips; Zoom = (0, +-40)

    if Pan:

        payload['Pan'] = Pan

    if Tilt:

        payload['Tilt'] = Tilt

    if Zoom:

        payload['Zoom'] = Zoom

    camera_command('10.31.81.11', 'ptzcontrol.cgi', payload)

def attributes_information():

    # http://<Device IP>/stw-cgi/<value>.cgi
    # ex.(http://10.31.81.11/stw-cgi/atttributes.cgi)
    # Syntax to access only the CGI: http://<Device IP>/stw-cgi/<value>.cgi/<cgi name>
    # <cgi name> = (i.e. system, network, IO)
    # ex.(http://<Device IP>/stw-cgi/<value>.cgi/system)
    # payload = {}
    # camera_command(<Device IP>, <value>.cgi, payload)

    payload = {}
    camera_command('10.31.81.11', 'attributes.cgi', payload)

def absolute_move(Pan = None, Tilt = None, Zoom = None):

    # http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value1>&action=<value2>[&<parameter(s)>=<value(s)3>]
    # ex.(http://10.31.81.11/stw-cgi/ptzcontrol.cgi?msubmenu=absolute&action=control&Pan=290&Tilt=5&Zoom=1)
    # payload = {msubmenu: <value1>, action: <value2>, <parameter(s)>: <value(s)3>}
    # camera_command(<Device IP>, <value>.cgi, payload)

    payload = {'msubmenu': 'absolute', 'action': 'control'}

    # Min/Max.Pan in Degrees = (0, 360)
    # Min/Max.Tilt in Degrees = (-20, 90)
    # Min/Max.Zoom = (1x, 40x)

    if Pan:

        payload['Pan'] = Pan

    if Tilt:

        payload['Tilt'] = Tilt

    if Zoom:

        payload['Zoom'] = Zoom

    camera_command('10.31.81.11', 'ptzcontrol.cgi', payload)

def continuous_control(Pan = None, Tilt = None, Zoom = None):

    # http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value1>&action=<value2>[&<parameter(s)>=<value(s)3>]
    # ex.(http://10.31.81.11/stw-cgi/ptzcontrol.cgi?msubmenu=continuous&action=control&Pan=5&Tilt=-1&Duration=6)
    # payload = {msubmenu: <value1>, action: <value2>, <parameter(s)>: <value(s)3>}
    # camera_command(<Device IP>, <value>.cgi, payload)

    payload = {'msubmenu': 'continuous', 'action': 'control'}

    if Pan:

        payload['Pan'] = Pan

    if Tilt:

        payload['Tilt'] = Tilt

    if Zoom:

        payload['Zoom'] = Zoom

    camera_command('10.31.81.11', 'ptzcontrol.cgi', payload)

    #Max Duration = 10 seconds
    #Max Speed of Pan = 6
    #Max Speed of Tilt = 6

def requesting_cameras_position_information(Query = None):

    # http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value1>&action=<value2>[&<parameter(s)>=<value(s)3>]
    # ex.(http://10.31.81.11/stw-cgi/ptzcontrol.cgi?msubmenu=query&action=view&Query=Pan,Tilt,Zoom)
    # payload = {msubmenu: <value1>, action: <value2>, <parameter(s)>: <value(s)3>}
    # camera_command(<Device IP>, <value>.cgi, payload)
    payload = {'msubmenu': 'query', 'action': 'view'}

    if Query:

        payload['Query'] = Query

    resp = camera_command('10.31.81.11', 'ptzcontrol.cgi', payload)
    print(resp.text)
    info = str(resp.text)
    with open('/home/waggle/PycharmProjects/pythonProject/test.txt', 'w') as f:
        f.write(info)
    return resp

def moving_to_preset_position(PresetName = None):

    # http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value1>&action=<value2>[&<parameter(s)>=<value(s)3>]
    # ex.(http://10.31.81.11/stw-cgi/ptzcontrol.cgi?msubmenu=preset&action=control&PresetName=Preset1)
    # payload = {msubmenu: <value1>, action: <value2>, <parameter(s)>: <value(s)3>}
    # camera_command(<Device IP>, <value>.cgi, payload)
    payload = {'msubmenu': 'preset', 'action': 'control', 'PresetName': 'Preset1'}

    if PresetName:

        payload['PresetName'] = PresetName

    camera_command('10.31.81.11', 'ptzcontrol.cgi', payload)

def moving_to_home_position(Channel = None):

    # http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value1>&action=<value2>[&<parameter(s)>=<value(s)3>]
    # ex.(http://10.31.81.11/stw-cgi/ptzcontrol.cgi?msubmenu=home&action=control&Channel=0)
    # payload = {msubmenu: <value1>, action: <value2>, <parameter(s)>: <value(s)3>}
    # camera_command(<Device IP>, <value>.cgi, payload)

    if Channel:
        payload['Channel'] = Channel

    payload = {'msubmenu': 'home', 'action': 'control'}
    camera_command('10.31.81.11', 'ptzcontrol.cgi', payload)

def area_zoom(X1 = None, X2 = None, Y1 = None, Y2 = None, TileWidth = None, TileHeight = None, Type = None):

    # http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value1>&action=<value2>[&<parameter(s)>=<value(s)3>]
    # ex.(http://10.31.81.11/stw-cgi/ptzcontrol.cgi?msubmenu=areazoom&action=control&Type=ZoomIn&\
    # X1=100&X2=2000&Y1=100&Y2=2000)
    # payload = {msubmenu: <value1>, action: <value2>, <parameter(s)>: <value(s)3>}
    # camera_command(<Device IP>, <value>.cgi, payload)
    payload = {'msubmenu': 'areazoom', 'action': 'control'}

    if X1:

        payload['X1'] = X1

    if X2:

        payload['X2'] = X2

    if Y1:

        payload['Y1'] = Y1

    if Y2:

        payload['Y2'] = Y2

    if TileWidth:

        payload['TileWidth'] = TileWidth

    if TileHeight:

        payload['TileHeight'] = TileHeight

    if Type:

        payload['Type'] = Type

    camera_command('10.31.81.11', 'ptzcontrol.cgi', payload)

def zoom_out():

    # http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value1>&action=<value2>[&<parameter(s)>=<value(s)3>]
    # ex.(http://10.31.81.11/stw-cgi/ptzcontrol.cgi?msubmenu=areazoom&action=control&Type=1x)
    # payload = {msubmenu: <value1>, action: <value2>, <parameter(s)>: <value(s)3>}
    # camera_command(<Device IP>, <value>.cgi, payload)
    payload = {'msubmenu': 'areazoom', 'action': 'control', 'Type': '1x'}
    camera_command('10.31.81.11', 'ptzcontrol.cgi', payload)

def stop_control():

    # http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value1>&action=<value2>[&<parameter(s)>=<value(s)3>]
    # ex.(http://10.31.81.11/stw-cgi/ptzcontrol.cgi?msubmenu=stop&action=control&OperationType=All)
    # payload = {msubmenu: <value1>, action: <value2>, <parameter(s)>: <value(s)3>}
    # camera_command(<Device IP>, <value>.cgi, payload)
    payload = {'msubmenu': 'stop', 'action': 'control', 'OperationType': 'All'}
    camera_command('10.31.81.11', 'ptzcontrol.cgi', payload)

def movement_control(Direction = None, MoveSpeed = None):

    # http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value1>&action=<value2>[&<parameter(s)>=<value(s)3>]
    # ex.(http://10.31.81.11/stw-cgi/ptzcontrol.cgi?msubmenu=move&action=control&Direction=LeftDown&MoveSpeed=3)
    # payload = {msubmenu: <value1>, action: <value2>, <parameter(s)>: <value(s)3>}
    # camera_command(<Device IP>, <value>.cgi, payload)

    payload = {'msubmenu': 'move', 'action': 'control'}

    if Direction:
        payload['Direction'] = Direction

    if MoveSpeed:
        payload['MoveSpeed'] = MoveSpeed

    camera_command('10.31.81.11', 'ptzcontrol.cgi', payload)

def swing_control(Channel = None, Mode = None):

    # http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value1>&action=<value2>[&<parameter(s)>=<value(s)3>]
    # ex.(http://10.31.81.11/stw-cgi/ptzcontrol.cgi?msubmenu=swing&action=control&Channel=0&Mode=PanTilt)
    # payload = {msubmenu: <value1>, action: <value2>, <parameter(s)>: <value(s)3>}
    # camera_command(<Device IP>, <value>.cgi, payload)

    payload = {'msubmenu': 'swing', 'action': 'control', 'Channel':'0', 'Mode': 'Pan', 'Mode': 'Tilt'}

    if Channel:
        payload['Channel'] = Channel

    if Mode:
        payload['Mode'] = Mode

    # Pan = (0, +-180); Tilt = (0, +-110) at 90 degrees camera flips; Zoom = (0, +-40)
    camera_command('10.31.81.11', 'ptzcontrol.cgi', payload)

def applications():

    # http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value1>&action=<value2>[&<parameter(s)>=<value(s)3>]
    # ex.(http://10.31.81.11/stw-cgi/opensdk.cgi?msubmenu=apps&action=view)
    # payload = {msubmenu: <value1>, action: <value2>, <parameter(s)>: <value(s)3>}
    # camera_command(<Device IP>, <value>.cgi, payload)

    payload = {'msubmenu': 'apps', 'action': 'view'}
    # Pan = (0, +-180); Tilt = (0, +-110) at 90 degrees camera flips; Zoom = (0, +-40)
    resp = camera_command('10.31.81.11', 'opensdk.cgi', payload)
    print(resp.text)
    return resp


open("test.txt", mode="r")

#requesting_cameras_position_information('Pan,Tilt,Zoom')
#zoom_out()
#area_zoom(7000, 10000, 2000, 5000)
#moving_to_home_position()