import ConfigParser

cfg = ConfigParser.ConfigParser()
cfg.read('config.ini')

DEBUG                   = cfg.getboolean("main", "DEBUG")
DEBUG_LEVEL             = cfg.getint("main", "DEBUG_LEVEL")
SLEEP_DURATION          = cfg.getint("main", "SLEEP_DURATION")
DISCOVER_DURATION       = cfg.getint("main", "DISCOVER_DURATION")
SOCK_TIMEOUT_DURATION   = cfg.getfloat("main", "SOCK_TIMEOUT_DURATION")

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
    BUTTON_LEFT   : cfg.get("button_action", "BUTTON_ACTION_LEFT"),
    BUTTON_RIGHT  : cfg.get("button_action", "BUTTON_ACTION_RIGHT"),
    BUTTON_UP     : cfg.get("button_action", "BUTTON_ACTION_UP"),
    BUTTON_DOWN   : cfg.get("button_action", "BUTTON_ACTION_DOWN"),
    BUTTON_PLUS   : cfg.get("button_action", "BUTTON_ACTION_PLUS"),
    BUTTON_MINUS  : cfg.get("button_action", "BUTTON_ACTION_MINUS"),
    BUTTON_A      : cfg.get("button_action", "BUTTON_ACTION_A"),
    BUTTON_B      : cfg.get("button_action", "BUTTON_ACTION_B"),
    }

ACCELEROMETER_ZERO       = cfg.getint("accel_config", "ACCELEROMETER_ZERO")
ACCELEROMETER_PRECISION  = cfg.getint("accel_config", "ACCELEROMETER_PRECISION")

ACCEL_ACTION = {
    "left"    : cfg.get("accel_action", "ACCEL_X_LEFT_ACTION"),
    "right"   : cfg.get("accel_action", "ACCEL_X_RIGHT_ACTION"),
    "up"      : cfg.get("accel_action", "ACCEL_Y_UP_ACTION"),
    "down"    : cfg.get("accel_action", "ACCEL_Y_DOWN_ACTION"),
    "front"   : cfg.get("accel_action", "ACCEL_Z_FRONT_ACTION"),
    "back"    : cfg.get("accel_action", "ACCEL_Z_BACK_ACTION"),
    }

