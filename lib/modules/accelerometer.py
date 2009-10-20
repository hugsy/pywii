"""

Those functions interprets accelerometer movement. It is a bit fuzzy,
but is really coherent after a short moment.
Please see http://wiibrew.org/wiki/Wiimote#Accelerometer for more
details

"""
from config import ACCELEROMETER_ZERO, ACCELEROMETER_PRECISION, ACCEL_ACTION
import logging
from subprocess import call

logging.basicConfig()
logger = logging.getLogger("Wiimote.accelerometer")
logger.setLevel(logging.DEBUG)

def update(bytes):
    """
    Extract positions from frame.
    """
    x = bytes[0]
    y = bytes[1]
    z = bytes[2]

    update_horizon(x)
    update_vertical(y)
    update_depth(z)


def perform_action(move):
    """
    Execute system call corresponding to movement
    """
    if move not in ('up','down','left','right','back','front'):
        logger.error("Unknown movement %s" % move)
        return
    
    if logger.isEnabledFor(logging.DEBUG) :
        logger.debug("%s movement detected" % move)
        
    call(ACCEL_ACTION[move], shell=True)
    
    
def update_horizon(x_pos):
    """
    Detecting horizontal movement
    """
    if x_pos < ACCELEROMETER_ZERO - ACCELEROMETER_PRECISION :
        perform_action('left')
        
    if x_pos > ACCELEROMETER_ZERO + ACCELEROMETER_PRECISION :
        perform_action('right')

        
def update_vertical(y_pos):
    """
    Detecting depth movement
    """
    if y_pos > ACCELEROMETER_ZERO + ACCELEROMETER_PRECISION :
        perform_action('front')
        
    if y_pos < ACCELEROMETER_ZERO - ACCELEROMETER_PRECISION :
        perform_action('back')

            
def update_depth(z_pos):
    """
    Detecting vertical movement
    """
    if z_pos < ACCELEROMETER_ZERO - ACCELEROMETER_PRECISION :
        perform_action('up')
        
    if z_pos > ACCELEROMETER_ZERO + ACCELEROMETER_PRECISION :
        perform_action('down')
