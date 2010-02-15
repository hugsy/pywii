"""Configuration parser"""

import ConfigParser

CFG = ConfigParser.ConfigParser()
CFG.read('config.ini')

DEBUG                   = CFG.getboolean("main", "DEBUG")
DEBUG_LEVEL             = CFG.getint("main", "DEBUG_LEVEL")
SLEEP_DURATION          = CFG.getint("main", "SLEEP_DURATION")
DISCOVER_DURATION       = CFG.getint("main", "DISCOVER_DURATION")
SOCK_TIMEOUT_DURATION   = CFG.getfloat("main", "SOCK_TIMEOUT_DURATION")
DAEMONIZE               = CFG.getboolean("main", "DAEMONIZE")

# buttons configuration
BUTTON_NULL             = 0x00
BUTTON_A                = 0x01
BUTTON_B                = 0x02
BUTTON_UP               = 0x03
BUTTON_DOWN             = 0x04
BUTTON_LEFT             = 0x05
BUTTON_RIGHT            = 0x06
BUTTON_MINUS            = 0x07
BUTTON_PLUS             = 0x08
BUTTON_HOME             = 0x09
BUTTON_1                = 0x10
BUTTON_2                = 0x11

BUTTON_ACTION = {
    BUTTON_LEFT   : CFG.get("button_action", "BUTTON_ACTION_LEFT"),
    BUTTON_RIGHT  : CFG.get("button_action", "BUTTON_ACTION_RIGHT"),
    BUTTON_UP     : CFG.get("button_action", "BUTTON_ACTION_UP"),
    BUTTON_DOWN   : CFG.get("button_action", "BUTTON_ACTION_DOWN"),
    BUTTON_PLUS   : CFG.get("button_action", "BUTTON_ACTION_PLUS"),
    BUTTON_MINUS  : CFG.get("button_action", "BUTTON_ACTION_MINUS"),
    BUTTON_A      : CFG.get("button_action", "BUTTON_ACTION_A"),
    BUTTON_B      : CFG.get("button_action", "BUTTON_ACTION_B"),
    }

# accelerometer configuration
ACCELEROMETER_ZERO       = CFG.getint("accel_config", "ACCELEROMETER_ZERO")
ACCELEROMETER_PRECISION  = CFG.getint("accel_config", "ACCELEROMETER_PRECISION")

ACCEL_ACTION = {
    "left"    : CFG.get("accel_action", "ACCEL_X_LEFT_ACTION"),
    "right"   : CFG.get("accel_action", "ACCEL_X_RIGHT_ACTION"),
    "up"      : CFG.get("accel_action", "ACCEL_Y_UP_ACTION"),
    "down"    : CFG.get("accel_action", "ACCEL_Y_DOWN_ACTION"),
    "front"   : CFG.get("accel_action", "ACCEL_Z_FRONT_ACTION"),
    "back"    : CFG.get("accel_action", "ACCEL_Z_BACK_ACTION"),
    }

