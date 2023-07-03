"""
Library for the control of HANWHA PTZ cameras using Sunapi
"""
import logging
import sys
import argparse
import ast
import time
import numpy as np
import math
import requests
from requests.auth import HTTPDigestAuth
from bs4 import BeautifulSoup

logging.basicConfig(filename='sunapi.log', filemode='w', level=logging.DEBUG)
logging.info('Started')

# pylint: disable=R0904


class CameraControl:
    """
    Module for the control of HANWHA cameras using Sunapi
    """

    def __init__(self, ip, user, password):
        self.__cam_ip = ip
        self.__cam_user = user
        self.__cam_password = password

    @staticmethod
    def __merge_dicts(*dict_args) -> dict:
        """
        Given any number of dicts, shallow copy and merge into a new dict,
        precedence goes to key value pairs in latter dicts

        Args:
            *dict_args: argument dictionary

        Returns:
            Return a merged dictionary
        """
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        return result

    def _camera_command(self, value_cgi, payload: dict):
        """
        Function used to send commands to the camera
        Args:
            payload: argument dictionary for camera control

        Returns:
            Returns the response from the device to the command sent

        """

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

        if abs(360 - current_pan) < 0.5 or current_pan < 0.5:

            # This if statement is necessary for when absolute pan is zero. When the camera position
            # is requested, the query returned was either approximately zero or 360. This statement
            # sets out to fix that bug by forcing the current pan position to be read as zero.

            current_pan = 0

        ptz_list = (current_pan, current_tilt, current_zoom)

        return ptz_list

    def absolute_control(self, pan: float = None, tilt: float = None, zoom: int = None):
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

        self._camera_command('ptzcontrol.cgi', {'msubmenu': 'absolute', 'action': 'control',
                             'Pan': pan, 'Tilt': tilt, 'Zoom': zoom})

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

        if abs(pan-360) < 0.05:

            pan = 0

        finished_position = pan+tilt+zoom

        while abs(current_position - finished_position) > 0.5:

            current_position = np.sum(self.operation_finished())

    def relative_control(self, pan: float = None, tilt: float = None, zoom: int = None):
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

            if (current_pan + pan) < 0:
                pan = 360 - pan

        if tilt is not None:

            # if the relative tilt given exceeds the 90 degree threshold, set the relative tilt
            # equal to the difference that will result in the maximum 90-degree tilt

            if 90 < (current_tilt + tilt):
                tilt = 90 - current_tilt

            # if the relative tilt given exceeds the -20 degree threshold, set the relative tilt
            # equal to the difference that will result in the minimum -20-degree tilt

            if (current_tilt + tilt) < -20:
                tilt = -20 + abs(current_tilt)

        if zoom is not None:

            # if the relative zoom given exceeds the 40 zoom threshold, set the relative zoom
            # equal to the difference that will result in the maximum 40 zoom

            if 40 < (current_zoom + zoom):
                zoom = 40 - current_zoom

            # if the relative zoom given exceeds the 1 degree threshold, set the relative zoom
            # equal the difference that will result in the minimum -20-degree tilt

            if (current_zoom + zoom) < 1:
                zoom = 1 - current_zoom

        if current_pan != 0:
            self._camera_command('ptzcontrol.cgi', {'msubmenu': 'relative', 'action': 'control',
                                                    'Pan': pan, 'Tilt': tilt, 'Zoom': zoom})

        if current_pan == 0:
            self._camera_command('ptzcontrol.cgi', {'msubmenu': 'absolute', 'action': 'control',
                                                    'Pan': pan, 'Tilt': tilt, 'Zoom': zoom})

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

        finished_position = pan + tilt + zoom + current_position

        while abs(current_position - finished_position) > 0.5:
            current_position = np.sum(self.operation_finished())

    def continuous_control(self, pan: int = None, tilt: int = None, zoom: int = None):
        """
        Operation for continuous Pan/Tilt and Zoom movements.

        Args:
            pan: speed of movement of Pan.
            tilt: speed of movement of Tilt.
            zoom: speed of movement of Zoom.

        Returns:
            Returns the response from the device to the command sent.

        """

        return self._camera_command('ptzcontrol.cgi', {'msubmenu': 'continuous', 'action': 'control',
                                     'Pan': pan, 'Tilt': tilt, 'Zoom': zoom})

    def stop_control(self):
        """
        Operation to stop ongoing pan, tilt and zoom movements of absolute relative and
        continuous type

        Returns:
            Returns the response from the device to the command sent

        """
        return self._camera_command('ptzcontrol.cgi', {'msubmenu': 'stop', 'action': 'control',
                                     'OperationType': 'All'})

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

        relative_zoom = tilewidth / abs(x1-x2)

        final_zoom = current_zoom * relative_zoom

        while abs(current_zoom - final_zoom) > 0.5:
            current_zoom = self.operation_finished()[2]


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

    def moving_to_preset_position(self, presetname: str = None):
        """
        Move to the position associated with the preset on server.

        Args:
            presetname: name of preset position server.

        Returns:
            Returns the response from the device to the command sent

        """
        return self._camera_command('ptzcontrol.cgi', {'msubmenu': 'preset', 'action': 'control',
                                     'PresetName': presetname})

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

        return self._camera_command('attributes.cgi', {})

    def swing_control(self, channel: int = None):
        """
              Move from one preset to another

              Args:
                  command = choose channel

              Returns:
                  Returns the response from the device to the command sent

              """

        return self._camera_command('ptzcontrol.cgi', {'msubmenu': 'swing', 'action': 'control',
                                                       'Channel': channel, 'Mode': 'PanTilt'})

    def applications(self):
        """
              Creates url and shares installed applications information
              Returns:
                  Returns the response from the device to the command sent

              """

        resp = self._camera_command('opensdk.cgi', {'msubmenu': 'apps', 'action': 'view'})
        print(resp.url)
        print(resp.text)

        return resp







    def go_to_server_preset_no(self, number: int = None, speed: int = None):
        """
        Move to the position associated with the specified preset position number.

        Args:
            number: number of preset position server.
            speed: speed move camera.

        Returns:
            Returns the response from the device to the command sent

        """
        return self._camera_command({'gotoserverpresetno': number, 'speed': speed})

    def go_to_device_preset(self, preset_pos: int = None, speed: int = None):
        """
        Bypasses the presetpos interface and tells the device to go directly to the preset
        position number stored in the device, where the is a device-specific preset position number.

        Args:
            preset_pos: number of preset position device
            speed: speed move camera

        Returns:
            Returns the response from the device to the command sent

        """
        return self._camera_command({'gotodevicepreset': preset_pos, 'speed': speed})

    def list_preset_device(self):
        """
        List the presets positions stored in the device.

        Returns:
            Returns the list of presets positions stored on the device.

        """
        return self._camera_command({'query': 'presetposcam'})

    def list_all_preset(self):
        """
        List all available presets position.

        Returns:
            Returns the list of all presets positions.

        """
        resp = self._camera_command({'query': 'presetposall'})
        soup = BeautifulSoup(resp.text, features="lxml")
        resp_presets = soup.text.split('\n')
        presets = []

        for i in range(1, len(resp_presets)-1):
            preset = resp_presets[i].split("=")
            presets.append((int(preset[0].split('presetposno')[1]), preset[1].rstrip('\r')))

        return presets

    def set_speed(self, speed: int = None):
        """
        Sets the head speed of the device that is connected to the specified camera.
        Args:
            speed: speed value.

        Returns:
            Returns the response from the device to the command sent.

        """
        return self._camera_command({'speed': speed})

    def get_speed(self):
        """
        Requests the camera's speed of movement.

        Returns:
            Returns the camera's move value.

        """
        resp = self._camera_command({'query': 'speed'})
        return int(resp.text.split()[0].split('=')[1])

    def info_ptz_commands(self):
        """
        Returns a description of available PTZ commands. No PTZ control is performed.

        Returns:
            Success (OK and system log content text) or Failure (error and description).

        """
        resp = self._camera_command({'info': '1'})
        return resp.text

    def center_move(self, pos_x: int = None, pos_y: int = None, speed: int = None):
        """
        Used to send the coordinates for the point in the image where the user clicked. This
        information is then used by the server to calculate the pan/tilt move required to
        (approximately) center the clicked point.

        Args:
            pos_x: value of the X coordinate.
            pos_y: value of the Y coordinate.
            speed: speed move camera.

        Returns:
            Returns the response from the device to the command sent

        """
        pan_tilt = str(pos_x) + "," + str(pos_y)
        return self._camera_command({'center': pan_tilt, 'speed': speed})

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

    parser.add_argument('-cc', '--continuous_control', type=int, help='to execute and specify "continuous_control" action',
                        nargs='+', choices=range(-6, 7), action=CustomAction)

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

    terminal_control = CameraControl(args.ipAddress, args.username, args.password)  # calling the Class CameraControl

    if args.Stop: # If Stop is True, execute command from CameraControl class body
        terminal_control.stop_control()

    if args.WiperOn: # If WiperOn is True, execute command from CameraControl class body
        terminal_control.aux_control(command='WiperOn')

    if args.HeaterOn: # If HeaterOn is True, execute command from CameraControl class body
        terminal_control.aux_control(command='HeaterOn')

    if args.HeaterOff: # If HeaterOff is True, execute command from CameraControl class body
        terminal_control.aux_control(command='HeaterOff')

    if args.requesting_cameras_position_information: # If requesting_cameras_position_information is True, execute command from CameraControl class body
        terminal_control.requesting_cameras_position_information()

    if args.zoom_out:  # If zoom_out is True, execute command from CameraControl class body
        terminal_control.zoom_out()

    if ordered_args:

        k = 1  # offsets i by 1, to provide the corresponding value[k] to destination[i]

        for i in ordered_args[::2]:  # starts from first position and iterates by two to get next destination

            if i == 'absolute_Zoom':
                # If absolute_Zoom is True, execute command from CameraControl class body

                # ptz_list = terminal_control.operation_finished()
                #
                # current_position = ptz_list[2]

                terminal_control.absolute_control(zoom=ast.literal_eval(ordered_args[k]))
                # print(ordered_args[k])
                #
                # finished_position = format(ast.literal_eval(ordered_args[k]), '.2f')
                #
                # while abs(float(current_position) - float(finished_position)) > 0.05:
                #     ptz_list = terminal_control.operation_finished()
                #     current_position = ptz_list[2]
                #     print(current_position)
                #     print(finished_position)

            if i == 'absolute_Pan':
                terminal_control.absolute_control(pan=ast.literal_eval(ordered_args[k]))

            if i == 'absolute_Tilt':
                terminal_control.absolute_control(tilt=ast.literal_eval(ordered_args[k]))

            if i == 'relative_Zoom':
                terminal_control.relative_control(zoom=ast.literal_eval(ordered_args[k]))

            if i == 'relative_Pan':
                terminal_control.relative_control(pan=ast.literal_eval(ordered_args[k]))

            if i == 'relative_Tilt':
                terminal_control.relative_control(tilt=ast.literal_eval(ordered_args[k]))

            if i == 'continuous_control':
                cc_param = ast.literal_eval(ordered_args[k])

                terminal_control.continuous_control(pan=cc_param[0], tilt=cc_param[1], zoom=cc_param[2])

            if i == 'continuous_control_Zoom':
                terminal_control.continuous_control(zoom=ordered_args[k])

            if i == 'continuous_control_Pan':
                terminal_control.continuous_control(pan=ordered_args[k])
                time.sleep(3)

            if i == 'continuous_control_Tilt':
                terminal_control.continuous_control(tilt=ordered_args[k])
                time.sleep(3)

            if i == 'Left':
                terminal_control.movement_control(direction='Left', movespeed=ordered_args[k])

            if i == 'Right':
                terminal_control.movement_control(direction='Right', movespeed=ordered_args[k])

            if i == 'Up':
                terminal_control.movement_control(direction='Up', movespeed=ordered_args[k])

            if i == 'Down':
                terminal_control.movement_control(direction='Down', movespeed=ordered_args[k])

            if i == 'LeftUp':
                terminal_control.movement_control(direction='LeftUp', movespeed=ordered_args[k])

            if i == 'RightUp':
                terminal_control.movement_control(direction='RightUp', movespeed=ordered_args[k])

            if i == 'LeftDown':
                terminal_control.movement_control(direction='LeftDown', movespeed=ordered_args[k])

            if i == 'RightDown':
                terminal_control.movement_control(direction='RightDown', movespeed=ordered_args[k])

            if i == 'area_Zoom':
                zoom_param = ast.literal_eval(ordered_args[k])

                TileWidth = None

                TileHeight = None

                X1, X2, Y1, Y2 = zoom_param[:4]  # gives first zoom parameters

                if len(zoom_param) > 4:

                    TileHeight, TileWidth = zoom_param[4:]

                terminal_control.area_zoom(x1=X1, x2=X2, y1=Y1, y2=Y2, tilewidth=TileWidth, tileheight=TileHeight)

            k = k + 2

if __name__ == '__main__':
    main()