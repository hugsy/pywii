from binascii import hexlify
from threading import Thread 
from bluetooth.bluez import BluetoothSocket, BluetoothError, L2CAP

import lib.handlers.buttons
import lib.handlers.accelerometer
from config import *


class Wiimote(Thread):
    """
    this object manages all wiimote interactions. 
    """
    
    def __init__ (self, mac, name, number):
        Thread.__init__(self)
        self.mac = mac
        self.name = name
        self.state  = 0
        self.receive_socket = None
        self.control_socket = None
        self.number = number

        # accelerometer information
        self.x = 0
        self.y = 0
        self.z = 0

    def __str__(self):
        desc = "Description of Wiimote-%d: \n" % self.number
        desc += "\tMac address: %s\n" % self.mac
        desc += "\tName: %s\n" % self.name
        desc += "\tState: %s\n" % STATUS[self.state]
        desc += "\n"
        return desc
        
    def run(self):
        """
        thread main program
        """
        if DEBUG : print "[!] Starting Wiimote-%d" % self.number
        self.receive_socket, self.control_socket = self.establish_connection()
        if self.receive_socket is None or self.control_socket is None : 
            # if establishing connection fails
            if DEBUG : print "[-] Failed to establish connection"
            self.change_state_notification(DISCONNECTED)
            return
        self.change_state_notification(CONNECTED)
        self.change_feature( 1 + 2**(3+self.number) )
        time.sleep(1)
        self.change_feature( 2**(3+self.number) )
        self.transmit_data()

    def change_state_notification(self, new_state):
        if new_state != self.state:
            self.state = new_state
            print "[!] Changing Wii-%d status to : %s" % (self.number, STATUS[status])
        
    def establish_connection (self):
        """
        this function is used to establish_connection with the wiimote
        return None if cannot be done
        """
        c_sock = BluetoothSocket(L2CAP)
        r_sock = BluetoothSocket(L2CAP)

        
        try :
            print "socket created"
            c_sock.connect((self.mac, 0x11))
            print "c_sock ok"
            r_sock.connect((self.mac, 0x13))
            print "r_sock ok"


            r_sock.settimeout(SOCK_TIMEOUT_DURATION)
        except BluetoothError, be:
            print "[-] Wii-%d failed connecting : %s " % (self.number, be)
            c_sock.close()
            r_sock.close()
            c_sock = None            
            r_sock = None

        return (r_sock, c_sock)
    
        
    def transmit_data(self):
        """
        this function reads data to the wiimote and interprets every frame
        """
        print "in transmit_data"
        while self.state == CONNECTED :
            try:
                raw_data = self.receive_socket.recv(23)
                frame = [ ]
                chaine = ''
                
                if len(raw_data):
                    for raw_byte in raw_data:
                        hex_value = hexlify(raw_byte)
                        int_value = ord(raw_byte)
                        frame.append(int_value)
                        chaine += '0x'+hex_value+' '

                    # let's make it raw 
                    if len(chaine) and DEBUG : print chaine

                    # we need to convert those bytes into readable data
                    list_buttons = self.interpret_frame(frame)

                    # assigning each button to a specific action
                    for button in list_buttons :
                        if button == "home" :
                            self.close_connection()
                        if button == "1" :
                            self.change_mode(MODE_BUTTON_ACCELEROMETER)
                        if button == "2" :
                            self.change_mode(MODE_BUTTON)

            except BluetoothError, be :
                print "[!] Exception raised %s" % str(be)
                pass
            
        return

    def close_connection(self):
        if DEBUG : print "[!] Trying to gracefully shutdown"
        self.receive_socket.close()
        self.control_socket.close()
        self.change_state_notification(DISCONNECTED)        
        print "[+] Wii-%d : Gracefully disconnected" % self.number

    def interpret_frame (self, list_bytes):
        # checking if we handle the suggested mode
        if not list_bytes[1] in (MODE_BUTTON,
                                 MODE_BUTTON_ACCELEROMETER):
            return []
        
        buttons_bytes = list_bytes[2:4]
        acceler_bytes = list_bytes[4:7]
        table = [ ]

        for idx in range(0,2) :
            # button analysis
            buttons_list = buttons.byte_to_button(buttons_bytes[idx], idx)
            table += buttons_list 

        if list_bytes[1] == MODE_BUTTON_ACCELEROMETER :
            # accelerometer handling
            accelerometer.update_position(acceler_bytes)
            
        if DEBUG : print table
        return table

    def send_control_frame(self, byte_table):
        # control frame always start with \x52
        frame = chr(0x52)

        for byte in byte_table:
            frame += byte

        self.control_socket.send(frame)

    def change_feature(self, mode):
        # change feature frame starts with \x52\x11
        print "[+] Wii-%d : Switching feature to %x" % (self.number,
                                                        mode)
        features_hexa = chr(0x11)
        mode_hexa = chr(mode)
        hexa_table = (features_hexa, mode_hexa)
        self.send_control_frame(hexa_table)

    def change_mode(self, mode, persist_data=False):
        # change mode frame start with \x52\x12
        print "[+] Wii-%d : Switching mode to %s" % (self.number,
                                                     hex(mode))
        mode_byte = chr(0x12)

        if persist_data :
            byte_mode_1=chr(0x04)
        else :
            byte_mode_1=chr(0x00)

        byte_mode_2 = chr(mode)

        byte_table = (mode_byte, byte_mode_1, byte_mode_2)
        self.send_control_frame(byte_table)
