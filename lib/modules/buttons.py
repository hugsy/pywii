from config import *
import logging
from subprocess import call


logging.basicConfig()
logger = logging.getLogger("Wiimote.buttons")
logger.setLevel(logging.DEBUG)

def byte_to_button(byte_value , byte_number):
    """
    Get the list of all buttons set
    """

    if not byte_number in (0,1):
        logger.error("Invalid byte range")
        return []

    index = 0
    offset  = 1
    spec_button_list = []
    
    while index < 0x10 :
        # examining each bit of the 2 first bytes
        button = None
        
        if byte_value & offset :
            if logger.isEnabledFor(logging.DEBUG) :
                logger.info("flag 0x%x up on byte %d at index 0x%x"%(offset,
                                                                     byte_number,
                                                                     index))
            button = assign_flag_to_button(index, byte_number)
            if logger.isEnabledFor(logging.DEBUG) :
                logger.debug('Button flags:' + button )
                
            if button in ("1", "2", "home"):
                spec_button_list.append(button)
            elif button != '':
                call(BUTTON_ACTION[button], shell=True)
            
        offset <<= 1
        index += 1
        
    return spec_button_list

def assign_flag_to_button (idx, byte_num):
    """
    Match a flag to corresponding button. Makes it human readable.
    Could be deleted in next versions.
    """
    # bit/buttons matching table
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
