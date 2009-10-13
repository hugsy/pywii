import threading
import time
import logging
from bluetooth.bluez import BluetoothSocket, BluetoothError, L2CAP

from config import *

import lib.modules.buttons as buttons
import lib.modules.accelerometer as accelerometer
import lib.modules.led as led
import lib.modules.rumble as rumble


logging.basicConfig()
logger = logging.getLogger("Wiimote.core")
logger.setLevel(logging.DEBUG)


class Wiimote(threading.Thread):
    """
    this object manages all wiimote interactions. 
    """

    DISCONNECTED = 0x0
    CONNECTED = 0x1
    STATUS = {
        DISCONNECTED : "Disconnected",
        CONNECTED : "Connected",
        }
    MODE_STATUS = 0x20
    MODE_BUTTON = 0x30
    MODE_BUTTON_ACCELEROMETER = MODE_BUTTON & 0x1

    def __init__ (self, mac, name, number):
        threading.Thread.__init__(self)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Creating a new wiimote thread")
        self.mac = mac
        self.name = name
        self.state = self.DISCONNECTED
        self.receive_socket = None
        self.control_socket = None
        self.number = number

        self.mode = self.MODE_BUTTON
        self.feature = 0x0000 

        # accelerometer information
        self.x = 0
        self.y = 0
        self.z = 0

    def __rep__(self):
        desc = "Description of Wiimote-%d: \n" % self.number
        desc += "\tMac address: %s\n" % self.mac
        desc += "\tName: %s\n" % self.name
        desc += "\tState: %s\n" % self.STATUS[self.state]
        desc += "\n"
        return desc

    def __str__(self):
        desc = "Wiimote-%d" % self.number
        desc += "(%s)" % self.STATUS[self.state]
        
    def run(self):
        """
        Thread main program :
        this function establishes a BT connection and if succeeded,
        starts reading data.
        """
        if logger.isEnabledFor(logging.DEBUG):
            logger.info("Running")
            
        (self.receive_socket, self.control_socket) = self.establish()
        if self.receive_socket is None or self.control_socket is None : 
            logger.critical("Failed to establish connection")
            self.change_state_notification(self.DISCONNECTED)
            return

        self.change_state_notification(self.CONNECTED)

        ## module activation & test
        rumble.setTimeRumble(self, 1) # activates 1 sec rumbling
        led.blink(self, 1, 1) # blinks 1 time of 1 second each
        
        ##  listen to received data
        self.read_data()

    def change_state_notification(self, newState):
        if newState != self.state:
            self.state = newState
            logger.info("Change status to: %s" % self.STATUS[self.state])
        
    def establish (self):
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
        self.change_state_notification(self.DISCONNECTED) 
        logger.info('Gracefully disconnected')

    def read_data(self):
        """
        This function reads data to the wiimote and interprets
        every frame.
        """
        while self.state == self.CONNECTED :
            try:
                raw_data = self.receive_socket.recv(23)
                frame = [ ord(x) for x in raw_data ]                
                chaine = ''   

                # this shit below is just for debug
                if logger.isEnabledFor(logging.DEBUG):
                    chaine = [ '0x%x' % x for x in frame ]
                    logger.debug('Frame received: %s' % chaine) 

                # we need to convert those bytes into readable data
                self.parse_frame(frame)

            except BluetoothError:
                pass
            
        return


    def parse_frame (self, bytes):
        """
        Applies one or more frame action(s).
        First received byte is always 0xa1.
        """
        if bytes[1] == self.MODE_STATUS:
            self.get_status(bytes[2:])

        # button handling            
        if bytes[1] & self.MODE_BUTTON:
            buttons_bytes = bytes[2:4]

        for idx in range(0,2) :
            buttons.execute(buttons_bytes[idx], idx, self)

        # accelerometer handling            
        if bytes[1] & self.MODE_BUTTON_ACCELEROMETER :
            acceler_bytes = bytes[4:7]            
            
        if bytes[1] == self.MODE_BUTTON_ACCELEROMETER :
            accelerometer.update(acceler_bytes)

    def send_control_frame(self, bytes):
        """
        Send a control frame on signalisation channel
        """
        # control frame always start with 0x52
        frame = chr(0x52)
        frame += ''.join(bytes)
        if logger.isEnabledFor(logging.DEBUG):
            logger.info('Sending %d byte control frame' % len(frame))
        self.control_socket.send(frame)

    def change_feature(self, mode):
        """
        Allows to change the Wiimote features.
        Currently implemented supported: led, rumble.
        """
        # change feature frame starts with 0x52 0x11
        logger.info("Switching feature to 0x%x" % mode)
        features_hexa = chr(0x11)
        mode_hexa = chr(mode)
        hexa_table = (features_hexa, mode_hexa)
        self.send_control_frame(hexa_table)

    def change_mode(self, mode, persist_data=False):
        """
        Allows to change mode:
        2 modes for now : buttons (default) / accelerometer
        """
        # change mode frame start with 0x52 0x12
        logger.info("Switching mode to 0x%x" % mode)
        mode_byte = chr(0x12)

        if persist_data :
            byte_mode_1=chr(0x04)
        else :
            byte_mode_1=chr(0x00)

        byte_mode_2 = chr(mode)
        byte_table = (mode_byte, byte_mode_1, byte_mode_2)
        self.send_control_frame(byte_table)

    def request_status(self):
        """
        Request Wiimote status (battery level, connected extensions,
        speaker/camera status ...)
        Note : this will turn rumble off if activated
        """
        statusFrame = chr(0x15) + chr(0x00)
        self.send_control_frame(statusFrame)

    def get_status(self, report):
        """
        Display Wiimote status.
        """
        led_nibble = report[2] & 0xf0
        stats_nibble = report[2] & 0x0f

        stats = {
            "Battery" : report[5],
            "Low Battery" : stats_nibble & 0x01,
            "Extension" : stats_nibble & 0x02,
            "Speaker" : stats_nibble & 0x04,
            "Camera" : stats_nibble & 0x08,
            }
            
        status = "Wiimote-%d: %s\n" % (self.number, self.name)
        for k in stats.keys() :
            if k == "Battery" : v = "%d" % stats[k]
            elif stats[k] : v = "On"
            else : v = "Off"
            status += "%s : %s\n" % (k,v)
        
        print (status)
