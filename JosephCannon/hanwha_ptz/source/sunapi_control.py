"""
Library for the control of HANWHA PTZ cameras using Sunapi
"""
import logging
import sys
import argparse
import ast
import time
import numpy as np
import requests
from requests.auth import HTTPDigestAuth
from bs4 import BeautifulSoup

logging.basicConfig(filename='sunapi.log', filemode='w', level=logging.DEBUG)
logging.info('Started')

class CameraControl:
    """
    Module for the control of HANWHA cameras using Sunapi
    """

    def __init__(self, ip, user, password):
        self.__cam_ip = ip
        self.__cam_user = user
        self.__cam_password = password

    def _camera_command(self, value_cgi, payload: dict):
        """
        Function used to send commands to the camera
        Args:
            payload: argument dictionary for camera control

        Returns:
            Returns the response from the device to the command sent

        """

        logging.info('camera_command(%s)', payload)

        url = 'http://' + self.__cam_ip + '/stw-cgi/' + value_cgi

        resp = requests.get(url, auth=HTTPDigestAuth(self.__cam_user, self.__cam_password),
                            params=payload)

        if (resp.status_code != 200) and (resp.status_code != 204):
            soup = BeautifulSoup(resp.text, features="lxml")
            logging.error('%s', soup.get_text())
            if resp.status_code == 401:
                sys.exit(1)

        return resp

    def operation_finished(self):
        """
        Operation to request PTZ status.

        Returns:
            Returns status and notifies when the operation is finished

        """
        resp = self._camera_command('ptzcontrol.cgi',
                                    {'msubmenu': 'query', 'action': 'view', 'Query': 'Pan,Tilt,Zoom'})

        current_pan = float(resp.text.split()[0].split('=')[1])
        current_tilt = float(resp.text.split()[1].split('=')[1])
        current_zoom = float(resp.text.split()[2].split('=')[1])

        if abs(360 - current_pan) < 0.02 or current_pan < 0.02:
            # This if statement is necessary for when absolute pan is zero. When the camera position
            # is requested, the query returned was either approximately 360 or zero. This statement
            # sets out to fix that bug by forcing the current pan position to be read as zero.

            current_pan = 0

        ptz_list = (current_pan, current_tilt, current_zoom)

        return ptz_list

    def stop_control(self):
        """
        Operation to stop ongoing pan, tilt and zoom movements of absolute relative and
        continuous type

        Returns:
            Returns the response from the device to the command sent

        """

        resp = self._camera_command('ptzcontrol.cgi', {'msubmenu': 'stop', 'action': 'control',
                                                       'OperationType': 'All'})

        print(resp.url + "\n" + str(resp.status_code) + "\n" + resp.text)

        return resp

    def absolute_control(self, pan: float = None, tilt: float = None, zoom: float = None, zoom_pulse: int = None,
                         channel: int = None):
        """
        Operation to move pan, tilt or zoom to an absolute destination.

        Args:
            pan: pans the device relative to the (0,0) position.
            tilt: tilts the device relative to the (0,0) position.
            zoom: zooms the device n steps relative to 1 zoom.

        Returns:
            Returns the response from the device to the command sent.

        """

        init_pos = self.operation_finished()  # takes current position values as an array

        resp = self._camera_command('ptzcontrol.cgi', {'msubmenu': 'absolute', 'action': 'control',
                                                       'Pan': pan, 'Tilt': tilt, 'Zoom': zoom,
                                                       'ZoomPulse': zoom_pulse, 'Channel': channel})

        print(resp.url + "\n" + str(resp.status_code) + "\n" + resp.text)

        current_position = np.sum(init_pos)  # sums elements in the array

        """
        If either pan, tilt, or zoom were not chosen, set their final position to be equal to
        their current position
        
        """
        if pan is None:
            pan = init_pos[0]

        if tilt is None:
            tilt = init_pos[1]

        if zoom is None:
            zoom = init_pos[2]

        # Since operation finished will set pan equal to zero if it is approximately close,
        # pan must be equal to zero here as well as the finished_position will be zero

        if abs(pan - 360) < 0.02:
            pan = 0

        finished_position = pan + tilt + zoom

        while abs(current_position - finished_position) > 0.01:
            current_position = np.sum(self.operation_finished())

        time.sleep(0.5)

    def relative_control(self, pan: float = None, tilt: float = None, zoom: int = None, zoom_pulse: int = None,
                         channel: int = None):
        """
        Operation for Relative Pan/Tilt and Zoom Move.

        Args:
            pan: pans the device n degrees relative to the current position.
            tilt: tilts the device n degrees relative to the current position.
            zoom: zooms the device n steps relative to the current position.

        Returns:
            Returns the response from the device to the command sent.

        """

        init_pos = self.operation_finished()  # takes current position values as an array

        current_position = np.sum(init_pos)  # sums elements in the initial position array

        current_pan = init_pos[0]  # provides the absolute pan position

        current_tilt = init_pos[1]  # provides the absolute tilt position

        current_zoom = init_pos[2]  # provides the absolute zoom position

        if pan is not None:

            # If the relative pan given causes the absolute pan position to surpass 360 degrees,
            # set pan to go the other direction to reach the same location

            if (current_pan + pan) > 360:
                pan = pan - 360

            # If the relative pan given causes the absolute pan position to fall below 0 degrees,
            # set pan to go the other direction to reach the same location

            elif (current_pan + pan) < 0:
                pan = 360 + pan

        if tilt is not None:

            # if the relative tilt given exceeds the 90 degree threshold, set the relative tilt
            # equal to the difference that will result in the maximum 90-degree tilt

            if 90 < (current_tilt + tilt):
                tilt = 90 - current_tilt

            # if the relative tilt given exceeds the -20 degree threshold, set the relative tilt
            # equal to the difference that will result in the minimum -20-degree tilt

            elif (current_tilt + tilt) < -20:
                tilt = -20 + abs(current_tilt)

        if zoom is not None:

            # if the relative zoom given exceeds the 40 zoom threshold, set the relative zoom
            # equal to the difference that will result in the maximum 40 zoom

            if 40 < (current_zoom + zoom):
                zoom = 40 - current_zoom

            # if the relative zoom given exceeds the 1 degree threshold, set the relative zoom
            # equal the difference that will result in the minimum -20-degree tilt

            elif (current_zoom + zoom) < 1:
                zoom = 1 - current_zoom

        if current_pan != 0:
            resp = self._camera_command('ptzcontrol.cgi', {'msubmenu': 'relative', 'action': 'control',
                                                           'Pan': pan, 'Tilt': tilt, 'Zoom': zoom,
                                                           'ZoomPulse': zoom_pulse, 'Channel': channel})

        elif current_pan == 0:
            resp = self._camera_command('ptzcontrol.cgi', {'msubmenu': 'absolute', 'action': 'control',
                                                           'Pan': pan, 'Tilt': tilt, 'Zoom': zoom,
                                                           'ZoomPulse': zoom_pulse, 'Channel': channel})

        print(resp.url + "\n" + str(resp.status_code) + "\n" + resp.text)

        # If either pan, tilt, or zoom were not chosen, set their relative movement equal to
        # zero as nothing will be changed.

        if pan is None:
            pan = 0

        if tilt is None:
            tilt = 0

        if zoom is None:
            zoom = 0

        # The finished_position will be set to the current_position plus whatever relative changes
        # will be made.

        if current_pan + pan == 360:
            finished_position = tilt + zoom + current_position - current_pan

        if current_pan + pan != 360:
            finished_position = tilt + zoom + current_position + pan

        while abs(current_position - finished_position) > 0.01:
            current_position = np.sum(self.operation_finished())
            print(current_position)
            print(finished_position)

        time.sleep(0.5)

    def continuous_control(self, normalized_speed: bool = None, pan: int = None, tilt: int = None, zoom: int = None,
                           focus: str = None):
        """
        Operation for continuous Pan/Tilt and Zoom movements.

        Args:
            normalized_speed: enables or disables the normalized speed range for pan, tilt, zoom.
            pan: speed of movement of Pan.
            tilt: speed of movement of Tilt.
            zoom: speed of movement of Zoom.
            focus: focus control. This parameter cannot be sent together with pan, tilt, or zoom.

        Returns:
            Returns the response from the device to the command sent.

        """

        if focus not in ("Near", "Far", "Stop", None):
            raise Exception("Unauthorized command: Please enter a string from the choices: 'Near', 'Far', or 'Stop'")

        return self._camera_command('ptzcontrol.cgi', {'msubmenu': 'continuous', 'action': 'control',
                                                       'NormalizedSpeed': normalized_speed, 'Pan': pan,
                                                       'Tilt': tilt, 'Zoom': zoom, 'Focus': focus})

    def area_zoom(self, x1: int = None, x2: int = None, y1: int = None,
                  y2: int = None, tilewidth: int = None, tileheight: int = None):
        """
        Centers on positions x,y (like the center command) and zooms by a factor of z/100.

        Args:
            x1: value of the x1 coordinate.
            x2: value of the x2 coordinate.
            y1: value of the y1 coordinate.
            y2: value of the y2 coordinate.
            tilewidth: sets tile pixel width
            tileheight: sets tile pixel height

        Returns:
            Returns the response from the device to the command sent

        """

        current_zoom = self.operation_finished()[2]

        self._camera_command('ptzcontrol.cgi', {'msubmenu': 'areazoom', 'action': 'control',
                                                'X1': x1, 'X2': x2, 'Y1': y1, 'Y2': y2, 'TileWidth': tilewidth,
                                                'TileHeight': tileheight})

        """
        Checks to see if area zoom is finished

        """
        if tilewidth is None:
            tilewidth = 10000

        if tileheight is None:
            tileheight = 10000

        print(tileheight)
        relative_zoom = tileheight / abs(y1 - y2)

        final_zoom = current_zoom * relative_zoom
        print(current_zoom)
        print(final_zoom)

        while abs(current_zoom - final_zoom) > 0.5:
            current_zoom = self.operation_finished()[2]
            print(current_zoom)

    def movement_control(self, direction: str = None, movespeed: float = None):
        """
        Moves the device continuously in the specified direction.

        Args:
            direction: direction to move. (home, up, down, left, right, upleft, upright, downleft...)
            movespeed: speed to move camera.

        Returns:
            Returns the response from the device to the command sent

        """

        return self._camera_command('ptzcontrol.cgi', {'msubmenu': 'move', 'action': 'control',
                                                       'Direction': direction, 'MoveSpeed': movespeed})

    def moving_to_home_position(self, channel: int = None):
        """
        Operation to move the PTZ device to its "home" position.

        Args:
            channel: returns to home position for provided channel

        Returns:
            Returns the response from the device to the command sent

        """
        return self._camera_command('ptzcontrol.cgi', {'msubmenu': 'home', 'action': 'control',
                                                       'Channel': channel})

    def requesting_cameras_position_information(self):
        """
        Operation to request PTZ status.

        Returns:
            Returns a tuple with the position of the camera (P, T, Z)

        """
        resp = self._camera_command('ptzcontrol.cgi',
                                    {'msubmenu': 'query', 'action': 'view', 'Query': 'Pan,Tilt,Zoom'})
        pan = float(resp.text.split()[0].split('=')[1])
        tilt = float(resp.text.split()[1].split('=')[1])
        zoom = float(resp.text.split()[2].split('=')[1])
        ptz_list = (pan, tilt, zoom)
        print(resp.text)
        print(ptz_list)
        return ptz_list

    def moving_to_preset_position(self, preset: int = None, presetname: str = None):
        """
        Move to the position associated with the preset on server.

        Args:
            preset: numbered position of preset
            presetname: name of preset position server.
            * cannot be sent together

        Returns:
            Returns the response from the device to the command sent

        """
        return self._camera_command('ptzcontrol.cgi', {'msubmenu': 'preset', 'action': 'control',
                                                       'Preset': preset, 'PresetName': presetname})

    def zoom_out(self):
        """
        Zoom Out to 1x

        Returns:
            Returns the response from the device to the command sent

        """
        return self._camera_command('ptzcontrol.cgi', {'msubmenu': 'areazoom', 'action': 'control',
                                                       'Type': '1x'})

    def aux_control(self, command: str = None):
        """
           Execute aux action

           Args:
               command = choice between WiperOn, HeaterOn, HeaterOff

           Returns:
               Returns the response from the device to the command sent

           """

        return self._camera_command('ptzcontrol.cgi', {'msubmenu': 'aux', 'action': 'control',
                                                       'Command': command})

    def attributes_information(self):
        """
           create url link to attributes information

           Returns:
               Returns the response from the device to the command sent

           """

        attributes = self._camera_command('attributes.cgi', {})

        print(attributes.url)

    def swing_control(self, channel: int = None, mode: str = None):
        """
              Move from one preset to another

              Args:
                  channel = choose channel
                  mode = select mode of either: "Pan", "Tilt", "PanTilt", "Stop"

              Returns:
                  Returns the response from the device to the command sent

              """

        if mode not in ("Pan", "Tilt", "PanTilt", "Stop", None):
            raise Exception(
                "Unauthorized command: Please enter a string from the choices: 'Pan', 'Tilt', 'PanTilt', 'Stop'")

        return self._camera_command('ptzcontrol.cgi', {'msubmenu': 'swing', 'action': 'control',
                                                       'Channel': channel, 'Mode': mode})

    def group_control(self, channel: int = None, group: int = None, mode: str = None):
        """
              Starts and stops a Group operation in which various presets are grouped and called
              in sequence.

              Args:
                  channel = choose channel
                  group = select a group sequence set in channel
                  mode = choose a mode of either "Start" or "Stop"

              Returns:
                  Returns the response from the device to the command sent

              """

        if mode not in ("Start", "Stop", None):
            raise Exception("Unauthorized command: Please enter a string from the choices: 'Start' or 'Stop'")

        return self._camera_command('ptzcontrol.cgi', {'msubmenu': 'group', 'action': 'control',
                                                       'Channel': channel, 'Group': group,
                                                       'Mode': mode})

    def tour_control(self, channel: int = None, tour: int = None, mode: str = None):
        """
              Starts and stops a Tour operation, calling groups of presets in sequence.

              Args:
                  channel = choose channel
                  tour = select a tour sequence set in channel
                  mode = choose a mode of either "Start" or "Stop"

              Returns:
                  Returns the response from the device to the command sent

              """

        if mode not in ("Start", "Stop", None):
            raise Exception("Unauthorized command: Please enter a string from the choices: 'Start' or 'Stop'")

        return self._camera_command('ptzcontrol.cgi', {'msubmenu': 'tour', 'action': 'control',
                                                       'Channel': channel, 'Tour': tour,
                                                       'Mode': mode})

    def trace_control(self, channel: int = None, trace: int = None, mode: str = None):
        """
              Starts and stops a Trace operation

              Args:
                  channel = choose channel
                  trace = select a trace action that has been set in channel
                  mode = choose a mode of either "Start" or "Stop"

              Returns:
                  Returns the response from the device to the command sent

              """

        if mode not in ("Start", "Stop", None):
            raise Exception("Unauthorized command: Please enter a string from the choices: 'Start' or 'Stop'")

        return self._camera_command('ptzcontrol.cgi', {'msubmenu': 'trace', 'action': 'control',
                                                       'Channel': channel, 'Trace': trace,
                                                       'Mode': mode})

    def applications(self):
        """
              Creates url and shares installed applications information
              Returns:
                  Returns the response from the device to the command sent

              """

        resp = self._camera_command('opensdk.cgi', {'msubmenu': 'apps', 'action': 'view'})

        print(resp.url + "\n" + str(resp.status_code) + "\n" + resp.text)

        return resp


