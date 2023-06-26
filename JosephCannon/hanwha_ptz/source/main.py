import re
import ast
import math
import time
import argparse
import requests
from requests.auth import HTTPDigestAuth

#http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value>&action=<value>[&<parameter>=<value>]
# <Device IP> = Device IP address
# <value>.cgi = CGI name
# msubmenu=<value> = Submenu
# action=<value> = Action
# [&<parameter>=<value>] = Parameter

def camera_command(Device_IP, value_cgi, username, password, payload):

    # Function used to send commands to the camera
    # Args:
    #     payload: argument dictionary for camera control
    # Returns:
    #     Returns the response from the device to the command sent

    url = 'http://' + Device_IP + '/stw-cgi/' + value_cgi

    resp = requests.get(url, auth=HTTPDigestAuth(username, password), params=payload)
    print(resp.status_code)
    print(resp.url)
    return resp

def relative_move(IP = None, user = None, pw = None, Pan = None, Tilt = None, Zoom = None):

    # http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value1>&action=<value2>[&<parameter(s)>=<value(s)3>]
    # ex.(http://10.31.81.11/stw-cgi/ptzcontrol.cgi?msubmenu=relative&action=control&Pan=90&Tilt=5&Zoom=1)
    # payload = {msubmenu: <value1>, action: <value2>, <parameter(s)>: <value(s)3>}
    # camera_command(<Device IP>, <value>.cgi, payload)

    payload = {'msubmenu': 'relative', 'action': 'control'}  # initializing dictionary of registered commands
    # Pan = (0, +-180); Tilt = (0, +-110) at 90 degrees camera flips; Zoom = (0, +-40)


    if Pan:

        payload['Pan'] = Pan  # adds new index key 'Pan' and corresponding value to payload

    if Tilt:

        payload['Tilt'] = Tilt  # adds new index key 'Tilt' and corresponding value to payload

    if Zoom:

        payload['Zoom'] = Zoom  # adds new index key 'Zoom' and corresponding value to payload

    camera_command(IP, 'ptzcontrol.cgi', user, pw, payload)

def attributes_information(IP = None, user = None, pw = None):

    # http://<Device IP>/stw-cgi/<value>.cgi
    # ex.(http://10.31.81.11/stw-cgi/atttributes.cgi)
    # Syntax to access only the CGI: http://<Device IP>/stw-cgi/<value>.cgi/<cgi name>
    # <cgi name> = (i.e. system, network, IO)
    # ex.(http://<Device IP>/stw-cgi/<value>.cgi/system)
    # payload = {}
    # camera_command(<Device IP>, <value>.cgi, payload)

    payload = {}  # initializing dictionary of registered commands
    camera_command(IP, 'attributes.cgi', user, pw, payload)

def absolute_move(IP = None, user = None, pw = None, Pan = None, Tilt = None, Zoom = None):

    # http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value1>&action=<value2>[&<parameter(s)>=<value(s)3>]
    # ex.(http://10.31.81.11/stw-cgi/ptzcontrol.cgi?msubmenu=absolute&action=control&Pan=290&Tilt=5&Zoom=1)
    # payload = {msubmenu: <value1>, action: <value2>, <parameter(s)>: <value(s)3>}
    # camera_command(<Device IP>, <value>.cgi, payload)

    payload = {'msubmenu': 'absolute', 'action': 'control'}  # initializing dictionary of registered commands

    # Min/Max.Pan in Degrees = (0, 360)
    # Min/Max.Tilt in Degrees = (-20, 90)
    # Min/Max.Zoom = (1x, 40x)

    if Pan:

        payload['Pan'] = Pan  # adds new index key 'Pan' and corresponding value to payload

    if Tilt:

        payload['Tilt'] = Tilt  # adds new index key 'Tilt' and corresponding value to payload

    if Zoom:

        payload['Zoom'] = Zoom  # adds new index key 'Zoom' and corresponding value to payload

    camera_command(IP, 'ptzcontrol.cgi', user, pw, payload)

