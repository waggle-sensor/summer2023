# **HANWHA_API**

Hello and welcome! Here are some examples of how to use this api for the XNP-6400RW PTZ camera:

## **Required Python Libraries**
- import argparse
- import requests
- from requests.auth import HTTPDigestAuth

## **Terminal Command Examples**

### Pan to the absolute position of pan 20&deg;

In terminal write:

- In long form:
- $ python3 main.py --ipAddress **Device IP** --username <username> --password <password> --absolute_Pan 20
- In short form:
- $ python3 main.py -ip <Device IP> -un <username> -pw <password> -ap 20

### Relative Tilt -30&deg; 

In terminal write:

- In long form:
- $ python3 main.py --ipAddress <Device IP> --username <username> --password <password> --relative_Tilt -30
- In short form:
- $ python3 main.py -ip <Device IP> -un <username> -pw <password> -rt -30

### Continuous control of Pan at a movement speed of 5

In terminal write:

- In long form:
- $ python3 main.py --ipAddress <Device IP> --username <username> --password <password> --continuous_control_Pan 5
- In short form:
- $ python3 main.py -ip <Device IP> -un <username> -pw <password> -ccp 5

### Pan to the absolute position of pan 20&deg;

In terminal write:

- In long form:
- $ python3 main.py --ipAddress <Device IP> --username <username> --password <password> --absolute_Pan 20
- In short form:
- $ python3 main.py -ip <Device IP> -un <username> -pw <password> -ap 20

### Stop all action;

In terminal write:

- In long form:
- $ python3 main.py --ipAddress <Device IP> --username <username> --password <password> --Stop
- In short form:
- $ python3 main.py -ip <Device IP> -un <username> -pw <password> -s
