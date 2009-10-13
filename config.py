import ConfigParser

cfg = ConfigParser.ConfigParser()
cfg.read('config.ini')

DEBUG = cfg.get("main", "DEBUG")
SLEEP_DURATION = int(cfg.get("main", "SLEEP_DURATION"))
DISCOVER_DURATION = int(cfg.get("main", "DISCOVER_DURATION"))
SOCK_TIMEOUT_DURATION = float(cfg.get("main", "SOCK_TIMEOUT_DURATION"))


# The following buttons MUST NOT BE BINDED
# Used by framework
# BUTTON_HOME -> exit
# BUTTON_1 -> toggle accelerometer mode 
# BUTTON_2 -> toggle camera mode (yet to come)

BUTTON_ACTION = {
    "left": cfg.get("button_action", "BUTTON_ACTION_LEFT"),
    "right": cfg.get("button_action", "BUTTON_ACTION_RIGHT"),
    "up": cfg.get("button_action", "BUTTON_ACTION_UP"),
    "down": cfg.get("button_action", "BUTTON_ACTION_DOWN"),
    "plus": cfg.get("button_action", "BUTTON_ACTION_PLUS"),
    "minus": cfg.get("button_action", "BUTTON_ACTION_MINUS"),
    "A": cfg.get("button_action", "BUTTON_ACTION_A"),
    "B": cfg.get("button_action", "BUTTON_ACTION_B"),
    }

ACCELEROMETER_ZERO = int(cfg.get("accel_config", "ACCELEROMETER_ZERO"))
ACCELEROMETER_PRECISION = int(cfg.get("accel_config", "ACCELEROMETER_PRECISION"))

ACCEL_ACTION = {
    "left": cfg.get("accel_action", "ACCEL_X_LEFT_ACTION"),
    "right": cfg.get("accel_action", "ACCEL_X_RIGHT_ACTION"),
    "up": cfg.get("accel_action", "ACCEL_Y_UP_ACTION"),
    "down": cfg.get("accel_action", "ACCEL_Y_DOWN_ACTION"),
    "front": cfg.get("accel_action", "ACCEL_Z_FRONT_ACTION"),
    "back": cfg.get("accel_action", "ACCEL_Z_BACK_ACTION"),
    }
    
                                        