def continuous_control(IP = None, user = None, pw = None, Pan = None, Tilt = None, Zoom = None, Duration = None):

    # http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value1>&action=<value2>[&<parameter(s)>=<value(s)3>]
    # ex.(http://10.31.81.11/stw-cgi/ptzcontrol.cgi?msubmenu=continuous&action=control&Pan=5&Tilt=-1&Duration=6)
    # payload = {msubmenu: <value1>, action: <value2>, <parameter(s)>: <value(s)3>}
    # camera_command(<Device IP>, <value>.cgi, payload)

    payload = {'msubmenu': 'continuous', 'action': 'control'}  # initializing dictionary of registered commands

    if Pan:

        payload['Pan'] = Pan  # adds new index key 'Pan' and corresponding value to payload

    if Tilt:

        payload['Tilt'] = Tilt  # adds new index key 'Tilt' and corresponding value to payload

    if Zoom:

        payload['Zoom'] = Zoom  # adds new index key 'Zoom' and corresponding value to payload

    if Duration:

        payload['Duration'] = Duration  # adds new index key 'Duration' and corresponding value to payload

    camera_command(IP, 'ptzcontrol.cgi', user, pw, payload)

    #Max Duration = 10 seconds
    #Max Speed of Pan = 6
    #Max Speed of Tilt = 6

def requesting_cameras_position_information(IP = None, user = None, pw = None, Query = None):

    # http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value1>&action=<value2>[&<parameter(s)>=<value(s)3>]
    # ex.(http://10.31.81.11/stw-cgi/ptzcontrol.cgi?msubmenu=query&action=view&Query=Pan,Tilt,Zoom)
    # payload = {msubmenu: <value1>, action: <value2>, <parameter(s)>: <value(s)3>}
    # camera_command(<Device IP>, <value>.cgi, payload)
    payload = {'msubmenu': 'query', 'action': 'view'} # initializing dictionary of registered commands

    if Query:

        payload['Query'] = Query  # adds new index key 'Query' and corresponding value to payload

    resp = camera_command(IP, 'ptzcontrol.cgi', user, pw, payload)
    print(resp.text)
    info = str(resp.text)
    print(info)
    with open('/home/waggle/PycharmProjects/pythonProject/test.txt', 'w') as f:
        f.write(info)
    return resp

def moving_to_preset_position(IP = None, user = None, pw = None, PresetName = None):

    # http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value1>&action=<value2>[&<parameter(s)>=<value(s)3>]
    # ex.(http://10.31.81.11/stw-cgi/ptzcontrol.cgi?msubmenu=preset&action=control&PresetName=Preset1)
    # payload = {msubmenu: <value1>, action: <value2>, <parameter(s)>: <value(s)3>}
    # camera_command(<Device IP>, <value>.cgi, payload)
    payload = {'msubmenu': 'preset', 'action': 'control', 'PresetName': 'Preset1'}  # initializing dictionary of registered commands

    if PresetName:

        payload['PresetName'] = PresetName  # adds new index key 'PresetName' and corresponding value to payload

    camera_command(IP, 'ptzcontrol.cgi', user, pw, payload)

def moving_to_home_position(IP = None, user = None, pw = None, Channel = None):

    # http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value1>&action=<value2>[&<parameter(s)>=<value(s)3>]
    # ex.(http://10.31.81.11/stw-cgi/ptzcontrol.cgi?msubmenu=home&action=control&Channel=0)
    # payload = {msubmenu: <value1>, action: <value2>, <parameter(s)>: <value(s)3>}
    # camera_command(<Device IP>, <value>.cgi, payload)

    payload = {'msubmenu': 'home', 'action': 'control'}  # initializing dictionary of registered commands
    if Channel:
        payload['Channel'] = Channel  # adds new index key 'Channel' and corresponding value to payload

    camera_command(IP, 'ptzcontrol.cgi', user, pw, payload)

