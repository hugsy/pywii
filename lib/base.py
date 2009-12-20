from config import DISCOVER_DURATION
from bluetooth.btcommon import BluetoothError
from bluetooth import discover_devices

def find_bluetooth_devices():
    """
    Look for all bluetooth devices around.
    """
    devices = []
    print ("Looking for Bluetooth device for %d seconds" % DISCOVER_DURATION)
    try :
        devices = discover_devices(duration=DISCOVER_DURATION,
                                   lookup_names=True)
    except BluetoothError, be:
        print ("%s" % str(be))
        devices = []
        
    return devices


def find_wiimotes():
    """
    From all bluetooth devices, find Wiimote based on MAC address prefix and
    pseudo-named interface
    """
    
    return [ dev \
                 for dev in find_bluetooth_devices() \
                 if dev[0].startswith("00:1") and dev[1].find("Nintendo") != -1 ]
                

