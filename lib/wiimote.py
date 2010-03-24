import threading
import time
import logging
import sys
from subprocess import Popen

try:
    # PyBluez is required
    from bluetooth.bluez import BluetoothSocket
    from bluetooth.bluez import BluetoothError
    from bluetooth.bluez import L2CAP
except ImportError:
    sys.stderr.write ("No Pybluez module found.")
    sys.stderr.write ("Please install latest PyBluez lib (https://code.google.com/p/pybluez/)")
    exit(1)


from lib.modules.buttons import ButtonsMap
from lib.modules.accelerometer import Accelerometer
from lib.modules.led import Led
from lib.modules.rumble import Rumble
from lib.modules.speaker import Speaker


DISCONNECTED = 0x00
CONNECTED    = 0x01
STATUS       = {
    DISCONNECTED : "Disconnected",
    CONNECTED    : "Connected",
    }

MODE_STATUS  = 0x20
MODE_BUTTON  = 0x30
MODE_BUTTON_ACCELEROMETER = 0x31


class Wiimote(threading.Thread):
    """
    This object manages all wiimote interactions. Basic mechanisms:
    - initializes wiimote
    - establishes 2 bluetooth communication channels (data & info)
    - if succeeded, runs a loop to read data unless user asks for
    disconnection

    Can now use modules embedded on the wiimote, such as the rumble, or
    buttons keymap. More modules are being added.
    """

    def __init__ (self, mac, name, number, cfg):
        threading.Thread.__init__(self)

        self.cfg = cfg

        # logging everything
        logging.basicConfig()
        self.logger = logging.getLogger("Wiimote.core")
        self.logger.setLevel(self.cfg.DEBUG_LEVEL)

        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug("Creating a new wiimote thread")

        
        # wiimote attributes
        self.mac             = mac
        self.name            = name
        self.state           = DISCONNECTED
        self.receive_socket  = None
        self.control_socket  = None
        self.number          = number

        # enable button mode w/ no extra feature
        self.mode           = MODE_BUTTON
        self.feature        = 0x00

        # accelerometer information
        self.accelerometer  = None
        self.x              = 0
        self.y              = 0
        self.z              = 0

        # led implementation
        self.led        = None

        # rumble implementation
        self.rumble     = None

        # speaker implementation
        self.speaker    = None


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

        try_left = 5
        
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.info("Starting %s" % str(self))

        while True :
            (self.receive_socket, self.control_socket) = self.connect()
            if self.receive_socket is None or self.control_socket is None :
                try_left -= 1
                if not try_left :
                    return

                self.logger.critical("Failed to establish connection")
                self.set_state(DISCONNECTED)
                self.logger.info("Retrying in 5 seconds")
                time.sleep(5)
                continue

            # here, we have established link 
            self.set_state(CONNECTED)

            # module activation & test
            self.buttons = ButtonsMap(self)
            self.led = Led(self)
            self.rumble = Rumble(self)
            self.rumble.setTimeRumble(1) # activates 1 sec rumbling

            # those loops are just for fun, small led animation
            for i in range(1,5):
                self.led.blink(length=0.3, repeat=1, diod=i)

            # turn on led matching the wiimote number
            self.led.switchLed(diod=self.number)

            # activates accelerometer
            self.accelerometer = Accelerometer(self)

            # speaker implementation
            # self.speaker    = Speaker(self)
            
            # listen for data
            self.read()

            # if asked to close connection
            self.close()
            
            if self.get_state() == DISCONNECTED :
                break

        if self.cfg.ON_EXIT_HOOK is not None and self.cfg.ON_EXIT_HOOK != "":
            Popen([self.cfg.ON_EXIT_HOOK], shell=True)

        return

    
    def set_state (self, newState):
        if newState != self.state:
            self.state = newState
            self.logger.info("Change status to: %s" % STATUS[self.state])

            
    def get_state(self):
        return self.state

    
    def connect(self):
        """
        this function is used to establish connection with the wiimote
        return None if cannot be done
        """
        c_sock = BluetoothSocket(L2CAP)
        r_sock = BluetoothSocket(L2CAP)

        try :
            c_sock.connect((self.mac, 0x11)) # 0x11 : control channel
            r_sock.connect((self.mac, 0x13)) # 0x13 : reception channel
            r_sock.settimeout(self.cfg.SOCK_TIMEOUT_DURATION)
        except BluetoothError, be:
            self.logger.error("Failed connecting: %s" % be)
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
        self.logger.info('Gracefully disconnected')

        
    def read(self):
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
                if self.logger.isEnabledFor(logging.DEBUG):
                    self.logger.debug('Frame received: %s' % [ '0x%x' % x for x in frame ] )

                # we need to convert those bytes into readable data
                self.parse (frame)

            except BluetoothError:
                pass


    def parse(self, bytes):
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

            for idx in xrange(2) :
                self.buttons.execute(buttons_bytes[idx], idx)

        # accelerometer handling
        accel_flag = ~MODE_BUTTON & MODE_BUTTON_ACCELEROMETER
        if bytes[1] & accel_flag :
            acceler_bytes = bytes[4:7]            
            self.accelerometer.update(acceler_bytes)

            
    def send(self, frame):
        """
        Send a frame on the signalisation channel
        """
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug('Frame sent: %s' % [ '0x%x' % ord(x) for x in frame ]) 
        
        frame = ''.join(frame)
        self.control_socket.send(frame)

        
    def send_control_frame(self, bytes):
        """
        Prepare a control frame on signalisation channel
        """
        # control frame always start with 0x52
        bytes.insert(0, chr(0x52))
        self.send(bytes)

        
    def change_feature(self, mode):
        """
        Allows to change the Wiimote features.
        """
        # change feature frame starts with 0x52 0x11
        self.logger.info("Switching feature to 0x%x" % mode)
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
        self.logger.info("Switching mode to 0x%x" % mode)
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
            "Accelerometer": self.mode,
            }
            
        status = str(self) + "\n"
        
        for k in stats.keys() :
            if k == "Battery" : v = "%d%%" % stats[k]
            elif stats[k] != 0: v = "On"
            else : v = "Off"
            status += "%16s : %10s\n" % (k,v)
        
        print ("%s" % status)

        
    def write_registers(self, address_bytes, data_bytes):
        """
        Write len(data_bytes) bytes at offset pointed by address_bytes
        """
        bytes = [chr(0x16), chr(0x04)]
        bytes += [ chr(x) for x in address_bytes ]
        bytes.append(chr(len(data_bytes)))
        bytes += [ chr(x) for x in data_bytes ]

        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug("Write %s at %s" % (data_bytes, address_bytes))
        
        self.send_control_frame(bytes)
        