def area_zoom(IP = None, user = None, pw = None, X1 = None, X2 = None, Y1 = None, Y2 = None, TileWidth = None, TileHeight = None, Type = None):

    # http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value1>&action=<value2>[&<parameter(s)>=<value(s)3>]
    # ex.(http://10.31.81.11/stw-cgi/ptzcontrol.cgi?msubmenu=areazoom&action=control&Type=ZoomIn&\
    # X1=100&X2=2000&Y1=100&Y2=2000)
    # payload = {msubmenu: <value1>, action: <value2>, <parameter(s)>: <value(s)3>}
    # camera_command(<Device IP>, <value>.cgi, payload)
    payload = {'msubmenu': 'areazoom', 'action': 'control'}  # initializing dictionary of registered commands

    if X1:

        payload['X1'] = X1  # adds new index key 'X1' and corresponding value to payload

    if X2:

        payload['X2'] = X2  # adds new index key 'X2' and corresponding value to payload

    if Y1:

        payload['Y1'] = Y1  # adds new index key 'Y1' and corresponding value to payload

    if Y2:

        payload['Y2'] = Y2  # adds new index key 'Y2' and corresponding value to payload

    if TileWidth:

        payload['TileWidth'] = TileWidth  # adds new index key 'TileWidth' and corresponding value to payload

    if TileHeight:

        payload['TileHeight'] = TileHeight  # adds new index key 'TileHeight' and corresponding value to payload

    if Type:

        payload['Type'] = Type  # adds new index key 'Type' and corresponding value to payload

    camera_command(IP, 'ptzcontrol.cgi', user, pw, payload)

def zoom_out(IP = None, user = None, pw = None):

    # http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value1>&action=<value2>[&<parameter(s)>=<value(s)3>]
    # ex.(http://10.31.81.11/stw-cgi/ptzcontrol.cgi?msubmenu=areazoom&action=control&Type=1x)
    # payload = {msubmenu: <value1>, action: <value2>, <parameter(s)>: <value(s)3>}
    # camera_command(<Device IP>, <value>.cgi, payload)
    payload = {'msubmenu': 'areazoom', 'action': 'control', 'Type': '1x'}  # initializing dictionary of registered commands
    camera_command(IP, 'ptzcontrol.cgi', user, pw, payload)

def stop_control(IP = None, user = None, pw = None):

    # http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value1>&action=<value2>[&<parameter(s)>=<value(s)3>]
    # ex.(http://10.31.81.11/stw-cgi/ptzcontrol.cgi?msubmenu=stop&action=control&OperationType=All)
    # payload = {msubmenu: <value1>, action: <value2>, <parameter(s)>: <value(s)3>}
    # camera_command(<Device IP>, <value>.cgi, payload)
    payload = {'msubmenu': 'stop', 'action': 'control', 'OperationType': 'All'}  # initializing dictionary of registered commands
    camera_command(IP, 'ptzcontrol.cgi', user, pw, payload)

def aux_control(IP = None, user = None, pw = None, WiperOn = None, HeaterOn = None, HeaterOff = None):
    # http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value1>&action=<value2>[&<parameter(s)>=<value(s)3>]
    # ex.(http://10.31.81.11/stw-cgi/ptzcontrol.cgi?msubmenu=aux&action=control&Command=WiperOn)
    # payload = {msubmenu: <value1>, action: <value2>, <parameter(s)>: <value(s)3>}
    # camera_command(<Device IP>, <value>.cgi, payload)

    payload = {'msubmenu': 'aux', 'action': 'control'}  # initializing dictionary of registered commands

    if WiperOn:
        payload['Command'] = 'WiperOn'

    if HeaterOn:
        payload['Command'] = 'HeaterOn'

    if HeaterOff:
        payload['Command'] = 'HeaterOff'

    camera_command(IP, 'ptzcontrol.cgi', user, pw, payload)

def movement_control(IP = None, user = None, pw = None, Direction = None, MoveSpeed = None):

    # http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value1>&action=<value2>[&<parameter(s)>=<value(s)3>]
    # ex.(http://10.31.81.11/stw-cgi/ptzcontrol.cgi?msubmenu=move&action=control&Direction=LeftDown&MoveSpeed=3)
    # payload = {msubmenu: <value1>, action: <value2>, <parameter(s)>: <value(s)3>}
    # camera_command(<Device IP>, <value>.cgi, payload)

    payload = {'msubmenu': 'move', 'action': 'control'}  # initializing dictionary of registered commands

    if Direction:
        payload['Direction'] = Direction  # adds new index key 'Direction' and corresponding value to payload

    if MoveSpeed:
        payload['MoveSpeed'] = MoveSpeed  # adds new index key 'MoveSpeed' and corresponding value to payload

    camera_command(IP, 'ptzcontrol.cgi', user, pw, payload)

