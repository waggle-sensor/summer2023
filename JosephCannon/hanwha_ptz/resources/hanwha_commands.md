#### DEVICE INFORMATION VIEW:
```
http://camera-ptz-rgb-hanwha/stw-cgi/system.cgi?msubmenu=deviceinfo&action=view 
```

#### ABSOLUTE CONTROL:
_**Syntax:** http://<Device IP>/stw-cgi/ptzcontrol.cgi?msubmenu=absolute&action=control[&<parameter>=<value>]_
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzcontrol.cgi?msubmenu=absolute&action=control&Pan=1
```

#### RELATIVE CONTROL:
_**Syntax:** http://<Device IP>/stw-cgi/ptzcontrol.cgi?msubmenu=relative&action=control[&<parameter>=<value>]_
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzcontrol.cgi?msubmenu=relative&action=control&Tilt=1 
```

#### CONTINUOUS CONTROL:
_**Syntax:** http://<Device IP>/stw-cgi/ptzcontrol.cgi?msubmenu=continuous&action=control[&<parameter>=<value>]_
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzcontrol.cgi?msubmenu=continuous&action=control&Pan=5 
```
#### REQUESTING CAMERA’S POSITION INFORMATION:
_**Syntax:** http://<Device IP>/stw-cgi/ptzcontrol.cgi?msubmenu=query&action=view[&<parameter>=<value>]_
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzcontrol.cgi?msubmenu=query&action=view&Query=Pan,Tilt,Zoom
```
#### ATTRIBUTES INFORMATION:
_**Syntax:** http://<Device IP>/stw-cgi/attributes.cgi_
```
http://camera-ptz-rgb-hanwha/stw-cgi/attributes.cgi
```
Syntax to access only the CGI: http://<Device IP>/stw-cgi/attributes.cgi/<cgi name>
```
http://camera-ptz-rgb-hanwha/stw-cgi/attributes.cgi/system
```
```
http://camera-ptz-rgb-hanwha/stw-cgi/attributes.cgi/network
```
```
http://camera-ptz-rgb-hanwha/stw-cgi/attributes.cgi/
```

#### MOVING TO PRESET POSITION:
_**Syntax:** http://<Device IP>/stw-cgi/ptzcontrol.cgi?msubmenu=preset&action=control[&<parameter>=<value>]_
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzcontrol.cgi?msubmenu=preset&action=view&Channel=0
```
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzcontrol.cgi?msubmenu=preset&action=control&Preset=0
```

