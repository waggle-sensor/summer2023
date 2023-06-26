import re
import ast
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
    print(payload)
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
    parser = argparse.ArgumentParser(description='Process some integers.')
    # parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #                     help='an integer for the accumulator')
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                     const=sum, default=max,
    #                     help='sum the integers (default: find the max)')

    parser.add_argument('-ip', '--ipAddress', action='store')
    parser.add_argument('-un', '--username', action='store')
    parser.add_argument('-pw', '--password', action='store')
    parser.add_argument('-a', '--action', nargs='+')
    parser.add_argument('-v', '--values', type=int, help='the specified value of the chosen action',
                        choices=range(0, 181), nargs='+')

    parser.add_argument('-az', '--absolute_Zoom', type=int, help='the numeric value of the "absolute_Zoom" action',
                        choices=range(0, 41))

    parser.add_argument('-ap', '--absolute_Pan', type=int, help='the numeric value of the "absolute_Pan" action',
                        choices=range(0, 361))

    parser.add_argument('-at', '--absolute_Tilt', type=int, help='the numeric value of the "absolute_Tilt" action',
                        choices=range(-20, 91))

    parser.add_argument('-rz', '--relative_Zoom', type=int, help='the numeric value of the "relative_Zoom" action',
                        choices=range(-41, 41))

    parser.add_argument('-rp', '--relative_Pan', type=int, help='the numeric value of the "relative_Pan" action',
                        choices=range(-181, 181))

    parser.add_argument('-rt', '--relative_Tilt', type=int, help='the numeric value of the "relative_Tilt" action',
                        choices=range(-111, 111))

    parser.add_argument('-ccz', '--continuous_control_Zoom', type=int,
                        help='the numeric value of the "continuous_control_Zoom" action',
                        choices=range(0, 7))

    parser.add_argument('-ccp', '--continuous_control_Pan', type=int,
                        help='the numeric value of the "continuous_control_Pan" action',
                        choices=range(0, 7))

    parser.add_argument('-cct', '--continuous_control_Tilt', type=int,
                        help='the numeric value of the "continuous_control_Tilt" action',
                        choices=range(0, 7))

    parser.add_argument('-l', '--Left', type=int, help='the numeric value of the "movement_Left" action',
                        choices=range(0, 7))

    parser.add_argument('-r', '--Right', type=int, help='the numeric value of the "movement_Right" action',
                        choices=range(0, 7))

    parser.add_argument('-u', '--Up', type=int, help='the numeric value of the "movement_Up" action',
                        choices=range(0, 7))

    parser.add_argument('-d', '--Down', type=int, help='the numeric value of the "movement_Down" action',
                        choices=range(0, 7))

    parser.add_argument('-lu', '--LeftUp', type=int, help='the numeric value of the "movement_LeftUp" action',
                        choices=range(0, 7))

    parser.add_argument('-ru', '--RightUp', type=int, help='the numeric value of the "movement_RightUp" action',
                        choices=range(0, 7))

    parser.add_argument('-ld', '--LeftDown', type=int, help='the numeric value of the "movement_LeftDown" action',
                        choices=range(0, 7))

    parser.add_argument('-rd', '--RightDown', type=int, help='the numeric value of the "movement_RightDown" action',
                        choices=range(0, 7))

    parser.add_argument('-s', '--Stop', action='store', help='to execute the "movement_Stop" action')

    args = parser.parse_args()

    action_array = args.action  # saves inputted movement controls given by terminal
    action_values = args.values  # saves values assigned to movements

    if args.absolute_Zoom:
        absolute_move(IP=args.ipAddress, user=args.username, pw=args.password, Zoom=args.absolute_Zoom)

    if args.absolute_Pan:
        absolute_move(IP=args.ipAddress, user=args.username, pw=args.password, Pan=args.absolute_Pan)

    if args.absolute_Tilt:
        absolute_move(IP=args.ipAddress, user=args.username, pw=args.password, Tilt=args.absolute_Tilt)

    if args.relative_Zoom:
        relative_move(IP=args.ipAddress, user=args.username, pw=args.password, Zoom=args.relative_Zoom)

    if args.relative_Pan:
        relative_move(IP=args.ipAddress, user=args.username, pw=args.password, Pan=args.relative_Pan)

    if args.relative_Tilt:
        relative_move(IP=args.ipAddress, user=args.username, pw=args.password,  Tilt=args.relative_Tilt)

    if args.continuous_control_Zoom:
        continuous_control(IP=args.ipAddress, user=args.username, pw=args.password, Zoom=args.continuous_control_Zoom)

    if args.continuous_control_Pan:
        continuous_control(IP=args.ipAddress, user=args.username, pw=args.password, Pan=args.continuous_control_Pan)

    if args.continuous_control_Tilt:
        continuous_control(IP=args.ipAddress, user=args.username, pw=args.password, Tilt=args.continuous_control_Tilt)

    if args.Left:
        movement_control(IP=args.ipAddress, user=args.username, pw=args.password, Direction='Left', MoveSpeed=args.Left)

    if args.Right:
        movement_control(IP=args.ipAddress, user=args.username, pw=args.password, Direction='Right', MoveSpeed=args.Right)

    if args.Up:
        movement_control(IP=args.ipAddress, user=args.username, pw=args.password, Direction='Up', MoveSpeed=args.Up)

    if args.Down:
        movement_control(IP=args.ipAddress, user=args.username, pw=args.password, Direction='Down', MoveSpeed=args.Down)

    if args.LeftUp:
        movement_control(IP=args.ipAddress, user=args.username, pw=args.password, Direction='LeftUp', MoveSpeed=args.LeftUp)

    if args.RightUp:
        movement_control(IP=args.ipAddress, user=args.username, pw=args.password, Direction='RightUp', MoveSpeed=args.RightUp)

    if args.LeftDown:
        movement_control(IP=args.ipAddress, user=args.username, pw=args.password, Direction='LeftDown', MoveSpeed=args.LeftDown)

    if args.RightDown:
        movement_control(IP=args.ipAddress, user=args.username, pw=args.password, Direction='RightDown', MoveSpeed=args.RightDown)

    if args.Stop:
        movement_control(IP=args.ipAddress, user=args.username, pw=args.password, Direction='Stop')


    if args.username == "name":
        print('hello')

