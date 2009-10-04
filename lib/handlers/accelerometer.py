from config import DEBUG
from os import system

ACCELEROMETER_ZERO = 0x80
ACCELEROMETER_PRECISION = 0x20

ACTION_HORIZ_LEFT  = "/usr/bin/xmms --rew"
ACTION_HORIZ_RIGHT = "/usr/bin/xmms --fwd"
ACTION_VERT_UP     = "echo VERT_UP > /dev/null"
ACTION_VERT_DOWN   = "echo VERT_DOWN > /dev/null"
ACTION_DEPTH_FRONT = "echo DEPTH_FRONT > /dev/null"
ACTION_DEPTH_BACK  = "echo DEPTH_BACK > /dev/null"

def update_position(list_bytes):
    x = list_bytes[0]
    y = list_bytes[1]
    z = list_bytes[2]

#     detecting horizontal movement
    if x < ACCELEROMETER_ZERO - ACCELEROMETER_PRECISION :
        if DEBUG : print "Horizontal (left) movement detected"
        system(ACTION_HORIZ_LEFT)
        
    if x > ACCELEROMETER_ZERO + ACCELEROMETER_PRECISION :
        if DEBUG : print "Horizontal (right) movement detected"
        system(ACTION_HORIZ_RIGHT)
        
#     detecting depth movement
    if y > ACCELEROMETER_ZERO + ACCELEROMETER_PRECISION :
        if DEBUG : print "Vertical (front) movement detected"
        
    if y < ACCELEROMETER_ZERO - ACCELEROMETER_PRECISION :
        if DEBUG : print "Vertical (back) movement detected"        
#         system(ACTION_DEPTH_BACK)

#     detecting vertical movement
    if z < ACCELEROMETER_ZERO - ACCELEROMETER_PRECISION :
        if DEBUG : print "Depth (up) movement detected"
#         system(ACTION_VERT_UP)

    if z > ACCELEROMETER_ZERO + ACCELEROMETER_PRECISION :
        if DEBUG : print "Depth (down) movement detected"
#         system(ACTION_VERT_DOWN)
