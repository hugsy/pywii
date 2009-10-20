from config import *
import logging
from subprocess import call

logging.basicConfig()
logger = logging.getLogger("Wiimote.buttons")
logger.setLevel(logging.DEBUG)

BUTTON_NULL  = 0x00
BUTTON_A     = 0x01
BUTTON_B     = 0x02
BUTTON_UP    = 0x03
BUTTON_DOWN  = 0x04
BUTTON_LEFT  = 0x05
BUTTON_RIGHT = 0x06
BUTTON_MINUS = 0x07
BUTTON_PLUS  = 0x08
BUTTON_HOME  = 0x09
BUTTON_1     = 0x10
BUTTON_2     = 0x11

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
            if button == BUTTON_HOME :
                wiimote.close()

            elif button == BUTTON_1 :
                accel_flag = 1 << 0
                if wiimote.mode & accel_flag :
                    wiimote.mode &= ~accel_flag
                else :
                    wiimote.mode |= accel_flag

                wiimote.change_mode(wiimote.mode)

            elif button == BUTTON_2 :
                wiimote.request_status()
                
            # si bouton 2 passage en mode camera (mode 0x34)
                
            elif button != BUTTON_NULL :
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
    values[0] = [BUTTON_LEFT, BUTTON_2]
    values[1] = [BUTTON_RIGHT, BUTTON_1]
    values[2] = [BUTTON_DOWN, BUTTON_B]
    values[3] = [BUTTON_UP, BUTTON_A]
    values[4] = [BUTTON_PLUS, BUTTON_MINUS]
    values[5] = [BUTTON_NULL, BUTTON_NULL]
    values[6] = [BUTTON_NULL, BUTTON_NULL]
    values[7] = [BUTTON_NULL, BUTTON_HOME]

    try:
        ret = values[idx][byte_num]
    except Exception , e:
        ret = BUTTON_NULL
        logger.error("Exception was raised on values (%d,%d): %s" % (idx,byte_num,e))
            
    return ret
