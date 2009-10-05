from config import *
import logging
from subprocess import call


logging.basicConfig()
logger = logging.getLogger("Wiimote.accelerometer")
logger.setLevel(logging.DEBUG)

def update_position(list_bytes):
    x = list_bytes[0]
    y = list_bytes[1]
    z = list_bytes[2]

    update_horizon(x)
    update_vertical(y)
    update_depth(z)

    
def update_horizon(x_pos):
    # detecting horizontal movement
    if x_pos < ACCELEROMETER_ZERO - ACCELEROMETER_PRECISION :
        if logger.isEnabledFor(logging.DEBUG) :
            logger.debug("Horizontal (left) movement detected")
        call(ACCEL_X_LEFT_ACTION, shell=True)
        
    if x_pos > ACCELEROMETER_ZERO + ACCELEROMETER_PRECISION :
        if logger.isEnabledFor(logging.DEBUG) :
            logger.debug("Horizontal (right) movement detected")
        call(ACCEL_X_RIGHT_ACTION, shell=True)

        
def update_vertical(y_pos):        
    ## detecting depth movement
    if y_pos > ACCELEROMETER_ZERO + ACCELEROMETER_PRECISION :
        if logger.isEnabledFor(logging.DEBUG) :        
            logger.debug("Vertical (front) movement detected")
        # call(ACCEL_Z_FRONT_ACTION, shell=True)
        
    if y_pos < ACCELEROMETER_ZERO - ACCELEROMETER_PRECISION :
        if logger.isEnabledFor(logging.DEBUG) :        
            logger.debug("Vertical (back) movement detected")        
        # call(ACCEL_Z_BACK_ACTION, shell=True)

            
def update_depth(z_pos):
    ## detecting vertical movement
    if z_pos < ACCELEROMETER_ZERO - ACCELEROMETER_PRECISION :
        if logger.isEnabledFor(logging.DEBUG) :        
            logger.debug("Depth (up) movement detected")
        # call(ACCEL_Y_UP_ACTION, shell=True)

    if z_pos > ACCELEROMETER_ZERO + ACCELEROMETER_PRECISION :
        if logger.isEnabledFor(logging.DEBUG) :        
            logger.debug("Depth (down) movement detected")
        # call(ACCEL_Y_DOWN_ACTION, shell=True)