def swing_control(IP = None, user = None, pw = None, Channel = None, Mode = None):

    # http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value1>&action=<value2>[&<parameter(s)>=<value(s)3>]
    # ex.(http://10.31.81.11/stw-cgi/ptzcontrol.cgi?msubmenu=swing&action=control&Channel=0&Mode=PanTilt)
    # payload = {msubmenu: <value1>, action: <value2>, <parameter(s)>: <value(s)3>}
    # camera_command(<Device IP>, <value>.cgi, payload)

    payload = {'msubmenu': 'swing', 'action': 'control', 'Channel':'0', 'Mode': 'Pan', 'Mode': 'Tilt'}  # initializing dictionary of registered commands

    if Channel:
        payload['Channel'] = Channel  # adds new index key 'Channel' and corresponding value to payload

    if Mode:
        payload['Mode'] = Mode  # adds new index key 'Mode' and corresponding value to payload

    # Pan = (0, +-180); Tilt = (0, +-110) at 90 degrees camera flips; Zoom = (0, +-40)
    camera_command(IP, 'ptzcontrol.cgi', user, pw, payload)

def applications(IP = None, user = None, pw = None):

    # http://<Device IP>/stw-cgi/<value>.cgi?msubmenu=<value1>&action=<value2>[&<parameter(s)>=<value(s)3>]
    # ex.(http://10.31.81.11/stw-cgi/opensdk.cgi?msubmenu=apps&action=view)
    # payload = {msubmenu: <value1>, action: <value2>, <parameter(s)>: <value(s)3>}
    # camera_command(<Device IP>, <value>.cgi, payload)

    payload = {'msubmenu': 'apps', 'action': 'view'}  # initializing dictionary of registered commands
    # Pan = (0, +-180); Tilt = (0, +-110) at 90 degrees camera flips; Zoom = (0, +-40)
    resp = camera_command(IP, 'opensdk.cgi', user, pw, payload)
    print(resp.text)
    return resp

