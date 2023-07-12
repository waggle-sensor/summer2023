# Ubiquiti_EdgeSwitch_API

Hello and welcome! This library is designed to provide control and configuration of Ubiquiti EdgeSwitches using .ssh calls.

**(Ubiquiti)** API support

## **Required Python Libraries**
- from paramiko import SSHClient, AutoAddPolicy
- from rich import print, pretty, inspect

## Execution

Example of use:

````
from source import ubiquiti_control

````



## Functions
### show


# From Terminal

Here are some examples of how to use the EdgeSwitch network directly from terminal:

## Terminal Command Examples

### Access Network;

In terminal write:
````

- $ ssh **username**@**Device IP** -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedAlgorithms=+ssh-rsa

- **username**@**Device IP**'s password: **password**

````