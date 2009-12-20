import threading
import time
import logging

from config import SOCK_TIMEOUT_DURATION

import lib.modules.buttons as buttons
import lib.modules.accelerometer as accelerometer
import lib.modules.led as led
import lib.modules.rumble as rumble
from lib.modules.speaker import Speaker

logging.basicConfig()
logger = logging.getLogger("Wiimote.core")
logger.setLevel(logging.DEBUG)

try:
    from bluetooth.bluez import BluetoothSocket
    from bluetooth.bluez import BluetoothError
    from bluetooth.bluez import L2CAP
except ImportError:
    logger.critical ("No Pybluez module found.")
    logger.critical ("Please install latest PyBluez lib (https://code.google.com/p/pybluez/)")
    exit(1)


DISCONNECTED = 0x0
CONNECTED    = 0x1
STATUS       = {
    DISCONNECTED : "Disconnected",
    CONNECTED    : "Connected",
    }
MODE_STATUS  = 0x20
MODE_BUTTON  = 0x30
MODE_BUTTON_ACCELEROMETER = MODE_BUTTON | 0x1

class Wiimote(threading.Thread):
    """
    This object manages all wiimote interactions. Basic mechanisms:
    - initializes wiimote
    - establishes 2 bluetooth communication channels (data & info)
    - if succeeded, runs a loop to read data unless user asks for
    disconnection

    Features that have been added to handle :
    - wiimote buttons, which integrated since 0.2. Button actions 
    must be specified in the configuration file
    - accelerometer, with the possibility to perform actions upon
    certains wiimote movements
    - LED activation
    - Rumble activation

    Yet to come :
    - Speaker usage
    - Infra-red camera interaction
    """

    def __init__ (self, mac, name, number):
        threading.Thread.__init__(self)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Creating a new wiimote thread")

        # wiimote attributes
        self.mac            = mac
        self.name           = name
        self.state          = DISCONNECTED
        self.receive_socket = None
        self.control_socket = None
        self.number         = number

        # enable button mode w/ no extra feature
        self.mode           = MODE_BUTTON
        self.feature        = 0x00

        # accelerometer information
        self.x              = 0
        self.y              = 0
        self.z              = 0

        # speaker implementation
        # self.speaker    = Speaker(self)
        

    def __repr__(self):
        desc  = "Description of Wiimote-%d: \n" % self.number
        desc += "\tMac address: %s\n" % self.mac
        desc += "\tName: %s\n" % self.name
        desc += "\tState: %s\n" % STATUS[self.state]
        desc += "\n"
        return desc

    def __str__(self):
        desc = "Wiimote-%d" % self.number
        desc += "(%s)" % STATUS[self.state]
        return desc
        
    def run(self):
        """
        Thread main program :
        this function establishes a BT connection and if succeeded,
        starts reading data.
        """
        if logger.isEnabledFor(logging.DEBUG):
            logger.info("Starting %s" % str(self))

        while True :
            (self.receive_socket, self.control_socket) = self.establish()
            if self.receive_socket is None or self.control_socket is None : 
                logger.critical("Failed to establish connection")
                self.set_state(DISCONNECTED)
                logger.info("Retrying in 5 seconds")
                time.sleep(5)
                continue

            self.set_state(CONNECTED)

            # module activation & test
            rumble.setTimeRumble(self, 1) # activates 1 sec rumbling
            led.blink(self, 1, 1) # blinks 1 time of 1 second each
        
            # listen for data
            self.read_data()

            # if asked to close connection
            if self.get_state() == DISCONNECTED :
                return 

            
    def set_state (self, newState):
        if newState != self.state:
            self.state = newState
            logger.info("Change status to: %s" % STATUS[self.state])

            
    def get_state(self):
        return self.state

    
    def establish(self):
        """
        this function is used to establish_connection with the wiimote
        return None if cannot be done
        """
        c_sock = BluetoothSocket(L2CAP)
        r_sock = BluetoothSocket(L2CAP)

        try :
            c_sock.connect((self.mac, 0x11)) # 0x11 : control channel
            r_sock.connect((self.mac, 0x13)) # 0x13 : reception channel
            r_sock.settimeout(SOCK_TIMEOUT_DURATION)
        except BluetoothError, be:
            logger.error("Failed connecting: %s" % be)
            c_sock.close()
            r_sock.close()
            c_sock = None 
            r_sock = None

        return (r_sock, c_sock)

    
    def close(self):
        """
        Killing connection nicely. The good way to leave !
        """
        self.receive_socket.close()
        self.control_socket.close()
        self.set_state(DISCONNECTED) 
        logger.info('Gracefully disconnected')

        
    def read_data(self):
        """
        This function reads data to the wiimote and interprets
        every frame.
        """
        self.request_status()
        
        while self.get_state() == CONNECTED :
            try:
                raw_data = self.receive_socket.recv(23)
                if not raw_data :
                    continue

                frame = [ ord(x) for x in raw_data ]
                if len(frame) < 2:
                    continue

                # this hack below is just for debug
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug('Frame received: %s' % [ '0x%x' % x for x in frame ] )

                # we need to convert those bytes into readable data
                self.parse_frame(frame)

            except BluetoothError:
                pass


    def parse_frame (self, bytes):
        """
        Applies one or more frame action(s).
        First received byte is always 0xa1.
        """
        # show wiimote status report
        if bytes[1] == MODE_STATUS:
            self.print_status(bytes[2:])

        # button handling            
        if bytes[1] & MODE_BUTTON:
            buttons_bytes = bytes[2:4]

        for idx in range(2) :
            buttons.execute(buttons_bytes[idx], idx, self)

        # accelerometer handling            
        if bytes[1] & MODE_BUTTON_ACCELEROMETER :
            acceler_bytes = bytes[4:7]            
            
        if bytes[1] == MODE_BUTTON_ACCELEROMETER :
            accelerometer.update(acceler_bytes)

    def send_data(self, frame):
        """
        Only send the frame over the signalisation channel
        """
        if logger.isEnabledFor(logging.DEBUG):
            chaine = [ '0x%x' % ord(x) for x in frame ]
            logger.debug('Frame sent: %s' % chaine) 
        
        frame = ''.join(frame)
        self.control_socket.send(frame)
        
    def send_control_frame(self, bytes):
        """
        Prepare a control frame on signalisation channel
        """
        # control frame always start with 0x52
        bytes.insert(0, chr(0x52))
        self.send_data(bytes)

    def change_feature(self, mode):
        """
        Allows to change the Wiimote features.
        Currently implemented supported: led, rumble.
        """
        # change feature frame starts with 0x52 0x11
        logger.info("Switching feature to 0x%x" % mode)
        features_code = chr(0x11)
        mode_code = chr(mode)
        bytes = [features_code, mode_code]
        self.send_control_frame(bytes)

    def change_mode(self, mode, persist_data=False):
        """
        Allows to change mode:
        2 modes for now : buttons (default) / accelerometer
        """
        # change mode frame start with 0x52 0x12
        logger.info("Switching mode to 0x%x" % mode)
        mode_byte = chr(0x12)

        if persist_data :
            byte_mode_1 = chr(0x04)
        else :
            byte_mode_1 = chr(0x00)

        byte_mode_2 = chr(mode)
        bytes = [mode_byte, byte_mode_1, byte_mode_2]
        self.send_control_frame(bytes)

    def request_status(self):
        """
        Request Wiimote status (battery level, connected extensions,
        speaker/camera status ...)
        Note : this will turn rumble off if activated
        """
        statusFrame = [chr(0x15), chr(0x00)]
        self.send_control_frame(statusFrame)

    def print_status(self, report):
        """
        Display Wiimote status.
        """
        led_nibble = report[2] & 0xf0
        stats_nibble = report[2] & 0x0f

        stats = {
            "Battery"      : report[5],
            "Low Battery"  : stats_nibble & 0x01,
            "Extension"    : stats_nibble & 0x02,
            "Speaker"      : stats_nibble & 0x04,
            "Camera"       : stats_nibble & 0x08,
            }
            
        status = str(self) + "\n"
        
        for k in stats.keys() :
            if k == "Battery" : v = "%d" % stats[k]
            elif stats[k] : v = "On"
            else : v = "Off"
            status += "%16s : %10s\n" % (k,v)
        
        print (status)

        
    def write_registers(self, address_bytes, data_bytes):
        """
        Write len(data_bytes) bytes at offset pointed by address_bytes
        """
        bytes = [chr(0x16), chr(0x04)]
        bytes += [ chr(x) for x in address_bytes ]
        bytes.append(chr(len(data_bytes)))
        bytes += [ chr(x) for x in data_bytes ]

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Write %s at %s" % (data_bytes, address_bytes))
        
        self.send_control_frame(bytes)
        