def main():

    class CustomAction(argparse.Action):
        # In this custom action class, an array is going to be made with actions being placed in [0, ODD #'s]
        #and corresponding values in [1, EVEN #'s].
        def __call__(self, parser, namespace, values, option_string=None):
            if not 'ordered_args' in namespace:  # if 'ordered_args' is not found in namespace
                setattr(namespace, 'ordered_args', [])  # Adds value 'ordered_args' to namespace
            previous = namespace.ordered_args
            previous.append(self.dest)  # Appends action_destination to 'ordered_args' in namespace
            previous.append(str(values))  # Appends action_value to 'ordered_args' in namespace
            setattr(namespace, 'ordered_args', previous)  # Appends action's value to 'ordered_args' in namespace

    parser = argparse.ArgumentParser(description='Process some actions.')

    parser.add_argument('-ip', '--ipAddress', action='store')
    parser.add_argument('-un', '--username', action='store')
    parser.add_argument('-pw', '--password', action='store')
    parser.add_argument('-a', '--action', nargs='+')
    parser.add_argument('-v', '--values', type=int, help='the specified value of the chosen action',
                        choices=range(-1, 181), nargs='+', action=CustomAction)

    parser.add_argument('-az', '--absolute_Zoom', type=int, help='the numeric value of the "absolute_Zoom" action',
                        choices=range(0, 41), action=CustomAction)

    parser.add_argument('-ap', '--absolute_Pan', type=int, help='the numeric value of the "absolute_Pan" action',
                        choices=range(0, 361), action=CustomAction)

    parser.add_argument('-at', '--absolute_Tilt', type=int, help='the numeric value of the "absolute_Tilt" action',
                        choices=range(-20, 91), action=CustomAction)

    parser.add_argument('-rz', '--relative_Zoom', type=int, help='the numeric value of the "relative_Zoom" action',
                        choices=range(-40, 41), action=CustomAction)

    parser.add_argument('-rp', '--relative_Pan', type=int, help='the numeric value of the "relative_Pan" action',
                        choices=range(-180, 181), action=CustomAction)

    parser.add_argument('-rt', '--relative_Tilt', type=int, help='the numeric value of the "relative_Tilt" action',
                        choices=range(-110, 111), action=CustomAction)

    parser.add_argument('-cc', '--continuous_control', type=int, help='to execute and specify "continuous_control" action',
                        nargs='+', action=CustomAction)

    parser.add_argument('-ccz', '--continuous_control_Zoom', type=int,
                        help='the numeric value of the "continuous_control_Zoom" action',
                        choices=range(-5, 6), action=CustomAction)

    parser.add_argument('-ccp', '--continuous_control_Pan', type=int,
                        help='the numeric value of the "continuous_control_Pan" action',
                        choices=range(-6, 7), action=CustomAction)

    parser.add_argument('-cct', '--continuous_control_Tilt', type=int,
                        help='the numeric value of the "continuous_control_Tilt" action',
                        choices=range(-6, 7), action=CustomAction)

    parser.add_argument('-l', '--Left', type=int, help='the numeric value of the "movement_Left" action',
                        choices=range(0, 7), action=CustomAction)

    parser.add_argument('-r', '--Right', type=int, help='the numeric value of the "movement_Right" action',
                        choices=range(0, 7), action=CustomAction)

    parser.add_argument('-u', '--Up', type=int, help='the numeric value of the "movement_Up" action',
                        choices=range(0, 7), action=CustomAction)

    parser.add_argument('-d', '--Down', type=int, help='the numeric value of the "movement_Down" action',
                        choices=range(0, 7), action=CustomAction)

    parser.add_argument('-lu', '--LeftUp', type=int, help='the numeric value of the "movement_LeftUp" action',
                        choices=range(0, 7), action=CustomAction)

    parser.add_argument('-ru', '--RightUp', type=int, help='the numeric value of the "movement_RightUp" action',
                        choices=range(0, 7), action=CustomAction)

    parser.add_argument('-ld', '--LeftDown', type=int, help='the numeric value of the "movement_LeftDown" action',
                        choices=range(0, 7), action=CustomAction)

    parser.add_argument('-rd', '--RightDown', type=int, help='the numeric value of the "movement_RightDown" action',
                        choices=range(0, 7), action=CustomAction)

    parser.add_argument('-arz', '--area_Zoom', type=int, help='to execute and specify "area_zoom" action',
                        nargs='+', action=CustomAction)

    parser.add_argument('-s', '--Stop', action='store_true',
                        help='to execute the "stop_control" action')

    parser.add_argument('-w', '--WiperOn', action='store_true',
                        help='to execute the "aux_control" action WiperOn')

    parser.add_argument('-hon', '--HeaterOn', action='store_true',
                        help='to execute the "aux_control" action HeaterOn')

    parser.add_argument('-hoff', '--HeaterOff', action='store_true',
                        help='to execute the "aux_control" action HeaterOff')

    parser.add_argument('-cpi', '--requesting_cameras_position_information', action='store_true',
                        help="retrieves camera's Pan, Tilt, and Zoom positions")

    parser.add_argument('-zo', '--zoom_out', action='store_true',
                        help="zoom's out to default")

    args = parser.parse_args()

    dictionary = vars(args)

    ordered_args = dictionary.get('ordered_args')

    if args.Stop: # If Stop is True, execute command
        stop_control(IP=args.ipAddress, user=args.username, pw=args.password)

    if args.WiperOn: # If WiperOn is True, execute command
        aux_control(IP=args.ipAddress, user=args.username, pw=args.password, WiperOn='WiperOn')

    if args.HeaterOn: # If HeaterOn is True, execute command
        aux_control(IP=args.ipAddress, user=args.username, pw=args.password, HeaterOn='HeaterOn')

    if args.HeaterOff: # If HeaterOff is True, execute command
        aux_control(IP=args.ipAddress, user=args.username, pw=args.password, HeaterOff='HeaterOff')

    if args.requesting_cameras_position_information: # If requesting_cameras_position_information is True, execute command
        requesting_cameras_position_information(IP=args.ipAddress, user=args.username, pw=args.password, Query='Pan,Tilt,Zoom')

    if args.zoom_out:  # If zoom_out is True, execute command
        zoom_out(IP=args.ipAddress, user=args.username, pw=args.password)

    if ordered_args:

        k = 1  # offsets i by 1, to provide the corresponding k-value to i-destination

        for i in ordered_args[::2]:  # starts from first position and steps by two to get next destination

            if i == 'absolute_Zoom':
                absolute_move(IP=args.ipAddress, user=args.username, pw=args.password, Zoom=ordered_args[k])
                time.sleep(2)

            if i == 'absolute_Pan':
                absolute_move(IP=args.ipAddress, user=args.username, pw=args.password, Pan=ordered_args[k])
                time.sleep(2)

            if i == 'absolute_Tilt':
                absolute_move(IP=args.ipAddress, user=args.username, pw=args.password, Tilt=ordered_args[k])
                time.sleep(2)

            if i == 'relative_Zoom':
                relative_move(IP=args.ipAddress, user=args.username, pw=args.password, Zoom=ordered_args[k])

            if i == 'relative_Pan':
                relative_move(IP=args.ipAddress, user=args.username, pw=args.password, Pan=ordered_args[k])

            if i == 'relative_Tilt':
                relative_move(IP=args.ipAddress, user=args.username, pw=args.password,  Tilt=ordered_args[k])

            if i == 'continuous_control':
                cc_param = ast.literal_eval(ordered_args[k])

                Pan = None

                Tilt = None

                Zoom = None

                j = 0

                while j < len(cc_param):

                    if j == 0:
                        Pan = cc_param[j]

                    if j == 1:
                        Tilt = cc_param[j]

                    if j == 2:
                        Zoom = cc_param[j]

                    j = j+1

                continuous_control(IP=args.ipAddress, user=args.username, pw=args.password,\
                          Pan=Pan, Tilt=Tilt, Zoom=Zoom)

            if i == 'continuous_control_Zoom':
                continuous_control(IP=args.ipAddress, user=args.username, pw=args.password, Zoom=ordered_args[k])

            if i == 'continuous_control_Pan':
                continuous_control(IP=args.ipAddress, user=args.username, pw=args.password, Pan=ordered_args[k])
                time.sleep(3)

            if i == 'continuous_control_Tilt':
                continuous_control(IP=args.ipAddress, user=args.username, pw=args.password, Tilt=ordered_args[k])
                time.sleep(3)

            if i == 'Left':
                movement_control(IP=args.ipAddress, user=args.username, pw=args.password, Direction='Left', MoveSpeed=ordered_args[k])

            if i == 'Right':
                movement_control(IP=args.ipAddress, user=args.username, pw=args.password, Direction='Right', MoveSpeed=ordered_args[k])

            if i == 'Up':
                movement_control(IP=args.ipAddress, user=args.username, pw=args.password, Direction='Up', MoveSpeed=ordered_args[k])

            if i == 'Down':
                movement_control(IP=args.ipAddress, user=args.username, pw=args.password, Direction='Down', MoveSpeed=ordered_args[k])

            if i == 'LeftUp':
                movement_control(IP=args.ipAddress, user=args.username, pw=args.password, Direction='LeftUp', MoveSpeed=ordered_args[k])

            if i == 'RightUp':
                movement_control(IP=args.ipAddress, user=args.username, pw=args.password, Direction='RightUp', MoveSpeed=ordered_args[k])

            if i == 'LeftDown':
                movement_control(IP=args.ipAddress, user=args.username, pw=args.password, Direction='LeftDown', MoveSpeed=ordered_args[k])

            if i == 'RightDown':
                movement_control(IP=args.ipAddress, user=args.username, pw=args.password, Direction='RightDown', MoveSpeed=ordered_args[k])

            if i == 'area_Zoom':
                zoom_param = ast.literal_eval(ordered_args[k])

                TileWidth = None

                TileHeight = None

                j = 0

                while j < len(zoom_param):

                    if j == 0:
                        X1 = zoom_param[j]

                    if j == 1:
                        X2 = zoom_param[j]

                    if j == 2:
                        Y1 = zoom_param[j]

                    if j == 3:
                        Y2 = zoom_param[j]

                    if j == 4:
                        TileHeight = zoom_param[j]

                    if j == 5:
                        TileWidth = zoom_param[j]

                    j = j+1

                area_zoom(IP=args.ipAddress, user=args.username, pw=args.password,\
                          X1=X1, X2=X2, Y1=Y1, Y2=Y2, TileWidth=TileWidth, TileHeight=TileHeight)

            k = k + 2

if __name__ == '__main__':
    main()