from subprocess import Popen
from moduleskel import Module

class ButtonsMap (Module):
    """
    This module aims to bind every Wiimote button to a specific action.
    Wiimote has :
    - A & B
    - 1 & 2
    - Minus / Home / Plus 
    - Arrow (up|left|down|right)

    Altogether, 11 buttons must be binded. Their respective actions are to
    be specified in the configuration file.
    """
    
    def __init__(self, wiimote):
        """ Buttons mapping initialization """ 
        Module.__init__(self,wiimote)


    def execute(self, byte_value, byte_number):
        """
        Executes the corresponding to the button :
        - first looks for the right button code
        - then execute matching action
        """

        if not byte_number in range(2):
            logger.error("Byte must be first or second")
            return

        index = 0
        offset  = 1
    
        while index < 0x10 :
            # examining each bit of the 2 first bytes
            action = None
        
            if byte_value & offset :
                action = self.get_action(index, byte_number)

                # button treatment
                # leave properly
                if action == "quit":
                    self.wiimote.close()

                # toggle accelerometer module
                elif action == "accel" :
                    accel_flag = 1 << 0
                    if self.wiimote.mode & accel_flag :
                        self.wiimote.mode &= ~accel_flag
                    else :
                        self.wiimote.mode |= accel_flag

                    self.wiimote.change_mode(self.wiimote.mode)

                # print wiimote stats (battery, modules, etc.)
                elif action == "status" :
                    self.wiimote.request_status()
                
                # otherwise, system call
                elif action is not None and action != 0 :
                    Popen(action, shell=True)
            
            offset <<= 1
            index += 1
        

    def get_action(self, idx, byte_num):
        """
        Match a flag to an action specified in the wiimote configuration.
        """

        try:
            ret = self.wiimote.cfg.keymap[idx][byte_num]
        except Exception , e:
            ret = 0
            self.wiimote.logger.error("Exception was raised on buttons_map (%d,%d): %s"
                                      % (idx,byte_num,e))
            
        return ret