def main():
    class CustomAction(argparse.Action):
        '''
        In this CustomAction class, an array will be made with action destinations being placed in 0 up through
        '+' EVEN# positions and their corresponding values paired in 1 up through '+' ODD# positions.
        '''

        def __call__(self, parser, namespace, values, option_string=None):
            if not 'ordered_args' in namespace:  # if 'ordered_args' is not found in namespace
                setattr(namespace, 'ordered_args', [])  # Add 'ordered_args' to namespace
            previous = namespace.ordered_args  # saves each previous entry to keep track of terminal commands
            previous.append(self.dest)  # appends action_destination to 'ordered_args' in namespace
            previous.append(str(values))  # appends action_value to 'ordered_args' in namespace
            setattr(namespace, 'ordered_args', previous)  # appends action's value to 'ordered_args' in namespace

    parser = argparse.ArgumentParser(description='Process some actions.')

    parser.add_argument('-ip', '--ipAddress', action='store')
    parser.add_argument('-un', '--username', action='store')
    parser.add_argument('-pw', '--password', action='store')

    parser.add_argument('-az', '--absolute_Zoom', type=int, help='the numeric value of the "absolute_Zoom" action',
                        choices=range(0, 41), action=CustomAction)

    parser.add_argument('-ap', '--absolute_Pan', type=int, help='the numeric value of the "absolute_Pan" action',
                        choices=range(0, 361), action=CustomAction)

    parser.add_argument('-at', '--absolute_Tilt', type=int, help='the numeric value of the "absolute_Tilt" action',
                        choices=range(-20, 91), action=CustomAction)

    parser.add_argument('-rz', '--relative_Zoom', type=int, help='the numeric value of the "relative_Zoom" action',
                        choices=range(-40, 41), action=CustomAction)

    parser.add_argument('-rp', '--relative_Pan', type=int, help='the numeric value of the "relative_Pan" action',
                        choices=range(-360, 361), action=CustomAction)

    parser.add_argument('-rt', '--relative_Tilt', type=int, help='the numeric value of the "relative_Tilt" action',
                        choices=range(-110, 111), action=CustomAction)

    parser.add_argument('-cc', '--continuous_control',
                        help='to execute and specify "continuous_control" action',
                        nargs='+', action=CustomAction)

    parser.add_argument('-ccz', '--continuous_control_Zoom',
                        help='the numeric value of the "continuous_control_Zoom" action',
                        nargs='+', action=CustomAction)

    parser.add_argument('-ccp', '--continuous_control_Pan',
                        help='the numeric value of the "continuous_control_Pan" action',
                        nargs='+', action=CustomAction)

    parser.add_argument('-cct', '--continuous_control_Tilt',
                        help='the numeric value of the "continuous_control_Tilt" action',
                        nargs='+', action=CustomAction)

    parser.add_argument('-ccf', '--continuous_control_Focus',
                        help='the enumerated value of the "continuous_control_Focus" action',
                        action=CustomAction)

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

    parser.add_argument('-sc', '--swing_control', help='to execute a swing action',
                        nargs=2, action=CustomAction)

    parser.add_argument('-gc', '--group_control', help='to execute a group action',
                        nargs=3, action=CustomAction)

    parser.add_argument('-tc', '--tour_control', help='to execute a tour action',
                        nargs=3, action=CustomAction)

    parser.add_argument('-trace', '--trace_control', help='to execute a trace action',
                        nargs=3, action=CustomAction)

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

    terminal_control = CameraControl(args.ipAddress, args.username, args.password)  # calling the Class CameraControl

    if args.Stop:  # If Stop is True, execute command from CameraControl class body
        terminal_control.stop_control()

    if args.WiperOn:  # If WiperOn is True, execute command from CameraControl class body
        terminal_control.aux_control(command='WiperOn')

    if args.HeaterOn:  # If HeaterOn is True, execute command from CameraControl class body
        terminal_control.aux_control(command='HeaterOn')

    if args.HeaterOff:  # If HeaterOff is True, execute command from CameraControl class body
        terminal_control.aux_control(command='HeaterOff')

    if args.requesting_cameras_position_information:  # If requesting_cameras_position_information is True, execute command from CameraControl class body
        terminal_control.requesting_cameras_position_information()

    if args.zoom_out:  # If zoom_out is True, execute command from CameraControl class body
        terminal_control.zoom_out()

    if ordered_args:

        k = 1  # offsets i by 1, to provide the corresponding value[k] to destination[i]

        for i in ordered_args[::2]:  # starts from first position and iterates by two to get next destination

            if i == 'absolute_Zoom':
                terminal_control.absolute_control(zoom=ast.literal_eval(ordered_args[k]))

            elif i == 'absolute_Pan':
                terminal_control.absolute_control(pan=ast.literal_eval(ordered_args[k]))

            elif i == 'absolute_Tilt':
                terminal_control.absolute_control(tilt=ast.literal_eval(ordered_args[k]))

            elif i == 'relative_Zoom':
                terminal_control.relative_control(zoom=ast.literal_eval(ordered_args[k]))

            elif i == 'relative_Pan':
                terminal_control.relative_control(pan=ast.literal_eval(ordered_args[k]))

            elif i == 'relative_Tilt':
                terminal_control.relative_control(tilt=ast.literal_eval(ordered_args[k]))

            elif i == 'continuous_control':
                cc_param = ast.literal_eval(ordered_args[k])

                normalized_speed = None

                pan = None

                tilt = None

                zoom = None

                j = 0

                while j < len(cc_param):

                    if j == 0:
                        normalized_speed = cc_param[j]

                    if j == 1:
                        pan = cc_param[j]

                    if j == 2:
                        tilt = cc_param[j]

                    if j == 3:
                        zoom = cc_param[j]

                    j = j + 1

                terminal_control.continuous_control(normalized_speed=normalized_speed, pan=pan,
                                                    tilt=tilt, zoom=zoom)

            elif i == 'continuous_control_Zoom':
                ccz_param = ast.literal_eval(ordered_args[k])

                normalized_speed, zoom = ccz_param[:2]  # gives first zoom parameters

                terminal_control.continuous_control(normalized_speed=normalized_speed,
                                                    zoom=zoom)

            elif i == 'continuous_control_Pan':
                ccp_param = ast.literal_eval(ordered_args[k])

                normalized_speed, pan = ccp_param[:2]  # gives first zoom parameters

                terminal_control.continuous_control(normalized_speed=normalized_speed,
                                                    pan=pan)

            elif i == 'continuous_control_Tilt':
                cct_param = ast.literal_eval(ordered_args[k])

                normalized_speed, tilt = cct_param[:2]  # gives first zoom parameters

                terminal_control.continuous_control(normalized_speed=normalized_speed,
                                                    tilt=tilt)

            elif i == 'continuous_control_Focus':
                terminal_control.continuous_control(focus=ordered_args[k])

            elif i == 'Left':
                terminal_control.movement_control(direction='Left', movespeed=ordered_args[k])

            elif i == 'Right':
                terminal_control.movement_control(direction='Right', movespeed=ordered_args[k])

            elif i == 'Up':
                terminal_control.movement_control(direction='Up', movespeed=ordered_args[k])

            elif i == 'Down':
                terminal_control.movement_control(direction='Down', movespeed=ordered_args[k])

            elif i == 'LeftUp':
                terminal_control.movement_control(direction='LeftUp', movespeed=ordered_args[k])

            elif i == 'RightUp':
                terminal_control.movement_control(direction='RightUp', movespeed=ordered_args[k])

            elif i == 'LeftDown':
                terminal_control.movement_control(direction='LeftDown', movespeed=ordered_args[k])

            elif i == 'RightDown':
                terminal_control.movement_control(direction='RightDown', movespeed=ordered_args[k])

            elif i == 'area_Zoom':
                zoom_param = ast.literal_eval(ordered_args[k])

                TileWidth = None

                TileHeight = None

                X1, X2, Y1, Y2 = zoom_param[:4]  # gives first zoom parameters

                if len(zoom_param) > 4:  # if TileWidth and TileHeight are changed
                    TileWidth, TileHeight = zoom_param[4:]

                terminal_control.area_zoom(x1=X1, x2=X2, y1=Y1, y2=Y2, tilewidth=TileWidth, tileheight=TileHeight)

            elif i == 'swing_control':
                swing_param = ast.literal_eval(ordered_args[k])

                channel, mode = swing_param[:2]

                terminal_control.swing_control(channel=channel, mode=mode)

            elif i == 'group_control':
                group_param = ast.literal_eval(ordered_args[k])

                channel, group, mode = group_param[:3]

                terminal_control.group_control(channel=channel, group=group, mode=mode)

            elif i == 'tour_control':
                tour_param = ast.literal_eval(ordered_args[k])

                channel, tour, mode = tour_param[:3]

                terminal_control.tour_control(channel=channel, tour=tour, mode=mode)

            elif i == 'trace_control':
                trace_param = ast.literal_eval(ordered_args[k])

                channel, trace, mode = trace_param[:3]

                terminal_control.trace_control(channel=channel, trace=trace, mode=mode)

            k = k + 2


if __name__ == '__main__':
    main()
