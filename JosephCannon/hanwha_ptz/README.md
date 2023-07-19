# HANWHA_Sunapi

Hello and welcome! This library is designed to provide control and configuration of Hanwha cameras using the Sunapi protocol.

**(Hanwha SDK)** SUNAPI support must be pre-authorized by Hanwha and is only available for Nx Witness VMS and select Powered-by-Nx products.

**(Hanwha SDK)** provides functionality for taking images; controlling Pan, Tilt, & Zoom; retrieve and control internal settings, record and retrieve video to/from the SD card, and much more.

## **Required Python Libraries**
- import logging
- import sys
- import argparse
- import ast
- import time
- import numpy as np
- import math
- import requests
- from requests.auth import HTTPDigestAuth
- from bs4 import BeautifulSoup

## Execution

Example of use:

````
from source import sunapi_control


Camera1 = sunapi_control.CameraControl('<ip_address>', '<username>', '<password>')

Camera1.absolute_control(80, 30, 20)
Camera1.relative_control(pan=80)

````



## Functions
### Sunapi Control

*	`absolute_control(pan, tilt, zoom)` - Operation to move Pan, Tilt, or Zoom to an absolute destination.
	-	pan (float): pans the device relative to the (0,0) position. Values (0.0, ... 360.0)
	-	tilt (float): tilts the device relative to the (0,0) position. Values(-20.0, ... 90.0)
	-	zoom (float): zooms the device n steps. Values (1.0, ... 40.0)
	
*	`relative_control(pan, tilt, zoom)` - Operation to move Pan, Tilt, or Zoom to a destination relative to current position.
	-	pan (float): pans the device relative to the current position. Values (-360.0, ... 360.0)
	-	tilt (float): tilts the device relative to the current position. Values(-110.0, ... 110.0)
	-	zoom (float): zooms the device n steps from current zoom position. Values (-40.0, ... 40.0)

*	`continuous_control(normalized_speed, pan, tilt, zoom)` - Operation for continuous Pan, Tilt, and Zoom movements.
	-	normalized_speed (bool): Enables or disables the normalized speed range for Pan, Tilt, and Zoom. If normalized_speed is not sent, or set as False, the Pan, Tilt, and Zoom speed
range will be device dependent values; If normalized_speed is set as True, the speed values for Pan, Tilt, and Zoom will be in the range of -100 to 100. normalized_speed must be sent together with Pan, Tilt, or Zoom.
	-	pan (int): Speed of Pan movement. (0, ... 6) or (-100, ... 100)
	-	tilt (int): Speed of Tilt movement. (0, ... 6) or (-100, ... 100)
	-	zoom (int): Speed of Zoom movement (0, ... 6) or (-100, ... 100)
	
*	`stop_control()` - Operation to stop ongoing Pan, Tilt, and Zoom movements

*	`area_zoom(x1, x2, y1, y2, tilewidth, tileheight)` - Operation zooms in on an area specified by boundaries x1 (int) and x2 (int), as well as y1 (int) to y2 (int). The default pixel dimensions are 10,000 by 10,000. The upper-left corner of the image is the (0, 0) position and the bottom-right corner of the image is the (10,000, 10,000) position. Changes can be made by adjusting the tilewidth (int) and tileheight (int). Can only zoom in on an area at a minimum of 50 by 50 pixels in dimension.

*	`movement_control(direction, movespeed)` - Continuously moves the device in the specified direction.
	-	direction (str): Offered directions 'home', 'up', 'down', 'left', 'right', 'upleft', 'upright', 'downleft', 'downright'
	-	movespeed (int): Speed of movement. (0, ... 6)
	
*	`moving_to_home_position(channel)` - Orient device to preset home position.
	-	Channel (int): Select specified camera channel to send command.
	
*	`requesting_cameras_position_information()` - Operation requests and returns PTZ status information such as Pan, Tilt, Zoom, Zoom_Pulse, and Channel.

*	`moving_to_preset_position(presetname)` - Orients camera to a preset position.
	-	presetname (str): Provide the assigned name of the preset position
	
*	`zoom_out()` - Zooms out to 1x zoom

*	`aux_control(command)` - Executes functions WiperOn, HeaterOn, and HeaterOff.
	-	command (str): Choose from one of the specified functions.
	
*	`attributes_information()` - Opens a webbrowser and returns the url link of the atttributes information for the connected device.

*	`swing_control(channel)` - Swings from one preset to another.
	-	channel (int): Select channel to issue the swing command
	
*	`applications()` - Returns the installed applications information


# From Terminal

Here are some examples of how to use the Sunapi from terminal for the XNP-6400RW PTZ camera:

## Terminal Command Examples

### Pan to the absolute position of pan 20&deg;

In terminal write:
````
- In long form:
- $ python3 main.py --ipAddress <Device IP> --username <username> --password <password> --absolute_Pan 20
- In short form:
- $ python3 main.py -ip <Device IP> -un <username> -pw <password> -ap 20
````

### Relative Tilt -30&deg; 

In terminal write:
````
- In long form:
- $ python3 main.py --ipAddress <Device IP> --username <username> --password <password> --relative_Tilt -30
- In short form:
- $ python3 main.py -ip <Device IP> -un <username> -pw <password> -rt -30
````

### Continuous control of Pan at a movement speed of 5

In terminal write:
````
- In long form:
- $ python3 main.py --ipAddress <Device IP> --username <username> --password <password> --continuous_control_Pan 5
- In short form:
- $ python3 main.py -ip <Device IP> -un <username> -pw <password> -ccp 5
````

### Pan to the absolute position of pan 20&deg;

In terminal write:
````
- In long form:
- $ python3 main.py --ipAddress <Device IP> --username <username> --password <password> --absolute_Pan 20
- In short form:
- $ python3 main.py -ip <Device IP> -un <username> -pw <password> -ap 20
````

### Stop all action;
````
In terminal write:

- In long form:
- $ python3 main.py --ipAddress <Device IP> --username <username> --password <password> --Stop
- In short form:
- $ python3 main.py -ip <Device IP> -un <username> -pw <password> -s
````
###Disclaimers:

In terminal:

- If camera is in continuous move, user must send stop command before doing a relative move. It is also recommended for an absolute command, area zoom, etc.