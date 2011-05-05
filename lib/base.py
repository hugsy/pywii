from bluetooth.btcommon import BluetoothError
from bluetooth import discover_devices


def find_bluetooth_devices(timeout):
    """
    Look for all bluetooth devices around.
    """
    devices = []
    print ("Discovering Bluetooth device (%d seconds)" % timeout)
    
    try :
        devices = discover_devices(duration=timeout,lookup_names=True)
    except BluetoothError, be:
        print ("%s" % str(be))
        devices = []
        
    return devices


def find_wiimotes(timeout):
    """
    From all bluetooth devices, find Wiimote based on MAC address prefix and
    pseudo-named interface
    """
    return [ dev \
                 for dev in find_bluetooth_devices(timeout) \
                 if dev[0].startswith("00:1") and dev[1].find("Nintendo") != -1 ]
                

