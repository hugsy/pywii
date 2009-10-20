from config import DISCOVER_DURATION
from bluetooth.btcommon import BluetoothError
from bluetooth import discover_devices

def find_bluetooth_devices():
    """
    Look for all bluetooth devices around.
    """
    devices = []
    try :
        devices = discover_devices(duration=DISCOVER_DURATION,
                                   lookup_names=True)
    except BluetoothError, be:
        print ("%s" % str(be))
        devices = []
        
    return devices


def find_wiimotes():
    """
    From all bluetooth devices, find Wiimote based on MAC address prefix
    """
    print ("Searching for Wiimotes around for %d seconds" % DISCOVER_DURATION)
    wm = []
    for dev in find_bluetooth_devices():
        if dev[0].startswith("00:19:1D"):
            print ("Wiimote found ! \n\t")
            print ("%s" % dev)
            wm.append(dev)
                
    return wm

