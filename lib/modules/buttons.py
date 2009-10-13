from config import *
import logging
from subprocess import call

logging.basicConfig()
logger = logging.getLogger("Wiimote.buttons")
logger.setLevel(logging.DEBUG)

def execute(byte_value, byte_number, wiimote):
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
        button = None
        
        if byte_value & offset :
            if logger.isEnabledFor(logging.DEBUG) :
                logger.info("flag 0x%x on %d at 0x%x"%(offset,
                                                       byte_number,
                                                       index))
            button = get_button(index, byte_number)
            if logger.isEnabledFor(logging.DEBUG) :
                logger.debug('Button flags:' + button)

            # button treatment
            ## special buttons for management
            if button == "home" :
                wiimote.close()

            elif button == "1" :
                accel_flag = 1 << 0
                if wiimote.mode & accel_flag :
                    wiimote.mode &= ~accel_flag
                else :
                    wiimote.mode |= accel_flag

                wiimote.change_mode(wiimote.mode)

            elif button == "2" :
                wiimote.request_status()
                
            # elif button == "2" :
                # en prevision de la camera (mode 0x34)
                
            elif button != '':
                call(BUTTON_ACTION[button], shell=True)
            
        offset <<= 1
        index += 1
        

def get_button(idx, byte_num):
    """
    Match a flag to corresponding button. Makes it human readable.
    Could be deleted in next versions.
    See http://wiibrew.org/wiki/Wiimote#Core_Buttons
    """
    values = range(0,8)
    values[0] = ["left", "2"]
    values[1] = ["right", "1"]
    values[2] = ["down", "B"]
    values[3] = ["up", "A"]
    values[4] = ["plus", "minus"]
    values[5] = ["", ""]
    values[6] = ["", ""]
    values[7] = ["n/a", "home"]

    try:
        ret = values[idx][byte_num]
    except Exception , e:
        ret = "n/a"
        logger.error("Exception was raised on values (%d,%d): %s" % (idx,byte_num,e))
            
    return ret