if __name__ == '__main__':
    main()


# movement_control(IP='10.31.81.11', user='admin', pw='why1not@', Direction = "Right", MoveSpeed = 6)
# movement_control(IP='10.31.81.11', user='admin', pw='why1not@', Direction = "Stop")
# absolute_move(IP='10.31.81.11', user='admin', pw='why1not@', Tilt = -20)
# stop_control()
# requesting_cameras_position_information(IP='10.31.81.11', user='admin', pw='why1not@', Query='Pan,Tilt,Zoom')
# zoom_out(IP='10.31.81.11', user='admin', pw='why1not@')
area_zoom(IP='10.31.81.11', user='admin', pw='why1not@', X1=7000, X2=10000, Y1=2000, Y2=5000)
# moving_to_home_position()

'''# reads query test.txt file
with open('test.txt') as f:
    lines = f.readlines()

    # initializing string
    query_str = lines[1]

    # printing original string
    print("The original string is : " + query_str)

    # Segregate Positive and Negative Integers
    # Using regex
    action_value = re.findall('[-+.]?\d+', query_str)
    
    print(action_value)
    print(float(action_value[0]))

    # printing result
    print("The numbered string is : " + str(action_value))'''

#     res = list(map(lambda sub: int(''.join(
#     [ele for ele in sub if ele.isdigit()])), lines))
#
# print(str(res))


    #
    # numbers = []
    # texts = []
    # query_part = []
    # query_part.append(lines[1])
    # print(query_part)
    # for string in lines:
    #     # to extract digits from the query test.txt file and add them to the numbers array
    #     numbers.append(re.findall('[-+.]?\d+', string))
    #     # to extract texts from the query test.txt file and add them to the texts array
    #     texts.append(re.sub("\d+", "", string).strip())
    #     print(float(numbers))