#### SWING CONTROL: 
_**Syntax:** http://<Device IP>/stw-cgi/ptzcontrol.cgi?msubmenu=swing&action=control[&<parameter>=<value>]_
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzcontrol.cgi?msubmenu=swing&action=control&Channel=0&Mode=Pan 
```
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzcontrol.cgi?msubmenu=swing&action=control&Channel=0&Mode=PanTilt 
```
#### GROUP CONTROL:
_**Syntax:** http://<Device IP>/stw-cgi/ptzcontrol.cgi?msubmenu=group&action=control[&<parameter>=<value>]_
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzcontrol.cgi?msubmenu=group&action=control&Channel=0
```
#### TOUR CONTROL: 
_**Syntax:** http://<Device IP>/stw-cgi/ptzcontrol.cgi?msubmenu=tour&action=control[&<parameter>=<value>]_
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzcontrol.cgi?msubmenu=tour&action=control&Channel=0&Tour=1&Mode=Start 
```
#### TRACE CONTROL:
_**Syntax:** http://<Device IP>/stw-cgi/ptzcontrol.cgi?msubmenu=trace&action=control[&<parameter>=<value>]_
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzcontrol.cgi?msubmenu=trace&action=control&Channel=0&Trace=1&Mode=Start 
```
#### MOVING TO HOME POSITION:
_**Syntax:** http://<Device IP>/stw-cgi/ptzcontrol.cgi?msubmenu=home&action=control[&<parameter>=<value>]_
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzcontrol.cgi?msubmenu=home&action=control&Channel=0 
```
#### AREA ZOOM:
_**Syntax:** http://<Device IP>/stw-cgi/ptzcontrol.cgi?msubmenu=areazoom&action=control[&<parameter>=<value>]_
Defining the Relative Coordinates of the Zoom Area:
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzcontrol.cgi?msubmenu=areazoom&action=control&X1=100&X2=200&Y1=100&Y2=200 
```
#### STOP CONTROL:
_**Syntax:** http://<Device IP>/stw-cgi/ptzcontrol.cgi?msubmenu=stop&action=control[&<parameter>=<value>]_
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzcontrol.cgi?msubmenu=stop&action=control&OperationType=All 
```
#### MOVEMENT CONTROL:
_**Syntax:** http://<Device IP>/stw-cgi/ptzcontrol.cgi?msubmenu=move&action=control[&<parameter>=<value>]_
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzcontrol.cgi?msubmenu=move&action=control&Direction=LeftDown&MoveSpeed=2 
```
#### AUX CONTROL:
_**Syntax:** http://<Device IP>/stw-cgi/ptzcontrol.cgi?msubmenu=aux&action=control[&<parameter>=<value>]_
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzcontrol.cgi?msubmenu=aux&action=control&Command=HeaterOn 
```
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzcontrol.cgi?msubmenu=aux&action=control&Command=HeaterOff 
```
#### DIGITAL AUTO TRACKING:
_**Syntax:** http://<Device IP>/stw-cgi/ptzcontrol.cgi?msubmenu=digitalautotracking&action=control[&<parameter>=<value>]_
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzcontrol.cgi?msubmenu=digitalautotracking&action=control&Profile=2&Mode=Start
```
#### RS485 COMMAND:
_**Syntax:** http://<Device IP>/stw-cgi/ptzcontrol.cgi?msubmenu=rs485Command&action=control[&<parameter>=<value>]_
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzcontrol.cgi?msubmenu=rs485Command%20&action=control&Channel=1&Command=AA1BC02B !!!!
```
#### OSD MENU:
_**Syntax:** http://<Device IP>/stw-cgi/ptzcontrol.cgi?msubmenu=osdmenu&action=control[&<parameter>=<value>]_
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzcontrol.cgi?msubmenu=osdmenu&action=view&Channel=1 !!!
```
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzcontrol.cgi?msubmenu=osdmenu&action=control&Channel=1&Mode=Up !!!
```

### PTZ CONFIGURATION:

#### SWING SETUP:
_**Syntax:** http://<Device IP>/stw-cgi/ptzcontrol.cgi?msubmenu=swing&action=control[&<parameter>=<value>]_
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzconfig.cgi?msubmenu=swing&action=view&Channel=0 
```
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzconfig.cgi?msubmenu=swing&action=set&Channel=0&Mode=Pan&FromPreset=1&ToPreset=2%20&Speed=1&DwellTime=1 
```
#### GROUP SETUP:
_**Syntax:** http://<Device IP>/stw-cgi/ptzcontrol.cgi?msubmenu=group&action=control[&<parameter>=<value>]_
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzconfig.cgi?msubmenu=group&action=view&Channel=0 
```
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzconfig.cgi?msubmenu=group&action=add&Channel=0&Group=1&PresetSequence=1&Preset=%202&Speed=60&DwellTime=2
```
#### TOUR SETUP:
_**Syntax:** http://<Device IP>/stw-cgi/ptzcontrol.cgi?msubmenu=tour&action=control[&<parameter>=<value>]_
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzconfig.cgi?msubmenu=tour&action=view&Channel=0 
```

#### TRACE SETUP:
_**Syntax:** http://<Device IP>/stw-cgi/ptzcontrol.cgi?msubmenu=trace&action=control[&<parameter>=<value>]_
```
http://camera-ptz-rgb-hanwha/stw-cgi/ptzconfig.cgi?msubmenu=trace&action=view&Channel=0
```
